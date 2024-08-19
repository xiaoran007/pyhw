from pyhw.frontend import Printer
from pyhw.backend import Data
from pyhw.backend.title import TitleDetect
from pyhw.backend.host import HostDetect
from pyhw.backend.kernel import KernelDetect
from pyhw.backend.shell import ShellDetect
from pyhw.backend.uptime import UptimeDetect
from pyhw.backend.os import OSDetect
from pyhw.backend.cpu import CPUDetect
from pyhw.backend.gpu import GPUDetect
from pyhw.backend.memory import MemoryDetect
from pyhw.pyhwUtil import createDataString
from pyhw.pyhwUtil import getOS, selectOSLogo


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
        print(data.GPU)
    data.Memory = MemoryDetect(os="linux").getMemoryInfo().memory

    Printer(logo_os=selectOSLogo(OSDetect(os="linux").getOSInfo().id), data=createDataString(data)).cPrint()


if __name__ == "__main__":
    main()
