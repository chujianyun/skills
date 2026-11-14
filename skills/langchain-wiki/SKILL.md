---
name: langchain-wiki
description: "LangChain Python 官方文档离线 Wiki。用于查询 create_agent、模型、消息、工具调用、结构化输出、中间件、记忆、流式输出、MCP、多智能体、RAG、前端、测试、部署与错误排查，也用于手动更新本 Wiki；保留英文原文，使用中文检索提示，不覆盖独立 LangGraph、Deep Agents 或供应商集成目录。"
---

# LangChain Python Wiki

使用随 Skill 打包的 Wiki 文档回答问题。离线文档是第一依据；只有本地材料不足、用户要求核对最新版或问题超出快照范围时，才补查规范来源。

## 资源

- [文档索引](references/INDEX.md)：浏览完整主题结构或搜索词不确定时读取。
- [来源与范围](references/SOURCE.md)：回答版本、许可证、完整性或时效性问题时读取。
- [更新协议](references/UPDATE.md)：用户要求刷新、同步或自动更新本 Wiki Skill 时读取。
- [抓取与覆盖核对](references/capture-method.md)：范围、导航交叉核对、正文与图片转换规则。
- [上游 MIT 许可](references/LICENSE-UPSTREAM.txt)：上游版权及许可原文。
- `references/discovery.json`：导航、站点地图与官方源码逐页交叉盘点。
- `references/docs/`：保持 Wiki 导航层级的 Markdown 正文；只读取与问题直接相关的文件。
- `references/wiki-manifest.json`：页面来源、路径和逐文档 SHA-256 清单。
- `scripts/search_docs.py`：零第三方依赖的本地全文检索。
- `scripts/capture_docs.py`：重新盘点并抓取官方 Markdown 与图片到临时目录。

## 主题定位

正文保留官方英文原文；中文问题先转换成英文术语、包名或 API 名再搜索。例如“短期记忆”搜索 `short-term memory checkpointer`，“工具审批”搜索 `human-in-the-loop interrupt`。

| 问题 | 目录 / 搜索词 |
| --- | --- |
| 安装、创建 Agent、升级 | `Get started/`、`Overview/`；`create_agent install` |
| 模型、消息、工具、结构化输出、流式输出 | `Core components/`；`tool calling structured output streaming` |
| 中间件、重试、降级、摘要、限流 | `Middleware/`；`middleware retry fallback summarization` |
| 记忆、上下文、审批、RAG | `Advanced usage/`；`memory context engineering retrieval interrupt` |
| MCP、多智能体、子智能体、移交、Skills | `Advanced usage/MCP/`、`Advanced usage/Multi-agent/` |
| 前端、生成式 UI、工具卡片 | `Frontend/`；`useStream generative UI tool calling` |
| 测试、评估、部署、观测 | `Agent development/`、`Production/`；`testing evals deployment observability` |
| SQL、语义搜索、语音、多智能体实战 | `Learn/Tutorials/`；`SQL agent semantic search voice handoffs` |
| 鉴权、限流、消息、工具结果等错误 | `Error reference/`；优先搜索原始错误码 |

`Retrieval` 是 LangChain 导航共用页面，官方现位于 Deep Agents 路径；收录这一页不代表收录 Deep Agents 全站。第三方供应商详细集成、完整 LangGraph/Deep Agents/LangSmith 文档与独立 API Reference 不在快照范围内；本地证据不足时按来源边界在线补充。

## 依赖

检索、抓取和同步脚本仅依赖 Python 3.10+ 标准库。运行前用 `python3 --version` 检查；版本不足时停止并提示从 <https://www.python.org/downloads/> 安装兼容版本，不自行安装。抓取需要访问官方文档与 GitHub 公共 HTTPS 端点；网络或页面失败时保留旧快照，报告缺口，不构建不完整更新。

## 回答工作流

1. 从当前 `SKILL.md` 所在目录确定 Skill 根目录，不假设用户工作目录。
2. 把问题提炼为 2–5 个关键词，保留产品名、类名、命令、包名和错误码。
3. 运行：

   ```bash
   python3 <skill-root>/scripts/search_docs.py "<keywords>"
   ```

   搜索过宽时加 `--prefix <directory>`；没有结果时换同义词或旧/新术语重试一次。
4. 读取排名最高且互相补充的 1–3 篇文档。需要理解主题全貌时再读索引，不一次加载全部语料。
5. 根据已读资料给出直接结论、必要步骤和前置条件。版本、包名、导入路径、配置键和命令不能凭记忆补全。
6. 文档不足或用户要求最新版时，只补查 `references/SOURCE.md` 指定的规范来源，并明确标为在线补充。

## 更新入口

用户要求更新本 Wiki Skill 时，完整阅读 [更新协议](references/UPDATE.md)。必须重新抓取完整范围到临时目录并先 dry-run；内容与元数据都没变化时保持正文、索引和清单原样。未经授权不得归档上游删页、创建后台任务、提交、推送或公开发布。

## 常见陷阱

- 离线快照不天然代表最新版本；版本敏感问题先看来源边界。
- 搜索无结果不等于功能不存在。更换产品术语、类名、命令或目录前缀后再判断。
- 同一主题可能分散在概览、教程、参考和排障文档；必要时交叉读取。
- 示例中的凭据只能当占位符，不读取、输出或写入用户真实密钥。
- 清单中的来源 URL 只用于溯源，不能据此绕过登录或访问控制。

## 输出契约

回答至少包含：直接结论或可执行做法，以及 `参考文档` 列表（实际读取的 `references/docs/...` 相对路径）。快照可能过期、资料冲突或使用在线补充时再添加版本说明。证据不足时明确列出已搜索关键词和语料缺口，不编造答案。
