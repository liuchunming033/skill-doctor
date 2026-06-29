> 学习目标：理解为什么必须有 Trace、需要记录哪四类数据，并能用 Langfuse 完整走完从安装到在平台上看到 Trace 的全流程——包括 `@observe` 装饰器和 LangChain Callback 两种接入方式，以及按实际场景选型框架。

---

## 引言

评分器告诉你 Agent 打了 85 分，但你不知道它在路上绕了多少圈、有没有差点调错接口。结果分数无法告诉你过程发生了什么。**没有 Trace，你的评估建在沙滩上。**

---

## 为什么必须有 Trace

三个具体场景，说明没有 Trace 时你看不到什么：

1. **同一个问题，三次结果不一致**：你只有输出，不知道是哪一步的工具调用出了岔子，还是 LLM 本身的随机性。无法定位，也无法修复。

2. **平均延迟突然升高**：日志只有总时长，你不知道瓶颈在 LLM 调用还是外部 API，更不知道是哪个 Span 拖慢了整条链路。

3. **Token 消耗超预期**：没有 Trace，你不知道哪个步骤在反复重试、哪个 prompt 过长——只能猜。

**Trace 的价值：让每一次 Agent 运行都变成可回放、可分析的数据，而不是一次性的黑盒执行。**

---

## 可观测性需要记什么

四类数据，缺一类就会有盲区：

| 数据类型 | 具体内容 | 最容易缺失的原因 |
|---------|---------|----------------|
| **LLM 调用** | 输入 prompt、输出内容、token 用量、耗时 | 框架默认就会记，很少缺 |
| **工具调用** | 函数名、入参、返回值、耗时 | **最容易缺失**——需要手动埋点，很多团队忘记 |
| **Trace 元数据** | user_id、session_id、环境标签 | 开发时不加，上线后查问题找不到上下文 |
| **错误与重试** | 异常类型、重试次数、失败原因 | 只记成功路径，失败路径一片空白 |

**工具调用是最容易缺失的那类。** LLM 调用通常由框架自动记录，但工具调用（查数据库、调 API、写文件）需要主动埋点，一旦漏掉，Trace 就出现断层——你只看到 LLM 给了指令，不知道工具实际执行了什么。

---

## Langfuse 完整采集流程

### Step 1：安装与初始化

```bash
pip install langfuse openai
```

```python
import os
os.environ["LANGFUSE_PUBLIC_KEY"] = "pk-lf-..."
os.environ["LANGFUSE_SECRET_KEY"] = "sk-lf-..."
os.environ["LANGFUSE_HOST"] = "https://cloud.langfuse.com"  # 或自部署地址
```

初始化会自动读取环境变量，后续无需重复传参。

---

### Step 2：自动追踪 LLM 调用（替换 import）

Langfuse 提供 OpenAI 的 drop-in 替换，**一行换掉 import，所有 LLM 调用自动记录**，无需修改调用代码：

```python
# 原来
from openai import OpenAI

# 替换为
from langfuse.openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "查询订单 12345 的物流状态"}],
)
# 这次调用的 prompt、输出、token 用量、耗时，自动出现在 Langfuse 平台
```

---

### Step 3：用 `@observe` 装饰器标记工具调用（推荐方式）

`@observe` 是 Langfuse 最推荐的接入方式。**给函数加一行装饰器，Langfuse 自动为它创建 Span，并将它挂到当前 Trace 下**——不需要手写 `langfuse.trace()` 或 `langfuse.span()`：

```python
from langfuse.decorators import observe, langfuse_context

@observe()  # 标记为一个 Span，自动记录入参、返回值、耗时
def query_logistics(order_id: str) -> dict:
    # 实际的 API 调用或数据库查询
    result = external_api.get_logistics(order_id)
    return result

@observe()  # 整个 Agent 运行作为顶层 Trace
def run_agent(user_query: str) -> str:
    # Step 1: LLM 分析意图（已由 Step 2 自动追踪）
    intent = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": user_query}],
    )
    order_id = extract_order_id(intent)

    # Step 2: 调用工具（@observe 自动记录这个 Span）
    logistics_info = query_logistics(order_id)

    # Step 3: 生成回复（已自动追踪）
    reply = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": f"物流信息：{logistics_info}，请生成客服回复"}],
    )
    return reply.choices[0].message.content
```

装饰器会自动处理嵌套关系：外层函数的 `@observe` 创建 Trace，内层函数的 `@observe` 创建子 Span，层级结构自动正确。

> 如果需要手动附加元数据（如 user_id、session_id），可以在函数内调用：
> ```python
> langfuse_context.update_current_trace(user_id="u_123", session_id="sess_456")
> ```

---

### Step 4：LangChain 框架级方案（Callback Handler）

如果你的 Agent 基于 LangChain，用 Callback Handler 在框架层统一接入，**无需逐个函数加装饰器**：

```python
from langfuse.callback import CallbackHandler

handler = CallbackHandler()

# 在 chain 或 agent 的 invoke/run 时传入
result = chain.invoke(
    {"input": "查询订单 12345 的物流状态"},
    config={"callbacks": [handler]},
)
```

Handler 会自动捕获：LLM 调用的输入输出、Chain 的每个节点、Tool 的调用入参和返回值。

---

### Step 5：平台上你会看到什么

接入完成后，在 Langfuse 平台打开任意一条 Trace，你会看到：

```
Trace: run_agent（总耗时 1948ms）
├── GENERATION: 意图识别（耗时 891ms，input_tokens: 120, output_tokens: 15）
├── SPAN: query_logistics（耗时 423ms，input: {order_id: "12345"}, output: {status: "运输中"}）
└── GENERATION: 生成回复（耗时 634ms，input_tokens: 224, output_tokens: 35）
```

每个节点可以点开看完整的 prompt、返回值和 token 明细。这就是 Ch22 解析和风险分析的数据来源。

---

## 框架选型：按场景给建议

不同情况下推荐不同方案，不要一刀切：

**刚起步、没有固定框架**
→ 直接用 Langfuse + `@observe` 装饰器。接入成本最低，一个装饰器搞定，平台 UI 直观，适合快速建立可观测性基础。
→ 局限：只在 Langfuse 生态内，如果将来迁移到其他平台需要改代码。

**已经在用 LangChain**
→ 用 Langfuse Callback Handler。框架层统一接入，不需要改业务代码，Chain 和 Agent 的所有节点自动记录。
→ 局限：Tool 的内部细节（如外部 API 的请求体）需要额外在 Tool 定义里埋点。

**有 RAG 管道，需要追踪检索质量**
→ 用 Langfuse 的 `@observe` + 手动记录检索结果（召回的文档块、相关性分数）作为 Span 的 output，或者考虑 Ragas（专门做 RAG 评估）搭配 Langfuse 一起用。
→ 局限：Ragas 不做通用 Trace 存储，只做指标计算，两者角色不同。

**已有 OpenTelemetry（OTel）基础设施**
→ Langfuse 支持 OTel 协议接入，直接复用现有 Collector，不需要单独部署 Langfuse SDK。
→ 局限：LLM 专属字段（token 用量、模型名称）需要自定义 attribute，配置略复杂。

**数据不能出内网**
→ 自部署 Langfuse（Docker Compose 或 Kubernetes），数据完全在本地。`LANGFUSE_HOST` 指向内网地址，其他代码不需要改。
→ 局限：需要自己维护服务，包括更新和备份。

---

## 🎯 本节核心观点

- **四类数据必须都有**：LLM 调用、工具调用、Trace 元数据、错误与重试——工具调用最容易漏，优先保证它有埋点。
- **`@observe` 是首选**：一行装饰器，自动建立 Trace/Span 层级，比手写 `langfuse.trace()` 简洁得多。
- **LangChain 用 Callback**：框架级接入，业务代码零改动。
- **框架选型看场景**：没有最好的，只有最合适当前约束的。

---

## 实操

**第一步**：在你的 Agent 里安装 Langfuse，替换 OpenAI import，跑一次，打开 Langfuse 平台确认 LLM 调用已经出现在 Trace 列表里。

**第二步**：找出你的 Agent 里最重要的一个工具调用函数，加上 `@observe()` 装饰器，再跑一次，确认 Trace 里出现了对应的 Span（包含入参和返回值）。

**第三步**：打开那条 Trace，记录下：总耗时是多少、LLM 调用了几次、工具调用了几次——这三个数字就是 Ch22 分析的起点。

---

## 下节预告

Trace 有了。Ch22 解决 Trace 到手之后怎么用：三层分析框架（表面层/效率层/风险层），用代码自动提取统计指标，并检测工具循环、空参数、超时等风险行为。
