# LLM Wiki 知识库

本项目是一个基于 [Karpathy 的 LLM Wiki 理念](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 构建的 Obsidian 知识库。

## 核心理念

将散落在代码、文档、沟通中的领域知识编译成**结构化、高度链接**的可消费知识资产，驱动 AI 研发从"能写"到"写得对"、"管得住"。

**人负责：记录、思考、决策**
`00-Inbox/` `Daily/` `01-Projects/` `02-Areas/` `03-Resources/` `04-Archive/` `raw/`

**AI 负责：整理、关联、检索、维护**
`wiki/` `output/`

## 目录结构

```
项目名称
🏛️ 你的知识库文件夹 (LLM-Wiki-Vault)
│
├── 📥 00-Inbox/                  ← 临时捕捉区：未经整理的想法、片段、待分类材料
│
├── 📅 Daily/                     ← 日记、日计划、流水记录
│
├── 🚀 01-Projects/               ← 项目文档镜像和项目入口（外部代码仓库同步，vault 端只读）
│
├── 🌱 02-Areas/                  ← 长期维护的责任领域（工作内容、个人系统、健康、兴趣研究）
│
├── 📚 03-Resources/              ← 可复用资料、行业报告、工具说明、参考文章和知识卡片
│
├── 🗃️ 04-Archive/                ← 已完成、暂停或不再活跃的项目与资料
│
├── 🏭 raw/                        ← 编译管线原料层：待 /ingest 处理的原始材料（只读，处理后自动归档）
│   ├── 📄 01-articles/            ← 网页剪藏、技术文章
│   ├── 🎓 02-papers/              ← 论文、深度研报
│   ├── 🎙️ 03-transcripts/         ← 转录文本、会议记录
│   ├── 📋 04-rules/               ← 编码规范、安全规范、研发约束规则、合规要求、权限模型、数据脱敏、审计规则
│   ├── ✅ 05-quality/             ← 测试资产、用例、缺陷库、评审卡点、质量门禁
│   ├── 🚨 06-ops/                 ← 线上运维、故障复盘、监控告警、应急预案
│   ├── 📖 07-lessons/             ← 技术决策、方案选型、踩坑复盘、最佳实践
│   ├── 📐 08-spec/                ← 产品需求文档(PRD)、UI/UX 设计文档
│   └── 🗃️ 09-archive/             ← 已归档区：/ingest 执行后源文件自动移动至此
│
├── 🧠 wiki/                      ← 知识编译输出层（LLM 拥有完全写权限，人类阅读层）
│   ├── 📑 index.md               ← 全局内容字典：记录所有 wiki 页面及其一句话索引
│   ├── 📜 log.md                 ← 行为流水线：以 Grep-friendly 格式记录 ingest/query 历史
│   ├── 🏗️ concepts/              ← 抽象层：方法论、架构模式、第一性原理
│   ├── 👥 entities/              ← 实体层：人名、公司、工具软件、项目
│   ├── 🔍 sources/               ← 摘要层：针对 raw 文件的一对一核心观点提炼
│   └── 💎 syntheses/             ← 综合层：针对复杂提问生成的深度研究报告（属知识图谱，被 index 索引、被 query 召回）
│
├── 📦 output/                    ← 交付物层（基于 wiki 生成的产物，不属知识图谱，可丢重建）
│
├── 🤖 CLAUDE.md                  ← 全局心智规范：定义语言协议、读写权限与 Wiki Schema
│
└── ⚙️ .claude/                   ← Claude Code 官方配置目录
    └── 🛠️ skills/                ← Agent Skill 中心
        ├── 🏗️ init-vault/        ← 自定义：初始化 Vault 标准目录结构与基石文件
        ├── ⚙️ ingest/            ← 自定义：编译收件箱 raw 文件到 wiki，并执行归档
        ├── 🔎 query/             ← 自定义：检索 wiki/index 并读取相关页面，生成带双链引用的回答
        ├── 🩺 lint/              ← 自定义：知识体检，修复死链、补充 index、发现认知冲突
        ├── 🔌 obsidian-cli/      ← Obsidian 官方：调用 Obsidian 原生 API 进行检索、打开页面
        └── 🪄 defuddle/          ← Obsidian 官方：将网页 URL 自动清理并转化为 Markdown 存入 raw/
```

## 使用方式

在 Obsidian 中打开本 vault 后，建议先完成以下插件配置，再执行 `/init-vault`、`/ingest`、`/query`、`/lint`。

### 1) Terminal 插件（在库内直接运行命令）

**作用**：

- 在 Obsidian 内直接打开终端，减少在编辑器和系统终端之间来回切换
- 可直接在 vault 根目录执行脚本、检查目录、运行辅助命令

**配置方式**：

1. 打开 `Settings -> Community plugins -> Browse`
2. 搜索并安装 `Terminal`（或同类终端插件）
3. 在插件设置中将默认工作目录设为当前 Vault 根目录
4. 建议开启 "Open in current file folder" 或 "Open in vault root"（按你的使用习惯二选一）

**推荐用法**：

- 固定一个终端窗口在 vault 根目录，专门用于运行 ingest/query/lint 相关命令
- 对批量处理任务，优先在此终端执行，保证路径一致

### 2) Git 插件（版本追踪与回滚）

**作用**：

- 自动追踪 `wiki/` 和规则文件（如 `CLAUDE.md`）的变更
- 在规则调整、知识批量重写后可快速回滚
- 支持自动提交和定时同步（可选）

**配置方式**：

1. 打开 `Settings -> Community plugins -> Browse`
2. 搜索并安装 `Obsidian Git`
3. 在插件设置中配置：
   - Commit message 模板（建议带日期时间）
   - Auto pull before push（开启）
   - Auto backup interval（按需，如 10-30 分钟）
4. 若你使用远程仓库，先在系统中完成 Git 凭据配置

**建议忽略项**：

- `output/`（可重建产物）
- 其他临时缓存目录

### 3) Claudian 插件（Agent 主工作入口）

**作用**：

- 在 Obsidian 中直接调用 Agent 执行 `/init-vault`、`/ingest`、`/query`、`/lint`
- 基于 `CLAUDE.md` 与 `.claude/skills/` 统一约束行为

**配置方式**：

1. 安装并启用 `Claudian` 插件
2. 在插件设置中确认：
   - 工作目录指向当前 Vault
   - 可读取 `CLAUDE.md` 与 `.claude/skills/`
   - 默认语言设为简体中文（如有该选项）
3. 首次进入仓库建议先执行 `/init-vault` 做结构补齐

**推荐工作流**：

1. `/init-vault`：初始化或补齐目录与基石文件
2. `/ingest`：将 `raw/` 中 Markdown 编译到 `wiki/`
3. `/query <问题>`：在知识图谱中检索并回答
4. `/lint`：做全局健康检查并修复链接/索引问题

### 常用命令

- `/init-vault` — 初始化或补齐 Vault 结构（目录、`CLAUDE.md`、`wiki/index.md`、`wiki/log.md`）
- `/query <问题>` — 在知识库中搜索相关内容
- `/ingest` — 将新的原始资料编译到知识库
- `/lint` — 检查知识库健康度（死链、孤儿页面）

## 与代码库形成 Memorepo（One Workspace）

目标是把"知识库 + 代码库 + 设计与测试资产"放进同一工作区，让产品、开发、设计、测试在同一上下文协作。

### 推荐结构

```text
one-workspace/
├── product-dev-wiki/           # 本仓库（知识层）
│   ├── raw/
│   ├── wiki/
│   ├── CLAUDE.md
│   └── .claude/skills/
├── app-web/                    # 前端代码库
├── app-api/                    # 后端代码库
├── qa-automation/              # 测试自动化仓库（可选）
└── design-assets/              # 设计源文件与规范（可选）
```

### 两种落地方式

1. 多仓库单工作区（推荐起步）
   - 保持各项目独立 Git 仓库
   - 在同一父目录并列放置多个仓库
   - 用 VS Code/Obsidian 打开同一工作区进行协作

2. 真正 Monorepo（统一仓库）
   - 把知识与代码合并到同一 Git 仓库
   - 适合组织内已统一发布节奏、统一权限管理
   - 需要更严格的目录权限和 CI 分层策略

### 角色协作映射（One Workspace）

- 产品：PRD/需求访谈先进入 `raw/08-spec/`，再由 `/ingest` 编译进 `wiki/`
- 设计：设计规范、评审纪要进入 `raw/08-spec/` 或 `03-Resources/`
- 开发：在代码仓库实现功能，同时把关键决策沉淀到 `raw/07-lessons/`
- 测试：测试策略、用例、缺陷复盘进入 `raw/05-quality/`，并在 `wiki/` 形成可检索知识

### 统一工作流（跨职能）

1. 新资料进入 `raw/`（必须是 Markdown）
2. 执行 `/ingest`，沉淀为 `wiki/sources`、`wiki/concepts`、`wiki/entities`
3. 开发与测试基于 `/query` 获取上下文，减少重复沟通
4. 执行 `/lint` 保持知识图谱健康

### 权限与边界建议

- `raw/`：正文只读，仅允许更新 frontmatter 的 ingest 状态字段
- `wiki/`：知识编译输出层，可持续维护
- `output/`：可重建产物，建议不作为长期事实源
- 代码仓库：继续按现有工程规范管理，不与知识库规则冲突

### 最小实施步骤（1 小时可落地）

1. 在同一父目录下并列放置知识库与代码库
2. 在知识库执行 `/init-vault` 校准结构
3. 配置 Obsidian 的 Terminal + Git + Claudian 插件
4. 约定团队输入口径：产品/设计/测试材料统一先入 `raw/`
5. 每日固定一次 `/ingest` + `/lint`，形成稳定知识更新节奏
