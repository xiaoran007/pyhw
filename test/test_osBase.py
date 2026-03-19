import pytest
import sys
from pyhw.backend.os.osBase import OSDetect
from pyhw.backend.os.osInfo import OSInfo
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def mock_detectors(monkeypatch):
    class MockLinux:
        def getOSInfo(self):
            return "LinuxOS"
            
    class MockMacOS:
        def getOSInfo(self):
            return "MacOSOS"
            
    class MockBSD:
        def getOSInfo(self):
            return "BSDOS"
            
    class MockWindows:
        def getOSInfo(self):
            return "WindowsOS"

    monkeypatch.setitem(sys.modules, "winreg", type("winreg", (), {}))

    import pyhw.backend.os.linux
    import pyhw.backend.os.macos
    import pyhw.backend.os.bsd
    import pyhw.backend.os.windows

    monkeypatch.setattr(pyhw.backend.os.linux, "OSDetectLinux", MockLinux)
    monkeypatch.setattr(pyhw.backend.os.macos, "OSDetectMacOS", MockMacOS)
    monkeypatch.setattr(pyhw.backend.os.bsd, "OSDetectBSD", MockBSD)
    monkeypatch.setattr(pyhw.backend.os.windows, "OSDetectWindows", MockWindows)


def test_os_detect_linux(mock_detectors):
    detector = OSDetect("linux")
    assert detector.getOSInfo() == "LinuxOS"


def test_os_detect_macos(mock_detectors):
    detector = OSDetect("macos")
    assert detector.getOSInfo() == "MacOSOS"


def test_os_detect_bsd(mock_detectors):
    detector = OSDetect("freebsd")
    assert detector.getOSInfo() == "BSDOS"


def test_os_detect_windows(mock_detectors):
    detector = OSDetect("windows")
    assert detector.getOSInfo() == "WindowsOS"


def test_os_detect_unsupported():
    detector = OSDetect("unknown")
    with pytest.raises(OSUnsupportedException):
        detector.getOSInfo()


def test_os_info():
    info = OSInfo()
    assert info.prettyName == ""
    assert info.version == ""
    assert info.id == ""
    assert info.name == ""
