from dataclasses import dataclass
from typing import Optional


@dataclass
class FoundationModelsInfo:
    status: str
    reason: Optional[str] = None
    model_variant: Optional[str] = None
    # Apple's public API does not expose an exact model weight version.
    model_version: Optional[str] = None
    error: Optional[str] = None
