---
title: "Ragas"
type: entity
tags: [评估框架, RAG, 开源]
created: 2026-06-24
updated: 2026-06-24
sources: [摘要-rag-效果评估]
related: [RAGEvaluation, AgentEvaluation, HuggingFace]
---

## 定义
Ragas 是一个开源的 RAG（检索增强生成）系统评估框架，提供一组标准化的评估指标（Metrics），用于衡量 RAG 应用的检索和生成性能。它支持从 HuggingFace Datasets 加载评测集、从文档自动生成测试集，以及与 LangChain / LlamaIndex 等框架集成。

## 核心评估指标

### 检索器相关
- **Context Precision（上下文精度）**：检索到的上下文与用户问题的相关程度，相关度高的排在前面
- **Context Recall（上下文召回率）**：检索器检索到所有必要信息以回答用户问题的能力
- **Context Entities Recall（上下文实体召回率）**：检索到的上下文中实体的召回率

### 生成器相关
- **Faithfulness（忠实度）**：答案与给定上下文的事实一致性，将答案拆解为陈述语句后逐一核查
- **Response Relevancy（响应相关性）**：通过从答案反向推导问题变体，计算与实际问题的平均余弦相似度
- **Noise Sensitivity（噪声敏感度）**：系统在使用相关/不相关文档时给出错误响应的频率，分数越低越好
- **Factual Correctness（事实正确性）**：响应与参考信息的事实重叠度，支持 Precision / Recall / F1 三种模式
- **Answer Semantic Similarity（答案语义相似度）**：使用交叉编码模型计算生成答案与真实答案的余弦相似度

## 评测集生成
Ragas 提供从文档到测试集的全链路支持：
1. 加载文档 → 创建知识图谱（KnowledgeGraph）
2. 应用变换（Transforms）丰富知识图谱
3. 定义查询分布（单跳具体/多跳抽象/多跳具体，默认权重 0.5/0.25/0.25）
4. 生成测试集（指定 testset_size）

## 关联连接
- [[RAGEvaluation]] — RAG 效果评估方法论
- [[AgentEvaluation]] — Agent 评估方法论
- [[HuggingFace]] — 数据集平台
- [[DeepEval]] — 另一个 LLM 评估框架
