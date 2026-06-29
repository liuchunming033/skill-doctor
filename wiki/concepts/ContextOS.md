---
title: "ContextOS"
type: concept
tags: [方法论, AI Coding, 上下文管理, ContextOS]
sources: [raw/01-articles/为什么当下大家采用Obsidian作为AICoding的ContextOS.md]
last_updated: 2026-06-05
---

## 定义

ContextOS（上下文操作系统）是 AI Coding 时代对知识管理工具的重新定义：它不只是个人笔记软件，而是作为 AI Agent 的"长期记忆 + 推理底座"，管理产品、技术、设计、测试等多维上下文，让 Agent 在任何时候都能获取足够精准的背景知识来完成任务。

## 四大硬性要求

| 要求                      | 说明                                                     |
| ------------------------- | -------------------------------------------------------- |
| 纯文本 / 纯 Markdown      | Agent 可直接解析，无需 API 权限，无私有格式壁垒          |
| 本地文件系统              | Agent 可批量读写，无访问限制，支持 Git 版本控制          |
| 双向链接                  | 提供知识关联图谱，Agent 读一个文件可遍历相关上下文       |
| 统一 Schema / Frontmatter | Agent 批量加载时能提取结构化元数据（标签、类型、来源等） |

## Obsidian 为什么是目前最优解

Obsidian 是唯一同时满足以上四点的主流知识工具：

- 纯 `.md` 文件，本地存储，Git 友好
- 原生双链（`[[wikilink]]`）语法
- 支持 YAML frontmatter
- 插件生态完善（Dataview、Templater 等）

详见 [[Obsidian]]。

## 在 AI Native 研发工作流中的位置

```
ContextOS (Obsidian)
    ├── wiki/business/  → 产品 Agent 的推理底座
    ├── wiki/repowiki/  → 技术方案 Agent 的代码知识图谱
    └── wiki/specs/     → 产物归档（可查询可追溯）
```

人类通过 raw/ 投喂素材，Agent 编译并维护 wiki/，所有下游 Agent（Spec、Tech、Test）都从 wiki/ 读取上下文，产出品质直接取决于 wiki 的 ingest 质量。

## 知识冲突

与"Notion 也可以"说法的对比：  
Notion 的数据库结构不对 Agent 友好，无法批量解析，依赖 API 访问，且迁移成本高。在真实 Agent 工作流中，Notion 劣势明显。

## 关联连接

- [[Obsidian]] — ContextOS 的最佳实现载体
- [[LLMWikiPattern]] — ContextOS 内部的知识维护范式
- [[AgentHumanPipeline]] — ContextOS 服务的宏观人机协作框架
- [[ProductRequirementPipeline]] — ContextOS 支撑的核心产出流水线
- [[摘要-obsidian-context-os]] — 详细论述来源
