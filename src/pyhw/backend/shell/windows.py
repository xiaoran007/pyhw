from ...pyhwException import BackendException
from .shellInfo import ShellInfo
import json
import subprocess
import os


class ShellDetectWindows:
    def __init__(self):
        self.__shellInfo = ShellInfo()

    def getShellInfo(self):
        if not self.__getShellBash():
            self.__getShellPowerShell()
        self.__shellInfo.info = self.__shellInfo.shell + " " + self.__shellInfo.version
        return self.__shellInfo

    def __getShellBash(self) -> bool:
        try:
            shell_env = os.getenv("SHELL", "")
            if "bash" in shell_env:
                self.__shellInfo.shell = "bash"
                self.__shellInfo.path = shell_env
                result = subprocess.run(["bash", "-c", "echo $BASH_VERSION"], capture_output=True, text=True)
                self.__shellInfo.version = result.stdout.strip().split("(")[0]
                self.__shellInfo.info = self.__shellInfo.shell + " " + self.__shellInfo.version
                return True
            else:
                return False
        except:
            return False

    def __getShellPowerShell(self):
        COMMAND = "$PSVersionTable.PSVersion | ConvertTo-JSON"

        try:
            result = subprocess.run(["powershell", "-NoProfile", "-Command", COMMAND], capture_output=True, text=True)
        except subprocess.SubprocessError:
            raise BackendException("Error running PowerShell command.")

        res = json.loads(result.stdout)
        major = res["Major"]
        minor = res["Minor"]

        self.__shellInfo.shell = "PowerShell"
        self.__shellInfo.version = f"{major}.{minor}"
