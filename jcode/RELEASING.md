# 发布 jcode

jcode 有两条发布路径：一条用于快速修复的本地快速路径，以及一条用于完整发布的 CI 路径。

## 快速发布（本地，约 2.5 分钟）

用于热修复和紧急更新。在本地构建 Linux + macOS 二进制文件并直接上传。

```bash
scripts/quick-release.sh v0.5.5                 # 构建 + 打标签 + 发布
scripts/quick-release.sh v0.5.5 "Fix bug"       # 带自定义标题
scripts/quick-release.sh --dry-run v0.5.5       # 仅构建，不发布
```

### 工作原理

- 并行构建 Linux x86_64（本地）和 macOS aarch64（通过 osxcross）
- 验证两个二进制文件（ELF 和 Mach-O 校验）
- 创建 Git 标签并推送（这也会触发 CI 构建 Windows 二进制文件）
- 通过 `gh release create` 将两个二进制文件上传到 GitHub Release[reference:0]
- 用户可立即运行 `jcode update`[reference:1]

### 先决条件

已在开发笔记本（xps13）上配置好：
- osxcross 位于 `~/.osxcross`，使用 macOS 14.5 SDK（darwin triple: `aarch64-apple-darwin23.5`）[reference:2]
- rustup 已安装 `aarch64-apple-darwin` target[reference:3]
- `~/.cargo/config.toml` 已配置 osxcross 链接器[reference:4]
- gh CLI 已通过 GitHub 认证[reference:5]

### 时间线

| 阶段 | 耗时 |
|---|---|
| 0s | 启动并行构建（Linux 本地 + macOS 交叉编译）|
| ~90s | Linux 构建完成 |
| ~150s | macOS 构建完成 |
| ~153s | 二进制文件上传，发布上线 ✅ Linux + macOS 用户可 `jcode update` |
| ~16m | CI 完成 Windows 构建，上传到同一发布 ✅ Windows 用户可 `jcode update`[reference:6] |

## CI 发布（自动化，Linux+macOS 约 11 分钟，Windows 约 16 分钟）

当 `v*` 标签推送到 GitHub 时自动触发[reference:7]。

### 工作流：`.github/workflows/release.yml`

```
Tag 推送 (v*)
│
├─► build-linux-macos（并行）
│   ├─► Linux x86_64（ubuntu-latest）~8 min
│   └─► macOS aarch64（macos-latest）~11 min
│
├─► build-windows（并行，非阻塞）
│   ├─► Windows x86_64（windows-latest）~16 min
│   └─► Windows ARM64（windows-11-arm）~16 min
│
├─► release（在 Linux + macOS 完成后）
│   ├─► 创建包含二进制文件的 GitHub Release
│   ├─► 更新 Homebrew formula（1jehuang/homebrew-jcode）
│   └─► 更新 AUR 包（jcode-bin）
│
└─► upload-windows-assets（在 Windows + release 完成后）
    └─► 将 Windows 二进制文件上传到已有发布[reference:8]
```

### 关键设计决策

- **Windows 不阻塞发布**。Linux 和 macOS 二进制文件准备就绪后立即发布，Windows 稍后添加[reference:9]。
- **浅克隆**（`fetch-depth: 1`）以最小化检出时间[reference:10]。
- `CARGO_INCREMENTAL=0` 用于 CI（增量编译在干净的 CI 构建中会增加开销）[reference:11]。
- `sccache` + `rust-cache` 用于跨运行的依赖缓存[reference:12]。
- Linux 上使用 `mold` 链接器以加快链接速度[reference:13]。

### 包管理器更新

CI 自动处理 Homebrew 和 AUR 更新：
- **Homebrew**：使用新的 SHA256 哈希更新 `1jehuang/homebrew-jcode` 中的 `Formula/jcode.rb`[reference:14]
- **AUR**：更新 `jcode-bin` AUR 仓库中的 `PKGBUILD` 和 `.SRCINFO`[reference:15]

两者均由 Linux + macOS 构建完成后的 `release` job 触发[reference:16]。

## 如何选择

| 场景 | 方法 | Linux+macOS 耗时 | Windows 耗时 |
|---|---|---|---|
| 热修复 / 紧急 bug | `scripts/quick-release.sh` | ~2.5 min | ~16 min（CI）|
| 常规发布 | 推送 `v*` 标签 | ~11 min | ~16 min |
| 需要 Homebrew/AUR | 推送 `v*` 标签 | ~11 min | ~16 min[reference:17] |

对于需要同时更新 Homebrew/AUR 的快速发布，先使用脚本（快速发布二进制文件），然后 CI 的标签推送会自动处理包管理器更新[reference:18]。CI 的 `softprops/action-gh-release` 会更新脚本创建的已有发布[reference:19]。

## 交叉编译配置

macOS 二进制文件通过 [osxcross](https://github.com/tpoechtrager/osxcross) 从 Linux 交叉编译[reference:20]。

### 当前配置

| 组件 | 值 |
|---|---|
| SDK | macOS 14.5 SDK |
| SDK 来源 | [joseluisq/macosx-sdks](https://github.com/joseluisq/macosx-sdks)[reference:21] |
| 安装位置 | `~/.osxcross/`[reference:22] |
| Darwin triple | `aarch64-apple-darwin23.5`[reference:23] |
| 链接器 | `aarch64-apple-darwin23.5-clang`[reference:24] |

### Cargo 配置（`~/.cargo/config.toml`）

```toml
[target.aarch64-apple-darwin]
linker = "aarch64-apple-darwin23.5-clang"

[env]
CC_aarch64_apple_darwin = "aarch64-apple-darwin23.5-clang"
CXX_aarch64_apple_darwin = "aarch64-apple-darwin23.5-clang++"
```[reference:25]

### 从头重建 osxcross

```bash
git clone https://github.com/tpoechtrager/osxcross /tmp/osxcross
curl -L -o /tmp/osxcross/tarballs/MacOSX14.5.sdk.tar.xz \
  https://github.com/joseluisq/macosx-sdks/releases/download/14.5/MacOSX14.5.sdk.tar.xz
cd /tmp/osxcross && UNATTENDED=1 TARGET_DIR=~/.osxcross ./build.sh
rustup target add aarch64-apple-darwin
```[reference:26]

构建约需 5 分钟。需要 `clang`、`cmake`、`libxml2`（在 Arch 上均可通过 pacman 获取）[reference:27]。

### 为什么用 osxcross（而不是 zigbuild）

`cargo-zigbuild` 可以为 macOS 交叉编译纯 Rust 代码，但 jcode 依赖的 crate 需要链接 macOS 系统框架：
- `arboard`（剪贴板）— 链接 AppKit、Foundation[reference:28]
- `native-tls` / `security-framework` — 链接 Security、SystemConfiguration[reference:29]
- `objc2` — 链接 Objective-C 运行时[reference:30]

这些需要实际的 macOS SDK 头文件和框架存根，而 osxcross 提供了这些[reference:31]。

## 构建性能

### 当前耗时（笔记本，8 核 Intel Ultra 7 256V）

| 构建 | 干净构建 | 依赖缓存 |
|---|---|---|
| Linux x86_64（本地）| ~90s | ~90s |
| macOS aarch64（交叉）| ~3 min | ~2.5 min |
| 两者并行 | ~3 min | ~2.5 min[reference:32] |

瓶颈在于编译 jcode 本身（12 万行 Rust 代码）。依赖项已缓存，无需重新编译[reference:33]。

`build.rs` 的时间戳会导致主 crate 在每次构建时完全重新编译[reference:34]。

### 为什么不能更快

- `opt-level = 1`、`codegen-units = 256`、`incremental = true` 已在 `[profile.release]` 中设置[reference:35]
- 8 核是硬件限制[reference:36]
- 拆分为 workspace crates 可以实现部分重编译（小改动约 1 分钟）[reference:37]
- 局域网（非 Tailscale）上的 20+ 核机器可将构建时间缩短至约 40-50 秒[reference:38]