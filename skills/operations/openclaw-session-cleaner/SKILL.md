---
name: openclaw-session-cleaner
description: OpenClaw session 清理助手。用于用户提到清理 OpenClaw sessions、删除旧 cron session、压缩或重建 sessions.json、排查 session 文件膨胀时使用。触发后优先检查 ~/.openclaw/agents/main/sessions/ 下的 session 文件数量和 sessions.json 大小，并按指令执行清理。
---

# OpenClaw Session Cleaner

当用户要求清理 OpenClaw session、删除旧的 cron session 文件、缩小 `sessions.json`、或重建 session 索引时，执行下面这段操作：

Check how many session files are in `~/.openclaw/agents/main/sessions/` and how big `sessions.json` is. If there are thousands of old cron session files bloating it, delete all the old `.jsonl` files except the main session, then rebuild `sessions.json` to only reference sessions that still exist on disk.

## 使用要求

- 默认操作目标是 `~/.openclaw/agents/main/sessions/`
- 在执行前先检查当前 session 文件数量和 `sessions.json` 大小
- 由 OpenClaw 自行判断哪些属于应清理的旧 cron session
- 保留 main session，不要误删主会话
- 清理完成后，确保 `sessions.json` 只引用磁盘上仍然存在的 session 文件
- 向用户汇报清理前后的数量变化，以及是否已完成重建
