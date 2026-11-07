# 更新 Dify Wiki

## 范围和依赖

- 规范入口：<https://docs.dify.ai/zh/cloud/use-dify/getting-started/introduction>
- 本快照限定中文 Cloud 顶部「使用」「学习」「开发者资源」。递归读取官方 `/_llms/zh/cloud.txt` 下的索引，包括共享中文教程、CLI、插件开发、API 指南与生成的接口参考。
- 不追加自部署产品、英语/日语、博客、社区或外链整站。范围变更先取得用户授权。
- 需要 Python 3.10+ 和 HTTPS 网络；全部脚本仅依赖标准库，不需要 API 密钥。用 `python3 --version` 验证；缺少兼容 Python 时停止更新并报告，不自行安装依赖。

## 1. 在新临时目录抓取

```bash
dify_stage=$(mktemp -d)
python3 <skill-root>/scripts/capture_docs.py --staging-dir "$dify_stage"
```

脚本先递归盘点全部索引，再与官方源码 `docs.json` 合并导航，并以独立 sitemap 和原始 OpenAPI 核对页面与接口。对索引和 sitemap 都漏列、但源码导航明确列出且正文可访问的页面，保留为导航补入项（初版为 `zh/home`），不静默排除。每页和每个图片资源最多初次请求加两次重试；401、403、429 不自动重试同一 URL。失败时不发布可供同步的 `inventory.json`，保留缓存和失败报告供诊断；修复问题后可用同一未完成临时目录恢复。成功目录不能重复当成新快照，刷新必须重新创建临时目录，避免误用旧缓存。

正文取官方 Markdown 导出，保留代码、标签页、折叠内容、表格和告警，移除重复的文档索引提示；保留原文内容及 AI 翻译提示。内部文档链接映射为本地相对路径，范围外链接保持在线。正文配图本地化；Mintlify CDN 图片映射到 Dify 官方源码中的原图，清单不保留临时签名。保留原始 OpenAPI JSON 和上游 CC BY 4.0 许可。

若站点导航、索引结构、许可或图片域名变化导致脚本失败，先检查官方导航与源码，再修复抓取逻辑；不得把失败页面从范围中静默剔除。大量相同鉴权或限流错误时停止批量操作并报告，不反复启动全量请求。

## 2. 核对覆盖并预演

核对新 `inventory.json` 的 `discovered == captured == len(pages)`、`failed == []`，并抽查首页、API、代码、表格和图片页。页面数可以随官方变动，不固定为初版 332；三个入口都必须覆盖。`capture-report.json` 记录实际数量与 sitemap 交叉核对结果。

```bash
python3 <skill-root>/scripts/sync_wiki_docs.py \
  --skill-root <skill-root> --staging-dir "$dify_stage" --dry-run
```

检查增加、修改、未变、移除的文档与资产。删页或改路径需获得相应授权后才能加 `--prune`；旧文件会归档到 `references/.baize-trash/`。未授权时保留当前快照并报告差异。

## 3. 同步、验证与安装

预演无异常且授权满足后，去掉 `--dry-run` 执行。若返回 `UNCHANGED`，正文、索引和清单不落盘；仅在运行输出报告检查结果。

发生变动时：

1. 按清单核对所有文档与资产 SHA-256、本地文档/图片链接与目录层级。
2. 用使用、学习、CLI、插件、API 各一个代表问题验证搜索并读取匹配文档。
3. 更新 `references/NAVIGATION.json`：使用新 inventory 的 pages、capture-report 的数量和索引列表；它是审计辅助资料，清单仍是来源和哈希的唯一事实来源。
4. 若从源码仓库更新，优先完成仓库校验，再按已有授权同步安装副本；不直接只改安装目录。
5. 只在用户明确要求时配置自动更新，使用当前 Agent 的调度工具；不私自修改系统 cron。

来源和分发许可见 [SOURCE.md](SOURCE.md)，完整许可见 [UPSTREAM-LICENSE.txt](assets/UPSTREAM-LICENSE.txt)。
