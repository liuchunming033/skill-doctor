---
title: "Obsidian"
type: entity
tags: [工具, 知识管理, Markdown, 本地优先]
sources:
  [
    raw/01-articles/为什么当下大家采用Obsidian作为AICoding的ContextOS.md,
    raw/01-articles/20分钟搭建AI驱动的产品知识库.md,
  ]
last_updated: 2026-06-05
---

## 定义

Obsidian 是一款基于本地 Markdown 文件的知识管理工具，以双向链接、图谱视图和插件生态著称。在 AI Native 时代，因其纯文本、本地优先、可被机器批量读取的特性，成为最适合作为 AI Coding ContextOS 的知识载体。

## 关键信息

**为什么 Obsidian 适合 AI Agent：**

| 特性             | 对 Agent 的价值                                           |
| ---------------- | --------------------------------------------------------- |
| 纯 Markdown 文件 | 无私有格式壁垒，可被脚本/Agent 批量解析                   |
| 双向链接（双链） | 给 Agent 提供业务关联图谱，读一个文件能遍历所有关联上下文 |
| 本地文件系统     | 直接作为 Agent 长期记忆库，无需 API 权限                  |
| 规范目录结构     | 可建立统一 Schema，Agent 批量加载                         |

**竞品对比（Agent 友好度）：**

- Notion：私有数据库结构，Agent 很难批量读取 ✗
- 飞书/语雀：偏文档，弱关联，无法形成知识网络 ✗
- Confluence：太重，维护成本极高 ✗
- 普通文件夹：结构混乱，上下文碎片化 ✗

**核心插件（与 AI 工作流配合）：**

- **Dataview**：查询页面 frontmatter，生成动态上下文视图
- **Templater**：一键生成符合格式的 Prompt 片段
- **Obsidian Web Clipper**：浏览器扩展，将网页文章转为 Markdown
- **Graph View**：可视化知识网络，发现孤儿页面和知识中心节点

**在 LLM-Wiki 架构中的角色：**

- 作为 IDE，LLM 是程序员，wiki 是代码库
- `raw/` 层：人投喂原始素材（只读，不可修改）
- `wiki/` 层：LLM 全权维护的结构化知识层
- `specs/` 层（可选）：Agent 产物归档层

## 关联连接

- [[摘要-obsidian-context-os]] — 为什么选 Obsidian 作为 AI Coding ContextOS
- [[摘要-20min-ai-knowledge-base]] — 20分钟搭建实操指南
- [[ContextOS]] — Obsidian 所承担的上下文操作系统角色
- [[LLMWikiPattern]] — Obsidian 是实现该模式的最佳载体
- [[GitHubCopilot]] — 与 Obsidian 配合的 AI 推理引擎
