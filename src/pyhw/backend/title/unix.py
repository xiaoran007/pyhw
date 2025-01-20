"""
 In dev.
"""
import subprocess
from .titleInfo import TitleInfo


class TitleDetectUnix:
    def __init__(self):
        self.__titleInfo = TitleInfo()

    def getTitle(self):
        self.__getTitle()
        return self.__titleInfo

    def __getTitle(self):
        try:
            username_result = subprocess.run(['whoami'], capture_output=True, text=True)
            self.__titleInfo.username = username_result.stdout.strip()
            hostname_result = subprocess.run(['hostname'], capture_output=True, text=True)
            self.__titleInfo.hostname = hostname_result.stdout.strip()
            self.__titleInfo.title = f"{self.__titleInfo.username}@{self.__titleInfo.hostname}"
        except Exception as e:
            pass


