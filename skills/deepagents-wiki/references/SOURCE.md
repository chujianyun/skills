# 来源与范围

- Wiki：Deep Agents
- 规范来源：<https://docs.langchain.com/oss/python/deepagents>
- 语言 / 版本：英文官方文档；Python SDK 当前在线版本；中文检索与回答入口
- 抓取范围：Python Deep Agents 全部导航页面与 4 个 Python 实战示例，合并官方 llms 索引、sitemap 和 docs.json 去重；包含导航直接引用的中间件、部署、OpenWiki、MCP、A2A 和更新日志入口，共 44 页。TypeScript SDK、Deep Agents Code、独立 API Reference 及链接目标子站的递归扩展不在范围内。
- 当前快照：完整；精确覆盖数与最近一次有变化的同步时间见 `wiki-manifest.json`
- 上游许可：MIT License，Copyright (c) 2025 LangChain；上游 https://github.com/langchain-ai/docs/blob/main/LICENSE，完整许可见 references/UPSTREAM-LICENSE.txt。正文使用官方 Markdown，配图来自官方源码的固定提交。

离线快照可能落后于上游。许可证不明或不允许再分发时，本 Skill 仅限用户授权的本地使用，不应提交到公开仓库或发布到市场。

## 盘点与转换证据

- 快照范围：2026-11-07 盘点的官方 Python Deep Agents 导航 40 页，以及 Examples → Deep Agents 的 4 篇实战文档。
- 使用官方 `llms.txt` 的 Python 索引、站点地图、在线导航和源码 `src/docs.json` 合并去重。站点地图列出 36 个 Python Deep Agents 路径；导航另有 8 个直接引用或重定向目标，合计 44 个规范页面，抓取失败数为 0。
- [导航映射](NAVIGATION.json) 保存原导航入口、分组、重定向后的规范 URL 和本地路径；文档内容与配图哈希见 `wiki-manifest.json`。完整性仅指这里声明的范围，不包括所有外链的递归抓取。
- 旧入口 `changelog-py` → Python releases changelog；`openwiki` → OpenWiki overview；`mcp` → LangChain MCP；`a2a` → Agent Server A2A。更新日志保留官方页面的整个正文，可能包含其他 Python 包的变动。Managed Deep Agents 只包含导航直接引用的概览页。
- 474 个范围内文档链接已改写为本地相对路径；范围外链接继续指向官方在线文档。20 张信息配图本地保存，来源固定到上游源码提交，完整许可见 [上游 MIT 许可证](UPSTREAM-LICENSE.txt)。
- 代码、标签页、折叠内容、表格和告警由官方 Markdown 导出展开保存。前端集成章节中的 JavaScript/TypeScript 示例是 Python SDK 配套前端代码，按原文保留。
- 文档正文为英文，Skill 使用中文引导检索与回答；这不是中文译本，也不固定到某个已发布 SDK 版本。

## 公开分发转换

为兼容仓库的敏感信息检查，6 篇文档中的 34 个 API 密钥示例占位符统一写作 `<API_KEY>`；未包含真实密钥。文档语义、参数名和命令结构保留原样，转换后的正文哈希由同步脚本生成。
