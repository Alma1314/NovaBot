import asyncio
import os
from pathlib import Path

import click
from filelock import FileLock, Timeout

from ..utils import check_dashboard, get_bulinbot_root

DASHBOARD_INITIAL_PASSWORD_ENV = "BULINBOT_DASHBOARD_INITIAL_PASSWORD"


def _initialize_config_from_env(bulinbot_root: Path) -> None:
    if DASHBOARD_INITIAL_PASSWORD_ENV not in os.environ:
        return

    from bulinbot.core.config.bulinbot_config import BulinBotConfig

    BulinBotConfig(config_path=str(bulinbot_root / "data" / "cmd_config.json"))
    click.echo("Initialized data/cmd_config.json with dashboard initial password.")


async def initialize_bulinbot(bulinbot_root: Path) -> None:
    """Execute BulinBot initialization logic"""
    dot_bulinbot = bulinbot_root / ".bulinbot"

    if not dot_bulinbot.exists():
        if click.confirm(
            f"Install BulinBot to this directory? {bulinbot_root}",
            default=True,
            abort=True,
        ):
            dot_bulinbot.touch()
            click.echo(f"Created {dot_bulinbot}")

    paths = {
        "data": bulinbot_root / "data",
        "config": bulinbot_root / "data" / "config",
        "plugins": bulinbot_root / "data" / "plugins",
        "temp": bulinbot_root / "data" / "temp",
    }

    for name, path in paths.items():
        path.mkdir(parents=True, exist_ok=True)
        click.echo(f"{'Created' if not path.exists() else 'Directory exists'}: {path}")

    _initialize_config_from_env(bulinbot_root)

    await check_dashboard(bulinbot_root / "data")


@click.command()
def init() -> None:
    """Initialize BulinBot"""
    click.echo("Initializing BulinBot...")
    bulinbot_root = get_bulinbot_root()
    lock_file = bulinbot_root / "bulinbot.lock"
    lock = FileLock(lock_file, timeout=5)

    try:
        with lock.acquire():
            asyncio.run(initialize_bulinbot(bulinbot_root))
            click.echo("Done! You can now run 'bulinbot run' to start BulinBot")
    except Timeout:
        raise click.ClickException(
            "Cannot acquire lock file. Please check if another instance is running"
        )

    except Exception as e:
        raise click.ClickException(f"Initialization failed: {e!s}")
