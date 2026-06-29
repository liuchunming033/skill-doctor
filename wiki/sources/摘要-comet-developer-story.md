---
title: "摘要-comet-developer-story"
type: source
tags: [来源, Comet, 开发者故事, Spec Coding, 状态机, 意图识别]
sources: [raw/01-articles/Comet Spec Skill的开发者故事.md]
last_updated: 2026-06-06
---

## 核心摘要

B 站视频（BV129Vf67EEi，11:52），Comet 作者分享开发历程：从 CLAUDE.md SOP 起步，遭遇 agent 跳步、skill 不真实触发、状态飘移三大问题后，演进出状态机 + guard 脚本的解决方案。重点解析四层意图识别漏斗和跨设备断点恢复机制。

## 开发演进路径

**阶段一（失败）**：写在 CLAUDE.md 的 SOP 流程

- 问题：agent 跳过步骤；即使用 ops 级模型，skill 也可能不真实触发（loading 标志不出现），而是 AI 按描述推理仿写

**阶段二（探索）**：强语气 + few-shot 示例

- 问题：agent 仍会跳过状态更新；few-shot 分散导致机制脆弱；上下文压缩后早期规则覆盖后续链路

**阶段三（成型）**：状态机 + CLI 脚本

- 关键决策：把 `ask_user` 改为调用 OpenSpec 的 `ask_user_question` 工具（参考 OpenSpec 最佳实践），强制等待用户确认
- 结果：稳定的阶段校验，agent 不再绕过

## 三大痛点（来自真实用户场景）

| 痛点                        | 现象                             | Comet 解法                                   |
| --------------------------- | -------------------------------- | -------------------------------------------- |
| Spec 文档太多触发上下文压缩 | agent 写完代码但文档步骤没打勾   | guard 脚本强制文档状态与代码状态同步         |
| 同天多次使用 Superpowers    | 多份相同日期文档，完成状态难辨认 | `.comet.yml` 状态快照 + archived 字段        |
| spec/plan 关联弱            | 只靠文件名相似，找不到对应文档   | comet-handoff 脚本生成带路径和哈希的结构化包 |

## 四层意图识别漏斗

用户输入 `/commit` 后，Comet 的识别链：

1. **preset**：用户输入是否包含明确意图
2. **探测活跃 change**：扫描 OpenSpec changes 目录
3. **发现状态快照**：读取 `.comet.yml`
4. **阶段判定链**：无歧义时自动推进，有歧义时阻塞等待用户确认

**人机交互原则**："如果直接一下跑完，和 vibe coding 有什么区别？"——关键节点保留用户确认，核心推进交给状态机。

## 关联连接

- [[Comet]] — 工具实体页
- [[摘要-comet-skill-intro]] — 同系列：Comet 功能介绍视频
- [[AtomicTDDWorkflow]] — 相同结论：instruction 是软约束，脚本是硬约束
- [[OpenSpec]] — 借鉴了 ask_user_question 最佳实践
- [[Superpowers]] — 执行层基础
