# jcode [![Latest Release](https://badgen.net/github/release/1jehuang/jcode?icon=github)](https://github.com/1jehuang/jcode/releases) [![License: MIT](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](LICENSE) [![Platforms](https://img.shields.io/badge/platforms-Linux%20%7C%20macOS%20%7C%20Windows-blue?style=flat-square)](https://github.com/1jehuang/jcode/releases) [![Last Commit](https://badgen.net/github/last-commit/1jehuang/jcode/master?icon=github)](https://github.com/1jehuang/jcode/commits/master) [![GitHub Stars](https://badgen.net/github/stars/1jehuang/jcode?icon=github)](https://github.com/1jehuang/jcode/stargazers) [![Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2?style=flat-square&logo=discord&logoColor=white)](https://discord.gg/nBe9vGyK9a)

下一代 Coding Agent 测试与评估框架（Coding Agent Harness），旨在提升技能天花板。
专为多会话工作流、无限可定制性和极致性能而设计。

[网站](https://solosystems.dev/jcode) · [功能](#features) · [安装](#installation) · [快速开始](#quick-start) · [延伸阅读](#further-reading) · [贡献指南](CONTRIBUTING.md)

## 安装

```bash
# macOS & Linux
curl -fsSL https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/install.sh | bash
```

需要 Windows、Homebrew、源码编译、配置 Provider，或者想让你的 Agent 帮你安装？[跳转到详细安装说明](#detailed-installation)。

## 性能与资源效率

jcode 在设计上追求极致的性能和资源效率。每一项指标都经过深度优化，这对于扩展多会话工作流至关重要。以下是几个关键指标的对比：内存占用和启动速度。

### 内存占用对比

**1 个活动会话**

| 工具 | PSS | 对比 |
|---|---|---|
| **jcode（关闭本地嵌入）** | **27.8 MB** | 基准 |
| **jcode** | 167.1 MB | 6.0× |
| pi | 144.4 MB | 5.2× |
| Codex CLI | 140.0 MB | 5.0× |
| OpenCode | 371.5 MB | 13.4× |
| GitHub Copilot CLI | 333.3 MB | 12.0× |
| Cursor Agent | 214.9 MB | 7.7× |
| Claude Code | 386.6 MB | 13.9× |
| Antigravity CLI | 243.7 MB | 8.8× |

**10 个活动会话**

| 工具 | PSS | 对比 |
|---|---|---|
| **jcode（关闭本地嵌入）** | **117.0 MB** | 基准 |
| **jcode** | 260.8 MB | 2.2× |
| pi | 833.0 MB | 7.1× |
| Codex CLI | 334.8 MB | 2.9× |
| OpenCode | 3237.2 MB | 27.7× |
| GitHub Copilot CLI | 1756.5 MB | 15.0× |
| Cursor Agent | 1632.4 MB | 14.0× |
| Claude Code | 2300.6 MB | 19.7× |
| Antigravity CLI | 1021.2 MB | 8.7× |

### 首帧时间（Time to first frame）

| 工具 | 首帧时间 | 范围 | 对比 |
|---|---|---|---|
| **jcode** | **14.0 ms** | 10.1–19.3 ms | 基准 |
| **Antigravity CLI** | **383.5 ms** | 363.1–415.4 ms | **27.4× 更慢** |
| **pi** | **590.7 ms** | 369.6–934.8 ms | **42.2× 更慢** |
| **Codex CLI** | **882.8 ms** | 742.3–1640.9 ms | **63.1× 更慢** |
| **OpenCode** | **1035.9 ms** | 922.5–1104.4 ms | **74.0× 更慢** |
| **GitHub Copilot CLI** | **1518.6 ms** | 1357.4–1826.8 ms | **108.5× 更慢** |
| **Cursor Agent** | **1949.7 ms** | 1711.0–2104.8 ms | **139.3× 更慢** |
| **Claude Code** | **3436.9 ms** | 2032.7–8927.2 ms | **245.5× 更慢** |

在 Linux 机器上通过 10 次交互式 PTY 启动测得。

### 首输入响应时间（Time to first input）

即键入的探测文本出现在渲染屏幕上的时间；Antigravity 使用其内部输入就绪日志标记，因为登录屏会抑制探测回显。

| 工具 | 首输入响应 | 范围 | 对比 |
|---|---|---|---|
| **jcode** | **48.7 ms** | 30.3–62.7 ms | 基准 |
| **Antigravity CLI** | **383.7 ms** | 363.4–415.7 ms | **7.9× 更慢** |
| **pi** | **596.4 ms** | 373.9–955.2 ms | **12.2× 更慢** |
| **Codex CLI** | **905.8 ms** | 760.1–1675.7 ms | **18.6× 更慢** |
| **OpenCode** | **1047.9 ms** | 931.1–1116.9 ms | **21.5× 更慢** |
| **GitHub Copilot CLI** | **1583.4 ms** | 1422.8–1880.0 ms | **32.5× 更慢** |
| **Cursor Agent** | **1978.7 ms** | 1727.3–2130.0 ms | **40.6× 更慢** |
| **Claude Code** | **3512.8 ms** | 2137.4–9002.0 ms | **72.2× 更慢** |

在 Linux 机器上通过 10 次交互式 PTY 启动测得。Antigravity CLI 此次运行时未认证；其登录屏正常渲染并输出了内部 `CLI ready for user input` 标记，但未回显键入的探测文本。

### 额外客户端 / 内存扩展

| 工具 | 每增加一个会话的额外 PSS | 对比 |
|---|---|---|
| **jcode（关闭本地嵌入）** | **~9.9 MB** | 基准 |
| **jcode** | **~10.4 MB** | **1.1×** |
| **pi** | **~76.5 MB** | **7.7×** |
| **Codex CLI** | **~21.6 MB** | **2.2×** |
| **OpenCode** | **~318.4 MB** | **32.2×** |
| **GitHub Copilot CLI** | **~158.1 MB** | **16.0×** |
| **Cursor Agent** | **~157.5 MB** | **15.9×** |
| **Claude Code** | **~212.7 MB** | **21.5×** |
| **Antigravity CLI** | **~86.4 MB** | **8.7×** |

本次修正后的内存重测中测试的版本：
- `jcode v0.9.1888-dev (be386f2)`
- `pi 0.62.0`
- `codex-cli 0.120.0`
- `opencode 1.0.203`
- `GitHub Copilot CLI 1.0.24`（1 会话重测）/ `1.0.27`（10 会话重测）
- `Cursor Agent 2026.04.08-a41fba1`
- `Claude Code 2.1.86 (Claude Code)`
- `Antigravity CLI 1.0.0`

## 记忆系统（Agent Memory）

jcode 将每一轮对话/响应嵌入为语义向量。每一轮都会查询记忆图，通过余弦相似度检查高效地找到相关的记忆条目。嵌入命中的内容会被注入对话中，或者可选地由记忆侧代理（memory sideagent）验证相关性，并在注入前进行更多信息检索工作。这形成了一个类人的记忆系统，使 Agent 能够自动回忆与对话相关的信息，而无需主动调用记忆工具或消耗大量 token。

要检索记忆，首先需要提取并存储记忆。每隔一段时间（语义漂移、距上次提取 K 轮、会话结束等），记忆会通过记忆侧代理提取并存入记忆图。该框架还提供了显式的记忆工具，允许 Agent 主动搜索或存储记忆，而不依赖后台被动进程。框架还提供了会话搜索功能，用于对历史会话进行传统 RAG（检索增强生成）搜索。记忆会通过环境模式（ambient mode）定期自动整合，进行重组、检查陈旧性和冲突等。

## UI：侧面板、图表、信息小部件、渲染、滚动、对齐

侧面板用于展示辅助信息。你可以让 jcode Agent 将文件加载到侧面板并实时更新，或让 Agent 直接写入侧面板，亦可将其用作差异对比（diff）查看器。侧面板（和聊天区域）支持内联渲染 Mermaid 图表。

为实现此功能，作者创建了一个全新的 Mermaid 渲染库，渲染速度快 **1800 倍**，且无浏览器和 TypeScript 依赖。参见 https://github.com/1jehuang/mermaid-rs-renderer

为了在不占用回复显示空间的前提下展示重要信息，作者开发了信息小部件（info widgets）。信息小部件只占用屏幕的空白区域来展示信息，空间不足时会自动让位。

jcode 可以 **1000+ fps** 渲染，彻底消除闪烁问题。jcode 的自定义回滚（scrollback）实现使其功能远超终端原生回滚。然而，终端层面的限制使得无法在自定义回滚中实现平滑的逐行滚动。为解决此问题，作者开发了自己的终端 Handterm（https://github.com/1jehuang/handterm），实现了原生滚动 API，且效率极高。此为正在进行中的工作。普通终端的滚动也已良好实现。

jcode 默认**左对齐**。你可以通过 `Alt+C` 快捷键、`/alignment` 命令或在配置文件中切换到居中模式。

## Swarm（集群/多 Agent 协作）

在同一代码库中启动两个或更多 Agent，服务器会自动管理它们，实现原生协作。当 Agent A 修改了 Agent B 已读取的文件时（代码在其脚下变动），服务器会通知 Agent B。Agent B 可以忽略无关通知，或检查差异以避免冲突。每个 Agent 都具备消息能力，可私信单个 Agent、广播给服务器托管的所有 Agent，或仅发送给同一代码库的 Agent。这使你可以在同一代码库中启动多个会话，所有冲突都会自动解决。

Agent 还能够自主调用 Swarm 工具，派生子 Agent 组成团队并行完成任务。这样做会将主 Agent 转变为协调者，子 Agent 转变为工作者。Agent 组、它们的消息通道、完成状态等均由系统自动管理。此功能可在无头（headless）或有头（headed）模式下运行。

## OAuth 与 Provider（模型提供商）

jcode 支持订阅制 OAuth 流程和多种 Provider 集成，因此你可以使用已付费的模型，并在需要时回退到直接 API Provider。

### 内置登录流程

- **Claude**（`jcode login --provider claude`）
- **OpenAI / ChatGPT / Codex**（`jcode login --provider openai`）
- **Google Gemini**（`jcode login --provider gemini`）
- **GitHub Copilot**（`jcode login --provider copilot`）
- **Azure OpenAI**（`jcode login --provider azure`）
- **阿里云编码计划**（`jcode login --provider alibaba-coding-plan`）
- **Fireworks**（`jcode login --provider fireworks`）
- **MiniMax**（`jcode login --provider minimax`）
- **LM Studio**（`jcode login --provider lmstudio`）
- **Ollama**（`jcode login --provider ollama`）
- **自定义 OpenAI 兼容端点**（`jcode login --provider openai-compatible`）

对于自定义 OpenAI 兼容端点，jcode 现在会提示输入 API 地址，并支持无需 API 密钥的本地 localhost 服务器。

### 自托管端点和 MCP 的配置文件设置

如果你更倾向于通过编辑文件而非使用登录 UI 进行配置，jcode 支持自定义 OpenAI 兼容端点配置和 MCP 配置文件。

#### OpenAI 兼容 Provider

许多托管服务都支持标准的 OpenAI `/v1/chat/completions` API。jcode 通过统一的 OpenAI 兼容 Provider 与它们通信，因此你几乎可以使用任何此类端点，而无需等待专用集成。

有两种设置方式：

- **内置命名配置文件**：jcode 为多个流行的 OpenAI 兼容服务预置了配置文件。通过 ID 登录，jcode 会自动填充 base URL 和密钥环境变量：
  ```bash
  jcode login --provider <id>
  # 例如：
  jcode login --provider openrouter
  jcode login --provider deepseek
  jcode login --provider opencode   # OpenCode Zen
  jcode login --provider moonshotai
  ```
  内置 OpenAI 兼容配置文件 ID 包括：`openrouter`、`deepseek`、`zai`、`kimi`、`moonshotai`、`opencode`（OpenCode Zen）、`opencode-go`、`302ai`、`baseten`、`cortecs`、`huggingface`、`nebius`、`scaleway`、`stackit` 和 `firmware`。每个配置文件仅设置端点和密钥变量；你仍需通过 `/model`（或 `--model`）选择模型。运行不带参数的 `jcode login` 可查看交互式列表。

- **任意其他端点**：使用 `jcode login --provider openai-compatible` 或下面描述的可脚本化 `jcode provider add` 命令，将 jcode 指向任意 OpenAI 兼容 API（托管或本地）。

这些端点有用的环境变量覆盖：
- `JCODE_STREAM_IDLE_TIMEOUT_SECS` — 提高流式空闲超时（默认 180 秒），适用于推理慢的模型（静默思考后才输出 token）。也可在 `config.toml` 中设置为 `[provider] stream_idle_timeout_secs`。
- 每模型 `context_window`（别名 `context_limit`）— 在 `[[providers..models]]` 条目中设置，当端点无可用 `/v1/models` 响应时指定上下文窗口，避免 jcode 回退到通用的 200k 默认值。
- `extra_body` — 向每个 chat/completions 请求体中注入非标准顶级字段，适用于需要这些字段的后端。参见下文 [额外请求体字段（extra_body）](#extra-request-body-fields-extra_body)。

#### 自托管 OpenAI 兼容端点（含 vLLM）

对于 Agent 和脚本，推荐使用一次性 provider profile 命令。它会将命名配置文件写入 `~/.jcode/config.toml`，按需将密钥存储在 jcode 的私有应用配置目录中，并打印精确的运行/验证命令：

```bash
# 带密钥的托管 OpenAI 兼容 API
printf '%s' "$MY_API_KEY" | jcode provider add my-api \
  --base-url https://llm.example.com/v1 \
  --model my-model-id \
  --api-key-stdin \
  --set-default \
  --json

# 冒烟测试该配置文件
jcode --provider-profile my-api auth-test --prompt 'Reply exactly JCODE_PROVIDER_SETUP_OK'

# 直接使用
jcode --provider-profile my-api run 'hello'
```

对于无需认证的本地服务器：
```bash
jcode provider add local-vllm \
  --base-url http://localhost:8000/v1 \
  --model Qwen/Qwen3-Coder-30B-A3B-Instruct \
  --no-api-key \
  --set-default
```

常用的桌面/本地运行环境有内置的本地配置文件：
```bash
# Ollama：先启动本地服务器并安装模型
ollama pull llama3.2
jcode login --provider ollama
jcode --provider ollama --model llama3.2 run 'hello'

# LM Studio：启动 Local Server，加载聊天模型，然后使用 LM Studio 显示的
# 或通过 curl http://localhost:1234/v1/models 获取的确切模型标识符
jcode login --provider lmstudio
jcode --provider lmstudio --model '<模型标识符>' run 'hello'
```

Ollama 和 LM Studio 都暴露了 OpenAI 兼容的 `/v1/models` 和 `/v1/chat/completions` 端点。jcode 使用流式聊天补全、函数/工具调用，以及针对支持视觉的本地模型的 OpenAI 风格图像内容。

如果本地服务器需要 token，可在 `jcode login` 时输入，或使用 `--api-key-stdin` 创建命名配置文件。

有用的标志：
- `--api-key-env NAME`：引用现有环境变量而非存储密钥。
- `--api-key-stdin`：从标准输入读取并存储密钥，避免密钥出现在 shell 历史中。
- `--context-window TOKENS`：为模型选择和路由持久化上下文窗口。
- `--overwrite`：替换同名的现有配置文件。
- `--model-catalog`：除已配置的模型外，还使用端点的 `/models` 响应。

生成的配置文件也可以手动编辑 `~/.jcode/config.toml`：
```toml
[provider]
default_provider = "my-api"
default_model = "my-model-id"

[providers.my-api]
type = "openai-compatible"
base_url = "https://llm.example.com/v1"
api_key_env = "JCODE_PROVIDER_MY_API_API_KEY"
env_file = "provider-my-api.env"
default_model = "my-model-id"

[[providers.my-api.models]]
id = "my-model-id"
context_window = 128000
```

##### 额外请求体字段（`extra_body`）

某些 OpenAI 兼容后端需要非标准的顶级请求字段。例如，NVIDIA NIM DeepSeek-V4 推理模型（`deepseek-ai/deepseek-v4-flash`、`deepseek-ai/deepseek-v4-pro`）仅在请求包含 `chat_template_kwargs` 时才启用思考；否则它们会在无推理的情况下回复（或在某些部署中挂起）。

jcode 允许你通过两种方式注入任意顶级字段：

1. 通过 `config.toml` 中的 `extra_body`（按命名配置文件，TOML 表会逐字合并到 JSON 体中）：
   ```toml
   [providers.my-nim]
   type = "openai-compatible"
   base_url = "https://integrate.api.nvidia.com/v1"
   api_key_env = "NVIDIA_API_KEY"
   default_model = "deepseek-ai/deepseek-v4-flash"

   [providers.my-nim.extra_body.chat_template_kwargs]
   thinking = true
   reasoning_effort = "high"
   ```

2. 对于内置配置文件（如 `nvidia-nim`）或任何端点，通过 `JCODE_OPENAI_EXTRA_BODY` 环境变量（JSON 对象字符串）。它可以放在 Provider 的 env 文件（`~/.config/jcode/nvidia-nim.env`）中，与 API 密钥一起：
   ```bash
   JCODE_OPENAI_EXTRA_BODY={"chat_template_kwargs":{"thinking":true,"reasoning_effort":"high"}}
   ```

来自 `extra_body` 的键会最后合并，并覆盖 jcode 生成的同名字段（键冲突时 `JCODE_OPENAI_EXTRA_BODY` 优先于配置的 `extra_body`）。无效值会被记录并忽略，而不会导致请求失败。

自定义 OpenAI 兼容 Provider 会从环境变量或 jcode 应用配置目录中的 env 文件读取覆盖值。在 Linux 上通常是 `~/.config/jcode/`，因此默认文件通常为：
```text
~/.config/jcode/openai-compatible.env
```

本地或局域网 vLLM 服务器示例：
```bash
JCODE_OPENAI_COMPAT_API_BASE=http://192.168.1.50:8000/v1
JCODE_OPENAI_COMPAT_DEFAULT_MODEL=Qwen/Qwen3-Coder-30B-A3B-Instruct
# 如果服务器需要认证（可选）
OPENAI_COMPAT_API_KEY=your-token-here
```

注意：
- `jcode login --provider openai-compatible` 可以为你创建或更新此文件。
- 纯 `http://` 仅接受 `localhost` 和私有 LAN IP。公共远程 HTTP 仍被拒绝。
- HTTPS 端点照常工作。

#### MCP 配置文件

MCP 配置独立于 `config.toml`。主配置文件：
- `~/.jcode/mcp.json` — 全局 MCP 服务器
- `.jcode/mcp.json` — 项目本地 MCP 服务器

Claude Code 兼容性：
- `~/.claude.json`（Claude Code 的用户配置）：顶级 `mcpServers`，以及当前目录下 `projects.<path>.mcpServers` 中的项目级服务器
- 仓库根目录下的 `.mcp.json`（Claude Code 的项目配置）
- `.claude/mcp.json`（遗留回退）

规范的 `mcpServers` 键和 jcode 历史遗留的 `servers` 键均被接受。jcode 目前仅支持 stdio（基于命令）服务器；HTTP/SSE 条目（`"type": "http"`/`"sse"`）会被识别并跳过（记录一行日志）。

MCP 配置示例：
```json
{
  "mcpServers": {
    "filesystem": {
      "command": "/path/to/mcp-server",
      "args": ["--root", "/workspace"],
      "env": {},
      "shared": true
    }
  }
}
```

首次运行时，如果 `~/.jcode/mcp.json` 尚不存在，jcode 还会尝试从 `~/.claude.json`（回退到遗留的 `~/.claude/mcp.json`）和 `~/.codex/config.toml` 导入 MCP 服务器。

对于无头（headless）或 SSH 会话，OAuth 风格的 Provider 支持 `jcode login --provider <provider> --no-browser`（别名 `--headless`），jcode 会打印认证 URL/QR 并回退到手动输入代码或回调粘贴，而不是尝试启动本地浏览器。

对于更可脚本化的远程流程，`claude`、`openai`、`gemini` 和 `antigravity` 也支持两步模式：
```bash
# 步骤 1：打印可恢复的认证 URL
jcode login --provider openai --print-auth-url --json

# 步骤 2：稍后使用回调 URL 或认证码完成
jcode login --provider openai --callback-url 'http://localhost:1455/auth/callback?...'
jcode login --provider gemini --auth-code '...'
```

其他可脚本化场景：
```bash
# Copilot 设备流：打印 URL + 用户码，稍后完成
jcode login --provider copilot --print-auth-url --json
jcode login --provider copilot --complete

# Gmail/Google OAuth（凭证已配置后）
jcode login --provider google --print-auth-url --google-access-tier readonly
jcode login --provider google --callback-url 'http://127.0.0.1:8456?...'
```

待完成的脚本化登录状态存储在 `~/.jcode/pending-login/` 下，会自动过期，并在新的脚本化登录启动或恢复时清理过期条目。

对于内置的 OpenAI 登录流程，jcode 默认在 `http://localhost:1455/auth/callback` 打开本地回调。

### 支持的 Provider

- **原生/第一方风格 Provider：** `claude`、`openai`、`copilot`、`gemini`、`azure`、`alibaba-coding-plan`
- **聚合/兼容性 Provider：** `openrouter`、`openai-compatible`
- **其他 Provider 集成：** `opencode`、`opencode-go`、`zai` / `kimi`、`302ai`、`baseten`、`cortecs`、`deepseek`、`firmware`、`huggingface`、`moonshotai`、`nebius`、`scaleway`、`stackit`、`groq`、`mistral`、`perplexity`、`togetherai`、`deepinfra`、`fireworks`、`minimax`、`xai`、`lmstudio`、`ollama`、`chutes`、`cerebras`、`cursor`、`antigravity`、`google`

jcode 还支持轻松的多账户切换。第一个 ChatGPT Pro 订阅的 token 用完了？用 `/account` 快速切换到第二个账户。

## 可定制性 / 自我开发（Self-Dev）

jcode 正在开创一种新的可定制形式——不局限于插件或扩展的能力。告诉你的 jcode Agent 进入自我开发模式，它就会开始修改自己的源代码。jcode 针对自我迭代进行了优化。围绕自我开发有大量基础设施，使其能够编辑、构建、测试自己的源代码，然后重新加载自己的二进制文件，在你的（可能很多个）会话中全自动继续工作。

建议使用前沿模型进行此操作。jcode 代码库并非简单，较弱的模型可能会做出微妙的、破坏性的更改。GPT 5.5 或最新的可用前沿模型效果不错。

## 其他细节

细节决定成败。jcode 有许多未文档化的优化和贴心设计。例如：
- Anthropic 的 Claude 缓存会在 5 分钟后失效。如果你在这 5 分钟后发起 Claude 请求，就会发生缓存未命中，可能耗费大量 token。UI 会在缓存变冷时发出警告，并在出现意外缓存未命中时通知你。
- jcode 附带了如何设置 Firefox Agent Bridge 的说明。让你的 Agent 进行设置，之后 jcode 也将拥有浏览器自动化功能。
- Agent Grep 是作者为 jcode Agent 打造的 grep 工具。它在 grep 返回结果中增加了文件结构信息（如函数列表及其偏移量等），使 Agent 无需实际读取文件即可推断更多内容。它还实现了框架级别的集成，能根据 Agent 已看到的内容自适应截断返回结果，大大节省了上下文。
- 输入默认与工作中的 Agent 交错进行。它会尽可能早地安全发送输入，而不会破坏 KV 缓存。使用 `Shift+Enter` 提交则会进入队列模式，等待 Agent 完全完成当前轮次后再发送。
- 支持从不同的框架恢复会话。Claude Code 崩溃了？从 jcode 恢复会话，从断点继续。支持从 codex、claude code、opencode 和 pi 恢复会话。
- 技能（Skills）不会在启动时全部加载。对话会被嵌入为语义向量，当有与记忆相似的嵌入命中时，会自动注入技能。Agent 也有一个技能工具，供你随时手动激活技能。你也可以通过斜杠命令激活。

## iOS 应用 / 原生 OpenClaw

jcode 的原生 iOS 应用版本即将推出。这将允许你通过 Tailscale 从手机远程操作个人机器上的 jcode 环境。类似 OpenClaw 的功能将捆绑在此 iOS 应用中。

## 其他计划中的功能

- Agent 不喜欢在 Git 状态脏（有未提交更改）时提交。Git 显然不是为多 Agent 工作流设计的，git worktrees 也不是好的解决方案。鉴于此，作者认为这是一个诞生新的 Git 类似原语的机会。
- 构建速度改进：在作者机器上，启用缓存的增量调试 cargo 构建大约需要 1 分钟。目标是 5-20 秒。通过重构和 crate seams 应该能够实现。

## 快速开始

```bash
# 启动 TUI
jcode

# 非交互式运行单条命令
jcode run "say hello"

# 按记忆名称恢复之前的会话
jcode --resume fox

# 作为持久后台服务器运行，然后连接更多客户端
jcode serve
jcode connect

# 从配置的 STT 命令发送语音输入
jcode dictate
```

jcode 支持交互式 TUI 使用、非交互式运行、持久服务器/客户端工作流，以及快捷键友好的语音输入（无需捆绑语音转文本栈）。

## 浏览器自动化

jcode 内置了一流的 `browser` 工具，用于在 Agent 会话中控制浏览器。

**当前内置后端：**
- Firefox（通过 Firefox Agent Bridge）

**当前内置工具操作包括：**
- `status`、`setup`、`open`、`snapshot`、`get_content`、`interactables`、`click`、`type`、`fill_form`、`select`、`wait`、`screenshot`、`eval`、`scroll`、`upload`、`press`

快速设置：
```bash
jcode browser status
jcode browser setup
```

设置完成后，模型可以直接使用内置的 `browser` 工具。UI 也会紧凑地总结浏览器工具调用，例如打开 URL、点击选择器或在字段中输入内容（不会回显敏感输入文本）。

注意：
- Provider/工具架构已为其他后端做好准备
- Firefox 是当前内置的后端
- Chrome bridge / 远程调试风格的 Provider 可以在同一浏览器工具之上后续添加

## 延伸阅读

- [环境模式 / OpenClaw](docs/AMBIENT_MODE.md)
- [浏览器 Provider 协议](docs/BROWSER_PROVIDER_PROTOCOL.md)
- [记忆架构](docs/MEMORY_ARCHITECTURE.md)
- [Swarm 架构](docs/SWARM_ARCHITECTURE.md)
- [服务器架构](docs/SERVER_ARCHITECTURE.md)
- [安全系统](docs/SAFETY_SYSTEM.md)
- [Windows 注意事项](docs/WINDOWS.md)
- [包装器与 Shell 集成](docs/WRAPPERS.md)
- [重构笔记](docs/REFACTORING.md)

## 详细安装

### 设置

如果你想让另一个 Agent 为你安装 jcode，给它以下提示：
```text
Set up jcode on this machine for me.
1. Detect the operating system, available package managers, and shell environment, then install jcode using the best matching command below instead of referring me somewhere else:
- macOS with Homebrew available: brew tap 1jehuang/jcode && brew install jcode
- macOS or Linux via install script: curl -fsSL https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/install.sh | bash
- Windows PowerShell: irm https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/install.ps1 | iex
- From source if the ...
```