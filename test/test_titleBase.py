import pytest
from pyhw.backend.title.titleBase import TitleDetect
from pyhw.backend.title.titleInfo import TitleInfo
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def mock_detectors(monkeypatch):
    class MockUnix:
        def getTitle(self):
            return "UnixTitle"
            
    class MockWindows:
        def getTitle(self):
            return "WindowsTitle"

    import pyhw.backend.title.unix
    import pyhw.backend.title.windows

    monkeypatch.setattr(pyhw.backend.title.unix, "TitleDetectUnix", MockUnix)
    monkeypatch.setattr(pyhw.backend.title.windows, "TitleDetectWindows", MockWindows)


def test_title_detect_linux(mock_detectors):
    detector = TitleDetect("linux")
    assert detector.getTitle() == "UnixTitle"


def test_title_detect_macos(mock_detectors):
    detector = TitleDetect("macos")
    assert detector.getTitle() == "UnixTitle"


def test_title_detect_bsd(mock_detectors):
    detector = TitleDetect("freebsd")
    assert detector.getTitle() == "UnixTitle"


def test_title_detect_windows(mock_detectors):
    detector = TitleDetect("windows")
    assert detector.getTitle() == "WindowsTitle"


def test_title_detect_unsupported():
    detector = TitleDetect("unknown")
    with pytest.raises(OSUnsupportedException):
        detector.getTitle()


def test_title_info():
    info = TitleInfo()
    assert info.username == ""
    assert info.hostname == ""
    assert info.title == ""
