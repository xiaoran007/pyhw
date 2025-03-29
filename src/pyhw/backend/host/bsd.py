from .linux import HostDetectLinux


class HostDetectBSD(HostDetectLinux):
    def __init__(self):
        HostDetectLinux.__init__(self)

    def getHostInfo(self):
        self._hostInfo.name = f"General {self._arch} FreeBSD Host"
        self._hostInfo.version = ""
        self._hostInfo.model = self._hostInfo.name + " " + self._hostInfo.version
        return self._hostInfo
