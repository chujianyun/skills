# 更新协议

规范来源：<https://docs.langchain.com/oss/python/langchain/overview>

1. 完整阅读 [抓取与覆盖核对](capture-method.md)，保持 LangChain Python 范围。使用新的临时目录与 HTTP 缓存运行：

   ```bash
   staging="$(mktemp -d)"
   python3 <skill-root>/scripts/capture_docs.py --staging-dir "$staging" --cache-dir "$staging/http-cache"
   ```

   抓取器自动重新盘点官方源码、Python 导航与站点地图。检查退出码为 0，`capture-report.json` 中失败为空，`inventory.json` 存在；不要复用上次更新的缓存，也不要在抓取不完整时构建。
2. 使用 `mktemp -d` 创建 staging，写入 `docs/`、可选 `assets/` 和 `inventory.json`。
3. `inventory.json` 使用 `schema_version: 1`，包含 `source_root`、`coverage`、`pages` 和可选 `assets`。每个 page 记录 `title`、`source_url`、`source_path`、`local_path`，可选 `summary` 与 `keywords`。
4. `coverage.discovered` 必须等于成功页数加失败页数，`coverage.captured` 必须等于 pages 数量。失败列表非空时默认停止。
5. 先预演：

   ```bash
   python3 <skill-root>/scripts/sync_wiki_docs.py \
     --skill-root <skill-root> \
     --staging-dir <staging> \
     --dry-run
   ```

6. 预演完整且没有未授权删页后去掉 `--dry-run`。上游删页或改路径时，只有获得授权才加 `--prune`；旧文件会移到 `references/.baize-trash/`。
7. `UNCHANGED` 表示成功且零文件写入。`CHANGED` 后重新验证本地搜索和安装副本。

若当前 Agent 安装了 `$baize`，优先用它完成抓取、覆盖率核对、位置判断和自动化配置。没有可用调度器时不要私自修改系统 cron。

## 同步后的核对

- 有变化时同步更新 `references/discovery.json`（来自 staging 中的同名文件），并检查 `capture-method.md` 对范围与别名的解释是否仍成立；文档、图片、来源与元数据均未变化时不复制审计文件或改写说明。
- 不把临时 `http-cache`、失败快照或原始 HTML 安装进 Skill。
- 用代表性检索检查 `create_agent`、`MCPAdapter`、`human-in-the-loop`，并核对正文及图片哈希、本地链接和安装副本。
- 若上游导航、源码路径或官方 Markdown 格式变化导致脚本失败，先修复抓取器并重新生成完整 staging；不得把失败页面列为范围外以绕过完整性门槛。
