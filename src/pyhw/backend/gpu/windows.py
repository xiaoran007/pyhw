from .gpuInfo import GPUInfo
from ...pyhwUtil import PCIManager


class GPUDetectWindows:
    def __init__(self):
        self.__gpuInfo = GPUInfo()

    def getGPUInfo(self):
        self.__getGPUInfo()
        self.__sortGPUList()
        return self.__gpuInfo

    def __getGPUInfo(self):
        gpu_devices = PCIManager.get_instance().FindAllVGA()
        if len(gpu_devices) == 0:
            self.__handleNonePciDevices()
        else:
            for device in gpu_devices:
                if device.subsystem_device_name != "":
                    device_name = f"{device.vendor_name} {device.device_name} ({device.subsystem_device_name})"
                else:
                    device_name = f"{device.vendor_name} {device.device_name}"
                self.__gpuInfo.gpus.append(self.__gpuNameClean(device_name))
                self.__gpuInfo.number += 1

    def __handleNonePciDevices(self):
        self.__gpuInfo.gpus.append("Not found")
        self.__gpuInfo.number = 1

    @staticmethod
    def __gpuNameClean(gpu_name: str):
        gpu_name_clean = gpu_name.replace("Corporation ", "")
        return gpu_name_clean

    def __sortGPUList(self):
        self.__gpuInfo.gpus.sort()
