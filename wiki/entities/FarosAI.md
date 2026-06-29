---
title: "FarosAI"
type: entity
tags: [研究机构, 工程效能分析, AI编码研究]
sources:
  [
    raw/01-articles/AI Native 时代为什么企业要建 Agent + 人 协作的软件交付流水线.md,
  ]
last_updated: 2026-06-05
---

## 定义

Faros AI 是一家工程效能分析平台，专注于量化软件研发团队的交付效能。2026年4月发布了迄今最大规模的企业级 AI 编码采用研究。

## 关键信息

**研究报告**："AI Coding at Scale: What 1,255 Teams Reveal About Enterprise AI Adoption"（2026年4月）

- 样本规模：1,255支团队、超万名开发者
- 结论标题：**"98% More PRs, Zero DORA Improvement"**

**核心数据：**

| 指标          | 数据     | 含义                           |
| ------------- | -------- | ------------------------------ |
| PR 合并量     | +98%     | 个体/团队级产出大幅提升        |
| PR 审查时间   | +91%     | 人类节点成为瓶颈               |
| 平均 PR 规模  | +154%    | AI生成代码块更大，审查难度上升 |
| DORA 指标     | 基本持平 | 公司级综合效能提升有限         |
| 人均 Bug 数量 | +9%      | AI辅助PR问题率更高             |
| 团队综合效能  | 约+15%   | 与个体+98%形成巨大落差         |

**核心结论**：AI 加速了代码生产，但同步放大了审查瓶颈，导致个体增益无法传导为组织效能提升。

## 关联连接

- [[摘要-ai-native-agent-pipeline]] — 来源文章
- [[ProductivityParadox]] — Faros AI 数据是该悖论的团队级证据
- [[DORAMetrics]] — Faros AI 研究的核心衡量框架
- [[NBER]] — 同期另一重要研究，个体视角
- [[AgentHumanPipeline]] — 问题的解决方案框架
