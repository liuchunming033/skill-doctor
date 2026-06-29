---
title: "摘要-skill-anthropic-doc-part2-video"
type: source
tags: [来源, Skill, 渐进式披露, Anthropic]
sources: [raw/03-transcripts/BV1JFkrBXEZL_字幕_无限上下文_skill渐进式披露机制_②.txt]
last_updated: 2026-06-18
---

## 核心摘要

Skill渐进式披露三层加载机制:Level 1 YAML元数据层(始终加载约100 token:name+description预加载到系统提示)→Level 2正文内容层(触发时加载<5000 token:SKILL.md核心指令与SOP逻辑)→Level 3附属文件层(按需加载理论上无限:markdown文档/配置文件/脚本)。认知与执行分离:Claude上下文只装载思考所需信息,执行在虚拟机进行,外部脚本带来确定性效率和复用性。近似无限上下文不是模型参数魔法而是架构思想。

## Skill文件结构

每一个skill都是一个文件夹,核心文件是SKILL.md,可以把它理解成这项技能的使用说明书和入口

**YAML front matter(元数据区)**:
- name:技能名称(如PDF)
- description:简要说明这项技能能做什么(如从PDF中抽取文本和表单字段)

**系统加载机制**:在agent的启动时会自动扫描所有技能的SKILL.md,并把每个技能的name和description预加载到系统提示词中。这意味着当code启动后他就已经知道我具备哪些技能和这些技能大致做什么,而不需要一次性加载所有技能的全部内容。这种设计让技能可以被索引而不被展开,也为接下来的渐进式披露打下了基础

## 渐进式披露三层加载机制

原文将渐进式披露比作一本组织良好的手册:你先读目录确定主题,再读相关章节掌握要点,最后只有在需要时才查阅详细的附录。这种阅读方式正是skill的结构逻辑

### Level 1:YAML元数据层
- **文件位置**:SKILL.md顶部的YAML front matter
- **内容**:技能的name和description
- **加载方式**:始终加载
- **Token消耗**:大约100个token
- **作用**:告诉模型有哪些技能和他们是做什么的

### Level 2:正文内容层
- **文件位置**:SKILL.md的markdown正文部分
- **内容**:技能的核心指令与SOP逻辑
- **加载方式**:在技能被触发时加载
- **Token消耗**:平均消耗小于5000个token
- **作用**:当Claude决定使用这个技能时他才真正打开这部分内容

### Level 3及以上:附属文件层
- **文件位置**:技能文件夹中除SKILL.md外的其他文件
- **内容**:markdown文档(如forms.md/reference.md)/配置文件(如.json)/脚本(如.py)
- **加载方式**:按需加载
- **Token上限**:理论上无限
- **作用**:Claude只有在SOP指令中被要求访问这些文件时才会读取或执行它们

通过这种分层结构,Claude不再一口气读完整本手册,而是像阅读文档一样逐步展开随用随取,这就是渐进式披露机制的精髓

## 认知与执行分离

问题:既然Level 3可以包含大量文件甚至脚本,为什么不会撑爆上下文?

**核心在于认知与执行的分离**:
- **Claude的上下文**可以被看作他的思考空间
- **文件系统和执行工具**则构成它的行动空间
- 二者在架构上是分离的但协同工作

**认知空间**:
- 只包含模型推理所需的文字信息
- 也就是Level 1的元数据加上被触发技能的部分Level 2内容
- 体量小可被直接加载进上下文

**执行空间**:
- 包含所有外部文件/脚本和数据
- 任务执行发生在外部虚拟机中
- Claude不会阅读这些脚本而是调用工具执行

**示例**:在PDF skill里,当Claude读到forms.md的指令"请运行scripts/extract_fields.py",他不会把那份5000行的Python代码加载进上下文,而是向虚拟机发出run bash command命令。脚本运行结束后虚拟机返回一小段结果"字段提取完成,结果已保存为forms.json",在上下文里只看到这个结果不承担脚本执行本身

原文写道:"Agents with a first-class filesystem and code execution tools don't need to read the entirety of a skill into their context window. The amount of context that can be bundled into a skill is effectively unbounded."

模型并不扩大上下文窗口,而是通过外部化执行让技能包的体积与上下文无关

## 确定性与效率

原文在最后还强调了代码执行的另一层意义:

语言模型可以写代码,但在处理排序/提取或数学运算时效率低成本高,而外部脚本执行既快速又可重复,结果可验证。因此Skill不仅让Claude知道怎么做,还确保每次都能做对

## 动态加载过程示例

原文用一张示意图展示了上下文在Skill被触发时的动态变化:

### 初始阶段
Claude的上下文中包含系统提示+所有技能的元数据片段(name和description)+用户的初始输入

### 技能被触发时
如用户请求"请帮我填写这份PDF表单",Claude判断任务与PDF技能相关,于是调用工具读取PDF SKILL.md的正文内容,这部分被加载进上下文

### 按需展开附录
如果正文中提到"请阅读forms.md",Claude再次调用工具读取forms.md的内容,这时forms.md的文字进入上下文,而未被提及的reference.md仍然留在文件系统中

### 执行外部脚本
当SOP要求运行脚本时,Claude发出执行命令,脚本在外部虚拟机中运行,只将执行结果返回上下文

### 任务完成
Claude综合当前上下文中的内容(包括SOP/读取结果/脚本输出)继续生成最终响应

从始至终上下文都只包含完成当前任务所需的信息,而技能包的完整内容则留在外部世界随时可被访问

## 三层逻辑总结

1. **结构上**:Skill是一个包含SKILL.md的文件夹,它的顶部元数据在系统提示中被预加载
2. **机制上**:渐进式披露让Skill分为三层(目录/正文/附录),Claude按需展开信息逐层显露
3. **架构上**:通过认知与执行的分离,模型的思考空间始终轻量,执行空间可以无限扩展,外部脚本带来了确定性/效率和复用性

因此**近似无限上下文并不是模型参数的魔法,而是一种架构思想**:让模型的上下文只装载需要思考的那一页,而把真正的世界留在它随时可访问的文件系统里

## 关联连接
- [[ProgressiveDisclosure]] — 渐进式披露机制
- [[CognitionExecutionSeparation]] — 认知与执行分离架构
- [[AgentSkill]] — Agent Skill核心概念
- [[DynamicLoading]] — 动态加载机制