import ctypes
import json
import platform
from pathlib import Path

from .foundationModelsInfo import FoundationModelsInfo


class FoundationModelsDetectMacOS:
    def getFoundationModelsInfo(self):
        if int(platform.mac_ver()[0].split(".")[0]) < 26:
            return FoundationModelsInfo(status="unsupported", reason="osUnsupported")

        try:
            package_root = Path(__file__).resolve().parents[2]
            lib = ctypes.CDLL(str(package_root / "library/lib/foundationModelsLib.dylib"))
            lib.getFoundationModelsInfo.argtypes = []
            # Keep the original pointer so the Swift allocation can be freed.
            lib.getFoundationModelsInfo.restype = ctypes.c_void_p
            lib.freeFoundationModelsInfo.argtypes = [ctypes.c_void_p]
            lib.freeFoundationModelsInfo.restype = None
            pointer = lib.getFoundationModelsInfo()
            if not pointer:
                raise MemoryError("Foundation Models bridge returned a null result")
            try:
                payload = json.loads(ctypes.string_at(pointer).decode("utf-8"))
                return FoundationModelsInfo(**payload)
            finally:
                lib.freeFoundationModelsInfo(pointer)
        except (OSError, AttributeError, ValueError, TypeError, MemoryError) as exc:
            return FoundationModelsInfo(status="detection_error", error=repr(exc))
