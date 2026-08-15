> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 网页抓取

> 抓取 URL 内容作为上下文

<Tip>
  涉及数学计算或数据分析的任务，建议同时启用 `code_interpreter` 和 Web extractor，以提升准确性。
</Tip>

## 快速开始

通过 Responses API 调用 Web extractor 来摘要网页内容。以下示例使用 `web_search` 和 `web_extractor`，搭配 `qwen3.8-max` 的思考模式。

<Tabs>
  <Tab title="Python">
    ```python {15}
    import os
    from openai import OpenAI

    client = OpenAI(
      # 如果未配置环境变量，请替换为：api_key="sk-xxx"
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )

    response = client.responses.create(
      model="qwen3.8-max",
      input="请访问千问AI平台官方文档，找到代码解释器主题并进行总结",
      tools=[
        {"type": "web_search"},
        {"type": "web_extractor"}
      ],
      extra_body={
        "enable_thinking": True
      }
    )

    # 取消注释可查看中间输出
    # print(response.output)
    print("=" * 20 + "Response" + "=" * 20)
    print(response.output_text)

    # 打印工具调用次数
    usage = response.usage
    print("=" * 20 + "Tool Invocation Count" + "=" * 20)
    if hasattr(usage, 'x_tools') and usage.x_tools:
      print(f"Web Extractor invocations: {usage.x_tools.get('web_extractor', {}).get('count', 0)}")
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript {16}
    import OpenAI from "openai";
    import process from 'process';

    const openai = new OpenAI({
      // 如果未配置环境变量，请替换为：apiKey: "sk-xxx"
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    });

    async function main() {
      const response = await openai.responses.create({
        model: "qwen3.8-max",
        input: "请访问千问AI平台官方文档，找到代码解释器主题并进行总结",
        tools: [
          { type: "web_search" },
          { type: "web_extractor" }
        ],
        enable_thinking: true
      });

      console.log("====================Response====================");
      console.log(response.output_text);

      // 打印工具调用次数
      console.log("====================Tool Invocation Count====================");
      if (response.usage && response.usage.x_tools) {
        console.log(`Web Extractor invocations: ${response.usage.x_tools.web_extractor?.count || 0}`);
        console.log(`Web Search invocations: ${response.usage.x_tools.web_search?.count || 0}`);
      }
      // 取消注释可查看中间输出
      // console.log(JSON.stringify(response.output[0], null, 2));
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash {9}
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "qwen3.8-max",
      "input": "请访问千问AI平台官方文档，找到代码解释器主题并进行总结",
      "tools": [
        {"type": "web_search"},
        {"type": "web_extractor"}
      ],
      "enable_thinking": true
    }'
    ```
  </Tab>
</Tabs>

### 响应结构

响应包含模型生成的文本及工具使用的元数据。

| 字段                                  | 说明                                                                               |
| ----------------------------------- | -------------------------------------------------------------------------------- |
| `output_text`                       | 模型基于提取的网页内容生成的最终文本响应                                                             |
| `output[]`                          | 中间结果数组，包含 `web_extractor_call` 对象（每个对象含 `goal` 和 `output` 字段，分别表示抓取的 URL 和提取的内容） |
| `usage.x_tools.web_extractor.count` | 本次请求中 Web extractor 的调用次数                                                        |
| `usage.x_tools.web_search.count`    | 本次请求中 Web search 的调用次数                                                           |

## 工作原理

1. 在 API 请求的 `tools` 数组中添加 `web_extractor`（通常同时添加 `web_search`），并在 prompt 中引用 URL 或主题。
2. 模型自动判断需要抓取的页面，获取页面内容，并将其作为额外的输入 token 追加到上下文中。
3. 模型基于获取的内容生成响应。

提取的网页内容会增加输入 token 数，影响计费。详见[计费](#计费)。

## 使用场景

| 场景                 | 工具配置                               | 原因                                         |
| ------------------ | ---------------------------------- | ------------------------------------------ |
| 回答关于**特定 URL** 的问题 | `web_extractor`（可选搭配 `web_search`） | 模型抓取并阅读完整页面内容，而非仅搜索摘要                      |
| **主题研究**，搜索多个网页    | `web_search` + `web_extractor`     | `web_search` 查找相关页面；`web_extractor` 读取完整内容 |
| 快速事实查询（无特定 URL）    | 仅 `web_search`                     | 搜索摘要通常足够，更经济高效                             |

当需要模型阅读页面的实际内容（而非搜索结果摘要）时，使用 `web_extractor`。

## 调用方式

Web extractor 支持三种 API。Responses API 提供最精细的工具控制能力，建议新项目优先使用。

| API                      | 工具配置                                                    | 是否必须流式 | 备注           |
| ------------------------ | ------------------------------------------------------- | ------ | ------------ |
| **Responses API**（推荐）    | 在 `tools` 中添加 `web_search` 和 `web_extractor`            | 否      | 支持中间工具执行状态   |
| **Chat Completions API** | 设置 `enable_search: true`，`search_strategy: "agent_max"` | 是      | 不支持非流式       |
| **DashScope API**        | 设置 `enable_search: true`，`search_strategy: "agent_max"` | 是      | 不支持 Java SDK |

<Note>
  使用 `qwen3.8-max` 时，需将 `enable_thinking` 设为 `true`。
</Note>

<Tabs>
  <Tab title="Responses API">
    ```python
    response = client.responses.create(
      model="qwen3.8-max",
      input="总结 https://example.com/article 的内容",
      tools=[
        {"type": "web_search"},
        {"type": "web_extractor"}
      ],
      extra_body={
        "enable_thinking": True
      }
    )
    ```
  </Tab>

  <Tab title="Chat Completions API">
    ```python
    completion = client.chat.completions.create(
      model="qwen3-max",
      messages=[{"role": "user", "content": "总结 https://example.com/article 的内容"}],
      extra_body={
        "enable_thinking": True,
        "enable_search": True,
        "search_options": {"search_strategy": "agent_max"}
      },
      stream=True
    )
    ```
  </Tab>

  <Tab title="DashScope API">
    ```python
    from dashscope import Generation

    response = Generation.call(
      model="qwen3-max",
      messages=[{"role": "user", "content": "总结 https://example.com/article 的内容"}],
      enable_search=True,
      search_options={"search_strategy": "agent_max"},
      enable_thinking=True,
      result_format="message",
      stream=True,
      incremental_output=True
    )
    ```
  </Tab>
</Tabs>

## 流式输出 Web extractor 事件

<Tip>
  流式输出的通用概念（SSE 协议、启用方式、token 用量）请参阅[流式输出](/developer-guides/run-and-scale/streaming)。本节仅介绍 Web extractor 特有的事件类型。
</Tip>

网页抓取可能需要一定时间。使用流式输出可以实时接收推理步骤、工具调用和响应文本。Responses API 支持暴露每个工具调用的中间执行状态，是流式场景的最佳选择。

使用 Responses API 进行流式输出时，以下事件类型表示提取和生成流程的各个阶段：

| 事件类型                            | 说明                                                      |
| ------------------------------- | ------------------------------------------------------- |
| `response.reasoning_text.delta` | 模型思考过程的增量推理文本                                           |
| `response.output_item.done`     | 工具调用已完成。检查 `item.type` 是否为 `web_extractor_call` 以获取提取结果 |
| `response.output_text.delta`    | 增量响应文本                                                  |
| `response.completed`            | 响应完成。`usage` 字段包含工具调用次数                                 |

处理流中的 `web_extractor_call` 事件时，检查事件类型并读取其 `goal` 和 `output` 字段：

```python
for chunk in stream:
  if chunk.type == 'response.output_item.done':
    if hasattr(chunk, 'item') and chunk.item.type == 'web_extractor_call':
      print(f"已抓取: {chunk.item.goal}")
      print(f"内容: {chunk.item.output}")
  elif chunk.type == 'response.output_text.delta':
    print(chunk.delta, end='', flush=True)
  elif chunk.type == 'response.completed':
    usage = chunk.response.usage
    if hasattr(usage, 'x_tools') and usage.x_tools:
      print(f"Web Extractor 调用次数: {usage.x_tools.get('web_extractor', {}).get('count', 0)}")
```

## 支持的模型

### 推荐模型

**Responses API**

- 千问Max：qwen3.8-max、Qwen3.7-Max 系列
- 千问Plus：Qwen3.7-Plus 系列、Qwen3.6-Plus 系列、Qwen3.5-Plus 系列
- DeepSeek：deepseek-v4-pro-0813、deepseek-v4-flash、deepseek-v4-flash-0731

**Chat Completions API / DashScope**

- 千问Max（思考模式）：Qwen3-Max 系列
- 千问Plus：Qwen3.6-Plus 系列、Qwen3.5-Plus 系列

### 其他模型

以下模型也支持此工具调用，但效果不如推荐模型。

- 千问Flash：Qwen3.7-Flash 系列、Qwen3.6-Flash 系列、Qwen3.5-Flash 系列
- Qwen3.8开源系列
- Qwen3.6 开源系列（qwen3.6-27b 除外）
- Qwen3.5 开源系列

## 使用限制

- Web extractor 仅能获取公开可访问的页面。需要登录认证或付费的页面返回空内容。
- 过大的页面可能在添加到上下文窗口前被截断。
- 纯 JavaScript 渲染的动态内容可能无法完整获取。
- 提取的内容作为输入 token 计算，大页面会增加延迟和成本。

## 错误处理

提取失败时，模型不会抛出错误。响应输出中的 `web_extractor_call` 项会返回空或部分内容，模型基于已有上下文生成响应。

常见的失败场景：

| 场景                        | 行为                      |
| ------------------------- | ----------------------- |
| URL 不可达（404、500、DNS 解析失败） | 提取返回空内容；模型使用其他可用上下文生成响应 |
| 页面加载超时                    | 返回部分或空内容                |
| 非 HTML 内容（PDF、图片）         | 可能无法提取内容；模型回退到其他工具或通用知识 |

<Tip>
  要验证提取是否成功，可检查 `response.output` 中的 `web_extractor_call` 项，或查看 `usage.x_tools.web_extractor.count` 获取成功调用次数。
</Tip>

## 计费

Web extractor 的费用包含两部分：

<Note>
  以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
</Note>

| 组成部分                 | 详情                                                                                                   |
| -------------------- | ---------------------------------------------------------------------------------------------------- |
| **模型费用**             | 提取的网页内容追加到 prompt 中，增加输入 token 数，按模型标准 token 价格计费。详见[定价](/developer-guides/getting-started/pricing)。 |
| **联网搜索费用**           | 每 1,000 次调用 4 元。使用网页抓取需同时开启联网搜索，联网搜索会独立计费。                                                           |
| **Web extractor 费用** | 限时免费。                                                                                                |
