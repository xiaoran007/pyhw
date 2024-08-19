from .uptimeInfo import UptimeInfo
from ...pyhwUtil import sysctlGetString
import re
import subprocess


class UptimeDetectMacOS:
    def __init__(self):
        self.__uptimeInfo = UptimeInfo()
        self.__boot_time = 0
        self.__now = 0

    def getUptimeInfo(self):
        self.__getUptime()
        uptime_seconds = self.__now - self.__boot_time
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
        return self.__uptimeInfo

    def __getUptime(self):
        result = sysctlGetString("kern.boottime")
        match = re.search(r'sec = (\d+),', result)
        if match:
            self.__boot_time = int(match.group(1))
        else:
            return
        self.__now = int(subprocess.check_output(["date", "+%s"]).decode().strip())

