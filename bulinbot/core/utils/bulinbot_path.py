"""Centralized BulinBot path helpers.

Project path:
- Fixed to the source tree location.

Root path:
- Defaults to the current working directory.
- Can be overridden with the ``BULINBOT_ROOT`` environment variable.

Data subdirectories:
- Most runtime data lives under ``<root>/data``.
- A few tool-runtime files intentionally live under the system temporary
  directory as ``.bulinbot``.
"""

import os
import tempfile

from bulinbot.core.utils.runtime_env import is_packaged_desktop_runtime


def get_bulinbot_path() -> str:
    """Return the BulinBot project source path."""
    return os.path.realpath(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../"),
    )


def get_bulinbot_root() -> str:
    """Return the BulinBot root directory."""
    if path := os.environ.get("BULINBOT_ROOT"):
        return os.path.realpath(path)
    if is_packaged_desktop_runtime():
        return os.path.realpath(os.path.join(os.path.expanduser("~"), ".bulinbot"))
    return os.path.realpath(os.getcwd())


def get_bulinbot_data_path() -> str:
    """Return the BulinBot data directory path."""
    return os.path.realpath(os.path.join(get_bulinbot_root(), "data"))


def get_bulinbot_config_path() -> str:
    """Return the BulinBot config directory path."""
    return os.path.realpath(os.path.join(get_bulinbot_data_path(), "config"))


def get_bulinbot_plugin_path() -> str:
    """Return the BulinBot plugin directory path."""
    return os.path.realpath(os.path.join(get_bulinbot_data_path(), "plugins"))


def get_bulinbot_plugin_data_path() -> str:
    """Return the BulinBot plugin data directory path."""
    return os.path.realpath(os.path.join(get_bulinbot_data_path(), "plugin_data"))


def get_bulinbot_t2i_templates_path() -> str:
    """Return the BulinBot T2I templates directory path."""
    return os.path.realpath(os.path.join(get_bulinbot_data_path(), "t2i_templates"))


def get_bulinbot_webchat_path() -> str:
    """Return the BulinBot WebChat data directory path."""
    return os.path.realpath(os.path.join(get_bulinbot_data_path(), "webchat"))


def get_bulinbot_temp_path() -> str:
    """Return the BulinBot temporary data directory path."""
    return os.path.realpath(os.path.join(get_bulinbot_data_path(), "temp"))


def get_bulinbot_skills_path() -> str:
    """Return the BulinBot skills directory path."""
    return os.path.realpath(os.path.join(get_bulinbot_data_path(), "skills"))


def get_bulinbot_workspaces_path() -> str:
    """Return the BulinBot workspaces directory path."""
    return os.path.realpath(os.path.join(get_bulinbot_data_path(), "workspaces"))


def get_bulinbot_system_tmp_path() -> str:
    """Return the shared system temporary directory used by local tools."""
    return os.path.realpath(os.path.join(tempfile.gettempdir(), ".bulinbot"))


def get_bulinbot_site_packages_path() -> str:
    """Return the BulinBot third-party site-packages directory path."""
    return os.path.realpath(os.path.join(get_bulinbot_data_path(), "site-packages"))


def get_bulinbot_knowledge_base_path() -> str:
    """Return the BulinBot knowledge base root path."""
    return os.path.realpath(os.path.join(get_bulinbot_data_path(), "knowledge_base"))


def get_bulinbot_backups_path() -> str:
    """Return the BulinBot backups directory path."""
    return os.path.realpath(os.path.join(get_bulinbot_data_path(), "backups"))
