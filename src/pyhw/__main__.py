from .frontend import Printer
from .backend import Data
from .backend.title import TitleDetect
from .backend.host import HostDetect
from .backend.kernel import KernelDetect
from .backend.shell import ShellDetect
from .backend.uptime import UptimeDetect
from .backend.os import OSDetect
from .pyhwUtil import createDataString
from .pyhwUtil import getOS


def main():
    print("This is a test version of PyHw. Currently, it only supports Linux.")
    if getOS() != "linux":
        print(f"Only Linux is supported for now. Current os: {getOS()}")
        return
    data = Data()
    data.title = TitleDetect(os="linux").getTitle().title
    data.Host = HostDetect(os="linux").getHostInfo().model
    data.Kernel = KernelDetect(os="linux").getKernelInfo().kernel
    data.Shell = ShellDetect(os="linux").getShellInfo().info
    data.Uptime = UptimeDetect(os="linux").getUptime().uptime
    data.OS = OSDetect(os="linux").getOSInfo().prettyName

    Printer(logo_os=OSDetect(os="linux").getOSInfo().id, data=createDataString(data)).cPrint()


if __name__ == "__main__":
    main()
