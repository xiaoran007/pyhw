import pytest
import getpass
import platform
from pyhw.backend.title.windows import TitleDetectWindows

def test_title_windows(monkeypatch):
    monkeypatch.setattr(getpass, "getuser", lambda: "testuser")
    monkeypatch.setattr(platform, "node", lambda: "testpc")

    detector = TitleDetectWindows()
    info = detector.getTitle()
    assert info.username == "testuser"
    assert info.hostname == "testpc"
    assert info.title == "testuser@testpc"
