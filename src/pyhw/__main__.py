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
from .backend.nic import NICDetect
from .backend.npu import NPUDetect
from .pyhwUtil import createDataString
from .pyhwUtil import getOS, selectOSLogo


def main():
    current_os = getOS()
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
