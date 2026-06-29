---
title: "从零到一：OpenSpec + Superpowers 新项目全流程实战指南"
source: "https://mp.weixin.qq.com/s?__biz=Mzg4MzcyOTQ2NQ==&mid=2247490468&idx=1&sn=99d55ec01da8931000212ade53766324&chksm=cf43aef2f83427e40fb57e45341d7bb96a3e551af5cd7ceb5eb08493875a521925145df2731a&cur_album_id=4354638012475867143&scene=190#rd"
author:
  - "[[运维有术]]"
published: false
created: 2026-06-06
description: "🚩 2026 年「术哥无界」系列实战文档 X 篇原创计划 第 87 篇，AI 编程最佳实战「2026」系列第"
tags:
  - "clippings"
ingested: false
---
运维有术 *2026年4月19日 09:29*

> 🚩 2026 年「术哥无界」系列实战文档 X 篇原创计划 第 *87* 篇，AI 编程最佳实战「2026」系列第 *19* 篇
> 
> 大家好，欢迎来到 **术哥无界 | ShugeX ｜ 运维有术** 。
> 
> 我是 **术哥** ，一名专注于 AI 编程、AI 智能体、Agent Skills、MCP、云原生、AIOps、Milvus 向量数据库的 **技术实践者与开源布道者** ！
> 
> **Talk is cheap, let's explore。无界探索，有术而行。**

![封面图](https://mmbiz.qpic.cn/mmbiz_png/icibtH5FrDwPcnxgW2YuG9R9l3LRRLtFzqVNN03icZo6JXqX7mUJ2dFa3ft0HycuLhGwiafGJtzNWxghCUu7bmib2bzVdiayGx2P18qaAiaPxiaibSfk/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

封面图

你在用 AI 写代码时，有没有遇到过这些问题：前后端对不上接口、需求改了但代码没同步、AI 助手写着写着就跑偏了？

翻了一圈社区讨论，发现这类问题几乎是 AI 编程的通病。根源在于：AI 编程助手擅长生成代码，但不擅长维护上下文一致性——需求、设计和代码三者之间缺少一个强制的对齐机制。

OpenSpec 和 Superpowers 这两个工具，恰好分别解决了这个问题的一端。前者管 **要做什么** ，后者管 **怎么做** 。合在一起，就是一条从需求规约到可运行代码的自动化流水线。

这篇文章会先拆解两个工具各自的能力和协作机制，然后用一个企业看板系统做完整实战演示，结尾聊聊这套工具链对团队分工意味着什么。

## 1\. 工具链能力矩阵：一个管需求，一个管工程

### 1.1 OpenSpec：用规约当团队的协作契约

OpenSpec 是 Fission AI 团队做的规约框架。核心理念就一句话： **写代码之前，先把要做什么写清楚，而且要写成 AI 可读的格式。**

它不是让你写 PRD 文档那种纯文本。OpenSpec 的产物是结构化的 Markdown 文件，AI 编程助手可以直接读取、理解、执行。

安装只需要一行命令：

```
npm install -g @fission-ai/openspec@latest
```

初始化后，项目里会出现这样的目录结构：

```
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

`specs/` 是整个系统的真实来源——它描述的是系统当前的行为。每次你要加功能或改需求，不是直接改 specs，而是创建一个新的 `change` 。

有意思的是它的 Delta Spec 机制。变更用增量描述，而不是全量覆盖：

- **ADDED Requirements** — 新增的行为
- **MODIFIED Requirements** — 修改的行为
- **REMOVED Requirements** — 废弃的行为

这和数据库的 WAL（Write-Ahead Log）是同一个思路： **先记录变更意图，归档时再合并到主规约。好处是可以随时回退，不会污染原始数据。**

OpenSpec 的制品之间有依赖关系，形成一个有向无环图（DAG）：

```
proposal（根节点）
    │
    ├── specs（依赖 proposal）
    │
    ├── design（依赖 proposal）
    │
    └── tasks（依赖 specs + design）
```

这意味着你不能跳过 proposal 直接写 tasks。AI 会按依赖顺序自动生成这些制品。

### 1.2 Superpowers：让 AI 编码代理按规矩干活

Superpowers 是 Jesse Vincent（Prime Radiant 团队）开发的工作流框架。如果说 OpenSpec 是 **立法机构** ，那 Superpowers 就是 **执法机构** —— **它确保 AI 在写代码时遵循标准化的工程实践。**

安装方式取决于你用的 AI 工具：

```
# Claude Code 用户
/plugin install superpowers@claude-plugins-official

# Cursor 用户
/add-plugin superpowers
```

它做了一件事： **给 AI 编码代理装上一套标准化的工作流程。**

这套流程包括 7 个核心工作流：

| 工作流 | 做什么 |
| --- | --- |
| brainstorming | 苏格拉底式对话，写代码之前先理清需求 |
| using-git-worktrees | 创建隔离的 Git 工作空间 |
| writing-plans | 把工作拆成 2-5 分钟可完成的小任务 |
| subagent-driven-development | 用子代理逐任务执行 |
| test-driven-development | 强制 RED-GREEN-REFACTOR 循环 |
| requesting-code-review | 自动触发代码审查 |
| finishing-a-development-branch | 完成分支，验证测试 |

其中子代理驱动开发（subagent-driven-development）的流程设计得比较精巧。不是简单地让 AI 写完代码就完事，而是三级审查层层过滤：

1. 为每个任务分派一个实现子代理
2. 实现完成后，自动分派规约审查子代理（检查代码是否符合设计规约）
3. 规约审查通过后，分派代码质量审查子代理（检查代码风格、性能等）
4. 三级审查全部通过，才标记任务完成

Superpowers 生成的文档也有固定的存放路径：

```
# 设计文档
docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md

# 实现计划
docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md
```

这些文档会被后续的审查流程自动读取。

![工具生态对比图](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

工具生态对比图

### 1.3 逻辑打通：两者如何在指令级实现闭环

很多人看了 OpenSpec 和 Superpowers 的介绍，觉得挺不错，但没想清楚它们怎么配合。关键在三个衔接点。

**衔接点一：tasks.md 到 writing-plans**

OpenSpec 生成的 tasks.md 是粗粒度的任务清单，比如 **实现任务卡片 CRUD** 。Superpowers 拿到后，通过 writing-plans 技能把它拆成更细的实现步骤——创建数据模型、写路由、加校验、编测试，每一步 2-5 分钟。

**衔接点二：design.md 到 subagent-driven-development**

OpenSpec 的 design.md 是技术方案。Superpowers 的子代理在写代码时会读取这份文档来理解上下文。比如 design.md 说了 **用 PostgreSQL 存储、REST API 接口** ，子代理就不会给你生成 MongoDB + GraphQL 的代码。

**衔接点三：specs/ 到 requesting-code-review**

Superpowers 做代码审查时，把 OpenSpec 的行为规约当作审查标准。代码是否合规约，不是人说了算，是 spec 说了算。

整个流转过程：

```
OpenSpec                     Superpowers
/opsx:propose                brainstorming
→ proposal + specs           → 细化设计文档
→ design + tasks             → 拆分实现计划
                              → 子代理逐任务实现
/opsx:apply                  → 规约审查 + 代码审查
→ 实现任务                   → TDD 循环
                              → 完成分支
/opsx:archive
→ 合并 Delta Spec
```

说白了，OpenSpec 的产物就是 Superpowers 的输入。一个是上游，一个是下游。两者通过文件系统中的 Markdown 文件完成握手——不依赖任何 API 调用或网络通信。

![协作衔接流程图](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

协作衔接流程图

## 2\. 角色驱动的全流程实战：以看板系统为例

接下来用一个具体的项目——企业看板管理系统，演示从零到一的完整流程。需求包括：看板创建、任务卡片管理、状态流转（Todo / In Progress / Done）、多人协作。

![四阶段实战流水线图](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

四阶段实战流水线图

### 2.1 第一阶段：规约设计（架构师执行）

这一步的目标： **在写一行代码之前，把看板系统的行为描述清楚。**

**步骤 1：项目初始化**

架构师创建项目目录，安装 OpenSpec，初始化项目结构：

```
# 创建项目目录
mkdir enterprise-kanban && cd enterprise-kanban

# 全局安装 OpenSpec
npm install -g @fission-ai/openspec@latest

# 初始化项目，指定要用的 AI 编程工具
openspec init --tools claude,cursor
```

`init` 命令会在项目根目录创建 `openspec/` 目录和基础 `config.yaml` 。

**步骤 2：配置项目上下文**

编辑 `openspec/config.yaml` ，告诉 AI 你的技术栈和编码规则：

```
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

**步骤 3：启动看板系统的变更提案**

在 AI 编程助手（Claude Code 或 Cursor）中执行 slash 命令：

```
/opsx:propose kanban-board-system
```

OpenSpec 会根据 DAG 依赖关系，自动按顺序生成四个制品：

```
openspec/changes/kanban-board-system/
├── proposal.md     # 看板系统的意图和范围
├── specs/          # 行为规约
│   └── board/
│       └── spec.md
├── design.md       # 技术方案
└── tasks.md        # 实现任务清单
```

其中 `specs/board/spec.md` 会用 Given/When/Then 格式定义行为：

```
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

```
# 校验所有规约的格式和逻辑一致性
openspec validate

# 查看制品的生成状态
openspec status --change kanban-board-system --json
```

`validate` 会检查格式错误和逻辑矛盾。比如你在 spec 里写了 **任务只能处于 Todo 状态** ，但 transition 规则里又允许流转到 In Progress，就会报冲突。

如果你赶时间，也可以用快进命令一次性生成所有制品：

```
/opsx:ff kanban-board-system
```

### 2.2 第二阶段：脚手架自动化生成（架构师/Lead 执行）

规约设计完成后，Superpowers 上场。这一阶段的关键是把 OpenSpec 的粗粒度规约，细化为可执行的工程计划。

> **前置说明** ：Superpowers 不是命令行工具，它是一套安装在 AI 编程助手里的 Skills 系统。你不需要在终端里输入 `superpowers xxx` ，而是通过自然语言对话或特定触发语句来激活对应的 Skill。AI 检测到你在做某类工作时，会自动调用对应流程。

**步骤 1：安装 Superpowers 插件**

```
# Claude Code 中执行
/plugin install superpowers@claude-plugins-official

# 或 Cursor Agent Chat 中执行
/add-plugin superpowers
```

安装完成后，Superpowers 的 14 个 Skills 会自动注册到 AI 编程助手中。你可以用以下命令确认安装成功：

```
# Claude Code 中查看已安装插件
/plugin list
```

**步骤 2：触发 brainstorming — 把规约细化成工程设计**

在 AI 编程助手的对话窗口中，告诉它你要开始做看板系统。Superpowers 检测到你准备开始一项新的开发工作，会自动触发 brainstorming 技能：

```
你（在 AI 助手中输入）：
我想开始实现企业看板管理系统。项目里已经有 OpenSpec 的规约，
请先看一下 openspec/changes/kanban-board-system/ 目录下的文件。
```

> **关键注意** ：Superpowers 的 brainstorming 技能第一步是"Explore project context"——它会扫描项目文件、文档和最近的 commits。但它 **不会自动识别 OpenSpec 的目录结构** 。你需要明确指出规约文件的位置，或者在对话中引导 AI 去读。

Superpowers 的 brainstorming 技能按以下流程推进（源自 brainstorming/SKILL.md 的 9 步 Checklist）：

1. **探索项目上下文** — 扫描项目结构、读取文档（此时会读到 OpenSpec 的制品）
2. **提出澄清问题** — 一次只问一个问题，逐个确认设计细节
3. **提出 2-3 个方案** — 带权衡分析和推荐方案
4. **分段展示设计** — 每段确认后继续下一段
5. **写设计文档** — 保存到固定路径
6. **设计自查** — 检查 placeholders、矛盾、歧义、范围
7. **用户审阅** — 请你确认设计文档

整个过程中，AI 会按顺序问你类似这样的问题：

```
AI：我看了 OpenSpec 的规约。看板的状态流转，除了 Todo/In Progress/Done
    之外，我有两个方案：

    方案 A：只支持三种固定状态，实现简单
    方案 B：支持自定义列名，但需要额外的列配置表

    我推荐方案 A。YAGNI 原则——先做最简单的版本。
    你倾向哪个？

你：同意方案 A，先支持三种默认状态。
```

确认完设计后，Superpowers 将设计文档保存到固定路径：

```
docs/superpowers/specs/2026-04-18-kanban-board-design.md
```

然后 Superpowers 会做 **设计自查** （检查有无 TBD、矛盾、范围过大等问题），修复后请你审阅：

```
AI：Spec written and committed to docs/superpowers/specs/2026-04-18-kanban-board-design.md
    Please review it and let me know if you want to make any changes
    before we start writing out the implementation plan.
```

**步骤 3：创建隔离的 Git 工作空间**

你审批设计后，Superpowers 在 brainstorming 流程内部直接调用 using-git-worktrees 技能（而不是单独触发），在隔离分支上准备工作空间：

```
# Superpowers 在 brainstorming 流程内自动执行

# 1. 检查是否已有 .worktrees 目录
ls -d .worktrees 2>/dev/null

# 2. 确认 .worktrees 已被 gitignore（防止意外提交 worktree 内容）
git check-ignore -q .worktrees 2>/dev/null

# 3. 创建隔离的 worktree 和新分支
git worktree add .worktrees/kanban-board -b feature/kanban-board

# 4. 自动检测并在 worktree 中安装依赖
cd .worktrees/kanban-board
#   → 检测到 package.json，执行 npm install
#   → 检测到 Cargo.toml，执行 cargo build
#   → （按项目实际情况自动选择）

# 5. 验证测试基线
npm test
```

Superpowers 输出：

```
Worktree ready at .worktrees/kanban-board
Tests passing (0 tests, 0 failures)
Ready to implement kanban-board
```

> **注意** ：worktree 在 brainstorming 阶段就创建了（源码标注为 "REQUIRED when design is approved"），不是之后才创建。writing-plans 的说明也写了 "This should be run in a dedicated worktree (created by brainstorming skill)"。

**步骤 4：触发 writing-plans — 生成 2-5 分钟粒度的实现计划**

brainstorming 的最后一步是自动调用 writing-plans 技能（源码："Transition to implementation — invoke writing-plans skill"）。你不需要手动触发。

Superpowers 的 writing-plans 技能会读取刚才生成的设计文档（ `docs/superpowers/specs/` ），结合项目上下文，拆分出详细的实现计划。计划中的每个步骤都是 2-5 分钟可完成的原子操作。

> **注意** ：writing-plans 生成的是 **独立的实现计划** ，它基于 brainstorming 的设计文档，而不是直接读取 OpenSpec 的 `tasks.md` 。OpenSpec 的 tasks.md 和 Superpowers 的实现计划是两份独立的文档——前者是业务任务清单，后者是工程实现步骤。

计划格式如下（源自 writing-plans/SKILL.md 的模板）：

```
# Kanban Board Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
> or superpowers:executing-plans to implement this plan task-by-task.
> Steps use checkbox (\`- [ ]\`) syntax for tracking.

**Goal:** 实现看板系统的任务卡片 CRUD 功能
**Architecture:** REST API + React SPA, PostgreSQL 存储
**Tech Stack:** TypeScript, Express, React, PostgreSQL, Vitest

---

### Task 1: TaskCard 数据模型

**Files:**
- Create: \`src/models/TaskCard.ts\`
- Test: \`tests/models/TaskCard.test.ts\`

- [ ] **Step 1: 写失败测试**

\`\`\`typescript
test('creates a task card with required fields', () => {
  const card = new TaskCard({
    title: '实现登录功能',
    boardId: 'board-1',
    status: 'todo'
  });
  expect(card.id).toBeDefined();
  expect(card.status).toBe('todo');
});
\`\`\`

- [ ] **Step 2: 运行测试确认失败**
Run: \`vitest run tests/models/TaskCard.test.ts\`
Expected: FAIL — "TaskCard is not defined"

- [ ] **Step 3: 写最小实现**
- [ ] **Step 4: 运行测试确认通过**
- [ ] **Step 5: 提交**

\`\`\`bash
git add src/models/TaskCard.ts tests/models/TaskCard.test.ts
git commit -m "feat: add TaskCard model with required fields"
\`\`\`

### Task 2: POST /api/cards 路由
...
```

完整的实现计划保存到：

```
docs/superpowers/plans/2026-04-18-kanban-board.md
```

Superpowers 完成计划后，会做一轮 **计划自查** （源码要求：检查 spec 覆盖度、placeholder 扫描、类型一致性），然后给出执行方式选择：

```
AI：Plan complete and saved to docs/superpowers/plans/2026-04-18-kanban-board.md
    Two execution options:

    1. Subagent-Driven (recommended) — 我为每个任务分派一个独立子代理，
       完成后自动审查，快速迭代

    2. Inline Execution — 在当前会话中批量执行，带人工检查点

    Which approach?
```

**推荐选择 Subagent-Driven** ，这是 Superpowers 最核心的能力。

到这一步，所有设计工作完成了。接下来是纯粹的执行阶段。

### 2.3 第三阶段：并行业务实现（后端和前端并行）

这一步是 Superpowers 真正发挥威力的地方。

**后端实现 — 子代理驱动开发**

在 AI 助手中选择 Subagent-Driven 方式后，Superpowers 的 subagent-driven-development 技能会自动启动。你不需要手动分派任何子代理——Superpowers 控制器会依次完成以下流程：

```
你（在 AI 助手中输入）：
选择方案 1，Subagent-Driven。
```

Superpowers 会自动执行以下循环：

**第 1 轮 — Task 1：TaskCard 数据模型**

```
AI：我正在使用 Subagent-Driven Development 来执行此计划。

    [读取计划文件：docs/superpowers/plans/2026-04-18-kanban-board.md]
    [提取所有 8 个任务的完整文本]

    Task 1: TaskCard 数据模型

    [分派实现子代理 — 包含完整任务文本和上下文]
```

实现子代理按 TDD 循环工作：

```
# 子代理自动执行（在隔离上下文中）

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

实现完成后，Superpowers 自动分派 **规约审查子代理** （spec reviewer）：

> **审查参照物说明** ：Superpowers 的规约审查子代理检查的是 **实现计划** 中的 spec 描述，不是 OpenSpec 的 spec 文件。两者的区别：OpenSpec 的 spec 定义的是系统行为（what），Superpowers 的实现计划定义的是工程步骤（how）。审查子代理确保代码 **按计划实现** ，至于计划本身是否符合 OpenSpec 的 spec，是 brainstorming 阶段要保证的。

```
AI：[分派 spec reviewer 子代理]
    对照实现计划检查代码...

    Spec compliance review:
    ✅ TaskCard 模型包含计划中定义的所有字段
    ✅ 状态字段限定为 todo/in-progress/done
    ✅ 包含 createdAt/updatedAt 时间戳
    ✅ Spec compliant — 没有超出计划范围的额外实现
```

规约审查通过后，Superpowers 自动分派 **代码质量审查子代理** （code quality reviewer）：

```
# 获取 git 提交范围
BASE_SHA=$(git rev-parse HEAD~1)
HEAD_SHA=$(git rev-parse HEAD)

# 代码质量审查子代理检查：
# - 代码风格和命名规范
# - 是否有冗余代码
# - 测试质量（是否测试了真实行为而非 mock）
```
```
AI：[分派代码质量审查子代理]

    Strengths: 清晰的接口定义，测试覆盖了创建场景

    Issues:
      Minor: 考虑为 status 字段添加联合类型而非 string

    Assessment: Ready to proceed ✅
```

三级审查全部通过，Task 1 标记完成。接着进入 Task 2。

**第 2 轮 — Task 2：POST /api/cards 路由**

同样的流程自动循环：

```
AI：Task 2: POST /api/cards 路由

    [分派实现子代理]

    实现子代理：
    - RED: 写测试 — 发送 POST 请求创建卡片，验证返回 201
    - 验证 RED: vitest run → FAIL ✅
    - GREEN: 实现 Express 路由处理器
    - 验证 GREEN: vitest run → PASS ✅
    - 提交: git commit -m "feat: add POST /api/cards route"

    [分派规约审查子代理]
    ✅ API 行为符合 spec 定义
    ✅ 错误场景覆盖（缺少 title 返回 400）

    [分派代码质量审查子代理]
    ✅ 输入校验完整
    Assessment: Ready to proceed
```

后续任务（GET /api/cards、前端组件等）依次按同样的三级循环执行，直到所有任务完成。

**全部任务完成后，Superpowers 执行最终审查和分支收尾：**

```
# 1. 运行全量测试套件
$ npm test
# 47 tests passing, 0 failures

# 2. 最终代码审查（审查整个实现，而非单个任务）
# 分派最终审查子代理，检查跨任务的一致性

# 3. 触发 finishing-a-development-branch 技能
```

Superpowers 会给你四个选择：

```
AI：Implementation complete. What would you like to do?

    1. Merge back to main locally
    2. Push and create a Pull Request
    3. Keep the branch as-is (I'll handle it later)
    4. Discard this work
```

如果你选择创建 PR：

```
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
- [ ] 手动验证任务卡片拖拽状态流转
EOF
)"

# 清理 worktree
git worktree remove .worktrees/kanban-board
```

**前端实现 — 可与后端并行**

前端开发者可以同时开工。因为 OpenSpec 的 spec.md 已经定义了完整的 API 行为，前端不需要等后端写完再动手。

在 **另一个 AI 助手会话** 中（注意：Superpowers 的 subagent-driven-development 是单会话内串行的，前后端需要各自独立的会话），前端开发者执行：

```
你（在 AI 助手中输入）：
我要实现看板系统的前端。
API 规约在 openspec/changes/kanban-board-system/specs/board/spec.md，
请基于这份规约生成前端组件。
```

Superpowers 同样会自动触发 brainstorming 技能。它读取 OpenSpec 的 spec.md，经过澄清问题和方案选择后，生成前端工程设计：

```
docs/superpowers/specs/2026-04-18-kanban-board-frontend-design.md
```

然后在独立的工作树中走同样的 writing-plans → subagent-driven-development 流程。

基于 spec.md 中的 Given/When/Then 规约，AI 助手会在 TDD 循环中逐步生成代码：

```
// 基于规约自动生成的类型定义
interface TaskCard {
  id: string;
  title: string;
  description: string;
  status: 'todo' | 'in-progress' | 'done';
  boardId: string;
  createdAt: string;
  updatedAt: string;
}

// API Client — 根据 spec 中的 API 行为定义生成
asyncfunction getCards(boardId: string): Promise<TaskCard[]> {
const response = await fetch(\`/api/cards?boardId=${boardId}\`);
return response.json();
}
```

前后端能并行的前提是 **规约先行** 。只要 spec.md 定义清楚，双方就有共同的参照物，不需要面对面坐下来对接口。

### 2.4 第四阶段：契约驱动的迭代（全员协作）

项目不可能一次做对。假设看板系统上线两周后，产品经理提了个紧急需求： **给任务卡片加上优先级字段。**

传统做法：后端改表结构、改 API，前端改类型定义、改 UI，改完还得联调测试。三个人忙一天。

用这套工具链呢？

**架构师修改契约：**

```
# 启动新的变更提案
/opsx:propose add-task-priority
```

OpenSpec 自动生成 Delta Spec，只描述变更部分：

```
## ADDED Requirements

### Task Priority

- GIVEN a task card with no priority set
- WHEN the user sets priority to "high"
- THEN the system records the priority
      and displays the card with a red indicator

- GIVEN a sorted task list
- WHEN multiple tasks have different priorities
- THEN the system sorts them by priority:
      critical > high > medium > low
```

**校验并应用：**

```
openspec validate
openspec status --change add-task-priority --json
```

**执行实现：**

在 AI 助手中执行 OpenSpec 的 `/opsx:apply` 命令：

```
/opsx:apply add-task-priority
```

这里需要澄清一个重要的区分： `/opsx:apply` 是 **OpenSpec 自身的工作流命令** ，不是 Superpowers 的。它做的事情是：

1. 读取 `openspec/changes/add-task-priority/tasks.md`
2. 逐条完成未勾选的任务
3. 写代码、创建文件、运行测试
4. 勾选已完成的 checkbox `[x]`

如果你同时安装了 Superpowers，它在 `/opsx:apply` 执行过程中可能会自动触发 TDD 等辅助技能，但 `/opsx:apply` 本身是 OpenSpec 的独立能力。

**归档变更：**

```
openspec archive add-task-priority
```

归档后， `specs/` 目录下的主规约自动更新，优先级相关行为成为系统规约的一部分。

从需求变更到代码实现，因为 Delta Spec 已经把变更描述得很清楚，AI 可以快速定位需要修改的代码范围。

![迭代闭环流程图](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

迭代闭环流程图

你在项目中用过类似的契约驱动方案吗？比如 OpenAPI/Swagger 或者 Pact？欢迎在评论区聊聊实际体验。

## 3\. 深度思辨：AI 时代的组织重构

### 3.1 角色坍缩：我们还需要前端和后端吗？

先说判断： **严格的前后端分工，正在被 AI 工具消解。**

理由不复杂。Superpowers 的子代理驱动开发里，一个子代理可以同时处理后端 API 和前端组件——因为两者基于同一份 spec.md。AI 不关心自己是写后端还是写前端，它只关心 spec 说了什么。

这带来一个有意思的变化： **技术壁垒从会不会写代码变成了会不会写规约。**

以前，前端工程师不碰后端，是因为不熟悉数据库设计、API 框架、部署流程。但现在，只要 spec.md 把 API 行为描述清楚，AI 就能生成后端代码。同理，后端工程师不需要懂 React 状态管理，AI 能基于 spec 生成前端组件。

但这里有个重要的限定： **AI 抹平的是实现层的壁垒，不是设计层的判断力。** 知道什么时候用 WebSocket 而不是 REST、什么时候需要乐观更新、怎么设计数据模型才能扛住未来半年的需求变化——这些决策能力，AI 目前替代不了。

所以更准确的说法是： **前后端的技能分工在坍缩，但思维分工还在。** 懂用户交互思维的人和懂数据建模思维的人，依然有价值，只是他们不再需要用不同的编程语言来实现各自的想法。

### 3.2 协作进化：3 人组会变成 2 人组吗？

我比较确信的趋势是： **传统的前端 + 后端 + 架构师三人组，会逐渐演变为架构师 + AI 工具操作者的两人结构。**

理由有三点：

**规约成为核心资产。** OpenSpec 的设计哲学——Fluid not rigid（灵活而非死板）——指向一个趋势：规约文件本身就是团队的核心知识资产。谁控制规约，谁就控制了产品方向。架构师的角色从 **画架构图给别人看** 变成 **写规约让 AI 执行** 。

**AI 工具的操作门槛在快速降低。** Superpowers 把写代码这件事标准化成了 7 个工作流。一个理解业务逻辑的人，即使编码能力一般，也能通过 AI 助手完成高质量的全栈实现。

**并行开发的效率提升是实在的。** 前后端基于同一份规约同时开工，AI 自动保证一致性，沟通成本大幅下降。

但也有不确定的地方。 **这个判断的风险点** ：如果项目的业务逻辑足够复杂，AI 生成的代码可能需要大量人工审查和修正。这时候一个人操作 AI 反而成为瓶颈——审查速度跟不上生成速度。

坦白讲，这套工具链对 **需求明确、技术方案清晰** 的项目效果很好。但对 **需求模糊、需要频繁试错** 的早期项目，人的判断力和沟通能力仍然不可替代。

如果你正在组建团队或调整分工，我的建议是： **先别急着裁人。先试试让现有的架构师用 OpenSpec 管理需求，让一个开发者用 Superpowers 做全栈实现。** 跑一轮完整流程后，你自然知道团队需要几个人。

说到底，工具改变的是做事的方式，不是做事的人。能定义清楚问题的人，永远比只会执行方案的人稀缺。OpenSpec + Superpowers 这套工具链，只是让这个事实暴露得更明显了。

**好啦，谢谢你观看我的文章，如果喜欢可以点赞转发给需要的朋友，我们下一期再见！敬请期待！**

**扫码关注，获取更多 AI 工具的实战经验和最佳实践。不错过每一篇干货！**

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**微信扫一扫赞赏作者**

AI编程最佳实战「2026」 · 目录

继续滑动看下一个

术哥无界

向上滑动看下一个