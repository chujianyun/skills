# 更新协议

规范来源：<https://docs.langchain.com/oss/python/langgraph>

1. 重新盘点来源范围内的完整导航，不沿用旧页面数量猜测新范围。
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

## LangGraph 完整抓取入口

先建立一个新的临时目录，然后运行随包提供的抓取器：

```bash
staging_dir="$(mktemp -d)"
python3 <skill-root>/scripts/capture_langgraph.py --staging-dir "$staging_dir"
python3 <skill-root>/scripts/sync_wiki_docs.py --skill-root <skill-root> --staging-dir "$staging_dir" --dry-run
```

核对预演通过后，使用同一 staging 去掉 `--dry-run` 执行同步。不要在已安装副本里直接更新；位于受治理仓库时先修改仓库版本，再按仓库要求提交、推送、安装。

抓取器只依赖 Python 3.10+ 标准库；合并 Python LangGraph 导航、`llms` Python 索引、站点地图及官方源码目录，额外纳入源码中的错误页。保留主导航原分组；从 Learn 导航或源码补充的教程、案例、错误页分别放在 `Learn/`、`Reference/Errors/`。新版新增且无法映射分组的页面会停止抓取，须先审查归属。

对旧 Changelog / Studio 地址跟随官方重定向，并重新请求目标的 `.md`，拒绝把 HTML 当 Markdown。内部链接映射为本地相对路径；配图从不带签名参数的官方源码地址下载。任何正文或配图抓取失败都不构建 inventory，不覆盖当前快照。

抓取完成会生成 `capture-report.json`；有实际变化时核对它，并更新 `references/capture-report.json` 和来源范围。仅上游源码树 SHA 改变而本 Skill 范围的正文、元数据、资产未变时，保持核对记录不变，避免无关更新。上游 MIT 许可保留在 `references/LICENSE.langchain.txt`。不要创建定时更新任务，除非用户明确要求。
