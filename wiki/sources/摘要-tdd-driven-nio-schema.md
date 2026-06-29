---
title: "摘要-tdd-driven-nio-schema"
type: source
tags: [来源, OpenSpec, Schema, TDD]
sources: [raw/01-articles/tdd-driven-nio Schema 完整设计方案.md]
last_updated: 2026-06-18
---

## 核心摘要

tdd-driven-nio 是 OpenSpec 自定义 Schema，将 Superpowers TDD 四层防护固化为可重复执行的工程流程。Schema名称tdd-driven-v2，制品DAG：proposal→specs/design→tasks→plans→apply执行。目录结构：schemas/tdd-driven-v2/包含schema.yaml（工作流定义）和templates/（proposal/spec/design/tasks/plan五个模板）。配置5步：安装OpenSpec并初始化→创建自定义Schema→写入schema.yaml→写入模板文件→配置config.yaml。核心设计：任务粒度物理约束（每个task=一个TDD阶段）、subagent串行隔离、三级审查（spec审查+quality审查）、evidence必填、writing-plans skill绑定plans artifact。

## 关键洞察

### 目录结构

```
openspec/
├── schemas/
│   └── tdd-driven-v2/
│       ├── schema.yaml          # 工作流定义（Workflow DSL核心）
│       └── templates/
│           ├── proposal.md      # WHEN/THEN可测试行为
│           ├── spec.md          # GIVEN/WHEN/THEN场景
│           ├── design.md        # 技术设计+测试文件路径
│           ├── tasks.md         # 原子TDD任务checkbox
│           └── plan.md          # 执行计划+证据要求
├── config.yaml                  # 项目配置
├── changes/                     # openspec init自动创建
└── specs/                       # openspec init自动创建
```

**注意**：`schemas/`目录和`config.yaml`不会由`openspec init`自动创建，需要手动操作。

### 制品 DAG（依赖关系）

```
proposal
   ├──→ specs  ──┐
   └──→ design ──┤
                 ▼
               tasks
                 ↓
               plans
                 ↓
             apply（执行）
```

**状态转换**：`BLOCKED` → `READY` → `DONE`（基于文件存在性检测）

### 配置5步流程

#### Step 1：安装OpenSpec并初始化项目

```bash
npm install -g @fission-ai/openspec@latest
openspec init --tools claude,cursor
```

初始化后自动生成：
- `openspec/changes/`（变更记录目录）
- `openspec/specs/`（规范目录）
- `.claude/skills/openspec-*/SKILL.md`（AI工具自动检测）

#### Step 2：创建自定义Schema

```bash
# 方式A：从零创建（会生成模板结构）
openspec schema init tdd-driven-v2

# 方式B：Fork现有模式修改
openspec schema fork default tdd-driven-v2
```

**Schema存储位置（二选一）**：
- **项目本地**（推荐，可版本控制）：`./openspec/schemas/tdd-driven-v2/`
- **用户全局**（所有项目可用）：`~/.local/share/openspec/schemas/tdd-driven-v2/`

#### Step 3：写入schema.yaml

写入`openspec/schemas/tdd-driven-v2/schema.yaml`。

#### Step 4：写入模板文件

写入templates/下的五个模板文件：
- proposal.md
- spec.md
- design.md
- tasks.md
- plan.md

#### Step 5：配置config.yaml

配置项目级别的config.yaml。

### 核心设计要点

#### 任务粒度物理约束

**每个task = 一个TDD阶段**：
- 将任务粒度作为物理约束，强制AI遵循TDD
- 每个task包含RED写失败测试 → GREEN最小实现 → REFACTOR完整TDD循环

#### Subagent串行隔离

- 每个task使用独立subagent执行
- 串行隔离，避免上下文污染
- task之间通过artifact传递

#### 三级审查机制

| 审查级别 | 审查内容 | 说明 |
|---------|---------|------|
| **spec审查** | 代码是否符合spec描述 | 确保实现符合规约 |
| **quality审查** | 代码风格、性能、测试质量 | 确保质量达标 |
| **第三级审查** | 完整性检查 | 确保全部通过才标记task完成 |

#### Evidence必填

- 每个task完成后必须提供evidence（证据）
- Evidence包含：测试结果、代码截图、运行日志等
- 确保每个task的完成有可验证证据

#### Writing-plans skill绑定

- `writing-plans` skill绑定到`plans` artifact
- 从design生成plans时调用writing-plans skill
- 确保plans是原子化可执行的

### OpenSpec官方CLI命令

```bash
# Schema操作
openspec schema init tdd-driven-v2        # 初始化Schema
openspec schema fork default tdd-driven-v2 # Fork现有Schema
openspec schema validate tdd-driven-v2    # 验证Schema

# 变更操作
openspec propose <change-name>            # 创建变更提案
openspec apply <change-name>              # 应用变更
openspec archive <change-name>            # 归档变更

# 状态检查
openspec status --change <change-name> --json # 检查变更状态
openspec validate                         # 验证所有规约
```

### DAG状态机

**状态转换逻辑**：
- `BLOCKED`：依赖的artifact未完成
- `READY`：依赖的artifact已完成，可以执行
- `DONE`：artifact已生成

**状态检测**：基于文件存在性检测（如proposal.md存在则proposal状态为DONE）。

## 关联连接

- [[OpenSpec]] — 规约驱动开发框架
- [[Superpowers]] — Claude Code插件，TDD四层防护
- [[AtomicTDDWorkflow]] — 原子化TDD工作流
- [[摘要-openspec-superpowers-workflow]] — OpenSpec实战流程