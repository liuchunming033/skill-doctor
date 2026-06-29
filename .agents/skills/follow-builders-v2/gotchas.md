# Gotchas —— follow-builders 踩坑记录

## 坑点1：OpenClaw Cron 使用 --channel last 失败

**现象**：`openclaw cron add --channel last` 创建定时任务，运行时报错 "Channel is required when multiple channels are configured"

**问题**：Cron 在隔离 session 中运行，没有"last channel"的上下文。用户配置了多个 channel（如 telegram + feishu），隔离环境不知道 last 是哪个。

**解决**：总是显式指定 `--channel <name> --to "<id>" --exact`。具体 ID 获取方式见 SKILL.md 中的 channel-target 对照表。

---

## 坑点2：Telegram Bot 未收到消息导致 getUpdates 为空

**现象**：用户创建了 Telegram Bot，配置了 token，但 `deliver.js` 发消息时报错 "chat not found"

**问题**：Telegram Bot 在用户主动发送第一条消息之前，无法向用户推送消息。getUpdates API 返回空数组。

**解决**：在 onboarding 中明确引导用户：获取 token 后，必须先打开 Bot 聊天窗口发送任意消息（如 "hi"），然后再运行 getUpdates 获取 chat ID。

---

## 坑点3：prepare-digest.js 返回空 JSON

**现象**：`node prepare-digest.js` 输出为 `null` 或空对象，Agent 没有数据可处理

**问题**：网络不通或中心 Feed 服务器不可达时，脚本静默失败。

**解决**：检查 `stats.podcastEpisodes === 0 && stats.xBuilders === 0`，向用户提示"No new updates"而非静默。如果是网络问题，提示用户检查网络连接。

---

## 坑点4：Node.js 未安装导致脚本无法执行

**现象**：`node: command not found`

**问题**：follow-builders 的核心脚本（prepare-digest.js、deliver.js）依赖 Node.js。

**解决**：Onboarding 时检测 `which node`，如未安装引导用户安装：`brew install node`（macOS）或 `apt install nodejs`（Linux）。

---

## 坑点5：Bilingual 模式段落交错混乱

**现象**：英中双语模式下，输出全部英文后再全部中文，或交错位置错乱

**问题**：Agent 没有严格按"paragraph by paragraph"交错处理。

**解决**：严格遵循流程：每个 builder 的推文摘要 → 英文一段 + 中文一段（紧接下方），再处理下一个 builder。不要先输出所有英文再输出所有中文。

---

## 坑点6：Agent 自行访问 x.com 或搜索网页

**现象**：Agent 看到 tweet URL 后尝试用 WebFetch 访问，或搜索 builder 背景信息

**问题**：浪费 token 和时间，且可能触发反爬。所有内容已在 prepare-digest.js 输出的 JSON 中。

**解决**：在 SKILL.md 中设置"绝对规则"：只用 JSON 中的数据，不访问外部 URL，不搜索网页。每次 delivery 流程开始时重申此规则。

---

## 坑点7：用户 Prompt 自定义被中心更新覆盖

**现象**：用户自定义了 prompt 文件（如 shorter summaries），skill 更新后自定义丢失

**问题**：中心 Feed 更新时，如果直接修改 `prompts/` 目录下的文件会被覆盖。

**解决**：用户自定义 prompt 必须复制到 `~/.follow-builders/prompts/` 目录，这个目录不会被中心更新覆盖。Agent 读取 prompt 时优先读取 `~/.follow-builders/prompts/`。
