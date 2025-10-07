#!/bin/bash

# File watcher script for automatic CV builds
# Watches for changes in .tex/.cls, YAML data files, and generator script

echo "🔍 Watching for changes in .tex/.cls, data/*.yml, and scripts/generate.py..."
echo "📝 Will automatically rebuild when files are saved"
echo "⏹️  Press Ctrl+C to stop watching"
echo ""

# Check if fswatch is installed
if ! command -v fswatch &> /dev/null; then
    echo "❌ fswatch is not installed. Please install it with:"
    echo "   brew install fswatch"
    exit 1
fi

# Function to build with timestamp
build_cv() {
    echo ""
    echo "🔄 [$(date '+%H:%M:%S')] File changed, rebuilding..."
    python3 scripts/build.py
    echo ""
}

# Initial build
echo "🚀 Running initial build..."
python3 scripts/build.py
echo ""`

# Watch for changes
fswatch -o \
    -e ".*" \
    -i ".*\\.tex$" \
    -i ".*\\.cls$" \
    -i ".*/data/.*\\.yml$" \
    -i ".*/scripts/generate\\.py$" \
    . data scripts/generate.py | while read f; do
    build_cv
done