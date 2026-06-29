---
title: "摘要-ai-agent-evaluation-quickstart-deepeval"
type: source
tags: [来源, Agent评估, DeepEval]
sources: [raw/03-transcripts/AI Agent Evaluation Quickstart  DeepEval - The LLM Evaluation Framework.md]
last_updated: 2026-06-21
---

## 核心摘要
DeepEval 的 Agent 评估快速入门指南。介绍了通过 Tracing（`@observe` 装饰器）对 Agent 进行端到端和组件级评估的方法：一次插装后每次运行生成 Trace，可在 Trace 级别（端到端）或 Span 级别（组件级，如 LLM 调用、工具调用、子 Agent）附加评估指标。支持 CI/CD 集成、多 Agent 系统和工具使用型 Agent 的评估。

## 关联连接
- [[DeepEval]] — 评估框架
- [[AgentEvaluation]] — Agent 评估方法论
- [[Trace]] — 核心评估数据结构
