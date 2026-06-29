---
title: "Claude"
type: entity
tags: [AI 模型, Anthropic]
sources: [raw/01-articles/01-SKILL到底是什么？精读《Equipping agents for the real world with Agent Skills》①.md]
last_updated: 2026-06-17
---

## 定义

Claude 是 Anthropic 公司开发的大语言模型系列，以安全性和可靠性为核心特征。Claude 系列包括 Claude 3.5 Sonnet、Claude 3 Opus 等版本，具备强大的对话、推理和任务执行能力。

## 关键信息

### 模型特点

- **对话能力强**：能够进行复杂对话，理解上下文和意图
- **推理能力突出**：在代码生成、分析推理等任务上表现优异
- **安全导向**：Anthropic 的核心理念体现在 Claude 的设计中，追求可靠、可解释的输出

### Agent 能力缺口

根据 Anthropic 官方文档，Claude 作为 Agent 在真实世界任务中存在两大缺口：

1. **缺乏过程知识**：不知道事情该怎么做（类似新员工不知道报销流程）
2. **缺乏组织背景**：不知道资源在哪里（类似新员工不知道 API 密钥位置）

### Skills 机制应用

- **动态加载 Skill**：Claude 根据任务主动发现相关 Skill，加载 SOP、脚本和模板
- **突破上下文限制**：通过动态加载机制，Claude 的智能边界不再受固定上下文窗口限制
- **任务专业化**：Skill 赋予 Claude 在特定场景（如分析财报、提取合同、生成合规文档）下的专业能力

### 产品形态

- **Claude 对话接口**：直接对话交互的 Web/API 形态
- **Claude Code**：AI 编程助手，内置 Skills 机制和工具调用能力

## 关联连接

- [[Anthropic]] — Claude 的开发公司
- [[摘要-skill-anthropic-doc-part1]] — Claude 能力缺口与 Skills 机制文档
- [[AgentSkill]] — Claude 突破能力瓶颈的核心机制