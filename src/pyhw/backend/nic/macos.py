from .nicInfo import NICInfo
import subprocess


class NICDetectMacOS:
    def __init__(self):
        self.__nicInfo = NICInfo()

    def getNICInfo(self):
        self.__nicInfo.nics.append("en0")
        self.__nicInfo.number = 1
        return self.__nicInfo

    def __getNICInfo(self):
        # Placeholder for a more advanced method.
        interfaces = subprocess.run(["bash", "-c", "route get default | grep interface"], capture_output=True, text=True).stdout.strip()


