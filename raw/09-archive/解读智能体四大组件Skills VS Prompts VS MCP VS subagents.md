# 解读智能体四大组件Skills VS Prompts VS MCP VS subagents

## 前言

在用 Claude 搭建智能体、做自动化工作流的时候，都会卡一个关键点：Prompt、Skills、subagents、MCP 这几个功能，看着都能让AI变强，到底直接输Prompt就行？还是得专门写个Skill？复杂任务要不要拆分给subagents？想让AI读取网盘、本地文件又该用什么方式？

这四项能力看着相似，但它们的定位、工作方式、适用场景完全不同。一旦搭配错误或者乱用，不仅做不出自动化效果，还会出现上下文臃肿、AI乱触发、输出结果忽好忽坏的问题，白白浪费自己的搭建时间。

今天这篇内容，依据 Anthropic 官方博客，带大家搞懂 Claude 四大核心组件：Prompts、Skills、Subagents、MCP。把每个功能的底层逻辑、适用场景、怎么取舍、如何互补联动讲透，让你之后搭建AI工作流，再也不用凭感觉瞎试。

## 四大核心组件核心定位

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OWI0N2UyNmZiYTkwNzA2ZTg1YzFjNDQwZmQwOWI3MjVfNDAyNGIwYzEyODBhZTk4OTYzMDZmNGZiYTc4ZWEzYzdfSUQ6NzY1MTgxMjkyMzkxMzg2NjQ1OV8xNzgxNjk4MTI5OjE3ODE3ODQ1MjlfVjM)

先给大家建立一个最直观的认知，四个工具各司其职、互不重叠，也是你搭建高阶AI工作流的核心根基：

- **Prompt 是一次性临时指令**

- **Skills 是可复用的专业能力库**

- **Subagents 是独立干活的专项AI助手**

- **MCP 是连接外部数据的万能通道**。

### Prompts：临时对话指令，主打「即用即走」

Prompt 就是我们聊天框里手动输入的自然语言指令，也是大家最常用的交互方式。它最大的特点就是临时、即时、不存档，只对当前这一轮对话生效，对话结束之后就失效了，不会保留任何配置。

像临时总结文章、改改文案语气、单次简单数据分析、即时调整格式，这种只用一次的需求，用Prompt最合适。但如果你发现自己总是反复复制同一套指令、每次干活都要重新输入一模一样的规则，那就说明这套流程已经固定了，完全可以升级成Skill，不用每次都重复劳动，还能让AI执行得更稳定。

### Skills：可复用专业技能，AI的「专属训练手册」

和一次性的Prompt不一样，Skills是Claude真正用来沉淀专业能力的核心工具。它不是单一文本，而是一套包含指令、脚本、各类配套资源的文件夹工具包。最亮眼的设计，就是它的渐进式披露加载机制，全程按需加载，不会乱七八糟的内容全都塞进上下文，避免资源浪费。

简单说下它的工作逻辑：Claude先读取轻量化的元数据，快速判断当前任务需不需要这个技能。如果匹配上场景，再加载完整指令，只有真正用到的时候，才会调用配套的脚本和资源。这种动态加载的模式，能让Skill跨所有对话永久生效，一次配置，反复使用。

所有标准化、高频重复的专业场景，都适合用Skill来固化。比如企业统一的品牌规范、PDF和Excel批量处理、固定的数据分析流程、合规审核标准等等。用了Skill之后，AI的输出风格、执行逻辑全程统一，不会时好时坏。

### Subagents（子智能体）：独立专项助手，专注任务隔离

Subagents也就是子智能体，大家可以把它理解成独立于主AI的专属员工。它拥有自己独立的上下文窗口、专属系统提示词，还能单独配置工具权限，和主任务完全隔离开，独立性非常强。

它最大的优势就是任务隔离、可以并行干活、权限可控。像代码审查、安全审计、专项测试这种严谨度高、步骤复杂的任务，就非常适合交给子智能体。我们可以单独限制它的工具权限，只读不写、避免误操作，既不干扰主对话流程，又能精准完成专项工作。

而且子智能体可以直接复用我们提前写好的Skills，不用重复搭建规则。既保证了任务独立拆分、高效执行，又能依托标准化的Skill能力，保证输出质量稳定靠谱。

### MCP：AI与外部世界的连接桥梁

如果大家记不住，我教大家一个最简单的区分方式：Skills是教会AI做事的方法，那MCP就是帮AI找到做事的素材。MCP全称模型上下文协议，是一套通用的开放标准，专门用来打通Claude和各类外部系统、数据源的壁垒。

有了MCP，Claude可以无缝对接谷歌网盘、GitHub、数据库、企业CRM等各类第三方工具。不用我们手动上传文件、手动更新资料，AI可以实时读取、同步调用外部数据，真正实现自动化联动。

这两者的搭配堪称绝配：MCP只负责打通通道、拿到外部数据，Skills只负责制定规则、处理数据、落地具体任务。一个解决素材来源，一个解决执行标准，组合起来就能跑通一套完整的自动化工作流。

## 别再单独用！四大组件取舍\+联动搭配

Anthropic 官方的核心设计思路非常清晰，每一组工具都有明确的适用边界，既能独立干活，又能强强搭配。接下来按照官方标准，给大家拆解几组最高频的组合用法，讲清楚什么时候单用、什么时候搭配用、组合起来能实现什么效果。

### Skills VS MCP：数据通道 \+ 处理规则的黄金组合

这一对组合，是实现全自动AI工作流的核心关键，也是很多人搞不懂的重点。

大家记住一句话：MCP 只管「拿到数据」，Skills 只管「处理数据」。

MCP 是外部连接通道，专门帮 Claude 打通网盘、代码库、数据库、各类办公工具，让 AI 能实时读取外部素材、同步最新数据。但 MCP 只负责连接和获取，不会规定怎么处理、怎么输出。

Skills 就是配套的处理规则，专门告诉 AI 拿到数据之后该怎么干活。比如读取表格后怎么整理数据、拿到文档后怎么分析、调取代码后怎么审查。

单独开 MCP，AI 只会读数据不会干活；单独写 Skill，AI 没有最新素材可以处理。两者搭配，才能实现「自动获取数据\+标准化处理输出」的完整自动化闭环。

### Skills VS Subagents：通用能力 \+ 独立员工的完美搭档

如果你想让**所有对话、所有 Claude 场景**都具备某项专业能力，直接用 Skills。你可以把它理解成给 Claude 统一做技能培训，相当于一套通用教科书，不管是哪个会话、哪个任务，需要的时候都能自动调用对应的专业能力。

如果你需要**独立、封闭、专属的专项任务执行者**，就用 Subagents 子智能体。子智能体相当于专属岗位员工，有自己独立的工作空间、独立权限、专属任务，专门用来独立处理复杂流程，不会干扰主AI的正常对话。

而它俩最强的用法，就是组合搭配。我们可以让专属子智能体，直接复用提前写好的 Skills 能力。

举个很直观的例子：你搭建一个代码审查子智能体，专门负责代码质检、漏洞排查。同时你提前写好一套代码规范 Skill，子智能体在工作的时候，会自动加载这套 Skill，按照统一标准审查代码。既保留了子智能体独立干活、权限隔离的优势，又靠 Skill 保证了执行标准统一、零出错。

### Skills VS Prompts：长期固化流程 \+ 临时个性化微调

这一组是我们日常用得最多的，两者完全不冲突，属于互补关系。

Prompts 主打临时、一次性、即时交互。适合单次提问、临时改需求、微调文案风格、即时数据分析，用完就失效，没有任何留存。

Skills 主打复用、长效、主动触发。只要是你反复用到的工作流程、固定标准、专业方法，全部可以封装成 Skill，跨会话永久生效，AI 会主动识别场景、自动启用。

日常搭建工作流，最优解一定是两者搭配使用。

我们用 Skills 沉淀好固定的底层规则和专业能力，给 AI 打好基础；再用 Prompts 根据单次任务的不同，做个性化调整、细化需求、聚焦重点。一套固定标准应对通用场景，临时指令适配个性化需求，既稳定又灵活。

最后给大家整理一个超好记的组合口诀：**单次微调用Prompt，通用能力沉淀用Skills，独立专项任务用子智能体，外部数据接入靠MCP，高阶工作流全部组合用**。

## 搭建竞品研究AI智能体（完整工作流）

单用任意一个工具，只能实现最基础的AI能力。真正专业、能落地、高效率的高阶工作流，一定是多个组件联动配合出来的。接下来我完全照着 Anthropic 官方的竞品研究智能体案例，一步步带大家拆解完整搭建逻辑，每一步做什么、用什么工具、解决什么问题，全程讲得清清楚楚。

全自动竞品调研智能体，让AI自主完成行业竞品分析、挖掘对手优缺点、找到市场缺口，最终输出完整专业的分析报告。整套流程只需要五步就能成型。

### **第一步：MCP打通数据源，解决「无素材可用」的问题**

做竞品分析，第一步肯定是解决素材问题，没有数据一切都是空谈。我们先通过 MCP 协议给 Claude 配置外部连接，对接谷歌网盘读取内部行业报告和竞品文档，对接 GitHub 查看竞品开源代码和技术架构，对接网页搜索获取最新的市场动态、行业资讯。简单来说，就是靠 MCP 让AI自动同步所有调研需要的素材，不用手动上传、手动更新。

### **第二步：新建专属Skills，固化分析标准和工作流程**

有了素材之后，不能让AI自由发挥。如果没有统一标准，每次分析的维度、重点、输出格式都会乱七八糟。这一步我们新建一个专属的「竞品分析Skill」，把整套工作标准全部封装进去。包含团队固定的分析维度、文档检索规则、报告输出模板、重点筛选标准、资料取舍逻辑等等。

```Markdown
# My Company GDrive Navigation Skill

## Overview
Optimized search and retrieval strategy for Meridian Tech's Google Drive structure. Use this skill to efficiently locate internal documents, research, and strategic materials.

## Drive Organization

**Top-level structure:**
- `/Strategy & Planning/` - OKRs, quarterly plans, board decks
- `/Product/` - PRDs, roadmaps, technical specs
- `/Research/` - Market research, competitive intel, user studies
- `/Sales & Marketing/` - Case studies, pitch decks, campaign materials
- `/Customer Success/` - Implementation guides, success metrics
- `/Company Ops/` - Policies, org charts, team directories

**Naming conventions:**
- Format: `YYYY-MM-DD_DocumentName_vX`
- Final versions marked with `_FINAL`
- Drafts include `_DRAFT` or `_WIP`

## Search Best Practices

1. **Start broad, then filter** - Use folder context + keywords
2. **Target document owners** - Sales materials from Sales/, not root
3. **Check recency** - Prioritize documents from last 6 months for current strategy
4. **Look for "source of truth"** - Files with `_FINAL`, `_APPROVED`, or in `/Archives/Official/`

## Research Agent Workflow

1. Identify topic category (product, market, customer)
2. Search relevant folder with targeted keywords
3. Retrieve 3-5 most recent/relevant documents
4. Cross-reference with `/Strategy & Planning/` for context
5. Cite sources with file names and dates
```

封装完成之后，后续所有竞品分析任务，AI 都会自动套用这套标准化流程。不用你每次重复讲解规则，输出结果统一、规整、专业，完全杜绝忽好忽坏的问题。

### **第三步：配置双路子智能体，实现任务分工并行**

复杂的调研任务，千万别全部丢给主AI处理，不仅效率低，还容易出错、遗漏细节。这里我们配置两个独立的子智能体，让它们各司其职、并行工作，分担全部专项任务。

第一个是市场调研子智能体，搭配搜索、读取类工具，专门负责整理宏观行业信息。比如市场体量、行业趋势、用户口碑、竞品运营策略这些内容，全都交给它负责。

```Markdown
name: market-researcher
description: Research market trends, industry reports, and competitive landscape data. Use proactively for competitive analysis.
tools: Read, Grep, Web-search
---
You are a market research analyst specializing in competitive intelligence.

When researching:
1. Identify authoritative sources (Gartner, Forrester, industry reports)
2. Gather quantitative data (market share, growth rates, funding)
3. Analyze qualitative insights (analyst opinions, customer reviews)
4. Synthesize trends and patterns

Present findings with citations and confidence levels.

```

第二个是技术分析子智能体，配备代码读取、架构分析工具，专门深耕技术层面的内容。负责拆解竞品的技术栈、功能实现逻辑、技术优势、架构短板等精细化技术分析。

```Markdown
name: technical-analyst
description: Analyze technical architecture, implementation approaches, and engineering decisions. Use for technical competitive analysis.
tools: Read, Bash, Grep
---
You are a technical architect analyzing competitor technology choices.

When analyzing:
1. Review public repositories and technical documentation
2. Assess architecture patterns and technology stack
3. Evaluate scalability and performance approaches
4. Identify technical strengths and limitations

Focus on actionable technical insights that inform our product decisions.
```

两个子智能体相互独立、互不干扰，同时推进工作，大幅提升调研效率。而且它们可以直接复用前面搭建的竞品分析Skill，不用重复配置规则，开箱即用。

### **第四步：Prompt精准微调，锁定输出细节**

Subagents按照Skill固化的是通用标准，执行完调研后，可以通过Prompt进行专属需求的微调。

比如我们可以临时指定聚焦医疗行业客户、重点对比AI功能差异、精简无效信息，只保留可落地的市场缺口。

靠Prompt灵活适配单次任务的个性化需求，弥补标准化流程的局限性。

## 三、核心总结

看完整套实战案例，大家就能彻底明白：这四大组件不是竞争关系，而是相辅相成、缺一不可的整体，各自承担着独一无二的职责。

MCP 专门解决数据来源问题，打通所有外部素材渠道；

Skills 统一执行标准，解决AI输出不规范、不稳定的问题；

子智能体拆分复杂任务，解决工作杂乱、效率低下的问题；

Prompt 灵活微调，适配每一次任务的个性化需求。

吃透这套组合逻辑，不管是做行业调研、数据分析、代码开发、内容创作，你都能搭建出稳定、高效、完全自动化的Claude智能体工作流，真正把AI的生产力拉满。

