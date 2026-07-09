# 编译性能计划

本文档跟踪使 jcode 的 self-dev / 重构循环更快而不牺牲完整功能构建的计划。

另请参阅：[COMPILE_TIME_ISOLATION_REFACTOR.md](https://github.com/1jehuang/jcode/blob/master/docs/COMPILE_TIME_ISOLATION_REFACTOR.md)

## 目标

- 保持完整功能构建可用于正常使用和 self-dev 重载。
- 使常见的 self-dev 编辑编译成本显著降低。
- 减少定制需要重新编译的频率。
- 在每个阶段后测量改进，并停止没有回报的变动。

## 当前基线（2026-03-24）

在当前树上本地测量：
- 热 `cargo check --quiet`：~8.5s
- 热 `scripts/dev_cargo.sh build --release -p jcode --bin jcode --quiet`：~47.3s

本次审计的额外观察：
- 之前一次较热的 `cargo check` 运行约 ~12.3s。
- 一次不太热的 `cargo check --timings` 运行约 ~23.8s。
- 之前本地默认的 `clang + mold` 设置在此机器上的 release 链接期间失败。
- `clang + lld` 在此成功链接 release jcode 二进制文件。

## 近期目标

对于不触及广泛共享接口的常见 self-dev 编辑：
- 热 `cargo check`：< 5s
- 热 `cargo build` / 重载导向构建：< 20–30s

对于共享/核心编辑，即使它们无法达到相同的快速路径，我们仍应努力显著低于今天的基线。

## 最重要的事项（排名）

1. **工作区 / crate 边界** - Rust 在 crate 边界处缓存最佳。未触及的重子系统应在完整构建中保持编译和可重用。
2. **良好的边界设计** - 高变动逻辑不应存在于广泛扇出的 crate 或不稳定的共享类型中。
3. **sccache** - 对重复本地构建和 CI 有实际收益。
4. **快速、可靠的链接器配置** - 对 `cargo build` 和 release/self-dev 重载构建尤其重要。
5. **重子系统隔离** - 嵌入、提供商实现和大型 TUI/渲染代码应停止搅动无关的构建。
6. **内循环的更窄构建目标** - 避免在不需要时重建额外的 bin/目标。
7. **减少完全重新编译的需求** - Issue #32 的定制记录和扩展点应使许多变更变为配置/钩子/技能/数据驱动，而非源码驱动。

## 执行计划

### 阶段 1 — 战术性构建速度提升

- 保持 `.cargo/config.toml` 对本地贡献者保守。
- 使用 `scripts/dev_cargo.sh` 进行本地 self-dev 构建：
  - 如果安装了 sccache 则自动启用
  - 在 Linux x86_64 上优先使用 `clang + lld`
  - 为 jcode self-dev 构建/重载路径使用专用的 Cargo `selfdev` profile
  - 可通过 `JCODE_FAST_LINKER=mold` 选择使用 `mold`
- 通过该包装器路由重构阴影构建。

### 阶段 2 — 测量和可重复性

标准 self-dev 检查点现在位于 `scripts/bench_selfdev_checkpoints.sh` 之后，运行：
- 冷 `cargo check`
- 热触及文件 `cargo check`
- 冷 self-dev `jcode` 构建
- 热触及文件 self-dev `jcode` 构建

在捕获可比较的重构前后数字时使用它。
- 为冷/热 `check` 和构建计时添加文档化命令。
- 在判断 ROI 时，优先使用触及文件计时（例如 `scripts/bench_compile.sh check --touch src/server.rs`）而不是无操作热缓存重新运行。
- 在每个结构阶段后跟踪计时增量。
- 在将任何计时数据视为权威之前修复构建/链接阻塞器。
- 2026-03-25：升级 `scripts/bench_compile.sh` 以支持重复运行、摘要统计、JSON 输出和额外的 cargo 参数。