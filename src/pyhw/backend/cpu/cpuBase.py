from ...pyhwException import OSUnsupportedException


class CPUDetect:
    def __init__(self, os):
        self.OS = os

    def getCPUInfo(self):
        if self.OS == "linux":
            from .linux import CPUDetectLinux
            return CPUDetectLinux().getCPUInfo()
        elif self.OS == "macos":
            from .macos import CPUDetectMacOS
            return CPUDetectMacOS().getCPUInfo()
        elif self.OS == "freebsd":
            from .bsd import CPUDetectBSD
            return CPUDetectBSD().getCPUInfo()
        elif self.OS == "windows":
            from .windows import CPUDetectWindows
            return CPUDetectWindows().getCPUInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
