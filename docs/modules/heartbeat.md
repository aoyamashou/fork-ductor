# 心跳检查

主要代码：`ductor_bot/heartbeat/`。

心跳观察器按间隔运行提示词，并根据静默时段、冷却时间和确认标记决定是否向 Telegram 发送结果。可为群组话题设置单独目标。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
