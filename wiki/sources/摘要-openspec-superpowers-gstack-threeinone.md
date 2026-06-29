---
title: "摘要-openspec-superpowers-gstack-threeinone"
type: source
tags:
  [来源, OpenSpec, Superpowers, Gstack, 三工具组合, 串联点, 七步流程, 避坑指南]
sources:
  [
    "raw/01-articles/OpenSpec、Superpowers、gstack三器合一：工程化AI编程实战，从需求到发布全流程自动化.md",
  ]
last_updated: 2026-06-06
---

## 核心摘要

B 站视频（BV1SG5d6kEMs，3:23），UP 主 Terminator-AI。聚焦三工具的**分工边界、自动串联架构和避坑原则**：OpenSpec 管需求（写代码前锁住需求），Superpowers 管质量（写代码时卡住质量），Gstack 管全流程（写完代码后包揽发布）。三套状态目录互不干扰，共存于同一 Claude Code 会话不冲突。核心结论：**关键不是三个工具都装上，而是它们之间怎么自动串联**。

## 三工具分工边界

| 工具        | 职责阶段                 | 状态存储位置             | 触发方式                    |
| ----------- | ------------------------ | ------------------------ | --------------------------- |
| OpenSpec    | 写代码**前**：需求锁定   | `openspec/` 目录         | 手动 `/opsx:propose` 等命令 |
| Superpowers | 写代码**时**：质量卡控   | `CLAUDE.md` + skill 文件 | 自动触发（Agent 检测匹配）  |
| Gstack      | 写代码**后**：全流程管理 | `gstack/` 目录           | 手动斜杠命令                |

三套状态**互不干扰**：各自独立目录，在同一会话共存不冲突。

## 四个自动串联点

1. **OpenSpec 产物 → Gstack 评审输入**：`/opsx:propose` 生成的 proposal/specs/design/tasks 四件套，直接作为 Gstack `/autoplan` 的评审材料（CEO + 工程 + 设计三视角）
2. **Superpowers HARD-GATE → 编码自动拦截**：HARD-GATE 自动拦截不先写测试直接写代码的行为，无需用户触发
3. **Superpowers TDD → Gstack review 自动生效**：有测试覆盖的代码才能通过 Gstack `/review` 的 diff 扫描
4. **Gstack /ship → OpenSpec archive 归档**：`/ship` 发布触发 delta 规范合入主规范，`/ship` 是唯一发布出口

## 七步完整流程

| 步骤 | 动作                                       | 工具        | 产物                               |
| ---- | ------------------------------------------ | ----------- | ---------------------------------- |
| 1    | 生成需求产物                               | OpenSpec    | proposal + specs + design + tasks  |
| 2    | `/autoplan` 读取产物三阶段评审             | Gstack      | CEO / 工程 / 设计评审意见          |
| 3    | TDD 铁律自动生效                           | Superpowers | 先写测试（HARD-GATE 拦截先写实现） |
| 4    | `/review` 审查代码，扫 diff                | Gstack      | code review 报告                   |
| 5    | `/qa` Playwright Chromium 真实浏览器验收   | Gstack      | QA 报告                            |
| 6    | `/ship` 版本升级 + CHANGELOG + PR 创建推送 | Gstack      | PR                                 |
| 7    | `/opsx:archive` delta 规范合入主规范       | OpenSpec    | 归档完成                           |

## 避坑三原则

- **不要重复门禁**：已用 OpenSpec specs 做设计评审，不要再用 Gstack `/plan-design-review` 重复审查同一份设计
- **specs 是唯一需求真相源**：Gstack 设计文档只描述实现细节，不得重定义需求
- **TDD 的三个例外**：一次性原型、生成的代码、配置文件可以跳过 TDD，其余铁律不打折扣

## 关联连接

- [[OpenSpec]] — 需求层工具
- [[Superpowers]] — 编码质量工具
- [[Gstack]] — 全流程工具
- [[摘要-openspec-superpowers-gstack-workflow]] — 同主题更详细版本（含完整流程）
- [[摘要-superpowers-gstack-integration]] — 37技能路由表和5个交接点（无OpenSpec）
- [[AtomicTDDWorkflow]] — Superpowers TDD 铁律的底层原理
- [[AgentHumanPipeline]] — 宏观人机协作框架
