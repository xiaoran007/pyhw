from ...pyhwException import BackendException
from .memoryInfo import MemoryInfo
import subprocess
import json


class MemoryDetectWindows:
    def __init__(self):
        self._memoryInfo = MemoryInfo()

    def getMemoryInfo(self):
        self._getMemory()
        self._memoryInfo.memory = f"{self._memoryInfo.used} MiB / {self._memoryInfo.total} MiB"
        return self._memoryInfo

    def _getMemory(self):
        COMMAND = 'Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object FreePhysicalMemory,TotalVisibleMemorySize | ConvertTo-JSON'
        try:
            result = subprocess.run(["powershell", "-NoProfile", "-Command", COMMAND], capture_output=True, text=True)
        except subprocess.SubprocessError:
            raise BackendException("Failed to get memory information on Windows.")

        res = json.loads(result.stdout)
        free_memory = int(res['FreePhysicalMemory']) / 1024
        total_memory = int(res['TotalVisibleMemorySize']) / 1024
        used_memory = total_memory - free_memory
        self._memoryInfo.total = round(total_memory, 2)
        self._memoryInfo.available = round(free_memory, 2)
        self._memoryInfo.used = round(used_memory, 2)







