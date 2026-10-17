# 安全边界

主要代码：`ductor_bot/security/`。

安全模块负责提示词与输入校验。Telegram 用户和群组白名单控制消息入口；文件路径、Webhook Token 和 API 认证分别由对应模块验证。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
