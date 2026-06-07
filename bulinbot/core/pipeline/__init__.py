"""Pipeline package exports.

This module intentionally avoids eager imports of all pipeline stage modules to
prevent import-time cycles. Stage classes remain available via lazy attribute
resolution for backward compatibility.
"""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

from bulinbot.core.message.message_event_result import (
    EventResultType,
    MessageEventResult,
)

from .stage_order import STAGES_ORDER

if TYPE_CHECKING:
    from .content_safety_check.stage import ContentSafetyCheckStage
    from .preprocess_stage.stage import PreProcessStage
    from .process_stage.stage import ProcessStage
    from .rate_limit_check.stage import RateLimitStage
    from .respond.stage import RespondStage
    from .result_decorate.stage import ResultDecorateStage
    from .session_status_check.stage import SessionStatusCheckStage
    from .waking_check.stage import WakingCheckStage
    from .whitelist_check.stage import WhitelistCheckStage

_LAZY_EXPORTS = {
    "ContentSafetyCheckStage": (
        "bulinbot.core.pipeline.content_safety_check.stage",
        "ContentSafetyCheckStage",
    ),
    "PreProcessStage": (
        "bulinbot.core.pipeline.preprocess_stage.stage",
        "PreProcessStage",
    ),
    "ProcessStage": (
        "bulinbot.core.pipeline.process_stage.stage",
        "ProcessStage",
    ),
    "RateLimitStage": (
        "bulinbot.core.pipeline.rate_limit_check.stage",
        "RateLimitStage",
    ),
    "RespondStage": (
        "bulinbot.core.pipeline.respond.stage",
        "RespondStage",
    ),
    "ResultDecorateStage": (
        "bulinbot.core.pipeline.result_decorate.stage",
        "ResultDecorateStage",
    ),
    "SessionStatusCheckStage": (
        "bulinbot.core.pipeline.session_status_check.stage",
        "SessionStatusCheckStage",
    ),
    "WakingCheckStage": (
        "bulinbot.core.pipeline.waking_check.stage",
        "WakingCheckStage",
    ),
    "WhitelistCheckStage": (
        "bulinbot.core.pipeline.whitelist_check.stage",
        "WhitelistCheckStage",
    ),
}

# Type-checking imports to satisfy static analyzers for __all__ exports
if TYPE_CHECKING:
    from .content_safety_check.stage import ContentSafetyCheckStage
    from .preprocess_stage.stage import PreProcessStage
    from .process_stage.stage import ProcessStage
    from .rate_limit_check.stage import RateLimitStage
    from .respond.stage import RespondStage
    from .result_decorate.stage import ResultDecorateStage
    from .session_status_check.stage import SessionStatusCheckStage
    from .waking_check.stage import WakingCheckStage
    from .whitelist_check.stage import WhitelistCheckStage

__all__ = [
    "ContentSafetyCheckStage",
    "EventResultType",
    "MessageEventResult",
    "PreProcessStage",
    "ProcessStage",
    "RateLimitStage",
    "RespondStage",
    "ResultDecorateStage",
    "SessionStatusCheckStage",
    "STAGES_ORDER",
    "WakingCheckStage",
    "WhitelistCheckStage",
]


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_path, attr_name = _LAZY_EXPORTS[name]
    module = import_module(module_path)
    value = getattr(module, attr_name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))
