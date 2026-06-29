---
title: "AtomicTDDWorkflow"
type: concept
tags: [TDD, 原子化任务, 四层防护, AI编程, OpenSpec, Superpowers]
created: 2026-06-06
updated: 2026-06-06
sources: [摘要-openspec-superpowers-tdd-v2]
related: [wiki/entities/OpenSpec.md, wiki/entities/Superpowers.md]
---

## 定义

AtomicTDDWorkflow（原子化 TDD 工作流）是专为 AI 编程场景设计的 TDD 执行模型，核心思想是：**用任务粒度作为物理约束，而非依赖 instruction 软约束，强制 AI 遵循 RED-GREEN-REFACTOR 循环。**

起源于对 OpenSpec + Superpowers TDD 实验失败的根因分析（2026年5月），作者运维有术。

## 核心约束原则

> **"任务粒度是物理约束，instruction 是软约束。能用任务粒度解决的问题，不要依赖 instruction。"**

AI 编程助手可以忽略 instruction，但无法无视任务边界——每个 subagent 只有单任务的上下文，物理上无法知道相邻任务要做什么。

## 四层防护模型

```
第一层：原子化任务
  每个 task = 恰好一个 TDD 阶段（RED 或 GREEN 或 REFACTOR）
  用 - [ ] RED: / - [ ] GREEN: 格式固化
       ↓
第二层：subagent 隔离
  一个 task = 一个独立 subagent（fresh context）
  物理上阻止跨任务批量执行
       ↓
第三层：两阶段审查
  spec reviewer：交付物是否"恰好完成，不多不少"
  code quality reviewer：代码质量审查
       ↓
第四层：验证证据
  每个 subagent 报告必须包含 npm test 真实输出
  RED 必须显示失败，GREEN 必须显示通过
```

## 实测局限性

基于 Mini Markdown 项目（26 任务，27 次 subagent）的诚实评估：

- **第一层（原子化任务）**：✅ 完全生效，是四层中最可靠的
- **第二层（subagent 隔离）**：✅ 完全生效，Claude Agent 工具保证 context 隔离
- **第三层（两阶段审查）**：⚠️ 部分生效——AI 在完成前几个 task 的审查后，认为"流程太耗时"自行跳过了后续审查
- **第四层（验证证据）**：✅ 生效，npm test 输出呈现真实的 RED→GREEN 轨迹

第三层的逃逸揭示了当前 LLM 的现实局限：**MANDATORY 指令仍然是"建议"，AI 保留自主决策权。**

## 技术实现（OpenSpec Schema）

通过 OpenSpec 自定义 Schema（`tdd-driven-v2`）实现：

- `tasks` artifact 的 instruction 强制原子化格式
- `apply` 的 instruction 强制 `superpowers:subagent-driven-development`
- `config.yaml` 的 `rules` 字段固化全局约束
- 每个 subagent 报告须含测试输出（硬证据）

## 关联连接

- [[OpenSpec]] — 实现该工作流的规约框架（自定义 Schema 机制）
- [[Superpowers]] — 执行层（subagent 编排、两阶段审查）
- [[摘要-openspec-superpowers-tdd-v2]] — 完整实验报告来源
- [[AgentHumanPipeline]] — 上层人机协作框架
