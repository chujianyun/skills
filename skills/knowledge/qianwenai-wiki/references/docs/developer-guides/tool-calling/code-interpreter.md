> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 代码解释器

> 在沙箱中运行 Python 代码

代码解释器允许模型在对话过程中，于安全沙箱内编写并执行 Python 代码。当模型遇到需要计算的任务（如数学运算、数据分析或图表生成）时，会自动生成代码、执行并将结果整合到回复中。

## 快速开始

以下示例展示了完整的代码解释器请求及输出。

<Tabs>
  <Tab title="Responses API">
    <CodeGroup>
      ```python Python {12}
      import os
      from openai import OpenAI

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
      )

      response = client.responses.create(
        model="qwen3-max-2026-01-23",
        input="12 的 3 次方是多少？",
        tools=[{"type": "code_interpreter"}],
        extra_body={"enable_thinking": True}
      )

      print(response.output_text)
      print(response.usage)
      ```

      ```javascript Node.js {13}
      import OpenAI from "openai";
      import process from 'process';

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      async function main() {
        const response = await openai.responses.create({
          model: "qwen3-max-2026-01-23",
          input: "12 的 3 次方是多少？",
          tools: [{ type: "code_interpreter" }],
          enable_thinking: true
        });

        console.log(response.output_text);
        console.log(response.usage);
      }

      main();
      ```

      ```bash curl {7}
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3-max-2026-01-23",
        "input": "12 的 3 次方是多少？",
        "tools": [{"type": "code_interpreter"}],
        "enable_thinking": true
      }'
      ```
    </CodeGroup>

    **响应示例**

    ```plaintext
    12 的 3 次方等于 **1728**。

    计算过程：
    12^3 = 12 x 12 x 12 = 144 x 12 = 1728
    ```
  </Tab>

  <Tab title="Chat Completions">
    <Note>
      Chat Completions API 不会返回解释器执行的代码。
    </Note>

    ```bash curl {12}
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "qwen3-max",
      "messages": [
        {
          "role": "user",
          "content": "123 的 21 次方是多少？"
        }
      ],
      "enable_code_interpreter": true,
      "enable_thinking": true,
      "stream": true
    }'
    ```

    **响应示例**

    ```plaintext
    123 的 21 次方是：77269364466549865653073473388030061522211723
    ```
  </Tab>

  <Tab title="DashScope">
    <Note>
      不支持 Java SDK。
    </Note>

    <CodeGroup>
      ```python Python {10}
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      response = dashscope.Generation.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen3-max",
        messages=[{"role": "user", "content": "123 的 21 次方是多少？"}],
        enable_code_interpreter=True,
        enable_thinking=True,
        result_format="message",
        stream=True
      )

      for chunk in response:
        print(chunk["output"])
      ```

      ```bash curl {16}
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -H "X-DashScope-SSE: enable" \
      -d '{
        "model": "qwen3-max",
        "input":{
          "messages":[
            {
              "role": "user",
              "content": "123 的 21 次方是多少？"
            }
          ]
        },
        "parameters": {
          "enable_code_interpreter": true,
          "enable_thinking": true,
          "result_format": "message"
        }
      }'
      ```
    </CodeGroup>

    **响应示例**

    ```plaintext
    123 的 21 次方是：77269364466549865653073473388030061522211723
    ```
  </Tab>
</Tabs>

## 工作原理

启用后，模型按以下阶段处理每个请求：

<Steps>
  <Step title="思考">
    模型分析请求，确定解题方法。
  </Step>

  <Step title="代码执行">
    模型在沙箱中生成并执行 Python 代码。
  </Step>

  <Step title="结果处理">
    模型处理执行结果，确定后续步骤。
  </Step>

  <Step title="生成回复">
    模型生成自然语言回复。
  </Step>
</Steps>

<Note>
  步骤 2 和 3 在单次请求中可能重复执行多次。
</Note>

## 支持的模型

### 推荐模型

**Responses API**

- 千问Max：qwen3.8-max、Qwen3.7-Max 系列
- 千问Plus：Qwen3.7-Plus 系列、Qwen3.6-Plus 系列、Qwen3.5-Plus 系列
- Qwen3.8开源系列
- DeepSeek：deepseek-v4-pro-0813、deepseek-v4-flash、deepseek-v4-flash-0731

**Chat Completions API / DashScope**

- 千问Max（思考模式）：Qwen3-Max 系列（需要启用[思考模式](/developer-guides/text-generation/thinking)）
- 千问Plus：Qwen3.5-Plus 系列

### 其他模型

以下模型也支持此工具调用，但效果不如推荐模型。

- 千问Flash：Qwen3.7-Flash 系列、Qwen3.6-Flash 系列、Qwen3.5-Flash 系列
- Qwen3.6 开源系列（qwen3.6-27b 除外）
- Qwen3.5 开源系列

## 获取执行的代码

**DashScope** API 在每个流式数据块的 `tool_info` 字段中返回解释器执行的代码。每个条目包含代码字符串和值为 `code_interpreter` 的 `type` 字段：

```json
"tool_info": [
  {
    "code_interpreter": {"code": "123**21"},
    "type": "code_interpreter"
  }
]
```

当模型在单次请求中多次调用解释器时，`tool_info` 会累积所有调用记录。总调用次数可通过 `usage.plugins` 获取：

```json
"plugins": {"code_interpreter": {"count": 2}}
```

<Note>
  Chat Completions API 不返回执行的代码。如需查看生成的代码，请使用 Responses API 或 DashScope API。
</Note>

## 使用限制

- **必须使用流式输出**（Chat Completions 和 DashScope）：代码解释器仅支持流式模式（`stream: true`），非流式请求会返回错误。Responses API 无此限制。

- 代码解释器与 [function calling](/developer-guides/tool-calling/function-calling) 互斥，不能同时启用。

  <Warning>
    同时启用两者会报错。
  </Warning>

- 启用代码解释器后，单次请求会触发多次模型推理。`usage` 字段汇总了所有推理的 Token 消耗。

## 计费

代码解释器**限时免费**，但会增加 Token 消耗。
