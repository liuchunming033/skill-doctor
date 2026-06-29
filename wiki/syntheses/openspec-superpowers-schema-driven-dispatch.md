---
title: "OpenSpec + Superpowers：Schema 驱动的全链路 Skill 调度方案"
type: synthesis
tags:
  [
    OpenSpec,
    Superpowers,
    Workflow,
    SchemaFirst,
    SkillDispatch,
    Level2,
    Software30,
    spec-driven-nio,
    ArtifactCentric,
    7Skills,
  ]
created: 2026-06-07
updated: 2026-06-07
sources: []
related:
  - wiki/entities/OpenSpec
  - wiki/entities/Superpowers
---

## 核心洞察

OpenSpec 的 `schema.yaml` 本质上是一个 **Workflow DSL**，Superpowers 是一个 **Skill Library**。当前社区普遍停留在 Level 1（文档模板），而两者真正的价值组合在 Level 2：让 schema.yaml 成为调度表，驱动 skill 自动调用，成为整个软件开发流程的**唯一事实来源**。

**Superpowers skills 是无状态的纯执行单元**：给我输入，我给你产物，不关心流程在哪步、之前发生了什么。**流程状态全部由 OpenSpec 持有**。

## SDLC → 命令映射

Software 3.0 的五阶段 SDLC 对应以下命令序列：

```
[/opsx:explore]  ← 可选，自由探索，无产物要求，无人工门
      ↓
/opsx:propose    Spec + Design  （规约 + 方案一体化）
      ↓
/opsx:apply      Build          （编码实现）
      ↓
/opsx:verify     Verify         （评审 + 测试）
      ↓
/opsx:archive    PR             （提PR + 资料整理）
```

`explore` 无强制要求，适合任务边界不清晰时先读代码/查资料积累上下文；任务清晰时可跳过直接 `propose`。

## 两工具分工边界

```
OpenSpec                              Superpowers（7 核心工作流）
────────────────────────              ──────────────────────────────────
schema.yaml（Workflow DSL）           brainstorming          ← explore/propose：需求澄清
.opsx/state.json（状态机）            using-git-worktrees    ← apply 前置：创建隔离工作空间
artifact DAG（依赖图）                writing-plans          ← propose/archive：收敛规划
SHA256 锁定（gate 后）                subagent-driven-development ← apply：逐任务子代理
Dispatcher（phase → artifact）        test-driven-development     ← apply 内部：RED-GREEN-REFACTOR
phase 顺序强制                        requesting-code-review      ← verify：代码评审
                                      finishing-a-development-branch ← archive：分支收尾
                                      [全部无状态，纯执行单元]
```

**关键事实**：writing-plans 生成的是**独立的工程执行计划**，基于 brainstorming 设计文档，而非直接读取 OpenSpec 的 `tasks.md`：

- OpenSpec `tasks.md` = 业务任务清单（OpenSpec `tracks` 解析 checkbox 追踪进度）
- Superpowers `plan.md` = 2-5 分钟工程步骤（writing-plans 独立输出，供 subagent-driven-development 消费）

## Schema 设计（产物中心 · 彻底融合版）

> **设计原则**：`skill`、`gate`、`lock_on_gate` 直接嵌入 artifact 定义。
> 消除独立 `commands:` 块——artifact 定义即调度声明，`schema.yaml` 是唯一事实来源。
> Dispatcher 按 `phase` 字段路由命令到对应 artifacts，沿 `requires` 拓扑排序执行。

```yaml
# openspec/schemas/spec-driven-nio/schema.yaml

name: spec-driven-nio
version: 1
description: >
  产物定义即调度声明：每个 artifact 内嵌绑定的 Superpowers skill、
  人工门配置和 SHA256 锁定开关。Dispatcher 按 phase 路由，无需独立命令块。

artifacts:
  # ══════════════════════════════════════════════════════════════
  # /opsx:explore — 可选探索（无人工门，无锁定）
  # ══════════════════════════════════════════════════════════════
  - id: exploration
    phase: explore
    generates: exploration.md
    skill: superpowers/brainstorming # 苏格拉底式对话，探索需求边界
    template: null
    instruction: |
      Use brainstorming to explore the codebase and clarify requirements.
      No mandatory output format — free-form exploration.md notes.
    requires: []
    optional: true # /opsx:explore 可跳过
    gate: null
    lock_on_gate: false

  # ══════════════════════════════════════════════════════════════
  # /opsx:propose — Spec + Design（人工门 + SHA256 锁定）
  # ══════════════════════════════════════════════════════════════
  - id: proposal
    phase: propose
    generates: proposal.md
    skill: superpowers/brainstorming # 发散：理清 WHAT，产出可测试行为
    template: templates/proposal.md
    instruction: |
      Use brainstorming. List every testable behavior in WHEN/THEN format:
        - WHEN [action or function call]
          THEN [observable outcome]
      Do NOT describe implementation details.
    requires: []
    gate: null
    lock_on_gate: false

  - id: specs
    phase: propose
    generates: specs/**/*.md
    skill: superpowers/writing-plans # 收敛：行为规约
    template: templates/spec.md
    instruction: |
      GIVEN/WHEN/THEN behavioral specs.
      Cover: happy path, edge cases, error cases.
      Each scenario must be independently testable.
    requires: [proposal]
    gate: null
    lock_on_gate: false

  - id: design
    phase: propose
    generates: design.md
    skill: superpowers/writing-plans # 收敛：技术设计
    template: templates/design.md
    instruction: |
      Technical design. MUST include:
        - Exact file paths for test files
        - Test strategy per file (unit/integration)
        - File structure showing tests alongside source
        - Test runner command (e.g., npm test)
        - API/interface contracts
    requires: [proposal]
    gate: null
    lock_on_gate: false

  - id: tasks
    phase: propose
    generates: tasks.md
    skill: superpowers/writing-plans # 收敛：原子任务清单
    template: templates/tasks.md
    instruction: |
      ATOMIC TDD task list. Each task = EXACTLY ONE TDD phase.
      MANDATORY FORMAT:
        - [ ] RED:      Write failing test — [behavior under test]
        - [ ] GREEN:    Implement — [minimal impl, reference RED task]
        - [ ] REFACTOR: Cleanup — [description] (optional)
      RULES:
        1. NEVER combine RED + GREEN in one task
        2. Every GREEN must reference its RED task
        3. Must use "- [ ]" checkbox format
        4. Alternate: RED → GREEN → (REFACTOR) → RED → ...
        5. No task takes more than 2-5 minutes
    requires: [specs, design]
    gate: null
    lock_on_gate: false

  - id: plans
    phase: propose
    generates: plan.md
    skill: superpowers/writing-plans # 收敛：工程执行计划
    template: templates/plan.md
    instruction: |
      PRECHECK: Verify superpowers:writing-plans is available.

      NOTE: This plan is INDEPENDENT from OpenSpec's tasks.md.
        tasks.md = business task list (OpenSpec tracks checkbox progress)
        plan.md  = engineering execution steps, 2-5 min each

      For each task, specify: file path, assertion, verify command, evidence.
      Append at end: "## Execution Mode: superpowers:subagent-driven-development"
    requires: [tasks]
    gate:
      type: human
      prompt: "规约 + 方案已达标？确认后锁定所有 propose 产物，进入构建阶段"
    lock_on_gate: true # SHA256 锁定本 phase 全部产物

  # ══════════════════════════════════════════════════════════════
  # /opsx:apply — Build（无人工门，内部验证）
  # ══════════════════════════════════════════════════════════════
  - id: workspace
    phase: apply
    generates: ".git/worktrees/feat-{{change_name}}"
    skill: superpowers/using-git-worktrees # 创建隔离 Git 工作空间
    instruction: |
      Create isolated Git worktree for this change.
      Branch name: feat/<change-name>
      All implementation happens inside this worktree.
    requires: [plans]
    gate: null
    lock_on_gate: false

  - id: implementation
    phase: apply
    generates:
      - "src/**"
      - "tests/**"
    skill: superpowers/subagent-driven-development # 逐任务子代理执行
    tracks: tasks.md
    instruction: |
      MANDATORY: subagent-driven-development skill.
      ONE subagent per task. Tasks execute IN ORDER. Never parallel.
      Each subagent internally uses test-driven-development skill
      to enforce RED-GREEN-REFACTOR cycle.

      Evidence requirements per subagent:
        - RED task:      report MUST include test failure output
        - GREEN task:    report MUST include test pass output
        - REFACTOR task: report MUST include full test suite pass

      After each task:
        1. spec reviewer: did subagent build exactly what was requested?
        2. code quality reviewer: is code clean, tested, maintainable?
        3. Only after BOTH approve → mark (- [ ] → - [x]) → proceed
    requires: [workspace]
    gate: null
    lock_on_gate: false

  # ══════════════════════════════════════════════════════════════
  # /opsx:verify — Verify（人工门 + SHA256 锁定）
  # ══════════════════════════════════════════════════════════════
  - id: review-report
    phase: verify
    generates: review-report.md
    skill: superpowers/requesting-code-review # 静态代码评审
    instruction: |
      Review code against specs/**/*.md and design.md as standards.
      Output review-report.md with PASS/FAIL verdict per spec.
    requires: [implementation]
    gate: null
    lock_on_gate: false

  - id: test-results
    phase: verify
    generates: "test-results/**"
    skill: superpowers/test-driven-development # 全量测试套件
    instruction: |
      Run FULL test suite. ALL tests must pass before gate.
      Output:
        - test-results/summary.md  (pass/fail/skip counts)
        - test-results/coverage.md (coverage %)
    requires: [implementation]
    gate:
      type: human
      prompt: "代码评审 + 全量测试通过？确认后锁定，允许归档"
    lock_on_gate: true

  # ══════════════════════════════════════════════════════════════
  # /opsx:archive — PR（无人工门，平台提 PR）
  # ══════════════════════════════════════════════════════════════
  - id: pr-materials
    phase: archive
    generates:
      - CHANGELOG.md
      - pr-description.md
    skill: superpowers/finishing-a-development-branch # 分支收尾 + PR 物料
    instruction: |
      Use finishing-a-development-branch skill:
        1. Run final full test suite verification
        2. Generate CHANGELOG.md (what changed and why)
        3. Generate pr-description.md (via writing-plans for structure)
        4. Ensure branch is clean and ready for PR platform submission
    requires: [review-report, test-results]
    gate: null
    lock_on_gate: false
```

## Dispatcher 执行逻辑（产物中心版）

```python
function opsx_dispatch(command):
  phase = command.phase   # "explore" | "propose" | "apply" | "verify" | "archive"

  # 1. SHA256 校验：上一 phase 锁定的产物是否被篡改
  prev_locked = schema.artifacts.filter(phase == prev_phase(phase), lock_on_gate == True)
  for artifact in prev_locked:
    if not sha256_verify(artifact.generates, state.locks[artifact.id]):
      abort(f"锁定产物已被篡改！请重新执行 /opsx:{prev_phase(phase)}")

  # 2. 按 phase 过滤 + 拓扑排序执行 artifacts
  phase_artifacts = schema.artifacts.filter(phase == phase)
  for artifact in topological_sort(phase_artifacts, key="requires"):

    # 3. 跨 phase 依赖校验（requires 中来自其他 phase 的产物）
    for dep_id in artifact.requires:
      dep = schema.find_artifact(dep_id)
      if dep.phase != phase and not state.is_complete(dep_id):
        abort(f"缺少前置产物：{dep_id}，请先执行 /opsx:{dep.phase}")

    # 4. 调用绑定的 Superpowers skill
    context = load_artifacts(artifact.requires)
    invoke_skill(artifact.skill, context, artifact.instruction)

    # 5. 校验产物是否生成
    validate_generates(artifact.generates)
    state.mark_complete(artifact.id)

    # 6. 人工门 + SHA256 锁定
    if artifact.gate:
      pause_for_human(artifact.gate.prompt)
      if artifact.lock_on_gate:
        # 对本 phase 所有已完成产物计算 SHA256
        for a in phase_artifacts:
          if state.is_complete(a.id):
            state.locks[a.id] = sha256_all(a.generates)
        state.save()   # 写入 .opsx/state.json
```

## 命令 → Skill → 产物 全景表

| 命令            | Phase   | 必须 | Superpowers Skill                                                                             | 关键产物                             | 人工门      |
| --------------- | ------- | ---- | --------------------------------------------------------------------------------------------- | ------------------------------------ | ----------- |
| `/opsx:explore` | explore | 可选 | **brainstorming**                                                                             | exploration.md                       | ❌          |
| `/opsx:propose` | propose | 必须 | **brainstorming** → **writing-plans** ×3                                                      | proposal, specs, design, tasks, plan | ✅ 锁定     |
| `/opsx:apply`   | apply   | 必须 | **using-git-worktrees** + **subagent-driven-development**（内含 **test-driven-development**） | worktree, src/**, tests/**           | ❌ 内部把关 |
| `/opsx:verify`  | verify  | 必须 | **requesting-code-review** + **test-driven-development**                                      | review-report.md, test-results/\*\*  | ✅ 锁定     |
| `/opsx:archive` | archive | 必须 | **finishing-a-development-branch**（内含 **writing-plans**）                                  | CHANGELOG.md, pr-description.md      | ❌ 平台提PR |

**7 个 Superpowers 工作流覆盖矩阵**：

| Skill                          | 做什么                               | 绑定 Phase            |
| ------------------------------ | ------------------------------------ | --------------------- |
| brainstorming                  | 苏格拉底式对话，写代码之前先理清需求 | explore / propose     |
| using-git-worktrees            | 创建隔离的 Git 工作空间              | apply                 |
| writing-plans                  | 把工作拆成 2-5 分钟可完成的小任务    | propose / archive     |
| subagent-driven-development    | 用子代理逐任务执行                   | apply                 |
| test-driven-development        | 强制 RED-GREEN-REFACTOR 循环         | apply（内部）/ verify |
| requesting-code-review         | 自动触发代码审查                     | verify                |
| finishing-a-development-branch | 完成分支，验证测试                   | archive               |

## 最轻量防护：SHA256 锁定

在纯两工具设计下，没有外部守护进程。防止「规约被悄悄修改」的唯一机制是文件哈希。

**触发时机**：人工确认门通过后，OpenSpec 对该 phase 所有已完成产物计算 SHA256，写入 `.opsx/state.json`：

```json
{
  "locks": {
    "spec.md": "sha256:a3f2c1...",
    "design.md": "sha256:9b4e7a...",
    "tasks.md": "sha256:d1c3f8..."
  }
}
```

**防护效果**：下一个命令（如 `/opsx:apply`）启动时，Dispatcher 重新计算哈希与记录比对。不一致 → 中止并报警，强制重新走人工确认门。

**典型风险场景**：

```
/opsx:propose → 人工确认 tasks.md ✅
      ↓
开发者手动缩减了 tasks.md 的验收标准（无人知晓）
      ↓
/opsx:apply → 哈希不匹配 → ABORT
      ↓
必须重新 /opsx:propose，明确确认新版规约
```

**可以去掉吗**：可以。若团队用 git commit + PR review 代替，`lock_on_gate: false` 即可，gate 退化为纯"确认继续"语义，无文件保护。

## Level 1 vs Level 2

| 层次                             | OpenSpec 角色 | Skill 使用方式    | 人工干预点   |
| -------------------------------- | ------------- | ----------------- | ------------ |
| Level 1（文档模板）              | 规约产物模板  | 手动决定调哪个    | 每步都需决策 |
| Level 2（Workflow Orchestrator） | 声明式调度表  | schema 绑定自动调 | 仅人工门     |

**分水岭**：没有 `skill:` 字段 → schema 只是文档模板（Level 1）。有 `skill:` 字段 → schema 成为调度表（Level 2），`schema.yaml` 成为整个软件开发流程的**唯一事实来源**。

## OpenSpec 目录结构与 Schema 实现参考

### 目录结构

```
openspec/
├── schemas/
│   └── spec-driven-nio/          # schema 包名
│       ├── schema.yaml           # 工作流定义（唯一事实来源）
│       └── templates/
│           ├── proposal.md       # WHEN/THEN 可测试行为模板
│           ├── spec.md           # GIVEN/WHEN/THEN 场景模板
│           ├── design.md         # 技术设计 + 测试策略模板
│           ├── tasks.md          # 原子 TDD 任务 checkbox 模板
│           └── plan.md           # 执行计划 + 证据要求模板
└── config.yaml                   # 项目级配置（tech stack、rules）
```

### 模板文件

**templates/proposal.md**

```markdown
# Proposal: {{change_name}}

## Problem

<!-- 描述要解决的问题 -->

## Testable Behaviors

<!-- WHEN/THEN 格式列出每一个可测试行为 -->

- WHEN [action or function call]
  THEN [observable outcome]

## Acceptance Criteria

<!-- 验收标准（机器可验证） -->
```

**templates/spec.md**

```markdown
# Spec: {{change_name}}

## Scenarios

### Scenario 1: [name]

- GIVEN: [前置条件]
- WHEN: [操作或触发]
- THEN: [期望结果]

<!-- Repeat for each scenario -->
```

**templates/design.md**

```markdown
# Design: {{change_name}}

## File Structure

<!-- 列出要创建的文件，包括测试文件 -->

## Test Strategy

| 文件              | 类型 | 说明 |
| ----------------- | ---- | ---- |
| tests/xxx.test.ts | unit | ...  |

## API Contracts

<!-- 接口签名 + 输入输出约定 -->

## Test Runner

`npm test`
```

**templates/tasks.md**

```markdown
# Tasks: {{change_name}}

## Atomic TDD Task List

### [Feature Name]

- [ ] RED: Write failing test — [behavior description]
- [ ] GREEN: Implement — [minimal impl, references RED]
- [ ] REFACTOR: Cleanup — [description]
```

**templates/plan.md**

```markdown
# Execution Plan: {{change_name}}

> NOTE: This plan is INDEPENDENT from tasks.md.
> tasks.md = business task list; plan.md = engineering execution steps.

## Steps

### Step 1: RED — [description]

- File: [exact path]
- Assertion: [what to test]
- Expected failure: [reason]
- Verify: `npm test -- [test-file]`
- Evidence: "Test MUST fail with [reason]"

### Step 2: GREEN — [description]

- Passes: Step 1
- Minimal code: [description]
- Verify: `npm test -- [test-file]`
- Evidence: "Test MUST pass"

---

## Execution Mode

REQUIRED: superpowers:subagent-driven-development
```

### 项目 config.yaml

```yaml
schema: spec-driven-nio

context: |
  Tech stack: TypeScript, Node.js, Jest
  Test runner: npm test
  Project: [描述项目类型]

rules:
  proposal:
    - List every testable behavior in WHEN/THEN format
  specs:
    - Use GIVEN/WHEN/THEN for every scenario
    - Cover happy path + edge cases + error cases
  tasks:
    - MUST use "- [ ]" checkbox for every task
    - Each task is exactly ONE TDD phase (RED/GREEN/REFACTOR)
    - GREEN tasks must reference their corresponding RED task
  plans:
    - Each step maps to exactly one task
    - Must specify verify command and expected evidence
```

### Artifact 字段 → 调度机制对应表

| `schema.yaml` 字段         | 对应机制                                          |
| -------------------------- | ------------------------------------------------- |
| `artifacts[].phase`        | Dispatcher 按 phase 路由命令 → 过滤对应 artifacts |
| `artifacts[].skill`        | 直接绑定的 Superpowers skill（产物即调度声明）    |
| `artifacts[].requires`     | 产物依赖 DAG，跨 phase 依赖触发前置 phase 校验    |
| `artifacts[].generates`    | 产物路径（SHA256 输入源 + 存在性校验）            |
| `artifacts[].template`     | `templates/` 目录模板文件                         |
| `artifacts[].gate`         | 人工确认门配置（type + prompt）                   |
| `artifacts[].lock_on_gate` | `true` → 门通过后对本 phase 所有产物 SHA256 锁定  |
| `artifacts[].tracks`       | state.json 中 checkbox 进度追踪（apply 专用）     |
| `artifacts[].optional`     | `true` → 命令可跳过此 artifact（explore 专用）    |

## 关联连接

- [[OpenSpec]] — 编排层，持有 schema.yaml 和 state.json
- [[Superpowers]] — 技能层，提供全部无状态执行 skill
- [[AtomicTDDWorkflow]] — apply 阶段内部的原子 TDD 机制
- [[摘要-opsx-openspec-new-workflow]] — OPSX 动作驱动架构：Schema DAG 取代线性阶段式模型
