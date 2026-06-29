# 解读Google文章《5 Agent Skill design patterns every ADK developer should know》

在上一篇[精读Anthropic 文章 《Equipping agents for the real world with Agent Skills》](https://my.feishu.cn/wiki/IooCwdfqMiYyYIkB2w0cIo5Bnmh)中，我们彻底搞懂了 Agent Skills 的底层原理、文件夹规范、渐进式加载机制和开发安全规范。

现在包括 Claude Code、Gemini CLI、Cursor 在内的 多款主流智能体，已经统一了 Skill 文件夹布局与格式标准。**格式写法、目录结构这些基础问题，不再是写Skill的门槛。**

当下开发 Skill **真正的核心挑战，只有一个：内容设计**。

Anthropic只定义了「Skill 该如何打包、用什么格式存放」，但完全没有讲解「Skill 内部逻辑该如何设计、流程该如何搭建」。这就导致一个普遍问题：两个外表结构一模一样的 SKILL\.md，内部逻辑、执行效果、落地能力天差地别。

基于 Anthropic、Vercel、Google 官方开源仓库与内部落地实践，业界沉淀出了 **五种通用、可复用的 Skill 标准设计模式**。所有专业级 Skill，基本都是基于这五种模式单独或组合搭建而成。

本篇我们逐点精读、通俗拆解每种模式的核心特点、落地场景、官方示例，同时讲清选型逻辑与组合用法，帮你彻底搞定 Skill 高阶内容设计。

## 一、当前 Skill 开发的核心痛点：格式免费，内容拼实力

1\. **格式标准化、无技术壁垒**：主流 AI 工具全部适配统一 Skill 规范，目录、YAML、文件结构不用再反复调试，新手也能快速搭出标准框架；参考https://agentskills\.io/clients

2\. **内容无规范、全靠经验**：官方只给“打包规则”，不给“内容设计规则”，绝大多数人写的 Skill 只是空有框架，逻辑混乱、执行不稳定、复用性极差；

3\. **同质化外壳，差异化内核**：看似标准的 Skill 文件，内部工作流程、逻辑架构、执行精度完全取决于内容设计，这也是导致专业智能体的能力差距巨大的原因。

## 二、五大核心 Skill 设计模式

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NTU0MjAyYTgzNTM1NTkzZDMyYWQ1MzMyODViZThkMGNfNWVhNDNiNGFjN2Q2NGZhY2Y5YTMzN2Q3YjAxYjVhMTBfSUQ6NzY1MDgyMDQ3OTM1MTI0NjA0MV8xNzgxNjk4MDU3OjE3ODE3ODQ0NTdfVjM)

这五种模式是从海量官方落地案例中，总结的高频通用范式，覆盖绝大多数工作场景，所有示例均为官方原生可运行的 ADK 代码案例，可直接复用。

- Tool Wrapper：让您的代理瞬间成为任何库的专家。

- Generator: 从可重复使用的模板生成结构化文档。

- Reviewer: 根据严重程度对照清单对内容进行评分。

- Inversion: 代理人先对你进行询问再采取行动。

- Pipeline: 实施严格的多步骤工作流程并设置检查点。

### 模式一：Tool Wrapper（工具封装模式）

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NDc1N2VjNWE5MmZhZmQxYmZhMTBiMThlYmM2ZTgwODBfMmNmMGFjMmQ1NmMzOTRjMGMwMzY0NDVkMWVjOTIzODRfSUQ6NzY1MDgyMTYwNjkzNTIzNTc5NF8xNzgxNjk4MDU3OjE3ODE3ODQ0NTdfVjM)

**核心定位**：**赋予智能体特定技术栈的专属专业知识**，是最简单、最基础的 Skill 设计模式。

**核心特点：**

不用把各类框架、类库的使用规范硬编码写进系统提示词，而是统一打包进 Skill。智能体只有在用到对应技术时，才会动态加载专属规范文档，做到按需加载、精准匹配，非常适合沉淀团队内部编码规范、框架最佳实践。

**工作逻辑：**

SKILL\.md 会监听用户指令中的技术关键词，一旦匹配，自动读取 references 目录下的规范文件，将对应规则作为绝对标准执行。

**示例：FastAPI 开发技能**

> https://github\.com/fastapi/fastapi/blob/master/fastapi/\.agents/skills/fastapi/SKILL\.md
> 
> 

专门用于 FastAPI 项目开发、代码审查、问题调试，内置完整的编码规范，智能体在写代码、审代码时自动加载规范，严格遵循对应语法、依赖注入、类型注解标准，输出统一、专业的代码。FastAPI 支持多种流式响应模式，但具体实现细节需要参考专门的"streaming reference"文档。推荐使用的开发工具，详情需参考"other tools reference"文档。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGFjMmUzZDRhZTE3ZGIzNzMyMTkwY2M0NDI3ODFlMTlfODI2MDRjYjdmMWIwN2E1ZDk5MzEzMzA4MjNiYTRmMmJfSUQ6NzY1MDgyMjU5NTU3ODk3MzEzMl8xNzgxNjk4MDU3OjE3ODE3ODQ0NTdfVjM)

### 模式二：Generator（内容生成模式）

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NzdmYTdlZTRjNjg4NzlhOTdkOWYzNjRjM2I0MjA5YTVfZDJjNDAwN2VhOTdhODdiMGVkMGVhNWE5MDljY2ZlNTVfSUQ6NzY1MDgyNDUwMDM4ODc2MDU1MV8xNzgxNjk4MDU3OjE3ODE3ODQ0NTdfVjM)

**核心定位**：**解决智能体输出不稳定、格式不统一的问题**，实现标准化、模板化内容生成。

**核心特点：**

很多时候智能体每次生成的文档结构、格式、风格都不一样，随机性极强。Generator 模式通过「模板\+样式规范」彻底解决这个问题，全程采用填空式标准化生成，零随机偏差。

该模式依赖两个专属目录：assets 存放输出模板，references 存放样式规范。Skill 本身不写具体内容，只负责统筹流程：加载模板、读取样式、补齐缺失信息、标准化输出。

**适用场景**：API 文档生成、提交信息标准化、项目架构模板搭建、技术报告输出。

**示例：标准化技术报告生成技能**

智能体先加载样式规范，再读取报告模板，主动询问用户缺失的核心信息（主题、核心结论、受众、数据），补齐所有内容后，严格按照模板生成完整规范的 Markdown 技术报告，保证每次输出结构完全一致。

```Markdown
# skills/report-generator/SKILL.md
---
name: report-generator
description: Generates structured technical reports in Markdown. Use when the user asks to write, create, or draft a report, summary, or analysis document.
metadata:
  pattern: generator
  output-format: markdown
---

You are a technical report generator. Follow these steps exactly:

Step 1: **Load 'references/style-guide.md'** for tone and formatting rules.

Step 2: **Load 'assets/report-template.md' **for the required output structure.

Step 3: **Ask the user for any missing information needed to fill** the template:
- Topic or subject
- Key findings or data points
- Target audience (technical, executive, general)

Step 4: Fill the template following the style guide rules. Every section in the template must be present in the output.

Step 5: Return the completed report as a single Markdown document.
```

### 模式三：Reviewer（审查评分模式）

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=ZmZmZTAxMDRhMWRmN2ZmYjk2NmRhMTJiNWJmNWRhMDlfY2U0MjRmMTg0NDk1NDEzZjU5NmQzZmMwMzllMTAwYzhfSUQ6NzY1MDgyNTc1MzM0NDU2MDA4OV8xNzgxNjk4MDU3OjE3ODE3ODQ0NTdfVjM)

**核心定位**：**模块化自动化审查、分级评分**，实现代码、文档的标准化质检。

**核心特点：**

核心逻辑是「审查流程和审查标准分离」。不用在提示词里堆砌冗长的审查规则，而是把所有质检标准、检查条目，统一放在 references 审查清单文件中。

Skill 只负责固定的审查流程，替换不同的清单文件，就能快速切换审查场景，适配性极强。同时支持按严重程度分级输出结果，审查结果更清晰、更专业。

**适用场景**：代码 PR 审核、漏洞检测、代码风格质检、文档合规校验。

**示例：Python 代码审查技能**

智能体自动加载 Python 代码审查清单，逐行核对用户代码，标记问题行数、区分错误、警告、提示三级严重程度，不仅标注问题，还解释原因、给出可直接替换的修复代码，最终输出包含总结、问题清单、评分、优化建议的标准化审查报告。

```Markdown
# skills/code-reviewer/SKILL.md
---
name: code-reviewer
description: Reviews Python code for quality, style, and common bugs. Use when the user submits code for review, asks for feedback on their code, or wants a code audit.
metadata:
  pattern: reviewer
  severity-levels: error,warning,info
---

You are a Python code reviewer. Follow this review protocol exactly:

Step 1: **Load 'references/review-checklist.md'** for the complete review criteria.

Step 2: Read the user's code carefully. Understand its purpose before critiquing.

Step 3: Apply each rule from the checklist to the code. For every violation found:
- Note the line number (or approximate location)
- Classify severity: error (must fix), warning (should fix), info (consider)
- Explain WHY it's a problem, not just WHAT is wrong
- Suggest a specific fix with corrected code

Step 4: Produce a structured review with these sections:
- **Summary**: What the code does, overall quality assessment
- **Findings**: Grouped by severity (errors first, then warnings, then info)
- **Score**: Rate 1-10 with brief justification
- **Top 3 Recommendations**: The most impactful improvements
```

### 模式四：Inversion（反向访谈模式）

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTM0M2ViNTIyYzk1MjY4MGQyYWZhNGQzMjZlM2I5MGVfMjZlZGJlMzA2OWQ0ZWI4MzNjZTViNGVhN2JlZjYyNTFfSUQ6NzY1MDgyNjg2MTU4NDUzNDcyNl8xNzgxNjk4MDU3OjE3ODE3ODQ0NTdfVjM)

**核心定位**：**反转人机交互逻辑，先摸清需求，再落地执行**，杜绝智能体盲目输出。

**核心特点：**

普通智能体的通病：用户刚说半句话，就急于猜测需求、直接生成结果。Inversion 模式彻底改掉这个问题，让智能体从「执行者」变成「访谈者」。

**通过强制门禁指令**，要求智能体必须按固定顺序、逐轮提问，收集完整需求、约束条件后，才能开始生成最终方案，中途绝不提前输出、绝不跳过提问环节。

**适用场景**：项目规划、系统设计、需求梳理、定制化方案输出。

**示例：软件项目规划技能**

智能体分三阶段结构化访谈：先调研业务问题、用户群体、项目规模；再确认部署环境、技术栈、硬性约束；收集完所有信息后，才加载模板生成完整项目方案，最后主动征求用户反馈、迭代优化。

```Markdown
# skills/project-planner/SKILL.md
---
name: project-planner
description: Plans a new software project by gathering requirements through structured questions before producing a plan. Use when the user says "I want to build", "help me plan", "design a system", or "start a new project".
metadata:
  pattern: inversion
  interaction: multi-turn
---

You are conducting a structured requirements interview. **DO NOT start** building or designing until all phases are complete.

## Phase 1 — Problem Discovery (ask one question at a time, wait for each answer)

**Ask these questions in order**. Do not skip any.

- Q1: "What problem does this project solve for its users?"
- Q2: "Who are the primary users? What is their technical level?"
- Q3: "What is the expected scale? (users per day, data volume, request rate)"

## Phase 2 — Technical Constraints (only after Phase 1 is fully answered)

- Q4: "What deployment environment will you use?"
- Q5: "Do you have any technology stack requirements or preferences?"
- Q6: "What are the non-negotiable requirements? (latency, uptime, compliance, budget)"

## Phase 3 — Synthesis (only after all questions are answered)

1. Load 'assets/plan-template.md' for the output format
2. Fill in every section of the template using the gathered requirements
3. Present the completed plan to the user
4. Ask: "Does this plan accurately capture your requirements? What would you change?"
5. Iterate on feedback until the user confirms
```

### 模式五：Pipeline（流水线校验模式）

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NmIzNTgyYmFkMGY0NGQ1YzNiMWRjNjgzMTA2MWQzODJfNTYyM2U2ZWQ5NjEzYzAwNDRmMGEyZTQzZmZhNWE0ODBfSUQ6NzY1MDgyNzUxMzYwOTg5ODk2NV8xNzgxNjk4MDU3OjE3ODE3ODQ0NTdfVjM)

**核心定位**：**强约束、多步骤、可校验的复杂工作流**，杜绝步骤遗漏、流程跳过。

**核心特点：**

针对复杂任务，专门设计带「硬性检查门禁」的串行工作流，**每一步都必须校验通过、用户确认后，才能进入下一步**，绝对不允许跳过步骤、简化流程。

该模式会按需调用各类模板、规范清单，不同步骤加载不同资源，精准控制上下文内容，保证流程严谨的同时，不浪费 Token。

**适用场景**：复杂文档生成、代码标准化改造、多步骤工程化任务。

**示例：Python API 文档流水线技能**

严格执行四步流水线：第一步盘点项目所有公开接口并确认；第二步按规范生成文档注释并逐一对齐；第三步组装完整 API 文档；第四步按质检清单自查修复，全程每一步都有校验门禁，必须合规通过才能进入下一环节，最终输出零瑕疵的标准化文档。

```Markdown
# skills/doc-pipeline/SKILL.md
---
name: doc-pipeline
description: Generates API documentation from Python source code through a multi-step pipeline. Use when the user asks to document a module, generate API docs, or create documentation from code.
metadata:
  pattern: pipeline
  steps: "4"
---

You are running a documentation generation pipeline. **Execute each step in order. Do NOT skip steps** or proceed if a step fails.

## Step 1 — Parse & Inventory
Analyze the user's Python code to extract all public classes, functions, and constants. Present the inventory as a checklist. **Ask: "Is this the complete public API you want documented?"**

## Step 2 — Generate Docstrings
For each function lacking a docstring:
- Load 'references/docstring-style.md' for the required format
- Generate a docstring following the style guide exactly
- Present each generated docstring for user approval
**Do NOT proceed to Step 3 until the user confirms.**

## Step 3 — Assemble Documentation
Load 'assets/api-doc-template.md' for the output structure. Compile all classes, functions, and docstrings into a single API reference document.

## Step 4 — Quality Check
Review against 'references/quality-checklist.md':
- Every public symbol documented
- Every parameter has a type and description
- At least one usage example per function
Report results. Fix issues before presenting the final document.
```

## 三、技能模式选型

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MjNiYzFhZTM3MDIzNGFmZDIwZGEwMzVlZTZlZDdmODNfZTUwMWNmNDlkNjY4NDYzOWE4MmZlZTNjNjY2ODQ1MDZfSUQ6NzY1MDgyODQ5ODM3MzkzODM3NF8xNzgxNjk4MDU3OjE3ODE3ODQ0NTdfVjM)

核心判断从一个问题开始：「这个技能是否会产生输出？」，根据回答（是 / 否）分成两大分支，分别走向不同的模式：输出型技能或者非输出型技能。

- 输出型技能：

当技能会主动生成内容 / 输出时，会继续判断它是否基于模板生成，分为两种模式：

1. From a template? → Yes → Generator 模式

    - 适用场景：基于固定模板批量生成文档 / 内容。

    - 示例：`document_create`（根据模板创建文档）。

    - 特点：输入模板参数 → 输出标准化内容，适合重复性、结构化的生成任务。

2. From a template? → No → Tool Wrapper 模式

    - 适用场景：封装一个能直接产生输出的工具 / API。

    - 示例：`book_open`（打开并读取书籍内容，返回文本）。

    - 特点：直接调用工具 / 系统能力，不依赖固定模板，输出由工具本身决定。

- **非输出型技能**

当技能不直接生成输出时，会通过 3 个连续判断，匹配到 4 种模式之一：

1. 判断 1：Does it evaluate existing input? → Yes → Reviewer checklist 模式

    - 适用场景：评估 / 检查已有的输入内容。

    - 示例：Reviewer checklist（对现有文档做合规性检查、质量审核）。

    - 特点：不生成新内容，只对已有内容进行校验、评分、反馈。

2. 判断 1：No → 进入判断 2：Needs user input first? → Yes → Inversion chat\_question 模式

    - 适用场景：需要先向用户提问获取信息，再继续执行。

    - 示例：`chat_question`（多轮对话，先问清用户需求再行动）。

    - 特点：技能流程以 “向用户提问” 为起点，依赖用户输入推进后续步骤。

3. 判断 2：No → 进入判断 3：Has ordered steps? → Yes → Pipeline workflow\_steps 模式

    - 适用场景：有明确先后顺序的多步骤工作流。

    - 示例：`workflow_steps`（按固定流程执行任务，比如 “数据清洗→分析→可视化”）。

    - 特点：步骤是串行的，必须按顺序执行，前一步的输出是后一步的输入。

4. 判断 3：No → Tool Wrapper 模式

    - 适用场景：无输出、无评估、无需用户输入、也无固定步骤的工具封装。

    - 示例：`book_open`（仅打开书籍，不读取 / 处理内容，只是执行一个动作）。

    - 特点：纯工具调用，不涉及复杂逻辑，仅执行单一、无状态的操作。

五种模式对应完全不同的工作场景，可根据需求快速选型：

1\. 需要适配特定技术栈、沉淀团队规范 → 选 **Tool Wrapper**

2\. 需要统一输出格式、标准化生成内容 → 选 **Generator**

3\. 需要自动化质检、审查、分级评分 → 选 **Reviewer**

4\. 需要梳理模糊需求、精准确认条件 → 选 **Inversion**

5\. 需要复杂多步骤、强校验、不可跳过的工作流 → 选 **Pipeline**

## 四、所有模式支持自由组合

五大设计模式**互不排斥、可自由组合**，这也是高阶专业 Skill 的核心设计思路。

单一模式只能解决简单场景，复杂业务场景需要多模式搭配使用：

1\. 流水线（Pipeline）结尾可嵌套审查模式（Reviewer），实现「流程执行\+最终自检」双重保障；

2\. 生成模式（Generator）可搭配反向访谈模式（Inversion），先收集完整需求，再标准化生成内容；

3\. 所有模式都依托 Skill 渐进式披露机制，运行时只会加载当前步骤所需的内容，不会浪费 Token，兼顾严谨性与性能。

## 五、全文总结

1\. 当下 Skill 开发早已告别「拼格式、拼结构」的初级阶段，**内容逻辑设计**是唯一核心壁垒；

2\. 业界通用的五种设计模式，覆盖绝大多数智能体工作场景，是标准化、可复用的 Skill 内容设计范式；

3\. 每种模式都有专属定位和固定落地逻辑，适配技术封装、内容生成、代码审查、需求梳理、复杂流水线等场景；

4\. 高阶 Skill 开发核心是「模式组合」，通过多模式搭配，可搭建出稳定、专业、可迭代的生产级智能体工作流，彻底替代臃肿、脆弱的传统长 Prompt。

