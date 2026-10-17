# 配置热更新

主要代码：`ductor_bot/config_reload.py`。

配置观察器按修改时间读取 `config.json`，用 Pydantic 验证后应用可热更新字段。Token、Docker 与 API 等设置需要重启；具体字段以 `_HOT_RELOADABLE` 为准。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
