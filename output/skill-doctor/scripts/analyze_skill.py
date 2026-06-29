#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Skill Doctor - Skill体检诊断脚本

用法：
  python analyze_skill.py <skill_path>
  python analyze_skill.py <skill_path> --output json
  python analyze_skill.py <skill_path> --output markdown

输出：
  - JSON报告（包含得分、问题清单、优化建议）
  - Markdown建议（人类可读的优化建议）
"""

from __future__ import print_function, unicode_literals
import os
import sys
import json
import argparse
from pathlib import Path

# Python 2/3 compatibility
if sys.version_info[0] >= 3:
    def s(text):
        return text
else:
    def s(text):
        return text.encode('utf-8')


class SkillDoctor:
    """Skill体检诊断工具"""

    def __init__(self, skill_path, config_path=None):
        self.skill_path = Path(skill_path)
        self.config = self.load_config(config_path)

    def load_config(self, config_path):
        """加载配置"""
        if config_path:
            with open(config_path) as f:
                return json.load(f)
        return {
            "check_weights": {
                "description": 1.5,
                "gotchas": 1.5,
                "file_organization": 1.0,
                "over_constraint": 1.0,
                "known_knowledge": 1.0,
                "memory_config": 1.0,
                "scripts": 1.0,
                "hooks": 1.0,
                "markdown_format": 1.0,
                "comprehensive": 1.0
            },
            "score_thresholds": {
                "grade_A": 90,
                "grade_B": 75,
                "grade_C": 60,
                "grade_D": 0
            },
            "max_description_length": 100,
            "max_skillmd_lines": 200,
            "min_gotchas_bytes": 500,
            "min_gotchas_items": 3
        }

    def analyze(self):
        """全面体检"""
        results = {
            "skill_name": self.skill_path.name,
            "overall_score": 0,
            "grade": "",
            "check_results": {},
            "priority_fixes": [],
            "suggestions": []
        }

        # 运行九大检查
        checks = [
            ("description", self.check_description),
            ("gotchas", self.check_gotchas),
            ("file_organization", self.check_file_organization),
            ("over_constraint", self.check_over_constraint),
            ("known_knowledge", self.check_known_knowledge),
            ("memory_config", self.check_memory_config),
            ("scripts", self.check_scripts),
            ("hooks", self.check_hooks),
            ("markdown_format", self.check_markdown_format)
        ]

        total_weighted_score = 0
        total_weight = 0

        for check_name, check_func in checks:
            if check_name in self.config.get("skip_checks", []):
                continue

            score, issues, suggestions = check_func()
            weight = self.config["check_weights"][check_name]

            results["check_results"][check_name] = {
                "score": score,
                "weight": weight,
                "issues": issues,
                "suggestions": suggestions
            }

            total_weighted_score += score * weight
            total_weight += weight

            # 收集优先修复项
            if score < 70:
                for issue in issues[:2]:
                    results["priority_fixes"].append(
                        "立即修复({}): {}".format(check_name, issue)
                    )

            # 收集优化建议
            results["suggestions"].extend(suggestions)

        # 计算总分
        results["overall_score"] = int(total_weighted_score / total_weight)

        # 确定等级
        score = results["overall_score"]
        if score >= 90:
            results["grade"] = "A"
        elif score >= 75:
            results["grade"] = "B"
        elif score >= 60:
            results["grade"] = "C"
        else:
            results["grade"] = "D"

        return results

    def check_description(self):
        """检查description"""
        issues = []
        suggestions = []

        # 检查SKILL.md是否存在
        skillmd_path = self.skill_path / "SKILL.md"
        if not skillmd_path.exists():
            return (0, ["SKILL.md不存在"], ["创建SKILL.md文件"])

        # 读取YAML frontmatter
        try:
            with open(skillmd_path) as f:
                content = f.read()

            # 提取description
            if not content.startswith("---"):
                return (0, ["缺少YAML frontmatter"], ["添加YAML frontmatter"])

            yaml_end = content.find("---", 3)
            if yaml_end == -1:
                return (0, ["YAML frontmatter格式错误"], ["修复YAML格式"])

            yaml_content = content[3:yaml_end]

            # 解析description
            description = None
            for line in yaml_content.split("\n"):
                if line.startswith("description:"):
                    description = line.split(":", 1)[1].strip()
                    break

            if not description:
                return (0, ["缺少description字段"], ["添加description"])

            # 检查长度
            if len(description) > self.config["max_description_length"]:
                issues.append("description过长({}字符)".format(len(description)))
                suggestions.append("缩短description至{}字符内".format(
                    self.config['max_description_length']))

            # 检查是否写成功能说明
            bad_patterns = ["这是一个", "该Skill用于", "本Skill", "这是一个帮助"]
            for pattern in bad_patterns:
                if pattern in description:
                    issues.append("description写成功能说明(包含'{}')".format(pattern))
                    suggestions.append("改为触发条件(如'当用户说XXX时触发')")

            # 检查触发关键词
            trigger_keywords = ["当用户说", "在", "触发", "用于"]
            has_trigger = any(kw in description for kw in trigger_keywords)
            if not has_trigger:
                issues.append("description缺少触发关键词")
                suggestions.append("添加触发关键词(如'当用户说XXX时触发')")

            # 计算得分
            if len(issues) == 0:
                score = 95
            elif len(issues) <= 1:
                score = 70
            else:
                score = 50

        except Exception as e:
            return (0, ["读取失败: {}".format(str(e))], ["检查文件格式"])

        return (score, issues, suggestions)

    def check_gotchas(self):
        """检查gotchas"""
        issues = []
        suggestions = []

        gotchas_path = self.skill_path / "gotchas.md"
        if not gotchas_path.exists():
            return (40, ["gotchas.md不存在"], ["创建gotchas.md文件"])

        try:
            with open(gotchas_path) as f:
                content = f.read()

            # 检查文件大小
            if len(content) < self.config["min_gotchas_bytes"]:
                issues.append("gotchas.md内容太少({}字节)".format(len(content)))
                suggestions.append("补充内容至{}字节以上".format(
                    self.config['min_gotchas_bytes']))

            # 检查占位符
            placeholders = ["暂无", "TODO", "待补充", "待完善"]
            for placeholder in placeholders:
                if placeholder in content:
                    issues.append("包含占位符'{}'".format(placeholder))
                    suggestions.append("补充真实坑点")

            # 检查坑点数量
            gotchas_count = content.count("## 坑点")
            if gotchas_count < self.config["min_gotchas_items"]:
                issues.append("坑点数量太少({}个)".format(gotchas_count))
                suggestions.append("补充至少{}个坑点".format(
                    self.config['min_gotchas_items']))

            # 检查结构
            if "现象" not in content or "问题" not in content or "解决" not in content:
                issues.append("缺少'现象-问题-解决'结构")
                suggestions.append("每个坑点包含：现象、问题、解决")

            # 计算得分
            if len(issues) == 0:
                score = 90
            elif len(issues) <= 2:
                score = 70
            else:
                score = 40

        except Exception as e:
            return (0, ["读取失败: {}".format(str(e))], ["检查文件格式"])

        return (score, issues, suggestions)

    def check_file_organization(self):
        """检查文件组织"""
        issues = []
        suggestions = []

        # 检查SKILL.md行数
        skillmd_path = self.skill_path / "SKILL.md"
        if skillmd_path.exists():
            with open(skillmd_path) as f:
                lines = len(f.readlines())

            if lines > self.config["max_skillmd_lines"]:
                issues.append("SKILL.md过长({}行)".format(lines))
                suggestions.append("缩短至{}行内，详细内容拆分到附属文件".format(
                    self.config['max_skillmd_lines']))

        # 检查是否有附属文件
        all_files = list(self.skill_path.glob("*.md"))
        if len(all_files) == 1:  # 只有SKILL.md
            issues.append("缺少附属文件")
            suggestions.append("创建gotchas.md、examples.md等附属文件")

        # 检查是否有references目录
        has_references = (self.skill_path / "references").exists()
        if not has_references and len(all_files) <= 2:
            suggestions.append("考虑创建references目录组织详细内容")

        # 计算得分
        if len(issues) == 0:
            score = 90
        elif len(issues) <= 1:
            score = 70
        else:
            score = 50

        return (score, issues, suggestions)

    def check_over_constraint(self):
        """检查过度约束"""
        issues = []
        suggestions = []

        skillmd_path = self.skill_path / "SKILL.md"
        if not skillmd_path.exists():
            return (0, ["SKILL.md不存在"], ["创建SKILL.md文件"])

        try:
            with open(skillmd_path) as f:
                content = f.read()

            # 检查死板流程
            step_patterns = ["第一步", "第二步", "Step 1", "Step 2", "1.", "2.", "3."]
            has_steps = sum(1 for pattern in step_patterns if pattern in content)

            if has_steps >= 3:
                issues.append("包含死板流程({}个步骤标记)".format(has_steps))
                suggestions.append("改为决策框架，描述目标而非路径")

            # 检查决策点
            decision_keywords = ["判断", "选择", "根据", "决定", "检查"]
            has_decisions = any(kw in content for kw in decision_keywords)
            if not has_decisions:
                issues.append("缺少决策点")
                suggestions.append("添加决策点(如'判断XXX类型')")

            # 计算得分
            if len(issues) == 0:
                score = 90
            elif len(issues) == 1:
                score = 70
            else:
                score = 50

        except Exception as e:
            return (0, ["读取失败: {}".format(str(e))], ["检查文件格式"])

        return (score, issues, suggestions)

    def check_known_knowledge(self):
        """检查已知知识"""
        issues = []
        suggestions = []

        skillmd_path = self.skill_path / "SKILL.md"
        if not skillmd_path.exists():
            return (0, ["SKILL.md不存在"], ["创建SKILL.md文件"])

        try:
            with open(skillmd_path) as f:
                content = f.read()

            # 检查教程式表述
            tutorial_patterns = ["什么是", "介绍", "教程", "入门", "指南"]
            has_tutorial = sum(1 for pattern in tutorial_patterns if pattern in content)

            if has_tutorial >= 2:
                issues.append("包含教程式内容({}处)".format(has_tutorial))
                suggestions.append("删除Agent已知知识，只补充团队特有知识")

            # 检查是否有团队特有内容
            team_keywords = ["团队", "公司", "规范", "特有", "配置"]
            has_team = any(kw in content for kw in team_keywords)
            if not has_team:
                issues.append("缺少团队特有知识")
                suggestions.append("补充团队规范、公司流程等特有内容")

            # 计算得分
            if len(issues) == 0:
                score = 95
            elif len(issues) == 1:
                score = 70
            else:
                score = 40

        except Exception as e:
            return (0, ["读取失败: {}".format(str(e))], ["检查文件格式"])

        return (score, issues, suggestions)

    def check_memory_config(self):
        """检查内存配置"""
        issues = []
        suggestions = []

        config_path = self.skill_path / "config.json"
        if not config_path.exists():
            # Skill可能不需要配置，返回N/A
            return (90, [], ["如果需要持久化配置，创建config.json"])

        try:
            with open(config_path) as f:
                config = json.load(f)

            # 检查是否为空
            if len(config) == 0:
                issues.append("config.json为空")
                suggestions.append("补充团队偏好配置")

            # 检查是否有合理配置项
            common_configs = ["language", "max_length", "team_rules", "default"]
            has_common = sum(1 for key in common_configs if key in config)

            if has_common == 0:
                issues.append("config.json缺少常见配置项")
                suggestions.append("补充language、team_rules等配置")

            # 计算得分
            if len(issues) == 0:
                score = 90
            elif len(issues) == 1:
                score = 70
            else:
                score = 50

        except Exception as e:
            return (0, ["读取失败: {}".format(str(e))], ["检查JSON格式"])

        return (score, issues, suggestions)

    def check_scripts(self):
        """检查脚本"""
        issues = []
        suggestions = []

        scripts_path = self.skill_path / "scripts"
        if not scripts_path.exists():
            # Skill可能不需要脚本，返回N/A
            return (90, [], ["如果需要稳定能力封装，创建scripts目录"])

        # 检查是否有Python脚本
        py_scripts = list(scripts_path.glob("*.py"))
        if len(py_scripts) == 0:
            issues.append("scripts目录缺少Python脚本")
            suggestions.append("创建稳定能力脚本")

        # 检查脚本是否有注释
        for script in py_scripts:
            with open(script) as f:
                content = f.read()
            if not content.startswith("#") or "用法" not in content:
                issues.append("{}缺少注释或用法说明".format(script.name))
                suggestions.append("为{}添加注释".format(script.name))

        # 计算得分
        if len(issues) == 0:
            score = 90
        elif len(issues) <= 1:
            score = 70
        else:
            score = 50

        return (score, issues, suggestions)

    def check_hooks(self):
        """检查hooks"""
        issues = []
        suggestions = []

        # 检查SKILL.md frontmatter中的hooks
        skillmd_path = self.skill_path / "SKILL.md"
        has_hooks_in_skillmd = False

        if skillmd_path.exists():
            with open(skillmd_path) as f:
                content = f.read()
            if "hooks:" in content:
                has_hooks_in_skillmd = True
                # 简单检查hooks格式
                if "PreToolUse" not in content and "PostToolUse" not in content:
                    issues.append("hooks类型错误(应为PreToolUse或PostToolUse)")
                    suggestions.append("修正hooks类型")

                if "matcher:" not in content:
                    issues.append("hooks缺少matcher")
                    suggestions.append("添加matcher字段")

        # 如果没有hooks，返回N/A
        if not has_hooks_in_skillmd:
            return (90, [], ["如果需要监控或拦截，配置hooks"])

        # 计算得分
        if len(issues) == 0:
            score = 95
        elif len(issues) == 1:
            score = 70
        else:
            score = 50

        return (score, issues, suggestions)

    def check_markdown_format(self):
        """检查Markdown格式"""
        issues = []
        suggestions = []

        skillmd_path = self.skill_path / "SKILL.md"
        if not skillmd_path.exists():
            return (0, ["SKILL.md不存在"], ["创建SKILL.md文件"])

        try:
            with open(skillmd_path) as f:
                content = f.read()

            # 检查YAML frontmatter
            if not content.startswith("---"):
                issues.append("缺少YAML frontmatter")
                suggestions.append("添加YAML frontmatter(包含name和description)")

            yaml_end = content.find("---", 3)
            if yaml_end == -1:
                issues.append("YAML frontmatter格式错误")
                suggestions.append("修复YAML格式(缺少结束---)")

            # 检查是否有name和description
            yaml_content = content[3:yaml_end] if yaml_end != -1 else ""
            if "name:" not in yaml_content:
                issues.append("YAML缺少name字段")
                suggestions.append("添加name字段")

            if "description:" not in yaml_content:
                issues.append("YAML缺少description字段")
                suggestions.append("添加description字段")

            # 检查表格格式（简单检查）
            if "|" in content:
                table_lines = [line for line in content.split("\n") if "|" in line]
                # 检查表格分隔行
                has_separator = any("---" in line or "|---|" in line for line in table_lines)
                if not has_separator:
                    issues.append("表格格式不规范(缺少分隔行)")
                    suggestions.append("添加表格分隔行(|---|)")

            # 计算得分
            if len(issues) == 0:
                score = 95
            elif len(issues) <= 2:
                score = 70
            else:
                score = 50

        except Exception as e:
            return (0, ["读取失败: {}".format(str(e))], ["检查文件格式"])

        return (score, issues, suggestions)

    def generate_markdown_report(self, results):
        """生成Markdown格式报告"""
        report = """# Skill体检报告：{}

## 总体评分

**得分**：{}/100
**等级**：{} ({})

---

## 各项检查得分

""".format(results['skill_name'],
           results['overall_score'],
           results['grade'],
           '优秀' if results['grade'] == 'A' else '良好' if results['grade'] == 'B' else '合格' if results['grade'] == 'C' else '不合格')

        # 添加各项检查结果
        for check_name, check_result in results["check_results"].items():
            status_icon = "✅" if check_result["score"] >= 90 else "⚠️" if check_result["score"] >= 70 else "❌"
            report += "{} **{}**：{}/100\n".format(status_icon, check_name, check_result['score'])

            if check_result["issues"]:
                report += "   - 问题：{}\n".format(', '.join(check_result['issues']))

            if check_result["suggestions"]:
                report += "   - 建议：{}\n".format(', '.join(check_result['suggestions'][:2]))

        report += "\n---\n\n## 优先修复项\n\n"

        for fix in results["priority_fixes"]:
            report += "- {}\n".format(fix)

        report += "\n---\n\n## 优化建议\n\n"

        for suggestion in results["suggestions"]:
            report += "- {}\n".format(suggestion)

        report += "\n---\n\n## 下一步行动\n\n"

        if results["grade"] == "A":
            report += "✅ Skill质量优秀，可直接投入使用。\n"
        elif results["grade"] == "B":
            report += "⚠️ Skill质量良好，建议按优先级修复少量问题。\n"
        elif results["grade"] == "C":
            report += "⚠️ Skill质量合格，建议重点修复优先项。\n"
        else:
            report += "❌ Skill质量不合格，建议重构或参考最佳实践。\n"

        return report


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="Skill体检诊断工具")
    parser.add_argument("skill_path", help="Skill目录路径")
    parser.add_argument("--output", choices=["json", "markdown", "both"], default="json",
                       help="输出格式")
    parser.add_argument("--config", help="配置文件路径")

    args = parser.parse_args()

    # 运行体检
    doctor = SkillDoctor(args.skill_path, args.config)
    results = doctor.analyze()

    # 输出结果
    if args.output == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    elif args.output == "markdown":
        report = doctor.generate_markdown_report(results)
        print(report)
    else:
        print(json.dumps(results, indent=2, ensure_ascii=False))
        print("\n---\n")
        report = doctor.generate_markdown_report(results)
        print(report)


if __name__ == "__main__":
    main()