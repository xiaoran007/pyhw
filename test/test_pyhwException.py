import pytest
from pyhw.pyhwException.pyhwException import (
    GPUNotFoundException,
    BackendException,
    OSUnsupportedException,
    LogoNotFoundException
)


def test_gpu_not_found_exception():
    with pytest.raises(GPUNotFoundException, match="GPU issue"):
        raise GPUNotFoundException("GPU issue")


def test_backend_exception():
    with pytest.raises(BackendException, match="Backend error"):
        raise BackendException("Backend error")


def test_os_unsupported_exception():
    with pytest.raises(OSUnsupportedException, match="Unsupported OS"):
        raise OSUnsupportedException("Unsupported OS")


def test_logo_not_found_exception():
    with pytest.raises(LogoNotFoundException, match="Logo missing"):
        raise LogoNotFoundException("Logo missing")
