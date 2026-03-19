import pytest
import sys
from pyhw.backend.host.hostBase import HostDetect
from pyhw.backend.host.hostInfo import HostInfo
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def mock_detectors(monkeypatch):
    class MockLinux:
        def getHostInfo(self):
            return "LinuxHost"
            
    class MockMacOS:
        def getHostInfo(self):
            return "MacOSHost"
            
    class MockBSD:
        def getHostInfo(self):
            return "BSDHost"
            
    class MockWindows:
        def getHostInfo(self):
            return "WindowsHost"
            
    monkeypatch.setitem(sys.modules, "winreg", type("winreg", (), {}))

    import pyhw.backend.host.linux
    import pyhw.backend.host.macos
    import pyhw.backend.host.bsd
    import pyhw.backend.host.windows

    monkeypatch.setattr(pyhw.backend.host.linux, "HostDetectLinux", MockLinux)
    monkeypatch.setattr(pyhw.backend.host.macos, "HostDetectMacOS", MockMacOS)
    monkeypatch.setattr(pyhw.backend.host.bsd, "HostDetectBSD", MockBSD)
    monkeypatch.setattr(pyhw.backend.host.windows, "HostDetectWindows", MockWindows)


def test_host_detect_linux(mock_detectors):
    detector = HostDetect("linux")
    assert detector.getHostInfo() == "LinuxHost"


def test_host_detect_macos(mock_detectors):
    detector = HostDetect("macos")
    assert detector.getHostInfo() == "MacOSHost"


def test_host_detect_bsd(mock_detectors):
    detector = HostDetect("freebsd")
    assert detector.getHostInfo() == "BSDHost"


def test_host_detect_windows(mock_detectors):
    detector = HostDetect("windows")
    assert detector.getHostInfo() == "WindowsHost"


def test_host_detect_unsupported():
    detector = HostDetect("unknown")
    with pytest.raises(OSUnsupportedException):
        detector.getHostInfo()


def test_host_info():
    info = HostInfo()
    assert info.os == ""
    assert info.model == ""
    assert info.vendor == ""
    assert info.version == ""
