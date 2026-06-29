
先说结论：它不是“LLM 在浏览器里瞎点”，而是一个“Spec 驱动 + Playwright 执行 + LLM 评审”的双阶段 QA 流水线。 真正执行交互的是 Playwright；LLM 负责读上下文、生成/选择测试场景、解释失败并形成 QA 报告。

superpowers

整体流程

### 1. `/qa` 启动时读什么

从仓库里的技能描述和前面 `/office-hours`、`/autoplan` 的设计看，`/qa` 会优先读取这些持久化产物：

|来源|作用|
|---|---|
|~/.gstack/projects//...design*.md|产品/设计意图（需求、边界、风险）|
|test-plan.md（若存在）|已有测试计划与场景|
|当前 Git diff / 分支|确定本次变更影响范围|
|应用 URL / 启动命令（环境配置）|知道测试目标站点在哪里|

这一步的目标是把 “要验证什么” 明确下来，而不是一上来生成脚本。仓库中多处都强调产物落在 `~/.gstack/projects/<slug>`，供后续阶段复用。

superpowers

### 2. 测试场景是怎么来的

有两种模式：

|模式|什么时候用|成本|
|---|---|---|
|Plan-first（推荐）|已有 test-plan.md 或历史 QA 资产|低 Token：复用场景，只做映射与增量补充|
|Agent-first（兜底）|没有测试计划，或需求发生较大变化|高 Token：重新推导场景与步骤|

你前面担心的 “每次都 LLM 生成脚本很费 Token”，主要发生在第二种模式。合理落地会把首次生成的测试计划和 Playwright 资产缓存起来，后续复用。

### 3. 真正执行的是 Playwright + Chromium

![7 Ways to Automate Chrome Screenshots | CaptureKit Blog](https://images.openai.com/static-rsc-4/7GdmP_9RUj6X1M6AT2NHDBu1sEtFFkNeqMpXFsXqL7ukU5zWLOPFoFORMf0k1DwnurgwP3mF0Cx4LnjkbzU9vzo9u4yy6CB1NIGU-Y9EBBj9pjBqmQw2f9Q8lPO5rCJESw5utV0FpeuUYSYbafV5xX9trUm7H9otec115Pi7byYRAqo6N_zFzyRiOj13pJvg?purpose=fullsize)

![Trace viewer | Playwright](https://images.openai.com/static-rsc-4/WTYJ1U82AC_SJCbL6h8UtCtRUhOe3J2P7pgzCdwf810dxwvA4_LVvYs5wythW47IqI3WnRnzXPuMbjN1blW7orpby5DIask8583qJsHsDFECv9CxIUFa0pyj3Eeq5O7UDwIzZZfFvm8r2ur1JN8pvbSVcKhOJopITJniXlA1080mD4sOUjyt8-eOjXeAF8o7?purpose=fullsize)

![Playwright Automation Simplified: Your 2025 End-to-End Testing Guide](https://images.openai.com/static-rsc-4/Uz-LRJ6kBbQ4z2t_SvOihVhrjlsC_-ZmFSh6BqpsQYVMG4dBoFGq6ybnv4_Mp-zArVhCosCV6UMGOIlamO_nCb-6GfKjAY_JYfvGB1j28LZY8Cb2eI_NdldiYNBHDzgYj5rBYWveVyxO5TCE5fII6bz6O7cftlJFBBWNPKKDAK6FfuJZpWE-Df0NMmWVwgfV?purpose=fullsize)

4

`/qa` 的核心执行层是 Playwright 的真实浏览器能力：

关键点：

1. 是真 Chromium，不是 jsdom。 DOM、CSS、路由、网络请求都按真实浏览器执行。
    
2. 可录制证据。 Playwright 原生支持截图、trace、视频、控制台日志、网络日志。
    
    superpowers
    
3. 可回放失败。 `trace.zip` 能在 Playwright Trace Viewer 里逐步回放。
    

### 4. LLM 在 QA 阶段到底做什么

它通常不负责低级浏览器操作，而是负责 语义验证与归因：

语义验证（把页面结果映射回 AC）

失败归因（比纯断言更像 QA 工程师）

### 5. 为什么它不是“纯 Playwright”

|传统 Playwright|Gstack `/qa` 目标|
|---|---|
|开发者手写 *.spec.ts|从 Spec/AC 自动推导场景|
|断言 DOM/URL/文本|断言 + 语义解释（是否满足需求）|
|失败输出堆栈|失败输出 QA 结论、原因、建议|
|CI 导向|Spec → Code → Validation 闭环导向|

### 6. 你最关心的 Token 成本

按这个技能的意图，高成本部分是“推导场景与解释结果”，不是浏览器执行本身。

|阶段|主要成本|
|---|---|
|读取 Design Doc / AC|LLM Tokens|
|生成或选择测试场景|LLM Tokens（大头）|
|Playwright 执行 Chromium|CPU/内存/时间，不消耗 LLM Tokens|
|分析失败与生成报告|LLM Tokens|

因此企业实践通常会做：

1. 把 `test-plan.md` 和 `tests/e2e/*.spec.ts` 缓存进仓库；
    
2. 后续 `/qa` 优先复用已有场景；
    
3. 只对 Git diff 影响的功能 做增量生成；
    
4. CI 中高频执行 Playwright，LLM 只在失败时做解释与 triage。
    

### 7. 一个最小化“真实产物”示例

一句话总结

`qa/SKILL.md` 的设计原理是：用 LLM 把 Design/AC 转成“要测什么”，用 Playwright+Chromium 真正“怎么测”，再用 LLM 把执行证据解释成“是否满足需求”的 QA 结论。 它更像 AI QA Engineer + Playwright Runner 的组合，而不是“每次都从零生成脚本并瞎跑浏览器”。
