from ...pyhwException import BackendException
from .uptimeInfo import UptimeInfo
import subprocess
import json
import re
from datetime import datetime


class UptimeDetectWindows:
    def __init__(self):
        self.__uptimeInfo = UptimeInfo()

    def getUptimeInfo(self):
        self.__getUptime()
        return self.__uptimeInfo

    def __getUptime(self):
        COMMAND = 'Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object LastBootUpTime | ConvertTo-JSON'
        try:
            result = subprocess.run(["powershell", "-NoProfile", "-Command", COMMAND], capture_output=True, text=True)
        except subprocess.SubprocessError:
            raise BackendException("Error while getting system uptime")

        res = json.loads(result.stdout)
        timestamp_str = res['LastBootUpTime']
        match = re.search(r'\d+', timestamp_str)

        if match:
            timestamp_ms = int(match.group(0))
            last_boot_time = datetime.utcfromtimestamp(timestamp_ms / 1000)
            current_time = datetime.utcnow()
            uptime = current_time - last_boot_time
            days = uptime.days
            seconds = uptime.seconds
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            secs = (seconds % 3600) % 60

            if days == 0:
                if hours == 0:
                    self.__uptimeInfo.uptime = f"{minutes} mins {secs} secs"
                else:
                    self.__uptimeInfo.uptime = f"{hours} hours {minutes} mins {secs} secs"
            else:
                self.__uptimeInfo.uptime = f"{days} days {hours} hours {minutes} mins {secs} secs"
        else:
            raise BackendException("Error while getting system uptime")
