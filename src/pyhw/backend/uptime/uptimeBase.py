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
            from .linux import UptimeDetectLinux
            return UptimeDetectLinux().getUptimeInfo()
        elif self.OS == "macos":
            from .macos import UptimeDetectMacOS
            return UptimeDetectMacOS().getUptimeInfo()
        elif self.OS == "freebsd":
            from .bsd import UptimeDetectBSD
            return UptimeDetectBSD().getUptimeInfo()
        elif self.OS == "windows":
            from .windows import UptimeDetectWindows
            return UptimeDetectWindows().getUptimeInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
