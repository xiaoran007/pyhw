"""
    In dev.
"""
from .uptimeInfo import UptimeInfo


class UptimeDetectLinux:
    def __init__(self):
        self.__uptimeInfo = UptimeInfo()

    def getUptimeInfo(self):
        self.__getUptime()
        return self.__uptimeInfo

    def __getUptime(self):
        with open("/proc/uptime", "r") as f:
            uptime_seconds = float(f.readline().split(" ")[0])
            hours, remainder = divmod(uptime_seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            days = int(days)
            hours = int(hours)
            minutes = int(minutes)
            seconds = int(seconds)
            if days == 0:
                if hours == 0:
                    self.__uptimeInfo.uptime = f"{minutes} min {seconds} sec"
                else:
                    self.__uptimeInfo.uptime = f"{hours} hours {minutes} min {seconds} sec"
            else:
                self.__uptimeInfo.uptime = f"{days} days {hours} hours {minutes} min {seconds} sec"
