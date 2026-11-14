# 来源与范围

- Wiki：LangSmith
- 规范来源：<https://docs.langchain.com/langsmith>
- 语言 / 版本：英文官方在线文档；Python 与 TypeScript 示例分别保留
- 抓取范围：docs.langchain.com 上全部公开 LangSmith 导航、递归 llms 索引与 sitemap 页面；包括 Evaluation 全部子目录与 LangSmith / Agent Server REST API；不含独立 reference.langchain.com SDK 参考站、博客、学院及未发布源码模板
- 当前快照：完整；精确覆盖数与最近一次有变化的同步时间见 `wiki-manifest.json`
- 上游许可：MIT，Copyright (c) 2025 LangChain；完整声明见 LICENSE.langchain.txt。上游文档仍按 MIT 授权，不因本集合的许可而改变。

离线快照可能落后于上游。许可证不明或不允许再分发时，本 Skill 仅限用户授权的本地使用，不应提交到公开仓库或发布到市场。

## 核对结果

- 导航唯一入口：610；站点地图：1250；递归官方索引：1250。三者取并集，重定向按最终页面合并。
- 唯一正文：1259；失败：0；配图：331。
- Evaluation：81 个导航入口全部覆盖，逐项 URL 见 capture-report.json。
- 官方源码树 SHA：`04d4d4a45cb57537c3d6e977f25333f2c5a4881b`（用于来源交叉核对；正文为在线 Markdown，不冒充固定 commit 的源码导出）。
- 未在官网发布的共享模板 / 旧源码页列于 capture-report.json 的 source_only_not_published，不混入当前公开文档。
- 上游示例中的凭据字面量、私钥边界标记规范化为短占位符，使用前须按官方说明配置自己的凭据。
- Markdown 正文保留代码、表格、标签页及折叠正文，内部页面链接改为本地相对路径，信息图片本地化；装饰性品牌链接保留线上地址。
- 上游源码与许可：https://github.com/langchain-ai/docs ，https://github.com/langchain-ai/docs/blob/main/LICENSE 。
