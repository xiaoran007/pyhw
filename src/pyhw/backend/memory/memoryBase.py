from .linux import MemoryDetectLinux
from .macos import MemoryDetectMacOS


class MemoryDetect:
    def __init__(self, os):
        self.OS = os

    def getMemoryInfo(self):
        if self.OS == "linux":
            return MemoryDetectLinux().getMemoryInfo()
        elif self.OS == "macos":
            return MemoryDetectMacOS().getMemoryInfo()
        else:
            raise NotImplementedError("Unsupported operating system")
