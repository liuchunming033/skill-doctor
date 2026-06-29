以下是"角色驱动的全流程实战：以看板系统为例"的**四阶段使用步骤总结**，已补充**触发方式**和**触发来源**列：

---

## 第一阶段：规约设计（架构师执行）

**目标**：写代码前，先把系统行为描述清楚

| 步骤 | 操作 | 触发方式 | 触发来源 | 说明 |
|:---|:---|:---|:---|:---|
| 1. 项目初始化 | `npm install -g @fission-ai/openspec@latest` + `openspec init --tools claude,cursor` | **人工触发** | — | 创建 `openspec/` 目录和基础配置 |
| 2. 配置技术上下文 | 编辑 `openspec/config.yaml` | **人工触发** | — | 声明技术栈（如 TypeScript/React/Node.js/PostgreSQL），避免 AI 生成偏离方向的方案 |
| 3. 启动变更提案 | 在 AI 助手中执行 `/opsx:propose kanban-board-system` | **人工触发** | — | 按 DAG 依赖自动生成 proposal.md → specs/ → design.md → tasks.md |
| 4. 校验规约 | `openspec validate` + `openspec status --change kanban-board-system --json` | **人工触发** | — | 检查格式错误和逻辑矛盾（如状态冲突）；赶时间可用 `/opsx:ff` 快进 |

---

## 第二阶段：脚手架自动化生成（架构师/Lead 执行）

**目标**：将粗粒度规约细化为可执行的工程计划

| 步骤 | 操作 | 触发方式 | 触发来源 | 说明 |
|:---|:---|:---|:---|:---|
| 1. 安装 Superpowers | `/plugin install superpowers@claude-plugins-official` 或 `/add-plugin superpowers` | **人工触发** | — | 14 个 Skills 注册到 AI 助手 |
| 2. 触发 brainstorming | 告诉 AI"开始实现看板系统，规约在 `openspec/changes/kanban-board-system/`" | **人工触发** | — | 启动后，AI **自动执行** 9 步流程：探索上下文 → 澄清问题 → 方案选择 → 分段确认 → 写设计文档 → 设计自查 → 用户审阅 |
| 3. 创建隔离工作空间 | Superpowers 调用 using-git-worktrees | **自动触发** | **brainstorming**（设计审批后） | 在 `.worktrees/kanban-board` 创建分支，自动安装依赖并验证测试基线 |
| 4. 生成原子实现计划 | Superpowers 调用 writing-plans | **自动触发** | **brainstorming**（最后一步"Transition to implementation"） | 读取设计文档，拆分为 2-5 分钟/步的原子任务，保存到 `docs/superpowers/plans/`；推荐选择 **Subagent-Driven** 执行方式 |

---

## 第三阶段：并行业务实现（后端/前端并行）

**目标**：AI 子代理自动执行开发，前后端基于同一份规约同步推进

**后端流程**（单会话内串行自动循环）：

| 步骤 | 操作 | 触发方式 | 触发来源 | 说明 |
|:---|:---|:---|:---|:---|
| 1. 选择 Subagent-Driven 方式 | 在 AI 助手中回复"选择方案 1" | **人工触发** | — | 确认执行方式后，后续全部自动循环 |
| 2. 读取计划并提取任务 | Superpowers 读取 `docs/superpowers/plans/` 并提取所有任务 | **自动触发** | **用户选择 Subagent-Driven** | 准备任务上下文 |
| 3. 分派实现子代理 | 为每个 Task 创建独立子代理 | **自动触发** | **subagent-driven-development 控制器** | 按 TDD 循环执行：RED写失败测试 → GREEN最小实现 → REFACTOR |
| 4. 分派规约审查子代理 | 检查代码是否按计划实现 | **自动触发** | **实现子代理完成** | 确保代码符合实现计划中的 spec 描述 |
| 5. 分派代码质量审查子代理 | 检查风格、性能、测试质量 | **自动触发** | **规约审查通过后** | 三级审查全部通过才标记任务完成 |
| 6. 进入下一 Task | 重复步骤 3-5 | **自动触发** | **上一 Task 三级审查通过** | 循环直至所有任务完成 |
| 7. 运行全量测试 | `npm test` | **自动触发** | **全部 Task 完成** | 验证整体一致性 |
| 8. 最终代码审查 | 分派审查子代理检查跨任务一致性 | **自动触发** | **全量测试通过** | 跨任务边界检查 |
| 9. 触发分支收尾 | 执行 finishing-a-development-branch | **自动触发** | **最终审查通过** | 提供四个选项：合并/创建 PR/保留分支/丢弃 |
| 10. 选择收尾方式 | 回复"创建 PR"或"合并"等 | **人工触发** | — | 人做最终决策，AI 执行具体操作 |

**前端流程**（**独立 AI 会话**中并行执行）：

| 步骤 | 操作 | 触发方式 | 触发来源 | 说明 |
|:---|:---|:---|:---|:---|
| 1. 启动前端实现 | 在**新 AI 会话**中告知"实现前端，规约在 `openspec/changes/.../spec.md`" | **人工触发** | — | 前后端需独立会话，Superpowers 子代理驱动是单会话串行 |
| 2. 自动触发 brainstorming | AI 检测到新开发工作 | **自动触发** | **用户输入启动指令** | 读取 spec.md，经澄清问题 → 方案选择 → 生成前端设计文档 |
| 3. 自动调用 worktree | 创建隔离工作空间 | **自动触发** | **brainstorming（设计审批后）** | 同后端流程 |
| 4. 自动调用 writing-plans | 生成前端原子实现计划 | **自动触发** | **brainstorming（最后一步）** | 同后端流程 |
| 5. 后续子代理循环 | TDD → 规约审查 → 质量审查 | **自动触发** | **用户选择 Subagent-Driven** | 同后端三级审查循环 |

> **并行前提**：spec.md 已定义清楚 API 行为，双方有共同参照物，无需面对面联调

---

## 第四阶段：契约驱动的迭代（全员协作）

**场景**：新增需求（如"任务卡片加优先级字段"）

| 步骤 | 操作 | 触发方式 | 触发来源 | 说明 |
|:---|:---|:---|:---|:---|
| 1. 启动新变更提案 | `/opsx:propose add-task-priority` | **人工触发** | — | 自动生成 Delta Spec（ADDED/MODIFIED/REMOVED），只描述变更部分 |
| 2. 校验 | `openspec validate` + `openspec status` | **人工触发** | — | 确认变更规约合法 |
| 3. 应用实现 | `/opsx:apply add-task-priority` | **人工触发** | — | OpenSpec 读取 tasks.md，逐条完成、写代码、跑测试、勾选进度；Superpowers 可能**自动辅助**触发 TDD |
| 4. 归档合并 | `openspec archive add-task-priority` | **人工触发** | — | Delta Spec 合并入主规约 `specs/`，成为系统行为的一部分 |

---

## 核心要点

| 维度 | 关键设计 |
|:---|:---|
| **协作契约** | OpenSpec 的 spec.md 是前后端共同的真实来源 |
| **隔离机制** | Git worktree 保证开发环境独立 |
| **质量关卡** | 三级审查（实现 → 规约合规 → 代码质量）层层过滤 |
| **变更追溯** | Delta Spec + WAL 式归档，随时回退不污染原始数据 |
| **人机分工** | 人负责"定义清楚问题"（写规约、做关键决策），AI 负责"按规矩执行"（生成代码、跑测试、做审查） |

---

## 触发方式汇总图

```
人工触发                自动触发
─────────────────────────────────────────────────────────
/opsx:propose    ──→   DAG 生成 proposal → specs → design → tasks
安装 Superpowers  ──→   brainstorming（检测到开发意图）
"开始实现"        ──→   using-git-worktrees（设计审批后）
选择 Subagent-Driven ──→  writing-plans（brainstorming 最后一步）
                      ──→  实现子代理（计划读取完成）
                      ──→  规约审查子代理（实现完成）
                      ──→  代码质量审查子代理（规约审查通过）
                      ──→  下一 Task（三级审查通过）
                      ──→  全量测试（全部 Task 完成）
                      ──→  最终审查（测试通过）
                      ──→  finishing-a-development-branch（审查通过）
```