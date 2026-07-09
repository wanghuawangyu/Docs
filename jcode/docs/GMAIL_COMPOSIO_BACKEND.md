# Gmail 工具：Composio 托管后端

原生 `gmail` 工具可从两个后端之一获取凭证和传输层。工具接口、确认门控、访问层级逻辑和精简令牌的输出格式在各后端之间完全相同；只有认证/传输层会发生变化。

## 后端

| 后端 | 认证方式 | 优点 | 缺点 |
|---|---|---|---|
| direct（默认） | 本地 Google OAuth 令牌（`jcode login google`） | 无第三方介入 | 未验证应用警告；Google“测试”模式下 7 天刷新令牌过期 |
| composio | Composio 托管的 OAuth（Google 已验证应用） | 无未验证应用警告，无 7 天过期，无需每个用户的 Google Cloud 项目 | Composio 代理 Gmail 令牌托管；外部依赖/成本 |

两个后端都调用相同的 Gmail REST 端点（`https://gmail.googleapis.com/gmail/v1/users/me/...`）。Composio 后端将这些调用通过 Composio 的 [proxy-execute](https://docs.composio.dev/reference/api-reference/tools/postToolsExecuteProxy) 端点路由，该端点会附加托管的 Gmail 凭证。由于上游响应形状不变，所有现有的类型化解析和输出格式化都被复用。

## 选择后端

后端在 `GmailClient::new()` 时从环境变量解析：
- `JCODE_GMAIL_BACKEND=direct`（或未设置）→ 直接 Google 后端。
- `JCODE_GMAIL_BACKEND=composio` → Composio 后端（需要 `COMPOSIO_API_KEY`）。

如果请求了 `composio` 但 `COMPOSIO_API_KEY` 缺失，jcode 会发出警告并回退到 direct。

### Composio 环境变量

| 变量 | 是否必需 | 描述 |
|---|---|---|
| `COMPOSIO_API_KEY` | 是 | 来自 [https://platform.composio.dev](https://platform.composio.dev) 的项目 API 密钥 |
| `COMPOSIO_BASE_URL` | 否 | 覆盖 API 基础地址（默认 `https://backend.composio.dev/api/v3.1`）|
| `COMPOSIO_GMAIL_AUTH_CONFIG_ID` | 用于连接 | 来自 Composio 仪表板的 Gmail 认证配置 ID（`ac_...`）。定义连接流程使用的 OAuth 蓝图/作用域。 |
| `COMPOSIO_GMAIL_CONNECTED_ACCOUNT_ID` | 否 | 固定一个特定的已连接账户（`ca_...`）。通常在连接后自动设置。 |
| `COMPOSIO_GMAIL_USER_ID` / `COMPOSIO_USER_ID` | 否 | 多用户已连接账户的终端用户 ID（默认为 `default`）|

## 连接 Gmail 账户（代理内 OAuth）

一旦设置了 `COMPOSIO_API_KEY` 和 `COMPOSIO_GMAIL_AUTH_CONFIG_ID`，用户（或代理）即可使用 `action: "connect"` 运行 `gmail` 工具：
- jcode 调用 Composio 的 `POST /connected_accounts/link`（托管的“Connect Link”流程）以启动 OAuth 会话。
- 返回的 `redirect_url` 在系统浏览器中打开（作为备用方案打印到 stderr，例如通过 SSH 时）。
- 用户在 Google 同意屏幕上批准 Gmail 访问权限。由于 Composio 拥有 Google 已验证应用，因此不会出现“未验证应用”警告。
- jcode 轮询 `GET /connected_accounts/{id}` 直到连接变为 `ACTIVE`，然后将其持久化到 `~/.jcode/composio_gmail.json`。
- 未来的会话会加载持久化的 `connected_account_id`，因此连接步骤对每个账户只需执行一次。

在连接存在之前的工具调用会返回提示，告知代理先运行 `action: "connect"`。

注意：Composio 正在弃用用于托管 OAuth 的 `initiate()`，转而采用此处使用的 Connect Link `link()` 流程，因此此路径是未来支持的路径。

## 一次性 Composio 设置

- 在 [https://platform.composio.dev](https://platform.composio.dev) 登录并复制你的项目 API 密钥。
- 连接一个 Gmail 账户（Composio 托管的 OAuth，无未验证应用警告）。如果需要固定它，请记下生成的 `connected_account_id`。
- 导出变量：

```bash
export JCODE_GMAIL_BACKEND=composio
export COMPOSIO_API_KEY="ck_..."
# 可选：
export COMPOSIO_GMAIL_CONNECTED_ACCOUNT_ID="ca_..."
export COMPOSIO_GMAIL_USER_ID="me"
```

- 确保 `gmail` 工具在 `config.toml` 中已启用：

```toml
[tools]
enabled = ["*"]
```

## 访问层级

- **direct**：遵循在 `jcode login google` 时选择的访问层级（“仅读取”和“仅草稿”登录无法发送/删除，在 OAuth 作用域层面强制执行）。
- **composio**：连接请求完整的 Gmail 作用域，因此发送/删除可用。工具仍然要求对 `send`、`send_draft` 和 `trash` 操作显式设置 `confirmed: true`。

## 信任说明

使用 Composio 后端时，Composio 持有你的 Gmail OAuth 授权并可见 API 流量。这是相对于直接后端的核心权衡。在将其设为默认选项之前，请向用户披露此信息。