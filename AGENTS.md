# AGENTS.md

This file defines the Codex development conventions for PyHw. It is the authoritative instruction file for future automated assistance in this repository. `.github/copilot-instructions.md` is historical Copilot context only and may be removed after the migration is complete.

## Project Overview

PyHw is a Python command-line system information tool similar to `neofetch`. It uses a `src/` package layout, and the CLI entry point is `src/pyhw/__main__.py`.

Main directories:

- `src/pyhw/backend/`: system information detection, organized by capability such as `cpu`, `gpu`, `memory`, `nic`, `npu`, `os`, and `host`.
- `src/pyhw/frontend/`: terminal output, colors, and ASCII logos.
- `src/pyhw/pyhwUtil/`: shared utilities such as OS/architecture detection, PCI management, sysctl helpers, and release checks.
- `src/pyhw/library/`: native libraries used for full-feature builds, including macOS IOKit Swift/C libraries and Linux NVML C++ libraries.
- `test/`: pytest test suite.
- `pyproject.toml`: package metadata, dependencies, and CLI entry point.

## Python Environment

- The project uses a repository-local `.venv`; do not use conda environments for this project.
- If `.venv` does not exist, initialize it with `python3 -m venv .venv`.
- Run project Python commands with `.venv/bin/python`.
- Run pip commands with `.venv/bin/python -m pip`.
- Do not use system `python`, system `python3`, conda Python, or global pip for project commands, except when creating `.venv`.
- Before using `Makefile` targets, activate `.venv` or ensure `.venv/bin` is first on `PATH`.

## Development Principles

- New features should follow the existing architecture first. Do not introduce a new organization pattern unless the user explicitly asks for a refactor.
- Each backend capability module should keep the current pattern:
  - `*Base.py` performs platform dispatch.
  - `*Info.py` stores the capability data structure.
  - `linux.py`, `macos.py`, `windows.py`, and `bsd.py` contain platform-specific implementations.
- Keep platform-specific logic in the corresponding platform file. Do not mix Linux, macOS, Windows, and BSD implementations in one file.
- Output logic belongs in `frontend/`, system detection logic belongs in `backend/`, and shared helpers belong in `pyhwUtil/`.
- Keep implementations simple and direct. Avoid adding excessive fallback logic unless the user asks for it or the existing code path already requires it.
- If an operation is expected to take a long time, add fine-grained progress reporting or make the execution stages visible to the caller.

## Dependency Policy

- Dependency preference order: Python standard library, internal implementation, existing dependencies, then new external dependencies.
- Do not add new external dependencies unless they are clearly necessary.
- If a new dependency is needed, explain why it is necessary, how it will be used, and what alternatives were considered before editing `pyproject.toml`.
- Do not silently replace missing dependencies with weaker degraded implementations.

## Build And Test

- This is a software package and system tool project. Code changes must be tested.
- The default test command is `.venv/bin/python -m pytest`.
- For local changes, run the most relevant tests first; before committing, prefer running the full test suite.
- Full-feature builds are expected to run on macOS development machines. Use `make build` when native libraries and package artifacts are needed.
- Ordinary package builds can use `.venv/bin/python -m build`.
- Install build or test dependencies only into `.venv` with `.venv/bin/python -m pip ...`.

## Logo Changes

When adding or modifying a distribution logo, usually update all of the following:

- `src/pyhw/frontend/logo/ascii/<os>.pyhw`
- `src/pyhw/frontend/color/colorConfig.py`
- `SupportedOS` in `src/pyhw/pyhwUtil/pyhwUtil.py`

The logo id, color configuration name, and `SupportedOS` entries must stay consistent.

## Git Workflow

- This repository uses git. Keep changes in small commits.
- Each commit should have one clear purpose. Do not mix unrelated changes into one commit.
- Check `git status --short` before committing.
- Do not revert, overwrite, or clean up user changes unless explicitly asked.
- Do not commit `.venv`, `dist/`, caches, or local environment artifacts.

