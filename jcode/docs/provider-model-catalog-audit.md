# OpenAI 兼容提供商 `/models` 审计

**范围**：`crates/jcode-provider-metadata/src/lib.rs` 中内置的 `OpenAiCompatibleProfile` 条目。

**图例**：
- `verified data[]`：文档展示或明确引用了 OpenAI 兼容的 `GET /models` 响应结构 `{ object: "list", data: [...] }`，或提供商声明其实现了 OpenAI Models API。
- `verified top-level array`：文档展示了一个顶级模型数组。
- `supported endpoint, shape not shown`：文档说明 `/models` 端点存在，或 OpenAI 兼容性包含了该端点，但未展示响应体。
- `catalog/static only`：文档指向静态目录/模型页面，而非实时的 `/models` 端点。
- `unknown`：未能找到提供商文档证明 `/models` 的存在。

## 已审计的提供商

| 提供商 | 证据 | 预期的解析器支持 | 备注 |
|---|---|---|---|
| OpenCode Zen | OpenCode 文档及 models.dev 目录 | static/bootstrap, endpoint unverified | OpenCode 自身使用 models.dev。Zen 的 `/models` 未独立验证。 |
| OpenCode Go | OpenCode 文档及 models.dev 目录 | static/bootstrap, endpoint unverified | 与 Zen 相同。 |
| Z.AI | 搜索未找到 `/models`；当前元数据路径中的提供商文档 URL 返回 404 | unknown | 需要直接访问当前文档 URL 或使用有效密钥进行在线测试。 |
| Kimi Code | 找到了 Kimi 第三方代理文档，仅包含 OpenAI 兼容配置 | unknown | 未找到 `/models` 响应结构。 |
| 302.AI | 官方文档包含 `Models（列出模型）GET` 页面 | likely OpenAI-compatible data[] | 存在专门的列出模型页面。获取到的文本中的响应体示例被截断了。 |
| Baseten | 官方文档说明了公共 OpenAI 兼容端点 `https://inference.baseten.co/v1` | supported endpoint, shape not shown | 未找到专门的 `/models` 响应。 |
| Cortecs | 仅有官方文档概览及 OpenCode 提供商条目 | catalog/static only | 未找到 `/models` 端点文档。 |
| DeepSeek | 官方 `GET /models` 文档展示了 `{ object, data[] }` | verified data[] | 解析器已覆盖。 |
| Comtegra | 官方文档列出了支持的 `/v1/models`，并链接到 OpenAI Models API | supported endpoint, shape OpenAI | 解析器已覆盖。 |
| FPT AI Marketplace | 官方文档展示了通过 LiteLLM/OpenAI 的 chat/completions，没有 models 端点 | unknown/no evidence | 实时 `/models` 可能失败。 |
| Firmware/FrogBot | 仅有 OpenCode 提供商文档 | catalog/static only | 未找到直接的提供商 API 文档。 |
| Hugging Face | 通用推理提供商文档，OpenAI 兼容 API | supported endpoint, shape not shown | 未验证专门的 `/models` 页面。 |
| Moonshot AI | 搜索/当前 URL 未暴露 `/models` 文档 | unknown | Kimi API 搜索提示了模型列表端点，但未获取到官方的 Moonshot 页面。 |
| Nebius | 快速入门文档中的 OpenAI 兼容端点 | supported endpoint, shape not shown | 未验证专门的 `/models` 页面。 |
| Scaleway | 找到了官方 “Using Models API” 文档 | supported endpoint, shape likely OpenAI | 如果是 OpenAI 结构，则解析器已覆盖。 |
| STACKIT | 官方集成文档说明 OpenAI 兼容 API，且模型选择器会获取 `/models` | supported endpoint, shape not shown | 如果是 OpenAI 结构，则已覆盖。 |
| Groq | API 参考中有 Models/List models | verified data[] | 已覆盖。 |
| Mistral | API 参考中有 Models/List Available Models | verified data[] style | 已覆盖。 |
| Perplexity | API 文档获取/搜索未找到 list-models 端点 | unknown | 可能不支持 `/models`；静态文档列出了模型。 |
| Together AI | 官方 `GET /models` 文档展示了顶级数组 | verified top-level array | 解析器已为此修复。 |
| DeepInfra | 官方 OpenAI 兼容文档指向静态模型目录，未找到 `/models` 页面 | catalog/static only | 实时 `/models` 未经验证。 |
| Fireworks | 找到了账户模型 API 的官方 list-models 文档 `{ models: [...] }`；同时存在 OpenAI 兼容端点 | verified models[] variant for account API | 解析器支持 `models[]` 和 `name`。实时基础端点结构仍未验证。 |
| MiniMax | 官方文本生成文档展示了 OpenAI 兼容基础及静态支持模型表格 | catalog/static only | 未找到 `/models` 端点。 |
| xAI | API 参考包含 Models 部分 | verified data[] likely | 已覆盖。 |
| LM Studio | 官方 OpenAI 兼容文档列出了 `GET /v1/models` | supported endpoint, shape not shown | 预期 OpenAI 本地服务器返回 data[]。 |
| Ollama | 官方 OpenAI 兼容博客/文档涵盖了 chat；在获取的页面中未找到 `/v1/models` 文档 | unknown | 需要原始文档/源码或本地在线测试。 |
| Chutes | 实时用户响应展示了 `{ object:"list", data:[...] }` 并包含数字定价 | verified data[] plus numeric pricing | 解析器已修复并移除了过时的默认值。 |
| Cerebras | 官方 `GET /v1/models` 文档展示了 `{ object, data[] }` | verified data[] | 已覆盖。 |
| Alibaba Coding Plan | 官方文档展示了 OpenAI 兼容基础 URL，但警告 Coding Plan 仅供编码工具使用；无 `/models` 文档 | unknown/no evidence | 可能需要静态默认值；实时 `/models` 可能失败。 |
| Generic openai-compatible | 用户提供的端点 | parser contract | 我们支持 `{data[]}`、顶级数组、`{models[]}`、id/name 标识符。 |

## `f291f0e` 之后的解析器覆盖范围

支持的响应形式：
- `{ "data": [{ "id": "..." }] }`
- 顶级 `[{ "id": "..." }]`
- `{ "models": [{ "id" or "name": "..." }] }`
- 数字或字符串定价字段
- 上下文字段：`context_length`、`contextLength`、`max_context_length`、`maxModelLength`、`max_model_len`、`trainingContextLength`

## 已识别的差距

目前尚未证明需要额外的解析器结构。剩余问题是提供商能力/配置文件的准确性：
- 部分提供商在 chat 方面兼容 OpenAI，但未记录实时的 `GET /models`。
- 对于这些提供商，实时目录刷新应保持“尽力而为”，并且必须优雅地回退到静态目录。
- 长期来看，`OpenAiCompatibleProfile` 可能应该携带一个 `model_catalog` 能力/策略，以便已知不支持 `/models` 的提供商不会发出嘈杂的刷新失败信息。