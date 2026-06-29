---
title: "BaselineBasedEvaluation"
type: concept
tags: [Agent评估, 基线, 回归测试]
created: 2026-06-21
updated: 2026-06-21
sources: [摘要-ai-agent-skill-测评方案及落地实践]
related: [AgentEvaluation, CapabilityVsRegressionEval, Trace]
---

## 定义
基线评估方法（Baseline-Based Evaluation）是腾讯 TEG 团队实践的 Agent 评估核心方法。用例设计阶段只定义 prompt 和检查规则，不手写预期输出；而是先执行一次，人工确认正确后将这次完整的执行快照作为"预期基线"，后续每次评估都将本次执行与基线对比。

## 基线内容

**预期过程**（Agent 应该"怎么做"）：
- 思维链（CoT）
- 工具调用序列（工具名、调用顺序、入参和返回值）
- 中间产物
- 完整 Trace

**预期结果**（Agent 应该"产出什么"）：
- 最终响应文本
- 输出文件
- 输出报告/结构化数据

## 基线建立流程

1. 触发 Agent 执行一次
2. 获取执行标识（session_id + message_id）
3. 人工审核：确认步骤正确、结论准确、建议合理
4. 通过后，将本次执行快照记录为基线
5. 后续评估从 API 动态获取基线数据做对比

## 基线对比维度

| 对比维度 | 确定性判定 | Rubric 判定 |
|---------|-----------|------------|
| 过程对比 | 关键步骤缺失或顺序偏离 → 过程退化 | 思维链合理性、步骤最优性 |
| 结果对比 | 关键内容缺失或产物不一致 → 结果退化 | 结论准确性、表述完整性 |
| 效率对比 | 超出基线一定比例 → 效率退化 | — |

## 基线更新时机

- Agent/Skill 逻辑变更
- 模型版本升级
- 用例本身修改

## 关联连接
- [[AgentEvaluation]] — Agent 评估总论
- [[CapabilityVsRegressionEval]] — 能力评估 vs 回归评估
- [[Trace]] — 执行轨迹
