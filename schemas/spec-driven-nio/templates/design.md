# Technical Design: {{change_name}}

<!--
模板说明：
  此文件由 /opsx:propose 阶段生成，记录技术设计决策与测试策略。
  基于 spec.md 的场景推导，回答"怎么做"——proposal/spec 回答"做什么"。
  人工确认（APPROVE）后被 SHA256 锁定。
  apply 阶段的 Superpowers:brainstorming 会读取此文件作为工程分析输入。
-->

---

change: "{{change_name}}"
linked_spec: "[[../specs/{{change_name}}.md]]"
date: "{{date}}"
author: "{{author}}"
status: DRAFT # DRAFT | APPROVED

---

## 架构决策

### 选择方案

<!-- 描述选定的技术实现方式，说明为什么这是最优选择 -->

**方案**：{{chosen_approach}}

**核心理由**：

- {{reason_1}}
- {{reason_2}}

### 备选方案对比

| 方案      | 优点           | 缺点           | 拒绝原因            |
| --------- | -------------- | -------------- | ------------------- |
| {{alt_1}} | {{alt_1_pros}} | {{alt_1_cons}} | {{alt_1_rejection}} |
| {{alt_2}} | {{alt_2_pros}} | {{alt_2_cons}} | {{alt_2_rejection}} |

## 变更影响分析

### 需要修改的文件

<!-- 每个文件说明：路径、修改类型（新增/修改/删除）、修改原因 -->

| 文件路径          | 变更类型 | 说明       |
| ----------------- | -------- | ---------- |
| `{{file_path_1}}` | 修改     | {{reason}} |
| `{{file_path_2}}` | 新增     | {{reason}} |

### 接口/API 变更

<!--
若有接口变更，描述 before/after 对比。
若无接口变更，写"无接口变更"。
-->

**无接口变更** / 或：

```
Before: {{before_signature}}
After:  {{after_signature}}
破坏性变更: 是 / 否
```

### 数据流说明

<!-- 简要描述数据如何在组件间流转（可选 ASCII 图或文字描述） -->

```
{{data_flow_description}}
```

## 测试策略

<!--
测试策略直接映射到 spec.md 的场景。
Superpowers:brainstorming 读取此节来制定 writing-plans 的 RED 步骤。
-->

### 单元测试

| 场景 ID | 测试目标           | 测试文件           | 测试方法           |
| ------- | ------------------ | ------------------ | ------------------ |
| SC-001  | {{test_target_1}}  | `{{test_file_1}}`  | {{test_method_1}}  |
| SC-002  | {{test_target_2}}  | `{{test_file_2}}`  | {{test_method_2}}  |
| SC-E01  | {{test_target_e1}} | `{{test_file_e1}}` | {{test_method_e1}} |
| SC-X01  | {{test_target_x1}} | `{{test_file_x1}}` | {{test_method_x1}} |

### 集成测试

<!-- 需要跨模块或跨服务验证的场景 -->

| 场景 ID   | 测试目标   | 涉及组件       |
| --------- | ---------- | -------------- |
| {{sc_id}} | {{target}} | {{components}} |

### 测试替身（Test Doubles）

<!-- 需要 Mock / Stub / Fake 的外部依赖 -->

| 依赖             | 类型               | 原因       |
| ---------------- | ------------------ | ---------- |
| {{dependency_1}} | Mock / Stub / Fake | {{reason}} |

### 覆盖率目标

- 新增代码行覆盖率：≥ {{coverage_threshold}}%
- 所有 spec 场景必须有对应测试：是

## 风险与缓解

| 风险       | 可能性   | 影响     | 缓解措施         |
| ---------- | -------- | -------- | ---------------- |
| {{risk_1}} | 低/中/高 | 低/中/高 | {{mitigation_1}} |
| {{risk_2}} | 低/中/高 | 低/中/高 | {{mitigation_2}} |

## 实现约束

<!--
在 apply 阶段 Superpowers:writing-plans 生成工程步骤时必须遵守的硬性约束。
-->

- {{constraint_1}}
- {{constraint_2}}

---

<!-- SHA256 锁定后由系统自动填充，请勿手动修改 -->
<!-- sha256_locked_at: -->
<!-- sha256_gate: propose-approved -->
