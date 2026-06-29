---
title: "Mymat 完整设计方案"
type: synthesis
tags: [Mymat, AI编程工作流, 状态机, OpenSpec, Superpowers, 设计方案]
created: 2026-06-06
updated: 2026-06-06
sources: []
related:
  - wiki/entities/OpenSpec
  - wiki/entities/Superpowers
  - wiki/entities/Comet
  - wiki/concepts/AtomicTDDWorkflow
---

## 一、什么是Mymat

Mymat（My Mate / Make AI Manageable And Trustworthy）是一个“让 AI 编程变得可管理、可恢复、可信任”的工作流系统。

如果你用过 Claude Code、Cursor 这类 AI 编程工具，会发现一个问题：AI 很聪明，但它不像真正的项目管理系统。今天写到一半，明天新开一个对话，它可能忘了昨天做到哪；它说“我已经测试过了”，但你不知道它是不是真的跑了测试；需求文档、实现计划、代码审查、接口验证、E2E 验收、发布这些环节，经常要靠人手动提醒它下一步做什么。

Mymat 要解决的就是这个问题。

它把一个需求从规约到 PR 创建，拆成 5 个阶段：

```text
Spec → Design → Build → Verify → Release
需求规约 → 方案设计 → 编码实现 → 验证 → 发布
```

你可以把它理解成一条“AI 需求交付流水线”。

每个阶段都有明确产物。需求阶段要有 OpenSpec 生成的 proposal/specs/design/tasks，设计阶段要有结构化方案和微任务计划，编码阶段每个小任务都要有测试文件、实现文件和通过的验证，验证阶段要有 review、api、e2e 三类报告，发布阶段要有 PR、版本/CHANGELOG 证据和 OpenSpec 归档结果。

Mymat 的核心思想很朴素：

> 不相信 AI 说“我做完了”，只相信磁盘上真的有什么。

所以它不是只靠提示词约束 AI，而是引入 guard 脚本来检查产物。AI 说测试写好了没用，脚本会检查测试文件是否存在；AI 说功能完成了没用，脚本会跑测试；AI 说需求没改没用，脚本会用 SHA256 检查需求文件有没有被偷偷改过；AI 说验证通过没用，脚本会检查 `/review`、`/api`、`/e2e` 的报告状态。

Mymat 还有一个很重要的东西：`state.json`。

它就像给 AI 留的一张地图。里面记录了当前 feature 做到哪个阶段、Build 做完了哪些 task、上次断点在哪里、当前状态是进行中、失败、停放还是完成。这样就算你明天新开一个对话，只要输入 `/mymat`，AI 就能读取状态，从 B-004 继续，而不是从头猜。

Mymat 也不是重新发明所有能力。它整合 OpenSpec + Superpowers，通过子任务级状态机和产物校验机制，实现从已确定需求到 PR 创建的 AI Coding 交付治理流程。

能力分工边界

| 能力层       | 职责层                         | 在 Mymat 里的角色                                          | 触发方式   | 事实源/状态存储       |
| ------------ | ------------------------------ | ---------------------------------------------------------- | ---------- | --------------------- |
| OpenSpec     | 需求层：写代码前锁住需求       | 把需求变成可冻结的规格和任务                               | Mymat 编排 | `openspec/` 目录      |
| Superpowers  | 构建方法层：写代码时卡住质量   | 负责方案设计、TDD、任务级验证                              | 自动触发   | skill 文件 + 项目代码 |
| Mymat Native | 治理层：验证、发布、状态和门禁 | 负责 `/review`、`/api`、`/e2e`、`/ship`、guard、state、HCG | Mymat 编排 | `.mymat/` 目录        |

Mymat 的价值不是替代 OpenSpec 或 Superpowers，而是把它们和自己的 native 验证/发布能力编排成一条稳定流程。用户不需要记住什么时候该调用 `/opsx:propose`，什么时候该跑 `brainstorming`，什么时候该执行 `/review`、`/api` 或 `/e2e`。你只需要进入对应的 `/mymat:spec`、`/mymat:build`、`/mymat:verify` 等阶段，Mymat 会按规则组织下一步。

它设置了 3 个必须由人确认的门：

```text
HCG-1：需求冻结确认
HCG-2：验证验收确认
HCG-3：发布确认
```

为什么要有人确认？因为这些点是“不可逆”或成本很高的决策。比如需求一旦冻结，后面就不能随便改；验证验收决定是否接受实现结果；发布会创建 PR、推动交付。Mymat 让 AI 自动做可逆的小步骤，把不可逆的大决策交还给人。

一句话总结：

> Mymat 是一个把 AI 编程从“聪明但容易失控的对话”变成“有状态、有门禁、有产物校验的需求交付流程”的系统。

可以这样做个比喻：

Claude Code 像一个很强的程序员助手，但它容易忘事，也可能自信地跳步骤。Mymat 像它旁边的项目经理 + 质检员 + 流程引擎：它告诉 AI 现在该做什么，记录做到哪里，检查它是否真的完成，并在关键节点请人拍板。

---

## 二、Mymat设计哲学

### 哲学一：可验证事实高于 AI 承诺

Mymat 的根本判断是：**AI 的自然语言承诺不构成可信事实；只有可被机器验证的产物和状态，才构成系统事实。**

这也是三层信任金字塔的来源：

```text
    ┌────────────────────────────────┐
  最高   │  产物校验（文件存在 + 测试通过） │  ← guard 脚本硬执行
    ├────────────────────────────────┤
  中间   │  状态机强制顺序（前置条件校验）  │  ← state.json 持久化
    ├────────────────────────────────┤
  最低   │  instruction 软约束             │  ← AI 自觉遵守
    └────────────────────────────────┘
```

Mymat 不把 AI 的“我已经完成了”当成完成，而是要求系统回答三个问题：

- 文件是否真的存在？
- 测试是否真的通过？
- 当前阶段是否真的满足前置条件？

所以，Mymat 的核心不是“让 AI 更听话”，而是**让 AI 的输出进入一个可验证、可恢复、可追责的事实系统**。

Mymat 不验证“产品是否值得做”，而验证“一个已确定需求是否被正确规约、实现、验证和发布”。

一句话概括：**不相信 AI 说它做了什么，只相信系统能验证什么。**

### 哲学二：覆盖优先于优化

Mymat 优先覆盖完整需求交付链路，而不是只把编码阶段优化到极致。

AI Coding 的真实瓶颈通常不在“能不能写代码”，而在：

- 需求来源是否清楚？
- 需求是否冻结？
- 任务是否可执行？
- 实现是否真的完成？
- 代码、接口和用户路径是否通过验证？
- 发布是否可控？

因此，Mymat 选择先打通整个链条⛓：

```text
Spec → Design → Build → Verify → Release
```

各阶段内部可以先不完美，但整条链必须闭合，创造一条最小可用、可验证、可恢复的 AI 需求交付流水线。

这背后的判断是：**一条链只有最薄弱的环节决定整体强度。**

### 哲学三：串联点是价值的倍增器

Mymat 不重新发明需求规约和 TDD 方法论，而是把 OpenSpec、Superpowers 与 Mymat native 验证/发布能力串成一条稳定流程。

单个能力的价值是局部的：

- OpenSpec 擅长需求规约和变更管理
- Superpowers 擅长方法论、TDD 和任务级执行习惯
- Mymat native skills 擅长验证、发布、状态治理和跨会话恢复

但真正的系统价值来自串联点：

- 已确定需求如何进入需求规约？
- 需求规约如何进入设计计划？
- 设计计划如何进入 TDD 构建？
- 构建结果如何进入 review/api/e2e 验证？
- 验证结果如何进入发布和归档？

Mymat 关注的不是“每个能力自己有多强”，而是**能力交接处是否丢信息、是否靠人脑记忆、是否可验证**。

一句话概括：**Mymat 的增值发生在交接处，而不是单点能力内部。**

### 哲学四：人机协作的分界线是“可逆性”

Mymat 不要求人类确认每一步，也不允许 AI 推进所有步骤。

它用“可逆性”划分人机边界：

- **可逆操作**：AI 自动推进
- **不可逆节点**：必须人类确认

例如：

- 单个 task 实现失败，可以 retry，所以 AI 可以自动处理
- 一个测试失败，可以修复后重跑，所以 AI 可以自动处理
- 需求冻结后会影响后续所有实现，因此必须 HCG-1 人类确认
- 验证验收决定是否接受结果，因此必须 HCG-2 人类确认
- 发布会创建 PR、推动交付，因此必须 HCG-3 人类确认

这使 Mymat 避免两个极端：

- 不是“AI 每一步都要问人”，否则流程失去自动化价值
- 也不是“AI 一路自动到发布”，否则风险不可控

一句话概括：**可逆的交给 AI，不可逆的交给人。**

### 哲学五：让工作可以被下一次会话接住

Mymat 把跨会话连续性视为 AI Coding 的核心基础设施。

AI 编程天然不是一次性完成的。一个 feature 可能会经历长对话、上下文压缩、模型切换、人工暂停、失败重试，甚至第二天重新打开一个全新的会话。问题不在于会话会不会断，而在于：**会话断了以后，工作还能不能被准确接住。**

因此，Mymat 不试图让单个 AI 会话记住一切，而是假设会话一定会丢上下文，然后把“下一次继续所需的信息”沉淀到 `state.json` 中。

`state.json` 不是为了记录历史流水账，而是为了让下一个会话中的 AI 立即知道：

- 当前 feature 是什么？
- 当前 phase 在哪里？
- 哪些 task 已经完成？
- 哪个 task 正在进行？
- 上一个可恢复断点在哪里？
- 继续执行前必须满足什么前置条件？

传统日志回答的是：“过去发生了什么？”

`state.json` 回答的是：“下一次应该从哪里接住？”

这对 AI Coding 尤其关键，因为 AI 的记忆不可靠，但磁盘上的状态可以可靠。Mymat 不把连续性寄托在模型记忆里，而是把连续性写进项目状态，让任何一个新的会话都能基于同一份事实继续推进。

一句话概括：**好的 AI 工作流，不要求会话永不断裂，而要求断裂之后仍然可以准确接上。**

---

## 三、五阶段管线（S-D-B-V-R）

```text
S → D → B → V → R
Spec  Design  Build  Verify  Release
[OpenSpec] [Superpowers] [Superpowers] [Mymat Native + OpenSpec] [Mymat Native + OpenSpec]
```

五阶段产物存放位置原则：

- **OpenSpec 产物回到 OpenSpec 事实源目录**：proposal/specs/design/tasks/verify/archive 写入 `openspec/`。
- **Mymat 自己管理运行态与验证证据**：guard 报告、handoff 文件、state、快照、review/api/e2e/ship 报告写入 `.mymat/features/{feature_id}/...`。
- **产生的代码本身留在项目结构中**：Build 阶段的实现文件和测试文件由项目结构决定。

### Phase S：Spec（需求规约）

**工具**：OpenSpec｜**目标**：将已确定需求转化为结构化、可冻结的需求规约

| 子任务    | 命令                             | 产物                                                                                                    | 产物位置                                                                        |
| --------- | -------------------------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| S-01      | OpenSpec `/opsx:explore`（可选） | 分析当前代码库、已有架构、已有Spec、已有API，然后开始讨论，输出问题分析、方案比较、风险分析、建议方案。 | 不落文件。                                                                      |
| S-02      | OpenSpec `/opsx:propose`         | proposal + specs + design + tasks 四件套                                                                | `openspec/changes/{change_id}/proposal.md`、`specs.md`、`design.md`、`tasks.md` |
| **HCG-1** | 用户确认                         | “需求范围确认，开始设计？”                                                                              | `.mymat/features/{feature_id}/snapshots/hcg-1.json`                             |

**Guard 校验**：四件套文件均存在 + tasks 列表非空 + SHA256 初始化写入 spec-graph.json + specs.md frontmatter 含 `generated_by: openspec-propose`（缺失时输出 `WARN: MISSING_TRIGGER` 警告，不阻塞流程）。

**HCG-1 PASS 后附加操作**：guard-spec.sh 同时：
① 生成 `.mymat/features/{id}/handoff/design-context.json`（记录 specs/tasks 路径及 SHA256，Build 阶段 `mymat-build.md` 强制从此读取，防止 AI 依赖被压缩的记忆，`guard-spec-integrity.sh` 在每个 Build task 前校验 SHA256 未变动）；
② 写入 `trigger-log.txt`，记录 `/opsx:propose` 真实触发时间戳。

**重要**：HCG-1 后，`openspec_specs` 与 `openspec_tasks` 进入冻结状态，SHA256 锁定。后续任何对 specs/tasks 文件的修改都会触发 guard hard stop。

---

### Phase D：Design（方案设计）

**工具**：Superpowers｜**目标**：结构化精炼需求，生成可执行的微任务计划

| 子任务 | Skill                      | 输入                                               | 产物                                                        | 产物位置                                                   |
| ------ | -------------------------- | -------------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------- |
| D-01   | Superpowers`brainstorming` | `specs.md`（边界契约）+ `design.md`（实现方向）    | 边界分析 + 方案选型 + 风险文档                              | `docs/superpowers/specs/YYYY-MM-DD-{feature_id}-design.md` |
| D-02   | Superpowers`writing-plans` | `tasks.md`（OpenSpec生成的）+ D-01 brainstorm 产物 | 2-5 分钟粒度微任务计划（N 个 task，作为非冻结设计计划留存） | `.mymat/features/{feature_id}/handoff/build-plan.json`     |

**约束**：此阶段描述实现方案，不得重定义需求——需求唯一真相源是 OpenSpec specs（单向事实链）。

**任务拆分边界**：D-02 产出非冻结的设计计划，写入 `.mymat/features/{feature_id}/handoff/build-plan.json`。拆任务过程中遇到必须做产品决策才能继续的步骤（例如某个边界行为是否需要处理、某个错误是否需要告知用户），而该决策无法从现有 输入 中推导。此时 `writing-plans` 必须停止，上报给用户，由用户决定是否回滚到 HCG-1 之前重新走 S 阶段，让 OpenSpec 补充 specs 后再进入 HCG-1。**Superpowers 发现的问题只是"信号"，修复动作必须回到 OpenSpec 那一层，不得由 D 阶段自行补充需求。**

> build-plan.json 是机器解析的结构化执行计划、且需要按 feature 隔离管理，不是供人阅读的 Markdown 设计文档，因此不属于 docs/superpowers/specs/，而归属于 Mymat 的 feature 生命周期目录 .mymat/features/{feature_id}/handoff/。

---

### Phase B：Build（编码实现）

**工具**：Superpowers｜**目标**：逐 task 执行 TDD 循环，每个 task 完成后写入断点

| 子任务 | Skill/动作                       | 产物                           | 产物位置                                                                 |
| ------ | -------------------------------- | ------------------------------ | ------------------------------------------------------------------------ |
| B-00   | Acceptance Criteria 锚定         | 当前 task 的验收条件上下文锚点 | 当前会话上下文；异常记录写入 `.mymat/features/{feature_id}/warn-log.txt` |
| B-01   | `test-driven-development`        | 单元测试文件                   | `{task.test_path}`                                                       |
| B-02   | `subagent-driven-development`    | 实现代码                       | `{task.impl_path}`                                                       |
| B-03   | `verification-before-completion` | 子任务验证结果 + 状态更新      | `.mymat/features/{feature_id}/state.json`                                |

每个具体 Build task 执行四步循环（B-00 为前置强制步骤）：

```text
B-00  AC 锚定（强制）  从 handoff/design-context.json → tasks.md 提取当前 task 的 acceptance_criteria → 粘贴到响应顶部作为上下文锚点；后续测试用例描述必须引用 AC 语言
B-01  写单元测试      Superpowers test-driven-development  自动触发
B-02  写实现代码      Superpowers subagent-driven-dev      自动触发
B-03  验证完成        Superpowers verification-before-comp  自动触发
   ↓
state.json 更新 build.last_task_id = N（断点记录）
   ↓
进入 B-(N+1)
```

**AC 锚定目的**：长对话中 specs.md 在 B-006+ 时已被压缩，B-00 确保每个 task 的验收条件始终在当前 subagent 活跃上下文顶部，不依赖 AI 的全局记忆。降级：design-context.json 不存在或 tasks.md 非 JSON 时，跳过锚点步骤并在 `warn-log.txt` 记录 `NO_AC task={id}`。

**测试级别**：单元测试（函数/类级别），用 mock 隔离外部依赖，可在实现前独立存在。这是 TDD 可操作性的基础——不能在没有运行服务的情况下写接口测试，但可以写单元测试。

**断点恢复**：新会话读取 `build.last_task_id`，跳过已完成 task，从断点 task 继续。

**Guard 校验（每个 task）**：

- 首个 task（`completed_tasks` 为空）时检查 `isolation.strategy` 已设置，否则 HARD STOP
- 测试文件存在 `src/__tests__/{Module}.test.ts`
- 测试通过 `npm test -- {Module}`
- 实现文件存在
- 测试描述 AC 关键词对齐检查（warn-only）：从 tasks.md 提取当前 task 的 `acceptance_criteria` 关键词，若测试文件的 `describe`/`it` 描述无一包含关键词，写入 `warn-log.txt`（不 exit 1；V 阶段 `/review` 做精确语义验证）

---

### Phase V：Verify（验证）

**工具**：Mymat Native + OpenSpec｜**目标**：用 review/api/e2e 三类能力验证实现是否可接受

| 子任务    | 命令                     | 产物                                                 | 产物位置                                                  |
| --------- | ------------------------ | ---------------------------------------------------- | --------------------------------------------------------- |
| V-00      | OpenSpec `/opsx:verify`  | 规约对齐验证报告（实现是否符合 specs 定义）          | `openspec/changes/{change_id}/verify.md`                  |
| V-01      | Mymat `/review`          | 代码审查 + 安全风险 + 架构偏移 + spec drift 检查报告 | `.mymat/features/{feature_id}/artifacts/verify/review.md` |
| V-02      | Mymat `/api`（条件必选） | API/接口/集成契约验证报告                            | `.mymat/features/{feature_id}/artifacts/verify/api.md`    |
| V-03      | Mymat `/e2e`（条件必选） | 真实用户路径 E2E 验收报告                            | `.mymat/features/{feature_id}/artifacts/verify/e2e.md`    |
| **HCG-2** | 用户确认                 | “验证通过，准备发布？”                               | `.mymat/features/{feature_id}/snapshots/hcg-2.json`       |

**能力边界**：

- `/review`：必选。检查代码质量、安全风险、架构偏移、测试覆盖、spec drift，是验证阶段总闸门。
- `/api`：条件必选。涉及后端接口、服务契约、集成边界、权限或错误码时必须执行；纯文案/样式/本地函数可跳过。
- `/e2e`：条件必选。涉及 UI、关键用户路径、浏览器行为或端到端业务闭环时必须执行；纯后端库代码可跳过。
- `/opsx:verify`：作为 V-00 前置规约对齐检查，不直接暴露为用户主命令。

**Guard 校验**：`/review` 报告状态为 PASS + required `/api`/`/e2e` 报告状态为 PASS + OpenSpec verify 无 blocking mismatch。

---

### Phase R：Release（发布）

**工具**：Mymat Native + OpenSpec｜**目标**：创建 PR，归档规约，完成 feature 生命周期

| 子任务           | 工具/命令                | 产物                                        | 产物位置                                                 |
| ---------------- | ------------------------ | ------------------------------------------- | -------------------------------------------------------- |
| R-01 / **HCG-3** | 用户确认                 | “发布是不可逆操作，确认执行？”              | `.mymat/features/{feature_id}/snapshots/hcg-3.json`      |
| R-02             | Mymat `/ship`            | 版本升级 + CHANGELOG + PR 创建推送          | `.mymat/features/{feature_id}/artifacts/release/ship.md` |
| R-03             | OpenSpec `/opsx:archive` | delta spec 合入主规范，feature 生命周期结束 | `openspec/specs/`                                        |

**设计边界（Mymat 止于 PR 创建）**：

| 环节                                | 归属            |
| ----------------------------------- | --------------- |
| 版本升级 + CHANGELOG + PR 创建推送  | Mymat（本阶段） |
| PR 人工 Code Review                 | 团队协作        |
| Merge 审批                          | 团队协作        |
| 多 PR 并发合并后的回归测试套件      | CI/CD 流水线    |
| 跨系统集成测试（Test/Staging 环境） | CI/CD 流水线    |
| Staging → Production 部署           | CI/CD 流水线    |
| 灰度发布与线上监控                  | 运维/可观测平台 |

**边界原因**：Claude Code 会话生命周期自然终止于 PR 推送——代码进入团队代码库后，merge 决策涉及多人协同和 CI 结果，不是单次 AI 会话的决策范围。多 PR 并发合并后的回归测试属于 CI/CD 天然职责，不应下沉到单个 feature 的 Claude Code 会话里。`/opsx:archive` 是规约归档收尾，不是发布动作。

---

## 四、三层测试体系

| 测试层级     | 阶段   | 工具            | 测试类型                          | 能否 mock    |
| ------------ | ------ | --------------- | --------------------------------- | ------------ |
| 单元测试     | Build  | Superpowers TDD | 函数/类级别                       | 是，必须     |
| API/集成测试 | Verify | Mymat `/api`    | 接口契约 + 集成边界 + 权限/错误码 | 部分         |
| E2E 测试     | Verify | Mymat `/e2e`    | 真实浏览器用户路径                | 否，必须真实 |

`/review` 不属于测试层级本身，而是 Verify 阶段的质量总闸门：它检查代码质量、安全风险、架构偏移、测试充分性和 spec drift。

---

## 五、全部子任务清单

| 任务 ID | 阶段    | 任务名称                              | 工具             | Skill/命令                       | 触发方式 ①      | HCG |
| ------- | ------- | ------------------------------------- | ---------------- | -------------------------------- | --------------- | --- |
| S-01    | Spec    | 探索现有代码库（可选）                | OpenSpec         | `/opsx:explore`                  | Mymat 编排      | —   |
| S-02    | Spec    | 生成需求四件套                        | OpenSpec         | `/opsx:propose`                  | Mymat 编排      | —   |
| S-03    | Spec    | 需求范围确认门禁                      | —                | HCG-1                            | **用户确认**    | ✅  |
| D-01    | Design  | 结构化需求精炼 + 边界分析             | Superpowers      | `brainstorming`                  | 自动（SP 钩子） | —   |
| D-02    | Design  | 生成微任务计划                        | Superpowers      | `writing-plans`                  | 自动（SP 钩子） | —   |
| B-00    | Build   | AC 锚定（每 task 前置）               | Mymat + OpenSpec | 读取 handoff/specs/tasks         | Mymat 编排      | —   |
| B-01    | Build   | 写单元测试（每 task 循环）            | Superpowers      | `test-driven-development`        | 自动（SP 钩子） | —   |
| B-02    | Build   | 写实现代码（每 task 循环）            | Superpowers      | `subagent-driven-development`    | 自动（SP 钩子） | —   |
| B-03    | Build   | 子任务完成验证（每 task 循环）        | Superpowers      | `verification-before-completion` | 自动（SP 钩子） | —   |
| V-00    | Verify  | 规约对齐验证                          | OpenSpec         | `/opsx:verify`                   | Mymat 编排      | —   |
| V-01    | Verify  | 代码审查 + 安全风险 + spec drift 检查 | Mymat Native     | `/review`                        | Mymat 编排      | —   |
| V-02    | Verify  | API/接口/集成契约验证（条件必选）     | Mymat Native     | `/api`                           | Mymat 编排      | —   |
| V-03    | Verify  | 真实用户路径 E2E 验收（条件必选）     | Mymat Native     | `/e2e`                           | Mymat 编排      | —   |
| V-04    | Verify  | 验证验收确认门禁                      | —                | HCG-2                            | **用户确认**    | ✅  |
| R-01    | Release | 发布确认门禁                          | —                | HCG-3                            | **用户确认**    | ✅  |
| R-02    | Release | 完整发布管线                          | Mymat Native     | `/ship`                          | Mymat 编排      | —   |
| R-03    | Release | delta 规范归档                        | OpenSpec         | `/opsx:archive`                  | Mymat 编排      | —   |

> **① 触发方式说明**（回答“哪些任务需要人工介入”）
>
> - **自动（SP 钩子）**：Superpowers 技能系统在 AI 执行任务时自动识别触发，无需任何命令
> - **Mymat 编排**：由 Mymat phase skill 按序调用底层工具或 native skill；用户只需执行对应的 `/mymat:` 阶段命令，**无需手动输入子工具命令**
> - **用户确认**：3 个 HCG 人工门禁，这是**唯一需要人工介入**的环节

---

## 六、子任务状态机

### 状态枚举

```text
not_started → in_progress → done
                         ↘ failed → retry（≤3次）→ abort
                         ↘ parked → in_progress（用户 /mymat:resume）
                         ↘ skipped（仅 optional/conditional 任务）
```

### 状态转移规则

| 当前          | 目标          | 触发条件                                        | 执行者                            |
| ------------- | ------------- | ----------------------------------------------- | --------------------------------- |
| `not_started` | `in_progress` | 前序任务 done + pre_conditions 全通过           | guard 脚本自动                    |
| `in_progress` | `done`        | post_conditions 全通过                          | guard 脚本自动                    |
| `in_progress` | `failed`      | post_conditions 失败（超过 retry_max）          | guard 脚本自动                    |
| `in_progress` | `parked`      | `/mymat:park`                                   | 用户主动                          |
| `parked`      | `in_progress` | `/mymat:resume`                                 | 用户主动                          |
| `failed`      | `in_progress` | `/mymat:retry`（retry_count < 3）               | 用户主动                          |
| `not_started` | `skipped`     | optional 或 conditional 任务经 guard 判定不适用 | guard 脚本自动 + 记录 skip_reason |
| `done`        | —             | **不可转移**                                    | —                                 |

### 阶段状态聚合规则

```text
所有必须子任务 done                         → 阶段: done
任意子任务 in_progress                      → 阶段: in_progress
任意必须任务 failed（blocking）             → 阶段: blocked
所有 optional/conditional 任务 skipped + 必须任务 done → 阶段: done
任意子任务 parked                           → 阶段: parked
```

### Build 阶段断点恢复

```json
{
  "build": {
    "status": "in_progress",
    "total_tasks": 8,
    "completed_tasks": ["B-001", "B-002", "B-003"],
    "last_task_id": "B-003",
    "last_task_title": "重构 TokenService.refresh()"
  }
}
```

新会话恢复时：B-001、B-002、B-003 均已在 `completed_tasks` 中（跳过），从 B-004 开始继续。

---

## 七、状态管理设计

### 目录结构

```text
.mymat/
├── features/
│   └── feat-20260606-login-refactor/
│       ├── state.json          ← 主状态文件（子任务级）
│       ├── spec-graph.json     ← Spec 产物 SHA256 完整性追踪
│       ├── trigger-log.txt     ← Skill 触发日志（guard-spec.sh PASS 后写入）
│       ├── warn-log.txt        ← AC 关键词对齐警告日志（guard-build.sh 写入）
│       ├── handoff/
│       │   ├── design-context.json  ← Spec→Build 交接包（guard-spec.sh 生成）
│       │   └── build-plan.json      ← Design→Build 微任务计划（D-02 生成）
│       ├── artifacts/
│       │   ├── verify/
│       │   │   ├── review.md
│       │   │   ├── api.md
│       │   │   └── e2e.md
│       │   └── release/
│       │       └── ship.md
│       └── snapshots/          ← 每次 HCG 前的完整快照（3 个门禁对应 3 份）
│           ├── hcg-1.json      ← 需求冻结前（pre HCG-1）
│           ├── hcg-2.json      ← 验证验收前（pre HCG-2）
│           └── hcg-3.json      ← 发布确认前（pre HCG-3）
└── config.json                 ← 项目级配置（工具路径、平台类型、验证适用性规则）
```

### state.json 完整结构

```json
{
  "version": "1.0",
  "feature_id": "feat-20260606-login-refactor",
  "feature_title": "重构登录流程",
  "workflow": "full",
  "current_phase": "build",
  "current_phase_status": "in_progress",
  "created_at": "2026-06-06T10:00:00Z",
  "updated_at": "2026-06-06T14:30:00Z",
  "isolation": {
    "strategy": "branch",
    "branch_name": "feat/feat-20260606-login-refactor",
    "created_at": "2026-06-06T11:30:00Z"
  },
  "phases": {
    "spec": {
      "status": "done",
      "outputs": {
        "proposal": "openspec/changes/xxx/proposal.md",
        "specs": "openspec/changes/xxx/specs.md",
        "design": "openspec/changes/xxx/design.md",
        "tasks": "openspec/changes/xxx/tasks.md"
      },
      "metrics": {
        "started_at": "2026-06-06T10:30:00Z",
        "completed_at": "2026-06-06T11:05:00Z",
        "elapsed_seconds": 2100,
        "output_chars": 11500,
        "input_chars": 28000,
        "api_usage": null
      }
    },
    "design": {
      "status": "done",
      "outputs": {
        "brainstorm": "docs/superpowers/specs/YYYY-MM-DD-xxx-design.md",
        "build_plan": ".mymat/features/xxx/handoff/build-plan.json"
      },
      "metrics": {
        "started_at": "2026-06-06T11:10:00Z",
        "completed_at": "2026-06-06T11:25:00Z",
        "elapsed_seconds": 900,
        "output_chars": 6800,
        "input_chars": 15000,
        "api_usage": null
      }
    },
    "build": {
      "status": "in_progress",
      "total_tasks": 8,
      "completed_tasks": ["B-001", "B-002", "B-003"],
      "last_task_id": "B-003",
      "last_task_title": "重构 TokenService.refresh()",
      "failed_task_id": null,
      "metrics": {
        "started_at": "2026-06-06T11:30:00Z",
        "completed_at": null,
        "elapsed_seconds": null,
        "output_chars": 24600,
        "input_chars": null,
        "api_usage": null
      }
    },
    "verify": {
      "status": "not_started",
      "applicability": {
        "api": "required | skipped",
        "e2e": "required | skipped",
        "skip_reasons": {
          "api": null,
          "e2e": null
        }
      },
      "outputs": {
        "spec_alignment_report": null,
        "review_report": null,
        "api_report": null,
        "e2e_report": null
      },
      "metrics": null
    },
    "release": {
      "status": "not_started",
      "outputs": {
        "ship_report": null,
        "pr_url": null,
        "version": null,
        "changelog_entry": null,
        "archive_path": null
      },
      "metrics": null
    }
  }
}
```

### spec-graph.json（Spec 完整性追踪）

```json
{
  "nodes": {
    "openspec_specs": {
      "path": "openspec/changes/xxx/specs.md",
      "sha256": "b7e2d...",
      "role": "requirements_truth",
      "frozen_after_phase": "spec",
      "immutable": true
    },
    "openspec_tasks": {
      "path": "openspec/changes/xxx/tasks.md",
      "sha256": "c1a9f...",
      "role": "task_list",
      "frozen_after_phase": "spec",
      "immutable": true
    },
    "openspec_proposal": {
      "path": "openspec/changes/xxx/proposal.md",
      "sha256": "d4b3e...",
      "role": "delivery_rationale",
      "frozen_after_phase": "spec",
      "immutable": false
    },
    "openspec_design": {
      "path": "openspec/changes/xxx/design.md",
      "sha256": "e5c4f...",
      "role": "implementation_approach",
      "frozen_after_phase": "spec",
      "immutable": false
    }
  },
  "integrity_violations": []
}
```

每次阶段推进前，guard 脚本校验 SHA256。冻结文件被修改则 hard stop + 报告违规。

### snapshots/ 快照设计

快照在每次**展示 HCG 前**由 `mymat-state.sh` 自动创建，内容为当时的完整状态副本：

| 字段           | 说明                                                 |
| -------------- | ---------------------------------------------------- |
| `snapshot_id`  | `hcg-{N}`，对应第几个门禁                            |
| `captured_at`  | 快照创建时间戳                                       |
| `hcg_question` | 展示给用户的确认问题                                 |
| `state`        | 完整 state.json 副本（含所有阶段 outputs + metrics） |
| `spec_graph`   | 完整 spec-graph.json 副本（含所有 SHA256 值）        |

**快照用途**：

- 用户**拒绝** HCG → 可运行 `/mymat:rollback hcg-1` 回滚到上一门禁状态，重新执行相应阶段，无需从头重来
- 问题诊断：对比不同快照的 spec-graph 可发现哪个阶段引入了 spec 漂移
- 审计留档：每次不可逆决策前的完整状态可溯源

**触发规则**：仅在 3 次 HCG 前各生成一份（hcg-1 至 hcg-3），不在普通任务完成时生成，控制存储开销。

> **关于 HCG 编号**：全流程共 3 个人工门禁——HCG-1（需求冻结）、HCG-2（验证验收）、HCG-3（发布确认）。Guard 脚本中的“→ HCG-2 放行”含义是：guard 验证产物后解除对 HCG-2 展示的阻塞，两者指同一个门禁，非重复。

### 分支隔离策略（isolation.strategy）

每个 feature Build 开始前写入 state.json `isolation` 字段，guard-build.sh 首任务时强制检查：

| 策略       | 适用场景                        | git 操作                                         |
| ---------- | ------------------------------- | ------------------------------------------------ |
| `branch`   | 单 feature 标准开发（推荐）     | `git checkout -b feat/{feature_id}`              |
| `worktree` | 多 feature 并发，目录独立       | `git worktree add ../{id} -b feat/{id}`          |
| `none`     | 纯文档/配置改动，**零代码变更** | 无操作（guard 校验 staged 文件无代码文件扩展名） |

### mymat-state.sh write 字段校验

`write` 命令写入前对关键字段做合法性校验，失败时输出 `SCHEMA_ERROR: invalid value '{v}' for field '{path}'` 并 exit 1：

| 字段                   | 允许值                                                                   |
| ---------------------- | ------------------------------------------------------------------------ |
| `current_phase`        | `spec / design / build / verify / release`                               |
| `current_phase_status` | `not_started / in_progress / done / parked / blocked / aborted / failed` |
| `workflow`             | `full / quick / micro / prototype`                                       |
| `isolation.strategy`   | `branch / worktree / none`                                               |

---

## 八、Guard 脚本体系

```text
mymat-guard-spec.sh           S-02 产物验证 → HCG-1 放行
mymat-guard-spec-integrity.sh 全程运行，每次阶段推进前 SHA256 校验
mymat-guard-build.sh          首任务 isolation.strategy 检查；每个 B-03 产物验证 + 测试描述 AC 关键词对齐 warn-only 检查（写 warn-log.txt）→ 下一 task 放行
mymat-guard-verify.sh         V-00/V-01/V-02/V-03 产物验证 + 条件必选判断 → HCG-2 放行
mymat-guard-release.sh        R-02/R-03 完成验证 → 流程结束
mymat-state.sh                统一读写 state.json
mymat-workflow-detect.sh      diff 分析 → 推荐工作流类型
```

**核心原则**：

```text
AI 生成内容 → 脚本验证产物 → 脚本更新状态 → AI 进入下一步
    软              硬              硬              软
（可能出错）    （一定执行）      （一定执行）   （基于可信状态）
```

---

## 九、内部编排实现机制

### 两层机制组合

**层一：Skill 文件（软层，控制 AI 行为）**

每个阶段的 Mymat skill 文件内部内嵌编排步骤、前后置约束和 guard 调用规则。执行外部能力时，必须读取并真实触发对应 skill；执行 Mymat native 能力时，必须按 Mymat 定义的产物格式写入 `.mymat/features/{feature_id}/artifacts/`，不得只用自然语言声明完成：

```markdown
# /mymat:spec skill 文件内容示例

## 执行步骤

1. 读取用户输入、issue、PRD 或 backlog 中的已确定需求
2. 读取并真实触发 OpenSpec `/opsx:propose` skill（不得仿写）：

- 由 OpenSpec 生成 proposal.md（业务价值与变更背景）
- 由 OpenSpec 生成 specs.md（验收场景、边界行为契约）
- 由 OpenSpec 生成 design.md（实现细节，不得重定义需求）
- 由 OpenSpec 生成 tasks.md（原子任务列表）

3. 运行 ./mymat-guard-spec.sh 校验四件套文件存在
4. 运行 ./mymat-state.sh 初始化 spec-graph.json SHA256
5. 展示 HCG-1，等待用户确认
6. 确认后运行 ./mymat-state.sh write spec.status done
```

**层二：Shell 脚本（硬层，强制执行，不依赖 AI 自觉）**

所有不能依赖 AI 自觉执行的操作交给 shell 脚本：校验产物、管理状态、控制流转。脚本通过 Claude Code 的 Bash 工具执行。

**职责分工**：

- AI 负责：生成内容（proposal、测试代码、实现代码、review/api/e2e/ship 报告）
- 脚本负责：校验产物存在、管理状态写入、控制阶段流转

用户只看到 Mymat 的 5 个阶段命令，底层 OpenSpec/Superpowers/native skill 的具体能力由 skill 文件内嵌逻辑编排调用。

**嵌套 Skill 触发防仿写**：skill 文件写“执行 OpenSpec propose”，AI 可能仿写格式相似的产物而非真实触发 `/opsx:propose`；guard 脚本仅验证文件存在，无法识别仿写。两层防护：

- **层一（文件校验）**：Skill 触发生成的产物在 YAML frontmatter 声明 `generated_by: openspec-propose`；guard-spec.sh 校验缺失时输出 `WARN: MISSING_TRIGGER`，不阻塞流程，仅作为审计信号。
- **层二（日志辅助）**：Skill 触发后写入 `.mymat/features/{id}/trigger-log.txt`，guard 可选校验其存在作为辅助证据。

**CLAUDE.md 强制规则**：

> 禁止仿写 Skill：执行 `/opsx:propose`、`brainstorming` 等外部 Skill 时，必须读取该 Skill 文件真实触发，不得根据描述自行生成格式相似的产物。执行 Mymat native `/review`、`/api`、`/e2e`、`/ship` 时，必须写入对应 `.mymat/` artifact，并由 guard 校验。

---

## 十、五个自动串联点

```text
串联点 1：用户输入 / issue / PRD / backlog ──→ OpenSpec /opsx:propose 输入
  Mymat 不做产品发现，只把已确定需求送入 OpenSpec 规约流程。

串联点 2：OpenSpec frozen specs/tasks ──→ Superpowers Design/Build
  HCG-1 后 specs/tasks 通过 SHA256 冻结，D/B 阶段只能消费，不得重定义需求。

串联点 3：Superpowers TDD 产物 ──→ Mymat /review
  Build 阶段有测试覆盖的代码，/review 扫描 diff 时直接识别测试文件和实现文件。

串联点 4：Build 产物 ──→ Mymat /api /e2e 条件验证
  涉及接口时触发 /api，涉及用户路径时触发 /e2e，验证报告写入 .mymat artifacts。

串联点 5：Mymat /ship ──→ OpenSpec /opsx:archive 触发
  /ship 创建 PR 后，自动触发 R-03 的 archive，delta spec 合入主规范，feature 生命周期正式结束。

横向保护：spec-graph SHA256 ──→ guard 全程完整性校验
  每次阶段推进前，guard 验证 spec 文件未被悄悄修改，需求唯一真相源受到机械性保护。
```

---

## 十一、命令设计

### 命名规范

前缀 `/mymat:`，与 OpenSpec 的 `/opsx:` 命名风格区分：OpenSpec 负责需求规约，Mymat 负责工作流治理。

### 主流程命令

| 命令                | 对应阶段 | 映射到的子任务                                                |
| ------------------- | -------- | ------------------------------------------------------------- |
| `/mymat:spec`       | S        | S-01、S-02、S-03                                              |
| `/mymat:design`     | D        | D-01、D-02                                                    |
| `/mymat:build`      | B        | B-00、B-01、B-02、B-03（对每个 Build task 循环）              |
| `/mymat:build B-05` | B        | 从 Build task B-05 恢复，继续执行 B-00、B-01、B-02、B-03 循环 |
| `/mymat:verify`     | V        | V-00、V-01、V-02、V-03、V-04                                  |
| `/mymat:release`    | R        | R-01、R-02、R-03                                              |

一个关键点是：**HCG 子任务不需要单独命令**。它们嵌在阶段命令末尾或开头：

- HCG-1 嵌在 `/mymat:spec` 末尾
- HCG-2 嵌在 `/mymat:verify` 末尾
- HCG-3 嵌在 `/mymat:release` 开头，因为发布前必须先确认

所以完整用户体验是：

```text
/mymat:spec
  → S-01? → S-02 → HCG-1

/mymat:design
  → D-01 → D-02
/mymat:build
  → for each Build task:
      B-00 → B-01 → B-02 → B-03

/mymat:verify
  → V-00 → V-01 → V-02? → V-03? → HCG-2

/mymat:release
  → HCG-3 → R-02 → R-03
```

### 状态管理命令

| 命令            | 作用                                             |
| --------------- | ------------------------------------------------ |
| `/mymat`        | 主入口，五层意图识别，自动路由到当前阶段         |
| `/mymat:status` | 展示当前 feature 所有阶段和子任务的状态快照      |
| `/mymat:park`   | 将当前进行中任务停放（`in_progress → parked`）   |
| `/mymat:resume` | 从 parked 恢复，自动定位到 last_task_id          |
| `/mymat:retry`  | 重试最近一次 failed 的子任务（最多3次）          |
| `/mymat:skip`   | 跳过当前 optional/conditional 子任务（需要确认） |

### 初始化与配置命令

| 命令             | 作用                                                                                    |
| ---------------- | --------------------------------------------------------------------------------------- |
| `/mymat:init`    | 项目初始化，安装 OpenSpec + Superpowers + Mymat，创建 `.mymat/` 目录                    |
| `/mymat:new`     | 创建新 feature，选择工作流类型，生成 state.json                                         |
| `/mymat:list`    | 列出所有活跃 feature 及其当前状态                                                       |
| `/mymat:doctor`  | 检查 jq/git/sha256sum 或 shasum 依赖、目录结构、state.json 完整性（路线图，MVP 范围外） |
| `/mymat:version` | 显示当前版本，提示可用更新（路线图，MVP 范围外）                                        |

> **可分发安装**：`npm install -g @liuchunming/mymat`，支持 Claude Code、Cursor、Codex 等 28+ 平台，Shell 脚本兼容 macOS/Linux/Windows Git Bash，并提供 `mymat update` 自更新命令。

### 工作流类型命令

| 命令               | 工作流   | 跳过阶段                        | 自动推荐条件                            |
| ------------------ | -------- | ------------------------------- | --------------------------------------- |
| `/mymat:full`      | 完整流程 | 无                              | 新文件 >5 个或影响核心模块              |
| `/mymat:quick`     | 快速流程 | 可跳过 D                        | 改动文件 3-5 个，非核心路径，需求已清楚 |
| `/mymat:micro`     | 微改动   | 可跳过 S + D，仅保留 B + 必要 V | 改动文件 <3 个，低风险局部修改          |
| `/mymat:prototype` | 原型验证 | 跳过 V + R                      | 分支名含 `proto/` 或 `spike/`           |

---

## 十二、入口意图识别（五层漏斗）

```text
层1  用户输入包含显式意图？
     "/mymat:build B-005" → 直接定位 Build 阶段 B-005 task

层2  扫描 .mymat/features/ 活跃 feature
     单一活跃 → 自动选择
     多个活跃 → 展示列表等待用户选择

层3  读取 state.json 当前状态
     status=in_progress → 展示当前进度，确认继续
     status=parked      → "上次停放于 xxx，是否恢复？"
     status=blocked     → 展示 failed task，等待处理

层4  工作流类型探测
     mymat-workflow-detect.sh 分析 diff 范围
     推荐 full / quick / micro，等待用户确认或覆盖

层5  阶段推进判定
     无歧义 → 自动推进
     有歧义 → 阻塞等待 HCG
```

---

## 十三、完整流程图

```text
/mymat 或 /mymat:spec
    ↓
┌─────────────────────────────────────────────┐
│ S: Spec                                     │
│  /opsx:propose → [HCG-1] → SHA256 锁定         │
└──────────────────────┬──────────────────────┘
                       ↓ confirmed
┌─────────────────────────────────────────────┐
│ D: Design（Superpowers 自动触发）            │
│  brainstorming → writing-plans → N 个微任务  │
└──────────────────────┬──────────────────────┘
                       ↓
┌─────────────────────────────────────────────┐
│ B: Build（循环）                            │
│  for B-001 to B-N:                          │
│    AC 锚定 → 写单元测试 → 写实现 → 验证      │
│    → state.json 记录 last_task_id           │
└──────────────────────┬──────────────────────┘
                       ↓ all tasks done
┌─────────────────────────────────────────────┐
│ V: Verify                                  │
│  /opsx:verify → /review → /api? → /e2e?     │
│  → [HCG-2]                                 │
└──────────────────────┬──────────────────────┘
                       ↓ confirmed
┌─────────────────────────────────────────────┐
│ R: Release                                  │
│  [HCG-3] → /ship → /opsx:archive           │
│  ────────────────────────────────           │
│  PR 创建完成（Merge+Deploy 由 CI/CD 负责）  │
└─────────────────────────────────────────────┘
```

---

## 十四、一句话总结

> **Mymat 是一个从已需求到 PR 的 AI Coding 交付治理系统。它用 OpenSpec 冻结需求，用 Superpowers 驱动 TDD 构建，用 Mymat native `/review`、`/api`、`/e2e` 完成验证，用 state.json 和 guard 脚本保证流程可恢复、可验证、可审计，用三个人工确认门（HCG）保住不可逆决策的人类主权。**

---

## 关联连接

- [[OpenSpec]] — 需求层基础工具
- [[Superpowers]] — 构建方法层基础工具
- [[Comet]] — 前代参考实现（OpenSpec+Superpowers）
- [[AtomicTDDWorkflow]] — Build 阶段 TDD 循环的底层原理
- [[AgentHumanPipeline]] — 宏观人机协作框架
