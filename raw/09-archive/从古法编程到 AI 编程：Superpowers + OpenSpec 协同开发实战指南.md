---
title: "从古法编程到 AI 编程：Superpowers + OpenSpec 协同开发实战指南"
source: "https://mp.weixin.qq.com/s?__biz=Mzg4MzcyOTQ2NQ==&mid=2247490458&idx=1&sn=f31215ae919c0c9c625eb0b47eff43bb&chksm=cf43aeccf83427daec12057f3f2c50f9abe5e91844c09e216c9f2fb3f11701af2484c6fdcf61&cur_album_id=4354638012475867143&scene=190#rd"
author:
  - "[[运维有术]]"
published: false
created: 2026-06-06
description: "🚩 2026 年「术哥无界」系列实战文档 X 篇原创计划 第 86 篇，AI 编程最佳实战「2026」系列第"
tags:
  - "clippings"
ingested: false
---
运维有术 *2026年4月18日 09:00*

> 🚩 2026 年「术哥无界」系列实战文档 X 篇原创计划 第 *86* 篇，AI 编程最佳实战「2026」系列第 *18* 篇
> 
> 大家好，欢迎来到 **术哥无界 | ShugeX ｜ 运维有术** 。
> 
> 我是 **术哥** ，一名专注于 AI 编程、AI 智能体、Agent Skills、MCP、云原生、AIOps、Milvus 向量数据库的 **技术实践者与开源布道者** ！

> **Talk is cheap, let's explore。无界探索，有术而行。**

![封面图 - 从古法到 AI：Superpowers + OpenSpec 协同开发实战手册全景信息图](https://mmbiz.qpic.cn/mmbiz_png/icibtH5FrDwPe1xlwib2SMKxLYsj3awOa2DwF7guS5AjNEQz6tNuU121AUyG2TRmIXTJoYBiae2hoicnNLk1Cmmd6ns3253LnmDuT0yrUm9icUicU4/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=0)

封面图 - 从古法到 AI：Superpowers + OpenSpec 协同开发实战手册全景信息图

*图 1：Superpowers + OpenSpec 协同开发实战手册全景概览*

假设你正在维护一个 3 年以上的老项目，代码是纯手工写的，没有测试用例，前后端耦合在一起，注释少得可怜。老板说要加一个限时抢购模块，上线时间很紧。

你想到用 AI 辅助编码来提速，但真动手了才发现问题一堆：AI 生成的代码风格和项目格格不入，改着改着把老功能搞崩了，前端改完接口后端还没同步……还不如自己写来得快。

CSDN 上有个高赞评论说得很直白： **Superpowers 值得研究的地方不是更强，而是更稳** 。另一个工具 OpenSpec 的核心理念更直接 - **在编写任何代码之前，就对要做什么达成一致** 。

这两句话放在一起看，恰好点出了老旧项目引入 AI 编/程的核心矛盾： **需求理解不准确，执行过程不可控。**

这篇文章要做的，就是用 Superpowers 和 OpenSpec 这两款工具，设计一套专门面向老旧项目的 AI 增强开发工作流。3 人团队，4 个阶段，从需求定义到代码落地，完整跑通。

## 1\. 两把钥匙：各管一摊

先说清楚这两款工具各自干什么，再说怎么配合。

![双层架构图 - OpenSpec 管需求层，Superpowers 管执行层](https://mmbiz.qpic.cn/sz_mmbiz_png/icibtH5FrDwPcicCsfKlVic07eMsVdXgiaxAdmo0CFejWUT5RgmEWdj5qAgibzDIEchpYRZ7N2au3Dwkgfy4WAu9ZC5yp59OoSUCmiczZKUSrvvENU/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=1)

双层架构图 - OpenSpec 管需求层，Superpowers 管执行层

*图 2：OpenSpec（需求层）与 Superpowers（执行层）双层分工架构*

**OpenSpec** - GitHub 上 40.9k Star，定位是 **规范驱动开发（SDD）** 。它的核心思路是把需求写成机器可理解的规范文件，让 AI 和人先在文字层面达成共识，再动手写代码。

它的双文件夹模型很清晰：

- `openspec/specs/` - 当前系统的规范，项目的事实来源
- `openspec/changes/` - 每次变更的提案、设计文档、任务清单

每份变更包含三个文件： `proposal.md` （为什么要做）、 `design.md` （技术方案）、 `tasks.md` （实施清单）。别小看这三个文件，据 CSDN 上的对比测试，使用 OpenSpec 后相同需求下 Token 消耗降低 30%-50%，返工率下降 60% 以上。

**Superpowers** - GitHub 上 158k Star，定位是 **AI 编码代理的完整工作方法论** 。它管的是 AI 写代码的过程：强制 TDD、子代理隔离、两阶段代码审查。

7 步强制流程：brainstorming → git worktree 隔离 → 拆 2-5 分钟小任务 → 子代理执行 → TDD 循环 → 代码审查 → 分支收尾。每一步都不可跳过。

一句话区分： **OpenSpec 管需求层，Superpowers 管执行层** 。一个解决 AI 理解需求不准确的问题，一个解决 AI 写代码过程不可控的问题。

## 2\. 角色重新洗牌

引入这两款工具后，3 人团队的职责会发生变化。不是简单地用 AI 替代人，而是人和 AI 的分工边界变了。

### 2.1 架构师

传统模式下架构师要画架构图、写技术方案、做 Code Review。引入工具后，架构师的核心职责变成了 **定义和消费规范** ：

- 用 OpenSpec 的 `/opsx:propose` 命令生成变更提案，把业务需求翻译成 AI 可理解的规范
- 审查 `design.md` 中的技术决策，确保不踩旧系统的坑
- 用 `/opsx:verify` 命令验证实现是否偏离设计

架构师不再是画完图就交给开发的角色，而是整个规范链条的起点和终点。

### 2.2 后端开发

后端不再需要从零写业务骨架。工作重心转移到：

- 消费 OpenSpec 生成的 `tasks.md` ，用 Superpowers 的 brainstorming 技能澄清每个任务的边界
- 依赖 Superpowers 的 TDD 循环写实现代码
- 旧系统的兼容性处理 - 这是 AI 暂时做不好的部分，需要人判断

### 2.3 前端开发

前端的变化和后端类似，但多了一个关键职责：

- 消费 `design.md` 中的接口规范，提前做页面开发
- 用 Superpowers 的子代理并行开发多个页面组件
- 当后端 API 变更时，通过 OpenSpec 的增量规范快速同步

三个角色之间不再靠口头沟通对齐，而是通过 OpenSpec 的规范文件形成 **可审查、可追溯** 的协作链条。

## 3\. 四阶段闭环工作流

![四阶段闭环流程图 - 旧代码分析→需求规约→代码生成→协同同步](https://mmbiz.qpic.cn/mmbiz_png/icibtH5FrDwPfVHvHiaHs68xCBwTq0pTZ1LBicpYXHF8WdCkTcF7iaY8nLib56UNJ7jsXfQnfv1cvVobUE28VAXTia9HJgibWaxSktfxGPyo5euwb1k/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=2)

四阶段闭环流程图 - 旧代码分析→需求规约→代码生成→协同同步

*图 3：四阶段闭环工作流全景流程*

这是整套方案的核心。每个阶段都有明确的输入、输出和工具支持。

### 3.1 阶段一：旧代码分析

老项目的关键问题不是代码烂，而是没人能完整说清楚它到底怎么运作的。AI 在这里能发挥巨大作用。

**操作步骤** ：

1. 在项目根目录执行 OpenSpec 初始化：
```
# 安装 OpenSpec
npm install -g @fission-ai/openspec@latest

# 在项目目录初始化
openspec init
```
2. 用 `/opsx:explore` 命令探索现有代码结构。这个命令的设计初衷就是 **开发前梳理思路** ，特别适合摸底老项目。
3. 让 AI 分析核心模块的依赖关系和业务逻辑，把结果写入 `openspec/specs/` 目录。这一步的产出物是 **现有系统的规范快照** 。
4. 架构师审查规范快照的准确性，补充 AI 遗漏的业务规则。别指望 AI 一次就能完全理解老项目的所有隐含逻辑 - 这部分需要人的经验补位。

**产出** ： `openspec/specs/` 目录下的现有系统规范，包括数据模型、接口列表、核心业务流程。

**关键提醒** ：这一步不要急于写代码。Phodal 在腾讯云的技术博客里提到，AI 辅助老旧系统改造的前两步永远是 **理解现有业务** 和 **设计与拆分模块** 。跳过分析直接写代码，后续返工的概率非常高。

### 3.2 阶段二：需求规约

有了旧系统的规范快照，就可以开始定义新需求了。

**操作步骤** ：

1. 架构师执行 `/opsx:propose` 命令，一步生成变更提案。OpenSpec 会自动创建包含 `proposal.md` 、 `design.md` 、 `tasks.md` 的变更目录。
2. 重点审查 `design.md` 中的技术方案，确保：
- 新功能与旧系统的数据模型兼容
- 不引入破坏性的接口变更
- 考虑到旧系统可能存在的性能瓶颈
3. 审查 `tasks.md` 中的任务拆分是否合理。按照 Superpowers 的要求，每个任务应该能在 2-5 分钟内完成。如果任务粒度太大，AI 执行时容易跑偏。

**产出** ： `openspec/changes/` 目录下完整的变更制品。

**OpenSpec 的增量规范（Delta Spec）机制在这里发挥了很大作用** 。它用 ADDED/MODIFIED/REMOVED 三种标记描述每个变更对现有规范的影响。老旧项目怕的就是改了 A 结果 B 坏了，Delta Spec 把影响面直接摆在台面上。

### 3.3 阶段三：代码生成与注入

这个阶段是 Superpowers 的主场。

**操作步骤** ：

1. 安装 Superpowers 插件：
```
# 在 Claude Code 中安装
/plugin install superpowers@claude-plugins-official
```
2. 将 OpenSpec 的 `tasks.md` 作为 Superpowers 的输入，启动 brainstorming 技能精炼每个任务。
3. Superpowers 自动进入 7 步工作流：

| 步骤 | 做什么 | 谁负责 |
| --- | --- | --- |
| brainstorming | 苏格拉底式提问，澄清任务细节 | AI + 架构师 |
| git worktree | 创建隔离分支，保护主分支 | AI 自动 |
| writing-plans | 拆解为 2-5 分钟可执行小任务 | AI 自动 |
| subagent 执行 | 每个任务派独立子代理 | AI 自动 |
| TDD 循环 | RED → GREEN → REFACTOR | AI 自动 |
| 代码审查 | 两阶段审查：规范合规 + 代码质量 | AI + 人 |
| 分支收尾 | 验证测试、合并决策 | AI + 人 |

4. 关键环节 - 处理旧系统兼容性。AI 生成的代码默认遵循现代编码规范，但老项目可能用的是旧版框架、奇特的命名规则、甚至全局变量。这部分需要人在代码审查环节重点把关。

**产出** ：经过 TDD 和代码审查的业务代码，附带测试用例。

### 3.4 阶段四：协同同步

当前后端都在并行开发时，接口变更的同步是老大难问题。

**操作步骤** ：

1. 当一方修改了接口定义，在 OpenSpec 中更新对应的增量规范。
2. 执行 `/opsx:sync` 命令，将变更的增量规格合并到主规格中。
3. 另一方消费更新后的主规格，用 Superpowers 的 systematic-debugging 技能排查兼容性问题。
4. 整个变更完成后执行 `/opsx:archive` 归档，保持规范目录的整洁。

**产出** ：同步后的系统规范，归档的变更记录。

四个阶段形成闭环：分析旧系统 → 定义新需求 → 生成代码 → 同步变更。每一轮迭代都会更新 `openspec/specs/` 中的系统规范，为下一轮开发提供更准确的起点。

## 4\. 实战跑通：给旧商城加个限时抢购

用一个具体的需求走一遍完整流程。场景是这样的：一个 3 年的旧商城系统，技术栈是 Spring Boot + jQuery + MySQL，没有测试用例，代码注释率不到 5%。需求是新增限时抢购模块。

### 4.1 第一步：摸底旧系统

先在项目根目录执行初始化：

```
openspec init
```

然后用 `/opsx:explore` 探索现有代码结构。重点关注三个模块：商品服务、订单服务、库存服务。AI 分析后生成规范快照，放到 `openspec/specs/` 目录。

架构师审查后补充了几条 AI 没发现的隐含规则：

- 库存扣减不是原子操作，高并发下可能超卖
- 商品价格存在两个地方：商品主表和订单快照表，要同时更新
- 旧系统的用户 session 放在 Redis 里，TTL 30 分钟

这些信息会被写入规范，后续所有开发活动都以这份规范为基准。

### 4.2 第二步：定义限时抢购规范

架构师执行 `/opsx:propose` ，描述需求背景： **为商城系统增加限时抢购功能，支持活动创建、库存预扣、订单快速确认** 。

OpenSpec 自动生成三个文件。以 `design.md` 为例，关键的技术决策：

- 抢购库存与商品主库存 **解耦** ，避免影响正常购买流程（对应旧系统库存扣减的隐含规则）
- 用 Redis 做库存预扣，MQ 异步落库（解决旧系统高并发超卖问题）
- 抢购订单走独立接口，不影响现有订单流程

`tasks.md` 拆分后的部分任务：

| 任务 | 预计时间 | 负责人 |
| --- | --- | --- |
| 创建 `flash_sale` 数据表 | 3 分钟 | 后端 |
| 实现 Redis 库存预扣接口 | 5 分钟 | 后端 |
| 抢购订单创建 API | 5 分钟 | 后端 |
| 抢购活动列表页面 | 4 分钟 | 前端 |
| 倒计时组件 | 3 分钟 | 前端 |
| 库存实时显示组件 | 3 分钟 | 前端 |

Delta Spec 标记了变更影响：ADDED 抢购相关接口和数据模型，MODIFIED 商品查询接口（增加抢购价格字段）。

### 4.3 第三步：代码生成

后端开发拿到 `tasks.md` 后，启动 Superpowers 工作流。

以 **实现 Redis 库存预扣接口** 这个任务为例，Superpowers 的执行过程：

1. Brainstorming 阶段：AI 提问 - 抢购活动的库存是共享商品主库存还是独立库存？超卖策略是拒绝还是排队？开发回答：独立库存，超卖拒绝。
2. Git worktree 自动创建隔离分支 `feature/flash-sale-stock` 。
3. Writing-plans 阶段拆解为更细的操作：
```
# 拆解后的子任务清单（部分）
1. 创建 RedisStockService 类
2. 实现 deductStock() 方法（Lua 脚本保证原子性）
3. 编写 deductStock() 的测试用例
4. 实现 stockRevert() 回滚方法（订单取消时调用）
5. 编写回滚方法的测试用例
```
4. TDD 循环自动执行：先写测试用例（RED）→ 写实现代码（GREEN）→ 优化代码结构（REFACTOR）。
5. 两阶段代码审查。审查时发现一个问题：AI 生成的代码用了 `@Autowired` 注入，但旧项目用的是构造器注入。人工标记后修正。

前端同步进行，消费 `design.md` 中的接口规范，用 Superpowers 并行开发抢购页面和倒计时组件。

### 4.4 第四步：联调与同步

前后端联调时发现一个差异：后端的抢购接口返回的时间戳是秒级，前端期望的是毫秒级。

后端在 OpenSpec 中更新了接口规范的 Delta Spec：

```
## MODIFIED: flash-sale-api-spec
- \`startTime\` 和 \`endTime\` 字段单位从秒改为毫秒
- 原因：前端倒计时组件需要毫秒精度
```

前端执行 `/opsx:sync` 拉取更新后的规范，确认无需改动代码（前端本身用的就是毫秒）。变更完成后 `/opsx:archive` 归档。

整个流程走下来，从需求定义到联调完成，3 人团队用 AI 辅助完成了原本可能需要一周的工作。关键不是 AI 写了多少代码，而是 **规范先行让所有人始终在同一页面上** 。

你在项目中用过类似的 AI 辅助方案吗？有没有踩过 AI 生成代码风格和老项目冲突的坑？欢迎在评论区聊聊。

## 5\. 落地避坑指南

![避坑指南卡片 - 4 大常见问题与解决方案速查卡](https://mmbiz.qpic.cn/mmbiz_png/icibtH5FrDwPcsdoqoNNSdFWriaa2H4TvI2ZlibcmuJ4T15QvVH03hKuPvOrIcFuKI1LOib66Vc2W59Ao52XYicWL2hjOsDzThjgyYWOpHWtbYDic8/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=3)

避坑指南卡片 - 4 大常见问题与解决方案速查卡

*图 4：老旧项目引入 AI 的 4 大常见问题与解决方案速查卡*

理论和实战都有了，但真正落地的时候，踩坑是不可避免的。以下是几个高频问题。

### 5.1 代码风格冲突

AI 生成的代码遵循现代编码规范，但老旧项目可能有自己的约定。比如旧项目用 `var` 声明变量，AI 偏好用 `let` / `const` ；旧项目的异常处理是返回错误码，AI 默认抛异常。

**解决建议** ：在 `openspec/specs/` 中增加一份代码风格规范，明确命名规则、异常处理方式、注释风格等。Superpowers 的 brainstorming 技能在开始每个任务前会读取项目规范，自动对齐风格。

别嫌麻烦，这份规范写一次，后续所有 AI 生成的代码都会参考它。

### 5.2 老旧依赖不兼容

Spring Boot 1.x 的项目，AI 生成的代码可能默认用了 2.x 的 API。jQuery 1.x 和 3.x 的方法差异也很大。

**解决建议** ：在 OpenSpec 的系统规范中明确标注依赖版本。更稳妥的做法是，在 Superpowers 的 brainstorming 阶段主动告知 AI 当前使用的框架版本号。

另外一个经验： **让 AI 先读旧代码再写新代码** 。Superpowers 的子代理每次处理新任务时，上下文是全新的。但它会读取项目规范和已有的代码文件，所以确保规范中有版本信息至关重要。

### 5.3 Spec 定义过度设计

OpenSpec 的三个文件（proposal → design → tasks）很容易让人写出几十页的设计文档，尤其是对老旧项目来说，恨不得把所有历史遗留问题都在这一轮 Spec 里解决。

**解决建议** ：OpenSpec 的核心哲学之一就是 **iterative not waterfall** 。每个变更只解决一个明确的问题。限时抢购就是限时抢购，不要在同一个变更里顺便重构订单模块。

官方也强调 **easy not complex** - 如果一个变更的 `tasks.md` 超过 10 个任务，考虑拆成多个变更。

### 5.4 旧系统没有测试用例

Superpowers 强制 TDD，但老旧项目可能连测试框架都没配好。

**解决建议** ：先别急着给老代码补测试。两个思路：

- 新功能用 Superpowers 的 TDD 流程正常开发，新代码自带测试
- 对涉及修改的老代码，只针对被修改的函数补充测试，用 Superpowers 的 verification-before-completion 技能确认覆盖

这对应了业界常说的 **绞杀者模式** （Strangler Fig Pattern）- 新代码用新规范，老代码逐步迁移，不要试图一次搞定。

## 6\. 工具安装与资源

两款工具的安装互不冲突，可以同时使用：

```
# 第一步：安装 OpenSpec
npm install -g @fission-ai/openspec@latest

# 第二步：在项目目录初始化
cd your-project && openspec init

# 第三步：安装 Superpowers（以 Claude Code 为例）
/plugin install superpowers@claude-plugins-official
```

Superpowers 也支持 Cursor（ `/add-plugin superpowers` ）、Codex CLI、OpenCode 等平台。OpenSpec 支持 25+ AI 编码助手，包括 Claude Code、Cursor、Windsurf 等。

两款工具都是 MIT 开源协议，免费使用。

## 总结

老旧项目接入 AI 编程，核心矛盾就两个： **AI 理解需求不准确，AI 写代码过程不可控。**

OpenSpec 解决前者 - 用结构化的规范文件让 AI 和人先对齐需求，再动手。Superpowers 解决后者 - 用强制性的工作流（TDD、子代理、代码审查）保证代码质量。

两者的分工边界很清晰： **OpenSpec 管需求层，Superpowers 管执行层。组合起来就是一套完整的 AI 增强开发工作流。**

说到底，老旧项目反而是 AI 编程尤其需要规范约束的场景。新项目写坏了可以重来，老项目写坏了影响线上业务。与其怕 AI 翻车而不用，不如用好工具给它套上缰绳。

建议收藏这篇，下次接到老项目新需求时翻出来对照着走一遍。如果你的同事也在为老旧项目引入 AI 发愁，转发给他看看。

**好啦，谢谢你观看我的文章，如果喜欢可以点赞转发给需要的朋友，我们下一期再见！敬请期待！**

**扫码关注，获取更多 AI 工具的实战经验和最佳实践。不错过每一篇干货！**

![图片](https://mmbiz.qpic.cn/mmbiz_png/icibtH5FrDwPejWfUVSiaMU94zo9E1LdJ3IEAS9TBKziakkibnLPOfbYxZd5qzXOCTESSCG80fUPACibggofvLuicxkicfblgic9H21jiakpdQxxhkAbo/640?wx_fmt=png&from=appmsg&watermark=1&tp=webp&wxfrom=5&wx_lazy=1#imgIndex=4)

**微信扫一扫赞赏作者**

AI编程最佳实战「2026」 · 目录

继续滑动看下一个

术哥无界

向上滑动看下一个