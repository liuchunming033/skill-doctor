---
title: "摘要-skill-anthropic-doc-part1-video"
type: source
tags: [来源, Skill, Anthropic, 视频]
sources: [raw/03-transcripts/BV1uZCFBdEs4_字幕_SKILL到底是什么_①.txt]
last_updated: 2026-06-18
---

## 核心摘要

Anthropic 2024年10月16日发布官方文档《Equipping agents for the real world with agent skills》,提出Skills机制解决Agent两大能力缺口:过程知识缺失(不知道事情该怎么做)和组织背景缺失(不知道东西在哪里)。Skill是由指令/脚本/资源组成的结构化文件夹,智能体能够动态发现并加载这些内容以提升特定任务表现。Skill与Tool的本质区别:Tool回答What(我能做什么),Skill回答How(我该如何做好这件事)。Tool是原子化能力,Skill是完整SOP。

## Agent两大能力缺口

把一个agent想象成一个聪明但没经验的新员工:
- **缺乏过程知识**:即不知道事情该怎么做,例如不知道报销流程/如何提交代码
- **缺乏组织背景**:即不知道东西在哪里,例如不知道项目API密钥在哪/PPT模板在哪

没有这两样东西,agent就无法处理真实世界中的具体工作

## Skill的定义

Skill的核心定义:由指令/脚本/资源组成的结构化文件夹,智能体能够动态发现并加载这些内容以提升特定任务的表现

**三要素拆解**:
- **Instructions**:相当于手册中的SOP文字,告诉如何一步步完成任务
- **Scripts**:需要执行的Python文件
- **Resources**:执行过程中用到的配置文件或模板,如JSON或docx文件

这三要素正好对应两个痛点:
- 过程知识的缺失由指令和脚本解决
- 组织背景的缺失由资源解决

**关键特性**:智能体能够动态发现并加载这些内容,意味着Skill不再被固定在系统提示中,而是可以被动态检索/挂载和使用

## Skill vs Tool

两者看起来相似但角色完全不同,Skill最终会调用Tool但架构地位不同

**类比理解**:
- **Tool像一台烤箱**:是底层的执行能力,功能强大但需要精确指令才能工作
- **Skill像一份妈妈的烤鸡食谱**:本身不烤鸡但封装了全部过程知识(烤多久/温度多少/需要哪些原料/经验性诀窍)

**维度区分**:
- Tool回答What(我能做什么),技术上执行代码;Skill回答How(我该如何做好这件事),技术上指导如何完成任务
- Tool是原子化能力(一个API或函数);Skill是完整SOP(包含指令/脚本/资源)
- Tool是执行器被动等待调用;Skill是流程编排者主动指导LLM调用Tool完成任务
- Tool的目标是提供原子能力;Skill的目标是封装可移植可复用的过程知识

**总结**:Skill不是Tool的替代品,而是调用Tool的SOP,它封装了可组合的过程知识,让agent真正具备会做事的能力

## 系统架构

### 右侧Agent虚拟机
- Agent的电脑和双手,是真正执行任务的地方
- Python引擎:当skill文件夹中包含脚本时LLM就能调用它执行
- Bash终端:Agent可以通过它操作文件(使用ls列出文件或cat读取文件内容)
- 文件系统:存放着所有skill的实体

### 左侧Agent配置
- LLM是大脑决策中心
- Agent配置更像是LLM可访问的SOP索引,包含核心系统提示和已装备技能清单(技能名称和简介)
- 当Claude想使用某个skill时,它会通过Tool操作虚拟机执行命令Run bash command,读取到的内容会返回给LLM的上下文窗口

## 动态发现与加载

当Claude面对不同任务时(如分析财报/提取合同字段/生成合规文档),他会主动发现最相关的skill,加载其中的SOP/脚本和模板,使输出更精准更一致也更可复现

这就是"提升特定任务表现"的真正含义:Skill不只是知识的存储单元,而是让agent在特定场景下变得更专业的能力模块。它赋予了Claude在需要时加载能力模块的心智模式,让智能边界不再受上下文窗口限制,而是能随任务实时扩展

## 关联连接
- [[AgentSkill]] — Agent Skill核心概念
- [[ProcessKnowledge]] — 过程知识
- [[OrganizationalContext]] — 组织背景
- [[DynamicLoading]] — 动态加载机制
- [[Anthropic]] — AI安全公司
- [[Claude]] — Anthropic开发的大语言模型