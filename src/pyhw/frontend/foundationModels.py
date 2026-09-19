def formatFoundationModels(info):
    if info.status == "available":
        return "Available — " + (info.model_variant or "Apple Foundation Model")
    if info.status == "detection_error":
        return "Detection unavailable"
    if info.reason == "osUnsupported":
        return "Unsupported — Requires macOS 26+"
    if info.reason == "deviceNotEligible":
        return "Unsupported — Device not eligible"
    reasons = {
        "appleIntelligenceNotEnabled": "Apple Intelligence not enabled",
        "modelNotReady": "Model not ready",
        "unknown": "Unknown reason",
    }
    return "Unavailable — " + reasons[info.reason]


def formatFoundationModelsDebug(info):
    return "\n".join([
        f"AFM status: {info.status}",
        f"AFM reason: {info.reason or 'none'}",
        f"AFM model variant: {info.model_variant or 'not reported'}",
        f"AFM model version: {info.model_version or 'not exposed'}",
    ] + ([f"error     : foundation_models: {info.error}"] if info.error else []))
