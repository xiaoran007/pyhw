import pytest
from pyhw.backend.os.linux import OSDetectLinux


def test_os_linux_normal(monkeypatch):
    mock_os_release = [
        'PRETTY_NAME="Ubuntu 22.04 LTS"',
        'NAME="Ubuntu"',
        'ID=ubuntu',
        'ID_LIKE=debian',
        'VERSION_ID="22.04"',
        'VERSION="22.04 LTS (Jammy Jellyfish)"',
        'VERSION_CODENAME=jammy'
    ]

    class MockFile:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def __iter__(self):
            return iter(mock_os_release)

    def mock_open(filename, *args, **kwargs):
        if filename == "/etc/os-release":
            return MockFile()
        raise FileNotFoundError()

    monkeypatch.setattr("builtins.open", mock_open)
    
    detector = OSDetectLinux()
    info = detector.getOSInfo()
    
    assert info.prettyName == "Ubuntu 22.04 LTS"
    assert info.name == "Ubuntu"
    assert info.id == "ubuntu"
    assert info.versionID == "22.04"


def test_os_linux_armbian(monkeypatch):
    mock_os_release = [
        'PRETTY_NAME="Armbian 23.02.2 Jammy"',
        'ID=debian'
    ]

    class MockFile:
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def __iter__(self):
            return iter(mock_os_release)

    def mock_open(filename, *args, **kwargs):
        if filename == "/etc/os-release":
            return MockFile()
        raise FileNotFoundError()

    monkeypatch.setattr("builtins.open", mock_open)
    
    detector = OSDetectLinux()
    info = detector.getOSInfo()
    
    assert info.prettyName == "Armbian 23.02.2 Jammy"
    assert info.id == "armbian"


def test_os_linux_error(monkeypatch):
    def mock_open_error(*args, **kwargs):
        raise Exception()

    monkeypatch.setattr("builtins.open", mock_open_error)
    
    detector = OSDetectLinux()
    info = detector.getOSInfo()
    
    assert info.prettyName == ""
    assert info.id == ""


def test_os_linux_extended_release_fields(monkeypatch):
    mock_os_release = [
        'PRETTY_NAME="Fedora Linux"',
        'VARIANT="KDE Plasma"',
        'VARIANT_ID=kde',
        'CODE_NAME=Rawhide',
        'BUILD_ID=20260515',
    ]

    class MockFile:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            pass

        def __iter__(self):
            return iter(mock_os_release)

    monkeypatch.setattr("builtins.open", lambda *args, **kwargs: MockFile())

    info = OSDetectLinux().getOSInfo()

    assert info.variant == "KDE Plasma"
    assert info.variantID == "kde"
    assert info.codeName == "Rawhide"
    assert info.buildID == "20260515"
