import pytest

from pyhw.backend import Data
from pyhw.backend.foundationModels import FoundationModelsInfo
from pyhw.frontend.foundationModels import formatFoundationModels, formatFoundationModelsDebug
from pyhw.pyhwUtil import createDataString


@pytest.mark.parametrize("info, expected", [
    (FoundationModelsInfo("available", model_variant="Test Model"), "Available — Test Model"),
    (FoundationModelsInfo("available"), "Available — Apple Foundation Model"),
    (FoundationModelsInfo("unavailable", "deviceNotEligible"), "Unsupported — Device not eligible"),
    (FoundationModelsInfo("unavailable", "appleIntelligenceNotEnabled"), "Unavailable — Apple Intelligence not enabled"),
    (FoundationModelsInfo("unavailable", "modelNotReady"), "Unavailable — Model not ready"),
    (FoundationModelsInfo("unavailable", "unknown"), "Unavailable — Unknown reason"),
    (FoundationModelsInfo("unsupported", "osUnsupported"), "Unsupported — Requires macOS 26+"),
    (FoundationModelsInfo("detection_error", error="missing library"), "Detection unavailable"),
])
def test_format(info, expected):
    assert formatFoundationModels(info) == expected


def test_optional_output_and_position():
    data = Data()
    assert "AFM:" not in createDataString(data)
    data.AFM = FoundationModelsInfo("available", model_variant="Test Model")
    text = createDataString(data)
    assert "AFM: Available — Test Model" in text
    assert text.index("NPU:") < text.index("AFM:") < text.index("Memory:")


def test_debug_does_not_invent_version():
    text = formatFoundationModelsDebug(FoundationModelsInfo("available", model_variant="Test Model"))
    assert "AFM model variant: Test Model" in text
    assert "AFM model version: not exposed" in text


def test_debug_reports_detection_error():
    text = formatFoundationModelsDebug(FoundationModelsInfo("detection_error", error="missing library"))
    assert "error     : foundation_models: missing library" in text
