
## 📋 目录

  

1. [需求访谈阶段](#1-需求访谈阶段)

2. [创建Skill](#2-创建skill)

3. [设计测试用例](#3-设计测试用例)

4. [运行测试](#4-运行测试)

5. [结果分析](#5-结果分析)

6. [迭代优化](#6-迭代优化)

  

---

  

## 1. 需求访谈阶段

  

### 1.1 明确核心问题

  

****关键问题清单****：

  

```

□ 目标用户和使用场景

  - 个人使用还是团队使用？

  - 主要用途（汇报/同步/复盘）？

  

□ 输入输出格式

  - 用户提供什么信息？（任务列表、自由文本、其他）

  - 输出什么格式？（飞书文档、Markdown、邮件）

  - 输入形式（自由文本/结构化/从工具导入）

  

□ 特色功能需求

  - 智能总结

  - 数据可视化

  - 自动信息收集

  - 多种模板风格

  - 多语言支持

  

□ 实际使用示例

  - 请求用户提供一个具体的使用案例

  - 包括输入和期望输出的示例

```

  

### 1.2 记录需求答案

  

****Weekly-Report Skill 需求示例****：

  

```

目标用户：个人和管理者

使用场景：团队同步

输入内容：

  - 本周完成任务列表

  - 下周计划

  - 遇到的问题

  - 心得体会等

输入形式：自由文本 + 飞书任务/日历导入

输出格式：飞书文档

特色功能：

  ✓ 智能总结

  ✓ 数据可视化

  ✓ 自动收集信息（飞书任务、日历）

  

使用示例：

输入："这周完成了用户登录功能的开发，修复了3个bug，

      开会讨论了新需求。下周计划做支付模块，

      可能需要协调前端团队。问题是测试环境不太稳定。"

  

输出：包含本周工作、下周计划、心得体会的完整周报

```

  

---

  

## 2. 创建Skill

  

### 2.1 目录结构

  

```bash

~/.claude/skills/<skill-name>/

├── SKILL.md          # 主文档（必需）

├── evals/            # 测试用例目录

│   └── evals.json    # 测试定义

├── scripts/          # 可执行脚本（可选）

├── references/       # 参考文档（可选）

└── assets/           # 资源文件（可选）

```

  

### 2.2 SKILL.md 模板

  

```markdown

---

name: <skill-name>

description: <描述skill功能，包含触发关键词>

---

  

# <Skill Title>

  

## When to Use This Skill

  

<明确列出触发场景>

  

## Workflow

  

### Step 1: <步骤名称>

  

<详细说明>

  

### Step 2: <步骤名称>

  

<详细说明>

  

...

  

## Special Features

  

<特色功能说明>

  

## Integration with Other Skills

  

<依赖的其他skills>

  

## Quality Guidelines

  

<质量检查清单>

  

## Example Usage

  

<使用示例>

```

  

### 2.3 关键写作原则

  

1. ****Description要"pushy"**** - 防止under-triggering

   ```markdown

   # ❌ 太被动

   description: "Generate weekly reports when asked."

  

   # ✅ 更主动

   description: "Generate professional weekly reports. Use when the user mentions '周报', 'weekly report', '工作汇报', or wants to summarize work progress, even if they don't explicitly ask for a 'report'."

   ```

  

2. ****结构化Workflow**** - 清晰的步骤指导

   ```markdown

   ### Step 1: Clarify Requirements

   Ask the user:

   1. Report type: Personal or team?

   2. Time range: This week or custom?

   3. Additional context?

   ```

  

4. ****提供具体示例**** - 避免模糊描述

   ```markdown

   # ❌ 模糊

   - Use active voice

  

   # ✅ 具体

   - Use active voice: "Completed feature X" not "Feature X was completed"

   - Be specific: "Fixed 3 critical bugs" not "Fixed some bugs"

   ```

  

4. ****处理错误情况****

   ```markdown

   ## Error Handling

   - No data found: Inform user and ask for manual input

   - Access denied: Proceed with available information

   - Incomplete input: Use reasonable defaults

   ```

  

### 2.4 Weekly-Report SKILL.md 核心内容

  

****创建命令****：

```bash

mkdir -p ~/.claude/skills/weekly-report

```

  

****核心结构****：

```markdown

---

name: weekly-report

description: Generate professional weekly reports. Use when user mentions "周报", "weekly report", "本周总结", "工作汇报", or wants to summarize work week.

---

  

# Weekly Report Generator

  

## Workflow

  

### Step 1: Clarify Report Type

Ask: Personal or team? Time range? Focus areas?

  

### Step 2: Collect Information

- From Feishu Tasks (lark-task skill)

- From Feishu Calendar (lark-calendar skill)

- User's free-text input

  

### Step 3: Parse and Organize

Extract completed tasks, plans, issues

  

### Step 4: Generate Report Structure

Standard template with 6 sections

  

### Step 5: Create Feishu Document

Use lark-cli docs +create

  

### Step 6: Offer Customization

Allow user to refine

```

  

****关键修正****：

```bash

# ❌ 错误用法

lark-cli docs +create --markdown @file.md

  

# ✅ 正确用法

lark-cli docs +create --markdown "$(cat file.md)"

```

  

---

  

## 3. 设计测试用例

  

### 3.1 测试用例结构

  

```json

{

  "skill_name": "weekly-report",

  "evals": [

    {

      "id": 1,

      "name": "descriptive-test-name",

      "prompt": "用户的实际输入",

      "expected_output": "期望的输出描述",

      "files": [],

      "assertions": []

    }

  ]

}

```

  

### 3.2 测试用例设计原则

  

1. ****覆盖不同场景****：

   - 简单场景（最小输入）

   - 复杂场景（完整功能）

   - 边界场景（特殊需求）

  

2. ****描述性命名****：

   ```json

   # ✅ 好的命名

   "name": "simple-personal-report"

   "name": "detailed-report-with-data-collection"

   "name": "team-manager-report"

  

   # ❌ 差的命名

   "name": "test1"

   "name": "eval-0"

   ```

  

3. ****真实的用户输入****：

   ```json

   # ✅ 真实场景

   "prompt": "帮我写个周报。这周完成了用户登录功能，

              修复了3个bug..."

  

   # ❌ 过于抽象

   "prompt": "生成周报"

   ```

  

### 3.3 Weekly-Report 测试用例

  

****创建evals.json****：

```bash

mkdir -p ~/.claude/skills/weekly-report/evals

```

  

****三个测试用例****：

  

```json

{

  "skill_name": "weekly-report",

  "evals": [

    {

      "id": 1,

      "name": "simple-personal-report",

      "prompt": "帮我写个周报。这周完成了用户登录功能的开发，修复了3个bug，开会讨论了新需求。下周计划做支付模块，可能需要协调前端团队。问题是测试环境不太稳定。",

      "expected_output": "生成包含本周工作、下周计划、问题建议的个人周报",

      "files": [],

      "assertions": []

    },

    {

      "id": 2,

      "name": "detailed-personal-report-with-data",

      "prompt": "生成我的本周工作周报。需要从飞书任务和日历中提取数据，我还要补充一些内容：这周最重要的成果是优化了数据库查询性能，响应时间从3秒降到200毫秒。遇到的主要挑战是跨部门协调比较耗时。下周重点是上线新版本。",

      "expected_output": "自动收集飞书数据，结合用户信息，生成完整周报",

      "files": [],

      "assertions": []

    },

    {

      "id": 3,

      "name": "team-manager-report",

      "prompt": "帮我生成团队周报。我们团队有张三、李四、王五三个人。张三完成了前端页面开发，李四做了后端API，王五负责测试。整体进度是70%。下周要完成集成测试和上线。",

      "expected_output": "生成团队周报，包含成员贡献和团队进度",

      "files": [],

      "assertions": []

    }

  ]

}

```

  

---

  

## 4. 运行测试

  

### 4.1 创建工作目录

  

```bash

mkdir -p ~/.claude/skills/<skill-name>/workspace/iteration-1

```

  

### 4.2 为每个测试用例创建目录

  

```bash

for eval_name in "simple-personal-report" "detailed-personal-report" "team-manager-report"; do

  mkdir -p ~/.claude/skills/<skill-name>/workspace/iteration-1/$eval_name/{with_skill,without_skill}/outputs

done

```

  

### 4.3 Spawn测试任务

  

****关键原则****：

- ****同时启动所有任务**** - with-skill和baseline在同一轮启动

- ****使用Task工具的run**_**_in_background_**** **_- 并行执行_**

- ****明确输出路径**** - 保存到对应目录

  

****命令模式****：

  

```python

# With Skill

Task(

    description="Test N: <name> with skill",

    prompt="""Execute this task:

- Skill path: /path/to/skill

- Task: <用户提示>

- Input files: none

- Save outputs to: /path/to/workspace/iteration-1/<eval-name>/with_skill/outputs/

- Outputs to save: <期望的输出文件>""",

    run_in_background=True,

    subagent_type="general-purpose"

)

  

# Baseline (NO skill)

Task(

    description="Test N: <name> baseline",

    prompt="""Execute this task WITHOUT using any skill:

- Task: <用户提示>

- Input files: none

- Save outputs to: /path/to/workspace/iteration-1/<eval-name>/without_skill/outputs/

- Outputs to save: <期望的输出文件>""",

    run_in_background=True,

    subagent_type="general-purpose"

)

```

  

### 4.4 收集Timing数据

  

****重要****：每个任务完成时立即保存timing数据！

  

```bash

# 当收到task-notification时，立即保存

echo '{

  "total_tokens": <from-notification>,

  "duration_ms": <from-notification>,

  "total_duration_seconds": <duration_ms/1000>

}' > /path/to/run-directory/timing.json

```

  

****示例****：

```json

{

  "total_tokens": 0,

  "duration_ms": 68510,

  "total_duration_seconds": 68.51

}

```

  

---

  

## 5. 结果分析

  

### 5.1 生成Benchmark统计

  

****手动创建benchmark.json****：

  

```json

{

  "metadata": {

    "skill_name": "weekly-report",

    "skill_path": "/path/to/skill",

    "executor_model": "claude-sonnet-4-6",

    "timestamp": "2026-06-16T00:00:00Z",

    "iteration": 1

  },

  "runs": [

    {

      "eval_id": 1,

      "eval_name": "simple-personal-report",

      "configuration": "with_skill",

      "time_seconds": 68.51,

      "tokens": 0

    },

    {

      "eval_id": 1,

      "eval_name": "simple-personal-report",

      "configuration": "without_skill",

      "time_seconds": 100.55,

      "tokens": 0

    }

  ],

  "run_summary": {

    "simple-personal-report": {

      "with_skill": {

        "time_seconds_mean": 68.51

      },

      "without_skill": {

        "time_seconds_mean": 100.55

      },

      "delta_time_seconds": -32.04,

      "delta_time_percent": -31.9

    }

  }

}

```

  

### 5.2 性能对比表格

  

| 测试用例 | With Skill | Baseline | 提升 | 提升率 |

|---------|-----------|----------|------|--------|

| Test 1 | X秒 | Y秒 | -(Y-X)秒 | -((Y-X)/Y)% |

| Test 2 | X秒 | Y秒 | -(Y-X)秒 | -((Y-X)/Y)% |

| Test 3 | X秒 | Y秒 | -(Y-X)秒 | -((Y-X)/Y)% |

  

### 5.3 Weekly-Report 测试结果

  

```

测试用例            With Skill    Baseline     提升      提升率

----------------------------------------------------------------

简单个人周报          68.5秒       100.6秒     -32秒     -31.9%

详细周报+数据收集     135.6秒      1539秒    -1403秒     -91.2% ⭐

团队周报              57.1秒       73.6秒    -16.5秒     -22.4%

```

  

****关键发现****：

- Test 2 性能提升最显著（11.3倍速度提升）

- 所有测试skill版本都优于baseline

- 平均提速48.5%

  

---

  

## 6. 迭代优化

  

### 6.1 Review文档质量

  

****检查清单****：

  

```

□ 对比with-skill和baseline的输出文档

□ 检查内容完整性

□ 评估结构合理性

□ 验证关键信息是否包含

□ 注意语言风格和专业性

```

  

### 6.2 根据测试结果改进

  

****改进方向****：

  

1. ****性能优化****：

   - 简化workflow步骤

   - 减少不必要的工具调用

   - 缓存中间结果

  

2. ****质量提升****：

   - 补充缺失的信息

   - 优化文档结构

   - 改进语言表达

  

3. ****功能增强****：

   - 添加更多示例

   - 支持更多输入格式

   - 提供更多自定义选项

  

### 6.3 更新SKILL.md

  

****修正示例****：

  

```markdown

# ❌ 错误

```bash

lark-cli docs +create --markdown @file.md

```

  

# ✅ 正确

```bash

lark-cli docs +create --markdown "$(cat file.md)"

```

```

  

### 6.4 重新测试

  

```bash

# 创建新的iteration目录

mkdir -p ~/.claude/skills/<skill-name>/workspace/iteration-2

  

# 重复步骤4-5

# 对比iteration-1和iteration-2的结果

```

  

---

  

## 7. 最佳实践总结

  

### 7.1 Skill设计原则

  

✅ ****DO****:

- Description要主动、pushy，防止under-triggering

- Workflow步骤清晰，每步有明确输出

- 提供具体示例，避免抽象描述

- 处理错误情况和边界条件

- 与其他skill明确集成方式

  

❌ ****DON'T****:

- 不要假设用户知道所有细节

- 不要省略错误处理逻辑

- 不要使用模糊的描述（"适当的"、"合理的"）

- 不要忽略工具调用的正确语法

  

### 7.2 测试设计原则

  

✅ ****DO****:

- 测试真实的用户场景

- 包含简单、复杂、边界场景

- 使用描述性的测试名称

- 同时启动所有测试（并行执行）

- 立即保存timing数据

  

❌ ****DON'T****:

- 不要用抽象的测试输入

- 不要只测试happy path

- 不要串行执行测试

- 不要忘记保存timing数据

  

### 7.3 常见问题解决

  

****问题1****：Skill没有触发

- ****原因****：Description不够pushy

- ****解决****：添加更多触发关键词，明确使用场景

  

****问题2****：工具调用错误

- ****原因****：语法不正确

- ****解决****：查阅工具文档，使用正确语法（如`"$(cat file)"`而非`@file`）

  

****问题3****：Baseline表现更好

- ****原因****：Skill过于复杂或指导不当

- ****解决****：简化workflow，删除冗余步骤

  

****问题4****：测试结果差异大

- ****原因****：测试用例不稳定或环境差异

- ****解决****：多次运行取平均值，检查环境一致性

  

---

  

## 8. 完整示例：Weekly-Report Skill

  

### 8.1 文件结构

  

```

~/.claude/skills/weekly-report/

├── SKILL.md              (主文档)

├── evals/

│   └── evals.json        (测试定义)

└── workspace/

    └── iteration-1/

        ├── simple-personal-report/

        │   ├── with_skill/

        │   │   ├── outputs/

        │   │   └── timing.json

        │   └── without_skill/

        │       ├── outputs/

        │       └── timing.json

        ├── detailed-personal-report/

        └── team-manager-report/

```

  

### 8.2 测试执行命令

  

```bash

# 创建目录结构

mkdir -p ~/.claude/skills/weekly-report/{evals,workspace/iteration-1}

  

# 创建测试用例（见第3节）

  

# 运行测试（使用Task工具，见第4节）

  

# 收集timing数据（每个任务完成时）

  

# 生成benchmark（见第5节）

  

# Review结果并迭代

```

  

### 8.3 成功指标

  

- ✅ 所有测试成功完成

- ✅ With-skill版本性能优于baseline

- ✅ 生成的文档质量达标

- ✅ Skill能够正确触发

- ✅ 错误情况得到妥善处理

  

---

  

## 9. 快速参考

  

### 9.1 关键命令速查

  

```bash

# 创建skill目录

mkdir -p ~/.claude/skills/<name>

  

# 创建测试目录

mkdir -p ~/.claude/skills/<name>/workspace/iteration-1/<test>/{with_skill,without_skill}/outputs

  

# 查看任务输出

tail -f /private/tmp/claude-503/<task-id>.output

  

# 保存timing数据

echo '{"total_tokens": 0, "duration_ms": XXXXX, "total_duration_seconds": XX.XX}' > timing.json

  

# 创建飞书文档（正确方式）

lark-cli docs +create --title "标题" --markdown "$(cat file.md)"

```

  

### 9.2 测试断言模板

  

```json

{

  "assertions": [

    {

      "name": "包含关键章节",

      "check": "文档包含'本周工作'章节",

      "expected": true

    },

    {

      "name": "包含具体数据",

      "check": "提到'3个bug'",

      "expected": true

    },

    {

      "name": "创建了飞书文档",

      "check": "生成了有效的文档URL",

      "expected": true

    }

  ]

}

```

  

---

  

## 10. 附录

  

### 10.1 工具链接

  

- ****Skill Creator****: `~/.claude/skills/skill-creator/SKILL.md`

- ****Lark CLI文档****: 各lark-* _skill的references目录_

- ****测试报告****: `workspace/iteration-N/benchmark.json`

  

### 10.2 相关Skills

  

- `lark-doc` - 飞书文档操作

- `lark-task` - 飞书任务管理

- `lark-calendar` - 飞书日历

- `lark-whiteboard` - 数据可视化

  

### 10.3 注意事项

  

⚠️ ****重要****：

1. 测试前确保所有依赖的工具已授权

2. 保存timing数据是****唯一机会****，错过无法找回

3. Baseline不要传skill路径

4. 使用并行测试提高效率

5. 每次迭代都要与前一版本对比

  

---

  

****文档版本****: 1.0

****创建日期****: 2026-06-16

****适用范围****: Claude Code Skill创建与测试