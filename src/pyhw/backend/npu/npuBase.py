from .linux import NPUDetectLinux
from .macos import NPUDetectMacOS


class NPUDetect:
    def __init__(self, os):
        self.OS = os

    def getNPUInfo(self):
        if self.OS == "linux":
            return NPUDetectLinux().getNPUInfo()
        elif self.OS == "macos":
            return NPUDetectMacOS().getNPUInfo()
        else:
            raise NotImplementedError("Unsupported operating system")


