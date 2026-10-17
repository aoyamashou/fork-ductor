# 加密 WebSocket API

主要代码：`ductor_bot/api/`。

可选直接 API 使用认证的 WebSocket 连接和加密帧，把请求交给 Orchestrator，并通过独立文件端点上传或下载文件。它不属于 Telegram 消息接入；默认关闭，可使用 `ductor api enable` 配置。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
