from .linux import MemoryDetectLinux


class MemoryDetectBSD(MemoryDetectLinux):
    def __init__(self):
        super().__init__()

    def getMemoryInfo(self):
        self.__memoryInfo.memory = f"Pass"
        return self.__memoryInfo

