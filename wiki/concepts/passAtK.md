---
title: "passAtK"
type: concept
tags: [Agent评估, 指标, 非确定性]
created: 2026-06-21
updated: 2026-06-21
sources: [摘要-demystifying-evals-for-ai-agents, 摘要-ai-agent-skill-测评方案及落地实践]
related: [AgentEvaluation, CapabilityVsRegressionEval]
---

## 定义
衡量非确定性 Agent 表现的两种互补指标，源自 NeurIPS 论文。

## pass@k —— 衡量峰值能力

**pass@k** = k 次试验中**至少 1 次**通过的概率。

- 随着 k 增加，pass@k 上升（更多"射门机会"→ 更高命中概率）
- pass@1 = 50% 表示一半任务在第一次尝试就成功
- **适用场景**：编码 Agent（关心能否找到解）、创意生成（多个方案有一个可用即可）

## pass^k —— 衡量稳定性

**pass^k** = k 次试验中**每次都**通过的概率。

- 随着 k 增加，pass^k 下降（要求持续可靠是更难的挑战）
- 若每次试验 75% 成功率，pass^3 = (0.75)³ ≈ 42%
- **适用场景**：面向客户的 Agent（用户期望每次行为可靠）

## 关键分叉

pass@k 和 pass^k 在 k=1 时相等。到 k=10 时讲述相反故事：pass@k 接近 100% 而 pass^k 降至 0%。

## 腾讯实践的稳定性阈值

| Agent 类型 | pass^k 容忍阈值 | 说明 |
|-----------|---------------|------|
| 关键决策类 | 0%（N/N 全部通过） | 任何一次失败不可容忍 |
| 辅助分析类 | ≤ 10% | 偶发偏差可接受 |
| 创意生成类 | ≤ 40% | 输出多样性本身是特性 |

## 关联连接
- [[AgentEvaluation]] — Agent 评估总论
- [[CapabilityVsRegressionEval]] — 能力评估 vs 回归评估
