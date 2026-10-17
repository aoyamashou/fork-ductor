# Telegram 机器人

主要代码：`ductor_bot/messenger/telegram/`。

aiogram 负责接收更新、身份验证、群组与话题检查、流式消息编辑、回调按钮和媒体文件。消息交给 Orchestrator 后，响应再由 Telegram 发送器投递。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
