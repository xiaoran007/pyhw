import pytest
import platform
import subprocess
from pyhw.pyhwUtil.pyhwUtil import (
    getOS, getArch, getDocker, getWSL, 
    DataStringProcessor, createDataString, createDataStringOld, selectOSLogo
)
from pyhw.backend.backendBase import Data


@pytest.fixture
def data_instance():
    data = Data()
    data.title = "Test User@Host"
    data.OS = "TestOS"
    data.Host = "TestHost"
    data.Kernel = "TestKernel"
    data.Uptime = "1 day"
    data.Shell = "zsh"
    data.CPU = "TestCPU"
    data.GPU = ["TestGPU1", "TestGPU2"]
    data.Memory = "16GB"
    data.NIC = ["TestNIC1"]
    data.NPU = ["TestNPU"]
    return data


@pytest.mark.parametrize("system_val, expected", [
    ("Windows", "windows"),
    ("Linux", "linux"),
    ("Darwin", "macos"),
    ("FreeBSD", "freebsd"),
    ("UnknownOS", "unknown"),
])
def test_getOS(monkeypatch, system_val, expected):
    monkeypatch.setattr(platform, "system", lambda: system_val)
    assert getOS() == expected


@pytest.mark.parametrize("machine_val, expected", [
    ("x86_64", "x86_64"),
    ("AMD64", "x86_64"),
    ("amd64", "x86_64"),
    ("i386", "x86"),
    ("i686", "x86"),
    ("x86", "x86"),
    ("aarch64", "aarch64"),
    ("arm64", "aarch64"),
    ("armv7l", "arm32"),
    ("riscv64", "riscv64"),
    ("s390x", "s390x"),
    ("ppc64le", "ppc64le"),
    ("mips64", "mips64"),
    ("unknown_arch", "unknown"),
])
def test_getArch(monkeypatch, machine_val, expected):
    monkeypatch.setattr(platform, "machine", lambda: machine_val)
    assert getArch() == expected


def test_getDocker(monkeypatch, tmp_path):
    monkeypatch.setattr("os.path.exists", lambda p: p == "/.dockerenv")
    assert getDocker() is True
    
    monkeypatch.setattr("os.path.exists", lambda p: False)
    assert getDocker() is False


def test_getWSL(monkeypatch):
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout

    def mock_run(cmd, *args, **kwargs):
        if "uname" in cmd:
            return MockProcess("5.10.16.3-microsoft-standard-WSL2\n")
        raise subprocess.SubprocessError()

    monkeypatch.setattr(subprocess, "run", mock_run)
    assert getWSL() is True

    def mock_run_no_wsl(cmd, *args, **kwargs):
        if "uname" in cmd:
            return MockProcess("5.10.0-10-amd64\n")
        raise subprocess.SubprocessError()

    monkeypatch.setattr(subprocess, "run", mock_run_no_wsl)
    assert getWSL() is False

    def mock_run_error(cmd, *args, **kwargs):
        raise subprocess.SubprocessError()

    monkeypatch.setattr(subprocess, "run", mock_run_error)
    assert getWSL() is False


def test_DataStringProcessor(data_instance, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")  # macos defaults to 80 cols
    processor = DataStringProcessor(data_instance)
    
    assert processor.getTitle() == " Test User@Host\n"
    assert processor.getLine() == " --------------\n"
    assert processor.getOS() == " OS: TestOS\n"
    assert "GPU: TestGPU1" in processor.getGPU()
    assert "GPU: TestGPU2" in processor.getGPU()
    assert "NIC: TestNIC1" in processor.getNIC()
    assert "NPU: TestNPU" in processor.getNPU()


def test_createDataString(data_instance, monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    res = createDataString(data_instance)
    assert "Test User@Host" in res
    assert "OS: TestOS" in res
    assert "GPU: TestGPU1" in res
    assert "NPU: TestNPU" in res


def test_createDataStringOld(data_instance):
    res = createDataStringOld(data_instance)
    assert "Test User@Host" in res
    assert "OS: TestOS" in res
    assert "GPU: TestGPU1" in res
    assert "NPU: TestNPU" in res


def test_selectOSLogo_macos(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    assert selectOSLogo("some_id") == "some_id"


def test_selectOSLogo_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    assert selectOSLogo("windows_10") == "windows_10"
    assert selectOSLogo("invalid_id") == "windows_11"


def test_selectOSLogo_linux(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout

    def mock_run_small(cmd, *args, **kwargs):
        return MockProcess("24 60\n")

    monkeypatch.setattr(subprocess, "run", mock_run_small)
    assert selectOSLogo("ubuntu") == "ubuntu_small"
    
    def mock_run_large(cmd, *args, **kwargs):
        return MockProcess("24 100\n")

    monkeypatch.setattr(subprocess, "run", mock_run_large)
    assert selectOSLogo("ubuntu") == "ubuntu"
    
    def mock_run_error(cmd, *args, **kwargs):
        raise subprocess.SubprocessError()
        
    monkeypatch.setattr(subprocess, "run", mock_run_error)
    assert selectOSLogo("ubuntu") == "ubuntu_small"  # fallback to 80cols -> small
    assert selectOSLogo("invalid_id") == "linux"
