# 命名后台会话

主要代码：`ductor_bot/background/`。

`/session` 创建可继续的命名后台会话。执行结果经消息总线回到原 Telegram 聊天；会话注册表保存于 `named_sessions.json`。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
