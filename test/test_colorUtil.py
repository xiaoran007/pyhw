import pytest
from pyhw.frontend.color.colorUtil import colorPrefix, colorSuffix


def test_colorPrefix():
    assert colorPrefix("31") == "\033[31m"
    assert colorPrefix("32") == "\033[32m"


def test_colorSuffix():
    assert colorSuffix() == "\033[0m"
