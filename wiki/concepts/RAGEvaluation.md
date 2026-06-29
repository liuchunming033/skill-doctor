---
title: "RAGEvaluation"
type: concept
tags: [RAG, 评估, 检索增强生成, Ragas]
created: 2026-06-24
updated: 2026-06-24
sources: [摘要-rag-效果评估]
related: [Ragas, AgentEvaluation, EvalDatasetEngineering, GraderTypes]
---

## 定义
RAG 效果评估是对检索增强生成（RAG）系统输出质量的系统化评测。通过统一的评估标准，公平、客观地比较不同 RAG 系统及其优化方法，帮助开发者发现系统优劣并为后续改进提供依据。

## 评估方式

三种方式及其适用场景：
- **人工打分**：精确、细致，擅长检测细微错误和幻觉，但耗时较长、成本高
- **大模型打分**：效率高，可快速处理大规模评估任务，但存在模型偏差
- **综合方式**：全量样本大模型打分 + 部分样本人工打分，充分利用两者优势

## 评估流程

1. 评测需求分析
2. 评测数据集构建（从 HuggingFace 加载 / 从文档自动生成 / 手工构建 SingleTurnSample）
3. 执行评测（选择评估器 LLM + 评估指标）
4. 分析评测数据
5. 出具评测报告

## 核心评估指标（基于 Ragas）

### 检索器指标
| 指标 | 含义 | 评估关系 |
|------|------|---------|
| Context Precision | 检索上下文与问题的相关程度 | question → context |
| Context Recall | 检索器获取所有必要信息的能力 | context → ground_truth |
| Context Entities Recall | 检索上下文中实体的召回率 | context 实体 → reference 实体 |

### 生成器指标
| 指标 | 含义 | 评估关系 |
|------|------|---------|
| Faithfulness | 答案与上下文的事实一致性 | context → answer |
| Noise Sensitivity | 不相关文档导致错误响应的频率 | context → answer |
| Response Relevancy | 答案与问题的相关程度 | question → answer |
| Factual Correctness | 答案与参考信息的事实准确度 | answer → ground_truth |
| Answer Semantic Similarity | 答案与真实答案的语义相似度 | answer → ground_truth |

### 关键计算方式
- **Faithfulness**：将答案拆解为独立陈述语句，逐一检查是否能从上下文中推断，得分 = 可从上下文推断的陈述数 / 总陈述数
- **Response Relevancy**：从答案反向推导 N 个问题变体，计算与实际问题的平均余弦相似度
- **Factual Correctness**：将响应和参考答案分别分解为主张（Claims），用 Precision / Recall / F1 量化事实重叠

## 与 Agent 评估的关系
RAG 评估是 Agent 评估的一个重要子领域。RAG 系统的检索-生成两阶段架构使其评估天然分为检索器评估和生成器评估。Agent 评估中关于评测集工程、评分器设计、人工/AI 分工的方法论同样适用于 RAG 评估。

## 关联连接
- [[Ragas]] — RAG 评估框架
- [[AgentEvaluation]] — Agent 评估方法论
- [[EvalDatasetEngineering]] — 评测集工程
- [[GraderTypes]] — 三类评分器
