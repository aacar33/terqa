import sys


def test_platform_protection():
    assert sys.platform != "win32", "Intentional Windows test failure"
