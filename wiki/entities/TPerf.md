---
title: "TPerf"
type: entity
tags: [工具, 腾讯, 性能测试, Agent评估]
created: 2026-06-21
updated: 2026-06-21
sources: [摘要-ai-agent-skill-测评方案及落地实践]
related: [Knot, AgentEvaluation, CodeBuddy]
---

## 定义
TPerf 是腾讯的性能测试平台，提供压测能力并集成了 AI 分析 Agent，能自动分析性能数据、识别资源瓶颈、输出优化建议。其 AI 分析 Agent 是腾讯 Agent 测评体系的落地验证项目。

## TPerf AI 分析 Agent

- **类型**：功能工具型 Agent
- **部署平台**：Knot 智能体平台
- **核心能力**：通过 MCP 工具调用 TPerf-API 获取性能数据，结合知识库检索进行深度分析，经决策树判断资源瓶颈点和压测有效性
- **调用链路**：用户压测 → Agent 自动触发分析 → MCP 拉取数据 → 知识库检索 → 输出结构化报告

## 测评实践

- 9 类场景 30+ 用例（CPU 瓶颈、网卡瓶颈、磁盘瓶颈等）
- 7 个模型对比评测
- 三层评分：操作步骤（LCS 对齐）+ 效率 + 报告质量（Rubric）
- CI 自动触发 + 定时巡检

## 关联连接
- [[Knot]] — 部署平台
- [[AgentEvaluation]] — Agent 评估方法论
- [[CodeBuddy]] — 用于 Rubric 评分的 CLI 工具
