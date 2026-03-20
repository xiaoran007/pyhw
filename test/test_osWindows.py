import pytest
import sys
import platform
import types

def test_os_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    monkeypatch.setattr(platform, "release", lambda: "10")
    monkeypatch.setattr(platform, "win32_edition", lambda: "Professional")
    monkeypatch.setattr(platform, "machine", lambda: "AMD64")

    mock_winreg = types.ModuleType("winreg")
    mock_winreg.HKEY_LOCAL_MACHINE = 1
    def mock_open_key(*args, **kwargs):
        return "MockKey"
    def mock_query_value(key, value_name):
        if value_name == "DisplayVersion":
            return ("22H2", None)
        raise FileNotFoundError()
    def mock_close_key(*args, **kwargs):
        pass
    mock_winreg.OpenKey = mock_open_key
    mock_winreg.QueryValueEx = mock_query_value
    mock_winreg.CloseKey = mock_close_key

    monkeypatch.setitem(sys.modules, "winreg", mock_winreg)
    
    import importlib
    import pyhw.backend.os.windows
    importlib.reload(pyhw.backend.os.windows)

    detector = pyhw.backend.os.windows.OSDetectWindows()
    info = detector.getOSInfo()
    assert info.id == "windows_10"
    assert "Windows 10 22H2 (Professional) AMD64" in info.prettyName
