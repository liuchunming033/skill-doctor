---
title: "EvalDatasetEngineering"
type: concept
tags: [Agent评估, 数据集, 效果工程]
created: 2026-06-23
updated: 2026-06-24
sources: [摘要-评测集工程, 摘要-评测集生产pipeline设计]
related: [AgentEvaluation, EvaluationStrategy, HuggingFace, AdversarialGT, RAGEvaluation]
---

## 定义
评测集工程（Evaluation Dataset Engineering）是 AI 效果工程的核心基础设施，涵盖评测集的构建、质量保障和维护管理。其核心原则：**评测集质量决定评测质量（Garbage in, garbage out）**。在 Agent 场景中，评测集不仅需覆盖模型能力，还需覆盖真实业务场景、多步骤推理、工具调用、RAG 问答和异常输入场景。

## 高质量评测集的四项要求

| 要求 | 说明 |
|------|------|
| **高质量问题** | 表达清晰、可判断好坏、能区分模型能力差异、避免无意义或过于简单 |
| **业务真实数据** | 来源于用户真实问题、历史工单、客服对话记录、搜索日志、API 调用记录 |
| **多样性覆盖** | 简单/复杂、单轮/多轮、单工具/多工具、标准/边界、正常/异常输入 |
| **无歧义表达** | 问题目标明确、含充分上下文、评价标准一致 |

## 构建方法

| 方法 | 数据来源 | 优点 | 缺点 |
|------|---------|------|------|
| **人工构造** | 领域专家手工编写 | 质量高、可控性强、可设计复杂场景 | 成本高、构建速度慢 |
| **日志挖掘** | 用户对话、搜索日志、客服工单、API 记录 | 真实场景、覆盖长尾问题 | 需数据清洗和脱敏、可能含噪声 |
| **数据增强** | 同义改写、表达变更、上下文扩充、边界/对抗样本构造 | 提升多样性、提升鲁棒性、降低人工成本 | 需控制质量、可能引入偏差 |
| **合成数据** | 大模型基于知识库/文档/模板自动生成 | 生成速度快、快速扩展规模、覆盖长尾 | 可能存在偏差、需人工审核 |

**实践建议**：采用混合策略——人工构造 + 日志挖掘 + 数据增强 + 合成数据组合使用。

## 公开评测集

国际常用大模型评测集包括 MMLU（综合知识）、C-Eval（中文评估）、SuperCLUE 等，大部分公开数据集可从 Hugging Face 获取（huggingface.co/datasets）。

## 评测集生产 Pipeline 架构

评测集从"一次性标注产物"升级为"持续演进的工程资产"，核心理念：**多轨并行、统一 Schema、自动为主、人工兜底、可持续演进**。

```
原始文档 / 线上日志
        │
        ▼
文档标准化 & 切分
        │
        ▼
GT 生产工厂（多轨并行）
        │
        ▼
GT 质量控制与审核层
        │
        ▼
统一评测集 Schema 仓库（Dataset + Version）
```

## 六种 GT 样本类型

所有样本遵循统一 Schema，按 `gt_type` 区分：

| 类型 | 定位 | 生产方式 | 占比建议 |
|------|------|---------|---------|
| **gold** | 最高可信度锚点样本 | 业务专家/QA 人工标注，双人 review | 10-20% |
| **synthetic** | 规模化主力 | LLM 自动生成 QA + Verifier 校验 | 规模主力 |
| **evidence** | 检索专用 | 只定义正确证据，不强制标准答案 | 按需 |
| **process** | 推理步骤评测 | SOP 自动生成 / Trace 反向抽象 | 按需 |
| **adversarial** | 幻觉抑制与安全 | 5 类策略自动生成 + QC Gate | ~15% |
| **online_goodcase** | 真实分布对齐 | 线上用户正反馈回流，去模板化 | ≥30% |

## 统一评测样本 Schema

核心字段：`sample_id` / `question` / `gt_type` / `ground_truth` / `context`（最小证据集合）/ `process_gt`（推理步骤）/ `difficulty` / `source`（追溯性）/ `status`（质量状态）/ `version`

不同 GT 类型按需填充字段，便于组合评测、版本化与回溯。

## Agent 推理步骤 GT（Process GT）

Agent 推理步骤 GT 的核心目标不是"它怎么想"，而是"它做了哪些对的动作，顺序是否合理"。三种设计要素：

1. **任务分解图（TDG）**：用 DAG 定义正确路径，节点=子任务，边=前置依赖。GT = 合法拓扑序集合（不是唯一顺序）
2. **可执行中间状态**：用"状态变化"定义推理是否发生，GT = 必须被填充的状态集合
3. **工具调用约束**：`required_tools` / `optional_tools` / `forbidden_tools`

两种自动生成策略：
- **A 类（SOP → GT）**：运维 SOP / 故障排查手册 → 标题=任务，编号步骤=推理节点，前提/如果=分支
- **B 类（Trace → GT）**：线上成功 Trace → 去噪 → 聚类 → 抽象为步骤模板。高频步骤=必须步骤，错误路径=negative GT

## 对抗样本 GT（Adversarial GT）

详见 [[AdversarialGT]]。五种策略：不存在事实 / 证据缺失 / 边界模糊 / 多证据冲突 / 诱导式推断。所有 adversarial 样本统一 answer_gt 为"无法回答"，禁止生成猜测型答案。

## 线上 Goodcase 回流

线上真实用户交互中被验证为"回答效果好"的样本，是最贴近真实分布的 GT 来源。转化路径：线上 Goodcase → Context-based GT（首选）→ Weak Answer GT → Gold 候选池。关键防护：去模板化、去"模型自嗨"答案、多样性采样。

## GT 质量控制（三层 Gate）

- **Gate-1（硬门槛）**：结构合法 + 可评测性
- **Gate-2（核心质量）**：Answer ⊆ Context（NLI 校验）、Question-Document 相关性、重复检测、难度分布控制
- **Gate-3（人工兜底）**：每批 5-10% 抽样审核，重点审合成 GT、对抗样本、Goodcase

## 实施路线图（12 周）

| Epic | 周期 | 目标 |
|------|------|------|
| Epic-1 基础设施 | 第1周 | Schema 设计 + Dataset 仓库初始化 |
| Epic-2 GT 生产 | 第2-6周 | 6 种 GT 类型 Pipeline，样本量 ≥100，Goodcase ≥30% |
| Epic-3 质量控制 | 第6-8周 | 自动 QC 脚本 + 人工抽样 + 质量看板 |
| Epic-4 项目落地 | 第8-12周 | 接入 2 个真实 RAG 项目 + v1.0 冻结 |

## 关联连接
- [[AgentEvaluation]] — Agent 评估总论
- [[EvaluationStrategy]] — 评估策略
- [[HuggingFace]] — 数据集平台
- [[AdversarialGT]] — 对抗样本 GT 生成策略
- [[RAGEvaluation]] — RAG 效果评估方法
