#!/usr/bin/env bash
# 从 aoyamashou/fork-ductor 安装 macOS Apple Silicon 版 ductor。
set -Eeuo pipefail

REPO_ARCHIVE="https://github.com/aoyamashou/fork-ductor/archive/refs/heads/main.tar.gz"
UV_INSTALL_URL="https://astral.sh/uv/install.sh"
INSTALL_ONLY="${DUCTOR_INSTALL_ONLY:-0}"
SOURCE_DIR="${DUCTOR_SOURCE_DIR:-}"

say() { printf '\n[ductor] %s\n' "$*"; }
fail() { printf '\n[ductor] 错误：%s\n' "$*" >&2; exit 1; }

[[ "$(uname -s)" == "Darwin" && "$(uname -m)" == "arm64" ]] ||
    fail "此安装脚本仅支持 macOS Apple Silicon（arm64）。"
[[ "$(id -u)" != "0" ]] || fail "请使用普通用户运行，不要使用 sudo。"
command -v curl >/dev/null 2>&1 || fail "找不到 curl。"
command -v tar >/dev/null 2>&1 || fail "找不到 tar。"

TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/ductor-install.XXXXXX")"
trap 'rm -rf -- "$TEMP_DIR"' EXIT

if ! command -v uv >/dev/null 2>&1; then
    say "正在安装 uv..."
    curl -fsSL --retry 3 "$UV_INSTALL_URL" -o "$TEMP_DIR/uv-install.sh"
    sh "$TEMP_DIR/uv-install.sh"
    export PATH="$HOME/.local/bin:$PATH"
fi
command -v uv >/dev/null 2>&1 || fail "uv 安装后仍不可用，请检查 ~/.local/bin。"
UV_BIN="$(command -v uv)"

say "正在准备 Python 3.13..."
"$UV_BIN" python install 3.13

if [[ -n "$SOURCE_DIR" ]]; then
    [[ -f "$SOURCE_DIR/pyproject.toml" ]] || fail "本地源码目录无效：$SOURCE_DIR"
    BUILD_SOURCE="$SOURCE_DIR"
else
    say "正在下载 aoyamashou/fork-ductor 的 main 分支..."
    curl -fsSL --retry 3 "$REPO_ARCHIVE" -o "$TEMP_DIR/source.tar.gz"
    mkdir "$TEMP_DIR/source"
    tar -xzf "$TEMP_DIR/source.tar.gz" --strip-components=1 -C "$TEMP_DIR/source"
    BUILD_SOURCE="$TEMP_DIR/source"
fi

say "正在构建安装包..."
"$UV_BIN" build --wheel --out-dir "$TEMP_DIR/dist" "$BUILD_SOURCE"
WHEELS=("$TEMP_DIR"/dist/ductor-*.whl)
[[ ${#WHEELS[@]} -eq 1 && -f "${WHEELS[0]}" ]] ||
    fail "未生成唯一的 ductor 安装包。"

TOOL_BIN="$("$UV_BIN" tool dir --bin)/ductor"
PLIST="$HOME/Library/LaunchAgents/dev.ductor.plist"
CONFIG="$HOME/.ductor/config/config.json"

say "正在检查安装依赖..."
UV_TOOL_DIR="$TEMP_DIR/staged-tools" UV_TOOL_BIN_DIR="$TEMP_DIR/staged-bin" \
    "$UV_BIN" tool install --python 3.13 "${WHEELS[0]}"

if [[ "$INSTALL_ONLY" != "1" && ( -f "$PLIST" || -f "$CONFIG" ) ]]; then
    say "正在备份现有设置..."
    BACKUP="$HOME/.ductor/backups/pre-one-click-$(date +%Y%m%d-%H%M%S)"
    mkdir -m 700 -p "$BACKUP"
    if [[ -f "$PLIST" ]]; then
        cp -p "$PLIST" "$BACKUP/dev.ductor.plist"
    fi
    if [[ -f "$CONFIG" ]]; then
        cp -p "$CONFIG" "$BACKUP/config.json"
    fi
    say "备份位置：$BACKUP"
fi

if [[ "$INSTALL_ONLY" != "1" && -f "$PLIST" ]]; then
    say "正在停止旧服务..."
    if [[ -x "$TOOL_BIN" ]]; then
        "$TOOL_BIN" service uninstall
    elif launchctl list dev.ductor >/dev/null 2>&1; then
        launchctl unload -w "$PLIST"
    fi
    launchctl list dev.ductor >/dev/null 2>&1 && fail "旧服务仍在运行，请手动停止后重试。"
fi

say "正在安装修改版..."
"$UV_BIN" tool install --force --reinstall-package ductor --python 3.13 "${WHEELS[0]}"
[[ -x "$TOOL_BIN" ]] || fail "安装完成后找不到 ductor 命令：$TOOL_BIN"

if [[ "$INSTALL_ONLY" == "1" ]]; then
    say "安装完成：${TOOL_BIN}（已跳过服务启动）。"
    exit 0
fi

if [[ -f "$CONFIG" ]]; then
    PYTHON_BIN="$("$UV_BIN" python find 3.13)"
    "$PYTHON_BIN" - "$CONFIG" <<'PY'
import json
import os
import sys
import tempfile
from pathlib import Path

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding="utf-8"))
data["language"] = "zh-CN"
data["transport"] = "telegram"
data["transports"] = ["telegram"]
data.pop("matrix", None)
data.pop("slack", None)
fd, temp_path = tempfile.mkstemp(prefix=".config-", suffix=".json", dir=path.parent)
try:
    with os.fdopen(fd, "w", encoding="utf-8") as stream:
        json.dump(data, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    os.chmod(temp_path, 0o600)
    os.replace(temp_path, path)
finally:
    if os.path.exists(temp_path):
        os.unlink(temp_path)
PY
fi

if [[ -f "$CONFIG" ]]; then
    PYTHON_BIN="$("$UV_BIN" python find 3.13)"
    if "$PYTHON_BIN" - "$CONFIG" <<'PY'
import json
import sys
from pathlib import Path

data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
token = data.get("telegram_token")
users = data.get("allowed_user_ids")
raise SystemExit(0 if token and not str(token).startswith("YOUR_") and users else 1)
PY
    then
        say "正在启动 macOS 后台服务..."
        "$TOOL_BIN" service install
        launchctl list dev.ductor >/dev/null 2>&1 ||
            fail "后台服务未加载，请运行 ductor service logs 查看日志。"
        say "安装完成。使用 ductor status 查看状态。"
        exit 0
    fi
fi

[[ -r /dev/tty ]] || fail "首次配置需要交互终端；安装已完成，请在终端运行 ${TOOL_BIN}。"
say "开始中文首次配置向导..."
"$TOOL_BIN" </dev/tty
