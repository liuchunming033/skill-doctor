---
title: "摘要-gstack-qa-skill-workflow"
type: source
tags: [来源, Gstack, QA, Playwright, AI测试]
sources: ["raw/01-articles/Gstack的qa SKILL 的工作原理.md"]
last_updated: 2026-06-07
---

## 核心摘要

Gstack 的 `/qa` skill 是"Spec 驱动 + Playwright 执行 + LLM 评审"的双阶段 QA 流水线。真正执行浏览器交互的是 Playwright（真实 Chromium），不消耗 LLM Token；LLM 的职责是读取 Design Doc/AC 推导测试场景、选择覆盖路径，以及对失败做语义归因并生成 QA 结论报告。有 Plan-first（复用已有 test-plan，低 Token）和 Agent-first（从需求重新推导，高 Token）两种模式，企业实践推荐将测试场景和 Playwright 脚本缓存在仓库，仅对 Git diff 范围做增量生成，CI 中高频执行 Playwright，LLM 只在失败时介入做解释与 triage。

## 关联连接

- [[Gstack]] — 该 skill 所属工具
- [[Playwright]] — QA 阶段的真实浏览器执行引擎
- [[Superpowers]] — Gstack 的搭档插件，处理 Build 阶段工程纪律
- [[AtomicTDDWorkflow]] — Build 阶段 TDD 的对应机制
