---
name: will-codex-quota-reset
description: 查询 willcodexquotareset.com 的 Codex 配额重置预测，返回 forecast 中的重置概率（score 百分比）、距上次重置的天数与小时数、最近重置时间、是否已宣布重置和评分构成。当用户询问 Codex quota 是否会重置、重置概率、上次重置多久、Will Codex Quota Reset 网站预测或要求调用 /api/forecast 时使用；不用于查询用户个人账户的实际用量或官方配额余额。
---

# Will Codex Quota Reset

通过只读公开接口获取预测，并把庞大的响应裁剪为可读的关键信息。

## 工作流

1. 运行：

   ```bash
   python3 scripts/fetch_forecast.py
   ```

2. 读取输出中的 `forecast`，至少向用户报告：
   - `score`：重置概率，数值本身就是百分比，例如 `3` 表示 `3%`
   - `daysSinceReset`：距上次确认重置的天数
   - `hoursSinceReset`：距上次确认重置的小时数
   - `latestResetAt`：最近一次确认重置时间
   - `resetAnnounced`：当前是否存在已宣布的重置信号

3. 按以下格式简洁回答：

   ```text
   Codex 配额重置概率：{score}%
   距上次重置：{daysSinceReset} 天（约 {hoursSinceReset} 小时）
   最近重置时间：{latestResetAt}
   已宣布重置：是/否
   评分依据：{breakdown}
   数据抓取时间：{fetchedAt}
   ```

4. 对 `hoursSinceReset` 最多保留两位小数。保留接口时间的 ISO 8601 原值；仅在用户要求时换算到本地时区。
5. 任一可选字段为 `null` 时回答“暂无数据”，不要把 `null` 当成 `0`；`score` 或两个时长字段缺失时按脚本错误停止。

## 可选操作

- 用户明确要求完整接口数据时，运行 `python3 scripts/fetch_forecast.py --raw`。
- 下游程序需要单行 JSON 时，添加 `--compact`。
- 网络环境不稳定时，用 `--retries N` 调整网络错误后的重试次数；默认重试一次。

## Gotchas

- 这是第三方预测，不是 OpenAI 官方承诺，也不是用户账户的实际配额状态。回答中称为“预测概率”，不要称为“官方重置概率”。
- 不要发送浏览器的 ETag、Cookie、`sec-*` 或完整指纹请求头；接口只需要公开的 `Accept`、`Referer` 和普通 `User-Agent`。
- 网络失败、HTTP 非 2xx、JSON 无效或关键字段缺失时，直接报告脚本错误；不要猜测概率或沿用旧结果。
- 运行依赖只有 Python 3 标准库和可访问的 HTTPS 接口。若 `python3 --version` 失败或网络不可达，说明缺失条件并停止，不要临时安装第三方包。
- `daysSinceReset` 与 `hoursSinceReset` 都描述距同一次最近重置的时间，只是单位不同，不要把 `hoursSinceReset` 误写成“距上次充值”。
