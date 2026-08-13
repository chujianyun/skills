---
name: llama-index-wiki
description: LlamaIndex 官方用户文档离线知识库，用于检索并回答 LlamaIndex Python 框架的安装、RAG、数据加载、索引、检索与查询、Agent、Workflow、模型、Embedding、向量库、评估、可观测性、部署、LlamaCloud 和 LlamaParse 等问题，也可生成有文档依据的示例代码与排障建议。当用户提到 LlamaIndex、llama-index、LlamaParse、VectorStoreIndex、QueryEngine、Retriever、AgentWorkflow 或相关集成用法时使用；纯源码贡献、内部实现审查或与 LlamaIndex 无关的通用 AI 问题不使用。
---

# LlamaIndex Wiki

使用随 Skill 打包的 LlamaIndex Python 用户文档回答问题。把离线文档作为第一依据；只有文档不足、用户要求核对最新版或问题涉及内部实现时，才补查官方源码仓库。

## 资源

- [文档索引](references/INDEX.md)：按目录列出全部文档及原始页面链接。需要浏览主题结构或搜索结果不稳定时读取。
- [来源与快照说明](references/SOURCE.md)：记录官方文档、源码仓库、快照范围和版本边界。回答时效性或来源问题时读取。
- `references/docs/`：离线 Markdown 文档正文。只读取与问题直接相关的文件。
- `scripts/search_docs.py`：零第三方依赖的全文检索工具。

## 工作流

1. 从当前 `SKILL.md` 所在目录确定 Skill 根目录，不要假设用户工作目录。
2. 将用户问题提炼为 2–5 个英文技术词；中文问题同时保留关键类名、包名和产品名。
3. 先运行：

   ```bash
   python3 <skill-root>/scripts/search_docs.py "persisting loading data" --prefix module_guides/storing
   ```

   搜索过宽时用 `--prefix module_guides/storing` 限定目录；没有结果时更换同义词、类名或包名重试一次。
4. 读取排名最高且互相补充的 1–3 篇文档。需要理解主题全貌时再读取 [文档索引](references/INDEX.md)，不要一次加载全部文档。
5. 对照文档给出直接答案、必要代码和前置条件。代码中的版本、包名、导入路径和环境变量必须来自已读取文档，不凭记忆补全。
6. 文档不足或用户要求核对最新版时，访问官方源码仓库 `https://github.com/run-llama/llama_index`。将源码得到的判断明确标为“源码补充”，不要伪装成文档结论。
7. 用用户的语言回答，并列出实际采用的离线文档相对路径；文档首行含原始页面 URL 时一并给出。

## 常见陷阱

- 这是一份离线快照，不代表最新发布版本。版本敏感问题必须说明快照边界，并在可联网时核对官方文档或源码。
- 语料聚焦 Python Framework。不要用它回答 TypeScript SDK 的精确 API，除非已补查对应官方资料。
- LlamaIndex 采用核心包与集成包拆分结构。区分 `llama-index`、`llama-index-core` 与 `llama-index-*` 集成包，不要把安装命令合并猜写。
- 同一主题可能同时存在入门、模块指南、集成和旧 FAQ。优先使用模块指南与具体集成文档，并用 changelog 或 `changes/deprecated_terms` 检查废弃用法。
- 示例中的 API Key 都只能当占位符。不要读取、输出或写入用户真实凭据；需要联网、付费服务或外部写入时先说明影响并取得确认。
- 搜索无结果不等于功能不存在。先改用类名、旧术语、新术语和目录过滤；仍无结果再说明语料未覆盖。

## 输出契约

回答至少包含：

1. 直接结论或可执行做法。
2. 必要的安装、代码、配置或排障步骤。
3. `参考文档`：列出实际读取的 `references/docs/...` 路径。
4. `版本说明`：仅在快照可能过期、文档互相冲突或使用源码补充时添加。

若证据不足，明确说“当前离线文档未找到可靠依据”，列出已搜索的关键词，不编造 API。
