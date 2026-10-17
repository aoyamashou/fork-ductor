# 在 macOS Apple Silicon 上安装

## 一键安装

此分支推送到 `aoyamashou/fork-ductor` 的 `main` 分支后，在 Mac 的终端运行：

```bash
curl -fsSL https://raw.githubusercontent.com/aoyamashou/fork-ductor/main/scripts/install.sh | bash
```

脚本只接受 macOS Apple Silicon（arm64）。它会自动安装 uv 和 Python 3.13，从你的仓库下载源码并构建安装包，使用 `uv tool` 安装。已有配置会先备份到 `~/.ductor/backups/`，Telegram 配置会切换为简体中文，然后用 launchd 启动；新用户会进入中文向导。脚本运行时需要网络连接和终端交互。以后更新也可以重新运行同一命令。

安装完成后检查：

```bash
ductor status
ductor service logs
```

若终端提示找不到 `ductor`，请新开一个终端，或运行 `export PATH="$HOME/.local/bin:$PATH"`。

## 前提

- macOS Apple Silicon（arm64）。
- Python 3.11 或更新版本，建议 3.13。
- 已安装并登录至少一个官方 CLI：`claude`、`codex`、`gemini`、`agy` 或 `grok`。
- Telegram Bot Token 和你的 Telegram 数字用户 ID。

## 从源码运行（开发）

```bash
brew install uv
uv python install 3.13
uv sync --python 3.13 --extra dev
uv run ductor
```

首次运行会打开向导。向导检查模型 CLI 的登录状态，然后依次收集 Telegram Bot Token、允许访问的用户 ID、Docker 选项、时区和后台服务选项。Token 可通过 `@BotFather` 的 `/newbot` 创建；用户 ID 可向 `@userinfobot` 发送 `/start` 查询。

机器人默认只接受 `allowed_user_ids` 中的用户。需要在群组使用时，还应把群组 ID 加入 `allowed_group_ids`。所有配置保存在 `~/.ductor/config/config.json`。

## 后台服务

项目使用 macOS 的 launchd Launch Agent。在向导中选择后台运行，或手动执行：

```bash
uv run ductor service install
uv run ductor service status
uv run ductor service logs
```

服务会在用户登录后启动，并在异常退出后重启。停止或卸载服务：

```bash
uv run ductor service stop
uv run ductor service uninstall
```

## Docker 隔离

向导可启用 Docker 沙箱，让模型 CLI 在容器中执行。若要访问宿主机项目目录，可使用 `ductor docker mount <路径>`；修改挂载后重启或重建容器。也可以在 `config.json` 中设置 `docker.enabled` 和 `docker.mounts`。

## 常见问题

- **机器人未回复**：先运行 `uv run ductor status`，再查看 `uv run ductor service logs`；检查 Token、用户 ID、CLI 登录状态。
- **找不到模型 CLI**：确认启动 launchd 服务时使用的账户及 PATH 能访问该 CLI。
- **修改配置不生效**：模型、语言、用户白名单等字段支持热更新；Token、Docker 和 API 设置需要重启。
- **Python 依赖安装失败**：使用 `uv python install 3.13`，再用 `uv sync --python 3.13 --extra dev` 重建环境。

## 升级与移除

通过一键脚本安装时，重新执行上述 `curl` 命令即可升级到仓库 `main` 分支的最新代码；避免使用 `ductor upgrade`，以免改装成上游发布版。从源码开发时，使用 Git 更新代码并重新同步依赖。删除服务和本地数据前，先备份 `~/.ductor/`；`ductor reset` 与 `ductor uninstall` 都可能清除数据。
