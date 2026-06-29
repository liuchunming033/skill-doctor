---
title: "摘要-skill-课程-第4章"
type: source
tags: [来源, Skill课程, SkillTriggerRouting, YAML, description]
created: 2026-06-18
updated: 2026-06-18
sources: [output/skill/04-YAML-Frontmatter精髓.md]
related: [wiki/concepts/SkillTriggerRouting.md, wiki/concepts/SkillFileStructure.md, wiki/concepts/DynamicLoading.md]
---

## 核心摘要

本章聚焦 SKILL.md 的 YAML Frontmatter 核心——description 字段。它是 Skill 的触发路由机制：智能体启动时预加载所有 Skill 的元数据进入系统提示词，AI 需要靠一句话简介判断当前任务是否触发该 Skill。写得差会造成 90% 的漏触发和误触发问题。给出正确写法公式：做什么 + 何时用 + 触发关键词，以及 Anthropic 强制规则和 Perplexity 最佳实践。

## 关键洞察

### description 的核心作用：触发路由机制

智能体启动时，所有 Skill 的 YAML 元数据（name + description）被预加载进系统提示词，AI 靠一句话简介判断：
- 当前任务要不要用这个技能
- 什么时候该触发这个技能

### 90% 的人常犯的三类错误

1. **太被动**："when asked" 导致 AI 不敢主动识别场景，大量漏触发
2. **太模糊**："helps with documents" 太泛，导致误触发和漏触发
3. **第一人称视角**："I can help you..." 会在系统提示词中造成混乱

### 正确写法公式

**好描述 = 做什么 + 何时用 + 触发关键词**

示例：`"Generate professional weekly reports. Use when the user mentions '周报', 'weekly report', '本周总结', even if they don't explicitly ask for a 'report'."`

### Anthropic 强制规则

- 必须第三人称编写（不能 "I can help you"）
- 不能包含 XML 标签
- 不能超过 1024 字符（建议控制在 200-300 字符以内）
- 不能包含保留词：`anthropic`、`claude`

### Perplexity 最佳实践

以 **"Load when"** 开头，明确触发逻辑，风格统一易于维护。

## 关联连接

- [[SkillTriggerRouting]] — Skill 触发路由机制概念
- [[SkillFileStructure]] — YAML Frontmatter 所在的文件结构
- [[DynamicLoading]] — 元数据预加载机制
- [[ProgressiveDisclosure]] — 分层加载原理
- [[摘要-skill-anthropic-doc-part2]] — YAML frontmatter 官方要求来源
