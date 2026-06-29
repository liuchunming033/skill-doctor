---
title: "CodeBuddy"
type: entity
tags: [工具, 腾讯, 代码助手, AI编程]
created: 2026-06-21
updated: 2026-06-21
sources: [摘要-ai-agent-skill-测评方案及落地实践]
related: [TPerf, AgentEvaluation, Trace]
---

## 定义
CodeBuddy 是腾讯的 AI 代码助手，支持 `-p`（pipe）模式输出结构化的 JSONL 执行轨迹，在腾讯 Agent 测评体系中被用作 Rubric 评分器的 CLI 工具，调用大模型对 Agent 报告进行逐项对比评分。

## 关键能力

- **-p 模式**：以 JSONL 格式逐行输出完整执行轨迹（工具调用、思维链、时间戳）
- **Rubric 评分**：作为 CLI 工具被测评框架调用，让大模型充当评委对比基线报告与 Trial 报告

## 在 Agent 评估中的角色

- Trace 输出示例（被腾讯文档引用为结构化 Trace 的标准格式）
- Rubric 评分器的执行引擎

## 关联连接
- [[TPerf]] — 测评落地项目
- [[Trace]] — 执行轨迹格式
- [[Knot]] — 腾讯智能体平台
