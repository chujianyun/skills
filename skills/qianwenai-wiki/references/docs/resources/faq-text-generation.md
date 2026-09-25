> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文本生成常见问题

> 流式输出、上下文管理、上下文缓存、结构化输出、思考模式、函数调用和批量处理的常见问题。

<a id="streaming" />

## 流式输出

**API**：[OpenAI 兼容](/api-reference/chat/openai-chat)、[DashScope](/api-reference/chat/dashscope)

### 流式输出中途停止？

检查代理或基础设施配置：

- **Nginx 缓冲** — Nginx 默认缓冲 SSE 响应。在服务器配置中添加 `proxy_buffering off`。
- **请求超时** — 如果超时时间短于响应时间，连接会提前关闭。需要增大超时设置。
- **防火墙关闭空闲连接** — 部分防火墙会在 token 输出间隔较长时判定连接空闲并关闭。
- **未收到 `data: [DONE]`** — 确保客户端持续读取流，直到连接关闭或收到终止标记。

### 如何将流式输出的片段拼接为完整响应？

**OpenAI 兼容**：设置 `stream=True`。每个 chunk 包含 `choices[0].delta.content`，将所有非空的 `content` 拼接即可。如需获取 token 用量，同时设置 `stream_options={"include_usage": True}`，用量信息在最后一个 chunk 中返回。

**DashScope**：设置 `incremental_output=True`。每个 chunk 只包含新增 token（而非完整响应），按顺序拼接即可。每个 chunk 都包含 token 用量信息。

对于先思考再回答的模型（QwQ、设置了 `enable_thinking=True` 的 Qwen3），chunk 分两个阶段输出：先输出 `reasoning_content`，再输出 `content`。需要分别拼接。

### 哪些模型必须使用流式输出？

QwQ 和 QVQ 仅支持流式输出。未设置 `stream=True` 调用会失败或返回空响应。大多数 Qwen3 模型同时支持流式和非流式。Qwen-Omni 模型（`qwen3.5-omni-plus`、`qwen3.5-omni-flash`、`qwen3-omni-flash`）仅在函数调用时必须使用流式输出，其他场景两种模式均支持。

---

<a id="context-multi-turn" />

## 上下文与多轮对话

**API**：[多轮对话](/developer-guides/run-and-scale/multi-turn)、[上下文缓存](/developer-guides/run-and-scale/context-cache)

### 多轮对话如何实现？

API 是无状态的，不会存储对话历史。你需要自行维护 `messages` 数组：每轮对话后，将助手的回复和用户的新消息追加到数组中，然后将完整数组随下一次请求发送。

Responses API（`/v2/apps/...`）提供了简化方式：传入 `previous_response_id` 即可自动关联上下轮，无需手动管理消息数组。Response ID 有效期为 7 天。

### 如何控制对话长度、避免 token 溢出？

常用策略：

- **截断** — 当总 token 数接近上下文限制时，丢弃最早的消息。
- **摘要** — 将较早的对话轮次压缩为一条系统消息或用户消息。
- **检索** — 将对话历史存入向量数据库，每次请求只检索相关内容。

通过每次响应中的 `usage.prompt_tokens` 监控 token 增长。不同模型的上下文限制不同，详见[模型选择](/developer-guides/getting-started/model-selection)。

### 什么是上下文缓存？何时使用？

上下文缓存会存储 prompt 的前缀部分，后续重复调用可复用该前缀并享受 token 价格折扣。共有三种模式：

| 模式     | 启用方式                                                    | 缓存创建价格     | 缓存命中价格    | 最小 token 数 |
| ------ | ------------------------------------------------------- | ---------- | --------- | ---------- |
| **隐式** | 自动生效，无需配置                                               | 标准输入价格     | 输入价格的 20% | 256        |
| **显式** | 添加 `cache_control: {type: ephemeral}` 标记                | 输入价格的 125% | 输入价格的 10% | 1024       |
| **会话** | Responses API + `x-dashscope-session-cache: enable` 请求头 | 输入价格的 125% | 输入价格的 10% | 1024       |

隐式缓存在模型检测到重复前缀时自动生效。显式和会话模式在写入前缀时收取缓存创建费用，后续命中按缓存命中价格计费。

显式缓存适合在每次请求前附加大段固定内容（如系统 prompt 或文档）的场景。会话缓存适用于 Responses API 工作流。

缓存命中信息在 `usage.prompt_tokens_details.cached_tokens` 中返回。缓存按账号和模型隔离，不同账号或模型之间不共享。

### API 会自动保存对话记忆吗？

不会。API 是无状态的，没有内置记忆功能。你需要自行维护 `messages` 数组。如需跨会话保持记忆，请在外部存储对话历史，并在每次请求中包含相关历史。

---

<a id="structured-output" />

## 结构化输出

**API**：[结构化输出](/developer-guides/text-generation/structured-output)

### 如何可靠地获取 JSON 输出？

设置 `response_format={"type": "json_object"}`，并在 prompt 中包含"JSON"一词（例如"以 JSON 对象格式返回，包含以下字段……"）。模型会被约束为只输出合法 JSON。

不要设置 `max_tokens` — 截断的响应会产生无效 JSON。

### 为什么模型在 JSON 前后输出了多余文本？

这通常是因为 prompt 没有明确要求只输出 JSON，或未设置 `response_format`。添加 `response_format={"type": "json_object"}` 并在 prompt 中明确要求只返回 JSON。

如果需要从思考模型获取结构化输出（思考模型不支持 `response_format`），先获取完整响应文本，然后调用 `json.loads()` 解析。如果抛出 `JSONDecodeError`，将原始文本发送给快速模型（如 `qwen3.5-flash`），设置 `response_format={"type": "json_object"}` 让其修复 JSON。

---

<a id="thinking-mode" />

## 思考模式

**API**：[思考模式](/developer-guides/text-generation/thinking)

### 什么是思考模式？

思考模式让模型在给出最终答案前先进行逐步推理。推理过程在 `reasoning_content` 中返回，最终答案在 `content` 中返回。这能提升数学、编程和多步推理等复杂任务的准确率，但会消耗更多 token 并增加延迟。

思考模型分为两类：

- **混合模型** — 可开关思考模式。Qwen3.5 系列默认开启；Qwen3、Qwen3-VL 和 Qwen3-Omni-Flash 默认关闭。Qwen3.5-Omni 不支持思考模式。通过 `enable_thinking=True/False` 切换：OpenAI 兼容在 `extra_body` 中设置，DashScope 作为直接参数设置。
- **纯思考模型** — QwQ 和 `-thinking` 变体始终启用思考，无法关闭。

在用户消息开头使用 `/think` 或 `/no_think` 可按轮次切换，无需修改请求参数。此方式仅适用于混合模型 — 纯思考模型（QwQ 和 `-thinking` 变体）无法关闭思考。

### 思考模式必须使用流式输出吗？

部分模型在 `enable_thinking=true` 时要求 `stream=true`。如果非流式调用返回 `parameter.enable_thinking only support stream call` 错误，请启用流式输出或设置 `enable_thinking=false`。

纯思考模型（QwQ、QVQ）无论思考设置如何，都只支持流式输出。参见[哪些模型必须使用流式输出？](#streaming)

DashScope API 在 `enable_thinking=true` 时还需设置 `incremental_output=true`，否则会返回错误。

### 思考模式如何计费？

思考 token（`reasoning_content`）按输出 token 价格计费。可设置 `thinking_budget` 为正整数来限制推理 token 上限；降低该值可减少费用，但可能影响复杂问题的推理质量。

批量处理对思考 token 和回答 token 均享受 50% 折扣。详见[定价](/developer-guides/getting-started/pricing)。

### 能否对终端用户隐藏思考过程？

可以。`reasoning_content` 和 `content` 是独立的字段。你可以在服务端记录或丢弃 `reasoning_content`，只将 `content` 返回给用户。

在启用思考的函数调用中，后续发送给模型的 assistant 消息必须包含 `reasoning_content` — 省略会降低准确率。这属于内部实现细节，不影响用户看到的内容。

---

<a id="function-calling" />

## 函数调用

**API**：[函数调用](/developer-guides/tool-calling/function-calling)

### 如何通过函数调用依次执行本地函数？

标准流程：

1. 发送用户消息和工具定义。
2. 模型返回 `tool_calls` 响应（此时没有最终答案）。
3. 使用提供的参数执行指定函数。
4. 将执行结果作为 `role: "tool"` 消息追加到消息数组。
5. 再次调用模型。重复以上步骤，直到响应中不再包含 `tool_calls`。
6. 最终响应（不含 `tool_calls`）即为答案。

仅当任务相互独立时使用 `parallel_tool_calls=True`。对于有依赖关系的任务（工具 A 的输入依赖工具 B 的输出），需串行执行：每次获取工具结果后发送给模型，等待下一个 `tool_calls` 响应后再执行下一个工具。

### 函数调用和内置工具有什么区别？

**函数调用**（`tools` 参数）允许你定义在应用中运行的自定义函数。模型返回结构化指令，由你的代码执行函数并返回结果。

**内置工具**（联网搜索、代码解释器、图片搜索）由平台提供。使用特定类型值将其作为工具定义传入即可，无需编写执行代码。详见[联网搜索](/developer-guides/tool-calling/web-search)、[代码解释器](/developer-guides/tool-calling/code-interpreter)。

工具描述计入输入 token，作为 prompt 的一部分计费。

### 能否通过函数调用依次调用两个本地函数？

可以 — 这就是标准流程。收到 `tool_calls` 响应后，执行函数，将结果作为 `role: "tool"` 消息发回，再次调用模型。模型返回下一个 `tool_calls` 响应。重复此过程直到没有 `tool_calls`。参见上方的函数调用流程。

---

<a id="batch" />

## 批量处理

**API**：[Batch API](/developer-guides/text-generation/batch)

### 什么时候用批量处理，什么时候用实时请求？

批量处理适合大规模离线任务（文档处理、数据集标注、评估流水线等），可接受数小时延迟。批量请求按**实时价格的 50%** 计费。

实时请求适合用户等待响应的交互场景。

### 批量处理的限制是什么？

| 限制项      | 值                    |
| -------- | -------------------- |
| 每个文件的请求数 | 50,000               |
| 文件大小     | 500 MB               |
| 单行大小     | 6 MB                 |
| 每个文件的模型数 | 1（所有请求必须使用同一模型）      |
| 完成时间窗口   | 24 小时 – 336 小时（14 天） |

支持的模型请参见 [Batch（文件输入）支持的模型](/developer-guides/text-generation/batch#支持的模型)。

### 如何获取批量处理结果？

1. 每 1–2 分钟轮询批次状态：使用 `client.batches.retrieve(batch_id)`（Python OpenAI SDK）或对应的 DashScope 接口。
2. 状态流转：`validating` → `in_progress` → `finalizing` → `completed`。
3. 状态变为 `completed` 后，使用 `client.files.content(output_file_id)` 下载结果。
4. 通过 `error_file_id` 单独下载失败请求的错误文件。

结果为 JSONL 格式，每行通过 `custom_id` 与原始请求对应。

批量折扣不与上下文缓存折扣或其他折扣叠加。只对成功请求计费。

---

<a id="models" />

## 模型

### Qwen 模型支持多少种语言？

Qwen3.5 和 Qwen3-VL 系列模型支持 33 种语言，包括中文、英文、日文、韩文、阿拉伯文、西班牙文、法文、葡萄牙文、德文、意大利文、俄文、越南文、泰文和印尼文。详见[模型选择](/developer-guides/getting-started/model-selection)了解各模型支持情况。

### qwen-plus-latest 具体对应哪个系列？

`qwen-plus-latest` 属于 Qwen3 系列，是 Qwen3 系列 Plus 档位模型的最新快照版本。

### 大语言模型参数是如何存储的？

开源模型可从 ModelScope 下载。模型结构定义在 JSON 配置文件中，学习到的权重以向量数据文件形式存储。使用 `transformers` 等 Python 库加载和解析。

### 模型能否与 MySQL 或 Hive 等结构化数据库集成？

标准 API 不直接支持。如需数据库集成，可使用函数调用：让模型生成 SQL，在应用中执行，然后将结果返回给模型。

---

<a id="api-sdk" />

## API 和 SDK

### 如何查看错误码信息？

详见[错误信息](/api-reference/preparation/error-messages)，包含完整的错误码列表、说明和解决方案。

### 如何安装 SDK？

千问AI平台支持 DashScope SDK（Python、Java）和 OpenAI SDK（Python、Node.js、Java、Go）。详见[安装 SDK](/api-reference/preparation/install-sdk)。

---

<a id="rate-limits" />

## 限流与性能

### 所有用户的文本生成速度一样吗？

不一样。生成速度受当前服务负载和请求并发量影响，用户无法自行配置。

### 触发限流后应该等多久？

等待时间取决于你的限流级别（RPM/RPS）。例如，120 RPM 限制（每秒 2 个请求）意味着在 0.2 秒内提交 2 个请求后，第 3 个会被限流。大约等待该秒的剩余时间后重试。建议使用指数退避策略提高稳定性。
