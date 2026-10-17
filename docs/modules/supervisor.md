# 进程监督

主要代码：`ductor_bot/multiagent/supervisor.py`。

监督器在一个 asyncio 进程中启动主智能体、子智能体和任务系统，监视智能体注册表并处理异常恢复。退出码 42 表示请求重启。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
