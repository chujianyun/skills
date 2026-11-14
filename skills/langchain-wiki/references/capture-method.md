# 抓取与覆盖核对

## 范围与证据

规范入口：https://docs.langchain.com/oss/python/langchain/overview

保留英文原文，提供中文检索指引。范围是 Python 的 LangChain 文档，包括主导航、Learn 中的 LangChain 教程与概念、源码中仍公开可访问的错误参考，以及 LangChain 导航直接引用的共享 Retrieval 和 Python Changelog。

初始快照共 **77 篇正文、19 张正文图片**：

- 68 篇位于 `/oss/python/langchain/` 且列入官方站点地图的页面。
- 7 篇 `/oss/python/langchain/errors/` 错误参考：官方源码有对应文件，官方 Markdown 端点可访问，但未列入站点地图。
- 1 篇共享 Retrieval：`/oss/python/deepagents/retrieval`，来自 LangChain 的 Advanced usage 导航。
- 1 篇共享 Python Changelog：`/oss/python/releases/changelog`，来自 LangChain 的 Get started 导航；旧 `changelog-py` 是别名。

官方 Python 导航覆盖其中 70 页；源码范围共 77 个 MDX 文件，映射并合并旧 Retrieval 路径和更新日志别名后，与上述 77 篇一致。逐页来源集合与源码版本见 `discovery.json`；当前覆盖率、正文来源和实际文件哈希以 `wiki-manifest.json` 为准，更新后不要沿用这里的初始数量作验收标准。

交叉核对来源：

1. [官方源码仓库](https://github.com/langchain-ai/docs)，递归树用于发现导航外错误页，`src/docs.json` 用于保留 Python / LangChain 和 Learn 的分组层级。源码配置与图片使用同一 commit 读取。
2. [官方 Python 文档索引](https://docs.langchain.com/_llms/agent-development-lifecycle/build/python.txt)，交叉核对页面身份。
3. [站点地图](https://docs.langchain.com/sitemap.xml)，合并 LangChain Python 子树中的公开页面。
4. 每个页面的官方 `.md` 导出用于正文，要求 `text/markdown`、非空标题与正文。

## 转换规则

- 直接使用官方渲染后的 Markdown，保留标签页中的全部代码、折叠块、表格、告警和 Mermaid 图；不通过 HTML 首屏提取正文。
- 移除重复的 Documentation Index 提示和代码围栏的显示主题参数，保留代码内容及语言标记。
- 本地目录按官方导航分组，文件名按正文标题；同页多入口、`/index` 与重定向别名合并为一页。
- 正文中指向已收录页面的链接改为本地相对 Markdown 路径；文档范围外的链接保留绝对地址，锚点保留。
- 正文图片全部下载，优先用官方源码仓库中同一 commit 的 MIT 原图，避免携带 CDN 图片优化签名；资产清单保存稳定的官方源码来源地址。
- 视频、外部演示、API Reference 与范围外文档的在线链接仅作为引用，不计为本地语料。
- 将上游示例的 `your-api-key` 等虚拟密钥统一为 `<API_KEY>`，保留变量名、调用方式及其余代码，避免占位符被仓库密钥扫描误报。
- 不以抓取时间、站点构建 ID 或随机锚点改写正文。更新使用新的临时 HTTP 缓存，避免误用旧内容。

## 排除项

- LangChain Academy 是外部课程跳转（源码 `academy.mdx` 的 `url` 指向 Academy），没有离线正文。
- 独立 JavaScript/TypeScript、LangGraph、Deep Agents、LangSmith 文档，第三方供应商集成目录、独立 API Reference、博客及 GitHub issue 不包含在此范围。共享 Retrieval 与 Python Changelog 是已说明的导航例外。
- 官方源码仓库采用 MIT，完整许可保留在 `LICENSE-UPSTREAM.txt`；本 Skill 不改变上游文档及配图的版权归属。

## 完整性门槛

`capture_docs.py` 先完成导航、站点地图和源码盘点，再抓取正文与图片；任一页面或图片失败时返回非零状态且不输出可构建的 `inventory.json`。同一 URL 最多尝试三次；不绕过身份验证或访问控制。

构建后核对：清单覆盖数与文件数一致、逐文档与资产哈希一致、所有本地链接存在、已收录页面无残留在线正文链接、正文图片全部本地化、代表性搜索可命中、同一 staging 再次同步返回 `UNCHANGED` 且不修改文件。白泽同步器拒绝不完整 staging 与未授权的删页。
