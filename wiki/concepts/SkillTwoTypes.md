---
title: "SkillTwoTypes"
type: concept
tags: [概念, Agent, Skill, 分类]
sources: [raw/01-articles/10-Anthropic：通过评测把skill变成可迭代资产.md]
last_updated: 2026-06-18
---

## 定义

Skill 两类分类是 Anthropic 提出的 Skill 分类方法：Capability Uplift Skills（补能力）教 Claude 原本不稳定、不会做或容易做错的事，价值前提是模型现在还不能可靠地自己完成，Eval 要回答这个 Skill 现在还带不带来真实增益；Encoded Preference Skills（固化偏好）固化你的偏好、流程、判断标准，价值前提是它有没有忠实执行你的工作流，Eval 要回答它还在按你的方式工作吗。两类 Skill 评估重点不同，但共同点：没有 Eval，你都只能猜。

## 两类 Skill 对比

| 类型 | 定义 | 价值前提 | Eval 要回答 | 典型场景 |
|------|------|---------|-----------|---------|
| **Capability Uplift Skills** | 补能力：教 Claude 做原本不稳定、不会做或容易做错的事 | 模型现在还不能可靠地自己完成 | 这个 Skill 现在还带不带来真实增益？模型升级后裸模型能否做得同样好？ | 处理某类 PDF、生成某种固定结构文档、跑一套特定分析流程 |
| **Encoded Preference Skills** | 固化偏好：固化你的偏好、流程、判断标准 | 它有没有忠实执行你的工作流 | 它还在按你的方式工作吗？ | 代码审查永远先看安全边界、写研究报告必须先区分事实推断和假设、生成视频稿遵循自己的叙事节奏 |

## Capability Uplift Skills（补能力）

### 定义

教 Claude 做一些原本不稳定、不会做或者很容易做错的事。

### 典型场景

- 处理某类 PDF
- 生成某种固定结构的文档
- 跑一套特定的分析流程

### 价值前提

**模型现在还不能可靠地自己完成**。

### Eval 要回答

**这个 Skill 现在还带不带来真实增益？**

如果模型升级以后裸模型已经能做得同样好甚至更好，那这个 Skill 可能就该退役了。

### 关键问题

**模型会进步**：今天必须靠 Skill 才能完成的任务，下一个模型版本可能自己就能完成。

Eval 和 Benchmark 一起跑，就能告诉你这个 Skill 还需不需要继续存在。

### 退役机制

Capability Uplift Skill 需要持续验证增量：
- 基准测试比较 with skill 和 without skill
- 如果不用 Skill 也能做到同样好，Skill 的存在价值就变弱了
- 如果有 Skill 明显更稳、更快、更省 token，那它就证明了自己的增量

## Encoded Preference Skills（固化偏好）

### 定义

固化的是你的偏好、你的流程、你的判断标准。

### 典型场景

- 代码审查永远先看安全边界
- 写研究报告时必须先区分事实推断和假设
- 每次生成视频稿都遵循你自己的叙事节奏

### 价值前提

**它有没有忠实执行你的工作流**。

### Eval 要回答

**它还在按你的方式工作吗？**

### 关键特点

Encoded Preference Skill 的价值不在于模型"能不能做"，而在于"是不是按你的方式做"。

即使模型自己能做这件事，但你希望它按特定的流程、特定的判断标准、特定的偏好来做，这时 Encoded Preference Skill 就有价值。

### 持续验证

Encoded Preference Skill 需要持续验证忠实度：
- 它是否还在执行你的流程？
- 它是否还在应用你的判断标准？
- 它是否还在遵循你的偏好？

## 两类 Skill 的共同点

**没有 Eval，你都只能猜。**

### 空洞问题

凭感觉改 Skill 时：
- 你怎么知道它真的变好了？
- 你怎么知道它没有只在刚才那个例子里变好？
- 你怎么知道它没有悄悄把另一个场景搞坏？

对于两类 Skill，这些问题都一样存在。

### 评估必要性

| Skill 类型 | 评估必要性 |
|-----------|-----------|
| **Capability Uplift** | 需要评估增量——Skill 带不带来真实增益？模型升级后是否还需要 Skill？ |
| **Encoded Preference** | 需要评估忠实度——Skill 是否还在按你的方式工作？ |

## 评估重点差异

### Capability Uplift 的评估重点

**增量验证**：
- with skill vs without skill 对比
- 证明 Skill 带来真实增益
- 监控模型升级后的变化，判断 Skill 是否该退役

### Encoded Preference 的评估重点

**忠实度验证**：
- Skill 是否执行你的流程
- Skill 是否应用你的判断标准
- Skill 是否遵循你的偏好

## 选择判断

**如何判断 Skill 属于哪一类？**

- **问自己**：这个 Skill 是让模型"能做原本不能做的事"（Capability Uplift），还是让模型"按我的方式做事"（Encoded Preference）？
- **价值前提不同**：前者价值在于模型还不能可靠完成，后者价值在于忠实执行你的工作流

## 关联连接

- [[摘要-anthropic-skill-lifecycle]] — 两类 Skill 来源文档
- [[Anthropic]] — 提出分类方法的公司
- [[SkillLifecycle]] — Skill 生命周期七步流程
- [[SkillThreeEvalScenarios]] — 基准测试验证增量