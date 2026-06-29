---
title: "LLMWikiPattern"
type: concept
tags: [方法论, 知识管理, LLM, 持久记忆]
sources:
  [
    raw/01-articles/为什么当下大家采用Obsidian作为AICoding的ContextOS.md,
    raw/01-articles/20分钟搭建AI驱动的产品知识库.md,
  ]
last_updated: 2026-06-05
---

## 定义

LLM-Wiki 模式是 Andrej Karpathy 提出的一种 AI 辅助知识管理范式：由 LLM 负责维护一个持续增长、高度互联的 Obsidian Wiki，人类负责投喂原始素材并做最终决策评审。其核心价值是将碎片化的信息转化为可复用、可检索、可复合推理的"编译型知识资产"。

## 工作原理

```
原始素材 (raw/) → [LLM 编译] → 结构化 Wiki (wiki/)
                                      ↑
                              (人类查询 / 评审 / 追加)
```

**三层分工：**

- **Raw 层（不可变）**：人类投喂原始素材，LLM 只读
- **Wiki 层（LLM 维护）**：LLM 全权维护结构化知识，提炼、消歧、建立双链
- **Query 层（人机协作）**：人提问，LLM 从 wiki 检索并合成答案，引用来源

## 核心机制

1. **Ingest（摄取）**：将 raw 素材提炼为 wiki 页面，创建双链，归档源文件
2. **Query（查询）**：优先从 wiki 读取，禁止凭模型记忆回答
3. **Lint（维护）**：定期检查孤儿页、死链、知识冲突
4. **Compounding（复利）**：每次 ingest 都让 wiki 更完整，答案质量逐步提升

## 与传统笔记的区别

| 维度     | 传统笔记   | LLM-Wiki 模式          |
| -------- | ---------- | ---------------------- |
| 维护者   | 人类       | LLM                    |
| 结构     | 主观、碎片 | 强制 Schema + 双链网络 |
| 检索     | 关键词搜索 | LLM 语义合成           |
| 知识复利 | 线性积累   | 指数级网络效应         |
| 人的角色 | 记录者     | 决策者 + 投喂者        |

## 知识筛选原则（Half-life × Synthesis Value）

适合 ingest 的知识：

- 半衰期长（不会很快过时）
- 合成价值高（跨多条知识整合后能产生新洞察）

**避免 ingest 的内容**：状态信息、操作流水账、会在1周内变化的数据

## 关联连接

- [[Obsidian]] — 最适合承载 LLM-Wiki 的工具
- [[ContextOS]] — LLM-Wiki 是 ContextOS 的实现机制之一
- [[摘要-obsidian-context-os]] — 详细论述为何 Obsidian 是最佳载体
- [[摘要-20min-ai-knowledge-base]] — 实操搭建 LLM-Wiki 的步骤指南
- [[摘要-software30-context-kb-project]] — 企业级 LLM-Wiki 建设专项
