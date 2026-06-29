---
title: "摘要-openspec-superpowers-collaboration"
type: source
tags: [来源, OpenSpec, Superpowers, 工作流]
sources: [raw/01-articles/OpenSpec+Superpowers 协同.md]
last_updated: 2026-06-18
---

## 核心摘要

OpenSpec(规约驱动开发,SDD)与Superpowers(AI编码工作方法论)组合实现完整AI辅助开发流程:OpenSpec管理需求层(解决AI理解需求不准确),Superpowers管理执行层(解决AI写代码过程不可控)。通过四阶段协作(理解老旧项目→需求规约设计→代码并行实现→归档)和进阶模式(统一opsx命令入口+QA测试阶段+部署阶段),实现从需求到发布全流程自动化。

## 核心设计

### 基础四阶段流程
1. **第〇阶段:理解老旧项目** - `/opsx:explore`摸底老项目,理解现有业务与设计,输出现有系统规范快照
2. **第①阶段:需求规约设计** - `/opsx:propose`冻结需求与设计,通过人工门禁,SHA256锁定产物
3. **第②阶段:生成开发计划+代码并行实现** - `/opsx:apply`触发Superpowers五阶段自动执行(brainstorming→worktrees→writing-plans→subagent-driven→finishing),前后端基于同一规约并行开发
4. **第④阶段:归档** - `/opsx:archive`合并Delta Spec入主规约

### 进阶模式:统一命令入口
- `/opsx:explore` - 探索现有代码
- `/opsx:propose` - 冻结需求与设计
- `/opsx:apply` - 完成功能与单测,创建PR
- `/opsx:archive` - 合并PR
- `/opsx:qa` - API/E2E测试/代码审查/覆盖率分析
- `/opsx:release` - 灰度/发布/回滚管理

### 关键设计要点
- **SHA256锁定**:人工确认门通过后,OpenSpec计算所有已完成产物SHA256,写入state.json,防止规约被悄悄修改
- **协作契约**:OpenSpec的spec.md是前后端共同的真实来源
- **隔离机制**:Git worktree保证开发环境独立
- **质量关卡**:三级审查(实现→规约合规→代码质量)
- **人机分工**:人负责"定义清楚问题",AI负责"按规矩执行"

### 自定义Schema架构
- **schema.yaml**:定义工作流DAG(命令→阶段→产物→门禁→Superpowers技能)
- **templates目录**:proposal/spec/design/tasks/plan模板
- **config.yaml**:激活项目配置,指定Schema与技术栈
- **QA阶段产物**:qa-plan.md定义测试策略
- **Release阶段产物**:release-plan.md定义发布策略

## 关联连接
- [[OpenSpec]] — 规约驱动开发框架
- [[Superpowers]] — AI编码工作方法论
- [[摘要-openspec-superpowers-workflow]] — 四阶段实战流程
- [[摘要-openspec-superpowers-nio-workflow]] — NIO定制版本