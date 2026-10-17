# 定时任务

主要代码：`ductor_bot/cron/`。

CronObserver 在进程内按用户时区调度任务。任务定义在 `cron_jobs.json`，可配置模型、目标 Telegram 聊天或话题、成功静默和投递重试。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
