# 更新协议

规范来源：<https://www.palantir.com/docs/zh/foundry/ontology/overview>

1. 重新盘点来源范围内的完整导航，不沿用旧页面数量猜测新范围。此 Skill 自带官方页面抓取器：

   ```bash
   staging=$(mktemp -d)
   python3 <skill-root>/scripts/capture_wiki.py --staging-dir "$staging"
   ```

   只依赖 Python 3.10+ 标准库，最多 8 个抓取线程。必须使用全新 staging 进行后续更新，不能复用上次缓存充当最新资料。遇到失效配图时先读错误与 `missing-assets.json`；只有用户明确接受该次缺图范围，才在同一 staging 加 `--allow-missing-assets` 继续。
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
7. 由新的 `capture-report.json` 核对配图是否完整。语料同步成功后，比较并按需更新 `references/capture-report.json`、`SOURCE.md` 和 `capture-method.md` 的范围与已知缺图说明；不要为了检查时间或下载顺序重写相同报告。`wiki-manifest.json` 的 `coverage` 仅统计文档，不能替代图片完整性报告。
8. `UNCHANGED` 表示语料与元数据均未变化；完整无变化检查不得改写任何正文、索引、清单、来源说明或报告。`CHANGED` 后重新验证本地搜索和安装副本。

若当前 Agent 安装了 `$baize`，优先用它完成抓取、覆盖率核对、位置判断和自动化配置。没有可用调度器时不要私自修改系统 cron。
