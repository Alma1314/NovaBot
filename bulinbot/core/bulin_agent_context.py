from pydantic import Field
from pydantic.dataclasses import dataclass

from bulinbot.core.agent.run_context import ContextWrapper
from bulinbot.core.platform.bulin_message_event import BulinMessageEvent
from bulinbot.core.star.context import Context


@dataclass
class BulinAgentContext:
    __pydantic_config__ = {"arbitrary_types_allowed": True}

    context: Context
    """The star context instance"""
    event: BulinMessageEvent
    """The message event associated with the agent context."""
    extra: dict[str, str] = Field(default_factory=dict)
    """Customized extra data."""


AgentContextWrapper = ContextWrapper[BulinAgentContext]
