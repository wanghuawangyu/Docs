# 代码质量计划待办列表

此文件跟踪 `docs/CODE_QUALITY_10_10_PLAN.md` 中描述的代码质量提升计划的执行 backlog。

状态值：
- `pending` - 待处理
- `in_progress` - 进行中
- `blocked` - 被阻塞
- `done` - 已完成

## 阶段 0：防止进一步退化

- [ ] 为 `cargo check --all-targets --all-features` 添加 CI 任务
- [ ] 为 `cargo clippy --all-targets --all-features -- -D warnings` 添加 CI 任务
- [ ] 保持警告策略向下收紧
- [ ] 向贡献者指南添加文档化的文件大小和函数大小目标

## 阶段 1：警告和死代码清理

- [ ] 盘点所有 `#![allow(dead_code)]` 位置并证明其合理性或移除
- [ ] 从当前水平显著减少基线警告计数
- [ ] 移除 `setup_hints.rs` 中过时的未使用函数
- [ ] 移除 TUI 支持模块中过时的未使用代码
- [ ] 审计宽泛的抑制并替换为狭窄的局部允许

## 阶段 2：分解最大的文件

### 最高优先级

- [x] 按功能区域拆分 `tests/e2e/main.rs`
  - 2026-03-24 开始：提取功能模块 `session_flow`、`transport`、`provider_behavior`、`binary_integration`、`safety`、`ambient`
  - 2026-03-24 完成：提取共享辅助到 `tests/e2e/test_support/mod.rs`
  - 2026-05-18 验证：`tests/e2e/main.rs` 现在只是功能模块入口点，完整非忽略的 e2e 目标通过了 44/44 测试
- [ ] 继续将 `src/server.rs` 拆分为聚焦的子模块
  - 2026-03-24 进展：提取共享服务器/swarm 状态到 `src/server/state.rs`
  - 2026-03-24 进展：提取 socket/bootstrap 辅助到 `src/server/socket.rs`
  - 2026-03-24 进展：提取重载标记/信号状态到 `src/server/reload_state.rs`
  - 2026-03-24 进展：提取路径/更新/swarm 身份工具到 `src/server/util.rs`
- [ ] 将 `src/agent.rs` 拆分为编排、流、中断和工具执行模块

### 下一波

- [ ] 将 `src/provider/mod.rs` 拆分为 traits、定价、路由和共享 HTTP 辅助
- [ ] 将 `src/provider/openai.rs` 拆分为请求、流、工具和响应模块
- [ ] 将 `src/tui/ui.rs` 按渲染职责拆分
- [ ] 将 `src/tui/info_widget.rs` 按 widget/领域部分拆分

## 阶段 3：错误处理强化

- [ ] 分别计数生产 `unwrap`/`expect` 与测试专用
- [ ] 将容易的生产 `unwrap`/`expect` 热点替换为显式错误
- [ ] 为提供商流解析失败添加更好的错误上下文
- [ ] 为重载和 socket 生命周期失败添加更好的错误上下文

## 阶段 4：测试策略

- [ ] 按功能区域拆分 E2E 测试
- [ ] 为关键状态转换添加针对性测试
- [ ] 为重载、流式、工具执行和 swarm 协调添加故障模式覆盖
- [ ] 添加长期可靠性检查