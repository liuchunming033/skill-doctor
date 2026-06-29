---
title: "摘要-perplexity-skill-practice"
type: source
tags: [来源, Skill, Perplexity]
sources: [raw/01-articles/解读 Perplexity的文章《Designing, Refining, and Maintaining Agent Skills at Perplexity》.md]
last_updated: 2026-06-18
---

## 核心摘要

Perplexity 内部建立了严格管理的 Skill 资源库，包含通用工具、专业领域能力和小众功能。Skill 是给大模型和运行环境搭建专属上下文，不是单纯代码。完整 Skill 由文件夹组成（SKILL.md + scripts/ + references/ + assets/ + config.json），采用三层加载机制（索引层/加载层/运行层），每层消耗不同 Token。

## 关键信息

### Skill 开发五步流程
1. **步骤0：先写测评用例** - 正向用例 + 反向用例，确认 Skill 能正常加载
2. **步骤1：打磨 description** - 以 Load when 开头，控制在 50 词以内，写用户真实需求
3. **步骤2：撰写 SKILL.md 正文** - 省略 AI 天生掌握的基础操作，重点写踩坑特例
4. **步骤3：分层文件夹拆分** - scripts 存固定逻辑，references 存大容量文档，assets 存模板
5. **步骤4：多轮迭代优化** - 先跑基准效果，扩充测评用例，完整测试后提交

### 长期维护机制
- **踩坑清单正向扩充（Gotchas Flywheel）**：AI 出现新错误 → 新增踩坑说明
- **多套测评套件持续校验**：加载路由测评、分层加载测评、端到端任务测评、多模型兼容测评

### Skill 使用判定
**需要做 Skill**：模型原生回答出错、输出不稳定、专属行业信息、带有主观审美
**不需要做 Skill**：模型已掌握的基础知识、通用全局规则、外部接口频繁更新

## 关联连接
- [[AgentSkill]] — Skill 的核心定义
- [[ProgressiveDisclosure]] — 渐进式披露机制
- [[SkillEvaluationFramework]] — Skill 评估框架
- [[Perplexity]] — 文章来源公司（潜在实体）