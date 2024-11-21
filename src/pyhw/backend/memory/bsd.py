from .linux import MemoryDetectLinux


class MemoryDetectBSD(MemoryDetectLinux):
    def __init__(self):
        MemoryDetectLinux.__init__(self)

    def getMemoryInfo(self):
        self._memoryInfo.memory = f"Pass"
        return self._memoryInfo

