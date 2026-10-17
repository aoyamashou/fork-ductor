"""Telegram bot creation."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ductor_bot.bus.bus import MessageBus
    from ductor_bot.bus.lock_pool import LockPool
    from ductor_bot.config import AgentConfig
    from ductor_bot.messenger.protocol import BotProtocol

def create_bot(
    config: AgentConfig,
    *,
    agent_name: str = "main",
    bus: MessageBus | None = None,
    lock_pool: LockPool | None = None,
) -> BotProtocol:
    """Create the Telegram bot for *config*."""
    if config.transport != "telegram" or config.transports != ["telegram"]:
        raise ValueError("This build supports Telegram only")
    return _create_telegram(config, agent_name=agent_name, bus=bus, lock_pool=lock_pool)


def _create_telegram(
    config: AgentConfig,
    *,
    agent_name: str,
    bus: MessageBus | None,
    lock_pool: LockPool | None,
) -> BotProtocol:
    from ductor_bot.messenger.telegram.app import TelegramBot

    return TelegramBot(config, agent_name=agent_name, bus=bus, lock_pool=lock_pool)
