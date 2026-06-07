import os

from bulinbot.core.config import BulinBotConfig
from bulinbot.core.config.default import DB_PATH
from bulinbot.core.db.sqlite import SQLiteDatabase
from bulinbot.core.file_token_service import FileTokenService
from bulinbot.core.utils.pip_installer import (
    DependencyConflictError as DependencyConflictError,
)
from bulinbot.core.utils.pip_installer import (
    PipInstaller,
)
from bulinbot.core.utils.requirements_utils import (
    RequirementsPrecheckFailed as RequirementsPrecheckFailed,
)
from bulinbot.core.utils.requirements_utils import (
    find_missing_requirements as find_missing_requirements,
)
from bulinbot.core.utils.requirements_utils import (
    find_missing_requirements_or_raise as find_missing_requirements_or_raise,
)
from bulinbot.core.utils.shared_preferences import SharedPreferences
from bulinbot.core.utils.t2i.renderer import HtmlRenderer

from .log import LogBroker, LogManager  # noqa
from .utils.bulinbot_path import get_bulinbot_data_path

# 初始化数据存储文件夹
os.makedirs(get_bulinbot_data_path(), exist_ok=True)

DEMO_MODE = os.getenv("DEMO_MODE", "False").strip().lower() in ("true", "1", "t")

bulinbot_config = BulinBotConfig()
t2i_base_url = bulinbot_config.get("t2i_endpoint", "https://t2i.soulter.top/text2img")
html_renderer = HtmlRenderer(t2i_base_url)
logger = LogManager.GetLogger(log_name="bulinbot")
LogManager.configure_logger(logger, bulinbot_config)
LogManager.configure_trace_logger(bulinbot_config)
db_helper = SQLiteDatabase(DB_PATH)
# 简单的偏好设置存储, 这里后续应该存储到数据库中, 一些部分可以存储到配置中
sp = SharedPreferences(db_helper=db_helper)
# 文件令牌服务
file_token_service = FileTokenService()
pip_installer = PipInstaller(
    bulinbot_config.get("pip_install_arg", ""),
    bulinbot_config.get("pypi_index_url", None),
)
