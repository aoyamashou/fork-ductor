"""Tests for agent-facing rule docs that are consumed by Gemini memory imports."""

from __future__ import annotations

from pathlib import Path


def test_agent_tools_rules_contains_transport_info() -> None:
    rules_path = (
        Path(__file__).resolve().parents[2]
        / "ductor_bot"
        / "_home_defaults"
        / "workspace"
        / "tools"
        / "agent_tools"
        / "RULES.md"
    )

    content = rules_path.read_text(encoding="utf-8")

    # Telegram is the only supported messaging transport.
    assert "Telegram" in content
    assert "Matrix" not in content
    assert "create_agent.py" in content
