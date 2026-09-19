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
* Other platforms are detected through `pypci-ng` package.

### Foundation Models (AFM)
On macOS, PyHw queries the default on-device model through Apple's public Foundation Models framework. The `AFM` line appears after NPU; it is omitted on other operating systems.

* macOS 26+ reports availability, or the system's reason: device not eligible, Apple Intelligence not enabled, or model not ready. "Model not ready" does not necessarily mean the model is absent or downloading.
* macOS 27+ also reports the official model variant's display name when available (for example, `AFM 3 Core`). macOS 26 displays the generic `Apple Foundation Model` name.
* Exact model weight versions/build numbers are not exposed by the public API. `--debug` shows `AFM model version: not exposed`, separately from the model variant, together with the raw status, reason, detection errors, and timing.
* macOS versions before 26 report `Unsupported — Requires macOS 26+` without loading the library. A missing or unloadable bridge reports `Detection unavailable`, which is distinct from a model being unavailable.
* Detection only reads model metadata. It does not create a generation session, prewarm the model, request downloads, or inspect private model asset directories. This reports the default local model, not all Apple Intelligence features or Private Cloud Compute.

The native bridge requires the macOS 27 SDK to build; other native libraries keep their existing build settings. See the [build instructions](../README.md#44-build-full-feature-package).

References: [SystemLanguageModel](https://developer.apple.com/documentation/foundationmodels/systemlanguagemodel), [availability reasons](https://developer.apple.com/documentation/foundationmodels/systemlanguagemodel/availability-swift.enum/unavailablereason), and [model variant](https://developer.apple.com/documentation/foundationmodels/systemlanguagemodel/variant-swift.property).

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
