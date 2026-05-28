# 用户路径画板规范

## 基本形态

最终交付必须优先做成“真实截图 + 备注”的横向路径故事板，样式类似：

标准参考图：`../assets/user-path-storyboard-standard.png`

这张图就是“用户完整路径时序图：真实截图 + 每一步操作备注”的输出标准。后续做案例拆解时，路径图至少要达到这个信息密度：真实截图、步骤编号、用户动作标题、业务备注、箭头顺序都要齐。

```text
[真实截图1] -> [真实截图2] -> [真实截图3] -> ...
 用户点击分享按钮   触发分享弹窗      选择分享人
```

这不是抽象的系统时序图。Mermaid 只能用来先梳理顺序，不能替代最终画板。

步骤按真实案例来定，不要硬套固定环节。通常可以覆盖：

1. 用户第一次看到入口。
2. 用户进入页面、内容、活动、商品、服务或工具。
3. 用户做出关键动作，比如浏览、点击、领取、注册、授权、加购、下单、留资、分享、进群、下载、关注、预约等。
4. 系统、页面、消息或人工服务给出反馈。
5. 用户被引导到下一步。
6. 用户完成关键目标动作。
7. 后续闭环，比如复访、留存、复购、传播、线索沉淀、付费、进群、咨询、下载或其他结果。

每个步骤都要写清楚：
- 真实截图。
- 用户动作，例如“用户点击分享按钮”。
- 系统反应或页面变化，例如“弹出分享面板”。
- 业务目的，例如“降低分享操作成本”。

备注优先写用户动作，不要只写页面名称。

## 画板布局

推荐布局：

- 一行横向排列截图。
- 每张截图下方放 1 行用户动作。
- 动作下面可再放 1 行业务备注。
- 截图之间用箭头连接。
- 一屏放不下时，分成两行，每行 5-8 步。
- 手机截图保持竖屏比例，不要拉伸变形。

## Mermaid 草稿

路径复杂时，可以先用 Mermaid 或文字列表梳理顺序，但最终要换成截图故事板。

## 截图摆放

如果案例来自视频：
- 不限制截图数量，按案例真实路径复杂度决定；路径越长、关键交互越多，截图就应该越详细。
- 所有能证明路径步骤、用户操作、页面反馈、关键规则、奖励变化、风控提示或转化引导的截图都可以保留。
- 截图标题写时间点和含义，比如 `00:42 注册表单`。
- 不要把等候、重复滑动、无关过渡页放进最终图。

## 本地故事板图片

已有截图和备注时，用 `scripts/build_user_path_storyboard.py` 生成本地横向图片：

```powershell
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\lark-version\scripts\build_user_path_storyboard.py" `
  --items ".\storyboard-items.tsv" `
  --output ".\user-path-storyboard.png"
```

`storyboard-items.tsv` 每行 3 列，用 Tab 分隔：

```text
.\step1.png	用户点击页面入口	看到核心利益点，准备进入下一步
.\step2.png	用户完成关键动作	系统给出结果反馈或下一步引导
```

## 飞书画板输出

推荐路径：

1. 先创建或更新飞书文档，并在 `## 用户完整路径时序图` 下创建空白画板：

```markdown
## 用户完整路径时序图
<whiteboard type="blank"></whiteboard>
```

2. 从返回结果读取 `board_tokens`。
3. 新建文档时，先把本地截图故事板图片插入飞书文档正文的 `## 用户完整路径时序图` 下方；已有文档需要精确插图时，必须走 docx block API 或新建迭代版文档。
4. 把截图故事板作为图片放入画板，或用画板 DSL 放置截图、箭头和备注。
5. 如果图片节点上传失败，生成文字卡片版路径图写入画板，真实截图故事板仍保留在文档正文。
6. 如果更新已有画板，先 dry-run。
7. 用 `lark-cli docs +whiteboard-update` 上传到画板。

不能在用户未确认的情况下覆盖非空画板。

## 正文小节截图不是画板

画板和 `用户完整路径时序图` 只解决“总览”。正式案例文档还必须在 `1. 用户路径` 和 `3. 玩法解析` 的每个小节下方放对应截图：

- 小节文字先解释发生了什么和为什么有效。
- 截图紧跟该小节文字。
- 图注说明这张图证明了什么。
- 不要把这些小节截图集中放到文末。

如果是新建文档，推荐按“追加文字小节 -> `docs +media-insert` 插入本地截图 -> 追加下一小节”的顺序创建，这样图片自然在小节下方。

如果是更新已有文档，`docs +media-insert` 只能追加到文末，不能指定插入位置；不要用它假装完成“小节下方插图”。需要精确位置时，必须使用 docx block API，或先新建迭代版文档验证。没有把握时先停下来说明限制，等用户确认后再动原文档。

## 画板图片节点

白板 DSL 支持图片节点，本地预览格式如下：

```json
{
  "version": 2,
  "nodes": [
    {
      "type": "image",
      "id": "storyboard",
      "x": 0,
      "y": 0,
      "width": 2004,
      "height": 644,
      "image": {
        "src": "./user-path-storyboard.png"
      }
    }
  ]
}
```

注意：
- 本地预览可以用本地图片路径。
- 真正写入飞书画板时，OpenAPI 需要的是 `image.token`，不能直接传本地路径。
- `docs +media-insert` 得到的文档图片 token、`drive +upload` 得到的云盘 file_token，不一定能作为画板 image token 使用；实测可能报服务端错误。
- 如果暂时拿不到画板可用图片 token，先把故事板图片插入飞书文档正文，再用文字卡片版路径图写入画板。不要只保留空画板占位。

## 图片写入失败时的兜底画板

当真实截图图片无法作为 image node 写入飞书画板时，用同一份 `storyboard-items.tsv` 生成文字卡片版画板 JSON：

```powershell
python "$env:USERPROFILE\.codex\skills\case-teardown-standard\lark-version\scripts\build_whiteboard_path_cards.py" `
  --items ".\storyboard-items.tsv" `
  --output ".\user-path-whiteboard-cards.json" `
  --title "用户完整路径图"
```

然后先本地渲染检查：

```powershell
npx -y @larksuite/whiteboard-cli@^0.1.0 -i ".\user-path-whiteboard-cards.json" -o ".\user-path-whiteboard-cards.png"
```

写入新建空白画板时，不要加 `--overwrite`：

```powershell
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
npx -y @larksuite/whiteboard-cli@^0.1.0 --to openapi -i ".\user-path-whiteboard-cards.json" --format json |
  lark-cli docs +whiteboard-update --whiteboard-token <token> --yes --as user
```

只有确认已有画板非空且用户同意覆盖后，才使用 `--overwrite`。

写入后必须下载白板缩略图验证：

```powershell
lark-cli docs +media-download --type whiteboard --token <token> --output ".\whiteboard-check.png" --overwrite --as user
```

## 常见问题

- Windows PowerShell 调外部命令时可能会吃掉 XML 属性双引号。传空白画板标签时用 `<whiteboard type=\"blank\"></whiteboard>`，并先看 dry-run 输出。
- Windows PowerShell 管道默认编码可能导致中文变成 `??`。执行 `whiteboard-cli | lark-cli docs +whiteboard-update` 前，先设置 `$OutputEncoding` 和 `[Console]::OutputEncoding` 为 UTF-8。
- 如果 `docs +create` 或 `docs +update` 返回成功，但重新读取文档后没有 `<whiteboard token="...">`，不能当作画板已经创建成功。
- 如果 `--overwrite` 报 `4003101 get whiteboard nodes failed`、`doc is applying`、`doc data is not ready`，先判断是不是刚新建的空白画板。新画板第一次写入通常不需要删除旧节点，去掉 `--overwrite` 后重试；仍失败再等 5-10 秒重试。
- 如果 image node 本地预览正常但上传飞书失败，不要继续反复用本地路径、文档图片 token 或云盘 file_token 重试。改用文字卡片版画板，并把真实截图故事板放进文档正文。
- 如果飞书文档正文需要在指定小节下方插入本地图片，不能靠 `<image token="...">` 或 `docs +media-insert`。前者会被 `docs +update` 跳过，后者只会追加到文末。遇到这个限制要先停下来说明。
- 已有文档含图片或画板时，不要直接 `overwrite` 或删除重建。先备份，再得到用户明确确认。
- 如果本机没有 `@larksuite/whiteboard-cli`，下载安装或使用 `npx -y` 之前要先得到用户同意。
