from .memoryInfo import MemoryInfo


class MemoryDetectLinux:
    def __init__(self):
        self._memoryInfo = MemoryInfo()

    def getMemoryInfo(self):
        self._getMemory()
        self._memoryInfo.memory = f"{self._memoryInfo.used} MiB / {self._memoryInfo.total} MiB"
        return self._memoryInfo

    def _getMemory(self):
        try:
            with open("/proc/meminfo", "r") as file:
                for line in file:
                    if line.startswith("MemTotal:"):
                        self._memoryInfo.total = round(float(line.split(":")[1].strip()[:-3]) / 1024, 2)
                    elif line.startswith("MemAvailable:"):
                        self._memoryInfo.available = round(float(line.split(":")[1].strip()[:-3]) / 1024, 2)
                self._memoryInfo.used = round(self._memoryInfo.total - self._memoryInfo.available, 2)
        except FileNotFoundError:
            pass
