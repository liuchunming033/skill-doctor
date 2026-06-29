---
title: "摘要-skill-anthropic-doc-part1"
type: source
tags: [来源, Agent Skill, Anthropic]
sources: [raw/01-articles/01-SKILL到底是什么？精读《Equipping agents for the real world with Agent Skills》①.md]
last_updated: 2026-06-17
---

## 核心摘要

本文精读 Anthropic 官方文档《Equipping agents for the real world with Agent Skills》第一部分，指出 AI Agent 从"会聊天"转向"能做事"的关键瓶颈：缺乏过程知识（不知道如何做）和组织背景（不知道资源在哪）。Skill 作为解决方案，通过指令、脚本、资源三要素动态加载，赋予 Agent 在特定场景下的专业能力，突破上下文窗口限制。

## 关键洞察

### Agent 的两大能力缺口

1. **过程知识缺失**：类似新员工不知道报销流程、代码提交流程等 SOP
2. **组织背景缺失**：类似新员工不知道 API 密钥、模板等资源位置

### Skill 的三要素

- **Instructions**：SOP 文字指导，告诉 Agent 如何完成任务
- **Scripts**：可执行的 Python 文件
- **Resources**：配置文件或模板（JSON、docx 等）

### Skill vs Tool 的核心区别

| 维度 | Tool | Skill |
|------|------|-------|
| 回答的问题 | What（我能做什么） | How（我该如何做好） |
| 技术角色 | 执行代码 | 指导完成任务 |
| 粒度 | 原子化能力（API/函数） | 完整 SOP（指令+脚本+资源） |
| 行为模式 | 被动等待调用 | 主动指导 LLM 调用 Tool |
| 目标 | 提供原子能力 | 封装可复用的过程知识 |

### 关键特性：动态加载

Skill 不固定在系统提示中，而是可被动态检索、挂载和使用。Agent 根据任务主动发现相关 Skill，加载 SOP、脚本和模板，使输出更精准、可复现。

### 系统架构

- **右侧 - Agent 虚拟机（执行空间）**：包含 Bash、Python 等执行引擎，Agent 通过它操作文件、运行脚本
- **左侧 - Agent 配置（认知空间）**：LLM 是决策中心，包含系统提示和已装备技能清单。LLM 通过 Tool 指挥虚拟机读取 SOP，内容返回上下文窗口供学习决策

## 关联连接

- [[Anthropic]] — 文档来源公司
- [[AgentSkill]] — 本文核心概念
- [[ProcessKnowledge]] — Agent 缺失的能力之一
- [[OrganizationalContext]] — Agent 缺失的能力之二
- [[DynamicLoading]] — Skill 的关键机制