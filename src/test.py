from pyhw.frontend import Printer
import os
import platform
import psutil

# System Information
system_info = {
    "User": os.getlogin(),
    "Hostname": platform.node(),
    "OS": f"{platform.system()} {platform.release()} {platform.machine()}",
    "Kernel": "macos",
    "Uptime": f"{psutil.boot_time()} seconds",
    "Packages": "208 (brew)",  # This is a placeholder, customize as needed
    "Shell": os.getenv('SHELL'),
    "Resolution": "1440x900",  # Placeholder, customize if needed
    "DE": "Aqua",
    "WM": "Quartz Compositor",
    "WM Theme": "Blue (Dark)",
    "Terminal": os.getenv('TERM'),
    "Terminal Font": "SFMono-Regular",
    "CPU": platform.processor(),
    "GPU": "Apple M1",  # Placeholder, adjust according to your machine
    "Memory": f"{psutil.virtual_memory().used // (1024 * 1024)}MiB / {psutil.virtual_memory().total // (1024 * 1024)}MiB"
}

# Prepare formatted system info
sys_info_str = f"""
{system_info['User']}@{system_info['Hostname']}
----------------------------------------
OS: {system_info['OS']}
Kernel: {system_info['Kernel']}
Uptime: {system_info['Uptime']}
Packages: {system_info['Packages']}
Shell: {system_info['Shell']}
Resolution: {system_info['Resolution']}
DE: {system_info['DE']}
WM: {system_info['WM']}
WM Theme: {system_info['WM Theme']}
Terminal: {system_info['Terminal']}
Terminal Font: {system_info['Terminal Font']}
CPU: {system_info['CPU']}
GPU: {system_info['GPU']}
Memory: {system_info['Memory']}
"""

Printer(logo_os="macOS", data=sys_info_str).cPrint()

