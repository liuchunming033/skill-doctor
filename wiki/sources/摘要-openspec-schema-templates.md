---
title: "摘要-openspec-schema-templates"
type: source
tags: [来源, OpenSpec, Schema, 模板]
sources: [raw/01-articles/openspec-schema/templates/]
last_updated: 2026-06-18
---

## 核心摘要

OpenSpec Schema定义的5个模板文件:proposal.md(提案模板:意图与范围/验收标准/关联知识/风险评估/SHA256)/spec.md(规约模板:领域模型/场景规约GIVEN-WHEN-THEN/异常场景/接口规约/数据模型变更)/design.md(设计模板:技术概要/架构设计/接口设计/测试策略/非功能设计/风险评估)/tasks.md(任务模板:业务任务清单/依赖关系)/plan.md(计划模板:工程实现计划)。所有模板均包含SHA256锁定机制,确保产物一致性。

## 模板文件清单

### 1. proposal.md - 提案模板

**核心结构**:
- **元信息**:RID/标题/阶段/状态/创建时间
- **意图与范围**:一句话描述/业务价值/范围(包含vs不包含)/用户故事
- **验收标准(WHEN/THEN)**:正向场景/异常场景/边界场景
- **关联知识**:Raw素材/Wiki概念/RepoWiki技术约束
- **风险评估**:风险/影响/概率/缓解措施表格
- **SHA256**:锁定文件完整性

### 2. spec.md - 规约模板

**核心结构**:
- **领域模型**:entities/fields/relations定义
- **场景规约(GIVEN/WHEN/THEN)**:
  - 场景1/场景2的Gherkin格式描述
  - 包含具体示例
- **异常场景**:错误场景的Gherkin描述
- **接口规约**:API名称/请求/响应/错误码
- **数据模型变更**:DDL语句
- **SHA256**:锁定文件完整性

### 3. design.md - 设计模板

**核心结构**:
- **技术概要**:实现思路/改动范围(模块/改动类型/说明)
- **架构设计**:架构图(Mermaid)/模块职责
- **接口设计**:API变更(端点/方法/变更类型/说明)/数据模型变更
- **测试策略**:单元测试/集成测试/E2E测试
- **非功能设计**:性能/安全/可观测性/灰度策略/回滚方案
- **风险评估**:风险/影响/概率/缓解措施
- **SHA256**:锁定文件完整性

### 4. tasks.md - 任务模板

**核心结构**:
- **业务任务清单**:
  - Task 1/2/3,每个任务包含子任务清单(checkbox格式)
  - 每个任务的验收标准
- **依赖关系**:Mermaid流程图展示任务间依赖
- **SHA256**:锁定文件完整性

### 5. plan.md - 计划模板

**核心结构**:(从读取的文件推断)
- 工程实现计划
- 具体实现步骤
- SHA256锁定

## 模板设计特点

### SHA256锁定机制
- 所有模板产物都包含SHA256哈希值
- 用于验证文件完整性,防止未经授权的修改
- 在schema.yaml的gate: sha256_check中使用

### 占位符系统
- 使用{{VARIABLE_NAME}}格式标记占位符
- 方便自动填充和模板渲染
- 保持结构一致性

### 阶段状态管理
- 每个模板明确标注阶段(Proposal)和状态
- 支持工作流追踪和门禁验证

### Gherkin格式验收标准
- 使用GIVEN-WHEN-THEN格式描述场景
- 可测试行为描述,验收标准即测试依据
- 支持正向/异常/边界场景全覆盖

## 关联连接
- [[OpenSpec]] — 规约驱动开发框架
- [[摘要-openspec-schema-yaml]] — Schema定义文件
- [[摘要-openspec-superpowers-collaboration]] — OpenSpec+Superpowers协同