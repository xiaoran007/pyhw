import platform
from ..backend import Data

def getOS():
    """
    Get the os type in lower case.
    :return: str, os type.
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
    elif arch == "aarch64":
        return "aarch64"
    elif arch.find("arm") != -1:
        return "arm32"
    else:
        return "unknown"


def createDataString(data: Data):
    data_string = f"""
    {data.title}
    {"-"*len(data.title)}
    OS: {data.OS}
    Host: {data.Host}
    Kernel: {data.Kernel}
    Uptime: {data.Uptime}
    Shell: {data.Shell}
    CPU: {data.CPU}
    GPU: {data.GPU[0]}
    Memory: {data.Memory}
    """
    return data_string
