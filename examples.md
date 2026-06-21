# Skill优化示例

## 示例1：description优化

### 错误示例

```yaml
---
name: pdf-processor
description: 这是一个帮助用户处理PDF文件的Skill，可以填写表单、提取文本、转换格式等功能，适合处理各种PDF相关任务。
---
```

**诊断问题**：
- ❌ 写成功能说明（"这是一个"、"可以做什么"）
- ❌ 缺少触发关键词
- ❌ 长度过长（>100字符）
- ❌ 不包含用户会说的关键词

---

### 正确示例

```yaml
---
name: pdf-form-filler
description: 当用户说填写PDF表单、处理PDF表格、或补充PDF字段时触发。用于填写填充式表单（非扫描版）。
---
```

**优化要点**：
- ✅ 写成触发条件（"当用户说"）
- ✅ 包含用户关键词（"填写PDF表单"）
- ✅ 长度合理（<100字符）
- ✅ 说明适用场景（"填充式表单"）

**得分提升**：50分 → 95分

---

## 示例2：gotchas优化

### 错误示例

```markdown
# Gotchas

暂无坑点，待补充。

TODO: 记录团队踩过的坑。
```

**诊断问题**：
- ❌ 只有占位符（"暂无"、"TODO"）
- ❌ 缺少真实坑点
- ❌ 文件太小（<500字节）
- ❌ 无"现象-问题-解决"结构

---

### 正确示例

```markdown
# Gotchas

## 坑点1：处理扫描版PDF

**现象**：用户提供扫描版PDF，Skill尝试提取文字但失败。

**问题**：填充式表单Skill无法处理扫描版PDF，需要OCR能力。

**解决**：在description中明确说明"仅处理填充式表单"，建议用户使用OCR工具处理扫描版。

---

## 坑点2：表单字段名不匹配

**现象**：Skill填写了错误的字段（把"姓名"填到了"公司名"）。

**问题**：PDF表单字段名不清晰，Agent判断错误。

**解决**：在Skill中提供字段映射表（常见字段→对应PDF字段名）。

---

## 坑点3：跨平台兼容性问题

**现象**：Mac上生成的PDF在Windows上打开显示异常。

**问题**：不同平台PDF渲染差异。

**解决**：使用标准PDF库（如pdfkit），测试跨平台兼容性。
```

**优化要点**：
- ✅ 3个真实坑点
- ✅ "现象-问题-解决"结构完整
- ✅ 文件内容充实（>1500字节）
- ✅ 有实际价值

**得分提升**：40分 → 90分

---

## 示例3：文件组织优化

### 错误示例

```
pdf-processor/
└── SKILL.md  (500行，包含所有内容)
```

**诊断问题**：
- ❌ 单文件堆砌（>300行）
- ❌ 违反渐进式披露
- ❌ context过载
- ❌ 缺少附属文件

---

### 正确示例

```
pdf-form-filler/
├── SKILL.md          (120行，核心逻辑)
├── gotchas.md        (坑点记录)
├── examples.md       (示例)
├── reference/
│   └── field-mapping.md  (字段映射表)
├── config/
│   └── config.json       (团队偏好配置)
└── scripts/
    └── fill_form.py  (稳定脚本)
```

**SKILL.md**：
```markdown
# PDF表单填写

## 流程

分析PDF表单字段，根据用户提供的信息填写对应字段。

## 字段映射

见 [field-mapping.md](field-mapping.md)

## 常见坑点

见 [gotchas.md](gotchas.md)

## 示例

见 [examples.md](examples.md)
```

**优化要点**：
- ✅ 主文件精简（120行）
- ✅ 详细内容拆分
- ✅ 使用链接引用
- ✅ 渐进式披露

**得分提升**：50分 → 90分

---

## 示例4：过度约束优化

### 错误示例

```markdown
## 流程

1. 使用pdftk命令打开PDF
2. 使用grep查找所有表单字段
3. 按字段顺序逐一填写
4. 检查每个字段是否填写正确
5. 保存PDF文件
```

**诊断问题**：
- ❌ 死板流程（"第一步第二步"）
- ❌ 无决策点
- ❌ 约束路径不约束目标
- ❌ 给Agent无自由度

---

### 正确示例

```markdown
## 流程

分析PDF表单结构，根据用户提供的信息智能填写。

**关键决策点**：
- 判断表单类型（填充式vs扫描版）
- 根据字段名匹配用户信息
- 验证填写结果是否符合预期

**目标**：准确填写表单字段，不是强制执行特定命令。

见 [field-mapping.md](field-mapping.md) 了解常见字段映射规则。
```

**优化要点**：
- ✅ 约束目标不约束路径
- ✅ 有决策点
- ✅ 给Agent自由度
- ✅ 描述决策框架

**得分提升**：50分 → 90分

---

## 示例5：已知知识优化

### 错误示例

```markdown
# Git Commit Skill

## 什么是Git

Git是一个版本控制系统...

## Git Commit的作用

Git commit用于保存代码变更...

## 如何写Commit Message

1. 先写标题
2. 再写正文
3. 最后写footer
...
```

**诊断问题**：
- ❌ 教程式内容（"什么是"、"如何使用"）
- ❌ 重复Agent已知知识
- ❌ 缺少团队特有知识
- ❌ 无价值增量

---

### 正确示例

```markdown
# Git Commit Message生成器

## 团队规范

- 使用Conventional Commits格式
- 标题不超过50字符
- 必须包含scope（模块名）
- Breaking Change必须标注

## 格式规范

<type>(<scope>): <subject>

<body>

<footer>

## 常见错误

见 [gotchas.md](gotchas.md)

## 示例

见 [examples.md](examples.md)
```

**优化要点**：
- ✅ 只补充团队规范
- ✅ 不教Agent已知知识
- ✅ 有价值增量
- ✅ 聚焦Agent不知道的

**得分提升**：40分 → 95分

---

## 示例6：脚本优化

### 错误示例

```markdown
# PDF处理

每次运行时让Agent编写Python代码提取PDF文本...
```

**诊断问题**：
- ❌ 每次重新写代码
- ❌ 无稳定能力封装
- ❌ 缺少scripts目录
- ❌ 执行不稳定

---

### 正确示例

```
pdf-processor/
├── SKILL.md
├── gotchas.md
└── scripts/
    └── extract_text.py  (稳定脚本)
```

**SKILL.md**：
```markdown
# PDF文本提取

## 流程

调用 `scripts/extract_text.py` 提取PDF文本。

## 脚本说明

见 [scripts/extract_text.py](scripts/extract_text.py)

## Gotchas

见 [gotchas.md](gotchas.md)
```

**extract_text.py**：
```python
#!/usr/bin/env python3
"""
PDF文本提取脚本
用法：python extract_text.py <pdf_file>
"""
import sys
import pdfplumber

def extract_text(pdf_path):
    """提取PDF文本"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        return f"错误: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python extract_text.py <pdf_file>")
        sys.exit(1)

    result = extract_text(sys.argv[1])
    print(result)
```

**优化要点**：
- ✅ 封装稳定能力
- ✅ 有scripts目录
- ✅ 脚本有注释和错误处理
- ✅ Skill调用脚本

**得分提升**：50分 → 90分

---

## 示例7：Hooks优化

### 错误示例

```yaml
---
name: pdf-processor
hooks:
  pre-use: log_usage.py  # 错误的hook类型
---
```

**诊断问题**：
- ❌ Hook类型错误（应该是PreToolUse）
- ❌ 缺少matcher
- ❌ 格式不正确
- ❌ 路径不完整

---

### 正确示例

**全局配置（settings.json）**：
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Skill",
      "hooks": [
        {"type": "command", "command": "~/.claude/hooks/log-skill.sh"}
      ]
    }]
  }
}
```

**Hook脚本（log-skill.sh）**：
```bash
#!/bin/bash
# stdin is the hook payload
payload=$(cat)
skill=$(jq -r '.tool_input.skill' <<< "$payload")
echo "$(date -u +%s)  $USER   $skill" >> ~/.claude/skill-usage.tsv
```

**优化要点**：
- ✅ PreToolUse类型正确
- ✅ matcher正确
- ✅ 格式完整
- ✅ 脚本可执行

**得分提升**：50分 → 95分

---

## 示例8：综合优化对比

### Before（不合格）

```
bad-skill/
└── SKILL.md  (600行)
```

**SKILL.md**：
```yaml
---
name: pdf-tool
description: 这是一个功能强大的PDF处理工具，可以提取文本、填写表单、转换格式等。
---

# PDF处理工具

## 什么是PDF

PDF是Portable Document Format...

## 功能介绍

这个Skill可以：
1. 提取文本
2. 填写表单
3. 转换格式

## 使用方法

第一步：用户提供PDF文件
第二步：Skill分析PDF结构
第三步：执行对应操作
第四步：返回结果

## 代码示例

每次运行时编写Python代码...
```

**诊断报告**：
- description：50分（功能说明）
- gotchas：40分（缺失）
- 文件组织：50分（单文件）
- 过度约束：50分（死板流程）
- 已知知识：40分（教程式）
- 脚本：50分（缺失）
- Hooks：N/A
- Markdown：60分（YAML缺少字段）

**总分：45分（等级D - 不合格）**

---

### After（优秀）

```
pdf-form-filler/
├── SKILL.md          (120行)
├── gotchas.md        (坑点记录)
├── examples.md       (示例)
├── reference/
│   └── field-mapping.md  (字段映射)
├── config/
│   └── config.json       (团队配置)
└── scripts/
    └── fill_form.py  (稳定脚本)
```

**SKILL.md**：
```yaml
---
name: pdf-form-filler
description: 当用户说填写PDF表单、处理PDF表格、或补充PDF字段时触发。用于填写填充式表单。
---

# PDF表单填写

## 流程

分析PDF表单字段，根据用户提供的信息智能填写。

## 字段映射

见 [field-mapping.md](field-mapping.md)

## 常见坑点

见 [gotchas.md](gotchas.md)

## 配置

见 [config.json](config.json)
```

**诊断报告**：
- description：95分（触发条件明确）
- gotchas：90分（内容充实）
- 文件组织：90分（合理拆分）
- 过度约束：90分（决策框架）
- 已知知识：95分（只补充特有）
- 脚本：90分（完整脚本）
- Hooks：N/A
- Markdown：95分（格式规范）

**总分：92分（等级A - 优秀）**

---

## 关键优化路径

1. **description重构**：从功能说明改为触发条件
2. **gotchas补充**：从空壳改为真实坑点
3. **文件拆分**：从单文件改为合理拆分
4. **流程重构**：从死板路径改为决策框架
5. **知识精简**：从教程式改为团队特有知识
6. **脚本封装**：从重复代码改为稳定脚本
7. **格式规范**：从混乱改为标准Markdown

**提升幅度**：45分 → 92分（+47分）

---

## 示例9：完整交互式优化流程

### 第一步：生成诊断报告

用户输入："检查这个 Skill：`my-skill/`"

Skill Doctor 分析后输出：

```json
{
  "skill_name": "my-skill",
  "overall_score": 55,
  "grade": "D",
  "check_results": {
    "description": {"score": 50, "issues": ["写成功能说明"], "suggestions": ["改为触发条件句式"], "expected_gain": 40},
    "gotchas": {"score": 40, "issues": ["gotchas.md是空壳"], "suggestions": ["补充3个以上真实坑点"], "expected_gain": 50},
    "file_organization": {"score": 50, "issues": ["单文件500行"], "suggestions": ["拆分为主文件+附属文件"], "expected_gain": 40},
    "over_constraint": {"score": 70, "issues": ["有轻微路径约束"], "suggestions": ["增加决策点描述"], "expected_gain": 20},
    "known_knowledge": {"score": 40, "issues": ["大量教程式内容"], "suggestions": ["删除基础概念，只保留团队特有知识"], "expected_gain": 50}
  }
}
```

### 第二步：呈现可优化项

```markdown
### 🔧 可优化项

| # | 检查项 | 当前分 | 预期分 | 提升 | 工作量 | Token/次 | 时间/次 | 操作 |
|---|-------|--------|--------|------|--------|---------|---------|------|
| 1 | description | 50 | 90 | +40 | 低 | ~150 | — | 283→96字符，触发条件句式 |
| 2 | gotchas | 40 | 90 | +50 | 中 | — | ~5min | 新建7个真实坑点 |
| 3 | 文件组织 | 50 | 90 | +40 | 高 | ~1200 | — | 466行→75行+4附属文件 |
| 4 | 过度约束 | 70 | 90 | +20 | 低 | ~200 | ~1min | 9步→决策框架+判断表 |
| 5 | 已知知识 | 40 | 90 | +50 | 中 | ~300 | — | 删除Agent已知教程内容 |

**接受全部优化后**：55分(D) → 85分(B)，提升30分

### 📈 综合收益（单次调用）
- Token节省：~1,850/次（从 ~2,500 → ~650）
- 时间节省：~6分钟/次（减少无效步骤+避免踩坑）

> 耗时 = 设计缺陷导致的额外浪费（踩坑调试、冗余步骤等），非技能执行总时长。

请选择："全部接受" / "接受1,2,5" / "跳过"
```

### 第三步：用户选择

用户回复："接受1,2,5"

### 第四步：逐项执行

```
✅ [1/3] description 优化完成：50 → 90 (+40)
   修改文件：SKILL.md — YAML description 重写为触发条件

✅ [2/3] gotchas 优化完成：40 → 90 (+50)
   修改文件：gotchas.md — 补充5个真实坑点

✅ [3/3] 已知知识优化完成：40 → 90 (+50)
   修改文件：SKILL.md — 删除教程式段落
```

### 第五步：重新体检 + 前后对比

```markdown
## 📊 优化前后对比

| 检查项 | 优化前 | 优化后 | 变化 |
|-------|--------|--------|------|
| description | 50 (功能说明) | 90 (触发条件) | +40 ⬆️ |
| gotchas | 40 (空壳) | 90 (充实) | +50 ⬆️ |
| 文件组织 | 50 (单文件) | 50 (未修改) | 0 — |
| 过度约束 | 70 (轻微约束) | 70 (未修改) | 0 — |
| 已知知识 | 40 (教程式) | 90 (特有知识) | +50 ⬆️ |
| **总分** | **55 (D)** | **78 (B)** | **+23 ⬆️** |

### 📈 综合收益（单次调用）
| 维度 | 优化前 | 优化后 | 节省 |
|------|--------|--------|---------|
| Token | ~2,500/次 | ~1,100/次 | ~1,400/次 |
| 耗时 | ~5min/次 | ~0 | ~5min/次 |
| 主文件 | 500行 | 500行（未改） | — |

> 耗时 = 设计缺陷导致的额外浪费（踩坑调试、冗余步骤等），非技能执行总时长。

### 已修改文件
- `SKILL.md` — 重写 description + 删除教程内容
- `gotchas.md` — 补充 5 个真实坑点

💡 **未优化项**（可选后续处理）：
- 文件组织：拆分500行单文件为多文件结构
- 过度约束：将步骤式流程改为决策框架
```

### 用户拒绝优化的场景

用户回复："跳过"

```
⏸️ 已跳过所有优化。报告已生成，你可以随时回复优化项编号来执行。
```