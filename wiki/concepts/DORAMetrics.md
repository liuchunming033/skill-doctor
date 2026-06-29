---
title: "DORAMetrics"
type: concept
tags: [DevOps, 工程效能, 度量指标, 软件交付]
sources:
  [
    raw/01-articles/AI Native 时代为什么企业要建 Agent + 人 协作的软件交付流水线.md,
  ]
last_updated: 2026-06-05
---

## 定义

DORA 指标（DevOps Research and Assessment Metrics）：由 DORA 研究团队（现隶属 Google Cloud）提出的四项核心软件交付效能指标，是业界衡量研发组织整体交付能力的标准框架。

## 关键信息

**四项核心指标：**

| 指标                                    | 含义                       |
| --------------------------------------- | -------------------------- |
| 部署频率（Deployment Frequency）        | 生产环境代码发布的频率     |
| 变更前置时间（Lead Time for Changes）   | 从代码提交到生产部署的时长 |
| 变更失败率（Change Failure Rate）       | 导致生产故障的变更比例     |
| 服务恢复时间（Time to Restore Service） | 生产故障的平均恢复时长     |

**在 AI 编码研究中的关键发现：**

[[FarosAI]] 对 1,255 支团队的研究：

- 高频 AI 使用团队 PR 合并量 **+98%**
- DORA 指标**基本持平**（几乎无改善）
- 结论：个体/团队级产出提升无法传导为组织级交付效能提升

**重要性**：DORA 指标是区分"个体效率幻觉"和"组织效能真实提升"的关键量尺。PR 数量增加不等于交付变好，DORA 指标才是最终裁判。

## 关联连接

- [[摘要-ai-native-agent-pipeline]] — 来源文章
- [[FarosAI]] — 在 AI 编码研究中使用 DORA 指标揭示组织落差
- [[ProductivityParadox]] — DORA 指标是量化悖论的核心工具
- [[AgentHumanPipeline]] — 该框架的目标之一是真正改善 DORA 指标
