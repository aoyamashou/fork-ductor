# 后台任务

主要代码：`ductor_bot/tasks/`。

TaskHub 运行委派任务，支持并发上限、取消、结果保留和持久注册表。任务结果经 MessageBus 返回原 Telegram 聊天。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
