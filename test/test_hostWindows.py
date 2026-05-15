import pytest
import sys
import types
from pyhw.pyhwException import BackendException

def test_host_windows(monkeypatch):
    mock_winreg = types.ModuleType("winreg")
    mock_winreg.HKEY_LOCAL_MACHINE = 1
    def mock_open_key(*args, **kwargs):
        return "MockKey"
    def mock_query_value(key, value_name):
        if value_name == "SystemManufacturer":
            return ("Dell", None)
        elif value_name == "SystemProductName":
            return ("XPS 15", None)
        elif value_name == "SystemVersion":
            return ("1.0", None)
        return ("", None)
    def mock_close_key(*args, **kwargs):
        pass
    mock_winreg.OpenKey = mock_open_key
    mock_winreg.QueryValueEx = mock_query_value
    mock_winreg.CloseKey = mock_close_key

    monkeypatch.setitem(sys.modules, "winreg", mock_winreg)
    
    import importlib
    import pyhw.backend.host.windows
    importlib.reload(pyhw.backend.host.windows)
    monkeypatch.setattr(pyhw.backend.host.windows, "getArch", lambda: "x86_64")

    detector = pyhw.backend.host.windows.HostDetectWindows()
    info = detector.getHostInfo()
    assert info.name == "XPS 15"
    assert info.vendor == "Dell"
    assert info.version == "1.0"


def test_host_windows_vmware_clears_version(monkeypatch):
    mock_winreg = types.ModuleType("winreg")
    mock_winreg.HKEY_LOCAL_MACHINE = 1
    mock_winreg.OpenKey = lambda *args, **kwargs: "MockKey"

    def mock_query_value(key, value_name):
        values = {
            "SystemManufacturer": "VMware",
            "SystemProductName": "VMware Virtual Platform",
            "SystemVersion": "None",
        }
        return values[value_name], None

    mock_winreg.QueryValueEx = mock_query_value
    mock_winreg.CloseKey = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, "winreg", mock_winreg)

    import importlib
    import pyhw.backend.host.windows
    importlib.reload(pyhw.backend.host.windows)
    monkeypatch.setattr(pyhw.backend.host.windows, "getArch", lambda: "x86_64")

    info = pyhw.backend.host.windows.HostDetectWindows().getHostInfo()

    assert info.version == ""
    assert info.model == "VMware Virtual Platform "


def test_host_windows_missing_registry(monkeypatch):
    mock_winreg = types.ModuleType("winreg")
    mock_winreg.HKEY_LOCAL_MACHINE = 1
    mock_winreg.OpenKey = lambda *args, **kwargs: (_ for _ in ()).throw(FileNotFoundError())
    mock_winreg.QueryValueEx = lambda *args, **kwargs: ("", None)
    mock_winreg.CloseKey = lambda *args, **kwargs: None
    monkeypatch.setitem(sys.modules, "winreg", mock_winreg)

    import importlib
    import pyhw.backend.host.windows
    importlib.reload(pyhw.backend.host.windows)

    with pytest.raises(BackendException):
        pyhw.backend.host.windows.HostDetectWindows().getHostInfo()
