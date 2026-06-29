# Onboarding 初始化流程

当 `~/.follow-builders/config.json` 不存在或 `onboardingComplete` 不为 `true` 时执行。

## 阶段1：欢迎介绍

告诉用户：

> "I'm your AI Builders Digest. I track the top builders in AI — researchers, founders, PMs, and engineers who are actually building things — across X/Twitter and YouTube podcasts. Every day (or week), I'll deliver you a curated summary of what they're saying, thinking, and building."
>
> "I currently track [N] builders on X and [M] podcasts. The list is curated and updated centrally — you'll always get the latest sources automatically."

[N] 和 [M] 从 `config/default-sources.json` 中获取实际数量。

## 阶段2：频率设置

提问："How often would you like your digest?"
- Daily（推荐）
- Weekly

然后提问时间和时区。例如："8am, Pacific Time" → `deliveryTime: "08:00"`, `timezone: "America/Los_Angeles"`。Weekly 模式额外询问周几。

## 阶段3：投递方式

**判断平台：`config.platform` 是否为 `openclaw`？**

### OpenClaw 平台

**跳过此阶段。** OpenClaw 已内置消息投递能力。设置 `delivery.method` 为 `"stdout"`。

### 非持久化 Agent（Claude Code、Cursor 等）

告知用户：

> "Since you're not using a persistent agent, I need a way to send you the digest when you're not in this terminal. You have two options:
> 1. **Telegram** — free, ~5 min to set up
> 2. **Email** — requires a free Resend account
> Or skip and just type /ai whenever you want."

**Telegram 配置引导**：
1. 打开 Telegram 搜索 @BotFather
2. 发送 `/newbot`，设置名称和用户名（以 bot 结尾）
3. 获取 token（如 `7123456789:AAH...`）
4. **关键**：用户必须先向 Bot 发送任意消息（如 "hi"）
5. 获取 chat ID：`curl -s "https://api.telegram.org/bot<TOKEN>/getUpdates" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['result'][0]['message']['chat']['id'])"`
6. 保存到 config

**Email 配置引导**：
1. 询问邮箱地址
2. 引导注册 Resend（https://resend.com，免费 100 封/天）
3. 获取 API key 并保存到 `~/.follow-builders/.env`

**On-demand 模式**：设置 `delivery.method` 为 `"stdout"`，不配置任何投递。

## 阶段4：语言选择

提问："What language do you prefer for your digest?"
- English
- Chinese（从英文翻译）
- Bilingual（段落交错中英对照）

## 阶段5：API Key 设置

- `stdout` 投递 → 不需要任何 key
- Telegram/Email → 仅需对应投递 key

创建 `~/.follow-builders/.env` 文件，只反注释需要的行。

## 阶段6：展示来源

从 `config/default-sources.json` 读取并展示完整列表。

## 阶段7：配置提醒

> "All your settings can be changed anytime through conversation. No need to edit files."

## 阶段8：设置 Cron

### OpenClaw 平台

**步骤1 — 获取目标 ID**：询问用户"Should I deliver to this same chat?"，确认后获取 channel 名称和 target ID。对照表：

| Channel | Target 格式 | 获取方式 |
|---------|------------|---------|
| Telegram | 数字 chat ID（如 `123456789`） | `openclaw logs --follow` 或 API getUpdates |
| Feishu | open_id（如 `ou_e67...`） | `openclaw pairing list feishu` |
| Discord | `user:<id>` 或 `channel:<id>` | 开启 Developer Mode 右键复制 |
| Slack | `channel:<id>`（如 `channel:C123`） | 右键频道链接提取 |
| WhatsApp | 带国家码手机号（如 `+15551234567`） | 用户提供 |

**步骤2 — 创建 Cron**：**禁止 `--channel last`**。必须显式指定 channel 和 target：

```bash
openclaw cron add \
  --name "AI Builders Digest" \
  --cron "<cron expression>" \
  --tz "<user IANA timezone>" \
  --session isolated \
  --message "Run the follow-builders skill: execute prepare-digest.js, remix the content into a digest following the prompts, then deliver via deliver.js" \
  --announce \
  --channel <channel name> \
  --to "<target ID>" \
  --exact
```

**步骤3 — 验证**：
```bash
openclaw cron list
openclaw cron run <jobId>
```
确认用户收到测试 digest 后再继续。

常见错误：
- "Channel is required" → 未使用 `--exact` 或未指定 channel
- "Delivering to X requires target" → 忘记 `--to`
- "No agent" → 添加 `--agent <agent-id>`

### 非持久化 Agent

- **Telegram/Email 投递**：使用系统 crontab（非 Agent cron），直接运行脚本管道
- **On-demand 模式**：跳过 cron

## 阶段9：欢迎 Digest

**不可跳过。** 立即运行 [delivery.md](delivery.md) 生成并发送首个 digest。

发送后询问：
- 长度是否合适？
- 是否有特别关注/减少的内容？

根据反馈调整 prompt 文件。

结束语：
- OpenClaw / Telegram / Email：下一份 digest 将在 [时间] 自动送达
- On-demand：随时输入 /ai 获取下一份
