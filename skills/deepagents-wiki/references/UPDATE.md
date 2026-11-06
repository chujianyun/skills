# 更新协议

规范来源：<https://docs.langchain.com/oss/python/deepagents>

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

## Deep Agents 来源发现与目录规则

1. 抓取 `https://docs.langchain.com/llms.txt` 并沿索引找到 Python 文档索引；同时抓取 `https://docs.langchain.com/sitemap.xml`、Deep Agents overview 的在线导航，以及 `https://raw.githubusercontent.com/langchain-ai/docs/main/src/docs.json`。
2. 选取包含 `oss/python/deepagents/overview` 的 Deep Agents tab，以及 Python Examples 中的 Deep Agents group。递归展开 `pages` 和带正文的 `root`；与 sitemap 中的 `/oss/python/deepagents/` 路径合并去重。参考 `NAVIGATION.json` 中保存的分组、旧入口和规范来源，但必须重新盘点，不能固定为 44 页。
3. 优先请求官方页面的 `.md` 导出。跟随重定向；若旧 `.md` 路径最终返回 HTML，则为规范目标补上 `.md` 再抓取。按最终规范 URL 去重。范围外的目标只抓导航直接引用的那一页，不递归展开整个 LangSmith、OpenWiki 或 LangChain 子站。
4. 目录沿用导航分组与现有文档映射，分组有正文时使用 `index.md`。保留全部代码、标签页、折叠区和表格。移除文首的 Documentation Index 提示；只在代码围栏之外改写链接，按规范 URL 与旧入口的完整映射将范围内链接改为本地相对路径。
5. 在生成哈希前，将明确以 `your-`、`your_` 或尖括号形式表示的 API 密钥占位符统一为 `<API_KEY>`。只处理已确认的示例占位符；发现疑似真实凭据时停止并报告位置，不回显原值。
6. 正文配图优先定位到官方 `langchain-ai/docs` 仓库的 `src/` 文件，使用当次固定提交下载到 `assets/images/`，避免保存 CDN 查询签名；同一图片去重。保留上游 MIT 许可。
7. 在执行本页前面的 dry-run/sync 后，按实际盘点同步 `NAVIGATION.json` 和 `SOURCE.md` 的覆盖数、目录映射和来源证据。若语料、来源与映射均未变化，这些说明文件也不得重写。
8. 运行本地全文检索至少验证 `create_deep_agent`、`CompositeBackend`、`interrupt_on`；检查所有本地图片与 Markdown 链接实际存在，再按所在仓库的注册、提交与安装规则收尾。
