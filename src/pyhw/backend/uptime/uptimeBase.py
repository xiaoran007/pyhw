from .linux import UptimeDetectLinux
from .macos import UptimeDetectMacOS
from .bsd import UptimeDetectBSD
from ...pyhwException import OSUnsupportedException


class UptimeDetect:
    """
    Class for system uptime detection.
    """
    def __init__(self, os):
        self.OS = os

    def getUptime(self):
        """
        Detects the system uptime.
        :return: dataclass UptimeInfo, direct attr: uptime
        """
        if self.OS == "linux":
            return UptimeDetectLinux().getUptimeInfo()
        elif self.OS == "macos":
            return UptimeDetectMacOS().getUptimeInfo()
        elif self.OS == "freebsd":
            return UptimeDetectBSD().getUptimeInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
