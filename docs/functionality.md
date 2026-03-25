# PyHw
## Features
The functionality of this package varies slightly on different operating systems and architectures since some operating system-specific settings or other availability limitations.

### OS
This detector is available on all operating systems.

### Host
This detector is available on all operating systems, but the information it provides may vary depending on the operating system.
* SBCs (Single Board Computers) are detected through device tree information, which is not available on all SBCs.
* X86_64 and ARM64 architectures are detected through the BIOS/UEFI information, which is not available on all motherboard.
* Docker and WSL can not get the detailed host information.

### Kernel
This detector is available on all operating systems.

### Uptime
This detector is available on all operating systems.

### Shell
This detector is available on all operating systems, but the information it provides may vary depending on the operating system.
* Windows shell only support `PowerShell` and `MSYS Bash`, other shells are not supported.
* Unix-like systems detect the default shell via the `SHELL` environment variable, not the currently running shell.
* In Docker environments, it falls back to parsing `/etc/passwd` for the root user.

### CPU
This detector is available on all operating systems, but the information it provides may vary depending on the operating system.
* SBCs (Single Board Computers) are detected through device tree information, which is not available on all SBCs.

### GPU
This detector is available on all operating systems, but the information it provides may vary depending on the operating system.
* SBCs (Single Board Computers) are detected through device tree information, which is not available on all SBCs.
* On Linux, obtaining NVIDIA GPU core counts requires a custom `nvmlGPULib` C library.
* On macOS, GPU details are gathered via a custom `iokitGPULib` swift library or `system_profiler`, handling both Integrated (Apple Silicon/Intel) and Discrete (AMD) GPUs.

### NPU
This detector is available on all operating systems, but the information it provides may vary depending on the operating system.
* SBCs (Single Board Computers) are detected through device tree information, which is not available on all SBCs.
* On macOS with Apple Silicon, the NPU (Apple Neural Engine) details and core counts are directly mapped from the detected CPU model.

### Memory
This detector is available on all operating systems. Information is natively gathered across platforms:
* Linux parses `/proc/meminfo`.
* Windows queries `Win32_OperatingSystem` via WMI/CIM.
* macOS combines `sysctl` hardware properties with detailed `vm_stat` page allocations.
* BSD utilizes `sysctl`.

### NIC
This detector is available on all operating systems, but the information it provides may vary depending on the operating system.
* Linux and Windows primarily rely on detecting PCI devices.
* On Linux, if PCI devices are absent (e.g., WSL, Docker), it falls back to reading `/sys/class/net/` and using the `ip` command.
* On macOS, it relies on a custom `iokitNICLib` swift library to fetch the default network interface, falling back to command-line tools like `networksetup` and `system_profiler` for Wi-Fi and link speed details.

### Title
This detector is available on all operating systems.
