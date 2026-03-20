import pytest
from pyhw.__main__ import main
import sys
import multiprocessing


def test_main_version(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["pyhw", "--version"])
    # mock ReleaseChecker to prevent network requests
    class MockReleaseChecker:
        def __init__(self, *args, **kwargs):
            self.CurrentVersion = "1.0.0"
    monkeypatch.setattr("pyhw.__main__.ReleaseChecker", MockReleaseChecker)
    
    main()
    
    captured = capsys.readouterr()
    assert "pyhw v1.0.0" in captured.out


def test_main_unsupported_os(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["pyhw"])
    monkeypatch.setattr("pyhw.__main__.getOS", lambda: "unknown")
    
    main()
    
    captured = capsys.readouterr()
    assert "Only Linux, macOS, FreeBSD, and Windows are supported" in captured.out


def test_main_run(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pyhw", "--debug"])
    monkeypatch.setattr("pyhw.__main__.getOS", lambda: "linux")
    
    # Mock multiprocessing Process to run synchronously
    class MockProcess:
        def __init__(self, target, args=()):
            self.target = target
            self.args = args
            
        def start(self):
            self.target(*self.args)
            
        def join(self, timeout=None):
            pass
            
        def terminate(self):
            pass
            
        def is_alive(self):
            # Test the condition where it's still alive to trigger termination logic
            if getattr(self, "_checked", False):
                return False
            self._checked = True
            return True
            
    monkeypatch.setattr(multiprocessing, "Process", MockProcess)
    
    # Mock backend detects to avoid errors
    class MockInfo:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    class MockDetect:
        def __init__(self, os):
            self.os = os
        def getTitle(self): return MockInfo(title="test@test")
        def getHostInfo(self): return MockInfo(model="test")
        def getKernelInfo(self): return MockInfo(kernel="test")
        def getShellInfo(self): return MockInfo(info="test")
        def getUptime(self): return MockInfo(uptime="test")
        def getOSInfo(self): return MockInfo(prettyName="test", id="linux")
        def getCPUInfo(self): return MockInfo(cpu="test")
        def getGPUInfo(self): return MockInfo(number=1, gpus=["test"])
        def getMemoryInfo(self): return MockInfo(memory="test")
        def getNICInfo(self): return MockInfo(number=1, nics=["test"])
        def getNPUInfo(self): return MockInfo(number=1, npus=["test"])

    monkeypatch.setattr("pyhw.__main__.TitleDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.HostDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.KernelDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.ShellDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.UptimeDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.OSDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.CPUDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.GPUDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.MemoryDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.NICDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.NPUDetect", MockDetect)
    
    class MockReleaseChecker:
        def __init__(self, *args, **kwargs):
            self.CurrentVersion = "1.0.0"
            self.LatestVersion = "1.0.1"
            self.isInPIPX = False
        def check_for_updates(self):
            return True
            
    monkeypatch.setattr("pyhw.__main__.ReleaseChecker", MockReleaseChecker)
    
    class MockPrinter:
        def __init__(self, logo_os, data):
            pass
        def cPrint(self):
            pass
            
    monkeypatch.setattr("pyhw.__main__.Printer", MockPrinter)
    
    main()

def test_main_run_macos(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pyhw"])
    monkeypatch.setattr("pyhw.__main__.getOS", lambda: "macos")
    
    # Mock multiprocessing Process to run synchronously
    class MockProcess:
        def __init__(self, target, args=()):
            self.target = target
            self.args = args
            
        def start(self):
            self.target(*self.args)
            
        def join(self, timeout=None):
            pass
            
        def terminate(self):
            pass
            
        def is_alive(self):
            return False
            
    monkeypatch.setattr(multiprocessing, "Process", MockProcess)
    
    # Mock backend detects to avoid errors
    class MockInfo:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
    
    class MockDetect:
        def __init__(self, os):
            self.os = os
        def getTitle(self): return MockInfo(title="test@test")
        def getHostInfo(self): return MockInfo(model="test")
        def getKernelInfo(self): return MockInfo(kernel="test")
        def getShellInfo(self): return MockInfo(info="test")
        def getUptime(self): return MockInfo(uptime="test")
        def getOSInfo(self): return MockInfo(prettyName="test", id="linux")
        def getCPUInfo(self): return MockInfo(cpu="test")
        def getGPUInfo(self): return MockInfo(number=1, gpus=["test"])
        def getMemoryInfo(self): return MockInfo(memory="test")
        def getNICInfo(self): return MockInfo(number=1, nics=["test"])
        def getNPUInfo(self): return MockInfo(number=1, npus=["test"])

    monkeypatch.setattr("pyhw.__main__.TitleDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.HostDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.KernelDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.ShellDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.UptimeDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.OSDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.CPUDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.GPUDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.MemoryDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.NICDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.NPUDetect", MockDetect)
    
    class MockReleaseChecker:
        def __init__(self, *args, **kwargs):
            self.CurrentVersion = "1.0.0"
            self.LatestVersion = "1.0.1"
            self.isInPIPX = True
        def check_for_updates(self):
            return True
            
    monkeypatch.setattr("pyhw.__main__.ReleaseChecker", MockReleaseChecker)
    
    class MockPrinter:
        def __init__(self, logo_os, data):
            pass
        def cPrint(self):
            pass
            
    monkeypatch.setattr("pyhw.__main__.Printer", MockPrinter)
    
    main()
