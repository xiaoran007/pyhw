from pyhw.frontend import Printer
import os
import platform
import psutil
from pyhw.backend import Data
from pyhw.backend.title import TitleDetect
from pyhw.backend.host import HostDetect
from pyhw.backend.kernel import KernelDetect
from pyhw.backend.shell import ShellDetect
from pyhw.backend.uptime import UptimeDetect
from pyhw.backend.os import OSDetect
from pyhw.pyhwUtil import createDataString


data = Data()
data.title = TitleDetect(os="linux").getTitle().title
data.Host = HostDetect(os="linux").getHostInfo().model
data.Kernel = KernelDetect(os="linux").getKernelInfo().kernel
data.Shell = ShellDetect(os="linux").getShellInfo().info
data.Uptime = UptimeDetect(os="linux").getUptime().uptime
data.OS = OSDetect(os="linux").getOSInfo().prettyName

Printer(logo_os=OSDetect(os="linux").getOSInfo().id, data=createDataString(data)).cPrint()

