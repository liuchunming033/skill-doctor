---
title: "摘要-解读-anthropic-demystifying-evals"
type: source
tags: [来源, Agent评估, Anthropic, 中文解读]
sources: [raw/02-papers/解读Anthropic _ Demystifying evals for AI agents.md]
last_updated: 2026-06-21
---

## 核心摘要
对 Anthropic《Demystifying evals for AI agents》的中文深度解读，不仅翻译原文，更增加了大量结构化拆解：8 个评估概念的一对一详解与关系图、错误传播累积机制图示、三类评分器的决策树与三层评估流水线架构、LLM-as-Judge 的 5 种校准方法、能力评估与回归评估的"毕业"机制、四种 Agent 类型（编码/对话/研究/计算机操作）的评估策略拆解、非确定性度量的 pass@k/pass^k 详细示例、8 步构建路线图的分步注解、以及 6 种评估方法的 Swiss Cheese Model 组合策略。

## 关联连接
- [[AgentEvaluation]] — Agent 评估核心概念
- [[GraderTypes]] — 三类评分器（本文含三层流水线架构）
- [[EvalHarness]] — 评估框架（本文含环境隔离详解）
- [[CapabilityVsRegressionEval]] — 能力vs回归评估
- [[passAtK]] — 非确定性度量
- [[Anthropic]] — 原文来源
