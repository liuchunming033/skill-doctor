---
title: "摘要-agent-evaluation-a-detailed-guide"
type: source
tags: [来源, Agent评估, 实践指南]
sources: [raw/03-transcripts/Agent Evaluation A Detailed Guide.md]
last_updated: 2026-06-21
---

## 核心摘要
Cameron R. Wolfe 撰写的 Agent 评估综合指南。从评估基础概念（Eval = 输入 → 执行 → 评分）出发，深入探讨了：Agent 评估为何比传统 LLM 评估更难（多步交互、状态变异、非确定性）；三类评估方法（直接评分、LLM-as-Judge、人工评估）的适用场景与局限；评估标准的选择（正确性、效率、安全性、用户体验）；以及评估基础设施（Harness、环境隔离、并发执行）的设计考量。还介绍了 SWE-bench、WebArena、τ-bench 等主流 Agent 基准测试。

## 关联连接
- [[AgentEvaluation]] — Agent 评估方法论
- [[EvalHarness]] — 评估框架
- [[GraderTypes]] — 三类评分器
- [[SWE-bench]] — 编码 Agent 基准
- [[CameronRWolfe]] — 作者
