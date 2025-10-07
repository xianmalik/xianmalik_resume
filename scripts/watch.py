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
    print("🔍 Watching for changes in .tex/.cls, data/*.yml, and scripts/generate.py...")
    print("📝 Will automatically rebuild when files are saved")
    print("⏹️  Press Ctrl+C to stop watching")
    print("")

    if shutil.which("fswatch") is None:
        print(f"❌ fswatch is not installed. Please install it with:\n   brew install fswatch")
        return 1

    def run_build() -> None:
        print("")
        print(f"🔄 [{subprocess.check_output(['date', '+%H:%M:%S']).decode().strip()}] File changed, rebuilding...")
        subprocess.run([sys.executable or "python3", "scripts/build.py"], check=False)
        print("")

    print("🚀 Running initial build...")
    subprocess.run([sys.executable or "python3", "scripts/build.py"], check=False)
    print("")

    # Build fswatch command
    cmd = [
        "fswatch", "-o",
        "-e", ".*",
        "-i", ".*\\.tex$",
        "-i", ".*\\.cls$",
        "-i", ".*/data/.*\\.yml$",
        "-i", ".*/scripts/generate\\.py$",
        ".", "data", "scripts/generate.py",
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


