import pytest
import subprocess
from pyhw.backend.os.macos import OSDetectMacOS


@pytest.fixture
def mock_sw_vers(monkeypatch):
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout

    def mock_run(cmd, *args, **kwargs):
        return MockProcess("ProductName:    macOS\nProductVersion: 14.2.1\nBuildVersion:   23C71\n")

    monkeypatch.setattr(subprocess, "run", mock_run)
    monkeypatch.setattr("pyhw.backend.os.macos.getArch", lambda: "aarch64")


def test_os_macos(mock_sw_vers):
    detector = OSDetectMacOS()
    info = detector.getOSInfo()
    
    assert info.id == "macOS"
    assert "macOS Sonoma 14.2.1 23C71 arm64" in info.prettyName


def test_os_macos_no_version_name(monkeypatch):
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout

    def mock_run(cmd, *args, **kwargs):
        return MockProcess("ProductName:    macOS\nProductVersion: 10.15.7\nBuildVersion:   19H15\n")

    monkeypatch.setattr(subprocess, "run", mock_run)
    monkeypatch.setattr("pyhw.backend.os.macos.getArch", lambda: "x86_64")
    
    detector = OSDetectMacOS()
    info = detector.getOSInfo()
    
    assert info.id == "macOS"
    assert "macOS 10.15.7 19H15 x86_64" in info.prettyName


def test_os_macos_error(monkeypatch):
    def mock_run_error(*args, **kwargs):
        raise subprocess.SubprocessError()

    monkeypatch.setattr(subprocess, "run", mock_run_error)
    monkeypatch.setattr("pyhw.backend.os.macos.getArch", lambda: "x86_64")
    
    detector = OSDetectMacOS()
    info = detector.getOSInfo()
    
    assert info.id == "macOS"
    # Should format correctly with empty versions
    assert "   x86_64" in info.prettyName
