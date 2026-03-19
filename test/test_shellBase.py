import pytest
from pyhw.backend.shell.shellBase import ShellDetect
from pyhw.backend.shell.shellInfo import ShellInfo
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def mock_detectors(monkeypatch):
    class MockUnix:
        def getShellInfo(self):
            return "UnixShell"
            
    class MockWindows:
        def getShellInfo(self):
            return "WindowsShell"

    import pyhw.backend.shell.unix
    import pyhw.backend.shell.windows

    monkeypatch.setattr(pyhw.backend.shell.unix, "ShellDetectUnix", MockUnix)
    monkeypatch.setattr(pyhw.backend.shell.windows, "ShellDetectWindows", MockWindows)


def test_shell_detect_linux(mock_detectors):
    detector = ShellDetect("linux")
    assert detector.getShellInfo() == "UnixShell"


def test_shell_detect_macos(mock_detectors):
    detector = ShellDetect("macos")
    assert detector.getShellInfo() == "UnixShell"


def test_shell_detect_bsd(mock_detectors):
    detector = ShellDetect("freebsd")
    assert detector.getShellInfo() == "UnixShell"


def test_shell_detect_windows(mock_detectors):
    detector = ShellDetect("windows")
    assert detector.getShellInfo() == "WindowsShell"


def test_shell_detect_unsupported():
    detector = ShellDetect("unknown")
    with pytest.raises(OSUnsupportedException):
        detector.getShellInfo()


def test_shell_info():
    info = ShellInfo()
    assert info.shell == ""
    assert info.version == ""
