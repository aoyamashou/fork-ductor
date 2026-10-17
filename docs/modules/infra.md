# 运行基础设施

主要代码：`ductor_bot/infra/`。

基础设施模块管理 PID 锁、进程退出、Docker 沙箱、升级和恢复。后台服务使用 macOS launchd Launch Agent；本分支仅在 macOS arm64 启动。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
