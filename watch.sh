#!/bin/bash

# File watcher script for automatic CV builds
# Watches for changes in .tex and .cls files and triggers build

echo "🔍 Watching for changes in .tex and .cls files..."
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
    ./build.sh
    echo ""
}

# Initial build
echo "🚀 Running initial build..."
./build.sh
echo ""

# Watch for changes in .tex and .cls files
fswatch -o -e ".*" -i "\\.tex$" -i "\\.cls$" . | while read f; do
    build_cv
done