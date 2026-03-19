import pytest
import sys
from pyhw.backend.uptime.uptimeBase import UptimeDetect
from pyhw.backend.uptime.uptimeInfo import UptimeInfo
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def mock_detectors(monkeypatch):
    class MockLinux:
        def getUptimeInfo(self):
            return "LinuxUptime"
            
    class MockMacOS:
        def getUptimeInfo(self):
            return "MacOSUptime"
            
    class MockBSD:
        def getUptimeInfo(self):
            return "BSDUptime"
            
    class MockWindows:
        def getUptimeInfo(self):
            return "WindowsUptime"

    monkeypatch.setitem(sys.modules, "winreg", type("winreg", (), {}))

    import pyhw.backend.uptime.linux
    import pyhw.backend.uptime.macos
    import pyhw.backend.uptime.bsd
    import pyhw.backend.uptime.windows

    monkeypatch.setattr(pyhw.backend.uptime.linux, "UptimeDetectLinux", MockLinux)
    monkeypatch.setattr(pyhw.backend.uptime.macos, "UptimeDetectMacOS", MockMacOS)
    monkeypatch.setattr(pyhw.backend.uptime.bsd, "UptimeDetectBSD", MockBSD)
    monkeypatch.setattr(pyhw.backend.uptime.windows, "UptimeDetectWindows", MockWindows)


def test_uptime_detect_linux(mock_detectors):
    detector = UptimeDetect("linux")
    assert detector.getUptime() == "LinuxUptime"


def test_uptime_detect_macos(mock_detectors):
    detector = UptimeDetect("macos")
    assert detector.getUptime() == "MacOSUptime"


def test_uptime_detect_bsd(mock_detectors):
    detector = UptimeDetect("freebsd")
    assert detector.getUptime() == "BSDUptime"


def test_uptime_detect_windows(mock_detectors):
    detector = UptimeDetect("windows")
    assert detector.getUptime() == "WindowsUptime"


def test_uptime_detect_unsupported():
    detector = UptimeDetect("unknown")
    with pytest.raises(OSUnsupportedException):
        detector.getUptime()


def test_uptime_info():
    info = UptimeInfo()
    assert info.uptime == ""
