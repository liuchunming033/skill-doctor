---
title: "Gstack"
type: entity
tags: [工具, Claude Code, 插件, 产品交付, AI编程]
sources:
  [
    "raw/01-articles/Superpowers + gstack 搭配实战：2 个插件，37 个技能，5 个关键交接点，闭环标准开发流程.md",
  ]
last_updated: 2026-06-06
---

## 定义

Gstack 是 Garry Tan（YC CEO）的日常开发工具集，封装为 Claude Code 开源插件（69K Star）。23 个斜杠命令每个对应一个专家角色，覆盖产品决策、浏览器 QA、安全审计、发布上线、监控等全生命周期环节。

## 关键信息

**触发方式**：手动触发——用户输入斜杠命令激活，如 `/qa`、`/ship`、`/review`。

**23个核心命令（代表性）：**

| 命令               | 角色         | 用途                                       |
| ------------------ | ------------ | ------------------------------------------ |
| `/office-hours`    | YC 合伙人    | 六个强制问题做产品方向诊断                 |
| `/plan-ceo-review` | CEO          | 挑战产品方向和优先级                       |
| `/autoplan`        | 自动审查     | CEO→设计→工程三阶段计划审查                |
| `/qa`              | QA 主管      | 真实 Chromium 浏览器端到端测试，自动修 bug |
| `/browse`          | 浏览器       | 真实 Chromium，~100ms 响应                 |
| `/review`          | Staff 工程师 | 找 CI 通过但生产爆炸的 Bug                 |
| `/cso`             | 安全官       | OWASP Top 10 + STRIDE 安全审计             |
| `/ship`            | 发布工程师   | 完整发布流水线（测试→覆盖率→PR）           |
| `/land-and-deploy` | 部署工程师   | 合并 + 部署验证                            |
| `/canary`          | 监控工程师   | 上线后控制台错误 + 性能回归监控            |

**安装路径**：`~/.claude/skills/gstack/` + 每个技能的符号链接。

**命名冲突注意**：无前缀模式（`/qa`）可能与其他插件冲突，建议用前缀模式：

```
cd ~/.claude/skills/gstack && ./setup --prefix
```

启用后命令变为 `/gstack-qa`、`/gstack-ship` 等。

**`/qa` skill 双阶段原理**：

- **阶段一（推导）**：LLM 读取 `~/.gstack/projects/<slug>/...design*.md`、`test-plan.md`、当前 Git diff，确定“要验证什么”
- **阶段二（执行）**：Playwright + 真实 Chromium 执行交互，录制截图/trace/视频证据
- **阶段三（评审）**：LLM 把执行证据映射回 AC，输出 QA 结论和归因报告

两种模式：Plan-first（复用已有 test-plan，低 Token）vs Agent-first（从需求重新推导，高 Token）。企业实践推荐将测试资产缓存在仓库，仅对 Git diff 范围做增量生成。

## 关联连接

- [[Superpowers]] — 搭档插件，处理工程编码纪律
- [[OpenSpec]] — 可在需求阶段配合，提供规约输入
- [[摘要-superpowers-gstack-integration]] — 两者搭配的详细分析
- [[摘要-gstack-superpowers-perfect-loop]] — 完美闭环：两插件组合的分工与任务分流
- [[摘要-openspec-superpowers-gstack-threeinone]] — 三工具七步流程与四个串联点
- [[Playwright]] — `/qa` skill 的真实浏览器执行引擎
- [[摘要-gstack-qa-skill-workflow]] — `/qa` skill 工作原理详解
- [[AgentHumanPipeline]] — 宏观人机协作框架
