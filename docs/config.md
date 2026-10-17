# 配置说明

主配置文件是 `~/.ductor/config/config.json`。首次运行向导会创建它；完整示例见 [config.example.json](../config.example.json)。配置加载时会递归补全新版本新增的默认字段，同时保留用户已设置的值。

此分支只支持 `"transport": "telegram"` 与 `"transports": ["telegram"]`。加载旧配置时会移除 Matrix/Slack 专用字段；如果仍将它们设为消息接入方式，配置校验会拒绝启动。可选的 `api` 是加密 WebSocket 接口，与消息平台配置分开。

## 基本字段

| 字段 | 作用 |
| --- | --- |
| `provider`、`model` | 默认模型提供商和模型 |
| `language` | 用户界面语言，默认 `zh-CN` |
| `ductor_home` | 数据目录，通常为 `~/.ductor` |
| `user_timezone` | 定时任务和安静时段的时区；留空时检测系统时区 |
| `log_level` | 日志级别 |
| `permission_mode` | 模型 CLI 权限模式 |
| `reasoning_effort` | 默认推理强度 |
| `cli_parameters` | 各模型 CLI 的附加参数 |
| `append_system_prompt_files` | 追加到系统提示词的本地文件 |
| `project_roots` | Telegram 话题与项目目录的映射 |

## Telegram

| 字段 | 作用 |
| --- | --- |
| `telegram_token` | 由 `@BotFather` 创建的 Bot Token |
| `allowed_user_ids` | 允许使用机器人的用户 ID 列表 |
| `allowed_group_ids` | 允许使用的群组 ID 列表 |
| `allowed_channel_ids` | 允许使用的频道 ID 列表 |
| `group_mention_only` | 群组中是否仅处理提及机器人的消息 |
| `streaming` | 流式消息编辑、刷新间隔与工具活动展示 |
| `scene` | 已读反应、状态反应和技术信息页脚 |

## 运行与自动化

| 配置段 | 作用 |
| --- | --- |
| `docker` | 沙箱镜像、容器、挂载和额外软件包 |
| `timeouts` | 前台、后台与子智能体执行超时 |
| `tasks` | 后台任务并发、超时和结果保留 |
| `heartbeat` | 主动检查的间隔、静默时段和目标聊天 |
| `webhooks` | Webhook 监听地址、Token 和请求限制 |
| `cleanup` | 文件清理保留期和运行时间 |
| `notifications` | 启动及升级通知目标 |
| `api` | 可选加密 WebSocket API |
| `transcription` | 音频和视频转录命令 |
| `skills` | 跨模型 CLI 的技能同步 |
| `memory_flush`、`memory_reflection`、`memory_compaction` | 记忆刷新、回顾和压缩 |

`project_roots` 的键可以是话题名称、话题 ID，或 `<chat_id>:<topic_id>`；值是已存在的本地目录。Docker 模式及命名后台会话不会使用该映射。

## 热更新

模型、提供商、推理强度、语言、Telegram 用户白名单、流式配置、心跳及部分会话参数可在配置文件变更后自动更新。Telegram Token、Docker 与 API 等字段需要重启。具体字段列表以 `ductor_bot/config_reload.py` 为准。

不要提交包含真实 Token 的 `config.json`。如果需要迁移数据，先停止机器人，再复制整个 `~/.ductor/` 目录。
