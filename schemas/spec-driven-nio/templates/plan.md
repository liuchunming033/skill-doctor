# Implementation Plan: {{change_name}}

<!--
⚠️ 架构关键：此文件是 Superpowers:writing-plans 的输出产物
════════════════════════════════════════════════════════
  .superpowers/impl-plan.md（本文件）= 工程实现步骤（HOW to implement）
                                       → 由 Superpowers:writing-plans 生成
                                       → 基于 brainstorming 对以下文件的分析：
                                         • proposal.md
                                         • specs/{change}.md
                                         • design.md
                                       → 绝对不读取、不依赖 tasks.md

  tasks.md                            = 业务任务清单（WHAT to do）
                                       → OpenSpec checkbox 状态追踪
════════════════════════════════════════════════════════

生成规范：
  - 每个步骤 2-5 分钟可完成（物理约束，防止 AI 批量执行）
  - 每个步骤标注 TDD 阶段：[RED] / [GREEN] / [REFACTOR]
  - 严格交替：RED → GREEN → (可选 REFACTOR) → RED → GREEN → ...
  - 每个步骤包含明确的证据要求（必须是真实命令输出）
-->

---

change: "{{change_name}}"
generated_by: "Superpowers:writing-plans"
input_artifacts:

- "proposal.md"
- "specs/{{change_name}}.md"
- "design.md"
  explicitly_excludes: "tasks.md"
  date: "{{date}}"

---

## 工程实现步骤

<!--
步骤格式：

### Step NNN [TDD_PHASE] — <简洁描述> (~X min)

**操作**：<具体要做什么，用代码/命令层面的语言>
**文件**：`<目标文件路径>`
**前置**：上一步已完成（Step NNN-1）

**证据要求**：
- 命令：`<测试命令>`
- RED 步骤预期输出：X failing, 0 passing（必须失败）
- GREEN 步骤预期输出：X passing, 0 failing（必须通过）
- 实际输出（由子代理填写）：[待填写]
-->

---

### Step 001 [RED] — {{test_name_1}} (~{{duration}} min)

**操作**：编写失败测试——`{{test_function_name_1}}`
**文件**：`{{test_file_path_1}}`
**对应场景**：SC-001（specs/{{change_name}}.md）
**前置**：工作分支 opsx/{{change_name}} 已创建

**证据要求**：

- 命令：`{{test_command}}`
- 预期：1 failing, 0 passing
- 实际输出（子代理填写）：

```
[待子代理填写——必须包含真实的测试失败输出]
```

---

### Step 002 [GREEN] — {{impl_description_1}} (~{{duration}} min)

**操作**：编写最少代码使 Step 001 的测试通过（不多写一行）
**文件**：`{{impl_file_path_1}}`
**前置**：Step 001 完成（1 failing 已确认）

**证据要求**：

- 命令：`{{test_command}}`
- 预期：1 passing, 0 failing
- 实际输出（子代理填写）：

```
[待子代理填写——必须包含真实的测试通过输出]
```

---

### Step 003 [REFACTOR] — {{refactor_description_1}} (~{{duration}} min)

<!--
REFACTOR 步骤可选——仅在需要代码清理时添加。
重构不改变行为，测试结果应与 Step 002 相同。
-->

**操作**：重构——{{refactor_rationale}}（不改变行为）
**文件**：`{{impl_file_path_1}}`
**前置**：Step 002 完成（1 passing 已确认）

**证据要求**：

- 命令：`{{test_command}}`
- 预期：1 passing, 0 failing（与 Step 002 相同）
- 实际输出（子代理填写）：

```
[待子代理填写]
```

---

### Step 004 [RED] — {{test_name_2}} (~{{duration}} min)

**操作**：编写失败测试——`{{test_function_name_2}}`
**文件**：`{{test_file_path_2}}`
**对应场景**：SC-002（specs/{{change_name}}.md）

**证据要求**：

- 命令：`{{test_command}}`
- 预期：2 failing, 0 passing（包含新失败测试）
- 实际输出（子代理填写）：

```
[待子代理填写]
```

---

<!-- 继续按 RED → GREEN → (REFACTOR) 模式添加步骤... -->

---

## 执行规则

<!--
子代理执行规范（固化在此，由 Superpowers:subagent-driven-development 强制执行）
-->

1. **物理隔离**：每个步骤由独立子代理执行（fresh context），禁止跨步骤批量执行
2. **单步单阶段**：每个子代理只执行一个 RED 或 GREEN 任务
3. **证据必填**：每个子代理提交时必须填写"实际输出"区块（不得留空）
4. **RED 验证**：[RED] 步骤的实际输出必须包含失败信息（不可伪造通过）
5. **GREEN 验证**：[GREEN] 步骤的实际输出必须包含全部测试通过
6. **禁止超出**：每步骤只完成描述的操作，不提前实现下一步

## 证据汇总

<!--
所有步骤完成后，由最终子代理汇总所有证据。
-->

| 步骤 | TDD 阶段 | 测试结果                        | 证据状态  |
| ---- | -------- | ------------------------------- | --------- |
| 001  | RED      | {{expected_fail_count}} failing | ⬜ 待执行 |
| 002  | GREEN    | {{expected_pass_count}} passing | ⬜ 待执行 |
| 003  | REFACTOR | {{expected_pass_count}} passing | ⬜ 待执行 |
| 004  | RED      | {{expected_fail_count}} failing | ⬜ 待执行 |

<!-- 状态图例：⬜ 待执行 | ✅ 已完成+证据已填写 | ❌ 失败/证据缺失 -->

## 覆盖率检查

完成所有步骤后执行：

```bash
{{coverage_command}}
```

预期：行覆盖率 ≥ {{coverage_threshold}}%，所有 spec 场景有对应测试。
