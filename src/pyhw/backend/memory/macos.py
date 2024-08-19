from .memoryInfo import MemoryInfo
from ...pyhwUtil import sysctlGetInt
import subprocess


class MemoryDetectMacOS:
    def __init__(self):
        self.__memoryInfo = MemoryInfo()
        self.__hw_pagesize = 0
        self.__mem_total = 0
        self.__active_count = 0
        self.__inactive_count = 0
        self.__speculative_count = 0
        self.__wire_count = 0
        self.__compressor_page_count = 0
        self.__purgeable_count = 0
        self.__external_page_count = 0
        self.__mem_used = 0

    def getMemoryInfo(self):
        self.__getMemory()
        self.__memoryInfo.total = self.__mem_total / 1024 / 1024  # Convert bytes to MiB
        self.__memoryInfo.used = self.__mem_used / 1024 / 1024  # Convert bytes to MiB
        self.__memoryInfo.memory = f"{round(self.__memoryInfo.used, 2)} MiB / {round(self.__memoryInfo.total, 2)} MiB"
        return self.__memoryInfo

    def __getMemory(self):
        self.__hw_pagesize = sysctlGetInt("hw.pagesize")
        self.__mem_total = sysctlGetInt("hw.memsize")
        self.__getVMStat()
        self.__mem_used = self.__hw_pagesize * (self.__active_count + self.__inactive_count + self.__speculative_count +
                                                self.__wire_count + self.__compressor_page_count -
                                                self.__purgeable_count - self.__external_page_count)

    def __getVMStat(self):
        try:
            result = subprocess.run(["vm_stat"], capture_output=True, text=True)
            vm_stats = result.stdout.split("\n")
        except subprocess.SubprocessError:
            vm_stats = []
        for vm_stat in vm_stats:
            if vm_stat.startswith("Pages active"):
                self.__active_count = int(vm_stat.split(":")[1].strip().split(".")[0])
            elif vm_stat.startswith("Pages inactive"):
                self.__inactive_count = int(vm_stat.split(":")[1].strip().split(".")[0])
            elif vm_stat.startswith("Pages speculative"):
                self.__speculative_count = int(vm_stat.split(":")[1].strip().split(".")[0])
            elif vm_stat.startswith("Pages wired down"):
                self.__wire_count = int(vm_stat.split(":")[1].strip().split(".")[0])
            elif vm_stat.startswith("Pages occupied by compressor"):  # compressor_page_count
                self.__compressor_page_count = int(vm_stat.split(":")[1].strip().split(".")[0])
            elif vm_stat.startswith("Pages purgeable"):
                self.__purgeable_count = int(vm_stat.split(":")[1].strip().split(".")[0])
            # miss external_page_count here
            elif vm_stat.startswith("File-backed pages:"):
                self.__external_page_count = int(vm_stat.split(":")[1].strip().split(".")[0])
