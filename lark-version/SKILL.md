---
name: case-teardown-lark
description: "Use when 用户要求把增长案例、竞品案例、用户路径图、真实截图时序图、UI交互分析/GIF 或视频案例拆解输出到飞书文档、Lark 文档或飞书画板。"
---

# 案例拆解 Lark / 飞书版本

## 目标

把一个增长案例输出成两份交付物：

1. 一篇结构固定的飞书案例拆解文档。
2. 一个展示完整用户路径的飞书画板，也就是“用户完整路径时序图”。这个图必须优先使用真实案例截图加备注，做成横向路径故事板。
3. 关键 UI 交互证据：弹窗、提示条、动画反馈、按钮状态变化等关键交互动作用连续关键帧 PNG 或关键帧拼图证明，并在 `3. 玩法解析` 里写清楚交互目的。GIF 只能作为补充材料，不能用本地 GIF 路径代替正文图片。
4. 用户要求拆 GIF 动效实现、交互动画还原、或输出可喂给 AI 的一比一提示词时，必须按 `../references/gif-animation-interaction-teardown.md` 做证据边界、抽帧、层级、时序、运动参数、状态机和提示词。

写作要用大白话。直接证据和推断要分开。不能编数据、编截图、编来源。

## 角色要求

拆解时要带入“高级用户增长产品经理”的视角，不是写观后感。

默认把这个案例当成后续产品设计的竞品参考来研究。每个重点结论都要回答：

- 这个设计在用户路径里解决了什么问题。
- 它用什么玩法、文案、交互、奖励、门槛或数值推动用户继续走。
- 如果我们要照着做，前台页面怎么设计，后台规则怎么配置，关键指标怎么看。
- 这套机制有什么风控和合规风险，应该怎么拦。

不要只说“这个设计很好”。要写清楚它为什么能让用户动起来，以及怎么复用成自己的产品能力。

## 工作流程

1. 读取案例材料。
   - 用户给飞书文档时，用 `lark-cli docs +fetch --doc <url> --as user` 读取。
   - 用户给视频时，先用 `ffprobe` 看视频信息，再用 `scripts/extract_video_keyframes.py` 抽关键截图。
   - 用户给产品网址时，抓取可见页面，并记录查看日期。

2. 整理证据包。
   - 截图按用户路径顺序排列。
   - 看到弹窗、toast、通知条、进度变化、红包动画、转盘动画、按钮变灰/高亮、分享面板等动态交互时，记录触发前、出现中、消失后这几个时刻。
   - 对影响用户决策的关键动态交互，先用 `scripts/build_interaction_keyframes.py` 从录屏里截出 3-6 张连续关键帧 PNG，并可合成一张关键帧拼图；GIF 只作为补充材料。飞书文档或画板无法稳定保留动图时，正文必须使用静态 PNG 关键帧，不要只插 GIF。
   - 如果用户直接给 GIF，先用根目录 `scripts/build_gif_keyframes.py` 抽样关键帧和拼图，再按 `../references/gif-animation-interaction-teardown.md` 拆动效实现；不要只看 GIF 第一帧或只描述观感。
   - 没有直接证据支撑的判断，一律标 `[推断]`。
   - 所有数字都要写清来源、日期、口径。

3. 起草案例拆解文档。
   - 使用 `references/case-teardown-template.md` 的标题顺序。
   - 除非用户明确要求，不要改标题顺序。
   - 案例命名和文档标题必须用中文。品牌或产品官方英文名可以保留，但标题要配中文机制描述，例如“拼多多现金大转盘案例拆解”，不要只写 `PDD cash wheel`。
   - 每个部分都要讲清楚三件事：发生了什么、为什么有效、我们能复用什么。
   - `1. 用户路径` 和 `3. 玩法解析` 下面的每个小节，都必须先写文案说明，再在该小节文字下方贴对应步骤截图/连续关键帧。截图或关键帧必须紧跟该小节，不能集中堆到文末。分析 UI 交互时，对应连续关键帧 PNG 或关键帧拼图必须贴在该小节下方，不能只放在总览图、附件或证据包里；GIF 可以补充，但不能替代正文图片。
   - `3. 玩法解析` 的每个小节还必须加“底层逻辑分析”，说明它利用了什么用户心理或行为机制，例如损失厌恶、收益放大、贪婪刺激、沉没成本、临门一脚、稀缺感、随机奖励、社交证明等；不能只描述页面发生了什么。
   - `3. 玩法解析` 遇到动态 UI 时必须补“UI 交互分析”：写清触发条件、出现位置、视觉强调方式、用户下一步、业务目的、可能的打扰或风险。比如“今日提现峰值提醒”不是只贴图，还要说明它为什么在临门一脚金额附近弹出、怎么把用户注意力拉回“继续提现”。
   - 如果用户要“这种动画怎么实现”或“提示词一比一还原”，输出不能只停留在玩法分析；必须补“实现提示词”段落，写清基础页面、动效层级、时序、运动参数、点击后状态、技术要求和不要做什么。
   - 每张小节截图都要有一句图注，说明这张图证明了哪个入口、文案、交互、进度、奖励、风控或转化设计。
   - 如果用户指定目标行业，例如 casino、电商、SaaS、游戏、金融等，`6. 如何复用` 和 `对我们 SaaS 产品的核心启发` 必须改成该行业能落地的产品方案，不要泛泛而谈。

4. 制作用户路径画板。
   - 使用 `references/user-path-whiteboard.md`。
   - 主方案是“真实截图 + 步骤备注”的横向故事板，不是抽象流程图。
   - 输出样式参考图是 `assets/user-path-storyboard-standard.png`，标题口径为“用户完整路径时序图：真实截图 + 每一步操作备注”。
   - 路径图必须按真实案例完整呈现，从第一次触达到关键目标动作和后续闭环；不要预设一定是付费、裂变或社群路径。
   - 每一步至少包含：真实截图、用户操作、系统反馈或页面变化、这一步的业务目的。
   - 本地生成的截图故事板图片必须同时放在飞书文档 `## 用户完整路径时序图` 部分，不能只放在附件或最终回复里。
   - Mermaid 只能用来先梳理顺序，不能作为最终用户路径图替代品。

5. 输出到飞书。
   - 用 `lark-cli docs +create` 或 `lark-cli docs +update` 创建或更新飞书文档。
   - 需要新路径图时，在 `## 用户完整路径时序图` 下创建空白画板。
   - 新建文档时，按“标题文字 -> 本地截图故事板图片 -> 空白画板 -> 后续正文”的顺序创建，让图片自然落在 `## 用户完整路径时序图` 下方。
   - 更新已有文档时，先检查 `lark-cli docs +media-insert --help` 是否支持 `--selection-with-ellipsis`。支持时，优先用文本锚点精确插图；不支持时，才走 docx block API 或新建迭代版文档验证。
   - 渲染画板内容后，用 `lark-cli docs +whiteboard-update` 写入画板。新建空白画板第一次写入时，优先不要加 `--overwrite`；已有非空画板才走 dry-run 和覆盖确认。
   - 如果要把本地截图插到已有飞书文档的指定小节下方，不能用普通 `docs +update` 假装完成；必须按“飞书图片插入限制”执行。
   - 已有文档包含图片、画板、表格时，默认禁止 `overwrite`、大范围 `delete_range`、根块 `batch_delete`、删除后半篇再重建。除非用户明确批准，并且已保存备份。

6. 验证结果。
   - 重新读取飞书文档，确认标题结构存在。
   - 确认文档里有 `<whiteboard token="...">`。
   - 确认案例标题和案例名称是中文。
   - 确认关键 UI 交互已用静态 PNG 连续关键帧或关键帧拼图呈现；GIF 只能作为补充，不能把本地 GIF 路径当成交互证据。
   - 如果画板渲染或上传失败，要说清楚具体卡在哪里，同时保证飞书文档正文可用。

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
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\lark-version\scripts\extract_video_keyframes.py" `
  "C:\path\case.mp4" `
  --out-dir "C:\path\frames" `
  --every 12 `
  --max-frames 18
```

已知关键时间点时，用下面方式指定：

```powershell
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\lark-version\scripts\extract_video_keyframes.py" `
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
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\lark-version\scripts\build_interaction_keyframes.py" `
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
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\lark-version\scripts\build_interaction_gif.py" `
  "C:\path\case.mp4" `
  --start "00:01:20.000" `
  --duration 2.5 `
  --highlight "40,90,640,160" `
  --output "C:\path\interaction-reminder.gif"
```

`--highlight` 的格式是 `x,y,w,h`，坐标基于当前画面；如果先用了 `--crop`，就基于裁剪后的画面。飞书文档或画板无法确认 GIF 动画时，要在正文里补连续关键帧 PNG 或关键帧拼图，不能只写本地 GIF 路径。

如果已经有截图和备注，用下面脚本生成横向路径故事板：

```powershell
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\lark-version\scripts\build_user_path_storyboard.py" `
  --items "C:\path\storyboard-items.tsv" `
  --output "C:\path\user-path-storyboard.png"
```

`storyboard-items.tsv` 每行 3 列，用 Tab 分隔：

```text
C:\path\step1.png	用户点击页面入口	看到核心利益点，准备进入下一步
C:\path\step2.png	用户完成关键动作	系统给出结果反馈或下一步引导
```

生成后的故事板图片可以先插入飞书文档正文；如果要写进飞书画板，需要拿到画板可用的图片 token。不要把本地路径、文档图片 token 或云盘 file_token 直接当成画板图片 token。

## 正文截图标准

飞书案例文档里有三类图，不能互相替代：

1. `用户完整路径时序图`：完整路径总览图，放在 `## 用户完整路径时序图` 下。
2. `1. 用户路径` 小节截图/关键帧：每个用户路径小节下方放该步骤的真实截图；分析动态交互时，把对应连续关键帧 PNG 或关键帧拼图也放在这里。
3. `3. 玩法解析` 小节截图/关键帧：每个玩法解析小节下方放证明该玩法的真实截图；分析 UI 交互时，把对应连续关键帧 PNG 或关键帧拼图也放在这里。

`1. 用户路径` 和 `3. 玩法解析` 的标准结构都是：

```markdown
### 小节标题

文案说明：发生了什么、交互怎么引导、底层逻辑是什么。
玩法解析小节必须单独补充“底层逻辑分析”：这一步为什么能驱动用户继续，利用了损失厌恶、收益放大、沉没成本、临门一脚、稀缺感、随机奖励、社交证明等哪类机制。必须对应到截图里的文案、数字、按钮、进度、奖励或页面反馈；证据不足时标 `[推断]`。

UI 交互分析：如果这一步有动态交互，要写触发条件、出现位置、视觉强调、持续时间、用户下一步和业务目的；证据不足时标 `[推断]`。

![对应步骤截图](图片)

[如果有关键交互，这里插入连续关键帧 PNG 或关键帧拼图；GIF 只能作为补充，不能只写路径]

图注：这张图证明了什么。
```

不能只在 `用户完整路径时序图` 放一张总图，然后正文不放截图。不能把所有小节截图集中放到文末。写了 UI 交互分析，就必须把对应连续关键帧 PNG 或关键帧拼图贴在该小节下方；不能只贴本地 GIF 路径。

如果暂时拿不到画板可用图片 token，用下面脚本把同一份 `storyboard-items.tsv` 生成文字卡片版画板 JSON。它不是替代真实截图故事板，而是飞书画板上传图片失败时的可用兜底；真实截图故事板仍必须插在文档正文里。

```powershell
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\lark-version\scripts\build_whiteboard_path_cards.py" `
  --items "C:\path\storyboard-items.tsv" `
  --output "C:\path\user-path-whiteboard-cards.json" `
  --title "用户完整路径图"
```

## 飞书规则

- 用户自己的文档，默认用 `--as user`。
- 如果授权失败，先执行 `lark-cli auth login --domain docs --no-wait --json`，把返回的授权链接发给用户，再用返回的 device code 完成授权。
- 修改已有飞书文档前，先 `docs +fetch` 保存一份本地备份。文档里已有 `<image token=...>` 或 `<whiteboard token=...>` 时，禁止直接 `overwrite`，除非用户明确批准。
- 更新已有画板前，必须先 dry-run：

```powershell
lark-cli docs +whiteboard-update --whiteboard-token <token> --overwrite --dry-run --as user
```

- 已有画板不是空的，不能直接覆盖，必须先得到用户明确确认。
- 新建画板时，把空白画板放到 `## 用户完整路径时序图` 下。
- 新建空白画板第一次写入时，不要先用 `--overwrite`。如果遇到 `4003101 get whiteboard nodes failed`、`doc is applying`、`doc data is not ready`，通常是飞书画板刚创建还没准备好；等 5-10 秒后重试，或者去掉 `--overwrite` 直接追加写入。
- Windows PowerShell 调外部命令时，XML 属性里的双引号容易被吃掉，所以要这样传：

```powershell
lark-cli docs +update --doc "<doc>" --mode insert_after --selection-by-title "## 用户完整路径时序图" --markdown '<whiteboard type=\"blank\"></whiteboard>' --as user
```

- 如果 dry-run 或返回结果里出现 `<whiteboard type=blank>`，说明双引号被吃掉了，要用上面的转义方式重试。
- 如果重新读取文档后没有 `<whiteboard token="...">`，不要说画板已经创建成功。
- 写入真实画板内容需要 `@larksuite/whiteboard-cli`。下载安装或用 `npx -y` 前，要先得到用户同意。
- 在 PowerShell 里把 `whiteboard-cli` 输出管道传给 `lark-cli docs +whiteboard-update` 时，先设置 UTF-8 输出编码，否则中文可能变成问号：

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
npx -y @larksuite/whiteboard-cli@^0.1.0 --to openapi -i ".\case-user-path.mmd" --format json |
  lark-cli docs +whiteboard-update --whiteboard-token <token> --yes --as user
```

已有非空画板需要覆盖时，才在用户确认后增加 `--overwrite`：

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
npx -y @larksuite/whiteboard-cli@^0.1.0 --to openapi -i ".\case-user-path.json" --format json |
  lark-cli docs +whiteboard-update --whiteboard-token <token> --overwrite --yes --as user
```

飞书画板图片写入的处理顺序：

1. 优先生成真实截图故事板图片，并用 `lark-cli docs +media-insert` 插入文档 `## 用户完整路径时序图`。
2. 只有拿到画板 OpenAPI 可用的图片 token，才把图片作为 image node 写入画板。
3. 不要用本地路径、文档 image token、云盘 file_token 冒充画板图片 token。
4. 如果图片节点上传失败，用 `build_whiteboard_path_cards.py` 生成文字卡片版画板 JSON 并写入画板，同时在最终回复里说明真实截图已经放在文档正文里。
5. 写入后用 `lark-cli docs +media-download --type whiteboard --token <token>` 下载缩略图验证，不能只看命令返回 `ok`。

## 飞书图片插入与定位

这些限制必须先讲清楚，不能边试边破坏文档：

- `lark-cli` 旧版本的 `docs +media-insert` 只能把本地图片插到文档末尾，不能指定插到某个小节下方。
- `lark-cli` 新版本如果在 `docs +media-insert --help` 里出现 `--selection-with-ellipsis`，就可以按文本定位插图。推荐用唯一锚点，例如 `**对应截图：1.2 中奖开场**`，再执行：

```powershell
npx -y @larksuite/cli@1.0.42 docs +media-insert `
  --doc "<doc_id_or_url>" `
  --file "C:\path\step.png" `
  --selection-with-ellipsis "对应截图：1.2 中奖开场" `
  --caption "图注：这张图证明了什么" `
  --width 360 `
  --as user
```

- 用定位插图前，先把正文更新成“文案说明 -> 唯一截图锚点 -> 图注”的结构；插图时匹配这个唯一锚点，避免插错位置。
- `lark-cli docs +update` 的 Markdown 图片只支持公开 `https://...` 图片 URL；不支持本地路径、data URL，也不支持复用 `<image token="...">`。
- 已经上传到某个图片 block 的 token 不能直接绑定到另一个图片 block；强行复用可能报 `relation mismatch`。
- 如果当前 CLI 没有 `--selection-with-ellipsis`，要把本地截图精确插入到已有文档的某个小节下方，才需要走 docx block API：定位目标 block index，创建空 image block，把本地图片上传到这个新 image block，再绑定 token。
- 如果当前既没有新版 `media-insert`，也没有把握用 block API 精确插图，必须先停下来说明限制，得到用户许可后再继续；不能用删除半篇、覆盖全文、把图片堆到文末等方式代替。

推荐安全策略：

1. 先在本地生成完整 Markdown 草稿和所有截图清单。
2. 新建文档时，可以按“文字块 -> media-insert 追加图片 -> 文字块”的顺序创建，因为每一步都是往文末追加，图片能自然跟在对应小节后面。
3. 更新已有文档时，如果需要精确插图，优先用新版 `docs +media-insert --selection-with-ellipsis`。每个小节先放唯一锚点，再逐张插图并重新 fetch 验证。
4. 新版 CLI 不可用时，优先新建一个迭代版文档验证；要改原文档，先说明会用 block API，并得到用户确认，不能用覆盖全文或删除重建代替。
5. 一旦发现 `IMAGE_MISSING_URL`、图片被跳过、token 不能复用、或 block API 报错，立即停止并报告真实限制。

## 质量要求

- 文档要像正式交付物，不要像素材笔记。
- 用户路径图必须用真实案例截图展示顺序，并配上每一步用户操作备注；只画抽象箭头不合格。
- `用户完整路径时序图` 必须包含真实截图故事板图片；画板也要放在同一部分附近，便于读者对照。
- 案例命名和文档标题必须用中文，不能用英文文件名或英文 slug 直接当交付标题。
- `1. 用户路径` 和 `3. 玩法解析` 每个小节下方必须配对应截图/连续关键帧和图注，没有截图或关键帧支撑的判断要标 `[推断]`。
- `3. 玩法解析` 不能只写心理机制；有弹窗、提示条、动画、按钮状态变化等动态 UI 时，必须补 UI 交互分析，并把连续关键帧 PNG 或关键帧拼图贴在对应小节下方。GIF 只能作为补充材料，不能替代正文图片。
- 已有飞书文档内的图片、画板、表格是不可随意重建的交付物；不能为了插图位置方便而覆盖或删除重建。
- “如何复用”和“核心启发”必须落到产品模块，不能只写营销观察。
- 最终回复里要给出飞书文档链接和画板 token；如果没生成成功，要说明真实原因。
