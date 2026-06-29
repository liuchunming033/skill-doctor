---
title: "摘要-demystifying-evals-for-ai-agents"
type: source
tags: [来源, Agent评估, Anthropic]
sources: [raw/03-transcripts/Demystifying evals for AI agents.md]
last_updated: 2026-06-21
---

## 核心摘要
Anthropic 工程师团队撰写的 Agent 评估权威指南。系统阐述了 Agent 评估的结构（任务、试验、评分器、转录本、结果、评估套件）、三类评分器（代码级、模型级、人工级）的优劣与组合方式、能力评估 vs 回归评估的区分、以及针对编码/对话/研究/计算机使用四类 Agent 的评估策略。提出了从零到一的 8 步评估路线图，强调"尽早开始、从手工测试转化、写无歧义任务、构建平衡用例集、设计稳健评估框架、读转录本、监控饱和、长期维护"。还介绍了 pass@k 和 pass^k 两个非确定性度量指标。

## 关联连接
- [[Anthropic]] — 发布机构
- [[AgentEvaluation]] — Agent 评估方法论
- [[EvalHarness]] — 评估框架
- [[passAtK]] — 非确定性评估指标
- [[CapabilityVsRegressionEval]] — 两类评估范式
- [[GraderTypes]] — 三类评分器
