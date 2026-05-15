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


def test_host_linux_x86_dmi_oem_placeholders(monkeypatch):
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
                return "Default string"
            if "product_version" in self.filename:
                return "1.0"
            return ""

    monkeypatch.setattr("builtins.open", lambda f, *args, **kwargs: MockFile(f))

    info = HostDetectLinux().getHostInfo()

    assert info.name == "General x86_64 Host"
    assert info.version == ""
    assert info.model == "General x86_64 Host "


def test_host_linux_x86_dmi_missing(monkeypatch):
    monkeypatch.setattr("pyhw.backend.host.linux.getArch", lambda: "x86_64")
    monkeypatch.setattr("pyhw.backend.host.linux.getDocker", lambda: False)
    monkeypatch.setattr("pyhw.backend.host.linux.getWSL", lambda: False)
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError()))

    info = HostDetectLinux().getHostInfo()

    assert info.model == ""


def test_host_linux_arm_dmi(monkeypatch):
    monkeypatch.setattr("pyhw.backend.host.linux.getArch", lambda: "aarch64")
    monkeypatch.setattr("pyhw.backend.host.linux.getDocker", lambda: False)
    monkeypatch.setattr("pyhw.backend.host.linux.getWSL", lambda: False)
    monkeypatch.setattr(os.path, "exists", lambda path: path == "/sys/devices/virtual/dmi/id")

    class MockFile:
        def __init__(self, filename):
            self.filename = filename

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def read(self):
            if "product_name" in self.filename:
                return "ARM Workstation"
            if "product_version" in self.filename:
                return "Rev A"
            return ""

    monkeypatch.setattr("builtins.open", lambda f, *args, **kwargs: MockFile(f))

    info = HostDetectLinux().getHostInfo()

    assert info.model == "ARM Workstation Rev A"


def test_host_linux_arm_dmi_placeholders(monkeypatch):
    monkeypatch.setattr("pyhw.backend.host.linux.getArch", lambda: "aarch64")
    monkeypatch.setattr("pyhw.backend.host.linux.getDocker", lambda: False)
    monkeypatch.setattr("pyhw.backend.host.linux.getWSL", lambda: False)
    monkeypatch.setattr(os.path, "exists", lambda path: path == "/sys/devices/virtual/dmi/id")

    class MockFile:
        def __init__(self, filename):
            self.filename = filename

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def read(self):
            if "product_name" in self.filename:
                return "Not Specified"
            if "product_version" in self.filename:
                return "Default string"
            return ""

    monkeypatch.setattr("builtins.open", lambda f, *args, **kwargs: MockFile(f))

    info = HostDetectLinux().getHostInfo()

    assert info.name == ""
    assert info.version == ""
    assert info.model == " "


def test_host_linux_arm_dmi_missing(monkeypatch):
    monkeypatch.setattr("pyhw.backend.host.linux.getArch", lambda: "aarch64")
    monkeypatch.setattr("pyhw.backend.host.linux.getDocker", lambda: False)
    monkeypatch.setattr("pyhw.backend.host.linux.getWSL", lambda: False)
    monkeypatch.setattr(os.path, "exists", lambda path: path == "/sys/devices/virtual/dmi/id")
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError()))

    info = HostDetectLinux().getHostInfo()

    assert info.model == ""


def test_host_linux_arm_device_tree(monkeypatch):
    monkeypatch.setattr("pyhw.backend.host.linux.getArch", lambda: "riscv64")
    monkeypatch.setattr("pyhw.backend.host.linux.getDocker", lambda: False)
    monkeypatch.setattr("pyhw.backend.host.linux.getWSL", lambda: False)
    monkeypatch.setattr(os.path, "exists", lambda path: False)

    class MockFile:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def read(self):
            return "VisionFive 2"

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())

    info = HostDetectLinux().getHostInfo()

    assert info.model == "VisionFive 2"


def test_host_linux_arm_device_tree_missing(monkeypatch):
    monkeypatch.setattr("pyhw.backend.host.linux.getArch", lambda: "mips64")
    monkeypatch.setattr("pyhw.backend.host.linux.getDocker", lambda: False)
    monkeypatch.setattr("pyhw.backend.host.linux.getWSL", lambda: False)
    monkeypatch.setattr(os.path, "exists", lambda path: False)
    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError()))

    info = HostDetectLinux().getHostInfo()

    assert info.model == ""


def test_host_linux_unused_private_placeholders():
    detector = HostDetectLinux()

    assert detector._HostDetectLinux__getHostFamily() is None
    assert detector._HostDetectLinux__getHostProductName() is None
