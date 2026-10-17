# 系统概览

本分支只接收 Telegram 消息，运行在 macOS Apple Silicon。可选的加密 WebSocket API 提供直接接入；它与 Telegram 共享 Orchestrator，但使用独立的会话标识。

```text
Telegram 更新
  → 认证与顺序处理中间件
  → TelegramBot
  → Orchestrator
  → CLIService
  → 官方模型 CLI 子进程
  → Telegram 消息发送
```

每条会话使用 `SessionKey(transport, chat_id, topic_id)` 标识。Telegram 私聊、群聊和论坛话题分别保存上下文；切换模型时，每个提供商仍维护自己的会话桶。`/new` 清空默认提供商的当前会话；`/reset` 清空当前活动提供商的会话。

后台任务、定时任务、Webhook 与心跳在同一个 asyncio 进程中运行。它们通过 `MessageBus` 统一向 Telegram 交付结果。`AgentSupervisor` 同时管理主智能体和可选的 Telegram 子智能体。主智能体状态位于 `~/.ductor/`；子智能体位于 `~/.ductor/agents/<name>/`。

主要代码入口：

| 位置 | 职责 |
| --- | --- |
| `ductor_bot/__main__.py` | 命令行入口、配置加载与启动 |
| `ductor_bot/config.py` | Pydantic 配置模型 |
| `ductor_bot/messenger/telegram/` | Telegram 消息接收与发送 |
| `ductor_bot/orchestrator/` | 命令路由、会话、任务与生命周期 |
| `ductor_bot/cli/` | 模型 CLI 封装和输出解析 |
| `ductor_bot/bus/` | 后台消息投递 |
| `ductor_bot/workspace/` | 路径、工作区初始化和规则同步 |
| `ductor_bot/multiagent/` | 子智能体管理与内部通信 |
| `ductor_bot/infra/service_macos.py` | launchd 服务安装与控制 |
