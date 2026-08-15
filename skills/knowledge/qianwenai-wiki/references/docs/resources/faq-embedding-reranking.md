> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 向量与重排序 FAQ

> 文本向量、多模态向量和重排序的常见问题——模型选择、维度、批量限制及使用场景。

<a id="text-embedding" />

## 文本向量

**API**：[OpenAI 兼容](/api-reference/text-embedding/openai-embedding)、[DashScope](/api-reference/text-embedding/dashscope-embedding)

### 单条文本的最大输入长度是多少？

每条文本最多支持 **8,192 个 token**。超出限制的内容会在生成向量前被截断。对长文档生成向量时请注意控制输入长度。

### 支持多大的批量？

单次 API 调用最多接受 **10 条文本**。数据量更大时，将输入拆分为每批 10 条，分多次调用。如果传入文件而非数组，文件最多包含 10 行。

### 支持哪些向量维度？

`text-embedding-v4` 支持 2,048、1,536、1,024（默认）、768、512、256、128 和 64 维。`text-embedding-v3` 支持 1,024（默认）、768 和 512 维。使用 `dimension` 参数选择具体维度。

维度越高，保留的语义信息越丰富，但存储和计算成本也越高。1,024 维适用于大多数场景；高精度领域可选择 1,536 或 2,048 维；存储受限时可选择 512 维或更低。

### 什么时候使用 `text_type` 参数？

在搜索任务中使用 `text_type` 可以获得更好的效果：

- `text_type: 'query'` — 用于**用户查询**，生成针对信息检索优化的向量。
- `text_type: 'document'`（默认）— 用于**存储文档**，生成针对被检索优化的综合向量。

如果所有文本角色相同（如聚类、分类），无需设置 `text_type`。该参数仅 DashScope 端点支持。

### 稠密向量和稀疏向量有什么区别？

`text-embedding-v4` 和 `text-embedding-v3` 支持三种输出类型，通过 `output_type` 参数控制：

| 类型             | 优势                | 不足                    | 适用场景             |
| -------------- | ----------------- | --------------------- | ---------------- |
| `dense`        | 深度语义理解，能处理同义词和上下文 | 计算和存储成本较高，无法保证精确关键词匹配 | 语义搜索、RAG、内容推荐    |
| `sparse`       | 精确关键词匹配速度快，开销低    | 无语义理解能力，会遗漏同义词        | 日志检索、SKU 查询、精确过滤 |
| `dense&sparse` | 兼具语义理解和关键词匹配能力    | 存储要求更高，检索逻辑更复杂        | 生产环境混合搜索引擎       |

生成 `dense&sparse` 的成本与仅生成单种向量相同。

该参数仅 DashScope 端点支持，OpenAI 兼容端点不支持 `output_type`。

### 文本向量适用于哪些场景？

常见应用：语义搜索（向量相似度匹配）、RAG（检索增强生成）、推荐系统（物品间相似度）、聚类和文本分类。

---

<a id="multimodal-embedding" />

## 多模态向量

**API**：[DashScope multimodal embedding](/api-reference/multimodal-embedding/dashscope-multimodal-embedding)

### 支持哪些模态？

`tongyi-embedding-vision-plus` 和 `tongyi-embedding-vision-flash` 均支持文本、图像和视频。文本仅限中英文。适用于跨模态搜索（以文搜图、以图搜图、以文搜视频）、图像分类和视频分类等场景。

### 支持哪些图片和视频格式？

- **图片**：JPEG、PNG、BMP，通过公开 URL 或 Base64 编码字符串传入。每次请求最多 8 张图片，单张不超过 3 MB。
- **视频**：MP4、MPEG、MOV、MPG、WEBM、AVI、FLV、MKV，仅支持 URL（不支持 Base64）。单个视频不超过 10 MB。

### 多模态向量是否支持 OpenAI 兼容端点？

不支持。多模态向量需要使用 DashScope SDK 或 REST API。OpenAI 兼容端点（`/compatible-mode/v1/embeddings`）仅支持文本向量。

### 单次请求能发送多少内容？

没有固定的元素数量限制。限制条件是所有输入的总 token 数——批量请求不得超过模型的单次请求 token 上限。文本输入每条限制为 1,024 个 token。

---

<a id="reranking" />

## 重排序

**API**：[OpenAI 兼容](/api-reference/rerank/openai-rerank)、[DashScope](/api-reference/rerank/dashscope-rerank)

### 重排序在什么场景最有价值？

初始检索返回 20–100+ 条相关度参差不齐的候选结果时，重排序的价值最大。典型 RAG 流程：先用向量检索 50–100 条候选，重排序后取 top 5–10，再传给大模型。

如果初始检索已返回高相关结果（如精确关键词匹配），重排序的提升有限。

### `instruct` 参数是什么？如何编写指令？

`instruct` 用于引导模型的排序策略。指令必须用英文编写。

两个常见示例：

- **问答检索（默认）**：`"Given a web search query, retrieve relevant passages that answer the query."` — 优先返回直接回答问题的文档。
- **语义相似度**：`"Retrieve semantically similar text."` — 优先返回表达相同含义但措辞不同的文档，适用于 FAQ 匹配。

如果不设置，模型默认使用问答检索策略。

### `top_n` 是什么？

`top_n` 限制返回的文档数量。设为 5 则只返回排名前 5 的文档。不设置则返回所有文档（按排序结果排列）。如果 `top_n` 超过文档总数，则返回所有文档。

---

<a id="model-selection" />

## 模型选择

### 应该选择哪个文本向量模型？

大多数情况下推荐使用 `text-embedding-v4`。它支持指令、稀疏向量，且维度选项比 `text-embedding-v3` 更丰富。两个模型定价相同（每百万输入 token 0.5元，此为目录价，具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看），批量限制也相同（10 条文本，每条 8,192 token）。

### 有哪些重排序模型可用？

当前可用的重排序模型为 `qwen3-rerank`，支持单次请求最多 500 篇文档、每篇最多 4,000 token，覆盖 100+ 种语言。关于计费，请参见[模型市场](https://www.qianwenai.com/models)。
