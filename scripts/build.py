#!/usr/bin/env python3

import os
import sys
import glob
import time
import shutil
import subprocess
import threading


# Color definitions (ANSI)
CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
BLUE = "\033[0;34m"
PURPLE = "\033[0;35m"
RED = "\033[0;31m"
WHITE = "\033[1;37m"
GRAY = "\033[0;37m"
NC = "\033[0m"  # No Color
BOLD = "\033[1m"
# 256-color orange (falls back gracefully if unsupported)
ORANGE = "\033[38;5;208m"


def print_banner() -> None:
    print(f"{CYAN}╭─────────────────────────────────────────────────────────────────────╮{NC}")
    print(f"{CYAN}│{WHITE} XeLaTeX CV Builder                                                  {CYAN}│{NC}")
    print(f"{CYAN}│                                                                     │{NC}")
    print(f"{CYAN}│{YELLOW} Compiling: {GREEN}resume.tex{WHITE} → {GREEN}dist/resume.pdf                             {CYAN}│{NC}")
    print(f"{CYAN}│{YELLOW} Engine: {BLUE}XeLaTeX{WHITE}                                                     {CYAN}│{NC}")
    print(f"{CYAN}│{YELLOW} Postbuild: {GRAY}Auto cleanup of auxiliary files after successful build   {CYAN}│{NC}")
    print(f"{CYAN}│                                                                     │{NC}")
    print(f"{CYAN}│{YELLOW} Usage: {GREEN}./scripts/build.py{WHITE}                                           {CYAN}│{NC}")
    print(f"{CYAN}│{YELLOW} Author: {PURPLE}@xianmalik{WHITE}                                                  {CYAN}│{NC}")
    print(f"{CYAN}╰─────────────────────────────────────────────────────────────────────╯{NC}")
    print("")


def ensure_output_dir() -> None:
    os.makedirs("dist", exist_ok=True)


def check_command_exists(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def generate_from_yaml_if_possible() -> None:
    # Mirrors the bash behavior: if python3 exists and generate.py is present,
    # ensure PyYAML is installed and data/*.yml exists, then run the generator.
    if not check_command_exists("python3"):
        return

    generate_script = os.path.join("scripts", "generate.py")
    if not os.path.isfile(generate_script):
        return

    # Verify PyYAML
    try:
        import yaml  # noqa: F401
    except Exception:
        print(f"{RED}PyYAML not installed.{NC} Install with: {YELLOW}python3 -m pip install -r requirements.txt{NC}")
        sys.exit(1)

    # Verify data directory exists with at least one .yml
    if not os.path.isdir("data") or len(glob.glob(os.path.join("data", "*.yml"))) == 0:
        print(f"{RED}No YAML data found in {WHITE}data/{NC}. Add files like {WHITE}data/summary.yml{NC}.")
        sys.exit(1)

    try:
        subprocess.run(["python3", generate_script], check=True)
    except subprocess.CalledProcessError:
        print(f"{RED}Data generation failed.{NC}")
        sys.exit(1)


def run_step_with_spinner(title: str, work_fn, color: str = GREEN) -> any:
    """Run a step showing a spinner (yellow) and finalize with a green checkmark.

    The provided work_fn is executed in a background thread; its return value
    is returned to the caller after completion.
    """
    spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    result_container = {"value": None, "error": None}

    def _runner():
        try:
            result_container["value"] = work_fn()
        except BaseException as exc:  # propagate later
            result_container["error"] = exc

    thread = threading.Thread(target=_runner, daemon=True)
    thread.start()

    i = 0
    # initial line
    sys.stdout.write(f"{color}{spinner_chars[i]} {title}{NC}")
    sys.stdout.flush()
    i = (i + 1) % len(spinner_chars)
    while thread.is_alive():
        time.sleep(0.1)
        sys.stdout.write(f"\r{color}{spinner_chars[i]} {title}{NC}")
        sys.stdout.flush()
        i = (i + 1) % len(spinner_chars)
    thread.join()

    if result_container["error"] is not None:
        # keep the line, but move to new line with error
        sys.stdout.write("\r")
        sys.stdout.flush()
        raise result_container["error"]

    # Replace spinner with a green checkmark on the same line
    sys.stdout.write(f"\r{color}✓ {title}{NC} {BOLD}{WHITE}DONE!{NC}\n")
    sys.stdout.flush()
    return result_container["value"]


def compile_xelatex() -> int:
    # Run xelatex in dist directory, capture output to resume.log
    log_path = os.path.join("dist", "resume.log")
    with open(log_path, "w") as log_file:
        process = subprocess.Popen(
            [
                "xelatex",
                "-interaction=nonstopmode",
                "-output-directory=dist",
                "resume.tex",
            ],
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )

        # Wait for completion
        process.wait()
        return process.returncode or 0


def cleanup_aux_files() -> None:
    patterns = [
        os.path.join("dist", "*.aux"),
        os.path.join("dist", "*.log"),
        os.path.join("dist", "*.out"),
        os.path.join("dist", "*.fls"),
        os.path.join("dist", "*.fdb_latexmk"),
    ]
    for pattern in patterns:
        for path in glob.glob(pattern):
            try:
                os.remove(path)
            except OSError:
                pass


def main() -> int:
    print_banner()
    ensure_output_dir()
    # Step 1: Generate TeX from YAML (if possible)
    def _maybe_generate():
        generate_from_yaml_if_possible()
    run_step_with_spinner("Generating TeX from YAML...", _maybe_generate, color=GREEN)

    # Step 2: Starting XeLaTeX
    def _start_xelatex() -> subprocess.Popen:
        # Start and immediately return; the next step will wait
        log_path_local = os.path.join("dist", "resume.log")
        with open(log_path_local, "w") as log_file_local:
            proc = subprocess.Popen(
                [
                    "xelatex",
                    "-interaction=nonstopmode",
                    "-output-directory=dist",
                    "resume.tex",
                ],
                stdout=log_file_local,
                stderr=subprocess.STDOUT,
            )
        return proc

    process = run_step_with_spinner("Starting XeLaTeX...", _start_xelatex, color=GREEN)

    # Step 3: Compiling...
    def _wait_compile() -> int:
        return process.wait() or 0

    run_step_with_spinner("Compiling...", _wait_compile, color=GREEN)
    exit_code = process.returncode or 0
    pdf_path = os.path.join("dist", "resume.pdf")

    if exit_code == 0 and os.path.isfile(pdf_path):
        # Step 4: Cleaning up aux files (delegate to scripts/clean.py)
        def _clean():
            subprocess.run(
                [sys.executable or "python3", "scripts/clean.py"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        run_step_with_spinner("Cleaning up auxiliary files...", _clean, color=GREEN)
        print("")
        print(f"{GREEN}✓ CV compiled successfully to: 📄{WHITE}{pdf_path}{NC}")
        print("")
        return 0
    else:
        print(f"{RED}✗ Compilation failed{NC}")
        print(f"{GRAY}Check dist/resume.log for details{NC}")
        return 1


if __name__ == "__main__":
    sys.exit(main())


