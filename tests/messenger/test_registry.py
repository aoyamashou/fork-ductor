"""Tests for the transport registry."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from ductor_bot.messenger.registry import create_bot


class TestTransportRegistry:
    def test_unknown_transport_raises(self) -> None:
        config = MagicMock()
        config.transport = "discord"
        config.transports = ["telegram"]
        with pytest.raises(ValueError, match="Telegram"):
            create_bot(config)

    def test_telegram_transport(self) -> None:
        config = MagicMock()
        config.transport = "telegram"
        config.transports = ["telegram"]
        fake_bot = MagicMock()
        with patch("ductor_bot.messenger.telegram.app.TelegramBot", return_value=fake_bot):
            bot = create_bot(config, agent_name="test")
        assert bot is fake_bot
