---
name: skill-doctor
description: 当用户说"检查Skill"、"体检Skill"、"诊断Skill"、或给出Skill路径要求检查时触发。对Skill进行全面体检，生成诊断报告和优化建议。
---

# Skill Doctor —— Skill 体检诊断工具

## 流程

1. 读取指定Skill目录
2. 检查核心文件是否存在（SKILL.md、gotchas.md等）
3. 运行九大体检项目
4. 生成诊断报告（包含得分、问题清单、优化建议）

## 九大体检项目

| 检查项 | 检查内容 | 通过标准 |
|-------|---------|---------|
| **description检查** | 是否写成触发条件，不是功能说明 | 包含触发关键词，长度<100字符 |
| **gotchas检查** | 是否有坑点记录 | gotchas.md存在且非空 |
| **文件组织检查** | 是否合理拆分文件 | 主文件<200行，有附属文件 |
| **过度约束检查** | 是否过度约束路径 | 没有"第一步第二步"等死板流程 |
| **已知知识检查** | 是否重复Agent已知内容 | 没有"什么是X"、"如何使用Y"等教程 |
| **内存配置检查** | 是否有config.json | config.json存在，有合理配置 |
| **脚本检查** | 是否需要脚本但缺失 | 如需稳定能力，有scripts目录 |
| **hooks检查** | hooks配置是否正确 | PreToolUse/PostToolUse格式正确 |
| **markdown格式检查** | 格式是否规范 | YAML、表格、代码块格式正确 |

## 体检报告格式

```json
{
  "skill_name": "xxx",
  "overall_score": 85,
  "grade": "B",
  "check_results": {
    "description": {"score": 90, "issues": [], "suggestions": []},
    "gotchas": {"score": 80, "issues": ["gotchas.md过短"], "suggestions": ["补充更多坑点"]}
  },
  "priority_fixes": [
    "立即修复：description缺少触发关键词",
    "建议优化：补充gotchas.md内容"
  ]
}
```

## 评分等级

- **A（90-100分）**：优秀，遵循所有最佳实践
- **B（75-89分）**：良好，有少量优化空间
- **C（60-74分）**：合格，有明显改进点
- **D（<60分）**：不合格，需要重构

## 详细检查清单

见 [checklists.md](checklists.md)

## 常见坑点

见 [gotchas.md](gotchas.md)

## 优化示例

见 [examples.md](examples.md)

## 执行方式

**方式一：手动检查**
- 用户提供Skill路径，Skill Doctor分析并生成报告

**方式二：自动检查（推荐）**
- 用户执行脚本：`python scripts/analyze_skill.py <skill_path>`
- 自动生成JSON报告和Markdown建议

**关键检查点**：
- description是否写成触发条件，不是功能说明
- gotchas是否有价值，不是空壳
- 文件组织是否合理，不是单文件堆砌
- 是否避免过度约束，给Agent足够自由度