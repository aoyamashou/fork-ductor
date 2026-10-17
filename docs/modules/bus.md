# 消息总线

主要代码：`ductor_bot/bus/`。

后台观察器、任务和智能体回调使用统一 Envelope，经 MessageBus 投递到 Telegram。前台消息和后台投递共用锁池，防止同一聊天的输出交错。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
