> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# OpenAI 兼容接口

> 只需修改 base_url、api_key 和 model 三个参数，即可从 OpenAI 迁移到千问AI平台。

千问AI平台提供 OpenAI 兼容的 API。如果您已有使用 OpenAI SDK 或 REST API 的代码，只需修改 `base_url`、`api_key` 和 `model` 三个参数即可切换到 Qwen 模型。

## 快速迁移

<Tabs>
  <Tab title="Python">
    ```python
    import os
    from openai import OpenAI

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
      model="qwen3.7-plus",
      messages=[{"role": "user", "content": "Hello!"}],
    )
    print(completion.choices[0].message.content)
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";

    const openai = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    });

    async function main() {
      const completion = await openai.chat.completions.create({
        model: "qwen3.7-plus",
        messages: [{ role: "user", content: "Hello!" }],
      });
      console.log(completion.choices[0].message.content);
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash
    curl https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3.7-plus",
        "messages": [{"role": "user", "content": "Hello!"}]
      }'
    ```
  </Tab>
</Tabs>

<Note>
  开始前，请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。如使用 OpenAI SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

## 支持的 API

| API                                   | Base URL（SDK 使用）                                                          | 说明              |
| ------------------------------------- | ------------------------------------------------------------------------- | --------------- |
| [Chat Completions](#chat-completions) | `https://dashscope.aliyuncs.com/compatible-mode/v1`                       | 文本生成、视觉理解、函数调用  |
| [Responses](#responses-api)           | `https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1` | 内置工具、简化多轮对话     |
| [Embedding](#embedding)               | `https://dashscope.aliyuncs.com/compatible-mode/v1`                       | 文本向量化           |
| [File](#file-api)                     | `https://dashscope.aliyuncs.com/compatible-mode/v1`                       | 文件上传与管理         |
| [Batch](#batch-api)                   | `https://dashscope.aliyuncs.com/compatible-mode/v1`                       | 异步批量处理，成本降低 50% |
| [Conversations](#conversations-api)   | `https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1` | 自动管理多轮对话上下文     |

<Warning>
  Responses API 和 Conversations API 的 `base_url` 与其他四个 API **不同**，请确保使用正确的 `base_url`。
</Warning>

## Chat Completions

Chat Completions API（`/v1/chat/completions`）与 OpenAI 的 Chat API 基本兼容，主要差异如下。

### Qwen 扩展参数

以下参数不属于 OpenAI 标准。在 OpenAI SDK 中通过 `extra_body` 传入。

| 参数                          | 类型      | 说明                                                                               |
| --------------------------- | ------- | -------------------------------------------------------------------------------- |
| `enable_thinking`           | Boolean | 启用深度推理模式。部分模型需要开启流式输出。参见[深度思考](/developer-guides/text-generation/thinking#注意事项)。 |
| `thinking_budget`           | Integer | 思考过程的最大 token 数。流式输出要求与 `enable_thinking` 相同。                                    |
| `enable_search`             | Boolean | 启用联网搜索，替代 OpenAI 的 `web_search_options`。                                         |
| `search_options`            | Object  | 配置搜索行为（策略、强制搜索等）。                                                                |
| `top_k`                     | Integer | 采样候选集大小。取值范围：(0, 100]。                                                           |
| `vl_high_resolution_images` | Boolean | 为视觉模型启用高分辨率模式。                                                                   |
| `enable_code_interpreter`   | Boolean | 启用代码解释器。需要开启流式输出（Responses API 除外）。                                              |

### 行为差异

- **`response_format`** 支持 `json_object` 和 `json_schema`。
- **`tool_choice`** 支持 `auto`、`none`、`required` 和指定函数对象（`{"type": "function", "function": {"name": "..."}}`）。
- **`tools`** 仅支持 `function` 类型。
- **`parallel_tool_calls`** 默认为 `true`（与 OpenAI 一致）。
- **`n`** 支持 1-4，仅限部分模型（qwen-plus、qwen-plus-character）。
- **`web_search_options`** 不支持，请改用 `extra_body.enable_search` 和 `extra_body.search_options`。

### 不支持的参数

以下参数会被静默忽略：`frequency_penalty`、`logit_bias`、`max_completion_tokens`、`metadata`、`prediction`、`prompt_cache_key`、`reasoning_effort`、`service_tier`、`store`、`verbosity`。

完整 API 参考和代码示例，参见 [Chat Completions](/api-reference/chat/openai-chat)。

## Responses API

Responses API 使用**不同的 base\_url**：`https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1`。

相比 Chat Completions，Responses API 提供：

- **内置工具**：`web_search`、`code_interpreter`、`web_extractor` 和 `image_search`，无需额外配置。
- **简化多轮对话**：传入 `previous_response_id` 即可，无需手动构建完整消息历史。
- **对话集成**：配合 [Conversations API](#conversations-api) 实现自动上下文管理。
- **会话缓存**：自动缓存跨轮次上下文，降低延迟和成本。通过 `x-dashscope-session-cache: enable` 请求头启用。参见[会话缓存](/developer-guides/run-and-scale/context-cache#session-cache)。

### 从 Chat Completions 迁移

从 Chat Completions 切换到 Responses API：

1. 将 `base_url` 修改为 `https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1`，接口路径从 `/v1/chat/completions` 改为 `/v1/responses`。
2. 用 `output_text` 替代 `choices[0].message.content` 读取响应。
3. 多轮对话时传入 `previous_response_id`，无需手动追加消息。

完整参考和代码示例，参见 [Responses](/api-reference/chat/openai-responses)。

## Embedding

Embedding API（`/v1/embeddings`）与 OpenAI 的 Embedding API 兼容，主要差异：

- **`encoding_format`**：支持 `float`（默认）和 `base64`。
- **`user`**：不支持（静默忽略）。
- **`dimensions`**：可选值取决于模型。例如 `text-embedding-v4` 支持 2,048、1,536、1,024（默认）、768、512、256、128 和 64。

支持的模型和代码示例，参见 [Embedding](/api-reference/text-embedding/openai-embedding)。

## File API

File API（`/v1/files`）与 OpenAI 的 Files API 兼容，主要差异：

- **`purpose`** 仅支持 `file-extract`（用于 Qwen-Long/Qwen-Doc 文档分析）和 `batch`（用于批量处理）。不支持 OpenAI 的 `fine-tune`、`assistants` 等值。
- **文件内容获取**（`GET /v1/files/{file_id}/content`）不支持。
- **列表过滤**：`GET /v1/files` 的 `purpose` 和 `order` 参数不支持。
- **存储限制**：最多 10,000 个文件，总容量 100 GB，文件永不过期。

完整参考，参见 [File](/api-reference/platform-api/file)。

## Batch API

Batch API（`/v1/batches`）与 OpenAI 的 Batch API 兼容，主要差异：

- **成本降低 50%**：相比实时调用价格。
- **`completion_window`**：支持 24h 到 336h（14 天），接受 "h"（小时）和 "d"（天）为单位的整数值。OpenAI 固定为 24h。
- **扩展元数据**：`metadata.ds_name`（任务名称）和 `metadata.ds_description`（任务描述）。
- **扩展列表过滤**：支持 `ds_name`、`input_file_ids`、`status`、`create_after`、`create_before`。
- **输入文件限制**：每个文件最多 50,000 条请求，单个文件大小不超过 500 MB，单行不超过 6 MB。同一文件中的所有请求必须使用相同模型。

完整使用指南，参见 [Batch API](/api-reference/platform-api/batch/create-batch)。

## Conversations API

Conversations API 是 Qwen 特有的功能，在 OpenAI 中没有对应接口。它可以跨设备和会话自动管理多轮对话上下文，`base_url` 与 Responses API 相同：`https://dashscope.aliyuncs.com/api/v2/apps/protocols/compatible-mode/v1`。

配合 Responses API 使用，可自动注入历史上下文，无需手动同步消息。

完整参考，参见 [Conversations](/api-reference/platform-api/conversations)。
