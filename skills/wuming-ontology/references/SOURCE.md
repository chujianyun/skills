# 来源与范围

- Skill：wuming-ontology
- 核心知识来源：[Palantir Foundry Ontology 官方文档](https://www.palantir.com/docs/foundry/ontology/overview)
- 离线 Wiki：Palantir Ontology
- 当前中文快照来源：<https://www.palantir.com/docs/zh/foundry/ontology/overview>
- 语言 / 版本：简体中文；官网机器翻译，准确性未经官方验证；未标注固定软件版本
- 抓取范围：用户提供页面所属的 Ontology 中文侧栏全部 316 篇文档：概览 5、定义本体 133、应用 159、本体架构 19；正文覆盖 100%，配图仅 944/1009，65 个官方失效图片地址已获用户接受并逐处标注；不含其他语言、整个 Foundry 文档站或独立 API Reference。
- 当前快照：正文完整，配图不完整（用户已明确接受）；正文 316/316，配图 944/1009，65 个官方失效地址均已标注。`wiki-manifest.json` 中 coverage.complete 仅表示导航文档覆盖完整，不表示全部配图可用。
- 上游许可：Palantir Technologies Inc. 保留上游文档、图片和商标的权利。未发现允许全文再分发的开放许可证；仓库所有者已明确授权把本快照收录进本公开集合仓库并承担相应风险；上游材料不随本仓库的 CC BY-NC-SA 许可证重新授权，转用时须保留 Palantir 署名与原始来源链接。

离线快照可能落后于上游。上游权利状态不因本次收录而改变；若 Palantir 提出移除或停止分发要求，应下架相关正文与配图。

技能名称与文档来源分开：`wuming-ontology` 是本 Skill 的名称；`wiki-manifest.json` 的 `wiki.source_root` 和逐页来源仍保留实际抓取的中文地址。英文核心来源可用于规范核对，不表示已经完整抓取其当前内容。OWL 映射、示例本体、生成脚本与 HTML 查看器是本 Skill 的扩展，不属于抓取的官方正文。

## 核对与许可边界

本次抓取与核对完成于 2026-10-31（Asia/Shanghai）。导航 316 篇全部能在官方 sitemap.xml 中核对；另以网页实际渲染的图片 src 独立核对 1,009 个资源地址，其中 11 张使用 `/docs/resources/zh/` 中文资源目录。抓取方法见 [抓取与覆盖核对](capture-method.md)，有效资源数量、失效地址及错误见 [机器可读抓取报告](capture-report.json)。

65 个失效图片地址返回的是 HTML 错误页，即使 HTTP 状态为 200 也未当成图片保存。受影响页面在图片位置标注“官方图片已失效”，末尾列出原地址；未用其他版本图片替换。用户已接受此次正文完整、配图不完整的快照；这不代表允许未来更新自动接受新的缺页或缺图。

正文保留官网关于机器翻译未经验证的告警。官网未标注固定发布版本；遇到中文译名、代码与英文官方说明不一致时，分别注明证据，不推断哪份材料最新。YouTube、博客及范围外的文档链接保留为在线外链，不属于离线覆盖范围。

本 Skill 非 Palantir 官方发布或背书。离线 Wiki 正文与配图来自公开官方页面，未使用账号、Cookie 或业务数据，未执行任何 Foundry 产品操作。上游权利仍归 Palantir 所有；本公开收录已获仓库所有者明确授权，不代表上游改为开放许可。
