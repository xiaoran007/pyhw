from .linux import MemoryDetectLinux


class MemoryDetect:
    def __init__(self, os):
        self.OS = os

    def getMemoryInfo(self):
        if self.OS == "linux":
            return MemoryDetectLinux().getMemoryInfo()
        else:
            raise NotImplementedError("Unsupported operating system")
