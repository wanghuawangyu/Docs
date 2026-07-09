# 仓库指南

## 开发工作流

- **边开发边提交** —— 每完成一个功能或修复后，立即进行小范围、聚焦的提交。
- 如果 Git 状态不干净，或者有多个 Agent 同时在代码库中并行工作，请尽最大努力仍然提交你的工作。
- **完成时推送** —— 完成任务或会话后，将所有提交推送到远程。
- **默认使用快速迭代** —— 迭代过程中优先使用 `cargo check`、针对性测试和开发构建。
- **完成后重新构建** —— 完成所有更改后，构建源代码。
- **发布时升级版本** —— 发布时更新 `Cargo.toml` 中的版本号。发布新版本时，查看自上次发布以来的所有变更，确定版本号应如何升级（如补丁级或次要级等）。
- **支持远程构建** —— 使用 `scripts/remote_build.sh` 将繁重的 cargo 工作卸载到另一台机器。如果你的构建被终止，很可能是因为本机资源不足，这种情况下请使用远程构建。在运行构建之前，请先检查机器的资源可用性。

## 日志

- 日志写入 `~/.jcode/logs/`（按日生成文件，如 `jcode-YYYY-MM-DD.log`）。

## 调试 Socket

- 使用调试 socket 进行运行时级别的调试。

## 安装说明

- `~/.local/bin/jcode` 是从 `PATH` 中使用的启动器符号链接。
- `~/.jcode/builds/current/jcode` 是当前本地/源码构建通道；自我开发构建和 `scripts/install_release.sh` 将启动器指向此处。
- `~/.jcode/builds/stable/jcode` 是稳定发布通道；`scripts/install.sh` 安装此版本并将启动器指向此处。
- `~/.jcode/builds/versions/<version>/jcode` 存储不可变二进制文件。
- `~/.jcode/builds/canary/jcode` 仍然存在，用于金丝雀/测试流程，但不是主要的自我开发安装路径。
- 在 Windows 上，对应的路径为：
  - 启动器：`%LOCALAPPDATA%\jcode\bin\jcode.exe`
  - 稳定版：`%LOCALAPPDATA%\jcode\builds\stable\jcode.exe`
  - 不可变安装：`%LOCALAPPDATA%\jcode\builds\versions\<version>\jcode.exe`
  - `scripts/install.ps1` 当前安装的是稳定通道。
- 确保 `~/.local/bin` 在 `PATH` 中排在 `~/.cargo/bin` **之前**。
  
