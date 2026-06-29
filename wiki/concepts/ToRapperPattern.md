---
title: "ToRapperPattern"
type: concept
tags: [概念, Agent, Skill, 设计模式]
sources: [raw/01-articles/04-Google总结了5种Skill设计模式，让Agent稳定输出.md]
last_updated: 2026-06-18
---

## 定义

ToRapper 模式（按需注入知识）是 Google 总结的五种 Skill 设计模式之一，解决"知识什么时候应该被交给 Agent"的问题。核心做法：把内容放进 references，Skill 只负责判断当前任务是否进入了某个领域（如 React 领域、数据库领域），只有判断命中才加载那一套知识。Skill 像一个总闸门，负责在合适的时候把某个专家手册接进上下文。

## 解决的问题

**知识注入时机问题**：
- 很多团队把某个技术栈的全部规范提前塞进 System Prompt
- 例如：React 规范、FastAPI 规范、团队组建约定、命名规则
- **问题**：大部分任务根本用不到这些东西
  - 既浪费 context（上下文空间）
  - 又容易被无关知识干扰（降低输出质量）

## 核心做法

### 结构设计

```
SKILL.md (判断层)
├── name: "技术栈专家"
├── description: "判断当前任务属于哪个技术栈领域"
└── 正文：
    ├── 判断逻辑：分析任务关键词、文件类型、依赖项
    └── 加载指令：如果命中某个领域，加载对应的 references

references/ (知识层)
├── react-guide.md — React 技术栈完整规范
├── fastapi-guide.md — FastAPI 技术栈完整规范
├── database-guide.md — 数据库设计规范
└── team-conventions.md — 团队约定
```

### 工作流程

1. **任务分析**：Skill 分析当前任务的关键词、文件类型、依赖项
2. **领域判断**：判断任务属于哪个技术栈领域
3. **按需加载**：只有判断命中才加载那一套知识
4. **执行任务**：在加载的知识指导下执行任务

## 本质理解

**Skill 像总闸门**：
- 不是把所有知识都提前装好
- 而是在合适的时候把某个专家手册接进上下文
- 实现知识的按需注入

**类比理解**：
- **传统方式** = 把整个图书馆的书都搬回家
- **ToRapper 模式** = 需要哪本书就去图书馆借哪本书

## 适用场景

- **技术栈规范**：React、Vue、FastAPI、Django 等框架规范
- **团队约定**：命名规范、代码风格、目录结构
- **领域知识**：安全规范、性能优化指南、架构模式
- **多技术栈项目**：项目使用多种技术栈，但单个任务只需其中一种

## 优势

### 节省上下文

- 只有需要的知识进入上下文
- 避免无关知识占用 token

### 减少干扰

- 无关知识不进入上下文
- 降低模型被无关信息干扰的概率

### 灵活扩展

- 新增技术栈只需添加新的 reference 文件
- 不影响已有的 Skill 结构

## 实现要点

### 判断逻辑设计

**判断依据**：
- 文件扩展名（`.tsx`、`.py`、`.go`）
- 依赖项（`package.json`、`requirements.txt`）
- 关键词（"React 组件"、"API 路由"、"数据库查询"）
- 目录结构（`src/components/`、`api/`）

### references 组织

- 每个领域一个独立文件
- 文件内容完整且自包含
- 避免跨 reference 的重复内容

## 与其他模式组合

- **ToRapper + Generator**：加载领域知识后，用模板生成代码
- **ToRapper + Reviewer**：加载领域规范后，审查代码是否符合规范
- **ToRapper + Pipeline**：不同步骤加载不同的领域知识

## 关联连接

- [[摘要-skill-google-5-patterns]] — 模式来源文档
- [[SkillDesignPattern]] — 五种设计模式总览
- [[Google]] — 提出该模式的公司