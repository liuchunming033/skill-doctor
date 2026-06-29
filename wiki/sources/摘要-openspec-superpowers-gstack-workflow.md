---
title: "摘要-openspec-superpowers-gstack-workflow"
type: source
tags: [来源, 原始文件, Claude Code, 开发流程, AI编程]
sources: [raw/01-articles/OpenSpec + Superpowers + Gstack 组合开发流程.md]
last_updated: 2026-06-06
---

## 核心摘要

OpenSpec + Superpowers + Gstack 三工具组合的完整 AI 辅助开发流程：OpenSpec 负责在编码前生成结构化规约（proposal → design → tasks）；Superpowers 负责工程质量纪律（brainstorming、TDD、调试、代码审查）；Gstack 负责产品决策和全生命周期交付（计划审查、浏览器 QA、发布、监控）。

## 三工具定位

| 工具              | 定位      | 核心价值                                    |
| --------------- | ------- | --------------------------------------- |
| **OpenSpec**    | 规约框架    | 写代码前先写清楚要做什么，产物是结构化 Markdown，AI 可直接读取执行 |
| **Superpowers** | 方法论框架   | 14个技能=工程纪律（94% PR拒绝率），自动触发，关注"怎么写好代码"   |
| **Gstack**      | 角色化虚拟团队 | 23个斜杠命令，手动触发，关注"做什么、做成什么样、怎么上线"         |

## 典型流程（需求阶段）

1. `openspec init` → 初始化项目，生成 `openspec/` 目录结构
2. `/opsx:propose <name>` → 生成 proposal、specs、design、tasks 四件套
3. `openspec validate` → 校验规约格式和逻辑一致性
4. 在 AI 助手中引导读取 `openspec/changes/` → 触发 Superpowers brainstorming
5. brainstorming 输出设计文档 → 自动转入 writing-plans

## OpenSpec 目录结构

```
openspec/
├── specs/          # 当前系统行为描述（唯一真相来源）
└── changes/        # 每个变更一个文件夹
    └── <name>/
        ├── proposal.md   # 意图和范围
        ├── design.md     # 技术方案
        ├── tasks.md      # 实现任务清单
        └── specs/        # Delta 规约（具体变更内容）
```

## 关联连接

- [[Superpowers]] — 工程纪律框架
- [[Gstack]] — 角色化虚拟团队
- [[OpenSpec]] — 规约驱动开发框架
- [[AgentHumanPipeline]] — 宏观人机协作框架
- [[摘要-superpowers-gstack-integration]] — 同系列：37个技能路由表和5个交接点
