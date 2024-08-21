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


def createDataString(data: Data):
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
    return data_string


@dataclass
class SupportedOS:
    ColorConfig = ["debian", "fedora", "macOS", "raspbian", "ubuntu"]
    AsciiLogo = ["debian", "fedora", "macOS", "raspbian", "ubuntu"]


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

