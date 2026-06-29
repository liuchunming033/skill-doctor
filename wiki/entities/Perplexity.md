---
title: "Perplexity"
type: entity
tags: [实体, 公司, AI, Skill]
sources: [raw/01-articles/解读 Perplexity的文章《Designing, Refining, and Maintaining Agent Skills at Perplexity》.md]
last_updated: 2026-06-18
---

## 定义

Perplexity 是一家 AI 搜索公司，其 AI Agent 产品内部搭建了严格管理的 Skill 资源库。Perplexity 团队对待 Skill 质量的标准和写正式代码同等严格，并公开了内部工程师统一开发、审核 Skill 的标准手册。

## 关键信息

### Skill 资源库结构
- **通用工具** - 操控电脑的基础功能
- **专业领域能力** - 金融、法律、医疗等垂直行业能力
- **小众功能** - 满足用户稀奇古怪的需求

### Skill 开发规范
- Skill 是一整个文件夹，不只是单个文件
- 采用三层加载机制（索引层/加载层/运行层）
- 遵循渐进式披露原则
- 持续维护踩坑清单（Gotchas Flywheel）

### 核心观点
- 每一段文字都有"Token 成本税"
- 优质 Skill 打磨起来很费时间
- 让大模型自己写 Skill，平均不会带来效果提升

## 关联连接
- [[AgentSkill]] — Perplexity 使用的 Skill 架构
- [[ProgressiveDisclosure]] — 三层加载机制
- [[摘要-perplexity-skill-practice]] — 来源文章摘要