---
name: ingest
description: 将 raw/ 目录下的 Markdown 原始资料编译到 wiki/ 中。支持 `/ingest` (扫描 raw/ 下所有 Markdown 文件) 或 `/ingest <path>` (处理指定文件)。若文件不是 Markdown，直接失败并提示先转换。通过 frontmatter 的 `ingested` 字段控制增量 ingest。
user-invocable: true
---

# ingest 技能

## 核心工作流：Markdown Only + Ingested

你正在维护一个 **LLM Wiki**（Obsidian 知识库）。`raw/` 目录是"待处理收件箱"，`wiki/` 是"编译输出层"。

**目录结构约定：**

- `raw/01-articles/` — 网页剪藏的 Markdown 文章
- `raw/02-papers/` — 已转换为 Markdown 的论文资料
- `raw/03-transcripts/` — 已转换为 Markdown 的转录文案
- `wiki/sources/` — 资料摘要
- `wiki/entities/` — 实体（人物、公司、工具、产品）
- `wiki/concepts/` — 概念（框架、方法论、理论）

**输入约束：**

- `raw/` 下只允许 `.md` 文件。
- 外部来源（PDF/网页/JSON/音视频）必须在进入 `raw/` 前转换为 Markdown。
- 执行 `/ingest` 时发现非 `.md` 文件，必须直接失败并提示："请先转换为 Markdown 后再 ingest"。

## 触发逻辑

1. **用户执行 `/ingest`**：扫描 `raw/` 所有子目录中的 `.md` 文件，按 `ingested` 判定是否处理。
2. **用户执行 `/ingest <path>`**：仅处理指定文件。
3. **隐式触发**：用户说"把这个资料摄入知识库"、"导入这篇文章"时，自动执行 ingest。

## 状态字段规范（写在 raw Markdown 的 frontmatter）

每个 `raw/*.md` 文件可维护以下字段：

```yaml
ingested: false
ingested_at:
ingest_error:
```

### 判定规则

- 若 `ingested=true`：默认跳过。
- 若 `ingested=false` 或字段缺失：进入处理流程。
- 需要重跑已处理文件时，将 `ingested` 置回 `false` 并清空 `ingested_at`。

## 编译流水线

对每个待处理源文件，严格按以下步骤执行：

### 步骤 1：读取源文件

- 仅接受 `.md` 文件。
- 若指定路径或扫描结果包含非 `.md` 文件：立即失败并提示先转换为 Markdown。
- 读取完整内容，拆分 frontmatter 与正文。

### 步骤 2：写入 processing 状态

- 开始处理前，更新 frontmatter：
  - `ingested=false`
  - `ingest_error=`（清空历史错误）

### 步骤 3：提炼核心并翻译

从源文件中提取：

- **核心主旨**：这段资料讲什么（1-2句话）
- **实体**：人物、公司、工具、产品等具体名词
- **概念**：框架、方法论、理论等抽象名词

如果是非中文内容，则翻译成中文。

### 步骤 4：创建来源摘要

在 `wiki/sources/` 创建 Markdown 文件：

```markdown
---
title: "摘要-文件slug"
type: source
tags: [来源, 原始文件]
sources: [raw/01-articles/xxx.md]
last_updated: YYYY-MM-DD
---

## 核心摘要

[3-5句话的核心总结]

## 关联连接

- [[EntityName]] — 关联实体
- [[ConceptName]] — 关联概念
```

文件名使用 kebab-case：`摘要-{文件slug}.md`

### 步骤 5：知识网络化（实体/概念页面）

对于步骤 2 提取的每个实体和概念：

**目标目录：**

- 实体 → `wiki/entities/`
- 概念 → `wiki/concepts/`

**处理逻辑：**

1. 页面不存在 → 按照 CLAUDE.md 的 Frontmatter 规范创建新页面
2. 页面已存在 → 读取现有内容，**增量合并**新信息
3. **发现冲突** → **立即暂停**，向用户报告冲突内容，询问处理方式后再继续

**页面模板：**

```markdown
---
title: "页面名称"
type: entity | concept
tags: [标签]
sources: [关联的源文件]
last_updated: YYYY-MM-DD
---

## 定义

[对该实体/概念的定义]

## 关键信息

[从源文件中提取的详细信息]

## 关联连接

- [[摘要-source-slug]] — 来源
- [[RelatedEntity]] — 相关实体
```

### 步骤 6：更新全局注册表

**更新 `wiki/index.md`：**
按照 CLAUDE.md 规定的格式，将新增页面添加到对应分类下：

- Sources: `[[摘要-source-slug]] — 该资料的核心主旨`
- Entities: `[[EntityName]] — 该实体的身份定义`
- Concepts: `[[ConceptName]] — 该概念的核心定义`

**更新 `wiki/log.md`：**
追加操作日志（Append-only）：

```markdown
## [YYYY-MM-DD] ingest | 操作简述

- **变更**: 新增 [[PageName]]; 更新 [[index.md]]
- **冲突**: 无 (或: 冲突 [[ConflictingPage]], 已暂停等待决策)
```

### 步骤 7：写回 ingest 状态（不归档、不移动）

在确认处理结果后，更新当前源文件 frontmatter：

- 成功：`ingested=true`
- 冲突或失败：`ingested=false`

并写入：

- `ingested_at=<当前时间>`（仅成功时）
- `ingest_error=<错误摘要>`（仅失败时，可选）

**禁止修改源文件正文内容。**

## 冲突处理流程

当发现新旧知识冲突时：

1. **暂停**：停止当前 ingest 流程
2. **报告**：向用户说明冲突内容（哪个页面、冲突点是什么）
3. **询问**：请用户选择处理方式：
   - A) 保留新旧两者，标注为"知识冲突"
   - B) 用新知识覆盖旧知识
   - C) 放弃本次 ingest
4. **继续**：根据用户选择继续或终止

## 注意事项

- ingest 只处理 `.md` 文件，发现非 `.md` 必须报错并提示先转换
- 所有 wiki 页面必须包含 `## 关联连接` 区域，不能产生孤岛页面
- 使用简体中文编写所有内容
- 实体命名使用 TitleCase，概念和来源使用 kebab-case
