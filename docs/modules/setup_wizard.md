# 首次配置向导

主要代码：`ductor_bot/cli/init_wizard.py`。

首次运行检查模型 CLI 登录状态，收集 Telegram Bot Token、允许的用户 ID、Docker 选项、时区和 launchd 服务设置，然后写入 `config.json`。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
