from ...pyhwException import OSUnsupportedException


class TitleDetect:
    def __init__(self, os):
        self.OS = os

    def getTitle(self):
        if self.OS in ["linux", "macos", "freebsd"]:
            from .unix import TitleDetectUnix
            return TitleDetectUnix().getTitle()
        elif self.OS == "windows":
            from .windows import TitleDetectWindows
            return TitleDetectWindows().getTitle()
        else:
            raise OSUnsupportedException("Unsupported operating system")
