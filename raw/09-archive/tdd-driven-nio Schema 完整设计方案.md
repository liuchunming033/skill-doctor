# tdd-driven-nio：完整 Schema 设计方案

> **定位**：OpenSpec 自定义 Schema，将 Superpowers TDD 四层防护固化为可重复执行的工程流程。
> Schema 名称：`tdd-driven-v2` | 来源参考：《OpenSpec + Superpowers 组合开发步骤》

---

## 目录结构

```
openspec/
├── schemas/
│   └── tdd-driven-v2/
│       ├── schema.yaml          # 工作流定义（Workflow DSL 核心）
│       └── templates/
│           ├── proposal.md      # WHEN/THEN 可测试行为
│           ├── spec.md          # GIVEN/WHEN/THEN 场景
│           ├── design.md        # 技术设计 + 测试文件路径
│           ├── tasks.md         # 原子 TDD 任务 checkbox
│           └── plan.md          # 执行计划 + 证据要求
├── config.yaml                  # 项目配置（注意：在 openspec/ 根目录）
├── changes/                     # openspec init 自动创建
└── specs/                       # openspec init 自动创建
```

> ⚠️ **注意**：`schemas/` 目录和 `config.yaml` **不会**由 `openspec init` 自动创建，需要手动操作。

---

## 制品 DAG（依赖关系）

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

状态转换：`BLOCKED` → `READY` → `DONE`（基于文件存在性检测）

---

## 完整配置方法（5 步）

### Step 1：安装 OpenSpec 并初始化项目

```bash
npm install -g @fission-ai/openspec@latest
openspec init --tools claude,cursor
```

初始化后自动生成：

- `openspec/changes/`（变更记录目录）
- `openspec/specs/`（规范目录）
- `.claude/skills/openspec-*/SKILL.md`（AI 工具自动检测）

### Step 2：创建自定义 Schema

```bash
# 方式 A：从零创建（会生成模板结构）
openspec schema init tdd-driven-v2

# 方式 B：Fork 现有模式修改
openspec schema fork default tdd-driven-v2
```

Schema 存储位置（二选一）：

- **项目本地**（推荐，可版本控制）：`./openspec/schemas/tdd-driven-v2/`
- **用户全局**（所有项目可用）：`~/.local/share/openspec/schemas/tdd-driven-v2/`

### Step 3：写入 schema.yaml

按下方 §schema.yaml 全文内容写入 `openspec/schemas/tdd-driven-v2/schema.yaml`。

验证 Schema 格式：

```bash
openspec schema validate tdd-driven-v2
openspec schema which tdd-driven-v2  # 确认解析路径
```

### Step 4：激活项目配置

创建 `openspec/config.yaml`，指定使用该 Schema：

```yaml
schema: tdd-driven-v2

context: |
  [填写你的项目技术栈、测试框架、核心约束]

rules:
  tasks:
    - MUST use checkbox format "- [ ]" for every task
    - Each task is exactly ONE TDD phase
```

> **配置优先级**（高→低）：CLI flag `--schema` > 变更目录 `.openspec.yaml` > `openspec/config.yaml` > 默认值

### Step 5：使用工作流

```bash
# 查看当前 Schema 和制品状态
openspec status
openspec schemas

# 启动变更（生成 proposal → specs → design → tasks → plans）
/opsx:propose <change-name>

# 单步创建（逐个制品，探索式）
/opsx:continue

# 快进（一次生成所有规划制品）
/opsx:ff <change-name>

# 执行实现（读取 tasks.md，调用 Superpowers subagent）
/opsx:apply <change-name>

# 归档（合并 Delta Spec 到主规范）
/opsx:archive <change-name>
```

---

## schema.yaml（全文）

```yaml
name: tdd-driven-v2
version: "2.0"
description: |
  Atomic TDD workflow with subagent isolation and evidence verification.
  Core constraint: each task = exactly one TDD phase;
  one subagent per phase; test output evidence required.

artifacts:
  - id: proposal
    generates: proposal.md
    template: templates/proposal.md
    description: Initial change proposal with testable behaviors (WHEN/THEN)
    instruction: |
      Create a proposal that explains WHY this change is needed.
      MANDATORY FORMAT for testable behaviors — use WHEN/THEN:
        - WHEN markdownToHtml("# Hello") is called
          THEN result is "<h1>Hello</h1>"
      Do NOT describe implementation details.
      Focus on WHAT should happen, not HOW.
    requires: []

  - id: specs
    generates: specs/**/*.md
    template: templates/spec.md
    description: Behavioral specifications (GIVEN/WHEN/THEN scenarios)
    instruction: |
      Write behavioral specs using GIVEN/WHEN/THEN scenarios.
      Rules:
      - Each scenario must be independently testable
      - Cover: happy path, edge cases, error cases
      - Express expected behavior, not implementation
    requires:
      - proposal

  - id: design
    generates: design.md
    template: templates/design.md
    description: Technical design with test strategy and exact file paths
    instruction: |
      Create a technical design explaining HOW to implement.
      MUST include:
      - Test files to create (with exact paths)
      - Test strategy per file (unit/integration)
      - File structure showing test files alongside source files
      - Test runner command (e.g., npm test)
    requires:
      - proposal

  - id: tasks
    generates: tasks.md
    template: templates/tasks.md
    description: Atomic TDD task list — one TDD phase per task
    instruction: |
      CRITICAL: Each task is EXACTLY ONE TDD phase (RED / GREEN / REFACTOR).
      MANDATORY FORMAT — checkbox syntax:
        - [ ] RED: Write failing test — [具体行为，含文件名和断言]
        - [ ] GREEN: Implement — [最小实现，引用对应 RED 任务]
        - [ ] REFACTOR: Cleanup — [描述]（可选）
      Rules:
      1. NEVER combine RED and GREEN in one task
      2. GREEN must reference its corresponding RED
      3. MUST use "- [ ]" format — no exceptions
      4. Alternate: RED → GREEN → (REFACTOR) → RED → GREEN → ...
      5. Each task ≤ 2-5 minutes
    requires:
      - specs
      - design

  - id: plans
    generates: plan.md
    template: templates/plan.md
    description: Execution plan — 1:1 task mapping with evidence requirements
    instruction: |
      PRECHECK: Verify superpowers:writing-plans skill is available.
      Each plan step maps to EXACTLY ONE task from tasks.md.
      For RED:    file path + assertion + expected failure + verify command
      For GREEN:  which RED test to pass + minimal code + verify command
      For REFACTOR: what to clean + verify command
      Evidence strings:
        RED     → "Test MUST fail with [expected reason]"
        GREEN   → "Test MUST pass"
        REFACTOR → "ALL tests MUST still pass"
      Append after plan:
      ---
      ## Execution Mode Selection
      REQUIRED: Use superpowers:subagent-driven-development skill.
      DO NOT use executing-plans or inline execution.
    requires:
      - tasks

apply:
  requires:
    - plans
  tracks: tasks.md
  instruction: |
    MANDATORY execution sequence — invoke Superpowers skills in this exact order.
    DO NOT skip any phase. DO NOT use executing-plans or inline execution.

    ──────────────────────────────────────────────────
    PHASE 1: superpowers:brainstorming
    ──────────────────────────────────────────────────
    Trigger: human ("开始实现，规约在 openspec/changes/<name>/")
    Input:   openspec/changes/<name>/specs/ + design.md
    Execute 9-step flow:
      explore → clarify → select approach → confirm
      → write design doc → self-review → user approval
    Gate: WAIT for user approval before Phase 2.

    ──────────────────────────────────────────────────
    PHASE 2: superpowers:using-git-worktrees
    ──────────────────────────────────────────────────
    Trigger: AUTOMATIC after brainstorming design approval
    Action:  create branch in .worktrees/<change-name>,
             install deps, verify test baseline passes

    ──────────────────────────────────────────────────
    PHASE 3: superpowers:writing-plans
    ──────────────────────────────────────────────────
    Trigger: AUTOMATIC — brainstorming last step "Transition to implementation"
    Input:   brainstorming design document (NOT tasks.md)
    Output:  docs/superpowers/plans/ — 2-5 min atomic steps
    Gate:    user selects "Subagent-Driven" mode to proceed.

    ──────────────────────────────────────────────────
    PHASE 4: superpowers:subagent-driven-development  [LOOP]
    ──────────────────────────────────────────────────
    Trigger: AUTOMATIC after user confirms Subagent-Driven mode
    - ONE subagent per task, in order — no skipping, no reordering
    - NEVER dispatch multiple implementation subagents in parallel

    Per-task inner loop:
      A. [superpowers:test-driven-development]
           RED:      write failing test — MUST provide failure output
                     "all tests passing" on RED → re-dispatch
           GREEN:    minimal impl — MUST provide pass output
                     still failing → re-dispatch with fix
           REFACTOR: clean up — MUST provide full suite output
                     any failure → re-dispatch with fix
      B. [superpowers:requesting-code-review] — spec reviewer
           Did subagent build exactly what was requested? Nothing more?
           Fail → re-dispatch with correction
      C. [superpowers:requesting-code-review] — code quality reviewer
           Code clean, tested, maintainable?
           Fail → re-dispatch with fix
      B + C approved → tasks.md: - [ ] → - [x] → next task

    ──────────────────────────────────────────────────
    PHASE 5: superpowers:finishing-a-development-branch
    ──────────────────────────────────────────────────
    Trigger: AUTOMATIC after all tasks complete + final review passes
    Actions: full test suite + verify all specs + check TODOs
             → present options: merge / PR / keep / discard
    Gate: WAIT for human final disposition.
```

---

## config.yaml（全文）

```yaml
# openspec/config.yaml
schema: tdd-driven-v2

context: |
  Tech stack: TypeScript, Node.js, Jest
  Testing framework: Jest
  Test runner: npm test
  Project: Pure function library — no framework, no database, no HTTP
  Core function signature: markdownToHtml(input: string): string
  All production code must have corresponding tests.

rules:
  proposal:
    - List every testable behavior in WHEN/THEN format
    - Do not describe implementation

  specs:
    - Use GIVEN/WHEN/THEN format for every scenario
    - Each scenario must be independently testable

  design:
    - Must specify exact test file paths
    - Must specify test strategy per file

  tasks:
    - MUST use checkbox format "- [ ]" for every task
    - Each task is exactly ONE TDD phase (RED, GREEN, or REFACTOR)
    - Tasks must alternate RED → GREEN → (optional REFACTOR)
    - GREEN tasks must reference their corresponding RED task

  plans:
    - Each plan step maps to exactly one task
    - Must specify verify command and expected evidence
```

---

## 模板文件

### templates/proposal.md

```markdown
# Proposal: {{change_name}}

## Problem

<!-- 描述要解决的问题 -->

## Testable Behaviors

<!-- WHEN/THEN 格式列出每一个可测试行为 -->

- WHEN
  THEN

## Acceptance Criteria

<!-- 验收标准 -->

- [ ]
```

### templates/spec.md

```markdown
# Spec: {{change_name}}

## Scenarios

### Scenario 1: [name]

- GIVEN: [前置条件]
- WHEN: [操作]
- THEN: [期望结果]

<!-- Repeat for each scenario -->
```

### templates/design.md

```markdown
# Design: {{change_name}}

## File Structure

<!-- 列出要创建的文件，包括测试文件 -->

## Test Strategy

<!-- 每个 test 文件的测试策略 -->

## Implementation Notes

<!-- 实现要点 -->
```

### templates/tasks.md

```markdown
# Tasks: {{change_name}}

## Atomic TDD Task List

<!-- 每个 task 只能是一个 TDD 阶段 -->
<!-- 必须使用 checkbox 格式 -->

### [AI fills feature name]

- [ ] RED: ...
- [ ] GREEN: ...
- [ ] REFACTOR: ...
```

### templates/plan.md

```markdown
# Execution Plan: {{change_name}}

## Micro-tasks

### Step 1: RED — [description]

- Test file: [path]
- Assertion: [what to test]
- Expected failure: [reason]
- Verify: `npm test -- [test-file]`

### Step 2: GREEN — [description]

- Pass test from: Step 1
- Minimal code: [what to implement]
- Verify: `npm test -- [test-file]`

<!-- Repeat for each task -->

---

## Execution Mode Selection

REQUIRED: Use superpowers:subagent-driven-development skill for execution.
```

---

## Superpowers Skill 调用序列（完整流水线）

`/opsx:apply` 触发后，按以下顺序调用 Superpowers 技能，五个阶段串行执行：

```
人工触发                           自动触发
──────────────────────────────────────────────────────────────────
"开始实现，规约在 openspec/..."  →  [PHASE 1] brainstorming
                                      9步：探索→澄清→方案选择→分段确认
                                           →写设计文档→自查→用户审阅
                                              ↓ 用户批准设计（人工门）
                                   [PHASE 2] using-git-worktrees
                                      创建 .worktrees/<name> 分支
                                      安装依赖 + 验证测试基线通过
                                              ↓
                                   [PHASE 3] writing-plans
                                      输入：brainstorming 设计文档（非 tasks.md）
                                      输出：docs/superpowers/plans/（原子步骤）
                                              ↓
用户选择 "Subagent-Driven"       →  [PHASE 4] subagent-driven-development  ←─┐
                                      ┌─────────────────────────────────┐    │
                                      │ 每个 Task 内循环（串行）        │    │
                                      │                                 │    │
                                      │ A. test-driven-development      │    │
                                      │    RED：写失败测试+提供失败输出 │    │
                                      │    GREEN：最小实现+提供通过输出 │    │
                                      │    REFACTOR：整理+提供全量输出  │    │
                                      │             ↓                   │    │
                                      │ B. requesting-code-review       │    │
                                      │    规约审查：恰好完成？不多？   │    │
                                      │             ↓（通过）           │    │
                                      │ C. requesting-code-review       │    │
                                      │    质量审查：整洁？可维护？     │    │
                                      │             ↓（B+C 全通过）     │    │
                                      │    tasks.md: - [ ] → - [x]     │    │
                                      └────────────┬────────────────────┘    │
                                             下一个 Task ───────────────────→┘
                                              ↓ 全部 Task 完成
                                   [PHASE 5] finishing-a-development-branch
                                      全量测试 + 验证所有 spec + 检查 TODO
                                      → 呈现：merge / PR / keep / discard
                                              ↓
用户选择处置方式                    （最终人工决策）
```

### 技能触发方式汇总

| 阶段  | Superpowers 技能                                          | 触发方式 | 触发来源                 | 输入                                  |
| ----- | --------------------------------------------------------- | -------- | ------------------------ | ------------------------------------- |
| 1     | `brainstorming`                                           | **人工** | 用户告知开始实现         | `openspec/changes/<name>/`            |
| 2     | `using-git-worktrees`                                     | **自动** | brainstorming 设计审批后 | —                                     |
| 3     | `writing-plans`                                           | **自动** | brainstorming 最后一步   | brainstorming 设计文档（非 tasks.md） |
| 4-A   | `subagent-driven-development` + `test-driven-development` | **自动** | 用户选 Subagent-Driven   | writing-plans 产出                    |
| 4-B/C | `requesting-code-review` ×2                               | **自动** | 实现子代理完成           | 每个 task 实现结果                    |
| 5     | `finishing-a-development-branch`                          | **自动** | 全部 task + 最终审查通过 | —                                     |

> **关键约束**：`writing-plans` 读取的是 brainstorming 产出的工程设计文档，**不读取 OpenSpec 的 `tasks.md`**。`tasks.md` 是 OpenSpec 的业务任务追踪（checkbox 状态机），`writing-plans` 产出是 Superpowers 的 2-5 分钟原子执行步骤——两者独立，职责不同。

---

## 与组合开发步骤的映射

| 组合开发步骤                                    | tdd-driven-v2 对应                                       |
| ----------------------------------------------- | -------------------------------------------------------- |
| 第一阶段 Step 3：`/opsx:propose`                | DAG 按序生成：proposal → specs/design → tasks → plans    |
| 第二阶段 Step 2：触发 brainstorming             | apply Phase 1：`superpowers:brainstorming`（人工触发）   |
| 第二阶段 Step 3：using-git-worktrees            | apply Phase 2：`superpowers:using-git-worktrees`（自动） |
| 第二阶段 Step 4：writing-plans                  | apply Phase 3：`superpowers:writing-plans`（自动）       |
| 第三阶段 Step 3：分派实现子代理                 | apply Phase 4-A：`subagent-driven-development` 串行循环  |
| 第三阶段 Step 3（TDD）：RED→GREEN→REFACTOR      | apply Phase 4-A：`test-driven-development` 强制循环      |
| 第三阶段 Step 4-5：规约/质量审查                | apply Phase 4-B/C：`requesting-code-review` ×2 子代理    |
| 第三阶段 Step 9：finishing-a-development-branch | apply Phase 5：`finishing-a-development-branch`（自动）  |

---

## 核心约束一览

| 约束                    | 机制                                                     |
| ----------------------- | -------------------------------------------------------- |
| 每 task = 一个 TDD 阶段 | tasks artifact instruction 强制 RED/GREEN/REFACTOR 分离  |
| 每 subagent = 一个 task | apply instruction：dispatch ONE subagent per task        |
| 不可并行                | apply instruction：NEVER dispatch multiple in parallel   |
| 必须提供测试输出        | apply instruction：evidence 字段检验真实命令输出         |
| 三级审查                | apply instruction：spec reviewer + code quality reviewer |
| 任务不可跳过/重排       | apply instruction：execute in order                      |

---

## 常用命令速查

```bash
openspec schemas                          # 列出所有可用 Schema
openspec schema which tdd-driven-v2       # 确认解析路径
openspec schema validate tdd-driven-v2    # 验证 schema.yaml 格式
openspec status --change <name> --json    # 查看制品 DAG 状态
openspec validate                         # 验证规约格式和逻辑一致性
```

---

## 集成测试阶段

`/opsx:archive <change-name>` 除完成 PR 提交和资料归档外，同时将变更移交测试团队进行**集成测试**。此阶段由 OpenSpec 协调，显式触发 4 个 NIO 自定义 Skill。

### 流程

```
/opsx:archive <change-name>
      │
      ├── [OpenSpec] SHA256 校验 verify 锁
      ├── [OpenSpec] 生成 PR 描述 + 产物归档
      │
      ├── 显式触发 nio-code-review      ← NIO 代码审查（团队规范 + 安全 + 性能）
      │         ↓（通过）
      ├── 显式触发 nio-qa               ← 功能验收（对照 proposal.md WHEN/THEN）
      │         ↓（通过）
      ├── 显式触发 nio-api-test         ← 接口契约（对照 spec.md GIVEN/WHEN/THEN）
      │         ↓（通过）
      └── 显式触发 nio-e2e-test         ← 端到端场景（覆盖完整用户路径）
                ↓（全部通过）
      [OpenSpec] 合并 Delta Spec 到主规范 + 清理 worktree
```

### 4 个 NIO 自定义 Skill

| Skill | 类型 | 验证对象 | 验证内容 |
|-------|------|---------|---------|
| `nio-code-review` | NIO 自定义 | 代码实现 | 团队编码规范、安全扫描（OWASP Top 10）、性能基线 |
| `nio-qa` | NIO 自定义 | proposal.md | 逐条验证 WHEN/THEN 行为是否可观察、可重现 |
| `nio-api-test` | NIO 自定义 | spec.md | 逐 Scenario 验证 GIVEN/WHEN/THEN 接口契约 |
| `nio-e2e-test` | NIO 自定义 | 完整用户路径 | 端到端场景覆盖，跨服务边界验证 |

### 触发规则

- 4 个 Skill **串行执行**，前一个通过才触发下一个
- 任意 Skill 不通过 → 阻断归档流程，返回开发阶段修复
- 全部通过后，OpenSpec 才执行 Delta Spec 合并和 worktree 清理
- 测试报告写入 `docs/superpowers/reviews/<change-name>-integration.md`

### 与提案产物的映射

| Skill | 读取产物 | 验证格式 |
|-------|---------|---------|
| `nio-qa` | `openspec/changes/<name>/proposal.md` | WHEN … THEN … |
| `nio-api-test` | `openspec/changes/<name>/spec.md` | GIVEN … WHEN … THEN … |
| `nio-e2e-test` | `openspec/changes/<name>/spec.md` + `design.md` | 完整场景路径 |
| `nio-code-review` | 代码变更（git diff vs main） | NIO 规范检查列表 |
