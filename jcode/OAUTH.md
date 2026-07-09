# 认证说明：OAuth + API 密钥提供商

本文档说明 J-Code 中的认证机制。[reference:0]

## 概述

J-Code 能够检测现有的本地凭证，也可以运行内置的 OAuth 和 API 密钥登录流程。[reference:1]

对于由其他工具/CLI 管理的认证文件，jcode 会在读取前询问用户。如果你批准了某个来源，jcode 会记住该外部认证文件路径的批准状态，供后续会话使用，并且不会移动、重写或修改原始文件的权限。符号链接的外部认证文件将被拒绝。[reference:2]

凭证存储在本地：
- **J-Code Claude OAuth**（通过 `jcode login --provider claude` 登录）：`~/.jcode/auth.json`[reference:3]
- **Claude Code CLI**：`~/.claude/.credentials.json`（Linux/Windows），或 macOS 登录钥匙串中的 `Claude Code-credentials` 项（macOS 默认，通常 JSON 文件不存在），或 `CLAUDE_CODE_OAUTH_TOKEN` 环境变量[reference:4]
- **OpenCode**（可选的提供商/OAuth 导入源）：`~/.local/share/opencode/auth.json`[reference:5]
- **pi**（可选的提供商/OAuth 导入源）：`~/.pi/agent/auth.json`[reference:6]
- **J-Code OpenAI/Codex OAuth**：`~/.jcode/openai-auth.json`[reference:7]
- **Codex CLI 认证源**（确认后原地读取）：`~/.codex/auth.json`[reference:8]
- **Gemini 原生 OAuth**：`~/.jcode/gemini_oauth.json`[reference:9]
- **Gemini CLI 导入回退**：`~/.gemini/oauth_creds.json`[reference:10]
- **Copilot CLI 明文回退**：`~/.copilot/config.json`[reference:11]
- **旧版 Copilot JSON 源**：`~/.config/github-copilot/hosts.json`、`~/.config/github-copilot/apps.json`[reference:12]

相关代码：
- Claude 提供商：`src/provider/claude.rs`[reference:13]
- OpenAI 登录 + 刷新：`src/auth/oauth.rs`[reference:14]
- OpenAI 凭证解析：`src/auth/codex.rs`[reference:15]
- OpenAI 请求：`src/provider/openai.rs`[reference:16]
- Azure OpenAI 认证/配置：`src/auth/azure.rs`[reference:17]
- Azure OpenAI 传输：`src/provider/openrouter.rs`[reference:18]
- Gemini 登录 + 刷新：`src/auth/gemini.rs`[reference:19]
- Gemini Code Assist 提供商：`src/provider/gemini.rs`[reference:20]
- OpenAI 兼容提供商元数据/登录描述符：`crates/jcode-provider-metadata/src/lib.rs`[reference:21]

## Claude（Claude Max）

### 登录步骤

- 运行 `jcode login --provider claude`（推荐），或 `jcode login` 然后选择 Claude。[reference:22]
- 无头/SSH 环境使用：`jcode login --provider claude --no-browser`[reference:23]
- 可脚本化的远程流程：`jcode login --provider claude --print-auth-url`，然后使用 `--callback-url` 或 `--auth-code` 完成。[reference:24]
- 替代方案：运行 `claude`（或 `claude setup-token`）。jcode 可以检测 Claude Code 的凭证，读取前询问，并记住该批准用于后续会话。无论 Claude Code 将凭证存储在 `~/.claude/.credentials.json`（Linux/Windows）、macOS 登录钥匙串（`Claude Code-credentials`）还是 `CLAUDE_CODE_OAUTH_TOKEN` 环境变量中，此方式均有效。在 macOS 上，批准钥匙串源后会一次性将凭证复制到 `~/.jcode/auth.json`，后续会话不再重复弹出钥匙串提示。[reference:25]
- 验证：`jcode --provider claude run "Say hello from jcode"`。[reference:26]

凭证发现顺序：
1. `~/.jcode/auth.json`[reference:27]
2. `~/.claude/.credentials.json`[reference:28]
3. Claude Code 原生凭证（macOS 钥匙串 `Claude Code-credentials`，或 `CLAUDE_CODE_OAUTH_TOKEN` 环境变量），经批准后[reference:29]
4. `~/.local/share/opencode/auth.json`[reference:30]
5. `~/.pi/agent/auth.json`[reference:31]

### 直接 Anthropic API（默认）

`--provider claude` 默认使用直接的 Anthropic Messages API。jcode 完全掌控完整的运行时路径：认证、刷新、请求整形、工具兼容性和传输。[reference:32]

#### Claude OAuth 直接 API 兼容性

Claude Code OAuth 令牌可直接用于 Messages API，但仅当请求符合 Claude Code 的“OAuth 契约”时。jcode 对默认的 Claude 运行时路径自动应用此契约。[reference:33]

必需的行为（由 Anthropic 提供商自动应用）：
- 使用 Messages 端点并带 `?beta=true`。[reference:34]
- 发送 `User-Agent: claude-cli/1.0.0`。[reference:35]
- 发送 `anthropic-beta: oauth-2025-04-20,claude-code-20250219`。[reference:36]
- 在系统块前添加 Claude Code 身份行作为第一个块：[reference:37]
  - `You are Claude Code, Anthropic's official CLI for Claude.`

工具名称允许列表：Claude OAuth 请求会拒绝某些工具名称。jcode 在传输层将少量内置工具名称映射为 Claude-Code 内置名称，并在响应时映射回来，使原生工具继续工作。所有其他工具均以其原名转发，因此完整的自定义工具集（websearch、webfetch、browser、codesearch、memory、swarm、multiedit、open 等）在 OAuth 下仍然可用。[reference:38]

映射名称：
- `bash` → `Bash`[reference:39]
- `read` → `Read`[reference:40]
- `write` → `Write`[reference:41]
- `edit` → `Edit`[reference:42]
- `glob` → `Glob`[reference:43]
- `grep` → `Grep`[reference:44]
- `subagent` → `Agent`[reference:45]
- `schedule` → `ScheduleWakeup`[reference:46]
- `skill_manage` → `Skill`[reference:47]

注意：
- 如果 OAuth 令牌过期，通过 Claude OAuth 刷新端点刷新。[reference:48]
- 没有身份行和允许列表中的工具名称，API 将拒绝 OAuth 请求，即使令牌本身有效。[reference:49]

### 已弃用的 Claude CLI 传输

旧的 Claude CLI shell-out 路径已弃用，仅用于遗留兼容性。你仍可通过以下方式临时强制使用：[reference:50]
- `JCODE_USE_CLAUDE_CLI=1`[reference:51]
- 或 `--provider claude-subprocess`（已弃用的隐藏兼容值）[reference:52]

以下环境变量控制已弃用的 Claude Code CLI 传输：[reference:53]
- `JCODE_CLAUDE_CLI_PATH`（默认：`claude`）[reference:54]
- `JCODE_CLAUDE_CLI_MODEL`（默认：`claude-opus-4-5-20251101`）[reference:55]
- `JCODE_CLAUDE_CLI_PERMISSION_MODE`（默认：`bypassPermissions`）[reference:56]
- `JCODE_CLAUDE_CLI_PARTIAL`（设为 `0` 以禁用部分流式传输）[reference:57]

## OpenAI / Codex OAuth

### 登录步骤

- 运行 `jcode login --provider openai`。[reference:58]
- 无头/SSH 环境使用：`jcode login --provider openai --no-browser`[reference:59]
- 可脚本化的远程流程：`jcode login --provider openai --print-auth-url`，然后使用 `--callback-url` 完成。[reference:60]
- 浏览器会打开 OpenAI OAuth 页面，除非使用 `--no-browser`。本地回调默认监听 `http://localhost:1455/auth/callback`。如果端口 1455 不可用，jcode 回退到手动粘贴流程，你可以粘贴完整的回调 URL 或查询字符串。[reference:61]
- 登录后，令牌保存到 `~/.jcode/openai-auth.json`。[reference:62]

凭证发现顺序：
1. `~/.jcode/openai-auth.json`[reference:63]
2. `~/.codex/auth.json`[reference:64]
3. 受信任的 OpenCode/pi OAuth：`~/.local/share/opencode/auth.json` / `~/.pi/agent/auth.json`[reference:65]
4. `OPENAI_API_KEY`[reference:66]

如果 jcode 在 `~/.codex/auth.json` 中发现现有凭证，会在读取前询问。批准后，它会记住该信任决定用于后续 jcode 会话，且不会移动、删除或重写 Codex 文件。[reference:67]

### 请求详情

J-Code 使用 Responses API。[reference:68]

如果你有 ChatGPT 订阅（存在 refresh_token 或 id_token），请求发送至：
- `https://chatgpt.com/backend-api/codex/responses`[reference:69]
- 请求头：[reference:70]
  - `originator: codex_cli_rs`[reference:71]
  - `chatgpt-account-id: <账号ID>`[reference:72]

否则使用：
- `https://api.openai.com/v1/responses`[reference:73]

对于 API 密钥使用（无 ChatGPT/Codex OAuth），Responses API 基础 URL 是可覆盖的，因此你可以指向本地或代理的 Responses-API 端点。按以下顺序设置（检查顺序）为绝对 `http(s)://` 基础 URL，以 API 版本结尾，例如 `http://127.0.0.1:8317/v1`：[reference:74]
- `JCODE_OPENAI_API_BASE`[reference:75]
- `OPENAI_BASE_URL`[reference:76]
- `OPENAI_API_BASE`[reference:77]

jcode 会自动追加 `/responses`，从同一基础 URL 派生 WebSocket 和 `/compact` 端点，并将 `/models` 目录探测指向该基础 URL。该覆盖在 ChatGPT/Codex OAuth 模式下被忽略（该后端是固定的），格式错误的值会被记录并忽略，不会中断请求。[reference:78]

### 故障排除

- Claude 401/认证错误：运行 `jcode login --provider claude`。[reference:79]
- 401/403：重新运行 `jcode login --provider openai`。[reference:80]
- 回调问题：确保端口 1455 空闲且浏览器可以访问 `http://localhost:1455/auth/callback`。[reference:81]

## Azure OpenAI

此功能是在将 J-Code 与 OpenCode/Crush 对比后添加的。有意义的认证差距不是另一个浏览器 OAuth 流程，而是对使用以下方式的 Azure OpenAI 的支持：[reference:82]
- Microsoft Entra ID 凭证（通过 Azure 的 `DefaultAzureCredential` 链），或[reference:83]
- Azure OpenAI API 密钥[reference:84]

### 登录/设置步骤

- 运行 `jcode login --provider azure`。[reference:85]
- 输入你的 Azure OpenAI 端点，例如：`https://your-resource.openai.azure.com`[reference:86]
- 输入你的 Azure 部署/模型名称。[reference:87]
- 选择一种认证方式：[reference:88]
  - Entra ID（推荐）[reference:89]
  - API 密钥[reference:90]
- jcode 将设置保存到 `~/.config/jcode/azure-openai.env`。[reference:91]

### 存储的配置

Azure env 文件可能包含：[reference:92]
- `AZURE_OPENAI_ENDPOINT`[reference:93]
- `AZURE_OPENAI_MODEL`[reference:94]
- `AZURE_OPENAI_USE_ENTRA`[reference:95]
- `AZURE_OPENAI_API_KEY`（仅在使用密钥认证时）[reference:96]

### 运行时行为

- jcode 将端点规范化为较新的 Azure OpenAI `/openai/v1` 基础 URL。[reference:97]
- Entra ID 模式下，jcode 使用 `azure_identity::DefaultAzureCredential` 获取 Bearer 令牌，作用域为 `https://cognitiveservices.azure.com/.default`。[reference:98]
- API 密钥模式下，jcode 在 Azure 风格的 `api-key` 请求头中发送凭证。[reference:99]
- Azure 提供商目前在底层复用 J-Code 的 OpenAI 兼容传输层。[reference:100]
- Azure 默认禁用模型目录获取，因此你应显式配置部署/模型。[reference:101]

### Entra ID 凭证源

`DefaultAzureCredential` 可以从以下来源解析凭证：[reference:102]
- `az login`[reference:103]
- 托管身份[reference:104]
- Azure 环境凭证[reference:105]

### 故障排除

- 如果 Entra ID 认证在本地失败，先尝试 `az login`。[reference:106]
- 确保你的身份具有访问 Azure OpenAI 资源的权限。[reference:107]
- 如果请求因部署/模型错误失败，验证 `AZURE_OPENAI_MODEL` 与你的部署模型名称匹配。[reference:108]
- 如果倾向于使用静态凭证，重新运行 `jcode login --provider azure` 并选择 API 密钥模式。[reference:109]

## Gemini OAuth

### 登录步骤

- 运行 `jcode login --provider gemini` 或在 TUI 内使用 `/login gemini`。[reference:110]
- 无头/SSH 环境使用：`jcode login --provider gemini --no-browser`[reference:111]
- 可脚本化的远程流程：`jcode login --provider gemini --print-auth-url`，然后使用 `--auth-code` 完成。[reference:112]
- jcode 打开浏览器进入用于 Gemini Code Assist 的 Google OAuth 流程，除非使用 `--no-browser`。[reference:113]
- 如果本地回调绑定不可用，jcode 回退到使用 `https://codeassist.google.com/authcode` 的手动粘贴流程。[reference:114]
- 令牌保存到 `~/.jcode/gemini_oauth.json`。[reference:115]

### 凭证发现顺序

- 原生 jcode Gemini 令牌：`~/.jcode/gemini_oauth.json`[reference:116]
- Gemini CLI OAuth 源（批准后只读）：`~/.gemini/oauth_creds.json`[reference:117]
- 受信任的 OpenCode/pi OAuth：`~/.local/share/opencode/auth.json` / `~/.pi/agent/auth.json`[reference:118]

### 运行时说明

- jcode 使用原生 Google OAuth 并直接与 Google Code Assist 后端通信。[reference:119]
- 过期令牌使用 Google refresh_token 自动刷新。[reference:120]
- 某些学校/工作区账户可能需要 `GOOGLE_CLOUD_PROJECT` 或 `GOOGLE_CLOUD_PROJECT_ID` 用于 Code Assist 权限检查。[reference:121]

### 故障排除

- 如果浏览器启动失败，使用 `--no-browser` 和粘贴回调/代码流程。[reference:122]
- 如果工作区账户的授权或入门失败，设置 `GOOGLE_CLOUD_PROJECT` 并重试。[reference:123]
- 如果登录成功但后续请求失败，重新运行 `jcode login --provider gemini` 以刷新存储的会话。[reference:124]

### 认证验证

使用内置认证验证器在登录后测试完整的本地认证/运行时路径：[reference:125]

```bash
# 立即运行 Gemini 登录，然后验证令牌刷新 + 提供商冒烟测试
jcode --provider gemini auth-test --login

# 验证现有 Gemini 认证，无需重新运行登录
jcode --provider gemini auth-test

# 检查每个当前配置的支持的认证提供商
jcode auth-test --all-configured
```

对于模型提供商，`auth-test` 尝试：[reference:126]
- 凭证发现[reference:127]
- 刷新/认证探测[reference:128]
- 真实提供商冒烟提示，期望 `AUTH_TEST_OK`[reference:129]
- 使用与正常聊天相同的工具附加请求路径进行工具启用冒烟提示[reference:130]

如果只需认证/简单运行时检查，使用 `--no-tool-smoke`。[reference:131]

对于 Gmail/Google，它验证凭证发现和令牌刷新，但跳过模型冒烟，因为它不是模型提供商。[reference:132]

## OpenAI 兼容 API 密钥提供商

J-Code 还为许多 OpenAI 兼容 API 提供了一流的提供商预设。这些提供商使用相同的内置登录流程模式：`jcode login --provider <提供商>`。[reference:133]

对于任意的 OpenAI 兼容 API，尤其是当 Agent 正在执行设置时，推荐使用命名配置文件命令，而不是手动编辑配置：[reference:134]

```bash
printf '%s' "$MY_API_KEY" | jcode provider add my-api \
  --base-url https://llm.example.com/v1 \
  --model my-model-id \
  --api-key-stdin \
  --set-default \
  --json

jcode --provider-profile my-api auth-test --no-tool-smoke
```

这会向 `~/.jcode/config.toml` 写入 `[providers.my-api]`，并将密钥存储在 jcode 的私有应用配置目录中，例如 `~/.config/jcode/provider-my-api.env`。对于本地主机服务器，使用 `--no-api-key`。[reference:135]

两个值得注意的预设：

### Fireworks

- 登录：`jcode login --provider fireworks`[reference:136]
- 存储的 env 文件：`~/.config/jcode/fireworks.env`[reference:137]
- API 密钥环境变量：`FIREWORKS_API_KEY`[reference:138]
- 基础 URL：`https://api.fireworks.ai/inference/v1`[reference:139]
- 默认模型提示：`accounts/fireworks/routers/kimi-k2p5-turbo`[reference:140]
- 文档：[https://docs.fireworks.ai/tools-sdks/openai-compatibility](https://docs.fireworks.ai/tools-sdks/openai-compatibility)[reference:141]

### MiniMax

- 登录：`jcode login --provider minimax`[reference:142]
- 存储的 env 文件：`~/.config/jcode/minimax.env`[reference:143]
- API 密钥环境变量：`OPENAI_API_KEY`[reference:144]
- 基础 URL：`https://api.minimax.io/v1`[reference:145]
- 默认模型提示：`MiniMax-M2.7`[reference:146]
- 文档：[https://platform.minimax.io/docs/guides/text-generation](https://platform.minimax.io/docs/guides/text-generation)[reference:147]

这些是一流的 jcode 提供商预设，而不仅仅是手动自定义端点示例。当没有内置预设时，你仍然可以对任意自定义提供商使用 `openai-compatible`。[reference:148]

如果 jcode 在受信任的 OpenCode/pi 认证文件中找到匹配的 API 密钥，它可以为相应的提供商预设重用这些密钥，而无需你再次粘贴密钥。[reference:149]

## 实验性 CLI 提供商

J-Code 还支持实验性的 CLI 后端提供商，以及带有原生 OAuth 登录的 Antigravity：[reference:150]
- `--provider cursor`[reference:151]
- `--provider copilot`[reference:152]
- `--provider antigravity`[reference:153]

Cursor 使用 jcode 的原生 HTTPS 传输。Copilot 使用 GitHub 设备流认证。Antigravity 登录/认证存储由 jcode 原生处理。[reference:154]

### Cursor

- 登录：`jcode login --provider cursor`[reference:155]
- 保存 `CURSOR_API_KEY` 到 `~/.config/jcode/cursor.env`[reference:156]
- 运行时：[reference:157]
  - jcode 使用原生 HTTPS 请求[reference:158]
  - 如果配置了 Cursor API 密钥，jcode 直接交换/使用它[reference:159]
- 环境变量：[reference:160]
  - `JCODE_CURSOR_MODEL`（默认：`composer-1.5`）[reference:161]
  - `CURSOR_API_KEY`（可选；覆盖已保存的密钥）[reference:162]

### GitHub Copilot

- 登录：`jcode login --provider copilot`[reference:163]
- 无头/SSH：`jcode login --provider copilot --no-browser`[reference:164]
- 可脚本化远程流程：`jcode login --provider copilot --print-auth-url`，然后 `jcode login --provider copilot --complete`[reference:165]
- jcode 使用 GitHub 设备码流程，可以在不打开本地浏览器的情况下打印验证 URL/QR。[reference:166]
- 凭证发现顺序：[reference:167]
  - `COPILOT_GITHUB_TOKEN`[reference:168]
  - `GH_TOKEN`[reference:169]
  - `GITHUB_TOKEN`[reference:170]
  - 受信任的 `~/.copilot/config.json`[reference:171]
  - 受信任的旧版 `~/.config/github-copilot/hosts.json`[reference:172]
  - 受信任的旧版 `~/.config/github-copilot/apps.json`[reference:173]
  - 受信任的 OpenCode/pi OAuth 条目[reference:174]
  - `gh auth token`[reference:175]
- 环境变量：[reference:176]
  - `JCODE_COPILOT_CLI_PATH`（可选覆盖 CLI 路径）[reference:177]
  - `JCODE_COPILOT_MODEL`（默认：`claude-sonnet-4`）[reference:178]

### Antigravity

- 登录：`jcode login --provider antigravity`（原生 Google OAuth 流程；不需要安装 Antigravity）[reference:179]
- 无头/SSH：`jcode login --provider antigravity --no-browser`[reference:180]
- 可脚本化远程流程：`jcode login --provider antigravity --print-auth-url`，然后使用 `--callback-url` 完成[reference:181]
- 令牌：`~/.jcode/antigravity_oauth.json`[reference:182]
- 凭证发现顺序：[reference:183]
  - 原生 jcode 令牌：`~/.jcode/antigravity_oauth.json`[reference:184]
  - 受信任的 OpenCode/pi OAuth 条目（如果存在）[reference:185]
- 运行时：[reference:186]
  - jcode 直接认证并自行存储/刷新 Antigravity OAuth 令牌[reference:187]
  - 如果选择 `--provider antigravity`，提供商传输仍然会 shell-out 到 Antigravity CLI 进行补全[reference:188]
- 环境变量：[reference:189]
  - `JCODE_ANTIGRAVITY_CLIENT_ID`（可选覆盖 OAuth 客户端 ID）[reference:190]
  - `JCODE_ANTIGRAVITY_CLIENT_SECRET`（可选覆盖 OAuth 客户端密钥）[reference:191]
  - `JCODE_ANTIGRAVITY_VERSION`（可选覆盖 Antigravity 请求指纹/版本）[reference:192]
  - `JCODE_ANTIGRAVITY_CLI_PATH`（默认：`antigravity`，仅运行时）[reference:193]
  - `JCODE_ANTIGRAVITY_MODEL`（默认：`default`）[reference:194]
  - `JCODE_ANTIGRAVITY_PROMPT_FLAG`（默认：`-p`）[reference:195]
  - `JCODE_ANTIGRAVITY_MODEL_FLAG`（默认：`--model`）[reference:196]

## Google / Gmail OAuth

### 登录步骤

- 运行 `jcode login --provider google`。[reference:197]
- 无头/SSH 环境使用：`jcode login --provider google --no-browser`[reference:198]
- 凭证已配置后的可脚本化远程流程：`jcode login --provider google --print-auth-url`[reference:199]
- 如果 Google 凭证尚未配置，jcode 首先引导你保存客户端 ID/客户端密钥或导入 JSON 凭证文件。[reference:200]
- 对于可脚本化的 Google 流程，如果你不希望使用默认的完全访问权限，可通过 `--google-access-tier full|readonly` 选择 Gmail 作用域。[reference:201]
- 稍后通过 `jcode login --provider google --callback-url '<URL>'` 完成打印的流程。[reference:202]

### 说明

- Google/Gmail 可脚本化认证需要先保存 OAuth 客户端凭证。[reference:203]
- 回调 URL 可以来自远程浏览器会话，该会话在环回重定向上失败。从地址栏复制最终 URL 并粘贴或传递回 jcode。[reference:204]

## 可脚本化认证状态生命周期

- jcode 将临时可脚本化登录状态存储在 `~/.jcode/pending-login/*.json`。[reference:205]
- 待处理状态会自动过期。[reference:206]
- 过期的待处理条目在可脚本化登录流程启动或恢复时被清理。[reference:207]
- Copilot 的 `--print-auth-url` 存储 GitHub 设备码会话，`--complete` 稍后恢复轮询。[reference:208]