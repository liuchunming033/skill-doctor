---
title: "摘要-skill-课程-第2章"
type: source
tags: [来源, Skill课程, AgentFourComponents, Prompt, Subagent, MCP]
created: 2026-06-18
updated: 2026-06-18
sources: [output/skill/02-四大组件扫盲.md]
related: [wiki/concepts/AgentFourComponents.md, wiki/concepts/AgentSkill.md, wiki/concepts/SkillAndMCP.md]
---

## 核心摘要

本章系统厘清 AI 工作流的四大组件：Prompt（一次性临时指令）、Skill（可复用专业能力库）、Subagent（独立专项 AI 助手）、MCP（外部数据通道）。四者各司其职互不重叠，并给出组合口诀与选择决策树。核心强调 Skill 与 MCP 的互补关系：Skill 提供方法论（How），MCP 提供资源连接（What），两者结合才是完整能力。

## 关键洞察

### 四大组件定位总览

| 组件 | 核心定位 | 特点 |
|------|---------|------|
| **Prompt** | 一次性临时指令 | 临时性、不可复用 |
| **Skill** | 可复用专业能力库 | 可复用、可迭代、可移植 |
| **Subagent** | 独立专项 AI 助手 | 隔离性、专项性、独立上下文 |
| **MCP** | 外部数据通道 | 连接性、资源访问 |

### 组合口诀

**单次微调用 Prompt，通用能力沉淀用 Skills，独立专项任务用子智能体，外部数据接入靠 MCP。**

### Skill 与 MCP 的互补关系

- Skill 提供"方法论"（How）：指导 AI 如何审查合同、分析数据、排查故障
- MCP 提供"资源连接"（What）：连接数据库、访问合同管理系统、接入监控仪表板
- **两者组合 = 既懂方法又能执行的完整能力**

### 选择决策树

1. 一次性任务 → Prompt
2. 需要长期复用沉淀 → Skill
3. 需要独立上下文隔离 → Subagent
4. 需要连接外部数据源 → MCP

## 关联连接

- [[AgentFourComponents]] — 四大组件框架概念
- [[AgentSkill]] — Skill 的完整定义
- [[SkillAndMCP]] — Skill 与 MCP 互补关系
- [[摘要-agent-four-components]] — Agent 四大组件定位与联动详解
