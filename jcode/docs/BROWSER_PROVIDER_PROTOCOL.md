# 浏览器 Provider 协议

**状态：** 草案  
**受众：** jcode 核心、浏览器桥接作者、适配器作者

## 为什么存在此文档

jcode 应暴露一个统一的一流 `browser` 工具，同时兼容多种浏览器自动化后端：

- Firefox Agent Bridge
- Chrome Agent Bridge
- Chrome 远程调试 / CDP 适配器
- WebDriver / BiDi 适配器
- Safari 自动化适配器
- 其他第三方浏览器控制系统

本文档中的协议定义了 **jcode 与浏览器 provider 之间的标准化契约**。这**并非**要求每个桥接器都使用完全相同的原生命令语言。而是：

- jcode 定义了一个它可依赖的**核心语义层**
- provider 声明其支持的能力和命令
- provider 可暴露核心之外的** provider 特定命令**
- 适配器可将 provider 的原生模型转换为此协议

这样既保证了一致性，又为桥接特定的强大功能留出了空间。

## 设计目标

1. **jcode 中有一个统一的一流工具** — 模型应使用单一的 `browser` 工具
2. **多种 provider 实现** — Firefox、Chrome、Safari、Edge、WebDriver 及其他系统都应适用
3. **能力协商** — jcode 应了解每个 provider 能做什么和不能做什么
4. **可扩展性且不碎片化** — 需要标准核心，但 provider 必须有空间支持浏览器特定功能
5. **稳定的会话和元素引用** — 模型应能对页面进行快照，然后对返回的引用执行操作
6. **传输中立语义** — 无论 provider 是进程内、通过 stdio、通过 socket 还是通过其他适配器包装，语义协议都应相同

## 非目标

1. 标准化每一个低级浏览器原语
2. 强制所有 provider 支持深度 DOM、网络或 JS 内省
3. 要求所有 provider 附加到用户的现有浏览器配置文件
4. 将 provider 特定命令作为必需核心的一部分

## 术语

- **browser 工具**：面向用户/模型的 jcode 工具
- **provider**：满足此协议的后端实现
- **bridge**：外部浏览器集成，如 Firefox Agent Bridge
- **adapter**：将桥接器的原生 API 转换为此协议的胶水代码
- **browser session**：provider 为 jcode 会话提供的隔离会话或附加范围
- **page**：会话下的标签页、目标或浏览表面
- **element ref**：provider 颁发的用于可操作元素的不透明句柄

## 合规模型

Provider 不需要实现所有功能。

### 认证所需的核心功能

Provider 应支持以下标准化操作才能被视为 `certified`：

- `provider.describe`
- `provider.status`
- `session.ensure`
- `session.close`
- `page.open`
- `page.snapshot`
- `page.click`
- `page.type`
- `page.wait`
- `page.screenshot`

### 可选但推荐

- `page.go_back`
- `page.go_forward`
- `page.reload`
- `tab.list`
- `tab.activate`
- `tab.close`
- `page.eval`
- `page.press`
- `page.scroll`
- `page.select`
- `download.list`

### Provider 特定扩展

Provider 可暴露额外命令，例如：

- `firefox.install_extension`
- `chrome.attach_debug_target`
- `cdp.send`
- `webdriver.perform_actions`

这些是允许的，但它们不是必需核心的一部分。

## 传输模型

此协议定义**消息语义**，而非一种必需的线缆格式。支持的实现风格包括：

- jcode 内部的直接 Rust trait 调用
- stdio JSON 请求/响应
- 本地 socket RPC
- 包装的远程 API

对于外部进程集成，推荐的信封是类似 JSON-RPC 的格式：

```json
{
  "id": "req_123",
  "method": "page.click",
  "params": {
    "ref": "elem_456"
  }
}
```

响应：

```json
{
  "id": "req_123",
  "result": {
    "success": true
  },
  "error": null
}
```

## 快照格式

`page.snapshot` 应返回页面的可访问性树或 DOM 结构，包含可交互元素及其引用：

```json
{
  "url": "https://example.com",
  "title": "Example Domain",
  "interactables": [
    {
      "ref": "elem_1",
      "type": "button",
      "text": "Click Me",
      "selector": "#submit-btn"
    },
    {
      "ref": "elem_2",
      "type": "input",
      "placeholder": "Enter name",
      "selector": "#name-input"
    }
  ],
  "content": "Page content summary..."
}
```

## 错误处理

Provider 应返回结构化的错误信息：

```json
{
  "id": "req_123",
  "error": {
    "code": "ELEMENT_NOT_FOUND",
    "message": "Element with ref 'elem_456' not found"
  }
}
```

标准错误码：

- `SESSION_NOT_FOUND`
- `PAGE_NOT_FOUND`
- `ELEMENT_NOT_FOUND`
- `TIMEOUT`
- `PROVIDER_BUSY`
- `INVALID_ARGUMENT`
- `PERMISSION_DENIED`
- `UNSUPPORTED`

## 能力宣告

Provider 应在 `provider.describe` 中宣告其能力：

```json
{
  "name": "firefox-bridge",
  "version": "1.0.0",
  "capabilities": {
    "core": ["open", "snapshot", "click", "type", "wait", "screenshot"],
    "optional": ["eval", "scroll", "go_back", "go_forward", "reload"],
    "extensions": ["firefox.install_extension"]
  },
  "session_isolated": true,
  "headless_supported": true
}
```

## 与 jcode 工具的集成

jcode 的 `browser` 工具将把模型提示翻译为 provider 命令，并将结果反馈给模型。模型只需调用 `browser` 工具并提供自然语言描述，jcode 内部会根据当前 provider 的能力选择合适的命令。
