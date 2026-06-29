# Spec: {{change_name}}

<!--
模板说明：
  此文件由 /opsx:propose 阶段生成，存放于 specs/ 目录。
  将 proposal.md 的 WHEN/THEN 行为展开为完整的 GIVEN/WHEN/THEN BDD 场景。
  每个场景直接对应 tasks.md 中的一个 TASK，并作为 verify 阶段的验证基准。
  人工确认（APPROVE）后被 SHA256 锁定。
-->

---

change: "{{change_name}}"
linked_proposal: "[[../proposal.md]]"
date: "{{date}}"
author: "{{author}}"
status: DRAFT # DRAFT | APPROVED

---

## 场景列表

<!--
BDD 格式规范：
  GIVEN  <前置条件——系统的初始状态>
    AND  <附加前置条件>（可选）
  WHEN   <用户动作或系统事件>
  THEN   <预期的可观察结果>
    AND  <附加结果>（可选）

命名规范：
  SC-NNN  主路径场景（Sequential Happy Path）
  SC-ENNN 边界场景（Edge Case）
  SC-XNNN 错误/异常场景（Error / Exception）
-->

---

### SC-001: {{happy_path_scenario_name}}

<!-- 对应 proposal.md B-001 -->

```gherkin
GIVEN {{precondition_1}}
  AND {{precondition_2}}
WHEN  {{user_action}}
THEN  {{expected_outcome_1}}
  AND {{expected_outcome_2}}
```

**验证方式**：{{verification_method}}
**关联任务**：TASK-001（见 tasks.md）

---

### SC-002: {{happy_path_scenario_name_2}}

<!-- 对应 proposal.md B-002 -->

```gherkin
GIVEN {{precondition}}
WHEN  {{user_action}}
THEN  {{expected_outcome}}
```

**验证方式**：{{verification_method}}
**关联任务**：TASK-002（见 tasks.md）

---

### SC-E01: {{edge_case_scenario_name}}

<!-- 对应 proposal.md B-E01 -->

```gherkin
GIVEN {{edge_precondition}}
WHEN  {{edge_action}}
THEN  {{edge_expected_outcome}}
```

**验证方式**：{{verification_method}}
**关联任务**：TASK-E01（见 tasks.md）

---

### SC-X01: {{error_scenario_name}}

<!-- 对应 proposal.md B-X01 -->

```gherkin
GIVEN {{error_precondition}}
WHEN  {{error_action}}
THEN  {{error_expected_outcome}}
  AND {{error_side_effect}}
```

**验证方式**：{{verification_method}}
**关联任务**：TASK-X01（见 tasks.md）

---

## 不变量（Invariants）

<!--
在所有场景执行前后必须保持为真的系统属性。
这些约束会在 verify 阶段作为隐性检查项。
-->

- **INV-001**: {{invariant_1}}
- **INV-002**: {{invariant_2}}

## 场景覆盖矩阵

| 场景 ID | proposal 行为 | 类型   | 关联任务 | 测试类型    |
| ------- | ------------- | ------ | -------- | ----------- |
| SC-001  | B-001         | 主路径 | TASK-001 | 单元 / 集成 |
| SC-002  | B-002         | 主路径 | TASK-002 | 单元        |
| SC-E01  | B-E01         | 边界   | TASK-E01 | 单元        |
| SC-X01  | B-X01         | 错误   | TASK-X01 | 单元        |

---

<!-- SHA256 锁定后由系统自动填充，请勿手动修改 -->
<!-- sha256_locked_at: -->
<!-- sha256_gate: propose-approved -->
