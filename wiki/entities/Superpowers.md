---
title: "Superpowers"
type: entity
tags: [工具, Claude Code, 插件, 工程纪律, AI编程]
sources:
  [
    "raw/01-articles/Superpowers + gstack 搭配实战：2 个插件，37 个技能，5 个关键交接点，闭环标准开发流程.md",
  ]
last_updated: 2026-06-06
---

## 定义

Superpowers 是 Jesse Vincent 开发的 Claude Code 开源插件（158K Star），核心是一个 94% PR 拒绝率的工程纪律框架。14 个 Skills 不是功能列表，而是一套强制性的工程规范：确保 AI 在写代码时遵循标准化实践，拒绝劣质代码。设计哲学：**更稳而非更强**。

## 关键信息

**触发方式**：自动触发——Agent 在执行任务前检测是否有适用的 Skill，无需用户显式调用。

**14个核心技能（代表性）：**

| 技能                             | 作用                                           |
| -------------------------------- | ---------------------------------------------- |
| `brainstorming`                  | 结构化需求精炼，9步流程，强制"先想后做"        |
| `writing-plans`                  | 生成 2-5分钟粒度的微任务计划                   |
| `test-driven-development`        | 强制 TDD 红绿循环，甚至会删掉先于测试写的代码  |
| `systematic-debugging`           | 4阶段根因分析，铁律：没有根因调查就不修复      |
| `requesting-code-review`         | 作者和审查者严格分离的双通道审查               |
| `subagent-driven-development`    | 每个任务派独立子代理，实现者和审查者不同上下文 |
| `verification-before-completion` | 声明完成前必须收集证据                         |
| `using-git-worktrees`            | 隔离 Git 工作空间                              |

**安装路径**：`~/.claude/skills/superpowers-*`（每个技能一个目录）

**与 Gstack 的分工**：Superpowers 处理"编码层决策"（自动触发），Gstack 处理"产品层和外部世界决策"（手动触发）。两者在激活机制和能力层面均无冲突。

## 关联连接

- [[Gstack]] — 搭档插件，处理产品决策和上线流程
- [[OpenSpec]] — 可在需求阶段配合，提供结构化规约输入
- [[摘要-superpowers-gstack-integration]] — 两者搭配的详细分析
- [[摘要-openspec-superpowers-gstack-workflow]] — 含 OpenSpec 的三工具组合流程
- [[摘要-superpowers-openspec-legacy-project]] — 老旧项目四阶段工作流实战
- [[摘要-gstack-superpowers-perfect-loop]] — 完美闭环：两插件组合的分工与任务分流
- [[摘要-openspec-superpowers-gstack-threeinone]] — 三工具七步流程与四个串联点
- [[AgentHumanPipeline]] — 宏观人机协作框架
