# 为什么要软件产品知识库？

领域知识决定了 AI 在业务中能发挥多大的价值和作用。任何 AI 系统都由模型、知识、架构三部分组成。模型由供应商提供，只能被动接受；架构常因模型能力升级而失效重做。相比之下，领域知识只能从内部积累——不可替代，且随业务演进而持续变化，是最值得长期投入的部分。

然而，领域知识的沉淀面临诸多挑战。知识散落在代码和注释、配置、文档、沟通记录、会议纪要等各处，没有统一载体，这带来两层后果：

- 知识质量退化：传播靠口口相传，人走知识就断；口径不一致，不同文档里定义矛盾，没人能仲裁；文档无人持续维护，三个月后就和线上对不上。
    
- 工程熵增：缺乏全局视图，团队无法获取全局知识、系统之间的矛盾数据带来技术负债。
    

问题排查、代码生成这些本可以被 AI 极大提效的场景，都卡在了"知识喂不进去"这一步。

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=YWIxZmNhMzQ5YWI0YjZlM2M5ZmQyODc2MTA3MzZlODZfdDlKRkZuQkRxS3dVZVpCRUZQbDJGRlVYenRsN2RvNEhfVG9rZW46RnlaY2JOSDRib2JkUHl4Wkw4OWNMZWJ5blZnXzE3ODI3MzUxNDM6MTc4MjczODc0M19WNA&add_watermark=true&scene_type=CCM)

# LLM 编译器：怎么建

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=N2JhMDdhNzZlYTY5NDhlMDJmOTZlMmI5MmM2NTY2YWVfZmxpdWZzVGpmSTFoc2l3aU9UTEl4SjgxM0VoUVpadk5fVG9rZW46RDVtNWJpRE4yb1N5M2Z4VHBnaGNjNDd3bnljXzE3ODI3MzUxNDM6MTc4MjczODc0M19WNA&add_watermark=true&scene_type=CCM)

## 是什么

LLM Wiki 不是一份"用 LLM 写出来的文档"，而是一份结构化、有约束、可验证的知识资产。它和传统文档的区别在四个层面：

- 结构可解析——单页内部结构。每个页面是 frontmatter + 正文的双层结构，frontmatter 是脚本可解析的 YAML，承载关系字段（type、domain、upstream、computed_by 等），正文承载语义描述。脚本可直接读取关系信息，不必依赖 LLM 反复解析正文。
    
- 层级可下钻——跨页层级结构。域按业务主题嵌套组织，形成可逐层下钻的树。Agent 检索时可从根域渐进披露，避免一次性灌入全部上下文。
    
- 关系可遍历——跨页关系结构。页面之间的血缘、归属、消费、引用关系以边的形式显式记录，构成有向图。脚本可遍历、可计算影响范围、可做多跳召回。
    
- 正确性可度量——分结构、语义、人工三层校验。结构层用机械规则做自动化约束；语义层用 LLM 评审页面内容（描述准确性、口径一致性、域归属合理性）；关键节点由人工确认兜底。三层叠加，知识库正确性从主观判断转为可度量的工程指标。
    

## 谁来建

让 LLM 来建，不是让人来建。人工维护 Wiki 的核心问题是成本高、腐化快、难持续。LLM 作为编译器，把散落的源材料（前面介绍的9大类资产）编译成结构化页面，人只在关键节点做确认。

## 怎么建

整体构建过程可以抽象为六个步骤：提取 → 生成 → 归类 → 聚合 → 链接 → 验证，本质是一条将散落源材料编译为结构化知识的流水线。

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=MThjNDQzZjg1MGUwZmRhNjQ3NTBmZWFhOWFjNjFlODBfYmU5WXp2ZkEyeWJMcVlPQnMxeTRJRVZiUGtCZTN6Y0FfVG9rZW46WmtyRGJlZDhub2tYRXF4V2t0S2NzbFRObnNnXzE3ODI3MzUxNDM6MTc4MjczODc0M19WNA&add_watermark=true&scene_type=CCM)

# 核心原则

## **知识来源要全**

Wiki 编译的核心目标，是让 AI 能够完整解答软件研发全链路问题。研发类问题天然跨文档、跨代码、跨流程、跨环境，只要缺失任意一类知识载体，编译产出的 Wiki 就会形成对应知识盲区，导致 AI 理解不全、方案遗漏约束、代码生成不符合规范、风险识别不完整。因此，知识材料的完整度，直接决定研发知识库的问题解答边界与 AI 研发交付能力上限。

软件研发领域的知识来源，同样从**广度、深度**两个维度做完整保障：

### 一、广度维度：区分编译时知识 & 运行时知识

两类知识各司其职、互补覆盖：编译时知识定义「系统应该是什么、规则是什么、流程怎么执行」；运行时知识反馈「系统当前实际运行状态」。

**1. 编译时知识（固化进 Wiki，****AI** **核心上下文）**

将研发体系内相对稳定、不随瞬时运行状态变化的资产，在构建阶段预编译固化为结构化 Wiki 页面，覆盖软件研发 5 大核心载体：

- **代码资产**：源码、公共组件、工具类、依赖版本、模块结构
    
- **架构契约**：系统拓扑、模块边界、服务链路、API 接口文档与版本契约
    
- **规范文档**：编码规范、安全规范、日志规范、流程制度、质量门禁规则
    
- **质量资产**：测试用例、缺陷案例、评审卡点、上线准入标准
    
- **经验资产**：技术方案、踩坑复盘、故障预案、最佳实践与决策取舍
    

**2. 运行时知识（实时调取，不入库 Wiki）**

仅查询瞬间才能确定的动态变量，不做静态固化，由 Agent 实时工具调用获取：线上日志、运行监控、实时报错、环境配置状态、流水线实时构建结果、动态权限状态等。用于辅助 AI 做实时问题排查、现状校验与风险判断。

### 二、深度维度：结构信息 + 逻辑信息双层补齐

软件研发知识不能只沉淀“表层结构”，必须同时沉淀“底层逻辑”，否则 Wiki 只有骨架、没有灵魂。

仅收录文档、接口定义属于浅层知识，只能告诉 AI「这个功能有什么、字段是什么」；必须同步收录**代码实现逻辑、业务约束、判断条件、****分支****逻辑、改造影响、历史问题**，才能让 AI 理解：为什么这么设计、哪些不能改、改哪里会影响什么、怎么改才合规安全。

**结构信息**：目录结构、接口字段、模块划分、流程步骤、规则条目（静态骨架）

**逻辑信息**：代码计算逻辑、分支判断、约束原因、兼容策略、历史踩坑原因、评审否决依据（动态内核）

只有结构+逻辑双完备，研发 Wiki 才能真正支撑 AI 完成代码生成、变更分析、风险评审、方案设计、问题排查全场景。

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=MDk4Y2YwMTNhMzU5ZGIwMzAwNTk1ODUzOTE1YWY5ZGNfQUh0SlA3bUxNQXgzZHAydTZBTHNCYVNBSVdDaXVTSlNfVG9rZW46QVBPdWJhV1k1b1hIZVh4YUozZGNaUHVhbnlkXzE3ODI3MzUxNDM6MTc4MjczODc0M19WNA&add_watermark=true&scene_type=CCM)

## **知识构建要准**

"准"是 Wiki 编译的核心挑战。源材料本身就带噪音——注释长期未更新、文档写错口径、不同来源对同一对象的描述相互矛盾；LLM 生成时存在幻觉，容易把不确定的推断写成确定的事实；像域归属、指标聚类这类判断本身就有一定主观性。仅凭"我们要保证准确"这句口号无法解决，需要一整套覆盖事前、事中、事后的工程纪律：

- 噪音过滤：分入口和生成两道。入口阶段做粗筛，从源头剔除明显过期、低质量的材料，降低后续编译需要处理的冲突量。生成阶段做细筛，由 LLM 在写 Wiki 时识别并跳过任务代码里的调试残留、文档里的过期片段，不让噪音进入页面正文。
    
- 代码即真相：剩下的冲突需要明确的裁决规则。不同来源对同一对象描述不一致时，以任务代码为权威——注释和文档可能长期失修，但任务代码每天实际跑在生产上，代表系统当下的真实行为。这条规则把所有"以谁为准"的争议收敛到唯一答案。
    
- 生成与判断分离：LLM 在生成基础 Wiki 时，需要推断的字段强制留空，只写有源材料直接支撑的内容，不允许在生成阶段做主观推断。等所有基础页面生成完，再独立跑一轮判断阶段，基于已写入的内容综合输出候选。判断结果同时经过两道门禁：机械门禁覆盖结构、链接、格式等可机械检查的维度，未通过则阻断发布；人工门禁覆盖域归属、聚类归并这类有主观性的判断，由用户确认。代价是多一轮处理，收益是把"生成"和"判断"两类容易出错的动作彻底解耦。
    
- 证据链可追溯：每个页面在 frontmatter 中保留 `sources` 字段，逐项指向具体的源材料（原始 DDL、任务代码、文档片段）。一旦某条信息被怀疑有误，可以立即定位到原材料；用户校验 AI 答案时，也可沿证据链反查依据。可溯源是事后兜底，也是 Wiki 与"凭印象写文档"最根本的区别。
    

## 知识关系图谱

单页内容解决"一张表是什么"，但业务问题往往不是关于一张表——"改了这张表影响哪些下游""这个指标是从哪些表算出来的""这个域下有多少资产"——都是关系层面的问题。如果关系只隐含在正文段落里，每次回答都需要 LLM 重新从文本中抽取，既不稳定也不高效。

因此我们需要把关系从正文中抽出来，显式存储为图：血缘、归属、消费、引用等语义落到 frontmatter 字段，再由构建流水线统一扫描提取，沉淀为全局关系图。每条边都是结构化的、可遍历的、可计算的。

显式建图带来三个能力维度：

- 影响范围可计算：修改一张表后，沿图向下游遍历即可得到完整影响面，不依赖人工记忆。
    
- 归属关系可聚合：任何一个域包含哪些表、接口、看板，一次查询完成，支撑全景感知。
    
- 枢纽节点可识别：按引用频次（入度）排序，可以快速发现数仓中的公共依赖和关键路径。
    

关系图同时也是多路召回的基础——检索命中图上任何一个节点后，可以沿边扩展关联节点，召回关键词未命中但血缘强相关的知识。

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=YmJiZDc0ZWYzNzM0ZmQ5ZDU1ODRmYmY4ODNmMjNjNjFfM2N4UzhycGVhazAxR1dHanpEQTVSbm5uS0l5ZnZHWHdfVG9rZW46Qk9NS2J0b0h1bzJyUmV4bVFIOWNGTlVjbnBiXzE3ODI3MzUxNDM6MTc4MjczODc0M19WNA&add_watermark=true&scene_type=CCM)

## **以检索为目的**

知识的构建和组织不是独立环节，而是为检索服务的。怎么生成页面、怎么划分层级、怎么记录关系，最终都要回答一个问题：AI 在有限的上下文里能否快速找到最相关的知识。围绕这个目标，层级结构和关系图分别承担不同的职责：

- 知识聚合：把大量Wiki页面按主题进行聚合——字段聚合为指标和维度，表、接口、看板聚合为域，域按业务主题嵌套组织。聚合后，检索面从数百个分散页面收敛到少数几个域入口，AI 和人都能快速定位到目标区域。
    
- 渐进式披露：Agent 上下文有限，不可能一次加载全部知识。层级结构天然支持逐层下钻：从全景概览定位相关域，从域定位关键页面，从页面获取字段和逻辑细节。每一层按需加载，在上下文预算内尽可能传递最相关的信息。
    
- 多路召回：聚合和渐进式披露解决的是纵向定位——从全局逐层收敛到目标页面。但业务问题往往涉及横向关联：一张表的上游、一个指标的计算依赖、一个域下的全部资产。关系图在这里提供了第二条检索路径——命中一个节点后，沿边扩展到血缘相关但关键词未命中的知识，覆盖单靠文本相似度无法触达的关联页面。
    

三者配合：聚合解决信息爆炸，渐进式披露解决上下文有限，多路召回解决召回不全——这是知识库能服务 AI 检索的三个工程支点。

# 架构设计

Wiki 系统以文件为底座，但在功能上构成了一个完整的知识管理系统。其中存储层（多级文件系统）、知识模型层（Schema）、计算层（Agent 编排）是三层主干，后续章节描述的构建、检索、增量、Lint 等流程都基于这三层运行。

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=ZDM0ZDMwMDdjMmExYWQ1ZjBhMmMzNzVjNTZmZjNhYzdfTVNDelJhZnJFdGxDZEM4SzNKRE96YjFyYkc4TzFZMTZfVG9rZW46T3R1WWJReDVKbzN3eU94N1dNN2NORmxnbjhnXzE3ODI3MzUxNDM6MTc4MjczODc0M19WNA&add_watermark=true&scene_type=CCM)

其架构可以与数据库系统做如下类比：

|   |   |   |
|---|---|---|
|数据库系统|Wiki 系统|对应关系|
|存储引擎|多级文件系统|知识的物理组织和生命周期管理|
|索引|图索引 + 树索引|加速检索的辅助结构|
|DDL（建表）|Schema 定义|定义知识结构和约束|
|写表（INSERT/UPDATE）|Wiki 生成|按 Schema 写入结构化页面|
|查询（SELECT）|Wiki 检索|按索引和条件读取知识|
|约束检查|健康检查 + 验证机制|保证数据一致性和正确性|
|事务可恢复性|断点续传 + 增量构建|中断后幂等重跑，已有正确产物跳过，只补未完成部分|
|执行引擎|Agent 编排|调度计算任务，管理并行与串行|

## **多级文件系统**

知识库的生命周期跨越多个阶段：清单维护、材料抓取、Wiki 生成、关系图构建、健康检查。每个阶段产出的物料形态不同——清单是输入、原始材料是中间态、Wiki 是最终产出，需要分目录隔离，避免互相污染。多级文件系统的本质是把不同生命周期的物料放进不同目录，由目录承担状态语义。

知识库根目录由环境变量 **KB_ROOT** 指定，完整目录结构适配**软件研发全链路知识资产**，改造后结构如下：

```Plain
${KB_ROOT}/
├── pre/                   # 待处理清单 + 临时下载产物（验证后移入 raw/）
├── raw/
│   ├── ready/             # 完整可用，直接进入 Wiki 生成
│   ├── pending/           # 存在缺失或问题，需治理后晋升 ready
│   └── archive/           # 已下线或弃用，不治理也不参与生成
├── wiki/
│   ├── domains/           # 业务域、架构域分层资产
│   ├── concepts/          # 研发术语、业务概念、技术定义
│   ├── apis/              # 接口契约、入参出参、版本、上下游调用
│   ├── tables/            # 数据模型、数据表结构、字段口径
│   ├── codebase/          # 代码结构、公共组件、依赖约束、调用链路
│   ├── rules/             # 编码规范、安全规范、研发约束规则
│   ├── quality/           # 测试资产、用例、缺陷库、评审卡点、质量门禁
│   ├── sdlc/              # 研发流程、准入准出、CI/CD、分支管理规范
│   ├── lessons/           # 技术决策、方案选型、踩坑复盘、最佳实践
│   ├── ops/               # 线上运维、故障复盘、监控告警、应急预案
│   ├── security/          # 合规要求、权限模型、数据脱敏、审计规则
│   ├── graph.json         # 研发全局关系图（服务依赖/代码引用/归属关系）
│   ├── index.md           # 研发知识库全局索引
│   └── overview.md        # 研发体系全景概览
├── log/                   # 构建日志、域候选、健康检查报告、治理台账
├── tmp/                   # 跨 skill 协作的中间状态、临时生成产物
└── schema/                # 页面模板（5类契约），统一 frontmatter + 正文规范
```

按职能可以分两类：

- 主流程目录承载知识从源到产物的状态流：
    
    - `pre/` 维护待处理清单，并临时承接抓取下来的原始材料，验证通过后移入 `raw/` ；
        
    - `raw/` 按状态分流存放原始材料，供下游编译使用；
        
    - `wiki/` 存放编译完成的结构化页面。
        
    
      清单 → 原始材料 → 结构化页面，三态接力构成完整的主路径。
    
- 支撑目录服务于编译过程本身：
    
    - `log/` 提供可观测性（构建日志、健康检查报告），
        
    - `tmp/` 承载跨 skill 协作的中间状态，
        
    - `schema/` 定义页面契约（frontmatter 与正文模板）。
        
    
      两类目录互不干扰，主流程跑通即可对外发布。
    

主流程中 `raw/` 又进一步细分为三态，承担材料质量的入口保障：

- ready/：完整可用，直接进入 Wiki 生成。
    
- pending/：存在缺失或问题，需经过治理后晋升 `ready/` 。
    
- archive/：已下线或弃用，不治理也不参与生成，仅作为历史归档保留。
    

Wiki 生成阶段只读 `ready/` ，从源头杜绝低质量材料进入编译流水线，把"材料是否可用"从隐藏字段变成目录归属的物理事实。

wiki/ 子目录：

**1. wiki/domains/**：承载业务知识、架构知识，存储业务域定义、系统架构分层、模块边界、跨系统集成方案。

**2. wiki/concepts/**：统一沉淀研发术语、业务名词、技术概念，解决口径不统一、语义歧义问题。

**3. wiki/apis/**：完整承载接口契约资产，包含入参出参、版本迭代、调用方式、上下游依赖，支撑架构级影响分析。

**4. wiki/tables/**：承载数据模型资产，存储表结构、字段释义、数据口径、模型关系。

**5. wiki/codebase/**：专属代码知识目录，存放仓库结构、公共组件、工具类、代码调用链路、第三方依赖约束。

**6. wiki/rules/**：统一收纳规范知识，包含编码规范、日志规范、异常规范、代码约束体系。

**7. wiki/quality/**：承载质量知识，沉淀测试用例、自动化资产、历史缺陷、PR评审规则、上线质量门禁。

**8. wiki/sdlc/**：承载流程知识，覆盖需求、开发、评审、集成、发布、回滚全 SDLC+CI/CD 流程规范。

**9. wiki/lessons/**：沉淀经验与决策知识，包含技术选型、方案取舍、重构经验、历史踩坑复盘、优化实践。

**10. wiki/ops/**：承载运维与线上稳定性知识，包含监控、故障复盘、应急预案、环境配置、回滚策略。

**11. wiki/security/**：承载合规安全知识，包含数据安全、权限模型、脱敏规则、审计规范、行业合规约束。

**12. graph.json / index.md / overview.md**：全局顶层资产，构建研发体系知识图谱、全局索引、全景视图，支撑多跳关联、影响范围分析、智能检索。

## **Schema 即契约**

> https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing

Wiki 系统中有多个环节需要读写页面：生成器写入、图构建器提取关系、健康检查校验结构、query 检索内容。

如果每个环节对"页面长什么样"各有理解，就会出现生成器写了但检查器读不出的状况。Schema 的作用是对所有环节提供唯一的结构约定，类似微服务间的接口协议——生产者按它写，消费者按它读，任何工具用同一个 parser 就能拿到一致视图。

每个页面是 frontmatter + 正文的双层结构，两者通过 Schema 绑定，形成统一契约。frontmatter 是 YAML 格式的结构化头部，包含共性字段（title、type、description、sources、created、updated 等所有页面都有的字段）和页面特有字段（如 table 的 upstream/downstream/domain/layer，metric 的 computed_by，dashboard 的 uses_datasets 等）。这些字段承载关系和元数据，脚本可直接按字段提取，不需要解析自然语言。

正文是 Markdown 格式的语义内容，每种页面类型定义了固定的章节模板（如 table 页面包含"业务背景 / 加工逻辑 / 字段说明 / 下游 / 使用建议"五个章节）。正文承载业务背景、加工口径、字段说明这些需要 LLM 理解的内容，供检索和问答使用。

正文中的 `[[表名]]` Wikilink 引用是 frontmatter 关系之外的兜底机制。frontmatter 记录的是显式声明的强关系（血缘、归属、消费），Wikilink 覆盖的是行文中提到但未落到字段里的弱关联，图构建器会扫描这些链接生成 `wikilink` 边，确保关系图不遗漏正文中隐含的引用。

## **Agent 编排：编排层与干活层分离**

Wiki 编译是一个多阶段、多类型的任务：材料预处理、基础页面生成、高阶聚合、图构建、健康检查，每个阶段的输入输出差异大，且 LLM 调用是主要时间瓶颈。如果用一个大 skill 串行处理所有事情，既无法并行加速，也难以独立调试某个阶段的问题。因此系统采用编排层与干活层分离的架构——编排器负责调度和协调，干活的 skill 各自只关心自己那一段的逻辑。

整个 Wiki 系统由 7 个 skill 组成，编排架构如下：

```Markdown
                       wiki-orchestrator (编排层)
                                  │
    ┌─────────┬───────┼───────┬─────────┬──────────┐
    ▼               ▼            ▼            ▼               ▼                ▼
  material          base        advanced      graph        health             query
  -prep             -gen         -gen          -builder      -check

 (4 子模块)    (3+2 阶段)
```

编排层（wiki-orchestrator）只做四件事：意图路由（识别用户在做哪个 Phase）、用户确认（域归属、看板归属、生成范围等关键决策点）、子 Agent 调度（spawn 并行或串行）、结果汇报（聚合各 skill 输出）。它不读原始材料、不写 Wiki 文件、不做 LLM 内容生成——职责严格收敛在"调度"这一层。

干活层的拆分遵循高内聚、低耦合原则：

- 高内聚——每个 skill 内部覆盖的所有子任务输入输出来源相同、执行模式相近，整体流程对所有对象类型一致，只在具体实现上按类型差异化（类似代码开发中的抽象接口和具体实现）。例如 wiki-material-prep 内部 5 类对象共用"读清单 → 调元数据接口 → 验证 → 三态分流"流程，wiki-base-generator 内部 4 种页面共用"扫描现状 → 批间串行批内并行生成 → 校验 → 落盘"流程，新增一类对象或页面只需补一个实现模块，流程框架不变。
    
- 低耦合——skill 之间不直接调用，仅通过文件系统约定的目录交互（前一个 skill 把产出落到约定目录，后一个 skill 读这个目录），任何 skill 都可以独立运行。
    

基础 Wiki 和高阶 Wiki 的拆分正是后一类粒度的边界，是干活层切分中最关键的一刀：

|   |   |   |
|---|---|---|
|维度|基础 Wiki|高阶 Wiki|
|性质|原子知识单元|聚合知识单元|
|类型|表、接口、数据集、概念|域、看板、指标、维度、index、overview|
|输入来源|raw/ready/ 中的源材料|已落盘的基础 Wiki|
|生成方式|一对一映射（每个对象生成一页）|多对一聚合（多对象按主题归并成一页）|
|依赖关系|不依赖其他 Wiki|必须等基础 Wiki 全部落盘|

两者属于天然的两个阶段，分开建模才能让"原子生成"和"聚合归并"各自独立优化、独立调试。

综合上述拆分原则，干活层的 6 个 skill 各自覆盖编译检索流水线的一个阶段：

|   |   |   |
|---|---|---|
|Skill|覆盖阶段|职责|
|wiki-material-prep|Phase 0 材料预处理|维护清单、抓取 DDL 和任务代码、验证分流|
|wiki-base-generator|Phase 1 基础生成|生成表、接口、数据集、概念四种基础页面|
|wiki-advanced-generator|Phase 1 高阶生成|生成域、看板、指标、维度、index、overview|
|wiki-graph-builder|Phase 1 图构建|扫描 frontmatter 和 Wikilink，沉淀关系图|
|wiki-health-check|Phase 2 健康检查|执行结构、链接、格式等多项校验|
|wiki-query|运行时检索|检索页面、查询血缘、关键词搜索|

每个 skill 只关心自己的输入输出契约，不感知其他 skill 的内部实现。

以上拆分（编排/干活两层 + 干活层 6 个 skill）共同带来三个收益：

- 可并行：LLM 调用是主要时间瓶颈，分离后凡是数据不依赖的步骤都可以 spawn 子 Agent 并行执行（如基础生成的批内并行、高阶生成的"域 + 看板 + 指标维度"三路并发），编译耗时显著下降。
    
- 可独立调试：某个阶段出错时只需重跑对应的 skill，不必从头走完整流水线。每个 skill 内聚度高，输入输出边界清晰，问题定位成本低。
    
- 可单独复用：任何 skill 都可以脱离编排器独立调用——比如只跑健康检查验证现有 Wiki、只跑 query 做检索，不必触发完整构建。
    

# 知识编译流水线

编译流水线分为三阶段——Phase 0 材料预处理、Phase 1 Wiki 生成（基础生成 + 高阶生成 + 图构建）、Phase 2 健康检查。每个阶段都有明确的输入、输出和处理逻辑，下面依次展开。

![](https://nio.feishu.cn/space/api/box/stream/download/asynccode/?code=Nzc3MGMyNDFkNzVkZWJjMWRiMGQ3MzEwMTYxYjU1NzNfd0tRNHh5Tmo5VFZSSmdDOXJzd1pCY0djenRxWmVBUWhfVG9rZW46U29YR2JhaHJObzN1WlR4ODJXUGNISVZubkNiXzE3ODI3MzUxNDM6MTc4MjczODc0M19WNA&add_watermark=true&scene_type=CCM)

## **Phase 0：材料预处理**

Phase 0 负责把源材料从外部系统抓取下来，经过验证和分流，作为 Phase 1 编译的输入。

流程分为五步：

1. 用户提供 9 类对象清单（接口、文档）。
    
2. LLM 解析清单内容并写入对应的 CSV 文件。
    
3. 脚本根据清单批量调用元数据接口抓取 DDL、任务代码、看板配置、接口配置、文档原文。
    
4. 脚本验证每个对象的材料完整性。
    
5. 按结果三态分流到 `raw/ready/`、`raw/pending/`、`raw/archive/`。
    

其中 LLM 仅在第二步介入（把自然语言输入转为结构化清单），其余环节都是确定性脚本。

其中 LLM 仅在第二步介入（把自然语言输入转为结构化清单），其余环节都是确定性脚本。

Phase 0 在设计上有三个关键考量：

- **全脚本化执行**：抓取、验证、分流是确定性逻辑，不依赖 LLM——避免了幻觉风险，结果可重放可复现，且不消耗 token。Phase 0 处理的是机械性高、判断性低的任务（抓 DDL、对账、移文件），脚本化是更合理的选择。
    
- **脚本验证前置**：材料抓取后并不直接进入 ready，必须先经过完整性校验（如表必须同时有 DDL 和任务代码、命名规范、内容非空），未通过的进入 pending 等待治理。质量门禁前置在入口，避免噪音材料污染后续编译。
    
- **支持断点续传**：抓取大批材料时网络异常或接口限流难以避免，断点续传可以从上次中断位置继续，不必重头抓所有对象——这是整体架构"事务可恢复性"在 Phase 0 的具体落点。
    

完成后等待用户确认材料的分流决策，确认通过后进入 Phase 1 基础生成。

## **Phase 1 基础：基础 Wiki 生成**

Phase 1 基础阶段负责把 `raw/ready/` 中的源材料编译为 4 种基础 Wiki 页面——表、接口、数据集、概念。

流程分为三步：扫描现状（对比已有 Wiki、新增材料、sources 一致性，确定本次需要生成、修复、跳过的对象集合）；按"批间串行、批内并行"的策略生成基础 Wiki 页面（含 frontmatter + 正文）；所有页面生成完毕后跑一轮统一校验，未通过的标记重生成。基础 Wiki 落盘后再独立执行域候选判断，输出候选列表供用户确认，回填 `domain` 字段。

基础 Wiki 生成阶段有四个关键设计：

- **批间串行、批内并行**：每批 5 个对象，批内 spawn 5 个独立子 Agent，每个子 Agent 只读自己那张表的源材料、独立生成。这种切分有两层价值——一是并发提速，5 路并行明显快于串行；二是上下文隔离，每个子 Agent 的 LLM 上下文只承载一个对象的信息，避免多对象拼接时 LLM 张冠李戴的幻觉。批的大小（5）是平衡 LLM 配额、错误恢复成本、并发收益的工程折中。
    
- **生成完后统一校验**：所有基础 Wiki 生成完毕后，由验证脚本统一校验产出页面——frontmatter 字段是否符合 Schema 约束（必填项齐全、枚举值合法、类型正确），正文表结构列出的字段是否真实存在于 DDL（防止 LLM 幻觉出不存在的列）。校验未通过的页面会被标记重生成。这是页面级的字段一致性校验，与 Phase 2 全局健康检查互为前后两道关卡。
    
- **生成与判断分离**：基础生成阶段 `domain` 等需要推断的字段一律留空，避免 LLM 在尚未掌握全局信息时做主观判断；所有基础页面落盘后再独立跑判断阶段，基于已写入的内容综合输出候选，由用户确认后回填——具体见 3.4。
    
- **增量感知**：扫描现状后只对真正发生变化的对象（新增材料、sources 不一致）触发生成，已有且一致的页面跳过。这是 Wiki 长期维护成本可控的前提。
    

基础 Wiki 落盘后，进入高阶聚合阶段。

## **Phase 1 高阶：高阶 Wiki 生成**

Phase 1 高阶阶段把已落盘的基础 Wiki 按业务主题聚合，产出 6 种聚合页面：域、看板、指标、维度、index、overview。

整个过程由一条 DAG 驱动——一阶段三路并行，二阶段串行汇聚：

- **一阶段（三路并行）**：
    
    - **域页面**：从基础 Wiki 的 `domain` 字段反查抽出域列表，按层级生成 `domains/{parent}/{leaf}.md`。
        
    - **看板页面**：基于数据集 Wiki 生成，对每个看板的域归属生成候选由用户确认。
        
    - **指标与维度**：脚本字段聚类 → 子 Agent DWD 分析 → 用户确认归并 → Wiki 生成 → 脚本一致性校验五个步骤。
        
- **二阶段（串行汇聚）**：必须等一阶段就绪才能跑。
    
    - **index.md**：每个一级域并行写章节，再合并为全局索引。
        
    - **overview.md**：基于域页面 + 表 frontmatter 产出全景概览。
        

这条 DAG 的蕴含两层设计意图：

- **并发最大化**：阶段三路无依赖的步骤齐头并进，二阶段有依赖的步骤等齐再跑，在依赖约束下尽量挖出并发收益。
    
- **关键节点嵌入审核**：看板的域归属、指标维度的聚类归并以及一致性校验都嵌在 DAG 节点中，由用户确认或脚本兜底，而不是事后补丁，把"机器无法独自判断"和"机器可机械验证"两类工作显式纳入流程。
    

高阶页面之所以能这样组织，关键在于**聚合靠 frontmatter 字段反查**。域页面、指标页面的内容来自基础 Wiki 的 frontmatter 字段聚合（如域页面列出"我下面有哪些表"是反查所有 `domain` 字段指向自己的表），不需要重新解析正文。这正是 4.2 frontmatter 设计的直接收益——单页关系字段化让跨页聚合可以低成本完成。

至此基础和高阶 Wiki 全部落盘，关系字段已就位，下一步进入图构建。

## Phase 1 链接：图构建

Phase 1 链接阶段产出全局关系图 `graph.json`，由节点和边两部分组成。 节点对应每一篇 Wiki 页面，仅记录 ID、类型与文件路径，不存储冗余内容；页面详情由程序按需读取对应文件的 Frontmatter。

---

一、节点定义（共 6 种，严格匹配 6 套 Schema 模板）

|   |   |   |
|---|---|---|
|节点类型|目录路径前缀|对应 Schema 模板|
|domain|domains/|Domain 域模板|
|entity|apis/、tables/|Entity 实体契约模板|
|code|codebase/|Code 代码资产模板|
|rule|rules/、sdlc/、security/|Rule 规范约束模板|
|case|quality/、lessons/、ops/|Case 经验 & 案例模板|
|concept|concepts/|Concept 概念词典模板|

> 节点 JSON 极简结构：

```JSON
{"nodes": [{"id": "页面唯一标识","node_type": "domain|entity|code|rule|case|concept","file_path": "wiki/domains/xxx.md"}]}
```

---

二、边定义：共 9 种正向关系，分为四大语义类别

所有关系均从 Frontmatter 结构化字段自动提取，全程无 LLM 依赖；正文 Wikilink 作为兜底弱关系。

- 第一类：归属层级关系（组织结构）
    

|   |   |   |   |
|---|---|---|---|
|边类型|业务含义|流向|来源 Frontmatter 字段|
|belongs_to|子域 / 接口 / 代码 / 规则归属到父业务域|子节点 → 父域|parent_domain / domain|

- 第二类：依赖调用关系（变更影响分析核心）
    

|   |   |   |   |
|---|---|---|---|
|边类型|业务含义|流向|来源 Frontmatter 字段|
|calls_upstream|服务 / 接口调用上游依赖|当前实体 → 上游服务 / 接口|upstream|
|calls_downstream|服务 / 接口被下游消费|当前实体 → 下游服务 / 接口|downstream|
|code_import|代码模块引用其他组件|当前代码 → 被依赖代码库|call_out|

- 第三类：约束与引用关系（规则绑定）
    

|   |   |   |   |
|---|---|---|---|
|边类型|业务含义|流向|来源 Frontmatter 字段|
|governed_by|实体 / 代码受规范约束|业务资产 → 对应规则|related_rules|
|derived_from|案例 / 缺陷关联到对应接口与代码|复盘案例 → 关联实体 / 代码|related_entity|

- 第四类：兜底弱关联（正文隐性引用）
    

|   |   |   |   |
|---|---|---|---|
|边类型|业务含义|流向|来源|
|wikilink|文档内手动链接兜底|引用页面 → 被引用页面|正文所有 [[页面名称]]|

完整 9 条正向边汇总表

1. `belongs_to` — 归属父域
    
2. `calls_upstream` — 调用上游服务
    
3. `calls_downstream` — 被下游服务调用
    
4. `code_import` — 代码组件互相引用
    
5. `governed_by` — 资产受某条规则管控
    
6. `derived_from` — 案例追溯到对应代码 / 接口
    
7. `wikilink` — 正文链接兜底
    

---

三、图自动化构建流程（纯脚本执行，无大模型）

1. 全目录扫描 遍历 `wiki/` 下全部 `.md` 文件，自动生成节点列表，根据文件路径自动识别 6 种节点类型。
    
2. 结构化字段抽取（强关系优先）
    

- 读取每一页 YAML Frontmatter；
    
- 按字段与边类型一一映射，批量生成强关系边：
    
    - `domain/parent_domain` → `belongs_to`
        
    - `upstream/downstream` → `calls_upstream` / `calls_downstream`
        
    - `call_out` → `code_import`
        
    - `related_rules` → `governed_by`
        
    - `related_entity` → `derived_from`
        

3. 补充弱关系边 逐行解析 Markdown 正文，匹配所有 `[[xxx]]` Wikilink，自动生成 `wikilink` 引用边，补齐自然语言里没有写入元数据的隐性关联。
    
4. 输出产物 合并节点 + 所有边，写入 `wiki/graph.json`，为后续多跳血缘分析、变更影响范围检索提供图数据。
    

---

四、graph.json 最简结构示例

```JSON
{"nodes": [{"id": "trade-domain", "node_type": "domain", "file_path": "wiki/domains/trade.md"},{"id": "pay-api", "node_type": "entity", "file_path": "wiki/apis/pay.md"}],"edges": [{"edge_type": "belongs_to","source_id": "pay-api","target_id": "trade-domain"},{"edge_type": "wikilink","source_id": "pay-api","target_id": "trade-domain"}]}
```

---

五、和你 9 大知识资产的配套价值

1. 依靠归属边，自动形成业务域树形结构；
    
2. 依靠调用 & 代码引用边，一键完成代码变更上下游影响分析；
    
3. 依靠规则绑定边，自动给每一行代码匹配对应的编码规范、安全红线；
    
4. 依靠案例追溯边，把历史缺陷、故障复盘自动关联到对应接口与代码；
    
5. 强元数据 + Wikilink 双保险，不会遗漏任何文档关联，完美支撑评审 Agent 做风险自动校验。
    

图构建完成后会**反哺 Wiki**：基于血缘类正向边反向计算每张表的下游列表，回填到 frontmatter 的 `downstream` 字段。只读 Wiki 不读图的工具也能直接拿到下游信息，避免轻量消费场景强制依赖 `graph.json`。

"**只存正向边 + 反向按需 + 回填关键反向字段 + 文件存储**"带来了三个收益：

- **存储与一致性**——反向边信息完全冗余于正向边，存两份必然带来双向同步的一致性负担。只存正向边将存储减半，一致性问题随之消失；运行时需要反向访问时按需构建索引，开销可控（O(E)）。
    
- **消费灵活性**——图供需要全局遍历的场景使用（多跳血缘、影响范围分析），反哺到 frontmatter 的 `downstream` 供只看单页的轻量场景使用，两类消费方各取所需。
    
- **轻量化**——关系图以单个 JSON 文件（`graph.json`）存储，无需部署和维护图数据库，任何工具直接读取，可随代码仓库版本管理，适合当前规模的知识库。
    

编译产出已完整，最后一步是健康检查兜底。

## **Phase 2：健康检查**

Phase 2 健康检查是编译流水线的最后一道质量门禁，对编译产物做全局对账，决定本次构建是否对外发布。

健康检查覆盖结构和格式两类维度，共 6 项：

|   |   |
|---|---|
|检查项|检查内容|
|数量一致性|DDL、Wiki 页面、graph.json 节点三方对账，确保对象数量对齐|
|结构完整性|按页面类型校验 frontmatter 字段集（必填项齐全、类型正确、枚举值合法）|
|链接有效性|Wikilink 断链检测、孤岛页面检测（无入边的页面）|
|Domain 格式|域字段是否符合层级正则（一级域/二级域/...）|
|YAML 语法|graph.json 和所有页面 frontmatter 的 YAML 语法合法性|
|Graph 完整性|节点路径合法、边类型在白名单、边两端节点存在|

任意一项检查未通过都视为本次编译失败，输出诊断报告到 `log/wiki-health-check-{timestamp}.md`，标记具体不通过的对象和原因，未通过的编译产物不对外发布。

健康检查与流水线前序阶段构成两道校验关卡：

- 5.2 的"生成完后统一校验"是页面级、生成时的字段一致性检查（如表结构列出的字段是否真实存在于 DDL）
    
- 5.5 是全局、构建后的对账与契约检查（如 Wiki 总数与 DDL 数量、`graph.json` 的边是否都连接到合法节点）。
    

两者互补——前者保证单页正确，后者保证整体一致，共同实现 3.4 提出的"正确性可度量"和 4.2 提出的"Schema 即契约"在流水线层面的兜底。

健康检查通过后，本次编译产出对外发布，一次完整的 Wiki 编译流水线结束。

# 知识检索

  

  

# **Schema模版**

所有页面统一双层结构：YAML Frontmatter + Markdown正文，全局通用字段在每套模板前置继承。

全局公共字段（所有6套模板必带，统一Parser解析）

```YAML
# 全局通用Frontmatter
title: ""
type: ""                # 页面类型，和模板一一对应：domain / entity / code / rule / case / concept
description: ""
sources: []             # 原始材料来源（代码文档/PR/故障记录等）
created: ""
updated: ""
owner: ""               # 责任人
tags: []
```

## 模板1：Domain 域模板（业务域/架构域）

适用目录：`wiki/domains/`

覆盖：业务域、系统架构分层、模块边界、跨系统集成方案

```YAML
title: ""
type: "domain"
description: ""
sources: []
created: ""
updated: ""
owner: ""
tags: []

# 域特有字段
domain_level: "business|architecture"   # 业务域 / 架构域
parent_domain: ""                      # 父域，用于构建层级关系
child_domains: []                      # 子域列表
modules: []                            # 下辖模块清单
dependent_domains: []                  # 依赖的其他域（强关系，自动录入graph.json）
scope_boundary: ""                     # 边界范围，界定权责

# Markdown 正文固定章节
## 1. 域全景概述
业务目标、系统定位、总体边界。

## 2. 层级与模块划分
拆分下属模块与职责边界。

## 3. 上下游依赖关系
关联外部域、依赖服务、外部集成系统。
[[关联域名称]]

## 4. 约束与设计原则
架构约束、业务红线、迭代规则。

## 5. 变更准入门槛
本域内需求、改造的准入评审条件。
```

## 模板2：Entity 实体契约模板（接口API / 数据表）

适用目录：`wiki/apis/`、`wiki/tables/`

覆盖：API接口契约、数据模型、表结构、字段口径、版本管理

```YAML
title: ""
type: "entity"
description: ""
sources: []
created: ""
updated: ""
owner: ""
tags: []

# 实体特有字段
entity_category: "api|table"
version: ""
status: "active|deprecated|archived"
domain: ""                     # 归属业务域
upstream: []                   # 上游依赖（强血缘，自动构建图谱）
downstream: []                 # 下游消费方
fields: []                     # 字段清单：name,type,comment,constraint
contract_changelog: []         # 版本变更记录

# Markdown 正文固定章节
## 1. 契约基本信息
用途、归属域、当前版本、生命周期状态。

## 2. 结构定义
API入参出参 / 数据表DDL、字段释义、数据口径。

## 3. 上下游血缘
上游来源系统，下游消费服务。
[[上游实体名称]] [[下游实体名称]]

## 4. 变更约束
字段兼容策略、版本升级规则、不允许随意修改的字段清单。

## 5. 使用示例与风险说明
调用样例、改造风险、常见误用场景。
```

## 模板3：Code 代码资产模板

适用目录：`wiki/codebase/`

覆盖：仓库结构、公共组件、工具类、调用链路DeepMap、依赖版本、代码所有权

```YAML
title: ""
type: "code"
description: ""
sources: []
created: ""
updated: ""
owner: ""
tags: []

# 代码特有字段
repo_name: ""
module_path: ""
component_type: "library|service|util"
dependencies: []                # 第三方依赖版本约束
call_in: []                     # 被哪些代码调用
call_out: []                    # 内部调用其他模块
modify_scope: []                # 允许修改的代码范围
code_owner_group: []            # 代码归属人

# Markdown 正文固定章节
## 1. 代码模块简介
模块能力、业务定位、仓库路径。

## 2. 目录结构与组件清单
核心类、公共工具、对外暴露能力。

## 3. 调用链路图谱
内部引用关系、外部调用依赖。
[[关联代码模块]]

## 4. 依赖版本约束
第三方包版本锁、禁止升级的依赖清单。

## 5. 修改规范与禁忌
不允许改动的核心逻辑、重构准入条件、兼容性要求。
```

## 模板4：Rule 规范约束模板

适用目录：`wiki/rules/`、`wiki/sdlc/`、`wiki/security/`

覆盖：编码规范、安全规范、SDLC流程、CI/CD制度、权限合规、监管红线

```YAML
title: ""
type: "rule"
description: ""
sources: []
created: ""
updated: ""
owner: ""
tags: []

# 规则特有字段
rule_category: "coding|security|sdlc|compliance"
enforce_level: "block|warn|suggest"   # 阻断/警告/建议（用于自动化门禁）
applicable_domain: []                # 适用业务域
check_items: []                      # 可自动化校验的检查项
related_rules: []                    # 关联其他约束条款

# Markdown 正文固定章节

## 1. 规则适用范围
生效场景、适用团队、生效门槛。

## 2. 约束条款原文
标准化条文，可直接注入AI生成与评审流程。

## 3. 校验执行方式
人工评审项 + 自动化卡点配置。
[[关联规则文档]]

## 4. 违规后果
阻断合并、打回整改、质量扣分机制。

## 5. 例外豁免条件
允许特批的场景与审批流程。
```

## 模板5：Case 质量&经验案例模板

适用目录：`wiki/quality/`、`wiki/lessons/`、`wiki/ops/`

覆盖：测试用例、缺陷记录、PR评审案例、技术方案复盘、线上故障复盘、应急预案、踩坑经验

```YAML
title: ""
type: "case"
description: ""
sources: []
created: ""
updated: ""
owner: ""
tags: []

# 案例特有字段
case_type: "defect|review|outage|solution|practice"
related_entity: []                # 关联接口/代码/域
root_cause: ""
lessons_summary: ""
prevent_action: []                # 后续预防措施
link_rules: []                    # 对应落地的规范规则

# Markdown 正文固定章节
## 1. 事件背景
问题现象、发生场景、版本环境。

## 2. 根因分析
技术原因、流程漏洞、人为疏漏。
[[关联代码/接口文档]]

## 3. 整改方案
临时止血 + 长期根治手段。

## 4. 沉淀经验与避坑要点
提炼可复用的最佳实践与禁忌事项。

## 5. 固化机制
转化为评审卡点、自动化规则、用例。
```

## 模板6：Concept 概念词典模板

适用目录：`wiki/concepts/`

覆盖：业务术语、技术名词、口径定义，统一全知识库语义

```YAML
title: ""
type: "concept"
description: ""
sources: []
created: ""
updated: ""
owner: ""
tags: []

# 概念特有字段
category: "business_term|tech_term"
synonyms: []                     # 同义词，用于检索归一化
antonyms: []
related_concepts: []              # 关联名词

# Markdown 正文固定章节
## 1. 标准释义
唯一权威定义，全团队统一口径。

## 2. 业务场景
在哪类需求、代码、评审中会使用该名词。
[[关联域/规则]]

## 3. 易混淆概念辨析
区分近似名词，避免理解歧义。

## 4. 使用约束
书写口径、缩写规范。
```

配套工程说明（贴合OKF开放知识格式）

1. 6类type严格固定：`domain / entity / code / rule / case / concept`，所有生成器、图构建、健康检查共用同一枚举；
    
2. Frontmatter里的数组、关联字段会自动被graph-builder抓取，生成强关系边；
    
3. 正文内 `[[页面名称]]` Wikilink 作为弱关联兜底，补齐正文里的隐性引用；
    
4. 健康检查Skill可以自动校验：必填字段不为空、关联页面必须存在、枚举值合法，实现契约自动化校验。