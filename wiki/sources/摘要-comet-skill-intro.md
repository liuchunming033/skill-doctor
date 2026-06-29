---
title: "摘要-comet-skill-intro"
type: source
tags: [来源, Comet, OpenSpec, Superpowers, 状态机, Spec Coding]
sources:
  [
    raw/01-articles/开源！Comet: 基于OpenSpec和Superpowers怎么做出更好用的自动Spec Skills.md,
  ]
last_updated: 2026-06-06
---

## 核心摘要

B 站视频（BV1y4Gi6CEo1，12:08），UP 主"将现在的你"介绍开源项目 Comet：将 OpenSpec（管需求/what）与 Superpowers（管实现/how）组合成同一条流程，用轻量状态机解决断点恢复问题。五阶段 BDVRA 流程（open→design→build→verify→archive），单一 `/commit` 入口，支持 28+ AI Coding 平台。

## 核心论点

**为什么需要组合？**

- OpenSpec 擅长 spec 生命周期管理（what），但需求澄清能力不强
- Superpowers 擅长头脑风暴和执行（how），但 spec 文档管理欠缺
- 两套工具叠加：命令分散、手动切换、两套 spec 混乱

**Comet 的三个核心设计决策：**

1. **状态机替代 agent 感觉**：`comet-guard` 脚本做阶段闸门，hard stop 替代软约束
2. **单向事实链**：OpenSpec 是需求侧唯一事实，Superpowers design doc 只写技术方案，`comet-handoff` 脚本生成带 SHA256 的结构化交接包
3. **断点恢复**：`.comet.yml` 存储阶段状态 + 文档路径 + build mode，跨会话/跨设备一键 `/commit` 接续

**关键洞察**：  
AI agent 有"任务做了就做好了"的倾向——不是真正完成，是感觉完成。只有把状态更新从 instruction（软约束）移到可执行脚本（硬校验），才能让阶段流转可靠。

## 关联连接

- [[Comet]] — 工具实体页
- [[OpenSpec]] — 需求层基础工具
- [[Superpowers]] — 执行层基础工具
- [[摘要-comet-developer-story]] — 同作者：开发历程与设计决策
- [[AtomicTDDWorkflow]] — 相关：同样探讨 instruction 软约束的局限
