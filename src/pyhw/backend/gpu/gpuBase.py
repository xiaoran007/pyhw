from .linux import GPUDetectLinux


class GPUDetect:
    def __init__(self, os):
        self.OS = os

    def getGPUInfo(self):
        if self.OS == "linux":
            return GPUDetectLinux().getGPUInfo()
        else:
            raise NotImplementedError("Unsupported operating system")
