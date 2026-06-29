---
title: "LangChain"
type: entity
tags: [框架, LLM, 工具]
created: 2026-06-24
updated: 2026-06-24
sources: [摘要-rag-效果评估]
related: [Ragas, LlamaIndex, AgentEvaluation]
---

## 定义
LangChain 是一个用于构建 LLM（大语言模型）应用的开源框架，提供模型调用、提示模板、链式调用、工具集成等核心抽象。在 RAG 评估场景中，LangChain 常作为 Ragas 的 LLM 交互后端，通过 `LangchainLLMWrapper` 将各类 LLM（OpenAI / 通义千问等）接入评估流程。

## 关联连接
- [[Ragas]] — 与其集成的 RAG 评估框架
- [[LlamaIndex]] — 同类 LLM 应用框架
