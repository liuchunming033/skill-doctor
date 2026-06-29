---
title: "摘要-skill-google-5-patterns"
type: source
tags: [来源, Agent Skill, Google]
sources: [raw/01-articles/04-Google总结了5种Skill设计模式，让Agent稳定输出.md]
last_updated: 2026-06-18
---

## 核心摘要

Google Cloud Tech 团队研究了 Anthropic、Vertex AI、Google 内部的 Skill 构建方式，总结出 5 种设计模式解决 Agent 输出不稳定问题。问题不在格式而在内容设计逻辑。五种模式：ToRapper（按需注入知识）、Generator（固定输出结构）、Reviewer（分离审查与检查规则）、Inversion（先问清需求再开工）、Pipeline（分步执行流程）。模式可叠加使用，先判断问题是知识/结构/审查/澄清/流程问题，选对模式才能稳定输出。

## 关键洞察

### 问题根源

**Skill 搭好了但输出不稳定**：
- 一会儿格式乱、一会儿漏步骤、一会儿自信地答偏
- 问题不在格式（主流工具已统一 SKILL.md 格式规范）
- **真正问题在内容设计**：Skill 里面的逻辑究竟该怎么组织

### 五种设计模式

| 模式 | 解决的问题 | 核心做法 | 适用场景 |
|------|-----------|---------|---------|
| ToRapper | 知识什么时候交给 Agent | 按需注入：判断命中领域才加载知识 | 技术栈规范、团队约定 |
| Generator | 输出格式不稳定 | 固定结构：模板+风格指南+补问变量 | API文档、标准化报告、commit message |
| Reviewer | 审查任务要推倒重来 | 分离规则：checklist（可替换）+流程（不动） | 代码审查、安全检查、合规审查 |
| Inversion | 信息不全却急着开工 | 先问后做：Discovery→Constraints→Synthesis | 模糊需求、缺少约束的任务 |
| Pipeline | 多步骤任务总有人跳步骤 | 分步执行：定义步骤+显式门控+按需加载 | 文档生成、复杂修改、发布流程 |

### 模式详解

#### 1. ToRapper（按需注入知识）

**问题**：把技术栈全部规范提前塞进 System Prompt，浪费 context，易被干扰。

**做法**：
- 把内容放进 references
- Skill 判断当前任务是否进入某个领域
- 只有判断命中才加载那一套知识

**本质**：Skill 像总闸门，负责在合适时把某个专家手册接进上下文。

#### 2. Generator（固定输出结构）

**问题**：让 Agent 写文档，今天长这样、明天长成另一样。原因：模型每次现场重新决定输出该长什么样。

**做法**：
- 输出结构固定在**模板**里（回答 what to produce）
- 表达方式固定在**风格指南**里（回答 how to write）
- SKILL.md 先补问缺失变量，再把内容填进去

#### 3. Reviewer（分离审查与检查规则）

**问题**：审查任务经常推倒重来。原因："检查什么"和"怎么检查"写混了。

**做法**：
- **检查什么** → 放进 checklist（可替换）
- **怎么检查** → 留在 SKILL.md（流程不动）

**价值**：流程不动、规则可换。今天 Python 风格审查，明天 OWASP 安全检查，后天合规规则，只需替换 checklist。输出统一成 error/warning/info 层级。

#### 4. Inversion（先问清需求再开工）

**问题**：Agent 太爱猜，一拿到模糊需求就急着生成，信息不够就自己补，补得非常自信。

**做法**：把流程反过来——Agent 先发问，用户先回答。三阶段：
1. **Discovery**：先确认你到底要解决什么问题
2. **Constraints**：把平台、技术栈、限制条件、交付要求问完整
3. **Synthesis**：信息齐了之后才允许开始生成

**关键**：用门控指令明确规定——信息没齐不准开工。

#### 5. Pipeline（分步执行流程）

**问题**：多步骤任务容易跳步骤。原因：当成一句 prompt，模型中途偷懒。

**做法**：
- 直接把 SKILL.md 写成工作流
- 定义第一步做什么、第二步做什么
- 定义什么时候能进入下一步
- 中间放 gate（显式门控）

**额外价值**：每一步只加载当前所需的 references 和 templates，让 context 一直保持干净。

### 模式选择指南

**决策树**：

1. **这个 Skill 是否要产出内容？**
   - 从模板里产出 → **Generator**
   - 运行时加载某一套知识 → **ToRapper**
2. **这个 Skill 是否在评估已有输入？** → **Reviewer**
3. **开始之前必须先向用户补全信息？** → **Inversion**
4. **有严格步骤和确认点，不能跳过？** → **Pipeline**

### 模式叠加

这些模式之间可以互相叠加：
- Generator 前面可以接 Inversion
- Pipeline 结尾可以接 Reviewer
- ToRapper 几乎可以叠在任何模式上，负责补知识

## 核心思想

别再把越来越复杂的指令一股脑塞进同一个 System Prompt。真正可靠的 Skill 靠的是更合适的结构。先判断自己遇到的到底是**知识问题、结构问题、审查问题、澄清问题还是流程问题**——模式选对了，Agent 才会稳定。

## 关联连接

- [[Google]] — 文档来源公司
- [[SkillDesignPattern]] — 五种设计模式总览
- [[ToRapperPattern]] — 按需注入知识模式
- [[GeneratorPattern]] — 固定输出结构模式
- [[ReviewerPattern]] — 分离审查与检查规则模式
- [[InversionPattern]] — 先问清需求再开工模式
- [[PipelinePattern]] — 分步执行流程模式