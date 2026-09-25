> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 前缀续写

> 从指定前缀继续生成内容

Partial Mode 从给定的前缀继续生成内容，确保模型输出与前缀无缝衔接。

## 工作原理

使用 Partial Mode 时，需要配置 `messages` 数组：将数组最后一条消息的 `role` 设为 `assistant`，在 `content` 中填入前缀内容，并在该消息中设置 `"partial": true` 参数。`messages` 格式如下：

```json
[
  {
    "role": "user",
    "content": "Complete this Fibonacci function. Do not add anything else."
  },
  {
    "role": "assistant",
    "content": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n",
    "partial": true
  }
]
```

模型会从指定前缀开始继续生成文本。

## 支持的模型

- **Qwen-Max 系列**
- **Qwen-Plus 系列**（非思考模式）
- **Qwen-Flash 系列**（非思考模式）
- **Qwen-Coder 系列**
- **Qwen-VL 系列** — qwen-vl-max 和 qwen-vl-plus 支持思考模式；qwen3-vl-plus 和 qwen3-vl-flash 仅支持非思考模式
- **Qwen-Turbo 系列**（非思考模式）
- **Qwen 开源系列** — Qwen3.5 MoE/dense 模型支持思考模式；Qwen3.5-35B-A3B、Qwen3 和 Qwen3-VL 开源模型仅支持非思考模式

模型 ID 和快照版本请参见[文本生成模型](/developer-guides/getting-started/text-generation-models)。

<Warning>
  思考模式不支持前缀续写。对于支持非思考模式的模型，请使用非思考模式；或选择仅支持非思考模式的模型系列。
</Warning>

## 快速开始

### 前提条件

[获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。如果您在子业务空间中，请确保超级管理员已[为您的业务空间授权模型访问](/developer-guides/administration/workspace)。

<Note>
  不支持 DashScope Java SDK。
</Note>

### 示例代码

以下示例使用 `qwen3-coder-plus` 补全一个 Python 函数。

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      # 1. 初始化客户端
      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )
      # 2. 定义待补全的代码前缀
      prefix = """def calculate_fibonacci(n):
        if n <= 1:
          return n
        else:
      """

      # 3. 发送 Partial Mode 请求
      # 注意：messages 数组的最后一条消息必须将 role 设为 "assistant"，并包含 "partial": True
      completion = client.chat.completions.create(
        model="qwen3-coder-plus",
        messages=[
          {"role": "user", "content": "Complete this Fibonacci function. Do not add anything else."},
          {"role": "assistant", "content": prefix, "partial": True},
        ],
      )

      # 4. 手动拼接前缀和模型生成的内容
      generated_code = completion.choices[0].message.content
      complete_code = prefix + generated_code

      print(complete_code)
      ```

      ```javascript Node.js
      import OpenAI from "openai";

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      // 定义待补全的代码前缀
      const prefix = `def calculate_fibonacci(n):
        if n <= 1:
          return n
        else:
      `;

      const completion = await openai.chat.completions.create({
        model: "qwen3-coder-plus",  // 使用代码模型
        messages: [
          { role: "user", content: "Complete this Fibonacci function. Do not add anything else." },
          { role: "assistant", content: prefix, partial: true }
        ],
      });

      // 手动拼接前缀和模型生成的内容
      const generatedCode = completion.choices[0].message.content;
      const completeCode = prefix + generatedCode;

      console.log(completeCode);
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3-coder-plus",
        "messages": [
          {
            "role": "user",
            "content": "Complete this Fibonacci function. Do not add anything else."
          },
          {
            "role": "assistant",
            "content": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n",
            "partial": true
          }
        ]
      }'
      ```
    </CodeGroup>

    **响应示例**

    <Note>
      输出内容可能因模型版本不同而有所差异。任何有效的 Fibonacci 实现均可接受。
    </Note>

    ```plaintext
    def calculate_fibonacci(n):
      if n <= 1:
        return n
      else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
    ```

    <Accordion title="完整 JSON 响应">
      ```json
      {
        "choices": [
          {
            "message": {
              "content": "        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
              "role": "assistant"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
          }
        ],
        "object": "chat.completion",
        "usage": {
          "prompt_tokens": 48,
          "completion_tokens": 19,
          "total_tokens": 67,
          "prompt_tokens_details": {
            "cache_type": "implicit",
            "cached_tokens": 0
          }
        },
        "created": 1756800231,
        "system_fingerprint": null,
        "model": "qwen3-coder-plus",
        "id": "chatcmpl-d103b1cf-4bda-942f-92d6-d7ecabfeeccb"
      }
      ```
    </Accordion>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      # 定义待补全的代码前缀
      prefix = """def calculate_fibonacci(n):
        if n <= 1:
          return n
        else:
      """

      messages = [
        {
          "role": "user",
          "content": "Complete this Fibonacci function. Do not add any other content."
        },
        {
          "role": "assistant",
          "content": prefix,
          "partial": True
        }
      ]

      response = dashscope.Generation.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model='qwen3-coder-plus',  # 使用代码模型
        messages=messages,
        result_format='message',
      )

      # 手动拼接前缀和模型生成的内容
      generated_code = response.output.choices[0].message.content
      complete_code = prefix + generated_code

      print(complete_code)
      ```

      ```bash curl
      curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3-coder-plus",
        "input":{
          "messages":[
            {
              "role": "user",
              "content": "Complete this Fibonacci function. Do not add anything else."
            },
            {
              "role": "assistant",
              "content": "def calculate_fibonacci(n):\n    if n <= 1:\n        return n\n    else:\n",
              "partial": true
            }
          ]
        },
        "parameters": {
          "result_format": "message"
        }
      }'
      ```
    </CodeGroup>

    **响应示例**

    <Note>
      输出内容可能因模型版本不同而有所差异。任何有效的 Fibonacci 实现均可接受。
    </Note>

    ```plaintext
    def calculate_fibonacci(n):
      if n <= 1:
        return n
      else:
        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
    ```

    <Accordion title="完整 JSON 响应">
      ```json
      {
        "output": {
          "choices": [
            {
              "message": {
                "content": "        return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)",
                "role": "assistant"
              },
              "finish_reason": "stop"
            }
          ]
        },
        "usage": {
          "total_tokens": 67,
          "output_tokens": 19,
          "input_tokens": 48,
          "prompt_tokens_details": {
            "cached_tokens": 0
          }
        },
        "request_id": "c61c62e5-cf97-90bc-a4ee-50e5e117b93f"
      }
      ```
    </Accordion>
  </Tab>
</Tabs>

## 使用场景

### 传入图片或视频

Qwen-VL 模型支持在包含图片或视频的请求中使用 Partial Mode。适用于生成商品描述、社交媒体文案、新闻稿件和创意文案等场景。

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
      )

      completion = client.chat.completions.create(
        model="qwen3-vl-plus",
        messages=[
          {
            "role": "user",
            "content": [
              {
                "type": "image_url",
                "image_url": {
                  "url": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
                },
              },
              {"type": "text", "text": "I want to post this on social media. Help me write a caption."},
            ],
          },
          {
            "role": "assistant",
            "content": "Today I discovered a hidden-gem café",
            "partial": True,
          },
        ],
      )
      print(completion.choices[0].message.content)
      ```

      ```javascript Node.js
      import OpenAI from "openai";

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      async function main() {
        const response = await openai.chat.completions.create({
          model: "qwen3-vl-plus",
          messages: [
            {
              role: "user",
              content: [
                {
                  type: "image_url",
                  image_url: {
                    "url": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
                  }
                },
                {
                  type: "text",
                  text: "I want to post this on social media. Help me write a caption."
                }
              ]
            },
            {
              role: "assistant",
              content: "Today I discovered a hidden-gem café",
              "partial": true
            }
          ]
        });
        console.log(response.choices[0].message.content);
      }

      main();
      ```

      ```bash curl
      curl -X POST 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "model": "qwen3-vl-plus",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "image_url",
                "image_url": {
                  "url": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
                }
              },
              {
                "type": "text",
                "text": "I want to post this on social media. Help me write a caption."
              }
            ]
          },
          {
            "role": "assistant",
            "content": "Today I discovered a hidden-gem café",
            "partial": true
          }
        ]
      }'
      ```
    </CodeGroup>

    **响应示例**

    ```plaintext
    — the tiramisu here is pure bliss! Every bite delivers perfect harmony between coffee and cream. Pure joy! #FoodShare #Tiramisu #CoffeeTime

    Hope you like this caption! Let me know if you need any changes.
    ```

    <Accordion title="完整 JSON 响应">
      ```json
      {
        "choices": [
          {
            "message": {
              "content": "— the tiramisu here is pure bliss! Every bite delivers perfect harmony between coffee and cream. Pure joy! #FoodShare #Tiramisu #CoffeeTime\n\nHope you like this caption! Let me know if you need any changes.",
              "role": "assistant"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
          }
        ],
        "object": "chat.completion",
        "usage": {
          "prompt_tokens": 282,
          "completion_tokens": 56,
          "total_tokens": 338,
          "prompt_tokens_details": {
            "cached_tokens": 0
          }
        },
        "created": 1756802933,
        "system_fingerprint": null,
        "model": "qwen3-vl-plus",
        "id": "chatcmpl-5780cbb7-ebae-9c63-b098-f8cc49e321f0"
      }
      ```
    </Accordion>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      messages = [
        {
          "role": "user",
          "content": [
            {
              "image": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"
            },
            {"text": "I want to post this on social media. Help me write a caption."},
          ],
        },
        {"role": "assistant", "content": "Today I discovered a hidden-gem café", "partial": True},
      ]

      response = dashscope.MultiModalConversation.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen3-vl-plus",
        messages=messages
      )

      print(response.output.choices[0].message.content[0]["text"])
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "model": "qwen3-vl-plus",
        "input":{
          "messages":[
            {"role": "user",
                   "content": [
                     {"image": "https://img.alicdn.com/imgextra/i3/O1CN01zFX2Bs1Q0f9pESgPC_!!6000000001914-2-tps-450-450.png"},
                     {"text": "I want to post this on social media. Help me write a caption."}]
            },
            {"role": "assistant",
                   "content": "Today I discovered a hidden-gem café",
                   "partial": true
            }
          ]
        }
      }'
      ```
    </CodeGroup>

    **响应示例**

    ```plaintext
    — the tiramisu here is pure bliss! Every bite delivers perfect harmony between coffee and cream. Pure joy! #FoodShare #Tiramisu #CoffeeTime

    Hope you like this caption! Let me know if you need any changes.
    ```

    <Accordion title="完整 JSON 响应">
      ```json
      {
        "output": {
          "choices": [
            {
              "message": {
                "content": [
                  {
                    "text": "— the tiramisu here is pure bliss! Every bite delivers perfect harmony between coffee and cream. Pure joy! #FoodShare #Tiramisu #CoffeeTime\n\nHope you like this caption! Let me know if you need any changes."
                  }
                ],
                "role": "assistant"
              },
              "finish_reason": "stop"
            }
          ]
        },
        "usage": {
          "total_tokens": 339,
          "input_tokens_details": {
            "image_tokens": 258,
            "text_tokens": 24
          },
          "output_tokens": 57,
          "input_tokens": 282,
          "output_tokens_details": {
            "text_tokens": 57
          },
          "image_tokens": 258
        },
        "request_id": "c741328c-23dc-9286-bfa7-626a4092ca09"
      }
      ```
    </Accordion>
  </Tab>
</Tabs>

### 续写未完成的输出

如果 `max_tokens` 参数值过小，大语言模型可能返回不完整的内容。您可以使用 Partial Mode 从截断处继续生成，确保输出语义完整。

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      def chat_completion(messages,max_tokens=None):
        response = client.chat.completions.create(
          model="qwen3.7-plus",
          messages=messages,
          max_tokens=max_tokens
        )
        print(f"### 停止生成的原因: {response.choices[0].finish_reason}")

        return response.choices[0].message.content

      # 示例用法
      messages = [{"role": "user", "content": "Write a short sci-fi story"}]

      # 第一次调用，将 max_tokens 设为 40
      first_content = chat_completion(messages, max_tokens=40)
      print(first_content)
      # 将第一次响应作为 assistant 消息添加，并设置 partial=True
      messages.append({"role": "assistant", "content": first_content, "partial": True})

      # 第二次调用
      second_content = chat_completion(messages)
      print("### 完整内容:")
      print(first_content+second_content)
      ```

      ```javascript Node.js
      import OpenAI from "openai";

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      async function chatCompletion(messages, maxTokens = null) {
        const completion = await openai.chat.completions.create({
          model: "qwen3.7-plus",
          messages: messages,
          max_tokens: maxTokens
        });

        console.log(`### 停止生成的原因: ${completion.choices[0].finish_reason}`);
        return completion.choices[0].message.content;
      }

      // 示例用法
      async function main() {
        let messages = [{"role": "user", "content": "Write a short sci-fi story"}];

        try {
          // 第一次调用，将 max_tokens 设为 40
          const firstContent = await chatCompletion(messages, 40);
          console.log(firstContent);

          // 将第一次响应作为 assistant 消息添加，并设置 partial=true
          messages.push({"role": "assistant", "content": firstContent, "partial": true});

          // 第二次调用
          const secondContent = await chatCompletion(messages);
          console.log("### 完整内容:");
          console.log(firstContent + secondContent);

        } catch (error) {
          console.error('执行出错:', error);
        }
      }

      // 运行示例
      main();
      ```
    </CodeGroup>

    **响应示例**

    `length` 表示已达到 `max_tokens` 限制。`stop` 表示模型自然生成完毕或遇到了 `stop` 参数中定义的停止词。

    ```plaintext
    ### 停止生成的原因: length
    **"The End of Memory"**

    In the distant future, Earth is no longer fit for human life. The atmosphere is polluted, oceans are dry, and cities lie in ruins. Humans migrated to a habitable planet named "Eden," with blue skies, fresh air, and endless resources.

    However, Eden is not a true paradise. It holds no human history, no past, and no memory.

    ...
    **"If we forget who we are, are we still human?"**

    — End —
    ```
  </Tab>

  <Tab title="DashScope">
    ```python
    import os
    import dashscope
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    # qwen3.7-plus 和 qwen3.5-plus 使用 MultiModalConversation。
    # 纯文本模型（如 qwen-plus 和 qwen3-max）请改用 dashscope.Generation.call。
    def chat_completion(messages, max_tokens=None):
      response = dashscope.MultiModalConversation.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model='qwen3.7-plus',
        messages=messages,
        max_tokens=max_tokens,
      )

      print(f"### 停止生成的原因: {response.output.choices[0].finish_reason}")
      return response.output.choices[0].message.content[0]["text"]

    # 示例用法
    messages = [{"role": "user", "content": [{"text": "Write a short sci-fi story"}]}]

    # 第一次调用，将 max_tokens 设为 40
    first_content = chat_completion(messages, max_tokens=40)
    print(first_content)

    # 将第一次响应作为 assistant 消息添加，并设置 partial=True
    messages.append({"role": "assistant", "content": first_content, "partial": True})

    # 第二次调用
    second_content = chat_completion(messages)
    print("### 完整内容:")
    print(first_content + second_content)
    ```

    **响应示例**

    ```plaintext
    ### 停止生成的原因: length
    Title: **"Origami Time"**
    ---

    In 2179, humanity finally mastered time travel. But this technology did not rely on massive machines or complex energy fields. It relied on paper.

    A single sheet of paper.

    It was called "Origami Time," made from an unknown alien material. Scientists could not explain how it worked. They only knew that drawing a scene on the paper and folding it in a specific way opened a door to the past or future.

    ...

    "You are not the key to time. You are just a reminder that our future is always in our hands."

    Then I tore it into pieces.

    ---

    **(End)**
    ```
  </Tab>
</Tabs>

## 计费说明

Partial Mode 按输入 token 和输出 token 计费。前缀内容计入输入 token。

## 错误码

调用失败时，请参见[错误信息](/api-reference/preparation/error-messages)。
