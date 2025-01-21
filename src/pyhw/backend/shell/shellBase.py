from ...pyhwException import OSUnsupportedException


class ShellDetect:
    def __init__(self, os):
        self.OS = os

    def getShellInfo(self):
        if self.OS in ["linux", "macos", "freebsd"]:
            from .unix import ShellDetectUnix
            return ShellDetectUnix().getShellInfo()
        elif self.OS == "windows":
            from .windows import ShellDetectWindows
            return ShellDetectWindows().getShellInfo()
        else:
            raise OSUnsupportedException("Unsupported operating system")
