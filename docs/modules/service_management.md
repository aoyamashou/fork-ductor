# macOS 后台服务

主要代码：`ductor_bot/infra/service_macos.py`。

`ductor service install` 创建 launchd Launch Agent，在用户登录后运行机器人并在异常退出后重启。`status`、`start`、`stop`、`logs` 和 `uninstall` 管理该服务。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
