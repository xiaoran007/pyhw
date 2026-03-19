import pytest
import os
import subprocess
from pyhw.backend.shell.unix import ShellDetectUnix


def test_shell_unix_normal_bash(monkeypatch):
    monkeypatch.setattr("pyhw.backend.shell.unix.getDocker", lambda: False)
    monkeypatch.setattr(os, "getenv", lambda k, d="": "/bin/bash" if k == "SHELL" else d)
    
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout

    def mock_run(cmd, *args, **kwargs):
        if "BASH_VERSION" in cmd[2]:
            return MockProcess("5.1.16(1)-release\n")
        raise subprocess.SubprocessError()

    monkeypatch.setattr(subprocess, "run", mock_run)

    detector = ShellDetectUnix()
    info = detector.getShellInfo()
    
    assert info.shell == "bash"
    assert info.version == "5.1.16"
    assert info.info == "bash 5.1.16"


def test_shell_unix_normal_zsh(monkeypatch):
    monkeypatch.setattr("pyhw.backend.shell.unix.getDocker", lambda: False)
    monkeypatch.setattr(os, "getenv", lambda k, d="": "/bin/zsh" if k == "SHELL" else d)
    
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout

    def mock_run(cmd, *args, **kwargs):
        if "ZSH_VERSION" in cmd[2]:
            return MockProcess("5.8.1\n")
        raise subprocess.SubprocessError()

    monkeypatch.setattr(subprocess, "run", mock_run)

    detector = ShellDetectUnix()
    info = detector.getShellInfo()
    
    assert info.shell == "zsh"
    assert info.version == "5.8.1"
    assert info.info == "zsh 5.8.1"


def test_shell_unix_docker(monkeypatch):
    monkeypatch.setattr("pyhw.backend.shell.unix.getDocker", lambda: True)
    
    mock_passwd = [
        "root:x:0:0:root:/root:/bin/ash"
    ]

    class MockFile:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def __iter__(self):
            return iter(mock_passwd)

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())

    detector = ShellDetectUnix()
    info = detector.getShellInfo()
    
    assert info.shell == "ash"
    assert info.version == ""
    assert info.info == "ash "


def test_shell_unix_error(monkeypatch):
    monkeypatch.setattr("pyhw.backend.shell.unix.getDocker", lambda: False)
    monkeypatch.setattr(os, "getenv", lambda k, d="": "")
    
    detector = ShellDetectUnix()
    info = detector.getShellInfo()
    
    assert info.shell == ""
    assert info.version == ""
    assert info.info == " "
