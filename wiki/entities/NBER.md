---
title: "NBER"
type: entity
tags: [研究机构, 经济研究, AI编码研究]
sources:
  [
    raw/01-articles/AI Native 时代为什么企业要建 Agent + 人 协作的软件交付流水线.md,
  ]
last_updated: 2026-06-05
---

## 定义

美国全国经济研究局（National Bureau of Economic Research），非营利学术研究机构，与 MIT、UPenn 合作发布了迄今最大规模的 AI 编码生产力实证研究。

## 关键信息

**Working Paper 35275**（2026年5月）：

- 研究团队：Mert Demirer, Leon Musolff, Liyuan Yang（MIT + UPenn）
- 样本规模：10万+ GitHub 开发者
- 研究对象：三代 AI 编码工具（Autocomplete → Sync Agent → Async Agent）

**核心衰减路径（六层产出指标）：**

| 产出指标   | Autocomplete | Sync Agent | Async Agent |
| ---------- | ------------ | ---------- | ----------- |
| 代码行数   | +228%        | +741%      | +1730%      |
| 提交次数   | +36%         | +140%      | +180%       |
| 版本发布数 | +10%         | +30%       | **+30%**    |

**核心结论**：AI 生成能力越强，从代码到发布的衰减越剧烈。Async Agent 代码提交 +180%，但版本发布仅 +30%——生产链条每一层级的人类瓶颈将上游增益逐级吞噬。

## 关联连接

- [[摘要-ai-native-agent-pipeline]] — 来源文章
- [[ProductivityParadox]] — NBER 数据是该悖论的核心实证
- [[AgentHumanPipeline]] — NBER 衰减数据支撑了流水线必要性的论证
- [[FarosAI]] — 同期另一重要研究机构，团队级视角
