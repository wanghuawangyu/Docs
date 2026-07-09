# 认证凭据来源（单一事实来源）

本文档的存在是因为同一个困惑反复出现：代理（或人类）搜索 `ANTHROPIC_API_KEY` / `sk-ant-api`，什么都没找到，读取一个过时的 `auth-validation.json` 条目显示“已过期”，然后错误地得出“没有有效的凭证”的结论。实际上凭证是存在且有效的；它只是存在于朴素搜索没有查看的地方[reference:0]。

如果你正在调试“提供商 X 是否有凭证？”，请先阅读本文。

## 两个“双认证”提供商：Anthropic 和 OpenAI

Anthropic/Claude 和 OpenAI 各自支持两个完全独立的凭证路径，作为两个单独的登录提供商呈现[reference:1]：

| 概念 | 登录提供商 ID | 认证类型 | 凭证存储位置 |
|---|---|---|---|
| Claude，OAuth/订阅 | `claude` | OAuth | `~/.jcode/auth.json` → `anthropic_accounts[]`.access（`sk-ant-oat...`）[reference:2] |
| Claude，API 密钥 | `anthropic-api` | API 密钥 | `ANTHROPIC_API_KEY` 环境变量 **或** `~/.config/jcode/anthropic.env`[reference:3] |
| OpenAI，OAuth | `openai` | OAuth | `~/.jcode/openai-auth.json`（Codex/ChatGPT 登录）[reference:4] |
| OpenAI，API 密钥 | `openai-api` | API 密钥 | `OPENAI_API_KEY` 环境变量 **或** `~/.config/jcode/openai.env`[reference:5] |

**容易让人踩坑的关键事实：**

- **OAuth 令牌不是 API 密钥。** Anthropic OAuth 令牌是 `sk-ant-oat01-...`（刷新令牌是 `sk-ant-ort01-...`）。直接 API 密钥是 `sk-ant-api03-...`。搜索 `sk-ant-api` 会漏掉仅 OAuth 的设置，反之亦然[reference:6]。
- **API 密钥通常在应用配置目录中，而不是环境变量。** 规范存储是 `~/.config/jcode/anthropic.env`（XDG `$XDG_CONFIG_HOME/jcode/anthropic.env`），由 `jcode login --provider anthropic-api` 写入[reference:7]。`printenv ANTHROPIC_API_KEY` 返回空**并不意味着**没有密钥[reference:8]。
- `~/.jcode/auth.json` 只保存 **OAuth 账户**，从不保存 API 密钥[reference:9]。
- `claude` 和 `anthropic-api` 是 **不同的提供商**，可用性不同。拥有 Claude 订阅登录（OAuth）**并不意味着** `anthropic-api` 可用，反之亦然[reference:10]。

### 如何正确检查（不要猜测）

```sh
# 每个提供商的诚实、规范化答案：
jcode auth status --json
```

每个提供商条目报告 `status`、`auth_kind`（"OAuth" vs "API key"）、`credential_source`（环境变量 / 应用配置文件 / jcode 管理的文件）以及确切方法[reference:11]。这是规范表面，优先于 grep 文件[reference:12]。

在程序层面，单一事实来源是 `crates/jcode-base/src/auth/mod.rs` 中的 `AuthStatus::assessment_for_provider(descriptor)`，它返回一个 `ProviderAuthAssessment`[reference:13]。

## 通过配置选择默认值

`~/.jcode/config.toml`：

```toml
[provider]
default_provider = "claude"           # Claude 订阅（OAuth）
# default_provider = "anthropic-api"  # 通过直接 Anthropic API 密钥使用 Claude
default_model = "claude-opus-4-8"
anthropic_reasoning_effort = "xhigh"
```

- `default_provider = "claude"` 使用 OAuth/订阅凭证[reference:14]。
- `default_provider = "anthropic-api"` 使用直接 API 密钥。在此模式下，运行时**不会**回退到 OAuth：如果未配置 API 密钥，请求将失败[reference:15]。确保 `~/.config/jcode/anthropic.env`（或 `ANTHROPIC_API_KEY`）存在[reference:16]。

完整的别名/词汇映射（运行时环境、路由稳定 ID、CLI `--provider`、模型前缀）集中在 `crates/jcode-provider-core/src/auth_mode.rs`（`AuthRoute`）中[reference:17]。不要手动解析这些字符串，请通过 `AuthRoute` 处理[reference:18]。

## 为什么“已过期”具有误导性：验证缓存不是实时状态

`~/.jcode/auth-validation.json` 缓存了每个提供商**上一次**运行时认证测试的结果[reference:19]。它是一个历史记录，而非当前的凭证状态[reference:20]。一个此后已自动刷新的 OAuth 令牌仍可能在这里显示几天前的“验证失败/已过期”条目[reference:21]。

为避免将过时记录呈现为当前事实，`format_record_label`（`crates/jcode-base/src/auth/validation.rs`）会将早于 `doctor::VALIDATION_STALE_AFTER_MS`（7 天）的任何记录标记为 `stale, ... re-validate`[reference:22]。将过时记录视为“未知，重新检查”，切勿将其视为事实依据[reference:23]。重新验证：

```sh
jcode auth-test --provider <提供商>
```

## “提供商 X 是否已认证？”快速决策树

1. 运行 `jcode auth status --json`，读取**特定**登录提供商 ID 的条目（`claude` 与 `anthropic-api` 是不同的！）[reference:24]。
2. 如果必须检查文件：OAuth → `~/.jcode/auth.json`（以及外部导入）；API 密钥 → `ANTHROPIC_API_KEY` 环境变量或 `~/.config/jcode/<provider>.env`[reference:25]。
3. 忽略早于 7 天的 `auth-validation.json` 裁决（显示为 `stale`），改为重新运行 `jcode auth-test`[reference:26]。

## 从其他代理工具导入凭证

在新安装时，jcode 可以**重用其他编码代理留下的登录信息**，包括 OAuth 令牌和 API 密钥[reference:27]。检测需要用户同意：jcode 列出它找到的来源，并仅在你批准每个来源后才读取它们（`crates/jcode-base/src/auth/external.rs`，`unconsented_sources` / `trust_external_auth_source`）[reference:28]。没有任何内容被复制到 jcode 自己的存储中；外部文件被原地读取[reference:29]。

共享的 `auth.json` 风格来源（`ExternalAuthSource`）[reference:30]：

| 工具 | 认证文件路径 | 磁盘结构 |
|---|---|---|
| OpenCode | `~/.local/share/opencode/auth.json` | 扁平 `{ provider: { type: "oauth", access, refresh, expires } \| { type: "api", key } }`[reference:31] |
| pi | `~/.pi/agent/auth.json` | 扁平 `{ provider: { type: "oauth", ... } \| { type: "api_key", key } }`（key 可能为 `$ENV` 引用）[reference:32] |
| OpenClaw | `~/.openclaw/agent/auth.json`、`~/.openclaw/agents/<agent>/auth-profiles.json`、`~/.openclaw/agents/<agent>/auth.json`、`~/.openclaw/credentials/oauth.json` | 旧版扁平 pi 结构，或当前 `{ "profiles": { "<profile>": ... } }` 存储（第一个存在的路径优先；`main` agent 和 `:default` profile 优先）[reference:33] |
| Hermes | `~/.hermes/auth.json` | 嵌套 `{ credential_pool: { provider: [ { auth_type, access_token, refresh_token, expires_at_ms } ] }, providers: {...} }`[reference:34] |

注意事项：
- pi/OpenClaw 的 API 密钥值如果是 `$ENV_VAR` 引用，则从环境中解析；以 `!` 开头的值（shell 命令）**永远不会被执行**，会被跳过[reference:35]。
- Hermes 在 `credential_pool` 条目的 `access_token` 字段中存储字面量 API 密钥，但许多提供商只存储环境变量**名称**，因此除非设置了该环境变量，否则这些条目不会导入任何内容[reference:36]。
- 其他工具特定的导入器存在于 Claude Code、Codex、Gemini CLI、GitHub Copilot 和 Cursor（参见 `auth/claude.rs`、`auth/codex.rs`、`auth/gemini.rs`、`auth/copilot.rs`、`auth/cursor.rs`）[reference:37]。