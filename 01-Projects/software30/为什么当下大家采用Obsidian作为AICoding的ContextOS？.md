# 为什么当下大家采用Obsidian作为AICoding的ContextOS？

## 一、AI Coding 真正的瓶颈是上下文

未来的 AI Coding 一定走向 Agent 自主开发： Agent 自己读需求 → 拆解任务 → 查知识库 → 写代码 → 自测 → 提交Agent 能不能靠谱，完全取决于它能拿到什么样的上下文。

稍微复杂一点的业务系统，不完整、低质量的上下文，会让AI 立刻翻车：

1. 不知道业务边界、历史决策、约束条件

2. 不知道模块之间依赖关系

3. 不知道旧代码为什么这么写（坑点、兼容、历史妥协）

4. 不知道产品规则、权限、风控、异常场景

AI 不是不会写代码，而是看不到完整世界，只能盲人摸象，不可避免产生非预期的输出。必须经过反复多轮协作才能达到目的，一方面大量Token消耗，另一方面AI并没有提效。

---

## 二、Agent 友好的上下文，必须满足 4 个硬性条件

1. 结构统一：文档格式、字段、层级一致，Agent 能批量解析

2. 可被程序读取：纯文本 Markdown，无私有格式壁垒

3. 知识可关联：模块、接口、需求、坑点、对话能互相链接跳转

4. 可长期沉淀迭代：每次改动自动更新上下文，形成持续可进化的业务大脑

市面上几乎没有工具同时满足这四条：

- Notion：私有数据库结构，Agent 很难批量读取

- 飞书 / 语雀：偏文档，弱关联，无法形成知识网络

- Confluence：太重，维护成本极高

- 普通文件夹：结构混乱，没有关联，上下文碎片化

Obsidian 天生是为「可被机器阅读的知识网络」设计的。在当下成为了很多中小项目共同的选择。

---

## 三、Obsidian 如何提供 Agent 级别的上下文能力

### 双链 = 给 Agent 提供业务关联图谱

- 一个需求链接对应的接口、模块、踩坑记录、AI 对话

- Agent 读一个文件，能自动遍历所有关联上下文

- 相当于给 AI 装上业务关系雷达，不会写出孤立、冲突、违背历史的代码

### 纯 Markdown \+ 规范目录 = 结构化、可被脚本 / Agent 批量加载

通过目录 \+ 模板，给业务建立统一 Schema：

- PRD 固定字段

- 接口文档固定格式

- 技术方案固定结构

- AI 对话固定归档

Agent 可以写一段简单脚本，自动扫描整个知识库，抽取需求、约束、接口、规则，拼成全局上下文喂给大模型。

### 本地文件 = 可以直接作为 Agent 的长期记忆库

- Agent 都可以直接读取 Vault

- 不需要 API、不需要权限、不需要云端接口

- 可以把整个产品知识库作为 System Prompt 背景知识库 挂载给 AI

这就是产品专属私有上下文，也是 AI 能稳定输出符合业务的代码的关键。

### Dataview \+ Templater = 自动生成动态上下文

- Dataview 自动汇总所有待开发需求、接口清单、历史坑点

- Templater 一键生成符合格式的 Prompt 片段 Agent 可以实时拉取最新视图，拿到动态更新的上下文，而不是静态旧文档。

---

## 四、Obsidian \+ Agent 的Context上下文架构图

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Y2E2NGYwYzQzZjlmODhmMDA4NDI3OTUwODNlNTQ0YjhfZGIyYTExMTg2ZjkzYTE4OWYwN2I0YjBjOGU5MmMzMTBfSUQ6NzY0NTA5Mzk1NDg0ODg4NTcyOV8xNzgyNDY5MzkzOjE3ODI1NTU3OTNfVjM)

---

## 五、一句话总结

普通编辑器只给 AI 提供 “局部代码片段”，而 Obsidian 能给 AI 提供 “整个产品的业务大脑”。 在 Agent 自主开发时代，上下文的完整度和可访问性，直接决定 AI 能不能替代大量研发工作，而 Obsidian 是目前性价比最高、最适合个人与小团队搭建这套上下文的载体。

# 六、下一篇

[20分钟搭建AI驱动的产品知识库](https://nio.feishu.cn/wiki/A1vjwU0GbiL482kXobmcd2qKnWd)

# 参考资料：

[我用Claude \+ Obsidian搭建一个产品经理知识库](https://mp.weixin.qq.com/s/JXRT02fDH2EH6oi_i0-yyw)

[用Claude code 和 Obsidian零基础搭建本地知识库](https://www.bilibili.com/video/BV1y19hBhEMT/?spm_id_from=333.1391.0.0&vd_source=7afb44332c571a8a5bfa5acec59995b0)

[karpathy](https://gist.github.com/karpathy)/[llm\-wiki\.md](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)



