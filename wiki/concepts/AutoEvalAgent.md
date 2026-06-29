---
title: "AutoEvalAgent"
type: concept
tags: [Agent评估, 运营Agent, 智能客服]
created: 2026-06-23
updated: 2026-06-23
sources: [摘要-ai评测ai-智能客服运营agent]
related: [AgentEvaluation, ContextEngineering, DeepThinkingMode, EvaluationStrategy]
---

## 定义
AutoEvalAgent（AI 评测 AI）是一种用 AI Agent 自动化评测其他 AI Agent 输出质量的工程模式。核心思路是构建一个专门的"运营 Agent"，让它扮演"裁判"角色，对目标 Agent（如智能客服）的对话质量进行端到端评估、根因归类和优化建议生成，形成"评估→诊断→优化"的自动化闭环。

## 核心架构：评估-诊断-优化三位一体

```
评估（Evaluation）
  • 端到端规则评测（语义相关性/表达质量/内容合规性/信息完整性）
  • 输出：BadCase 列表
    ↓
诊断（Diagnosis）
  • 按对话链路关键环节归因（知识召回/中控决策/LLM生成）
  • 十几种根因类别：粗召遗漏、精排问题、生成幻觉、生成错误、缺少知识等
    ↓
优化（Optimization）
  • 自动生成相似问 → 自动入库生效
  • 互联网检索补充知识 → 审核入库
  • Prompt/策略调整建议 → 运营/技术协作
    ↓
二次验证 → 持续闭环
```

## 关键工程实践

### 评测规则设计：正向+负向混合策略
纯负向评判会让 LLM 过度关注缺陷忽略整体价值，纯正向评判又过于宽松。采用"混合策略"：先找优点 → 再找缺点 → 综合权衡，既设明确的红线扣分点，也保留 LLM 的综合判断空间，更接近人类全面评估。

### 业务场景强依赖处理
- **两级诉求识别**：业务品类（一级）+ 业务场景（二级），将千奇百怪的用户问法映射到可枚举的业务范围
- **参考知识精准供给**：降低 RAG 召回阈值扩大 TopN，确保相关分片被覆盖，而非遍历全量知识文档
- **豁免机制**：特殊业务场景（如触发转人工/固定话术）的豁免判断独立抽取为前置逻辑，避免误判

### 工程可靠性
- **多 LLM 对抗**：2-3 个不同 LLM 执行相同 Prompt，统计学投票降低单一模型偏差
- **Checkpoint 恢复**：长时间运行任务的中断自动恢复，按阶段续跑而非从头开始
- **并发限流**：控制线程并发数 + max_tokens 限制输出，应对 QPM/TPM 限流

### 实际效果
BadCase 发现准确率 85%+，根因归类和优化建议生成准确率 80%+，大幅节省人工运营成本。

## 关联连接
- [[AgentEvaluation]] — Agent 评估总论
- [[ContextEngineering]] — 上下文工程
- [[DeepThinkingMode]] — 深度思考模式
- [[EvaluationStrategy]] — 评估策略（含闭环策略）
- [[GraderTypes]] — 评分器类型（含多LLM对抗方案）
