---
title: "OrganizationalContext"
type: concept
tags: [概念, Agent, 组织背景]
sources: [raw/01-articles/01-SKILL到底是什么？精读《Equipping agents for the real world with Agent Skills》①.md]
last_updated: 2026-06-17
---

## 定义

组织背景（Organizational Context）是指特定组织环境中的资源位置、工具配置、项目信息和上下文关系。对于 AI Agent 而言，组织背景的缺失表现为"不知道东西在哪里"，类似新员工不知道 API 密钥位置、模板路径、项目文档地址等。

## 核心特征

### 缺失的表现

- 不知道资源存储位置（如 API 密钥在哪里）
- 不知道模板文件路径（如 PPT 模板、合同模板在哪）
- 不知道项目文档地址（如需求文档、设计文档在哪）
- 不知道工具配置信息（如数据库连接、测试环境配置）

### 与过程知识的区别

- **组织背景**：关注"在哪里"（资源位置、工具配置）
- **过程知识**：关注"如何做"（流程、步骤、方法）

## Skill 如何解决

Agent Skill 通过以下方式解决组织背景缺失：

- **Resources**：提供配置文件、模板、示例等资源文件
- **路径信息**：在 Instructions 或 Resources 中明确资源位置
- **组合效果**：直接提供资源文件或指引路径，弥补组织背景缺口

## 类比理解

类比新员工入职第一天：
- **聪明**：具备理解能力和逻辑推理能力（类似 LLM 的对话能力）
- **缺乏组织背景**：不知道 API 密钥在哪里、模板路径是什么、项目文档在哪个目录
- **需要指引**：需要老员工指点资源位置，或者查阅组织资源目录

## 关联连接

- [[摘要-skill-anthropic-doc-part1]] — 组织背景概念来源
- [[AgentSkill]] — 解决组织背景缺失的核心机制
- [[ProcessKnowledge]] — Agent 缺失的另一能力