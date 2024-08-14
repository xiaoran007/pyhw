from pyhw.backend.host import HostDetect
from pyhw.backend.title import TitleDetect
from pyhw.backend.kernel import KernelDetect

ans = KernelDetect('linux').getKernelInfo()
print(ans.kernel)

