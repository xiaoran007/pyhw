import pytest
from pyhw.backend.memory.memoryBase import MemoryDetect
from pyhw.backend.memory.memoryInfo import MemoryInfo
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def mock_detectors(monkeypatch):
    class MockLinux:
        def getMemoryInfo(self):
            return "LinuxMemory"
            
    class MockMacOS:
        def getMemoryInfo(self):
            return "MacOSMemory"
            
    class MockBSD:
        def getMemoryInfo(self):
            return "BSDMemory"
            
    class MockWindows:
        def getMemoryInfo(self):
            return "WindowsMemory"

    import pyhw.backend.memory.linux
    import pyhw.backend.memory.macos
    import pyhw.backend.memory.bsd
    import pyhw.backend.memory.windows

    monkeypatch.setattr(pyhw.backend.memory.linux, "MemoryDetectLinux", MockLinux)
    monkeypatch.setattr(pyhw.backend.memory.macos, "MemoryDetectMacOS", MockMacOS)
    monkeypatch.setattr(pyhw.backend.memory.bsd, "MemoryDetectBSD", MockBSD)
    monkeypatch.setattr(pyhw.backend.memory.windows, "MemoryDetectWindows", MockWindows)


def test_memory_detect_linux(mock_detectors):
    detector = MemoryDetect("linux")
    assert detector.getMemoryInfo() == "LinuxMemory"


def test_memory_detect_macos(mock_detectors):
    detector = MemoryDetect("macos")
    assert detector.getMemoryInfo() == "MacOSMemory"


def test_memory_detect_bsd(mock_detectors):
    detector = MemoryDetect("freebsd")
    assert detector.getMemoryInfo() == "BSDMemory"


def test_memory_detect_windows(mock_detectors):
    detector = MemoryDetect("windows")
    assert detector.getMemoryInfo() == "WindowsMemory"


def test_memory_detect_unsupported():
    detector = MemoryDetect("unknown")
    with pytest.raises(OSUnsupportedException):
        detector.getMemoryInfo()


def test_memory_info():
    info = MemoryInfo()
    assert info.memory == ""
    assert info.total == 0
    assert info.available == 0
    assert info.used == 0
