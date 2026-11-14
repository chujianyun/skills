# 更新协议

规范来源：<https://docs.langchain.com/langsmith>

1. 重新盘点来源范围内的完整导航，不沿用旧页面数量猜测新范围。
2. 使用新临时目录抓取完整语料（不会直接修改 Skill）：

   ```bash
   staging_dir=$(mktemp -d)
   python3 <skill-root>/scripts/capture_langsmith.py --staging-dir "$staging_dir" --workers 8
   ```

   脚本合并公开导航、递归 llms 索引和 sitemap；生成 `docs/`、`assets/`、`inventory.json`、`capture-report.json`。缓存仅在临时目录。页面或资源失败时停止，先排查；单个请求最多尝试三次，禁止绕过鉴权。
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

同步成功后核对新 `capture-report.json` 的 Evaluation 导航覆盖，并复制到 `references/capture-report.json`；内容相同时不要重写报告。上游许可证仍需保留。没有内容变化时不改 SOURCE 中的统计；有变化时同步其计数和 SKILL 快照边界。
