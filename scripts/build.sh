#!/bin/bash

# Build script for XeLaTeX CV
# Compiles resume.tex to PDF

# Color definitions
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
RED='\033[0;31m'
WHITE='\033[1;37m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}╭─────────────────────────────────────────────────────────────────────╮${NC}"
echo -e "${CYAN}│${WHITE} XeLaTeX CV Builder                                                  ${CYAN}│${NC}"
echo -e "${CYAN}│                                                                     │${NC}"
echo -e "${CYAN}│${YELLOW} Compiling: ${GREEN}resume.tex${WHITE} → ${GREEN}output/resume.pdf                           ${CYAN}│${NC}"
echo -e "${CYAN}│${YELLOW} Engine: ${BLUE}XeLaTeX${WHITE}                                                     ${CYAN}│${NC}"
echo -e "${CYAN}│${YELLOW} Postbuild: ${GRAY}Auto cleanup of auxiliary files after successful build   ${CYAN}│${NC}"
echo -e "${CYAN}│                                                                     │${NC}"
echo -e "${CYAN}│${YELLOW} Usage: ${GREEN}./build.sh${WHITE}                                                   ${CYAN}│${NC}"
echo -e "${CYAN}│${YELLOW} Author: ${PURPLE}@xianmalik${WHITE}                                                  ${CYAN}│${NC}"
echo -e "${CYAN}╰─────────────────────────────────────────────────────────────────────╯${NC}"
echo ""

# Create output directory if it doesn't exist
mkdir -p output

# Function to show spinner while compilation runs
show_spinner() {
    local pid=$1
    local spinner_chars="⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"
    local i=0

    echo -ne "${YELLOW}Compiling: ${NC}"
    while kill -0 $pid 2>/dev/null; do
        printf "\b${GREEN}%s${NC}" "${spinner_chars:$i:1}"
        i=$(( (i + 1) % ${#spinner_chars} ))
        sleep 0.1
    done
    printf "\b${GREEN}Done!${NC}\n"
}

# Optional: generate TeX from YAML (no-op if Python or data missing)
if command -v python3 >/dev/null 2>&1; then
  if [ -f "scripts/generate.py" ]; then
    # Verify PyYAML
    if ! python3 -c "import yaml" >/dev/null 2>&1; then
      echo -e "${RED}PyYAML not installed.${NC} Install with: ${YELLOW}python3 -m pip install -r requirements.txt${NC}"
      exit 1
    fi
    # Verify data directory exists with at least one yml
    if [ ! -d "data" ] || ! ls data/*.yml >/dev/null 2>&1; then
      echo -e "${RED}No YAML data found in ${WHITE}data/${NC}. Add files like ${WHITE}data/summary.yml${NC}."
      exit 1
    fi
    echo -e "${YELLOW}Generating TeX from YAML...${NC}"
    if ! python3 scripts/generate.py; then
      echo -e "${RED}Data generation failed.${NC}"
      exit 1
    fi
  fi
fi

# Start compilation in background and show spinner
echo -e "${YELLOW}Starting XeLaTeX compilation...${NC}"
xelatex -interaction=nonstopmode -output-directory=output resume.tex > /dev/null 2>&1 &
LATEX_PID=$!

# Show spinner while compilation runs
show_spinner $LATEX_PID

# Wait for LaTeX compilation to finish and get exit code
wait $LATEX_PID
LATEX_EXIT_CODE=$?

# Check if PDF was generated successfully
if [ $LATEX_EXIT_CODE -eq 0 ] && [ -f "output/resume.pdf" ]; then
    echo -e "${GREEN}✓ CV compiled successfully to ${WHITE}output/resume.pdf${NC}"

    # Clean up auxiliary files after successful build
    echo -e "${YELLOW}Cleaning up auxiliary files...${NC}"
    rm -f output/*.aux output/*.log output/*.out output/*.fls output/*.fdb_latexmk
    echo -e "${GREEN}✓ Cleanup completed${NC}"
else
    echo -e "${RED}✗ Compilation failed${NC}"
    echo -e "${GRAY}Check output/resume.log for details${NC}"
    exit 1
fi