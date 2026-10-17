# 仓库开发说明

## 项目概览

ductor 是运行在 macOS Apple Silicon (arm64) 上的 Telegram 智能体编排器。它通过官方 `claude`、`codex`、`gemini`、`agy`、`grok` CLI 子进程执行请求，在同一个 asyncio 进程中管理主智能体、Telegram 子智能体和自动化任务。可选的加密 WebSocket API 是独立的直接接入方式。

技术栈：Python 3.11+、aiogram 3.x、aiohttp、Pydantic 2.x、asyncio。建议本地使用 Python 3.13。

## 开发命令

```bash
uv sync --python 3.13 --extra dev
uv run ductor
uv run pytest
uv run ruff check .
uv run mypy ductor_bot
python3 -m ductor_bot.i18n.check
```

## 运行路径

```text
Telegram 更新 → 认证和顺序处理中间件 → TelegramBot
  → Orchestrator → CLIService → 模型 CLI 子进程 → Telegram 发送

后台观察器 / TaskHub / 智能体总线
  → Envelope → MessageBus → TelegramTransport
```

Telegram 私聊、群组和论坛话题使用 `SessionKey("tg", chat_id, topic_id)` 隔离上下文。可选 API 使用独立的 `api` 会话标识。前台 Telegram 消息和 MessageBus 共用锁池。

## 模块地图

| 模块 | 职责 |
| --- | --- |
| `cli_commands/` | 终端命令 |
| `messenger/telegram/` | Telegram 接收、认证、流式回复、按钮和媒体 |
| `messenger/` | 消息协议、通知与 Telegram 注册表 |
| `orchestrator/` | 命令路由、会话、模型和任务编排 |
| `bus/` | Envelope、MessageBus 与锁池 |
| `cli/` | 官方模型 CLI 封装、流式事件和进程控制 |
| `session/` | 提供商隔离会话与命名会话 |
| `tasks/`、`background/` | 委派任务与命名后台会话 |
| `multiagent/` | 主智能体与 Telegram 子智能体监督器 |
| `api/` | 可选加密 WebSocket API 与文件端点 |
| `cron/`、`webhook/`、`heartbeat/`、`cleanup/` | 进程内自动化 |
| `workspace/` | 数据路径、工作区初始化、规则和技能同步 |
| `infra/service_macos.py` | macOS launchd 后台服务 |

## 配置与持久化

`DuctorPaths` (`workspace/paths.py`) 是运行路径的统一来源，默认数据目录为 `~/.ductor/`。主配置在 `config/config.json`；会话、任务、定时任务、Webhook、智能体注册表和日志分别保存在同目录中的 JSON 或 Markdown 文件。

配置加载会递归补全新字段。`language` 默认 `zh-CN`；消息传输只允许 `telegram`。模型、语言、白名单等部分字段可热更新；Token、Docker 与 API 配置需要重启。

工作区初始化分为框架管理文件的覆盖更新和用户文件的首次创建。规则和技能同步由 `workspace/` 管理。子智能体拥有独立工作区与 Telegram Bot Token，位于 `~/.ductor/agents/<name>/`。

## 行为约定

- `/new` 清空当前会话键的默认提供商桶。
- `/reset` 清空当前活动提供商桶。
- `MessageBus` 是后台结果的统一投递路径。
- 模型缓存观察器只为启动认证检查发现的 CLI 创建。
- 后台服务使用 launchd，监督器的重启退出码为 `42`。
- 测试使用 `asyncio_mode = "auto"`；代码行长 100；ruff 严格规则；mypy strict。

用户帮助与开发文档见 [docs/README.md](docs/README.md)。
