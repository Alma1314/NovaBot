from bulinbot.core.utils.bulinbot_path import get_bulinbot_root
from bulinbot.core.utils.runtime_env import is_packaged_desktop_runtime


def test_desktop_client_env_marks_desktop_runtime_without_frozen(monkeypatch):
    monkeypatch.setenv("BULINBOT_DESKTOP_CLIENT", "1")
    monkeypatch.delattr("sys.frozen", raising=False)

    assert is_packaged_desktop_runtime() is True


def test_desktop_client_uses_home_root_without_explicit_bulinbot_root(monkeypatch):
    monkeypatch.setenv("BULINBOT_DESKTOP_CLIENT", "1")
    monkeypatch.delenv("BULINBOT_ROOT", raising=False)
    monkeypatch.delattr("sys.frozen", raising=False)

    assert get_bulinbot_root().endswith(".bulinbot")


def test_explicit_bulinbot_root_overrides_desktop_default(monkeypatch, tmp_path):
    explicit_root = tmp_path / "bulinbot-root"
    monkeypatch.setenv("BULINBOT_DESKTOP_CLIENT", "1")
    monkeypatch.setenv("BULINBOT_ROOT", str(explicit_root))
    monkeypatch.delattr("sys.frozen", raising=False)

    assert get_bulinbot_root() == str(explicit_root.resolve())
