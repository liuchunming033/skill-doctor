---
title: "Comet"
type: entity
tags: [工具, Claude Code, 插件, 状态机, AI编程, Spec Coding]
sources:
  - raw/01-articles/开源！Comet: 基于OpenSpec和Superpowers怎么做出更好用的自动Spec Skills.md
  - raw/01-articles/Comet Spec Skill的开发者故事.md
  - raw/01-articles/rpamiscomet Comet OpenSpec + Superpowers dual-star development workflow.md
last_updated: 2026-06-06
---

## 定义

Comet（`@rpamis/comet`）是 Bilibili UP主"将现在的你"开发的开源 AI Coding Skill，基于 OpenSpec 和 Superpowers 二次开发。核心定位：**不替代两者，只做组合调度**——把 OpenSpec 管需求（what）的能力和 Superpowers 管实现（how）的能力接入同一条流程，并用轻量状态机解决断点恢复问题。

开源数天即获 400+ Star，NPM 下载超 4500 次，B站播放超 12 万。

## 关键信息

**安装**：

```
npm install -g @rpamis/comet
cd your-project
comet init
```

支持 28+ AI Coding 平台（Claude Code、Cursor、Codex、OpenCold、WindSurf 等），交互式初始化自动分发 skill 文件。

**五阶段流程（BDVRA）：**

| 阶段 | 名称          | 负责工具                      | 核心产物                  |
| ---- | ------------- | ----------------------------- | ------------------------- |
| 1    | comet open    | OpenSpec                      | proposal + design + tasks |
| 2    | comet design  | Superpowers brainstorming     | 边界方案风险文档          |
| 3    | comet build   | Superpowers TDD + subagent    | 经过验证的代码            |
| 4    | comet verify  | OpenSpec + Superpowers 双收口 | 测试报告 + 需求对齐       |
| 5    | comet archive | OpenSpec archive + 双向关联   | 归档完整 spec 文档        |

**入口命令**：`/commit` 单一入口，自动检测当前 spec 状态，路由到对应阶段，支持跨会话/跨设备断点恢复。

**三种工作流：**

- `comet`（完整流程）：新功能开发
- `comet hotfix`：跳过 brainstorm/design，直接 open→build→verify→archive
- `comet tweak`：文案/配置/文档/prompt 微调，比完整流程更轻

**状态机机制（核心创新）：**

Comet 的状态通过 CLI 脚本而非 agent 感觉来维护：

- `comet-guard` 脚本：阶段闸门，检查文件存在 + phase 匹配 + tasks 完成，条件不满足则 hard stop
- `comet-state` 脚本：统一读写 `.comet.yml` 状态文件
- `comet-validate` 脚本：校验必填字段、枚举值、路径引用
- `comet-archive` 脚本：验证入口状态→同步 specs→移动 change→写入 archived=true

**两套 Spec 的分工（单向事实链）：**

- OpenSpec 的 Delta Spec = 需求侧唯一事实（验收场景、边界行为契约）
- Superpowers 的 design doc = 技术选型、数据流、实现方案（不得重复定义需求）
- `comet-handoff` 脚本：从 OpenSpec 产物生成结构化交接包（含文件路径、行范围、SHA256 哈希），避免 agent 临场手写 summary

**解决的核心问题：**

- 两套 skill 命令分散、无法自动触发 → 统一 `/commit` 入口
- 断点恢复消耗大量 token → 状态机 + `.comet.yml` 快照
- 任务完成但文档没打勾 → guard 脚本强制校验，非程序性校验不放行
- spec 文档双套管理混乱 → 单向事实链划清职责边界

## 关联连接

- [[OpenSpec]] — 需求层基础工具（Comet 的上游）
- [[Superpowers]] — 执行层基础工具（Comet 的上游）
- [[AtomicTDDWorkflow]] — Comet 的 build 阶段采用的 TDD 模型
- [[摘要-comet-skill-intro]] — Comet 功能介绍视频来源
- [[摘要-comet-developer-story]] — Comet 开发者故事来源
- [[摘要-comet-readme-zh]] — 官方 README，守护脚本详解和跨平台安装指南
- [[AgentHumanPipeline]] — 宏观人机协作框架
- [[摘要-comet-readme-zh]] — 官方 README，守护脚本详解和跨平台安装指南
