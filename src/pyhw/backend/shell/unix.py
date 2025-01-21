"""
    In dev.
"""
from ...pyhwUtil import getDocker
from .shellInfo import ShellInfo
import os
import subprocess


class ShellDetectUnix:
    def __init__(self):
        self.__shellInfo = ShellInfo()

    def getShellInfo(self):
        if getDocker():
            self.__getShellDocker()
        else:
            self.__getShell()
        self.__getVersion()
        self.__shellInfo.info = self.__shellInfo.shell + " " + self.__shellInfo.version
        return self.__shellInfo

    def __getShell(self):
        # Get the default shell, not the current shell.
        shell_env = os.getenv("SHELL", "")
        if shell_env != "":
            self.__shellInfo.shell = shell_env.split("/")[-1]
            self.__shellInfo.path = shell_env

    def __getShellDocker(self):
        try:
            with open("/etc/passwd", "r") as f:
                for line in f:
                    if line.startswith("root:"):
                        root_shell = line.strip().split(":")[-1]
                        break
        except:
            root_shell = ""
        if root_shell != "":
            self.__shellInfo.shell = root_shell.split("/")[-1]
            self.__shellInfo.path = root_shell

    def __getVersion(self):
        shell = self.__shellInfo.shell
        if shell != "":
            if shell in ["sh", "ash", "dash", "es"]:
                pass
            elif shell == "bash":
                try:
                    result = subprocess.run(["bash", "-c", "echo $BASH_VERSION"], capture_output=True, text=True)
                    self.__shellInfo.version = result.stdout.strip().split("(")[0]
                except subprocess.SubprocessError:
                    pass
            elif shell == "zsh":
                try:
                    result = subprocess.run(["zsh", "-c", "echo $ZSH_VERSION"], capture_output=True, text=True)
                    self.__shellInfo.version = result.stdout.strip()
                except subprocess.SubprocessError:
                    pass







