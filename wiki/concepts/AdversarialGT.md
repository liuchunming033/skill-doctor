---
title: "AdversarialGT"
type: concept
tags: [评测集, 对抗样本, RAG, 质量保障]
created: 2026-06-24
updated: 2026-06-24
sources: [摘要-评测集生产pipeline设计]
related: [EvalDatasetEngineering, RAGEvaluation, AgentEvaluation]
---

## 定义
Adversarial GT（对抗样本 Ground Truth）是专门设计用于测试 RAG/Agent 系统在"不能答"的情况下能否"不乱答"的评测样本。其核心目标是评估系统的幻觉抑制与安全能力，测试系统是否会：编造不存在的事实、忽略证据缺失或冲突、对不确定信息给出过度确定的答案。

## 设计原则

1. 不是随机刁难，而是系统性覆盖失败模式
2. 生成必须基于真实知识边界（KB / Evidence）
3. 自动生成 ≠ 自动入库，必须过 QC Gate

## 五种生成策略

### A 类：不存在的事实（Non-existent Fact）
测试系统是否会凭空编造事实。
- 从 KB 中选实体 → 构造 KB 时间轴之外 / 文档中不存在的事件
- 典型问题："系统 A 在 2026 年发生过哪些 P0 事故？"

### B 类：证据缺失（Evidence Missing）
测试系统是否会在没有证据时仍然给出答案。
- 从现有 QA / Gold GT 出发 → 移除 supporting evidence → 保留问题不变
- 标注为"不可回答"

### C 类：边界模糊（Boundary / Ambiguous）
测试系统是否过度确定。
- 找到包含"通常""大约""可能"等模糊词的文档 → 构造强确定性问法
- 典型问题："系统 B 的恢复时间是否一定是 1 小时？"

### D 类：多证据冲突（Conflicting Evidence）
测试系统是否忽略冲突、强行给结论。
- 检索同一实体的相互矛盾文档 → 构造需要"选边站"的问题

### E 类：诱导式推断（Implicit Assumption Trap）
测试系统是否默认用户前提是对的。
- 构造问题中隐含未给定前提，前提在 KB 中未被证实
- 典型问题："系统 C 迁移到云原生架构后，性能提升了多少？"

## GT 构造规则

所有 Adversarial GT 固定模板：
```json
{
  "gt_type": "adversarial",
  "answer_gt": "在当前提供的资料中，无法找到支持该问题的相关信息，因此无法回答。",
  "evidence_gt": [],
  "difficulty": "mid | hard"
}
```

禁止生成"猜测型 answer_gt"。

## 自动 QC Gate（三层）

- **Gate-1（硬门槛）**：结构合法 + 可评测性
- **Gate-2（核心质量）**：不可回答性验证（LLM Judge）+ 诱导强度检查 + 去重与多样性
- **Gate-3（人工兜底）**：业务可信度

## 关联连接
- [[EvalDatasetEngineering]] — 评测集工程与 Pipeline
- [[RAGEvaluation]] — RAG 效果评估
- [[AgentEvaluation]] — Agent 评估方法论
