# Anthropic的Skill 编写最佳实践

现在AI Agent Skill越来越火，但**绝大多数人写的 Skill 又臃肿、又难用、还经常不触发**。

其实并不是你的思路不对，而是缺少一套标准化的开发规范。

今天这篇内容，来自 Anthropic 官方针对 Claude 智能体的 **Skill 最佳实践指南**，专门解决一个核心问题：**如何写出简洁、稳定、能被 Claude 精准识别、好维护的高质量 Skill**。

官方整套方法论只围绕一个超级核心原则：**极致简洁**。

因为模型上下文是公共资源，Skill 的名称、描述常驻占用 token，正文按需加载，多余一句话都会拖累整体效果。

指南系统讲透了一整套落地标准：

怎么规范命名、怎么写高触发率的 Skill 描述、如何用「渐进式披露架构」精简上下文、怎么根据任务自由度设计工作流、如何用测试迭代优化效果、以及新手最容易踩的所有反模式。

同时也给出了非常落地的工程规范：

根据场景拿捏指令自由度、拆分多层级文件结构、搭建带校验的任务反馈循环、先做基线测试再开发、脚本与运行环境的最佳写法、依赖与工具调用的标准化方式。

如果你一直在自己瞎写 Skill、总遇到触发不准、输出不稳定、结构混乱、难以迭代的问题，**这套官方标准，就是你最需要的统一开发范式**。

# **核心原则**

## **简洁至关重要**

上下文窗口是共享资源，Skill元数据（名称和描述）预加载，SKILL\.md仅在相关时读取。默认假设Claude已具备基础智能，只补充其缺失的上下文，避免冗余解释。

对每条信息进行审视：

- "Claude 真的需要这个解释吗？"

- "我能否假设 Claude 已经知道这一点？"

- "这段内容是否值得其Token成本？"

良好示例：简洁（约 50 个令牌）：

```Shell
## Extract PDF text

Use pdfplumber for text extraction:

```python
import pdfplumber

with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```
```

不良示例：过于冗长（约 150 个令牌）：

```Python
## Extract PDF text

PDF (Portable Document Format) files are a common file format that contains
text, images, and other content. To extract text from a PDF, you'll need to
use a library. There are many libraries available for PDF processing, but
pdfplumber is recommended because it's easy to use and handles most cases well.
First, you'll need to install it using pip. Then you can use the code below...
```

## **设置适当的自由度**

根据任务特性匹配自由程度。

- 高自由度（文本指令）适用于多种方法都有效的场景，给出大致方向，相信 Claude 能找到最佳路线。示例：代码审查，其中上下文决定最佳方法。

```Shell
## Code review process

1. Analyze the code structure and organization
2. Check for potential bugs or edge cases
3. Suggest improvements for readability and maintainability
4. Verify adherence to project conventions
```

- 中等自由度（伪代码）适用于存在首选模式但允许变通的场景；给出伪代码或带参数的脚本，允许一定程度的变化，但又有一定的配置进行约束。

```Python
## Generate report

Use this template and customize as needed:

```python
def generate_report(data, format="markdown", include_charts=True):
    # Process data
    # Generate output in specified format
    # Optionally include visualizations
```
```

- 低自由度（精确脚本）适用于脆弱、一致性关键的操作。提供具体的防护措施和精确的指令，给出特定脚本，例如必须按精确顺序运行的数据库迁移。

```Shell
## Database migration

Run exactly this script:

```bash
python scripts/migrate.py --verify --backup
```

Do not modify the command or add additional flags.
```

## 使用您计划使用的所有模型进行测试

同一个Skill在不同能力的模型上表现不同，Skill不是"写一次通吃所有模型"，而是要根据模型的智商水平调整说明书的详细程度——对"学霸"少说两句，对"学渣"多给几步。

按模型划分的测试考虑因素：

- Claude Haiku（快速、经济）：Skill 是否提供了足够的指导？

- Claude Sonnet（平衡）：Skill 是否清晰高效？

- Claude Opus（强大的推理能力）：Skill 是否避免了过度解释？

对 Opus 完美有效的内容可能需要为 Haiku 提供更多细节。

# **Skill结构**

**YAML Frontmatter**： SKILL\.md 的 frontmatter 需要两个字段：

`name`：

- 最多 64 个字符

- 只能包含小写字母、数字和连字符

- 不能包含 XML 标签

- 不能包含保留词："anthropic"、"claude"

`description`：

- 必须非空

- 最多 1024 个字符

- 不能包含 XML 标签

- 应描述 Skill 的功能以及何时使用它

有关完整的 Skill 结构详情，请参阅 [Skill 概述](https://platform.claude.com/docs/zh-CN/agents-and-tools/agent-skills/overview#skill-structure)。

## 命名约定

名称使用小写字母/数字/连字符（最多64字符），推荐动名词形式（如processing\-pdfs）；

良好的命名示例（动名词形式）：

- `processing-pdfs`

- `analyzing-spreadsheets`

- `managing-databases`

- `testing-code`

- `writing-documentation`

可接受的替代方案：

- 名词短语：`pdf-processing`、`spreadsheet-analysis`

- 动作导向：`process-pdfs`、`analyze-spreadsheets`

避免：

- 模糊的名称：`helper`、`utils`、`tools`

- 过于通用：`documents`、`data`、`files`

- 保留词：`anthropic-helper`、`claude-tools`

- Skill 集合内不一致的模式

一致的命名使以下事项更容易：

- 在文档和对话中引用 Skill

- 一眼就能理解 Skill 的功能

- 组织和搜索多个 Skill

- 维护专业、统一的 Skill 库

## 编写有效的描述

`description` 字段用于实现 Skill 发现，应同时包含 Skill 的功能以及何时使用它。

始终使用**第三人称编写**。描述会被注入到系统提示中，不一致的人称视角可能导致发现问题。

- 良好： "Processes Excel files and generates reports"（处理 Excel 文件并生成报告）

- 避免： "I can help you process Excel files"（我可以帮助您处理 Excel 文件）

- 避免： "You can use this to process Excel files"（您可以使用此功能处理 Excel 文件）

具体明确并包含关键术语。同时包含 Skill 的功能以及何时使用它的具体触发条件/上下文。

每个 Skill 只有一个描述字段。描述对于 Skill 选择至关重要：Claude 使用它从可能超过 100 个可用 Skill 中选择正确的 Skill。您的描述必须提供足够的细节，让 Claude 知道何时选择此 Skill，而 SKILL\.md 的其余部分则提供实现细节。

有效示例：

```Shell
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
```

```Shell
description: Analyze Excel spreadsheets, create pivot tables, generate charts. Use when analyzing Excel files, spreadsheets, tabular data, or .xlsx files.
```

```Shell
description: Generate descriptive commit messages by analyzing git diffs. Use when the user asks for help writing commit messages or reviewing staged changes.
```

避免像下面这样模糊的描述：

- description: Helps with documents

- description: Processes data

- description: Does stuff with files

## **渐进式披露模式**

SKILL\.md作为概览控制在500行以内，通过链接将详细内容拆分到单独文件，按领域组织（如reference/finance\.md、reference/sales\.md），避免深层嵌套引用，确保Claude按需加载、减少令牌消耗。

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=MTVlZWMwNDI2ZDIwOTc4MTRiYTljMDNiOThlMjQxY2JfZWUwMzQzMDYxYjVjYTlhZDJjZDlkMDE1NjFlZmY5ZmJfSUQ6NzY1MTU4NjQ4NDc1MTQwMzk3MF8xNzgxNjk4MTE1OjE3ODE3ODQ1MTVfVjM)

完整的 Skill 目录结构可能如下所示：

```Python
pdf/
├── SKILL.md              # Main instructions (loaded when triggered)
├── FORMS.md              # Form-filling guide (loaded as needed)
├── reference.md          # API reference (loaded as needed)
├── examples.md           # Usage examples (loaded as needed)
└── scripts/
    ├── analyze_form.py   # Utility script (executed, not loaded)
    ├── fill_form.py      # Form filling script
    └── validate.py       # Validation script
```

**模式 1：带引用的高级指南**

```YAML
---
name: pdf-processing
description: Extracts text and tables from PDF files, fills forms, and merges documents. Use when working with PDF files or when the user mentions PDFs, forms, or document extraction.
---

# PDF Processing

## Quick start

Extract text with pdfplumber:
```python
import pdfplumber
with pdfplumber.open("file.pdf") as pdf:
    text = pdf.pages[0].extract_text()
```

## Advanced features

**Form filling**: See [FORMS.md](FORMS.md) for complete guide
**API reference**: See [REFERENCE.md](REFERENCE.md) for all methods
**Examples**: See [EXAMPLES.md](EXAMPLES.md) for common patterns
```

Claude 仅在需要时加载 `FORMS.md`、`REFERENCE.md `或 `EXAMPLES.md`。

**模式 2：按领域组织**

对于涉及多个领域的 Skill，按领域组织内容以避免加载不相关的上下文。当用户询问销售指标时，Claude 只需读取与销售相关的架构，而不是财务或营销数据。这可以保持较低的令牌使用量并使上下文保持聚焦。

```Shell
bigquery-skill/
├── SKILL.md (overview and navigation)
└── reference/
    ├── finance.md (revenue, billing metrics)
    ├── sales.md (opportunities, pipeline)
    ├── product.md (API usage, features)
    └── marketing.md (campaigns, attribution)
```

```Markdown
# BigQuery Data Analysis

## Available datasets

**Finance**: Revenue, ARR, billing → See [reference/finance.md](reference/finance.md)
**Sales**: Opportunities, pipeline, accounts → See [reference/sales.md](reference/sales.md)
**Product**: API usage, features, adoption → See [reference/product.md](reference/product.md)
**Marketing**: Campaigns, attribution, email → See [reference/marketing.md](reference/marketing.md)

## Quick search

Find specific metrics using grep:

```bash
grep -i "revenue" reference/finance.md
grep -i "pipeline" reference/sales.md
grep -i "api usage" reference/product.md
```
```

**模式 3：条件性详情**

显示基本内容，链接到高级内容：

```Shell
# DOCX Processing

## Creating documents

Use docx-js for new documents. See [DOCX-JS.md](DOCX-JS.md).

## Editing documents

For simple edits, modify the XML directly.

**For tracked changes**: See [REDLINING.md](REDLINING.md)
**For OOXML details**: See [OOXML.md](OOXML.md)
```

## 避免深层嵌套引用

当文件从其他被引用的文件中被引用时，Claude 可能会部分读取文件。遇到嵌套引用时，Claude 可能会使用 `head -100` 等命令预览内容，而不是读取整个文件，从而导致信息不完整。

保持引用距 SKILL\.md 仅一层深度。所有参考文件都应直接从 SKILL\.md 链接，以确保 Claude 在需要时读取完整文件。

不良示例：层级过深：

```Shell
# SKILL.md
See [advanced.md](advanced.md)...

# advanced.md
See [details.md](details.md)...

# details.md
Here's the actual information...
```

良好示例：仅一层深度：

```Shell
# SKILL.md

**Basic usage**: [instructions in SKILL.md]
**Advanced features**: See [advanced.md](advanced.md)
**API reference**: See [reference.md](reference.md)
**Examples**: See [examples.md](examples.md)
```

## 为较长的参考文件添加目录结构

对于超过 100 行的参考文件，在顶部包含目录。这确保即使在部分读取预览时，Claude 也能看到可用信息的完整范围。

示例：

```Markdown
# API Reference

## Contents
- Authentication and setup
- Core methods (create, read, update, delete)
- Advanced features (batch operations, webhooks)
- Error handling patterns
- Code examples

## Authentication and setup
...

## Core methods
...
```

然后 Claude 可以根据需要读取完整文件或跳转到特定部分。

# **工作流与反馈循环**

## 对复杂任务使用工作流

将复杂操作分解为清晰的顺序步骤。对于特别复杂的工作流，提供一个检查清单，Claude 可以将其复制到响应中并在进展过程中逐项勾选。

示例 1：研究综合工作流（适用于不含代码的 Skill）：

```Markdown
## Research synthesis workflow

Copy this checklist and track your progress:

```
Research Progress:
- [ ] Step 1: Read all source documents
- [ ] Step 2: Identify key themes
- [ ] Step 3: Cross-reference claims
- [ ] Step 4: Create structured summary
- [ ] Step 5: Verify citations
```

**Step 1: Read all source documents**

Review each document in the `sources/` directory. Note the main arguments and supporting evidence.

**Step 2: Identify key themes**

Look for patterns across sources. What themes appear repeatedly? Where do sources agree or disagree?

**Step 3: Cross-reference claims**

For each major claim, verify it appears in the source material. Note which source supports each point.

**Step 4: Create structured summary**

Organize findings by theme. Include:
- Main claim
- Supporting evidence from sources
- Conflicting viewpoints (if any)

**Step 5: Verify citations**

Check that every claim references the correct source document. If citations are incomplete, return to Step 3.
```

检查清单模式适用于任何复杂的多步骤流程。

示例 2：PDF 表单填写工作流（适用于含代码的 Skill）：

```Markdown
## PDF form filling workflow

Copy this checklist and check off items as you complete them:

```
Task Progress:
- [ ] Step 1: Analyze the form (run analyze_form.py)
- [ ] Step 2: Create field mapping (edit fields.json)
- [ ] Step 3: Validate mapping (run validate_fields.py)
- [ ] Step 4: Fill the form (run fill_form.py)
- [ ] Step 5: Verify output (run verify_output.py)
```

**Step 1: Analyze the form**

Run: `python scripts/analyze_form.py input.pdf`

This extracts form fields and their locations, saving to `fields.json`.

**Step 2: Create field mapping**

Edit `fields.json` to add values for each field.

**Step 3: Validate mapping**

Run: `python scripts/validate_fields.py fields.json`

Fix any validation errors before continuing.

**Step 4: Fill the form**

Run: `python scripts/fill_form.py input.pdf fields.json output.pdf`

**Step 5: Verify output**

Run: `python scripts/verify_output.py output.pdf`

If verification fails, return to Step 2.
```

清晰的步骤可防止 Claude 跳过关键验证。检查清单帮助 Claude 和您跟踪多步骤工作流的进度。

## 实现反馈循环

常见模式： 运行验证器 → 修复错误 → 重复。此模式可大大提高输出质量。

示例 1：风格指南合规性（适用于不含代码的 Skill）：

```Markdown
## Content review process

1. Draft your content following the guidelines in STYLE_GUIDE.md
2. Review against the checklist:
   - Check terminology consistency
   - Verify examples follow the standard format
   - Confirm all required sections are present
3. If issues found:
   - Note each issue with specific section reference
   - Revise the content
   - Review the checklist again
4. Only proceed when all requirements are met
5. Finalize and save the document
```

这展示了使用参考文档而非脚本的验证循环模式。"验证器"是 STYLE\_GUIDE\.md，Claude 通过读取和比较来执行检查。

示例 2：文档编辑流程（适用于含代码的 Skill）：

```Markdown
## Document editing process

1. Make your edits to `word/document.xml`
2. **Validate immediately**: `python ooxml/scripts/validate.py unpacked_dir/`
3. If validation fails:
   - Review the error message carefully
   - Fix the issues in the XML
   - Run validation again
4. **Only proceed when validation passes**
5. Rebuild: `python ooxml/scripts/pack.py unpacked_dir/ output.docx`
6. Test the output document
```

验证循环可及早发现错误。

# 内容指南

## 避免时效性信息

不要包含会过时的信息：

不良示例：时效性信息（会变得错误）：

```Markdown
If you're doing this before August 2025, use the old API.
After August 2025, use the new API.
```

良好示例（使用"旧模式"部分）：

```Markdown
## Current method

Use the v2 API endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated 2025-08)</summary>

The v1 API used: `api.example.com/v1/messages`

This endpoint is no longer supported.
</details>
```

旧模式部分提供历史背景，而不会使主要内容变得杂乱。

## 使用一致的术语

选择一个术语并在整个 Skill 中使用它：

良好 \- 一致：

- 始终使用 "API endpoint"

- 始终使用 "field"

- 始终使用 "extract"

不良 \- 不一致：

- 混用 "API endpoint"、"URL"、"API route"、"path"

- 混用 "field"、"box"、"element"、"control"

- 混用 "extract"、"pull"、"get"、"retrieve"

一致性有助于 Claude 理解和遵循指令。

# 常见模式

## 模板模式

为输出格式提供模板。根据您的需求匹配严格程度。

对于严格要求（如 API 响应或数据格式）：

```Markdown
## Report structure

**ALWAYS use this exact template structure:**

```markdown
# [Analysis Title]

## Executive summary
[One-paragraph overview of key findings]

## Key findings
- Finding 1 with supporting data
- Finding 2 with supporting data
- Finding 3 with supporting data

## Recommendations
1. Specific actionable recommendation
2. Specific actionable recommendation
```
```

对于灵活指导（当适应性有用时）：

```Python
## Report structure

Here is a sensible default format, but use your best judgment based on the analysis:

```markdown
# [Analysis Title]

## Executive summary
[Overview]

## Key findings
[Adapt sections based on what you discover]

## Recommendations
[Tailor to the specific context]
```

Adjust sections as needed for the specific analysis type.
```

## 示例模式

对于输出质量依赖于查看示例的 Skill，像常规提示一样提供输入/输出对：

```JavaScript
## Commit message format

Generate commit messages following these examples:

**Example 1:**
Input: Added user authentication with JWT tokens
Output:
```
feat(auth): implement JWT-based authentication

Add login endpoint and token validation middleware
```

**Example 2:**
Input: Fixed bug where dates displayed incorrectly in reports
Output:
```
fix(reports): correct date formatting in timezone conversion

Use UTC timestamps consistently across report generation
```

**Example 3:**
Input: Updated dependencies and refactored error handling
Output:
```
chore: update dependencies and refactor error handling

- Upgrade lodash to 4.17.21
- Standardize error response format across endpoints
```

Follow this style: type(scope): brief description, then detailed explanation.
```

与单纯的描述相比，示例能帮助 Claude 更清楚地理解所需的风格和详细程度。

## 条件工作流模式

引导 Claude 通过决策点：

```Markdown
## Document modification workflow

1. Determine the modification type:

   **Creating new content?** → Follow "Creation workflow" below
   **Editing existing content?** → Follow "Editing workflow" below

2. Creation workflow:
   - Use docx-js library
   - Build document from scratch
   - Export to .docx format

3. Editing workflow:
   - Unpack existing document
   - Modify XML directly
   - Validate after each change
   - Repack when complete
```

如果工作流变得庞大或复杂，包含许多步骤，请考虑将它们放入单独的文件中，并告诉 Claude 根据当前任务读取相应的文件。

# 评估和迭代

## 构建评估

在编写大量文档之前创建评估。 这确保您的 Skill 解决的是真实问题，而不是记录想象中的问题。

评估驱动的开发：

1. 识别差距： 在没有 Skill 的情况下让 Claude 执行代表性任务。记录具体的失败或缺失的上下文

2. 创建评估： 构建三个测试这些差距的场景

3. 建立基线： 测量 Claude 在没有 Skill 的情况下的表现

4. 编写最少的指令： 创建刚好足够的内容来解决差距并通过评估

5. 迭代： 执行评估，与基线比较，并进行优化

这种方法确保您解决的是实际问题，而不是预测可能永远不会出现的需求。

评估结构：

```JSON
{
  "skills": ["pdf-processing"],
  "query": "Extract all text from this PDF file and save it to output.txt",
  "files": ["test-files/document.pdf"],
  "expected_behavior": [
    "Successfully reads the PDF file using an appropriate PDF processing library or command-line tool",
    "Extracts text content from all pages in the document without missing any pages",
    "Saves the extracted text to a file named output.txt in a clear, readable format"
  ]
}
```

## 与 Claude 一起迭代开发 Skill

与一个 Claude 实例（"Claude A"）合作创建一个供其他实例（"Claude B"）使用的 Skill。

Anthropic提供了skill\-creator，一个用于编写Skill的Skill。

Claude A 帮助您设计和完善指令，而 Claude B 在实际任务中测试它们。这之所以有效，是因为 Claude 模型既了解如何编写有效的智能体指令，也了解智能体需要什么信息。

创建新 Skill：

1. 在没有 Skill 的情况下完成任务： 使用常规提示与 Claude A 一起解决问题。在工作过程中，您会自然地提供上下文、解释偏好并分享程序性知识。注意您反复提供的信息。

2. 识别可重用模式： 完成任务后，识别您提供的哪些上下文对未来类似任务有用。

3. 示例： 如果您完成了一个 BigQuery 分析，您可能提供了表名、字段定义、过滤规则（如"始终排除测试账户"）和常见查询模式。

4. 请 Claude A 创建 Skill： "创建一个 Skill，捕获我们刚刚使用的这个 BigQuery 分析模式。包括表架构、命名约定以及关于过滤测试账户的规则。"

5. Claude 模型原生理解 Skill 格式和结构。您不需要特殊的系统提示或"编写 Skill"的 Skill 来让 Claude 帮助创建 Skill。只需请 Claude 创建一个 Skill，它就会生成结构正确的 SKILL\.md 内容，包含适当的 frontmatter 和正文内容。

6. 审查简洁性： 检查 Claude A 是否添加了不必要的解释。询问："删除关于胜率含义的解释——Claude 已经知道这一点。"

7. 改进信息架构： 请 Claude A 更有效地组织内容。例如："重新组织一下，将表架构放在单独的参考文件中。我们以后可能会添加更多表。"

8. 在类似任务上测试： 在相关用例上使用 Claude B（加载了 Skill 的全新实例）测试该 Skill。观察 Claude B 是否找到正确的信息、正确应用规则并成功处理任务。

9. 基于观察进行迭代： 如果 Claude B 遇到困难或遗漏了某些内容，带着具体信息返回 Claude A："当 Claude 使用这个 Skill 时，它忘记了为 Q4 按日期过滤。我们是否应该添加一个关于日期过滤模式的部分？"

迭代现有 Skill：

改进 Skill 时，同样的分层模式继续适用。您在以下之间交替：

- 与 Claude A 合作（帮助完善 Skill 的专家）

- 使用 Claude B 测试（使用 Skill 执行实际工作的智能体）

- 观察 Claude B 的行为并将洞察带回 Claude A

1. 在实际工作流中使用 Skill： 给 Claude B（已加载 Skill）实际任务，而不是测试场景

2. 观察 Claude B 的行为： 记录它在哪里遇到困难、成功或做出意外选择

3. 观察示例： "当我向 Claude B 请求区域销售报告时，它编写了查询，但忘记过滤掉测试账户，尽管 Skill 提到了这条规则。"

4. 返回 Claude A 进行改进： 分享当前的 SKILL\.md 并描述您观察到的情况。询问："我注意到当我请求区域报告时，Claude B 忘记过滤测试账户。Skill 提到了过滤，但也许不够突出？"

5. 审查 Claude A 的建议： Claude A 可能建议重新组织以使规则更突出，使用更强的语言如"必须过滤"而不是"始终过滤"，或重构工作流部分。

6. 应用并测试更改： 使用 Claude A 的改进更新 Skill，然后在类似请求上再次使用 Claude B 测试

7. 基于使用情况重复： 在遇到新场景时继续这个观察\-完善\-测试循环。每次迭代都基于真实的智能体行为而非假设来改进 Skill。

收集团队反馈：

1. 与团队成员分享 Skill 并观察他们的使用情况

2. 询问：Skill 是否在预期时激活？指令是否清晰？缺少什么？

3. 整合反馈以解决您自己使用模式中的盲点

这个方法中，Claude A 了解智能体需求，您提供领域专业知识，Claude B 通过实际使用揭示差距，迭代完善基于观察到的行为来改进 Skill。

## 观察 Claude 如何浏览 Skill

在迭代 Skill 时，注意 Claude 在实践中如何实际使用它们。观察以下情况：

- 意外的探索路径： Claude 是否以您未预料的顺序读取文件？这可能表明您的结构不如您想象的那样直观

- 遗漏的连接： Claude 是否未能跟随对重要文件的引用？您的链接可能需要更明确或更突出

- 过度依赖某些部分： 如果 Claude 反复读取同一个文件，请考虑该内容是否应该放在主 SKILL\.md 中

- 被忽略的内容： 如果 Claude 从未访问某个打包文件，它可能是不必要的，或者在主指令中标示不清

基于这些观察而非假设进行迭代。Skill 元数据中的 'name' 和 'description' 尤为关键。Claude 在决定是否针对当前任务触发 Skill 时会使用这些信息。确保它们清楚地描述 Skill 的功能以及何时应该使用它。

# 应避免的反模式

## 避免 Windows 风格的路径

始终在文件路径中使用正斜杠，即使在 Windows 上也是如此：

- ✓ 良好： `scripts/helper.py`、`reference/guide.md`

- ✗ 避免： `scripts\helper.py`、`reference\guide.md`

Unix 风格的路径在所有平台上都有效，而 Windows 风格的路径在 Unix 系统上会导致错误。

## 避免提供过多选项

除非必要，否则不要提供多种方法：

```Markdown
**Bad example: Too many choices** (confusing):
"You can use pypdf, or pdfplumber, or PyMuPDF, or pdf2image, or..."

**Good example: Provide a default** (with escape hatch):
"Use pdfplumber for text extraction:
```python
import pdfplumber
```

For scanned PDFs requiring OCR, use pdf2image with pytesseract instead."
```

# 高级：包含可执行代码的 Skill

以下部分重点介绍包含可执行脚本的 Skill。如果您的 Skill 仅使用 markdown 指令，请跳至[高效 Skill 检查清单](https://platform.claude.com/docs/zh-CN/agents-and-tools/agent-skills/best-practices#checklist-for-effective-skills)。

## 解决问题，而非推卸

在为 Skill 编写脚本时，处理错误条件而不是推卸给 Claude。

良好示例：显式处理错误：

```Python
def process_file(path):
    """Process a file, creating it if it doesn't exist."""
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        # 创建带有默认内容的文件，而不是失败
        print(f"File {path} not found, creating default")
        with open(path, "w") as f:
            f.write("")
        return ""
    except PermissionError:
        # 提供替代方案，而不是失败
        print(f"Cannot access {path}, using default")
        return ""
```

不良示例：推卸给 Claude：

```Markdown
def process_file(path):
    # 直接失败，让 Claude 自行处理
    return open(path).read()
```

配置参数也应有充分理由并加以记录，以避免"巫术常量"（Ousterhout 定律）。如果您不知道正确的值，Claude 又如何确定它？

良好示例：自文档化：

```Markdown
# HTTP 请求通常在 30 秒内完成
# 较长的超时时间可应对慢速连接
REQUEST_TIMEOUT = 30

# 三次重试在可靠性与速度之间取得平衡
# 大多数间歇性故障在第二次重试时即可解决
MAX_RETRIES = 3
```

不良示例：魔法数字：

```Markdown
TIMEOUT = 47  # Why 47?
RETRIES = 5  # Why 5?
```

## 提供实用脚本

即使 Claude 可以编写脚本，预制脚本也具有优势：

实用脚本的好处：

- 比生成的代码更可靠

- 节省令牌（无需在上下文中包含代码）

- 节省时间（无需生成代码）

- 确保跨使用的一致性

![Image](https://internal-api-drive-stream.feishu.cn/space/api/box/stream/download/authcode/?code=NThjNDQ3ZjkzYjFmMGY3OTE2NWE1YmM2MzZhYTI0NTZfNjkyZmQzNTdlN2VkYTEwYmM3NGQ2MDk4ODdhMTQzNDJfSUQ6NzY1MTYzMTMxNjczMTE1MzYxOV8xNzgxNjk4MTE1OjE3ODE3ODQ1MTVfVjM)

上图显示了可执行脚本如何与指令文件协同工作。指令文件（forms\.md）引用脚本，Claude 可以执行它而无需将其内容加载到上下文中。

重要区别： 在您的指令中明确说明 Claude 应该：

- 执行脚本（最常见）："运行 `analyze_form.py` 以提取字段"

- 将其作为参考阅读（用于复杂逻辑）："参见 `analyze_form.py` 了解字段提取算法"

对于大多数实用脚本，执行是首选，因为它更可靠、更高效。有关脚本执行工作原理的详细信息，请参阅下方的[运行时环境](https://platform.claude.com/docs/zh-CN/agents-and-tools/agent-skills/best-practices#runtime-environment)部分。

示例：

```Python
## Utility scripts

**analyze_form.py**: Extract all form fields from PDF

```bash
python scripts/analyze_form.py input.pdf > fields.json
```

Output format:
```json
{
  "field_name": {"type": "text", "x": 100, "y": 200},
  "signature": {"type": "sig", "x": 150, "y": 500}
}
```

**validate_boxes.py**: Check for overlapping bounding boxes

```bash
python scripts/validate_boxes.py fields.json
# Returns: "OK" or lists conflicts
```

**fill_form.py**: Apply field values to PDF

```bash
python scripts/fill_form.py input.pdf fields.json output.pdf
```
```

## 使用视觉分析

当输入可以渲染为图像时，让 Claude 分析它们：

```Markdown
## Form layout analysis

1. Convert PDF to images:
   ```bash
   python scripts/pdf_to_images.py form.pdf
   ```

2. Analyze each page image to identify form fields
3. Claude can see field locations and types visually
```

Claude 的视觉能力有助于理解布局和结构。

## 创建可验证的中间输出

当 Claude 执行复杂的开放式任务时，可能会出错。"计划\-验证\-执行"模式通过让 Claude 首先以结构化格式创建计划，然后在执行之前用脚本验证该计划，从而及早发现错误。

示例： 假设要求 Claude 根据电子表格更新 PDF 中的 50 个表单字段。如果没有验证，Claude 可能会引用不存在的字段、创建冲突的值、遗漏必填字段或错误地应用更新。

解决方案： 使用上面显示的工作流模式（PDF 表单填写），但添加一个中间 `changes.json` 文件，在应用更改之前对其进行验证。工作流变为：分析 → 创建计划文件 → 验证计划 → 执行 → 验证。

为什么此模式有效：

- 及早发现错误： 验证在应用更改之前发现问题

- 机器可验证： 脚本提供客观验证

- 可逆的计划： Claude 可以在不触及原始文件的情况下迭代计划

- 清晰的调试： 错误消息指向具体问题

何时使用： 批量操作、破坏性更改、复杂验证规则、高风险操作。

实现提示： 使验证脚本输出详细的具体错误消息，如"未找到字段 'signature\_date'。可用字段：customer\_name、order\_total、signature\_date\_signed"，以帮助 Claude 修复问题。

## 包依赖

Skill 在代码执行环境中运行，具有特定于平台的限制：

- claude\.ai： 可以从 npm 和 PyPI 安装包，并从 GitHub 仓库拉取

- Claude API： 没有网络访问权限，也无法在运行时安装包

在您的 SKILL\.md 中列出所需的包，并在[代码执行工具文档](https://platform.claude.com/docs/zh-CN/agents-and-tools/tool-use/code-execution-tool)中验证它们是否可用。

## 运行时环境

Skill 在具有文件系统访问、bash 命令和代码执行能力的代码执行环境中运行。有关此架构的概念性解释，请参阅概述中的 [Skill 架构](https://platform.claude.com/docs/zh-CN/agents-and-tools/agent-skills/overview#the-skills-architecture)。

这如何影响您的编写：

Claude 如何访问 Skill：

1. 元数据预加载： 在启动时，所有 Skill 的 YAML frontmatter 中的名称和描述会被加载到系统提示中

2. 按需读取文件： Claude 在需要时使用 bash Read 工具从文件系统访问 SKILL\.md 和其他文件

3. 高效执行脚本： 实用脚本可以通过 bash 执行，而无需将其完整内容加载到上下文中。只有脚本的输出会消耗令牌

4. 大文件无上下文开销： 参考文件、数据或文档在实际读取之前不会消耗上下文令牌

- 文件路径很重要： Claude 像浏览文件系统一样浏览您的 Skill 目录。使用正斜杠（`reference/guide.md`），而不是反斜杠

- 描述性地命名文件： 使用指示内容的名称：`form_validation_rules.md`，而不是 `doc2.md`

- 为发现而组织： 按领域或功能构建目录

    - 良好：`reference/finance.md`、`reference/sales.md`

    - 不良：`docs/file1.md`、`docs/file2.md`

- 打包全面的资源： 包含完整的 API 文档、大量示例、大型数据集；在访问之前没有上下文开销

- 对确定性操作优先使用脚本： 编写 `validate_form.py`，而不是要求 Claude 生成验证代码

- 明确执行意图：

    - "运行 `analyze_form.py` 以提取字段"（执行）

    - "参见 `analyze_form.py` 了解提取算法"（作为参考阅读）

- 测试文件访问模式： 通过实际请求测试来验证 Claude 能够浏览您的目录结构

示例：

```Markdown
bigquery-skill/
├── SKILL.md (overview, points to reference files)
└── reference/
    ├── finance.md (revenue metrics)
    ├── sales.md (pipeline data)
    └── product.md (usage analytics)
```

当用户询问收入时，Claude 读取 SKILL\.md，看到对 `reference/finance.md` 的引用，并调用 bash 仅读取该文件。sales\.md 和 product\.md 文件保留在文件系统上，在需要之前消耗零上下文令牌。这种基于文件系统的模型正是实现渐进式披露的关键。Claude 可以浏览并有选择地加载每个任务所需的内容。

## MCP 工具引用

如果您的 Skill 使用 MCP（Model Context Protocol）工具，请始终使用完全限定的工具名称以避免"未找到工具"错误。

格式： `ServerName:tool_name`

示例：

```Markdown
Use the BigQuery:bigquery_schema tool to retrieve table schemas.
Use the GitHub:create_issue tool to create issues.
```

其中：

- `BigQuery` 和 `GitHub` 是 MCP 服务器名称

- `bigquery_schema` 和 `create_issue` 是这些服务器中的工具名称

如果没有服务器前缀，Claude 可能无法定位工具，尤其是当有多个 MCP 服务器可用时。

## 避免假设工具已安装

不要假设包可用：

```Markdown
**Bad example: Assumes installation**:
"Use the pdf library to process the file."

**Good example: Explicit about dependencies**:
"Install required package: `pip install pypdf`

Then use it:
```python
from pypdf import PdfReader
reader = PdfReader("file.pdf")
```"
```

# 高效 Skill 检查清单

在分享 Skill 之前，请验证：

## 核心质量

* [ ] 描述具体且包含关键术语

* [ ] 描述同时包含 Skill 的功能和何时使用它

* [ ] SKILL\.md 正文在 500 行以内

* [ ] 额外详情在单独的文件中（如果需要）

* [ ] 无时效性信息（或在"旧模式"部分中）

* [ ] 全文术语一致

* [ ] 示例具体而非抽象

* [ ] 文件引用仅一层深度

* [ ] 适当使用渐进式披露

* [ ] 工作流有清晰的步骤

## 代码和脚本

* [ ] 脚本解决问题而不是推卸给 Claude

* [ ] 错误处理明确且有帮助

* [ ] 没有"巫术常量"（所有值都有理由）

* [ ] 所需包在指令中列出并验证为可用

* [ ] 脚本有清晰的文档

* [ ] 没有 Windows 风格的路径（全部使用正斜杠）

* [ ] 关键操作有验证/核实步骤

* [ ] 质量关键任务包含反馈循环

## 测试

* [ ] 至少创建了三个评估

* [ ] 使用 Haiku、Sonnet 和 Opus 进行了测试

* [ ] 使用真实使用场景进行了测试

* [ ] 整合了团队反馈（如适用）

