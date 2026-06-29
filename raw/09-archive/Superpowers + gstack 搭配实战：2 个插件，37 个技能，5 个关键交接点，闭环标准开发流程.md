---
title: "Superpowers + gstack 搭配实战：2 个插件，37 个技能，5 个关键交接点，闭环标准开发流程"
source: "https://mp.weixin.qq.com/s/YpPiXV-GRhe4yX5tCivgNA"
author:
  - "[[运维有术]]"
published: false
created: 2026-06-06
description:
tags:
  - "clippings"
ingested: false
---
运维有术 *2026年4月12日 09:18*

> 🚩 2026 年「术哥无界」系列实战文档 X 篇原创计划 第 *80* 篇，AI 编程最佳实战「2026」系列第 *14* 篇
> 
> 大家好，欢迎来到 **术哥无界 | ShugeX ｜ 运维有术** 。
> 
> 我是 **术哥** ，一名专注于 AI 编程、AI 智能体、Agent Skills、MCP、云原生、AIOps、Milvus 向量数据库的 **技术实践者与开源布道者** ！
> 
> **Talk is cheap, let's explore。无界探索，有术而行。**

![封面图：Superpowers + gstack 搭配架构](https://mmbiz.qpic.cn/sz_mmbiz_png/icibtH5FrDwPclicbVxBUAAxIme1mcDTfgEzjC6t1rNVsWbRIJmC5HenXV5b2FRPN3T6ellLoDYZrAK5Ves5H73RT5k3d455zPA4Bo3eDPiaWick/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

封面图：Superpowers + gstack 搭配架构

用 Claude Code 做项目的人，十有八九踩过这个坑：插件装了一堆，skill 互相抢匹配。你说"做个计划"，三个 skill 同时响应；你说"帮我测试一下"，Claude Code 不知道该走哪个流程。

折腾下来发现， **插件多不等于能力强，反而让行为变得不可预测** 。

翻了一圈 GitHub 上关注度很高的两个 Claude Code 插件项目 - Superpowers（145K Star）和 gstack（69K Star），发现一个有意思的事： **这两者的能力边界几乎没有重叠** 。Superpowers 专注"怎么写好代码"，gstack 专注"做什么、做成什么样、怎么上线"。

一个管思考，一个管执行。这组合不是拍脑袋想出来的 - 两个项目的设计哲学、技能架构、触发机制从源码层面就决定了它们天然互补。

今天这篇文章，不是入门介绍。之前已经分别写过 Superpowers 的 14 个 Skills 实战和 gstack 的 23 个 AI 技能实战。这一篇专门拆解： **为什么这两个插件能搭配、怎么搭配、从源码看交接点在哪** 。

## 1\. 先搞清楚：为什么是这两个插件

很多人装插件时只看功能列表 - 这个有 code review，那个也有；这个能写计划，那个也能。功能列表看着重叠，但实际用起来天差地别。

翻完两个项目的源码和设计文档后，我发现一个关键区别：

**Superpowers 是方法论框架** - 它的核心是一个 94% PR 拒绝率的开源项目（来源：Superpowers CLAUDE.md），对待代码质量极其严格。它的 14 个 Skills 不是功能列表，而是一套工程纪律：brainstorming 强制"先想后做"、test-driven-development 强制 TDD 红绿循环、systematic-debugging 强制"找不到根因就不能修"、subagent-driven-development 强制"实现者和审查者绝不在同一个上下文里"。

**gstack 是角色化虚拟团队** - 它的核心是 Garry Tan（YC CEO）的日常开发工具集。23 个斜杠命令每个对应一个专家角色： `/office-hours` 是 YC 合伙人做产品诊断、 `/plan-ceo-review` 是 CEO 挑战产品方向、 `/qa` 是 QA 主管跑真实浏览器测试、 `/ship` 是发布工程师跑完整发布流水线。

这两个项目的差异从作者背景就能看出来：Jesse Vincent 是开源老兵，关注的是 **工程规范和代码质量** ；Garry Tan 是投资了 Coinbase、Instacart 的 YC 总裁，关注的是 **产品决策和全生命周期交付** 。

![Superpowers 与 gstack 的能力边界对比](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

Superpowers 与 gstack 的能力边界对比

从源码结构看差异更明显：

| 维度 | Superpowers | gstack |
| --- | --- | --- |
| 技能数量 | 14 个 Skills | 23 个斜杠命令 + 8 个工具 |
| 源码结构 | 每个技能一个 `SKILL.md` （纯 Markdown） | TypeScript + Go Template 生成 `SKILL.md` |
| 触发方式 | **自动触发**  （Agent 检测到适用场景就启动） | **手动触发**  （用户输入斜杠命令） |
| 核心关注 | 代码工程方法论（TDD、调试、审查） | 产品全生命周期（战略、设计、QA、发布、监控） |
| 哲学文档 | 无独立哲学文档（哲学内嵌在技能提示词中） | `ETHOS.md`  （Boil the Lake、Search Before Building、User Sovereignty） |
| 架构文档 | 无（纯 Skill 文件，无运行时依赖） | `ARCHITECTURE.md`  （Bun + Playwright 守护进程模型） |
| 安装路径 | `~/.claude/skills/superpowers-*` | `~/.claude/skills/gstack/`  \+ 符号链接 |

一句话总结差异： **Superpowers 是"怎么写好代码"的纪律框架，gstack 是"做成什么样、怎么上线"的执行工具箱** 。

## 2\. 从源码看兼容性：为什么不会冲突

"两个插件能不能同时装"这个问题，答案藏在安装结构和命令命名空间里。

### 2.1 安装路径隔离

Superpowers 通过官方插件市场安装，技能文件落在 `~/.claude/skills/` 下以 `superpowers-` 为前缀的目录中。

gstack 通过 `git clone` 安装到 `~/.claude/skills/gstack/` ，然后运行 `./setup` 创建符号链接 - 在 `~/.claude/skills/` 下为每个技能单独建一个目录（如 `qa/` 、 `review/` 、 `ship/` ），里面放一个指向 `gstack/` 对应目录的 `SKILL.md` 符号链接。

来源：gstack CLAUDE.md 的 "Dev symlink awareness" 章节明确说明了这个设计。

```
~/.claude/skills/
├── superpowers-brainstorming/     ← Superpowers 的技能目录
├── superpowers-writing-plans/
├── superpowers-systematic-debugging/
├── ...（14 个 superpowers 技能）
├── gstack/                        ← gstack 的主仓库
├── qa/                            ← gstack 的符号链接
│   └── SKILL.md → ../gstack/qa/SKILL.md
├── review/
│   └── SKILL.md → ../gstack/review/SKILL.md
└── ...（23+ 个 gstack 技能符号链接）
```

两个项目的文件完全隔离， **在磁盘层面没有冲突** 。

### 2.2 命名空间隔离

Superpowers 的技能通过 **自动触发机制** 激活 - Agent 在执行任务前检查是否有适用的 Skill，没有显式的斜杠命令。README 原文是："The agent checks for relevant skills before any task. Mandatory workflows, not suggestions."

gstack 的技能通过 **斜杠命令手动触发** - 用户输入 `/qa` 、 `/ship` 、 `/review` 等命令激活。README 的设计是："all slash commands, all Markdown."

一个自动触发，一个手动触发。 **在激活机制层面没有冲突** 。

但有一个需要注意的点：gstack 支持无前缀模式（ `/qa` ）和前缀模式（ `/gstack-qa` ）。如果你同时装了其他也有 `/review` 命令的插件，建议用前缀模式：

```
cd ~/.claude/skills/gstack && ./setup --prefix
```

这样 gstack 的所有命令变成 `/gstack-qa` 、 `/gstack-review` 、 `/gstack-ship` ，彻底避免命名冲突。

来源：gstack README 的 Troubleshooting 部分。

### 2.3 触发机制的互补性

这是兼容设计里精妙的一点。

Superpowers 的自动触发处理的是 **编码过程中的决策点** ："要写代码了 → 先检查是不是该 brainstorming"、"写完了 → 是不是该做 code review"、"遇到 bug → 是不是该启动 systematic-debugging"。

gstack 的手动触发处理的是 **产品流程中的决策点** ："需求想清楚了 → 跑 `/plan-ceo-review` 挑战一下方向"、"代码写完了 → 跑 `/qa` 用真实浏览器验证"、"准备上线 → 跑 `/ship` 发布"。

两者在不同层面做决策， **不抢同一个触发点** 。

*Superpowers 自动触发处理编码过程决策，gstack 手动触发处理产品流程决策，两者在不同层面做决策，不抢同一个触发点。*

### 2.4 需要注意的冲突点

从调研中整理出 4 个潜在冲突：

| 冲突类型 | 说明 | 解决方案 |
| --- | --- | --- |
| CLAUDE.md 配置 | 两个项目都需要在 CLAUDE.md 中声明 | 用 `## Superpowers` 和 `## gstack` 分区管理 |
| 命令名称 | 无前缀模式下可能命令重叠 | gstack 使用 `./setup --prefix` 启用前缀 |
| Token 消耗 | 两套技能文件同时占用上下文窗口 | 按需启用，不用的技能暂时移出 CLAUDE.md |
| 上下文窗口 | 两套技能文件总大小可能达到数百 KB | gstack 的 `/freeze` 限制编辑范围 |

Token 消耗是实际使用中 **需要重点留意的问题** 。两套技能文件同时在上下文里，意味着每次对话都要消耗额外的 Token 加载这些技能描述。如果任务只需要其中一个插件的能力，建议暂时禁用另一个。

## 3\. 技能路由表：37 个技能的精确分工

两个插件加起来 37 个技能（14 + 23），但分工比数字重要得多。从官方源码提取出一张完整的技能路由表，任何任务先查表。

| 开发阶段 | 任务 | 走 Superpowers | 走 gstack | 说明 |
| --- | --- | --- | --- | --- |
| **需求分析** | 想清楚要做什么 | ✅ `brainstorming` | — | Superpowers 强制在写代码前完成设计审批 |
| **产品方向** | 挑战产品方向和优先级 | — | ✅ `/office-hours` | gstack 的 YC 合伙人视角做产品诊断 |
| **计划撰写** | 写实施计划 | ✅ `writing-plans` | — | Superpowers 专长的流程 |
| **计划审查** | 多视角审查计划 | — | ✅ `/autoplan` | CEO → 设计 → 工程自动审查流水线 |
| **编码实现** | 写代码 | ✅ `test-driven-development` | — | 强制 TDD 红绿循环 |
| **编码实现** | 子代理开发 | ✅ `subagent-driven-development` | — | 每个任务派独立子代理 + 两阶段审查 |
| **调试** | 系统 bug 排查 | ✅ `systematic-debugging` | — | 4 阶段根因分析，禁止瞎猜 |
| **调试** | 看真实页面效果 | — | ✅ `/browse` | 真实 Chromium 浏览器，~100ms 响应 |
| **代码审查** | 内部审查 | ✅ `requesting-code-review` | — | 独立 reviewer 通道，作者审查者分离 |
| **代码审查** | Staff 工程师级别审查 | — | ✅ `/review` | 找 CI 通过但生产爆炸的 Bug |
| **代码审查** | 跨模型第二意见 | — | ✅ `/codex` | OpenAI Codex 独立审查 |
| **质量验证** | 完成前自检 | ✅ `verification-before-completion` | — | 声明完成前必须收集证据 |
| **质量验证** | 端到端 QA | — | ✅ `/qa` | 真实浏览器测试 + 自动修 Bug |
| **安全审计** | 安全检查 | — | ✅ `/cso` | OWASP Top 10 + STRIDE |
| **设计审查** | 80 项设计审计 | — | ✅ `/plan-design-review` | AI Slop 检测 + 交互状态覆盖 |
| **发布** | 发布流水线 | — | ✅ `/ship` | 测试 + 覆盖率 + PR |
| **发布** | 合并 + 部署 | — | ✅ `/land-and-deploy` | CI + 部署验证 |
| **监控** | 上线后观察 | — | ✅ `/canary` | 控制台错误 + 性能回归 |
| **分支管理** | Git Worktree 隔离 | ✅ `using-git-worktrees` | — | 并行开发不污染主分支 |
| **分支管理** | 分支收尾 | ✅ `finishing-a-development-branch` | — | 验证测试 + 合并/PR/清理 |

有个细节值得说：gstack 的 `/plan-ceo-review` 和 Superpowers 的 `brainstorming` 看起来都做"需求分析"，但视角完全不同。

从源码看，Superpowers 的 `brainstorming` （来源： `skills/brainstorming/SKILL.md` ）是一个 **结构化的需求精炼流程** ：先探索项目上下文 → 一次问一个问题 → 提出 2-3 种方案 → 分段展示设计让用户审批 → 写设计文档 → 转入 `writing-plans` 。它关注的是这个功能怎么实现。

gstack 的 `/office-hours` （来源： `docs/skills.md` 的 office-hours 章节）是一个 **产品方向诊断** ：六个强制问题重构产品认知、挑战你的前提假设、生成实施替代方案。它关注的是这个产品值不值得做。

一个是工程视角的怎么做，一个是商业视角的做不做。视角不同，不冲突，反而互补。

你在项目中用过类似的搭配方案吗？欢迎在评论区聊聊。

## 4\. 五个关键交接点：从源码拆解

"能装在一起"只是第一步，真正的问题是： **两个插件的技能之间怎么衔接** 。从源码里提取出 5 个关键的交接点。

### 4.1 交接点一：brainstorming → /autoplan（从"怎么做"到"做得对不对"）

这是第一个交接点：Superpowers 的 `brainstorming` 完成需求精炼和设计文档后，可以让 gstack 的 `/autoplan` 接手做 **多视角计划审查** 。

从源码看这个交接为什么自然：

Superpowers 的 `brainstorming` 的终端状态（来源：SKILL.md 第 66 行）明确写道："The terminal state is invoking writing-plans. Do NOT invoke frontend-design, mcp-builder, or any other implementation skill." 也就是说，brainstorming 的输出是一份 **设计文档** （ `docs/superpowers/specs/YYYY-MM-DD-<topic>-design.md` ）。

gstack 的 `/autoplan` （来源：README）读取设计上下文，自动运行 CEO → 设计 → 工程三阶段审查："Runs CEO → design → eng review automatically with encoded decision principles. Surfaces only taste decisions for your approval."

**交接机制** ：设计文档作为桥梁。brainstorming 输出的设计文档，正好是 `/autoplan` 需要的输入。

### 4.2 交接点二：writing-plans → /plan-eng-review（从"计划够不够详细"到"架构有没有问题"）

Superpowers 的 `writing-plans` （来源：README）把工作拆成 2-5 分钟的微任务，每个任务包含精确的文件路径、完整代码、验证步骤。这是一个 **工程可执行的计划** 。

但 Superpowers 的计划审查只有自身的 `requesting-code-review` ，侧重代码规范和质量。它 **不审查架构层面的问题** - 数据流、状态转换、失败模式、信任边界。

这正是 gstack 的 `/plan-eng-review` （来源： `docs/skills.md` ）覆盖的领域："Lock in architecture, data flow, diagrams, edge cases, and tests. Forces hidden assumptions into the open." 它还会生成 ASCII 架构图、测试矩阵、数据流图。

**交接机制** ：Superpowers 的实施计划文件 → gstack 的 `/plan-eng-review` 读取并做架构层面审查。

### 4.3 交接点三：test-driven-development → /qa（从"单元测试通过"到"真实浏览器验证"）

这个交接点尤为关键，也最能体现两者互补的价值。

Superpowers 的 `test-driven-development` （来源：README）强制 RED-GREEN-REFACTOR 循环：写失败测试 → 看它失败 → 写最小代码 → 看它通过 → 提交。它在源码层面的注释甚至说："Deletes code written before tests" - 如果你在测试之前写了生产代码，它会删掉重来。

但 TDD 验证的是 **单元和集成层面的正确性** 。它不验证：

- 页面在真实浏览器里渲染是否正确
- 用户交互流程是否顺畅
- 前后端联调是否有问题
- 不同视口下的布局是否正常

这些正是 gstack 的 `/qa` （来源： `docs/skills.md` 的 qa 章节）做的事。它启动真实 Chromium 浏览器，跑完整用户流程，发现 bug 自动修、修完自动生成回归测试。

**交接机制** ：TDD 通过后 → gstack `/qa` 接手做端到端验证。

![技能路由表可视化](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

技能路由表可视化

### 4.4 交接点四：systematic-debugging → /investigate（从"方法论"到"实战调试"）

Superpowers 的 `systematic-debugging` （来源： `skills/systematic-debugging/SKILL.md` ）是一套 **4 阶段根因分析方法论** ：

1. **Phase 1: Root Cause Investigation** - 读错误信息、复现、检查变更、收集证据
2. **Phase 2: Pattern Analysis** - 找正常代码对比、识别差异
3. **Phase 3: Hypothesis and Testing** - 提出单一假设、最小化测试
4. **Phase 4: Implementation** - 写失败测试、修根因、验证

源码里有一条铁律（第 19 行）：NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST。如果 3 次修复都失败，它不是继续试第 4 次，而是让你 **质疑架构本身** 。

gstack 的 `/investigate` （来源： `docs/skills.md` ）遵循同样的"铁律：没有调查就没有修复"原则，但它多了 **浏览器级别的调试能力** 。Superpowers 的调试是在代码和测试层面进行的，gstack 可以启动浏览器去看真实的 DOM、网络请求、控制台错误。

**交接机制** ：Superpowers 的调试定位到可能是前端问题 → 切换到 gstack 的 `/investigate` 用浏览器做进一步排查。

### 4.5 交接点五：finishing-a-development-branch → /ship（从"代码完成"到"发布上线"）

Superpowers 的 `finishing-a-development-branch` （来源：README）是分支收尾的 checklist：验证测试通过 → 提供选项（合并/PR/保留/丢弃） → 清理 worktree。

gstack 的 `/ship` （来源： `docs/skills.md` 的 ship 章节）是完整的发布流水线：同步 main → 运行测试 → 审查覆盖率 → push → 创建 PR。如果项目没有测试框架，它甚至会自动搭建。

**交接机制** ：Superpowers 的分支收尾完成后 → gstack 的 `/ship` 接手发布。这是一个 **天然的线性衔接** - 一个负责"代码准备好了"，另一个负责"把它送出去"。

## 5\. 标准开发闭环：一条龙走完

把上面的 5 个交接点串起来，就是一条从想法到上线的完整路径：

```
[需求想法]
    ↓
Superpowers: brainstorming           ← 想清楚要做什么
    ↓
gstack: /autoplan                    ← 多视角审查计划
    ↓
Superpowers: writing-plans           ← 写可执行的实施计划
    ↓
Superpowers: using-git-worktrees     ← 创建隔离工作空间
    ↓
Superpowers: subagent-driven-development ← 子代理逐任务开发
    ↓
Superpowers: test-driven-development ← TDD 红绿循环
    ↓
gstack: /qa                          ← 真实浏览器端到端验证
    ↓
Superpowers: verification-before-completion ← 收集完成证据
    ↓
Superpowers: requesting-code-review  ← 独立 reviewer 审查
    ↓
gstack: /review                      ← Staff 工程师级别审查
    ↓
Superpowers: finishing-a-development-branch ← 分支收尾
    ↓
gstack: /ship                        ← 发布流水线
    ↓
gstack: /land-and-deploy             ← 合并 + 部署
    ↓
gstack: /canary                      ← 上线后监控
    ↓
[完成]
```

注意这个闭环的节奏： **Superpowers 和 gstack 像接力赛一样交替工作** 。Superpowers 处理编码质量相关的环节（设计、实现、测试、审查），gstack 处理外部世界相关的环节（浏览器验证、发布、部署、监控）。

不是每个项目都需要走完整个闭环。日常开发中更常见的用法是按需组合：

| 场景 | 推荐技能组合 |
| --- | --- |
| 纯后端功能开发 | Superpowers 全套（brainstorming → TDD → review → branch） |
| 前端功能开发 | Superpowers 编码 + gstack `/qa` + `/browse` 验证 |
| Bug 修复 | Superpowers `systematic-debugging` + gstack `/browse` （如需看页面） |
| 需求探索 | gstack `/office-hours` + `/plan-ceo-review` → Superpowers `brainstorming` |
| 安全审计 | gstack `/cso` （独立使用） |
| 快速原型 | gstack `/autoplan` → 编码 → `/ship` （省掉 Superpowers 的重量级流程） |

## 6\. CLAUDE.md 配置模板

光装好插件不够，还得在 `CLAUDE.md` 里写清楚分工裁决。Claude Code 遇到模糊指令时，会按这个配置决定走哪个技能。

以下是经过调研验证的配置模板：

```
# Superpowers + gstack 搭配配置

## Superpowers（思考与流程层）
负责所有 plan、brainstorm、debug、TDD、verify、code review。
触发方式：自动触发。

## gstack（执行与外部世界层）
负责浏览器操作、QA、ship、deploy、canary、安全审计。
触发方式：斜杠命令手动触发。

## 浏览器规则
使用 /browse 作为唯一浏览器入口。
禁止使用 mcp__claude-in-chrome__* 操作浏览器。

## 分工裁决
- 计划撰写 → Superpowers: writing-plans
- 计划多视角审查 → gstack: /autoplan
- 编码 → Superpowers: test-driven-development
- 调试 → Superpowers: systematic-debugging
- 真实环境验证 → gstack: /qa
- 代码审查 → Superpowers: requesting-code-review
- 发布 → gstack: /ship
- 安全审计 → gstack: /cso

Available skills: /office-hours, /plan-ceo-review, /plan-eng-review,
/plan-design-review, /design-consultation, /design-shotgun, /design-html,
/review, /ship, /land-and-deploy, /canary, /benchmark, /browse, /qa,
/qa-only, /design-review, /setup-browser-cookies, /setup-deploy, /retro,
/investigate, /document-release, /codex, /cso, /autoplan, /pair-agent,
/careful, /freeze, /guard, /unfreeze, /gstack-upgrade, /learn
```

这段配置的核心作用是 **把模糊的指令映射到确定的技能** 。没有这个配置，Claude Code 在遇到"做个计划"这种泛指令时会随机匹配。有了这个配置，行为变得可预测、可复现。

## 7\. 安装步骤

两步搞定，不需要额外依赖。

**第一步：安装 Superpowers**

```
/plugin install superpowers@claude-plugins-official
```

如果你还想要 Superpowers 的完整扩展（实验工具、Chrome 底层控制），可以额外装：

```
/plugin install superpowers-chrome@superpowers-marketplace
/plugin install superpowers-lab@superpowers-marketplace
```

来源：Superpowers README 的 Installation 章节。

**第二步：安装 gstack**

在 Claude Code 中粘贴以下命令：

```
git clone --single-branch --depth 1 https://github.com/garrytan/gstack.git \
  ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup
```

如果担心命令冲突，用前缀模式安装：

```
cd ~/.claude/skills/gstack && ./setup --prefix
```

来源：gstack README 的 "Install — 30 seconds" 章节。

**验证安装** ：开一个新的 Claude Code 会话，说一句： help me plan this feature。如果 Superpowers 的 brainstorming 自动启动，说明第一个装好了。然后输入 `/qa` ，如果 gstack 的 QA 技能响应，说明第二个也装好了。

## 8\. 两种推荐搭配方案

根据调研和源码分析，推荐两种搭配方案，适配不同场景。

### 方案 A：Superpowers 为主，gstack 为辅

适合 **追求工程规范的团队或技术项目** 。

核心引擎用 Superpowers 的自动触发流程（brainstorming → writing-plans → subagent-driven-development → TDD → code review → branch finishing），日常编码完全由 Superpowers 驱动。

只在关键节点请 gstack 出场：

- 计划审查： `/autoplan` （多视角审查）
- 前端验证： `/qa` （真实浏览器测试）
- 发布上线： `/ship` → `/land-and-deploy`
- 安全检查： `/cso` （OWASP + STRIDE）

好处是 Superpowers 的自动触发机制能保证编码质量，gstack 的手动触发不会干扰日常工作流。

### 方案 B：gstack 为主，Superpowers 为辅

适合 **个人开发者、创业者、快速原型开发** 。

核心引擎用 gstack 的 Sprint 流程（ `/office-hours` → `/plan-ceo-review` → `/plan-eng-review` → 编码 → `/review` → `/qa` → `/ship` ），用产品视角驱动开发。

只在代码质量关键点请 Superpowers 出场：

- 编码时： `test-driven-development` （强制 TDD）
- 调试时： `systematic-debugging` （系统化根因分析）
- 完成时： `verification-before-completion` （完成前验证）

好处是 gstack 的产品视角更适合快速迭代，Superpowers 的工程纪律在关键节点兜底。

![两种搭配方案的适用场景](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

两种搭配方案的适用场景

## 9\. 实战案例：从需求到上线走一遍

用一个真实场景走一遍完整的搭配流程。假设需求是： **给 SaaS 后台管理系统加一个用户行为分析看板** 。

**阶段一：想清楚（Superpowers + gstack 配合）**

先让 Superpowers 的 `brainstorming` 自动启动。它会问几个关键问题：看板要展示哪些指标？数据来源是什么？更新频率？目标用户是运营还是产品经理？

设计文档写完后，不急着开干。调用 gstack 的 `/autoplan` ，让它从 CEO、设计、工程三个视角审查这份设计文档。大概率会被挑战：你真的需要实时更新吗？30 秒延迟行不行？这个功能是 3 个页面就能搞定的 MVP，还是需要完整的分析平台？

**阶段二：写代码（Superpowers 主导）**

计划确认后，Superpowers 接管： `writing-plans` 拆成微任务 → `using-git-worktrees` 创建隔离分支 → `subagent-driven-development` 逐任务派子代理开发 → `test-driven-development` 强制先写测试。

后端 API、数据聚合逻辑、前端组件 - 每一步都在 TDD 的红绿循环里完成。

**阶段三：验证（gstack 接手）**

单元测试全部通过后，进入 gstack 的领域。 `/qa` 启动真实 Chromium 浏览器，打开本地开发服务器，点一遍所有页面，检查图表渲染、数据加载、错误处理、移动端布局。发现 bug 自动修、修完自动生成回归测试。

如果设计上有疑虑，跑一遍 `/plan-design-review` ，让它从 80 项设计维度打分：空状态有没有处理？加载状态怎么展示？数据为 0 时显示什么？图表颜色对比度够不够？

**阶段四：审查与发布（两个插件交替）**

Superpowers 的 `verification-before-completion` 收集所有证据：测试报告、QA 报告、截图。然后 `requesting-code-review` 开一个独立 reviewer 通道做代码审查。

审查通过后，gstack 的 `/ship` 接手发布：同步 main → 运行测试 → 审查覆盖率 → push → 创建 PR。如果项目没有测试框架， `/ship` 还会自动搭建一个。

PR 合并后， `/land-and-deploy` 等 CI 通过、等部署完成、验证生产环境。最后 `/canary` 监控上线后的控制台错误和性能指标。

整个过程，两个插件在接力赛中交替工作，每一步都有明确的产物和交接。

![标准开发闭环流程图](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

标准开发闭环流程图

说到底，Superpowers 和 gstack 能搭配使用的根本原因，不是谁兼容了谁，而是两者在设计上就 **没重叠** 。一个解决怎么写好代码的问题，一个解决做成什么样、怎么上线的问题。

把 **思考和执行** 分给两个专注的工具，比装十个功能重叠的插件要高效得多。更少的组件，更清晰的边界，更明确的交接 - 这不只是 Claude Code 插件的搭配哲学，也是任何复杂系统的最优配置策略。

如果你也在被 Claude Code 的 skill 冲突困扰，建议收藏这篇文章，下次配置的时候翻出来对照着搭。如果你的同事也在折腾插件搭配，转发给他看看这套方案。

**相关资源**

Superpowers GitHub：https://github.com/obra/superpowers

gstack GitHub：https://github.com/garrytan/gstack

gstack 技能深度文档：https://github.com/garrytan/gstack/blob/main/docs/skills.md

gstack 架构文档：https://github.com/garrytan/gstack/blob/main/ARCHITECTURE.md

gstack 设计哲学：https://github.com/garrytan/gstack/blob/main/ETHOS.md

**好啦，谢谢你观看我的文章，如果喜欢可以点赞转发给需要的朋友，我们下一期再见！敬请期待！**

**扫码关注，获取更多 AI 工具的实战经验和最佳实践。不错过每一篇干货！**

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**微信扫一扫赞赏作者**

AI编程最佳实战「2026」 · 目录

继续滑动看下一个

术哥无界

向上滑动看下一个