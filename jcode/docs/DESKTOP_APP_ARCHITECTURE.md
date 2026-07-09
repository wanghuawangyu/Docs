# Jcode 桌面应用架构方向

**状态：** 已提议  
**更新日期：** 2026-04-25

本文档记录了 Jcode 桌面应用在以下约束下的初始方向：
- 不使用 Electron/Tauri/Web 应用外壳
- 不使用通用 UI 框架
- 极高性能
- 低空闲资源占用
- 高度定制化的产品 UI
- 主要开发机器可能为 Linux
- 大多数早期用户预计为 macOS

目标是让桌面客户端成为 Jcode 的一流交互界面，同时不分支 Jcode 运行时，也不将应用变成重量级 IDE 的克隆品。

另请参阅：

## 执行摘要

将 Jcode Desktop 构建为一个轻量级 Rust 桌面客户端，带有自定义 GPU 渲染 UI。应用应连接到本地 Jcode 服务器/守护进程，后者拥有会话、工具、代理执行、持久化和权限。前端应优化为渲染/输入界面：

- Linux 应成为一流的开发平台。
- macOS 应成为一流的产品/分发平台。
- UI 不应依赖 Linux 专属的桌面概念。
- UI 不应是 Web 视图。
- UI 不应直接嵌入代理运行时。
- 渲染应为按需、虚拟化，并从第一天起可度量。

推荐的初始技术栈：

| 领域 | 决策 |
|---|---|
| 前端语言 | Rust |
| 后端/运行时 | 现有的 Rust Jcode 服务器/会话运行时 |
| 进程模型 | 桌面前端 + 本地 Jcode 守护进程/服务器 |
| 窗口/输入层 | 薄平台层，初期可能使用 winit |
| 渲染 | wgpu 配合自定义 2D 渲染器 |
| UI 架构 | 带脏标记追踪的保留 UI 树 |
| 布局 | 小型自定义布局系统，非 CSS/DOM |
| 文本 | 专用文本布局/光栅缓存，初期可能使用 cosmic-text/swash，后期可切换平台后端 |
| 协议 | 带版本号的类型化本地事件协议 |
| 持久化 | 服务器拥有的会话/事件持久化 |
| 产品定位 | 代理操作控制台 / 任务指挥中心 |

## 产品定位

Jcode Desktop 不应一开始就做成完整的 IDE，也不应看起来像传统的聊天机器人。差异化的产品是一个键盘驱动、类似 Niri 的代理工作区超级应用，专为本地开发设计。[reference:0]

一等对象不是聊天窗口，而是一个包含多个可导航界面的工作区：
- 代理会话
- 活动/任务视图
- 差异对比和已更改文件
- 文件/diff/工具界面
- 可选的未来扩展界面
- 设置/调试/工具界面[reference:1]

应用应帮助用户：
- 监督自主编码工作
- 检查工具活动
- 管理后台任务
- 审查已更改文件
- 响应权限提示
- 恢复和协调会话
- 在空间上导航多个相关界面[reference:2]

桌面客户端应补充 TUI/CLI，而非取代它们。[reference:3]

## 平台策略

### 开发主机：Linux

Linux 应支持最快的内部循环：
- 本地启动桌面客户端
- 运行渲染器压力测试
- 运行协议集成测试
- 基准测试内存/帧率/布局/文本性能
- 无需 Mac 即可调试 UI 引擎[reference:4]

Linux 构建应是真实的，而非模拟器。它应通过相同的 UI 引擎渲染，并执行与 macOS 相同的协议/视图模型路径。[reference:5]

### 产品目标：macOS 优先

大多数早期用户预计使用 macOS，因此即使日常开发在 Linux 上进行，macOS 的精致度也应成为产品需求。不应推迟太久的 Mac 特定工作：
- `.app` 应用捆绑包
- 应用图标和菜单栏集成
- Command 键快捷键
- 系统浅色/深色外观
- Retina 渲染正确性
- 触控板滚动质量
- 原生剪贴板行为
- 文件/打开方式集成
- 代码签名和公证路径
- 在 Mission Control、Spaces 和全屏窗口下的良好行为[reference:6]

### 避免 Linux 形态的产品假设

由于开发者可能使用 Linux，架构应明确避免固化仅在 Linux 窗口管理器下工作良好的假设。不要将这些作为硬依赖：
- Niri 风格的外部空间窗口管理
- X11 特定 API
- Wayland 专属行为
- 终端优先的会话工作流
- Linux 通知语义
- 在 macOS 上不可用或不友好的全局快捷键[reference:7]

现有的 Linux/Niri 工作流应保持优秀，但桌面产品质量应主要根据 macOS 的期望来评判。[reference:8]

## 进程架构

使用分离进程架构：

**Jcode Desktop 前端**
- 窗口/输入
- 自定义渲染
- 本地视图模型
- 瞬态 UI 状态
- 界面本地状态
- 协议客户端[reference:9]

**Jcode 服务器/守护进程**
- 会话
- 代理运行时
- 工具运行时
- 后台任务
- 持久化
- 权限
- 模型/提供商配置[reference:10]

服务器是以下内容的权威来源：
- 规范的会话历史
- 流式事件
- 工具执行
- 文件编辑
- 后台任务
- 权限状态
- 持久化配置[reference:11]

桌面前端仅拥有界面本地状态：
- 选中的会话/界面
- 草稿输入
- 光标和文本选择
- 滚动偏移
- 面板尺寸
- 焦点面板
- 本地命令面板状态
- 渲染缓存[reference:12]

这与多会话模型一致，即服务器拥有的会话可以随时间被不同客户端或界面显示。[reference:13]

## 本地协议方向

桌面应用应消费一个带版本号、类型化的事件流，而非定期获取完整的会话快照。[reference:14]

早期协议属性：
- 本地优先传输
- 显式协议版本
- 能力协商
- 仅追加的会话事件
- 助手/工具输出的流式增量
- 按事件游标可恢复的订阅
- 高容量工具输出的紧凑事件
- 服务器拥有的权限请求[reference:15]

可能的传输方式：
- 现有的 Jcode 服务器通道（如果与桌面需求兼容）
- Linux/macOS 上的 Unix 域套接字，Windows 上的命名管道
- 用于早期原型和测试工具的 Stdio JSON 协议[reference:16]

避免将 localhost HTTP 作为默认传输，除非有充分理由。它比用户拥有的套接字/管道产生更大的本地安全攻击面。[reference:17]

示例事件族：
- `session.created`
- `session.updated`
- `surface.attached`
- `message.created`
- `message.delta`
- `message.completed`
- `tool.started`
- `tool.output.delta`
- `tool.completed`
- `task.started`
- `task.progress`
- `task.completed`
- `workspace.changed`
- `git.changed`
- `permission.requested`
- `permission.resolved`
- `error`[reference:18]

## 渲染架构

使用自定义渲染器，而非原生控件层级或 Web 视图。[reference:19]

推荐层次：
> 平台窗口/输入 → 输入归一化 → 应用状态/视图模型 → 保留 UI 树 → 布局 → 文本布局/缓存 → 显示列表 → GPU 渲染器[reference:20]

核心规则：
- 空闲时无持续渲染循环
- 仅在输入、数据事件、动画或显式失效时渲染
- 虚拟化所有无界列表
- 将布局成本与绘制成本分离
- 按内容/字体/宽度缓存已 shaping 的文本
- 使用稳定 ID 进行脏标记追踪
- 在应用内显示调试/性能计数器[reference:21]

渲染器初期应支持：
- 矩形
- 圆角矩形
- 边框
- 纯色填充
- 裁剪
- 滚动容器
- 文本运行
- 等宽块
- 简单图标或类矢量图元
- 后续支持图像[reference:22]

推迟实现：
- 模糊效果
- 复杂阴影
- 动画框架
- SVG 重度渲染
- 完整 Markdown 渲染器
- 完整终端模拟器
- 嵌入式代码编辑器[reference:23]

## UI 架构

使用带即时风格构建器 ergonomics 的保留 UI 树。[reference:24]

理由：
- 转录本是长寿命且增量流式的
- 工具输出可能很大
- 面板需要稳定的焦点/选择状态
- 脏标记追踪对资源使用很重要
- 可访问性最终需要稳定的语义节点
- 多会话界面需要稳定身份[reference:25]

模型不应模仿 DOM/CSS 栈。一个小型产品特定的布局系统就足够了：
- row
- column
- stack
- 拆分面板
- 固定尺寸
- flex 填充
- 滚动容器
- 虚拟列表
- 覆盖层/模态框
- 内在文本测量[reference:26]

## 文本策略

文本是此项目中最困难的部分之一，应作为核心系统而非细节对待。[reference:27]

桌面客户端需要：
- Unicode shaping
- 字体回退
- 等宽代码/工具输出
- 换行
- 增量追加布局
- 选择/复制
- 输入光标行为
- 命令面板文本输入
- 类 Markdown 的转录本样式
- 最终支持类 ANSI 的工具输出样式[reference:28]

初期建议：
- 如果依赖审查可接受，使用 Rust 文本栈如 `cosmic-text`/`swash`
- 维护 GPU 字形图集
- 按稳定块 ID 和可用宽度缓存已 shaping 的行/运行
- 特化流式追加路径，使新输出不会重新布局整个转录本[reference:29]

Mac 特定文本质量应尽早评估。如果 Rust 文本渲染在 macOS 上不够好，考虑为 macOS 使用平台后端文本，同时保留相同的高层文本布局 API。[reference:30]

## 性能和资源预算

初期预算应在 Linux 开发机和代表性的 macOS 硬件上同时测量。[reference:31]

| 指标 | MVP 目标 | 长期目标 |
|---|---|---|
| 冷启动到可见窗口 | < 500 ms | < 150 ms |
| 前端空闲 CPU | ~0% | ~0% |
| 前端空闲 RSS | < 100 MiB | < 50 MiB |
| 输入到绘制延迟 | < 32 ms | < 16 ms |
| 滚动 | 60 fps | 支持 120 fps |
| 假转录本压力测试 | 10 万块可用 | 10 万块流畅 |
| 追加时完整转录本重新布局 | 禁止 | 禁止 |
| 无界保留可见节点 | 禁止 | 禁止 |
| 空闲时渲染器帧 | 禁止 | 禁止 |

[reference:32]

所需的早期 instrumentation：
- 帧时间
- 布局时间
- 文本 shaping 时间
- 显示列表构建时间
- GPU 提交时间
- 可见节点数
- 总保留节点数
- 字形图集大小
- 文本缓存大小
- 协议事件积压
- 守护进程往返延迟
- 前端 RSS（如可用）[reference:33]

在认为真实 Jcode 集成完成之前，原型中应存在调试 HUD。示例 HUD：
> frame 1.8ms | layout 0.3ms | text 0.6ms | gpu 0.4ms nodes 812 | visible 47 | glyph atlas 12.4 MiB | events 0 | daemon 2ms[reference:34]

## MVP 范围

第一个 UI 里程碑应在证明每个产品工作流之前先证明引擎。[reference:35]

### 里程碑 1：带假数据的自定义外壳

成功标准：
- 从 Linux 启动原生桌面窗口
- 通过自定义 GPU 管线渲染
- 显示会话侧边栏、转录本、编辑器组合框和活动面板
- 处理鼠标、键盘、焦点和滚动
- 渲染假流式转录本数据
- 虚拟化 10 万块转录本
- 空闲时 CPU 接近零
- 显示性能/调试 HUD
- 在可行的情况下有截图或黄金状态测试[reference:36]

### 里程碑 2：协议连接

成功标准：
- 连接到本地 Jcode 服务器/守护进程
- 列出会话
- 附加到会话/界面
- 订阅事件流
- 发送用户提示
- 将助手/工具事件流式传输到转录本中
- 可以停止/取消正在运行的任务
- 能从守护进程重启或断开连接中优雅恢复，至少满足开发使用[reference:37]

### 里程碑 3：有用的代理控制台

成功标准：
- 后台任务/工具调用的活动中心
- 权限请求覆盖层
- 工作区/Git 状态面板
- 已更改文件列表
- 打开外部编辑器/diff 操作
- 会话搜索/过滤
- macOS 应用捆绑包原型

## Crate 布局提案

不要将整个桌面应用放在根 crate 中。建议的结构：
```text
crates/
  jcode-desktop-protocol/   # shared protocol/event types if not already covered by server types
  jcode-desktop-ui/         # UI tree, layout, text/cache abstractions, renderer-agnostic pieces
  jcode-desktop-renderer/   # wgpu renderer and GPU resources
  jcode-desktop/            # app shell, platform window, protocol client, product UI
```

如果编译时间成为问题，保持协议/UI crate 轻量，并将 GPU/窗口依赖关在最终应用 crate 后面。[reference:40]

## 依赖策略

“无框架”并不意味着“无库”。它应意味着无重量级应用框架和无 Web 外壳产品架构。[reference:41]

可能可接受的依赖：
- `wgpu` 用于渲染抽象
- 一个非常薄的窗口/输入层，如 `winit` 用于引导
- `cosmic-text`/`swash` 或等效库用于文本 shaping/光栅化
- 小型序列化/协议 crate，与 Jcode 保持一致[reference:42]

避免：
- Electron
- Tauri
- Qt
- Flutter
- GTK 作为应用框架
- WebView UI 外壳
- React/Vue/Svelte 风格 UI 栈
- 基于 CSS/DOM 的架构[reference:43]

如果 `winit` 在 macOS 精致度上存在限制，平台层可以增加直接的 AppKit 支持，同时保留渲染器和 UI 模型。

## macOS 验证检查清单

由于 macOS 是主要用户目标，即使开发在 Linux 上进行，也应尽早验证以下内容：
- Retina 缩放因子正确性
- 触控板惯性滚动
- 与原生应用相比的文本清晰度
- 键盘快捷键适当地使用 Command 而非 Control
- 系统深色/浅色模式跟随用户偏好
- 窗口调整大小和全屏行为感觉原生
- 应用菜单和关闭/最小化/退出语义正确
- 剪贴板往返对代码和转录本足够丰富
- 本地套接字权限安全
- 应用捆绑包能可靠启动/找到守护进程[reference:45]

## 待定决策

这些应在实现进入假数据原型阶段之前解决：
- 初期使用 `winit` 还是从头开始编写直接平台外壳？
- 使用 `wgpu` 还是直接 Metal 优先渲染？
- 使用 `cosmic-text`/`swash` 还是平台文本 API？
- 复用现有 Jcode 服务器协议还是引入桌面特定事件协议 crate？
- 首个桌面二进制文件是否支持多界面模式，还是仅支持一个活动界面？
- 最低支持的 macOS 版本是多少？
- 首个分发路径是什么：本地 `.app`、Homebrew cask，还是签名/公证的 DMG？[reference:46]

## 推荐的下一步

创建一个使用假数据的桌面原型，在 Linux 上运行，但测量最终 macOS 产品所需的精确性能特征。原型不应等待完美的守护进程 API。它应首先验证昂贵的 UI 系统：
- 窗口创建
- 渲染器启动
- 保留树
- 布局
- 文本缓存
- 虚拟化转录本
- 按需重绘
- 调试 HUD

只有在完成这些之后，才应连接真实的 Jcode 事件流。