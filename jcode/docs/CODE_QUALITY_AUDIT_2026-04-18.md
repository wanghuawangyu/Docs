# 代码质量审计 - 2026-04-18

本报告盘点代码库中可通过静态扫描和针对性结构启发式检测到的代码质量问题。它旨在作为一个全面的 backlog 种子，而不仅仅是一个短名单。

## 范围和方法

- 扫描了 `target`、`.git` 和 `node_modules` 之外的所有 Rust 文件
- 按 LOC 测量文件大小
- 通过括号平衡的 `fn` 块近似函数大小
- 通过路径基础的测试分类计数 panic 倾向的宏和方法
- 盘点 `allow(...)` 抑制和 `TODO`/`FIXME`/`HACK`/`XXX` 标记
- 注意：基于路径的生产与测试分类是近似的，可能高估嵌入在生产文件中的测试专用代码

## 当前优点

- `cargo clippy --all-targets --all-features -- -D warnings` 干净通过
- Rust 源中不再有 `#[allow(dead_code)]` 抑制
- 格式化当前是干净的

## 代码库指标

- 扫描的 Rust 文件：455
- `src/` Rust 文件：429，总计 277,014 LOC
- `tests/` Rust 文件：11，总计 4,802 LOC
- `crates/` Rust 文件：14，总计 5,335 LOC
- 超过 1200 LOC 的生产文件：50
- 在 801 到 1200 LOC 之间的生产文件：62
- 超过 100 LOC 的近似生产函数：304，分布在 165 个文件中

## unwrap / expect 按生产与测试文件拆分

使用改进的基于路径的分类：

| 范围 | unwrap / expect 出现次数 |
|---|---|
| 生产文件 | 1258 |
| 测试专用文件 | 1334 |

### 最高计数的生产文件

| 计数 | 文件 |
|---|---|
| 136 | `src/tool/communicate.rs` |
| 62 | `src/build.rs` |
| 52 | `src/auth/cursor.rs` |
| 46 | `src/auth/codex.rs` |
| 42 | `src/provider/openai.rs` |
| 37 | `src/auth/claude.rs` |
| 30 | `src/cli/dispatch.rs` |
| 28 | `src/tool/bash.rs` |
| 26 | `src/storage.rs` |
| 25 | `src/auth/gemini.rs` |
| 25 | `src/tool/read.rs` |
| 25 | `src/tui/session_picker/loading.rs` |
| 24 | `src/side_panel.rs` |
| 24 | `src/cli/args.rs` |
| 24 | `src/server/comm_control.rs` |

### 最高计数的测试专用文件

| 计数 | 文件 |
|---|---|
| 788 | `src/tui/app/tests.rs` |
| 98 | `src/tool/selfdev/tests.rs` |
| 59 | `src/memory_tests.rs` |
| 44 | `src/import_tests.rs` |
| 26 | `src/provider/tests.rs` |
| 26 | `src/tool/agentgrep_tests.rs` |
| 24 | `src/tui/mermaid_tests.rs` |
| 24 | `src/server/socket_tests.rs` |
| 21 | `src/tui/markdown_tests/cases.rs` |
| 20 | `src/provider/openrouter_tests.rs` |
| 18 | `src/tui/ui_pinned_tests.rs` |
| 17 | `src/cli/provider_init_tests.rs` |
| 15 | `src/agent_tests.rs` |
| 12 | ... |