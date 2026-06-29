---
title: "SkillDesignPattern"
type: concept
tags: [概念, Agent, Skill, 设计模式]
sources: [raw/01-articles/04-Google总结了5种Skill设计模式，让Agent稳定输出.md]
last_updated: 2026-06-18
---

## 定义

Skill 设计模式是 Google Cloud Tech 团队从 Anthropic、Vertex AI、Google 内部的 Skill 构建实践中总结出的五种模式，用于解决 Agent 输出不稳定问题。问题不在格式而在内容设计逻辑。五种模式：ToRapper（按需注入知识）、Generator（固定输出结构）、Reviewer（分离审查与检查规则）、Inversion（先问清需求再开工）、Pipeline（分步执行流程）。模式可叠加使用。

## 问题根源

**Skill 搭好了但输出不稳定**：
- 一会儿格式乱、一会儿漏步骤、一会儿自信地答偏
- 问题不在格式（主流工具已统一 SKILL.md 格式规范）
- **真正问题在内容设计**：Skill 里面的逻辑究竟该怎么组织

## 五种设计模式总览

| 模式 | 解决的问题 | 核心做法 | 适用场景 |
|------|-----------|---------|---------|
| ToRapper | 知识什么时候交给 Agent | 按需注入：判断命中领域才加载知识 | 技术栈规范、团队约定 |
| Generator | 输出格式不稳定 | 固定结构：模板+风格指南+补问变量 | API文档、标准化报告、commit message |
| Reviewer | 审查任务要推倒重来 | 分离规则：checklist（可替换）+流程（不动） | 代码审查、安全检查、合规审查 |
| Inversion | 信息不全却急着开工 | 先问后做：Discovery→Constraints→Synthesis | 模糊需求、缺少约束的任务 |
| Pipeline | 多步骤任务总有人跳步骤 | 分步执行：定义步骤+显式门控+按需加载 | 文档生成、复杂修改、发布流程 |

## 模式选择决策树

**如何选择适合的模式**：

1. **这个 Skill 是否要产出内容？**
   - 从模板里产出 → **Generator**
   - 运行时加载某一套知识 → **ToRapper**
2. **这个 Skill 是否在评估已有输入？** → **Reviewer**
3. **开始之前必须先向用户补全信息？** → **Inversion**
4. **有严格步骤和确认点，不能跳过？** → **Pipeline**

## 模式叠加原则

这些模式之间可以互相叠加：

- **Generator + Inversion**：Generator 前面接 Inversion，先问清需求再生成
- **Pipeline + Reviewer**：Pipeline 结尾接 Reviewer，流程执行完自动审查
- **ToRapper + 任意模式**：ToRapper 几乎可以叠在任何模式上，负责补知识

## 核心思想

别再把越来越复杂的指令一股脑塞进同一个 System Prompt。真正可靠的 Skill 靠的是更合适的结构。先判断自己遇到的到底是**知识问题、结构问题、审查问题、澄清问题还是流程问题**——模式选对了，Agent 才会稳定。

## 问题类型与模式对应

| 问题类型 | 对应模式 | 核心机制 |
|---------|---------|---------|
| 知识问题 | ToRapper | 按需加载领域知识 |
| 结构问题 | Generator | 模板固定输出结构 |
| 审查问题 | Reviewer | 分离检查规则与流程 |
| 澄清问题 | Inversion | 先问清再开工 |
| 流程问题 | Pipeline | 分步执行+显式门控 |

## 关联连接

- [[摘要-skill-google-5-patterns]] — 设计模式来源文档
- [[Google]] — 提出设计模式的公司
- [[ToRapperPattern]] — 按需注入知识模式
- [[GeneratorPattern]] — 固定输出结构模式
- [[ReviewerPattern]] — 分离审查与检查规则模式
- [[InversionPattern]] — 先问清需求再开工模式
- [[PipelinePattern]] — 分步执行流程模式