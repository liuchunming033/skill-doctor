# Skill Doctor —— Skill体检诊断工具

[English](README.md) | 简体中文

> 这个skill基于[《hands-on-skill》](https://github.com/liuchunming033/hands-on-skill)开发。

## 🎯 功能特性

- ✅ **九大体检项目**：description、gotchas、文件组织、过度约束、已知知识、内存配置、脚本、hooks、markdown格式
- ✅ **轻量Skill豁免**：单文件≤80行自动识别，不强制要求附属文件和目录结构
- ✅ **交互式优化**：展示可优化项列表 + 预期提升 + 收益估算，用户按需选择
- ✅ **自动化检查**：Python脚本自动分析，生成JSON报告和Markdown建议
- ✅ **评分系统**：A/B/C/D四级评分，量化Skill质量
- ✅ **优化建议**：针对每个问题提供具体的修复建议
- ✅ **最佳实践示例**：包含大量Before/After对比示例

## 📦 安装

### 方式一：直接告诉 Agent（推荐）

> "安装 skill-doctor，来自 `github.com/liuchunming033/skill-doctor`。"

你的 Agent 会自动 clone、放到正确的位置。

### 方式二：`npx skills add`

```bash
# 项目级（./.claude/skills 或你 Agent 的 skills 目录）
npx skills add liuchunming033/skill-doctor

# 全局（所有项目可用）
npx skills add liuchunming033/skill-doctor -g
```

### 使用

安装后，在对话中说：

```
检查这个Skill：path/to/your/skill
```

Skill Doctor 会自动加载目标 Skill，运行九大体检项目，生成诊断报告和优化建议。

## 🔧 检查项目

涵盖 description、gotchas、文件组织、过度约束、已知知识、内存配置、脚本、hooks、markdown格式九大维度。详见 [SKILL.md](SKILL.md)。

## 📊 评分

A/B/C/D 四级（90-100 / 75-89 / 60-74 / <60），详见 [SKILL.md](SKILL.md)。

## 🏗️ 文件结构

```
skill-doctor/
├── SKILL.md              # 核心逻辑（遵循最佳实践）
├── gotchas.md            # 坑点记录（17个真实坑点）
├── examples.md           # Before/After优化示例
├── README.md             # 使用说明
├── reference/
│   └── checklists.md     # 详细检查清单
├── config/
│   └── config.json       # 检查规则配置
└── scripts/
    └── analyze_skill.py  # 自动化体检脚本
```

## ✅ 遵循的最佳实践

这个skill-doctor本身严格遵循[《hands-on-skill》](https://github.com/liuchunming033/hands-on-skill)的所有最佳实践：

- ✅ **description写成触发条件**（不是功能说明）
- ✅ **gotchas充实有价值**（17个真实坑点）
- ✅ **三分类目录结构**（根目录仅 SKILL.md + gotchas.md + examples.md，参考材料在 reference/，配置在 config/，脚本在 scripts/）
- ✅ **避免过度约束**（描述决策框架）
- ✅ **不写已知知识**（只补充Skill特有知识）
- ✅ **有内存配置**（config.json）
- ✅ **有稳定脚本**（analyze_skill.py）
- ✅ **Markdown格式规范**（YAML、表格、代码块正确）
- ✅ **渐进式披露**（详细内容在附属文件）

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

---

**用skill-doctor，让每个Skill都成为精品！** 🎯