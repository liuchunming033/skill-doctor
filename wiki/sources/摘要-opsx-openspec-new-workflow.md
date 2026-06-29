---
title: "摘要-opsx-openspec-new-workflow"
type: source
tags: [来源, OpenSpec, OPSX, 动作驱动, 工作流, Schema, DAG]
sources: [raw/01-articles/OPSX是OpenSpec的新标准工作流.md]
last_updated: 2026-06-07
---

## 核心摘要

OPSX 是 OpenSpec 的新标准工作流，取代原有的线性阶段式流程（规划→实施→完成），改为**动作驱动**（Action-Driven）模型。用户可随时执行 propose、explore、apply、sync、archive 等命令，依赖关系作为启用条件而非强制门槛，允许在实施过程中回溯更新设计文档。核心改进：外部化配置（schema.yaml YAML DAG）、增量式制品创建、文件系统状态感知、跨编辑器兼容。

## 旧工作流缺陷 vs OPSX 改进

| 旧问题               | OPSX 解决方案                            |
| -------------------- | ---------------------------------------- |
| 指令硬编码，无法修改 | schema.yaml + 模板文件，可编辑           |
| 全有或无，阶段一刀切 | 独立验证，每个制品单独处理               |
| 固定结构，无法自定义 | `openspec schema init/fork` 自定义工作流 |
| 黑盒调试，无法追踪   | 文件系统状态感知，过程透明               |

## 命令体系

**核心命令**：

| 命令      | 用途                         |
| --------- | ---------------------------- |
| `propose` | 快速创建制品（DAG 顺序生成） |
| `explore` | 调研思考，不产出制品         |
| `apply`   | 实施任务                     |
| `sync`    | 同步规范到主文档             |
| `archive` | 归档已完成变更               |

**扩展命令**：`new`、`continue`、`ff`（快进）、`verify`

## DAG 依赖模型

制品构成有向无环图（DAG），状态转换：

```
BLOCKED → READY → DONE
（依赖未满足）（可创建/编辑）（已完成）
```

依赖关系示例（tdd-driven-v2）：

```
proposal → specs / design → tasks → plans → apply
```

- `requires`：基于依赖满足度和文件存在性检测（**不检查内容**）
- 依赖是"启用条件"（enabler），而非"强制门槛"（gate）

## 信息流演进

| 维度       | 旧工作流         | OPSX                       |
| ---------- | ---------------- | -------------------------- |
| 指令来源   | 静态硬编码       | CLI 动态查询当前状态       |
| 制品创建   | 全部一次性生成   | 逐件创建，带依赖上下文     |
| 上下文注入 | XML 标签一次注入 | 包含依赖制品内容的富上下文 |
| 调试方式   | 黑盒             | 文件系统状态透明可见       |

## 更新 vs 新建决策框架

类比 Git 分支管理策略：

- **选择更新**：意图一致、范围重叠度高、原制品仍可完成时（保留上下文）
- **选择新建**：需要清晰边界、意图发生根本变化时

## 架构对比

**旧系统**：TypeScript 硬编码模板 → 工具适配器 → 命令文件

**OPSX**：YAML 模式定义 → DAG 拓扑排序引擎 → 文件系统状态检测 → 跨编辑器兼容技能文件

## 关联连接

- [[OpenSpec]] — OPSX 所属的开发框架主体
- [[AtomicTDDWorkflow]] — OPSX schema 的具体实现案例（tdd-driven-v2）
- [[摘要-openspec-superpowers-tdd-v2]] — TDD v2 Schema 的完整实战报告
- [[openspec-superpowers-schema-driven-dispatch]] — Schema 驱动的 Skill 调度设计方案
