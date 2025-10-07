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


def print_banner() -> None:
    print(f"{CYAN}╭─────────────────────────────────────────────────────────────────────╮{NC}")
    print(f"{CYAN}│{WHITE} XeLaTeX CV Builder                                                  {CYAN}│{NC}")
    print(f"{CYAN}│                                                                     │{NC}")
    print(f"{CYAN}│{YELLOW} Compiling: {GREEN}resume.tex{WHITE} → {GREEN}output/resume.pdf                           {CYAN}│{NC}")
    print(f"{CYAN}│{YELLOW} Engine: {BLUE}XeLaTeX{WHITE}                                                     {CYAN}│{NC}")
    print(f"{CYAN}│{YELLOW} Postbuild: {GRAY}Auto cleanup of auxiliary files after successful build   {CYAN}│{NC}")
    print(f"{CYAN}│                                                                     │{NC}")
    print(f"{CYAN}│{YELLOW} Usage: {GREEN}./scripts/build.py{WHITE}                                           {CYAN}│{NC}")
    print(f"{CYAN}│{YELLOW} Author: {PURPLE}@xianmalik{WHITE}                                                  {CYAN}│{NC}")
    print(f"{CYAN}╰─────────────────────────────────────────────────────────────────────╯{NC}")
    print("")


def ensure_output_dir() -> None:
    os.makedirs("output", exist_ok=True)


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

    print(f"{YELLOW}Generating TeX from YAML...{NC}")
    try:
        subprocess.run(["python3", generate_script], check=True)
    except subprocess.CalledProcessError:
        print(f"{RED}Data generation failed.{NC}")
        sys.exit(1)


def show_spinner(process: subprocess.Popen) -> None:
    spinner_chars = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    i = 0
    sys.stdout.write(f"{YELLOW}Compiling:  {NC}")
    sys.stdout.flush()
    while process.poll() is None:
        sys.stdout.write(f"\b{GREEN}{spinner_chars[i]}{NC}")
        sys.stdout.flush()
        i = (i + 1) % len(spinner_chars)
        time.sleep(0.1)
    sys.stdout.write(f"\b{GREEN}Done!{NC}\n")
    sys.stdout.flush()


def compile_xelatex() -> int:
    print(f"{YELLOW}Starting XeLaTeX compilation...{NC}")
    # Run xelatex in output directory, capture output to resume.log
    log_path = os.path.join("output", "resume.log")
    with open(log_path, "w") as log_file:
        process = subprocess.Popen(
            [
                "xelatex",
                "-interaction=nonstopmode",
                "-output-directory=output",
                "resume.tex",
            ],
            stdout=log_file,
            stderr=subprocess.STDOUT,
        )

        spinner_thread = threading.Thread(target=show_spinner, args=(process,), daemon=True)
        spinner_thread.start()
        process.wait()
        spinner_thread.join()
        return process.returncode or 0


def cleanup_aux_files() -> None:
    print(f"{YELLOW}Cleaning up auxiliary files...{NC}")
    patterns = [
        os.path.join("output", "*.aux"),
        os.path.join("output", "*.log"),
        os.path.join("output", "*.out"),
        os.path.join("output", "*.fls"),
        os.path.join("output", "*.fdb_latexmk"),
    ]
    for pattern in patterns:
        for path in glob.glob(pattern):
            try:
                os.remove(path)
            except OSError:
                pass
    print(f"{GREEN}✓ Cleanup completed{NC}")


def main() -> int:
    print_banner()
    ensure_output_dir()
    generate_from_yaml_if_possible()

    exit_code = compile_xelatex()
    pdf_path = os.path.join("output", "resume.pdf")

    if exit_code == 0 and os.path.isfile(pdf_path):
        print(f"{GREEN}✓ CV compiled successfully to: 📄{WHITE}{pdf_path}{NC}")
        cleanup_aux_files()
        return 0
    else:
        print(f"{RED}✗ Compilation failed{NC}")
        print(f"{GRAY}Check output/resume.log for details{NC}")
        return 1


if __name__ == "__main__":
    sys.exit(main())


