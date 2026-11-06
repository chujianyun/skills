# 来源与范围

- Wiki：LangGraph Python
- 规范来源：<https://docs.langchain.com/oss/python/langgraph>
- 语言 / 版本：英文正文；Python SDK 当前在线文档，不固定包版本；支持中文提问与回答
- 抓取范围：Python LangGraph 导航、llms 索引、站点地图及官方源码交叉盘点的全部 52 篇产品文档，加导航直接关联的 Studio 页面，共 53 篇；含 Changelog 重定向目标、6 篇错误说明、RAG/SQL 教程与案例；不包含 JavaScript SDK、独立 API Reference 或整个 LangSmith 文档站。
- 当前快照：完整；精确覆盖数与最近一次有变化的同步时间见 `wiki-manifest.json`
- 上游许可：LangChain 文档仓库采用 MIT License；保留 references/LICENSE.langchain.txt。上游许可不受本仓库默认许可替代。

离线快照可能落后于上游。许可证不明或不允许再分发时，本 Skill 仅限用户授权的本地使用，不应提交到公开仓库或发布到市场。

## 盘点依据与映射

- [原始入口](https://docs.langchain.com/oss/python/langgraph/overview)；英文正文，Python SDK。
- [官方导航配置](https://github.com/langchain-ai/docs/blob/main/src/docs.json)：Python LangGraph 标签共 44 个导航页面（包括 Studio 链接）。
- [官方 Python 文档索引](https://docs.langchain.com/_llms/agent-development-lifecycle/build/python.txt)与[站点地图](https://docs.langchain.com/sitemap.xml)：各含 45 个唯一 Python LangGraph 产品页面。
- [官方源码目录](https://github.com/langchain-ai/docs/tree/main/src/oss/langgraph)：53 个源文档，排除 JavaScript 专用 Changelog 后为 52 篇，再加主导航关联的 Studio 页面，共 53 篇。
- 导航分组保持原名；额外教程、案例和错误文档按 Learn 与 Reference 分组保存。全部页面、来源 URL、路径及 SHA-256 见 `wiki-manifest.json`。
- [Changelog](https://docs.langchain.com/oss/python/langgraph/changelog-py) 跳转到 Python Releases Changelog；[旧 Studio 入口](https://docs.langchain.com/oss/python/studio) 跳转到 LangSmith Studio；两者均抓取目标 Markdown 正文，其余 LangSmith 页面不递归纳入。
- 26 次图片引用去重为 24 个本地资产；代码块、Mermaid 图、表格与标签页展开结果均从官方 Markdown 保留。移除站点导航提示、页脚及代码围栏中的渲染主题元数据。
- 版本说明：这是在线文档快照，未锁定 `langgraph` 包版本。正文中涉及具体版本的要求以对应页面为准；查旧版本或最新变化需另行核对。

## 许可

[LangChain docs 上游仓库 MIT License](https://github.com/langchain-ai/docs/blob/main/LICENSE)涵盖软件及配套文档；原许可全文见 `LICENSE.langchain.txt`。本仓库的默认许可不替代上游许可，原有第三方链接和署名保留。

公开仓库适配：认证示例中含 `your` 的长占位密钥统一为 `<API_KEY>`，保留环境变量名、SDK 参数与调用流程；这不涉及真实凭据。
