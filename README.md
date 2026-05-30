# case-teardown-standard

这是一套用于“案例拆解”的 Agent Skill，适合拆解增长案例、竞品玩法、用户路径、活动转化链路、UI 交互细节和视频录屏案例。

它的重点不是写一篇泛泛的观察笔记，而是按“高级用户增长产品经理”的视角，把真实截图、用户路径、玩法机制、UI 交互、增长归因、后台能力和复用方案整理成可交付文档。

## 1. 这套 SKILL 能做什么

### 支持的输入

- 视频录屏，例如 App 活动流程、H5 活动流程、游戏化任务流程。
- 产品截图，例如用户路径截图、弹窗截图、规则页截图、奖励反馈截图。
- 已有文档，例如本地 DOCX、Google Docs、飞书文档里的案例材料。
- 网页或产品页面材料，前提是 Agent 所在工具能打开、截图或读取页面。

### 支持的输出

- 飞书文档版本：见 `lark-version/SKILL.md`。
- 飞书画板路径图版本：见 `lark-version` 下的画板和路径图标准。
- Google Docs 版本：见 `google-docs-version/SKILL.md`。
- 本地 DOCX / Word 版本：同样走 `google-docs-version/SKILL.md` 的标准。

### 能拆解的内容

- 用户完整路径：用真实截图按顺序还原每一步。
- 玩法解析：解释奖励、门槛、任务、倒计时、抽奖、分享等设计为什么能推动用户继续走。
- UI 交互分析：分析弹窗、toast、顶部提示条、按钮变化、转盘动画、红包动画等交互的触发条件、位置、目的和风险。
- 增长内核与归因：拆出拉新、回流、留存、转化、分享传播背后的机制。
- SaaS 后台逻辑：反推需要哪些后台能力，例如用户分层、任务配置、奖励账户、风控、数据看板。
- 行业复用方案：把案例里的玩法拆成可复用的产品模块，而不是只抄页面。

## 2. 如何安装

### 推荐方式：Codex

Codex 最适合这套 Skill，因为它可以同时处理本地文件、视频抽帧、图片写入、本地 DOCX、Google Drive / Google Docs 插件、飞书 CLI 等工具链。

安装到 Codex 的本地 skills 目录：

```powershell
git clone https://github.com/hhu122392/case-teardown-standard.git "$env:USERPROFILE\.codex\skills\case-teardown-standard"
```

如果目录已经存在，更新即可：

```powershell
cd "$env:USERPROFILE\.codex\skills\case-teardown-standard"
git pull
```

安装后，Codex 会在可用技能里识别：

- `case-teardown-standard`
- `case-teardown-lark`
- `case-teardown-google-docs`

### Claude Code

Claude Code 的常见技能目录是：

```powershell
git clone https://github.com/hhu122392/case-teardown-standard.git "$env:USERPROFILE\.claude\skills\case-teardown-standard"
```

如果你的 Claude Code 使用的是别的 skills 目录，就把仓库复制到对应目录下，保持目录结构不变：

```text
case-teardown-standard/
  SKILL.md
  lark-version/
  google-docs-version/
  scripts/
  references/
  assets/
```

Claude Code 是否能完整执行，取决于它当前环境是否能读取图片、运行脚本、处理视频抽帧和写入目标文档。

### Cursor、Windsurf、Trae 等 IDE Agent

很多 IDE 工具不一定原生支持 Skill 自动发现。可以用两种方式：

1. 把本仓库克隆到项目目录或全局提示词目录。
2. 在 Agent 的自定义规则里写明：

```text
当我要求“案例拆解”“用户路径拆解”“UI 交互分析”“写入飞书/Google Docs/本地 DOCX”时，
先读取 case-teardown-standard/SKILL.md，
再按目标平台读取 lark-version/SKILL.md 或 google-docs-version/SKILL.md。
```

IDE Agent 必须能访问本地文件，并且最好能运行 PowerShell / bash 命令。否则视频抽帧、故事板生成、关键帧生成会受限。

## 3. 输出标准及案例

### 固定正文结构

所有版本默认按下面顺序输出：

1. 概述
2. 研究边界与方法
3. 用户完整路径时序图
4. 1. 用户路径
5. 2. 规则设计
6. 3. 玩法解析
7. 4. 增长内核与归因
8. 5. SaaS 后台逻辑
9. 6. 如何复用
10. 7. 商业闭环
11. 8. 不足分析
12. 对我们 SaaS 产品的核心启发

### 图片和视频证据标准

- 必须使用真实截图，不要只画抽象流程图。
- 用户路径图默认每张最多放 2 步，单个手机截图保留约 720px 宽，避免小字糊掉。
- 金额明细、规则说明、列表小字等关键页面，可以 1 步 1 图。
- `1. 用户路径` 和 `3. 玩法解析` 的每个小节下方，都要放对应截图或关键帧，不能只把图集中放到文末。
- 分析 UI 交互时，正文主证据必须是静态 PNG 连续关键帧或关键帧拼图。
- GIF 只能作为补充材料。不要在 DOCX、Google Docs、飞书文档正文里只写本地 GIF 路径。
- 本地 DOCX 如果后续会导入 Google Docs 或其他在线文档，更要用 PNG 关键帧做主证据，因为 GIF 经常会丢失或不可见。

### GIF / 录屏动效拆解标准

GIF、短视频和录屏片段统一按 `references/gif-animation-interaction-teardown.md` 执行。核心要求是先定证据边界，再抽连续关键帧，然后拆层级、时序、运动参数、状态机、增长目的和风险。

简单动效可以输出一段式还原提示词。复杂流程不要只给一段很长的提示词，必须把拆解文档和生产用提示词分开：

- 超过 10 秒的录屏或完整活动链路，先做宏观链路表，再拆每个关键微观动效。
- 长链路要补业务状态机，不只写 `idle -> triggered -> settled` 这种单弹窗状态。
- 面向 H5 / 原型 / 动画复刻时，默认给分轮提示词：先静态骨架，再前半段动效，再后半段动效。
- 生产用提示词要包含视觉基准图、硬约束、验收标准和返工短评，避免 AI 生成通用抽奖页。
- 面向开发交付时，还要补组件树、Props、API 数据结构、Motion Spec、埋点事件、异常状态和合规口径。
- 抽奖、现金、bonus、casino、充值、提现类案例，要检查假倒计时、虚假中奖名单、隐藏提现门槛、优惠券冒充现金到账等风险。

脚本路径不要写死某个人的本地目录。示例中的 `<case-teardown-standard skill root>`、`<google-docs-version skill root>`、`<lark-version skill root>` 都表示当前机器上的实际 skill 安装目录。

### 文案标准

- 案例命名、文档标题、小节里的案例名称都用中文。
- 直接证据和推断分开写，没有证据支撑的判断标 `[推断]`。
- 不编数据、不编截图、不编来源。
- 用大白话写清楚“发生了什么、为什么有效、我们能复用什么”。
- 不只写心理机制，还要落到页面里的按钮、文案、金额、进度、弹窗、提示条和用户下一步。

### 案例：拼多多“现金大转盘”

这套 Skill 可以把一段活动录屏拆成这样的交付内容：

- 用户路径：入口加载、25 元待提现、答题任务、金额跳到 44.5 元、进入转盘、沾福气卡、49.8 元峰值提醒、49.9 元后分享好友门槛、提现记录、活动规则。
- UI 交互分析：例如“今日提现峰值提醒”出现在接近 50 元门槛时，用顶部通知条制造紧迫感和社会证明，把用户注意力拉回“继续提现”。
- 玩法解析：先给大额心理账户，再用临门一脚、小额奖励强反馈、抽奖次数、分享门槛把用户继续留在路径里。
- SaaS 复用：可以沉淀为目标账户、任务链、奖励账户、交互触发器、分享助力、风控看板等模块。

## 4. 使用说明：如何调用这套 SKILL

### 自动路由

直接说 `case-teardown-standard` 即可，Skill 会按目标平台分流：

- 说“飞书”“Lark”“飞书画板”，走 `lark-version/SKILL.md`。
- 说“Google Docs”“谷歌文档”“Google Drive”，走 `google-docs-version/SKILL.md`。
- 说“本地 DOCX”“Word 文档”“本地文档”，也走 `google-docs-version/SKILL.md`，但最终输出本地 `.docx`。

### 常用调用方式

输出到飞书：

```text
使用 case-teardown-standard SKILL，拆解这个视频，输出到飞书文档，并生成用户路径图。
```

输出到 Google Docs：

```text
使用 case-teardown-standard SKILL，拆解这个案例，写入 Google Docs。
```

输出成本地 DOCX：

```text
使用 case-teardown-standard SKILL，拆解这个录屏，输出成本地 Word 文档。
```

只做用户路径和 UI 交互分析：

```text
使用 case-teardown-standard SKILL，只拆用户路径和 UI 交互分析。交互动效用连续关键帧，不要只放 GIF。
```

### 内置脚本

视频抽关键帧：

```powershell
$skillRoot = "<google-docs-version skill root>"
python (Join-Path $skillRoot "scripts\extract_video_keyframes.py") `
  "C:\path\case.mp4" `
  --out-dir "C:\path\frames" `
  --every 12 `
  --max-frames 18
```

生成用户路径故事板：

```powershell
$skillRoot = "<google-docs-version skill root>"
python (Join-Path $skillRoot "scripts\build_user_path_storyboard.py") `
  --items "C:\path\storyboard-items.tsv" `
  --output "C:\path\user-path-storyboard.png"
```

生成 UI 交互连续关键帧：

```powershell
$skillRoot = "<google-docs-version skill root>"
python (Join-Path $skillRoot "scripts\build_interaction_keyframes.py") `
  "C:\path\case.mp4" `
  --start "00:01:20.000" `
  --duration 2.5 `
  --highlight "40,90,640,160" `
  --frames 4 `
  --make-strip `
  --output-dir "C:\path\interaction-reminder"
```

可选生成 GIF：

```powershell
$skillRoot = "<google-docs-version skill root>"
python (Join-Path $skillRoot "scripts\build_interaction_gif.py") `
  "C:\path\case.mp4" `
  --start "00:01:20.000" `
  --duration 2.5 `
  --highlight "40,90,640,160" `
  --output "C:\path\interaction-reminder.gif"
```

注意：GIF 只是补充，不是正文主证据。正文主证据用 PNG 关键帧。

## 5. 模型和工具要求

使用这套 Skill 的内置模型必须支持多模态，至少要能读取图片。处理视频案例时，还需要能通过工具抽帧、查看关键帧，或直接理解视频内容。

建议优先基于 Codex 使用，原因很直接：

- 能读取本地视频、图片、DOCX 等文件。
- 能运行 `ffmpeg`、Python 脚本和本地校验命令。
- 能生成本地 DOCX，并检查文档结构。
- 能配合 Google Drive / Google Docs 插件写入在线文档。
- 能配合飞书 CLI 或飞书相关 Skill 输出飞书文档和画板。

基础工具建议：

- Python 3
- ffmpeg
- Git
- 目标平台连接能力：Google Drive / Google Docs 插件，或飞书 CLI
- 一个支持图片/视频理解的多模态模型

如果模型不能看图，只能读文字，它不适合直接使用这套 Skill。最多只能根据人工整理好的截图说明写文字，不能独立完成高质量案例拆解。
