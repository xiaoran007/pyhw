import pytest
import subprocess
from pyhw.backend.title.unix import TitleDetectUnix


@pytest.fixture
def mock_whoami_hostname(monkeypatch):
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout

    def mock_run(cmd, *args, **kwargs):
        if cmd == ['whoami']:
            return MockProcess("testuser\n")
        elif cmd == ['hostname']:
            return MockProcess("testhost\n")
        raise subprocess.SubprocessError()

    monkeypatch.setattr(subprocess, "run", mock_run)


def test_title_unix(mock_whoami_hostname):
    detector = TitleDetectUnix()
    info = detector.getTitle()
    
    assert info.username == "testuser"
    assert info.hostname == "testhost"
    assert info.title == "testuser@testhost"


def test_title_unix_error(monkeypatch):
    def mock_run_error(*args, **kwargs):
        raise Exception()

    monkeypatch.setattr(subprocess, "run", mock_run_error)

    detector = TitleDetectUnix()
    info = detector.getTitle()
    
    assert info.username == ""
    assert info.hostname == ""
    assert info.title == ""
