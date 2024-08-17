from pyhw.frontend import Printer
import os
import platform
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


data = Data()
data.title = TitleDetect(os="linux").getTitle().title
data.Host = HostDetect(os="linux").getHostInfo().model
data.Kernel = KernelDetect(os="linux").getKernelInfo().kernel
data.Shell = ShellDetect(os="linux").getShellInfo().info
data.Uptime = UptimeDetect(os="linux").getUptime().uptime
data.OS = OSDetect(os="linux").getOSInfo().prettyName
data.CPU = CPUDetect(os="linux").getCPUInfo().cpu
if GPUDetect(os="linux").getGPUInfo().number > 0:
    data.GPU = GPUDetect(os="linux").getGPUInfo().gpus
data.Memory = MemoryDetect(os="linux").getMemoryInfo().memory

Printer(logo_os=OSDetect(os="linux").getOSInfo().id, data=createDataString(data)).cPrint()
# Printer(logo_os="macOS", data=createDataString(data)).cPrint()

