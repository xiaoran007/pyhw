import pytest
import subprocess
from pyhw.backend.kernel.unix import KernelDetectUnix


@pytest.fixture
def mock_uname(monkeypatch):
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout

    def mock_run(cmd, *args, **kwargs):
        if "-s" in cmd:
            return MockProcess("Linux\n")
        elif "-r" in cmd:
            return MockProcess("5.15.0-101-generic\n")
        elif "-m" in cmd:
            return MockProcess("x86_64\n")
        else:
            raise subprocess.SubprocessError()

    monkeypatch.setattr(subprocess, "run", mock_run)


def test_kernel_unix(mock_uname):
    detector = KernelDetectUnix()
    info = detector.getKernelInfo()
    assert info.name == "Linux"
    assert info.version == "5.15.0-101-generic"
    assert info.machine == "x86_64"
    assert info.kernel == "Linux 5.15.0-101-generic x86_64"


def test_kernel_unix_error(monkeypatch):
    def mock_run_error(*args, **kwargs):
        raise subprocess.SubprocessError()

    monkeypatch.setattr(subprocess, "run", mock_run_error)

    detector = KernelDetectUnix()
    info = detector.getKernelInfo()
    assert info.name == ""
    assert info.version == ""
    assert info.machine == ""
    assert info.kernel == "  "
