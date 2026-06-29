---
title: "Playwright"
type: entity
tags: [工具, 测试, 浏览器自动化, E2E]
sources: ["raw/01-articles/Gstack的qa SKILL 的工作原理.md"]
last_updated: 2026-06-07
---

## 定义

Playwright 是 Microsoft 开源的端到端浏览器自动化框架，支持真实 Chromium/Firefox/WebKit 执行，原生支持截图、trace、视频、控制台日志和网络日志录制，失败可在 Playwright Trace Viewer 中逐步回放。

## 关键信息

**在 Gstack `/qa` 中的角色**：Playwright 是 `/qa` skill 的执行层，负责真实浏览器交互，不消耗 LLM Token。LLM 负责上层的场景推导和失败语义解释。

**Token 成本分配**：

| 阶段                             | 成本来源             |
| -------------------------------- | -------------------- |
| Playwright 执行（CPU/内存/时间） | **不消耗 LLM Token** |
| 场景推导、AC 映射                | LLM Token（大头）    |
| 失败归因、QA 报告生成            | LLM Token            |

**与传统 Playwright 的区别**：

| 传统 Playwright        | Gstack `/qa` 模式                 |
| ---------------------- | --------------------------------- |
| 开发者手写 `*.spec.ts` | 从 Spec/AC 自动推导场景           |
| 断言 DOM/URL/文本      | 断言 + 语义解释（是否满足需求）   |
| 失败输出堆栈           | 失败输出 QA 结论、原因、建议      |
| CI 导向                | Spec → Code → Validation 闭环导向 |

**企业实践**：将 `test-plan.md` 和 `tests/e2e/*.spec.ts` 缓存进仓库，后续 `/qa` 优先复用已有场景，只对 Git diff 影响范围做增量生成。CI 中高频执行 Playwright，LLM 只在失败时做解释与 triage。

## 关联连接

- [[Gstack]] — 在 `/qa` skill 中集成使用
- [[摘要-gstack-qa-skill-workflow]] — 来源
- [[AtomicTDDWorkflow]] — Build 阶段对应的测试机制
