# 解读Anthropic 文章 《Equipping agents for the real world with Agent Skills》

> 精读Anthropic 文章 《Equipping agents for the real world with Agent Skills》
> 
> 

普通大模型、通用智能体，擅长语言理解与文本生成，但严重缺少两类关键能力：**程序性知识**（不知道事情怎么做）和 **结构化上下文**（不知道资源在哪、规范是什么）。

所以 Anthropic 推出了 **Agent Skills**：一套专门用来把「通用智能体」升级成「专业化智能体」的标准化方案。

## 一、是什么促使 Anthropic 开发出 Agent Skills？（诞生背景）

随着模型能力迭代，Anthropic 打造出能运行在计算机环境中的**通用 AI 智能体Claude Code。**Claude Code 可以读写本地文件、执行代码、处理跨领域复杂任务，让 AI 真正拥有了“操作电脑”的能力。

但能力变强之后，新的工程痛点也逐渐暴露：

通用智能体Claude Code 本身没有行业知识、没有业务流程、没有团队规范。只能靠大量 Prompt、碎片化定制来补强，这种方式**不可规模化、不可移植、无法沉淀**。

也就是说，缺少一套标准方式，把团队的流程、经验、脚本、资源，批量、复用、可迭代地交给通用智能体Claude Code。

这就是Anthropic 推出 Agent Skills 的原因：**给通用智能体一套标准化的“专业装备”，让它可以快速适配真实世界的各类工作。**

> 补充：2025年12月18日，Agent Skills 正式成为**跨平台开放标准**，不再局限于 Claude 生态。
> 
> 

## 二、到底什么是 Agent** **Skill？

用Anthropic 的话说，**Agent Skills 是一套由指令、脚本、资源构成的结构化文件夹。AI 可以主动发现、动态加载这些内容，从而在特定任务上获得更强、更专业、更稳定的表现。**

通俗理解：通用Agent是一个“聪明但没经验的新人”，Skill 就是给这个新人的**整套岗位手册 \+ 工具包 \+ 资源库**。

不需要重新训练、不需要反复写提示词，只要加载对应的 Skill，通用 Agent 立刻变身**专业化智能体**，适配对应场景的专属工作。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZWU1YThmNjNjMWNmNjI2YTk5NjU3YzUzNjJlMDNiMzVfMDY2ZWEwMzEwODkyOGNmMTYzY2FkZjk1YWY5NjYxNWZfSUQ6NzY1MDc5NjY4ODM3MTczMTQwM18xNzgxNjk4MDY2OjE3ODE3ODQ0NjZfVjM)

## 三、Skill 的完整构成（三大核心要素）

一套完整的 Skill 包含三类内容，三者共同补齐通用Agent的能力短板：

```Plain Text
my-skill/
├── SKILL.md          # Required: metadata + instructions
├── scripts/          # Optional: executable code
├── references/       # Optional: documentation
├── assets/           # Optional: templates, resources
└── ...               # Any additional files or directories
```

**1\. SKILL\.md（指令流程）**

标准化 SOP，写清任务步骤、执行逻辑、输出规范。用来补齐通用Agent**程序性知识缺失**的问题，告诉 通用Agent「这件事具体怎么做」。

**2\. Scripts（可执行脚本）**

Python、Shell 等可运行代码，替代低效的文本推演，让任务执行高效、稳定、可复现。

**3\. Resources（配套资源）**

包括模板`templates/`、参考文档`references/`、资源文件`assets/`等。用来补齐 通用Agent **结构化上下文缺失**的问题，告诉 AI「工作需要的资源在哪里、规范是什么」。

## 四、核心文件SKILL\.md 

SKILL\.md 是每一个 Skill 的**唯一核心入口**，也是官方强制要求的必备文件，分为两大部分：

**1\. 头部 YAML 元数据（必填）**

包含技能名称、技能简介。智能体启动时，会预加载所有 Skill 的元数据进入系统提示词。

作用：让 AI 只看一句话简介，就能判断「当前任务要不要用这个技能」，不需要加载全文，极致节省 Token。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MWE3ODRkZmQ0NzNhYjI4NzNhNDgxZjZmZDdiNjg2MmRfNjk0ODI3NjkzY2Y5OWIwYzhmMDBjZDRlOGRhYTc1NjFfSUQ6NzY1MDgwMDU5MjM5ODQzNzU3Ml8xNzgxNjk4MDY2OjE3ODE3ODQ0NjZfVjM)

**2\. 主体正文内容**

完整的任务流程、操作规范、使用说明、注意事项。当 AI 判断需要使用该技能时，才会加载完整这部分内容，指导 AI 完成标准作业。

## 五、Additional Content：技能的附加扩展文件

复杂技能不可能全部塞进单一 SKILL\.md，所以支持**附加附属文件（additional content）**。

开发者可以在 Skill 文件夹中新建多个辅助文件，例如 reference\.md、forms\.md、配置文件、模板文件等，并在 SKILL\.md 中引用。

这些附加内容**不会默认加载**，只有 AI 执行到对应细分场景、需要对应信息时，才会按需读取。

举例（Anthropic的 PDF 技能）：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YWRlNWM3YjNhZDgwNTY1YWM3NjZiNzhlOTUyYTY4YjhfNDM1YzlkNzIwYTI3ODU4MGUwMDFmNDNjNzhmYmJlNmFfSUQ6NzY1MDgwMTcyODcxOTUzOTQyOF8xNzgxNjk4MDY2OjE3ODE3ODQ0NjZfVjM)

表单填充的专属规则单独放在 forms\.md，AI 日常解析 PDF 不需要加载，只有做表单填充任务时，才会动态读取。

## 六、Skill 核心精髓：渐进式披露机制（Progressive Disclosure）

这是 Skill 碾压传统 Prompt、成为新一代智能体范式的**核心设计原理。**

**核心思想：分层加载、按需披露、用到才读、不用不载**。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZDViODgzMjkzMWViODlhM2E1ZmY5OWY5Mzg4MjFmNzlfYWY0YTJmYjY0MWU2NTAxN2NiODZmZDQ2YWQ1MWM2N2FfSUQ6NzY1MDgwMjUyNzIxMDI5NDQ2Nl8xNzgxNjk4MDY2OjE3ODE3ODQ0NjZfVjM)

一共三层披露逻辑：

**第一层：元数据（常驻、轻量）**——用于判断是否触发技能，消耗约100 token。

**第二层：SKILL\.md 正文（按需加载）**——用于执行常规任务，消耗约5000 token。

**第三层：附属附加文件（精准加载）**——用于执行细分复杂任务

这套机制让 Skill 的上下文承载量**近乎无上限**，彻底突破大模型窗口限制。即使某个Skill包含TB级资料（代码库、数据库、文档），Agent只需在上下文中保留**当前任务的微量信息**，其余通过工具动态调用。

## 七、工作原理：用户触发技能后，上下文窗口如何变化？

下图展示了当「用户触发 PDF 技能」时，上下文窗口的变化情况。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MWMxMzBjMDNmZGRhN2Y1OGE2NTUyMDI4NDAwMjVhNTVfYTVhNGEzMTZjMmI1OTg1NjVjYzYyOGIwNjU3NTllNDlfSUQ6NzY1MDgwMzc2NTMxMzk5ODA1Nl8xNzgxNjk4MDY2OjE3ODE3ODQ0NjZfVjM)

**阶段1：初始状态（最小上下文）**

上下文窗口包含核心系统提示（System Prompt）、每个已安装技能的YAML 元数据以及用户的初始消息（`User：Fill out ...`）；

**阶段2：技能判定与触发**

AI 通过元数据判断当前任务需要 PDF 技能，主动调用 Bash 工具，从文件系统读取 `pdf/SKILL.md` 完整内容载入上下文。

**阶段3：按需加载附加内容**

如果任务需要填充表单，AI 继续读取附属文件 `forms.md`，补充细分规则进上下文。

**阶段4：完整执行任务**

上下文集齐所需全部规范，AI 按照 Skill 流程完成标准化任务。

简单总结：**上下文不是一次性塞满，而是跟着任务动态、增量、精准扩容**。

## 八、Skill 的高阶能力：可搭载可执行代码

Skill 不只是文档手册，还可以包含可执行代码。Claude 可以**自主判断、自主调用**这些代码作为工具执行。

为什么必须要有代码能力？

大模型纯文本推演存在两个致命问题：**Token 消耗极高、结果不具备确定性**。

而代码执行是确定性、可复现、高效率的。

以Anthropic的 PDF 技能为例：内置 Python 脚本用来提取表单字段。AI 不需要把 PDF、脚本全部读进上下文，直接调用运行，结果稳定、每次一致。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGMxM2JlZGU4MDRjZDAwNTllZTBkMGQ1Mjk3YTFlM2VfZGJmY2JkNDc3MmZjZjRlZTBhNTljNmUyNzI5MzVmOWNfSUQ6NzY1MDgwOTkwNDg5Mjg0MDk0M18xNzgxNjk4MDY2OjE3ODE3ODQ0NjZfVjM)

## 九、官方标准：开发与评估 Skill 的四步流程

Ahthropic 给出了Skill 创作迭代四步法：

**1\. 先评估、后开发**

先用真实任务测试通用智能体，精准找到能力短板、信息缺失、执行卡点，再针对性开发Skill，拒绝盲目写文档。

**2\. 模块化结构化设计**

当`SKILL.md`文件变得太大，难以管理时，可将其内容拆分为多个独立文件并进行引用。如果某些上下文互斥或很少同时使用，保持路径分离有助于减少令牌使用量。最后，代码既可作为可执行工具，也可用作文档。应明确Claude是直接运行脚本，还是将脚本作为参考读入上下文。

**3\. 站在 Claude 视角优化**

特别关注你技能的 `name` 和 `description`（AI 触发的核心依据），持续观测触发准确率、执行路径，修复误触发、漏触发、流程跑偏问题。

**4\. 人机协同循环迭代**

让 AI 沉淀成功路径、总结常见错误、复盘失败原因，持续把实战经验固化进 Skill，实现技能自优化。

## 十、使用 Skill 的安全规范（必看）

因为 Skill 可以搭载脚本、文件操作、网络调用等高权限能力，要特别关注安全问题：

1\. **只使用可信来源的技能**，杜绝来路不明的第三方 Skill；

2\. 引入陌生技能必须**全量审计**所有文件、脚本、依赖、资源；

3\. 重点排查外网连接、数据导出、文件读写等高危逻辑，防止数据泄露、恶意执行、越权操作。

## 全文总结

1\. 为了解决通用智能体「只会聊天、不会干活」的问题，解决 Prompt 不可沉淀、不可规模化的痛点，Anthropic 基于 Claude Code 实践推出 Agent Skills；

2\. Skill 是结构化文件夹体系，由指令、脚本、资源三部分组成，核心入口为 SKILL\.md，支持附属扩展内容；

3\. 依靠**渐进式披露**分层加载机制，动态改变上下文内容，突破传统上下文限制，成为替代长 Prompt 的新范式；

4\. Skill 支持确定性代码执行，搭配标准化的四步开发评估流程、严格的安全规范，让通用 AI 可以低成本、标准化迭代为专业化工作智能体。

