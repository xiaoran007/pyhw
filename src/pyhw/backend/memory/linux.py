from dataclasses import dataclass


@dataclass
class MemoryInfoLinux:
    memory = ""
    total = 0
    available = 0
    used = 0


class MemoryDetectLinux:
    def __init__(self):
        self.__memoryInfo = MemoryInfoLinux()

    def getMemoryInfo(self):
        self.__getMemory()
        self.__memoryInfo.memory = f"{self.__memoryInfo.used} MiB / {self.__memoryInfo.total} MiB"
        return self.__memoryInfo

    def __getMemory(self):
        try:
            with open("/proc/meminfo", "r") as file:
                for line in file:
                    if line.startswith("MemTotal:"):
                        self.__memoryInfo.total = round(float(line.split(":")[1].strip()[:-3]) / 1024, 2)
                    elif line.startswith("MemAvailable:"):
                        self.__memoryInfo.available = round(float(line.split(":")[1].strip()[:-3]) / 1024, 2)
                self.__memoryInfo.used = round(self.__memoryInfo.total - self.__memoryInfo.available, 2)
        except FileNotFoundError:
            pass

