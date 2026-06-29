---
title: "摘要-openspec-superpowers-new-project-guide"
type: source
tags: [来源, OpenSpec, Superpowers, 新项目, 全流程, 看板系统]
sources:
  - Clippings/从零到一：OpenSpec + Superpowers 新项目全流程实战指南.md
  - raw/01-articles/从零到一：OpenSpec + Superpowers 新项目全流程实战指南 1.md
last_updated: 2026-06-07
---

## 核心摘要

面向新项目的完整工具链实战指南：以企业看板系统（TypeScript + React + Node.js + PostgreSQL）为例，演示 OpenSpec + Superpowers 的四阶段闭环。重点拆解了两工具的三个指令级衔接点，以及 Superpowers 各 Skill 的真实触发机制（自动触发 vs 手动引导）。

## 工具能力矩阵

| 工具        | 角色                       | 核心类比                          |
| ----------- | -------------------------- | --------------------------------- |
| OpenSpec    | 立法机构——写清楚要做什么   | WAL（先记变更意图，再合并主规约） |
| Superpowers | 执法机构——确保代码按规矩写 | 三级审查流水线                    |

**OpenSpec DAG 制品依赖关系**：

```
proposal（根节点）
    ├── specs（依赖 proposal）
    ├── design（依赖 proposal）
    └── tasks（依赖 specs + design）
```

## 三个指令级衔接点

| 衔接点                                  | OpenSpec 输出  | Superpowers 消费         |
| --------------------------------------- | -------------- | ------------------------ |
| tasks.md → writing-plans                | 粗粒度业务任务 | 拆解为 2-5 分钟工程步骤  |
| design.md → subagent-driven-development | 技术方案文档   | 子代理读取后约束实现方向 |
| specs/ → requesting-code-review         | 行为规约       | 作为代码审查的合规标准   |

**关键事实**：两工具通过**文件系统中的 Markdown 文件**握手——不依赖任何 API 调用或网络通信。

## 四阶段新项目全流程

### 第一阶段：规约设计（架构师）

- `openspec init --tools claude` → 生成目录结构
- 编辑 `config.yaml`，写清楚技术栈（context 字段决定 AI 生成方向）
- `/opsx:propose <project>` → 自动按 DAG 顺序生成四件套
- `openspec validate` → 校验格式和逻辑一致性；`/opsx:ff` 快进生成

### 第二阶段：脚手架自动化生成（架构师/Lead）

- `/plugin install superpowers@claude-plugins-official`
- 对 AI 说"我想实现 XX 功能，规约在 openspec/changes/ 目录"→ 自动触发 brainstorming
- **注意**：Superpowers 不自动识别 OpenSpec 目录，需明确引导 AI 读取
- brainstorming 9步流程 → 设计文档 → 自动调用 git worktrees（在 brainstorming 阶段就创建分支）→ 自动调用 writing-plans
- writing-plans 基于 brainstorming 的设计文档（非直接读取 OpenSpec tasks.md）

### 第三阶段：并行业务实现（后端 + 前端并行）

- 选择 Subagent-Driven 模式（推荐）
- Superpowers 控制器自动循环：dispatch 实现子代理 → spec reviewer → code quality reviewer → 标记完成
- 后端：子代理执行 TDD 循环，每个任务一个独立 context
- 前端：消费 design.md 中的接口规范，并行开发页面组件

### 第四阶段：联调与同步

- 接口差异通过 OpenSpec 更新 Delta Spec
- `/opsx:sync` 合并 → `/opsx:archive` 归档

## Superpowers 实际工作方式（澄清常见误解）

- Superpowers **不是**命令行工具，是 AI 助手内的 Skills 系统
- Skills **自动触发**，不需要手动输入命令
- brainstorming 技能包含 9 步检查清单，内部会自动调用 using-git-worktrees 和 writing-plans
- writing-plans 生成的计划是**独立文档**（不是 OpenSpec tasks.md 的副本）

## 关联连接

- [[OpenSpec]] — 规约驱动框架
- [[Superpowers]] — 工程执行框架
- [[AgentHumanPipeline]] — 宏观人机协作框架
- [[摘要-openspec-superpowers-tdd-v2]] — 同系列：TDD 约束深度实验
- [[摘要-superpowers-openspec-legacy-project]] — 同系列：老旧项目场景
