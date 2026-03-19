import pytest
import sys
from pyhw.backend.kernel.kernelBase import KernelDetect
from pyhw.backend.kernel.kernelInfo import KernelInfo
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def mock_detectors(monkeypatch):
    class MockUnix:
        def getKernelInfo(self):
            return "UnixKernel"
            
    class MockWindows:
        def getKernelInfo(self):
            return "WindowsKernel"

    monkeypatch.setitem(sys.modules, "winreg", type("winreg", (), {}))

    import pyhw.backend.kernel.unix
    import pyhw.backend.kernel.windows

    monkeypatch.setattr(pyhw.backend.kernel.unix, "KernelDetectUnix", MockUnix)
    monkeypatch.setattr(pyhw.backend.kernel.windows, "KernelDetectWindows", MockWindows)


def test_kernel_detect_linux(mock_detectors):
    detector = KernelDetect("linux")
    assert detector.getKernelInfo() == "UnixKernel"


def test_kernel_detect_macos(mock_detectors):
    detector = KernelDetect("macos")
    assert detector.getKernelInfo() == "UnixKernel"


def test_kernel_detect_bsd(mock_detectors):
    detector = KernelDetect("freebsd")
    assert detector.getKernelInfo() == "UnixKernel"


def test_kernel_detect_windows(mock_detectors):
    detector = KernelDetect("windows")
    assert detector.getKernelInfo() == "WindowsKernel"


def test_kernel_detect_unsupported():
    detector = KernelDetect("unknown")
    with pytest.raises(OSUnsupportedException):
        detector.getKernelInfo()


def test_kernel_info():
    info = KernelInfo()
    assert info.kernel == ""
    assert info.name == ""
    assert info.version == ""
