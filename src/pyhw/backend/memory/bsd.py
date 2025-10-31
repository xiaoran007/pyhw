from .linux import MemoryDetectLinux
from ...pyhwUtil import sysctlGetInt


class MemoryDetectBSD(MemoryDetectLinux):
    def __init__(self):
        MemoryDetectLinux.__init__(self)
        self.__page_size = 0
        self.__physical_memory = 0
        self.__free_pages = 0
        self.__free_memory = 0

    def getMemoryInfo(self):
        self.__getMemorySysctl()
        self._memoryInfo.total = self.__physical_memory / 1024 / 1024 / 1024  # Convert bytes to GiB
        self._memoryInfo.used = (self.__physical_memory - self.__free_memory) / 1024 / 1024 / 1024  # Convert bytes to GiB
        self._memoryInfo.memory = f"{round(self._memoryInfo.used, 2)} GiB / {round(self._memoryInfo.total, 2)} GiB"
        return self._memoryInfo

    def __getMemorySysctl(self):
        self.__page_size = sysctlGetInt("hw.pagesize")
        self.__physical_memory = sysctlGetInt("hw.physmem")
        self.__free_pages = sysctlGetInt("vm.stats.vm.v_free_count")
        self.__free_memory = self.__free_pages * self.__page_size
