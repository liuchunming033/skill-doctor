---
name: skill-doctor
description: 当用户说"检查Skill"、"体检Skill"、"诊断Skill"、或给出Skill路径要求检查时触发。对Skill进行全面体检，生成诊断报告和优化建议。
---

# Skill Doctor —— Skill 体检诊断工具

## 流程

1. 读取指定 Skill 目录
2. 检查核心文件是否存在（SKILL.md、gotchas.md 等）
3. **调用脚本获取结构化报告**：`python scripts/analyze_skill.py <skill_path> --output json`，得到每个检查项的得分、问题和建议
4. **针对每个低分项（<70分），在脚本报告基础上补充具体优化建议 + 预期提升分数 + 工作量评估**
5. **列出所有可优化项，让用户选择接受哪些**
6. **对用户接受的项目逐一优化（直接修改文件）**
7. **优化完成后再次调用脚本重新体检，输出前后对比报告**

> Agent 负责智能层（优化建议、用户交互、执行修改），脚本负责稳定层（评分计算、结构化输出）。脚本用法见 [analyze_skill.py](analyze_skill.py)。

## 九大体检项目

| 检查项 | 检查内容 | 通过标准 |
|-------|---------|---------|
| **description检查** | 是否写成触发条件，不是功能说明 | 包含触发关键词，长度<100字符 |
| **gotchas检查** | 是否有坑点记录 | gotchas.md存在且非空 |
| **文件组织检查** | 是否按三分类标准组织 | 根目录仅 SKILL.md + gotchas.md + examples.md，参考材料在 reference/，脚本在 scripts/，配置在 config/ |
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
  "overall_score": 55,
  "grade": "D",
  "check_results": {
    "description": {"score": 50, "issues": ["写成功能说明"], "suggestions": ["改为触发条件句式"], "expected_gain": 40},
    "gotchas": {"score": 40, "issues": ["gotchas.md是空壳"], "suggestions": ["补充3个以上真实坑点"], "expected_gain": 50}
  },
  "optimization_options": [
    {"id": 1, "item": "description", "current_score": 50, "expected_score": 90, "gain": 40,
     "effort": "低", "action": "重写description为触发条件句式",
     "token_saved_per_call": 50, "time_saved_per_call_sec": 0},
    {"id": 2, "item": "gotchas", "current_score": 40, "expected_score": 90, "gain": 50,
     "effort": "中", "action": "补充真实坑点",
     "token_saved_per_call": 0, "time_saved_per_call_sec": 180}
  ],
  "overall_after_accept_all": 85,
  "total_benefits": {
    "token_saved_per_call": 200,
    "time_saved_per_call_sec": 300
  }
}
```

## 收益估算规则

| 优化类型 | Token节省（每次调用） | 时间节省（每次调用） | 说明 |
|---------|---------------------|---------------------|------|
| description缩短 | 每条多余字符×1 token | — | 减少context加载量 |
| gotchas补充 | — | 每坑点2-5分钟 | 避免重复踩坑调试 |
| 文件拆分 | (原行数-新行数)×3 tokens | — | 参考材料移入reference/，按需加载不进context |
| 过度约束→决策框架 | 每条死板步骤×20 tokens | 每步10-30秒 | 减少无效步骤执行 |
| 删除已知知识 | 教程段落长度 tokens | — | 不重复Agent已知内容 |
| 脚本封装 | — | 每次1-3分钟 | 避免Agent每次重写代码 |

> 收益为单次调用估算值，实际数值因Skill内容和使用方式而异。
>
> **关于"耗时"的说明**：报告中的"耗时"指**设计缺陷产生的额外浪费**，而非技能执行总时长。具体包括：
> - gotchas 缺失 → Agent 反复踩坑调试（每次 2-5 分钟）
> - 过度约束 → Agent 执行无意义的死板步骤（每步 10-30 秒）
> - 脚本缺失 → Agent 每次重新编写相同代码（每次 1-3 分钟）
>
> **对比逻辑**：优化前的数值 = 这些浪费的总和；优化后浪费归零 → ~0；"节省" = 被消除的浪费量。优化后技能执行本身仍需要时间，但不再有这些额外损耗。

## 优化建议呈现

生成报告后，将可优化项以清单形式展示给用户，每项包含：

```markdown
### 🔧 可优化项

| # | 检查项 | 当前分 | 预期分 | 提升 | 工作量 | Token/次 | 时间/次 | 操作 |
|---|-------|--------|--------|------|--------|---------|---------|------|
| 1 | description | 50 | 90 | +40 | 低 | ~50 | — | 重写为触发条件 |
| 2 | gotchas | 40 | 90 | +50 | 中 | — | ~3min | 补充真实坑点 |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**接受全部优化后**：55分(D) → 85分(B)，提升30分

### 📈 综合收益（单次调用）
- Token 节省：~200/次
- 时间节省：~5分钟/次
- 踩坑规避：gotchas 补充后可避免常见错误

> **耗时统计口径**：此处"时间节省"指**设计缺陷导致的额外浪费**，非技能执行总时长：
> - gotchas 缺失 → Agent 反复踩坑调试（每次 2-5 分钟）
> - 过度约束 → Agent 执行无意义的死板步骤（每步 10-30 秒）
> - 脚本缺失 → Agent 每次重新编写相同代码（每次 1-3 分钟）
> - 优化前数值 = 浪费总和，优化后浪费归零，"节省" = 被消除的浪费量

请选择：
- **"全部接受"** — 一键优化所有项
- **"接受1,3"** — 只优化指定项
- **"跳过"** — 只看报告不做优化
```

## 用户确认后执行

1. 用户选择后，逐项修改对应文件
2. 每完成一项，标记状态
3. 全部完成后，重新运行体检生成对比报告

## 前后对比报告格式

```markdown
## 📊 优化前后对比

| 检查项 | 优化前 | 优化后 | 变化 |
|-------|--------|--------|------|
| description | 50 (功能说明) | 90 (触发条件) | +40 ⬆️ |
| gotchas | 40 (空壳) | 90 (充实) | +50 ⬆️ |
| ... | ... | ... | ... |
| **总分** | **55 (D)** | **85 (B)** | **+30 ⬆️** |

### 📈 综合收益（单次调用）
| 维度 | 优化前 | 优化后 | 节省 |
|------|--------|--------|---------|
| Token | ~800/次 | ~600/次 | ~200/次 |
| 耗时浪费 | ~5min | ~0 | ~5min |
| 主文件 | 466行 | 75行 | -84% |

> 耗时浪费 = 设计缺陷导致的额外开销（踩坑调试、冗余步骤等），非技能执行总时长。见 [收益估算规则](#收益估算规则)。

### 已修改文件
- `SKILL.md` — 重写 description
- `gotchas.md` — 补充 5 个真实坑点
```

## 完整交互示例

见 [examples.md](examples.md) 示例9

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

## 脚本

体检核心逻辑封装在 `scripts/analyze_skill.py`，Agent 通过调用它获取结构化评分：

```bash
python scripts/analyze_skill.py <skill_path> --output json    # 步骤3：获取评分报告
python scripts/analyze_skill.py <skill_path> --output markdown # 可选：生成人类可读报告
```

脚本负责：评分计算、问题检测、等级判定（稳定层）
Agent 负责：优化建议生成、用户交互、文件修改执行（智能层）