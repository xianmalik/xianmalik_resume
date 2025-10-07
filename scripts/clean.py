#!/usr/bin/env python3

import os
import glob


def find_files(patterns):
    for pattern in patterns:
        for path in glob.glob(pattern):
            if os.path.isfile(path):
                yield path


def main() -> int:
    print("")
    print("🧹 Cleaning LaTeX auxiliary files...")

    extensions = [
        "aux",
        "bcf",
        "log",
        "run.xml",
        "bbl",
        "blg",
        "fdb_latexmk",
        "fls",
        "toc",
        "out",
        "nav",
        "snm",
        "synctex.gz",
        "xdv",
    ]

    total_removed = 0

    # Output directory
    if os.path.isdir("output"):
        for ext in extensions:
            matches = list(find_files([os.path.join("output", f"*.{ext}")]))
            if matches:
                print(f"  🗑️  Removing {len(matches)} .{ext} file(s)")
                for m in matches:
                    try:
                        os.remove(m)
                        total_removed += 1
                    except OSError:
                        pass

    # Root directory
    for ext in extensions:
        matches = list(find_files([f"*.{ext}"]))
        if matches:
            print(f"  🗑️  Removing {len(matches)} .{ext} file(s) from root")
            for m in matches:
                try:
                    os.remove(m)
                    total_removed += 1
                except OSError:
                    pass

    if total_removed == 0:
        print("✨ No auxiliary files found - already clean!")
    else:
        print(f"✅ Cleaned up {total_removed} auxiliary file(s)")

    if os.path.isdir("output"):
        print("")
        print("📂 Remaining files in output/:")
        for name in sorted(os.listdir("output")):
            try:
                path = os.path.join("output", name)
                size = os.path.getsize(path)
                print(f"   {name}  {size} bytes")
            except OSError:
                print(f"   {name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


