# 会话

主要代码：`ductor_bot/session/`。

SessionKey 使用 `tg`、Telegram chat ID 和可选话题 ID 隔离上下文。会话按模型提供商分桶并写入 `sessions.json`；命名会话另存于 `named_sessions.json`。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
