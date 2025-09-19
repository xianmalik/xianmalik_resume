#!/bin/bash

# Cleanup script for LaTeX auxiliary files
# Removes all build artifacts except the final PDF

echo "🧹 Cleaning LaTeX auxiliary files..."

# LaTeX auxiliary file extensions to remove
EXTENSIONS=(
    "aux"
    "bcf"
    "log"
    "run.xml"
    "bbl"
    "blg"
    "fdb_latexmk"
    "fls"
    "toc"
    "out"
    "nav"
    "snm"
    "synctex.gz"
    "xdv"
)

# Count files before cleanup
total_removed=0

# Remove auxiliary files from output directory
if [ -d "output" ]; then
    for ext in "${EXTENSIONS[@]}"; do
        files_found=$(find output -name "*.${ext}" -type f | wc -l | tr -d ' ')
        if [ "$files_found" -gt 0 ]; then
            echo "  🗑️  Removing ${files_found} .${ext} file(s)"
            find output -name "*.${ext}" -type f -delete
            total_removed=$((total_removed + files_found))
        fi
    done
fi

# Remove auxiliary files from root directory (in case they were generated there)
for ext in "${EXTENSIONS[@]}"; do
    files_found=$(find . -maxdepth 1 -name "*.${ext}" -type f | wc -l | tr -d ' ')
    if [ "$files_found" -gt 0 ]; then
        echo "  🗑️  Removing ${files_found} .${ext} file(s) from root"
        find . -maxdepth 1 -name "*.${ext}" -type f -delete
        total_removed=$((total_removed + files_found))
    fi
done

if [ "$total_removed" -eq 0 ]; then
    echo "✨ No auxiliary files found - already clean!"
else
    echo "✅ Cleaned up ${total_removed} auxiliary file(s)"
fi

# Show remaining files in output directory
if [ -d "output" ]; then
    echo ""
    echo "📂 Remaining files in output/:"
    ls -la output/ | grep -v "^total" | while read line; do
        echo "   $line"
    done
fi