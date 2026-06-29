---
name: follow-builders
description: 当用户说/ai、AI日报、AI行业动态、AI builders digest、或想了解AI建设者最新观点时触发。追踪top AI builders的X和播客内容，生成摘要。
---

# Follow Builders, Not Influencers

追踪 AI 领域实际在构建产品、运营公司、做研究的 builders，聚合他们在 X/Twitter 和 YouTube 播客的内容，生成可消化的摘要。

核心理念：follow builders with original opinions, not influencers who regurgitate.

**用户无需 API key**。所有 X/Twitter 和播客内容通过中心 Feed 获取。

## 平台检测

每次启动先检测运行环境：

```bash
which openclaw 2>/dev/null && echo "PLATFORM=openclaw" || echo "PLATFORM=other"
```

- **OpenClaw**：持久化 Agent，投递通过内置 channel，cron 用 `openclaw cron add`
- **Other**（Claude Code、Cursor 等）：非持久化，终端关闭即停止；自动投递需配置 Telegram/Email

保存到 `config.json` 的 `platform` 字段。

## 决策流程

### 入口判断：Onboarding 还是交付？

1. 检查 `~/.follow-builders/config.json` 中 `onboardingComplete` 字段
2. **未完成** → 执行 [onboarding.md](onboarding.md)，按平台引导用户完成初始化
3. **已完成** + 用户触发 `/ai` 或手动请求 → 立即执行 [delivery.md](delivery.md)
4. **已完成** + Cron 触发 → 执行 [delivery.md](delivery.md) 并自动投递

### Onboarding 关键决策点

| 阶段 | 决策 | OpenClaw | 其他平台 |
|------|------|----------|---------|
| 频率 | 每日/每周？ | 直接设置 | 直接设置 |
| 投递方式 | Telegram/Email/stdout？ | **跳过**（内置 channel） | 引导用户选择并配置 |
| 语言 | en/zh/bilingual？ | 两种平台一致 | — |
| API Key | 需要吗？ | 不需要 | 仅 Telegram/Email 需要 |
| Cron | 如何定时？ | `openclaw cron add` | 系统 `crontab` 或跳过 |

详细引导对话见 [onboarding.md](onboarding.md)。

### 内容交付核心原则

**Agent 的唯一职责是 remix（二次加工）**，不 fetch、不爬取、不搜索：

```bash
cd ${CLAUDE_SKILL_DIR}/scripts && node prepare-digest.js 2>/dev/null
```

脚本输出一个 JSON，包含 `config`、`podcasts`、`x`、`prompts`、`stats`、`errors`。

**绝对规则**（详见 [delivery.md](delivery.md)）：
- 只用 JSON 中的数据，不发明内容
- 每条内容含 URL，无 URL 不收录
- 不猜测职位，用 `bio` 字段或只用姓名
- 不访问 x.com、不搜索网页、不调任何 API

## 配置变更

用户通过对话修改设置（频率、语言、时间等）。处理方式见 [config-handling.md](config-handling.md)。

原则：
- 来源列表集中管理，用户不可修改
- Prompt 自定义复制到 `~/.follow-builders/prompts/` 避免被覆盖
- 每次配置变更后确认

## 常见坑点

见 [gotchas.md](gotchas.md)
