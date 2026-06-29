# OpenSpec\+Superpowers 协同

# **OpenSpec\+Superpowers 协同开发**

**OpenSpec** \- GitHub 上 40\.9k Star，定位是**规范驱动开发（SDD）**。它的核心思路是把需求写成机器可理解的规范文件，让 AI 和人先在文字层面达成共识，再动手写代码。

它的双文件夹模型很清晰：

- `openspec/specs/` \- 当前系统的规范，项目的事实来源

- `openspec/changes/` \- 每次变更的提案、设计文档、任务清单

**Superpowers** \- GitHub 上 158k Star，定位是**AI 编码代理的完整工作方法论**。它管的是 AI 写代码的过程：强制 TDD、子代理隔离、两阶段代码审查。

7 步强制流程：brainstorming → git worktree 隔离 → 拆 2\-5 分钟小任务 → 子代理执行 → TDD 循环 → 代码审查 → 分支收尾。每一步都不可跳过。

**本方案用OpenSpec 管需求层，用Superpowers 管执行层**。一个解决 AI 理解需求不准确的问题，一个解决 AI 写代码过程不可控的问题。

## 第〇阶段：理解老旧项目

**目标：**开发前梳理思路，特别适合摸底老项目，理解现有业务和设计与拆分模块，输出现有系统的规范快照。

**工具：**OpenSpec

|步骤|操作|触发方式|说明|
|---|---|---|---|
|1\. 项目初始化<br>|`npm install -g @fission-ai/openspec@latest` <br>`openspec init --tools claude,cursor`|人工触发<br>|创建 `openspec/` 目录和基础配置|
|2. 摸底老项目|`/opsx:explore` 探索现有代码|人工触发|`openspec/specs/` 目录下的生成现有系统规范，包括数据模型、接口列表、核心业务流程。|

> 审查规范快照的准确性，补充 AI 遗漏的业务规则。别指望 AI 一次就能完全理解老项目的所有隐含逻辑 \- 这部分需要人的经验补位。
> 
> 

## 第①阶段：需求规约设计

**目标**：写代码前，先把系统行为描述清楚

**工具：**OpenSpec

|步骤|操作|触发方式|说明|
|---|---|---|---|
|配置技术上下文|编辑 `openspec/config.yaml`<br>|**人工触发**|声明技术栈（如 TypeScript/React/Node\.js/PostgreSQL），避免 AI 生成偏离方向的方案，可以参考项目目录下的`AGENTS.md`|
|启动变更提案|在 AI 助手中执行 `/opsx:propose kanban-board-system`|**人工触发**|按 DAG 依赖自动生成 proposal\.md → specs/ → design\.md → tasks\.md|
|校验规约|`openspec validate` \+ `openspec status --change kanban-board-system --json`|**人工触发**|检查格式错误和逻辑矛盾（如状态冲突）；赶时间可用 `/opsx:ff` 快进|

## 第②阶段：生成开发计划

**目标**：将粗粒度规约细化为可执行的工程计划

**工具：**Superpowers

|步骤|操作|触发方式|触发来源|说明|
|---|---|---|---|---|
|1\. 安装 Superpowers|`/plugin install superpowers@claude-plugins-official` 或 `/add-plugin superpowers`|**人工触发**|—|14 个 Skills 注册到 AI 助手|
|2\. 触发 brainstorming|告诉 AI"开始实现看板系统，规约在 `openspec/changes/kanban-board-system/`"|**人工触发**|—|启动后，AI **自动执行** 9 步流程：探索上下文 → 澄清问题 → 方案选择 → 分段确认 → 写设计文档 → 设计自查 → 用户审阅|
|3\. 创建隔离工作空间|Superpowers 调用 using\-git\-worktrees|**自动触发**|**brainstorming**（设计审批后）|在 `.worktrees/kanban-board` 创建分支，自动安装依赖并验证测试基线|
|4\. 生成原子实现计划|Superpowers 调用 writing\-plans|**自动触发**|**brainstorming**（最后一步"Transition to implementation"）|读取设计文档，拆分为 2\-5 分钟/步的原子任务，保存到 `docs/superpowers/plans/`；推荐选择 **Subagent\-Driven** 执行方式|

> `writing-plans` 读取的是 brainstorming 产出的工程设计文档，不读取 OpenSpec 的 `tasks.md`。`tasks.md` 是 OpenSpec 的业务任务追踪（checkbox 状态机），`writing-plans` 产出是 Superpowers 的 2\-5 分钟原子执行步骤——两者独立，职责不同。
> 
> 

## 第③阶段：代码并行实现

**目标**：AI 子代理自动执行开发，前后端基于同一份规约同步推进

**工具：**Superpowers

**后端流程**（单会话内串行自动循环）：

|步骤|操作|触发方式|触发来源|说明|
|---|---|---|---|---|
|1\. 选择 Subagent\-Driven 方式|在 AI 助手中回复"选择方案 1"|**人工触发**|—|确认执行方式后，后续全部自动循环|
|2\. 读取计划并提取任务|Superpowers 读取 `docs/superpowers/plans/` 并提取所有任务|**自动触发**|**用户选择 Subagent\-Driven**|准备任务上下文|
|3\. 分派实现子代理|为每个 Task 创建独立子代理|**自动触发**|**subagent\-driven\-development 控制器**|按 TDD 循环执行：RED写失败测试 → GREEN最小实现 → REFACTOR|
|4\. 分派规约审查子代理|检查代码是否按计划实现|**自动触发**|**实现子代理完成**|确保代码符合实现计划中的 spec 描述|
|5\. 分派代码质量审查子代理|检查风格、性能、测试质量|**自动触发**|**规约审查通过后**|三级审查全部通过才标记任务完成|
|6\. 进入下一 Task|重复步骤 3\-5|**自动触发**|**上一 Task 三级审查通过**|循环直至所有任务完成|
|7\. 运行全量测试|`npm test`|**自动触发**|**全部 Task 完成**|验证整体一致性|
|8\. 最终代码审查|分派审查子代理检查跨任务一致性|**自动触发**|**全量测试通过**|跨任务边界检查|
|9\. 触发分支收尾|执行 finishing\-a\-development\-branch|**自动触发**|**最终审查通过**|提供四个选项：合并/创建 PR/保留分支/丢弃|
|10\. 选择收尾方式|回复"创建 PR"或"合并"等|**人工触发**|—|人做最终决策，AI 执行具体操作|

**前端流程**（**独立 AI 会话**中并行执行）：

|步骤|操作|触发方式|触发来源|说明|
|---|---|---|---|---|
|1\. 启动前端实现|在**新 AI 会话**中告知"实现前端，规约在 `openspec/changes/.../spec.md`"|**人工触发**|—|前后端需独立会话，Superpowers 子代理驱动是单会话串行|
|2\. 自动触发 brainstorming|AI 检测到新开发工作|**自动触发**|**用户输入启动指令**|读取 spec\.md，经澄清问题 → 方案选择 → 生成前端设计文档|
|3\. 自动调用 worktree|创建隔离工作空间|**自动触发**|**brainstorming（设计审批后）**|同后端流程|
|4\. 自动调用 writing\-plans|生成前端原子实现计划|**自动触发**|**brainstorming（最后一步）**|同后端流程|
|5\. 后续子代理循环|TDD → 规约审查 → 质量审查|**自动触发**|**用户选择 Subagent\-Driven**|同后端三级审查循环|

> **并行前提**：spec\.md 已定义清楚 API 行为，双方有共同参照物，无需面对面联调
> 
> 

---

## 第④阶段：归档

**目标**：Delta Spec 合并入主规约 `specs/`，成为系统行为的一部分。

**工具：**OpenSpec

|步骤|操作|触发方式|说明|
|---|---|---|---|
|归档合并|`/opsx:archive <change-name>`|**人工触发**|Delta Spec 合并入主规约 `specs/`，成为系统行为的一部分|

# 进阶模式

OpenSpec 作为唯一用户操作入口，不必记住OpenSpec 和 Superpowers 两组命令，Superpowers 作为 Skill Library集成到OpenSpec对应的命令中。

另外集成测试阶段、部署阶段的命令，增加到OpenSpec的WorkFlow中。

```JSON
/opsx:explore
      ↓
/opsx:propose
      ↓
(人工审批)
      ↓
/opsx:apply
      ↓
(开发完成，人工审批)
      ↓
PR_CREATED
      ↓
/opsx:archive
      ↓
(合并PR，提测)
      ↓
/opsx:qa
      ↓
(测试执行)
      ↓
QA_PASSED
      ↓
/opsx:release
```

这样，各阶段的命令，都统一`/opsx:xxx`的形式，如下：

|步骤|阶段|命令|核心目标|
|---|---|---|---|
|0|第〇阶段：理解老旧项目|`/opsx:explore` 探索现有代码|摸底老项目，理解现有业务和设计与拆分模块|
|1|第①阶段：需求规约设计|`/opsx:propose <change-name>`|冻结需求与设计|
|2|第②阶段：生成开发计划<br>第③阶段：代码并行实现<br>|`/opsx:apply <change-name>`|完成功能与单测，创建 PR|
|3|第④阶段：归档|`/opsx:archive <change-name>`|合并 PR|
|4|第⑤阶段：集成测试<br>合并了多个PR并提测后执行。|`/opsx:qa`选择测试类型：<br>- nio\-code\-review<br>- nio\-api\-test<br>- nio\-e2e\-test<br>可多选|API测试、E2E测试、代码审查、覆盖率分析，生成PR\-CodeReview报告、测试报告和覆盖率报告。<br>```Plain Text<br>├── 显式触发 nio-code-review      ← NIO 代码审查（团队规范 + 安全 + 性能）<br>│         ↓（通过）<br>├── 显式触发 nio-qa               ← 功能验收（对照 proposal.md WHEN/THEN）<br>│         ↓（通过）<br>├── 显式触发 nio-api-test         ← 接口契约（对照 spec.md GIVEN/WHEN/THEN）<br>│         ↓（通过）<br>└── 显式触发 nio-e2e-test         ← 端到端场景（覆盖完整用户路径）<br>```|
|5|第⑥阶段：部署|`/opsx:release`<br>选择环境、版本、分支。|灰度、发布、回滚管理|

# 关键点设计

## `/opsx:apply` 

触发后，会按以下顺序调用 Superpowers 技能，五个阶段串行执行：

```Plain Text
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
                                         用户选择处置方式  （最终人工决策）
```

核心要点

|维度|关键设计|
|---|---|
|**协作契约**|OpenSpec 的 spec\.md 是前后端共同的真实来源|
|**隔离机制**|Git worktree 保证开发环境独立|
|**质量关卡**|三级审查（实现 → 规约合规 → 代码质量）层层过滤|
|**变更追溯**|Delta Spec \+ WAL 式归档，随时回退不污染原始数据|
|**人机分工**|人负责"定义清楚问题"（写规约、做关键决策），AI 负责"按规矩执行"（生成代码、跑测试、做审查）|

## `/opsx:qa`

API测试、E2E测试、代码审查、覆盖率分析。对应测试团队提供的各种 Skill。

目标：

对已创建 PR 或已合并待提测代码执行自动化质量验证，生成统一质量报告。

与 `/opsx:apply` 不同：

- `/opsx:apply` 关注代码是否实现需求 

- `/opsx:qa` 关注代码是否达到提测标准 

输入：

```Plain Text
proposal.md
spec.md
design.md
tasks.md
qa-plan.md
PR Diff
当前运行代码
```

输出：

```Plain Text
reports/code-review.md
reports/api-test-report.html
reports/e2e-report.html
reports/coverage-report.html
reports/quality-gate.md
```

执行流程：

```Plain Text
人工触发
/opsx:qa
      ↓
读取 qa-plan.md
      ↓
nio-code-review
      ↓
nio-api-test
      ↓
nio-e2e-test
      ↓
coverage-analysis
      ↓
Quality Gate
      ↓
QA_PASSED / QA_FAILED
```

### Code Review

调用：

```Plain Text
skill: nio-code-review
```

检查：

- proposal\.md 需求一致性 

- spec\.md 场景一致性 

- 安全问题 

- 性能问题 

- 可维护性问题 

生成：

```Plain Text
reports/code-review.md
```

### API Contract Test

调用：

```Plain Text
skill: nio-api-test
```

依据：

```Plain Text
spec.md
OpenAPI
运行服务
```

自动从 GIVEN/WHEN/THEN 场景生成契约测试。

生成：

```Plain Text
reports/api-test-report.html
reports/api-test-report.json
```

### E2E Test

调用：

```Plain Text
skill: nio-e2e-test
```

依据：

```Plain Text
proposal.md
spec.md
```

自动抽取用户旅程并生成 Playwright/Cypress 测试。

生成：

```Plain Text
reports/e2e-report.html
```

### Coverage Analysis

调用：

```Plain Text
skill: coverage-analysis
```

统计：

```Plain Text
Line Coverage
Branch Coverage
Function Coverage
```

生成：

```Plain Text
reports/coverage-report.html
```

### Quality Gate

汇总：

```Plain Text
Code Review
API Test
E2E Test
Coverage
```

生成：

```Plain Text
reports/quality-gate.md
```

结果：

```Plain Text
QA_PASSED
```

或：

```Plain Text
QA_FAILED
```

只有 QA\_PASSED 才允许进入：

```Plain Text
/opsx:release
```

---

# 3\.3 /opsx:release

灰度、发布、回滚管理，对应发布平台 CLI 与 Skill。

目标：

统一部署、灰度、发布、回滚流程。

输入：

```Plain Text
release-plan.md
QA Report
Git Tag
PR
```

输出：

```Plain Text
release/deployment-log.md
release/health-check.md
release/release-record.md
```

流程：

```Plain Text
人工触发
/opsx:release
      ↓
读取 release-plan.md
      ↓
选择环境
      ↓
执行部署
      ↓
健康检查
      ↓
灰度发布
      ↓
全量发布
      ↓
发布完成
```

### Deploy

调用：

```Plain Text
skill: deploy-release
```

支持：

```Plain Text
ArgoCD
Spinnaker
Jenkins
GitHub Actions
Kubernetes CLI
```

生成：

```Plain Text
release/deployment-log.md
```

### Health Check

调用：

```Plain Text
skill: health-check
```

检查：

```Plain Text
Error Rate
Latency
CPU
Memory
Service Status
```

生成：

```Plain Text
release/health-check.md
```

### Canary Release

调用：

```Plain Text
skill: canary-release
```

例如：

```Plain Text
traffic:
  - 5%
  - 20%
  - 50%
  - 100%
```

逐阶段观察：

```Plain Text
Error Rate
Success Rate
Latency
Business Metrics
```

### Rollback

调用：

```Plain Text
skill: rollback-release
```

触发条件：

```Plain Text
rollback:
  error_rate > threshold
  latency > threshold
  health_check_failed
```

生成：

```Plain Text
release/release-record.md
```

结果：

```Plain Text
RELEASE_SUCCEEDED
```

或：

```Plain Text
RELEASE_ROLLED_BACK
```

# 自定义OpenSpec的Schema

> 参考https://github\.com/Fission\-AI/OpenSpec/tree/main/schemas
> 
> 

要想实现进阶模式，这里的关键设计是：

- 将 Superpowers 执行的第②阶段：生成开发计划和第③阶段：代码并行实现整合进 `/opsx:apply`

- 新增 QA 与 Release 两类 Artifact，用于驱动测试与发布阶段 

- 不修改 OpenSpec 源码，不新增 qa/release Workflow 节点 

- `/opsx:qa` 与 `/opsx:release` 作为 Dispatcher 命令，分别读取 `qa-plan.md` 与 `release-plan.md` 执行对应 Skill

## 初始化Schema

```Bash
# 方式 A：从零创建（会生成模板结构）
openspec schema init spec-driven-dd

# 方式 B：Fork 现有模式spec-driven再修改(推荐)
openspec schema fork spec-driven spec-driven-dd
```

`openspec schema`命令会在当前目录创建`schemas`文件夹。Schema 存储位置（二选一）：

- 项目本地（可版本控制）：`openspec/schemas/tdd-driven-v2/`

- 用户全局（所有项目可用）：`~/.local/share/openspec/schemas/spec-driven-dd/`

在项目本地创建，整个目录的样子如下：

```Plain Text
openspec/
├── schemas/
│   └── spec-driven-dd/
│       ├── schema.yaml          # 工作流定义（Workflow DSL 核心）
│       └── templates/
│           ├── proposal.md      # WHEN/THEN 可测试行为
│           ├── spec.md          # GIVEN/WHEN/THEN 场景
│           ├── design.md        # 技术设计 + 测试文件路径
│           ├── tasks.md         # 原子 TDD 任务 checkbox
│           └── plan.md          # 执行计划 + 证据要求
│           ├── qa-plan.md       # 
│           └── release-plan.md  # 
```

## 设计schema\.yaml

`schema.yaml`内容如下

```YAML
name: spec-driven-dd
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
    generates: specs/****/*.md**
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
      - Test runner command (e.g., npm test)requires:- proposal

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
      
  - id: qa-plan
    generates: qa-plan.md
    template: templates/qa-plan.md
    description: Integrated QA execution plan
    instruction: |
      Define:
      - code review strategy
      - API contract testing strategy
      - E2E testing scope
      - coverage requirements
      - quality gate rules
    requires:
      - tasks

  - id: release-plan
    generates: release-plan.md
    template: templates/release-plan.md
    description: Deployment and rollback plan
    instruction: |
      Define:
      - deployment strategy
      - health check rules
      - canary rollout stages
      - rollback criteria
    requires:
      - qa-plan

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
      A. [superpowers:test-driven-development]RED:      write failing test — MUST provide failure output
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

验证 Schema 格式：

```Bash
openspec schema validate spec-driven-dd
openspec schema which spec-driven-dd  # 确认解析路径
```

## 激活项目配置`config.yaml`

更新 `openspec/config.yaml`，指定使用`spec-driven-dd`这个Schema：

```YAML
# openspec/config.yaml
schema: spec-driven-dd

context: |
  [填写你的项目技术栈、测试框架、核心约束]
  
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

## 模板文件

- templates/qa\-plan\.md

```XML
# QA Plan: {{change_name}}

## Code Review

<!-- 审查策略 -->

## API Contract Test

<!-- 接口契约测试 -->

## E2E Test

<!-- 端到端场景 -->

## Coverage Requirements

<!-- 覆盖率要求 -->

## Quality Gate

<!-- PASS/FAIL 规则 -->
```

- templates/release\-plan\.md

```XML
# Release Plan: {{change_name}}

## Deployment Strategy

<!-- 发布方式 -->

## Health Check

<!-- 健康检查项 -->

## Canary Plan

<!-- 灰度比例 -->

## Rollback Strategy

<!-- 回滚条件 -->
```

- templates/proposal\.md

```Markdown
**# Proposal: {{change_name}}**
***## Problem***
*<!-- 描述要解决的问题 -->*
***## Testable Behaviors***
*<!-- WHEN/THEN 格式列出每一个可测试行为 -->*
*- WHEN*
*  THEN*

***## Acceptance Criteria***
*<!-- 验收标准 -->*
*- [ ]*
```

- templates/spec\.md

```Markdown
**# Spec: {{change_name}}**
**## Scenarios**
**### Scenario 1: [name]**
- GIVEN: [前置条件]
- WHEN: [操作]
- THEN: [期望结果]

<!-- Repeat for each scenario -->
```

- templates/design\.md

```Markdown
**# Design: {{change_name}}**
**## File Structure**
<!-- 列出要创建的文件，包括测试文件 -->
**## Test Strategy**
<!-- 每个 test 文件的测试策略 -->
**## Implementation Notes**
<!-- 实现要点 -->
```

- templates/tasks\.md

```Markdown
**# Tasks: {{change_name}}**
**## Atomic TDD Task List**
<!-- 每个 task 只能是一个 TDD 阶段 -->
<!-- 必须使用 checkbox 格式 -->
**### [AI fills feature name]**
- [ ] RED: ...
- [ ] GREEN: ...
- [ ] REFACTOR: ...
```

- templates/plan\.md

```Markdown
**# Execution Plan: {{change_name}}**
**## Micro-tasks**
**### Step 1: RED — [description]**
- Test file: [path]
- Assertion: [what to test]
- Expected failure: [reason]
- Verify: `npm test -- [test-file]`
**### Step 2: GREEN — [description]**
- Pass test from: Step 1
- Minimal code: [what to implement]
- Verify: `npm test -- [test-file]`

<!-- Repeat for each task -->
---
**## Execution Mode Selection**

REQUIRED: Use superpowers:subagent-driven-development skill for execution.
```

# 最轻量防护：SHA256 锁定

在纯两工具设计下，没有外部守护进程。防止「规约被悄悄修改」的唯一机制是文件哈希。

触发时机：人工确认门通过后，OpenSpec 对该 phase 所有已完成产物计算 SHA256，写入 `.opsx/state.json`：

```JSON
{"locks": {"spec.md": "sha256:a3f2c1...","design.md": "sha256:9b4e7a...","tasks.md": "sha256:d1c3f8..."}}
```

防护效果：下一个命令（如 `/opsx:apply`）启动时，Dispatcher 重新计算哈希与记录比对。不一致 → 中止并报警，强制重新走人工确认门。

典型风险场景：

```Plain Text
/opsx:propose → 人工确认 tasks.md ✅
      ↓
开发者手动缩减了 tasks.md 的验收标准（无人知晓）
      ↓
/opsx:apply → 哈希不匹配 → ABORT
      ↓
必须重新 /opsx:propose，明确确认新版规约
```

可以去掉吗：可以。若团队用 git commit \+ PR review 代替，`lock_on_gate: false` 即可，gate 退化为纯"确认继续"语义，无文件保护。

