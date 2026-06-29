# Tasks: {{change_name}}

<!--
⚠️ 架构关键：此文件是 OpenSpec 业务任务清单
════════════════════════════════════════════════════════
  tasks.md（本文件）         = 业务任务清单（WHAT to do）
                               → OpenSpec checkbox 状态追踪
                               → 每个 task 映射到 spec.md 的一个场景

  .superpowers/impl-plan.md  = 工程实现步骤（HOW to implement）
                               → Superpowers writing-plans 生成
                               → subagent 执行，含 [RED]/[GREEN] 标注
════════════════════════════════════════════════════════
两份文档互相独立，绝对不能混淆其职责。
-->

---

change: "{{change_name}}"
linked_design: "[[../design.md]]"
date: "{{date}}"
author: "{{author}}"
status: DRAFT # DRAFT | IN_PROGRESS | DONE

---

## 业务任务清单

<!--
格式规范：
  - [ ] TASK-NNN: <业务描述>（用业务语言，不用工程语言）
  链接：对应 spec.md 中的场景 ID

  TASK-NNN   主路径任务
  TASK-ENNN  边界任务
  TASK-XNNN  错误/异常任务

  ⚠️ 禁止在此处写：
    - 具体函数名
    - 文件路径
    - [RED] / [GREEN] 标注
    - 工程实现步骤
  （以上内容属于 .superpowers/impl-plan.md 的职责）
-->

### 主路径任务

- [ ] TASK-001: {{business_task_description_1}}
      场景：[[specs/{{change_name}}.md#SC-001]]

- [ ] TASK-002: {{business_task_description_2}}
      场景：[[specs/{{change_name}}.md#SC-002]]

### 边界任务

- [ ] TASK-E01: {{edge_task_description}}
      场景：[[specs/{{change_name}}.md#SC-E01]]

### 错误处理任务

- [ ] TASK-X01: {{error_task_description}}
      场景：[[specs/{{change_name}}.md#SC-X01]]

## 完成标准

<!--
所有 tasks 标记为 [x] 且满足以下条件，视为本变更业务层完成。
工程层完成标准由 /opsx:verify 阶段负责。
-->

- [ ] 所有 TASK-NNN 标记为 [x]
- [ ] specs/{change}.md 中每个场景至少有一个对应测试通过
- [ ] design.md 的测试覆盖率目标已达到

## 任务-场景-测试 追踪矩阵

| 任务 ID  | 场景 ID | 业务描述（摘要） | 完成状态 |
| -------- | ------- | ---------------- | -------- |
| TASK-001 | SC-001  | {{summary_1}}    | ⬜       |
| TASK-002 | SC-002  | {{summary_2}}    | ⬜       |
| TASK-E01 | SC-E01  | {{summary_e1}}   | ⬜       |
| TASK-X01 | SC-X01  | {{summary_x1}}   | ⬜       |

<!-- 状态图例：⬜ 未开始 | 🔄 进行中 | ✅ 完成 -->

---

<!-- SHA256 锁定后由系统自动填充，请勿手动修改 -->
<!-- sha256_locked_at: -->
<!-- sha256_gate: propose-approved -->
