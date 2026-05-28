---
name: case-teardown-google-docs
description: "Use when 用户要求把增长案例、竞品案例、用户路径图、真实截图时序图、UI交互分析/GIF 或视频案例拆解输出到 Google Docs、谷歌文档、Google Drive、本地 DOCX 或 Word 文档。"
---

# 案例拆解 Google Docs / 本地 DOCX 版本

## 目标

把一个增长案例输出成一篇 Google Docs 或本地 DOCX 案例拆解文档。文档必须包含：

1. 固定结构的案例拆解正文。
2. `用户完整路径时序图`：真实截图 + 每一步操作备注的横向故事板图片。
3. `1. 用户路径` 和 `3. 玩法解析` 小节下方的对应截图/连续关键帧与图注。
4. 关键 UI 交互证据：弹窗、提示条、动画反馈、按钮状态变化等关键交互动作，用连续关键帧 PNG 或关键帧拼图作为正文证据，并在 `3. 玩法解析` 里写清楚交互目的。GIF 只能作为补充材料，不能用本地 GIF 路径代替正文图片。

这个版本只负责文档交付，目标可以是 Google Docs / Google Drive / 本地 DOCX / Word；不创建飞书文档，也不创建飞书画板。

写作要用大白话。直接证据和推断要分开。不能编数据、编截图、编来源。

## 先判断交付目标

这个版本有两条交付路径，拆解标准完全一致，差别只在最后写入哪里：

- 用户要求 Google Docs、谷歌文档、Google Drive 文档、在线文档：走 Google Docs connector 写入，最终给 Google Docs 链接。
- 用户要求本地 doc、本地 docx、Word 文档、本地文档：走本地 DOCX 生成，最终给 `.docx` 文件路径。

写入或更新 Google Docs 前，必须使用 `google-drive:google-docs` skill，并按任务读取对应引用：

- 新建普通 Google Doc：读 `reference-native-create-direct.md`。
- 用 connector 直接写正文：读 `reference-direct-request-composition.md`。
- 文档包含截图、路径图、图表或图片：读 `reference-figures-and-image-insertion.md`。
- 文档里要创建真实表格：读 `reference-table-formatting-deep-dive.md`。
- 如果用户要求高保真排版、复杂页面设计、PDF 级交付效果，再按 `google-drive:google-docs` 走 DOCX-first 导入路线。

生成本地 DOCX 前，优先使用 `documents:documents` skill、Documents 插件能力或本地 `python-docx` 生成真实 `.docx`。本地 DOCX 也必须使用真实标题、段落、表格、图片对象，不能只交付 Markdown。

不要用本地脚本、浏览器复制粘贴、光标操作或肉眼页面来假装完成 Google Docs 写入。Google Docs 是否完成，以 connector 写入和 connector 读回为准。本地 DOCX 是否完成，以真实 `.docx` 文件存在、可被读取、结构检查通过为准。

## 工作流程

1. 读取案例材料。
   - 用户给 Google Docs 链接时，用 Google Docs connector 读取目标文档。
   - 用户给本地 DOCX 或 Word 文档时，先读取本地文件内容和已有结构；最终输出仍按本版本的文档标准执行。
   - 用户给飞书文档时，可以先用飞书工具读取材料，但最终写入仍按 Google Docs 或本地 DOCX 目标执行。
   - 用户给视频时，先用 `ffprobe` 看视频信息，再用本版本 `scripts/extract_video_keyframes.py` 抽关键截图。
   - 用户给产品网址时，抓取可见页面，并记录查看日期。

2. 整理证据包。
   - 截图按用户真实路径排序。
   - 看到弹窗、toast、通知条、进度变化、红包动画、转盘动画、按钮变灰/高亮、分享面板等动态交互时，记录触发前、出现中、消失后这几个时刻。
   - 对影响用户决策的关键动态交互，先用 `scripts/build_interaction_keyframes.py` 从录屏里截出 3-6 张连续关键帧 PNG，并可合成一张关键帧拼图；GIF 只作为补充材料。Google Docs 或本地 DOCX 后续会转在线文档时，正文必须使用静态 PNG 关键帧，不要只插 GIF。
   - 没有直接证据支撑的判断，一律标 `[推断]`。
   - 所有数字都要写清来源、日期、口径。

3. 起草案例拆解文档。
   - 使用 `references/case-teardown-template.md` 的标题顺序。
   - 除非用户明确要求，不要改标题顺序。
   - 案例命名和文档标题必须用中文。品牌或产品官方英文名可以保留，但标题要配中文机制描述，例如“拼多多现金大转盘案例拆解”，不要只写 `PDD cash wheel`。
   - 每个部分都要讲清楚三件事：发生了什么、为什么有效、我们能复用什么。
   - `1. 用户路径` 和 `3. 玩法解析` 每个小节都要先写说明，再放对应截图/连续关键帧和图注。分析 UI 交互时，对应连续关键帧 PNG 或关键帧拼图必须贴在该小节下方，不能只放在总览图、附件或证据包里；GIF 可以补充，但不能替代正文图片。
   - `3. 玩法解析` 每个小节必须写“底层逻辑分析”，说明它利用了什么用户心理或行为机制，例如损失厌恶、收益放大、沉没成本、临门一脚、稀缺感、随机奖励、社交证明等。证据不足就标 `[推断]`。
   - `3. 玩法解析` 遇到动态 UI 时必须补“UI 交互分析”：写清触发条件、出现位置、视觉强调方式、用户下一步、业务目的、可能的打扰或风险。比如“今日提现峰值提醒”不是只贴图，还要说明它为什么在临门一脚金额附近弹出、怎么把用户注意力拉回“继续提现”。
   - 如果用户指定目标行业，例如 casino、电商、SaaS、游戏、金融等，`6. 如何复用` 和 `对我们 SaaS 产品的核心启发` 必须改成该行业能落地的产品方案。

4. 制作用户路径故事板。
   - 使用 `references/user-path-storyboard.md`。
   - 主方案是“真实截图 + 步骤备注”的横向故事板，不是抽象流程图。
   - 输出样式参考 `assets/user-path-storyboard-standard.png`。
   - 本版本必须输出分段高清故事板：每张最多 2 步，单个手机截图保留约 720px 宽。金额明细、规则说明、列表小字等关键截图要补 1 步 1 张图或正文原始单屏截图。完整总览图只能辅助看顺序，不能作为文档里的唯一用户流程图。
   - 用本版本脚本生成故事板：

```powershell
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\google-docs-version\scripts\build_user_path_storyboard.py" `
  --items "C:\path\storyboard-items.tsv" `
  --output "C:\path\user-path-storyboard.png"
```

5. 写入目标文档。
   - 目标是本地 DOCX 时，生成 `.docx` 文件，使用真实标题、段落、列表、表格、图片对象；不要把 Markdown 文件当成最终交付。
   - 本地 DOCX 里的截图、故事板、UI 交互关键帧要作为图片对象插入。若该 DOCX 可能导入 Google Docs、飞书或其他在线文档，正文必须插入静态 PNG 关键帧或关键帧拼图；不要只插 GIF，也不要在正文里写本地 GIF 路径。GIF 文件只能作为额外补充材料，不能算作完成交互证据。
   - 本地 DOCX 的表格要用真实 Word 表格，不要用纯文本对齐。
   - 目标是 Google Docs 时，用 Google Drive connector 创建 native Google Doc，再用 Docs connector `batchUpdate` 写正文。
   - 目标是 Google Docs 时，写正文使用真实 Docs 结构：标题、段落、列表、表格、图片对象；不要把 Markdown 当作最终完成状态。
   - 目标是 Google Docs 时，表格要用 Google Docs 真实表格，不要用纯文本对齐。
   - 目标是 Google Docs 时，截图和故事板图片只能通过 connector 支持的图片插入路径写入，或通过 DOCX-first 导入路线进入 Google Docs。
   - 目标是 Google Docs 时，不要把本地图片路径、data URL、Markdown `![...](C:\path\image.png)` 当作已经插入 Google Docs。
   - 更新已有 Google Doc 前，先读回目标文档，确认 document id、tabId、revisionId 和要写入的位置。不要大范围删除重建，除非用户明确批准。

6. 验证结果。
   - 目标是 Google Docs 时，重新读取 Google Doc，确认固定标题顺序存在。
   - 目标是本地 DOCX 时，重新读取 `.docx`，确认固定标题顺序、表格、图片数量和关键图注存在。
   - 确认案例标题和案例名称是中文。
   - 确认关键表格是真实表格，关键列表是真实列表。
   - 确认 `用户完整路径时序图` 下方有分段高清故事板图片对象；如果 connector 无法插入或读回图片，要说明真实限制，不能说已经完成图片写入。
   - 确认 `1. 用户路径` 和 `3. 玩法解析` 的小节下方有对应截图/连续关键帧或明确的未插入原因。
   - 确认关键 UI 交互已用静态 PNG 连续关键帧或关键帧拼图呈现；GIF 只能作为补充，不能把本地 GIF 路径当成交互证据。
   - 最终回复给目标文档链接或本地 `.docx` 文件路径；如果图片、表格或视觉排版无法完整验证，要说清楚哪一部分没法验证。

## 固定标题

必须按下面顺序输出：

1. `概述`
2. `研究边界与方法`
3. `用户完整路径时序图`
4. `1. 用户路径`
5. `2. 规则设计`
6. `3. 玩法解析`
7. `4. 增长内核与归因`
8. `5. SaaS 后台逻辑`
9. `6. 如何复用`
10. `7. 商业闭环`
11. `8. 不足分析`
12. `对我们 SaaS 产品的核心启发`

每个标题的作用、写法和检查点，见 `references/case-teardown-template.md`。

## 视频截图

案例材料包含录屏时，用下面脚本抽关键截图：

```powershell
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\google-docs-version\scripts\extract_video_keyframes.py" `
  "C:\path\case.mp4" `
  --out-dir "C:\path\frames" `
  --every 12 `
  --max-frames 18
```

已知关键时间点时，用下面方式指定：

```powershell
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\google-docs-version\scripts\extract_video_keyframes.py" `
  "C:\path\case.mp4" `
  --out-dir "C:\path\frames" `
  --times "00:00:03,00:00:18,00:00:42,00:01:20"
```

脚本会生成 `manifest.md`，把它当作截图清单。看完截图后，再补充每张图对应的路径步骤和说明。

## 关键交互证据

录屏里出现会影响用户决策的动态 UI 时，要把关键片段截成连续关键帧 PNG 或关键帧拼图，作为 `3. 玩法解析` 的正文证据。GIF 可以另外生成，但只能作为补充材料。常见对象包括：

- 弹窗、toast、顶部通知条、权限请求、规则提示。
- 红包、转盘、翻牌、进度条、金额跳动、积分变化。
- 按钮状态变化、任务完成反馈、分享面板、倒计时提醒。

优先用下面脚本从视频生成静态关键帧，并可给关键区域加红框：

```powershell
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\google-docs-version\scripts\build_interaction_keyframes.py" `
  "C:\path\case.mp4" `
  --start "00:01:20.000" `
  --duration 2.5 `
  --highlight "40,90,640,160" `
  --frames 4 `
  --make-strip `
  --output-dir "C:\path\interaction-reminder"
```

如果还需要补充 GIF，再用下面脚本生成动图：

```powershell
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\google-docs-version\scripts\build_interaction_gif.py" `
  "C:\path\case.mp4" `
  --start "00:01:20.000" `
  --duration 2.5 `
  --highlight "40,90,640,160" `
  --output "C:\path\interaction-reminder.gif"
```

`--highlight` 的格式是 `x,y,w,h`，坐标基于当前画面；如果先用了 `--crop`，就基于裁剪后的画面。Google Docs 或本地 DOCX 转在线文档时，正文只认静态 PNG 关键帧或关键帧拼图；不能只写本地 GIF 路径。

## 正文截图标准

Google Docs / 本地 DOCX 案例文档里有三类图，不能互相替代：

1. `用户完整路径时序图`：完整路径总览图，放在该标题下方。
2. `1. 用户路径` 小节截图/关键帧：每个用户路径小节下方放该步骤的真实截图；分析动态交互时，把对应连续关键帧 PNG 或关键帧拼图也放在这里。
3. `3. 玩法解析` 小节截图/关键帧：每个玩法解析小节下方放证明该玩法的真实截图；分析 UI 交互时，把对应连续关键帧 PNG 或关键帧拼图也放在这里。

`1. 用户路径` 和 `3. 玩法解析` 的标准结构都是：

```markdown
### 小节标题

文案说明：发生了什么、交互怎么引导、底层逻辑是什么。

玩法解析小节必须单独补充“底层逻辑分析”：这一步为什么能驱动用户继续，利用了损失厌恶、收益放大、沉没成本、临门一脚、稀缺感、随机奖励、社交证明等哪类机制。必须对应到截图里的文案、数字、按钮、进度、奖励或页面反馈；证据不足时标 `[推断]`。

UI 交互分析：如果这一步有动态交互，要写触发条件、出现位置、视觉强调、持续时间、用户下一步和业务目的；证据不足时标 `[推断]`。

[这里插入对应步骤截图]

[如果有关键交互，这里插入连续关键帧 PNG 或关键帧拼图；GIF 只能作为补充，不能只写路径]

图注：这张图证明了什么。
```

不能只在 `用户完整路径时序图` 放一张总图，然后正文不放截图。不能把所有小节截图集中放到文末。写了 UI 交互分析，就必须把对应连续关键帧 PNG 或关键帧拼图贴在该小节下方；不能只贴本地 GIF 路径。

## Google Docs / 本地 DOCX 规则

- 目标是 Google Docs 时，默认按 Google Drive / Google Docs connector 的当前授权身份操作。
- 目标是 Google Docs 时，必须先确认 document id 和链接。写错文档是严重错误。
- 目标是 Google Docs 时，新建普通文档优先走 native Google Doc，不要先生成本地 `.docx`，除非交付物明显需要复杂排版或 DOCX-first 导入。
- 目标是 Google Docs 时，写入正文必须用 Docs connector 的结构化请求，不要把请求数组转成字符串。
- 目标是 Google Docs 且文档有 tabs 时，必须带上正确 `tabId`。
- 目标是 Google Docs 且基于读回结果写入时，优先带 `requiredRevisionId`，避免覆盖协作者的新改动。
- 目标是 Google Docs 时，插入图片必须走 connector 支持的图片写入或 DOCX-first 导入。没有可验证图片对象时，只能说“正文文本已写入，图片插入未完成/未验证”，不能说完成。
- 更新已有 Google Docs 或本地 DOCX 时，禁止默认整篇覆盖、删除后半篇再重建、把图片占位符堆到文末。除非用户明确批准，并且已读回原文档结构。
- 用户明确要本地 DOCX / Word 时，不需要 Google Docs connector；生成并验证本地 `.docx` 后，最终回复给本地文件路径。
- 本地 DOCX 不要写 Google Docs 链接占位，不要说“已写入 Google Docs”。Google Docs connector 不可用时，也不要把本地 DOCX 说成在线文档。

## 质量要求

- 文档要像正式交付物，不要像素材笔记。
- 用户路径图必须用真实案例截图展示顺序，并配上每一步用户操作备注；只画抽象箭头不合格。
- `用户完整路径时序图` 必须包含真实截图故事板图片。长路径要用分段高清图，不能只放一张压缩总览图；如果图片写入失败，要明确说明卡在哪一步。
- 案例命名和文档标题必须用中文，不能用英文文件名或英文 slug 直接当交付标题。
- `1. 用户路径` 和 `3. 玩法解析` 每个小节下方必须配对应截图/连续关键帧和图注；没有截图或关键帧支撑的判断要标 `[推断]`。
- `3. 玩法解析` 不能只写心理机制；有弹窗、提示条、动画、按钮状态变化等动态 UI 时，必须补 UI 交互分析，并把连续关键帧 PNG 或关键帧拼图贴在对应小节下方。GIF 只能作为补充材料，不能替代正文图片。
- “如何复用”和“核心启发”必须落到产品模块，不能只写营销观察。
- 最终回复里要给出目标文档链接或本地 `.docx` 文件路径；如果没生成成功，要说明真实原因。
