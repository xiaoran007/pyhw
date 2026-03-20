import pytest
import sys
import platform
import types

def test_kernel_windows(monkeypatch):
    monkeypatch.setattr(platform, "version", lambda: "10.0.19045")
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
    import pyhw.backend.kernel.windows
    importlib.reload(pyhw.backend.kernel.windows)

    detector = pyhw.backend.kernel.windows.KernelDetectWindows()
    info = detector.getKernelInfo()
    assert info.kernel == "10.0.19045 (22H2) AMD64"
