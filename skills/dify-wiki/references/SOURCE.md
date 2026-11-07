# 来源与范围

- 快照日期：2026-11-07；规范入口：<https://docs.dify.ai/zh/cloud/use-dify/getting-started/introduction>。
- 语言与产品：中文 Cloud 当前在线文档，含共享的中文学习、CLI、插件与 API 文档；不是固定发行版。
- 范围：顶部「使用」108 篇、「学习」17 篇、「开发者资源」207 篇，共 **332 篇**。开发者资源包括 CLI 13 篇、插件开发 39 篇、API 155 篇（指南 13 篇与生成接口 142 篇）。
- 不含：自部署产品的独立「部署」文档及其他产品专属差异、其他语言、博客和社区外链的递归扩展。范围外链接保留在线地址。
- 覆盖状态：完整覆盖上述导航范围，抓取失败 0；逐页来源、路径、哈希及最近有变化的同步时间见 [wiki-manifest.json](wiki-manifest.json)。

## 完整性证据

1. 从 <https://docs.dify.ai/llms.txt> 递归读取中文 Cloud、开发者资源和 API 三份官方索引，共 331 篇。
2. 与 [官方 docs.json 导航](https://github.com/langgenius/dify-docs/blob/main/docs.json) 交叉核对：190 个直接文档路径和 142 个生成 API 操作，共 332 篇。
3. 索引与 [sitemap](https://docs.dify.ai/sitemap.xml) 均未列出可访问的 [Dify 文档概览](https://docs.dify.ai/zh/home)，本快照按源码导航补入，未将它误当作重定向或漏页排除。
4. 331 篇与 sitemap 对应，另 1 篇来自上述导航补入；142 个生成 API 端点均与导航及原始 OpenAPI 的 method/path 一致。
5. [NAVIGATION.json](NAVIGATION.json) 保存全部导航分组、映射与交叉核对数量；索引和清单均包含全部 332 篇。

## 内容和离线边界

- 正文使用官方 Markdown 导出，保留表格、代码语言、步骤、告警以及展开的标签页/折叠块；仅移除文档索引提示和 Mintlify 平台页脚。
- 内部文档链接重写为本地相对路径；代码块及行内代码保持原样，示例 URL 不作为真实待下载资源。
- 510 个正文图片/媒体资源本地保存，另保留原始 [OpenAPI JSON](assets/openapi_service.json) 和上游许可，共 512 个清单资产。原图来自文档所引用的公开域名；Mintlify CDN 图片改从 Dify 官方源码获取，不保留临时签名参数。
- 文档中的外部交互式应用、示例站点和范围外资源仍需联网；不承诺离线运行 Dify 或外部服务。
- 中文页面部分由上游 AI 翻译，原有英文参考链接与提示已保留。版本、价格、配额、兼容性或用户要求最新版时应在线核对。

## 许可与署名

原文与配图来源为 **Dify / LangGenius 及其文档贡献者**，上游文档仓库为 <https://github.com/langgenius/dify-docs>，许可为 **Creative Commons Attribution 4.0 International（CC BY 4.0）**：

- [上游许可原文](https://github.com/langgenius/dify-docs/blob/main/LICENSE)
- [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- [随包保留的完整许可](assets/UPSTREAM-LICENSE.txt)

每篇原始来源 URL 见清单和索引。此处进行了 Markdown 导出整理、本地路径与媒体链接转换、目录和检索索引生成；未另写或改译产品正文。上游文档保留 CC BY 4.0，不因所在集合仓库采用其他许可而改变；不暗示 Dify 官方为本 Skill 背书。
