# ductor（macOS Apple Silicon 版）

ductor 让你通过 Telegram 使用本机已安装的 Claude Code、Codex、Gemini、Antigravity 或 Grok CLI。机器人在你的 Mac 上运行，调用官方 CLI 子进程，并把结果发送回 Telegram。项目需要 macOS Apple Silicon（arm64）和 Python 3.11 或更新版本。

这个分支只提供 Telegram 消息接入。可选的加密 WebSocket API 仍可用于直接连接；它不属于消息平台。

## 一键安装与首次启动

将此分支推送到你自己的 GitHub 仓库 `aoyamashou/fork-ductor` 的 `main` 分支后，在 macOS Apple Silicon 的终端运行：

```bash
curl -fsSL https://raw.githubusercontent.com/aoyamashou/fork-ductor/main/scripts/install.sh | bash
```

脚本会安装 uv 和 Python 3.13，从该仓库下载并构建 ductor，保留并备份现有配置，然后安装修改版。已有 Telegram 配置时会启动 launchd 后台服务；首次安装会进入中文向导。重新运行同一命令即可安装仓库中的新版本。脚本源码见 [scripts/install.sh](scripts/install.sh)。

也可以在项目目录中手动运行开发版：

```bash
brew install uv
uv python install 3.13
uv sync --python 3.13 --extra dev
uv run ductor
```

首次启动会检查可用的模型 CLI，要求至少有一个已安装且完成登录；然后引导你填写 Telegram Bot Token 和允许使用机器人的用户 ID。Bot Token 可在 Telegram 的 `@BotFather` 使用 `/newbot` 创建；用户 ID 可向 `@userinfobot` 发送 `/start` 查询。

向导还会询问是否启用 Docker 隔离、时区及 macOS 登录后自动启动。配置和运行数据位于 `~/.ductor/`。如果想使用其他位置，启动前设置 `DUCTOR_HOME`。

```bash
export DUCTOR_HOME="$HOME/.ductor"
uv run ductor
```

## 日常使用

给机器人发送普通消息即可调用当前模型。Telegram 私聊、群聊和论坛话题分别保存会话；每个话题可切换自己的模型。所有会话共享主智能体工作区，除非通过 `project_roots` 为话题指定项目目录。

常用机器人命令：

| 命令 | 作用 |
| --- | --- |
| `/help` | 查看完整命令帮助 |
| `/model` | 查看或切换模型与提供商 |
| `/effort` | 设置推理强度 |
| `/new` | 为当前聊天开启新会话 |
| `/reset` | 重置当前提供商会话 |
| `/stop` | 停止当前任务并清空等待队列 |
| `/interrupt` | 中断当前任务，保留等待队列 |
| `/status` | 查看当前会话状态 |
| `/memory` | 查看主记忆 |
| `/session` | 创建或管理命名后台会话 |
| `/tasks` | 查看后台任务 |
| `/cron` | 管理定时任务 |
| `/showfiles` | 浏览工作区文件 |
| `/diagnose` | 查看运行诊断 |

主智能体可创建独立的 Telegram 子智能体。每个子智能体使用自己的 Bot Token、工作区和模型配置，可通过 `ductor agents add <名称>` 创建。

## 终端命令

```bash
uv run ductor status                 # 查看运行状态
uv run ductor service install        # 安装 launchd 登录启动服务
uv run ductor service status         # 查看服务状态
uv run ductor service logs           # 查看日志
uv run ductor service stop           # 停止服务
uv run ductor agents list            # 查看子智能体
uv run ductor docker enable          # 启用 Docker 隔离
uv run ductor api enable             # 启用可选的加密 WebSocket API
```

`ductor reset` 会重新执行向导并清除已有数据，使用前请备份 `~/.ductor/`。`ductor uninstall` 也会删除该目录。

## 配置与数据

主配置文件是 `~/.ductor/config/config.json`。常用字段：

| 字段 | 说明 |
| --- | --- |
| `provider`、`model` | 默认模型提供商和模型 |
| `language` | 界面语言；本分支默认 `zh-CN` |
| `telegram_token` | Telegram Bot Token |
| `allowed_user_ids` | 可使用机器人的用户 ID 列表 |
| `allowed_group_ids` | 可访问的群组 ID 列表 |
| `user_timezone` | 定时任务和安静时段使用的时区 |
| `project_roots` | 将 Telegram 话题映射到本地项目目录 |
| `docker.enabled` | 是否在 Docker 沙箱中执行模型 CLI |
| `heartbeat.enabled` | 是否开启定期主动检查 |
| `api.enabled` | 是否开启独立的加密 WebSocket API |

部分配置可在运行时更新；Telegram Token、Docker 与 API 等设置需要重启。完整字段见 [配置示例](config.example.json)。不要把真实 Token 提交到 Git。

数据目录还包括会话、任务、定时任务、日志和工作区文件。代码入口在 `ductor_bot/__main__.py`；消息处理在 `ductor_bot/messenger/telegram/`，模型调用在 `ductor_bot/cli/`，路由在 `ductor_bot/orchestrator/`。

## 开发

```bash
uv sync --python 3.13 --extra dev
uv run pytest
uv run ruff check .
uv run mypy ductor_bot
```

更多说明见 [中文文档索引](docs/README.md)。项目使用 MIT 许可证，见 [LICENSE](LICENSE)。
