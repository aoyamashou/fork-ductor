# 模型 CLI

主要代码：`ductor_bot/cli/`。

CLIService 是官方模型 CLI 的统一调用入口。提供商封装负责命令参数、流式事件、认证检查、模型缓存和进程控制。当前支持 Claude、Codex、Gemini、Antigravity 和 Grok。

相关操作与配置见 [配置说明](../config.md)、[系统概览](../system_overview.md) 和 [Telegram 命令帮助](../help.md)。
