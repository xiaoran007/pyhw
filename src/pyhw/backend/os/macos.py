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
        self.__Arch = self.__handleOSArch()

    def getOSInfo(self):
        self.__getOS()
        self.__handelOSName()
        if self.__VersionName != "":
            self.__osInfo.prettyName = f"{self.__ProductName} {self.__VersionName} {self.__ProductVersion} {self.__BuildVersion} {self.__Arch}"
        else:
            self.__osInfo.prettyName = f"{self.__ProductName} {self.__ProductVersion} {self.__BuildVersion} {self.__Arch}"
        self.__osInfo.id = "macOS"
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
        # Only supports modern macOS
        macOSVersionMap = {
            "11": "Big Sur",
            "12": "Monterey",
            "13": "Ventura",
            "14": "Sonoma",
            "15": "Sequoia"
        }
        if "." in self.__ProductVersion:
            major = self.__ProductVersion.split(".")[0]
        else:
            major = self.__ProductVersion
        version_name = macOSVersionMap.get(major, "")
        if version_name != "":
            self.__VersionName = version_name

    @staticmethod
    def __handleOSArch():
        arch = getArch()
        if arch == "aarch64":
            return "arm64"
        else:
            return arch
