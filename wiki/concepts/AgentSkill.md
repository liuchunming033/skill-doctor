---
title: "AgentSkill"
type: concept
tags: [概念, Agent, Skill]
sources: [raw/01-articles/01-SKILL到底是什么？精读《Equipping agents for the real world with Agent Skills》①.md]
last_updated: 2026-06-17
---

## 定义

Agent Skill 是由 Anthropic 提出的核心概念，指由指令（Instructions）、脚本（Scripts）和资源（Resources）组成的结构化文件夹，智能体能够动态发现并加载这些内容，以提升特定任务的表现。Skill 是解决 Agent 从"会聊天"转向"能做事"的关键机制。

## 核心要素

### 三要素结构

- **Instructions**：相当于 SOP 文字，告诉 Agent 如何一步步完成任务
- **Scripts**：需要执行的 Python 文件或其他脚本
- **Resources**：执行过程中用到的配置文件或模板（JSON、docx 等）

### 解决的痛点

- **过程知识缺失**：由指令和脚本解决（告诉 Agent "怎么做")
- **组织背景缺失**：由资源解决（告诉 Agent "资源在哪")

## 关键特性

### 动态加载机制

Skill 不再固定在系统提示中，而是可被动态检索、挂载和使用：

- Agent 根据任务主动发现最相关的 Skill
- 加载其中的 SOP、脚本和模板
- 输出更精准、更一致、更可复现
- 突破上下文窗口限制，智能边界可扩展

### Skill vs Tool 的本质区别

| 维度 | Tool | Skill |
|------|------|-------|
| 回答的问题 | What（我能做什么） | How（我该如何做好） |
| 技术角色 | 执行代码 | 指导完成任务 |
| 粒度 | 原子化能力（API/函数） | 完整 SOP（指令+脚本+资源） |
| 行为模式 | 被动等待调用 | 主动指导 LLM 调用 Tool |
| 目标 | 提供原子能力 | 封装可复用的过程知识 |

**类比**：Tool 像烤箱（底层执行能力），Skill 像烤鸡食谱（封装全部过程知识——温度、时间、原料、诀窍）

### 系统架构中的位置

- **左侧 - Agent 配置（认知空间）**：LLM 是决策中心，配置中包含已装备技能清单
- **右侧 - Agent 虚拟机（执行空间）**：LLM 通过 Tool 指挥虚拟机读取 Skill 内容
- **交互机制**：虚拟机读取 SOP 返回上下文窗口，LLM 学习并决策下一步

## 应用场景

- **分析财报**：加载 PDF 分析 Skill，提取关键数据
- **提取合同字段**：加载合同解析 Skill，标准化提取字段
- **生成合规文档**：加载合规 Skill，生成符合规范文档
- **代码提交流程**：加载 Git Skill，执行标准提交流程

## 关联连接

- [[摘要-skill-anthropic-doc-part1]] — Skill 定义来源文档
- [[Anthropic]] — Skill 概念提出公司
- [[Claude]] — Skill 应用主体
- [[ProcessKnowledge]] — Skill 解决的痛点之一
- [[OrganizationalContext]] — Skill 解决的痛点之二
- [[DynamicLoading]] — Skill 的核心机制