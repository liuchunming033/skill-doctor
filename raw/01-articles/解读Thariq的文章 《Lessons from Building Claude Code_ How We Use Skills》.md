# 解读Thariq的文章 《Lessons from Building Claude Code: How We Use Skills》

很多人存在一个误区，觉得 Skill 就只是单纯的 Markdown 文件。但实际上并非如此。

Skill 本质是**文件夹**，除了文本内容外，还可以放入脚本、静态资源、数据文件等各类内容，智能体能够主动发现、查看并调用这些文件。

在 Claude Code 中，Skill 还支持丰富的配置项，甚至可以注册动态钩子。Anthropic 的实践里表现出色的技能，大多都灵活运用了文件夹结构与各类配置能力。

本文我们精读Anthropic 的核心开发者Thariq发表在X上的文章 《Lessons from Building Claude Code: How We Use Skills》，看看Anthropic内部是如何使用Skill的。

## 一、9大类 Skill

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YzU4MjQ4MjRjOWUyYjJjZGQyMTI1NGFkMzNhYjc4NGRfOTA1NTRlYTg1N2M2YzAxZWRiZDNkN2ZjYmNjZGQwYjJfSUQ6NzY1MDg0NTAxMTg1MTk3MTU2M18xNzgxNjk4MDgwOjE3ODE3ODQ0ODBfVjM)

Thariq梳理了Anthropic构建Claude Code时使用的数百项技能，归纳出9个主流类别，最优秀的技能通常能清晰地归属于某一类；而较模糊的技能则可能跨越多个类别。这有助于思考自己组织内部是否缺少某些关键技能。下面逐一介绍每类技能的定位、特点和实际案例：

### 1\. 库与接口参考类

- **定位**：解释如何正确使用库、命令行工具或 SDK 的技能。这些技能既适用于内部库，也适用于 Claude Code 有时难以处理的常用库。

- **特点**：文件夹内通常会存放代码片段，同时整理出使用过程中的常见坑点，提醒Claude Code需要规避。

- **示例**：

    - 内部计费库Skill，重点标注边界场景、高危用法

    - 内部平台命令行工具Skill，附带每条子命令的使用场景

    - frontend\-design——前端设计规范及坑点

### 2\. 产品验证类

- **定位**：定义代码、功能的测试与校验规则，用来核验代码运行结果是否符合预期。

- **特点**：一般会搭配 Playwright、tmux 等外部工具使用，技能内部包含各类执行脚本；可以实现录屏、分步状态断言等能力，保障输出结果准确。投入精力打磨这类技能，性价比很高。

- **示例**：

    - 自动化测试Skill，无头浏览器走完全流程，分步校验状态

    - 收银台校验Skill，使用测试卡完成支付流程，核对订单状态。

### 3\. 数据查询与分析类

- **定位**：对接企业数据平台、监控系统，使用凭据获取数据的库、特定的仪表板ID等，以及常见工作流程或获取数据的方法说明。

- **特点**：内置数据查询依赖、账号凭证、仪表盘编号等信息，同时标注常规分析流程与查询语句。

- **示例**：

    - 漏斗数据查询Skill，“我需要参与哪些事件才能看到从注册 → 激活 → 付费的转化路径”，以及包含实际标准用户ID的表格。

    - 用户分群对比Skill，比较两个队列的留存率或转化率，标记统计上显著的差异，并链接至细分定义

    - Grafana Skill，数据源UID、集群名称、问题 → 仪表板查找表。

### 4\. 业务流程与团队自动化类

- **定位**：把高频、重复的日常工作流程封装为一键执行的能力。这类Skill是最容易被快速感知到收益的一类。

- **特点**：主体指令逻辑简单，往往会依赖其他技能或 MCP 协议；支持用日志文件留存历史执行记录，让智能体保持行为一致。

- **示例**：

    - 站会简报Skill，汇总你的工单跟踪、GitHub 活动以及之前的 Slack 内容，生成格式化的站会报告。

    - 工单创建Skill，强制执行数据结构（有效枚举值、必填字段），并执行创建后的流程。

    - 每周工作汇总Skill，格式化后的回顾文章。

### 5\. 代码脚手架与模板类

- **定位**：自动生成项目基础代码、文件模板，省去重复编写样板代码的工作。使得团队的项目结构和风格保持一致。

- **特点**：可搭配各类可组合脚本，尤其适合需要自然语言进行要求、而且这些要求无法完全靠代码实现的场景。

- **示例**：

    - 新服务/工作流模板Skill， 生成新的服务/工作流/处理器。

    - 数据库迁移文件模板Skill，迁移文件模板及常见问题。

    - 内部应用初始化Skill，预先集成权限、日志、部署配置。

### 6\. 代码质量与审查类

- **定位**：落地团队代码规范，完成自动化代码评审。是值得反复打磨的一类Skill。

- **特点**：搭配确定性执行脚本与工具，稳定性强；可结合钩子、GitHub 自动化流程自动运行。

- **示例**：

    - Adversarial Review Skill，启动子代理反复评审、修复问题，直至仅存细节优化。

    - 代码风格Skill，强制执行代码风格，特别是 Claude 默认情况下表现不佳的那些风格。

    - 测试Skill，如何编写测试以及测试什么的指导说明。

### 7\. 持续集成/部署类

- **定位**：完成代码拉取、推送、上线部署等工程化操作。

- **特点**：可引用其他技能获取所需信息，覆盖完整上线链路。

- **示例**：

    - babysit\-pr Skill，监控合并请求、重试异常CI、解决冲突、开启自动合并。

    - 服务部署Skill，编译、冒烟测试、灰度放量、异常自动回滚。

    - Cherry\-pick Skill，生产代码择优合并技能。

### 8\. 运维故障处理手册类

- **定位**：根据告警、报错、现象，一步步完成故障排查，并输出结构化报告。将工程师的排障思路沉淀成组织可以复用的资产。

- **特点**：梳理“问题现象\-排查工具\-查询方式”的对应关系，适配线上突发问题处理。

- **示例**：

    - 服务调试Skill，将症状映射到工具，进而关联至高流量服务的查询模式。

    - Oncall Skill，拉取告警信息、排查常见问题、整理结果。

    - 日志关联检索Skill，根据请求ID，从所有可能涉及该请求的系统中提取匹配的日志

### 9\. 基础设施运维类

- **定位**：完成服务器、容器、存储等基础设施的日常维护操作。

- **特点**：部分操作存在风险，技能内会增加防护规则，引导工程师遵循最佳实践。

- **示例**：

    - 冗余资源清理Skill，扫描闲置资源、通知团队、等待确认后批量清理。

    - 依赖包管理审批Skill，组织内的依赖审批工作流程。

    - 成本调查Skill，“为什么我们的存储/出站费用突然激增”，并附上具体的存储桶和查询模式

## 三、什么样的技能值得开发？

结合 Claude Code 内部落地经验，优先开发能解决实际痛点、复用价值高的技能：

1. 弥补大模型短板的技能：针对 Claude 不熟悉的内部组件、小众工具、专属规范开发技能；

2. 保障产出质量的技能：产品验证、代码审查、故障排查这类技能，能大幅降低出错概率，值得重点投入；

3. 替代重复劳动的技能：代码模板、流程自动化、数据查询类技能，减少人工重复操作，提升整体效率；

4. 规范团队标准的技能：统一代码风格、工单格式、部署流程的技能，拉平团队协作标准。

## 四、写出优质技能的核心秘诀

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NWY0ODQ3MzIxOTE2MDk0YzE5YmU5NWZkMGI3YmNlZDhfZTk1MGNlOGNhNmY5YmI4YjhjMTUzYjNlN2IwZTRiZmJfSUQ6NzY1MDg1OTAwODc0MzQ1OTgwM18xNzgxNjk4MDgwOjE3ODE3ODQ0ODBfVjM)

这是官方在海量实践中总结出的实用技巧，也是打造好用技能的关键：

1. **不写常识内容（Don’t State the Obvious）**

Claude 本身具备丰富的编码知识，技能里不要堆砌基础常识，重点补充它不了解的内部规则、特殊用法、定制化要求。

2. **专门增设「踩坑清单」板块（Build a Gotchas Section）**

这是技能里价值最高的内容。持续收集智能体使用过程中频繁出错的场景，不断更新到清单中，提前规避问题。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTU5NmY1MjJlMWMzYTg3NDQ0NzU0NzY3ZmM0MTM4ZGFfZWJhOTE3ZmM1MDU0M2JjMTBhOWQxZTllZjA0ODNhYzdfSUQ6NzY1MDg1OTM1NzY2MzYyODUwMl8xNzgxNjk4MDgwOjE3ODE3ODQ0ODBfVjM)

3. **善用文件夹与渐进式披露（Use the File System \& Progressive Disclosure）**

充分利用文件夹结构拆分内容，把详细文档、示例、模板分到不同子文件中，让智能体按需读取，合理控制上下文大小。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NzRlY2JkNjIxMmUxMjliMDIzMWE1NTRlNDBiNzk5MjZfODU1Mjg4ZDgwNzM0ZWVmMGVmMDAxZTkxOGQ3NDNmMGRfSUQ6NzY1MDg1OTUwNTk4MjQyNjA4MV8xNzgxNjk4MDgwOjE3ODE3ODQ0ODBfVjM)

4. **指令留足灵活空间（Avoid Railroading Claude）**

不要把指令写得过于死板、限制过多。给到必要规则的同时，保留适配不同场景的弹性，避免功能僵化。也就是给预期结果，不限定实现路径。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OTE4M2I3NDc3ZDlmZGQ1NzJlNmIwMDQ1MmJhMzA1NDdfMWJkNzM0MjAwOGNhMzlhY2JhMTE2YTE4ZjM1YTY2MWVfSUQ6NzY1MDg1OTkzMDg5OTI1NDIyMF8xNzgxNjk4MDgwOjE3ODE3ODQ0ODBfVjM)

5. **完善初始化配置（Think through the Setup）**

某些技能可能需要根据用户的上下文进行设置。例如，如果你创建一个将每日站会内容发布到 Slack 的技能，你可能希望 Claude 询问应该发布到哪个 Slack 频道。

一个很好的做法是，将此设置信息存储在技能目录中的 config\.json 文件里。如果配置未设置，代理可以向用户询问相关信息。

如果你想让代理提出结构化的选择题，可以指示Claude使用AskUserQuestion工具。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=Y2M4NDhiZjJhZDdiZjRmZTBlNmIxODhkZDY3MDZmNmJfNjVkMDY4ZTdhMTQ2OTIyYThmYjljODFmOGE3OGM1NjFfSUQ6NzY1MDg2MDIxMjI2NTY4Mzk0Nl8xNzgxNjk4MDgwOjE3ODE3ODQ0ODBfVjM)

6. **重视技能描述字段**

当 Claude Code 开始一次会话时，它会列出所有可用技能及其描述。这个列表是 Claude 用来判断“是否有适用于此请求的技能”的依据。这意味着描述字段并非摘要，而是说明在何种情况下应触发该技能。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MGVkOTQ3ZDlmMWQ3ZWNlMTQ0MzA3MDNkMjM5ZTdiZTZfMGNiYmJkZWQzMzNmY2MyMmViZDI4ZjZlYzA2NTA2YWJfSUQ6NzY1MDg2MTAzMzYyMzUyMjUxOV8xNzgxNjk4MDgwOjE3ODE3ODQ0ODBfVjM)

7. **合理使用数据记录能力**

可以用日志、JSON、数据库等文件留存执行历史，让智能体参考过往记录，保证行为连贯；官方也提供了专属稳定目录存放数据，避免升级技能时数据丢失。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=OGM2YTAxMzNiMWZhZWJhNDE5NWNmZjYxODU5ZjlmY2VfNjcwOTZiMDYwMWMzOWFlNzcwYWU2ODI2ZTAxYmI1NzRfSUQ6NzY1MDg2MTE4MjUyOTc4NTA1MF8xNzgxNjk4MDgwOjE3ODE3ODQ0ODBfVjM)

8. **多内置可执行脚本**

把通用工具函数、执行脚本放进技能，让智能体专注于流程组合，不用反复编写基础代码。

例如，在你的数据科学技能中，你可能有一组用于从事件源获取数据的函数库。为了让Claude进行复杂分析，你可以向它提供一组辅助函数，如下所示：

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=M2E2MzU0YWE0NGVjNDNjNjY1MzFiNmY4YzY0MjBlMThfYTgzY2ZmNWNlZTFkMjNmOGQ5NTc0YzBhYWM2NmU5OWVfSUQ6NzY1MDg2MTM3NDg5NzIyOTAxNV8xNzgxNjk4MDgwOjE3ODE3ODQ0ODBfVjM)

随后，Claude 可以即使需要生成脚本，也可以组合这些功能。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=YTk4NmQ2ZmQ2NTAwNzEzM2ZmMTQwNzNkMWUzNzliZWFfNDE4ZjUyZjlmNTQxZDgxOTY2M2U2NjczZjc2YTFiNmJfSUQ6NzY1MDg2MTY5NTQ2NzgwMTU4MF8xNzgxNjk4MDgwOjE3ODE3ODQ0ODBfVjM)

9. **按需配置动态钩子**

技能中可以包含在调用时被激活的钩子。针对高危操作、临时约束场景配置钩子，在调用对应技能时生效。

例如，通过 Bash 上的 PreToolUse 匹配器阻止 `rm -rf`、`DROP TABLE`、强制推送和 `kubectl delete` 操作。

```Markdown
# .claude/skills/careful/SKILL.md
---
name: careful
description: Arms strict guardrails for this session. Invoke when touching
  production systems, running migrations, or operating in restricted
  directories. Blocks rm -rf, DROP TABLE, force-push, and kubectl delete.
hooks:
  PreToolUse:
    - matcher: Bash
      hooks:
        - type: command
          command: .claude/hooks/block-destructive.sh
---

You are operating in careful mode. Every destructive command will be blocked.
Confirm with the user before proceeding with any irreversible operation.
```

10. **组合技能**

你可能需要一些相互依赖的技能。例如，你可以有一个文件上传技能用于上传文件，以及一个生成CSV文件并上传的技能。

你可以在一个Skill中直接通过名称引用其他技能，如果这些技能已安装，模型会自动调用它们。

## 五、运营和管理团队Skill

### 1\. 分享Skill

1. 技能完成基础功能、经过内部实测可用后，就可以小范围分享给团队试用；

2. 技能获得较多同事认可、使用频次变高，确认具备通用价值后，正式纳入团队公共技能库；

3. 提前做内容筛选，避免上线重复、劣质的技能。

### 2\. 两种主流分享方式

1. **代码仓库内嵌**：适合小型团队、仓库数量少的场景，直接把技能提交到项目仓库的指定目录（位于 \./\.claude/skills 目录下），同仓库成员可直接使用；缺点是技能会小幅增加模型上下文负载。

2. **插件市场分发**：适合团队规模扩大后使用，统一搭建内部插件市场，由使用者按需安装技能，灵活可控。

### 3\. **效果衡量**

为了了解某个技能的使用情况，我们使用了一个PreToolUse钩子，用于记录公司内部的技能使用情况。这样我们就能发现哪些技能受欢迎，或与我们的预期相比触发频率过低。

```Bash
# ~/.claude/settings.json
  {
    "hooks": {
      "PreToolUse": [{
        "matcher": "Skill",
        "hooks": [{ "type": "command", "command": "~/.claude/hooks/log-skill.sh" }]
      }]
    }
  }
```

```Bash
# ~/.claude/hooks/log-skill.sh
  
  #!/bin/bash
  # stdin is the hook payload: { tool_name, tool_input: { skill, args }, session_id, ... }
  # matcher already filtered to Skill, so no tool_name check needed
  payload=$(cat)
  skill=$(jq -r '.tool_input.skill' <<< "$payload")
  args=$(jq -r '.tool_input.args // ""' <<< "$payload")

  echo "$(date -u +%s)  $USER   $skill  $args" >> ~/.claude/skill-usage.
```



