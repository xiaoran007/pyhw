from .osInfo import OSInfo


class OSDetectLinux:
    def __init__(self):
        self._osInfo = OSInfo()

    def getOSInfo(self):
        """
        Detects the os distribution and its version.
        :return: dataclass OSInfoLinux, direct attrs: prettyName
        """
        self._getOSInfo()
        self._handleArmbian()
        return self._osInfo

    def _getOSInfo(self):
        try:
            with open("/etc/os-release", "r") as f:
                for line in f:
                    key, value = line.strip().split("=")
                    if key == "PRETTY_NAME":
                        self._osInfo.prettyName = value.strip('"')
                    elif key == "NAME":
                        self._osInfo.name = value.strip('"')
                    elif key == "ID":
                        self._osInfo.id = value.strip('"')
                    elif key == "ID_LIKE":
                        self._osInfo.idLike = value.strip('"')
                    elif key == "VARIANT":
                        self._osInfo.variant = value.strip('"')
                    elif key == "VARIANT_ID":
                        self._osInfo.variantID = value.strip('"')
                    elif key == "VERSION":
                        self._osInfo.version = value.strip('"')
                    elif key == "VERSION_ID":
                        self._osInfo.versionID = value.strip('"')
                    elif key == "VERSION_CODENAME":
                        self._osInfo.versionCodename = value.strip('"')
                    elif key == "CODE_NAME":
                        self._osInfo.codeName = value.strip('"')
                    elif key == "BUILD_ID":
                        self._osInfo.buildID = value.strip('"')
        except Exception:
            pass

    def _handleArmbian(self):
        if "Armbian" in self._osInfo.prettyName or "armbian" in self._osInfo.prettyName:
            self._osInfo.id = "armbian"
