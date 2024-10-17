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
from pyhw.backend.nic import NICDetect
from pyhw.backend.npu import NPUDetect
from pyhw.pyhwUtil import createDataString
from pyhw.pyhwUtil import getOS, selectOSLogo


def main():
    current_os = getOS()
    print("This is a test version of PyHw. Currently, it only supports Linux and macOS.")
    if current_os != "linux" and current_os != "macos":
        print(f"Only Linux and macOS is supported for now. Current os: {current_os}")
        return
    data = Data()
    data.title = TitleDetect(os=current_os).getTitle().title
    data.Host = HostDetect(os=current_os).getHostInfo().model
    data.Kernel = KernelDetect(os=current_os).getKernelInfo().kernel
    data.Shell = ShellDetect(os=current_os).getShellInfo().info
    data.Uptime = UptimeDetect(os=current_os).getUptime().uptime
    data.OS = OSDetect(os=current_os).getOSInfo().prettyName
    data.CPU = CPUDetect(os=current_os).getCPUInfo().cpu
    gpu_info = GPUDetect(os=current_os).getGPUInfo()
    if gpu_info.number > 0:
        data.GPU = gpu_info.gpus
    data.Memory = MemoryDetect(os=current_os).getMemoryInfo().memory
    nic_info = NICDetect(os=current_os).getNICInfo()
    if nic_info.number > 0:
        data.NIC = nic_info.nics
    npu_info = NPUDetect(os=current_os).getNPUInfo()
    if npu_info.number > 0:
        data.NPU = npu_info.npus

    Printer(logo_os=selectOSLogo(OSDetect(os=current_os).getOSInfo().id), data=createDataString(data)).cPrint()


if __name__ == "__main__":
    main()
