> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# PDF理解

> PDF文件通过VL模型解析

PDF理解功能使模型能够解析并理解PDF文档，提取文档中的文字与图片内容进行分析。您可以通过 OpenAI 兼容的 Chat Completions 接口或 DashScope 接口，以 URL 或 Base64 编码方式传入 PDF 文件。

<Note>
  暂不支持通过 Responses API 调用 PDF 理解功能。
</Note>

## 支持的模型

qwen3.8-max

## 快速开始

运行以下代码，向模型传入PDF文件。

获取[千问AI平台 API Key](/api-reference/preparation/api-key)并[配置环境变量](/api-reference/preparation/export-api-key-env)。

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python
      from openai import OpenAI
      import os

      client = OpenAI(
          # 若没有配置环境变量，请用千问AI平台 API Key 将下行替换为：api_key="sk-xxx"（不建议）,
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      completion = client.chat.completions.create(
          model="qwen3.8-max",
          messages=[
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "file",
                          "file": {
                              "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"
                          }
                      },
                      {
                          "type": "text",
                          "text": "总结一下这个PDF文档的内容"
                      }
                  ]
              }
          ],
          stream=True,
          stream_options={"include_usage": True}
      )

      for chunk in completion:
          if not chunk.choices:
              print(f"\nUsage: {chunk.usage}")
              continue
          delta = chunk.choices[0].delta
          if hasattr(delta, "content") and delta.content:
              print(delta.content, end="", flush=True)
      ```

      ```javascript Node.js
      import OpenAI from "openai";
      import process from 'process';

      const openai = new OpenAI({
          // 若没有配置环境变量，请用千问AI平台 API Key 将下行替换为：apiKey: "sk-xxx",
          apiKey: process.env.DASHSCOPE_API_KEY,
          baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
      });

      async function main() {
          const stream = await openai.chat.completions.create({
              model: 'qwen3.8-max',
              messages: [
                  {
                      role: 'user',
                      content: [
                          {
                              type: 'file',
                              file: {
                                  file_url: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf'
                              }
                          },
                          {
                              type: 'text',
                              text: '总结一下这个PDF文档的内容'
                          }
                      ]
                  }
              ],
              stream: true,
              stream_options: { include_usage: true }
          });

          for await (const chunk of stream) {
              if (!chunk.choices?.length) {
                  console.log('\nUsage:', chunk.usage);
                  continue;
              }
              const delta = chunk.choices[0].delta;
              if (delta.content) {
                  process.stdout.write(delta.content);
              }
          }
      }

      main();
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
          "model": "qwen3.8-max",
          "messages": [
              {
                  "role": "user",
                  "content": [
                      {
                          "type": "file",
                          "file": {
                              "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"
                          }
                      },
                      {
                          "type": "text",
                          "text": "总结一下这个PDF文档的内容"
                      }
                  ]
              }
          ],
          "stream": true,
          "stream_options": {
              "include_usage": true
          }
      }'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python
      import os
      from dashscope import MultiModalConversation
      import dashscope

      dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

      messages = [
          {
              "role": "user",
              "content": [
                  {
                      "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"
                  },
                  {
                      "text": "总结一下这个PDF文档的内容"
                  }
              ]
          }
      ]

      completion = MultiModalConversation.call(
          # 若没有配置环境变量，请用千问AI平台 API Key 将下行替换为：api_key = "sk-xxx",
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="qwen3.8-max",
          messages=messages,
          stream=True,
          incremental_output=True
      )

      for chunk in completion:
          message = chunk.output.choices[0].message
          if message.content:
              print(message.content[0]["text"], end="", flush=True)
      ```

      ```bash curl
      curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -H "X-DashScope-SSE: enable" \
      -d '{
          "model": "qwen3.8-max",
          "input": {
              "messages": [
                  {
                      "role": "user",
                      "content": [
                          {
                              "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260616/qmycjl/1506.02640v5.pdf"
                          },
                          {
                              "text": "总结一下这个PDF文档的内容"
                          }
                      ]
                  }
              ]
          },
          "parameters": {
              "incremental_output": true,
              "result_format": "message"
          }
      }'
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## 使用Base64输入

如果无法提供文件的URL地址，也可以将PDF文件以Base64编码字符串的形式传入。使用 `file_data` 时，`filename` 字段为必填项。

<Tabs>
  <Tab title="OpenAI 兼容">
    ```python Python
    import base64
    from openai import OpenAI
    import os

    client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 读取并编码PDF文件
    with open("report.pdf", "rb") as f:
        pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

    completion = client.chat.completions.create(
        model="qwen3.8-max",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "file",
                        "file": {
                            "file_data": f"data:application/pdf;base64,{pdf_base64}",
                            "filename": "report.pdf"
                        }
                    },
                    {
                        "type": "text",
                        "text": "这份报告的核心结论是什么？"
                    }
                ]
            }
        ]
    )

    print(completion.choices[0].message.content)
    ```
  </Tab>

  <Tab title="DashScope">
    ```python Python
    import base64
    import os
    from dashscope import MultiModalConversation
    import dashscope

    dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

    # 读取并编码PDF文件
    with open("report.pdf", "rb") as f:
        pdf_base64 = base64.b64encode(f.read()).decode("utf-8")

    messages = [
        {
            "role": "user",
            "content": [
                {
                    "file_data": f"data:application/pdf;base64,{pdf_base64}",
                    "filename": "report.pdf"
                },
                {
                    "text": "这份报告的核心结论是什么？"
                }
            ]
        }
    ]

    response = MultiModalConversation.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen3.8-max",
        messages=messages
    )

    print(response.output.choices[0].message.content[0]["text"])
    ```
  </Tab>
</Tabs>

## 请求参数

文件输入通过content数组中的元素指定，OpenAI兼容协议使用 `type: "file"` 类型，DashScope协议使用包含 `file_url`/`file_data` 的元素。

<Note>
  协议中 URL 部分仅支持字符串输入，不支持 list（数组）形式。
</Note>

**OpenAI兼容协议格式：**

| 参数            | 类型     | 是否必填  | 说明                                                                         |
| ------------- | ------ | ----- | -------------------------------------------------------------------------- |
| `file_url`    | string | 二选一必填 | 指定PDF文件的下载地址，和 `file_data` 二选一必填。                                          |
| `file_data`   | string | 二选一必填 | Base64格式的PDF文件输入，格式为 `data:application/pdf;base64,xxx`，和 `file_url` 二选一必填。 |
| `filename`    | string | 条件必填  | 文件名，使用 `file_data` 作为入参时必填。                                                |
| `file_format` | string | 否     | 文件格式，可选参数，当前仅支持 `pdf`，默认 `pdf`。                                            |

## 限制说明

| 项目      | 限制    |
| ------- | ----- |
| 单文件大小限制 | 150MB |
| 单文档页数限制 | 500页  |

<Note>
  PDF解析可能比普通文本请求耗时更长，首包超时时间最长为300秒，建议使用流式输出方式实时获取结果，避免长时间等待。
</Note>

## 计费说明

计费涉及以下方面：

- **模型调用费用**：PDF文件解析出的文字与图片会计入模型的输入Token，按照模型的标准输入价格计费。
- **文档解析费用**：按PDF文档解析的页数计费，0.02元/页。

## 错误码

如果调用失败，请参阅[错误码](/api-reference/preparation/error-messages)。
