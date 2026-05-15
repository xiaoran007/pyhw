from pyhw.__main__ import main, run_detector, detect_gpu, detect_nic, detect_npu
import sys
import runpy


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


def test_run_detector_catches_exception():
    def failing_detector(os):
        raise RuntimeError(f"failed on {os}")

    name, result, elapsed, error = run_detector("failing", failing_detector, "macos")

    assert name == "failing"
    assert result == {}
    assert elapsed >= 0
    assert "RuntimeError" in error


def test_optional_detectors_return_empty_when_no_devices(monkeypatch):
    class MockDetect:
        def __init__(self, os):
            self.os = os

        def getGPUInfo(self):
            return type("GPUInfo", (), {"number": 0, "gpus": []})()

        def getNICInfo(self):
            return type("NICInfo", (), {"number": 0, "nics": []})()

        def getNPUInfo(self):
            return type("NPUInfo", (), {"number": 0, "npus": []})()

    monkeypatch.setattr("pyhw.__main__.GPUDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.NICDetect", MockDetect)
    monkeypatch.setattr("pyhw.__main__.NPUDetect", MockDetect)

    assert detect_gpu("linux") == {}
    assert detect_nic("linux") == {}
    assert detect_npu("linux") == {}


def test_main_run(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pyhw", "--debug"])
    monkeypatch.setattr("pyhw.__main__.getOS", lambda: "linux")
    
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


def test_main_debug_prints_detector_error(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["pyhw", "--debug"])
    monkeypatch.setattr("pyhw.__main__.getOS", lambda: "linux")

    class MockInfo:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)

    class MockDetect:
        def __init__(self, os):
            self.os = os
        def getTitle(self): return MockInfo(title="test@test")
        def getHostInfo(self): raise RuntimeError("host failed")
        def getKernelInfo(self): return MockInfo(kernel="test")
        def getShellInfo(self): return MockInfo(info="test")
        def getUptime(self): return MockInfo(uptime="test")
        def getOSInfo(self): return MockInfo(prettyName="test", id="linux")
        def getCPUInfo(self): return MockInfo(cpu="test")
        def getGPUInfo(self): return MockInfo(number=0, gpus=[])
        def getMemoryInfo(self): return MockInfo(memory="test")
        def getNICInfo(self): return MockInfo(number=0, nics=[])
        def getNPUInfo(self): return MockInfo(number=0, npus=[])

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

    class MockQueue:
        def put(self, value):
            pass

        def get(self, timeout):
            return {"is_new_release": False}

    class MockPrinter:
        def __init__(self, logo_os, data):
            pass

        def cPrint(self):
            pass

    monkeypatch.setattr("pyhw.__main__.queue.Queue", lambda: MockQueue())
    monkeypatch.setattr("pyhw.__main__.check_release", lambda release_queue: None)
    monkeypatch.setattr("pyhw.__main__.Printer", MockPrinter)

    main()

    captured = capsys.readouterr()
    assert "error     : host:" in captured.out


def test_main_release_queue_timeout(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["pyhw"])
    monkeypatch.setattr("pyhw.__main__.getOS", lambda: "linux")

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
        def getGPUInfo(self): return MockInfo(number=0, gpus=[])
        def getMemoryInfo(self): return MockInfo(memory="test")
        def getNICInfo(self): return MockInfo(number=0, nics=[])
        def getNPUInfo(self): return MockInfo(number=0, npus=[])

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

    class MockQueue:
        def put(self, value):
            pass

        def get(self, timeout):
            raise __import__("queue").Empty()

    class MockPrinter:
        def __init__(self, logo_os, data):
            pass

        def cPrint(self):
            pass

    monkeypatch.setattr("pyhw.__main__.queue.Queue", lambda: MockQueue())
    monkeypatch.setattr("pyhw.__main__.check_release", lambda release_queue: None)
    monkeypatch.setattr("pyhw.__main__.Printer", MockPrinter)

    main()


def test_main_module_entrypoint(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["pyhw", "--version"])
    monkeypatch.delitem(sys.modules, "pyhw.__main__", raising=False)

    runpy.run_module("pyhw.__main__", run_name="__main__")

    captured = capsys.readouterr()
    assert "pyhw v" in captured.out
