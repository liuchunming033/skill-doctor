---
title: "摘要-comet-readme-zh"
type: source
tags: [来源, Comet, README, 安装指南, 技术文档]
sources:
  [
    raw/01-articles/rpamiscomet Comet OpenSpec + Superpowers dual-star development workflow.md,
  ]
last_updated: 2026-06-06
---

## 核心摘要

Comet 官方 README 中文版（GitHub rpamis/comet）。补充了 6 项可学习实践要点、跨平台安装细节，以及 `comet-guard.sh`、`comet-yaml-validate.sh`、`comet-state.sh` 等守护脚本的用途说明。

## 补充技术细节

**安装前置要求**：Node.js 20+、npm/npx、Git、bash 环境（Windows 建议 Git Bash）

**`comet init` 七步交互初始化**：

1. 选择 AI 平台（自动检测已有配置）
2. 选择安装范围：项目级 / 全局
3. 选择 Skill 语言：中文 / English
4. 自动安装 OpenSpec Skill
5. 自动安装 Superpowers Skill
6. 部署 Comet Skill
7. 创建 `docs/superpowers/specs/` 和 `docs/superpowers/plans/` 工作目录

**守护脚本职责**：

- `comet-guard.sh` — 阶段退出守卫，检查任务完成状态和验证证据
- `comet-yaml-validate.sh` — YAML 字段校验（必填字段、枚举值、路径引用）
- `comet-state.sh` — 状态统一读写接口

**跨平台支持**：Claude Code、Cursor、Codex、OpenClaw、Hermes、WindSurf 等 28+ 平台；Shell 脚本兼容 macOS/Linux/Windows Git Bash

**OpenClaw/Hermes 等通用 skills CLI 平台**：`npx skills add rpamis/comet`

## 核心价值（README 原文总结）

Comet 作为"参考实现"可教会开发者：

1. 如何稳定触发嵌套 Skill（真正触发 vs. AI 仿写）
2. 如何实现多阶段自动流转（状态机保障）
3. 如何把 Spec 生命周期做成可恢复流程（`.comet.yaml` 快照）
4. 如何把文档同步从"用户提醒"变成自动化（handoff 脚本）
5. 如何设计 Agent 可执行的守护条件（脚本 > instruction）
6. 如何做跨平台 Skill 分发和安装

## 关联连接

- [[Comet]] — 工具实体页（含完整功能描述）
- [[摘要-comet-skill-intro]] — B 站视频来源
- [[摘要-comet-developer-story]] — 开发者故事来源
- [[OpenSpec]] — 依赖工具
- [[Superpowers]] — 依赖工具
