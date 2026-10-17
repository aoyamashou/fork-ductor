# Webhook

主要代码：`ductor_bot/webhook/`。

WebhookObserver 接收经过认证的外部事件，可唤醒当前聊天或创建独立后台任务。监听地址、Token、请求大小和速率限制由 `webhooks` 配置控制。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
