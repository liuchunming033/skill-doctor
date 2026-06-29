---
title: "Knot"
type: entity
tags: [工具, 腾讯, 智能体平台, Agent部署]
created: 2026-06-21
updated: 2026-06-21
sources: [摘要-ai-agent-skill-测评方案及落地实践]
related: [TPerf, AgentEvaluation]
---

## 定义
Knot 是腾讯的智能体平台，支持 Agent 的部署和运行，通过 AG-UI 协议进行交互。TPerf AI 分析 Agent 部署在 Knot 上，其 Trace 数据通过 Knot API 获取。

## 关键能力

- **AG-UI 协议**：Agent 与前端界面之间通信格式的标准协议
- **会话管理**：通过 session_id + message_id 标识每次 Agent 执行
- **事件流**：提供工具调用事件、文本消息事件、时间消耗等结构化数据
- **API 查询**：支持通过 API 获取完整执行历史和 Trace

## 在 Agent 评估中的角色

- 基线数据来源：通过 Knot API 动态获取基线会话的完整数据（报告、步骤、耗时、Token）
- Trace 获取：AG-UI 事件流解析为结构化工具调用步骤列表

## 关联连接
- [[TPerf]] — 部署于 Knot 的 Agent
- [[AgentEvaluation]] — Agent 评估方法论
- [[Trace]] — 执行轨迹
