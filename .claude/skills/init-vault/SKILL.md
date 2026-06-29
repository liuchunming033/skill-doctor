---
name: init-vault
description: 初始化 LLM Wiki Vault：创建标准目录结构与基石文件（含 CLAUDE.md、wiki/index.md、wiki/log.md），并进行最小化健康检查。支持 `/init-vault` 与 `/init-vault --force`。
user-invocable: true
---

# init-vault 技能

## 目标

用于"新仓库首建"或"老仓库补齐"，一次性初始化 Vault 的基础骨架。

初始化范围：

- 目录结构
- `CLAUDE.md` 基础规则文件
- `wiki/index.md` 与 `wiki/log.md` 基石文件
- `raw/` 下的标准子目录

## 触发方式

1. 用户执行 `/init-vault`
2. 用户执行 `/init-vault --force`
3. 隐式触发：用户表达"初始化 vault"、"搭建知识库骨架"、"创建目录结构和 CLAUDE.md"

## 执行模式

### 默认模式（安全模式）

- 只创建缺失项
- 已存在文件不覆盖
- 输出"已创建 / 已跳过"清单

### 强制模式（`--force`）

- 允许覆盖基石文件：`CLAUDE.md`、`wiki/index.md`、`wiki/log.md`
- 覆盖前必须明确提示风险

## 标准目录结构

必须确保以下目录存在：

- `raw/`
- `raw/01-articles/`
- `raw/02-papers/`
- `raw/03-transcripts/`
- `raw/09-archive/`
- `wiki/`
- `wiki/sources/`
- `wiki/entities/`
- `wiki/concepts/`
- `wiki/syntheses/`
- `schemas/`
- `00-inbox/`
- `Clippings/`
- `output/`

## 文件初始化规则

### 1) `CLAUDE.md`

如果不存在，则创建标准模板，至少包含：

- 语言与角色约束（简体中文 + LLM Wiki）
- 不可变边界（`raw/` 正文只读）
- `raw/` 全目录仅 Markdown
- `wiki/index.md` 与 `wiki/log.md` 的维护契约
- `/ingest`、`/query`、`/lint` 的工作流约定

若已存在：

- 默认不改写
- 输出提示："已存在，跳过"

### 2) `wiki/index.md`

如果不存在，创建最小模板：

```markdown
# Wiki Index

## Sources

## Entities

## Concepts

## Syntheses
```

### 3) `wiki/log.md`

如果不存在，创建最小模板：

```markdown
# 操作日志
```

并追加一次初始化记录：

```markdown
## [YYYY-MM-DD] sync | vault 初始化

- **变更**: 初始化目录结构与基石文件
- **冲突**: 无
```

## 初始化后检查

执行快速检查并汇报：

1. `raw/` 是否包含非 Markdown 文件（发现则告警，不自动删除）
2. `wiki/index.md` 是否存在并可读
3. `wiki/log.md` 是否存在并可追加

## 输出格式

执行完成后必须返回：

- 创建的目录列表
- 创建的文件列表
- 跳过的文件列表
- 检查告警列表（如有）
- 下一步建议：
  - 先把外部资料转换成 Markdown 后再放入 `raw/`
  - 执行 `/ingest` 开始编译知识库

## 最小执行示例

### 示例 1：默认模式（不覆盖）

用户输入：

```text
/init-vault
```

处理步骤（最小闭环）：

1. 扫描目标路径下是否存在标准目录与基石文件。
2. 仅创建缺失目录和缺失文件。
3. 对已存在项目标记为 skipped。
4. 执行初始化后检查并汇总告警。
5. 按标准输出样例返回结构化结果。

### 示例 2：强制模式（允许覆盖）

用户输入：

```text
/init-vault --force
```

处理步骤（最小闭环）：

1. 明确提示将覆盖 `CLAUDE.md`、`wiki/index.md`、`wiki/log.md`。
2. 覆盖基石文件并保留目录补齐逻辑。
3. 执行初始化后检查并汇总告警。
4. 按标准输出样例返回结构化结果。

## 标准输出样例

后续 agent 调用时，优先按以下结构返回，保证可预测性：

```yaml
status: success
mode: safe
workspace: /path/to/vault
created:
  directories:
    - raw/01-articles
    - raw/02-papers
    - wiki/sources
    - wiki/entities
  files:
    - wiki/index.md
    - wiki/log.md
skipped:
  directories:
    - raw/03-transcripts
    - wiki/concepts
  files:
    - CLAUDE.md
checks:
  non_markdown_in_raw:
    passed: false
    warnings:
      - raw/BVxxxx.json
  wiki_index_readable: true
  wiki_log_appendable: true
warnings:
  - raw/ 存在非 Markdown 文件，请先转换后再 ingest
next_steps:
  - 将外部资料先转换为 Markdown 再放入 raw/
  - 执行 /ingest 开始编译知识库
```

失败时将 `status` 置为 `failed`，并追加：

```yaml
error:
  code: INIT_VAULT_FAILED
  message: 失败原因摘要
```

## 约束

- 不修改 `raw/` 下 Markdown 正文
- 不移动、不删除 `raw/` 源文件
- 不在未授权情况下覆盖已有基石文件
- 全程使用简体中文
