# llama-index-wiki

面向 LlamaIndex Python Framework 的离线文档知识库 Skill。它把 455 篇用户文档与一个本地搜索工具打包在一起，可用于回答安装、RAG、索引、检索、Agent、Workflow、模型与向量库集成、评估、部署、LlamaCloud 和 LlamaParse 等问题。

## 使用示例

- “LlamaIndex 怎么把索引持久化到磁盘？”
- “VectorStoreIndex 和 SummaryIndex 有什么区别？”
- “用 Ollama 和 HuggingFace Embedding 写一个本地 RAG 示例。”
- “AgentWorkflow 如何做多 Agent 协作？”
- “LlamaParse 接入前需要安装哪些包？”

调用 `$llama-index-wiki` 后，Agent 会先检索离线文档，读取少量相关页面，再给出带来源路径的答案。文档快照之外的最新变化或实现细节会回到官方源码仓库核对。

## 范围与边界

- 语料以 Python Framework 用户文档为主，不保证覆盖 TypeScript SDK。
- 离线快照可能落后于最新版；版本敏感问题需要在线核对。
- Skill 不包含任何真实凭据，也不会默认执行付费 API 调用或外部写入。
- 官方源码仓库：<https://github.com/run-llama/llama_index>
- 官方文档：<https://developers.llamaindex.ai/python/framework/>

打包的上游文档与源码材料沿用 LlamaIndex 项目的 MIT License，见 [UPSTREAM_LICENSE](UPSTREAM_LICENSE)。
