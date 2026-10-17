# 架构

## 启动

`ductor` 进入 `ductor_bot/__main__.py`，验证当前系统是 macOS arm64，加载 `~/.ductor/config/config.json`，合并新增默认字段并初始化工作区。随后 `AgentSupervisor` 创建主智能体、可选的 Telegram 子智能体、内部任务 API 和观察器。macOS 后台运行通过 launchd Launch Agent 实现。

## 前台消息

Telegram 更新经认证和会话顺序处理中间件进入 `TelegramBot`。`Orchestrator` 先识别 `/` 命令、选择模型及会话，再构造 `AgentRequest`。`CLIService` 按提供商创建对应的 CLI 封装，在工作目录执行官方命令并解析流式事件。机器人把文本增量、工具活动和最终结果发送给 Telegram。

## 会话与目录

`SessionKey("tg", chat_id, topic_id)` 区分私聊、群聊和话题。会话元数据写入 `sessions.json`，命名会话写入 `named_sessions.json`。默认工作目录为 `~/.ductor/workspace/`；`project_roots` 可把特定 Telegram 话题映射到其他项目目录。命名会话始终使用默认工作区，以保持恢复时的目录一致。

## 后台消息

定时任务、Webhook、心跳、后台会话和子智能体回调构造 `Envelope`，由 `MessageBus` 交给 Telegram 传输适配器。前台消息与消息总线共用锁池，避免同一聊天的消息交错。可选 WebSocket API 有自己的连接与锁池。

## 配置更新

配置观察器定时检查配置文件的修改时间。模型、语言、用户白名单、流式显示和部分运行参数可热更新；Telegram Token、Docker、API 等需要重启。配置模型在 `ductor_bot/config.py`，热更新字段清单在 `ductor_bot/config_reload.py`。

## 自动化与隔离

定时任务、Webhook、心跳和清理任务均在同一 asyncio 进程中运行。Docker 沙箱可用于执行模型 CLI；宿主机路径挂载由配置控制。子智能体拥有独立目录和 Telegram Bot Token，主智能体通过内部总线委派任务。
