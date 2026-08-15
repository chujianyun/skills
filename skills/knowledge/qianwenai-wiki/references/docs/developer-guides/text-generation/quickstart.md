> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文本生成

> 发起第一次文本生成调用

文本生成模型接收自然语言输入，生成问答、写作、摘要、翻译、结构化输出等文本内容。

## 请求结构

文本生成请求通常以 `messages` 数组的形式发送，每条消息包含 `role`（角色）和 `content`（内容）两个字段。

- **System message**：设定模型行为的全局指令。
- **User message**：用户的输入或任务描述。
- **Assistant message**：模型的回复内容。

一个典型的请求至少包含一条 `user` 消息，可选地附带一条 `system` 消息以获得更稳定、可控的输出。

<Tip>
  `system` 消息非必需，但如果你希望模型表现更一致，建议添加。
</Tip>

```json
[
  {"role": "system", "content": "You are a helpful assistant. Answer clearly and concisely."},
  {"role": "user", "content": "用三个要点概括太阳能的优势。"}
]
```

模型会以 `assistant` 消息返回回复。

```json
{
  "role": "assistant",
  "content": "- 减少对化石燃料的依赖。\n- 降低长期用电成本。\n- 运行过程中几乎不产生排放。"
}
```

## 发起第一次调用

开始之前，请先[获取 API Key](/api-reference/preparation/api-key)、[将其设为环境变量](/api-reference/preparation/export-api-key-env)，并按需[安装 OpenAI 或 DashScope SDK](/api-reference/preparation/install-sdk)。

根据你的技术栈选择合适的 API 风格：

- 新项目建议使用 **OpenAI Compatible -- Responses API**。
- 已有 OpenAI 兼容代码需要迁移时，使用 **OpenAI Compatible -- Chat Completions API**。
- 偏好原生 SDK 时，使用 **DashScope**。

<Tabs>
  <Tab title="OpenAI Compatible -- Responses API">
    接口说明、代码示例和迁移指南请参见 [OpenAI compatible - Responses](/api-reference/chat/openai-responses)。

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      try:
        client = OpenAI(
          # 如果未设置环境变量，请将下行替换为：api_key="sk-xxx",
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        response = client.responses.create(
          model="qwen3.7-plus",
          input="用三个要点概括太阳能的优势。"
        )

        print(response)
      except Exception as e:
        print(f"错误信息：{e}")
      ```

      ```javascript Node.js
      // 需要 Node.js v18+，在 ES Module 环境下运行
      import OpenAI from "openai";

      const openai = new OpenAI({
        // 如果未设置环境变量，请将下行替换为：apiKey: "sk-xxx",
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      async function main() {
        try {
          const response = await openai.responses.create({
            model: "qwen3.7-plus",
            input: "用三个要点概括太阳能的优势。"
          });

          // 获取模型回复
          console.log(response);
        } catch (error) {
          console.error("错误：", error);
        }
      }

      main();
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3.7-plus",
        "input": "用三个要点概括太阳能的优势。",
        "enable_thinking": true
      }'
      ```
    </CodeGroup>

    **响应**

    响应包含以下主要字段：

    - `id`：响应 ID。

    - `output`：输出列表，包含 `reasoning`（思考过程）和 `message`（回复内容）。

      <Note>
        `reasoning` 字段仅在开启[深度思考](/developer-guides/text-generation/thinking)时出现（例如 Qwen3.5 和 Qwen3.6 系列默认开启）。
      </Note>

    - `usage`：Token 用量统计。

    示例文本输出：

    ```text
    - 减少对化石燃料的依赖。
    - 降低长期用电成本。
    - 运行过程中几乎不产生排放。
    ```

    <Accordion title="完整 JSON 响应">
      ```json
      {
        "created_at": 1772249518,
        "id": "7ad48c6b-3cc4-904f-9284-5f419c6c5xxx",
        "model": "qwen3.7-plus",
        "object": "response",
        "output": [
          {
            "id": "msg_94805179-2801-45da-ac1c-a87e8ea20xxx",
            "summary": [
              {
                "text": "The user wants a concise answer in exactly three bullet points. Focus on the most broadly useful benefits of solar energy: reduced reliance on fossil fuels, long-term cost savings, and lower operating emissions. Keep the wording simple and direct.\n",
                "type": "summary_text"
              }
            ],
            "type": "reasoning"
          },
          {
            "content": [
              {
                "annotations": [],
                "text": "- 减少对化石燃料的依赖。\n- 降低长期用电成本。\n- 运行过程中几乎不产生排放。",
                "type": "output_text"
              }
            ],
            "id": "msg_35be06c6-ca4d-4f2b-9677-7897e488dxxx",
            "role": "assistant",
            "status": "completed",
            "type": "message"
          }
        ],
        "parallel_tool_calls": false,
        "status": "completed",
        "tool_choice": "auto",
        "tools": [],
        "usage": {
          "input_tokens": 54,
          "input_tokens_details": {
            "cached_tokens": 0
          },
          "output_tokens": 662,
          "output_tokens_details": {
            "reasoning_tokens": 447
          },
          "total_tokens": 716,
          "x_details": [
            {
              "input_tokens": 54,
              "output_tokens": 662,
              "output_tokens_details": {
                "reasoning_tokens": 447
              },
              "total_tokens": 716,
              "x_billing_type": "response_api"
            }
          ]
        }
      }
      ```
    </Accordion>
  </Tab>

  <Tab title="OpenAI Compatible -- Chat Completions API">
    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      try:
        client = OpenAI(
          # 如果未设置环境变量，请将下行替换为：api_key="sk-xxx",
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        completion = client.chat.completions.create(
          model="qwen3.7-plus",
          messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "用三个要点概括太阳能的优势。"},
          ],
        )
        print(completion.choices[0].message.content)
        # 查看完整响应，取消注释下行
        # print(completion.model_dump_json())
      except Exception as e:
        print(f"错误信息：{e}")
      ```

      ```java Java
      // 建议 OpenAI Java SDK 版本 >= 3.5.0
      import com.openai.client.OpenAIClient;
      import com.openai.client.okhttp.OpenAIOkHttpClient;
      import com.openai.models.chat.completions.ChatCompletion;
      import com.openai.models.chat.completions.ChatCompletionCreateParams;

      public class Main {
        public static void main(String[] args) {
          try {
            OpenAIClient client = OpenAIOkHttpClient.builder()
                // 如果未设置环境变量，请将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                .build();

            // 创建 ChatCompletion 参数
            ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .model("qwen3.7-plus")
                .addSystemMessage("You are a helpful assistant.")
                .addUserMessage("用三个要点概括太阳能的优势。")
                .build();

            // 发送请求并获取响应
            ChatCompletion chatCompletion = client.chat().completions().create(params);
            String content = chatCompletion.choices().get(0).message().content().orElse("未返回内容");
            System.out.println(content);

          } catch (Exception e) {
            System.err.println("错误信息：" + e.getMessage());
          }
        }
      }
      ```

      ```javascript Node.js
      // 需要 Node.js v18+，在 ES Module 环境下运行
      import OpenAI from "openai";

      const openai = new OpenAI(
        {
          // 如果未设置环境变量，请将下行替换为：apiKey: "sk-xxx",
          apiKey: process.env.DASHSCOPE_API_KEY,
          baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"

        }
      );
      const completion = await openai.chat.completions.create({
        model: "qwen3.7-plus",
        messages: [
          { role: "system", content: "You are a helpful assistant." },
          { role: "user", content: "用三个要点概括太阳能的优势。" }
        ],
      });
      console.log(completion.choices[0].message.content);
      // 查看完整响应，取消注释下行
      // console.log(JSON.stringify(completion, null, 4));
      ```

      ```go Go
      // OpenAI Go SDK 版本 >= v2.4.0
      package main

      import (
        "context"
        // 查看完整响应，取消注释下行
        // "encoding/json"
        "fmt"
        "os"

        "github.com/openai/openai-go/v2"
        "github.com/openai/openai-go/v2/option"
      )

      func main() {
        // 如果未设置环境变量，请将下行替换为：apiKey := "sk-xxx"
        apiKey := os.Getenv("DASHSCOPE_API_KEY")
        client := openai.NewClient(
          option.WithAPIKey(apiKey),
          option.WithBaseURL("https://dashscope.aliyuncs.com/compatible-mode/v1"),
        )
        chatCompletion, err := client.Chat.Completions.New(
          context.TODO(), openai.ChatCompletionNewParams{
            Messages: []openai.ChatCompletionMessageParamUnion{
              openai.SystemMessage("You are a helpful assistant."),
              openai.UserMessage("用三个要点概括太阳能的优势。"),
            },
            Model: "qwen3.7-plus",
          },
        )

        if err != nil {
          fmt.Fprintf(os.Stderr, "请求失败：%v\n", err)
          os.Exit(1)
        }

        if len(chatCompletion.Choices) > 0 {
          fmt.Println(chatCompletion.Choices[0].Message.Content)
        }
        // 查看完整响应，取消注释下行
        // jsonData, _ := json.MarshalIndent(chatCompletion, "", "  ")
        // fmt.Println(string(jsonData))

      }
      ```

      ```csharp C#
      using System.Net.Http.Headers;
      using System.Text;
      using System.Text.Json;

      class Program
      {
        private static readonly HttpClient httpClient = new HttpClient();

        static async Task Main(string[] args)
        {
          // 如果未设置环境变量，请将下行替换为：string? apiKey = "sk-xxx";
          string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");
          string url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions";
          string jsonContent = @"{
            ""model"": ""qwen3.7-plus"",
            ""messages"": [
              {
                ""role"": ""system"",
                ""content"": ""You are a helpful assistant.""
              },
              {
                ""role"": ""user"",
                ""content"": ""用三个要点概括太阳能的优势。""
              }
            ]
          }";

          // 发送请求并获取响应
          string result = await SendPostRequestAsync(url, jsonContent, apiKey);

          // 查看完整响应，取消注释下行
          // Console.WriteLine(result);

          // 解析 JSON 并仅输出 content 字段
          using JsonDocument doc = JsonDocument.Parse(result);
          JsonElement root = doc.RootElement;

          if (root.TryGetProperty("choices", out JsonElement choices) &&
            choices.GetArrayLength() > 0)
          {
            JsonElement firstChoice = choices[0];
            if (firstChoice.TryGetProperty("message", out JsonElement message) &&
              message.TryGetProperty("content", out JsonElement content))
            {
              Console.WriteLine(content.GetString());
            }
          }
        }

        private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
        {
          using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
          {
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));
            HttpResponseMessage response = await httpClient.PostAsync(url, content);
            if (response.IsSuccessStatusCode)
            {
              return await response.Content.ReadAsStringAsync();
            }
            else
            {
              return $"请求失败：{response.StatusCode}";
            }
          }
        }
      }
      ```

      ```php PHP
      <?php
      // 设置请求 URL
      $url = 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions';
      // 如果未设置环境变量，请将下行替换为：$apiKey = "sk-xxx";
      $apiKey = getenv('DASHSCOPE_API_KEY');
      // 设置请求头
      $headers = [
        'Authorization: Bearer '.$apiKey,
        'Content-Type: application/json'
      ];
      // 设置请求体
      $data = [
        "model" => "qwen3.7-plus",
        "messages" => [
          [
            "role" => "system",
            "content" => "You are a helpful assistant."
          ],
          [
            "role" => "user",
            "content" => "用三个要点概括太阳能的优势。"
          ]
        ]
      ];
      // 初始化 cURL 会话
      $ch = curl_init();
      // 设置 cURL 选项
      curl_setopt($ch, CURLOPT_URL, $url);
      curl_setopt($ch, CURLOPT_POST, true);
      curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
      curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
      curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
      // 执行 cURL 会话
      $response = curl_exec($ch);
      // 检查错误
      if (curl_errno($ch)) {
        echo 'Curl error: ' . curl_error($ch);
      }
      // 关闭 cURL 资源
      curl_close($ch);
      // 输出响应
      $dataObject = json_decode($response);
      $content = $dataObject->choices[0]->message->content;
      echo $content;
      // 查看完整响应，取消注释下行
      //echo $response;
      ?>
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3.7-plus",
        "messages": [
          {
            "role": "system",
            "content": "You are a helpful assistant."
          },
          {
            "role": "user",
            "content": "用三个要点概括太阳能的优势。"
          }
        ]
      }'
      ```
    </CodeGroup>

    **响应**

    ```text
    - 减少对化石燃料的依赖。
    - 降低长期用电成本。
    - 运行过程中几乎不产生排放。
    ```

    <Accordion title="完整 JSON 响应">
      ```json
      {
        "choices": [
          {
            "message": {
              "role": "assistant",
              "content": "- 减少对化石燃料的依赖。\n- 降低长期用电成本。\n- 运行过程中几乎不产生排放。"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
          }
        ],
        "object": "chat.completion",
        "usage": {
          "prompt_tokens": 26,
          "completion_tokens": 66,
          "total_tokens": 92
        },
        "created": 1726127645,
        "system_fingerprint": null,
        "model": "qwen3.7-plus",
        "id": "chatcmpl-81951b98-28b8-9659-ab07-xxxxxx"
      }
      ```
    </Accordion>
  </Tab>

  <Tab title="DashScope">
    <Note>
      qwen3.7-max、qwen3.7-max-2026-05-20 和 qwen3.6-max-preview 仅支持文本接口（`Generation`）。qwen3.8-max、qwen3.7-max-2026-06-08、Qwen3.6 和 Qwen3.5 系列需要使用多模态接口（`MultiModalConversation`）。本标签页的示例使用 `qwen-plus`，通过文本接口调用。如需使用多模态接口，请参见**多模态接口**标签页。
    </Note>

    <CodeGroup>
      ```python Python
      import json
      import os
      from dashscope import Generation
      import dashscope

      dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

      messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "用三个要点概括太阳能的优势。"},
      ]
      response = Generation.call(
        # 如果未设置环境变量，请将下行替换为：api_key = "sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen-plus",
        messages=messages,
        result_format="message",
      )

      if response.status_code == 200:
        print(response.output.choices[0].message.content)
        # 查看完整响应，取消注释下行
        # print(json.dumps(response, default=lambda o: o.__dict__, indent=4))
      else:
        print(f"HTTP 状态码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
      ```

      ```java Java
      import java.util.Arrays;
      import java.lang.System;
      import com.alibaba.dashscope.aigc.generation.Generation;
      import com.alibaba.dashscope.aigc.generation.GenerationParam;
      import com.alibaba.dashscope.aigc.generation.GenerationResult;
      import com.alibaba.dashscope.common.Message;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.InputRequiredException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.protocol.Protocol;
      import com.alibaba.dashscope.utils.JsonUtils;

      public class Main {
        public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
          Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");
          Message systemMsg = Message.builder()
              .role(Role.SYSTEM.getValue())
              .content("You are a helpful assistant.")
              .build();
          Message userMsg = Message.builder()
              .role(Role.USER.getValue())
              .content("用三个要点概括太阳能的优势。")
              .build();
          GenerationParam param = GenerationParam.builder()
              // 如果未设置环境变量，请将下行替换为：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen-plus")
              .messages(Arrays.asList(systemMsg, userMsg))
              .resultFormat(GenerationParam.ResultFormat.MESSAGE)
              .build();
          return gen.call(param);
        }
        public static void main(String[] args) {
          try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
            // 查看完整响应，取消注释下行
            // System.out.println(JsonUtils.toJson(result));
          } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("错误信息："+e.getMessage());
          }
        }
      }
      ```

      ```javascript Node.js
      // 需要 Node.js v18+
      // 如果未设置环境变量，请将下行替换为：const apiKey = "sk-xxx";
      const apiKey = process.env.DASHSCOPE_API_KEY;

      const data = {
        model: "qwen-plus",
        input: {
          messages: [
            {
              role: "system",
              content: "You are a helpful assistant."
            },
            {
              role: "user",
              content: "用三个要点概括太阳能的优势。"
            }
          ]
        },
        parameters: {
          result_format: "message"
        }
      };

      async function callApi() {
        try {
            const response = await fetch('https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation', {
            method: 'POST',
            headers: {
              'Authorization': `Bearer ${apiKey}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
          });

          const result = await response.json();
          console.log(result.output.choices[0].message.content);
          // 查看完整响应，取消注释下行
          // console.log(JSON.stringify(result));
        } catch (error) {
          console.error('调用失败：', error.message);
        }
      }

      callApi();
      ```

      ```go Go
      package main

      import (
        "bytes"
        "encoding/json"
        "fmt"
        "io"
        "log"
        "net/http"
        "os"
      )

      func main() {
        requestBody := map[string]interface{}{
          "model": "qwen-plus",
          "input": map[string]interface{}{
            "messages": []map[string]string{
              {
                "role":    "system",
                "content": "You are a helpful assistant.",
              },
              {
                "role":    "user",
                "content": "用三个要点概括太阳能的优势。",
              },
            },
          },
          "parameters": map[string]string{
            "result_format": "message",
          },
        }

        // 序列化为 JSON
        jsonData, _ := json.Marshal(requestBody)

        // 创建 HTTP 客户端和请求
        client := &http.Client{}
        req, _ := http.NewRequest("POST", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation", bytes.NewBuffer(jsonData))

        // 设置请求头
        apiKey := os.Getenv("DASHSCOPE_API_KEY")
        req.Header.Set("Authorization", "Bearer "+apiKey)
        req.Header.Set("Content-Type", "application/json")

        // 发送请求
        resp, err := client.Do(req)
        if err != nil {
          log.Fatal(err)
        }
        defer resp.Body.Close()

        // 读取响应体
        bodyText, _ := io.ReadAll(resp.Body)

        // 解析 JSON 并输出内容
        var result map[string]interface{}
        json.Unmarshal(bodyText, &result)
        content := result["output"].(map[string]interface{})["choices"].([]interface{})[0].(map[string]interface{})["message"].(map[string]interface{})["content"].(string)
        fmt.Println(content)

        // 查看完整响应，取消注释下行
        // fmt.Printf("%s\n", bodyText)
      }
      ```

      ```csharp C#
      using System.Net.Http.Headers;
      using System.Text;

      class Program
      {
        private static readonly HttpClient httpClient = new HttpClient();

        static async Task Main(string[] args)
        {
          // 如果未设置环境变量，请将下行替换为：string? apiKey = "sk-xxx";
          string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");
          // 设置请求 URL 和内容
          string url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
          string jsonContent = @"{
            ""model"": ""qwen-plus"",
            ""input"": {
              ""messages"": [
                {
                  ""role"": ""system"",
                  ""content"": ""You are a helpful assistant.""
                },
                {
                  ""role"": ""user"",
                  ""content"": ""用三个要点概括太阳能的优势。""
                }
              ]
            },
            ""parameters"": {
              ""result_format"": ""message""
            }
          }";

          // 发送请求并获取响应
          string result = await SendPostRequestAsync(url, jsonContent, apiKey);
          var jsonResult = System.Text.Json.JsonDocument.Parse(result);
          var content = jsonResult.RootElement.GetProperty("output").GetProperty("choices")[0].GetProperty("message").GetProperty("content").GetString();
          Console.WriteLine(content);
          // 查看完整响应，取消注释下行
          // Console.WriteLine(result);
        }

        private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
        {
          using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
          {
            // 设置请求头
            httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
            httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

            // 发送请求并获取响应
            HttpResponseMessage response = await httpClient.PostAsync(url, content);

            // 处理响应
            if (response.IsSuccessStatusCode)
            {
              return await response.Content.ReadAsStringAsync();
            }
            else
            {
              return $"请求失败：{response.StatusCode}";
            }
          }
        }
      }
      ```

      ```php PHP
      <?php
      $url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
      $apiKey = getenv('DASHSCOPE_API_KEY');

      $data = [
        "model" => "qwen-plus",
        "input" => [
          "messages" => [
            [
              "role" => "system",
              "content" => "You are a helpful assistant."
            ],
            [
              "role" => "user",
              "content" => "用三个要点概括太阳能的优势。"
            ]
          ]
        ],
        "parameters" => [
          "result_format" => "message"
        ]
      ];

      $jsonData = json_encode($data);

      $ch = curl_init($url);
      curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
      curl_setopt($ch, CURLOPT_POST, true);
      curl_setopt($ch, CURLOPT_POSTFIELDS, $jsonData);
      curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "Authorization: Bearer $apiKey",
        "Content-Type: application/json"
      ]);

      $response = curl_exec($ch);
      $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

      if ($httpCode == 200) {
        $jsonResult = json_decode($response, true);
        $content = $jsonResult['output']['choices'][0]['message']['content'];
        echo $content;
        // 查看完整响应，取消注释下行
        // echo "模型回复：" . $response;
      } else {
        echo "请求错误：" . $httpCode . " - " . $response;
      }

      curl_close($ch);
      ?>
      ```

      ```bash curl
      curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --data '{
        "model": "qwen-plus",
        "input":{
          "messages":[
            {
              "role": "system",
              "content": "You are a helpful assistant."
            },
            {
              "role": "user",
              "content": "用三个要点概括太阳能的优势。"
            }
          ]
        },
        "parameters": {
          "result_format": "message"
        }
      }'
      ```
    </CodeGroup>

    **响应**

    ```text
    - 减少对化石燃料的依赖。
    - 降低长期用电成本。
    - 运行过程中几乎不产生排放。
    ```

    <Accordion title="完整 JSON 响应">
      ```json
      {
        "output": {
          "choices": [
            {
              "finish_reason": "stop",
              "message": {
                "role": "assistant",
                "content": "- 减少对化石燃料的依赖。\n- 降低长期用电成本。\n- 运行过程中几乎不产生排放。"
              }
            }
          ]
        },
        "usage": {
          "total_tokens": 92,
          "output_tokens": 66,
          "input_tokens": 26
        },
        "request_id": "09dceb20-ae2e-999b-85f9-xxxxxx",
        "model": "qwen-plus"
      }
      ```
    </Accordion>
  </Tab>

  <Tab title="DashScope -- 多模态接口">
    qwen3.8-max、qwen3.7-max-2026-06-08、Qwen3.6 和 Qwen3.5 系列的 DashScope API 需使用多模态接口（`MultiModalConversation`），而非文本接口（`Generation`）。直接运行上一标签页的示例会提示 url error 错误。用户消息的 content 必须是对象数组。

    <CodeGroup>
      ```python Python
      import os
      import dashscope
      from dashscope import MultiModalConversation

      dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

      messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {
          "role": "user",
          "content": [{"text": "用三个要点概括太阳能的优势。"}],
        },
      ]
      response = MultiModalConversation.call(
        # 如果未设置环境变量，请将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen3.7-plus",
        messages=messages,
      )

      if response.status_code == 200:
        print(response.output.choices[0].message.content[0]["text"])
        # 查看完整响应，取消注释下行
        # import json; print(json.dumps(response, default=lambda o: o.__dict__, indent=4))
      else:
        print(f"HTTP 状态码：{response.status_code}")
        print(f"错误码：{response.code}")
        print(f"错误信息：{response.message}")
      ```

      ```java Java
      import java.util.Arrays;
      import java.util.Collections;
      import java.util.List;

      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;

      public class Main {
        static {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        }

        public static void main(String[] args) {
          try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMessage = MultiModalMessage.builder()
                .role(Role.USER.getValue())
                .content(List.of(Collections.singletonMap("text", "用三个要点概括太阳能的优势。")))
                .build();
            MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 如果未设置环境变量，请将下行替换为：.apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.7-plus")
                .messages(Arrays.asList(userMessage))
                .build();
            MultiModalConversationResult result = conv.call(param);
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.err.println("错误信息：" + e.getMessage());
          }
        }
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3.7-plus",
        "input": {
          "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {
              "role": "user",
              "content": [{"text": "用三个要点概括太阳能的优势。"}]
            }
          ]
        }
      }'
      ```
    </CodeGroup>

    **响应**

    ```text
    - 减少对化石燃料的依赖。
    - 降低长期用电成本。
    - 运行过程中几乎不产生排放。
    ```

    <Accordion title="完整 JSON 响应">
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
                    "text": "- 减少对化石燃料的依赖。\n- 降低长期用电成本。\n- 运行过程中几乎不产生排放。"
                  }
                ]
              }
            }
          ]
        },
        "usage": {
          "input_tokens": 25,
          "output_tokens": 613,
          "total_tokens": 638
        },
        "request_id": "1486945b-ebc7-93a1-af4d-651f8e18e76f"
      }
      ```
    </Accordion>
  </Tab>
</Tabs>

## 异步调用

同步调用跑通后，可通过异步调用提升高并发场景下的吞吐量。

<Tabs>
  <Tab title="OpenAI Compatible -- Chat Completions API">
    <CodeGroup>
      ```python Python
      import os
      import asyncio
      from openai import AsyncOpenAI
      import platform

      # 创建异步客户端实例
      client = AsyncOpenAI(
        # 如果未设置环境变量，请将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
      )

      # 定义异步任务
      async def task(question):
        print(f"发送问题：{question}")
        response = await client.chat.completions.create(
          messages=[
            {"role": "user", "content": question}
          ],
          model="qwen3.7-plus",
        )
        print(f"模型回复：{response.choices[0].message.content}")

      # 主异步函数
      async def main():
        questions = [
          "用三个要点概括太阳能的优势。",
          "为产品发布邮件写一个主题行。",
          '将"欢迎使用我们的平台"翻译成西班牙语。'
        ]
        tasks = [task(q) for q in questions]
        await asyncio.gather(*tasks)

      if __name__ == '__main__':
        # 设置事件循环策略
        if platform.system() == 'Windows':
          asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        # 运行主协程
        asyncio.run(main(), debug=False)

      ```

      ```java Java
      import com.openai.client.OpenAIClientAsync;
      import com.openai.client.okhttp.OpenAIOkHttpClientAsync;
      import com.openai.models.chat.completions.ChatCompletionCreateParams;

      import java.util.Arrays;
      import java.util.List;
      import java.util.concurrent.CompletableFuture;

      public class Main {
        public static void main(String[] args) {
          // 创建连接 DashScope 兼容端点的 OpenAI 异步客户端
          OpenAIClientAsync client = OpenAIOkHttpClientAsync.builder()
              // 如果未设置环境变量，请将下行替换为：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
              .build();

          // 定义问题列表
          List<String> questions = Arrays.asList(
              "用三个要点概括太阳能的优势。",
              "为产品发布邮件写一个主题行。",
              "将\"欢迎使用我们的平台\"翻译成西班牙语。"
          );

          // 创建异步任务列表
          CompletableFuture<?>[] futures = questions.stream()
              .map(question -> CompletableFuture.supplyAsync(() -> {
                System.out.println("发送问题：" + question);
                // 创建 ChatCompletion 参数
                ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                    .model("qwen3.7-plus")
                    .addSystemMessage("You are a helpful assistant.")
                    .addUserMessage(question)
                    .build();

                // 发送异步请求并处理响应
                return client.chat().completions().create(params)
                  .thenAccept(chatCompletion -> {
                    String content = chatCompletion.choices().get(0).message().content().orElse("未返回内容");
                    System.out.println("模型回复：" + content);
                  })
                  .exceptionally(e -> {
                    System.err.println("错误：" + e.getMessage());
                    return null;
                  });
              }).thenCompose(future -> future))
              .toArray(CompletableFuture[]::new);

          // 等待所有异步操作完成
          CompletableFuture.allOf(futures).join();
        }
      }
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    DashScope SDK 仅在 Python 中支持异步文本生成调用。

    ```python
    # DashScope Python SDK 版本须 >= 1.19.0
    import asyncio
    import platform
    from dashscope.aigc.generation import AioGeneration
    import os
    import dashscope
    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    # 定义异步任务
    async def task(question):
      print(f"发送问题：{question}")
      response = await AioGeneration.call(
        # 如果未设置环境变量，请将下行替换为：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen-plus",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": question}],
        result_format="message",
      )
      if response.status_code == 200:
        print(f"模型回复：{response.output.choices[0].message.content}")
      else:
        print(f"请求失败：code={response.status_code}, message={response.message}")

    # 主异步函数
    async def main():
      questions = [
        "用三个要点概括太阳能的优势。",
        "为产品发布邮件写一个主题行。",
        '将"欢迎使用我们的平台"翻译成西班牙语。'
      ]
      tasks = [task(q) for q in questions]
      await asyncio.gather(*tasks)

    if __name__ == '__main__':
      # 设置事件循环策略
      if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
      # 运行主协程
      asyncio.run(main(), debug=False)
    ```
  </Tab>
</Tabs>

**响应**

<Note>
  由于调用是异步的，响应顺序可能与示例不同。
</Note>

```text
发送问题：用三个要点概括太阳能的优势。
发送问题：为产品发布邮件写一个主题行。
发送问题：将"欢迎使用我们的平台"翻译成西班牙语。
模型回复：- 减少对化石燃料的依赖。
- 降低长期用电成本。
- 运行过程中几乎不产生排放。
模型回复：Meet our newest product launch
模型回复：Bienvenido a nuestra plataforma.
```

## 生产优化

### 构建更优质的上下文

将原始数据直接输入大语言模型会因上下文长度限制导致成本上升、质量下降。上下文工程通过动态加载精准知识来提升输出质量和效率。核心技术包括：

- **Prompt 工程**：设计和优化提示词，引导模型生成预期的输出。详见[文本生成 Prompt 指南](/developer-guides/accuracy-tuning/text-generation)。
- **检索增强生成（RAG）**：当模型需要基于产品文档、技术手册等外部知识库回答问题时使用。
- **工具调用**：让模型获取天气、交通等实时数据，或执行调用 API、发送邮件等操作。
- **记忆机制**：为模型提供短期和长期记忆，使其理解对话历史。

### 探索更多文本生成功能

适用于复杂场景：

- [多轮对话](/developer-guides/run-and-scale/multi-turn)：适用于追问、信息采集等需要连续对话的场景。
- [流式输出](/developer-guides/run-and-scale/streaming)：适用于聊天机器人或实时代码生成，提升用户体验并避免长响应导致的超时。
- [深度思考](/developer-guides/text-generation/thinking)：适用于复杂推理或政策分析等需要高质量结构化回答的场景。
- [结构化输出](/developer-guides/text-generation/structured-output)：当需要模型以稳定的 JSON 格式回复，用于程序化处理或数据解析时使用。
- [续写模式](/developer-guides/text-generation/partial-mode)：适用于代码补全或长文写作，让模型从现有文本继续生成。

## 参考

完整的模型调用参数列表，请参见 [OpenAI Compatible API 参考](/api-reference/chat/openai-chat)和 [DashScope API 参考](/api-reference/chat/dashscope)。

## 常见问题

**为什么输入 Token 数比我发送的文本 Token 数多？**

在处理对话时，系统会使用对话模板（Chat Template）对输入的原始文本进行包装，添加角色标识、消息边界等控制标记。这些由系统添加的标记同样会计入 Token。

例如，向 `qwen3.8-max` 发送消息 `{"role": "user", "content": "你好"}`，"你好"在分词（Tokenize）后仅对应 1 个 Token，但系统处理时，实际输入完整文本为 `<|im_start|>user\n你好<|im_end|>\n<|im_start|>assistant\n<think>`，分词后总 Token 数会增加到 11 个。

**为什么 Qwen API 无法解析网页链接？**

Qwen API 无法直接访问或解析网页链接。你可以使用[工具调用](/developer-guides/tool-calling/function-calling)，或结合 Python Beautiful Soup 等网页抓取工具来读取网页内容。

**为什么通义千问 Web 端和 API 的回复不同？**

通义千问 Web 端在 Qwen API 基础上做了额外的工程优化，支持网页解析、联网搜索、绘图、PPT 生成等功能。这些能力不属于大语言模型 API 本身，你可以通过[工具调用](/developer-guides/tool-calling/function-calling)来实现类似效果。

**模型能直接生成 Word、Excel、PDF 或 PPT 文件吗？**

不能。千问AI平台文本生成模型仅输出纯文本，你可以通过代码或第三方库将文本转换为所需格式。
