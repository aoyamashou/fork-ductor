#!/usr/bin/env python3
"""创建 Telegram 子智能体 by writing to agents.json.

The AgentSupervisor watches agents.json via FileWatcher and automatically
starts the new agent within seconds.

Usage (Telegram):
    python3 create_agent.py --name NAME --token TOKEN --users ID1,ID2 [--provider P] [--model M]

"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _agents_path() -> Path:
    """Resolve agents.json path (always in main agent home).

    Sub-agents have DUCTOR_HOME = ~/.ductor/agents/<name>/, so we navigate
    up to the main home. Main agent's DUCTOR_HOME points directly to ~/.ductor/.
    """
    import os

    home = Path(os.environ.get("DUCTOR_HOME", str(Path.home() / ".ductor")))
    direct = home / "agents.json"
    if direct.is_file():
        return direct
    # Sub-agent: navigate up from agents/<name>/ to main home
    main_home = home.parent.parent
    main_path = main_home / "agents.json"
    if main_path.is_file() or (main_home / "config").is_dir():
        return main_path
    return direct


_CLAUDE_MODELS = ("haiku", "sonnet", "sonnet[1m]", "opus", "opus[1m]", "fable")
_GROK_MODELS = ("grok-4.5", "grok-composer-2.5-fast")


def _main_home() -> Path:
    """Resolve the main agent's DUCTOR_HOME."""
    import os

    home = Path(os.environ.get("DUCTOR_HOME", str(Path.home() / ".ductor")))
    if home.name != ".ductor" and (home.parent.parent / "config").is_dir():
        return home.parent.parent
    return home


def _resolve_codex_model(model: str, home: Path) -> str:
    """Validate/resolve a Codex model against the cached model list."""
    cache_path = home / "config" / "codex_models.json"
    if not cache_path.is_file():
        return model
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
        models = data.get("models", [])
        valid_ids = [m["id"] for m in models if isinstance(m, dict)]
        if model in valid_ids:
            return model
        for m in models:
            if isinstance(m, dict) and m.get("is_default"):
                print(f"Note: '{model}' is not a valid Codex model. Using default: {m['id']}")
                return m["id"]
        if valid_ids:
            print(f"Note: '{model}' is not a valid Codex model. Using: {valid_ids[0]}")
            return valid_ids[0]
    except (json.JSONDecodeError, OSError, KeyError):
        pass
    return model


def _resolve_gemini_model(model: str, home: Path) -> str:
    """Validate/resolve a Gemini model against the cached model list."""
    cache_path = home / "config" / "gemini_models.json"
    if not cache_path.is_file():
        return model
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
        valid_ids = data.get("models", [])
        if model in valid_ids:
            return model
        if valid_ids:
            print(f"Note: '{model}' is not a valid Gemini model. Using: {valid_ids[0]}")
            return valid_ids[0]
    except (json.JSONDecodeError, OSError):
        pass
    return model


def _resolve_model(provider: str | None, model: str | None) -> str | None:
    """Validate model name against known models for the given provider.

    Catches common mistakes like ``--model codex`` (provider name, not a model).
    Uses cached model lists from ``config/codex_models.json`` and
    ``config/gemini_models.json`` and hardcoded Claude models. Antigravity
    names pass through unchanged; prefer ``antigravity-default`` because
    ``agy`` model selection is not reliable.
    """
    if model is None or provider is None:
        return model

    home = _main_home()

    if provider == "claude":
        if model in _CLAUDE_MODELS:
            return model
        print(f"Note: '{model}' is not a valid Claude model. Using: sonnet")
        return "sonnet"

    if provider in ("openai", "codex"):
        return _resolve_codex_model(model, home)

    if provider == "gemini":
        return _resolve_gemini_model(model, home)

    if provider == "grok":
        if model in _GROK_MODELS or model.startswith("grok-"):
            return model
        print(f"Note: '{model}' is not a valid Grok model. Using: grok-4.5")
        return "grok-4.5"

    return model


def main() -> None:
    parser = argparse.ArgumentParser(description="创建 Telegram 子智能体")
    parser.add_argument("--name", required=True, help="智能体名称（小写且不含空格）")
    parser.add_argument("--transport", choices=("telegram",), default="telegram")
    # Telegram-specific
    parser.add_argument("--token", default=None, help="Telegram Bot Token")
    parser.add_argument(
        "--users", default=None, help="以逗号分隔的 Telegram 数字用户 ID"
    )

    # Common
    parser.add_argument(
        "--provider",
        default=None,
        help="模型提供商（claude/openai/gemini/antigravity）",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="具体模型名称，例如 gpt-5.5、opus、gemini-2.5-pro",
    )
    parser.add_argument(
        "--description",
        default=None,
        help="加入通知中显示的简短智能体说明",
    )
    args = parser.parse_args()

    # --- Validate name ---
    name = args.name.lower().strip()
    if not name or " " in name or name == "main":
        print(
            f"错误：无效的智能体名称 '{name}'. 名称必须小写、不含空格，且不能为 main。",
            file=sys.stderr,
        )
        sys.exit(1)

    if not args.token or not args.users:
        parser.error("Telegram 子智能体需要 --token 和 --users")
    try:
        user_ids = [int(uid.strip()) for uid in args.users.split(",") if uid.strip()]
    except ValueError:
        parser.error("Telegram 用户 ID 必须是整数")
    if not user_ids:
        parser.error("至少需要一个用户 ID")

    # --- Load existing agents ---
    path = _agents_path()
    agents: list[dict] = []
    if path.is_file():
        try:
            agents = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            agents = []

    # Check for duplicate
    if any(a.get("name") == name for a in agents):
        print(f"错误：智能体 '{name}' 已存在。", file=sys.stderr)
        sys.exit(1)

    # Normalize provider name (codex -> openai)
    provider = args.provider
    if provider == "codex":
        provider = "openai"

    # Resolve model against cached model lists
    resolved_model = _resolve_model(provider, args.model)

    # --- Build Telegram agent entry ---
    entry: dict = {
        "name": name,
        "transport": "telegram",
        "telegram_token": args.token,
        "allowed_user_ids": user_ids,
    }

    if provider:
        entry["provider"] = provider
    if resolved_model:
        entry["model"] = resolved_model

    agents.append(entry)

    # Write
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(agents, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    # Write JOIN_NOTIFICATION.md if description provided
    if args.description:
        agent_workspace = _main_home() / "agents" / name / "workspace"
        agent_workspace.mkdir(parents=True, exist_ok=True)
        notification_path = agent_workspace / "JOIN_NOTIFICATION.md"
        notification_path.write_text(args.description + "\n", encoding="utf-8")
        print(f"  JOIN_NOTIFICATION.md written.")

    # --- Output ---
    print(f"子智能体 '{name}' 已创建。")
    print(f"  Telegram 用户：{user_ids}")
    if provider:
        print(f"  提供商：{provider}")
    if resolved_model:
        print(f"  模型：{resolved_model}")
    print("智能体将在数秒内自动启动；用户可直接打开它的 Telegram 聊天。")


if __name__ == "__main__":
    main()
