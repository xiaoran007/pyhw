import pytest
import sys
from pyhw.backend.cpu.cpuBase import CPUDetect
from pyhw.backend.cpu.cpuInfo import CPUInfo
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def mock_detectors(monkeypatch):
    class MockLinux:
        def getCPUInfo(self):
            return "LinuxCPU"
            
    class MockMacOS:
        def getCPUInfo(self):
            return "MacOSCPU"
            
    class MockBSD:
        def getCPUInfo(self):
            return "BSDCPU"
            
    class MockWindows:
        def getCPUInfo(self):
            return "WindowsCPU"

    # We need to monkeypatch the imports inside the getCPUInfo method
    # Since they are local imports, we have to patch sys.modules
    import pyhw.backend.cpu.linux
    import pyhw.backend.cpu.macos
    import pyhw.backend.cpu.bsd
    import pyhw.backend.cpu.windows

    monkeypatch.setattr(pyhw.backend.cpu.linux, "CPUDetectLinux", MockLinux)
    monkeypatch.setattr(pyhw.backend.cpu.macos, "CPUDetectMacOS", MockMacOS)
    monkeypatch.setattr(pyhw.backend.cpu.bsd, "CPUDetectBSD", MockBSD)
    monkeypatch.setattr(pyhw.backend.cpu.windows, "CPUDetectWindows", MockWindows)


def test_cpu_detect_linux(mock_detectors):
    detector = CPUDetect("linux")
    assert detector.getCPUInfo() == "LinuxCPU"


def test_cpu_detect_macos(mock_detectors):
    detector = CPUDetect("macos")
    assert detector.getCPUInfo() == "MacOSCPU"


def test_cpu_detect_bsd(mock_detectors):
    detector = CPUDetect("freebsd")
    assert detector.getCPUInfo() == "BSDCPU"


def test_cpu_detect_windows(mock_detectors):
    detector = CPUDetect("windows")
    assert detector.getCPUInfo() == "WindowsCPU"


def test_cpu_detect_unsupported():
    detector = CPUDetect("unknown")
    with pytest.raises(OSUnsupportedException):
        detector.getCPUInfo()


def test_cpu_info():
    info = CPUInfo()
    assert info.cpu == ""
    assert info.model == ""
    assert info.cores == ""
    assert info.frequency == ""
