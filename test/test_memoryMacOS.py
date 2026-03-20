import pytest
import subprocess
from pyhw.backend.memory.macos import MemoryDetectMacOS


def test_memory_macos(monkeypatch):
    def mock_sysctl_get_int(key):
        if key == "hw.pagesize":
            return 16384
        elif key == "hw.memsize":
            return 17179869184 # 16GB
        return 0
    monkeypatch.setattr("pyhw.backend.memory.macos.sysctlGetInt", mock_sysctl_get_int)
    
    class MockProcess:
        def __init__(self, stdout):
            self.stdout = stdout
            
    def mock_run(*args, **kwargs):
        stdout = (
            "Pages active:           100000.\n"
            "Pages inactive:         100000.\n"
            "Pages speculative:      10000.\n"
            "Pages wired down:       50000.\n"
            "Pages occupied by compressor: 10000.\n"
            "Pages purgeable:        5000.\n"
            "File-backed pages:      20000.\n"
        )
        return MockProcess(stdout)
    monkeypatch.setattr(subprocess, "run", mock_run)
    
    detector = MemoryDetectMacOS()
    info = detector.getMemoryInfo()
    assert info.total == 16.0
    assert info.used > 0
    assert "GiB / 16.00 GiB" in info.memory


def test_memory_macos_error(monkeypatch):
    def mock_sysctl_get_int(key):
        return 16384 if key == "hw.pagesize" else 8589934592

    monkeypatch.setattr("pyhw.backend.memory.macos.sysctlGetInt", mock_sysctl_get_int)
    
    def mock_run_error(*args, **kwargs):
        raise subprocess.SubprocessError()
    monkeypatch.setattr(subprocess, "run", mock_run_error)
    
    detector = MemoryDetectMacOS()
    info = detector.getMemoryInfo()
    assert info.total == 8.0
    assert info.used == 0.0
