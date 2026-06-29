---
title: "摘要-rag-效果评估"
type: source
tags: [来源, RAG, 评估, Ragas]
sources: [raw/02-papers/RAG 效果评估.md]
last_updated: 2026-06-24
---

## 核心摘要
本文详细介绍 RAG（检索增强生成）系统的效果评估标准与方法。文章基于 Ragas 框架，系统讲解三大评估方式（人工打分/大模型打分/综合方式）、八大核心评估指标（检索器指标：上下文精度/召回率/实体召回率；生成器指标：忠实度/噪声敏感度/响应相关性/事实正确性/语义相似度），以及从评测集构建到执行评估的完整实操流程。文章还包含大量代码示例，展示如何用 Ragas + LangChain/LlamaIndex 生成评测集、选择评估器模型、执行评估并导出结果。

## 关联连接
- [[Ragas]] — RAG 评估框架
- [[RAGEvaluation]] — RAG 效果评估方法论
- [[HuggingFace]] — 数据集托管平台
- [[LangChain]] — LLM 应用框架
- [[LlamaIndex]] — 数据索引框架
- [[AgentEvaluation]] — Agent 评估方法论（通用）
