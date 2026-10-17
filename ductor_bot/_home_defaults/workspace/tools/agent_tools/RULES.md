# 子智能体工具

本分支只创建 Telegram 子智能体。每个子智能体都有独立的 Bot Token、聊天、工作区和记忆。主智能体可以把任务交给子智能体；结果会回到发起委派的智能体聊天。创建后，也应告诉用户可以直接打开子智能体的 Telegram 聊天。

## 可用工具

| 工具 | 用途 |
| --- | --- |
| `ask_agent.py` | 同步向子智能体提问 |
| `ask_agent_async.py` | 异步委派任务 |
| `edit_shared_knowledge.py` | 查看或编辑共享记忆 |
| `create_agent.py` | 创建 Telegram 子智能体；仅主智能体使用 |
| `remove_agent.py` | 从注册表移除子智能体；仅主智能体使用 |
| `list_agents.py` | 查看子智能体状态 |

创建子智能体时，先为它在 `@BotFather` 创建独立机器人，再确认获准使用的 Telegram 数字用户 ID：

```bash
python3 tools/agent_tools/create_agent.py \
  --name "researcher" \
  --token "BOT_TOKEN" \
  --users "USER_ID1,USER_ID2" \
  --provider claude \
  --model sonnet \
  --description "负责资料研究"
```

`--model` 应使用具体模型 ID，而不是提供商名称。`create_agent.py` 写入 `agents.json` 后，运行中的监督器会自动发现并启动它。子智能体工作区位于 `~/.ductor/agents/<name>/workspace/`。

内部工具命令无需直接展示给 Telegram 用户；用户只需要知道如何打开对应机器人的聊天，以及委派任务的结果会发回原聊天。
