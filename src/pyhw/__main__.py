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
import concurrent.futures
import queue
import argparse
import threading
import time


def check_release(release_queue):
    release_checker = ReleaseChecker()
    release_queue.put({
        "is_new_release": release_checker.check_for_updates(),
        "release": release_checker.LatestVersion,
        "current": release_checker.CurrentVersion,
        "is_in_pipx": release_checker.isInPIPX,
    })


def detect_title(os):
    return {"title": TitleDetect(os=os).getTitle().title}


def detect_host(os):
    return {"Host": HostDetect(os=os).getHostInfo().model}


def detect_kernel(os):
    return {"Kernel": KernelDetect(os=os).getKernelInfo().kernel}


def detect_shell(os):
    return {"Shell": ShellDetect(os=os).getShellInfo().info}


def detect_uptime(os):
    return {"Uptime": UptimeDetect(os=os).getUptime().uptime}


def detect_os(os):
    return {"OS": OSDetect(os=os).getOSInfo().prettyName}


def detect_cpu(os):
    return {"CPU": CPUDetect(os=os).getCPUInfo().cpu}


def detect_gpu(os):
    gpu_info = GPUDetect(os=os).getGPUInfo()
    if gpu_info.number > 0:
        return {"GPU": gpu_info.gpus}
    return {}


def detect_memory(os):
    return {"Memory": MemoryDetect(os=os).getMemoryInfo().memory}


def detect_nic(os):
    nic_info = NICDetect(os=os).getNICInfo()
    if nic_info.number > 0:
        return {"NIC": nic_info.nics}
    return {}


def detect_npu(os):
    npu_info = NPUDetect(os=os).getNPUInfo()
    if npu_info.number > 0:
        return {"NPU": npu_info.npus}
    return {}


def detect_pci_related(os):
    result = {}
    result.update(detect_gpu(os))
    result.update(detect_nic(os))
    result.update(detect_npu(os))
    return result


def run_detector(name, func, os):
    start_time = time.time()
    try:
        return name, func(os), time.time() - start_time, None
    except Exception as exc:
        return name, {}, time.time() - start_time, repr(exc)


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

    release_queue = queue.Queue()
    release_thread = threading.Thread(target=check_release, args=(release_queue,), daemon=True)

    detector_tasks = [
        ("title", detect_title),
        ("host", detect_host),
        ("kernel", detect_kernel),
        ("shell", detect_shell),
        ("uptime", detect_uptime),
        ("os", detect_os),
        ("cpu", detect_cpu),
        ("memory", detect_memory),
    ]

    if current_os == "macos":
        detector_tasks.extend([
            ("gpu", detect_gpu),
            ("nic", detect_nic),
            ("npu", detect_npu),
        ])
    else:
        detector_tasks.append(("pci_related", detect_pci_related))

    start_time = time.time()
    release_thread.start()
    result_dict = {}
    debug_dict = {}
    detector_errors = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(detector_tasks)) as executor:
        futures = [
            executor.submit(run_detector, name, func, current_os)
            for name, func in detector_tasks
        ]
        for future in concurrent.futures.as_completed(futures):
            name, result, elapsed, error = future.result()
            if error is None:
                result_dict.update(result)
            else:
                detector_errors.append(f"{name}: {error}")
            if args.debug:
                debug_dict[name] = elapsed

    detection_time = time.time() - start_time
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
            print(f"{func_name:<10}: {elapsed:.4f} s")
        for error in detector_errors:
            print(f"error     : {error}")
        print("-" * 50)
        print(f"Total detection time: {detection_time:.4f} s")
        print("-"*50)
        print(f"Total execution time: {total_time:.4f} s")
        print("="*50)

    try:
        release_dict = release_queue.get(timeout=3)
    except queue.Empty:
        release_dict = {"is_new_release": False}

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
