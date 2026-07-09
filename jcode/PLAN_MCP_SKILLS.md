# 计划：动态技能与 MCP 支持

## 目标

- 无需重启即可热加载技能（Skills）
- MCP（模型上下文协议）服务器支持[reference:0]
- 运行时动态注册工具[reference:1]
- Agent 可自行添加/配置 MCP 服务器[reference:2]

## 当前状态

- 技能：启动时从 `~/.claude/skills/` 和 `./.claude/skills/` 加载[reference:3]
- 工具：在 `Registry::new()` 中硬编码[reference:4]
- 无 MCP 支持[reference:5]

## 实施计划

### 第一阶段：技能热加载

修改 `src/skill.rs`：
- 为 `SkillRegistry` 添加 `reload(&mut self)` 方法[reference:6]
- 技能可在不重启的情况下重新加载[reference:7]

新增工具 `reload_skills`：
- Agent 可触发 `reload_skills` 以加载新技能[reference:8]

### 第二阶段：动态工具注册

修改 `src/tool/mod.rs`：

```rust
impl Registry {
    /// 在运行时注册新工具
    pub async fn register(&self, tool: Arc<dyn Tool>);
    /// 按名称注销工具
    pub async fn unregister(&self, name: &str);
    /// 列出所有已注册的工具
    pub async fn list(&self) -> Vec<Arc<dyn Tool>>;
}
```

[reference:9]

### 第三阶段：MCP 客户端

新增模块 `src/mcp/mod.rs`：
- MCP 协议类型（JSON-RPC 2.0）[reference:10]
- 基于 stdio 的 MCP 客户端[reference:11]
- MCP 工具包装器（将 MCP 工具转换为我们的 Tool trait）[reference:12]

配置文件 `~/.claude/mcp.json`：

```json
{
  "servers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem", "/path"],
      "env": {}
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-github"],
      "env": {"GITHUB_TOKEN": "..."}
    }
  }
}
```

[reference:13]

MCP 管理器：
- 启动时加载配置[reference:14]
- 连接到已配置的服务器[reference:15]
- 将 MCP 工具转换为 jcode 的 Tool trait[reference:16]
- 处理服务器生命周期（启动、停止、重启）[reference:17]

### 第四阶段：Agent 自配置

新增工具：
- `mcp_list` — 列出已连接的 MCP 服务器[reference:18]
- `mcp_connect` — 启动新的 MCP 服务器[reference:19]
- `mcp_disconnect` — 停止 MCP 服务器[reference:20]
- `mcp_reload` — 重新加载所有 MCP 服务器[reference:21]

工作流程：
- Agent 调用 `mcp_connect {"name": "playwright", "command": "npx", "args": ["-y", "@anthropic/mcp-server-playwright"]}`[reference:22]
- jcode 启动进程，执行 MCP 握手[reference:23]
- 服务器的工具被添加到注册表中[reference:24]
- Agent 可立即使用新工具[reference:25]

## MCP 协议摘要

MCP 通过 stdio 使用 JSON-RPC 2.0：

**初始化：**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2024-11-05",
    "capabilities": {},
    "clientInfo": {
      "name": "jcode",
      "version": "0.1.0"
    }
  }
}
```

[reference:26]

**列出工具：**

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/list",
  "params": {}
}
```

[reference:27]

**调用工具：**

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "read_file",
    "arguments": {
      "path": "/tmp/test.txt"
    }
  }
}
```

[reference:28]

## 待创建/修改的文件

- `src/mcp/mod.rs` — MCP 模块[reference:29]
- `src/mcp/protocol.rs` — JSON-RPC 类型[reference:30]
- `src/mcp/client.rs` — MCP 客户端[reference:31]
- `src/mcp/manager.rs` — 多服务器管理器[reference:32]
- `src/mcp/tool.rs` — MCP 工具包装器[reference:33]
- `src/tool/mod.rs` — 添加动态注册功能[reference:34]
- `src/tool/mcp_tools.rs` — `mcp_connect`、`mcp_list` 等工具[reference:35]
- `src/skill.rs` — 添加 `reload()` 方法[reference:36]
- `src/tool/reload_skills.rs` — `reload_skills` 工具[reference:37]

## 实施顺序

1. 动态工具注册（前置条件）[reference:38]
2. 技能热加载（快速见效）[reference:39]
3. MCP 协议类型[reference:40]
4. MCP 客户端（单服务器）[reference:41]
5. MCP 管理器（多服务器）[reference:42]
6. Agent 自配置的 MCP 工具[reference:43]