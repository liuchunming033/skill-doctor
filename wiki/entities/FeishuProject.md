---
title: "FeishuProject"
type: entity
tags: [工具, 项目管理, 飞书, 流程枢纽]
sources:
  [
    raw/01-articles/AI 驱动的产品需求与设计自动化流水线.md,
    raw/01-articles/这是你想要的AI驱动的产品需求工作流吗.md,
  ]
last_updated: 2026-06-05
---

## 定义

飞书项目（FeishuProject）是字节跳动飞书旗下的项目管理工具，在 AI Native 研发工作流中承担**流程枢纽**角色：Issue 创建 → Spec 生成 → 技术方案 → 测试评审的全生命周期载体，内置与 GitLab 的 CI/CD 集成，支持自动门禁评审触发。

## 关键信息

**在 AI 产品需求流水线中的作用：**

| 节点         | 飞书项目角色                                           |
| ------------ | ------------------------------------------------------ |
| Issue 提出   | 飞书项目创建需求 Issue，分配 RID                       |
| Spec 生成    | Issue 触发 Agent 生成 Spec，自动挂载到 Issue 评论/附件 |
| 技术方案评审 | 工作流流转到技术负责人评审节点，评审通过后自动触发开发 |
| 测试用例评审 | 评审通过后触发 CI/CD 流水线                            |
| 流水线门禁   | 集成 GitLab MR 质量门禁，Spec 不合格则 MR 被 Block     |

**RID 机制：**

RID = 飞书项目自动生成的 Issue ID（如 ISSUE-8921）。全流程所有产物（Spec、技术方案、测试用例）都以 RID 为唯一索引，Agent 通过 RID 读取、绑定和追踪所有上下文。

**核心优势（相对传统工具）：**

- 与飞书IM无缝集成，减少跨工具摩擦
- 原生支持工作流自动化（飞书自动化）
- 内置 GitLab 集成，支持代码评审与流程联动

## 关联连接

- [[摘要-ai-product-requirement-pipeline]] — 五节点流水线详解
- [[摘要-ai-product-workflow]] — 三大 Agent 技能与飞书项目的协作方式
- [[ProductRequirementPipeline]] — 核心框架概念
- [[AgentHumanPipeline]] — 宏观协作框架
- [[Obsidian]] — 搭档知识底座
