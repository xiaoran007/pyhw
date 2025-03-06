from .cpuInfo import CPUInfo
from ...pyhwUtil import sysctlGetString, sysctlGetInt, getArch


class CPUDetectMacOS:
    def __init__(self):
        self.__cpuInfo = CPUInfo()
        self.__arch = getArch()
        self.__pCore = 0
        self.__eCore = 0

    def getCPUInfo(self):
        if self.__arch == "aarch64":
            self.__getCPUModel()
            self.__AppleSiliconBaseFrequency()
            self.__handleAppleSilicon()
            self.__cpuInfo.cpu = f"{self.__cpuInfo.model} ({self.__pCore}P, {self.__eCore}E) @ {self.__cpuInfo.frequency}"
        else:
            self.__getCPUModel()
            self.__getCPUCores()
            self.__getCPUFrequency()
            # need test on Intel Macs.
            self.__cpuInfo.cpu = f"{self.__cpuInfo.model.replace('CPU', f'({self.__cpuInfo.cores})')}"
        return self.__cpuInfo

    def __getCPUModel(self):
        model = sysctlGetString("machdep.cpu.brand_string")
        model = model.replace("(R)", "")
        model = model.replace("(TM)", "")
        self.__cpuInfo.model = model

    def __getCPUCores(self):
        cores = sysctlGetString("hw.logicalcpu_max")
        self.__cpuInfo.cores = cores

    def __getCPUFrequency(self):
        # sysctl doesn't provide the exact CPU frequency on Apple Silicon Macs, there are some indirect methods
        # to get the CPU frequency, but can not integrate with Python directly.
        # C-Based helper module will be added later.
        # See https://github.com/fastfetch-cli/fastfetch/blob/dev/src/detection/cpu/cpu_apple.c for more details.
        freq = sysctlGetString("hw.cpufrequency")
        self.__cpuInfo.frequency = freq

    def __handleAppleSilicon(self):
        nlevels = sysctlGetInt("hw.nperflevels")
        if nlevels is not None and nlevels == 2:    # currently, Apple Silicon chip only has 2 performance levels.
            pcore = sysctlGetInt("hw.perflevel0.logicalcpu_max")    # level 0 is P-core
            ecore = sysctlGetInt("hw.perflevel1.logicalcpu_max")    # level 1 is E-core
            if pcore is not None and ecore is not None:
                self.__pCore = pcore
                self.__eCore = ecore

    def __AppleSiliconBaseFrequency(self):
        # see https://en.wikipedia.org/wiki/Apple_silicon#M_series for more details.
        # https://eclecticlight.co/2025/01/20/what-are-cpu-core-frequencies-in-apple-silicon-macs/
        freq = {
            "Apple M1": "3.20 GHz",
            "Apple M1 Pro": "3.23 GHz",
            "Apple M1 Max": "3.23 GHz",
            "Apple M1 Ultra": "3.23 GHz",
            "Apple M2": "3.50 GHz",
            "Apple M2 Pro": "3.50 GHz",
            "Apple M2 Max": "3.69 GHz",
            "Apple M2 Ultra": "3.70 Ghz",
            "Apple M3": "4.05 GHz",
            "Apple M3 Pro": "4.05 GHz",
            "Apple M3 Max": "4.05 GHz",
            "Apple M3 Ultra": "4.05 GHz",  # Need more info
            "Apple M4": "4.40 GHz",
            "Apple M4 Pro": "4.51 GHz",
            "Apple M4 Max": "4.51 GHz"
        }
        self.__cpuInfo.frequency = freq.get(self.__cpuInfo.model, "Unknown")
