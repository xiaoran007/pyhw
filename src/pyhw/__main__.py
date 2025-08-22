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
from .pyhwUtil import ReleaseChecker
from .frontend.color import colorPrefix, colorSuffix, ColorSet
import multiprocessing
import argparse
import time
import functools


def timed_function(func):
    @functools.wraps(func)
    def wrapper(debug_info, os, result_dict):
        if not debug_info.get('debug', False):
            return func(debug_info, os, result_dict)

        start_time = time.time()
        result = func(debug_info, os, result_dict)
        elapsed = time.time() - start_time
        debug_dict = debug_info.get('debug_dict', {})
        if debug_dict is not None:
            debug_dict[func.__name__] = elapsed
        return result

    wrapper.__module__ = func.__module__
    return wrapper


def check_release(release_dict):
    releaseChecker = ReleaseChecker()
    release_dict["is_new_release"] = releaseChecker.check_for_updates()
    release_dict["release"] = releaseChecker.LatestVersion
    release_dict["current"] = releaseChecker.CurrentVersion
    release_dict["is_in_pipx"] = releaseChecker.isInPIPX


@timed_function
def detect_title(debug_info, os, result_dict):
    result_dict["title"] = TitleDetect(os=os).getTitle().title


@timed_function
def detect_host(debug_info, os, result_dict):
    result_dict["Host"] = HostDetect(os=os).getHostInfo().model


@timed_function
def detect_kernel(debug_info, os, result_dict):
    result_dict["Kernel"] = KernelDetect(os=os).getKernelInfo().kernel


@timed_function
def detect_shell(debug_info, os, result_dict):
    result_dict["Shell"] = ShellDetect(os=os).getShellInfo().info


@timed_function
def detect_uptime(debug_info, os, result_dict):
    result_dict["Uptime"] = UptimeDetect(os=os).getUptime().uptime


@timed_function
def detect_os(debug_info, os, result_dict):
    result_dict["OS"] = OSDetect(os=os).getOSInfo().prettyName


@timed_function
def detect_cpu(debug_info, os, result_dict):
    result_dict["CPU"] = CPUDetect(os=os).getCPUInfo().cpu


@timed_function
def detect_gpu(debug_info, os, result_dict):
    gpu_info = GPUDetect(os=os).getGPUInfo()
    if gpu_info.number > 0:
        result_dict["GPU"] = gpu_info.gpus


@timed_function
def detect_memory(debug_info, os, result_dict):
    result_dict["Memory"] = MemoryDetect(os=os).getMemoryInfo().memory


@timed_function
def detect_nic(debug_info, os, result_dict):
    nic_info = NICDetect(os=os).getNICInfo()
    if nic_info.number > 0:
        result_dict["NIC"] = nic_info.nics


@timed_function
def detect_npu(debug_info, os, result_dict):
    npu_info = NPUDetect(os=os).getNPUInfo()
    if npu_info.number > 0:
        result_dict["NPU"] = npu_info.npus


@timed_function
def detect_pci_related(debug_info, os, result_dict):
    detect_gpu(debug_info, os, result_dict)
    detect_nic(debug_info, os, result_dict)
    detect_npu(debug_info, os, result_dict)


def print_version():
    releaseChecker = ReleaseChecker(only_local=True)
    print(f"pyhw v{releaseChecker.CurrentVersion}")


def main():
    parser = argparse.ArgumentParser(description='PyHw, a neofetch-like command line tool for fetching system information')
    parser.add_argument('-v', '--version', action='store_true', help='Print version information and exit')
    parser.add_argument('-d', '--debug', action='store_true', help='Run in debug mode')

    args = parser.parse_args()

    if args.version:
        print_version()
        return

    current_os = getOS()
    if current_os not in ["linux", "macos", "freebsd", "windows"]:
        print(f"Only Linux, macOS, FreeBSD, and Windows are supported for now. Current OS: {current_os}")
        return

    data = Data()

    manager = multiprocessing.Manager()
    result_dict = manager.dict()
    release_dict = manager.dict()
    debug_dict = manager.dict() if args.debug else None
    debug_info = {'debug': args.debug, 'debug_dict': debug_dict}

    processes = [
        multiprocessing.Process(target=check_release, args=(release_dict,)),
        multiprocessing.Process(target=detect_title, args=(debug_info, current_os, result_dict)),
        multiprocessing.Process(target=detect_host, args=(debug_info, current_os, result_dict)),
        multiprocessing.Process(target=detect_kernel, args=(debug_info, current_os, result_dict)),
        multiprocessing.Process(target=detect_shell, args=(debug_info, current_os, result_dict)),
        multiprocessing.Process(target=detect_uptime, args=(debug_info, current_os, result_dict)),
        multiprocessing.Process(target=detect_os, args=(debug_info, current_os, result_dict)),
        multiprocessing.Process(target=detect_cpu, args=(debug_info, current_os, result_dict)),
        multiprocessing.Process(target=detect_memory, args=(debug_info, current_os, result_dict)),
    ]

    if current_os == "macos":
        processes.append(multiprocessing.Process(target=detect_gpu, args=(debug_info, current_os, result_dict)))
        processes.append(multiprocessing.Process(target=detect_nic, args=(debug_info, current_os, result_dict)))
        processes.append(multiprocessing.Process(target=detect_npu, args=(debug_info, current_os, result_dict)))
    else:
        processes.append(multiprocessing.Process(target=detect_pci_related, args=(debug_info, current_os, result_dict)))

    start_time = time.time()
    for process in processes:
        process.start()

    detection_time = time.time() - start_time

    for process in processes[1:]:
        process.join()

    total_time = time.time() - start_time

    for key, value in result_dict.items():
        setattr(data, key, value)

    logo_os = selectOSLogo(OSDetect(os=current_os).getOSInfo().id)
    Printer(logo_os=logo_os, data=createDataString(data)).cPrint()

    if args.debug:
        print("\n" + "="*50)
        print(f"🔍 DEBUG MODE: Timing Information")
        print("="*50)
        for func_name, elapsed in debug_dict.items():
            detection_name = func_name.replace("detect_", "")
            print(f"{detection_name:<10}: {elapsed:.4f} s")
        print("-" * 50)
        print(f"Total create time: {detection_time:.4f} s")
        print("-"*50)
        print(f"Total execution time: {total_time:.4f} s")
        print("="*50)

    timeout = 3
    processes[0].join(timeout)
    if processes[0].is_alive():
        processes[0].terminate()
        processes[0].join()
        release_dict["is_new_release"] = False
    else:
        pass

    if release_dict["is_new_release"]:
        print(f"🔔 Found a newer version: v{release_dict['release']} (current: v{release_dict['current']})")
        print("🚀 You can use the following command to upgrade:")
        if release_dict["is_in_pipx"]:
            print(f"👉 {colorPrefix(ColorSet.COLOR_MODE_BOLD)}{colorPrefix(ColorSet.COLOR_FG_YELLOW)}pipx upgrade pyhw{colorSuffix()}")
        else:
            print(f"👉 {colorPrefix(ColorSet.COLOR_MODE_BOLD)}{colorPrefix(ColorSet.COLOR_FG_YELLOW)}pip install -U pyhw{colorSuffix()}")
    # else:
    #     # debug
    #     print("🎉 You are using the latest version of pyhw!")
    #     print(f"🔔 Release: v{release_dict['release']} (current: v{release_dict['current']})")


if __name__ == "__main__":
    main()
