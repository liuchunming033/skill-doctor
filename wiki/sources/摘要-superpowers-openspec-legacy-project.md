---
title: "摘要-superpowers-openspec-legacy-project"
type: source
tags: [来源, 原始文件, 老旧项目, AI编程, 规约驱动]
sources:
  [Clippings/从古法编程到 AI 编程：Superpowers + OpenSpec 协同开发实战指南.md]
last_updated: 2026-06-06
---

## 核心摘要

专门面向老旧项目引入 AI 编程的实战指南：用 OpenSpec（需求层）+ Superpowers（执行层）的双层架构，设计一套 3 人团队的四阶段闭环工作流（旧代码分析→需求规约→代码生成→协同同步）。核心价值是"规范先行"——先让 AI 和人在文字层面对需求达成共识，再进入受控的执行流程。

## 双层分工

| 工具                         | 层次   | 解决什么问题                                                            |
| ---------------------------- | ------ | ----------------------------------------------------------------------- |
| **OpenSpec**（40.9k Star）   | 需求层 | AI 理解需求不准确；规范先于代码，Token 消耗降低 30-50%，返工率下降 60%+ |
| **Superpowers**（158k Star） | 执行层 | AI 写代码过程不可控；7步强制流程确保"更稳"而非"更强"                    |

## 四阶段工作流

1. **旧代码分析**：`openspec init` + `/opsx:explore` 生成现有系统规范快照，架构师补充 AI 遗漏的隐含规则
2. **需求规约**：`/opsx:propose` 生成 proposal + design + tasks 三件套；Delta Spec（ADDED/MODIFIED/REMOVED）显式标注影响面
3. **代码生成**：Superpowers 7步工作流：brainstorming → git worktree → writing-plans → subagent → TDD → 代码审查 → 分支收尾
4. **协同同步**：`/opsx:sync` 合并增量规范，`/opsx:archive` 归档变更记录

## 老旧项目四大踩坑点

- **代码风格冲突**：在 `openspec/specs/` 中写入代码风格规范，Superpowers brainstorming 会自动对齐
- **老旧依赖不兼容**：规范中明确标注框架版本号；让 AI 先读旧代码再写新代码
- **Spec 过度设计**：任务粒度控制在 2-5 分钟；Spec 写核心约束，不要面面俱到
- **旧系统隐含规则遗漏**：架构师在第一阶段分析时必须人工补充 AI 无法推断的业务规则

## 关联连接

- [[Superpowers]] — 执行层工具，7步工作流
- [[OpenSpec]] — 需求层工具，规约驱动开发
- [[摘要-openspec-superpowers-gstack-workflow]] — 同系列：三工具组合（含 Gstack）
- [[AgentHumanPipeline]] — 宏观人机协作框架
