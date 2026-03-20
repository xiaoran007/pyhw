import pytest
import subprocess
import json
import os
from pyhw.backend.shell.windows import ShellDetectWindows


def test_shell_windows_powershell(monkeypatch):
    monkeypatch.setattr(os, "getenv", lambda k, d="": "")
    class MockProcess:
        def __init__(self):
            self.stdout = json.dumps({
                "Major": 5,
                "Minor": 1
            })

    def mock_run(*args, **kwargs):
        return MockProcess()

    monkeypatch.setattr(subprocess, "run", mock_run)

    detector = ShellDetectWindows()
    info = detector.getShellInfo()
    assert info.shell == "PowerShell"
    assert info.version == "5.1"
    assert info.info == "PowerShell 5.1"


def test_shell_windows_bash(monkeypatch):
    monkeypatch.setattr(os, "getenv", lambda k, d="": "/bin/bash" if k == "SHELL" else d)
    class MockProcess:
        def __init__(self):
            self.stdout = "5.1.16(1)-release\n"

    def mock_run(*args, **kwargs):
        return MockProcess()

    monkeypatch.setattr(subprocess, "run", mock_run)

    detector = ShellDetectWindows()
    info = detector.getShellInfo()
    assert info.shell == "bash"
    assert info.version == "5.1.16"
    assert info.info == "bash 5.1.16"
