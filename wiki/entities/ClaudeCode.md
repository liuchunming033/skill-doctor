---
title: "ClaudeCode"
type: entity
tags: [产品, AI编程助手, Anthropic]
sources:
  [
    raw/01-articles/05-你的团队缺哪类Skill？Claude Code内部9类能力地图.md,
    raw/01-articles/06-Claude Code内部实践：Skill编写的9个最佳实践.md,
  ]
last_updated: 2026-06-18
---

## 定义

Claude Code 是 Anthropic 开发的 AI 编程助手，基于 Claude 模型构建，内置 Skills 机制和工具调用能力。Claude Code 核心团队总结了内部几百个 Skill 的实践经验，提出 9 类能力地图和 9 个最佳实践，成为 Skill 设计和运营的重要参考。

## 关键信息

### 产品定位

- **AI 编程助手**：辅助开发、测试、部署全流程
- **内置 Skills 机制**：动态加载技能模块，突破上下文限制
- **工具调用能力**：可以运行脚本、访问文件系统、连接外部 API

### Skill 实践贡献

#### 9 类能力地图

Claude Code 核心团队盘点内部几百个 Skill，总结为 9 类能力，收束到四个环节：
- **认知环节**：内部库与接口文档、数据获取与分析、故障排查手册
- **生产环节**：代码脚手架与模板、业务流程与团队自动化
- **验证环节**：代码质量与审查、产品验证
- **交付环节**：持续集成与部署、基础设施运维

**核心价值**：这张地图帮团队看清哪些能力已沉淀成系统，哪些关键经验还停留在人脑里。

#### 9 个最佳实践

Claude Code 核心开发者总结构建 Skill 的 9 个最佳实践，解决三个递进问题：
- **内容层**（被看见和被理解）：description 写触发条件、不陈述显而易见的事、构建 Gotchas 部分
- **结构层**（可复用和不僵化）：使用文件系统和渐进式披露、仔细考虑设置流程、避免过度约束
- **高级技术层**（有状态和可组合）：内存与数据存储、存储脚本并生成代码、按需 Hooks

**核心思想**：好的 Skill 不是告诉 Claude 每一步做什么，而是给它组合的能力，让它在执行时自己决定怎么做。

### 典型 Skill 案例

#### frontend-design Skill

- **问题**：Claude 生成的前端界面总是用 Inter 字体和紫色渐变，看起来很"AI味"，客户不喜欢
- **Skill 设计**：不教 Claude 怎么写 React（Claude 本来就会），只告诉它——别再用 Inter 和紫色渐变，客户不喜欢
- **启示**：Skill 的价值在于补充 Claude 默认不知道的上下文、偏好和坑

#### careful Skill

- **功能**：阻止危险命令（如 `rm -rf`、`drop table`）
- **机制**：调用 careful 时注册一个 hook，只在当前会话有效，会话结束后自动失效
- **启示**：按需 Hooks，规则不一直开启但特定场景下需要

### 产品特点

- **Skills 动态加载**：按需检索、挂载和使用技能模块
- **工具集成**：运行 Bash、Python、访问文件系统
- **渐进式披露**：三层加载（元数据→正文→附属文件）
- **认知执行分离**：上下文只装载思考所需信息，执行在虚拟机进行

## 关联连接

- [[Anthropic]] — Claude Code 的开发公司
- [[Claude]] — Claude Code 基于的 AI 模型
- [[摘要-claude-code-9-skill-types]] — 9 类能力地图来源文档
- [[摘要-skill-9-best-practices]] — 9 个最佳实践来源文档
- [[SkillCapabilityMap]] — 9 类能力地图概念
- [[SkillBestPractices]] — 9 个最佳实践概念