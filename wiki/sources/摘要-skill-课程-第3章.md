---
title: "摘要-skill-课程-第3章"
type: source
tags: [来源, Skill课程, SkillFileStructure, YAML, Frontmatter]
created: 2026-06-18
updated: 2026-06-18
sources: [output/skill/03-Skill长什么样.md]
related: [wiki/concepts/SkillFileStructure.md, wiki/concepts/AgentSkill.md, wiki/concepts/ProgressiveDisclosure.md]
---

## 核心摘要

本章详解 Skill 的标准文件结构：以文件夹为单位，SKILL.md 是唯一核心入口（必需），scripts/、references/、assets/ 为可选扩展。重点讲解命名规范（文件夹必须 kebab-case，SKILL.md 必须大写），以及 YAML Frontmatter 的字段约束。以 Anthropic 官方 PDF Skill 为实战示例，演示分层设计原则：SKILL.md 写核心流程、附属文件按需加载。

## 关键洞察

### 标准文件结构

```
my-skill/
├── SKILL.md          # Required: 核心入口（必需）
├── scripts/          # Optional: 可执行脚本
├── references/       # Optional: 参考文档
├── assets/           # Optional: 资源文件
```

### 四类文件的职责分工

- **SKILL.md**：包含 YAML Frontmatter（元数据路由）+ 主体正文（执行指导），两部分分工明确
- **scripts/**：提供确定性执行能力，避免 AI 自己生成代码
- **references/**：AI 按需读取，不默认加载，降低 Token 消耗
- **assets/**：标准化输出模板和配置规范

### 命名规范（不可违反）

- 文件夹：全部 kebab-case（小写+连字符），不能用空格、下划线、大写
- 入口文件：必须是 `SKILL.md`（全大写），不能是 skill.md 或 README.md
- name 字段：最多 64 字符，只含小写字母、数字和连字符，不含 `anthropic`、`claude` 保留词
- description 字段：必须非空，最多 1024 字符

### 设计原则

- SKILL.md 正文保持 5000 tokens 以内（官方建议 500 行以内）
- 详细内容拆分到 references/，AI 按需读取
- 确定性操作放到 scripts/，不让 AI 现场生成代码

## 关联连接

- [[SkillFileStructure]] — Skill 文件结构完整规范
- [[AgentSkill]] — Skill 的核心概念
- [[ProgressiveDisclosure]] — 文件分层设计背后的机制
- [[摘要-skill-anthropic-doc-part1]] — Skill 核心概念来源
- [[摘要-skill-anthropic-doc-part2]] — 渐进式披露机制详解
