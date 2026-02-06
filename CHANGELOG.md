# Changelog

## [2.5.0] - 2025-02-06

### Changed
- Standardized package name to `psimon-h7` across all platforms.
- Renamed internal package from `simon_h7` to `psimon`.
- Updated version to 2.5.0.
- Updated GitHub Actions to support dual publishing (PyPI and TestPyPI) using Trusted Publishing.

## [2.3.0] - 2025-02-02

### Added
- First official release to PyPI.
- Added `pyproject.toml` for standard packaging and installation.
- Added `LICENSE` file (MIT).
- Added `walkthrough.md` with technical documentation.
- Integrated `main.py` entry point as a CLI command `simon-h7`.

### Changed
- Updated version to 2.3 across all files.
- Refactored `main.py` to use direct module calls instead of subprocesses for better compatibility.
- Improved package structure for distribution.
