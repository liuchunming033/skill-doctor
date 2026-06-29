---
title: "DeepEval"
type: entity
tags: [工具, Agent评估, LLM评估框架, 开源]
created: 2026-06-21
updated: 2026-06-21
sources: [摘要-ai-agent-evaluation-quickstart-deepeval]
related: [EvalHarness, AgentEvaluation, Trace]
---

## 定义
DeepEval 是一个 LLM 评估框架，提供 Agent 评估能力，包括端到端评估和组件级评估。通过 Trace 驱动的评估方式，一次插装后每次 Agent 运行都会生成 Trace，可在 Trace 级别（端到端）或 Span 级别（组件级）附加评估指标。

## 关键特性

- **@observe 装饰器**：一次插装，自动生成 Trace
- **Span 级别评估**：对 Agent 内部的每个组件（LLM 调用、工具调用、检索器、子 Agent）独立评分
- **CI/CD 集成**：通过 `evals_iterator()` 在持续集成中运行评估
- **多 Agent 支持**：支持多 Agent 系统和工具使用型 Agent

## 评估架构

1. 插装 Agent（`@observe` 或框架集成）
2. 每次运行生成 Trace（每个组件一个 Span）
3. 在 Trace/Span 级别附加评估指标
4. 从 Trace 自动构建测试用例

## 关联连接
- [[EvalHarness]] — 评估框架
- [[AgentEvaluation]] — Agent 评估方法论
- [[Trace]] — 执行轨迹
