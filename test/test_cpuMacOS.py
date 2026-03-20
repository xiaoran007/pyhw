import pytest
from pyhw.backend.cpu.macos import CPUDetectMacOS


def test_cpu_macos_apple_silicon(monkeypatch):
    monkeypatch.setattr("pyhw.backend.cpu.macos.getArch", lambda: "aarch64")
    monkeypatch.setattr("pyhw.backend.cpu.macos.sysctlGetString", lambda x: "Apple M1" if "brand" in x else "2.4 GHz")
    monkeypatch.setattr("pyhw.backend.cpu.macos.sysctlGetInt", lambda x: 2 if "nperflevels" in x else (4 if "perflevel0" in x else 4))
    
    # Mock ctypes.CDLL to raise exception and fallback to base frequency
    def mock_cdll(*args, **kwargs):
        raise Exception()
    monkeypatch.setattr("ctypes.CDLL", mock_cdll)
    
    detector = CPUDetectMacOS()
    info = detector.getCPUInfo()
    assert info.model == "Apple M1"
    assert info.cpu == "Apple M1 (4P, 4E) @ 3.20 GHz"


def test_cpu_macos_intel(monkeypatch):
    monkeypatch.setattr("pyhw.backend.cpu.macos.getArch", lambda: "x86_64")
    
    def mock_sysctl_get_string(key):
        if key == "machdep.cpu.brand_string":
            return "Intel(R) Core(TM) i9 CPU @ 2.40GHz"
        elif key == "hw.logicalcpu_max":
            return "16"
        elif key == "hw.cpufrequency":
            return "2400000000"
        return ""
        
    monkeypatch.setattr("pyhw.backend.cpu.macos.sysctlGetString", mock_sysctl_get_string)
    
    detector = CPUDetectMacOS()
    info = detector.getCPUInfo()
    assert info.model == "Intel Core i9 CPU @ 2.40GHz"
    assert info.cores == "16"
    assert "Intel Core i9 (16) @ 2.40GHz" in info.cpu
