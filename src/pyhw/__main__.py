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
import multiprocessing


def detect_title(os, result_dict):
    result_dict["title"] = TitleDetect(os=os).getTitle().title


def detect_host(os, result_dict):
    result_dict["Host"] = HostDetect(os=os).getHostInfo().model


def detect_kernel(os, result_dict):
    result_dict["Kernel"] = KernelDetect(os=os).getKernelInfo().kernel


def detect_shell(os, result_dict):
    result_dict["Shell"] = ShellDetect(os=os).getShellInfo().info


def detect_uptime(os, result_dict):
    result_dict["Uptime"] = UptimeDetect(os=os).getUptime().uptime


def detect_os(os, result_dict):
    result_dict["OS"] = OSDetect(os=os).getOSInfo().prettyName


def detect_cpu(os, result_dict):
    result_dict["CPU"] = CPUDetect(os=os).getCPUInfo().cpu


def detect_gpu(os, result_dict):
    gpu_info = GPUDetect(os=os).getGPUInfo()
    if gpu_info.number > 0:
        result_dict["GPU"] = gpu_info.gpus


def detect_memory(os, result_dict):
    result_dict["Memory"] = MemoryDetect(os=os).getMemoryInfo().memory


def detect_nic(os, result_dict):
    nic_info = NICDetect(os=os).getNICInfo()
    if nic_info.number > 0:
        result_dict["NIC"] = nic_info.nics


def detect_npu(os, result_dict):
    npu_info = NPUDetect(os=os).getNPUInfo()
    if npu_info.number > 0:
        result_dict["NPU"] = npu_info.npus


def main():
    current_os = getOS()
    if current_os not in ["linux", "macos", "freebsd", "windows"]:
        print(f"Only Linux, macOS, FreeBSD, and Windows are supported for now. Current OS: {current_os}")
        return

    data = Data()

    manager = multiprocessing.Manager()
    result_dict = manager.dict()

    processes = [
        multiprocessing.Process(target=detect_title, args=(current_os, result_dict)),
        multiprocessing.Process(target=detect_host, args=(current_os, result_dict)),
        multiprocessing.Process(target=detect_kernel, args=(current_os, result_dict)),
        multiprocessing.Process(target=detect_shell, args=(current_os, result_dict)),
        multiprocessing.Process(target=detect_uptime, args=(current_os, result_dict)),
        multiprocessing.Process(target=detect_os, args=(current_os, result_dict)),
        multiprocessing.Process(target=detect_cpu, args=(current_os, result_dict)),
        multiprocessing.Process(target=detect_gpu, args=(current_os, result_dict)),
        multiprocessing.Process(target=detect_memory, args=(current_os, result_dict)),
        multiprocessing.Process(target=detect_nic, args=(current_os, result_dict)),
        multiprocessing.Process(target=detect_npu, args=(current_os, result_dict)),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

    for key, value in result_dict.items():
        setattr(data, key, value)

    logo_os = selectOSLogo(OSDetect(os=current_os).getOSInfo().id)
    Printer(logo_os=logo_os, data=createDataString(data)).cPrint()


# def main():
#     current_os = getOS()
#     if current_os not in ["linux", "macos", "freebsd", "windows"]:
#         print(f"Only Linux, macOS, FreeBSD and Windows are supported for now. Current OS: {current_os}")
#         return
#     data = Data()
#     data.title = TitleDetect(os=current_os).getTitle().title
#     data.Host = HostDetect(os=current_os).getHostInfo().model
#     data.Kernel = KernelDetect(os=current_os).getKernelInfo().kernel
#     data.Shell = ShellDetect(os=current_os).getShellInfo().info
#     data.Uptime = UptimeDetect(os=current_os).getUptime().uptime
#     data.OS = OSDetect(os=current_os).getOSInfo().prettyName
#     data.CPU = CPUDetect(os=current_os).getCPUInfo().cpu
#     gpu_info = GPUDetect(os=current_os).getGPUInfo()
#     if gpu_info.number > 0:
#         data.GPU = gpu_info.gpus
#     data.Memory = MemoryDetect(os=current_os).getMemoryInfo().memory
#     nic_info = NICDetect(os=current_os).getNICInfo()
#     if nic_info.number > 0:
#         data.NIC = nic_info.nics
#     npu_info = NPUDetect(os=current_os).getNPUInfo()
#     if npu_info.number > 0:
#         data.NPU = npu_info.npus
#
#     Printer(logo_os=selectOSLogo(OSDetect(os=current_os).getOSInfo().id), data=createDataString(data)).cPrint()


if __name__ == "__main__":
    main()
