---
title: "OpenAI"
type: entity
tags: [公司, AI 公司, GPT]
sources: [raw/01-articles/08-OpenAI：如何系统评估skill，证明它没被改坏？.md]
last_updated: 2026-06-18
---

## 定义

OpenAI 是一家专注于人工智能研究和开发的公司，开发了 GPT 系列大语言模型和 Codex 代码生成模型。OpenAI 在 Agent Skill 评估领域提出了系统化方法，强调通过证据闭环而非体感维护 Skill。

## 关键信息

### 公司定位

- **核心产品**：GPT 系列（GPT-4、GPT-3.5）、Codex 代码生成模型、ChatGPT
- **技术贡献**：大语言模型训练、代码生成、Agent 技能评估方法论

### Skill 评估贡献

OpenAI 发布文章《Testing Agent Skills Systematically with Evals》，提出系统评估 Skill 的方法论：

#### 定义成功的四类目标

- **结果目标（Outcome）**：任务有没有完成？应用能不能跑？
- **过程目标（Process）**：是否按预想步骤执行？验证行为路径本身
- **风格目标（Style）**：输出是否符合规范？保证下游可接受
- **效率目标（Efficiency）**：有无浪费？避免烧 token

#### 识别两个维护面

- **执行体**：instructions、工具链、步骤
- **触发边界**：name 和 description

两个维护面可独立失控，只盯执行体看不见触发边界腐烂。

#### 三类隐藏假设失控点

- **触发假设**：哪些 prompt 应触发却没触发？哪些误触发？
- **环境假设**：Skill 默认运行前提（最隐蔽，不在代码里在上下文里）
- **执行假设**：执行顺序是否正确？

#### 构建回归样本集

- 10~20 条 prompt 覆盖四类样本（显式/隐式/带上下文/负控）
- 重点不在数量，在能否卡住真实的失败模式

### 核心思想

**从靠体感维护换成靠最小证据闭环维护**。

Skill 一旦接入生产，不再只是 prompt 技巧，变成要被持续验证的工作流资产。维护资产至少回答三件事：
1. 想让它做成什么？
2. 它会在哪些地方失控？
3. 用哪些样本持续盯住失控点？

## 关联连接

- [[摘要-openai-skill-evaluation]] — Skill 评估方法来源文档
- [[SkillEvaluationFramework]] — OpenAI 提出的评估框架
- [[SkillFourSuccessGoals]] — 四类成功目标
- [[SkillThreeHiddenAssumptions]] — 三类隐藏假设
- [[GPT]] — OpenAI 开发的 AI 模型系列