from ...pyhwException import OSUnsupportedException


class NPUDetect:
    def __init__(self, os):
        self.OS = os

    def getNPUInfo(self):
        if self.OS == "linux":
            from .linux import NPUDetectLinux
            return NPUDetectLinux().getNPUInfo()
        elif self.OS == "macos":
            from .macos import NPUDetectMacOS
            return NPUDetectMacOS().getNPUInfo()
        elif self.OS == "freebsd":
            from .bsd import NPUDetectBSD
            return NPUDetectBSD().getNPUInfo()
        elif self.OS == "windows":
            from .windows import NPUDetectWindows
            return NPUDetectWindows().getNPUInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
