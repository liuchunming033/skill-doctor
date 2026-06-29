# Skill Doctor —— Skill体检诊断工具

> 一个完全遵循《Skill课程最佳实践》的Skill体检诊断工具

## 🎯 功能特性

- ✅ **九大体检项目**：description、gotchas、文件组织、过度约束、已知知识、内存配置、脚本、hooks、markdown格式
- ✅ **自动化检查**：Python脚本自动分析，生成JSON报告和Markdown建议
- ✅ **评分系统**：A/B/C/D四级评分，量化Skill质量
- ✅ **优化建议**：针对每个问题提供具体的修复建议
- ✅ **最佳实践示例**：包含大量Before/After对比示例

## 📦 安装使用

### 前置要求

- Python 3.6+（推荐Python 3.13）
- 需要标准库（无需额外依赖）

### 方式一：直接使用（推荐）

```bash
# 克隆仓库
git clone https://github.com/yourusername/skill-doctor.git

# 进入目录
cd skill-doctor

# 运行体检（使用python3）
python3 scripts/analyze_skill.py <skill_path>

# 输出JSON报告
python3 scripts/analyze_skill.py <skill_path> --output json

# 输出Markdown报告
python3 scripts/analyze_skill.py <skill_path> --output markdown

# 同时输出两种格式
python3 scripts/analyze_skill.py <skill_path> --output both
```

### 方式二：作为Claude Code Skill使用

将skill-doctor目录复制到你的Claude Code skills目录：

```bash
cp -r skill-doctor ~/.claude/skills/
```

然后在Claude Code中说：
```
检查这个Skill：path/to/your/skill
```

## 🔧 九大体检项目

| 检查项 | 检查内容 | 通过标准 |
|-------|---------|---------|
| **description检查** | 是否写成触发条件 | 包含触发关键词，长度<100字符 |
| **gotchas检查** | 是否有坑点记录 | gotchas.md存在且内容充实 |
| **文件组织检查** | 是否合理拆分文件 | 主文件<200行，有附属文件 |
| **过度约束检查** | 是否过度约束路径 | 没有死板流程，有决策点 |
| **已知知识检查** | 是否重复已知内容 | 没有教程式内容 |
| **内存配置检查** | 是否有config.json | config.json存在且合理 |
| **脚本检查** | 是否需要脚本但缺失 | 有scripts目录且脚本完整 |
| **hooks检查** | hooks配置是否正确 | 格式正确，matcher准确 |
| **markdown格式检查** | 格式是否规范 | YAML、表格、代码块正确 |

## 📊 评分等级

- **A（90-100分）**：优秀，遵循所有最佳实践
- **B（75-89分）**：良好，有少量优化空间
- **C（60-74分）**：合格，有明显改进点
- **D（<60分）**：不合格，需要重构

## 📝 使用示例

### 示例1：体检一个PDF Skill

```bash
$ python3 scripts/analyze_skill.py ./my-pdf-skill

Skill体检报告：my-pdf-skill

总体评分
得分：85/100
等级：B (良好)

各项检查得分：
✅ description：95/100
⚠️ gotchas：70/100
   - 问题：gotchas.md内容太少(350字节)
   - 建议：补充内容至500字节以上
✅ file_organization：90/100
⚠️ over_constraint：70/100
   - 问题：包含死板流程(4个步骤标记)
   - 建议：改为决策框架，描述目标而非路径
...

优化建议：
- 补充内容至500字节以上
- 改为决策框架，描述目标而非路径
```

### 示例2：生成详细报告

```bash
$ python3 scripts/analyze_skill.py ./my-skill --output markdown > report.md
```

### 示例3：skill-doctor自身体检

```bash
$ python3 scripts/analyze_skill.py . --output both

得分：84/100
等级：B (良好)

说明：skill-doctor自身也遵循最佳实践，体检得分84分。
主要优化点：gotchas中包含占位符、checklists有死板流程标记（检查清单特性）。
```

## 🏗️ 文件结构

```
skill-doctor/
├── SKILL.md              # 核心逻辑（遵循最佳实践）
├── gotchas.md            # 坑点记录（10个真实坑点）
├── checklists.md         # 详细检查清单
├── examples.md           # Before/After优化示例
├── config.json           # 检查规则配置
├── README.md             # 使用说明
└── scripts/
    └── analyze_skill.py  # 自动化体检脚本
```

## ✅ 遵循的最佳实践

这个skill-doctor本身严格遵循《Skill课程》的所有最佳实践：

- ✅ **description写成触发条件**（不是功能说明）
- ✅ **gotchas充实有价值**（10个真实坑点）
- ✅ **文件组织合理**（主文件<200行，有附属文件）
- ✅ **避免过度约束**（描述决策框架）
- ✅ **不写已知知识**（只补充Skill特有知识）
- ✅ **有内存配置**（config.json）
- ✅ **有稳定脚本**（analyze_skill.py）
- ✅ **Markdown格式规范**（YAML、表格、代码块正确）
- ✅ **渐进式披露**（详细内容在附属文件）

## 🎓 相关课程

这个skill基于《Skill完整课程》开发：

- **认知篇**：心智模型、渐进式披露、自由度设计
- **设计篇**：五大设计模式
- **实战篇**：description、gotchas、文件组织、脚本、hooks
- **评估篇**：评估指标、A/B测试
- **运营篇**：长期维护、团队管理

## 🤝 贡献指南

欢迎贡献！

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

## 🙏 致谢

- 感谢Anthropic提供的Skill最佳实践
- 感谢Google、OpenAI的企业级实践案例
- 感谢开源社区的贡献

## 📮 联系方式

- 项目主页：https://github.com/yourusername/skill-doctor
- 问题反馈：https://github.com/yourusername/skill-doctor/issues

---

**用skill-doctor，让每个Skill都成为精品！** 🎯