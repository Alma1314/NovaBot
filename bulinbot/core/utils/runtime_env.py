import os
import sys


def is_frozen_runtime() -> bool:
    return bool(getattr(sys, "frozen", False))


def is_packaged_desktop_runtime() -> bool:
    return os.environ.get("BULINBOT_DESKTOP_CLIENT") == "1"
