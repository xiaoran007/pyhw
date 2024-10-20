from .nicInfo import NICInfo
import subprocess


class NICDetectMacOS:
    def __init__(self):
        self.__nicInfo = NICInfo()

    def getNICInfo(self):
        self.__getNICInfo()
        return self.__nicInfo

    def __getNICInfo(self):
        # Placeholder for a more advanced method.
        try:
            interface = subprocess.run(["bash", "-c", "route get default | grep interface"], capture_output=True, text=True).stdout.strip().split(":")[1]
            if_ip = subprocess.run(["bash", "-c", f"ipconfig getifaddr {interface}"], capture_output=True, text=True).stdout.strip()
            self.__nicInfo.nics.append(f"{interface} @ {if_ip}")
            self.__nicInfo.number += 1
        except:
            self.__handleError()

    def __handleError(self):
        self.__nicInfo.nics.append("en0")
        self.__nicInfo.number = 1


