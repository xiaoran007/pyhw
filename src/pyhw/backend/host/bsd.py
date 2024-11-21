from .linux import HostDetectLinux


class HostDetectBSD(HostDetectLinux):
    def __init__(self):
        super().__init__()

    def getHostInfo(self):
        self.__hostInfo.name = f"General {self.__arch} FreeBSD Host"
        self.__hostInfo.version = ""
        self.__hostInfo.model = self.__hostInfo.name + " " + self.__hostInfo.version

