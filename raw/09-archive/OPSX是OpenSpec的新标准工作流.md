**全文摘要**
OPSX是OpenSpec的新标准工作流，取代原有的线性阶段式流程，采用灵活的迭代动作模型。用户可随时执行创建、实现、更新、归档等操作，通过YAML模式定义工件依赖关系，支持自定义模板和即时测试，无需等待版本发布。核心改进包括：外部化配置、增量式工件创建、文件系统状态感知，以及跨编辑器兼容的技能文件系统。

**关键段落**

- **核心问题与解决方案**: 旧工作流存在指令硬编码、全有或无一刀切、固定结构、黑盒调试等缺陷；OPSX通过schema.yaml和模板文件实现可编辑配置、独立验证、自定义工作流和即时迭代。

- **用户体验重构**: 摒弃"规划→实施→完成"的线性阶段，改为动作驱动模式；依赖关系作为启用条件而非强制门槛，允许在实施过程中回溯更新设计文档。

- **项目配置机制**: 通过openspec/config.yaml设置默认模式、注入项目上下文（技术栈、API规范等）及按工件类型的规则；上下文和规则以XML标签形式注入指令模板。

- **命令体系**: 核心命令包括propose（快速创建）、explore（调研思考）、apply（实施任务）、sync（同步规范）、archive（归档）；扩展命令提供new、continue、ff、verify等细粒度控制。

- **更新与新建决策框架**: 以意图一致性、范围重叠度、原工件可完成性为判断标准；保留上下文时选择更新，需要清晰边界时选择新建，类比Git分支管理策略。

- **架构对比**: 旧系统使用TypeScript硬编码模板经工具适配器生成命令文件；OPSX采用YAML模式定义、DAG拓扑排序引擎、文件系统状态检测，生成跨编辑器兼容的技能文件。

- **依赖图模型**: 工件构成有向无环图（proposal→specs/design→tasks→apply）；状态转换遵循BLOCKED→READY→DONE，基于依赖满足度和文件存在性检测。

- **信息流差异**: 旧工作流接收静态指令一次性创建全部工件；OPSX通过CLI查询当前状态，获取包含依赖上下文和解锁信息的丰富指令，逐件创建并反馈进展。

- **自定义模式**: 支持通过openspec schema init/fork创建自定义工作流，存储于项目本地或用户全局目录；示例展示research-first模式在默认流程前增加调研阶段。
- 
根据文档，自定义工作流通过 **schema 模式系统** 实现。以下是针对你的 `tdd-driven-v2` 示例的完整配置方法：

---

## 1. 初始化自定义模式

```bash
# 方式A：从零创建（会生成模板结构）
openspec schema init tdd-driven-v2

# 方式B：Fork现有模式修改
openspec schema fork default tdd-driven-v2
```

---

## 2. 配置 schema.yaml

你的 `schema.yaml` 需要定义 **DAG 依赖图** 和 **工件类型**：

```yaml
# schemas/tdd-driven-v2/schema.yaml
name: tdd-driven-v2
version: "1.0.0"
description: "TDD驱动开发工作流：先写测试，再实现功能"

# 定义工件类型（DAG节点）
artifacts:
  - id: proposal
    file: proposal.md
    template: templates/proposal.md
    description: "功能提案与测试策略"

  - id: spec
    file: spec.md
    template: templates/spec.md
    depends_on: [proposal]      # 依赖proposal完成
    description: "需求规格与验收标准"

  - id: design
    file: design.md
    template: templates/design.md
    depends_on: [spec]
    description: "架构设计与测试方案"

  - id: tasks
    file: tasks.md
    template: templates/tasks.md
    depends_on: [design]
    description: "任务清单（含测试任务）"

  - id: plan
    file: plan.md
    template: templates/plan.md
    depends_on: [tasks]
    description: "迭代执行计划（TDD循环）"

# 可选：定义状态转换规则
states:
  - blocked    # 依赖未满足
  - ready      # 可创建/编辑
  - done       # 已完成
```

---

## 3. 编写模板文件（带变量注入）

模板使用 **XML标签** 接收项目上下文和规则注入：

```markdown
<!-- templates/proposal.md -->
# 功能提案: {{project.name}}

## 背景
{{context.business_goal}}

## 测试策略
> 规则注入：{{rules.tdd.requirements}}

## 验收标准
- [ ] 所有功能有对应单元测试
- [ ] 测试覆盖率 ≥ {{rules.coverage.threshold|default:"80%"}}
```

**可用变量**（由 `openspec/config.yaml` 注入）：
- `{{project.name}}` / `{{project.tech_stack}}`
- `{{context.*}}` — 业务上下文
- `{{rules.*}}` — 该工件类型的专属规则

---

## 4. 项目级配置激活

在 **项目根目录** 的 `openspec/config.yaml` 中指定默认模式：

```yaml
# openspec/config.yaml
schema: tdd-driven-v2    # 使用你的自定义模式

# 注入项目上下文（所有模板可用）
context:
  business_goal: "重构支付模块以支持多币种"
  tech_stack: "Python/FastAPI, pytest"

# 按工件类型的规则（注入对应模板）
rules:
  tdd:
    requirements: "先写失败测试，再写最小实现，最后重构"
  coverage:
    threshold: "90%"
```

---

## 5. 使用工作流

```bash
# 查看当前状态（DAG实时计算）
openspec status

# 创建proposal（解锁下游依赖）
openspec propose

# 当proposal.done后，spec自动变为ready
openspec apply spec        # 或 openspec apply --next

# 回溯更新上游工件（非线性流程）
openspec update proposal   # 依赖spec/design会重新验证
```

---

## 关键设计原则

| 特性         | 实现方式                                                          |
| ------------ | ----------------------------------------------------------------- |
| **DAG依赖**  | `depends_on` 定义解锁顺序，非强制阻塞                             |
| **增量创建** | 每个工件独立验证，可随时 `update`                                 |
| **状态感知** | 文件存在性 + 依赖满足度 = `ready`/`blocked`                       |
| **跨编辑器** | 生成 `.cursor/rules` 或 `.github/copilot-instructions` 等技能文件 |

---

## 存储位置选择

```bash
# 项目本地（仅当前项目可用）
./openspec/schemas/tdd-driven-v2/

# 用户全局（所有项目可用）
~/.openspec/schemas/tdd-driven-v2/
```

运行 `openspec schema list` 查看所有可用模式。