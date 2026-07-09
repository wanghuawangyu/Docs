# 客户端核心与表现层分离计划

**状态：** 已提议

本文档审计当前的 TUI/客户端栈，并提出一个安全的、增量式的分离方案，将可重用的 `client-core` 层与 ratatui/crossterm 表现层分开。目标是使当前的单面客户端更易于维护，同时为 `MULTI_SESSION_CLIENT_ARCHITECTURE.md` 中描述的多面方向扫清障碍。

另请参阅：[MULTI_SESSION_CLIENT_ARCHITECTURE.md](https://github.com/1jehuang/jcode/blob/master/docs/MULTI_SESSION_CLIENT_ARCHITECTURE.md)

## 执行摘要

如今，客户端栈在功能上是分离的，但在结构上并非如此：
- `src/tui/app.rs` 拥有一个非常大的 `App` 状态对象，其中混合了会话状态、传输状态、输入状态、瞬态 UI 状态和运行时句柄。
- `src/tui/app/*.rs` 就像一个分布式 reducer，但变更表示为直接的 `impl App` 方法，而不是类型化的 action 和 reducer 入口点。
- `src/tui/ui.rs` 和 `src/tui/ui_*.rs` 已经主要是表现层，但它们仍然依赖于一个非常宽的 `TuiState` trait 和一些进程全局的渲染缓存。
- `src/tui/workspace_client.rs` 是进程全局的可变状态，这是当前实现真正的客户端核心分离和多面客户端的最明确障碍。

最安全的计划是：
1. 先在现有 crate 内定义一个真正的 `client-core` 状态模型。
2. 将纯状态和 reducer 移到该边界之后，不改变行为。
3. 将 ratatui 渲染、覆盖层、markdown、mermaid 和渲染缓存保留在表现层。
4. 只有在边界清理干净后，才考虑将 `client-core` 移到自己的 crate 中。

## 当前栈审计

### 入口点和循环

当前运行时入口点：
- `src/cli/tui_launch.rs` - 启动终端运行时，构造 `tui::App`，恢复会话/启动提示，调用 `app.run(...)`
- `src/tui/app/run_shell.rs` - 本地循环：`App::run`，远程循环：`App::run_remote`，重放循环辅助函数
- `src/tui/app/local.rs` - 本地 tick 处理、终端事件处理、总线事件处理、完成 turn 记账
- `src/tui/app/remote.rs` - 远程 tick 和终端事件处理、重连和断开处理
- `src/tui/app/remote/reconnect.rs` - 连接/重连编排
- `src/tui/app/remote/input_dispatch.rs` - 远程发送/拆分提交路径
- `src/tui/app/remote/server_events.rs` - 今天的主要远程事件 reducer

渲染入口点：
- `src/tui/mod.rs` - `render_frame(frame, state)`
- `src/tui/ui.rs` - `draw(frame, app: &dyn TuiState)`，`draw_inner(...)`
- `src/tui/ui_prepare.rs`，`ui_viewport.rs`，`ui_messages.rs`，`ui_input.rs`，`ui_pinned.rs`，`ui_overlays.rs`，`ui_header.rs`，`ui_diagram_pane.rs` - 帧准备和渲染

### 当前状态根

主要根：
- `src/tui/app.rs` - `pub struct App`，`DisplayMessage`，`ProcessingStatus`，几个传输和待处理操作辅助结构体

`App` 当前混合了所有这些关注点。目标是将 `App` 分解为：
- 一个核心状态模型（`ClientCore`）
- 表现层特定的状态（`PresentationState`）
- 一个明确的 action/reducer 层