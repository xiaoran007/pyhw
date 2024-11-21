from .linux import NPUDetectLinux
from .macos import NPUDetectMacOS
from .bsd import NPUDetectBSD


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
        else:
            raise NotImplementedError("Unsupported operating system")


