# AWS Bedrock 提供商

Jcode 支持原生的 AWS Bedrock 提供商，通过 AWS Rust SDK 和 `ConverseStream` 直接与 Bedrock Runtime 通信。[reference:0]

## 配置凭证

Jcode 支持两种 Bedrock 认证方式：[reference:1]

- **Bedrock API 密钥 / Bearer 令牌**：本地入门最简单。Jcode 将令牌存储在配置 env 文件中，并通过 AWS SDK 作为 `AWS_BEARER_TOKEN_BEDROCK` 发送。[reference:2]
- **AWS IAM 凭证**：适用于常规 AWS 客户环境。可以是 AWS CLI/SSO 配置文件、环境访问密钥、Web 身份、EC2/ECS 元数据凭证或其他标准 AWS SDK 凭证源。[reference:3]

对于引导式 API 密钥流程，运行：

```bash
jcode login --provider bedrock
```

这将保存 `AWS_BEARER_TOKEN_BEDROCK` 和 `JCODE_BEDROCK_REGION` 到 `~/.config/jcode/bedrock.env`。[reference:4]

你也可以手动配置：

```bash
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
export AWS_REGION=us-east-1
```

对于 AWS CLI/IAM/SSO 凭证：

```bash
export AWS_PROFILE=my-profile
export AWS_REGION=us-east-1
# 可选的 Jcode 特定覆盖：
export JCODE_BEDROCK_PROFILE=my-profile
export JCODE_BEDROCK_REGION=us-east-1
```

如果你依赖实例/容器元数据凭证且没有本地配置文件环境变量，显式选择加入：

```bash
export JCODE_BEDROCK_ENABLE=1
export AWS_REGION=us-east-1
```

对于 AWS SSO 配置文件，运行：

```bash
aws sso login --profile my-profile
```

对于 AWS CLI 控制台登录配置文件，Jcode 也可以使用以下命令导出的凭证：

```bash
aws configure export-credentials --profile my-profile --format env-no-export
```

Jcode 不存储这些导出的会话凭证；它在 Bedrock 提供商初始化时向 AWS CLI 配置文件提供者请求凭证。[reference:5]

## IAM 权限

运行时路径至少需要：[reference:6]

```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:InvokeModel",
    "bedrock:InvokeModelWithResponseStream"
  ],
  "Resource": "*"
}
```

模型发现额外使用：[reference:7]

```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock:ListFoundationModels",
    "bedrock:ListInferenceProfiles"
  ],
  "Resource": "*"
}
```

如果启用 `JCODE_BEDROCK_VALIDATE_STS=1`，允许 `sts:GetCallerIdentity`。[reference:8]

## 使用 Bedrock 运行 Jcode

```bash
jcode --provider bedrock --model anthropic.claude-3-5-sonnet-20241022-v2:0
```

或：

```bash
jcode --model bedrock:anthropic.claude-3-5-sonnet-20241022-v2:0
```

推理配置文件 ID/ARN 也接受作为模型 ID，例如：[reference:9]

```bash
jcode --model bedrock:us.anthropic.claude-3-5-sonnet-20241022-v2:0
```

当你的账户有访问权限时，推荐的主动配置文件风格选择包括：[reference:10]

```text
us.amazon.nova-2-lite-v1:0
us.amazon.nova-lite-v1:0
us.amazon.nova-micro-v1:0
us.anthropic.claude-sonnet-4-6
us.anthropic.claude-haiku-4-5-20251001-v1:0
us.deepseek.r1-v1:0
```

当基础模型 ID 和配置文件 ID 同时出现时，优先使用区域/配置文件 ID，如 `us.amazon.nova-2-lite-v1:0`。某些 Bedrock 模型不支持按需调用，必须通过推理配置文件调用。[reference:11]

## 模型选择器 UX

`/model` 保持 Bedrock 行紧凑：[reference:12]
- `×` 表示该路由不可选择。选择该行可查看完整原因，如旧版模型访问权限或缺少凭证。[reference:13]
- `⚠` 表示该路由可选择但有限制，最常见的是不支持工具使用。[reference:14]
- 选中的推理配置文件路由会显示其目标基础模型。[reference:15]

如果在启用模型访问、更改区域或刷新凭证后模型列表看起来过时，运行：[reference:16]

```text
/refresh-model-list
```

这会强制调用 `ListFoundationModels` 和 `ListInferenceProfiles`，更新缓存的旧版/配置文件元数据，并在可用推理配置文件路由存在时移除过时的重复基础模型行。[reference:17]

## 可选请求参数

```bash
export JCODE_BEDROCK_MAX_TOKENS=4096
export JCODE_BEDROCK_TEMPERATURE=0.2
export JCODE_BEDROCK_TOP_P=0.9
export JCODE_BEDROCK_STOP_SEQUENCES=',STOP'
```

## 模型发现

Jcode 将立即使用静态 Bedrock 模型列表。当模型预取/目录刷新运行时，它会调用 `ListFoundationModels` 和 `ListInferenceProfiles`，然后将结果缓存到 Jcode 的配置目录中。[reference:18]

缓存的 Bedrock 目录是区域范围的；如果你切换 `JCODE_BEDROCK_REGION`/`AWS_REGION`，Jcode 会忽略旧区域缓存并为新区域刷新。[reference:19]

## 实时冒烟测试

实时测试默认被忽略。仅在具有有效 AWS 凭证和已启用模型访问权限时运行：[reference:20]

```bash
JCODE_BEDROCK_LIVE_TEST=1 \
  AWS_PROFILE=my-profile \
  AWS_REGION=us-east-1 \
  cargo test -p jcode --lib provider::bedrock::tests::bedrock_live_smoke_test -- --ignored
```

## 故障排除

- `AccessDenied`：授予 Bedrock invoke/list 权限，并在 AWS Console 中启用模型访问。[reference:21]
- `model not found` 或验证错误：验证模型 ID/推理配置文件和区域支持。[reference:22]
- SSO 令牌错误：运行 `aws sso login --profile `。[reference:23]
- API 密钥认证：设置 `AWS_BEARER_TOKEN_BEDROCK` 和 `AWS_REGION`。[reference:24]
- 缺少区域：设置 `AWS_REGION` 或 `JCODE_BEDROCK_REGION`。[reference:25]