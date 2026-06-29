# OpenSpec + Superpowers + Gstack 组合开发流程

> 来源：[飞书文档](https://nio.feishu.cn/wiki/EWFuwKHhvi4NJukJJJwcnGbNnue)
> 转换时间：2026-06-05

# 主角介绍

## OpenSpec

OpenSpec 是 Fission AI 团队做的规约框架。核心理念就一句话：**写代码之前，先把要做什么写清楚，OpenSpec 的产物是结构化的 Markdown 文件，AI 编程助手可以直接读取、理解、执行。**

## Superpowers

**Superpowers 是方法论框架** — 它的核心是一个 94% PR 拒绝率的开源项目（来源：Superpowers CLAUDE.md），对待代码质量极其严格。它的 14 个 Skills 不是功能列表，而是一套工程纪律，**它确保 AI 在写代码时遵循标准化的工程实践。**

## gstack

**gstack 是角色化虚拟团队** — 它的核心是 Garry Tan（YC CEO）的日常开发工具集。23 个斜杠命令每个对应一个专家角色：`/office-hours` 是 YC 合伙人做产品诊断、`/plan-ceo-review` 是 CEO 挑战产品方向、`/qa` 是 QA 主管跑真实浏览器测试、`/ship` 是发布工程师跑完整发布流水线。

## Superpower VS Gstack

Superpower关注的是**工程规范和代码质量**；Gstack关注的是**产品决策和全生命周期交付**。

![[Superpower与Gstack对比.png]]

Superpowers 自动触发处理编码过程决策，gstack 手动触发处理产品流程决策，两者在不同层面做决策，不抢同一个触发点。

> ⚠️ 避免与其他插件冲突：
> gstack 支持无前缀模式（`/qa`）和前缀模式（`/gstack-qa`）。如果你同时装了其他也有 `/review` 命令的插件，建议用前缀模式：
> `cd ~/.claude/skills/gstack && ./setup --prefix`

# 如何配合

![[三者配合示意图1.png]]

![[三者配合示意图2.png]]

# 流程闭环

![[流程闭环示意图.png]]

# 开发流程

![[开发流程示意图.png]]

> 嵌入的电子表格内容（sheet-id: 0cIV0h），需查看原文档获取完整内容。

## OpenSpec + Superpowers在需求阶段的配合

![[OpenSpec与Superpower需求阶段配合.png]]

OpenSpec 是 Fission AI 团队做的规约框架。核心理念是：**写代码之前，先把要做什么写清楚，OpenSpec 的产物是结构化的 Markdown 文件，AI 编程助手可以直接读取、理解、执行。**

# 实战案例

## 需求阶段

**步骤 1：项目初始化**

架构师创建项目目录，安装 OpenSpec，初始化项目结构：

```Plain Text
# 创建项目目录
mkdir enterprise-kanban && cd enterprise-kanban

# 全局安装 OpenSpec
npm install -g @fission-ai/openspec@latest

# 初始化项目，指定要用的 AI 编程工具
openspec init --tools claude,cursor
```

`init` 命令会在项目根目录创建 `openspec/` 目录和基础 `config.yaml`

```Python
openspec/
├── specs/              # 当前系统的行为描述（真实来源）
│   └── <domain>/
│       └── spec.md
├── changes/            # 拟议的修改（每个变更一个文件夹）
│   └── <change-name>/
│       ├── proposal.md     # 意图和范围
│       ├── design.md       # 技术方案
│       ├── tasks.md        # 实现任务清单
│       └── specs/          # Delta 规约（具体变更内容）
└── config.yaml         # 项目配置
```

**步骤 2：配置项目上下文**

编辑 `openspec/config.yaml`，告诉 AI 你的技术栈和编码规则：

```Plain Text
schema: spec-driven
context:|
  Tech stack: TypeScript, React, Node.js, PostgreSQL
  Architecture: REST API + SPA frontend
rules:
proposal:
    -Includerollbackplan
specs:
    -UseGiven/When/Thenformat
```

`context` 字段很关键。它决定了 AI 生成规约时的技术方向。写清楚技术栈，AI 就不会给你生成 Python + Django 的方案。

`specs`字段规定了需要描述的格式。

**步骤 3：生成变更提案**

比如是一个**看板系统**的提案：

```Plain Text
/opsx:propose kanban-board-system
```

OpenSpec 会自动按顺序生成四个制品：

```Plain Text
openspec/changes/kanban-board-system/
├── proposal.md     # 看板系统的意图和范围
├── specs/          # 行为规约
│   └── board/
│       └── spec.md
├── design.md       # 技术方案
└── tasks.md        # 实现任务清单
```

其中 `specs/board/spec.md` 会用 Given/When/Then 格式定义行为：

```SQL
## Board Management

### Create Board

- GIVEN a user with board creation permission
- WHEN they submit a new board with title "Sprint 2026-Q2"
- THEN the system creates a board with default columns:
      Todo, In Progress, Done

### Task Status Transition

- GIVEN a task card with status "Todo"
- WHEN the user drags it to "In Progress" column
- THEN the system updates the task status
      and records the transition timestamp
```

**步骤 4：校验规约合法性**

```Plain Text
# 校验所有规约的格式和逻辑一致性
openspec validate

# 查看制品的生成状态
openspec status --change kanban-board-system --json
```

`validate` 会检查格式错误和逻辑矛盾。

规约设计完成后，Superpowers 上场。这一阶段的关键是把 OpenSpec 的粗粒度规约，细化为可执行的工程计划。

**步骤 5：触发 brainstorming生成实现计划**

在 AI 编程助手的对话窗口中，告诉它你要开始做看板系统。Superpowers 检测到你准备开始一项新的开发工作，会自动触发 brainstorming 技能：

```Plain Text
我想开始实现企业看板管理系统。项目里已经有 OpenSpec 的规约，
请先看一下 openspec/changes/kanban-board-system/ 目录下的文件。
```

> 👍 **关键注意**：Superpowers 的 brainstorming 技能第一步是"Explore project context"——它会扫描项目文件、文档和最近的 commits。但它**不会自动识别 OpenSpec 的目录结构**。你需要明确指出规约文件的位置，或者在对话中引导 AI 去读。

brainstorming 技能按以下流程推进（源自 brainstorming/SKILL.md 的 9 步 Checklist）：

1. **探索项目上下文** — 扫描项目结构、读取文档（此时会读到 OpenSpec 的制品）
2. **提出澄清问题** — 一次只问一个问题，逐个确认设计细节
3. **提出 2-3 个方案** — 带权衡分析和推荐方案
4. **��段展示设计** — 每段确认后继续下一段
5. **写设计文档** — 保存到固定路径
6. **设计自查** — 检查 placeholders、矛盾、歧义、范围
7. **用户审阅** — **请你确认设计文档**

```Plain Text
AI：Spec written and committed to docs/superpowers/specs/2026-04-18-kanban-board-design.md
    Please review it and let me know if you want to make any changes
    before we start writing out the implementation plan.
```

当你确认之后，自动执行第8、9步：

1. **隔离的 Git 工作空间 —** 自动调用 using-git-worktrees 技能创建
2. **生成实现计划 —** 自动调用 writing-plans 技能

> 🏆 **注意**：writing-plans 生成的是**独立的实现计划**，它基于 brainstorming 的设计文档，而不是直接读取 OpenSpec 的 `tasks.md`

完整的实现计划保存到：

```Plain Text
docs/superpowers/plans/2026-04-18-kanban-board.md
```

Superpowers 完成计划后，会做一轮**计划自查**（源码要求：检查 spec 覆盖度、placeholder 扫描、类型一致性），然后给出执行方式选择：

```Plain Text
I：Plan complete and saved to docs/superpowers/plans/2026-04-18-kanban-board.md
    Two execution options:

    1. Subagent-Driven (recommended) — 我为每个任务分派一个独立子代理，
       完成后自动审查，快速迭代

    2. Inline Execution — 在当前会话中批量执行，带人工检查点

    Which approach?
```

## 并行业务实现（后端和前端并行）

**推荐选择 Subagent-Driven**，Superpowers 的 subagent-driven-development 技能会自动启动。Superpowers 会自动执行以下循环：

实现一个任务

```Plain Text
AI：我正在使用 Subagent-Driven Development 来执行此计划。

    [读取计划文件：docs/superpowers/plans/2026-04-18-kanban-board.md]
    [提取所有 8 个任务的完整文本]

    Task 1: TaskCard 数据模型

    [分派实现子代理 — 包含完整任务文本和上下文]
```

实现子代理按 TDD 循环工作：

```Markdown
 子代理自动执行（在隔离上下文中）

# RED — 写失败测试
# 创建 tests/models/TaskCard.test.ts

# 验证 RED
$ vitest run tests/models/TaskCard.test.ts
# FAIL: TaskCard is not defined  ✅ 预期失败

# GREEN — 写最小实现
# 创建 src/models/TaskCard.ts

# 验证 GREEN
$ vitest run tests/models/TaskCard.test.ts
# PASS  ✅

# REFACTOR — 清理（如有必要）

# 提交
$ git add src/models/TaskCard.ts tests/models/TaskCard.test.ts
$ git commit -m "feat: add TaskCard model with required fields"
```

实现完成后，Superpowers 自动分派**规约审查子代理**（spec reviewer）：

> ⛱️ **审查参照物说明**：Superpowers 的规约审查子代理检查的是**实现计划**中的 spec 描述，不是 OpenSpec 的 spec 文件。两者的区别：OpenSpec 的 spec 定义的是系统行为（what），Superpowers 的实现计划定义的是工程步骤（how）。审查子代理确保代码**按计划实现**，至于计划本身是否符合 OpenSpec 的 spec，是 brainstorming 阶段要保证的。

```Plain Text
AI：[分派 spec reviewer 子代理]
    对照实现计划检查代码...

    Spec compliance review:
    ✅ TaskCard 模型包含计划中定义的所有字段
    ✅ 状态字段限定为 todo/in-progress/done
    ✅ 包含 createdAt/updatedAt 时间戳
    ✅ Spec compliant — 没有超出计划范围的额外实现
```

规约审查通过后，Superpowers 自动分派**代码质量审查子代理**（code quality reviewer）：

```Plain Text
# 获取 git 提交范围
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)

# 代码质量审查子代理检查：
# - 代码风格和命名规范
# - 是否有冗余代码
# - 测试质量（是否测试了真实行为而非 mock）
```

```Plain Text
AI：[分派代码质量审查子代理]

    Strengths: 清晰的接口定义，测试覆盖了创建场景

    Issues:
      Minor: 考虑为 status 字段添加联合类型而非 string

    Assessment: Ready to proceed ✅
```

三级审查全部通过，Task 标记完成，执行在一个任务。后续任务依次按同样的三级循环执行，直到所有任务完成。

**全部任务完成后，Superpowers 执行最终审查和分支收尾：**

```Plain Text
1. 运行全量测试套件
$ npm test
# 47 tests passing, 0 failures

# 2. 最终代码审查（审查整个实现，而非单个任务）
# 分派最终审查子代理，检查跨任务的一致性

# 3. 触发 finishing-a-development-branch 技能
```

Superpowers 会给你四个选择：

```Plain Text
AI：Implementation complete. What would you like to do?

    1. Merge back to main locally
    2. Push and create a Pull Request
    3. Keep the branch as-is (I'll handle it later)
    4. Discard this work
```

如果你选择创建 PR：

```Markdown
# Superpowers 自动执行
git push -u origin feature/kanban-board

gh pr create --title "feat: kanban board system" --body "$(cat <<'EOF'
## Summary
- 实现 TaskCard 数据模型和 CRUD API
- 实现看板管理 API（创建/查询/删除）
- 实现任务状态流转（Todo → In Progress → Done）

## Test Plan
- [ ] 47 个单元测试全部通过
- [ ] 手动验证看板创建流程
- [ ] 手动���证任务卡片拖拽状态流转
EOF
)"

# 清理 worktree
git worktree remove .worktrees/kanban-board
```

**前端实现 — 可与后端并行**

前端开发者可以同时开工。因为 OpenSpec 的 spec.md 已经定义了完整的 API 行为，前端不需要等后端写完再动手。

在**另一个 AI 助手会话**中（注意：Superpowers 的 subagent-driven-development 是单会话内串行的，前后端需要各自独立的会话），前端开发者执行：

```Plain Text
你（在 AI 助手中输入）：
我要实现看板系统的前端。
API 规约在 openspec/changes/kanban-board-system/specs/board/spec.md，
请基于这份规约生成前端组件。
```

Superpowers 同样会自动触发 brainstorming 技能。它读取 OpenSpec 的 spec.md，经过澄清问题和方案选择后，生成前端工程设计：

```Plain Text
docs/superpowers/specs/2026-04-18-kanban-board-frontend-design.md
```

然后在独立的工作树中走同样的 writing-plans → subagent-driven-development 流程。

基于 spec.md 中的 Given/When/Then 规约，AI 助手会在 TDD 循环中逐步生成代码。前后端能并行的前提是**规约先行**。只要 spec.md 定义清楚，双方就有共同的参照物，不需要面对面坐下来对接口。

## 需求迭代

openspec开发 -> superpower开发 -> gstack开发 -> openspec+superpower开发 -> superpower+gstack开发 -> openspec+superpower+gstack开发

适用场景：什么情况下采用什么流程？
