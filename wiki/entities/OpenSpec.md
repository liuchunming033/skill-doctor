---
title: "OpenSpec"
type: entity
tags: [工具, 规约驱动, AI编程, Fission AI]
sources:
  - raw/01-articles/OpenSpec + Superpowers + Gstack 组合开发流程.md
  - Clippings/从古法编程到 AI 编程：Superpowers + OpenSpec 协同开发实战指南.md
  - raw/01-articles/OPSX是OpenSpec的新标准工作流.md
last_updated: 2026-06-07
---

## 定义

OpenSpec 是 Fission AI 团队开发的规约驱动开发框架（GitHub 40.9k Star）。核心理念：**写代码之前，先把要做什么写清楚**。产物是结构化的 Markdown 文件，AI 编程助手可以直接读取、理解、执行。据实测，使用 OpenSpec 后同需求下 Token 消耗降低 30-50%，返工率下降 60% 以上。

## 关键信息

**四件套产物**（每个变更自动生成）：

- `proposal.md` — 意图和范围
- `design.md` — 技术方案
- `tasks.md` — 实现任务清单
- `specs/` — Delta 规约（Given/When/Then 格式的行为描述）

**核心命令：**

```
openspec init --tools claude,cursor   # 项目初始化
/opsx:explore                         # 探索现有代码结构（适合老旧项目摸底）
/opsx:propose <change-name>           # 生成变更四件套
/opsx:ff <change-name>                # 快进命令，一次性生成所有制品
/opsx:apply <change-name>             # 执行变更（AI 获取 instruction 并执行）
/opsx:sync                            # 合并增量规范到主规范
/opsx:archive                         # 归档已完成的变更记录
/opsx:verify                          # 验证实现是否偏离设计
openspec validate                     # 校验规约格式和逻辑一致性
openspec status --change <name> --json
openspec schema validate <schema>     # 校验自定义 Schema（实验性功能）
```

**config.yaml 关键字段：**

- `context`：技术栈和架构约束（决定 AI 生成方向）
- `rules.specs`：规约格式要求（如 Given/When/Then）

**与 Superpowers 的配合注意事项**：  
Superpowers 的 brainstorming 技能**不会自动识别** OpenSpec 的目录结构。需要在对话中明确引导 AI 读取 `openspec/changes/` 目录下的文件。

## OPSX：动作驱动架构（新标准工作流）

OPSX 是 OpenSpec 的新标准工作流，取代旧版线性阶段式流程，改为**动作驱动**（Action-Driven）模型：

- **旧模式**：规划 → 实施 → 完成（强制线性，全有或无）
- **OPSX 模式**：随时执行任意命令，依赖关系是「启用条件」而非「强制门槛」

**底层引擎**：YAML 模式定义 + DAG 拓扑排序 + 文件系统状态感知（BLOCKED → READY → DONE）

**自定义工作流**：`openspec schema init <name>` 或 `openspec schema fork default <name>` 创建专属 Schema（如 tdd-driven-v2）

## 关联连接

- [[Superpowers]] — 需求阶段后的工程执行框架
- [[Gstack]] — 产品决策和上线流程框架
- [[摘要-openspec-superpowers-gstack-workflow]] — 三工具组合的完整流程
- [[ProductRequirementPipeline]] — 同类理念：AI驱动的结构化需求流水线
- [[摘要-superpowers-openspec-legacy-project]] — 老旧项目引入 OpenSpec+Superpowers 的四阶段工作流
- [[摘要-openspec-superpowers-tdd-v2]] — TDD Schema 实验报告，四层防护模型
- [[摘要-openspec-superpowers-new-project-guide]] — 新项目三个连接点全流程
- [[摘要-opsx-openspec-new-workflow]] — OPSX 动作驱动架构与 DAG 状态机详解
