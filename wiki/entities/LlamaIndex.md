---
title: "LlamaIndex"
type: entity
tags: [框架, RAG, 数据索引]
created: 2026-06-24
updated: 2026-06-24
sources: [摘要-rag-效果评估]
related: [Ragas, LangChain, RAGEvaluation]
---

## 定义
LlamaIndex 是一个用于构建 RAG 应用的数据索引框架，提供文档加载、索引构建、查询引擎等核心功能。在 RAG 评估场景中，LlamaIndex 可通过 `SimpleDirectoryReader` 加载文档，并通过 `LlamaIndexLLMWrapper` 集成到 Ragas 评估流程中。

## 关联连接
- [[Ragas]] — 与其集成的 RAG 评估框架
- [[LangChain]] — 同类 LLM 应用框架
- [[RAGEvaluation]] — RAG 效果评估方法论
