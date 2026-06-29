---
title: "摘要-评测集生产pipeline设计"
type: source
tags: [来源, RAG, 评测集, Pipeline]
sources: [raw/02-papers/可信可持续演进的类RAG应用评测集生产 Pipeline 设计.md]
last_updated: 2026-06-24
---

## 核心摘要
本文是一份完整的类 RAG 应用评测集生产 Pipeline 工程设计方案，核心理念是"多轨并行、统一 Schema、自动为主、人工兜底"。文档定义了 6 种 GT（Ground Truth）样本类型——gold（人工锚点）/ synthetic（LLM合成主力）/ evidence（检索专用）/ process（推理步骤）/ adversarial（对抗边界）/ online_goodcase（线上回流），并设计了统一的评测样本 JSON Schema。重点包括：Agent 推理步骤 GT 的三种自动生成策略（SOP 自动生成/ Trace 反向抽象/ 工具调用约束）、adversarial GT 的 5 类系统性生成策略、三层 QC Gate 质量审核机制、线上 Goodcase 回流机制，以及 12 周 4 个 Epic 的实施路线图。

## 关联连接
- [[EvalDatasetEngineering]] — 评测集工程（含 Pipeline 架构与 GT 类型）
- [[AdversarialGT]] — 对抗样本 GT 生成策略
- [[RAGEvaluation]] — RAG 效果评估方法论
- [[AgentEvaluation]] — Agent 评估方法论
