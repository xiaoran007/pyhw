import pytest
from pyhw.backend.host.linux import HostDetectLinux
import os


def test_host_linux_dmi(monkeypatch):
    monkeypatch.setattr("pyhw.backend.host.linux.getArch", lambda: "x86_64")
    monkeypatch.setattr("pyhw.backend.host.linux.getDocker", lambda: False)
    monkeypatch.setattr("pyhw.backend.host.linux.getWSL", lambda: False)

    class MockFile:
        def __init__(self, filename):
            self.filename = filename
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def read(self):
            if "product_name" in self.filename:
                return "My Host"
            elif "product_version" in self.filename:
                return "1.0"
            return ""
            
    monkeypatch.setattr("builtins.open", lambda f, *args, **kwargs: MockFile(f))
    
    detector = HostDetectLinux()
    info = detector.getHostInfo()
    assert info.name == "My Host"
    assert info.version == "1.0"
    assert info.model == "My Host 1.0"


def test_host_linux_wsl(monkeypatch):
    monkeypatch.setattr("pyhw.backend.host.linux.getArch", lambda: "x86_64")
    monkeypatch.setattr("pyhw.backend.host.linux.getDocker", lambda: False)
    monkeypatch.setattr("pyhw.backend.host.linux.getWSL", lambda: True)

    detector = HostDetectLinux()
    info = detector.getHostInfo()
    assert info.name == "Windows WSL x86_64 Host"


def test_host_linux_docker(monkeypatch):
    monkeypatch.setattr("pyhw.backend.host.linux.getArch", lambda: "aarch64")
    monkeypatch.setattr("pyhw.backend.host.linux.getDocker", lambda: True)
    monkeypatch.setattr("pyhw.backend.host.linux.getWSL", lambda: False)

    detector = HostDetectLinux()
    info = detector.getHostInfo()
    assert info.name == "General aarch64 Docker Host"
