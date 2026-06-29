---
title: "摘要-superpowers-gstack-integration"
type: source
tags: [来源, 原始文件, Claude Code, 插件搭配, 开发流程]
sources:
  [
    "raw/01-articles/Superpowers + gstack 搭配实战：2 个插件，37 个技能，5 个关键交接点，闭环标准开发流程.md",
  ]
last_updated: 2026-06-06
---

## 核心摘要

深度拆解 Superpowers（145K Star）和 Gstack（69K Star）两个 Claude Code 插件如何天然互补：从源码层面验证两者能力边界无重叠、触发机制不冲突，整理 37 个技能的精确路由表和 5 个关键交接点，给出从需求到上线的完整闭环流程。

## 为什么这两个插件不冲突

| 维度     | Superpowers                          | Gstack                                         |
| -------- | ------------------------------------ | ---------------------------------------------- |
| 安装路径 | `~/.claude/skills/superpowers-*`     | `~/.claude/skills/gstack/` + 符号链接          |
| 触发方式 | **自动触发**（Agent 检测到适用场景） | **手动触发**（用户斜杠命令）                   |
| 核心关注 | 工程规范和代码质量                   | 产品决策和全生命周期交付                       |
| 技能数量 | 14 个 Skills（纯 Markdown）          | 23个命令 + 8个工具（TypeScript + Go Template） |

## 37技能路由表（关键节点）

| 开发阶段            | 走 Superpowers            | 走 Gstack                    |
| ------------------- | ------------------------- | ---------------------------- |
| 需求精炼            | `brainstorming`           | —                            |
| 产品方向诊断        | —                         | `/office-hours`              |
| 计划撰写            | `writing-plans`           | —                            |
| 计划多视角审查      | —                         | `/autoplan`                  |
| 编码实现（TDD）     | `test-driven-development` | —                            |
| 端到端 QA           | —                         | `/qa`（真实 Chromium）       |
| 代码审查（内部）    | `requesting-code-review`  | —                            |
| 代码审查（Staff级） | —                         | `/review`                    |
| 安全审计            | —                         | `/cso`（OWASP Top 10）       |
| 发布流水线          | —                         | `/ship` + `/land-and-deploy` |
| 上线监控            | —                         | `/canary`                    |

## 5个关键交接点

1. **brainstorming → /autoplan**：设计文档作为桥梁，从"怎么做"到"做得对不对"
2. **writing-plans → /plan-eng-review**：工程计划 → 架构层面审查（数据流、失败模式）
3. **test-driven-development → /qa**：单元测试通过 → 真实浏览器端到端验证
4. **systematic-debugging → /investigate**：代码层调试 → 浏览器级调试
5. **finishing-a-development-branch → /ship**：分支收尾 → 完整发布流水线

## 完整开发闭环

```
brainstorming → /autoplan → writing-plans → using-git-worktrees
→ subagent-driven-development → TDD → /qa → verification-before-completion
→ requesting-code-review → /review → finishing-branch → /ship → /canary
```

## 关联连接

- [[Superpowers]] — 工程纪律框架详情
- [[Gstack]] — 角色化虚拟团队详情
- [[AgentHumanPipeline]] — 宏观人机协作框架
- [[摘要-openspec-superpowers-gstack-workflow]] — 同系列：含 OpenSpec 的三工具组合流程
