from .unix import TitleDetectUnix
from .windows import TitleDetectWindows
from ...pyhwException import OSUnsupportedException


class TitleDetect:
    def __init__(self, os):
        self.OS = os

    def getTitle(self):
        if self.OS in ["linux", "macos", "freebsd"]:
            return TitleDetectUnix().getTitle()
        elif self.OS == "windows":
            return TitleDetectWindows().getTitle()
        else:
            raise OSUnsupportedException("Unsupported operating system")
