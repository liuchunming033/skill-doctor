---
title: "Trace"
type: concept
tags: [Agent评估, 可观测性, 数据结构]
created: 2026-06-21
updated: 2026-06-21
sources: [摘要-demystifying-evals-for-ai-agents, 摘要-evaluate-agent-workflows-openai-api, 摘要-ai-agent-skill-测评方案及落地实践]
related: [AgentEvaluation, EvalHarness, BaselineBasedEvaluation]
---

## 定义
Trace（执行轨迹 / 转录本 / Trajectory）是 Agent 执行过程中产生的结构化日志，记录了每一步的工具调用、参数、返回值和思考过程，类似于程序调试中的"调用栈记录"。在 Anthropic API 中即评估运行结束时的完整 messages 数组。

## Trace 包含的内容

- 模型调用记录
- 工具调用（名称、入参、返回值）
- 思维链 / 推理过程
- 中间产物
- 时间戳
- Token 消耗

## Trace 在评估中的核心地位

Trace 是 Agent 评估的**基础数据源**，几乎所有过程评分都依赖它：

- **工具调用检查**：是否调用了正确工具、参数是否正确
- **步骤对比**：使用 LCS（最长公共子序列）算法对齐基线 Trace 与当前 Trace
- **效率统计**：工具调用次数、Token 消耗、端到端延迟
- **思维链评估**：推理是否自洽

## Trace 的结构化输出要求

- 格式：JSONL / JSON，每行独立解析
- 字段：工具名称、入参、返回值、时间戳（至少），思维链（理想）
- 稳定性：字段命名和结构在版本间保持一致

示例（CodeBuddy-Code 的 `-p` 模式）：
```jsonl
{"type":"tool_call","name":"read_file","params":{"path":"src/main.ts"},"timestamp":"..."}
{"type":"tool_result","name":"read_file","result":"...","timestamp":"..."}
{"type":"thinking","content":"文件结构清晰...","timestamp":"..."}
```

## 如果 Agent 不支持结构化 Trace？

| 情况 | 策略 |
|------|------|
| 有日志但非结构化 | 编写解析器提取（成本高、易碎） |
| 仅有最终输出 | 只能做结果评测，放弃过程评测 |
| 可改造 | 推动 Agent 增加 Trace 输出（推荐） |

## 关联连接
- [[AgentEvaluation]] — Agent 评估总论
- [[EvalHarness]] — 评估框架
- [[BaselineBasedEvaluation]] — 基线评估方法
