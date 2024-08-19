from .kernelInfo import KernelInfo
import subprocess


class KernelDetectUnix:
    def __init__(self):
        self.__kernelInfo = KernelInfo()

    def getKernelInfo(self):
        self.__getKernelName()
        self.__getKernelVersion()
        self.__getKernelMachine()
        self.__kernelInfo.kernel = self.__kernelInfo.name + " " + self.__kernelInfo.version + " " + self.__kernelInfo.machine
        return self.__kernelInfo

    def __getKernelName(self):
        try:
            result = subprocess.run(['uname', '-s'], capture_output=True, text=True)
            self.__kernelInfo.name = result.stdout.strip()
        except subprocess.SubprocessError:
            pass

    def __getKernelVersion(self):
        try:
            result = subprocess.run(['uname', '-r'], capture_output=True, text=True)
            self.__kernelInfo.version = result.stdout.strip()
        except subprocess.SubprocessError:
            pass

    def __getKernelMachine(self):
        try:
            result = subprocess.run(['uname', '-m'], capture_output=True, text=True)
            self.__kernelInfo.machine = result.stdout.strip()
        except subprocess.SubprocessError:
            pass

