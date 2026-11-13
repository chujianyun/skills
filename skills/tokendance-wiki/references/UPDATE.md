# 更新协议

规范来源：<https://tokendance.space/docs>

1. 重新盘点来源范围内的完整导航，不沿用旧页面数量猜测新范围。
2. 用 `mktemp -d` 创建空临时目录，运行随包提供的采集器（Python 3.10+ 标准库；需要 HTTPS 网络）：

   ```bash
   python3 <skill-root>/scripts/capture_docs.py --staging-dir <empty-staging>
   ```

   采集器读取官方索引、完整导出、当前浏览器公开注册表，三方一致才抓全部页面及 Markdown/HTML 图片；按导航建目录并改写内部链接。网络可通过标准 `HTTPS_PROXY` 环境变量配置，不将本机代理或凭据写入 Skill。输出 `docs/`、`assets/`、`inventory.json`。目标目录非空、导航不一致、正文为空、未知图片域名或重试两次仍失败则停止；保留当前安装和仓库版本，检查上游后换新临时目录重试，不降低覆盖门槛。

   若站点结构变化导致脚本失效，可按上述官方来源重新完整盘点、转换；先修复本 Skill 中的采集器再同步。
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
