> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 结构化输出

> 让模型稳定返回合法 JSON，并可通过 JSON Schema 精确约束输出结构

执行信息抽取或结构化数据生成任务时，模型可能返回多余文本（如 ` ```json ` 包裹符），导致下游解析失败。开启结构化输出可确保模型输出标准格式的 JSON 字符串；使用 JSON Schema 模式还能精确控制输出的结构和类型，无需额外校验或重试。

## 两种模式

| 特性                   | JSON Object 模式                    | JSON Schema 模式                                                  |
| -------------------- | --------------------------------- | --------------------------------------------------------------- |
| 输出合法 JSON            | 是                                 | 是                                                               |
| 严格遵循 Schema          | 否                                 | 是                                                               |
| 支持模型                 | 千问大部分模型、Kimi、GLM、DeepSeek、Stepfun | 仅支持部分模型                                                         |
| `response_format` 设置 | `{"type": "json_object"}`         | `{"type": "json_schema", "json_schema": {...}, "strict": true}` |
| 提示词要求                | 必须包含 "JSON"                       | 建议明确说明                                                          |
| 适用场景                 | 灵活的 JSON 输出                       | 精确的结构验证                                                         |

**JSON Object 模式**：确保输出为标准格式的 JSON 字符串，但不保证符合特定结构。使用方式：

1. 将请求体中的 `response_format` 参数设置为 `{"type": "json_object"}`。
2. System Message 或 User Message 中包含 "JSON" 关键词（不区分大小写），否则会报错：`'messages' must contain the word 'json' in some form, to use 'response_format' of type 'json_object'.`

**JSON Schema 模式**：确保输出内容为指定的结构。将 `response_format` 设置为 `{"type": "json_schema", "json_schema": {...}, "strict": true}`。

<Note>
  JSON Schema 模式下，提示词无需包含 "JSON" 关键词。
</Note>

## 支持的模型

### JSON Object

<Accordion title="展开查看完整模型列表">
  #### 千问

  **文本生成模型**

  - **千问 Max**：Qwen3.8-Max 系列、Qwen3.7-Max 系列
  - **千问 Max**（非思考模式）：Qwen3.6-Max 系列、Qwen3-Max 系列、Qwen-Max 系列
  - **千问 Plus**：Qwen3.7-Plus 系列
  - **千问 Plus**（非思考模式）：Qwen3.6-Plus 系列、Qwen3.5-Plus 系列、Qwen-Plus 系列
  - **千问 Flash**：Qwen3.7-Flash 系列
  - **千问 Flash**（非思考模式）：Qwen3.6-Flash 系列、Qwen3.5-Flash 系列、Qwen-Flash 系列
  - **千问 Turbo**（非思考模式）：Qwen-Turbo 系列
  - **千问 Coder**：Qwen3-Coder 系列
  - **千问 Long**：Qwen-Long 系列
  - **开源系列**：Qwen3.8 开源系列
  - **开源系列**（非思考模式）：Qwen3.6 开源系列、Qwen3.5 开源系列、Qwen3 开源系列
  - **开源系列**：Qwen3-Coder 开源系列、Qwen2.5 开源系列（不含 math 与 coder 模型）

  **多模态模型**（非思考模式）

  - **千问 VL**：Qwen3-VL-Plus 系列、Qwen3-VL-Flash 系列、Qwen-VL-Max 系列（不包括最新版与快照版模型）、Qwen-VL-Plus 系列（不包括最新版与快照版模型）
  - **千问 Omni**：Qwen3.5-Omni-Plus 系列
  - **开源系列**：Qwen3-VL 开源系列

  #### Kimi

  **千问AI平台部署**

  - `kimi-k2-thinking`

  **月之暗面部署**

  - `kimi/kimi-k3`、`kimi/kimi-k2.7-code-highspeed`、`kimi/kimi-k2.7-code`、`kimi/kimi-k2.6`、`kimi/kimi-k2.5`

  #### DeepSeek

  **千问AI平台部署**

  - `deepseek-v4-pro-0813`、`deepseek-v4-pro`、`deepseek-v4-flash`

  **快手万擎部署**

  - `vanchin/deepseek-v3.2-think`、`vanchin/deepseek-v3`、`vanchin/deepseek-ocr`

  #### GLM

  - `glm-5.1`、`glm-4.5`、`glm-4.5-air`
  - 非思考模式：`glm-5`、`glm-4.7`、`glm-4.6`

  #### Stepfun

  - 混合思考模式：`stepfun/step-3.7-flash`
</Accordion>

<Note>
  标注为"非思考模式"的模型，在思考模式下将 `response_format` 设置为 `{"type": "json_object"}` 不会报错，但结构化输出可能失效。如需稳定获取标准 JSON，请参见[常见问题](#常见问题)。
</Note>

### JSON Schema

Qwen3.8-Max 系列、Qwen3.7-Max 系列、Qwen3.7-Plus 系列。

## 快速开始

以从个人简介中抽取信息为例，演示 JSON Object 模式的基本用法。

<Info>
  调用前需先[获取 API Key](/api-reference/preparation/api-key) 并[配置到环境变量](/api-reference/preparation/export-api-key-env)。通过 OpenAI SDK 或 DashScope SDK 调用还需[安装 SDK](/api-reference/preparation/install-sdk)。
</Info>

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python {16}
      from openai import OpenAI
      import os

      client = OpenAI(
        # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      completion = client.chat.completions.create(
        model="qwen3.8-max",
        messages=[
          {"role": "system", "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"},
          {"role": "user", "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"},
        ],
        response_format={"type": "json_object"},
      )
      json_string = completion.choices[0].message.content
      print(json_string)
      ```

      ```javascript Node.js {15}
      import OpenAI from "openai";

      const openai = new OpenAI({
        // 若没有配置环境变量，请将下行替换为：apiKey: "sk-xxx"
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      const completion = await openai.chat.completions.create({
        model: "qwen3.8-max",
        messages: [
          { role: "system", content: "请抽取用户的姓名与年龄信息，以JSON格式返回" },
          { role: "user", content: "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游" }
        ],
        response_format: { type: "json_object" }
      });
      const jsonString = completion.choices[0].message.content;
      console.log(jsonString);
      ```

      ```bash curl {10}
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3.8-max",
        "messages": [
          {"role": "system", "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"},
          {"role": "user", "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}
        ],
        "response_format": {"type": "json_object"}
      }'
      ```
    </CodeGroup>

    SDK 返回结果：

    ```json
    {
      "姓名": "刘五",
      "年龄": 34
    }
    ```

    <Accordion title="curl 完整响应">
      ```json
      {
        "choices": [
          {
            "message": {
              "role": "assistant",
              "content": "{\"姓名\":\"刘五\",\"年龄\":34}"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
          }
        ],
        "object": "chat.completion",
        "usage": {
          "prompt_tokens": 207,
          "completion_tokens": 20,
          "total_tokens": 227,
          "prompt_tokens_details": {
            "cached_tokens": 0
          }
        },
        "created": 1756455080,
        "system_fingerprint": null,
        "model": "qwen3.8-max",
        "id": "chatcmpl-624b665b-fb93-99e7-9ebd-bb6d86d314d2"
      }
      ```
    </Accordion>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python {16}
      import os
      import dashscope

      dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

      messages = [
        {"role": "system", "content": [{"text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]},
        {"role": "user", "content": [{"text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}]},
      ]

      response = dashscope.MultiModalConversation.call(
        # 若没有配置环境变量，请将下行替换为：api_key="sk-xxx"
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model="qwen3.8-max",
        messages=messages,
        response_format={'type': 'json_object'},
      )
      json_string = response.output.choices[0].message.content[0]["text"]
      print(json_string)
      ```

      ```java Java {35}
      // DashScope Java SDK 版本需要不低于 2.21.4
      import java.util.Arrays;
      import java.util.Collections;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.common.ResponseFormat;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;

      public class Main {
        static {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        }

        public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
          MultiModalConversation conv = new MultiModalConversation();
          MultiModalMessage systemMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
              .content(Arrays.asList(
                  Collections.singletonMap("text", "请抽取用户的姓名与年龄信息，以JSON格式返回"))).build();
          MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
              .content(Arrays.asList(
                  Collections.singletonMap("text", "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"))).build();
          ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
          MultiModalConversationParam param = MultiModalConversationParam.builder()
              // 若没有配置环境变量，请将下行替换为：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen3.8-max")
              .messages(Arrays.asList(systemMessage, userMessage))
              .responseFormat(jsonMode)
              .build();
          MultiModalConversationResult result = conv.call(param);
          System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
        }

        public static void main(String[] args) {
          try {
            simpleMultiModalConversationCall();
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
        }
      }
      ```

      ```bash curl {13}
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3.8-max",
        "input": {
          "messages": [
            {"role": "system", "content": [{"text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]},
            {"role": "user", "content": [{"text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}]}
          ]
        },
        "parameters": {
          "response_format": {
            "type": "json_object"
          }
        }
      }'
      ```
    </CodeGroup>

    SDK 返回结果：

    ```json
    {
      "姓名": "刘五",
      "年龄": 34
    }
    ```

    <Accordion title="curl 完整响应">
      ```json
      {
        "output": {
          "choices": [
            {
              "finish_reason": "stop",
              "message": {
                "role": "assistant",
                "content": [
                  {
                    "text": "{\n  \"姓名\": \"刘五\",\n  \"年龄\": 34\n}"
                  }
                ]
              }
            }
          ]
        },
        "usage": {
          "total_tokens": 72,
          "output_tokens": 18,
          "input_tokens": 54,
          "cached_tokens": 0
        },
        "request_id": "xxx-xxx-xxx-xxx-xxx"
      }
      ```
    </Accordion>
  </Tab>
</Tabs>

## 从图片和视频中提取结构化数据

多模态模型同样支持对图像和视频数据进行结构化输出。通过 JSON Object 模式，可以从视觉内容中提取结构化数据，例如票据字段、图像中的目标位置或视频中的事件信息。

<Note>
  图片、视频的文件限制请参见[图像与视频理解](/developer-guides/multimodal/vision)。
</Note>

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python {29}
      import os
      from openai import OpenAI

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      completion = client.chat.completions.create(
        model="qwen3.8-max",
        messages=[
          {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."}],
          },
          {
            "role": "user",
            "content": [
              {
                "type": "image_url",
                "image_url": {
                  "url": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"
                },
              },
              {"type": "text", "text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"},
            ],
          },
        ],
        response_format={"type": "json_object"},
      )
      json_string = completion.choices[0].message.content
      print(json_string)
      ```

      ```javascript Node.js {30}
      import OpenAI from "openai";

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      async function main() {
        const response = await openai.chat.completions.create({
          model: "qwen3.8-max",
          messages: [
            {
              role: "system",
              content: [{ type: "text", text: "You are a helpful assistant." }]
            },
            {
              role: "user",
              content: [
                {
                  type: "image_url",
                  image_url: { url: "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg" }
                },
                {
                  type: "text",
                  text: "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"
                }
              ]
            }
          ],
          response_format: { type: "json_object" }
        });
        console.log(response.choices[0].message.content);
      }

      main()
      ```

      ```bash curl {16}
      curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json' \
      --data '{
        "model": "qwen3.8-max",
        "messages": [
          {"role":"system","content":[{"type": "text", "text": "You are a helpful assistant."}]},
          {
            "role": "user",
            "content": [
              {"type": "image_url", "image_url": {"url": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"}},
              {"type": "text", "text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"}
            ]
          }
        ],
        "response_format": {"type": "json_object"}
      }'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python {24}
      import os
      import dashscope

      dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

      messages = [
        {
          "role": "system",
          "content": [{"text": "You are a helpful assistant."}]
        },
        {
          "role": "user",
          "content": [
            {"image": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"},
            {"text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"}
          ]
        }
      ]

      response = dashscope.MultiModalConversation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3.8-max',
        messages=messages,
        response_format={'type': 'json_object'},
      )
      json_string = response.output.choices[0].message.content[0]["text"]
      print(json_string)
      ```

      ```java Java {35}
      // DashScope Java SDK 版本需要不低于 2.21.4
      import java.util.Arrays;
      import java.util.Collections;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.common.ResponseFormat;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;

      public class Main {
        static {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        }

        public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
          MultiModalConversation conv = new MultiModalConversation();
          MultiModalMessage systemMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
              .content(Arrays.asList(
                  Collections.singletonMap("text", "You are a helpful assistant."))).build();
          MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
              .content(Arrays.asList(
                  Collections.singletonMap("image", "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"),
                  Collections.singletonMap("text", "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"))).build();
          ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
          MultiModalConversationParam param = MultiModalConversationParam.builder()
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen3.8-max")
              .messages(Arrays.asList(systemMessage, userMessage))
              .responseFormat(jsonMode)
              .build();
          MultiModalConversationResult result = conv.call(param);
          System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
        }

        public static void main(String[] args) {
          try {
            simpleMultiModalConversationCall();
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
        }
      }
      ```

      ```bash curl {19}
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "model": "qwen3.8-max",
        "input": {
          "messages": [
            {"role": "system", "content": [{"text": "You are a helpful assistant."}]},
            {
              "role": "user",
              "content": [
                {"image": "http://duguang-labelling.oss-cn-shanghai.aliyuncs.com/demo_ocr/receipt_zh_demo.jpg"},
                {"text": "提取图中ticket(数组类型，包括 travel_date、trains、seat_num、arrival_site、price)和 invoice 的信息（数组类型，包括 invoice_code 和 invoice_number ），请输出包含 ticket 和 invoice 数组的JSON"}
              ]
            }
          ]
        },
        "parameters": {
          "response_format": {"type": "json_object"}
        }
      }'
      ```
    </CodeGroup>
  </Tab>
</Tabs>

返回结果：

```json
{
  "ticket": [
    {
      "travel_date": "2013-06-29",
      "trains": "流水",
      "seat_num": "371",
      "arrival_site": "开发区",
      "price": "8.00"
    }
  ],
  "invoice": [
    {
      "invoice_code": "221021325353",
      "invoice_number": "10283819"
    }
  ]
}
```

## 思考模型的结构化输出

启用[思考模式](/developer-guides/text-generation/thinking)后，模型会先进行推理再生成 JSON，输出结果通常比非思考模式更准确。思考模式下需开启流式输出。

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python {17,20}
      from openai import OpenAI
      import os

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      messages = [
        {"role": "system", "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"},
        {"role": "user", "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"},
      ]

      completion = client.chat.completions.create(
        model="qwen3.8-max",
        messages=messages,
        extra_body={"enable_thinking": True},
        stream=True,
        stream_options={"include_usage": True},
        response_format={"type": "json_object"},
      )

      reasoning_content = ""  # 完整思考过程
      answer_content = ""     # 完整回复
      is_answering = False    # 是否进入回复阶段

      print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
      for chunk in completion:
        if not chunk.choices:
          print("\nUsage:")
          print(chunk.usage)
          continue
        delta = chunk.choices[0].delta
        # 只收集思考内容
        if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
          if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
          reasoning_content += delta.reasoning_content
        # 收到 content，开始进行回复
        if hasattr(delta, "content") and delta.content:
          if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
          print(delta.content, end="", flush=True)
          answer_content += delta.content
      ```

      ```javascript Node.js {23,24}
      import OpenAI from "openai";
      import process from 'process';

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
      });

      let reasoningContent = '';
      let answerContent = '';
      let isAnswering = false;

      async function main() {
        try {
          const messages = [
            { role: "system", content: "请抽取用户的姓名与年龄信息，以JSON格式返回" },
            { role: "user", content: "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游" }
          ];
          const stream = await openai.chat.completions.create({
            model: 'qwen3.8-max',
            messages,
            stream: true,
            enable_thinking: true,
            response_format: { type: 'json_object' }
          });
          console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');
          for await (const chunk of stream) {
            if (!chunk.choices?.length) {
              console.log('\nUsage:');
              console.log(chunk.usage);
              continue;
            }
            const delta = chunk.choices[0].delta;
            // 只收集思考内容
            if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
              if (!isAnswering) {
                process.stdout.write(delta.reasoning_content);
              }
              reasoningContent += delta.reasoning_content;
            }
            // 收到 content，开始进行回复
            if (delta.content !== undefined && delta.content) {
              if (!isAnswering) {
                console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
                isAnswering = true;
              }
              process.stdout.write(delta.content);
              answerContent += delta.content;
            }
          }
        } catch (error) {
          console.error('Error:', error);
        }
      }

      main();
      ```

      ```bash curl {12,13}
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3.8-max",
        "messages": [
          {"role": "system", "content": "请抽取用户的姓名与年龄信息，以JSON格式返回"},
          {"role": "user", "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}
        ],
        "stream": true,
        "stream_options": {"include_usage": true},
        "enable_thinking": true,
        "response_format": {"type": "json_object"}
      }'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python {15,16}
      import os
      import dashscope

      dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

      messages = [
        {"role": "system", "content": [{"text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]},
        {"role": "user", "content": [{"text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}]},
      ]

      completion = dashscope.MultiModalConversation.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen3.8-max",
        messages=messages,
        enable_thinking=True,
        response_format={"type": "json_object"},
        stream=True,
        incremental_output=True,
      )

      reasoning_content = ""  # 完整思考过程
      answer_content = ""     # 完整回复
      is_answering = False    # 是否结束思考过程并开始回复

      print("=" * 20 + "思考过程" + "=" * 20)
      for chunk in completion:
        message = chunk.output.choices[0].message
        # 如果思考过程与回复皆为空，则忽略
        if not message.content and message.reasoning_content == "":
          continue
        # 如果当前为思考过程
        if message.reasoning_content != "" and not message.content:
          print(message.reasoning_content, end="", flush=True)
          reasoning_content += message.reasoning_content
        # 如果当前为回复
        elif message.content:
          if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20)
            is_answering = True
          print(message.content[0]["text"], end="", flush=True)
          answer_content += message.content[0]["text"]
      ```

      ```java Java {57,60}
      // DashScope Java SDK 版本需要不低于 2.22.1
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.ResponseFormat;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import io.reactivex.Flowable;
      import java.util.Arrays;
      import java.util.Collections;
      import java.util.List;
      import java.util.Map;
      import com.alibaba.dashscope.utils.Constants;
      import org.slf4j.Logger;
      import org.slf4j.LoggerFactory;

      public class Main {
        static {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        }

        private static final Logger logger = LoggerFactory.getLogger(Main.class);
        private static StringBuilder reasoningContent = new StringBuilder();
        private static StringBuilder finalContent = new StringBuilder();
        private static boolean isFirstPrint = true;

        private static void handleResult(MultiModalConversationResult message) {
          String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
          List<Map<String, Object>> content = message.getOutput().getChoices().get(0).getMessage().getContent();
          if (reasoning != null && !reasoning.isEmpty()) {
            reasoningContent.append(reasoning);
            if (isFirstPrint) {
              System.out.println("====================思考过程====================");
              isFirstPrint = false;
            }
            System.out.print(reasoning);
          }
          if (content != null && !content.isEmpty()) {
            String text = (String) content.get(0).get("text");
            finalContent.append(text);
            if (!isFirstPrint) {
              System.out.println("\n====================完整回复====================");
              isFirstPrint = true;
            }
            System.out.print(text);
          }
        }

        private static MultiModalConversationParam buildParam(List<MultiModalMessage> msgs) {
          ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
          return MultiModalConversationParam.builder()
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen3.8-max")
              .enableThinking(true)
              .incrementalOutput(true)
              .messages(msgs)
              .responseFormat(jsonMode)
              .build();
        }

        public static void streamCall(MultiModalConversation conv, List<MultiModalMessage> msgs)
            throws NoApiKeyException, ApiException, UploadFileException {
          MultiModalConversationParam param = buildParam(msgs);
          Flowable<MultiModalConversationResult> result = conv.streamCall(param);
          result.blockingForEach(message -> handleResult(message));
        }

        public static void main(String[] args) {
          try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage systemMsg = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "请抽取用户的姓名与年龄信息，以JSON格式返回"))).build();
            MultiModalMessage userMsg = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"))).build();
            List<MultiModalMessage> msgs = Arrays.asList(systemMsg, userMsg);
            streamCall(conv, msgs);
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            logger.error("An exception occurred: {}", e.getMessage());
          }
        }
      }
      ```

      ```bash curl {14,16}
      curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -H "X-DashScope-SSE: enable" \
      -d '{
        "model": "qwen3.8-max",
        "input": {
          "messages": [
            {"role": "system", "content": [{"text": "请抽取用户的姓名与年龄信息，以JSON格式返回"}]},
            {"role": "user", "content": [{"text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}]}
          ]
        },
        "parameters": {
          "enable_thinking": true,
          "incremental_output": true,
          "response_format": {"type": "json_object"}
        }
      }'
      ```
    </CodeGroup>
  </Tab>
</Tabs>

<Accordion title="返回结果（含思考过程）">
  ```text
  ====================思考过程====================
  用户要求抽取姓名与年龄信息，并以JSON格式返回。
  从文本中可以看到：
  - 姓名：刘五
  - 年龄：34
  - 邮箱：liuwu@example.com（但用户只要求姓名和年龄）
  - 爱好：打篮球和旅游（但用户只要求姓名和年龄）
  根据要求，只需要提取姓名和年龄信息，并以JSON格式返回。
  考虑到用户使用的是中文提问，使用中文键名可能更合适。
  最终输出：
  {
    "姓名": "刘五",
    "年龄": 34
  }
  ====================完整回复====================
  {"姓名":"刘五","年龄":34}

  Usage:
  CompletionUsage(completion_tokens=203, prompt_tokens=48, total_tokens=251, completion_tokens_details=CompletionTokensDetails(reasoning_tokens=190))
  ```
</Accordion>

## 优化提示词

模糊的提示词（如"返回用户信息"）会导致输出结构不可预期。为获得可靠的结果，建议在提示词中明确描述预期的结构：指定字段名称、类型、是否必填、格式要求（如日期格式），并提供示例。

以下 System Prompt 演示了这一写法：约束字段类型、区分必填与非必填字段，并用 4 个示例说明"未提及爱好时省略 `hobby` 字段"。

```text System Prompt
请从用户输入中提取个人信息并按照指定的JSON Schema格式输出：

【输出格式要求】
输出必须严格遵循以下JSON结构：
{
  "info": {
    "name": "字符串类型，必需字段，用户姓名",
    "age": "字符串类型，必需字段，格式为'数字+岁'，例如'25岁'",
    "email": "字符串类型，必需字段，标准邮箱格式，例如'user@example.com'"
  },
  "hobby": ["字符串数组类型，非必需字段，包含用户的所有爱好，如未提及则完全不输出此字段"]
}

【字段提取规则】
1. name: 从文本中识别用户姓名，必需提取
2. age: 识别年龄信息，转换为"数字+岁"格式，必需提取
3. email: 识别邮箱地址，保持原始格式，必需提取
4. hobby: 识别用户爱好，以字符串数组形式输出，如未提及爱好信息则完全省略hobby字段

【参考示例】
示例1（包含爱好）：
Q：我叫张三，今年25岁，邮箱是zhangsan@example.com，爱好是唱歌
A：{"info":{"name":"张三","age":"25岁","email":"zhangsan@example.com"},"hobby":["唱歌"]}
示例2（包含多个爱好）：
Q：我叫李四，今年30岁，邮箱是lisi@example.com，平时喜欢跳舞和游泳
A：{"info":{"name":"李四","age":"30岁","email":"lisi@example.com"},"hobby":["跳舞","游泳"]}
示例3（不包含爱好）：
Q：我叫赵六，今年28岁，我的邮箱是zhaoliu@example.com
A：{"info":{"name":"赵六","age":"28岁","email":"zhaoliu@example.com"}}
示例4（不包含爱好）：
Q：我是孙七，35岁，邮箱sunqi@example.com
A：{"info":{"name":"孙七","age":"35岁","email":"sunqi@example.com"}}

请严格按照上述格式和规则提取信息并输出JSON。如果用户未提及爱好，则不要在输出中包含hobby字段。
```

将上述内容作为 System Message 传入即可：

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python {17}
      from openai import OpenAI
      import os

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      system_prompt = """..."""  # 替换为上文的 System Prompt

      completion = client.chat.completions.create(
        model="qwen3.8-max",
        messages=[
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"},
        ],
        response_format={"type": "json_object"},
      )
      print(completion.choices[0].message.content)
      ```

      ```javascript Node.js {16}
      import OpenAI from "openai";

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      const systemPrompt = `...`;  // 替换为上文的 System Prompt

      const completion = await openai.chat.completions.create({
        model: "qwen3.8-max",
        messages: [
          { role: "system", content: systemPrompt },
          { role: "user", content: "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游" }
        ],
        response_format: { type: "json_object" }
      });
      console.log(completion.choices[0].message.content);
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python {17}
      import os
      import dashscope

      dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

      system_prompt = """..."""  # 替换为上文的 System Prompt

      messages = [
        {"role": "system", "content": [{"text": system_prompt}]},
        {"role": "user", "content": [{"text": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"}]},
      ]

      response = dashscope.MultiModalConversation.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen3.8-max",
        messages=messages,
        response_format={"type": "json_object"},
      )
      print(response.output.choices[0].message.content[0]["text"])
      ```

      ```java Java {35}
      // DashScope Java SDK 版本需要不低于 2.21.4
      import java.util.Arrays;
      import java.util.Collections;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.ResponseFormat;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;

      public class Main {
        static {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        }

        // 替换为上文的 System Prompt
        private static final String SYSTEM_PROMPT = "...";

        public static void main(String[] args) {
          try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage systemMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", SYSTEM_PROMPT))).build();
            MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游"))).build();
            ResponseFormat jsonMode = ResponseFormat.builder().type("json_object").build();
            MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.8-max")
                .messages(Arrays.asList(systemMessage, userMessage))
                .responseFormat(jsonMode)
                .build();
            MultiModalConversationResult result = conv.call(param);
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
        }
      }
      ```
    </CodeGroup>
  </Tab>
</Tabs>

返回结果：

```json
{
  "info": {
    "name": "刘五",
    "age": "34岁",
    "email": "liuwu@example.com"
  },
  "hobby": ["打篮球", "旅游"]
}
```

## 使用 JSON Schema 精确约束输出

JSON Object 模式只保证输出是合法 JSON，字段名、类型、层级都可能与预期不符。对于自动化解析、API 互操作等需要严格类型约束的场景，将 `type` 设为 `json_schema`，模型会严格按照给定的 Schema 输出。

`response_format` 的结构如下：

<CodeGroup>
  ```json 结构
  {
    "type": "json_schema",
    "json_schema": {
      "name": "schema_name",       // Schema 的名称
      "strict": true,              // 推荐设置为 true，严格遵守格式
      "schema": {
        "type": "object",
        "properties": {...},       // 定义字段结构
        "required": [...],         // 必填字段列表
        "additionalProperties": false  // 推荐设置为 false，只输出定义的字段
      }
    }
  }
  ```

  ```json 示例
  {
    "type": "json_schema",
    "json_schema": {
      "name": "user_info",
      "strict": true,
      "schema": {
        "type": "object",
        "properties": {
          "name": {
            "type": "string",
            "description": "用户姓名"
          },
          "age": {
            "type": "integer",
            "description": "用户年龄"
          },
          "email": {
            "type": "string",
            "description": "邮箱地址"
          }
        },
        "required": ["name", "age"],
        "additionalProperties": false
      }
    }
  }
  ```
</CodeGroup>

上述示例会强制模型输出包含 `name` 和 `age` 两个必填字段、以及可选的 `email` 字段的 JSON 对象。

### 使用方法

通过 OpenAI SDK 的 `parse` 方法，可直接传入 Python Pydantic 类或 Node.js Zod 对象，SDK 会自动转换为 JSON Schema，无需手动编写。DashScope SDK 需按上文格式手动构造 JSON Schema。

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python {14,20}
      from pydantic import BaseModel, Field
      from openai import OpenAI
      import os

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      class UserInfo(BaseModel):
        name: str = Field(description="用户的姓名")
        age: int = Field(description="用户的年龄，单位为岁")

      completion = client.chat.completions.parse(
        model="qwen3.8-max",
        messages=[
          {"role": "system", "content": "提取姓名与年龄信息。"},
          {"role": "user", "content": "我叫刘五，今年25岁。"},
        ],
        response_format=UserInfo,          # ← 直接传入 Pydantic 类
      )
      result = completion.choices[0].message.parsed
      print(f"姓名：{result.name}，年龄：{result.age}")
      ```

      ```javascript Node.js {15,21}
      import OpenAI from "openai";
      import { zodResponseFormat } from "openai/helpers/zod";
      import { z } from "zod";

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      const UserInfo = z.object({
        name: z.string().describe("用户的姓名"),
        age: z.number().int().describe("用户的年龄，单位为岁"),
      });

      const completion = await openai.chat.completions.parse({
        model: "qwen3.8-max",
        messages: [
          { role: "system", content: "提取姓名与年龄信息。" },
          { role: "user", content: "我叫刘五，今年25岁。" },
        ],
        response_format: zodResponseFormat(UserInfo, "user_info"),  // ← 直接传入 Zod 对象
      });
      const userInfo = completion.choices[0].message.parsed;
      console.log(`姓名：${userInfo.name}`);
      console.log(`年龄：${userInfo.age}`);
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <Note>
      DashScope 的 JSON Schema 模式暂不支持 Java SDK。
    </Note>

    ```python Python {18}
    import os
    import json
    import dashscope

    dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

    messages = [
      {
        "role": "user",
        "content": [{"text": "我叫刘五，今年25岁。"}],
      },
    ]

    response = dashscope.MultiModalConversation.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      model="qwen3.8-max",
      messages=messages,
      response_format={
        "type": "json_schema",
        "json_schema": {
          "name": "user_info",
          "strict": True,
          "schema": {
            "type": "object",
            "title": "UserInfo",
            "properties": {
              "name": {"title": "Name", "type": "string"},
              "age": {"title": "Age", "type": "integer"},
            },
            "required": ["name", "age"],
          },
        },
      },
    )
    json_object = json.loads(response.output.choices[0].message.content[0]["text"])
    print(f"姓名：{json_object['name']}，年龄：{json_object['age']}")
    ```
  </Tab>
</Tabs>

返回结果：

```text
姓名：刘五，年龄：25
```

### 配置指南

<AccordionGroup>
  <Accordion title="必填字段声明">
    将必填字段列在 `required` 数组中，可选字段不列入：

    ```json
    {
      "properties": {
        "name": {"type": "string"},
        "age": {"type": "integer"},
        "email": {"type": "string"}
      },
      "required": ["name", "age"]
    }
    ```

    若输入未提供 email 信息，输出中将不包含此字段。
  </Accordion>

  <Accordion title="可选字段的实现方式">
    除了不列入 `required`，也可以通过允许 `null` 类型实现可选字段：

    ```json
    {
      "properties": {
        "name": {"type": "string"},
        "email": {"type": ["string", "null"]}  // 可以是字符串或 null
      },
      "required": ["name", "email"]  // 两个都在 required 中
    }
    ```

    此时输出将始终包含 `email` 字段，但其值可能为 `null`。
  </Accordion>

  <Accordion title="additionalProperties 配置">
    控制是否允许输出未在 Schema 中定义的额外字段：

    ```json
    {
      "properties": {"name": {"type": "string"}},
      "required": ["name"],
      "additionalProperties": true  // 允许额外字段
    }
    ```

    输入"我叫张三，25岁"时，输出为 `{"name": "张三", "age": 25}`，包含未定义的 `age` 字段。

| 值       | 行为       | 适用场景     |
| ------- | -------- | -------- |
| `false` | 只输出定义的字段 | 需要精确控制结构 |
| `true`  | 允许额外字段   | 需要捕获更多信息 |
  </Accordion>

  <Accordion title="支持的数据类型">
    `string`、`number`、`integer`、`boolean`、`object`、`array`、`enum`。
  </Accordion>
</AccordionGroup>

## 应用于生产环境

**有效性校验**

使用 JSON Object 模式时，输出只保证是合法 JSON，不保证符合业务约定的结构。传递给下游业务前，建议用 jsonschema（Python）、Ajv（JavaScript）、Everit（Java）等工具校验，避免因字段缺失、类型错误导致下游解析失败、数据丢失或业务逻辑中断。校验失败时可通过重试或让模型改写来修复。

**禁用 max\_tokens**

开启结构化输出时请勿设置 `max_tokens`。该参数限制输出 Token 数（默认为模型最大输出 Token 数），设置后可能导致 JSON 字符串在输出过程中被截断，产生无效 JSON。

**使用 SDK 辅助生成 Schema**

推荐用 SDK 自动生成 Schema，避免手写维护出错，同时获得自动校验与类型安全的解析结果。

<CodeGroup>
  ```python Python {16,22}
  from pydantic import BaseModel, Field
  from typing import Optional
  from openai import OpenAI
  import os

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  class UserInfo(BaseModel):
    name: str = Field(description="用户姓名")
    age: int = Field(description="用户年龄")
    email: Optional[str] = None        # 可选字段

  completion = client.chat.completions.parse(
    model="qwen3.8-max",
    messages=[
      {"role": "system", "content": "提取姓名与年龄信息。"},
      {"role": "user", "content": "我叫刘五，今年25岁。"},
    ],
    response_format=UserInfo,          # 直接传入 Pydantic 模型
  )
  result = completion.choices[0].message.parsed   # 类型安全的解析结果
  print(f"姓名：{result.name}，年龄：{result.age}")
  ```

  ```javascript Node.js {16,22}
  import { z } from "zod";
  import { zodResponseFormat } from "openai/helpers/zod";
  import OpenAI from "openai";

  const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  });

  const UserInfo = z.object({
    name: z.string().describe("用户姓名"),
    age: z.number().int().describe("用户年龄"),
    email: z.string().optional().nullable()   // 可选字段
  });

  const completion = await client.chat.completions.parse({
    model: "qwen3.8-max",
    messages: [
      { role: "system", content: "提取姓名与年龄信息。" },
      { role: "user", content: "我叫刘五，今年25岁。" },
    ],
    response_format: zodResponseFormat(UserInfo, "user_info")
  });
  console.log(completion.choices[0].message.parsed);
  ```
</CodeGroup>

## 常见问题

<Accordion title="标注为“非思考模式”的模型，开启思考后如何获得结构化输出？">
  [支持的模型](#支持的模型)中标注为"非思考模式"的模型，在思考模式下返回的内容可能不是严格的标准 JSON。可采用两步法：先调用思考模型获取高质量输出，再把格式不正确的 JSON 交给支持 JSON Object 模式的模型修复。

  **第一步：获取思考模式下的输出**

  <Note>
    开启思考模式时设置 `response_format` 为 `{"type": "json_object"}` 不会报错。以下为兜底示例，仅在模型返回内容不是标准 JSON 时用于演示两步修复法，因此未设置 `response_format`。
  </Note>

  ```python {11}
  completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[
      {"role": "system", "content": system_prompt},
      {
        "role": "user",
        "content": "大家好，我叫刘五，今年34岁，邮箱是liuwu@example.com，平时喜欢打篮球和旅游",
      },
    ],
    # 开启思考模式；本兜底示例未设置 response_format 参数（直接设置不会报错）
    extra_body={"enable_thinking": True},
    # 思考模式下需要开启流式输出
    stream=True,
  )
  # 拼接模型生成的 JSON 结果
  json_string = ""
  for chunk in completion:
    if not chunk.choices:
      continue
    if chunk.choices[0].delta.content is not None:
      json_string += chunk.choices[0].delta.content
  ```

  **第二步：校验并修复输出**

  尝试解析上一步得到的 `json_string`。若是有效 JSON，直接使用；若无效，调用支持结构化输出的模型修复（建议选择速度快、成本低的模型，如非思考模式的 `qwen-flash`）。

  ```python {28}
  import json
  from openai import OpenAI
  import os

  # 若前面的代码块未定义 client 变量，请取消下面的注释
  # client = OpenAI(
  #   api_key=os.getenv("DASHSCOPE_API_KEY"),
  #   base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  # )

  try:
    json_object_from_thinking_model = json.loads(json_string)
    print("生成标准格式JSON字符串")
  except json.JSONDecodeError:
    print("未生成标准格式JSON字符串，通过支持结构化输出的模型进行修复")
    completion = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[
        {
          "role": "system",
          "content": "你是一个json格式修复专家，请将用户输入的json字符串修复为标准格式",
        },
        {
          "role": "user",
          "content": json_string,
        },
      ],
      response_format={"type": "json_object"},
    )
    json_object_from_thinking_model = json.loads(completion.choices[0].message.content)
  ```
</Accordion>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误码](/api-reference/preparation/error-messages)进行解决。
