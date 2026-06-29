---
title: "摘要-anthropic-skill-creator-practice"
type: source
tags: [来源, Skill, Anthropic, skill-creator]
sources: [raw/01-articles/Anthropic的skill-creator实践  .md]
last_updated: 2026-06-18
---

## 核心摘要

skill-creator 是 Anthropic 的 Meta Skill（元技能），管理整个 Skill 的生命周期，而非单一业务能力。2026 年 3 月更新后，从"Skill 生成器"演进为完整的 Skill Engineering 体系，覆盖创建、修改、测试、评估、优化五大功能。

## 关键信息

### 五类核心场景
1. **从零新建专属 Skill** - 封装固定工作流程、模板、规则为永久可用 Skill
2. **编辑优化已有 Skill** - 改造旧 Skill、补漏洞、适配新场景
3. **标准化测评验证** - 跑真实测试用例，检验输出是否合规稳定
4. **专业性能基准测试** - 方差分析对比版本快慢、稳定性、Token 消耗差异
5. **触发精度专项优化** - 解决 Skill 该用不用、乱触发、漏触发问题

### 完整闭环
形成：定需求 → 写初稿 → 跑双组对照测试 → 量化打分 + 人工评审 → 迭代优化 → 触发精准度优化闭环。

### skill-creator 能力清单
- 创建新技能
- 改进现有技能
- 运行测试
- 性能评估
- 优化触发描述

## 关联连接
- [[SkillLifecycle]] — Skill 七步生命周期
- [[SkillScorerSystem]] — 评分器系统
- [[SkillEvaluationFramework]] — Skill 评估框架
- [[Anthropic]] — 开发 skill-creator 的公司
- [[ClaudeCode]] — skill-creator 的运行环境