from .osInfo import OSInfo
from ...pyhwUtil import getArch
import subprocess


class OSDetectMacOS:
    def __init__(self):
        self.__osInfo = OSInfo()
        self.__ProductName = ""
        self.__ProductVersion = ""
        self.__BuildVersion = ""
        self.__VersionName = ""

    def getOSInfo(self):
        self.__getOS()
        self.__osInfo.prettyName = f"{self.__ProductName} {self.__ProductVersion} {self.__BuildVersion} {getArch()}"
        return self.__osInfo

    def __getOS(self):
        try:
            result = subprocess.run(["sw_vers"], capture_output=True, text=True)
            sw_vers = result.stdout.split("\n")
        except subprocess.SubprocessError:
            sw_vers = []
        for sw_ver in sw_vers:
            if sw_ver.startswith("ProductName:"):
                self.__ProductName = sw_ver.split(":")[1].strip()
            elif sw_ver.startswith("ProductVersion:"):
                self.__ProductVersion = sw_ver.split(":")[1].strip()
            elif sw_ver.startswith("BuildVersion:"):
                self.__BuildVersion = sw_ver.split(":")[1].strip()

    def __handelOSName(self):
        # Add os name -- product version conversion logic in the future.
        pass
