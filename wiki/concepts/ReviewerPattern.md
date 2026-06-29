---
title: "ReviewerPattern"
type: concept
tags: [概念, Agent, Skill, 设计模式]
sources: [raw/01-articles/04-Google总结了5种Skill设计模式，让Agent稳定输出.md]
last_updated: 2026-06-18
---

## 定义

Reviewer 模式（分离审查与检查规则）是 Google 总结的五种 Skill 设计模式之一，解决"为什么审查任务经常要推倒重来"的问题。核心做法：把"检查什么"和"怎么检查"硬拆开——检查什么放进 checklist（可替换）、怎么检查留在 SKILL.md（流程不动）。流程不动、规则可换，只需替换 checklist 即可适应不同审查场景。

## 解决的问题

**审查任务推倒重来**：
- 今天审查 Python 代码，明天审查安全漏洞，后天审查合规规则
- 每次审查都要重新设计 Skill
- 流程逻辑和检查规则混在一起，难以复用

**根本原因**：
- "检查什么"（检查规则）和"怎么检查"（审查流程）写混了
- 每次更换审查类型都要重新设计整个 Skill
- 无法复用已有的审查流程

## 核心做法

### 分层结构

```
SKILL.md (流程层 - 不动)
├── 审查流程：输入分析 → 规则应用 → 问题分级 → 输出报告
├── 分级逻辑：error / warning / info
└── 输出格式：统一的问题报告格式

checklists/ (规则层 - 可替换)
├── python-style-checklist.md — Python 代码风格检查规则
├── owasp-security-checklist.md — OWASP 安全检查规则
├── compliance-checklist.md — 合规规则检查清单
└── team-conventions-checklist.md — 团队约定检查清单
```

### 工作流程

1. **输入分析**：Skill 分析待审查的输入（代码、文档、配置）
2. **加载 checklist**：根据审查类型加载对应的 checklist
3. **应用规则**：逐一检查 checklist 中的规则
4. **问题分级**：将问题分为 error / warning / info 三级
5. **输出报告**：生成统一格式的问题报告

## 核心价值

### 流程不动

**审查流程标准化**：
- 输入分析步骤固定
- 问题分级逻辑固定
- 输出报告格式固定

### 规则可换

**检查规则灵活替换**：
- 今天 Python 风格审查 → 加载 `python-style-checklist.md`
- 明天 OWASP 安全检查 → 加载 `owasp-security-checklist.md`
- 后天合规规则检查 → 加载 `compliance-checklist.md`

只需替换 checklist，流程代码完全不变。

## 问题分级机制

### 三级分类

| 级别 | 定义 | 处理建议 |
|------|------|---------|
| **error** | 严重问题，必须修复 | 阻止通过，立即修复 |
| **warning** | 潜在问题，建议修复 | 提醒用户，可选修复 |
| **info** | 信息提示，可选修复 | 提供信息，由用户决定 |

### 统一输出格式

```markdown
## 审查报告

### Error (必须修复)
- [E001] 缺少输入验证
  - 位置：src/api/user.py:23
  - 规则：OWASP-A1
  - 说明：用户输入未验证可能导致注入攻击

### Warning (建议修复)
- [W001] 变量命名不规范
  - 位置：src/utils/helper.py:15
  - 规则：Python-Style-005
  - 说明：变量名应使用小写字母和下划线

### Info (信息提示)
- [I001] 代码可优化
  - 位置：src/core/engine.py:42
  - 说明：循环可以使用列表推导式简化
```

## 适用场景

- **代码审查**：Python 风格审查、JavaScript 风格审查、Go 风格审查
- **安全检查**：OWASP 安全检查、漏洞扫描、权限审查
- **合规审查**：GDPR 合规、数据安全合规、行业规范审查
- **团队约定**：命名规范、目录结构、代码组织审查

## 优势

### 可复用流程

- 审查流程只需设计一次
- 不同审查类型复用同一流程

### 快速切换

- 切换审查类型只需更换 checklist
- 不需要重新设计 Skill

### 统一输出

- 所有审查任务输出格式统一
- 易于后续处理和自动化

## 实现要点

### Checklist 设计

**规则格式**：
```markdown
## Python 风格检查清单

### 代码风格
- [PS001] 使用 4 空格缩进
- [PS002] 变量名使用小写字母和下划线
- [PS003] 类名使用驼峰命名法

### 代码质量
- [PQ001] 函数不应超过 50 行
- [PQ002] 避免深层嵌套（最多 3 层）
- [PQ003] 添加必要的注释

### 最佳实践
- [BP001] 使用类型注解
- [BP002] 异常处理应具体化
- [BP003] 避免全局变量
```

### 流程层设计

**关键逻辑**：
- 如何加载 checklist
- 如何应用规则（逐一检查）
- 如何分级问题（error/warning/info）
- 如何输出报告（统一格式）

## 与其他模式组合

- **Pipeline + Reviewer**：Pipeline 流程执行完自动审查
- **ToRapper + Reviewer**：加载领域规范后审查是否符合
- **Generator + Reviewer**：生成文档后审查是否符合模板

## 关联连接

- [[摘要-skill-google-5-patterns]] — 模式来源文档
- [[SkillDesignPattern]] — 五种设计模式总览
- [[Google]] — 提出该模式的公司