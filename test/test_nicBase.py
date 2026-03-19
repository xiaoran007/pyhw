import pytest
from pyhw.backend.nic.nicBase import NICDetect
from pyhw.backend.nic.nicInfo import NICInfo
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def mock_detectors(monkeypatch):
    class MockLinux:
        def getNICInfo(self):
            return "LinuxNIC"
            
    class MockMacOS:
        def getNICInfo(self):
            return "MacOSNIC"
            
    class MockBSD:
        def getNICInfo(self):
            return "BSDNIC"
            
    class MockWindows:
        def getNICInfo(self):
            return "WindowsNIC"

    import pyhw.backend.nic.linux
    import pyhw.backend.nic.macos
    import pyhw.backend.nic.bsd
    import pyhw.backend.nic.windows

    monkeypatch.setattr(pyhw.backend.nic.linux, "NICDetectLinux", MockLinux)
    monkeypatch.setattr(pyhw.backend.nic.macos, "NICDetectMacOS", MockMacOS)
    monkeypatch.setattr(pyhw.backend.nic.bsd, "NICDetectBSD", MockBSD)
    monkeypatch.setattr(pyhw.backend.nic.windows, "NICDetectWindows", MockWindows)


def test_nic_detect_linux(mock_detectors):
    detector = NICDetect("linux")
    assert detector.getNICInfo() == "LinuxNIC"


def test_nic_detect_macos(mock_detectors):
    detector = NICDetect("macos")
    assert detector.getNICInfo() == "MacOSNIC"


def test_nic_detect_bsd(mock_detectors):
    detector = NICDetect("freebsd")
    assert detector.getNICInfo() == "BSDNIC"


def test_nic_detect_windows(mock_detectors):
    detector = NICDetect("windows")
    assert detector.getNICInfo() == "WindowsNIC"


def test_nic_detect_unsupported():
    detector = NICDetect("unknown")
    with pytest.raises(OSUnsupportedException):
        detector.getNICInfo()


def test_nic_info():
    info = NICInfo()
    assert info.number == 0
    assert info.nics == []
