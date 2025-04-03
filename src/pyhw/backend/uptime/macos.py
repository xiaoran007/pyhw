from .uptimeInfo import UptimeInfo
from ...pyhwUtil import sysctlGetString
import re
import subprocess


class UptimeDetectMacOS:
    def __init__(self):
        self._uptimeInfo = UptimeInfo()
        self._boot_time = 0
        self._now = 0

    def getUptimeInfo(self):
        self._getUptime()
        uptime_seconds = self._now - self._boot_time
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        days = int(days)
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)
        if days == 0:
            if hours == 0:
                self._uptimeInfo.uptime = f"{minutes} mins {seconds} secs"
            else:
                self._uptimeInfo.uptime = f"{hours} hours {minutes} mins {seconds} secs"
        else:
            self._uptimeInfo.uptime = f"{days} days {hours} hours {minutes} mins {seconds} secs"
        return self._uptimeInfo

    def _getUptime(self):
        result = sysctlGetString("kern.boottime")
        match = re.search(r'sec = (\d+),', result)
        if match:
            self._boot_time = int(match.group(1))
        else:
            return
        self._now = int(subprocess.check_output(["date", "+%s"]).decode().strip())
