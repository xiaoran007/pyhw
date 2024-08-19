from .linux import OSDetectLinux
from .macos import OSDetectMacOS
from ...pyhwException import OSUnsupportedException


class OSDetect:
    def __init__(self, os):
        self.__OS = os

    def getOSInfo(self):
        if self.__OS == "linux":
            return OSDetectLinux().getOSInfo()
        elif self.__OS == "macos":
            return OSDetectMacOS().getOSInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
