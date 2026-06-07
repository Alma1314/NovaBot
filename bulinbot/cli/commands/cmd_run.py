import asyncio
import os
import sys
import traceback
from pathlib import Path

import click
from filelock import FileLock, Timeout

from ..utils import check_bulinbot_root, check_dashboard, get_bulinbot_root


async def run_bulinbot(bulinbot_root: Path) -> None:
    """Run BulinBot"""
    from bulinbot.core import LogBroker, LogManager, db_helper, logger
    from bulinbot.core.initial_loader import InitialLoader

    await check_dashboard(bulinbot_root / "data")

    log_broker = LogBroker()
    LogManager.set_queue_handler(logger, log_broker)
    db = db_helper

    core_lifecycle = InitialLoader(db, log_broker)

    await core_lifecycle.start()


@click.option("--reload", "-r", is_flag=True, help="Auto-reload plugins")
@click.option("--port", "-p", help="BulinBot Dashboard port", required=False, type=str)
@click.command()
def run(reload: bool, port: str) -> None:
    """Run BulinBot"""
    try:
        os.environ["BULINBOT_CLI"] = "1"
        bulinbot_root = get_bulinbot_root()

        if not check_bulinbot_root(bulinbot_root):
            raise click.ClickException(
                f"{bulinbot_root} is not a valid BulinBot root directory. Use 'bulinbot init' to initialize",
            )

        os.environ["BULINBOT_ROOT"] = str(bulinbot_root)
        sys.path.insert(0, str(bulinbot_root))

        if port:
            os.environ["DASHBOARD_PORT"] = port

        if reload:
            click.echo("Plugin auto-reload enabled")
            os.environ["BULINBOT_RELOAD"] = "1"

        lock_file = bulinbot_root / "bulinbot.lock"
        lock = FileLock(lock_file, timeout=5)
        with lock.acquire():
            asyncio.run(run_bulinbot(bulinbot_root))
    except KeyboardInterrupt:
        click.echo("BulinBot has been shut down.")
    except Timeout:
        raise click.ClickException(
            "Cannot acquire lock file. Please check if another instance is running"
        )
    except Exception as e:
        raise click.ClickException(f"Runtime error: {e}\n{traceback.format_exc()}")
