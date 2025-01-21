"""
 In dev.
"""
from .titleInfo import TitleInfo
import getpass
import platform


class TitleDetectWindows:
    def __init__(self):
        self.__titleInfo = TitleInfo()

    def getTitle(self):
        self.__titleInfo.username = getpass.getuser()
        self.__titleInfo.hostname = platform.node()
        self.__titleInfo.title = f"{self.__titleInfo.username}@{self.__titleInfo.hostname}"
        return self.__titleInfo
