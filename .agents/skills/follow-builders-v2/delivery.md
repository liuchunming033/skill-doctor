# 内容交付流程

Cron 触发或用户 `/ai` 时执行。

## 阶段1：加载配置

读取 `~/.follow-builders/config.json`。

## 阶段2：运行 prepare 脚本

Agent 不 fetch 任何内容。一切数据由脚本提供：

```bash
cd ${CLAUDE_SKILL_DIR}/scripts && node prepare-digest.js 2>/dev/null
```

JSON 输出包含：
- `config` — 语言和投递偏好
- `podcasts` — 播客片段 + 完整逐字稿
- `x` — builders 的推文（text、URL、bio）
- `prompts` — remix 指令
- `stats` — 数据统计
- `errors` — 非致命错误（忽略）

脚本完全失败（无 JSON 输出）→ 提示用户检查网络。

## 阶段3：空内容检查

`stats.podcastEpisodes === 0 AND stats.xBuilders === 0` → 回复"No new updates today. Check back tomorrow!" 然后停止。

## 阶段4：Remix 内容

Agent 唯一职责：remix JSON 中的内容。不访问任何 URL，不调任何 API。

从 JSON 的 `prompts` 字段读取指令：
- `prompts.digest_intro` — 整体框架
- `prompts.summarize_podcast` — 播客 remix 规则
- `prompts.summarize_tweets` — 推文 remix 规则
- `prompts.translate` — 中文翻译规则

**推文处理**（先处理）：
1. 用 `bio` 字段获取角色（如 bio: "ceo @box" → "Box CEO Aaron Levie"）
2. 按 `prompts.summarize_tweets` 摘要
3. 每条必须包含 JSON 中的 `url`

**播客处理**（后处理）：
1. `podcasts` 数组最多 1 个 episode
2. 按 `prompts.summarize_podcast` 摘要 `transcript`
3. 使用 JSON 中的 `name`、`title`、`url`（非 transcript 中的）

按 `prompts.digest_intro` 组装。

**绝对规则**：
- 不发明内容，只用 JSON 数据
- 每条内容含 URL，无 URL 不收录
- 不猜测职位，用 `bio` 字段或只用姓名
- 不访问 x.com、不搜索网页、不调 API

## 阶段5：语言处理

根据 `config.language`：

- **en**：全英文
- **zh**：全中文，按 `prompts.translate`
- **bilingual**：段落交错中英对照。每个 builder → 英文 + 中文（紧跟），再下一个 builder。播客 → 英文摘要 + 中文翻译

不要先输出全部英文再全部中文。

## 阶段6：投递

根据 `config.delivery.method`：

- **stdout**：直接输出
- **telegram / email**：
```bash
echo '<digest text>' > /tmp/fb-digest.txt
cd ${CLAUDE_SKILL_DIR}/scripts && node deliver.js --file /tmp/fb-digest.txt 2>/dev/null
```
投递失败时 fallback：在终端显示内容。

## 手动触发（/ai）

跳过 cron 检查，直接运行阶段1-6。
