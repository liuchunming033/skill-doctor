# 配置处理

用户通过对话修改设置时的处理规则。

## 来源变更

来源列表集中管理，用户不可修改。用户请求添加/删除来源时回复：
> "The source list is curated centrally and updates automatically. If you'd like to suggest a source, open an issue at https://github.com/zarazhangrui/follow-builders."

## 频率/时间变更

- "Switch to weekly/daily" → 更新 `frequency` 并更新 cron
- "Change time to X" → 更新 `deliveryTime` 并更新 cron
- "Change timezone to X" → 更新 `timezone` 并更新 cron

**Cron 更新方式**：
- OpenClaw：`openclaw cron list` → 找到 job ID → `openclaw cron remove <id>` → 重新 `openclaw cron add`
- 系统 crontab：`crontab -l` → 编辑 → `crontab -e`

## 语言变更

- "Switch to Chinese/English/bilingual" → 更新 `language` 字段

## 投递变更

- "Switch to Telegram/email" → 更新 `delivery.method`，引导用户完成新渠道配置
- "Change my email" → 更新 `delivery.email`
- "Send to this chat instead" → 设置 `delivery.method` 为 `stdout`

## Prompt 自定义

用户想自定义摘要风格时：
1. 复制 prompt 文件到 `~/.follow-builders/prompts/`（此目录不会被中心更新覆盖）
2. 按用户要求编辑

```bash
mkdir -p ~/.follow-builders/prompts
cp ${CLAUDE_SKILL_DIR}/prompts/<filename>.md ~/.follow-builders/prompts/<filename>.md
```

- "Make summaries shorter/longer" → 编辑 `summarize-podcast.md` 或 `summarize-tweets.md`
- "Focus more on [X]" → 编辑对应 prompt
- "Change the tone to [X]" → 编辑对应 prompt
- "Reset to default" → 删除 `~/.follow-builders/prompts/<filename>.md`

Agent 读取 prompt 时优先读取 `~/.follow-builders/prompts/`，不存在时 fallback 到 `prompts/`。

## 信息查询

- "Show my settings" → 读取 config.json 友好展示
- "Show my sources" → 读取 config + defaults 列出来源
- "Show my prompts" → 读取并展示当前生效的 prompt 文件

每次配置变更后确认修改内容。
