import platform
from ..backend import Data
import os
from dataclasses import dataclass


def getOS():
    """
    Get the os type in lower case.
    :return: str, os type, value in [windows, linux, macos, unknown].
    """
    system = platform.system()
    if system == "Windows":
        return "windows"
    elif system == "Linux":
        return "linux"
    elif system == "Darwin":
        return "macos"
    else:
        return "unknown"


def getArch():
    """
    Get the machine architecture.
    :return: str, value in [x86_64, x86, aarch64, arm32].
    """
    arch = platform.machine()
    if arch == "x86_64" or arch == "AMD64" or arch == "amd64":
        return "x86_64"
    elif arch == "i386" or arch == "i686" or arch == "x86":
        return "x86"
    elif arch == "aarch64" or arch == "arm64":
        return "aarch64"
    elif arch.find("arm") != -1:
        return "arm32"
    else:
        return "unknown"


class DataStringProcessor:
    def __init__(self, data: Data):
        self.data = data
        self.columns = self.__getENV()

    @staticmethod
    def __getENV() -> int:
        if getOS() == "linux":
            _, columns_str = os.popen('stty size', 'r').read().split()
            columns = int(columns_str)
        else:
            # macOS default terminal size is 80 columns
            columns = 80
        return columns

    def __dropLongString(self, string: str) -> str:
        """
        Drop the string if it's too long to fit in the terminal.
        :param string: str, the input string.
        :return: str, the shortened string, do not include newline char.
        """
        if len(string) >= self.columns:
            return f"{string[:self.columns-1]}"
        else:
            return f"{string}"

    def getTitle(self) -> str:
        return f" {self.data.title}\n"

    def getLine(self) -> str:
        return f" {'-'*len(self.data.title)}\n"

    def getOS(self) -> str:
        os_str = f" OS: {self.data.OS}"
        return f"{self.__dropLongString(os_str)}\n"

    def getHost(self) -> str:
        host_str = f" Host: {self.data.Host}"
        return f"{self.__dropLongString(host_str)}\n"

    def getKernel(self) -> str:
        kernel_str = f" Kernel: {self.data.Kernel}"
        return f"{self.__dropLongString(kernel_str)}\n"

    def getUptime(self) -> str:
        uptime_str = f" Uptime: {self.data.Uptime}"
        return f"{self.__dropLongString(uptime_str)}\n"

    def getShell(self) -> str:
        shell_str = f" Shell: {self.data.Shell}"
        return f"{self.__dropLongString(shell_str)}\n"

    def getCPU(self) -> str:
        cpu_str = f" CPU: {self.data.CPU}"
        return f"{self.__dropLongString(cpu_str)}\n"

    def getGPU(self) -> str:
        ret_str = ""
        for gpu in self.data.GPU:
            gpu_str = f" GPU: {gpu}"
            ret_str += f"{self.__dropLongString(gpu_str)}\n"
        return ret_str

    def getMemory(self) -> str:
        memory_str = f" Memory: {self.data.Memory}"
        return f"{self.__dropLongString(memory_str)}\n"

    def getNIC(self) -> str:
        ret_str = ""
        for nic in self.data.NIC:
            nic_str = f" NIC: {nic}"
            ret_str += f"{self.__dropLongString(nic_str)}\n"
        return ret_str

    def getNPU(self) -> str:
        ret_str = ""
        for npu in self.data.NPU:
            npu_str = f" NPU: {npu}"
            ret_str += f"{self.__dropLongString(npu_str)}\n"
        return ret_str


def createDataString(data: Data):
    data_string_processor = DataStringProcessor(data)
    data_string = ""
    data_string += data_string_processor.getTitle()
    data_string += data_string_processor.getLine()
    data_string += data_string_processor.getOS()
    data_string += data_string_processor.getHost()
    data_string += data_string_processor.getKernel()
    data_string += data_string_processor.getUptime()
    data_string += data_string_processor.getShell()
    data_string += data_string_processor.getCPU()
    data_string += data_string_processor.getGPU()
    data_string += data_string_processor.getMemory()
    data_string += data_string_processor.getNIC()
    data_string += data_string_processor.getNPU()
    return data_string


def createDataStringOld(data: Data):
    data_string = ""
    data_string += f" {data.title}\n"
    data_string += f" {'-'*len(data.title)}\n"
    data_string += f" OS: {data.OS}\n"
    data_string += f" Host: {data.Host}\n"
    data_string += f" Kernel: {data.Kernel}\n"
    data_string += f" Uptime: {data.Uptime}\n"
    data_string += f" Shell: {data.Shell}\n"
    data_string += f" CPU: {data.CPU}\n"
    for gpu in data.GPU:
        data_string += f" GPU: {gpu}\n"
    data_string += f" Memory: {data.Memory}\n"
    for nic in data.NIC:
        data_string += f" NIC: {nic}\n"
    for npu in data.NPU:
        data_string += f" NPU: {npu}\n"
    return data_string


@dataclass
class SupportedOS:
    ColorConfig = ["armbian", "arch", "alpine", "centos", "debian", "fedora", "macOS", "raspbian", "ubuntu"]
    AsciiLogo = ["armbian", "arch", "alpine", "centos", "debian", "fedora", "macOS", "raspbian", "ubuntu"]


def selectOSLogo(os_id: str):
    """
    Select the logo based on the os id and terminal size.
    :param os_id: str, os id.
    :return: str, logo id.
    """
    if getOS() == "macos":
        return os_id
    if os_id in SupportedOS.ColorConfig and os_id in SupportedOS.AsciiLogo:
        pass
    else:
        return "linux"
    rows_str, columns_str = os.popen('stty size', 'r').read().split()
    rows = int(rows_str)
    columns = int(columns_str)
    if columns <= 80:
        if os_id in ["fedora", "ubuntu"]:
            return f"{os_id}_small"
        else:
            return os_id
    else:
        return os_id

