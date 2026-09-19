import ctypes
import json
from unittest.mock import Mock

import pytest

from pyhw.backend.foundationModels import FoundationModelsDetect
from pyhw.backend.foundationModels.macos import FoundationModelsDetectMacOS
from pyhw.pyhwException import OSUnsupportedException


@pytest.fixture
def bridge(monkeypatch):
    monkeypatch.setattr("platform.mac_ver", lambda: ("27.0", (), "arm64"))
    library = Mock()
    monkeypatch.setattr("ctypes.CDLL", Mock(return_value=library))
    return library


@pytest.mark.parametrize("payload", [
    {"status": "available", "model_variant": "Test Model"},
    {"status": "available"},  # macOS 26 has no variant API.
    {"status": "unavailable", "reason": "deviceNotEligible"},
    {"status": "unavailable", "reason": "appleIntelligenceNotEnabled"},
    {"status": "unavailable", "reason": "modelNotReady"},
    {"status": "unavailable", "reason": "unknown"},
])
def test_bridge_result_and_memory_ownership(bridge, payload):
    buffer = ctypes.create_string_buffer(json.dumps(payload).encode())
    pointer = ctypes.addressof(buffer)
    bridge.getFoundationModelsInfo.return_value = pointer

    info = FoundationModelsDetect("macos").getFoundationModelsInfo()

    assert info.status == payload["status"]
    assert info.reason == payload.get("reason")
    assert info.model_variant == payload.get("model_variant")
    assert info.model_version is None
    assert info.error is None
    assert bridge.getFoundationModelsInfo.restype is ctypes.c_void_p
    bridge.freeFoundationModelsInfo.assert_called_once_with(pointer)


def test_old_os_does_not_load_library(monkeypatch):
    monkeypatch.setattr("platform.mac_ver", lambda: ("15.7", (), "arm64"))
    loader = Mock(side_effect=AssertionError("must not load"))
    monkeypatch.setattr("ctypes.CDLL", loader)

    info = FoundationModelsDetectMacOS().getFoundationModelsInfo()

    assert (info.status, info.reason) == ("unsupported", "osUnsupported")
    loader.assert_not_called()


def test_missing_library_is_not_model_unavailable(bridge, monkeypatch):
    monkeypatch.setattr("ctypes.CDLL", Mock(side_effect=OSError("missing library")))
    info = FoundationModelsDetectMacOS().getFoundationModelsInfo()
    assert info.status == "detection_error"
    assert "missing library" in info.error


def test_invalid_json_still_frees_result(bridge):
    buffer = ctypes.create_string_buffer(b"invalid json")
    pointer = ctypes.addressof(buffer)
    bridge.getFoundationModelsInfo.return_value = pointer
    info = FoundationModelsDetectMacOS().getFoundationModelsInfo()
    assert info.status == "detection_error"
    bridge.freeFoundationModelsInfo.assert_called_once_with(pointer)


def test_null_result(bridge):
    bridge.getFoundationModelsInfo.return_value = None
    info = FoundationModelsDetectMacOS().getFoundationModelsInfo()
    assert info.status == "detection_error"
    bridge.freeFoundationModelsInfo.assert_not_called()


@pytest.mark.parametrize("os", ["linux", "windows", "freebsd"])
def test_other_platforms_rejected(os):
    with pytest.raises(OSUnsupportedException):
        FoundationModelsDetect(os).getFoundationModelsInfo()
