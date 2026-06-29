---
title: "摘要-skill-课程-第1章"
type: source
tags: [来源, Skill课程, AgentSkill, 通用AI, 能力缺口]
created: 2026-06-18
updated: 2026-06-18
sources: [output/skill/01-为什么要学Skill.md]
related: [wiki/concepts/AgentSkill.md, wiki/concepts/ProcessKnowledge.md, wiki/concepts/OrganizationalContext.md]
---

## 核心摘要

本章是 Skill 课程的开篇，系统阐述通用 AI 智能体的两大核心缺口：程序性知识缺失（不知道事情怎么做）和结构化上下文缺失（不知道资源在哪）。传统靠 Prompt 碎片化定制存在三大致命缺陷（不可规模化、不可移植、无法沉淀），而 Anthropic 的 Agent Skills 正是专门解决这两类缺口的标准化方案。核心比喻：通用 Agent 是"聪明但没经验的新人"，Skill 是整套"岗位手册 + 工具包 + 资源库"。

## 关键洞察

### 通用 AI 的两类能力缺口

1. **程序性知识缺失**：不知道如何审查合同、排查故障、部署服务——这些需要经验、流程和判断标准
2. **结构化上下文缺失**：不知道数据库凭证在哪、团队规范是什么、监控仪表板 ID 是多少

### 传统 Prompt 的三大致命缺陷

- **不可规模化**：每个场景都要重写，维护成本随数量线性增长
- **不可移植**：换 AI 平台或换人就失效
- **无法沉淀**：经验、踩坑、最佳实践无法固化为组织资产

### Skill 的三大核心要素

- **SKILL.md（指令流程）**：补齐程序性知识缺失，告诉 AI 这件事具体怎么做
- **Scripts（可执行脚本）**：让任务执行高效、稳定、可复现
- **Resources（配套资源）**：补齐结构化上下文缺失，告诉 AI 工作需要的资源在哪里

### 核心定位

**Skill 不是锦上添花，而是通用智能体进入真实世界的最后一公里。**没有 Skill，通用 AI 只能做通用文本工作；有了 Skill，才能做专业领域的真实工作。

## 关联连接

- [[AgentSkill]] — Skill 的完整概念定义
- [[ProcessKnowledge]] — 程序性知识缺失问题
- [[OrganizationalContext]] — 结构化上下文缺失问题
- [[DynamicLoading]] — Skill 动态加载机制
- [[摘要-skill-anthropic-doc-part1]] — Anthropic 官方文档精读，Skill 核心概念来源
