> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 重排序

> 提升搜索精准度

检索系统以速度为优先，返回结果的精准度可能不够理想。Reranking 模型对检索到的文档重新打分排序，将最相关的结果排在前面，显著提升搜索精准度。

<Tip>
  **Reranking 的最佳使用场景**： 当初始检索返回 20-100+ 条相关度参差不齐的候选结果时，Reranking 的提升效果最明显。如果检索结果本身已高度相关（如精确关键词匹配），Reranking 的价值有限。典型 RAG 流水线：先用 Embedding 检索 50-100 条候选文档，再用 Reranking 筛选出 Top 5-10，最后将这些结果传给 LLM。
</Tip>

## 前提条件

[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。

## 文档重排序

将查询和候选文档列表传入 API，模型会按相关度对文档排序后返回。

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-api/v1",
      )

      results = client.post(
        "/reranks",
        body={
          "model": "qwen3-rerank",
          "query": "什么是重排序模型",
          "documents": [
            "重排序模型广泛应用于搜索引擎和推荐系统，用于按相关性对候选文本排序",
            "量子计算是计算科学的前沿领域",
            "预训练语言模型的发展为重排序模型带来了新的突破"
          ],
          "top_n": 2
        },
        cast_to=object
      )

      print(results)
      ```

      ```javascript Node.js
      const OpenAI = require("openai");

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-api/v1",
      });

      async function rerank() {
        const results = await openai.post("/reranks", {
          body: {
            model: "qwen3-rerank",
            query: "什么是重排序模型",
            documents: [
              "重排序模型广泛应用于搜索引擎和推荐系统，用于按相关性对候选文本排序",
              "量子计算是计算科学的前沿领域",
              "预训练语言模型的发展为重排序模型带来了新的突破",
            ],
            top_n: 2,
          },
        });

        console.log(JSON.stringify(results, null, 2));
      }

      rerank();
      ```

      ```bash curl
      curl --request POST \
        --url https://dashscope.aliyuncs.com/compatible-api/v1/reranks \
        --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
        --header "Content-Type: application/json" \
        --data '{
          "model": "qwen3-rerank",
          "query": "什么是重排序模型",
          "documents": [
            "重排序模型广泛应用于搜索引擎和推荐系统，用于按相关性对候选文本排序",
            "量子计算是计算科学的前沿领域",
            "预训练语言模型的发展为重排序模型带来了新的突破"
          ],
          "top_n": 2
      }'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python
      import dashscope
      from http import HTTPStatus

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      resp = dashscope.TextReRank.call(
        model="qwen3-rerank",
        query="什么是重排序模型",
        documents=[
          "重排序模型广泛应用于搜索引擎和推荐系统，用于按相关性对候选文本排序",
          "量子计算是计算科学的前沿领域",
          "预训练语言模型的发展为重排序模型带来了新的突破"
        ],
        top_n=2,
        return_documents=True
      )

      if resp.status_code == HTTPStatus.OK:
        print(resp)
      ```

      ```bash curl
      curl --request POST \
        --url https://dashscope.aliyuncs.com/api/v1/services/rerank/text-rerank/text-rerank \
        --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
        --header "Content-Type: application/json" \
        --data '{
        "model": "qwen3-rerank",
        "input": {
          "query": "什么是重排序模型",
          "documents": [
            "重排序模型广泛应用于搜索引擎和推荐系统，用于按相关性对候选文本排序",
            "量子计算是计算科学的前沿领域",
            "预训练语言模型的发展为重排序模型带来了新的突破"
          ]
        },
        "parameters": {
          "top_n": 2,
          "return_documents": true
        }
      }'
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## 核心功能

### 使用指令优化排序（instruct）

`instruct` 参数用于引导模型采用不同的排序策略。指令需使用英文编写。

- **问答检索（默认）**：`"Given a web search query, retrieve relevant passages that answer the query."`
  - 侧重：找到答案。对于查询"How to prevent colds?"，"Washing hands frequently prevents colds" 的得分高于 "The common cold is a widespread illness"（虽然主题相关但未回答问题）。

- **语义相似度**：`"Retrieve semantically similar text."`
  - 侧重：语义等价，不受措辞影响。例如在 FAQ 场景中，"How to change my password?" 会匹配 "What if I forgot my password?"。

如果未设置，模型默认使用问答检索策略。更多任务指令示例请参见[模型仓库](https://github.com/QwenLM/Qwen3-Embedding/blob/main/evaluation/task_prompts.json)。

<Tabs>
  <Tab title="OpenAI 兼容">
    ```bash curl
    curl --request POST \
      --url https://dashscope.aliyuncs.com/compatible-api/v1/reranks \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --data '{
        "model": "qwen3-rerank",
        "query": "How to change my password?",
        "documents": [
          "Click Settings > Security > Change Password to update your credentials",
          "What if I forgot my password?",
          "Our platform supports two-factor authentication"
        ],
        "instruct": "Retrieve semantically similar text."
    }'
    ```
  </Tab>

  <Tab title="DashScope">
    ```python Python
    import dashscope
    from http import HTTPStatus

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    resp = dashscope.TextReRank.call(
      model="qwen3-rerank",
      query="How to change my password?",
      documents=[
        "Click Settings > Security > Change Password to update your credentials",
        "What if I forgot my password?",
        "Our platform supports two-factor authentication"
      ],
      instruct="Retrieve semantically similar text."
    )

    if resp.status_code == HTTPStatus.OK:
      print(resp)
    ```
  </Tab>
</Tabs>

### 返回前 N 个结果（top\_n）

使用 `top_n` 指定只返回排名最高的若干文档。如果不设置，默认按相关度排序返回所有文档。如果 `top_n` 超过文档总数，则返回全部文档。

## 支持的模型

<Note>
  gte-rerank 模型将于 2026 年 05 月 30 日下线，推荐使用 qwen3-rerank 模型替代。详情请参见[官网公告](https://www.aliyun.com/notice/118217)。
</Note>

| 模型           | 最大文档数 | 单文档最大 Token 数 | 单请求最大 Token 数 | 支持语言                                         | 适用场景          |
| ------------ | ----- | ------------- | ------------- | -------------------------------------------- | ------------- |
| qwen3-rerank | 500   | 4,000         | 120,000       | 100+ 种语言：中文、英文、西班牙文、法文、葡萄牙文、印尼文、日文、韩文、德文、俄文等 | 语义文本搜索、RAG 应用 |

**关键概念**：

- **单文档最大 Token 数**：每条查询或文档的最大 Token 数。超出部分会被截断，排序结果仅基于截断后的内容计算，可能影响排序精度。
- **最大文档数**：单次请求允许的最大文档数量。
- **单请求最大 Token 数**：计算方式为 `查询 Token 数 x 文档数量 + 所有文档 Token 总数`，不得超过单请求限制。

## API 参考

- [OpenAI 兼容端点](/api-reference/rerank/openai-rerank)
- [DashScope 端点](/api-reference/rerank/dashscope-rerank)

## 错误码

调用失败时，请参见[错误码](/api-reference/preparation/error-messages)。

## 限流

请参见[限流](/developer-guides/administration/rate-limits)。
