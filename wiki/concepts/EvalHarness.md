---
title: "EvalHarness"
type: concept
tags: [Agent评估, 基础设施, 工程]
created: 2026-06-21
updated: 2026-06-23
sources: [摘要-demystifying-evals-for-ai-agents, 摘要-ai-agent-skill-测评方案及落地实践, 摘要-agent-evaluation-a-detailed-guide, 摘要-解读-anthropic-demystifying-evals, 摘要-ai评测ai-智能客服运营agent]
related: [AgentEvaluation, GraderTypes, BaselineBasedEvaluation, AutoEvalAgent]
---

## 定义
评估框架（Eval Harness）是端到端运行 Agent 评估的基础设施，负责提供指令和工具、并发运行任务、记录所有步骤、评分输出并聚合结果。

## 核心要求

### 环境隔离

- 每次试验从干净环境启动
- 避免共享状态（残留文件、缓存数据、资源耗尽）导致关联失败
- **常见陷阱**：
  - **git 历史残留**：Agent 通过读取之前试验留下的 git 历史"作弊"，成绩虚高
  - **资源未释放**：内存耗尽等导致多个试验连环失败，看似 Agent 问题实则是环境撑不住
  - **文件残留**：上次试验的临时文件、数据库记录被本次 Agent 读取利用
- 例如：Claude 在内部评估中曾通过检查 git 历史获得不公平优势

### Agent 框架（Agent Harness / Scaffold）

使模型作为 Agent 行动的系统：处理输入、编排工具调用、返回结果。

**Agent Harness vs 普通 LLM Harness**：

| 特性 | 普通 LLM Harness | Agent Harness |
|------|-----------------|---------------|
| **交互模式** | 单次请求-响应 | 多轮循环（观察→思考→行动） |
| **环境状态** | 无状态或简单上下文 | 复杂状态管理（工具结果持久化） |
| **执行终止** | 模型输出即结束 | 需判断何时停止（任务完成/最大轮数/错误） |
| **副作用处理** | 通常无 | 必须管理（模拟/回滚/隔离） |
| **错误传播** | 单次错误即结束 | 错误可在多轮中传播累积 |

评估时评估的是"框架 + 模型"的组合，而非单独模型。同一模型在不同 Agent 框架下表现可能差异显著。

### Trace 输出能力
- 被测 Agent 必须输出结构化执行轨迹（如 JSONL 格式）
- 包含：工具名称、入参、返回值、时间戳、思维链
- 如果 Agent 只输出最终回答而无可解析中间过程，则只能做结果评估

## 主流开源/商业框架

| 框架 | 特点 |
|------|------|
| **Harbor** | 容器化环境中运行 Agent，标准化任务和评分器格式，Terminal-Bench 2.0 通过其发布 |
| **Braintrust** | 离线评估 + 生产可观测性 + 实验跟踪，内置 autoevals 评分器库 |
| **DeepEval** | 通过 @observe 装饰器进行 Trace 驱动的评估，支持 CI/CD 集成 |
| **LangSmith** | 追踪、离线/在线评估、数据集管理，深度集成 LangChain 生态 |
| **Langfuse** | 自托管开源替代方案，适合有数据驻留要求的团队 |
| **Arize Phoenix** | 开源 LLM 追踪、调试和评估平台 |

## 长时间运行任务的可靠性

### Checkpoint 中断恢复机制

Agent 评测任务通常是长时间运行的任务，每项任务包含大量服务记录，每条记录又包含多个阶段的 LLM 调用（BadCase 识别→根因归类→优化建议生成）。服务重启或异常中断会导致任务失败，重新从头运行浪费大量 Token。

**核心设计**：
- 每个阶段执行时，每条服务记录上报心跳更新任务最新状态
- 定时任务轮询超期任务，识别中断
- 中断恢复时按当前阶段续跑，而非从"初始化阶段"开始
- 避免频繁扫表（DB），通过心跳机制被动感知中断

### 并发与限流管理

大规模并发调用 LLM 时需应对两类限流：
- **QPM（每分钟请求数）**：通过控制线程并发数解决
- **TPM（每分钟 Token 数）**：输入 Token + 思考过程输出 Token 都计入，可通过 max_tokens 参数限制输出

注意：高并发即使未达限流阈值也会显著降低 LLM 响应速度（可达几十秒）。

## 关联连接
- [[AgentEvaluation]] — Agent 评估总论
- [[GraderTypes]] — 三类评分器
- [[Trace]] — 执行轨迹
- [[DeepEval]] — 评估框架
