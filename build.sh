#!/bin/bash

# Build script for XeLaTeX CV
# Compiles resume.tex to PDF

echo "Building CV..."

# Create output directory if it doesn't exist
mkdir -p output

xelatex -interaction=nonstopmode -output-directory=output resume.tex

# Check if PDF was generated successfully
if [ -f "output/resume.pdf" ]; then
    echo "✓ CV compiled successfully to output/resume.pdf"
else
    echo "✗ Compilation failed - PDF not generated"
    exit 1
fi