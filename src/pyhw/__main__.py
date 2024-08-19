from .frontend import Printer
from .backend import Data
from .backend.title import TitleDetect
from .backend.host import HostDetect
from .backend.kernel import KernelDetect
from .backend.shell import ShellDetect
from .backend.uptime import UptimeDetect
from .backend.os import OSDetect
from .backend.cpu import CPUDetect
from .backend.gpu import GPUDetect
from .backend.memory import MemoryDetect
from .pyhwUtil import createDataString
from .pyhwUtil import getOS, selectOSLogo


def main():
    print("This is a test version of PyHw. Currently, it only supports Linux. Currently there are some display issues on small terminals.")
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
    data.CPU = CPUDetect(os="linux").getCPUInfo().cpu
    gpu_info = GPUDetect(os="linux").getGPUInfo()
    if gpu_info.number > 0:
        data.GPU = gpu_info.gpus
    data.Memory = MemoryDetect(os="linux").getMemoryInfo().memory

    Printer(logo_os=selectOSLogo(OSDetect(os="linux").getOSInfo().id), data=createDataString(data)).cPrint()


if __name__ == "__main__":
    main()
