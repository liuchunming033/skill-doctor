---
title: "摘要-ai-product-workflow"
type: source
tags: [来源, 原始文件, 产品需求工作流, Agent技能, LLM-Wiki]
sources: [raw/01-articles/这是你想要的AI驱动的产品需求工作流吗.md]
last_updated: 2026-06-05
---

## 核心摘要

完整的 AI 原生产品需求工作流设计方案：人负责投喂原始意图与上下文，AI 负责记忆、推理、生成、归档，人工只做决策评审。核心是三大标准化 Agent 技能（Spec 生成 → 技术方案生成 → 测试用例生成）的严格依赖链，配合飞书项目流水线和 Obsidian + Git 知识底座。

## 核心分工

| 角色           | 职责                                                              |
| -------------- | ----------------------------------------------------------------- |
| 人类产品经理   | 低摩擦原始信息投喂 + 最终决策评审，不整理、不结构化、不写正式文档 |
| 产品 Agent     | 严格按依赖顺序自动完成 Spec → 技术方案 → 测试用例                 |
| Obsidian + Git | 唯一可信知识底座 & 版本归档仓库                                   |
| 飞书项目       | 唯一流程枢纽、门禁评审、任务流转载体                              |

## Obsidian 知识库目录结构

```
Vault/
├── raw/          # 原始素材收件箱（只读，AI 不修改）
├── wiki/
│   ├── business/ # 产品业务知识：概念、决策、用户、战略、规则
│   └── repowiki/ # 代码技术知识：技术栈、架构、接口、数据表
└── specs/        # Agent 正式产物归档（以 RID 为唯一维度）
```

## 三大 Agent 技能

- **Skill01（SK-01-SPEC）**：Spec/PRD 自动生成，无前置依赖，流水线入口
- **Skill02（SK-02-TECH）**：技术方案自动生成，强依赖 Skill01
- **Skill03（SK-03-TEST）**：测试用例自动生成，强依赖 Skill01 + Skill02

**通用规则**：技能固定依赖链，后置技能被调用时自动校验前置产物是否存在，缺失则自动补全前置再执行。

## 全局唯一标识

RID = 飞书项目自动生成的原生 Issue ID（如 ISSUE-8921），无需手动填写，系统全自动绑定。

## 关联连接

- [[FeishuProject]] — 流程枢纽
- [[Obsidian]] — 知识底座
- [[ProductRequirementPipeline]] — 核心框架
- [[AgentHumanPipeline]] — 宏观框架
- [[LLMWikiPattern]] — 知识库底层模式
- [[摘要-ai-product-requirement-pipeline]] — 同系列：五节点流水线详解
