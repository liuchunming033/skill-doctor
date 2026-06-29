---
title: "CognitionExecutionSeparation"
type: concept
tags: [概念, Agent, 架构]
sources: [raw/01-articles/02-无限上下文？Skill渐进式披露机制——精读《Equipping agents for the real world with Agent Skills》②.md]
last_updated: 2026-06-17
---

## 定义

认知与执行分离（Cognition-Execution Separation）是 Agent Skill 的核心架构思想，指模型的思考空间（认知空间）与任务执行空间（执行空间）物理分离。认知空间只包含推理所需的文字信息，执行空间在虚拟机中处理外部文件、脚本和数据，通过工具调用连接两个空间。

## 核心原理

### 认知空间（上下文窗口）

- **内容**：模型推理所需的文字信息
  - Level 1 的所有技能元数据
  - 被触发技能的部分 Level 2 内容
  - 执行结果（脚本输出、文件读取结果）
- **特点**：体量小，直接加载进上下文窗口
- **限制**：受模型上下文窗口大小限制

### 执行空间（文件系统+执行工具）

- **内容**：所有外部文件、脚本和数据
  - 脚本文件（如 `.py`）
  - 配置文件（如 `.json`）
  - 文档文件（如 `.md`）
- **特点**：体量可无限扩展，不受上下文窗口限制
- **执行方式**：Claude 通过工具调用（如 `run bash command`）操作执行空间

## 关键机制

### 脚本执行的分离

**例子**：PDF Skill 指令要求运行 `scripts/extract_fields.py`

1. **认知空间**：Claude 读取 SOP 指令"请运行 scripts/extract_fields.py"
2. **工具调用**：Claude 发出 `run bash command: python scripts/extract_fields.py`
3. **执行空间**：虚拟机运行脚本（5000 行 Python 代码）
4. **结果返回**：虚拟机返回简短结果"字段提取完成，已保存为 forms.json"
5. **认知空间**：上下文只看到执行结果，不承担脚本代码本身

### 外部化执行的价值

原文引用：
> "Agents with a file system and code execution tools don't need to read the entirety of a skill into their context window. The amount of context that can be bundled into a skill is effectively unbounded."

**核心思想**：模型并不扩大上下文窗口，而是通过外部化执行，让技能包的体积与上下文无关。

## 确定性与效率

### 外部脚本的优势

- **确定性**：排序、提取、数学运算等任务，脚本执行结果可重复验证
- **效率**：比 LLM 生成代码更快、成本更低
- **可复现性**：相同输入必定产生相同输出

### Skill 的价值

Skill 不仅让 Claude 知道怎么做（SOP），还确保每次都能做对（确定性脚本）。

## 类比理解

### 类比操作系统

- **认知空间** = 内存（RAM）：存储正在运行的程序和活动数据
- **执行空间** = 硬盘 + CPU：存储所有程序和数据，执行计算任务
- **工具调用** = 系统调用：程序通过系统调用操作硬盘和 CPU

### 类比人脑

- **认知空间** = 工作记忆：处理当前任务所需的信息
- **执行空间** = 外部工具和文档：计算器、参考手册、数据库
- **工具调用** = 查阅文档或使用计算器：把复杂计算外包给外部工具

## 架构价值

### 突破上下文限制

- **传统方式**：所有内容必须进入上下文窗口
- **认知执行分离**：只有思考所需内容进入上下文，执行在外部进行

### 实现无限扩展

- **理论上无限**：技能包可以包含任意大小的脚本、数据、文档
- **上下文无关**：技能包体积不影响上下文窗口占用

## 关联连接

- [[摘要-skill-anthropic-doc-part2]] — 认知与执行分离概念来源
- [[AgentSkill]] — 认知与执行分离的应用场景
- [[ProgressiveDisclosure]] — 依赖认知执行分离实现的加载机制
- [[DynamicLoading]] — 认知执行分离的动态调用机制