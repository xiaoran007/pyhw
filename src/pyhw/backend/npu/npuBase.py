from .linux import NPUDetectLinux
from .macos import NPUDetectMacOS
from .bsd import NPUDetectBSD
from .windows import NPUDetectWindows


class NPUDetect:
    def __init__(self, os):
        self.OS = os

    def getNPUInfo(self):
        if self.OS == "linux":
            return NPUDetectLinux().getNPUInfo()
        elif self.OS == "macos":
            return NPUDetectMacOS().getNPUInfo()
        elif self.OS == "freebsd":
            return NPUDetectBSD().getNPUInfo()
        elif self.OS == "windows":
            return NPUDetectWindows().getNPUInfo()
        else:
            raise NotImplementedError("Unsupported operating system")


