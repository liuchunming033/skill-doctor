
> 学习目标：掌握 Trace 分析的三个层次（表面层/效率层/风险层），学会用代码自动提取 Trace 统计指标、检测风险行为——让 Trace 真正成为可以驱动决策的评估数据。

---

## 引言

Ch21 解决了 Trace 怎么来的问题。这章解决 Trace 到手之后怎么用。

评分器告诉你 Agent 拿了 85 分。你看一眼 Trace——第三步差点删库，第五步绕了 10 个圈子才找到答案。这 85 分的水分有多大？

结果分数告诉你 Agent 最终给出了什么，但无法告诉你 Agent 在路上做了什么。而"路上做了什么"，往往才是真正决定可不可以发布的信息。

---

## 💡 Trace 分析三个层次

拿到一条 Trace，按三个层次检查：

| 层次 | 检查内容 | 对应代码指标 |
|------|---------|------------|
| **表面层** | 工具调用序列对不对？参数有没有传错？ | `execution_chain`、`empty_tool_input` |
| **效率层** | 有没有绕路？有没有反复调同一个 API？Token 消耗是否合理？ | `tool_call_count`、`tool_loop`、`total_tokens` |
| **风险层** | 有没有在用户未确认时发起不可逆操作？有没有访问权限外的数据？ | `llm_slow_call`、`too_many_steps`、`has_critical_risk` |

**风险层是最重要也最容易被评分器漏掉的部分。** 评分器能判断输出内容质量，但识别不了"API 超时后直接跳退款"这种过程风险。

---

## 🔍 用代码读懂 Trace：通用解析方法

下面是一个通用解析函数，直接读取 Langfuse Trace 对象，自动提取所有关键统计指标，兼容 `@observe` 装饰器和 LangChain Callback 两种埋点方式。

```python
from langfuse import Langfuse


def _latency(obs) -> int | None:
    """计算单个 Observation 的耗时（毫秒）"""
    if obs.start_time and obs.end_time:
        return round((obs.end_time - obs.start_time).total_seconds() * 1000)
    return None


def parse_trace(trace_id: str) -> dict:
    """
    通用 Trace 解析函数
    兼容 @observe 装饰器与 LangChain Callback 两种埋点方式
    """
    lf = Langfuse()
    trace = lf.get_trace(trace_id)
    observations = trace.observations  # 所有 Span + Generation

    # 按类型分组
    generations = [o for o in observations if o.type == "GENERATION"]
    spans       = [o for o in observations if o.type == "SPAN"]

    # ── LLM 调用统计 ──
    llm_latencies = []
    total_input_tokens = 0
    total_output_tokens = 0

    for gen in generations:
        llm_latencies.append({"name": gen.name, "latency_ms": _latency(gen)})
        if gen.usage:
            total_input_tokens  += getattr(gen.usage, "input",  0) or 0
            total_output_tokens += getattr(gen.usage, "output", 0) or 0

    # ── Tool 调用统计 ──
    tool_latencies = [
        {"name": span.name, "latency_ms": _latency(span)}
        for span in spans
    ]

    # ── Trace 整体耗时 ──
    timed = [o for o in observations if o.start_time and o.end_time]
    trace_latency_ms = None
    if timed:
        earliest = min(o.start_time for o in timed)
        latest   = max(o.end_time   for o in timed)
        trace_latency_ms = round((latest - earliest).total_seconds() * 1000)

    # ── 调用链路顺序（按 start_time 排序）──
    sorted_obs = sorted(
        [o for o in observations if o.start_time],
        key=lambda o: o.start_time,
    )
    execution_chain = [
        {"step": i + 1, "type": o.type, "name": o.name}
        for i, o in enumerate(sorted_obs)
    ]

    return {
        "trace_id":            trace_id,
        "llm_call_count":      len(generations),
        "tool_call_count":     len(spans),
        "llm_latencies":       llm_latencies,
        "tool_latencies":      tool_latencies,
        "trace_latency_ms":    trace_latency_ms,
        "total_input_tokens":  total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "total_tokens":        total_input_tokens + total_output_tokens,
        "execution_chain":     execution_chain,
    }
```

一条典型的客服 Agent Trace 解析后输出：

```python
{
  "trace_id": "abc123",
  "llm_call_count": 2,
  "tool_call_count": 1,
  "llm_latencies":  [
    {"name": "意图识别", "latency_ms": 891},
    {"name": "生成回复", "latency_ms": 634}
  ],
  "tool_latencies": [
    {"name": "query_logistics", "latency_ms": 423}
  ],
  "trace_latency_ms":    1948,
  "total_input_tokens":  344,
  "total_output_tokens":  50,
  "total_tokens":        394,
  "execution_chain": [
    {"step": 1, "type": "GENERATION", "name": "意图识别"},
    {"step": 2, "type": "SPAN",       "name": "query_logistics"},
    {"step": 3, "type": "GENERATION", "name": "生成回复"}
  ]
}
```

---

## 🚨 风险规则定义与自动检测

有了结构化的 Trace 数据，就可以用规则自动检测风险。下面定义四条核心风险规则，对应三层分析框架的效率层和风险层。

### 四条风险规则

| 规则 | 触发条件 | 严重级别 | 对应层次 |
|------|---------|---------|---------|
| `llm_slow_call` | 单次 Generation > 3000ms | WARNING | 风险层 |
| `tool_loop` | 同一 tool 连续调用 ≥2 次 | ERROR | 效率层 + 风险层 |
| `too_many_steps` | 单次 Trace 工具调用 ≥6 次 | WARNING | 效率层 |
| `empty_tool_input` | 工具 input 为空 | WARNING | 表面层 |

### 完整增强版解析函数

```python
RISK_RULES = {
    "llm_slow_call":    {"threshold_ms": 3000, "severity": "WARNING"},
    "tool_loop":        {"min_repeat": 2,       "severity": "ERROR"},
    "too_many_steps":   {"max_tool_calls": 6,   "severity": "WARNING"},
    "empty_tool_input": {                       "severity": "WARNING"},
}


def detect_risks(stats: dict, observations: list) -> list[dict]:
    risks = []

    # 规则 1：LLM 单次超时
    for llm in stats["llm_latencies"]:
        if llm["latency_ms"] and llm["latency_ms"] > RISK_RULES["llm_slow_call"]["threshold_ms"]:
            risks.append({
                "rule":     "llm_slow_call",
                "severity": "WARNING",
                "detail":   f"LLM '{llm['name']}' 单次耗时 {llm['latency_ms']}ms，超过 3000ms 阈值",
            })

    # 规则 2：工具循环调用（同一 tool 连续 ≥2 次）
    tool_seq = [
        o.name for o in sorted(observations, key=lambda o: o.start_time or 0)
        if o.type == "SPAN" and o.start_time
    ]
    for i in range(len(tool_seq) - 1):
        if tool_seq[i] == tool_seq[i + 1]:
            risks.append({
                "rule":     "tool_loop",
                "severity": "ERROR",
                "detail":   f"工具 '{tool_seq[i]}' 连续被调用 ≥2 次，Agent 可能陷入死循环",
            })
            break  # 一条 Trace 只报一次

    # 规则 3：总步骤过多
    if stats["tool_call_count"] >= RISK_RULES["too_many_steps"]["max_tool_calls"]:
        risks.append({
            "rule":     "too_many_steps",
            "severity": "WARNING",
            "detail":   f"工具调用 {stats['tool_call_count']} 次，≥6 次通常意味着 Agent 思维发散",
        })

    # 规则 4：空工具参数
    for obs in observations:
        if obs.type == "SPAN" and not obs.input:
            risks.append({
                "rule":     "empty_tool_input",
                "severity": "WARNING",
                "detail":   f"工具 '{obs.name}' 调用时 input 为空，可能是参数提取失败",
            })

    return risks


def parse_trace_with_risks(trace_id: str) -> dict:
    """
    增强版：解析 + 风险检测一步完成
    兼容 @observe 装饰器与 LangChain Callback 两种埋点方式
    """
    lf = Langfuse()
    trace = lf.get_trace(trace_id)
    observations = trace.observations

    stats = parse_trace(trace_id)
    risks = detect_risks(stats, observations)

    return {
        **stats,
        "risks":             risks,
        "has_critical_risk": any(r["severity"] == "ERROR" for r in risks),
    }
```

### 使用示例

```python
result = parse_trace_with_risks("trace_id_here")

if result["has_critical_risk"]:
    print("⚠️  发现高危风险，需要人工复查")
    for r in result["risks"]:
        if r["severity"] == "ERROR":
            print(f"  [{r['rule']}] {r['detail']}")

# 典型输出（发现工具循环）：
# ⚠️  发现高危风险，需要人工复查
#   [tool_loop] 工具 'query_logistics' 连续被调用 ≥2 次，Agent 可能陷入死循环
```

> `parse_trace` 负责数据提取，`detect_risks` 负责规则判断，两者解耦。后续新增规则，只扩展 `detect_risks` 即可，不影响解析逻辑。

---

## 🎯 本节核心观点

**三层分析对应三类指标：**
- 表面层 → `execution_chain`、`empty_tool_input`：调用序列和参数是否正确
- 效率层 → `tool_call_count`、`tool_loop`、`total_tokens`：有没有绕路和循环
- 风险层 → `llm_slow_call`、`too_many_steps`、`has_critical_risk`：有没有危险行为

**两个函数，职责分明：**
- `parse_trace`：提取 7 项统计数据，是后续所有分析的原材料
- `parse_trace_with_risks`：解析 + 4 条规则检测一步完成，`has_critical_risk=True` 即触发人工复查

**评分器告诉你结果，Trace 告诉你过程。两者都不看，你是瞎子；只看结果，你是独眼龙。**

---

## 实操

用 Ch21 接入 Langfuse 后采集到的 Trace，完成以下验证：

**第一步**：用 `parse_trace` 跑一遍，检查 `execution_chain` 的顺序是否符合预期，`total_tokens` 是否在合理范围。

**第二步**：用 `parse_trace_with_risks` 跑一遍，看有没有规则触发。如果有 WARNING，结合 Trace 判断是真实问题还是阈值需要调整。

**第三步**：如果发现 `has_critical_risk=True`，打开 Langfuse 平台上对应的 Trace，定位是哪一步触发了规则，写一句话："风险发生在 Step __ 的 __ 环节，原因是 __。"

---

## 下节预告

Trace 读完了，基线建好了，用例设计清楚了，评测集也有了。前面 21 章把工程方法全铺开了。如果今天是 Day 1，第一步做什么？Anthropic 团队走过的 8 步，是你最短的上手路径。
