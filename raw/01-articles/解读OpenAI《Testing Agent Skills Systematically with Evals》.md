# 解读OpenAI《Testing Agent Skills Systematically with Evals》

## 一、为什么要做评估（Evals）？

迭代优化智能体Skill时，单凭主观感受很难判断改动是真优化，还是只是改变了行为。经常会出现各类问题：技能不触发、漏掉必要步骤、产生多余文件等功能退化。

评估是为了摆脱“凭感觉判断好坏”的方式，用客观标准验证Skill表现，清晰区分优化项和功能退化，让Skill迭代有据可依。与其问“这样感觉好些吗？”（或依赖直觉），评估让你能够提出具体的问题，例如：

- 代理是否调用了该Skill？

- 它执行了预期的命令吗？

- 它生成的输出是否符合你关心的规范？

## 二、评估（Evals）是什么？

评估用来校验大模型的输出内容、执行步骤是否符合预期。

简单定义：**指令 → 完整运行轨迹\+产出文件 → 多项校验规则 → 可长期对比的分数**。

它本质是端到端测试：运行智能体、记录全过程、按照规则打分。

## 三、基础评估流程

1. 提前定义好“技能成功标准”；

2. 编写对应技能；

3. 手动运行技能，排查各类潜在问题；

4. 搭建少量针对性测试用例；

5. 采集技能运行轨迹，通过评分器完成校验打分；

6. 随着技能迭代，逐步扩展评估维度。

## 四、先定义成功标准

动手写Skill之前，先把“成功”拆解为可量化的检查项，分为四类目标：

1. **结果目标**：任务是否正常完成、程序能否正常运行；

2. **过程目标**：智能体是否正常调用技能、是否按指定工具和步骤执行；

3. **风格目标**：输出内容是否符合团队规范与格式要求；

4. **效率目标**：执行过程是否冗余，有无多余命令、是否过度消耗 Token。

注意：不用把所有细节偏好都写进规则里，只重点保留**必须达标**的核心行为即可。

## 五、三类常见失控的场景

创建一个以可预测且可重复的方式搭建小型 React 演示应用的Skill，用于解释常见的失控场景。

```Markdown
---
name: setup-demo-app
description: Scaffold a Vite + React + Tailwind demo app with a small, consistent project structure.
---

## When to use this

Use when you need a fresh demo app for quick UI experiments or reproductions.

## What to build

Create a Vite React TypeScript app and configure Tailwind. Keep it minimal.

Project structure after setup:

- src/
  - main.tsx (entry)
  - App.tsx (root UI)
  - components/
    - Header.tsx
    - Card.tsx
  - index.css (Tailwind import)
- index.html
- package.json

Style requirements:

- TypeScript components
- Functional components only
- Tailwind classes for styling (no CSS modules)
- No extra UI libraries

## Steps

1. Scaffold with Vite using the React TS template:
   npm create vite@latest demo-app -- --template react-ts

2. Install dependencies:
   cd demo-app
   npm install

3. Install and configure Tailwind using the Vite plugin.
   - npm install tailwindcss @tailwindcss/vite
   - Add the tailwind plugin to vite.config.ts
   - In src/index.css, replace contents with:
     @import "tailwindcss";

4. Implement the minimal UI:
   - Header: app title and short subtitle
   - Card: reusable card container
   - App: render Header + 2 Cards with placeholder text

## Definition of done

- npm run dev starts successfully
- package.json exists
- src/components/Header.tsx and src/components/Card.tsx exist
```

手动运行这个Skill，以揭露Skill容易出问题的地方：

1. **触发假设**

有的指令本该唤起技能却没触发；也有不相关的指令，意外唤醒了技能。例如，像“设置一个快速的 React 演示”这样的提示本应调用  `setup-demo-app` ，但实际没有，或者更通用的提示（如“添加 Tailwind 样式”）意外地触发了它。

2. **环境假设**

Skill默认运行在空目录、默认使用 npm 包管理器，切换环境后就会执行失败。

3. **执行假设**

智能体想当然认为依赖已安装，跳过`npm install`；或是颠倒步骤，在 Vite 项目存在之前配置了 Tailwind。

发现这些问题后，及时修正Skill，再纳入后续评估范围。

当你准备让这些手动评估变得可重复时，请执行如下命令进行自动测试：

```Shell
codex exec --full-auto \
  'Use the $setup-demo-app skill to create the project in this directory.'
```

该命令会将进度流式传输到`stderr`，并仅将最终结果写入`stdout`。

默认情况下，`codex exec` 在受限的沙箱环境中运行。如果你的任务需要写入文件，请使用`--full-auto`运行。在自动化操作时，应使用完成任务所需的最小权限。

这次初步的实操主要是为了发现边界情况，而非验证正确性。你在此处所做的每项手动修正，例如添加缺失的 `npm install`、修复 Tailwind 配置或完善触发器描述，都可能成为未来评估的候选内容，以便在大规模评估前锁定预期行为。

## 六、用少量针对性样本提前发现回归问题

不需要庞大的测试集，单套Skill准备 **10\~20 条指令** 就足够快速发现功能退化。随着开发或使用过程中遇到实际失败情况，逐步扩展它。

从一个小型的CSV文件开始，每一行应代表一种你关心Skill是否激活的情况，以及当Skill执行完成后的具体表现。

```Bash
id,should_trigger,prompt
test-01,true,"Create a demo app named `devday-demo` using the $setup-demo-app skill"
test-02,true,"Set up a minimal React demo app with Tailwind for quick UI experiments"
test-03,true,"Create a small demo app to showcase the Responses API"
test-04,false,"Add Tailwind styling to my existing React app"
```

一共分为四类样本：

1. **显式调用**：指令里直接写明技能名称，验证技能被主动指定时能否正常运行，例如`test-01`；

2. **隐式调用**：不提及技能名，只描述业务场景，验证技能名称、简介能否让智能体自主识别并唤起，例如`test-02`；

3. **上下文调用**：指令附带额外业务信息，模拟真实复杂对话，检验技能在干扰信息下依旧正常工作，例如；`test-03`

4. **负控样本**：明确不该使用当前Skill的场景，可能会无意间匹配Skill描述，用于检验Skill被误触发、滥用的情况。`test-04`

当你发现遗漏、未能触发技能的提示，或输出偏离预期的情况时，请将它们作为新行添加进去。随着时间推移，这个小型CSV文件就会成为一份不断更新的记录，涵盖技能必须持续正确处理的各种场景。

## 七、记录 Skill 完整执行轨迹

评估的基础是留存运行数据，执行命令时开启轨迹记录`codex exec --json`，完整捕获智能体调用的工具、执行的命令、生成的文件、每一步行为日志。

所有轨迹以结构化格式保存，以便你的评估工具能够对实际发生的情况进行评分，而不仅仅是判断最终输出是否看起来正确。

## 八、两类评分器设计

### 1\. 轻量级确定性评分器

依托记录的运行轨迹做硬性规则校验，结果非真即假，完全客观、可复现。

常见检查项：是否执行指定命令、是否生成目标文件、命令执行顺序是否正确。

优点：排查问题简单直接，一旦校验失败，可直接查看轨迹定位原因。

一个极简的 Node\.js 运行器是这样的：

1. 对于每个提示，运行`codex exec --json --full-auto "<prompt>"`

2. 将 JSONL 跟踪保存到磁盘

3. 解析跟踪日志并对事件执行确定性检查

```JavaScript
// evals/run-setup-demo-app-evals.mjs
import { spawnSync } from "node:child_process";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import path from "node:path";

function runCodex(prompt, outJsonlPath) {
  const res = spawnSync(
    "codex",
    [
      "exec",
      "--json", // REQUIRED: emit structured events
      "--full-auto", // Allow file system changes
      prompt,
    ],
    { encoding: "utf8" }
  );

  mkdirSync(path.dirname(outJsonlPath), { recursive: true });

  // stdout is JSONL when --json is enabled
  writeFileSync(outJsonlPath, res.stdout, "utf8");

  return { exitCode: res.status ?? 1, stderr: res.stderr };
}

function parseJsonl(jsonlText) {
  return jsonlText
    .split("\n")
    .filter(Boolean)
    .map((line) => JSON.parse(line));
}

// deterministic check: did the agent run `npm install`?
function checkRanNpmInstall(events) {
  return events.some(
    (e) =>
      (e.type === "item.started" || e.type === "item.completed") &&
      e.item?.type === "command_execution" &&
      typeof e.item?.command === "string" &&
      e.item.command.includes("npm install")
  );
}

// deterministic check: did `package.json` get created?
function checkPackageJsonExists(projectDir) {
  return existsSync(path.join(projectDir, "package.json"));
}

// Example single-case run
const projectDir = process.cwd();
const tracePath = path.join(projectDir, "evals", "artifacts", "test-01.jsonl");

const prompt =
  "Create a demo app named demo-app using the $setup-demo-app skill";

runCodex(prompt, tracePath);

const events = parseJsonl(readFileSync(tracePath, "utf8"));

console.log({
  ranNpmInstall: checkRanNpmInstall(events),
  hasPackageJson: checkPackageJsonExists(path.join(projectDir, "demo-app")),
});
```

这里的价值在于一切都是确定的且可调试的。

如果检查失败，你可以打开 JSONL 文件，查看具体发生了什么。每个命令的执行都会按顺序显示为一个`item.*`事件，这使得回归问题易于解释和修复。

### 2\. 定性检查 \+ 评分标准打分

硬性规则只能校验“有没有做”，无法判断“做得好不好、是否符合规范”。对于像 `setup-demo-app` 这样的技能，许多要求是定性的：组件结构、样式规范，或 Tailwind 是否遵循了预期的配置。这些仅靠基本的文件存在性检查或命令数量统计很难准确捕捉。

针对代码风格、目录结构、配置规范等偏主观的要求，采用这套方案：

1. 运行Skill生成产物；

2. 让智能体按照预设评分细则检查成果；

3. 限定输出为固定 JSON 格式，包含总分、分项结果、问题备注，方便统一统计和对比。

举个例子，该命令仅用于检查仓库并输出符合评分标准的 JSON 响应：

```Shell
codex exec \
  "Evaluate the demo-app repository against these requirements:
   - Vite + React + TypeScript project exists
   - Tailwind is configured via @tailwindcss/vite and CSS imports tailwindcss
   - src/components contains Header.tsx and Card.tsx
   - Components are functional and styled with Tailwind utility classes (no CSS modules)
   Return a rubric result as JSON with check ids: vite, tailwind, structure, style." \
  --output-schema ./evals/style-rubric.schema.json \
  -o ./evals/artifacts/test-01.style.json
```

其中`evals/style-rubric.schema.json`是评估输出的的Schema文件，规定了输出的格式。

```JSON
{
  "type": "object",
  "properties": {
    "overall_pass": { "type": "boolean" },
    "score": { "type": "integer", "minimum": 0, "maximum": 100 },
    "checks": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": { "type": "string" },
          "pass": { "type": "boolean" },
          "notes": { "type": "string" }
        },
        "required": ["id", "pass", "notes"],
        "additionalProperties": false
      }
    }
  },
  "required": ["overall_pass", "score", "checks"],
  "additionalProperties": false
}
```

## 九、评估体系的6个扩展方向

基础评估跑通后，可按需增加更多校验维度，循序渐进提升评估完整性：

1. **命令执行次数**

统计 JSONL 日志中的`command_execution`项，以检测Agent开始循环或重复执行命令的次数。令牌使用情况也可在`turn.completed`事件中查看。以检测代理开始循环或重复执行命令的回归问题。

2. **Token 消耗统计**

监控输入Token`usage.input_tokens`、输出 Token `usage.output_tokens`用量，以发现意外的提示膨胀，并比较不同版本之间的效率。

3. **编译构建校验**

在Skill执行完成后，执行打包、编译命令，检查项目能否正常构建；

4. **运行冒烟测试**

启动服务`npm run dev`、简单接口请求`curl`，验证程序可正常运行；

5. **代码仓库整洁度**

检查是否产生多余文件，确保运行过程不会生成任何不必要的文件。

6. **权限校验**

确认技能运行没有越权，始终遵循最小权限原则。

## 十、五条核心评估原则

前面展示了从“感觉更好”到“有证据”的转变：运行代理，记录发生的情况，并通过一组简单的检查进行评分。一旦建立了这样的循环，每次调整都更容易验证，任何倒退也都会变得清晰明了。以下是总结的进行评估关键要点：

1. 只评估核心关键项，聚焦真正影响使用的行为，衡量真正重要的指标。良好的评估能让回归结果清晰明了，让失败原因易于解释。

2. 先定义可校验的“完成标准”，再开发Skill，可以借助`$skill-creator`进行初始化，然后逐步收紧指令，直到成功结果变得明确无误。

3. 评估以**实际运行行为**为依据，依托执行轨迹做客观判断；

4. 纯硬性规则覆盖不到的风格、规范类要求，借助智能体按评分细则质检；

5. 线上、使用中出现的真实问题，都补充为测试用例，持续完善评估体系。

