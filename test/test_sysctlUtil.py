import pytest
import subprocess
from pyhw.pyhwUtil.sysctlUtil import __sysctlGet, sysctlGetString, sysctlGetInt


@pytest.fixture
def mock_subprocess_run(monkeypatch):
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout

    def mock_run(cmd, *args, **kwargs):
        if "hw.memsize" in cmd:
            return MockProcess("17179869184\n")
        elif "hw.model" in cmd:
            return MockProcess("MacBookPro18,3\n")
        else:
            raise subprocess.SubprocessError("Mocked error")

    monkeypatch.setattr(subprocess, "run", mock_run)


def test_sysctlGet_success(mock_subprocess_run):
    assert __sysctlGet("hw.model") == "MacBookPro18,3"


def test_sysctlGet_error(mock_subprocess_run):
    assert __sysctlGet("unknown.key") == ""


def test_sysctlGetString(mock_subprocess_run):
    assert sysctlGetString("hw.model") == "MacBookPro18,3"
    assert sysctlGetString("unknown.key") == ""


def test_sysctlGetInt_success(mock_subprocess_run):
    assert sysctlGetInt("hw.memsize") == 17179869184


def test_sysctlGetInt_error(mock_subprocess_run):
    assert sysctlGetInt("hw.model") is None
    assert sysctlGetInt("unknown.key") is None
