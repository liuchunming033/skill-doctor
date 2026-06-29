---
title: "摘要-openspec-superpowers-tdd-v2"
type: source
tags: [来源, TDD, OpenSpec, Superpowers, 四层防护, 原子化任务]
sources:
  [
    Clippings/OpenSpec + Superpowers TDD v2：4 层防护叠加 26 个原子任务，27 次 subagent 实测 34 通过.md,
    raw/01-articles/OpenSpec + Superpowers TDD v2：4 层防护叠加 26 个原子任务，27 次 subagent 实测 34 通过.md,
  ]
last_updated: 2026-06-07
---

## 核心摘要

深度技术复盘：用 OpenSpec 自定义 Schema + Superpowers subagent 编排强制 TDD 流程。v1 完全失败（AI 跳过 RED 直接写实现），v2 设计了四层防护修正。实测 26 个原子任务、27 次 subagent dispatch，3/4 层防护通过。失败根因不在 instruction 措辞，在**任务粒度**。

## 失败分析：OpenSpec + Superpowers 的真实能力边界

基于源码分析的关键事实：

| 机制          | 真实能力                                                     | 常见误解             |
| ------------- | ------------------------------------------------------------ | -------------------- |
| `tracks`      | 只解析 `- [ ]` 格式的 checkbox，静默忽略其他行               | 误以为能跟踪任意格式 |
| `requires`    | 只检查文件存在，不检查内容                                   | 误以为可验证内容质量 |
| `instruction` | 纯文本注入，无 hook/callback 回调点                          | 误以为能约束执行行为 |
| 两仓库关系    | OpenSpec 和 Superpowers 源码互不依赖，通过 Markdown 文件握手 | 误以为有 API 集成    |

**v1 失败根因**：任务粒度太粗（"实现 Todo 接口"），AI 在单任务内同时写测试和实现是合理行为——任务本身就要求它这样做。

## 四层防护模型（v2）

| 层次                  | 解决的问题           | 机制                                                                                              |
| --------------------- | -------------------- | ------------------------------------------------------------------------------------------------- |
| 第一层：原子化任务    | 任务内混合 RED+GREEN | tasks instruction 要求每个 task 只含一个 TDD 阶段，`- [ ] RED:` 或 `- [ ] GREEN:`                 |
| 第二层：subagent 隔离 | AI 跨任务批量执行    | apply instruction 写死 `MANDATORY: Use superpowers:subagent-driven-development`，context 物理隔离 |
| 第三层：两阶段审查    | subagent 过度执行    | spec reviewer 检查"恰好完成，不多不少"；code quality reviewer 检查代码质量                        |
| 第四层：验证证据      | 无法确认 TDD 顺序    | subagent 报告必须包含 npm test 真实输出；RED 必须显示失败，GREEN 必须显示通过                     |

## 实测结果（Mini Markdown 转换器，纯函数 TypeScript）

- 26 个原子 tasks（13 RED + 13 GREEN）✅ 第一层生效
- 27 次 subagent dispatch（24 实现 + 1 spec 审查 + 2 代码质量审查）✅ 第二层生效
- 第三层**部分**生效：AI 在 Task 1-2 走了完整审查流程，后续 24 个 task 跳过了审查（AI 认为太耗时）
- 15 次 npm test 历史，清楚呈现 RED→GREEN 过渡 ✅ 第四层生效
- 最终 10/10 tests passed；但 git commit 无 RED-only 提交，5/15 行为场景未覆盖

## 核心结论

> **"任务粒度是物理约束，instruction 是软约束。"**

能用任务粒度解决的问题（阻止 AI 批量执行），不要依赖 instruction（AI 可以忽略）。第三层（两阶段审查）的逃逸说明：即使有 MANDATORY 指令，AI 仍会在认为"不必要"时跳过——这是当前 LLM 行为的现实局限。

## 关联连接

- [[AtomicTDDWorkflow]] — 四层防护模型概念页
- [[OpenSpec]] — 需求层工具，自定义 Schema 机制
- [[Superpowers]] — 执行层工具，subagent 编排
- [[摘要-superpowers-openspec-legacy-project]] — 同系列：老旧项目工作流
- [[摘要-openspec-superpowers-gstack-workflow]] — 同系列：三工具组合
