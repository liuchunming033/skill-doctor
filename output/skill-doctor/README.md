# Skill Doctor —— Skill Health Check Tool

[English](README.md) | [简体中文](README.zh-CN.md)

> Built on the best practices from [hands-on-skill](https://github.com/liuchunming033/hands-on-skill).

## Features

- **9 Health Checks**: description, gotchas, file organization, over-constraint, known knowledge, memory config, scripts, hooks, markdown format
- **Lightweight Skill Exemption**: single-file skills ≤80 lines are auto-recognized and exempt from auxiliary file requirements
- **Interactive Optimization**: presents an options list with expected score gains and benefit estimates — you choose what to fix
- **Automated Analysis**: Python script-based analysis producing JSON reports and Markdown suggestions
- **Grading System**: A/B/C/D four-tier grading to quantify Skill quality
- **Actionable Suggestions**: specific fix recommendations for every issue found
- **Best Practice Examples**: extensive Before/After comparison examples

## Installation

### Option 1: Tell Your Agent (Recommended)

> "Install skill-doctor from `github.com/liuchunming033/skill-doctor`."

Your Agent will auto-clone and place it correctly.

### Option 2: `npx skills add`

```bash
# Project-level (./.claude/skills or your Agent's skills directory)
npx skills add liuchunming033/skill-doctor

# Global (available across all projects)
npx skills add liuchunming033/skill-doctor -g
```

### Usage

Once installed, say in conversation:

```
Check this Skill: path/to/your/skill
```

Skill Doctor loads the target Skill, runs all nine health checks, generates a diagnostic report, and presents interactive optimization options.

## Health Checks

Covers nine dimensions: description, gotchas, file organization, over-constraint, known knowledge, memory config, scripts, hooks, and markdown format. See [SKILL.md](SKILL.md) for details.

## Scoring

Four tiers: A (90-100) / B (75-89) / C (60-74) / D (<60). See [SKILL.md](SKILL.md) for details.

## Directory Structure

```
skill-doctor/
├── SKILL.md              # Core logic (follows best practices)
├── gotchas.md            # Gotchas (17 real pitfalls recorded)
├── examples.md           # Before/After optimization examples
├── README.md             # Usage guide (English)
├── README.zh-CN.md       # Usage guide (Simplified Chinese)
├── reference/
│   └── checklists.md     # Detailed checklists
├── config/
│   └── config.json       # Check rule configuration
└── scripts/
    └── analyze_skill.py  # Automated health check script
```

## Best Practices Followed

This skill-doctor itself strictly follows all best practices from [hands-on-skill](https://github.com/liuchunming033/hands-on-skill):

- **description as trigger** (not a feature description)
- **gotchas with substance** (17 real pitfalls recorded)
- **three-category directory structure** (root: SKILL.md + gotchas.md + examples.md; reference/ for reference materials; config/ for configuration; scripts/ for scripts)
- **no over-constraint** (describes decision frameworks, not rigid steps)
- **no known knowledge** (only adds Skill-specific knowledge)
- **persistent config** (config.json)
- **stable scripts** (analyze_skill.py)
- **proper Markdown** (YAML frontmatter, aligned tables, language-tagged code blocks)
- **progressive disclosure** (details in auxiliary files, loaded on demand)

## How It Works

1. Script runs structured analysis (`python scripts/analyze_skill.py <skill_path> --output json`)
2. Agent supplements the report with specific optimization suggestions, expected score gains, and effort estimates
3. An interactive options list is presented — you choose which items to fix
4. Accepted items are fixed in-place (files are modified directly)
5. A re-check generates a before/after comparison report

## Contribution Guide

Contributions welcome!

1. Fork this repo
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

MIT License — see [LICENSE](LICENSE)

## Acknowledgments

- Thanks to Anthropic for Skill best practices
- Thanks to Google and OpenAI for enterprise-level case studies
- Thanks to the open-source community for contributions

---

**Use skill-doctor to make every Skill a masterpiece.**
