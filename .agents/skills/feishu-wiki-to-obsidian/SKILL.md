---
name: feishu-wiki-to-obsidian
description: 将飞书知识库（Wiki）中的文档导入到本地 Obsidian Vault 的 raw/ 目录。自动获取文档 Markdown 内容、下载文档中的图片到本地 assets 目录、将图片引用替换为 Obsidian 标准语法 `![[文件名称.png]]`。当用户说"导入飞书文档"、"把飞书 Wiki 文章导入本地"、"拉取飞书文档到 Obsidian"、"将飞书文档下载到 raw" 或给出飞书 Wiki URL 并要求导入时触发。
---

# 飞书 Wiki 文档导入 Obsidian

将飞书知识库（Wiki）中的文档导入到本地 Obsidian Vault 的指定目录，并自动处理图片。

## 工作流程

### Step 1: 解析输入

用户可能提供：
- 飞书 Wiki URL：`https://nio.feishu.cn/wiki/<wiki_token>`
- 飞书 Docx URL：`https://nio.feishu.cn/docx/<doc_token>`
- 纯 token

从 URL 中提取 wiki_token 或 doc_token。

### Step 2: 获取文档信息

如果是 Wiki URL，先通过 `wiki spaces get_node` 获取文档信息：

```bash
lark-cli wiki spaces get_node --as user --params '{"token":"<wiki_token>","obj_type":"wiki"}' --format json
```

从返回中提取：
- `obj_token`（文档的实际 token）
- `title`（文档标题，用于文件名）

### Step 3: 权限校验

```bash
lark-cli drive permission.members auth --as user --params '{"token":"<obj_token>","type":"docx","action":"edit"}' --format json
```

返回 `auth_result: true` 才继续，否则提示用户无权限。

### Step 4: 获取文档 Markdown 内容

```bash
lark-cli docs +fetch --api-version v2 --doc <obj_token> --doc-format markdown --format pretty
```

### Step 5: 提取并下载图片

从 Markdown 内容中提取所有图片 URL（格式为 `![](https://internal-api-drive-stream.feishu.cn/...)`），下载到目标 `assets` 目录：

```bash
curl -s -o <assets_dir>/<filename> "<image_url>"
```

图片命名规则：根据图片上下文语义命名（如 `流水线价值示意图.png`），若无上下文则用 `image-序号`。

### Step 6: 处理 Markdown 内容并保存

1. 将 Markdown 中的图片 URL（`![](https://...)`）替换为 Obsidian 标准内嵌图片语法 `![[<filename>]]`，无需指定路径前缀，因为 Obsidian 会根据附件文件夹配置自动解析。
2. 在文件开头添加来源元信息（来源链接、转换时间）
3. 保存到目标目录（如 `raw/01-articles/`）文件名使用文档标题

### 输出格式

每个文档保存为一个 Markdown 文件，开头包含：

```markdown
# {文档标题}

> 来源：[飞书文档](原始链接)
> 转换时间：{YYYY-MM-DD}
```

## 注意事项

- 图片下载使用 `curl`，需要网络访问权限
- 如果图片下载失败，保留原 URL 并标注 `<!-- 图片下载失败 -->`
- 文档中的嵌入表格（sheet）内容无法通过 Markdown 导出获取，需标注说明
- 所有命令必须使用 `--as user` 身份执行
- 目标目录需用户确认（默认 `raw/01-articles/`，图片默认 `raw/assets/`）
