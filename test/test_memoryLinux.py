import pytest
from pyhw.backend.memory.linux import MemoryDetectLinux


def test_memory_linux(monkeypatch):
    class MockFile:
        def __init__(self, filename):
            pass
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            pass
        def __iter__(self):
            return iter([
                "MemTotal:        16384000 kB\n",
                "MemAvailable:     8192000 kB\n"
            ])
            
    monkeypatch.setattr("builtins.open", lambda f, *args, **kwargs: MockFile(f))
    
    detector = MemoryDetectLinux()
    info = detector.getMemoryInfo()
    assert info.total == 15.62
    assert info.available == 7.81
    assert info.used == 7.81


def test_memory_linux_error(monkeypatch):
    def mock_open_error(*args, **kwargs):
        raise FileNotFoundError()

    monkeypatch.setattr("builtins.open", mock_open_error)
    
    detector = MemoryDetectLinux()
    info = detector.getMemoryInfo()
    assert info.total == 0
    assert info.used == 0
