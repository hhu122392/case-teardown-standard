---
name: case-teardown-standard
description: "Use when 用户要求拆解增长案例、竞品案例、用户路径图、真实截图时序图、视频案例抽帧、UI交互分析/GIF、Lark/飞书文档、飞书画板、Google Docs、Google Drive、本地 DOCX 或 Word 文档输出；也适用于按高级用户增长产品经理视角反推玩法、路径、数值设计、风控和行业复用方案。"
---

# 案例拆解标准

这个 skill 现在有两个交付版本，都放在本目录下面：

- `lark-version/SKILL.md`：飞书文档 + 飞书画板版本。用户说飞书、Lark、飞书画板、飞书云文档时，读这个版本。
- `google-docs-version/SKILL.md`：Google Docs / Google Drive / 本地 DOCX / Word 文档版本。用户说 Google Docs、谷歌文档、Google Drive、本地 doc、docx、Word 文档时，读这个版本。

如果用户没有指定交付平台，默认走 `lark-version/SKILL.md`，因为原始版本就是飞书交付。

## 共同标准

无论输出到哪个平台，都必须遵守这些规则：

1. 用大白话写，不要写成素材笔记或观后感。
2. 直接证据和推断分开。没有证据支撑的判断统一标 `[推断]`。
3. 不编数据、不编截图、不编来源。
4. 拆解视角是“高级用户增长产品经理”，重点回答：这个设计为什么推动用户继续走、怎么复用成产品能力、有什么风控和合规风险。
5. 案例命名、文档标题、小节里引用的案例名称都用中文；品牌或产品官方英文名可以保留，但必须配中文说明，不能只用英文 slug 当标题。
6. 用户路径图必须优先使用真实案例截图 + 每一步操作备注，不能只画抽象流程图。
7. 正文里的 `1. 用户路径` 和 `3. 玩法解析` 每个小节都要贴对应截图/连续关键帧和图注，不能只在总览图里放截图。
8. `3. 玩法解析` 必须补 UI 交互分析：弹窗、提示条、动画反馈、按钮状态变化等动态 UI，要说明触发条件、视觉强调、用户下一步和业务目的；关键交互优先用连续关键帧 PNG 或关键帧拼图作为正文证据，GIF 只能作为补充材料，不能用本地 GIF 路径代替正文图片。

## 平台不能混用

- 走飞书版时，按 `lark-version/SKILL.md` 使用 `lark-cli`、飞书文档和飞书画板规则。
- 走 Google Docs 输出时，按 `google-docs-version/SKILL.md` 使用 `google-drive:google-docs` 的 connector-first 规则。
- 走本地 DOCX / Word 输出时，也按 `google-docs-version/SKILL.md` 的拆解和截图标准执行，但最终生成本地 `.docx` 文件，不要假装已经写入 Google Docs。若本地 DOCX 后续会导入 Google Docs、飞书或其他在线文档，交互动效必须用静态 PNG 关键帧作为主内容，不要只插 GIF 或写 GIF 路径。
- Google Docs / 本地 DOCX 版不要调用 `lark-cli`，不要创建飞书画板，不要把飞书 `<image token>`、`<whiteboard token>` 或 Lark Markdown 标签写进文档。
- 飞书版不要把 Google Docs connector 或本地 DOCX 生成方式硬套进去。

## 固定标题

两个版本的正文标题顺序一致：

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

先读对应版本的 `SKILL.md`，再读该版本 `references/` 里的模板和交付规则。
