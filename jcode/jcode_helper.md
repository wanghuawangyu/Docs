- [Jcode 使用指南](#jcode-使用指南)
  - [概述](#概述)
  - [安装](#安装)
    - [快速安装](#快速安装)
    - [macOS 通过 Homebrew](#macos-通过-homebrew)
    - [源码编译](#源码编译)
    - [Termux (Android)](#termux-android)
    - [卸载](#卸载)
    - [平台支持](#平台支持)
  - [架构](#架构)
  - [快速开始](#快速开始)
  - [命令行命令](#命令行命令)
    - [全局选项](#全局选项)
    - [子命令](#子命令)
  - [JSON 输出与脚本集成](#json-输出与脚本集成)
  - [提供商与模型配置](#提供商与模型配置)
    - [支持的登录方式](#支持的登录方式)
    - [OpenAI 兼容提供商配置](#openai-兼容提供商配置)
    - [自定义 API 端点](#自定义-api-端点)
    - [本地运行环境](#本地运行环境)
    - [配置示例 (`~/.jcode/config.toml`)](#配置示例-jcodeconfigtoml)
      - [1. TOML 主配置 — DeepSeek 与本地配置实例](#1-toml-主配置--deepseek-与本地配置实例)
      - [2. JSON 环境变量（JSON Env）](#2-json-环境变量json-env)
      - [3. ENV 文件凭据](#3-env-文件凭据)
      - [4. 环境变量运行时覆盖](#4-环境变量运行时覆盖)
  - [配置文件格式](#配置文件格式)
    - [支持的格式总览](#支持的格式总览)
    - [主配置（TOML）](#主配置toml)
      - [`[display]` — 显示与界面](#display--显示与界面)
      - [`[display.native_scrollbars]` — 原生滚动条](#displaynative_scrollbars--原生滚动条)
      - [`[keybindings]` — 快捷键绑定](#keybindings--快捷键绑定)
      - [`[dictation]` — 语音听写](#dictation--语音听写)
      - [`[features]` — 功能开关](#features--功能开关)
      - [`[provider]` — 提供商全局设置](#provider--提供商全局设置)
      - [`[agents]` — Agent 设置](#agents--agent-设置)
      - [`[websearch]` — 网络搜索](#websearch--网络搜索)
      - [`[tools]` — 工具配置](#tools--工具配置)
      - [`[ambient]` — 后台环境模式](#ambient--后台环境模式)
      - [`[safety]` — 安全系统通知](#safety--安全系统通知)
      - [`[notifications]` — 通知设置](#notifications--通知设置)
      - [`[compaction]` — 上下文压缩](#compaction--上下文压缩)
      - [`[hooks]` — 钩子](#hooks--钩子)
      - [`[power]` — 电源管理](#power--电源管理)
      - [`[gateway]` — HTTP 网关](#gateway--http-网关)
      - [`[sponsors]` — 赞助商](#sponsors--赞助商)
      - [`[launch_hotkeys]` — 启动热键](#launch_hotkeys--启动热键)
      - [`[acp]` — ACP（Agent Communication Protocol）](#acp--acpagent-communication-protocol)
      - [`[auth]` — 认证](#auth--认证)
      - [`[autoreview]` / `[autojudge]` — 自动审查/评判](#autoreview--autojudge--自动审查评判)
    - [MCP 配置（JSON）](#mcp-配置json)
    - [凭据存储（ENV 文件）](#凭据存储env-文件)
    - [其他配置文件（JSON）](#其他配置文件json)
    - [运行时环境变量覆盖](#运行时环境变量覆盖)
  - [数据目录结构](#数据目录结构)
  - [内部命令（TUI 中可使用）](#内部命令tui-中可使用)
  - [记忆系统](#记忆系统)
    - [工作原理](#工作原理)
    - [记忆工具](#记忆工具)
    - [记忆 CLI 命令](#记忆-cli-命令)
    - [记忆存存储位置](#记忆存存储位置)
    - [环境依赖与模型下载](#环境依赖与模型下载)
  - [Swarm 群体协作](#swarm-群体协作)
    - [核心特性](#核心特性)
    - [工作流](#工作流)
    - [Swarm 提示配置](#swarm-提示配置)
  - [Ambient 后台环境模式](#ambient-后台环境模式)
    - [功能](#功能)
    - [工作原理](#工作原理-1)
    - [配置](#配置)
  - [安全系统](#安全系统)
    - [权限分级](#权限分级)
    - [安全系统 CLI](#安全系统-cli)
  - [浏览器自动化](#浏览器自动化)
    - [快速设置](#快速设置)
    - [支持的浏览器操作](#支持的浏览器操作)
  - [自开发（Self-Dev）](#自开发self-dev)
  - [性能对比](#性能对比)
  - [快捷键](#快捷键)
  - [会话管理](#会话管理)
    - [创建/恢复会话](#创建恢复会话)
    - [跨工具会话恢复](#跨工具会话恢复)
  - [日志与调试](#日志与调试)
  - [常见问题（FAQ）](#常见问题faq)
    - [如何切换模型？](#如何切换模型)
    - [如何切换账号？](#如何切换账号)
    - [如何让 Agent 帮我安装 Jcode？](#如何让-agent-帮我安装-jcode)
    - [断线后如何恢复？](#断线后如何恢复)
    - [如何退出 Ambient 模式？](#如何退出-ambient-模式)
    - [如何查看 Ambient 活动？](#如何查看-ambient-活动)
  - [更多资料](#更多资料)

# Jcode 使用指南

## 概述

**Jcode** 是一款面向开发者的下一代编码助手工具（coding agent harness），专注于提升多会话工作流、无限可定制性和极致性能。Jcode 基于 Rust 编写，提供 TUI（终端界面）、多模型支持、群体协作（Swarm）、浏览器自动化、记忆系统等功能。

- **项目主页**: [https://github.com/1jehuang/jcode](https://github.com/1jehuang/jcode)
- **官网**: [https://solosystems.dev/jcode](https://solosystems.dev/jcode)
- **许可证**: MIT

---

## 安装

### 快速安装

```bash
# macOS & Linux
curl -fsSL https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/install.sh | bash

# Windows (PowerShell)
irm https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/install.ps1 | iex
```

### macOS 通过 Homebrew

```bash
brew tap 1jehuang/jcode
brew install jcode
```

### 源码编译

```bash
git clone https://github.com/1jehuang/jcode.git
cd jcode
cargo build --release
scripts/install_release.sh
```

### Termux (Android)

```bash
pkg install glibc patchelf
curl -fsSL https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/install.sh | bash
```

### 卸载

```bash
# 保留配置和会话数据
curl -fsSL https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/uninstall.sh | bash -s -- --yes

# 完全清除（包括配置、认证、会话、日志、记忆等）
curl -fsSL https://raw.githubusercontent.com/1jehuang/jcode/master/scripts/uninstall.sh | bash -s -- --purge --yes
```

### 平台支持

| 平台 | 状态 |
|------|------|
| **Linux** x86_64 / aarch64 | 完全支持 |
| **macOS** Apple Silicon & Intel | 支持 |
| **Windows** x86_64 | 支持（原生 + WSL2） |
| **Termux** aarch64 / x86_64 | 支持（需安装 glibc + patchelf） |

---

## 架构

Jcode 采用 **单服务器（Server）、多客户端（Client）** 架构：

```
┌─────────────────────────────────────────────────────────────┐
│                     SERVER (后台守护进程)                      │
│                                                             │
│  jcode serve                                                 │
│  ├── Unix Socket:  /run/user/$UID/jcode.sock                 │
│  ├── Debug Socket: /run/user/$UID/jcode-debug.sock           │
│  ├── Registry:     ~/.jcode/servers.json                     │
│  ├── Provider (Claude/OpenAI/OpenRouter 等)                   │
│  ├── MCP 池（所有会话共享）                                     │
│  └── 会话:                                                     │
│        ├── 🦊 fox   (活跃)                                    │
│        ├── 🐻 bear  (活跃)                                    │
│        └── 🦉 owl   (空闲)                                    │
└─────────────────────────────────────────────────────────────┘
         │              │              │
         ▼              ▼              ▼
    ┌─────────┐   ┌─────────┐   ┌─────────┐
    │ Client 1│   │ Client 2│   │ Client 3│
    │ 🦊 fox  │   │ 🐻 bear │   │ 🦉 owl  │
    └─────────┘   └─────────┘   └─────────┘
```

**核心行为：**
- 第一次运行 `jcode` 自动启动后台守护进程
- 后续运行直接连接已有服务器
- 客户端断开不影响服务器或其他客户端
- `/reload` 热重载到新二进制，客户端自动重连
- 所有客户端关闭后，服务器 5 分钟空闲超时自动退出

---

## 快速开始

```bash
# 启动 TUI 界面
jcode

# 非交互模式：运行单条指令
jcode run "say hello"

# 按记忆名称恢复会话
jcode --resume fox

# 作为持久后台服务器运行，然后连接更多客户端
jcode serve
jcode connect

# 语音输入
jcode dictate
```

---

## 命令行命令

### 全局选项

| 选项 | 说明 |
|------|------|
| `-p, --provider <PROVIDER>` | 指定 AI 提供商（默认 auto 自动检测） |
| `-m, --model <MODEL>` | 指定模型（如 claude-opus-4-6、gpt-5.5） |
| `-C, --cwd <PATH>` | 指定工作目录 |
| `--no-update` | 跳过自动更新检查 |
| `--auto-update` | 自动更新（默认开启） |
| `--trace` | 记录工具输入/输出到 stderr |
| `--quiet` | 抑制非错误输出（用于脚本） |
| `--resume [SESSION]` | 恢复会话（不传参数列出所有会话） |
| `--no-selfdev` | 禁用仓库自检和自开发模式 |
| `--socket <PATH>` | 自定义 socket 路径 |
| `--debug-socket` | 启用调试 socket |
| `--provider-profile <NAME>` | 指定配置文件中定义的 provider 配置 |
| `--tool-profile <PROFILE>` | 指定工具配置（full、lite、none） |
| `--tools <LIST>` | 工具白名单（逗号分隔） |
| `--disabled-tools <LIST>` | 工具黑名单（逗号分隔） |
| `--disable-base-tools` | 禁用所有内置工具 |

### 子命令

| 子命令 | 说明 |
|--------|------|
| `serve` | 启动后台守护进程服务器 |
| `connect` | 连接已在运行的服务器 |
| `run <MESSAGE>` | 单条消息模式，执行后退出 |
| `login [PROVIDER]` | 登录提供商 (OAuth / API Key) |
| `repl` | 简单 REPL 模式（无 TUI） |
| `update` | 更新 jcode 到最新版本 |
| `version` | 显示版本信息 |
| `usage` | 显示已连接提供商的用量限制 |
| `self-dev` | 自开发模式 |
| `debug` | 调试 socket CLI |
| `auth` | 认证状态和验证（子命令：status、doctor） |
| `provider` | 提供商管理（子命令：list、current、add） |
| `memory` | 记忆管理（子命令：list、search、export、import、stats） |
| `session` | 会话管理（子命令：rename） |
| `ambient` | 后台环境模式管理（子命令：status、log、trigger、stop） |
| `cloud sessions` | 云会话管理（子命令：configure、status、upload、list、verify、dashboard、view） |
| `pair` | 生成配对码（iOS/Web 客户端） |
| `permissions` | 审查待处理的权限请求 |
| `transcript` | 注入外部转录文本到活跃 Jcode TUI |
| `dictate` | 运行语音听写 |
| `setup-hotkey` | 设置全局热键 |
| `setup-launcher` | 安装启动器 |
| `browser` | 浏览器自动化设置和状态 |
| `replay` | 在 TUI 中回放保存的会话 |
| `model` | 模型管理（子命令：list） |
| `provider-test-coverage` | 显示实时验证覆盖 |
| `provider-doctor` | 诊断提供商问题 |
| `auth-test` | 端到端测试认证流程 |
| `restart` | 保存/恢复重启状态 |
| `menubar` | 显示 macOS 菜单栏指示器 |

---

## JSON 输出与脚本集成

Jcode 支持脚本友好型的 JSON/NDJSON 输出：

```bash
# 列出模型（JSON）
jcode --quiet model list --json

# 列出提供商
jcode --quiet provider list --json

# 运行单条指令并返回 JSON
jcode --quiet run --json "Reply with exactly OK"

# 流式输出（NDJSON）
jcode --quiet run --ndjson "Hello"

# 认证状态
jcode --quiet auth status --json

# 版本信息
jcode --quiet version --json

# 当前提供商/模型选择
jcode --quiet provider current --json
```

推荐脚本中使用的全局选项：`--quiet --no-update --no-selfdev`

---

## 提供商与模型配置

### 支持的登录方式

Jcode 支持多种 AI 提供商的 OAuth 登录：

| 提供商 | 登录命令 |
|--------|----------|
| Claude | `jcode login --provider claude` |
| OpenAI / ChatGPT / Codex | `jcode login --provider openai` |
| Google Gemini | `jcode login --provider gemini` |
| GitHub Copilot | `jcode login --provider copilot` |
| Azure OpenAI | `jcode login --provider azure` |
| 阿里云编码计划 | `jcode login --provider alibaba-coding-plan` |
| Fireworks | `jcode login --provider fireworks` |
| MiniMax | `jcode login --provider minimax` |
| LM Studio | `jcode login --provider lmstudio` |
| Ollama | `jcode login --provider ollama` |
| 自定义 OpenAI 兼容端点 | `jcode login --provider openai-compatible` |

### OpenAI 兼容提供商配置

通过内置配置文件快速设置：

```bash
jcode login --provider openrouter
jcode login --provider deepseek
jcode login --provider moonshotai
```

**内置 OpenAI 兼容配置文件 ID：** openrouter、deepseek、zai、kimi、moonshotai、opencode、302ai、baseten、cortecs、huggingface、nebius、scaleway、stackit、firmware、groq、mistral、perplexity、togetherai、deepinfra、xai、nvidia-nim、chutes、cerebras、cursor、antigravity、google

### 自定义 API 端点

```bash
# 安全配置 API Key
printf '%s' "$MY_API_KEY" | jcode provider add my-api \
  --base-url https://llm.example.com/v1 \
  --model my-model-id \
  --api-key-stdin \
  --set-default

# 本地服务器（无需认证）
jcode provider add local-vllm \
  --base-url http://localhost:8000/v1 \
  --model Qwen/Qwen3-Coder-30B-A3B-Instruct \
  --no-api-key \
  --set-default
```

### 本地运行环境

```bash
# Ollama
ollama pull llama3.2
jcode login --provider ollama
jcode --provider ollama --model llama3.2 run 'hello'

# LM Studio：先在 LM Studio 中启动 Local Server，加载模型
jcode login --provider lmstudio
jcode --provider lmstudio --model '<model-id>' run 'hello'
```

### 配置示例 (`~/.jcode/config.toml`)

以下展示三种配置方式的具体实例。

#### 1. TOML 主配置 — DeepSeek 与本地配置实例

`~/.jcode/config.toml` 是核心配置文件，涵盖提供商、模型、Ambient 模式等设置。以下展示 **DeepSeek** 和 **本地（Local）** 两类提供商的典型配置：

```toml
[provider]
default_provider = "deepseek"
default_model = "deepseek-v4-flash"

# --- DeepSeek 提供商配置 ---
[providers.deepseek]
type = "openai-compatible"
base_url = "https://api.deepseek.com/v1"
api_key_env = "DEEPSEEK_API_KEY"
env_file = "provider-deepseek.env"
default_model = "deepseek-v4-flash"

[[providers.deepseek.models]]
id = "deepseek-v4-flash"
context_window = 128000

[[providers.deepseek.models]]
id = "deepseek-v4-pro"
context_window = 128000

# --- 本地模型（vLLM/Ollama/LM Studio） ---
[providers.local]
type = "openai-compatible"
base_url = "http://192.168.2.215:8080/v1"
no_api_key = true
default_model = "Qwen/Qwen3-Coder-30B-A3B-Instruct"

[[providers.local.models]]
id = "Qwen/Qwen3-Coder-30B-A3B-Instruct"
context_window = 32000

# --- Ambient 模式 ---
[ambient]
enabled = false
min_interval_minutes = 5
max_interval_minutes = 120
```

#### 2. JSON 环境变量（JSON Env）

通过环境变量注入 JSON 格式的结构化数据，覆盖运行时行为，无需修改配置文件：

```bash
# 为 OpenAI 兼容 API 注入额外请求体字段（JSON 字符串）
export JCODE_OPENAI_EXTRA_BODY='{"temperature":0.7,"max_tokens":4096,"stop":["<|im_end|>"]}'

# 搭配启动
jcode --provider openai-compatible
```

除自定义请求体外，JSON 格式的 MCP 配置文件也属于此类用法：

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

```bash
# 通过环境变量指定 MCP 配置文件路径（覆盖默认 ~/.jcode/mcp.json）
export JCODE_MCP_CONFIG="/path/to/custom-mcp.json"
```

#### 3. ENV 文件凭据

敏感 API Key 存储在独立的 ENV 文件中，避免写入主配置或暴露在命令行历史中：

```
# ~/.config/jcode/provider-my-api.env
JCODE_PROVIDER_MY_API_API_KEY=sk-your-api-key-here
```

```bash
# 亦可使用自定义路径，通过环境变量指向
export JCODE_ENV_FILE="/secure/path/provider.env"
jcode
```

#### 4. 环境变量运行时覆盖

无需修改配置文件，通过环境变量即可覆盖多项运行时行为：

```bash
# 覆盖 OpenAI 兼容 API 地址和默认模型
export JCODE_OPENAI_COMPAT_API_BASE="https://custom-endpoint.example.com/v1"
export JCODE_OPENAI_COMPAT_DEFAULT_MODEL="gpt-4o"

# 修改流式传输空闲超时（默认 180 秒）
export JCODE_STREAM_IDLE_TIMEOUT_SECS=300

# 切换 Bing 搜索区域市场
export JCODE_BING_MARKET="zh-CN"

# 设置服务器显示名称（服务管理器使用）
export JCODE_SERVER_DISPLAY_NAME="my-jcode-server"

# 启动后所有会话自动使用上述覆盖
jcode
```

---

## 配置文件格式

Jcode 支持多种配置文件格式，涵盖主配置、MCP 服务器、凭据存储和运行时覆盖。

### 支持的格式总览

| 格式 | 用途 |
|------|------|
| **TOML** | 主配置文件，最核心的配置格式 |
| **JSON** | MCP 配置、服务器注册、外部工具兼容配置 |
| **ENV 文件** | 敏感凭据存储，独立于主配置 |
| **环境变量** | 运行时覆盖配置值 |

### 主配置（TOML）

`~/.jcode/config.toml` 是 Jcode 最主要的配置文件，涵盖提供商、模型、显示、快捷键、Agent、Ambient 模式、安全系统等全部配置。

项目级覆盖配置位于 `.jcode/config.toml`。

以下是各配置节的详细说明（以用户实际配置为例）：

#### `[display]` — 显示与界面

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `diff_mode` | 差异显示方式（见下方可选值） | `"inline"` | `"inline"` |
| `queue_mode` | 队列模式 | `false` | `false` |
| `auto_server_reload` | 自动热重载服务器 | `true` | `true` |
| `mouse_capture` | 捕获鼠标事件。</br>`true`：jcode 拦截鼠标用于 TUI 内部操作（点击切换焦点、滚轮滚动、点击复制徽章等），终端原生的选中即复制/右键粘贴被屏蔽；</br>`false`：鼠标事件穿透到终端，终端原生选中复制、右键粘贴可用，但 TUI 内部鼠标交互失效 | `false` | `true` |
| `debug_socket` | 启用调试 socket | `false` | `false` |
| `centered` | 居中显示 | `false` | `false` |
| `show_thinking` | 显示模型思考过程 | `true` | `true` |
| `reasoning_display` | 推理过程显示方式 | `"current"` | `"current"` |
| `diagram_mode` | 图表模式（none/mermaid） | `"none"` | `"none"` |
| `markdown_spacing` | Markdown 间距 | `"compact"` | `"compact"` |
| `pin_images` | 固定图片显示 | `true` | `true` |
| `idle_animation` | 空闲动画 | `true` | `true` |
| `prompt_entry_animation` | 输入动画 | `true` | `true` |
| `disabled_animations` | 禁用的动画列表 | `[]` | `[]` |
| `diff_line_wrap` | 差异视图自动换行 | `true` | `true` |
| `animation_fps` | 动画帧率 | `60` | `60` |
| `redraw_fps` | 重绘帧率 | `60` | `60` |
| `prompt_preview` | 输入预览 | `true` | `true` |
| `compact_notifications` | 紧凑通知 | `false` | `false` |
| `show_agentgrep_output` | 显示搜索工具输出 | `false` | `false` |
| `keybinding_hints` | 快捷键提示 | `true` | `true` |
| `theme` | 主题（留空为默认） | `""` | `""` |
| `active_sessions_manager` | 活跃会话管理器 | `false` | `false` |

**`diff_mode` 可选值：**

| 值 | 别名（环境变量中可用） | 效果 |
|-----|----------------------|------|
| `"off"` | `"none"`, `"0"`, `"false"` | 不显示差异，完全隐藏所有 diff |
| `"inline"` | `"on"`, `"1"`, `"true"` | **默认值。** 在聊天消息中内联显示差异，自动截断长预览 |
| `"full-inline"` | `"full_inline"`, `"full"`, `"inlinefull"` | 在聊天消息中内联显示完整差异，不截断预览 |
| `"pinned"` | `"pin"` | 在右侧固定的专用面板中显示差异预览，不影响聊天区布局 |
| `"file"` | — | 在侧面板中显示完整文件内容 + 差异高亮，与滚动位置联动 |

> 循环顺序（快捷键 `Alt+G` 切换）：`off → inline → full-inline → pinned → file → off`

#### `[display.native_scrollbars]` — 原生滚动条

| 键 | 说明 | 示例值 |
|-----|------|--------|
| `chat` | 聊天面板使用原生滚动条 | `true` |
| `side_panel` | 侧面板使用原生滚动条 | `true` |

#### `[keybindings]` — 快捷键绑定

快捷键在配置文件中以 `action = "key_combo"` 形式定义。常见操作如下：

| 操作 | 说明 | 示例绑定 |
|------|------|----------|
| `scroll_up` | 向上滚动 | `"ctrl+shift+k"` |
| `scroll_down` | 向下滚动 | `"ctrl+shift+j"` |
| `scroll_page_up` | 向上翻页 | `"alt+u"` |
| `scroll_page_down` | 向下翻页 | `"alt+d"` |
| `model_switch_next` | 下一个模型 | `"ctrl+tab"` |
| `model_switch_prev` | 上一个模型 | `"ctrl+shift+tab"` |
| `fallback_switch` | 回退切换 | `"ctrl+y"` |
| `effort_increase` | 增加推理努力度 | `"alt+right"` |
| `effort_decrease` | 减少推理努力度 | `"alt+left"` |
| `centered_toggle` | 切换居中显示 | `"alt+c"` |
| `scroll_prompt_up` | 提示区域向上滚动 | `"ctrl+k"` |
| `scroll_prompt_down` | 提示区域向下滚动 | `"ctrl+j"` |
| `scroll_bookmark` | 滚动到书签 | `"ctrl+g"` |
| `workspace_left/down/up/right` | 面板焦点移动 | `"alt+h/j/k/l"` |
| `side_panel_toggle` | 开关侧面板 | `"alt+m"` |
| `copy_selection_toggle` | 复制选中内容 | `"alt+y"` |
| `diagram_pane_toggle` | 开关图表面板 | `"alt+t"` |
| `typing_scroll_lock_toggle` | 输入滚动锁定 | `"alt+s"` |
| `diff_mode_cycle` | 循环切换差异模式 | `"alt+g"` |
| `info_widget_toggle` | 开关信息组件 | `"alt+i"` |
| `todo_card_toggle` | 开关待办卡片 | `"alt+x"` |
| `swarm_panel_focus` | 聚焦 Swarm 面板 | `"alt+n"` |
| `new_terminal` | 新建终端 | `"alt+shift+;"` |
| `open_resume` | 打开恢复列表 | `"alt+r"` |
| `session_picker_enter` | 会话选择器进入方式 | `"current-terminal"` |

#### `[dictation]` — 语音听写

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `command` | 语音识别命令 | `""` | `""` |
| `mode` | 发送模式（send/paste） | `"send"` | `"send"` |
| `key` | 快捷键（off 为禁用） | `"off"` | `"off"` |
| `timeout_secs` | 超时秒数 | `90` | `90` |

#### `[features]` — 功能开关

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `memory` | 启用记忆系统 | `true` | `true` |
| `swarm` | 启用群体协作 | `true` | `true` |
| `message_timestamps` | 显示消息时间戳 | `true` | `true` |
| `persist_memory_injections` | 持久化记忆注入 | `false` | `false` |
| `kv_cache_miss_notices` | 缓存未命中通知 | `true` | `true` |
| `update_channel` | 更新渠道（stable/canary） | `"stable"` | `"stable"` |

#### `[provider]` — 提供商全局设置

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `default_provider` | 默认提供商 | `"my-api"` | — |
| `default_model` | 默认模型 | `"my-model-id"` | — |
| `openai_reasoning_effort` | OpenAI 推理努力度 | `"low"` | `"medium"` |
| `openai_service_tier` | OpenAI 服务等级 | `"priority"` | — |
| `openai_native_compaction_mode` | 原生压缩模式 | `"auto"` | `"auto"` |
| `openai_native_compaction_threshold_tokens` | 原生压缩阈值 | `200000` | — |
| `preserve_reasoning_context` | 保留推理上下文 | `true` | `true` |
| `cross_provider_failover` | 跨提供商故障转移策略 | `"countdown"` | — |
| `same_provider_account_failover` | 同提供商账号故障转移 | `true` | `true` |
| `stream_idle_timeout_secs` | 流式空闲超时（秒） | `180` | `180` |
| `model_picker_providers` | 筛选 `/model` 命令显示的提供商列表（见下方说明） | — | — |

**`model_picker_providers` 说明：**

当本地存在多个提供商配置，但其中一些不可用时，可用此配置过滤 `/model` 命令中的显示列表。

```toml
[provider]
model_picker_providers = ["openai", "anthropic", "myprofile"]
```

| 条目格式 | 匹配对象 | 示例 |
|---------|---------|------|
| 提供商标签 | 登录后的提供商名称 | `"openai"`, `"anthropic"`, `"copilot"`, `"openrouter"` |
| 路由 API 方法 | OAuth 或兼容配置标识 | `"claude-oauth"`, `"openai-compatible:myprofile"` |
| OpenAI 兼容 profile ID | `provider add` 创建的自定义配置名 | `"myprofile"`, `"my-api"` |

> 未设置或为空数组时显示全部。当前会话正在使用的模型始终可见，不受此过滤影响。

#### `[agents]` — Agent 设置

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `swarm_spawn_mode` | Swarm 生成方式 | `"inline"` | `"inline"` |
| `swarm_strip_layout` | Swarm 面板布局 | `"vertical"` | `"vertical"` |
| `memory_sidecar_enabled` | 启用记忆侧车验证 | `true` | `true` |
| `memory_rerank_cadence` | 记忆重排序频率（轮次间隔） | `3` | `3` |
| `memory_rerank_votes` | 重排序投票数 | `2` | `2` |
| `memory_rerank_min_agree` | 重排序最少达成一致数 | `2` | `2` |
| `memory_embedding_backend` | 记忆嵌入后端 | `"local"` | `"local"` |
| `subagent_timeout_secs` | 子 Agent 超时秒数 | `600` | `600` |
| `swarm_max_concurrent_agents` | Swarm 最大并发 Agent 数 | `32` | `32` |

#### `[websearch]` — 网络搜索

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `engine` | 搜索引擎（见下方可选值） | `"duckduckgo"` | `"duckduckgo"` |
| `fallback_engines` | 主引擎失败时的备用引擎列表 | `["bing"]` | `[]` |
| `bing_api_key_env` | Bing API Key 的环境变量名 | `"JCODE_BING_API_KEY"` | — |
| `bing_market` | Bing 搜索市场区域 | `"en-US"` | `"en-US"` |
| `searxng_url_env` | SearXNG 地址的环境变量名 | `"JCODE_SEARXNG_URL"` | — |

**`engine` 可选值：**

| 值 | 效果 |
|-----|------|
| `"duckduckgo"`（别名 `"ddg"`） | **默认值。** DuckDuckGo HTML 搜索，无需 API Key |
| `"bing"` | Bing 搜索。配置了 API Key 时走 Bing API，否则走 Bing HTML 搜索 |
| `"searxng"`（别名 `"searx"`） | SearXNG 元搜索引擎。需配置 `searxng_url` 或 `JCODE_SEARXNG_URL` 环境变量 |

> `fallback_engines` 列表中的引擎会在主引擎失败后自动依次尝试。可通过 `JCODE_WEBSEARCH_ENGINE` 环境变量覆盖。

#### `[tools]` — 工具配置

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `profile` | 工具配置文件（full/lite/none） | `""` | `""` |
| `enabled` | 工具白名单 | `[]` | `[]` |
| `disabled` | 工具黑名单 | `[]` | `[]` |
| `disable_base_tools` | 禁用所有内置工具 | `false` | `false` |

#### `[ambient]` — 后台环境模式

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `enabled` | 启用 Ambient 模式 | `false` | `false` |
| `allow_api_keys` | 允许 Ambient 使用 API Key | `false` | `false` |
| `min_interval_minutes` | 最小间隔（分钟） | `5` | `5` |
| `max_interval_minutes` | 最大间隔（分钟） | `120` | `120` |
| `pause_on_active_session` | 用户活跃时暂停 | `true` | `true` |
| `proactive_work` | 启用自主任务 | `true` | `true` |
| `work_branch_prefix` | 工作分支前缀 | `"ambient/"` | `"ambient/"` |
| `visible` | Ambient 是否可见 | `true` | `true` |

#### `[safety]` — 安全系统通知

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `ntfy_server` | ntfy.sh 推送通知服务器地址 | `"https://ntfy.sh"` | `"https://ntfy.sh"` |
| `ntfy_topic` | ntfy.sh 主题名，用于接收推送通知 | — | — |
| `desktop_notifications` | 桌面通知 | `true` | `true` |
| `email_enabled` | 邮件通知 | `false` | `false` |
| `email_smtp_port` | SMTP 端口 | `587` | `587` |
| `email_imap_port` | IMAP 端口 | `993` | `993` |
| `email_reply_enabled` | 邮件回复审批 | `false` | `false` |
| `telegram_enabled` | Telegram 通知 | `false` | `false` |
| `telegram_reply_enabled` | Telegram 回复审批 | `false` | `false` |
| `discord_enabled` | Discord 通知 | `false` | `false` |
| `discord_reply_enabled` | Discord 回复审批 | `false` | `false` |
| `jade_relay_enabled` | Jade Relay 通知 | `false` | `false` |
| `jade_relay_reply_enabled` | Jade Relay 回复审批 | `false` | `false` |
| `jade_relay_launch_enabled` | Jade Relay 启动审批 | `false` | `false` |

**ntfy 推送通知说明：**

[ntfy.sh](https://ntfy.sh) 是一个免费的开源推送通知服务（Android / iOS 均有 app）。Jcode 在 Agent 执行需人工审批的 Tier 2 操作（发邮件、推送代码、部署等）时，通过 ntfy 推送审批请求到手机，方便你不在电脑前时也能及时处理。

配置步骤：
1. 手机安装 [ntfy app](https://ntfy.sh/app)，注册或匿名使用
2. 在应用中订阅一个主题名（建议用随机字符串，如 `jcode-your-secret-topic`）
3. 在 `~/.jcode/config.toml` 中配置：
   ```toml
   [safety]
   ntfy_topic = "jcode-your-secret-topic"
   ntfy_server = "https://ntfy.sh"   # 也可自建 ntfy 服务器
   ```
4. 在 TUI 中用 `jcode safety review` 查看待审批请求，或 `jcode safety list` / `approve` / `deny` 处理

> `ntfy_server` 默认指向公共 ntfy.sh 服务器。你也可以自建 ntfy 服务器（私有部署），将地址填在此处即可。

#### `[notifications]` — 通知设置

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `turn_complete` | 每轮完成时通知 | `true` | `true` |
| `turn_complete_min_secs` | 通知最小间隔（秒） | `120` | `120` |
| `turn_complete_todo_min_secs` | 有待办时的最小间隔（秒） | `30` | `30` |
| `turn_complete_only_when_unfocused` | 仅未聚焦时通知 | `true` | `true` |
| `turn_complete_sound` | 通知音效 | `"Glass"` | — |

#### `[compaction]` — 上下文压缩

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `mode` | 压缩模式 | `"reactive"` | `"reactive"` |
| `lookahead_turns` | 预检测轮次 | `15` | `15` |
| `ewma_alpha` | EWMA 平滑系数 | `0.3` | `0.3` |
| `proactive_floor` | 主动压缩下限 | `0.4` | — |
| `min_samples` | 最少采样数 | `3` | `3` |
| `stall_window` | 停滞检测窗口 | `5` | `5` |
| `min_turns_between_compactions` | 轮次压缩最小间隔 | `10` | `10` |
| `topic_shift_threshold` | 主题转移检测阈值 | `0.45` | — |
| `relevance_keep_threshold` | 相关性保留阈值 | `0.65` | — |
| `goal_window_turns` | 目标窗口轮次 | `5` | `5` |

#### `[hooks]` — 钩子

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `pre_tool_timeout_ms` | 工具前置钩子超时（毫秒） | `5000` | `5000` |

#### `[power]` — 电源管理

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `prevent_sleep_while_streaming` | 流式传输时阻止系统休眠 | `true` | `true` |

#### `[gateway]` — HTTP 网关

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `enabled` | 启用网关服务 | `false` | `false` |
| `port` | 监听端口 | `7643` | `7643` |
| `bind_addr` | 绑定地址 | `"0.0.0.0"` | `"0.0.0.0"` |

#### `[sponsors]` — 赞助商

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `enabled` | 启用赞助商功能 | `true` | `true` |
| `endpoint` | 发现 API 端点 | `"https://api.solosystems.dev/v1/discovery"` | — |

#### `[launch_hotkeys]` — 启动热键

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `enabled` | 启用启动热键 | `true` | `true` |

每个热键由 `[[launch_hotkeys.entries]]` 数组定义：

| 键 | 说明 | 示例值 |
|-----|------|--------|
| `chord` | 快捷键组合 | `"cmd+;"` |
| `dir` | 工作目录 | `"F:\\OneDrive\\Project\\ggufy-web"` |
| `label` | 显示标签 | `"ggufy-web"` |
| `self_dev` | 是否进入自开发模式 | `false` |

#### `[acp]` — ACP（Agent Communication Protocol）

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `profile` | ACP 配置文件 | `"standard"` | — |
| `tool_profile` | ACP 工具配置 | `"acp"` | — |

#### `[auth]` — 认证

| 键 | 说明 | 示例值 |
|-----|------|--------|
| `trusted_external_sources` | 信任的外部来源列表 | `[]` |

#### `[autoreview]` / `[autojudge]` — 自动审查/评判

| 键 | 说明 | 示例值 | 默认值 |
|-----|------|--------|--------|
| `enabled` | 启用该功能 | `false` | `false` |

### MCP 配置（JSON）

MCP 服务器使用 JSON 格式配置：

| 文件 | 作用域 |
|------|--------|
| `~/.jcode/mcp.json` | 全局 MCP 服务器 |
| `.jcode/mcp.json` | 项目级 MCP 服务器 |
| `~/.claude.json` | Claude Code 兼容 |
| `.mcp.json` | 仓库根目录（Claude Code 项目配置） |
| `.claude/mcp.json` | 传统兼容路径 |

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

首次启动时，如果 `~/.jcode/mcp.json` 不存在，Jcode 会尝试从 `~/.claude.json`、`~/.claude/mcp.json` 和 `~/.codex/config.toml` 导入 MCP 配置。

### 凭据存储（ENV 文件）

敏感信息（如 API Key）存储在独立的 ENV 文件中，不直接写入主配置，提升安全性：

```
~/.config/jcode/provider-my-api.env
~/.config/jcode/openai-compatible.env
~/.config/jcode/fireworks.env
~/.config/jcode/nvidia-nim.env
```

### 其他配置文件（JSON）

| 文件 | 说明 |
|------|------|
| `~/.jcode/servers.json` | 服务器注册信息 |
| `~/.jcode/safety/queue.json` | 安全系统待审批请求 |
| `~/.jcode/safety/history.json` | 安全系统决策历史 |
| `~/.jcode/ambient/state.json` | Ambient 模式状态 |
| `~/.jcode/ambient/queue.json` | Ambient 调度队列 |

### 运行时环境变量覆盖

无需修改配置文件，通过环境变量即可覆盖某些配置：

| 环境变量 | 说明 |
|----------|------|
| `JCODE_STREAM_IDLE_TIMEOUT_SECS` | 流式传输空闲超时（默认 180s） |
| `JCODE_SERVER_NAME` | 服务器稳定名称 |
| `JCODE_OPENAI_COMPAT_API_BASE` | OpenAI 兼容 API 基础 URL |
| `JCODE_OPENAI_COMPAT_DEFAULT_MODEL` | OpenAI 兼容默认模型 |
| `JCODE_OPENAI_EXTRA_BODY` | 注入自定义请求体字段（JSON 字符串） |
| `JCODE_SERVER_DISPLAY_NAME` | 服务器显示名称（服务管理器使用） |
| `JCODE_BING_MARKET` | Bing 搜索市场（默认 en-US） |

---

## 数据目录结构

```
~/.jcode/
├── config.toml            # 主配置文件（TOML）
├── mcp.json               # MCP 服务器配置（JSON）
├── servers.json           # 服务器注册信息（JSON）
├── auth.json              # 认证信息
├── sessions/              # 会话文件
├── memory/                # 记忆存储
├── safety/                # 安全系统
│   ├── queue.json         # 待审批请求
│   └── history.json       # 决策历史
├── ambient/               # Ambient 模式
│   ├── state.json         # 当前状态
│   └── queue.json         # 调度队列
├── builds/                # 构建分发包
│   ├── current/           # 本地构建（自开发）
│   ├── stable/            # 稳定版
│   └── versions/          # 按版本归档
└── logs/                  # 日志文件
```

---

## 内部命令（TUI 中可使用）

在聊天输入框中以 `/` 开头的指令会被解析为内部命令。

| 命令 | 说明 |
|------|------|
| `/alignment` | 切换对齐方式（左对齐/居中） |
| `/model` | 切换模型 |
| `/account` | 切换账号（多账号支持） |
| `/reload` | 热重载服务器 |
| `/ambient` | 触发后台环境模式 |
| `/alignment [left\|center]` | 切换对齐方式 |
| `/reasoning` | 切换推理内容显示模式（off → current → full → off） |
| `/thinking` | `/reasoning` 的别名 |
| `/diff [mode]` | 设置差异显示模式（off / inline / full-inline / pinned / file） |
| `/compact` | 手动触发上下文压缩 |
| `/compact mode [reactive\|proactive\|semantic]` | 设置压缩模式 |
| `/fix` | 紧急修复当前会话 |
| `/clear` | 清屏 |
| `/save [label]` | 保存当前会话（可选标签） |
| `/unsave` | 取消保存 |
| `/rename [name]` | 重命名当前会话 |
| `/resume` | 打开会话恢复列表 |
| `/sessions` | 同 `/resume` |
| `/active` | 显示所有活跃会话 |
| `/back` | 返回上一个会话 |
| `/fork` | 分叉当前会话为新会话 |
| `/split` | 同 `/fork` |
| `/catchup` | 追赶共享服务器的历史消息 |
| `/transfer` | 将会话转移到另一客户端 |
| `/memory [status\|on\|off]` | 记忆系统状态或开关 |
| `/swarm [status\|on\|off]` | Swarm 群体协作状态或开关 |
| `/rewind [undo\|n]` | 回滚 `n` 轮对话，`/rewind undo` 撤销上次回滚 |
| `/git [command]` | 执行 Git 命令 |
| `/commit` | 交互式提交当前修改 |
| `/commit-push` | 提交并推送 |
| `/cut-release` | 创建新版本发布 |
| `/transcript [path]` | 显示或设置转录文件路径 |
| `/ssh [path]` | 切换到指定路径的会话 |
| `/poke [on\|off\|status]` | 自动预取模式开关 |
| `/agents` | 查看/设置 Agent 参数 |
| `/subagent [prompt]` | 生成子 Agent 执行任务 |
| `/subagent-model [model]` | 设置子 Agent 默认模型 |
| `/selfdev [prompt]` | 进入自开发模式 |
| `/initiatives` | 查看/管理目标列表 |
| `/goals` | 同 `/initiatives` |
| `/mission` | 查看当前任务 |
| `/goal` | 查看当前目标 |
| `/test` | 运行测试 |
| `/dictate` | 触发语音听写 |
| `/keys` | 查看快捷键绑定 |
| `/keybindings` | 同 `/keys` |
| `/config` | 显示当前配置摘要 |
| `/config init` | 创建默认配置文件 |
| `/config edit` | 打开配置文件编辑器 |
| `/usage` | 显示 API 用量 |
| `/subscription` | 显示 Jcode 订阅状态 |
| `/provider-test-coverage` | 显示提供商验证覆盖 |
| `/model-status` | 显示当前模型状态 |
| `/compact-notifications [on\|off]` | 开关紧凑通知模式 |
| `/show-agentgrep-output [on\|off]` | 开关显示搜索工具输出 |
| `/log` | 显示服务器日志 |
| `/btw [text]` | 以旁白方式补充上下文给 Agent |
| `/feedback [text]` | 发送反馈 |
| `/help` | 显示帮助信息 |
| `/commands` | 列出所有可用命令 |

---

## 记忆系统

Jcode 拥有类似人类的记忆系统，支持自动语义检索。

### 工作原理

1. **嵌入存储** — 每次交互/响应自动嵌入为语义向量
2. **自动检索** — 每轮对话自动查询记忆图，找出相关记忆
3. **侧车处理** — 使用轻量级侧车模型验证记忆相关性
4. **后台整理** — Ambient 模式自动整理、去重、合并、清理记忆

### 记忆工具

```
memory { action: "remember", content: "...", category: "fact|preference|correction",
         scope: "project|global", tags: ["tag1", "tag2"] }
memory { action: "recall" }
memory { action: "search", query: "..." }
memory { action: "list", tag: "..." }
memory { action: "forget", id: "..." }
memory { action: "link", from: "id1", to: "id2", relation: "relates_to" }
memory { action: "tag", id: "...", tags: ["new", "tags"] }
```

### 记忆 CLI 命令

```bash
jcode memory list                # 列出所有记忆
jcode memory search <query>      # 搜索记忆
jcode memory export <output>     # 导出记忆到 JSON
jcode memory import <input>      # 从 JSON 导入记忆
jcode memory stats               # 记忆统计
```

### 记忆存存储位置

```
~/.jcode/memory/
├── graph.json
├── projects/
│   └── <project_hash>.json
├── global.json
├── embeddings/
├── clusters/
└── tags/
```

### 环境依赖与模型下载

记忆系统使用嵌入模型（Embedding Model）将文本转换为语义向量，实现相似度检索。

**本地嵌入模型（默认）：**

当 `[agents]` 中 `memory_embedding_backend = "local"`（默认值）时，Jcode 使用 **all-MiniLM-L6-v2** 模型进行语义嵌入。该模型由以下 Rust 库直接在 Jcode 进程中加载运行：

- **tract-hir / tract-onnx** — Rust 原生 ONNX 推理引擎，编译在 Jcode 二进制中
- **tokenizers** — HuggingFace 分词器（Rust 实现，也是编译在二进制中）

**无需提前安装任何外部工具**（Python、PyTorch、ONNX Runtime 等）。

首次启动服务器时，会自动从 Hugging Face 下载模型文件到以下目录：

```
~/.jcode/models/all-MiniLM-L6-v2/
├── model.onnx          (~23 MB)
└── tokenizer.json
```

**自动下载失败时的处理：**

如果自动下载失败（网络受限、无法访问 Hugging Face 等），可手动下载并放置到对应目录：

1. 创建模型目录：
   ```bash
   mkdir -p ~/.jcode/models/all-MiniLM-L6-v2
   ```

2. 从 Hugging Face 下载两个文件：
   - [model.onnx](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/onnx/model.onnx)（约 23 MB）
   - [tokenizer.json](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/resolve/main/tokenizer.json)

3. 将下载的文件放入 `~/.jcode/models/all-MiniLM-L6-v2/` 目录

4. 重启 Jcode 服务器，系统将自动加载已存在的模型文件，跳过下载步骤。

**远程嵌入后端（可选）：**

若环境不便运行本地模型，可改用 OpenAI 兼容的远程嵌入服务：

```toml
[agents]
memory_embedding_backend = "openai"
memory_embedding_model = "text-embedding-3-small"
memory_embedding_base_url = "https://api.openai.com/v1"
memory_embedding_dim = 1536
```

要求对应的 API Key 具有 embeddings 权限。远程嵌入的优势是不占用本地 CPU/内存资源，且向量维度可配置。

---

## Swarm 群体协作

Jcode 支持多 Agent 并行协作。

### 核心特性

1. **递归生成** — 任何 Agent 都可以生成子 Agent（无深度限制，仅受总成员上限约束）
2. **自动协作** — Agent A 编辑了 Agent B 正在读取的文件，服务器自动通知 Agent B
3. **通信方式** — 私信（DM）、子组广播（Subtree Broadcast）、频道（Channel）
4. **任务 DAG** — 有向无环图管理任务间的依赖关系
5. **计划管理** — 协调者（Coordinator）拥有计划，可分配、更新、审批

### 工作流

1. 协调者创建计划并分解任务
2. 按依赖关系将任务分配给各 Agent
3. Agent 之间通过 DM/Broadcast/Channel 直接协作
4. Agent 完成任务后自动报告给协调者
5. Git Worktree（可选）用于隔离风险变更

### Swarm 提示配置

Swarm 的模型路由策略通过 `~/.jcode/swarm-prompt.md` 或 `./jcode/swarm-prompt.md` 配置。

---

## Ambient 后台环境模式

Ambient 模式是 Jcode 的自主后台 Agent，在用户不主动提示时自动工作。

### 功能

1. **花园（Garden）** — 整理、修剪、强化记忆图
2. **侦察（Scout）** — 分析近期会话、Git 历史、记忆，了解用户关注点
3. **工作（Work）** — 自主完成用户可能欣赏的任务

### 工作原理

```
每个 Ambient 周期：
1. 检查计划队列
2. 加载记忆图
3. 花园阶段：合并重复、解决矛盾、修剪弱记忆
4. 侦察阶段：分析近期会话和 Git 历史
5. 工作阶段：执行自主任务
6. 报告并安排下次唤醒
```

### 配置

```toml
[ambient]
enabled = false                     # 启用 Ambient 模式
min_interval_minutes = 5            # 最小间隔
max_interval_minutes = 120          # 最大间隔
pause_on_active_session = true      # 用户活跃时暂停
proactive_work = true               # 启用自主任务
work_branch_prefix = "ambient/"     # 工作分支前缀
```

---

## 安全系统

安全系统为无人监控的 Agent 操作提供人工介入（Human-in-the-loop）的安全层。

### 权限分级

**自动允许（Tier 1）：**
- 读取项目文件
- 读取 Git 历史/状态
- 运行只读测试
- 记忆操作
- 创建本地分支/Git 工作树

**需审批（Tier 2）：**
- 与人通信（发送邮件、创建 Issue/PR、发消息）
- 修改代码（必须使用工作树 + PR）
- 推送到远程
- 修改 CI/CD 管道
- 安装系统包
- 修改系统配置
- 部署到任何环境
- 删除文件
- 财务/账户操作

### 安全系统 CLI

```bash
jcode safety review            # 交互式审查待处理请求
jcode safety list              # 列出所有待处理请求
jcode safety approve <id>      # 批准请求
jcode safety deny <id>         # 拒绝请求
jcode safety log               # 查看决策历史
```

---

## 浏览器自动化

Jcode 内置浏览器自动化工具。

### 快速设置

```bash
jcode browser status    # 检查状态
jcode browser setup     # 设置（Firefox Agent Bridge）
```

### 支持的浏览器操作

open、snapshot、get_content、click、type、fill_form、select、wait、screenshot、eval、scroll、upload、press

**支持的浏览器后端：**
- Firefox（通过 Firefox Agent Bridge）
- Chrome（计划中，可通过 CDP 适配器添加）

---

## 自开发（Self-Dev）

Jcode 支持自我修改，Agent 可以直接修改自身源码、编译、测试、热重载。

```bash
# 进入自开发模式
jcode self-dev

# 或者告诉 Agent "enter self dev mode"
```

自开发模式下的工具链：
- 自动检测 jcode 仓库
- 启用自开发提示和工具集
- 编辑源码、编译、测试、热重载全自动
- 推荐使用前沿模型（如 GPT 5.5）处理代码修改

---

## 性能对比

**性能对比数据（与同类工具）：**

| 指标 | Jcode | Claude Code | Cursor Agent |
|------|-------|-------------|--------------|
| 首帧时间 | **14ms** | 3437ms (245×) | 1950ms (139×) |
| 单会话 RAM | **27.8MB** | 386.6MB (13.9×) | 214.9MB (7.7×) |
| 10 会话 RAM | **117MB** | 2300.6MB (19.7×) | 1632.4MB (14×) |
| 每额外会话 | **~9.9MB** | ~212.7MB (21.5×) | ~157.5MB (15.9×) |

---

## 快捷键

| 快捷键 | 说明 |
|--------|------|
| `Alt+C` | 切换对齐方式（左对齐/居中） |
| `Shift+Enter` | 队列发送（等待 Agent 完成当前轮次后再发送） |

---

## 会话管理

### 创建/恢复会话

```bash
jcode                    # 启动新会话
jcode --resume fox       # 恢复名为 fox 的会话
jcode --resume           # 列出所有可恢复的会话
jcode session rename fox my-new-name    # 重命名会话
```

### 跨工具会话恢复

Jcode 支持从其他工具恢复会话：Codex、Claude Code、OpenCode、Pi。

```bash
# 例如从 Codex 断开的会话恢复
/resume
```

---

## 日志与调试

```bash
# 日志文件位置
~/.jcode/logs/jcode-YYYY-MM-DD.log

# 启用调试 socket（广播所有 TUI 状态变更）
jcode --debug-socket

# 调试命令
jcode debug list          # 列出活跃会话
jcode debug sessions      # 会话信息
jcode debug state         # 状态信息
```


---

## 常见问题（FAQ）

### 如何切换模型？

在 TUI 中使用 `/model` 命令，或启动时使用 `--model` 参数。

### 如何切换账号？

在 TUI 中使用 `/account` 命令。

### 如何让 Agent 帮我安装 Jcode？

可以使用提供的安装提示（详见 README 的 Setup 部分），直接复制给任何编码助手即可。

### 断线后如何恢复？

Jcode 客户端自动重连。未启动 TUI 时，使用 `jcode --resume <session>` 恢复。

### 如何退出 Ambient 模式？

```bash
jcode ambient stop
```

### 如何查看 Ambient 活动？

```bash
jcode ambient log
jcode ambient status
```

---

## 更多资料

- [Ambient Mode / OpenClaw](docs/AMBIENT_MODE.md)
- [Browser Provider Protocol](docs/BROWSER_PROVIDER_PROTOCOL.md)
- [Memory Architecture](docs/MEMORY_ARCHITECTURE.md)
- [Swarm Architecture](docs/SWARM_ARCHITECTURE.md)
- [Server Architecture](docs/SERVER_ARCHITECTURE.md)
- [Safety System](docs/SAFETY_SYSTEM.md)
- [Windows Notes](docs/WINDOWS.md)
- [Wrappers and Shell Integration](docs/WRAPPERS.md)
- [Refactoring Notes](docs/REFACTORING.md)
- [Contributing](CONTRIBUTING.md)
