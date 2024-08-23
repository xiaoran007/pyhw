"""
    In dev.
"""
from .osInfo import OSInfo


class OSDetectLinux:
    def __init__(self):
        self.__osInfo = OSInfo()

    def getOSInfo(self):
        """
        Detects the os distribution and its version.
        :return: dataclass OSInfoLinux, direct attrs: prettyName
        """
        self.__getOSInfo()
        self.__handleArmbian()
        return self.__osInfo

    def __getOSInfo(self):
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    key, value = line.strip().split("=")
                    if key == "PRETTY_NAME":
                        self.__osInfo.prettyName = value.strip('"')
                    elif key == "NAME":
                        self.__osInfo.name = value.strip('"')
                    elif key == "ID":
                        self.__osInfo.id = value.strip('"')
                    elif key == "ID_LIKE":
                        self.__osInfo.idLike = value.strip('"')
                    elif key == "VARIANT":
                        self.__osInfo.variant = value.strip('"')
                    elif key == "VARIANT_ID":
                        self.__osInfo.variantID = value.strip('"')
                    elif key == "VERSION":
                        self.__osInfo.version = value.strip('"')
                    elif key == "VERSION_ID":
                        self.__osInfo.versionID = value.strip('"')
                    elif key == "VERSION_CODENAME":
                        self.__osInfo.versionCodename = value.strip('"')
                    elif key == "CODE_NAME":
                        self.__osInfo.codeName = value.strip('"')
                    elif key == "BUILD_ID":
                        self.__osInfo.buildID = value.strip('"')
        except Exception:
            pass

    def __handleArmbian(self):
        if "Armbian" in self.__osInfo.prettyName or "armbian" in self.__osInfo.prettyName:
            self.__osInfo.id = "armbian"
