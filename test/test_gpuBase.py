import pytest
from pyhw.backend.gpu.gpuBase import GPUDetect
from pyhw.backend.gpu.gpuInfo import GPUInfo
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def mock_detectors(monkeypatch):
    class MockLinux:
        def getGPUInfo(self):
            return "LinuxGPU"
            
    class MockMacOS:
        def getGPUInfo(self):
            return "MacOSGPU"
            
    class MockBSD:
        def getGPUInfo(self):
            return "BSDGPU"
            
    class MockWindows:
        def getGPUInfo(self):
            return "WindowsGPU"

    import pyhw.backend.gpu.linux
    import pyhw.backend.gpu.macos
    import pyhw.backend.gpu.bsd
    import pyhw.backend.gpu.windows

    monkeypatch.setattr(pyhw.backend.gpu.linux, "GPUDetectLinux", MockLinux)
    monkeypatch.setattr(pyhw.backend.gpu.macos, "GPUDetectMacOS", MockMacOS)
    monkeypatch.setattr(pyhw.backend.gpu.bsd, "GPUDetectBSD", MockBSD)
    monkeypatch.setattr(pyhw.backend.gpu.windows, "GPUDetectWindows", MockWindows)


def test_gpu_detect_linux(mock_detectors):
    detector = GPUDetect("linux")
    assert detector.getGPUInfo() == "LinuxGPU"


def test_gpu_detect_macos(mock_detectors):
    detector = GPUDetect("macos")
    assert detector.getGPUInfo() == "MacOSGPU"


def test_gpu_detect_bsd(mock_detectors):
    detector = GPUDetect("freebsd")
    assert detector.getGPUInfo() == "BSDGPU"


def test_gpu_detect_windows(mock_detectors):
    detector = GPUDetect("windows")
    assert detector.getGPUInfo() == "WindowsGPU"


def test_gpu_detect_unsupported():
    detector = GPUDetect("unknown")
    with pytest.raises(OSUnsupportedException):
        detector.getGPUInfo()


def test_gpu_info():
    info = GPUInfo()
    assert info.number == 0
    assert info.gpus == []
