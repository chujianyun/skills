# 更新协议

来源固定为 <https://ai-passport.folotoy.cn/guides/> 的中文教程区。更新不扩展到英文版、社区、工具或开发仓库。

## 抓取与预演

1. 读取首页全部教程卡片，并与 <https://ai-passport.folotoy.cn/sitemap.xml> 中的中文 `/guides/` 条目交叉核对；去重后得到完整页面清单。导航和站点地图不一致时检查新增、遗漏或重定向，不沿用旧的 9 页数量猜测覆盖。
2. 用 `mktemp -d` 创建新的临时目录，写入 `docs/`、`assets/` 和 `inventory.json`。目录页放在 `教程中心/index.md`，教程按页面标题放在该目录同级；更新时优先沿用清单中的已有路径。
3. 只转换页面主正文：详情页读取 `article.article-content`，目录页读取主内容区。排除站点导航、侧边重复目录、页脚和复制按钮；保留步骤标题、`step-*` 锚点、提示、列表和代码块。开发提示词中的输入框必须保留为 `<填写应用需求>` 占位符，不能因它没有文本节点而丢失。
4. 先建立全部页面的 URL → 本地路径映射，再改写教程区内链接。下载正文所需的公开图片到 `assets/guides/`，相同 URL 去重；正文中的相对路径按最终 `references/docs/` 与 `references/assets/` 布局计算。不要抓取设备专属链接、SN、KEY、登录态或临时签名 URL。
5. `inventory.json` 使用 `schema_version: 1`，包含 `source_root`、`coverage`、`pages` 和 `assets`。每页记录 `title`、`source_url`、`source_path`、`local_path`，可加 `summary` 与 `keywords`；每个图片记录 `source_url`、`local_path`。
6. `coverage.discovered == coverage.captured == len(pages)` 且 `failed` 为空才可同步。每页最多重试两次；持续失败、正文为空或必要图片抓取失败时停止，不覆盖旧快照。确实需要部分快照时先取得用户对缺失范围的明确接受。
7. 检查 Python 3.10+ 可用，先预演：

   ```bash
   python3 <skill-root>/scripts/sync_wiki_docs.py \
     --skill-root <skill-root> \
     --staging-dir <staging> \
     --dry-run
   ```

## 写入与完成条件

预演通过后去掉 `--dry-run`。脚本仅写入内容或元数据变化的页面；`UNCHANGED` 表示成功且零文件写入，不为留下检查记录而更新时间戳。

上游删页或改路径时默认停止。只有确认用户已授权后才能加 `--prune`，旧文件将归档到 `references/.baize-trash/`。与本次同步无关的覆盖、外部提交、推送、公开发布和定时任务需要各自适用的授权。

同步后核对页面数、目录、内部链接、图片、清单哈希和 2–3 个代表性检索问题。检查上游范围或许可是否变化，再完成已授权的本地安装副本同步。

安装了 `$baize` 时可用它完成抓取与覆盖核对；没有白泽也可按以上输入结构使用随包同步脚本。没有兼容 Python 时保留旧快照并报告，不手工伪造哈希。
