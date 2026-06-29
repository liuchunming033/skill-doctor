---
title: "spec-driven-nio-design"
type: synthesis
tags:
  [
    OpenSpec,
    Superpowers,
    WorkflowDSL,
    SkillLibrary,
    SHA256,
    TDD,
    spec-driven-nio,
    OPSX,
  ]
created: 2026-06-07
updated: 2026-06-07
sources:
  [
    摘要-opsx-openspec-new-workflow,
    摘要-openspec-superpowers-tdd-v2,
    摘要-openspec-superpowers-new-project-guide,
  ]
related:
  - wiki/entities/OpenSpec.md
  - wiki/entities/Superpowers.md
  - wiki/concepts/AtomicTDDWorkflow.md
  - wiki/syntheses/openspec-superpowers-schema-driven-dispatch.md
---

# spec-driven-nio 设计方案

## 一、核心定位

spec-driven-nio 是一个 OpenSpec + Superpowers 的组合工作流系统：**OpenSpec 作为 Workflow DSL，Superpowers 作为 Skill Library**。

OpenSpec 负责定义流程、产物、状态、门禁和归档规则；Superpowers 负责在具体阶段执行标准化工程动作。两者不通过 API 集成，而是通过文件系统中的 Markdown 制品完成指令级闭环：OpenSpec 生产结构化规约，Superpowers 读取规约并生成实现计划、代码、测试证据和审查报告。

一句话架构：

> OpenSpec 持有“流程事实”，Superpowers 提供“执行能力”；Dispatcher 按 `schema.yaml` 路由命令、校验依赖、调用 skill、锁定产物。

## 二、系统目标

本方案要解决三个问题：

1. **需求不漂移**：所有实现必须回到 `specs/` 行为规约，而不是口头记忆或上下文残留。
2. **工程不失控**：AI 编码必须经过 brainstorming、计划拆分、子代理执行、TDD、审查、分支收尾等纪律约束。
3. **变更可回退**：所有新增/修改/删除先落在 `changes/`，通过 Delta Spec 和 SHA256 锁定保证变更可审查、可验证、可归档。

## 三、OpenSpec 核心机制

OpenSpec 在本系统中不是“文档模板工具”，而是 Workflow DSL 与状态机。

### 3.1 结构化 Markdown 规约

OpenSpec 使用结构化 Markdown 描述系统行为：

- `specs/`：系统当前行为的真实来源，记录主规约。
- `changes/{change}/proposal.md`：变更动机、范围、影响面和验收口径。
- `changes/{change}/specs/*.md`：针对主规约的 Delta Spec。
- `changes/{change}/design.md`：技术设计、接口约束、测试策略。
- `changes/{change}/tasks.md`：业务任务清单，用于 OpenSpec 进度追踪。

### 3.2 Delta Spec 变更机制

Delta Spec 用增量方式表达变更，避免直接改写主规约：

```markdown
## ADDED Requirements

### Requirement: 用户可以创建任务

#### Scenario: 创建成功

- GIVEN 已登录用户
- WHEN 提交合法任务标题
- THEN 系统创建任务并返回任务 ID

## MODIFIED Requirements

### Requirement: 用户可以更新任务状态

<!-- 描述修改后的行为 -->

## REMOVED Requirements

### Requirement: 旧版任务标签逻辑

<!-- 描述删除原因和兼容策略 -->
```

`ADDED / MODIFIED / REMOVED` 让变更具备 WAL 式特征：先记录变更意图，再经过实现、验证和人工确认，最后归档合并回主规约。

### 3.3 制品 DAG 依赖

OpenSpec 制品按 DAG 组织，Dispatcher 按依赖拓扑执行：

```text
proposal.md
      ↓
specs/*.md
      ↓
design.md
      ↓
tasks.md                         ← OpenSpec 业务任务清单
      ↓
.superpowers/plan.md             ← Superpowers 工程实现计划
      ↓
src/** + tests/**
      ↓
review-report.md + test-results/**
      ↓
pr-description.md + archive
```

注意：这里的 `tasks.md → .superpowers/plan.md` 是“就绪依赖”，不是“内容复制”。`tasks.md` 证明业务任务清单已经存在，Superpowers 的 `writing-plans` 生成工程计划时应读取 `proposal.md`、`specs/*.md`、`design.md` 和 brainstorming 设计文档，而不是把 OpenSpec `tasks.md` 改写成工程步骤。

### 3.4 WAL 式回退与归档合并

变更生命周期：

```text
changes/{change}/      记录变更意图
      ↓
apply                  生成代码和测试
      ↓
verify                 对照规约评审与测试
      ↓
archive                合并 Delta Spec 到 specs/，归档 changes/{change}
```

如果实现失败或验证不通过，系统保留 `changes/{change}` 作为可回退记录；如果验证通过，则将 Delta Spec 合并进 `specs/`，并把变更包归档。

## 四、Superpowers 七项核心工作流

Superpowers 在本系统中是无状态 Skill Library。它不持有全局流程状态，只接收 OpenSpec 提供的上下文和当前阶段指令，然后产出对应工程制品。

| 工作流                           | 做什么                               | 在 spec-driven-nio 中的角色                                                       |
| -------------------------------- | ------------------------------------ | --------------------------------------------------------------------------------- |
| `brainstorming`                  | 苏格拉底式对话，写代码之前先理清需求 | 在 `propose` 阶段辅助澄清行为边界；在 `apply` 阶段基于已锁定规约做工程分析        |
| `using-git-worktrees`            | 创建隔离的 Git 工作空间              | `apply` 前创建独立 worktree，避免污染主工作区                                     |
| `writing-plans`                  | 把工作拆成 2-5 分钟可完成的小任务    | 生成独立工程实现计划 `.superpowers/plan.md`，不直接读取或覆盖 OpenSpec `tasks.md` |
| `subagent-driven-development`    | 用子代理逐任务执行                   | 每个工程步骤一个实现子代理，并由独立 reviewer 检查结果                            |
| `test-driven-development`        | 强制 RED-GREEN-REFACTOR 循环         | 每个实现任务必须先产生失败测试，再最小实现，再重构                                |
| `requesting-code-review`         | 自动触发代码审查                     | `verify` 阶段以 `specs/` 和 `design.md` 为审查标准                                |
| `finishing-a-development-branch` | 完成分支，验证测试                   | `archive` 阶段完成最终验证、PR 描述和资料整理                                     |

## 五、OpenSpec × Superpowers 三重映射

传统理解中，两者有三个指令级衔接点：

| OpenSpec 制品 | Superpowers 工作流            | 衔接方式                                                                      |
| ------------- | ----------------------------- | ----------------------------------------------------------------------------- |
| `tasks.md`    | `writing-plans`               | `tasks.md` 只作为业务任务清单和就绪信号；`writing-plans` 另行生成工程实现计划 |
| `design.md`   | `subagent-driven-development` | 技术设计约束子代理的代码生成方向、接口边界和测试策略                          |
| `specs/`      | `requesting-code-review`      | 行为规约作为审查标准，逐条判断代码是否满足 GIVEN/WHEN/THEN 场景               |

这里必须明确一个关键修正：**OpenSpec 的 `tasks.md` 和 Superpowers 的实现计划是两份独立文档**。

| 文档       | 位置                                                                   | 生成者                      | 本质                    | 消费者                        |
| ---------- | ---------------------------------------------------------------------- | --------------------------- | ----------------------- | ----------------------------- |
| `tasks.md` | `openspec/changes/{change}/tasks.md`                                   | OpenSpec `/opsx:propose`    | 业务任务清单，回答 WHAT | OpenSpec state / Dispatcher   |
| `plan.md`  | `.superpowers/{change}/plan.md` 或 `openspec/changes/{change}/plan.md` | Superpowers `writing-plans` | 工程执行步骤，回答 HOW  | `subagent-driven-development` |

`writing-plans` 的输入应是 brainstorming 形成的工程设计文档，以及 OpenSpec 的 `proposal.md`、`specs/*.md`、`design.md`。它不应直接读取 `tasks.md` 后机械拆分，否则会把“业务任务追踪”污染成“工程执行脚本”。

## 六、五命令主流程

spec-driven-nio 将 Software 3.0 交付流程压缩成五个 OPSX 命令：

```text
[/opsx:explore]  ← 可选，自由探索，无产物要求，无人工门
      ↓
/opsx:propose    Spec + Design  （规约 + 方案一体化，有人工门禁）
      ↓
/opsx:apply      Build          （编码实现）
      ↓
/opsx:verify     Verify         （评审 + 测试，有人工门禁）
      ↓
/opsx:archive    PR             （提 PR + 资料整理）
```

### 6.1 `/opsx:explore`：可选探索

适用场景：需求边界不清、老项目不熟、需要先阅读代码或资料。

特征：

- 可跳过。
- 无强制产物。
- 无人工门禁。
- 可产出 `exploration.md` 作为上下文笔记，但不进入锁定范围。

### 6.2 `/opsx:propose`：规约 + 方案一体化

目标：生成可验证、可执行、可审查的一组变更制品。

产物：

- `proposal.md`：问题、范围、验收标准、WHEN/THEN 可测试行为。
- `specs/*.md`：GIVEN/WHEN/THEN 场景，使用 Delta Spec 描述变更。
- `design.md`：技术设计、接口约束、测试策略、文件结构。
- `tasks.md`：业务任务 checklist，用于 OpenSpec 进度追踪。

门禁：

- 人工确认 `proposal + specs + design + tasks` 是否达标。
- 通过后计算 SHA256，写入 `.opsx/locks/{change}.propose-approved.lock.json`。

### 6.3 `/opsx:apply`：构建实现

目标：在锁定规约约束下生成代码和测试。

执行顺序：

1. Dispatcher 校验 `propose-approved` SHA256。
2. `using-git-worktrees` 创建隔离工作空间。
3. `brainstorming` 基于已锁定制品做工程分析，不重新发散需求。
4. `writing-plans` 生成独立 `.superpowers/{change}/plan.md`。
5. `subagent-driven-development` 按 plan 逐任务执行。
6. 每个任务内部必须走 `test-driven-development` 的 RED-GREEN-REFACTOR。
7. 每个子任务完成后触发 spec reviewer 和 code quality reviewer。

### 6.4 `/opsx:verify`：评审 + 测试

目标：证明代码满足规约，并把验证证据固化。

产物：

- `review-report.md`：基于 `specs/` 和 `design.md` 的代码审查报告。
- `test-results/summary.md`：测试执行摘要。
- `test-results/coverage.md`：覆盖率或关键路径验证结果。

门禁：

- 人工确认代码审查和测试证据是否达标。
- 通过后计算 SHA256，写入 `.opsx/locks/{change}.verify-approved.lock.json`。

### 6.5 `/opsx:archive`：PR + 资料整理

目标：完成分支收尾、PR 物料和规约归档。

执行内容：

- 校验 `verify-approved` SHA256。
- 运行最终测试和分支清洁检查。
- 生成 `pr-description.md`、`CHANGELOG.md` 或变更摘要。
- 将 Delta Spec 合并到 `specs/`。
- 归档 `changes/{change}`。

## 七、四阶段实战流水线

上面的五命令是系统 DSL；落地到团队实践时，可以表达为四个工作阶段。

### 阶段一：规约设计

对应命令：`/opsx:explore`（可选）+ `/opsx:propose`

动作：

- 初始化 OpenSpec。
- 配置项目技术上下文，例如语言、框架、测试命令、架构边界。
- 生成 `proposal.md`、`specs/*.md`、`design.md`、`tasks.md`。
- 运行 `openspec validate` 或 schema 校验。
- 通过人工门禁后锁定 propose 产物。

### 阶段二：脚手架自动化

对应命令：`/opsx:apply` 前半段

动作：

- Superpowers `brainstorming` 基于已锁定设计做工程澄清。
- `using-git-worktrees` 创建隔离工作区。
- `writing-plans` 生成 2-5 分钟粒度的工程实现计划。
- 明确每步测试文件、断言、验证命令和证据要求。

### 阶段三：并行业务实现

对应命令：`/opsx:apply` 后半段

动作：

- 后端：`subagent-driven-development` 逐任务执行，内部强制 TDD。
- 前端：基于同一份 `specs/*.md` 与 `design.md` 独立开发 UI、接口消费和交互状态。
- 两端以 `design.md` 中的 API contract 对齐，不靠口头同步。
- 每个子任务完成后执行 spec reviewer 与 code quality reviewer。

### 阶段四：契约驱动迭代

对应命令：`/opsx:verify` + `/opsx:archive`

动作：

- 用 `requesting-code-review` 对照 `specs/` 审查代码。
- 运行全量测试，生成可审计证据。
- 若发现需求或接口变化，重新 `/opsx:propose` 生成 Delta Spec，而不是直接改代码。
- `/opsx:archive` 将通过验证的 Delta Spec 合并进主规约，并整理 PR 物料。

## 八、Schema 包目录设计

本方案采用一个可复用的 schema 包：

```text
schemas/
└── spec-driven-nio/
    ├── schema.yaml
    └── templates/
        ├── proposal.md
        ├── spec.md
        ├── design.md
        ├── tasks.md
        └── plan.md
```

各模板职责：

| 文件          | 职责                     | 关键要求                                                     |
| ------------- | ------------------------ | ------------------------------------------------------------ |
| `proposal.md` | 变更意图与可测试行为     | 使用 WHEN/THEN 描述行为，不写实现细节                        |
| `spec.md`     | 行为规约                 | 使用 GIVEN/WHEN/THEN，覆盖 happy path、edge case、error case |
| `design.md`   | 技术设计与测试策略       | 包含文件结构、接口契约、测试命令、风险点                     |
| `tasks.md`    | OpenSpec 业务任务清单    | checkbox 格式，用于业务进度追踪                              |
| `plan.md`     | Superpowers 工程执行计划 | 每步 2-5 分钟，包含 RED/GREEN/REFACTOR、证据和验证命令       |

## 九、schema.yaml 核心设计

`schema.yaml` 是 Workflow DSL 的核心。建议采用“产物即调度声明”的写法：每个 artifact 声明所属 phase、生成路径、依赖、绑定 skill、门禁和是否锁定。

```yaml
name: spec-driven-nio
version: 1
description: OpenSpec as Workflow DSL, Superpowers as Skill Library

artifacts:
  - id: exploration
    phase: explore
    generates: exploration.md
    optional: true
    skill: null
    requires: []
    gate: null
    lock_on_gate: false

  - id: proposal
    phase: propose
    generates: proposal.md
    template: templates/proposal.md
    skill: null
    requires: []
    gate: null
    lock_on_gate: false

  - id: specs
    phase: propose
    generates: specs/**/*.md
    template: templates/spec.md
    skill: null
    requires: [proposal]
    gate: null
    lock_on_gate: false

  - id: design
    phase: propose
    generates: design.md
    template: templates/design.md
    skill: null
    requires: [proposal, specs]
    gate: null
    lock_on_gate: false

  - id: tasks
    phase: propose
    generates: tasks.md
    template: templates/tasks.md
    skill: null
    requires: [specs, design]
    gate:
      type: human
      id: propose-approved
      prompt: 规约、设计和业务任务是否确认进入实现？
    lock_on_gate: true

  - id: worktree
    phase: apply
    generates: .git/worktrees/{{change_name}}
    skill: superpowers/using-git-worktrees
    requires: [tasks]
    gate: null
    lock_on_gate: false

  - id: impl-plan
    phase: apply
    generates: .superpowers/{{change_name}}/plan.md
    template: templates/plan.md
    skill: superpowers/writing-plans
    requires: [proposal, specs, design, worktree]
    note: Do not read tasks.md as source plan; tasks.md is only a business checklist.
    gate: null
    lock_on_gate: false

  - id: implementation
    phase: apply
    generates:
      - src/**
      - tests/**
    skill: superpowers/subagent-driven-development
    requires: [impl-plan]
    inner_skills:
      - superpowers/test-driven-development
    gate: null
    lock_on_gate: false

  - id: review-report
    phase: verify
    generates: review-report.md
    skill: superpowers/requesting-code-review
    requires: [implementation, specs, design]
    gate: null
    lock_on_gate: false

  - id: test-results
    phase: verify
    generates: test-results/**
    skill: superpowers/test-driven-development
    requires: [implementation]
    gate:
      type: human
      id: verify-approved
      prompt: 代码审查和测试证据是否确认通过？
    lock_on_gate: true

  - id: pr-materials
    phase: archive
    generates:
      - pr-description.md
      - CHANGELOG.md
    skill: superpowers/finishing-a-development-branch
    requires: [review-report, test-results]
    gate: null
    lock_on_gate: false
```

## 十、最轻量防护：SHA256 锁定

SHA256 锁定是本方案的最低成本防护层，用来防止人工门禁通过后，关键规约或验证证据被悄悄改动。

### 10.1 锁定时机

两个锁定点：

| 锁                 | 触发时机                   | 锁定对象                                                                 | 下一个校验命令  |
| ------------------ | -------------------------- | ------------------------------------------------------------------------ | --------------- |
| `propose-approved` | `/opsx:propose` 人工确认后 | `proposal.md`、`specs/*.md`、`design.md`、`tasks.md`                     | `/opsx:apply`   |
| `verify-approved`  | `/opsx:verify` 人工确认后  | `review-report.md`、`test-results/**`、必要时包含 `.superpowers/plan.md` | `/opsx:archive` |

### 10.2 锁文件格式

```json
{
  "change": "create-task-board",
  "gate": "propose-approved",
  "created_at": "2026-06-07T10:00:00Z",
  "artifacts": {
    "proposal.md": "sha256:a3f2c1...",
    "specs/task-board.md": "sha256:88b71d...",
    "design.md": "sha256:9b4e7a...",
    "tasks.md": "sha256:d1c3f8..."
  }
}
```

### 10.3 防护效果

下一个命令启动时，Dispatcher 重新计算哈希并与记录比对：

```text
/opsx:propose → 人工确认 → 写入 SHA256 lock
      ↓
有人手动修改 design.md 或 tasks.md
      ↓
/opsx:apply 启动 → 重新计算哈希
      ↓
哈希不一致 → 中止并报警
      ↓
必须重新走 /opsx:propose 和人工确认门
```

这不是权限系统，也不是安全沙箱；它是最轻量的“流程完整性保险丝”。它保证后续命令消费的是被人类确认过的那一版制品。

## 十一、Dispatcher 执行逻辑

Dispatcher 是 schema 的解释器，负责把 `/opsx:*` 命令转换为产物执行序列。

```python
def dispatch(command, change):
    phase = command.replace("/opsx:", "")

    verify_previous_locks(phase, change)

    artifacts = schema.artifacts.filter(phase=phase)
    for artifact in topo_sort(artifacts):
        ensure_requires_done(artifact.requires)
        context = load_context(artifact.requires)

        if artifact.skill:
            invoke_superpowers_skill(artifact.skill, context, artifact)
        else:
            render_template_or_generate_openspec_artifact(artifact, context)

        validate_generated_paths(artifact.generates)
        mark_done(artifact.id)

        if artifact.gate:
            wait_for_human_approval(artifact.gate)
            if artifact.lock_on_gate:
                lock_phase_artifacts(phase, change)
```

关键规则：

- 每个命令只执行自己 phase 内的 artifacts。
- `requires` 允许跨 phase 依赖，但必须要求前置产物已完成。
- 有 `skill` 字段时调用 Superpowers；无 `skill` 字段时由 OpenSpec 自身生成或校验制品。
- 人工门通过后才写 SHA256 lock。
- 后续命令启动时先校验上一门禁锁。

## 十二、模板设计要点

### 12.1 proposal.md

```markdown
# Proposal: {{change_name}}

## Problem

## Scope

## Testable Behaviors

- WHEN [action]
  THEN [observable outcome]

## Acceptance Criteria
```

要求：只写行为和验收，不写实现方案。

### 12.2 spec.md

```markdown
# Spec: {{feature}}

## ADDED Requirements

### Requirement: [name]

#### Scenario: [name]

- GIVEN [context]
- WHEN [action]
- THEN [outcome]
```

要求：每个场景必须独立可测试。

### 12.3 design.md

```markdown
# Design: {{change_name}}

## Architecture Decision

## API Contracts

## File Structure

## Test Strategy

## Risks and Rollback
```

要求：明确测试文件路径、测试命令、接口契约和风险回退。

### 12.4 tasks.md

```markdown
# Tasks: {{change_name}}

## Business Task Checklist

- [ ] Define task creation behavior
- [ ] Define task update behavior
- [ ] Define validation and error behavior
- [ ] Verify user-facing acceptance criteria
```

要求：业务任务清单，不承担 2-5 分钟工程步骤职责。

### 12.5 plan.md

```markdown
# Implementation Plan: {{change_name}}

> This plan is generated by Superpowers writing-plans.
> It is independent from OpenSpec tasks.md.

## Steps

### Step 1: RED - [behavior]

- File: tests/[file].test.ts
- Assertion: [assertion]
- Verify: npm test -- [file]
- Evidence: test must fail for the expected reason

### Step 2: GREEN - [behavior]

- File: src/[file].ts
- Minimal implementation: [description]
- Verify: npm test -- [file]
- Evidence: test must pass

## Execution Mode

Use superpowers/subagent-driven-development.
```

要求：工程步骤必须小到 2-5 分钟，并包含证据要求。

## 十三、命令到 Skill 覆盖矩阵

| 命令            | OpenSpec 角色            | Superpowers Skill                                                                                                 | 主要产物                                             | 人工门   |
| --------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | -------- |
| `/opsx:explore` | 自由探索                 | 可不用 skill，必要时可借助 brainstorming                                                                          | `exploration.md` 可选                                | 无       |
| `/opsx:propose` | 生成规约、设计、业务任务 | 可借助 brainstorming 澄清需求                                                                                     | `proposal.md`、`specs/*.md`、`design.md`、`tasks.md` | 有，锁定 |
| `/opsx:apply`   | 校验锁、驱动实现         | `using-git-worktrees`、`brainstorming`、`writing-plans`、`subagent-driven-development`、`test-driven-development` | `.superpowers/plan.md`、`src/**`、`tests/**`         | 无       |
| `/opsx:verify`  | 固化验证证据             | `requesting-code-review`、`test-driven-development`                                                               | `review-report.md`、`test-results/**`                | 有，锁定 |
| `/opsx:archive` | 合并规约、归档变更       | `finishing-a-development-branch`                                                                                  | `pr-description.md`、`CHANGELOG.md`、归档记录        | 无       |

## 十四、边界与反模式

必须避免的反模式：

- 把 `tasks.md` 当成 Superpowers `plan.md` 使用。
- 在 `/opsx:apply` 中发现需求变化后直接改代码，而不是回到 `/opsx:propose` 写 Delta Spec。
- 让 Superpowers 持有流程状态；流程状态必须由 OpenSpec schema、state 和 lock 持有。
- 人工门通过后允许静默修改规约。
- 把 review 降级为“看起来没问题”的总结；必须逐条对照 `specs/`。

允许的弹性：

- 小团队可关闭 `verify-approved` 锁，只保留 `propose-approved` 锁。
- 如果已有严格 PR 流程，SHA256 锁可与 Git commit hash 绑定。
- `plan.md` 可以落在 `.superpowers/{change}/plan.md`，也可以落在 `openspec/changes/{change}/plan.md`，但必须与 `tasks.md` 明确区分。

## 十五、最小可落地版本

MVP 只需要实现以下能力：

1. `schemas/spec-driven-nio/schema.yaml` 定义五个 phase 和 artifact DAG。
2. 五个模板文件：`proposal.md`、`spec.md`、`design.md`、`tasks.md`、`plan.md`。
3. Dispatcher 支持 `/opsx:propose`、`/opsx:apply`、`/opsx:verify`、`/opsx:archive`。
4. 人工门通过后计算 SHA256 并写 lock 文件。
5. 下一个命令启动时校验 lock，不一致则中止。
6. Superpowers `writing-plans` 只生成独立 `plan.md`，不改写 OpenSpec `tasks.md`。
7. `verify` 阶段必须以 `specs/` 为审查标准输出 review report。

## 十六、与前代设计的演进

| 维度             | tdd-driven-v2      | spec-driven-nio                              |
| ---------------- | ------------------ | -------------------------------------------- |
| 流程结构         | propose → apply    | explore → propose → apply → verify → archive |
| OpenSpec 角色    | 规约模板           | Workflow DSL + 状态机                        |
| Superpowers 角色 | 手动触发技能       | Skill Library，被 schema 调度                |
| 人工门禁         | 弱                 | propose、verify 两处显式门禁                 |
| 防篡改           | 无                 | SHA256 锁定                                  |
| `tasks.md` 职责  | 容易混合业务和工程 | 只做业务任务清单                             |
| 工程计划         | 常混在 tasks 中    | 独立 `plan.md`                               |
| 审查             | 容易被实现阶段跳过 | 独立 `/opsx:verify` 阶段强制执行             |

## 关联连接

- [[OpenSpec]] — Workflow DSL 主体，OPSX 动作驱动架构
- [[Superpowers]] — Skill Library 主体，7 个核心工作流
- [[AtomicTDDWorkflow]] — RED-GREEN-REFACTOR 与原子任务约束
- [[摘要-openspec-superpowers-new-project-guide]] — 新项目场景下 OpenSpec 与 Superpowers 的三重衔接
- [[摘要-opsx-openspec-new-workflow]] — OPSX Schema DAG 机制详解
- [[摘要-openspec-superpowers-tdd-v2]] — 前代 TDD Schema 实验报告
- [[openspec-superpowers-schema-driven-dispatch]] — Schema 作为 Workflow Orchestrator 的 Level 2 设计
