import abc

from bulinbot.core.config import BulinBotConfig
from bulinbot.core.platform.bulin_message_event import BulinMessageEvent
from bulinbot.core.platform.message_type import MessageType


class HandlerFilter(abc.ABC):
    @abc.abstractmethod
    def filter(self, event: BulinMessageEvent, cfg: BulinBotConfig) -> bool:
        """是否应当被过滤"""
        raise NotImplementedError


__all__ = ["BulinBotConfig", "BulinMessageEvent", "HandlerFilter", "MessageType"]
