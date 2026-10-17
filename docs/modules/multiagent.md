# 多智能体

主要代码：`ductor_bot/multiagent/`。

AgentSupervisor 管理主智能体和 Telegram 子智能体。子智能体在 `agents.json` 定义，各自拥有 Token、会话和工作区；内部总线负责委派与结果返回。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
