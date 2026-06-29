---
title: "摘要-skill-anthropic-doc-part2"
type: source
tags: [来源, Agent Skill, Anthropic]
sources: [raw/01-articles/02-无限上下文？Skill渐进式披露机制——精读《Equipping agents for the real world with Agent Skills》②.md]
last_updated: 2026-06-17
---

## 核心摘要

本文精读 Anthropic 官方文档第二部分，深入解析 Skill 的内部构成与渐进式披露（Progressive Disclosure）机制。通过三层加载（元数据层→正文层→附属文件层）和认知执行分离架构，让 Claude 拥有近似无限上下文的工作方式，突破模型上下文窗口限制。

## 关键洞察

### Skill 的文件结构

每个 Skill 是一个文件夹，核心文件是 `SKILL.md`——技能的使用说明书和入口。顶部 YAML front matter 包含：
- **name**：技能名称（如 `pdf`）
- **description**：简要说明技能功能（如"从PDF中抽取文本和表单字段"）

系统在 Agent 启动时扫描所有技能的 `SKILL.md`，预加载 name 和 description 到系统提示，实现**索引而不展开**。

### 渐进式披露的三层加载

类比：先读目录确定主题，再读相关章节掌握要点，最后按需查阅详细附录。

| 层级 | 文件位置 | 内容 | 加载方式 | Token 消耗 |
|------|---------|------|---------|-----------|
| Level 1 | SKILL.md 顶部 YAML | name + description | 始终加载 | ~100 tokens |
| Level 2 | SKILL.md 正文 | 核心指令与 SOP 逻辑 | 技能被触发时加载 | < 5000 tokens |
| Level 3+ | 其他文件 | 文档/配置/脚本 | 按需加载 | 理论上无限 |

### 认知与执行的分离

**核心机制**：模型上下文窗口只包含推理所需文字信息，执行发生在外部虚拟机。

- **认知空间（上下文窗口）**：Level 1 元数据 + 被触发技能的部分 Level 2 内容
- **执行空间（文件系统+执行工具）**：外部文件、脚本和数据，Claude 调用工具执行

**例子**：PDF Skill 指令要求运行 `scripts/extract_fields.py` 时：
- Claude 发出 `run bash command` 命令
- 脚本在虚拟机运行（5000行代码不进入上下文）
- 只返回执行结果（"字段提取完成，已保存为 forms.json"）

### 外部脚本的确定性与效率

- **确定性**：排序、提取、数学运算等任务，脚本执行结果可重复验证
- **效率**：比 LLM 生成代码更快、成本更低
- **价值**：Skill 确保 Claude 不仅知道怎么做，还能每次做对

### Skill 被触发时的动态变化

1. **初始阶段**：上下文包含系统提示 + 所有技能元数据 + 用户输入
2. **技能触发**：Claude 判断任务相关，调用工具读取 SKILL.md 正文
3. **按需展开**：SOP 提到什么文件就读取什么，未提及的留在文件系统
4. **执行脚本**：发出执行命令，脚本在虚拟机运行，只返回结果
5. **任务完成**：综合上下文内容（SOP + 脚本输出）生成响应

## 核心思想

**近似无限上下文不是模型参数魔法，而是架构思想**——让模型上下文只装载需要思考的那一页，把真正的世界留在随时可访问的文件系统里。

## 关联连接

- [[摘要-skill-anthropic-doc-part1]] — 第一部分：Skill 核心定义
- [[Anthropic]] — 文档来源公司
- [[AgentSkill]] — 渐进式披露的主体对象
- [[ProgressiveDisclosure]] — 渐进式披露机制
- [[CognitionExecutionSeparation]] — 认知与执行分离架构