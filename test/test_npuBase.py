import pytest
from pyhw.backend.npu.npuBase import NPUDetect
from pyhw.backend.npu.npuInfo import NPUInfo
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def mock_detectors(monkeypatch):
    class MockLinux:
        def getNPUInfo(self):
            return "LinuxNPU"
            
    class MockMacOS:
        def getNPUInfo(self):
            return "MacOSNPU"
            
    class MockBSD:
        def getNPUInfo(self):
            return "BSDNPU"
            
    class MockWindows:
        def getNPUInfo(self):
            return "WindowsNPU"

    import pyhw.backend.npu.linux
    import pyhw.backend.npu.macos
    import pyhw.backend.npu.bsd
    import pyhw.backend.npu.windows

    monkeypatch.setattr(pyhw.backend.npu.linux, "NPUDetectLinux", MockLinux)
    monkeypatch.setattr(pyhw.backend.npu.macos, "NPUDetectMacOS", MockMacOS)
    monkeypatch.setattr(pyhw.backend.npu.bsd, "NPUDetectBSD", MockBSD)
    monkeypatch.setattr(pyhw.backend.npu.windows, "NPUDetectWindows", MockWindows)


def test_npu_detect_linux(mock_detectors):
    detector = NPUDetect("linux")
    assert detector.getNPUInfo() == "LinuxNPU"


def test_npu_detect_macos(mock_detectors):
    detector = NPUDetect("macos")
    assert detector.getNPUInfo() == "MacOSNPU"


def test_npu_detect_bsd(mock_detectors):
    detector = NPUDetect("freebsd")
    assert detector.getNPUInfo() == "BSDNPU"


def test_npu_detect_windows(mock_detectors):
    detector = NPUDetect("windows")
    assert detector.getNPUInfo() == "WindowsNPU"


def test_npu_detect_unsupported():
    detector = NPUDetect("unknown")
    with pytest.raises(OSUnsupportedException):
        detector.getNPUInfo()


def test_npu_info():
    info = NPUInfo()
    assert info.number == 0
    assert info.npus == []
