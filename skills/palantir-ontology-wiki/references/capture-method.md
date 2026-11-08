# 抓取与覆盖核对

## 范围与发现

入口为 <https://www.palantir.com/docs/zh/foundry/ontology/overview/>。使用官方页面 `__NEXT_DATA__.props.pageProps.sidebarNavProps.items`，递归遍历 `section.items` 与 `pageGroup.pages`，以 `header` 保持上级分组；不是从搜索引擎或正文外链猜测范围。

| 导航部分 | 文档数 |
|---|---:|
| 顶层概览 | 5 |
| 定义本体 | 133 |
| 应用 | 159 |
| 本体架构 | 19 |
| 合计 | 316 |

316 个中文页面 URL 唯一，全部存在于官方 <https://www.palantir.com/docs/sitemap.xml>。HTML 的 canonical 字段可能指向英文页，因此保留实际中文导航 URL，不将两种语言合并。

## 正文与路径

直接提取官方 `pageProps.markdown`，保留标题、表格、代码语言、标签页、折叠块和 `:::callout` 告警；不从网页可见文本重建正文。少数页面将标题放在 Markdown 之外，因此补上对应导航标题。保留原始中英文导航分组，标题中的文件系统不安全字符替换为 `-`；内部文档链接改为本地相对路径并编码空格和中文。

代码围栏内部不改写链接；只执行白泽契约要求的 Unicode NFC、换行和行尾空白规范化。文档 URL、路径、摘要、关键词和 SHA-256 均在 `wiki-manifest.json` 中。

## 配图

合并 `docAssetMetadata`、Markdown 图片、HTML 图片标签与实际网页渲染的 `img.src`，忽略尺寸 query 后得到 1,009 个唯一资源地址。渲染地址是语言资源解析的校验依据；11 张图片实际位于 `/docs/resources/zh/`，不能仅靠英文资源路径推算。

944 张资源有效，下载原始 PNG、JPG、GIF、SVG 至 `references/assets/`，保留目录和本地链接。65 个官方地址重试后仍返回 HTML 错误页；未将这些 HTML 文件伪装成图片，也未使用其他版本图片替代。在原位置保留标注后的在线链接，并在页尾列出失效地址。逐地址结果见 [抓取报告](capture-report.json)。

`wiki-manifest.json` 的 `coverage` 计算导航文档覆盖率；资源完整性单独由抓取报告的 `media_complete` 与 `missing_assets` 表示。不得将正文覆盖 100% 描述为图文全部完整。

## 重现

`scripts/capture_wiki.py` 只依赖 Python 3.10+ 标准库。每次刷新使用新的 `mktemp -d` 目录；缓存只用于同一次抓取的恢复，不能用于冒充在线更新。默认遇到缺页、空正文、站点地图不一致或缺图即退出。

本次用户明确接受缺图后使用了 `--allow-missing-assets`。未来出现新的缺图时仍应先报告，不能把当前接受视作无限授权。此脚本只生成 staging；不会提交、推送、安装或修改旧 Skill。
