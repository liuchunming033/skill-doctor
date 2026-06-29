---
title: "ProcessKnowledge"
type: concept
tags: [概念, Agent, 过程知识]
sources: [raw/01-articles/01-SKILL到底是什么？精读《Equipping agents for the real world with Agent Skills》①.md]
last_updated: 2026-06-17
---

## 定义

过程知识（Process Knowledge）是指完成某项任务所需的标准流程、操作步骤和经验诀窍。对于 AI Agent 而言，过程知识的缺失表现为"不知道事情该怎么做"，类似新员工不知道报销流程、代码提交流程等 SOP。

## 核心特征

### 缺失的表现

- 不知道任务的标准流程（如报销流程是什么）
- 不知道操作的先后顺序（如代码提交的步骤）
- 不知道关键的检查点（如发布前需要哪些验证）
- 不知道经验性的诀窍（如如何避免常见错误）

### 与组织背景的区别

- **过程知识**：关注"如何做"（流程、步骤、方法）
- **组织背景**：关注"在哪里"（资源位置、工具配置）

## Skill 如何解决

Agent Skill 通过以下方式解决过程知识缺失：

- **Instructions**：提供完整的 SOP 文字指导，告诉 Agent 如何一步步完成任务
- **Scripts**：提供可执行的脚本，自动执行标准化流程
- **组合效果**：指令描述流程，脚本执行流程，共同弥补过程知识缺口

## 类比理解

类比新员工入职第一天：
- **聪明**：具备理解能力和逻辑推理能力（类似 LLM 的对话能力）
- **缺乏过程知识**：不知道报销流程、代码提交规范、会议预定流程等
- **需要培训**：需要老员工传授 SOP，或者阅读手册学习流程

## 关联连接

- [[摘要-skill-anthropic-doc-part1]] — 过程知识概念来源
- [[AgentSkill]] — 解决过程知识缺失的核心机制
- [[OrganizationalContext]] — Agent 缺失的另一能力