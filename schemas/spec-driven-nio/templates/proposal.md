# Proposal: {{change_name}}

<!--
模板说明：
  此文件由 /opsx:propose 阶段生成，格式为 WHEN/THEN 可测试行为规约。
  聚焦用户可观察的结果，不含任何实现细节。
  人工确认（APPROVE）后被 SHA256 锁定，apply 阶段启动时会验证哈希。
-->

---

change: "{{change_name}}"
date: "{{date}}"
author: "{{author}}"
status: DRAFT # DRAFT | APPROVED（人工门禁通过后改为 APPROVED）

---

## 问题陈述

<!-- 描述要解决的问题或要实现的目标，1-3 句话，聚焦"为什么"，不涉及"怎么做" -->

{{problem_statement}}

## 可测试行为（WHEN/THEN）

<!--
格式规范：
  WHEN  <触发动作或条件>
  THEN  <可观察的系统响应>

原则：
  - 每个 WHEN/THEN 对必须可独立验证
  - THEN 描述外部可观察结果（API 响应、UI 变化、数据状态）
  - 不在此处描述内部实现（函数调用、数据库操作等）
  - 使用具体数值而非模糊描述（"返回 404" 优于 "返回错误"）
-->

### 主路径行为

**B-001**
WHEN {{primary_trigger_1}}
THEN {{primary_outcome_1}}

**B-002**
WHEN {{primary_trigger_2}}
THEN {{primary_outcome_2}}

<!-- 根据需要继续添加 B-003, B-004... -->

### 边界行为

**B-E01**
WHEN {{edge_trigger_1}}
THEN {{edge_outcome_1}}

### 错误行为

**B-X01**
WHEN {{error_trigger_1}}
THEN {{error_outcome_1}}

## 变更范围

### 包含（In Scope）

- {{in_scope_item_1}}
- {{in_scope_item_2}}

### 排除（Out of Scope）

- {{out_of_scope_item_1}}
<!-- 明确排除防止 scope creep -->

## 验收标准

<!--
此处是 verify 阶段的检查清单原型。
每条标准应与上方某个 WHEN/THEN 行为对应。
-->

- [ ] {{acceptance_criterion_1}} <!-- 对应 B-001 -->
- [ ] {{acceptance_criterion_2}} <!-- 对应 B-002 -->
- [ ] {{acceptance_criterion_E01}} <!-- 对应 B-E01 -->
- [ ] {{acceptance_criterion_X01}} <!-- 对应 B-X01 -->

## 影响评估

**影响范围**：{{impact_scope}}（低 / 中 / 高）
**估计复杂度**：{{complexity}}（简单 / 中等 / 复杂）
**依赖项**：{{dependencies}}（无 / 列举依赖的其他变更或外部服务）

---

<!-- SHA256 锁定后由系统自动填充，请勿手动修改 -->
<!-- sha256_locked_at: -->
<!-- sha256_gate: propose-approved -->
