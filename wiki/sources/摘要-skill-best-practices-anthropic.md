---
title: "摘要-skill-best-practices-anthropic"
type: source
tags: [来源, Skill, 最佳实践, Anthropic]
sources: [raw/01-articles/Anthropic的Skill 编写最佳实践.md]
last_updated: 2026-06-18
---

## 核心摘要

Anthropic官方Skill编写最佳实践指南,核心原则是极致简洁(上下文是公共资源,每个token都与其他内容竞争)。系统讲解Skill命名规范、描述编写技巧、渐进式披露架构、自由度设计策略、测试迭代方法、常见反模式,以及包含可执行代码的Skill工程规范(脚本编写、依赖管理、MCP工具引用、运行时环境理解)。

## 核心原则

### 简洁至关重要
- 默认假设Claude已具备基础智能,只补充缺失上下文
- 每条信息审视:"Claude真的需要这个解释吗?""这段内容是否值得其token成本?"
- 元数据(name+description)预加载,SKILL.md仅在相关时读取,避免冗余解释

### 设置适当的自由度
- **高自由度(文本指令)**:适用于多种方法都有效的场景,给出大致方向
- **中等自由度(伪代码)**:适用于存在首选模式但允许变通的场景
- **低自由度(精确脚本)**:适用于脆弱、一致性关键的操作,提供具体防护措施和精确指令

### 多模型测试
- Claude Haiku:Skill是否提供了足够的指导?
- Claude Sonnet:Skill是否清晰高效?
- Claude Opus:Skill是否避免了过度解释?
- 对Opus完美有效的可能需要为Haiku提供更多细节

## Skill结构规范

### YAML Frontmatter
- **name**:最多64字符,小写字母/数字/连字符,不含XML标签和保留词(anthropic/claude)
- **description**:最多1024字符,必须非空,描述Skill功能及何时使用,使用第三人称编写

### 命名约定
- 推荐**动名词形式**:processing-pdfs,analyzing-spreadsheets,managing-databases
- 可接受:名词短语(pdf-processing),动作导向(process-pdfs)
- 避免:模糊名称(helper/utils),过于通用(documents),保留词,不一致模式

### 编写有效的描述
- 必须同时包含Skill功能和何时使用的具体触发条件/上下文
- 具体明确并包含关键术语
- 每个Skill只有一个描述字段,对于Skill选择至关重要

## 渐进式披露模式

### 三层加载机制
- **Level 1:YAML元数据层**(始终加载,约100 token):name+description预加载到系统提示
- **Level 2:正文内容层**(触发时加载,<5000 token):SKILL.md核心指令与SOP逻辑
- **Level 3:附属文件层**(按需加载,理论上无限):markdown文档/配置文件/脚本

### 三种组织模式
1. **带引用的高级指南**:SKILL.md作为概述,链接到详细内容(FORMS.md/REFERENCE.md)
2. **按领域组织**:涉及多个领域的Skill按领域组织内容避免加载不相关上下文
3. **条件性详情**:显示基本内容,链接到高级内容

### 避免深层嵌套引用
- 保持引用距SKILL.md仅一层深度
- 所有参考文件都应直接从SKILL.md链接
- 为超过100行的参考文件添加目录结构

## 工作流与反馈循环

### 对复杂任务使用工作流
- 将复杂操作分解为清晰的顺序步骤
- 提供检查清单,Claude可复制到响应中并在进展过程中逐项勾选
- 清晰步骤防止Claude跳过关键验证

### 实现反馈循环
- 常见模式:运行验证器→修复错误→重复
- 验证循环可大大提高输出质量
- 验证器可以是参考文档(STYLE_GUIDE.md)或脚本(validate.py)

## 内容指南

### 避免时效性信息
- 不要包含会过时的信息
- 使用"旧模式"部分提供历史背景而不使主要内容杂乱

### 使用一致的术语
- 选择一个术语并在整个Skill中使用它
- 一致性有助于Claude理解和遵循指令

## 评估和迭代

### 构建评估
- 在编写大量文档之前创建评估
- 识别差距→创建评估→建立基线→编写最少指令→迭代
- 评估驱动的开发确保解决真实问题而非预测需求

### 与Claude一起迭代开发Skill
- 与Claude A合作创建Skill,Claude B在实际任务中测试
- Claude A帮助设计和完善指令,Claude B通过实际使用揭示差距
- 基于使用观察而非假设进行迭代

## 应避免的反模式

### 避免Windows风格的路径
- 始终使用正斜杠,即使在Windows上
- Unix风格路径在所有平台有效

### 避免提供过多选项
- 除非必要,不要提供多种方法
- 提供默认方案并给出逃生出口

## 高级:包含可执行代码的Skill

### 解决问题而非推卸
- 处理错误条件而不是推卸给Claude
- 配置参数应有充分理由并加以记录,避免"巫术常量"

### 提供实用脚本
- 比生成代码更可靠,节省token和时间
- 确保跨使用的一致性
- 明确执行意图:"运行脚本"(执行)vs"参见脚本"(参考阅读)

### 运行时环境
- 元数据预加载:所有Skill的name+description加载到系统提示
- 按需读取文件:使用bash Read工具从文件系统访问SKILL.md
- 高效执行脚本:通过bash执行,只有输出消耗token
- 大文件无上下文开销:参考文件在读取前不消耗上下文token

### MCP工具引用
- 使用完全限定工具名称避免"未找到工具"错误
- 格式:`ServerName:tool_name`(如BigQuery:bigquery_schema)

## 关联连接
- [[SkillBestPractices]] — Claude Code 9个最佳实践
- [[ProgressiveDisclosure]] — 渐进式披露机制
- [[SkillDesignPattern]] — 五种设计模式
- [[Anthropic]] — AI安全公司