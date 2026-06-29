# OpenSpec + Superpowers 组合开发流程 — NIO 定制版

> **设计目标**：将 OpenSpec 作为 Workflow DSL（流程定义语言），Superpowers 作为 Skill Library（技能库），构建一套可编排、可门禁、可追溯的 AI 原生开发流水线。

---

## 一、整体架构

```
┌─────────────────────────────────────────────────────────┐
│                    OpenSpec (Workflow DSL)               │
│  定义流程、门禁、产物约束、阶段流转                       │
│  schema.yaml → 命令路由 → Dispatcher → 阶段编排          │
└────────────┬────────────────────────────────────────────┘
             │ 调用
             ▼
┌───────────────────────────────────────────────��─────────┐
│                  Superpowers (Skill Library)              │
│  7 个核心工作流，按需注入                                   │
│  brainstorming | using-git-worktrees | writing-plans     │
│  subagent-driven-development | TDD | code-review | finish│
└─────────────────────────────────────────────────────────┘
```

### 1.1 核心分工

| 层 | 职责 | 谁维护 |
|----|------|--------|
| **OpenSpec (DSL)** | 定义"做什么、按什么顺序、谁审批" | 架构师 / 团队 Lead |
| **Superpowers (Skills)** | 定义"怎么做"——标准化工程实践 | 社区 + 团队积累 |
| **Dispatcher** | 运行时编排：路由命令、校验门禁、调用 Skills | AI Agent |
| **开发者** | 决策、评审、写代码 | 人 |

### 1.2 设计原则

1. **DSL 驱动流程**：所有阶段流转、门禁规则、产物约束由 schema.yaml 定义，Agent 按配置执行
2. **技能按需注入**：Superpowers 的 7 个工作流不是全部自动触发，而是由 Dispatcher 根据当前阶段按需调用
3. **人工门禁保护关键节点**：propose 和 verify 阶段设置人工评审，确保质量和一致性
4. **SHA256 锁定**：产物防篡改，确保下游阶段使用的是经过确认的版本

---

## 二、流程总览

```
/opsx:explore  ← 可选，自由探索，无产物要求，无人工门禁
      │
      ▼
/opsx:propose  Spec + Design（规约 + 方案一体化，有人工门禁）
      │
      ▼
/opsx:apply    Build（编码实现，SHA256 校验前置产物）
      │
      ▼
/opsx:verify   Verify（评审 + 测试，有人工门禁）
      │
      ▼
/opsx:archive  PR（提 PR + 资料整理）
```

### 各阶段速览

| 命令 | 阶段 | 产物 | 门禁 | 调用的 Superpowers Skills |
|------|------|------|------|--------------------------|
| `/opsx:explore` | 探索 | 无 | 无 | 无（使用 OpenSpec 原生能力） |
| `/opsx:propose` | 提案 | proposal.md, spec.md, design.md, tasks.md | 人工评审 | brainstorming |
| `/opsx:apply` | 实现 | plan.md, 代码 | SHA256 校验 | using-git-worktrees, writing-plans, subagent-driven-development, TDD |
| `/opsx:verify` | 验证 | 审查报告, 测试报告 | 人工评审 | requesting-code-review |
| `/opsx:archive` | 归档 | PR, 归档摘要 | 无 | finishing-a-development-branch |

---

## 三、阶段详解

### 3.1 `/opsx:explore` — 自由探索

**触发方式**：`/opsx:explore <topic>`

**目的**：自由探索一个想法、技术方向、或问题空间，不做任何产物要求���

**关键规则**：
- 使用 OpenSpec 原生能力（无需 Superpowers brainstorming）
- 不生成任何正式产物
- 无人工门禁
- 探索结果可自由丢弃，也可作为 `/opsx:propose` 的输入素材

**典型场景**：
```
/opsx:explore 看板系统的状态流转方案
/opsx:explore 当前代码库中支付模块的架构
/opsx:explore 对比三种缓存方案的优劣
```

**输出**：仅限对话中的讨论记录，无文件产物。

---

### 3.2 `/opsx:propose` — 提案（有人工门禁）

**触发方式**：`/opsx:propose <change-name>`

**目的**：生成完整的规约 + 方案，包含业务描述、行为规约、技术设计、任务清单。

**流程**：

```
1. Dispatcher 读取 schema.yaml 确认 propose 阶段规则
2. 调用 Superpowers brainstorming 辅助生成（苏格拉底式对话）
   ├── 探索项目上下文
   ├── 提出澄清问题（一次一个）
   ├── 提出 2-3 个方案（带权衡分析）
   └── 分段展示设计
3. 生成 4 份产物：
   ├── proposal.md   — WHEN/THEN 可测试行为模板
   ├── spec.md       — GIVEN/WHEN/THEN 场景模板
   ├── design.md     — 技术设计 + 测试策略模板
   └── tasks.md      — 原子 TDD 任务 checkbox 模板
4. 自动计算 SHA256，写入 .opsx/lock/propose.sha256
5. 提交人工评审
6. 评审通过 → 进入下一阶段
7. 评审不通过 → 填写结构化修改意见，Agent 迭代重生成
```

**人工评审表单**：

```json
{
  "reviewer": "姓名",
  "issue_type": "业务理解偏差 / 术语不一致 / 违背历史决策 / 技术不可行 / 边界缺失 / AI 幻觉",
  "suggestion": "具体修改建议",
  "adopted": true/false
}
```

---

### 3.3 `/opsx:apply` — 编码实现（SHA256 防护）

**触发方式**：`/opsx:apply <change-name>`

**目的**：基于 propose 阶段的产物，完成编码实现。

**流程**：

```
1. Dispatcher 读取 .opsx/lock/propose.sha256
2. 重新计算 proposal.md + spec.md + design.md + tasks.md 的 SHA256
3. 比对哈希：
   ├── 一致 → 继续
   └── 不一致 → 中止，输出差异文件列表，强制重新走人工确认
4. 调用 Superpowers 4 个工作流：
   ├── using-git-worktrees     → 创建隔离 Git 工作空间
   ├── writing-plans           → 生成 plan.md（独立的工程实现计划）
   ├── subagent-driven-development → 逐任务执行
   └── test-driven-development → 强制 RED-GREEN-REFACTOR 循环
5. 生成 plan.md
6. 自动���算 SHA256，写入 .opsx/lock/apply.sha256
```

**关键约束**：

- **writing-plans 生成的是独立的实现计划**，它基于 brainstorming 的设计文档，而不是直接读取 OpenSpec 的 tasks.md
- OpenSpec 的 tasks.md 和 Superpowers 的实现计划是两份独立的文档——前者是业务任务清单（what），后者是工程实现步骤（how）
- plan.md 中的任务必须拆分为 2-5 分钟可完成的小任务
- 必须遵循 RED-GREEN-REFACTOR 循环

---

### 3.4 `/opsx:verify` — 验证（有人工门禁）

**触发方式**：`/opsx:verify <change-name>`

**目的**：代码审查 + 测试验证，确保交付质量。

**流程**：

```
1. Dispatcher 读取 .opsx/lock/apply.sha256 校验 plan.md 完整性
2. 调用 Superpowers requesting-code-review
   ├── 规约审查（对照 spec.md）
   ├── 代码质量审查
   └── 生成审查报告
3. 运行全量测试套件
4. 提交人工评审
5. 评审通过 → 进入下一阶段
6. 评审不通过 → 填写结构化修改意见，Agent 迭代重生成
7. 自动计算 SHA256，写入 .opsx/lock/verify.sha256
```

---

### 3.5 `/opsx:archive` — 归档

**触发方式**：`/opsx:archive <change-name>`

**目的**：提 PR + 资料整理，完成交付闭环。

**流程**：

```
1. 调用 Superpowers finishing-a-development-branch
   ├── 运行全量测试套件
   ├── 最终代码审查（跨任务一致性）
   └── 提供 4 个选项：
       1. Merge back to main locally
       2. Push and create a Pull Request
       3. Keep the branch as-is
       4. Discard this work
2. 生成 PR 描述 + 归档摘要
3. 清理 Git worktree
```

---

## 四、Superpowers 7 个核心工作流

| 工作流 | 做什么 | 在哪个阶段使用 |
|--------|--------|---------------|
| **brainstorming** | 苏格拉底式对话，写代码之前先理清需求。探索项目上下文 → 澄清问题 → 提出方案 → 分段展示 → 写设计文档 | `/opsx:propose` |
| **using-git-worktrees** | 创建隔离的 Git 工作空间，避免污染主分支 | `/opsx:apply` |
| **writing-plans** | 把工作拆成 2-5 分钟可完成的小任务。**注意**：生成的是独立的实现计划，基于 brainstorming 的设计文档，不是 OpenSpec 的 tasks.md | `/opsx:apply` |
| **subagent-driven-development** | 用子代理逐任务执行。Dispatcher 为每个任务分派独立子代理，完成后自动触发审查 | `/opsx:apply` |
| **test-driven-development** | 强制 RED-GREEN-REFACTOR 循环。写失败测试 → 写最小实现 → 清理 | `/opsx:apply` |
| **requesting-code-review** | 自动触发代码审查。规约审查 + 代码质量审查 + 生成审查报告 | `/opsx:verify` |
| **finishing-a-development-branch** | 完成分支，验证测试，提供合并/PR/保留/丢弃选项 | `/opsx:archive` |

### 4.1 技能调用时序

```
/opsx:propose
  └── brainstorming（辅助生成提案）

/opsx:apply
  ├── using-git-worktrees（第一步：创建隔离环境）
  ├── writing-plans（第二步：生成实现计划）
  └── subagent-driven-development（第三步：逐任务执行）
        └── test-driven-development（每个任务的 TDD 循环）

/opsx:verify
  └── requesting-code-review（审查）

/opsx:archive
  └── finishing-a-development-branch（收尾）
```

---

## 五、最轻量防护：SHA256 锁定

### 5.1 原理

在每个有人工门禁的阶段完成后，自动计算所有产物的 SHA256 哈希，写入 `.opsx/lock/` 目录。

```
.opsx/lock/
├── propose.sha256    # proposal.md + spec.md + design.md + tasks.md
├── apply.sha256      # plan.md + 代码清单
└── verify.sha256     # 审查报告 + 测试报告
```

### 5.2 防护效果

下一个命令（如 `/opsx:apply`）启动时，Dispatcher 重新计算哈希与记录比对：

- **一致** → 继续执行
- **不一致** → 中止并报警，强制重新走人工确认门

### 5.3 实现方式

```bash
# 锁定：计算产物哈希
sha256sum openspec/changes/<change-name>/*.md > .opsx/lock/propose.sha256

# 校验：重新计算并比对
sha256sum -c .opsx/lock/propose.sha256
```

### 5.4 覆盖范围

| 阶段 | 锁定内容 | 被谁校验 |
|------|----------|----------|
| propose | proposal.md, spec.md, design.md, tasks.md | `/opsx:apply` |
| apply | plan.md + 代码清单 | `/opsx:verify` |
| verify | 审查报告 + 测试报告 | `/opsx:archive` |

---

## 六、目录结构

```
{project_root}/
├── openspec/
│   ├── schemas/
│   │   └── spec-driven-nio/          # schema 包名，可自定义
│   │       ├── schema.yaml           # 工作流定义（核心）
│   │       └── templates/
│   │           ├── proposal.md       # WHEN/THEN 可测试行为模板
│   │           ├── spec.md           # GIVEN/WHEN/THEN 场景模板
│   │           ├── design.md         # 技术设计 + 测试策略模板
│   │           ├── tasks.md          # 原子 TDD 任务 checkbox 模板
│   │           └── plan.md           # 执行计划 + 证据要求模板
│   ├── specs/                        # 当前系统的行为描述（真实来源）
│   │   └── <domain>/
│   │       └── spec.md
│   ├── changes/                      # 拟议的修改（每个变更一个文件夹）
│   │   └── <change-name>/
│   │       ├── proposal.md           # 意图和范围
│   │       ├── spec.md               # 行为规约
│   │       ├── design.md             # 技术方案 + 测试策略
│   │       ├── tasks.md              # 业务任务清单
│   │       ├── plan.md               # 工程实现计划（由 writing-plans 生成）
│   │       └── specs/                # Delta 规约
│   │           └── <domain>/
│   │               └── spec.md
│   └── config.yaml                   # 项目配置（技术栈、规则）
├── .opsx/
│   ├── lock/                         # SHA256 锁定文件
│   │   ├── propose.sha256
│   │   ├── apply.sha256
│   │   └── verify.sha256
│   └── state/                        # 当前阶段状态
│       └── current.json
└── docs/
    └── superpowers/                  # Superpowers 产物
        ├── specs/                    # brainstorming 设计文档
        ├── plans/                    # writing-plans 实现计划
        └── reviews/                  # code-review 审查报告
```

---

## 七、配置示例

`openspec/config.yaml`：

```yaml
schema: spec-driven-nio
version: 1.0.0

context: |
  Tech stack: TypeScript, React, Node.js, PostgreSQL
  Architecture: REST API + SPA frontend
  Coding standards: ESLint + Prettier, TDD required

rules:
  proposal:
    - Include rollback plan
    - Include test strategy
  specs:
    - Use Given/When/Then format
  design:
    - Must include architecture diagram (mermaid)
    - Must include data model changes

gates:
  sha256:
    enabled: true
    lock_dir: .opsx/lock
  manual_review:
    required_for:
      - propose
      - verify
    review_form:
      - reviewer
      - issue_type
      - suggestion
      - adopted
```

---

## 八、完整流程示例

### 场景：实现看板系统的任务卡片拖拽功能

```bash
# Step 1: 探索（可选）
/opsx:explore 看板系统的拖拽交互方案

# Step 2: 提案
/opsx:propose kanban-drag-drop
# → 生成 proposal.md, spec.md, design.md, tasks.md
# → 自动 SHA256 锁定
# → 等待人工评审...

# Step 3: 实现（SHA256 校验通过后）
/opsx:apply kanban-drag-drop
# → 校验 propose 产物哈希
# → 创建 Git worktree
# → 生成 plan.md（writing-plans）
# → 逐任务 TDD 实现（subagent-driven-development）
# → 自动 SHA256 锁定

# Step 4: 验证
/opsx:verify kanban-drag-drop
# → 校验 apply 产物哈希
# → 自动代码审查（requesting-code-review）
# → 运行全量测试
# → 等待人工评审...

# Step 5: 归档
/opsx:archive kanban-drag-drop
# → 校验 verify 产物哈希
# → 提 PR + 归档摘要
# → 清理 worktree
```

---

## 九、核心优势

1. **DSL 驱动流程**：所有阶段流转由 schema.yaml 定义，无需硬编码
2. **技能按需注入**：Superpowers 的 7 个工作流按阶段调用，不浪费资源
3. **双重门禁**：SHA256 自动防护 + 人工评审，兼顾效率与质量
4. **产物标准化**：5 个模板覆盖提案到实现的全流程，格式统一
5. **可追溯**：每个阶段的产物、哈希、评审记录完整留存
6. **灵活入口**：`/opsx:explore` 提供低摩擦的探索通道，无需经过正式流程
7. **独立分工**：OpenSpec 的 tasks.md（业务任务）与 Superpowers 的 plan.md（工程计划）职责分离，互不耦合
