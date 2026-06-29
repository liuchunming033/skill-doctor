---
title: "摘要-openspec-superpowers-workflow"
type: source
tags: [来源, OpenSpec, Superpowers, 实战]
sources: [raw/01-articles/OpenSpec + Superpowers 组合开发步骤.md]
last_updated: 2026-06-18
---

## 核心摘要

OpenSpec + Superpowers 组合开发四阶段实战流程：第一阶段规约设计（架构师执行，项目初始化→配置技术栈→启动变更提案→校验规约），第二阶段脚手架自动化生成（安装Superpowers→触发brainstorming→创建隔离工作空间→生成原子实现计划），第三阶段并行业务实现（后端/前端独立会话并行，Subagent-Driven执行TDD循环+三级审查），第四阶段契约驱动迭代（新变更提案→校验→应用→归档合并）。核心要点：spec.md是前后端共同真实来源、Git worktree隔离、三级审查关卡、Delta Spec追溯、人机分工明确。

## 四阶段完整流程

### 第一阶段：规约设计（架构师执行）

**目标**：写代码前，先把系统行为描述清楚。

| 步骤 | 操作 | 触发方式 | 说明 |
|------|------|---------|------|
| 1. 项目初始化 | `npm install -g @fission-ai/openspec@latest` + `openspec init` | 人工触发 | 创建 `openspec/` 目录和基础配置 |
| 2. 配置技术栈 | 编辑 `openspec/config.yaml` | 人工触发 | 声明技术栈（TypeScript/React/Node.js/PostgreSQL） |
| 3. 启动变更提案 | `/opsx:propose kanban-board-system` | 人工触发 | 按 DAG 生成 proposal.md → specs/ → design.md → tasks.md |
| 4. 校验规约 | `openspec validate` + `openspec status` | 人工触发 | 检查格式错误和逻辑矛盾，可用 `/opsx:ff` 快进 |

### 第二阶段：脚手架自动化生成（架构师/Lead执行）

**目标**：将粗粒度规约细化为可执行的工程计划。

| 步骤 | 操作 | 触发方式 | 触发来源 | 说明 |
|------|------|---------|---------|------|
| 1. 安装 Superpowers | `/plugin install superpowers` | 人工触发 | — | 14个 Skills 注册到 AI 助手 |
| 2. 触发 brainstorming | 告诉AI"开始实现，规约在openspec/changes/" | 人工触发 | — | 自动执行9步流程：探索→澄清→方案→确认→设计→自查→审阅 |
| 3. 创建隔离工作空间 | Superpowers 调用 using-git-worktrees | 自动触发 | brainstorming（设计审批后） | 在 `.worktrees/` 创建分支，安装依赖验证基线 |
| 4. 生成原子实现计划 | Superpowers 调用 writing-plans | 自动触发 | brainstorming（最后一步） | 拆分为2-5分钟/步原子任务，保存到 `docs/superpowers/plans/` |

### 第三阶段：并行业务实现（后端/前端并行）

**目标**：AI 子代理自动执行开发，前后端基于同一份规约同步推进。

#### 后端流程（单会话内串行自动循环）

| 步骤 | 操作 | 触发方式 | 触发来源 |
|------|------|---------|---------|
| 1. 选择 Subagent-Driven | 回复"选择方案1" | 人工触发 | — |
| 2. 读取计划提取任务 | Superpowers读取plans/并提取 | 自动触发 | 用户选择 |
| 3. 分派实现子代理 | 为每个Task创建独立子代理 | 自动触发 | subagent-driven控制器 |
| 4. 分派规约审查子代理 | 检查代码是否按计划实现 | 自动触发 | 实现子代理完成 |
| 5. 分派代码质量审查子代理 | 检查风格、性能、测试质量 | 自动触发 | 规约审查通过 |
| 6. 进入下一Task | 重复步骤3-5 | 自动触发 | 上一Task三级审查通过 |
| 7. 运行全量测试 | `npm test` | 自动触发 | 全部Task完成 |
| 8. 最终代码审查 | 检查跨任务一致性 | 自动触发 | 全量测试通过 |
| 9. 触发分支收尾 | 执行 finishing-a-development-branch | 自动触发 | 最终审查通过 |
| 10. 选择收尾方式 | 回复"创建PR"或"合并" | 人工触发 | — |

**TDD循环**：RED写失败测试 → GREEN最小实现 → REFACTOR

**三级审查**：实现 → 规约合规 → 代码质量，层层过滤。

#### 前端流程（独立AI会话并行执行）

| 步骤 | 操作 | 触发方式 |
|------|------|---------|
| 1. 启动前端实现 | 新AI会话告知"实现前端，规约在openspec/changes/" | 人工触发 |
| 2. 自动触发 brainstorming | 读取spec.md，经澄清→方案→设计 | 自动触发 |
| 3. 自动调用 worktree | 创建隔离工作空间 | 自动触发 |
| 4. 自动调用 writing-plans | 生成前端原子实现计划 | 自动触发 |
| 5. 后续子代理循环 | TDD → 规约审查 → 质量审查 | 自动触发 |

**并行前提**：spec.md 已定义清楚 API 行为，前后端有共同参照物，无需面对面联调。

### 第四阶段：契约驱动的迭代（全员协作）

**场景**：新增需求（如"任务卡片加优先级字段"）

| 步骤 | 操作 | 说明 |
|------|------|------|
| 1. 启动新变更提案 | `/opsx:propose add-task-priority` | 自动生成 Delta Spec（ADDED/MODIFIED/REMOVED） |
| 2. 校验 | `openspec validate` + `openspec status` | 确认变更规约合法 |
| 3. 应用实现 | `/opsx:apply add-task-priority` | OpenSpec读取tasks.md，逐条完成、写代码、跑测试 |
| 4. 归档合并 | `openspec archive add-task-priority` | Delta Spec合并入主规约specs/，成为系统行为一部分 |

## 核心要点

| 维度 | 关键设计 |
|------|---------|
| **协作契约** | OpenSpec 的 spec.md 是前后端共同的真实来源 |
| **隔离机制** | Git worktree 保证开发环境独立 |
| **质量关卡** | 三级审查（实现 → 规约合规 → 代码质量）层层过滤 |
| **变更追溯** | Delta Spec + WAL式归档，随时回退不污染原始数据 |
| **人机分工** | 人负责"定义清楚问题"（写规约、做关键决策），AI负责"按规矩执行"（生成代码、跑测试、做审查） |

## 触发方式汇总

```
人工触发                自动触发
──────────────────────────────────────────────
/opsx:propose    ──→   DAG生成proposal→specs→design→tasks
安装Superpowers  ──→   brainstorming（检测到开发意图）
"开始实现"        ──→   using-git-worktrees（设计审批后）
选择Subagent-Driven ──→  writing-plans（brainstorming最后一步）
                      ──→  实现子代理（计划读取完成）
                      ──→  规约审查子代理（实现完成）
                      ──→  代码质量审查子代理（规约审查通过）
                      ──→ 下一Task（三级审查通过）
                      ──→ 全量测试（全部Task完成）
                      ──→ 最终审查（测试通过）
                      ──→ finishing-a-development-branch（审查通过）
```

## 关联连接

- [[OpenSpec]] — 规约驱动开发框架
- [[Superpowers]] — Claude Code插件，14个Skills自动触发
- [[openspec-superpowers-schema-driven-dispatch]] — Schema驱动调度
- [[摘要-openspec-superpowers-gstack-workflow]] — 三工具组合流程