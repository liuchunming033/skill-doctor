---
title: "摘要-20min-ai-knowledge-base"
type: source
tags: [来源, 原始文件, 知识库搭建, Obsidian, LLM-Wiki]
sources: [raw/01-articles/20分钟搭建AI驱动的产品知识库.md]
last_updated: 2026-06-05
---

## 核心摘要

20分钟内用 Obsidian + GitHub Copilot + Git 搭建 AI 驱动产品知识库的实操指南。核心思想来自 [[KarpathyAndrej]] 的 LLM-Wiki 模式：人只做两件事（喂资料、提问题），LLM 承担全部维护工作，实现知识复利效应。相比 PARA 分类体系，Karpathy 方案对人的要求更低、知识积累效应更强。

## 知识库五个核心环节

1. **采集** — 把外部信息拉进 raw/
2. **摄入** — AI 自动结构化处理（ingest）
3. **整理** — 建立双向链接与分类
4. **查询** — 自然语言问答式检索，生成新知识（Spec、TestCase等）
5. **维护** — 定期清理与更新（lint）

## PARA vs Karpathy 对比

| 维度     | PARA                     | Karpathy LLM-Wiki          |
| -------- | ------------------------ | -------------------------- |
| 本质     | 分类体系（文件夹往哪放） | 工作流系统（知识怎么流转） |
| 维护者   | 人手动分类整理           | LLM 自动编译维护           |
| 维护成本 | 随笔记增长，人越来越累   | LLM 承担维护，近乎为零     |

## 核心工具组合

- **Obsidian**：本地知识库载体（纯 Markdown + 双链）
- **GitHub Copilot**：AI 推理引擎（执行 ingest/query/lint）
- **Git**：版本管理和协作

## 关联连接

- [[Obsidian]] — 核心工具
- [[GitHubCopilot]] — AI 推理引擎
- [[LLMWikiPattern]] — 核心知识库模式
- [[ContextOS]] — 知识库作为 AI Coding 的上下文操作系统
- [[摘要-obsidian-context-os]] — 前篇：为什么选 Obsidian
