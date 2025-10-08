#!/usr/bin/env python3

import os
import sys
import shutil
import subprocess


BLUE = "\033[0;34m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
WHITE = "\033[1;37m"
NC = "\033[0m"


def main() -> int:
    if shutil.which("fswatch") is None:
        print(f"❌ fswatch is not installed. Please install it with:\n   brew install fswatch")
        return 1

    def run_build() -> None:
        print("")
        print(f"🔄 [{subprocess.check_output(['date', '+%H:%M:%S']).decode().strip()}] File changed, rebuilding...")
        subprocess.run(
            [sys.executable or "python3", "scripts/build.py"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"{GREEN}✓ Done{NC}")
        print("")

    print("🚀 Running initial build...")
    subprocess.run(
        [sys.executable or "python3", "scripts/build.py"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("")

    # Show watch information AFTER initial build completes
    print("🔍 Watching: resume.tex, xianmalik.cls, and data/*.yml ...")
    print("📝 Will automatically rebuild when files are saved")
    print("⏹️  Press Ctrl+C to stop watching")
    print("")

    # Build fswatch command
    cmd = [
        "fswatch", "-o",
        "-e", ".*",
        # Only include these
        "-i", ".*/resume\\.tex$",
        "-i", ".*/xianmalik\\.cls$",
        "-i", ".*/data/.*\\.yml$",
        # Watch only these paths
        "resume.tex", "xianmalik.cls", "data",
    ]

    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
        try:
            for _ in proc.stdout:  # each event triggers a build
                run_build()
        except KeyboardInterrupt:
            proc.terminate()
            proc.wait()
            print("👋 Stopped watching.")
            return 0
        finally:
            if proc.poll() is None:
                proc.terminate()
    return 0


if __name__ == "__main__":
    sys.exit(main())


