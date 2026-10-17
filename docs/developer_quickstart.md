# 开发快速入门

## 准备环境

本分支只支持 macOS Apple Silicon（arm64）。建议使用 Python 3.13：

```bash
brew install uv
uv python install 3.13
uv sync --python 3.13 --extra dev
```

运行检查：

```bash
uv run pytest
uv run ruff check .
uv run mypy ductor_bot
python3 -m ductor_bot.i18n.check
```

## 本地运行

```bash
uv run ductor
uv run ductor -v
```

首次运行会创建 `~/.ductor/` 并打开 Telegram 配置向导。测试时可用 `DUCTOR_HOME` 指向单独的数据目录，避免覆盖日常机器人状态。

## 修改代码

- 修改 Telegram 交互：从 `ductor_bot/messenger/telegram/` 的处理器开始。
- 修改命令路由：查看 `ductor_bot/orchestrator/`。
- 修改模型执行：查看 `ductor_bot/cli/service.py` 和各提供商封装。
- 修改配置：同时更新 `AgentConfig`、`config.example.json` 和相关测试。
- 修改用户文案：更新 `ductor_bot/i18n/zh-CN/`，运行完整性检查，保留 `{name}` 等占位符和 Rich 样式标签。
- 修改后台投递：查看 `ductor_bot/bus/`，确保同一聊天的消息顺序正确。

工作区初始化分为覆盖更新的框架文件和只在首次运行时创建的用户文件。更新模板前先查看 `ductor_bot/workspace/init.py`，避免覆盖用户自有内容。
