---
title: "摘要-openspec-superpowers-nio-workflow"
type: source
tags: [来源, OpenSpec, Superpowers, 实战]
sources: [raw/01-articles/OpenSpec + Superpowers 组合开发流程 NIO定制版.md]
last_updated: 2026-06-18
---

## 核心摘要

NIO定制版将OpenSpec作为Workflow DSL（流程定义语言）、Superpowers作为Skill Library（技能库），构建可编排、可门禁、可追溯的AI原生开发流水线。核心分工：OpenSpec定义"做什么、按什么顺序、谁审批"，Superpowers定义"怎么做"，Dispatcher运行时编排，开发者决策评审。设计原则：DSL驱动流程、技能按需注入、人工门禁保护关键节点、SHA256锁定产物防篡改。五阶段流程：explore（可选探索）→ propose（规约+方案一体化有人工门禁）→ apply（编码实现SHA256校验）→ verify（评审+测试有人工门禁）→ archive（提PR+资料整理）。

## 关键洞察

### 整体架构

```
┌─────────────────────────────────────────────┐
│         OpenSpec (Workflow DSL)              │
│  定义流程、门禁、产物约束、阶段流转           │
│  schema.yaml → 命令路由 → Dispatcher        │
└────────────┬────────────────────────────────┘
             │ 调用
             ▼
┌─────────────────────────────────────────────┐
│       Superpowers (Skill Library)            │
│  7个核心工作流，按需注入                      │
│  brainstorming | using-git-worktrees        │
│  writing-plans | subagent-driven            │
│  TDD | code-review | finish                 │
└─────────────────────────────────────────────┘
```

### 核心分工

| 层 | 职责 | 谁维护 |
|----|------|--------|
| **OpenSpec (DSL)** | 定义"做什么、按什么顺序、谁审批" | 架构师/团队Lead |
| **Superpowers (Skills)** | 定义"怎么做"——标准化工程实践 | 社区+团队积累 |
| **Dispatcher** | 运行时编排：路由命令、校验门禁、调用Skills | AI Agent |
| **开发者** | 决策、评审、写代码 | 人 |

### 设计原则

1. **DSL驱动流程**：所有阶段流转、门禁规则、产物约束由schema.yaml定义，Agent按配置执行
2. **技能按需注入**：Superpowers的7个工作流不是全部自动触发，而是由Dispatcher根据当前阶段按需调用
3. **人工门禁保护关键节点**：propose和verify阶段设置人工评审，确保质量和一致性
4. **SHA256锁定**：产物防篡改，确保下游阶段使用的是经过确认的版本

### 流程总览

```
/opsx:explore  ← 可选，自由探索，无产物要求，无人工门禁
      │
      ▼
/opsx:propose  Spec + Design（规约+方案一体化，有人工门禁）
      │
      ▼
/opsx:apply    Build（编码实现，SHA256校验前置产物）
      │
      ▼
/opsx:verify   Verify（评审+测试，有人工门禁）
      │
      ▼
/opsx:archive  PR（提PR+资料整理）
```

### 五阶段详解

#### 阶段1：explore（可选）

- **定位**：自由探索，无产物要求，无人工门禁
- **触发**：`/opsx:explore`
- **目的**：快速验证想法，探索技术方案

#### 阶段2：propose（规约+方案一体化）

- **定位**：Spec + Design合并，有人工门禁
- **触发**：`/opsx:propose`
- **产物**：proposal.md + specs/ + design.md
- **人工门禁**：需要人工确认才能进入下一阶段
- **SHA256锁定**：锁定产物hash，防止篡改

#### 阶段3：apply（编码实现）

- **定位**：Build编码实现
- **触发**：`/opsx:apply`
- **前置校验**：SHA256校验前置产物（propose阶段的产物）
- **调用Skills**：
  - brainstorming（设计评审）
  - using-git-worktrees（创建隔离分支）
  - writing-plans（生成实现计划）
  - subagent-driven-development（执行TDD循环）

#### 阶段4：verify（评审+测试）

- **定位**：Verify评审+测试
- **触发**：`/opsx:verify`
- **人工门禁**：需要人工确认才能进入下一阶段
- **调用Skills**：
  - TDD（运行测试）
  - code-review（代码审查）
- **SHA256锁定**：锁定产物hash

#### 阶段5：archive（提PR+资料整理）

- **定位**：PR提PR+资料整理
- **触发**：`/opsx:archive`
- **调用Skills**：
  - finishing-a-development-branch（创建PR或合并）
- **归档**：将change归档到specs/

### 关键机制

#### SHA256锁定

**作用**：产物防篡改，确保下游阶段使用的是经过确认的版本。

**机制**：
- propose阶段完成后，计算产物hash
- apply阶段开始前，校验hash确保产物未被篡改
- verify阶段完成后，计算产物hash
- archive阶段开始前，校验hash

#### 人工门禁

**位置**：
- propose阶段结束：人工确认规约和方案
- verify阶段结束：人工确认评审和测试通过

**目的**：确保关键节点的质量和一致性。

#### 按需注入Skills

**不是全部自动触发**，而是Dispatcher根据当前阶段按需调用：
- propose阶段：可能调用brainstorming
- apply阶段：调用brainstorming、using-git-worktrees、writing-plans、subagent-driven-development
- verify阶段：调用TDD、code-review
- archive阶段：调用finishing-a-development-branch

## 关联连接

- [[OpenSpec]] — Workflow DSL
- [[Superpowers]] — Skill Library
- [[摘要-openspec-superpowers-workflow]] — 标准实战流程
- [[摘要-openspec-superpowers-gstack-threeinone]] — 三工具合一流程