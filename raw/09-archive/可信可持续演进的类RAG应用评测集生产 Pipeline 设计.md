# 可信可持续演进的类RAG应用评测集生产 Pipeline 设计

# 背景与目标

随着类 RAG（Retrieval\-Augmented Generation）在公司级项目中的落地，评测已成为模型选型、方案对比、持续优化的关键基础设施。其中 **评测集（Evaluation Dataset）与 Ground Truth（GT）构建方式** 是决定评测是否可信、可扩展、可持续的核心。

本设计文档目标是：

> 在一个季度内，构建一条 **支持多种 GT 方法并行、统一数据 Schema、以自动化为主、以人工为兜底** 的评测集生产 Pipeline，使评测集从“一次性标注产物”升级为“持续演进的工程资产”。
> 
> 

---

# 设计原则

1. **多轨并行（Multi\-track）**
不同评测目标（检索、生成、稳健性、Agent 行为）对应不同 GT 生产方式，避免“一种 GT 评天下”。

2. **统一 Schema（Unified Schema）**
所有样本遵循统一数据协议，便于组合评测、版本化与回溯。

3. **自动为主（Automation\-first）**
LLM \+ 规则驱动规模化生产样本，降低长期人力成本。

4. **人工兜底（Human\-in\-the\-loop）**
人工只用于高价值样本与质量校准（Gold Set、抽样审核）。

5. **可持续演进（Evolvable）**
支持从线上真实流量（goodcase / badcase）持续回流，避免评测集与业务脱节。

---

# 总体流程概览

```Plain Text
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
统一评测集Shema及仓库（Dataset + Version）
```

---

# 统一评测样本 Schema 设计

所有评测样本遵循统一 Schema，不同 GT 类型按需填充字段。

```JSON
{
  "sample_id": "uuid",
  "question": "...",
  "gt_type": "gold | synthetic | process | adversarial | online_goodcase",  //样本类型，用于权重加权
  "groud_truth": "...",
  "context": [  //最小证据集合，用于Faithfulness指标
    { "doc_id": "...", "span": "..." }  //文档或 chunk 唯一标识,支持答案的原文片段
  ],
  "process_gt": ["step1", "step2"],  //理想的推理 / 思考步骤,用于推理一致性评测，Step-wise Correctness
  "difficulty": "easy | mid | hard",
  "domain": "业务线 / 系统",  //业务线 / 系统 / 产品域
  "source": {  //GT 来源与可追溯性
    "generator": "human | llm",  //由谁生成
    "model": "gpt-4 / claude",  //使用的模型（llm适用）
  },
  "status": "draft | auto_pass | human_pass | rejected",  //当前 样本 的质量状态
  "reviewer": "xxx",  //审核人（人名或系统）
  "version": "v1.0",            // GT 版本
  "tags": ["ambiguous", "long"] // 运营 & 分析用
  "time": "YYYY-MM-DD HH:MM:SS"
}
```

# 支持的样本类型

评测样本统一 Schema中，`gt_type`，表示样本的类型，**类型**：Enum：

- `gold`：人工标注的高置信 GT

- `synthetic`：LLM 合成 GT

- `evidence`：以检索证据为核心的 GT

- `process`：包含推理/步骤的 GT

- `adversarial`：对抗 / 无答案 / 边界样本

- `online_goodcase`：线上真实 Goodcase 回流

**类型值可以用于**评测分桶、权重加权、质量门槛区分。

## `gold`：人工标注的高置信样本

> **由业务专家或 QA 人工标注、强一致性、高可信度的 Ground Truth。**
> 
> 

这是**评测体系中的“锚点样本”**，数量不必多，但**权重最高**。适用场景：

- 核心业务逻辑

- 高风险决策

- 模型方案选型的最终裁决

特点是：成本高、质量最高，常用于 **回归评测 / 质量底线。**

样本示例：

```JSON
{
  "gt_type": "gold",
  "question": "F1 MES 系统中，工单关闭的前置条件有哪些？",
  "answer_gt": "工单必须完成全部工序校验，并通过质量检查，且相关物料状态为已消耗。",
  "evidence_gt": [
    {
      "doc_id": "mes_spec_v3",
      "span": "工单关闭前，需完成全部工序校验，并通过质量检查，物料状态需为已消耗。"
    }
  ],
  "difficulty": "mid"
}
```

## `synthetic`：LLM 合成 样本

> **通过 LLM 自动生成的问题 \+ 答案 \+（可选）证据的 GT。**
> 
> 

这是**规模化评测集的主力来源**。适用场景：

- 快速覆盖知识面

- 新系统冷启动

- 回归集扩充

特点是：成本低、规模大、需要严格质量审查。

样本示例：

```JSON
{
  "gt_type": "synthetic",
  "question": "系统 A 的日志保留策略是多久？",
  "answer_gt": "系统 A 的日志默认保留 180 天。",
  "evidence_gt": [
    {
      "doc_id": "log_policy",
      "span": "系统 A 的日志保留期限为 180 天。"
    }
  ],
  "difficulty": "easy",
  "source": {
    "generator": "llm",
    "model": "gpt-4",
    "prompt_id": "syn_v2"
  }
}
```

## `evidence`：以检索证据为核心的样本

> **答案本身并不复杂，关键在于：**
> ** 系统能否“检索到正确的证据”。**
> 
> 

这是**专门用于评测 RAG 检索层**的样本。适用场景：

- 向量检索 / 混合检索对比

- Chunk 划分策略验证

特点：`evidence_gt` 是主角、答案往往是简短或引用式。

样本示例：

```JSON
{
  "gt_type": "evidence",
  "question": "文档中哪里说明了系统 B 支持多租户？",
  "answer_gt": "系统 B 支持多租户架构。",
  "evidence_gt": [
    {
      "doc_id": "system_b_arch",
      "span": "系统 B 采用多租户架构设计，支持多个租户并行运行。"
    }
  ],
  "difficulty": "easy"
}
```

## `process`：包含推理 / 步骤的 样本

> **评测的不只是“答案对不对”， 而是“推理过程是否合理”。**
> 
> 

用于评测 **多步推理 / 业务流程理解能力**。适用场景：

- 流程型问题

- 复杂决策路径

- Agent / Tool 调用

样本特点：`process_gt` 是核心，不强制模型输出相同步骤。

样本示例：

```JSON
{
  "gt_type": "process",
  "question": "当系统 C 出现接口超时时，应如何排查？",
  "process_gt": [
    "确认接口调用是否达到超时阈值",
    "检查下游服务健康状态",
    "查看网络与负载情况",
    "分析最近的变更记录"
  ],
  "difficulty": "hard"
}
```

## `adversarial`：对抗 / 无答案 / 边界样本

> **刻意设计的问题，用来测试系统在“不能答”时， 能否“不乱答”。**
> 
> 

这是**幻觉抑制与安全能力的核心评测样本，在问题本身“刻意刁难系统”的情况下，系统仍然应该做出“正确行为”的评测样本**。子类型：

- 无答案（文档中不存在）

- 诱导编造

- 边界模糊问题

这里的“**正确行为**”，**不一定是“给出答案”**，而是：

- 正确拒答

- 正确说明不知道

- 正确处理边界情况

一个标准 adversarial GT 示例：

```JSON
{
  "gt_type": "adversarial",
  "question": "系统 X 在 2025 年发生过哪些 P0 事故？",
  "answer_gt": "在当前提供的文档中，没有关于系统 X 在 2025 年发生 P0 事故的记录，因此无法回答该问题。",
  "evidence_gt": [],
  "difficulty": "mid"
}

```

## `online_goodcase`：线上真实 Goodcase 回流样本

> **来自真实线上用户交互，被验证为“回答效果好”的样本。**
> 
> 

是**最贴近真实分布的 GT 来源**。适用场景：

- 评测集“贴地气”

- 防止离线评测与线上体验脱节

样本特点：

- 来源真实

- 需脱敏 / 清洗

- 常转化为其他 GT 类型

样本示例：

```JSON
{
  "gt_type": "online_goodcase",
  "question": "系统 E 的账号被锁定后如何解锁？",
  "answer_gt": "账号被锁定后，可通过管理员在控制台进行解锁，或联系运维支持处理。",
  "evidence_gt": [
    {
      "doc_id": "account_ops",
      "span": "账号锁定后，可由管理员在控制台解锁，或提交工单联系运维。"
    }
  ],
  "difficulty": "easy",
  "source": {
    "generator": "human",
    "time": "2025-03-10"
  }
}
```

## 样本类型总结

不同 GT 类型不是为了“凑样本”，而是为了用最小的成本，覆盖模型最容易出问题的地方。

# DataSet生产方案设计

## 人工 Gold GT （少而精）

**定位**：最高可信度评测锚点（Anchor Set）
**来源**：核心业务问题、事故复盘、关键决策场景

**流程**：

1. 人工设计问题

2. 人工撰写标准答案

3. 强制绑定 context

4. 双人或抽样 review

**占比建议**：10–20%

---

## LLM 合成 GT （规模主力）

**定位**：覆盖面与规模

**流程**：

```Plain Text
Document → LLM(QA Generator)
        → LLM(QA Verifier)
        → 自动过滤
```

**产出**：Question \+ Answer \+ context

**关键控制点**：

- Answer 必须可由 context 推导

- 避免文档外常识混入

---

## Context\-based GT （检索专用）

**定位**：评测 Retriever 与 Faithfulness

**特点**：

- 只定义正确证据

- 不强制定义标准答案

**适用指标**：Recall@K、Context Precision

---

# process推理步骤GT 生成策略

## 用来评测什么？

Agent Process GT 的核心目标

> **不是“它怎么想”，**
> ** 而是：**
> ** 它“做了哪些对的动作，顺序是否合理”。**
> 
> 

## Agent 推理步骤 GT 应该包含哪些？

**应该包含① 任务分解图（Task Decomposition Graph, TDG）**

> 用**任务结构**而不是语言，定义正确路径。
> 
> 

构建方式：

- 人工 or 半自动把任务拆成 DAG

- 节点 = 子任务

- 边 = 前置依赖

```Markdown
任务：判断系统 A 是否满足上线条件

TDG:
T1: 获取系统 A 当前版本
T2: 获取版本对应的测试结果
T3: 获取上线门禁规则
T4: 对照测试结果与门禁规则

```

👉 **GT = 合法拓扑序集合（不是唯一顺序）**

**应该包含② 可执行中间状态（Executable State Transition）**

> 用“状态变化”定义推理是否发生。
> 
> 

核心思想：如果 Agent 真在推理，它一定改变了某些 **可观测状态**。

示例：

👉 **GT = 必须被填充的状态集合**

---

**应该包含③ 工具调用约束（Tool Invocation Contract）**

> 不关心它怎么想，只关心 **“用没用对工具”**。
> 
> 

```JSON
{
  "required_tools": ["search_doc", "query_release", "check_gate"],
  "optional_tools": ["summarize"],
  "forbidden_tools": ["guess"]
}
```

## Agent 推理 GT 的自动生成策略

### A 类：从 SOP / Playbook 自动生成（最强、最稳）

数据来源

- 运维 SOP

- 故障排查手册

- 发布流程文档

自动生成规则

- 标题 → 任务

- 编号步骤 → 推理节点

- “前提 / 如果” → 分支

例如，SOP 原文如下

```Markdown
1. 确认系统版本
2. 查看对应测试报告
3. 若存在 P0 问题，禁止上线
```

生成的 Agent GT是

```JSON
{
  "required_steps": ["check_version", "fetch_test_report", "evaluate_gate"],
  "dependency": {
    "fetch_test_report": ["check_version"],
    "evaluate_gate": ["fetch_test_report"]
  }
}

```

### B 类：从真实 Agent Trace 反向抽象

数据来源：

- 线上 Agent 成功任务 Trace

- 人工验收通过的执行日志

自动化流程：

```Markdown
Trace → 去噪 → 聚类 → 抽象为步骤模板
```

得到的 GT 形态：

- 高频步骤 = 必须步骤

- 低频步骤 = 可选步骤

- 错误路径 = negative GT（非常值钱）

## Agent 推理步骤 GT 的统一 Schema

```JSON
{
  "agent_task_id": "uuid",
  "task": "...",
  "gt_type": "agent_process",
  "required_steps": ["step_a", "step_b"],
  "optional_steps": ["step_c"],
  "dependency_graph": {
    "step_b": ["step_a"]
  },
  "required_states": {
    "version": "known",
    "status": "evaluated"
  },
  "tool_constraints": {
    "required": ["search", "query"],
    "forbidden": ["hallucinate"]
  }
}
```

## 评测时怎么用（非常关键）

1️⃣ Trace 对齐评分（而不是文本比对）

# adversarial GT 的自动生成策略

## 总体设计原则

1. 不是随机刁难，而是系统性覆盖失败模式

2. 生成必须基于真实知识边界（KB / Evidence）

3. 自动生成 ≠ 自动入库，必须过 QC Gate

---

## A类：不存在的事实（Non\-existent Fact）

目的是测试智能体是否会**凭空编造事实**。

生成策略：

- 从 KB 中选实体（系统 / 产品 / 人名）

- 构造 **KB 时间轴之外 / 文档中不存在的事件**

示例 Prompt（生成问题）：

```Plain Text
给定以下实体列表：
{entities}

请为每个实体生成 1 个问题，
问题应询问一个【文档中不存在的事实或事件】，
但问题本身看起来非常合理、具体。

不要生成答案。
```

典型问题：

> “系统 A 在 2026 年发生过哪些 P0 事故？”
> 
> 

---

## B 类：证据缺失（Evidence Missing）

测试智能体是否会**在没有证据时仍然给出答案**。

生成策略：

- 从现有 QA / Gold GT 出发

- **移除 supporting evidence**

- 保留问题不变

示例 Prompt：

```Plain Text
以下是一个可回答的问题及其证据：

Question:
{question}

Evidence:
{evidence}

请构造一个 adversarial 样本：
- 保持问题不变
- 移除所有可支持答案的证据
- 标注为“不可回答”
```

---

## C 类：边界模糊（Boundary / Ambiguous）

目的是：测试模型是否**过度确定**。

生成策略：

- 找到包含模糊词的文档：

    - “通常”

    - “大约”

    - “可能”

- 构造 **强确定性问法**

示例 Prompt：

```Plain Text
以下 Evidence 中包含不确定性描述：

Evidence:
{evidence}

请生成一个问题，
该问题将不确定描述转化为“是/否”或精确数值问题，
使其在证据范围内无法确定。
```

典型问题：

> “系统 B 的恢复时间是否一定是 1 小时？”
> 
> 

---

## D 类：多证据冲突（Conflicting Evidence）

目的是测试智能体是否**忽略冲突、强行给结论**。生成策略：

- 检索同一实体的 **相互矛盾文档**

- 构造需要“选边站”的问题

示例 Prompt：

```Plain Text
以下两段 Evidence 存在潜在冲突：

Evidence 1:
{evidence_1}

Evidence 2:
{evidence_2}

请生成一个问题，
该问题在当前证据下无法给出唯一确定答案。
```

---

## E 类：诱导式推断（Implicit Assumption Trap）

目的是：测试模型是否**默认用户前提是对的**。

生成策略：

- 构造问题中隐含未给定前提

- 前提在 KB 中未被证实

示例 Prompt：

```Plain Text
请生成一个问题：
- 问题中隐含一个未经证实的前提
- 该前提在现有文档中未被提及
- 问题整体看起来合理
```

典型问题：

> “系统 C 迁移到云原生架构后，性能提升了多少？”
> 
> 

---

## GT 构造规则

对所有 adversarial 样本：

```JSON
{
  "gt_type": "adversarial",
  "answer_gt": "在当前提供的资料中，无法找到支持该问题的相关信息，因此无法回答。",
  "evidence_gt": [],
  "difficulty": "mid | hard"
}
```

> ⚠️ 不允许生成“猜测型 answer\_gt”。
> 
> 

---

## 自动质量 QC Gate（必须有）

Gate\-1：不可回答性验证（LLM Judge）

- 输入：Question \+ 全量 Evidence

- 输出：unanswerable = true

Gate\-2：诱导强度检查

- 是否问题“看起来很正常”

- 是否不是明显胡扯

Gate\-3：去重 \& 多样性

- 与已有 adversarial 相似度 \< 阈值

---

## 完整自动 Pipeline

```Plain Text
知识库 / Gold GT
      ↓
adversarial 生成（5 类策略并行）
      ↓
不可回答性 Judge
      ↓
诱导强度 Judge
      ↓
去重 / 难度分级
      ↓
进入评测集（adversarial bucket）
```

## Prompt设计（Pipeline 级）

### 系统 Prompt

```Markdown
你是一个“评测集构建专家”，
专门为 RAG / 知识问答系统生成 adversarial Ground Truth 样本。

你的目标不是刁难用户，
而是构造“非常像真实用户提问，
但在当前知识范围内不应被回答”的问题。

这些问题将用于评估系统是否会：
- 编造不存在的事实
- 忽略证据缺失或冲突
- 对不确定信息给出过度确定的答案

```

### 核心Prompt

```Markdown
请基于以下 Knowledge Scope，
生成 1 条 adversarial 问题。

【生成要求】
- 问题在语言上必须自然、专业、具体
- 问题应符合真实业务用户的提问风格
- 问题不能明显胡扯或荒谬
- 在当前 Knowledge Scope 内，该问题：
  - 要么没有任何证据支持
  - 要么证据不足以得出唯一结论
  - 要么问题隐含了未被证实的前提

【禁止事项】
- 不要编造 Knowledge Scope 之外的文档内容
- 不要给出任何答案或解释
- 不要说明为什么不可回答

【输出】
仅输出「问题文本」

【补充约束】
……
```

补充约束部分，根据adversarial的5种类型设置。

1️⃣ non\_existent\_fact（不存在事实）

```Markdown
【补充约束】
问题应询问一个：
- 看起来合理
- 但在 Knowledge Scope 中完全不存在的事件、指标或结论

```

2️⃣ evidence\_missing（证据缺失）

```Markdown
【补充约束】
问题应基于 Knowledge Scope 中提到的概念，
但询问的关键信息在文档中没有直接或间接支持。

```

3️⃣ boundary\_ambiguous（边界模糊）

```Markdown
【补充约束】
问题应将 Knowledge Scope 中的
“不确定 / 模糊 / 条件性描述”
转化为“确定性结论”的询问。

```

4️⃣ conflicting\_evidence（证据冲突）

```Markdown
【补充约束】
问题应在存在潜在冲突或不一致描述的情况下，
要求给出单一、确定的答案。

```

5️⃣ implicit\_assumption（隐含前提）

```Markdown
【补充约束】
问题应隐含一个未经 Knowledge Scope 证实的前提，
但问题本身不应显式暴露该前提。

```

入库时的固定补全样本其他部分（非 Prompt）

```JSON
{
  "gt_type": "adversarial",
  "answer_gt": "在当前提供的资料中，无法找到支持该问题的相关信息，因此无法回答。",
  "evidence_gt": [],
  "review.status": "draft"
}

```

## adversarial GT 的推荐配比（经验值）

---

# 线上 Goodcase 回流 GT（真实分布对齐）

**定位**：提高系统“上限”与稳定性

1. **Goodcase 识别**

- 用户正反馈 / 无追问

- LLM Judge 判断高质量

- 无人工投诉

2. **Goodcase → GT 转化方式**

    1. **Context\-based GT（首选）**
    从线上 contexts 中抽取关键证据

    2. **Weak Answer GT**
    使用线上答案作为弱参考，仅用于回归对比

    3. **Gold 候选池**
    高频、高价值问题升级为人工 Gold GT

3. **关键防护**

- 去模板化

- 去“模型自嗨”答案

- 多样性采样

---

# GT 质量控制与审核机制

## GT QC 通用指标（所有 GT 必须具备）

## 按 GT 类型的专用指标

**QA / Answer GT**

**Evidence GT**

**Process / Reasoning GT**

**对抗 / 无答案 GT**

**线上 Goodcase 回流 GT**

## 自动QC校验（必做）

- Answer ⊆ Context（NLI / LLM）

- Question–Document 相关性

- 重复样本检测

- 难度与类型分布控制

自动 QC 分层 Gate：

```Plain Text
Gate-1（硬门槛）：结构合法 + 可评测性
Gate-2（核心质量）：Context & 正确性
Gate-3（人工兜底）：业务可信度
```

**Answer–Context 一致性**

```Plain Text
你是评测集质量审查员。
判断 Answer 是否完全可以由 Context 支持。

Question: {question}
Answer: {answer}
Context: {evidence}

请返回：
- supported: true / false
- missing_points: []
- hallucinated_points: []
```

**问题清晰度 \& 可判定性**

```Plain Text
请判断以下问题是否存在多种合理答案，或依赖未给定前提。
返回 clarity_score (1-5) 与 ambiguity_flag。

Question: {question}
```

规则化自动检查：

## 6\.2 人工抽样审核（低成本）

- 每批 5–10%

- 重点审核：合成 GT、对抗样本、goodcase

---

## GT 质量运营看板（周会可用）

### 核心指标

---

### 周会视角

- 本周新增 GT 数

- Gate\-1 / Gate\-2 拒绝原因 Top\-N

- Goodcase 回流占比

- 人工审核主要争议点

---

# 实施 Roadmap

本 Pipeline 以 **1 个季度（≈12 周）** 为交付周期，目标不是一次性“做全”，而是 **跑起来 \+ 可持续 \+ 能支撑真实项目决策**。

---

## Epic 总览

---

## Epic\-1：评测集基础设施与 Schema（第 1周）

**目标**：先解决评测样本中“装什么、怎么装”的问题。

**Stories**：

- Story 1\.1：统一评测样本 Schema 设计（支持多 GT 类型）

- Story 1\.2：评测集 Dataset 存储结构（JSON / Parquet \+ version）

- Story 1\.3：样本导入 / 导出接口（供评测工具使用）

**交付物**：

- Schema 文档 v1

- Dataset 仓库初始化（≥N 样本）

---

## Epic\-2：GT 生产能力（多轨并行）（第 2–6 周）

**目标**：让 GT 能被“持续生产”，而不是靠人堆。

**Stories**：

- Story 2\.1：LLM 合成 GT Pipeline（QA \+ Evidence）

- Story 2\.2：Evidence\-based GT Pipeline（检索专用）

- Story 2\.3：人工 Gold GT 流程与规范

- Story 2\.4：对抗样本 GT 生成（无答案 / 冲突）

- Story 2\.5：线上 Goodcase 识别与筛选

- Story 2\.6：Goodcase → Evidence / Weak GT / Gold 候选转化

**交付物**：

- GT 类型 ≥ 6 种

- 样本量 ≥ 100

- Goodcase 回流样本占比 ≥ 30%

---

## Epic\-3：GT 质量控制与审核（第 6–8 周）

**目标**：防止评测集“规模化变脏”。

**Stories**：

- Story 3\.1：自动校验规则（Answer ⊆ Evidence、相关性、去重）

- Story 3\.2：人工抽样审核机制（5–10%）

- Story 3\.3：GT 质量指标统计与看板

**交付物**：

- 自动 QC 脚本

- 每批 GT 的质量报告

---

## Epic\-4：项目化落地与运行（第 8–12 周）

**目标**：不是 Demo，而是“真的有人用”。

**Stories**：

- Story 5\.1：接入 2 个真实 RAG 项目

- Story 5\.2：评测节奏固化（周评测 / 月冻结）

- Story 5\.3：对内宣讲与使用指南

**交付物**：

- 项目评测报告 ×2

- 评测集 v1\.0 冻结版本

---

## 周粒度 Roadmap

```Plain Text
Week 1   Schema & Dataset 基础
Week 2–4   LLM 合成 + Context GT
Week 5–6   Gold / 对抗 / Goodcase 回流
Week 7–8   自动 QC + 抽样审核
Week 9–11  真实项目落地试用
Week 12    总结 & v1.0 冻结
```

---

# 资源投入

# 总结

通过“**多轨并行、统一 Schema、自动为主、人工兜底**”的评测集生产 Pipeline：

- 评测集不再是一次性标注成本，而是持续增长的质量资产；

- 评测不再只关注 badcase，而是同时覆盖真实 goodcase 分布；

- RAG 评测从“主观体验”升级为“工程化、可复现、可对比”的决策依据。

