# Makefile for xianmalik_cv
# Targets: build (default), watch, open, clean, deps, venv

.PHONY: build watch open clean deps venv

BUILD_SCRIPT := ./scripts/build.py
PDF := output/resume.pdf
VENV_DIR := .venv
PY := $(VENV_DIR)/bin/python3
PIP := $(VENV_DIR)/bin/pip

build: deps
	@PATH="$(VENV_DIR)/bin:$$PATH" $(PY) $(BUILD_SCRIPT)

deps: venv
	@$(PY) -c "import yaml" >/dev/null 2>&1 || $(PIP) install -r requirements.txt

venv:
	@command -v python3 >/dev/null 2>&1 || { echo "python3 not found"; exit 1; }
	@[ -d $(VENV_DIR) ] || python3 -m venv $(VENV_DIR)
	@$(PIP) -q install --upgrade pip

watch: deps
	@PATH="$(VENV_DIR)/bin:$$PATH" ./scripts/watch.sh

open: build
	@([ -f $(PDF) ] && open $(PDF)) || { echo "$(PDF) not found"; exit 1; }

clean:
	@./scripts/clean.sh

