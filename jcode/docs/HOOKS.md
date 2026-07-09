# 生命周期钩子（Lifecycle Hooks）

jcode 可以在定义好的生命周期节点上运行外部命令，这样其他程序就可以观察或控制代理行为，而无需修改 jcode 本身。这些钩子是对 [spawn 钩子](https://github.com/1jehuang/jcode/blob/master/docs/SPAWN_HOOK.md)（用于控制有头会话在何处显示）的补充；生命周期钩子则告诉你这些会话内部正在发生什么。

## 配置

```toml
# ~/.jcode/config.toml
[hooks]
turn_end = "~/bin/jcode-turn-notify"   # observer
session_start = ""                     # observer
session_end = ""                       # observer
pre_tool = "~/bin/jcode-tool-policy"   # gate
post_tool = ""                         # observer
pre_tool_timeout_ms = 5000
```

环境变量覆盖（始终优先；设为空值可禁用对应的配置钩子）：
`JCODE_HOOK_TURN_END`、`JCODE_HOOK_SESSION_START`、`JCODE_HOOK_SESSION_END`、`JCODE_HOOK_PRE_TOOL`、`JCODE_HOOK_POST_TOOL`、`JCODE_HOOK_PRE_TOOL_TIMEOUT_MS`。

## 通用契约

- 钩子命令行按 shell 风格解析（支持引号和反斜杠转义），但直接执行，不经过 shell。程序路径开头的 `~/` 会被展开。
- 钩子在会话的工作目录中运行（如果已知）。
- 每个钩子都会收到以下环境变量：

| 变量 | 含义 |
|---|---|
| `JCODE_HOOK_EVENT` | `turn_end`、`session_start`、`session_end`、`pre_tool`、`post_tool` |
| `JCODE_HOOK_SESSION_ID` | 事件所属的会话 ID |
| `JCODE_HOOK_CWD` | 会话的工作目录 |
| `JCODE_HOOK_PAYLOAD` | JSON 对象，镜像所有字段（上限 16 KB）|
| `JCODE_HOOKS_DISABLED` | 始终为 `1`；用于在嵌套的 jcode 调用中抑制钩子（递归防护）|

## 观察者钩子（Observer hooks）

`turn_end`、`session_start`、`session_end` 和 `post_tool` 是观察者钩子：以分离（detached）方式触发，即发即忘。它们永远不会阻塞或拖慢代理；失败只会被记录。

### turn_end

在代理回合完成时触发（流式回合路径，涵盖 TUI、桌面、swarm 工作进程和无头会话）。额外字段：
- `JCODE_HOOK_STATUS`（`ok`/`error`）
- `JCODE_HOOK_DURATION_MS`
- `JCODE_HOOK_MODEL`
- `JCODE_HOOK_LAST_ASSISTANT_TEXT`（前 4000 个字符）
- `JCODE_HOOK_ERROR`（失败时）

### session_start / session_end

`session_start` 在代理会话变为活动状态时触发，`JCODE_HOOK_SOURCE` 为 `create`（全新创建）、`attach`（附加到已有会话对象）或 `resume`（按 ID 恢复）。`session_end` 在正常关闭时触发（`JCODE_HOOK_SOURCE=close`）。

### post_tool

在每次工具调用之后触发。额外字段：
- `JCODE_HOOK_TOOL_NAME`
- `JCODE_HOOK_STATUS`
- `JCODE_HOOK_DURATION_MS`
- `JCODE_HOOK_OUTPUT_BYTES`（成功时）
- `JCODE_HOOK_ERROR`（失败时）

## 门控钩子：pre_tool

`pre_tool` 在每次工具调用之前同步运行，并且可以阻止该调用：

- 钩子会收到 `JCODE_HOOK_TOOL_NAME`，以及通过标准输入传入的完整工具输入 JSON（同时会在 `JCODE_HOOK_TOOL_INPUT` 中存放一份截断至 16 KB 的副本）。
- 退出码 `0`：允许调用。
- 退出码 `2`：阻止调用。钩子的 stderr（经过修剪，上限 2000 字符）会作为工具错误返回给模型，以便模型据此调整。
- 其他任何情况均视为“失败开放”（fail-open）：包括其他退出码、超时（`pre_tool_timeout_ms`，默认 5 秒）、命令缺失、spawn 错误等，仅记录警告。**失败开放是有意为之**：一个损坏的策略脚本应该退化为“无策略”，而不是阻塞每一个会话。如果你需要“失败关闭”（fail-closed）语义，请让钩子自身足够健壮（它属于你的信任边界，而非 jcode 的）。

### 示例策略脚本

```bash
#!/usr/bin/env bash
# ~/bin/jcode-tool-policy
# stdin: 工具输入 JSON。环境变量：JCODE_HOOK_TOOL_NAME、JCODE_HOOK_SESSION_ID...

input=$(cat)
case "$JCODE_HOOK_TOOL_NAME" in
  bash)
    if grep -qE 'rm -rf /([^a-zA-Z]|$)|mkfs|dd if=' <<<"$input"; then
      echo "blocked: destructive shell command" >&2
      exit 2
    fi
    ;;
  write|edit)
    if grep -q '"file_path":"/etc/' <<<"$input"; then
      echo "blocked: writes to /etc are not allowed" >&2
      exit 2
    fi
    ;;
esac
exit 0
```

## 示例：回合结束时的 tmux 状态 + 桌面通知

```bash
#!/usr/bin/env bash
# ~/bin/jcode-turn-notify

if [ "$JCODE_HOOK_STATUS" = ok ]; then
  icon=✅
else
  icon=❌
fi

tmux display-message "jcode $icon ${JCODE_HOOK_SESSION_ID:0:12}" 2>/dev/null
notify-send "jcode turn $JCODE_HOOK_STATUS" \
  "${JCODE_HOOK_LAST_ASSISTANT_TEXT:0:120}" 2>/dev/null
exit 0
```

## 示例：将所有钩子活动记录到 JSON 事件日志

将多个钩子指向同一个脚本，并根据 `JCODE_HOOK_EVENT` 进行分发：

```bash
#!/usr/bin/env bash
# ~/bin/jcode-event-log
echo "$JCODE_HOOK_PAYLOAD" >> ~/.local/state/jcode-events.jsonl
```

```toml
[hooks]
turn_end = "~/bin/jcode-event-log"
session_start = "~/bin/jcode-event-log"
session_end = "~/bin/jcode-event-log"
post_tool = "~/bin/jcode-event-log"
```

## 设计说明

- 钩子查找由配置驱动，并在配置重载时重新读取；你可以在不重启 jcode 的情况下添加或修改钩子。
- 热路径（`pre_tool`/`post_tool`）会在构建任何 payload 之前检查钩子是否已配置，因此未配置的钩子几乎不产生任何开销。
- 递归防护（`JCODE_HOOKS_DISABLED=1`）意味着钩子可以安全地调用 jcode CLI 命令，而不会在嵌套进程中再次触发钩子。