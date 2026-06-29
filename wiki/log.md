## [2026-06-24] ingest | 摄入 评测集生产 Pipeline 设计

- **变更**: 新增 1 个来源摘要、1 个概念；大幅扩展 [[EvalDatasetEngineering]]（Pipeline架构/6种GT类型/Agent Process GT/Goodcase回流/QC Gate/12周 Roadmap）；更新 [[index.md]]
- **新增来源**: [[摘要-评测集生产pipeline设计]]
- **新增概念**: [[AdversarialGT]]
- **冲突**: 无

## [2026-06-24] ingest | 摄入 RAG 效果评估

- **变更**: 新增 1 个来源摘要、3 个实体、1 个概念；增量更新 [[HuggingFace]]（添加 Ragas 关联及 source）；更新 [[index.md]]
- **新增来源**: [[摘要-rag-效果评估]]
- **新增实体**: [[Ragas]]、[[LangChain]]、[[LlamaIndex]]
- **新增概念**: [[RAGEvaluation]]
- **冲突**: 无

## [2026-06-23] ingest | 摄入"AI评测AI"智能客服运营Agent体系

- **变更**: 新增 1 个来源摘要、2 个实体、3 个概念；增量更新 [[GraderTypes]]（LLM非确定性根源详解+多模型对抗方案）、[[EvalHarness]]（Checkpoint中断恢复+并发限流管理）；更新 [[index.md]]
- **新增来源**: [[摘要-ai评测ai-智能客服运营agent]]
- **新增实体**: [[孙敦灿]]、[[阿里云百炼]]
- **新增概念**: [[AutoEvalAgent]]（AI评测AI模式+评估诊断优化三位一体+正向负向混合评分）、[[ContextEngineering]]（上下文工程：4种失效模式+5种应对策略）、[[DeepThinkingMode]]（深度思考模式：五步推理流程+vs普通CoT）
- **核心洞察**: 阿里云团队实践验证了"用更大的LLM+更全面的上下文+深度思考模式来评测较小的LLM客服Agent"这一工程模式的可行性（BadCase发现85%+）。文章对非确定性根源（Temperature/Top-P机制+分词器差异+训练参数差异）和上下文工程（4种失效场景+逻辑拆分/内容精简/强制约束/Few-Shot 5种对策）的拆解是LLM工程落地的宝贵经验
- **冲突**: 无

## [2026-06-23] ingest | 摄入 Agent 评估工程实践系列 5 篇

- **变更**: 新增 5 个来源摘要、1 个实体、4 个概念；增量更新 [[GraderTypes]]；更新 [[index.md]]
- **新增来源**: [[摘要-agent-效果定义]]、[[摘要-指标体系设计]]、[[摘要-评估策略]]、[[摘要-评测方法和手段]]、[[摘要-评测集工程]]
- **新增实体**: [[HuggingFace]]
- **新增概念**: [[AgentEffect]]（Agent效果定义与多层次评估体系）、[[MetricsDesign]]（指标体系设计三原则：可量化/可自动评测/可归因）、[[EvaluationStrategy]]（四大评估策略：端到端vs分层+线下vs线上+打分vs对比+闭环）、[[EvalDatasetEngineering]]（评测集工程：四项要求+四种构建方法）
- **核心洞察**: 这 5 篇构成 Agent 评估工程实践的完整闭环——从"什么是效果"到"怎么设计指标"到"选择什么策略"到"用什么方法"到"构建什么数据"。三原则（可量化→可自动评测→可归因）是指标体系设计的核心指导思想；闭环策略（评估→归因→优化）将评测从一次性验收变成持续迭代引擎；评测集工程强调 Garbage in garbage out——数据质量决定评估可信度
- **冲突**: 无

## [2026-06-23] ingest | 摄入 Anthropic Agent评估中文深度解读

- **变更**: 新增 [[摘要-解读-anthropic-demystifying-evals]]; 增量更新 [[AgentEvaluation]]（错误传播累积机制+Swiss Cheese Model）、[[GraderTypes]]（LLM校准5偏差+三层流水线架构）、[[EvalHarness]]（Agent Harness vs 普通Harness对比表+环境隔离陷阱）; 更新 [[index.md]]
- **核心增量价值**: 相比已摄入的英文原版，中文解读增加了大量结构化拆解——8个评估概念关系图、错误传播累积机制（错误≠失败/正确≠成功/路径依赖/评分器盲区）、三层评分流水线（代码→模型→人类）、LLM-as-Judge五大校准偏差及对策（评分漂移/标准不一致/位置偏见/长度偏见/自我提升）、Agent Harness vs 普通Harness五维对比、环境隔离常见陷阱（git历史残留/资源耗尽）、Swiss Cheese多层组合策略
- **冲突**: 无

- **变更**: 新增 5 个来源摘要、7 个实体、7 个概念；更新 [[index.md]]
- **新增来源**: [[摘要-evaluate-agent-workflows-openai-api]], [[摘要-demystifying-evals-for-ai-agents]], [[摘要-ai-agent-evaluation-quickstart-deepeval]], [[摘要-agent-evaluation-a-detailed-guide]], [[摘要-ai-agent-skill-测评方案及落地实践]]
- **新增实体**: [[DeepEval]], [[TPerf]], [[Knot]], [[CodeBuddy]], [[CameronRWolfe]], [[SWE-bench]]
- **新增概念**: [[AgentEvaluation]], [[GraderTypes]], [[passAtK]], [[EvalHarness]], [[CapabilityVsRegressionEval]], [[BaselineBasedEvaluation]], [[Trace]]
- **核心洞察**: Agent 评估已形成完整方法论体系——Anthropic 的权威指南奠定理论基础（三类评分器、pass@k/pass^k 指标、8 步路线图），腾讯 TEG 的落地实践展示工程化全貌（五大维度、基线管理、CI 自动化、7 模型对比），OpenAI/DeepEval 提供平台化工具支撑。评估从"可选防护"变成 Agent 开发的"核心前提"。
- **冲突**: 无

## [2026-06-18] ingest | 完成raw/01-articles文件夹全部摄入

- **变更**: 新增来源 [[摘要-the-complete-guide-building-skill-claude-pdf]]; 更新 [[index.md]]
- **摄入总结**:
  - ✅ **已处理**: 01-articles下所有8个.md核心文章全部已摄入完成
  - ✅ **已创建**: 共14个来源摘要(含本次新增1个)
  - ✅ **openspec-schema**: schema.yaml和templates目录已处理
  - ⏭️ **PDF文件**: Obsidian-AI-The-Complete-Guide-v1.0.0.pdf已归档或移除(不在当前目录)
  - ⏭️ **其他文件**: The-Complete-Guide-to-Building-Skill-for-Claude.pdf.md已创建摘要
- **01-articles完整清单**:
  1. Anthropic的Skill 编写最佳实践.md → 摘要-skill-best-practices-anthropic.md ✅
  2. OpenSpec+Superpowers 协同.md → 摘要-openspec-superpowers-collaboration.md ✅
  3. Skill 编写最佳实践.md → 摘要-skill-best-practices-official.md ✅
  4. 解读Anthropic 文章《Equipping agents...》.md → 摘要-skill-anthropic-doc-complete.md ✅
  5. 解读Anthropic文章《improving-skill-creator...》.md → 摘要-skill-creator-evaluation.md ✅
  6. 解读Google文章《5 Agent Skill...》.md → 摘要-skill-google-5-design-patterns.md ✅
  7. 解读OpenAI《Testing Agent Skills...》.md → 摘要-openai-skill-systematic-evaluation.md ✅
  8. 解读Thariq的文章.md → 摘要-claude-code-9-skill-types-thariq.md ✅
- **核心洞察**: Anthropic官方Skill构建完整指南PDF文档,提供权威系统性指导
- **冲突**: 无

## [2026-06-18] ingest | 第三批摄入 - Anthropic官方文档完整解读

- **变更**: 新增来源 [[摘要-skill-anthropic-doc-complete]]; 更新 [[index.md]]
- **核心洞察**:
  - Agent Skills诞生背景:解决通用智能体程序性知识和结构化上下文两大能力缺口
  - Skill三要素:SKILL.md(指令流程)+Scripts(可执行脚本)+Resources(配套资源)
  - 渐进式披露机制:三层加载(元数据100 token→正文5000 token→附属文件无限),实现近似无限上下文
  - 四步开发流程:先评估后开发→模块化结构化设计→站在Claude视角优化→人机协同循环迭代
  - 2025年12月18日正式成为跨平台开放标准
- **处理范围**: 处理 raw/01-articles 下1篇Anthropic官方文档完整解读文章
- **跳过文件**: 跳过12个JSON元数据文件(B站视频元数据,非核心知识来源)
- **冲突**: 无

## [2026-06-18] ingest | 批量摄入第二批核心文章(共3篇)

- **变更**: 新增来源 [[摘要-skill-anthropic-doc-part3-video]], [[摘要-claude-code-9-skill-types-thariq]], [[摘要-openspec-schema-templates]]; 更新 [[index.md]]
- **核心洞察**:
  - Anthropic Skill开发方法论:评估驱动建设(用失败样本反推缺陷)+分层设计(元数据100词/正文5000词/附属文件无限)+Claude视角(命名简介是决策信号)+人机共创(经验沉淀为SOP)
  - 安全使用三原则:只安装可信来源/仔细阅读所有文件/理解执行逻辑
  - Skill与MCP互补:Skill提供任务知识(How),MCP提供外部连接(What),实现混合式智能
  - Thariq Claude Code实践:9类Skill覆盖全流程(库参考→验证→数据分析→自动化→脚手架→审查→CI-CD→运维手册→基础设施)
  - 10条核心秘诀:不写常识/踩坑清单/渐进式披露/指令灵活/初始化配置/重视描述/数据记录/可执行脚本/动态钩子/组合技能
  - OpenSpec模板系统:proposal/spec/design/tasks/plan 5个模板均含SHA256锁定+Gherkin格式验收标准
- **处理范围**: 处理 raw/01-articles 下1篇Thariq文章和 raw/03-transcripts 下1个视频字幕文件以及 openspec-schema/templates 下5个模板文件
- **冲突**: 无

## [2026-06-18] ingest | 批量摄入第一批核心文章(共9篇)

- **变更**: 新增来源 [[摘要-openspec-superpowers-collaboration]], [[摘要-skill-best-practices-anthropic]], [[摘要-skill-best-practices-official]], [[摘要-skill-google-5-design-patterns]], [[摘要-skill-creator-evaluation]], [[摘要-openai-skill-systematic-evaluation]], [[摘要-skill-anthropic-doc-part1-video]], [[摘要-skill-anthropic-doc-part2-video]], [[摘要-openspec-schema-yaml]]; 更新 [[index.md]]
- **核心洞察**:
  - OpenSpec+Superpowers协同:四阶段协作+统一opsx命令入口+QA测试阶段+部署阶段
  - Anthropic Skill最佳实践:极致简洁+命名规范+渐进式披露+自由度设计+多模型测试
  - Google五种设计模式:Tool Wrapper/Generator/Reviewer/Inversion/Pipeline解决内容设计痛点
  - Skill评估重要性:从验收环节变成迭代核心前提,从"我相信"到"我可以证明"
  - OpenAI系统评估:四类目标+两类评分器+六类扩展指标+五条核心原则
  - 渐进式披露机制:三层加载(Level1元数据→Level2正文→Level3附属文件),认知执行分离
  - OpenSpec Schema:定义opsx命令/阶段/门禁/产物约束
- **处理范围**: 处理 raw/01-articles 下9篇核心文章和 raw/03-transcripts 下2个视频字幕文件
- **冲突**: 无

## [2026-06-18] ingest | 摄入 Perplexity Skill 实践与 skill-creator 元技能文章

- **变更**: 新增 [[摘要-perplexity-skill-practice]], [[摘要-anthropic-skill-creator-practice]]; 新增实体 [[Perplexity]]; 更新 [[index.md]]
- **核心洞察**:
  - Perplexity 内部 Skill 开发标准：五步流程（测评用例→description→正文→分层拆分→迭代）、三层加载机制、踩坑清单正向扩充（Gotchas Flywheel）
  - skill-creator 是 Meta Skill：管理 Skill 完整生命周期，覆盖创建/修改/测试/评估/优化五大功能，形成定需求→写初稿→双组对照测试→量化打分→迭代优化闭环
- **处理范围**: 处理 raw/01-articles/ 下两篇新文章，其余文章已有对应摘要
- **冲突**: 无

## [2026-06-18] synthesis | 生成 Skill 课程第8-15章完整教程文案

- **变更**: 新增 8 章教程文案（08-五大设计模式上、09-五大设计模式下、10-两类Skill分类、11-Anthropic的9大Skill分类、12-没有评估的Skill只是假设、13-评估实战、14-Skill的长期维护与团队管理、15-Skill安全三原则）；所有文件已保存至 output/skill/ 目录
- **核心内容**:
  - 第8章：ToRapper 和 Generator 设计模式（按需注入知识、固定输出结构）
  - 第9章：Reviewer、Inversion、Pipeline 设计模式（分离规则、先问后做、分步执行）
  - 第10章：Capability Uplift 和 Encoded Preference 两类分类（补能力 vs 固化偏好）
  - 第11章：Claude Code 9 大能力地图四环节（认知→生产→验证→交付）
  - 第12章：Evals 体系入门（七步生命周期、三个评测场景、从"我相信"到"我可以证明"）
  - 第13章：评估实战（两类评分器、六类指标、A/B对比测试）
  - 第14章：长期维护与团队管理（分发策略、市场管理、依赖关系、度量优化）
  - 第15章：安全三原则（只安装可信来源、仔细阅读文件、理解执行逻辑）
- **风格**: 保持"张咋啦"风格，痛点驱动开场白、口语化、松弛感
- **篇幅**: 每章3-5分钟视频时长对应篇幅
- **结构**: 每章包含开场白、核心内容、总结、下章预告、参考资料
- **引用来源**: 基于知识库真实内容生成，所有章节均包含参考资料链接到知识库相关页面
- **冲突**: 无

## [2026-06-18] ingest | 最终摄入 - 共18篇核心文章完成知识库构建

- **变更**: 新增 [[摘要-personal-growth-methodology]], [[摘要-openspec-superpowers-nio-workflow]]; 更新 [[index.md]]
- **核心洞察**: 个人成长方法论（follow Builders+费曼输出+观点导向+完整闭环）；NIO定制版（OpenSpec DSL+Superpowers技能库+人工门禁+SHA256锁定+按需注入）
- **最终总结**:
  - ✅ **已完成摄入**：18篇核心文章（Skill系列13篇+OpenSpec实战5篇）
  - ✅ **知识库总量**：来源38个、实体17个、概念35个
  - ✅ **完整知识体系**：Skill全链路（概念→设计→实践→评估→心智模型→框架）+ OpenSpec实战应用（标准流程+定制版本+架构对比+Schema设计）+ 方法论补充
  - ⏭️ **剩余文件**：约10篇"解读"类文章（与核心内容重复）、1个PDF文件
  - 🎯 **核心价值**：知识库已构建完整，剩余文章可根据需要选择性处理
- **冲突**: 无

## [2026-06-18] ingest | 完成知识库核心摄入 - 共16篇重要文章

- **变更**: 新增 [[摘要-tdd-driven-nio-schema]]; 更新 [[index.md]]
- **核心洞察**: tdd-driven-nio Schema将TDD四层防护固化为工程流程，制品DAG物理约束，任务粒度强制TDD，三级审查机制
- **最终总结**: 本次对话已完成16篇核心文章摄入，构建完整知识体系：Skill系列13篇（概念→设计→实践→评估→心智模型→框架）+ OpenSpec实战3篇（组合流程+架构对比+Schema设计）
- **剩余文件**: 约10篇文章（部分"解读"类与已摄入内容重复、PDF文件、转录文案等），可根据需要后续处理
- **冲突**: 无

## [2026-06-18] ingest | 补充摄入 OpenSpec实战与Agent架构对比文章

- **变更**: 新增 [[摘要-openspec-superpowers-workflow]], [[摘要-agent-four-components]]; 更新 [[index.md]]
- **核心洞察**: OpenSpec+Superpowers四阶段实战流程（规约设计→脚手架生成→并行业务实现→契约迭代，TDD循环+三级审查+Subagent-Driven执行）；Agent四大组件定位与联动（Prompts临时/Skills复用/Subagents隔离/MCP连接，组合口诀单次微调+通用能力+独立专项+外部数据+高阶工作流组合）
- **总结**: 本次对话已完成 Skill系列13篇核心文章 + OpenSpec实战 + Agent架构对比共15篇重要文章摄入，知识库已构建完整Skill知识体系与实战应用框架
- **冲突**: 无

## [2026-06-18] ingest | 完成 Skill 系列全部 13 篇文章摄入（第11-13篇）

- **变更**: 新增 [[摘要-skill-mental-model]], [[摘要-skill-four-types]], [[摘要-skill-0to1-framework]]; 新增概念 [[SkillMentalModel]], [[SkillFourTypes]], [[Skill0to1Framework]]; 更新 [[index.md]]
- **核心洞察**: 心智模型跃迁（从执行者到设计者，写约束而非步骤，写的是Agent决策框架）；四大Skill类型（触发式/工具式/流程式/偏好式，类型决定设计维护策略）；0到1四阶段框架（认知定位→最小可行→扩展结构化→运营优化，先搭反馈回路再迭代）
- **总结**: Skill系列全部13篇文章已摄入完成，覆盖从核心概念到设计模式到最佳实践到评估评测到心智模型到完整框架的全链路知识体系
- **冲突**: 无

## [2026-06-18] ingest | 批量摄入 Skill 系列 OpenAI 与 Anthropic 评分评测（第9-10篇）

- **变更**: 新增 [[摘要-openai-skill-scorer]], [[摘要-anthropic-skill-lifecycle]]; 新增概念 [[SkillScorerSystem]], [[SkillLifecycle]], [[SkillTwoTypes]]; 更新 [[index.md]]
- **核心洞察**: OpenAI评分器系统（确定性检查抓底线+评分细则检查抓质量，锁死格式收集评估数据）；Anthropic生命周期七步流程（评估变成持续提升前提，从"我相信"到"我可以证明"，把失败变成可复现对象进入迭代闭环）；Skill两类分类（Capability Uplift补能力验证增量，Encoded Preference固化偏好验证忠实度）
- **冲突**: 无

## [2026-06-18] ingest | 批量摄入 Skill 系列 OpenAI 评估与生态运营（第7-8篇）

- **变更**: 新增 [[摘要-skill-ecosystem-operation]], [[摘要-openai-skill-evaluation]]; 新增实体 [[OpenAI]]; 新增概念 [[SkillEcosystemOperation]], [[SkillEvaluationFramework]]; 更新 [[index.md]]
- **核心洞察**: 生态运营三机制（分发策略/市场管理/依赖关系/数据驱动），先搭反馈回路再迭代；OpenAI评估框架（四类目标/两类维护面/三类假设/四类样本），从体感维护到证据闭环，从会写Skill到会维护Skill
- **冲突**: 无

## [2026-06-18] ingest | 批量摄入 Skill 系列 Claude Code 核心实践（第5-6篇）

- **变更**: 新增 [[摘要-claude-code-9-skill-types]], [[摘要-skill-9-best-practices]]; 新增实体 [[ClaudeCode]]; 新增概念 [[SkillCapabilityMap]], [[SkillFourStages]], [[SkillBestPractices]], [[SkillThreeLayers]]; 更新 [[index.md]]
- **核心洞察**: 9类能力地图四环节（认知→生产→验证→交付）帮团队诊断能力缺口；9个最佳实践三层架构（内容层→结构层→高级技术层）解决不被调用和效果差问题；核心思想：好的Skill给组合能力而非固定步骤
- **冲突**: 无

## [2026-06-18] ingest | 摄入 Skill 系列 Google 5 种设计模式

- **变更**: 新增 [[摘要-skill-google-5-patterns]]; 更新实体 [[Google]]（补充Skill设计贡献）; 新增概念 [[SkillDesignPattern]], [[ToRapperPattern]], [[GeneratorPattern]], [[ReviewerPattern]], [[InversionPattern]], [[PipelinePattern]]; 更新 [[index.md]]
- **核心洞察**: 问题不在格式而在内容设计逻辑，五种模式解决五大问题：ToRapper（按需注入知识）、Generator（固定输出结构）、Reviewer（分离审查与检查规则）、Inversion（先问清需求再开工）、Pipeline（分步执行流程），模式可叠加，先判断问题类型再选模式
- **冲突**: 无

## [2026-06-17] ingest | 摄入 Skill 系列第三篇：开发评估与安全使用

- **变更**: 新增 [[摘要-skill-anthropic-doc-part3]]; 新增概念 [[ProblemDrivenConstruction]], [[HumanMachineCoCreation]], [[SkillSecurity]], [[SkillAndMCP]]; 更新 [[index.md]]
- **核心洞察**: 问题驱动建设（失败样本反推缺陷），分层文件结构（元数据/正文/附属文件三层），从Claude角度设计（name/description是决策信号），人机共创迭代（反思沉淀SOP），安全三原则（可信来源/阅读文件/理解逻辑），Skill与MCP互补（方法论+外部连接），Skill生态愿景（共享发现+自主创建）
- **冲突**: 无

## [2026-06-17] ingest | 摄入 Skill 系列第二篇：渐进式披露机制

- **变更**: 新增 [[摘要-skill-anthropic-doc-part2]]; 新增概念 [[ProgressiveDisclosure]], [[CognitionExecutionSeparation]]; 更新 [[index.md]]
- **核心洞察**: Skill文件结构（SKILL.md+YAML元数据），三层加载（Level 1元数据→Level 2正文→Level 3附属文件），认知与执行分离（上下文只装载思考所需信息，执行在虚拟机进行），近似无限上下文是架构思想而非模型参数魔法
- **冲突**: 无

## [2026-06-17] ingest | 摄入 Skill 系列第一篇：核心概念与三要素

- **变更**: 新增 [[摘要-skill-anthropic-doc-part1]]; 新增实体 [[Anthropic]], [[Claude]]; 新增概念 [[AgentSkill]], [[ProcessKnowledge]], [[OrganizationalContext]], [[DynamicLoading]]; 更新 [[index.md]]
- **核心洞察**: Agent两大能力缺口（过程知识+组织背景），Skill三要素（指令/脚本/资源），动态加载机制突破上下文限制，Skill vs Tool的本质区别（How vs What）
- **冲突**: 无

## [2026-06-07] ingest | 设计 tdd-driven-nio Schema 完整方案

- **变更**: 新增 `raw/01-articles/tdd-driven-nio Schema 完整设计方案.md`；创建 `schemas/tdd-driven-v2/` 完整 Schema 包（schema.yaml + 5个模板 + config.yaml）
- **产物**: schema.yaml（含 proposal/specs/design/tasks/plans + apply 完整定义）、templates/{proposal,spec,design,tasks,plan}.md、config.yaml
- **核心设计**: 任务粒度物理约束（每 task=一个 TDD 阶段）、subagent 串行隔离、三级审查（spec+quality）、evidence 必填、writing-plans skill 绑定 plans artifact
- **配置方法**: 5步全流程含 OPSX 官方 CLI 命令、DAG 状态机、schema init/fork/validate
- **冲突**: 无

## [2026-06-07] sync | 扩写 spec-driven-nio 设计方案

- **变更**: 更新 [[spec-driven-nio-design]]，补齐 OpenSpec 核心机制、Superpowers 七项核心工作流、三重映射、五命令主流程、四阶段实战流水线、schema 包目录、schema.yaml 设计、模板规范、SHA256 锁定和 Dispatcher 逻辑
- **决策**: 明确 OpenSpec `tasks.md` 是业务任务清单，Superpowers `plan.md` 是独立工程实现计划；`writing-plans` 基于 brainstorming 设计文档与 proposal/spec/design，而不是直接读取 `tasks.md`
- **冲突**: 无

## [2026-06-07] ingest | 设计 spec-driven-nio OpenSpec×Superpowers 组合系统

- **变更**: 新增 [[spec-driven-nio-design]]（Syntheses）；创建 schemas/spec-driven-nio/ 完整 Schema 包（schema.yaml + 5个模板）；更新 [[index.md]]
- **产物**: schemas/spec-driven-nio/schema.yaml、templates/{proposal,spec,design,tasks,plan}.md
- **核心设计**: OpenSpec=Workflow DSL + Superpowers=Skill Library；五阶段流程；双 SHA256 人工门禁（propose-approved / verify-approved）；tasks.md(业务) vs impl-plan.md(工程) 分离原则；explore 阶段禁止 brainstorming
- **冲突**: 无

## [2026-06-07] lint | 知识库健康检查

- **结果**: 修复 1 个死链（重建 [[openspec-superpowers-schema-driven-dispatch]]，文件 21KB 已写入磁盘）；发现 1 个未解决知识冲突 [[ContextOS]]（§知识冲突保留待后续处理）
- **统计**: 44 文件扫描，18 Sources / 13 Entities / 8 Concepts / 4 Syntheses 全部注册

## [2026-06-07] query | 设计 spec-driven-nio 全链路 Schema，完成产物中心彻底融合

- **变更**: 重建 [[openspec-superpowers-schema-driven-dispatch]]：frontmatter（tags+spec-driven-nio+ArtifactCentric+7Skills）、核心洞察、SDLC命令映射（5阶段含explore）、两工具分工边界（7个无状态skill）、Schema设计（产物中心彻底融合版9个artifact）、Dispatcher伪代码（phase路由+拓扑排序）、命令→Skill→产物全景表（7技能矩阵）、SHA256锁定、Level1vsLevel2、OpenSpec目录结构（spec-driven-nio模板包）
- **冲突**: 无

- **变更**: 新增 [[摘要-opsx-openspec-new-workflow]]; 更新 [[OpenSpec]]（OPSX 动作驱动架构节）; 更新 [[摘要-openspec-superpowers-tdd-v2]] 源路径; 更新 [[摘要-openspec-superpowers-new-project-guide]] 源路径; 更新 [[index.md]]
- **冒**: 无

- **变更**: 新增 [[openspec-superpowers-schema-driven-dispatch]]; 更新 [[index.md]]
- **冲突**: 无

## [2026-06-07] ingest | 摄入 Gstack /qa skill 工作原理

- **变更**: 新增 [[摘要-gstack-qa-skill-workflow]], [[Playwright]]; 更新 [[Gstack]], [[index.md]]
- **冲突**: 无

## [2026-06-06] sync | design↔impl-spec 9 项一致性修复

- **变更 (impl-spec)**:
  - **[严重]** [[mymat-impl-spec]] §四 mymat-state.sh：删除所有 `case` 分支中的 `local` 关键字（bash 函数外不可用，运行时崩溃）；影响 `read/write/init/active/snapshot/rollback/task-done/metrics/validate` 共 7 个分支
  - **[中]** [[mymat-impl-spec]] §五.7 workflow-detect.sh：工作流阈值以 design 为准，`file_count -lt 10` 改为 `file_count -lt 6`（>5 文件 → full）
  - **[中]** [[mymat-impl-spec]] §五.4 guard-build.sh：新增检查 #3「实现文件存在」（按 platform 匹配 src/${MODULE_NAME}.\*，排除 test 文件）
  - **[轻]** [[mymat-impl-spec]] §五.4 guard-build.sh：新增 `isolation=none` 策略验证（检测 staged/changed 代码文件数，>0 则 HARD STOP）
  - **[中]** [[mymat-impl-spec]] §十二 待实现清单：删除 `/mymat:rollback` 行（已在 §六.1 路由表中实现）；新增 `/mymat:doctor`、`/mymat:version` 两行；`可分发安装/doctor` 拆分为 `可分发安装`
- **变更 (design)**:
  - **[中]** [[mymat-design]] §九 目录结构：补充缺失的 `trigger-log.txt`、`warn-log.txt`、`handoff/design-context.json` 三项（与 impl-spec §一.1 对齐）
  - **[中]** [[mymat-design]] §九 spec-graph.json 示例：替换错误节点（`superpowers_design`、`gstack_autoplan`）为正确的 4 个 OpenSpec 节点（`openspec_specs/tasks/proposal/design`）
  - **[中]** [[mymat-design]] §五 Phase S：`MISSING_TRIGGER` 从「错误」改为「warn-only，不阻塞流程」（与 impl-spec guard-spec.sh 行为对齐）
  - **[中]** [[mymat-design]] §十三 命令表：`/mymat:quick` 自动推荐条件 `3-10 个` 改为 `3-5 个`（与 full 阈值 >5 自洽）
- **冲突**: 无

## [2026-06-09] sync | impl-spec.md §六 补全 skills/ 完整规范

- **变更**:
  - [[mymat-impl-spec]] §六.3 新增 `mymat-product.md` skill 规范（P-01/P-02/Guard/HCG-1）
  - [[mymat-impl-spec]] §六.4 新增 `mymat-spec.md` skill 规范（S-01~S-03/Guard/HCG-2）
  - [[mymat-impl-spec]] §六.5 新增 `mymat-design.md` skill 规范（D-01/D-02/integrity 前置/完成流程）
  - [[mymat-impl-spec]] §六.6 新增 `mymat-verify.md` skill 规范（Vt-01~Vt-03/Vp-01~Vp-02/Guard/HCG-3）
  - [[mymat-impl-spec]] §六.7 新增 `mymat-release.md` skill 规范（HCG-4/R-01 /ship/R-02 /opsx:archive/Guard/完成展示）
- **冲突**: 无

## [2026-06-09] sync | impl-spec.md §十三–十八 融入前置章节并删除

- **变更**:
  - [[mymat-impl-spec]] §三 CLAUDE.md：新增「禁止仿写 Skill」强制规则
  - [[mymat-impl-spec]] §四 mymat-state.sh：新增 `validate_field()` + `validate` 子命令 + write 前校验调用
  - [[mymat-impl-spec]] §五.2 guard-spec.sh：新增产物 frontmatter 校验 + trigger-log 写入 + design-context.json 生成（HCG-2 PASS 分支末尾）
  - [[mymat-impl-spec]] §五.4 guard-build.sh：新增首任务 isolation 策略检查；AC 关键词注释去除 §十八.2 引用
  - [[mymat-impl-spec]] §六.2 mymat-build.md：新增前置条件 0（读取交接包，缺失即 HARD STOP）+ 隔离策略确认菜单；更新 AC 锚定引用
  - [[mymat-impl-spec]] 删除独立章节 §十三、§十四、§十五、§十六、§十八；删除 §十二 过渡注释；清除全部陈旧章节引用注释
- **冲突**: 无

## [2026-06-08] sync | 一致性审查：impl-spec.md 补齐 design.md §十八 + 结构性修复

- **变更**:
  - [[mymat-impl-spec]] §一.1 目录结构：补充 `handoff/design-context.json`、`trigger-log.txt`、`warn-log.txt` 三项（与 §十三-十四-十八 对齐）
  - [[mymat-impl-spec]] §六.1 路由表：修复 `mymat-design-skill.md` → `mymat-design.md`（与 §一.1 文件名对齐）
  - [[mymat-impl-spec]] §六.2 mymat-build.md：Build 循环 ELSE 分支顶部插入 per-task AC 上下文锚定步骤（对应 design §十八.1）
  - [[mymat-impl-spec]] §五.4 guard-build.sh：测试运行块后追加关键词对齐 warn-only 检查，读路径经由 handoff/design-context.json（对应 design §十八.2）
  - [[mymat-impl-spec]] §十八 新增"交付可靠性补强实现规范"（18.1 AC锚点 + 18.2 warn-log 设计说明）
- **冲突**: 无
- **一致性报告**: 见本次对话最终输出

## [2026-06-07] sync | Comet 对比分析补强：design.md §十七 + impl-spec.md §十三-十六

- **变更**:
  - [[mymat-design]] §九 state.json: `token_estimate` → `output_chars/input_chars/api_usage:null`（4处）；新增 `isolation` 字段
  - [[mymat-design]] §十七 新增"工程化补强"（5小节）：交接包、Skill触发验证、Schema校验、分支隔离、可分发安装路线图
  - [[mymat-impl-spec]] §七: 完整替换"token 估算"→"metrics 字段设计与可测量性"
  - [[mymat-impl-spec]] §四.2: init 模板新增 `"isolation": null`
  - [[mymat-impl-spec]] §十二: 删除 `token 精确计量` 行；补充 §十三-十六 导航注释
  - [[mymat-impl-spec]] §十三-十六: 新增 4 节实现规范（交接包脚本、Skill触发两层验证、Schema校验函数+validate子命令、分支隔离guard-build.sh检查）
- **决策**: `api_usage: null` 预留，`elapsed_seconds` 作为成本代理指标
- **冲突**: 无

## [2026-06-06] synthesis | 编写 Mymat 实现细节规范

- **变更**: 新增 [[mymat-impl-spec]]（Guard 脚本实现、Skill 模板、state.sh 接口、安装脏本、序列图）; 更新 [[index.md]]
- **决策**: mvp 范围内实现 7 个 guard 脚本 + mymat-state.sh + 6 个 skill 文件 + 安装脚本
- **冲突**: 无

## [2026-06-06] synthesis | 编写 Mymat 完整设计方案

- **变更**: 新增综合设计文档 [[mymat-design]]（七阶段、四HCG、子任务级状态机、两层编排机制、四个自动串联点、Guard 脚本体系）; 更新 [[index.md]]
- **来源**: 本次会话约10轮设计讨论的完整结论汇总
- **冲突**: 无

## [2026-06-06] ingest | 处理 raw/01-articles 中 2 篇文章（三器合一视频 + gstack+Superpowers 完美闭环）

- **变更**: 新增来源 [[摘要-openspec-superpowers-gstack-threeinone]]、[[摘要-gstack-superpowers-perfect-loop]]; 增量更新实体 [[Gstack]]、[[Superpowers]]（补充来源引用）; 更新 [[index.md]]
- **冲突**: 无
- **归档**: 2 篇源文件已移至 raw/09-archive/

## [2026-06-06] ingest | 处理 raw/01-articles 中 3 篇文章（Comet 开源 Skill 系列）

- **变更**: 新增实体 [[Comet]]; 新增来源 [[摘要-comet-skill-intro]]、[[摘要-comet-developer-story]]、[[摘要-comet-readme-zh]]; 更新 [[index.md]]
- **冲突**: 无
- **归档**: 3 篇源文件已移至 raw/09-archive/；raw/ 目录现已清空

## [2026-06-06] ingest | 处理 Clippings 中 2 篇文章（TDD v2 + 新项目全流程指南）

- **变更**: 新增来源 [[摘要-openspec-superpowers-tdd-v2]]、[[摘要-openspec-superpowers-new-project-guide]]; 新增概念 [[AtomicTDDWorkflow]]; 增量更新实体 [[OpenSpec]]（补充命令）; 更新 [[index.md]]
- **冲突**: 无
- **归档**: 源文件已移至 raw/09-archive/

## [2026-06-06] ingest | 处理 Clippings 中 1 篇文章（Superpowers + OpenSpec 老旧项目实战）

- **变更**: 新增来源 [[摘要-superpowers-openspec-legacy-project]]; 增量更新实体 [[Superpowers]]（Star数修正）、[[OpenSpec]]（补充新命令）; 更新 [[index.md]]
- **冲突**: 无
- **归档**: 源文件已移至 raw/09-archive/

## [2026-06-06] ingest | 处理2篇文章（Superpowers + Gstack + OpenSpec 开发流程系列）

- **变更**: 新增来源 [[摘要-openspec-superpowers-gstack-workflow]], [[摘要-superpowers-gstack-integration]]; 新增实体 [[Superpowers]], [[Gstack]], [[OpenSpec]]; 更新 [[index.md]]
- **冲突**: 无
- **归档**: 2个源文件已移入 raw/09-archive/

## [2026-06-05] query | 企业AI研发阶段分布现状查询

- **输出**: 已保存至 [[企业AI研发阶段分布与生产力悖论]]；引用 [[摘要-ai-native-agent-pipeline]], [[ProductivityParadox]], [[FarosAI]], [[Google]], [[ApolloIO]], [[Accenture]], [[AgentHumanPipeline]]

## [2026-06-05] ingest | 批量处理5篇文章（Obsidian知识库与AI产品需求流水线系列）

- **变更**: 新增来源 [[摘要-obsidian-context-os]], [[摘要-20min-ai-knowledge-base]], [[摘要-ai-product-requirement-pipeline]], [[摘要-ai-product-workflow]], [[摘要-software30-context-kb-project]]; 新增实体 [[Obsidian]], [[FeishuProject]]; 新增概念 [[LLMWikiPattern]], [[ContextOS]], [[ProductRequirementPipeline]], [[Software30]]; 更新 [[index.md]]
- **冲突**: 无
- **归档**: 5个源文件已移入 raw/09-archive/

## [2026-06-05] ingest | AI Native时代为什么企业要建Agent+人协作的软件交付流水线

- **变更**: 新增 [[摘要-ai-native-agent-pipeline]]; 新增实体 [[NBER]], [[FarosAI]], [[Google]], [[ApolloIO]], [[Accenture]], [[GitHubCopilot]]; 新增概念 [[AgentHumanPipeline]], [[ProductivityParadox]], [[DORAMetrics]]; 更新 [[index.md]]
- **图片**: 原文含2张本地图片引用（流水线价值示意图.png、企业AI研发阶段分布.png），需确认是否已下载至 raw/assets/
- **冲突**: 无

## [2026-06-06] sync | 修复 mymat-design 评审发现与 impl guard 误判

- **变更 (design)**:
  - [[mymat-design]] §五：HCG-2 冻结对象从仅 `openspec_specs` 扩展为 `openspec_specs` + `openspec_tasks`
  - [[mymat-design]] §五：D-02 明确只产出非冻结设计计划；如需修改 `tasks.md` 必须回滚到 HCG-1 重走 S 阶段
  - [[mymat-design]] §八：Build 断点恢复示例修正为 B-001~B-003 跳过，从 B-004 继续
  - [[mymat-design]] §十一：将“内嵌子工具关键逻辑”改为“内嵌编排步骤”，强调必须读取并真实触发外部 skill，不得仿写
  - [[mymat-design]] §十一：`MISSING_TRIGGER` 明确为 warn-only 审计信号
  - [[mymat-design]] §十二：串联点 1 修正为 Gstack `/autoplan` → OpenSpec `/opsx:propose` 输入
  - [[mymat-design]] §十三：`/mymat:doctor` 依赖描述改为 `sha256sum` 或 `shasum`；修复可分发安装加粗格式
- **变更 (impl-spec)**:
  - [[mymat-impl-spec]] §五.2：`HANDOFF_HASH` 计算支持 `sha256sum` / `shasum` fallback
  - [[mymat-impl-spec]] §五.4：测试文件检查改为按平台使用 `find + -name`，避免 `{ts,js}` 在变量中不展开导致误报
  - [[mymat-impl-spec]] §五.4：实现文件检查改为递归匹配常见目录结构，避免只查 `src/${MODULE_NAME}.ts` 的误杀
  - [[mymat-impl-spec]] §五.4 / §五.7：修复 `grep -c ... || echo 0` 可能产生双 0 的计数写法
  - [[mymat-impl-spec]] §九：安装脚本依赖检查接受 `sha256sum` 或 `shasum`
- **冲突**: 无

## [2026-06-06] sync | 重写 mymat-design §三设计哲学

- **变更**:
  - [[mymat-design]] §三：将“三层信任金字塔”升级为哲学一“可验证事实高于 AI 承诺”
  - [[mymat-design]] §三：重排五个设计哲学：可信事实、覆盖优先、串联点、人机可逆性边界、`state.json` 恢复地图
  - [[mymat-design]] §三：补充 guard/state/instruction 三层信任模型与“AI 承诺不等于系统事实”原则
- **冲突**: 无

## [2026-06-06] sync | 重整 mymat-design 叙事结构

- **变更**:
  - [[mymat-design]]：删除旧 §二“解决思路”，其“三层信任金字塔”已并入新版设计哲学
  - [[mymat-design]]：删除旧 §四“系统定位”，将三工具分工边界合并到 §一“什么是 Mymat”
  - [[mymat-design]]：整体重排后续章节编号，保持七阶段、HCG、state.json、guard、命令语义不变
- **影响**: 仅为设计文档叙事结构调整，不影响 [[mymat-impl-spec]] 的实现规范
- **冲突**: 无

## [2026-06-06] sync | 对齐 impl-spec D 阶段非冻结设计计划

- **变更**:
  - [[mymat-impl-spec]] §六.5：D-02 writing-plans 产物改为非冻结设计计划，默认写入 `docs/plan-{feature_id}.md` 或 `.mymat/features/{feature_id}/handoff/build-plan.json`
  - [[mymat-impl-spec]] §六.5：删除“更新现有 tasks.md”的旧口径，明确 HCG-2 后不得直接修改 frozen `tasks.md`
  - [[mymat-impl-spec]] §六.5：若 D 阶段发现 tasks 粒度不足，必须回滚到 HCG-1 重新走 S 阶段
- **冲突**: 无

## [2026-06-06] sync | 补充 mymat-design 主流程命令与子任务映射

- **变更**:
  - [[mymat-design]] §十一：主流程命令表新增“映射到的子任务”列，明确用户命令与 P/S/D/B/Vt/Vp/R 子任务 ID 的关系
  - [[mymat-design]] §十一：补充 HCG 子任务嵌入说明，明确 HCG-1/2/3/4 分别嵌入 product/spec/verify/release
  - [[mymat-design]] §十一：新增完整用户体验流程示意，说明主流程命令如何编排内部子任务
- **影响**: 文档解释增强，不影响 [[mymat-impl-spec]] 实现规范
- **冲突**: 无

## [2026-06-06] sync | 精简 mymat-design 主流程命令表

- **变更**:
  - [[mymat-design]] §十一：删除主流程命令表中的“内部编排的子工具”列，仅保留命令、对应阶段、映射到的子任务
- **影响**: 表格阅读简化，不改变 HCG 嵌入说明与 [[mymat-impl-spec]] 实现规范
- **冲突**: 无

## [2026-06-06] sync | 统一 Build 循环步骤命名

- **变更**:
  - [[mymat-design]]：将 Build 循环步骤从 `B-N-01/B-N-02/B-N-03` 改为 `B-01/B-02/B-03`，AC 锚定步骤改为 `B-00`
  - [[mymat-impl-spec]]：同步 Build skill 说明中的 `B-N-*` 命名，避免设计与实现规范口径不一致
- **影响**: 仅调整 Build 子步骤命名表达，不改变 Build task 断点语义
- **冲突**: 无

## [2026-06-06] sync | 补充七阶段产物位置

- **变更**:
  - [[mymat-design]] §三：为 P/S/D/B/Vt/Vp/R 各阶段表格新增“产物位置”列
  - [[mymat-design]] §三：外部工具产物遵循各自事实源目录，Gstack 写入 `gstack/{feature_id}/`，OpenSpec 写入 `openspec/changes/{change_id}/` 与 `openspec/specs/`
  - [[mymat-design]] §三：Mymat 自有状态、快照、handoff、warn-log 仍写入 `.mymat/features/{feature_id}/`
- **影响**: 明确产物归属与落盘位置，不改变七阶段流程语义
- **冲突**: 无

## [2026-06-06] sync | 重构 mymat-design 为五阶段主流程

- **变更**:
  - [[mymat-design]]：删除 Phase P，将主流程从 `P-S-D-B-Vt-Vp-R` 调整为 `S-D-B-V-R`
  - [[mymat-design]]：合并 VerifyTech 与 VerifyProduct 为 Phase V，并定义 Mymat native `/review`、`/api`、`/e2e` 三类验证能力
  - [[mymat-design]]：将 HCG 从 4 个调整为 3 个：需求冻结、验证验收、发布确认
  - [[mymat-design]]：去除 Gstack 核心依赖口径，改为 OpenSpec + Superpowers + Mymat Native Skills
- **影响**: 明确 Mymat 只治理“已确定需求到 PR 创建”的 AI Coding 交付流程，不再承担产品发现职责
- **冲突**: 旧七阶段产物位置记录中的 Gstack 路径已被本次设计取代；后续需同步 [[mymat-impl-spec]]
