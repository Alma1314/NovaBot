import json

from bulinbot import logger
from bulinbot.core.conversation_mgr import ConversationManager
from bulinbot.core.platform.bulin_message_event import BulinMessageEvent
from bulinbot.core.provider.entities import ProviderRequest


async def persist_agent_history(
    conversation_manager: ConversationManager,
    *,
    event: BulinMessageEvent,
    req: ProviderRequest,
    summary_note: str,
) -> None:
    """Persist agent interaction into conversation history."""
    if not req or not req.conversation:
        return

    history = []
    try:
        history = json.loads(req.conversation.history or "[]")
    except Exception as exc:  # noqa: BLE001
        logger.warning("Failed to parse conversation history: %s", exc)
    history.append({"role": "user", "content": "Output your last task result below."})
    history.append({"role": "assistant", "content": summary_note})
    await conversation_manager.update_conversation(
        event.unified_msg_origin,
        req.conversation.cid,
        history=history,
    )
