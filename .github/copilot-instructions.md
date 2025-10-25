## Welcome to PyHw!

This document provides a guide for AI developers to get started with the PyHw codebase.

### Big Picture

PyHw is a command-line tool for fetching system information, similar to `neofetch`. It's written primarily in Python and designed to be cross-platform.

The architecture is split into two main components:

1.  **Backend (`src/pyhw/backend`)**: This component is responsible for gathering system information. It has a modular design, with submodules for different hardware components (CPU, GPU, memory, etc.). Each submodule follows a factory pattern:
    *   A `*Base.py` file (e.g., `cpuBase.py`) acts as a factory, detecting the operating system and loading the appropriate platform-specific implementation.
    *   A `*Info.py` file (e.g., `cpuInfo.py`) defines a dataclass to store the information for that component.
    *   Platform-specific files (e.g., `macos.py`, `linux.py`) contain the actual implementation for gathering the data on that OS. These often use a mix of Python standard libraries, system calls (`sysctl`), and custom C libraries (located in `src/pyhw/library`).

2.  **Frontend (`src/pyhw/frontend`)**: This component is responsible for displaying the collected information.
    *   `frontendBase.py` contains the `Printer` class, which handles formatting, coloring, and printing the output, including the ASCII logo.
    *   The `logo` and `color` submodules manage the ASCII art and color schemes.

### Developer Workflows

**Building the project:**

The project uses a `Makefile` to streamline the build process. To build the project, including the C libraries, run:

```bash
make build
```

This command will first compile the C libraries using the `lib` target and then build the Python package.

**Testing:**

The testing workflow relies on Docker. To run the tests, use the following command:

```bash
make test
```

This will build the project and then run the tests inside a Docker container, as defined in `scripts/docker_local.sh`.

### Project Conventions

*   **Platform-specific code:** All platform-specific code is isolated in its respective file within the backend modules (e.g., `cpu/macos.py`, `cpu/linux.py`). When adding new features, follow this pattern.
*   **Data Structures:** System information is stored in dataclasses defined in the `*Info.py` files. This provides a consistent structure for the data.
*   **External Dependencies:** The project has a dependency on `pypci-ng` for PCI device information. It also uses custom C libraries for performance-critical or low-level data gathering. These libraries are located in `src/pyhw/library` and are compiled as part of the build process.
*   **Adding a new logo:** To add a new logo, you need to:
    1.  Create a `<os>.pyhw` file in `src/pyhw/frontend/logo/ascii`.
    2.  Modify `colorConfig.py` to add a new logo style.
    3.  Update `pyhwUtil.py` to enable the new logo style.

### Key Files

*   `src/pyhw/backend/backendBase.py`: Defines the `Data` dataclass, which is the central data structure for all collected information.
*   `src/pyhw/frontend/frontendBase.py`: Contains the `Printer` class, which is the core of the display logic.
*   `Makefile`: The entry point for build and test workflows.
*   `pyproject.toml`: Defines project metadata, dependencies, and entry points.
