# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OCR application using RapidOCR library for optical character recognition tasks. The project uses `uv` for Python dependency management.

## Commands

### Dependency Management
- Install dependencies: `uv sync`
- Add new dependency: `uv add <package-name>`
- Run Python script: `uv run python main.py`

### Python Environment
- Python version: 3.12+ (specified in .python-version)
- Virtual environment managed by uv in `.venv/`

## Architecture

This is a minimal OCR application scaffold:
- `main.py`: Entry point with placeholder implementation
- Dependencies: Uses `rapidocr` (v3.6.0+) for OCR functionality and `onnxruntime` (v1.24.1+) as backend
- The project structure suggests this is an early-stage or demo application
