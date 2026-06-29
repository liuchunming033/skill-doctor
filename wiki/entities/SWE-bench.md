---
title: "SWE-bench"
type: entity
tags: [基准测试, Agent评估, 编码Agent]
created: 2026-06-21
updated: 2026-06-21
sources: [摘要-agent-evaluation-a-detailed-guide, 摘要-demystifying-evals-for-ai-agents]
related: [AgentEvaluation, CapabilityVsRegressionEval]
---

## 定义
SWE-bench 是广泛使用的编码 Agent 基准测试。SWE-bench Verified 版本给 Agent 分配来自流行 Python 仓库的 GitHub Issues，通过运行测试套件来评分：只有在不破坏已有测试的前提下修复了失败测试的解决方案才算通过。LLM 在该基准上一年内从 40% 提升至 >80%，接近饱和。

## 关键特征

- **确定性评分**：代码能否运行、测试是否通过
- **任务来源**：真实开源项目的 GitHub Issues
- **SWE-bench Verified**：经过人工验证的高质量子集
- **参考价值**：是能力评估→回归评估转化的典型示例

## 关联连接
- [[AgentEvaluation]] — Agent 评估方法论
- [[CapabilityVsRegressionEval]] — 评估范式
