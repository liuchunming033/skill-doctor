# Anthropic的skill\-creator实践  

今天很多人第一次接触 Anthropic Skills 时，会把 Skill\-creator 理解成“创建 Skill 的向导”。但如果你认真研究官方仓库，会发现这是一个典型的 **Meta Skill（元技能）**——它管理的不是某一个业务能力，而是整个 Skill 的生命周期。官方给它的定义也非常明确：创建、修改、测试、评估、优化 Skill。

事实上，2026 年 3 月 Anthropic 更新后的 Skill\-creator，已经从一个“Skill 生成器”演进成了一套完整的 **Skill Engineering（技能工程）体系**。

在Claude Code中输入`/skill-creator`，你会看到如下信息：

```Markdown
❯ /skill-creator

⏺ 你好！我已经加载了 skill-creator skill。这个skill可以帮助你：

  🎯 主要功能：
  - 创建新技能 - 从零开始创建新的skill
  - 改进现有技能 - 编辑和优化已有的skill
  - 运行测试 - 用测试用例验证skill是否正常工作
  - 性能评估 - 量化对比不同版本的表现
  - 优化触发 - 改进skill描述提高触发准确性

  接下来你想做什么？

  1. 创建一个全新的skill - 告诉我你想要什么功能
  2. 改进现有的skill - 告诉我哪个skill需要改进
  3. 测试skill性能 - 运行evals看看效果如何
  4. 优化skill描述 - 让skill更容易被触发

  或者你有其他具体的需求？

  请告诉我你的目标，我会引导你完成整个流程！✨
```

它一共覆盖 5 类刚需场景：

1. **从零新建专属Skill**：把你的固定工作流程、模板、规则封装成永久可用Skill；

2. **编辑优化已有Skill**：改造旧Skill、补漏洞、适配新场景；

3. **标准化测评验证**：跑真实测试用例，检验输出是否合规、稳定；

4. **专业性能基准测试**：通过方差分析，对比版本快慢、稳定性、Token 消耗差异；

5. **触发精度专项优化**：解决 90% 用户的通病 —— Skill该用不用、乱触发、漏触发。

形成：定需求 → 写初稿 → 跑双组对照测试 → 量化打分 \+ 人工评审 → 迭代优化 → 触发精准度优化闭环。

今天我们就针对https://github\.com/anthropics/skills/blob/main/skills/skill\-creator/SKILL\.md进行详细解读。







