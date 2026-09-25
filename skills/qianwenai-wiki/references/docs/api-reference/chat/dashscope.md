> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# DashScope API 参考

> 原生 SDK 与 HTTP API

<Note>
  [获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

## 接口地址

- HTTP（纯文本模型，如 `qwen-plus`）：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation`
- HTTP（多模态模型，如 `qwen3.7-plus`、`qwen3-vl-plus`）：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`
- SDK `base_http_api_url`：`https://dashscope.aliyuncs.com/api/v1`

**Python SDK**：

```python
dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
```

**Java SDK**：

```java
// 方式一：实例化时指定
import com.alibaba.dashscope.protocol.Protocol;
Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");

// 方式二：全局设置
import com.alibaba.dashscope.utils.Constants;
Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
```

## OpenAPI

````yaml post /api/v1/services/aigc/text-generation/generation
openapi: 3.1.0
info:
  title: Qwen DashScope API
  description: 通过 DashScope 原生 HTTP API 调用 Qwen 模型。支持文本和多模态模型、流式输出、工具调用和结构化输出。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com
    description: 北京
security:
  - ApiKeyAuth: []
paths:
  /api/v1/services/aigc/text-generation/generation:
    post:
      operationId: dashscopeTextGeneration
      summary: 文本生成
      description: |-
        向 Qwen 纯文本模型（如 `qwen-plus`、`qwen-turbo`、`qwen-max`）发送消息并获取生成的回复。支持多轮对话、流式输出、工具调用、结构化输出和思考模式。

        如需通过 HTTP 实现流式输出，请添加 `X-DashScope-SSE: enable` 请求头。

        如需使用多模态模型（图像、视频、音频），请使用 `/api/v1/services/aigc/multimodal-generation/generation` 端点。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DashScopeTextRequest"
            example:
              model: qwen-plus
              input:
                messages:
                  - role: system
                    content: You are a helpful assistant.
                  - role: user
                    content: Who are you?
              parameters:
                result_format: message
      responses:
        "200":
          description: 请求成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeResponse"
              example:
                status_code: 200
                request_id: 902fee3b-f7f0-9a8c-96a1-6b4ea25af114
                code: ""
                message: ""
                output:
                  text: null
                  finish_reason: null
                  choices:
                    - finish_reason: stop
                      message:
                        role: assistant
                        content: I am a large-scale language model developed by Alibaba Cloud. My name is Qwen.
                        tool_calls: null
                        reasoning_content: null
                usage:
                  input_tokens: 22
                  output_tokens: 17
                  total_tokens: 39
                  image_tokens: null
                  video_tokens: null
                  audio_tokens: null
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeError"
              example:
                status_code: 400
                request_id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
                code: InvalidParameter
                message: The parameter 'model' is required.
        "401":
          description: 鉴权失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeError"
              example:
                status_code: 401
                request_id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
                code: InvalidApiKey
                message: Invalid API key provided.
        "429":
          description: 请求超过限流
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeError"
              example:
                status_code: 429
                request_id: a1b2c3d4-e5f6-7890-abcd-ef1234567890
                code: Throttling
                message: Request was throttled.
      x-codeSamples:
        - lang: python
          label: 文本输入
          source: |-
            import os
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            messages = [
              {'role': 'system', 'content': 'You are a helpful assistant.'},
              {'role': 'user', 'content': 'Who are you?'}
            ]
            response = dashscope.Generation.call(
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen-plus',
              messages=messages,
              result_format='message'
            )
            print(response)
        - lang: python
          label: 流式输出（文本）
          source: |-
            import os
            import dashscope
            from dashscope import Generation

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            messages = [
              {'role': 'system', 'content': 'You are a helpful assistant.'},
              {'role': 'user', 'content': 'Who are you?'}
            ]
            responses = Generation.call(
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen-plus',
              messages=messages,
              result_format='message',
              stream=True,
              incremental_output=True
            )
            for response in responses:
              print(response.output.choices[0].message.content, end='', flush=True)
            print()
        - lang: curl
          label: 文本输入
          source: |-
            curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header "Content-Type: application/json" \
            --data '{
              "model": "qwen-plus",
              "input": {
                "messages": [
                  {"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": "Who are you?"}
                ]
              },
              "parameters": {"result_format": "message"}
            }'
        - lang: curl
          label: 流式输出（文本）
          source: |-
            curl --location "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header "Content-Type: application/json" \
            --header "X-DashScope-SSE: enable" \
            --data '{
              "model": "qwen-plus",
              "input": {
                "messages": [
                  {"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": "Who are you?"}
                ]
              },
              "parameters": {"result_format": "message", "stream": true, "incremental_output": true}
            }'
        - lang: java
          label: 文本输入
          source: |-
            import java.util.Arrays;
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
              public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException {
                Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");
                Message systemMsg = Message.builder().role(Role.SYSTEM.getValue()).content("You are a helpful assistant.").build();
                Message userMsg = Message.builder().role(Role.USER.getValue()).content("Who are you?").build();
                GenerationParam param = GenerationParam.builder()
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("qwen-plus")
                    .messages(Arrays.asList(systemMsg, userMsg))
                    .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                    .build();
                GenerationResult result = gen.call(param);
                System.out.println(JsonUtils.toJson(result));
              }
            }
        - lang: java
          label: 流式输出（文本）
          source: |-
            import java.util.Arrays;
            import com.alibaba.dashscope.aigc.generation.Generation;
            import com.alibaba.dashscope.aigc.generation.GenerationParam;
            import com.alibaba.dashscope.aigc.generation.GenerationResult;
            import com.alibaba.dashscope.common.Message;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.protocol.Protocol;
            import io.reactivex.Flowable;

            public class Main {
              public static void main(String[] args) throws ApiException, NoApiKeyException, InputRequiredException {
                Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");
                Message systemMsg = Message.builder().role(Role.SYSTEM.getValue()).content("You are a helpful assistant.").build();
                Message userMsg = Message.builder().role(Role.USER.getValue()).content("Who are you?").build();
                GenerationParam param = GenerationParam.builder()
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("qwen-plus")
                    .messages(Arrays.asList(systemMsg, userMsg))
                    .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                    .incrementalOutput(true)
                    .build();
                Flowable<GenerationResult> result = gen.streamCall(param);
                result.blockingForEach(r ->
                  System.out.print(r.getOutput().getChoices().get(0).getMessage().getContent())
                );
                System.out.println();
              }
            }
        - lang: php
          label: 文本输入
          source: |-
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
                    "content" => "Who are you?"
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
            curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
            curl_setopt($ch, CURLOPT_HTTPHEADER, [
              "Authorization: Bearer $apiKey",
              "Content-Type: application/json"
            ]);

            $response = curl_exec($ch);
            $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);

            if ($httpCode == 200) {
              echo "Response: " . $response;
            } else {
              echo "Error: " . $httpCode . " - " . $response;
            }

            curl_close($ch);
            ?>
        - lang: javascript
          label: 文本输入
          source: |-
            import fetch from 'node-fetch';
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
                    content: "Who are you?"
                  }
                ]
              },
              parameters: {
                result_format: "message"
              }
            };

            fetch('https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation', {
              method: 'POST',
              headers: {
                'Authorization': `Bearer ${apiKey}`,
                'Content-Type': 'application/json'
              },
              body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
              console.log(JSON.stringify(data));
            })
            .catch(error => {
              console.error('Error:', error);
            });
        - lang: csharp
          label: 文本输入
          source: |-
            using System.Net.Http.Headers;
            using System.Text;

            class Program
            {
              private static readonly HttpClient httpClient = new HttpClient();

              static async Task Main(string[] args)
              {
                // 如果未设置环境变量，请将下面一行替换为 string? apiKey = "sk-xxx";
                string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");

                if (string.IsNullOrEmpty(apiKey))
                {
                  Console.WriteLine("未设置 API Key。请确保已设置环境变量 'DASHSCOPE_API_KEY'。");
                  return;
                }

                // 设置请求 URL 和内容。
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
                        ""content"": ""Who are you?""
                      }
                    ]
                  },
                  ""parameters"": {
                    ""result_format"": ""message""
                  }
                }";

                // 发送请求并获取响应。
                string result = await SendPostRequestAsync(url, jsonContent, apiKey);

                // 输出结果。
                Console.WriteLine(result);
              }

              private static async Task<string> SendPostRequestAsync(string url, string jsonContent, string apiKey)
              {
                using (var content = new StringContent(jsonContent, Encoding.UTF8, "application/json"))
                {
                  // 设置请求头。
                  httpClient.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", apiKey);
                  httpClient.DefaultRequestHeaders.Accept.Add(new MediaTypeWithQualityHeaderValue("application/json"));

                  // 发送请求并获取响应。
                  HttpResponseMessage response = await httpClient.PostAsync(url, content);

                  // 处理响应。
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
        - lang: go
          label: 文本输入
          source: |-
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

            type Message struct {
              Role    string `json:"role"`
              Content string `json:"content"`
            }

            type Input struct {
              Messages []Message `json:"messages"`
            }

            type Parameters struct {
              ResultFormat string `json:"result_format"`
            }

            type RequestBody struct {
              Model      string     `json:"model"`
              Input      Input      `json:"input"`
              Parameters Parameters `json:"parameters"`
            }

            func main() {
              // 创建 HTTP 客户端。
              client := &http.Client{}

              // 构建请求体。
              requestBody := RequestBody{
                Model: "qwen-plus",
                Input: Input{
                  Messages: []Message{
                    {
                      Role:    "system",
                      Content: "You are a helpful assistant.",
                    },
                    {
                      Role:    "user",
                      Content: "Who are you?",
                    },
                  },
                },
                Parameters: Parameters{
                  ResultFormat: "message",
                },
              }

              jsonData, err := json.Marshal(requestBody)
              if err != nil {
                log.Fatal(err)
              }

              // 创建 POST 请求。
              req, err := http.NewRequest("POST", "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation", bytes.NewBuffer(jsonData))
              if err != nil {
                log.Fatal(err)
              }

              // 设置请求头。
              // 如果未设置环境变量，请将下面一行替换为 apiKey := "sk-xxx"。
              apiKey := os.Getenv("DASHSCOPE_API_KEY")
              req.Header.Set("Authorization", "Bearer "+apiKey)
              req.Header.Set("Content-Type", "application/json")

              // 发送请求。
              resp, err := client.Do(req)
              if err != nil {
                log.Fatal(err)
              }
              defer resp.Body.Close()

              // 读取响应体。
              bodyText, err := io.ReadAll(resp.Body)
              if err != nil {
                log.Fatal(err)
              }

              // 输出响应。
              fmt.Printf("%s\n", bodyText)
            }
components:
  securitySchemes:
    ApiKeyAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    DashScopeTextRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 调用的模型名称。支持 Qwen 大语言模型（商业版和开源版）、Qwen-Coder、数学模型、DeepSeek（阿里云直供、硅基流动直供）、Kimi（阿里云直供）、GLM（阿里云直供）、MiniMax（阿里云直供、稀宇科技直供）。模型列表详见[文本生成 — Qwen](/developer-guides/getting-started/text-generation-models)。
          example: qwen-plus
        input:
          type: object
          required:
            - messages
          description: 模型的输入。
          properties:
            messages:
              type: array
              description: 对话上下文，以有序的消息列表形式提供。每条消息为 system、user、assistant 或 tool 消息对象。
              items:
                $ref: "#/components/schemas/Message"
        parameters:
          $ref: "#/components/schemas/TextParameters"
    DashScopeMultimodalRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 调用的多模态模型名称，如 `qwen3.7-plus` 或 `qwen3-vl-plus`。
          example: qwen3-vl-plus
        input:
          type: object
          required:
            - messages
          description: 模型的输入。
          properties:
            messages:
              type: array
              description: 对话上下文。对于多模态模型，用户消息的 `content` 字段为内容部分的数组（文本、图像、视频）。
              items:
                $ref: "#/components/schemas/MultimodalMessage"
        parameters:
          $ref: "#/components/schemas/MultimodalParameters"
    Message:
      oneOf:
        - title: 系统消息
          type: object
          required:
            - role
            - content
          description: 设置模型的角色、语气、任务目标或约束条件。通常放在 messages 数组的首位。QwQ 模型请勿设置此消息。QVQ 模型设置后不生效。
          properties:
            role:
              type: string
              enum:
                - system
              description: 固定为 `system`。
            content:
              type: string
              description: 为模型设定上下文的系统消息内容。
        - title: 用户消息
          type: object
          required:
            - role
            - content
          description: 向模型传递问题、指令或上下文信息。
          properties:
            role:
              type: string
              enum:
                - user
              description: 固定为 `user`。
            content:
              oneOf:
                - type: string
                  description: 纯文本输入。
                - type: array
                  description: 多模态输入（图像、视频、文件）或显式缓存的内容部分数组。
                  items:
                    type: object
                    properties:
                      text:
                        type: string
                        description: 输入文本。
                      image:
                        type: string
                        description: 图像，支持公开 URL、base64（data:image/<format>;base64,<data>）或本地文件路径。适用模型：Qwen-VL、QVQ。使用示例详见[视觉理解指南](/developer-guides/multimodal/vision)。
                      video:
                        oneOf:
                          - type: string
                          - type: array
                            items:
                              type: string
                        description: 视频，支持文件 URL（字符串）或图像 URL 列表（数组）。适用模型：Qwen-VL、QVQ。使用示例详见[视觉理解指南](/developer-guides/multimodal/vision)。
                      fps:
                        type: number
                        minimum: 0.1
                        maximum: 10
                        description: |-
                          视频抽帧的帧率。取值范围：[0.1, 10]。默认值：2.0。

                          `fps` 参数有两个作用：
                          - **抽帧频率**：传入视频文件时，控制抽帧的频率（每 1/fps 秒抽取一帧）。适用于 Qwen-VL 和 QVQ 模型。
                          - **时序理解**：告知模型相邻帧之间的时间间隔，帮助模型理解视频的时序动态。适用于视频文件和图像列表，适合事件时间定位或按片段进行内容总结。支持 Qwen3.5、Qwen3-VL、Qwen2.5-VL 和 QVQ 模型。

                          较大的 `fps` 值适合高速运动场景（体育、动作片）。较小的值适合长视频或静态内容。
                      max_frames:
                        type: integer
                        description: |-
                          视频最大抽帧数。如果计算得到的帧数超过此限制，系统会均匀采样以保持在限制范围内。

                          **各模型的默认值和最大值：**
                          - qwen3.5 系列、qwen3-vl-plus 系列、qwen3-vl-flash 系列、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct：**2000**
                          - qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：**512**

                          使用 OpenAI 兼容 API 时不支持自定义 `max_frames`，API 会自动使用各模型的默认值。
                      min_pixels:
                        type: integer
                        description: |-
                          输入图像或视频帧的最小像素数。低于此阈值的图像会被放大。

                          **各模型默认值：**

                          **图像输入**：
                          - Qwen3.5、Qwen3-VL：最小值和默认值 = **65536**
                          - qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：最小值和默认值 = **4096**
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：最小值和默认值 = **3136**

                          **视频输入**（视频文件或图像列表）：
                          - Qwen3.5、Qwen3-VL（商业版和开源版）、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：默认值 = **65536**，最小值 = **4096**
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：默认值 = **50176**，最小值 = **3136**
                      max_pixels:
                        type: integer
                        description: |-
                          输入图像或视频帧的最大像素数。像素数在 [min_pixels, max_pixels] 范围内的图像按原始分辨率处理。超过 max_pixels 的图像会被缩小。

                          **图像输入**（取决于 `vl_high_resolution_images`）：

                          当 `vl_high_resolution_images` 为 **false** 时：
                          - Qwen3.5、Qwen3-VL：默认值 = **2621440**，最大值 = **16777216**
                          - qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：默认值 = **1310720**，最大值 = **16777216**
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：默认值 = **1003520**，最大值 = **12845056**

                          当 `vl_high_resolution_images` 为 **true** 时：
                          - Qwen3.5、Qwen3-VL、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：max_pixels **被忽略**，固定为 **16777216**
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：max_pixels **被忽略**，固定为 **12845056**

                          **视频输入**（视频文件或图像列表）：
                          - qwen3.5 系列、qwen3-vl-plus 系列、qwen3-vl-flash 系列、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct：默认值 = **655360**，最大值 = **2048000**
                          - 其他 Qwen3-VL 开源模型、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：默认值 = **655360**，最大值 = **786432**
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：默认值 = **501760**，最大值 = **602112**
                      total_pixels:
                        type: integer
                        description: |-
                          所有视频帧的最大总像素数，计算方式为（每帧像素数）×（总帧数）。超过此限制时，系统会缩小帧的分辨率，同时保持单帧像素数在 [min_pixels, max_pixels] 范围内。适用于 Qwen-VL 和 QVQ 模型。处理长视频时可降低此值以减少 token 消耗。

                          **各模型默认值：**
                          - qwen3.5 系列、qwen3-vl-plus 系列、qwen3-vl-flash 系列、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct：**134217728**（对应 131072 个图像 token，每个 token 对应 32×32 像素）
                          - 其他 Qwen3-VL 开源模型、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：**67108864**（对应 65536 个图像 token，每个 token 对应 32×32 像素）
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：**51380224**（对应 65536 个图像 token，每个 token 对应 28×28 像素）
                      file:
                        type: string
                        description: 文档的公开 URL（PDF、DOCX 等）。适用模型：Qwen-VL。
                      cache_control:
                        type: object
                        description: 启用显式缓存。仅支持具有显式缓存功能的模型。
                        properties:
                          type:
                            type: string
                            enum:
                              - ephemeral
              description: 消息内容。纯文本输入使用字符串；多模态输入（图像、视频、文件）或显式缓存使用数组。
        - title: 助手消息
          type: object
          required:
            - role
          description: 模型对用户消息的回复。
          properties:
            role:
              type: string
              enum:
                - assistant
              description: 固定为 `assistant`。
            content:
              type: string
              nullable: true
              description: 消息内容。存在 `tool_calls` 时非必填。
            tool_calls:
              type: array
              description: 模型请求的工具调用。包含前一次模型响应中的一个或多个工具调用对象。
              items:
                $ref: "#/components/schemas/ToolCall"
            partial:
              type: boolean
              description: 是否启用前缀续写。支持的模型详见[前缀续写](/developer-guides/text-generation/partial-mode)。
        - title: 工具消息
          type: object
          required:
            - role
            - content
          description: 工具函数调用的输出结果。
          properties:
            role:
              type: string
              enum:
                - tool
              description: 固定为 `tool`。
            content:
              type: string
              description: 工具函数的输出结果。必须为字符串。
            tool_call_id:
              type: string
              description: 此消息对应的工具调用 ID。可从 `response.output.choices[0].message.tool_calls[$index].id` 获取。
    MultimodalMessage:
      oneOf:
        - title: 用户消息
          type: object
          required:
            - role
            - content
          description: 向模型传递包含多模态内容的问题、指令或上下文信息。
          properties:
            role:
              type: string
              enum:
                - user
              description: 固定为 `user`。
            content:
              type: array
              description: 内容部分的数组。每个部分可包含 text、image、video、file 或 cache_control 属性。
              items:
                type: object
                properties:
                  text:
                    type: string
                    description: 输入文本。
                  image:
                    type: string
                    description: 图像，支持公开 URL、base64（data:image/<format>;base64,<data>）或本地文件路径。适用模型：Qwen-VL、QVQ。使用示例详见[视觉理解指南](/developer-guides/multimodal/vision)。
                  video:
                    oneOf:
                      - type: string
                      - type: array
                        items:
                          type: string
                    description: 视频，支持文件 URL（字符串）或图像 URL 列表（数组）。适用模型：Qwen-VL、QVQ。使用示例详见[视觉理解指南](/developer-guides/multimodal/vision)。
                  fps:
                    type: number
                    minimum: 0.1
                    maximum: 10
                    description: |-
                      视频抽帧的帧率。取值范围：[0.1, 10]。默认值：2.0。

                      `fps` 参数有两个作用：
                      - **抽帧频率**：传入视频文件时，控制抽帧的频率（每 1/fps 秒抽取一帧）。适用于 Qwen-VL 和 QVQ 模型。
                      - **时序理解**：告知模型相邻帧之间的时间间隔，帮助模型理解视频的时序动态。适用于视频文件和图像列表，适合事件时间定位或按片段进行内容总结。支持 Qwen3.5、Qwen3-VL、Qwen2.5-VL 和 QVQ 模型。

                      较大的 `fps` 值适合高速运动场景（体育、动作片）。较小的值适合长视频或静态内容。
                  max_frames:
                    type: integer
                    description: |-
                      视频最大抽帧数。如果计算得到的帧数超过此限制，系统会均匀采样以保持在限制范围内。

                      **各模型的默认值和最大值：**
                      - qwen3.5 系列、qwen3-vl-plus 系列、qwen3-vl-flash 系列、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct：**2000**
                      - qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：**512**

                      使用 OpenAI 兼容 API 时不支持自定义 `max_frames`，API 会自动使用各模型的默认值。
                  min_pixels:
                    type: integer
                    description: |-
                      输入图像或视频帧的最小像素数。低于此阈值的图像会被放大。

                      **各模型默认值：**

                      **图像输入**：
                      - Qwen3.5、Qwen3-VL：最小值和默认值 = **65536**
                      - qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：最小值和默认值 = **4096**
                      - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：最小值和默认值 = **3136**

                      **视频输入**（视频文件或图像列表）：
                      - Qwen3.5、Qwen3-VL（商业版和开源版）、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：默认值 = **65536**，最小值 = **4096**
                      - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：默认值 = **50176**，最小值 = **3136**
                  max_pixels:
                    type: integer
                    description: |-
                      输入图像或视频帧的最大像素数。像素数在 [min_pixels, max_pixels] 范围内的图像按原始分辨率处理。超过 max_pixels 的图像会被缩小。

                      **图像输入**（取决于 `vl_high_resolution_images`）：

                      当 `vl_high_resolution_images` 为 **false** 时：
                      - Qwen3.5、Qwen3-VL：默认值 = **2621440**，最大值 = **16777216**
                      - qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：默认值 = **1310720**，最大值 = **16777216**
                      - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：默认值 = **1003520**，最大值 = **12845056**

                      当 `vl_high_resolution_images` 为 **true** 时：
                      - Qwen3.5、Qwen3-VL、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：max_pixels **被忽略**，固定为 **16777216**
                      - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：max_pixels **被忽略**，固定为 **12845056**

                      **视频输入**（视频文件或图像列表）：
                      - qwen3.5 系列、qwen3-vl-plus 系列、qwen3-vl-flash 系列、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct：默认值 = **655360**，最大值 = **2048000**
                      - 其他 Qwen3-VL 开源模型、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：默认值 = **655360**，最大值 = **786432**
                      - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：默认值 = **501760**，最大值 = **602112**
                  total_pixels:
                    type: integer
                    description: |-
                      所有视频帧的最大总像素数，计算方式为（每帧像素数）×（总帧数）。超过此限制时，系统会缩小帧的分辨率，同时保持单帧像素数在 [min_pixels, max_pixels] 范围内。适用于 Qwen-VL 和 QVQ 模型。处理长视频时可降低此值以减少 token 消耗。

                      **各模型默认值：**
                      - qwen3.5 系列、qwen3-vl-plus 系列、qwen3-vl-flash 系列、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct：**134217728**（对应 131072 个图像 token，每个 token 对应 32×32 像素）
                      - 其他 Qwen3-VL 开源模型、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：**67108864**（对应 65536 个图像 token，每个 token 对应 32×32 像素）
                      - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：**51380224**（对应 65536 个图像 token，每个 token 对应 28×28 像素）
                  file:
                    type: string
                    description: 文档的公开 URL（PDF、DOCX 等）。适用模型：Qwen-VL。
                  cache_control:
                    type: object
                    description: 启用显式缓存。仅支持具有显式缓存功能的模型。
                    properties:
                      type:
                        type: string
                        enum:
                          - ephemeral
        - title: 助手消息
          type: object
          required:
            - role
          description: 模型对用户消息的回复。
          properties:
            role:
              type: string
              enum:
                - assistant
              description: 固定为 `assistant`。
            content:
              type: array
              description: 模型响应中的内容部分数组。
              items:
                oneOf:
                  - title: 文本
                    type: object
                    properties:
                      text:
                        type: string
                        description: 输入文本。
                  - title: 图像
                    type: object
                    properties:
                      image:
                        type: string
                        description: 图像，支持公开 URL、base64（data:image/<format>;base64,<data>）或本地文件路径。适用模型：Qwen-VL、QVQ。使用示例详见[视觉理解指南](/developer-guides/multimodal/vision)。
                  - title: 视频
                    type: object
                    properties:
                      video:
                        oneOf:
                          - type: string
                          - type: array
                            items:
                              type: string
                        description: 视频，支持文件 URL（字符串）或图像 URL 列表（数组）。适用模型：Qwen-VL、QVQ。使用示例详见[视觉理解指南](/developer-guides/multimodal/vision)。
                      fps:
                        type: number
                        minimum: 0.1
                        maximum: 10
                        description: |-
                          视频抽帧的帧率。取值范围：[0.1, 10]。默认值：2.0。

                          `fps` 参数有两个作用：
                          - **抽帧频率**：传入视频文件时，控制抽帧的频率（每 1/fps 秒抽取一帧）。适用于 Qwen-VL 和 QVQ 模型。
                          - **时序理解**：告知模型相邻帧之间的时间间隔，帮助模型理解视频的时序动态。适用于视频文件和图像列表，适合事件时间定位或按片段进行内容总结。支持 Qwen3.5、Qwen3-VL、Qwen2.5-VL 和 QVQ 模型。

                          较大的 `fps` 值适合高速运动场景（体育、动作片）。较小的值适合长视频或静态内容。
                      max_frames:
                        type: integer
                        description: |-
                          视频最大抽帧数。如果计算得到的帧数超过此限制，系统会均匀采样以保持在限制范围内。

                          **各模型的默认值和最大值：**
                          - qwen3.5 系列、qwen3-vl-plus 系列、qwen3-vl-flash 系列、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct：**2000**
                          - qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：**512**

                          使用 OpenAI 兼容 API 时不支持自定义 `max_frames`，API 会自动使用各模型的默认值。
                      min_pixels:
                        type: integer
                        description: |-
                          输入图像或视频帧的最小像素数。低于此阈值的图像会被放大。

                          **各模型默认值：**

                          **图像输入**：
                          - Qwen3.5、Qwen3-VL：最小值和默认值 = **65536**
                          - qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：最小值和默认值 = **4096**
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：最小值和默认值 = **3136**

                          **视频输入**（视频文件或图像列表）：
                          - Qwen3.5、Qwen3-VL（商业版和开源版）、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：默认值 = **65536**，最小值 = **4096**
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：默认值 = **50176**，最小值 = **3136**
                      max_pixels:
                        type: integer
                        description: |-
                          输入图像或视频帧的最大像素数。像素数在 [min_pixels, max_pixels] 范围内的图像按原始分辨率处理。超过 max_pixels 的图像会被缩小。

                          **图像输入**（取决于 `vl_high_resolution_images`）：

                          当 `vl_high_resolution_images` 为 **false** 时：
                          - Qwen3.5、Qwen3-VL：默认值 = **2621440**，最大值 = **16777216**
                          - qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：默认值 = **1310720**，最大值 = **16777216**
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：默认值 = **1003520**，最大值 = **12845056**

                          当 `vl_high_resolution_images` 为 **true** 时：
                          - Qwen3.5、Qwen3-VL、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：max_pixels **被忽略**，固定为 **16777216**
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：max_pixels **被忽略**，固定为 **12845056**

                          **视频输入**（视频文件或图像列表）：
                          - qwen3.5 系列、qwen3-vl-plus 系列、qwen3-vl-flash 系列、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct：默认值 = **655360**，最大值 = **2048000**
                          - 其他 Qwen3-VL 开源模型、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：默认值 = **655360**，最大值 = **786432**
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：默认值 = **501760**，最大值 = **602112**
                      total_pixels:
                        type: integer
                        description: |-
                          所有视频帧的最大总像素数，计算方式为（每帧像素数）×（总帧数）。超过此限制时，系统会缩小帧的分辨率，同时保持单帧像素数在 [min_pixels, max_pixels] 范围内。适用于 Qwen-VL 和 QVQ 模型。处理长视频时可降低此值以减少 token 消耗。

                          **各模型默认值：**
                          - qwen3.5 系列、qwen3-vl-plus 系列、qwen3-vl-flash 系列、qwen3-vl-235b-a22b-thinking、qwen3-vl-235b-a22b-instruct：**134217728**（对应 131072 个图像 token，每个 token 对应 32×32 像素）
                          - 其他 Qwen3-VL 开源模型、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：**67108864**（对应 65536 个图像 token，每个 token 对应 32×32 像素）
                          - 其他 qwen-vl-plus 模型、其他 qwen-vl-max 模型、Qwen2.5-VL 开源系列、QVQ 系列：**51380224**（对应 65536 个图像 token，每个 token 对应 28×28 像素）
                  - title: 文件
                    type: object
                    properties:
                      file:
                        type: string
                        description: 文档的公开 URL（PDF、DOCX 等）。适用模型：Qwen-VL。
                      cache_control:
                        type: object
                        description: 启用显式缓存。仅支持具有显式缓存功能的模型。
                        properties:
                          type:
                            type: string
                            enum:
                              - ephemeral
            partial:
              type: boolean
              description: 是否启用前缀续写。支持的模型详见前缀续写。
    ToolCall:
      type: object
      properties:
        id:
          type: string
          description: 工具调用的 ID。
        type:
          type: string
          enum:
            - function
          description: 工具类型。目前仅支持 `function`。
        function:
          type: object
          properties:
            name:
              type: string
              description: 工具函数的名称。
            arguments:
              type: string
              description: 工具的输入参数，为 JSON 字符串。
        index:
          type: integer
          description: 此工具调用在 tool_calls 数组中的索引。
    TextParameters:
      type: object
      description: 文本模型的可选生成参数。
      properties:
        result_format:
          type: string
          enum:
            - message
            - text
          default: text
          description: |-
            返回数据的格式。多轮对话时请设为 `message`。

            **默认值：**大多数模型默认为 `text`，但 Qwen3-Max、Qwen3-VL、QwQ 和 Qwen3 开源模型（qwen3-next-80b-a3b-instruct 除外）默认为 `message`。

            使用 Qwen-VL/QVQ 模型时，设为 `text` 不生效。Qwen3-Max、Qwen3-VL 和 Qwen3 模型在思考模式下只能设为 `message`。
        temperature:
          type: number
          minimum: 0
          exclusiveMaximum: 2
          description: |-
            采样温度。控制输出的多样性。较高的值使输出更多样化，较低的值使输出更确定。取值范围：[0, 2)。

            QVQ 模型请勿修改默认温度值。

            **默认 `temperature` 值：**
            - `qwen3.8-max`（仅思考模式）：0.6，传入小于 0.6 的值会自动调整为 0.6
            - Qwen3.7（非思考模式）、Qwen3.6（非思考模式）、Qwen3.5-Omni、Qwen3.5（非思考模式）、Qwen3（非思考模式）、Qwen3-Instruct 系列、Qwen3-Coder 系列、qwen-max 系列、qwen-plus 系列（非思考模式）、qwen-flash 系列（非思考模式）、qwen-turbo 系列（非思考模式）、qwen 开源系列、qwen-coder 系列、qwen-doc-turbo、Qwen3-VL（非思考模式）：0.7
            - QVQ 系列：0.5
            - qwen-audio-turbo 系列：0.00001
            - qwen-vl 系列、qwen2.5-omni-7b：0.01
            - qwen-math 系列：0
            - Qwen3.7（思考模式）、Qwen3.6（思考模式）、Qwen3.5（思考模式）、Qwen3（思考模式）、Qwen3-Thinking、Qwen3-Omni-Captioner、QwQ 系列：0.6
            - qwen3-max-preview（思考模式）、qwen-long 系列：1.0
            - qwen-plus-character：0.92
            - qwen3-omni-flash 系列：0.9
            - Qwen3-VL（思考模式）：0.8

            **第三方模型默认 `temperature` 值：**
            - DeepSeek 系列（阿里云直供）：deepseek-v4-pro-0813、deepseek-v4-pro、deepseek-v4-flash、deepseek-v4-flash-0731、deepseek-v3.2（非思考模式）: 1.0；deepseek-v3.2（思考模式）、deepseek-v3.2-exp、deepseek-v3.1、deepseek-r1、deepseek-r1-0528、deepseek-r1-distill-qwen 蒸馏版: 0.6；deepseek-v3: 0.7
            - DeepSeek 系列（硅基流动直供）：siliconflow/deepseek-v3.2、siliconflow/deepseek-v3.1-terminus、siliconflow/deepseek-r1-0528、siliconflow/deepseek-v3-0324: 1.0
            - DeepSeek 系列（快手万擎直供）：vanchin/deepseek-v3.2-think（思考模式）: 0.6；vanchin/deepseek-v3.1-terminus: 0.7；vanchin/deepseek-v3.2-speciale、vanchin/deepseek-r1、vanchin/deepseek-v3、vanchin/deepseek-ocr: 1.0
            - Kimi 系列（阿里云直供）：kimi-k2.7-code、kimi-k2.6（思考模式）、kimi-k2.5（思考模式）、kimi-k2-thinking: 1.0；kimi-k2.6（非思考模式）、kimi-k2.5（非思考模式）、Moonshot-Kimi-K2-Instruct: 0.6
            - Kimi 系列（月之暗面直供）：kimi/kimi-k3、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code、kimi/kimi-k2.6（思考模式）、kimi/kimi-k2.5（思考模式）: 1.0；kimi/kimi-k2.6（非思考模式）、kimi/kimi-k2.5（非思考模式）: 0.6
            - GLM 系列（阿里云直供）：glm-5.1、glm-5、glm-4.7、glm-4.6: 1.0；glm-4.5、glm-4.5-air: 0.6
            - GLM 系列（智谱直供）：ZHIPU/GLM-5.1、ZHIPU/GLM-5: 0.6
            - MiniMax 系列（阿里云直供）：MiniMax-M2.5、MiniMax-M2.1: 1.0
            - MiniMax 系列（稀宇科技直供）：MiniMax/MiniMax-M3、MiniMax/MiniMax-M2.7、MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1: 1.0
            - MiMo 系列（小米直供）：mimo-v2.5-pro: 1.0，范围 [0, 1.5]
        top_p:
          type: number
          exclusiveMinimum: 0
          maximum: 1
          description: |-
            核采样阈值。较高的值使输出更多样化。取值范围：(0, 1.0]。

            **各模型默认值：**
            - Qwen3.7（思考模式）、Qwen3.6（非思考模式）、Qwen3.5-Omni、Qwen3.5（非思考模式）、Qwen3（非思考模式）、Qwen3-Instruct 系列、Qwen3-Coder 系列、qwen-max 系列、qwen-plus 系列（非思考模式）、qwen-flash 系列（非思考模式）、qwen-turbo 系列（非思考模式）、qwen 开源系列、qwen-coder 系列、qwen-long、qwq-32b-preview、qwen-doc-turbo、qwen-vl-max-2025-08-13、Qwen3-VL（非思考模式）：**0.8**
            - qwen-vl-max-2024-11-19、qwen-omni-turbo 系列：**0.01**
            - qwen-vl-plus 系列、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2025-04-08、qwen2.5-vl-3b/7b/32b/72b-instruct、qwen2.5-omni-7b：**0.001**
            - QVQ 系列、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15：**0.5**
            - qwen3-max-preview（思考模式）、qwen-math 系列、Qwen3-Omni-Flash 系列：**1.0**
            - Qwen3.7（思考模式）、Qwen3.6（思考模式）、Qwen3.5（思考模式）、Qwen3（思考模式）、Qwen3-VL（思考模式）、Qwen3-Thinking、QwQ 系列、Qwen3-Omni-Captioner、qwen-plus-character：**0.95**
            - DeepSeek 系列（阿里云直供）：deepseek-v4-pro-0813、deepseek-v4-pro、deepseek-v4-flash、deepseek-v4-flash-0731、deepseek-v3.2、deepseek-v3.2-exp、deepseek-v3.1、deepseek-r1、deepseek-r1-0528、deepseek-r1-distill-qwen 蒸馏版: 0.95；deepseek-v3: 0.6
            - DeepSeek 系列（硅基流动直供）：siliconflow/deepseek-v3.2、siliconflow/deepseek-v3.1-terminus、siliconflow/deepseek-r1-0528、siliconflow/deepseek-v3-0324: 1.0
            - DeepSeek 系列（快手万擎直供）：vanchin/deepseek-v3.2-think、vanchin/deepseek-v3.1-terminus: 0.95；vanchin/deepseep-v3.2-speciale: 0.9；vanchin/deepseek-r1: 0.8；vanchin/deepseek-v3、vanchin/deepseek-ocr: 1.0
            - Kimi 系列（阿里云直供）：kimi-k2.7-code、kimi-k2.6、kimi-k2.5、kimi-k2-thinking: 0.95；Moonshot-Kimi-K2-Instruct: 1.0
            - Kimi 系列（月之暗面直供）：kimi/kimi-k2.7-code、kimi/kimi-k2.6、kimi/kimi-k2.5: 0.95
            - GLM 系列（阿里云直供）：0.95
            - GLM 系列（智谱直供）：ZHIPU/GLM-5.1、ZHIPU/GLM-5: 0.95
            - MiniMax 系列（阿里云直供）：MiniMax-M2.5、MiniMax-M2.1: 0.95
            - MiniMax 系列（稀宇科技直供）：MiniMax/MiniMax-M2.7、MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1: 0.9
            - MiMo 系列（小米直供）：xiaomi/mimo-v2.5-pro: 0.95，范围 [0.01, 1.0]

            QVQ 模型请勿修改默认 `top_p` 值。
        top_k:
          type: integer
          minimum: 0
          description: |-
            采样候选 token 集合的大小。较大的值增加随机性，较小的值增加确定性。如果为 `None` 或大于 100，则 top_k 不生效，仅 top_p 起作用。必须 >= 0。

            **各模型默认值：**
            - QVQ 系列、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15：**10**
            - QwQ 系列：**40**
            - 其他 Qwen-VL-Plus 系列、2025 年 8 月 13 日之前发布的 Qwen-VL-Max 模型、qwen2.5-omni-7b：**1**
            - Qwen3-Omni-Flash 系列：**50**
            - GLM 系列（阿里云直供）：**20**
            - DeepSeek/Kimi/MiniMax 系列均不支持 top_k 参数
            - 所有其他模型：**20**

            QVQ 模型请勿修改默认 `top_k` 值。
        max_tokens:
          type: integer
          description: |-
            （即将废弃，新接入请使用 `max_completion_tokens`）生成的最大 token 数。达到限制时，生成停止且 `finish_reason` 为 `length`。不限制思考链长度。默认为模型的最大输出长度。

            **注意：** 对于 GLM-5.2 及之后的 GLM 系列模型，`max_tokens` 的行为与 `max_completion_tokens` 一致——它限制包含思维链在内的总输出长度，而非仅限制最终回复。建议对 GLM-5.2 系列模型直接使用 `max_completion_tokens` 以获得更明确的语义控制。
          deprecated: true
        max_completion_tokens:
          type: integer
          description: |-
            限制模型本次响应中输出的最大 Token 数，包含思维链。达到限制时，生成停止且 `finish_reason` 为 `length`。默认值与最大值均为模型的最大输出长度。

            与 `max_tokens` 的区别：`max_completion_tokens` 同时限制思考过程与最终响应的总长度，而 `max_tokens` 不限制思维链长度。思考类模型推荐使用 `max_completion_tokens`。

            **支持以下模型：**
            - 千问 Max：Qwen3.7-Max 及之后的模型
            - 千问 Plus：Qwen3.5-Plus 及之后的模型
            - 千问 Flash：Qwen3.5-Flash 及之后的模型
            - Kimi：kimi-k2.5 及之后的模型
            - GLM：glm-5 及其之后推出的GLM系列模型
            - MiniMax：MiniMax-M2.5 及之后的模型
            - DeepSeek：deepseek-v3、deepseek-r1、deepseek-r1-0528、deepseek-v3.1、deepseek-v3.2、deepseek-v3.2-exp、deepseek-v4-pro-0813、deepseek-v4-pro、deepseek-v4-flash 及之后的模型

            以上模型均不包含三方直供模型。实际输出 Token 数与设置值之间最多可能存在 10 个 Token 的误差。

            Java SDK 暂不支持该参数。通过 HTTP 调用时，请将 `max_completion_tokens` 放入 `parameters` 对象中。
        stream:
          type: boolean
          default: false
          description: "是否流式输出响应。HTTP 流式输出还需设置 `X-DashScope-SSE: enable` 请求头。Java SDK 流式输出请使用 `streamCall` 接口。"
        incremental_output:
          type: boolean
          default: false
          description: 流式输出时，是否仅返回新增的增量 token（true）还是返回到目前为止的完整累积文本（false）。
        enable_thinking:
          type: boolean
          description: 是否启用思考模式。适用于混合思考模型：Qwen3.7、Qwen3.6、Qwen3.5、Qwen3 和 Qwen3-VL 系列，以及 DeepSeek-V4-Pro/V4-Flash 系列（阿里云直供）、DeepSeek-V3.2/V3.2-exp/V3.1 系列（阿里云直供、硅基流动直供）、Kimi-K2.6/K2.5 系列（阿里云直供）、GLM 系列。qwen3.8-max 默认开启思考模式。DeepSeek-V4 系列默认开启思考，可通过 `reasoning_effort` 参数调整推理力度。启用后，思考内容通过 `reasoning_content` 字段返回。Java SDK 为 enableThinking；通过 HTTP 调用时，请将 enable_thinking 放入 parameters 对象中。
        preserve_thinking:
          type: boolean
          default: false
          description: |-
            是否将对话历史中 assistant 消息的 reasoning_content 拼接至模型输入。适用于需要模型参考历史思考过程的场景。目前支持 qwen3.8-max（默认开启）、qwen3.7-max、qwen3.7-max-2026-05-20以及后续快照、qwen3.6-max-preview、qwen3.7-plus、qwen3.7-plus-2026-05-26、qwen3.6-plus、qwen3.6-plus-2026-04-02、qwen3.7-flash、qwen3.7-flash-2026-07-15、qwen3.6-flash、qwen3.6-flash-2026-04-16、kimi-k2.6（千问AI平台部署）、kimi-k2.7-code（千问AI平台部署，默认开启）、kimi/kimi-k2.7-code-highspeed（月之暗面直供，默认开启）、kimi/kimi-k2.7-code（月之暗面直供，默认开启）。

            - 若历史消息中不包含 reasoning_content，开启此参数不会报错，正常兼容。
            - 开启后，历史对话中的 reasoning_content 会计入输入 Token 数量并计费。

            通过 HTTP 调用时，请将 preserve_thinking 放入 parameters 对象中。暂不支持 Java SDK。

            **重要：** 使用 qwen3.8-max 时，preserve_thinking 默认为 true，必须将历史对话中所有的 reasoning_content 完整回传。不支持将 reasoning_content 拼接到 content 字段中回传。
        thinking_budget:
          type: integer
          description: 思考链的最大长度。适用于 Qwen3.7、Qwen3.6、Qwen3.5、Qwen3-VL、Qwen3、GLM（阿里云直供）和 Kimi（阿里云直供）系列模型。默认为模型的最大思维链长度。Java SDK 为 thinkingBudget。通过 HTTP 调用时，请将 thinking_budget 放入 parameters 对象中。
        reasoning_effort:
          type: string
          enum:
            - low
            - medium
            - high
            - xhigh
            - max
          description: |-
            控制模型的推理力度。

            **Qwen3.8-Max 与 Qwen3.8-Max-Preview：** 可选值：`low`、`medium`、`xhigh`。默认 `xhigh`。不支持与 thinking_budget 同时设置，同时设置会报错。两者支持互转：未设置 thinking_budget 时，reasoning_effort 自动映射 thinking_budget（`low`→4096，`medium`→16384，`xhigh`→262144）；未设置 reasoning_effort 时，thinking_budget 自动映射回 reasoning_effort（0-4096→`low`，4097-16384→`medium`，16385-262144→`xhigh`）；两者均未设置时，使用默认 thinking_budget（131072），默认 reasoning_effort（`xhigh`）。

            **DeepSeek-V4 与 GLM 系列：** 可选值：`high`（高力度推理）、`max`（最大力度推理）。low 和 medium 映射为 high，xhigh 映射为 max。适用于 glm-5.2、glm-5.1、glm-5、deepseek-v4-pro-0813、deepseek-v4-pro、deepseek-v4-flash、deepseek-v4-flash-0731（阿里云直供）。

            通过 HTTP 调用时，请将 reasoning_effort 放入 parameters 对象中。
        clear_thinking:
          type: boolean
          default: false
          description: |-
            用于控制多轮对话中是否将历史轮次的 reasoning_content（思考过程）作为上下文输入给模型。仅 GLM 系列（glm-5.2、glm-5.1、glm-5、glm-4.7）模型支持。

            - `true`：开启。忽略历史轮次的 reasoning_content，仅使用可见文本、工具调用与结果等非推理内容作为上下文输入，可降低上下文长度与成本。
            - `false`（默认）：不开启。保留历史轮次的 reasoning_content 并随上下文一同提供给模型。若希望启用 Preserved Thinking，必须在 messages 中完整、未修改、按原顺序透传历史 reasoning_content，缺失、裁剪、改写或重排会导致效果下降或无法生效。

            通过 HTTP 调用时，请将 clear_thinking 放入 parameters 对象中。
        tool_stream:
          type: boolean
          default: false
          description: |-
            仅影响复杂工具参数的流式输出行为，仅在流式调用时生效。普通工具参数（所有参数类型均为 string）只要开启流式调用即可流式输出，`tool_stream` 对其无影响。复杂工具是指工具定义中某些参数类型为 array 或 object。当前仅 Qwen 和 GLM 系列支持。

            **Qwen 系列支持列表：**
            - qwen-max 系列：qwen3.7-max 系列的文本模态
            - qwen-plus 系列：qwen3.7-plus 系列、qwen3.6-plus 系列的文本模态，以及 qwen3.5-plus 系列的全模态
            - qwen-flash 系列：qwen3.7-flash 系列、qwen3.6-flash 系列、qwen3.5-flash 的全模态

            **Qwen 系列使用参考：**
            - `tool_stream=false`：复杂工具参数会一次性输出，默认行为，复杂格式会更准确。
            - `tool_stream=true`：复杂工具参数会流式输出，复杂格式没有超时风险。

            **GLM 系列支持列表：** glm-4.6、glm-4.7、glm-5、glm-5.1（阿里云直供）。

            **GLM 系列使用参考：**
            - `tool_stream=false`：工具参数会一次性输出，默认行为，复杂格式会更准确。
            - `tool_stream=true`：工具参数会流式输出，复杂格式没有超时风险。

            通过 HTTP 调用时，请将 tool_stream 放入 parameters 对象中。
        enable_code_interpreter:
          type: boolean
          default: false
          description: 是否启用代码解释器功能。
        repetition_penalty:
          type: number
          description: |-
            token 重复惩罚系数。1.0 表示不惩罚，较高的值减少重复。必须为正数。

            **第三方模型默认值：**
            - DeepSeek 系列（阿里云直供）：deepseek-v3.2-exp/v3.1: 1.0
            - GLM 系列（阿里云直供）：1.0

            使用 `qwen-vl-plus_2025-01-25` 模型进行文字识别时，请将 `repetition_penalty` 设为 1.0。QVQ 模型请勿修改默认 `repetition_penalty` 值。
        presence_penalty:
          type: number
          minimum: -2
          maximum: 2
          description: |-
            控制模型避免重复文本中已有内容的程度。取值范围：[-2.0, 2.0]。正值减少重复，负值增加重复。

            **各模型默认值：**
            - Qwen3.6（非思考模式）、Qwen3.5（非思考模式）、qwen3-max-preview（思考模式）、Qwen3（非思考模式）、Qwen3-Instruct 系列、qwen3-0.6b/1.7b/4b（思考模式）、QVQ 系列、qwen-max、qwen-max-latest、qwen2.5-vl 系列、qwen-vl-max 系列、qwen-vl-plus、Qwen3-VL（非思考模式）：**1.5**
            - qwen-vl-plus-latest、qwen-vl-plus-2025-08-15：**1.2**
            - qwen-vl-plus-2025-01-25：**1.0**
            - qwen3-8b/14b/32b/30b-a3b/235b-a22b（思考模式）、qwen-plus/qwen-plus-latest/2025-04-28（思考模式）、qwen-turbo/qwen-turbo/2025-04-28（思考模式）：**0.5**
            - 所有其他模型：**0.0**

            使用 `qwen-vl-plus-2025-01-25` 进行文字识别时，请将 `presence_penalty` 设为 1.5。QVQ 模型请勿修改默认值。
        seed:
          type: integer
          minimum: 0
          description: 随机种子，用于结果复现。取值范围：[0, 2³¹−1]。使用相同的种子和参数时，模型会尽可能返回相同的结果。
        stop:
          oneOf:
            - type: string
            - type: array
              items:
                oneOf:
                  - type: string
                  - type: integer
          description: 停止序列。当生成的文本包含指定的字符串或 token ID 时，生成立即停止。同一数组中不要混用字符串和 token ID。并非所有模型都支持，请查看模型文档。
        tools:
          type: array
          description: 用于函数调用的工具对象数组。使用工具时，必须将 `result_format` 设为 `message`。不支持 qwen-vl 系列模型。使用示例详见[函数调用指南](/developer-guides/tool-calling/function-calling)。
          items:
            type: object
            required:
              - type
              - function
            properties:
              type:
                type: string
                enum:
                  - function
                description: 工具类型。目前仅支持 `function`。
              function:
                type: object
                required:
                  - name
                  - description
                properties:
                  name:
                    type: string
                    description: 工具函数的名称。可包含字母、数字、下划线和连字符。最长 64 个字符。
                  description:
                    type: string
                    description: 工具函数的描述，帮助模型判断何时以及如何调用该函数。
                  parameters:
                    type: object
                    description: 描述函数参数的 JSON Schema 对象。默认为 `{}`。
        tool_choice:
          oneOf:
            - type: string
              enum:
                - auto
                - none
              description: "`auto`：模型自主选择工具策略。`none`：禁用此次请求的所有工具调用。"
            - type: object
              description: '强制调用指定工具：`{"type": "function", "function": {"name": "the_function_to_call"}}`。'
          default: auto
          description: 定义工具选择策略。思考模式的模型不支持强制指定工具。
        parallel_tool_calls:
          type: boolean
          default: false
          description: 是否启用并行工具调用。思考模式的模型在强制指定工具时不支持此功能。详见[并行工具调用](/developer-guides/tool-calling/function-calling)。
        response_format:
          type: object
          default:
            type: text
          description: 返回内容的格式。设为 `json_object` 时，必须在提示词中指示模型输出 JSON。
          properties:
            type:
              type: string
              enum:
                - text
                - json_object
                - json_schema
              description: 输出格式类型。`text`：纯文本。`json_object`：标准 JSON 字符串。`json_schema`：符合指定 schema 的 JSON。
            json_schema:
              type: object
              description: 当 `type` 为 `json_schema` 时必填。定义结构化输出的 JSON Schema。支持的模型详见[结构化输出](/developer-guides/text-generation/structured-output)。
              properties:
                name:
                  type: string
                  description: 唯一的 schema 名称（字母、数字、下划线、连字符；最长 64 个字符）。
                description:
                  type: string
                  description: schema 用途的描述。
                schema:
                  type: object
                  description: 定义输出数据结构的 JSON Schema 对象。
                strict:
                  type: boolean
                  default: false
                  description: 模型是否必须严格遵守所有 schema 约束。建议设为 `true`。
        logprobs:
          type: boolean
          default: false
          description: 是否返回输出 token 的对数概率。支持的模型：qwen-plus/qwen-turbo 系列的快照模型、qwen3-vl-plus/qwen3-vl-flash 系列、Qwen3 开源模型。具体支持的模型请查看模型页面。
        top_logprobs:
          type: integer
          minimum: 0
          maximum: 5
          default: 0
          description: 每个生成步骤返回的最可能候选 token 数。有效值：0–5。仅在 `logprobs` 为 `true` 时生效。支持的模型与 `logprobs` 相同。
        n:
          type: integer
          minimum: 1
          maximum: 4
          default: 1
          description: 生成的响应数量。范围：1–4。目前仅支持非思考模式的 Qwen3 模型。指定 `tools` 时固定为 1。会增加输出 token 消耗。
        vl_high_resolution_images:
          type: boolean
          default: false
          description: |-
            是否启用高分辨率图像处理。启用后使用固定分辨率策略，`max_pixels` 被忽略。默认值：false。

            **启用时（true）的像素限制：**
            - Qwen3.5 系列、Qwen3-VL 系列、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：固定为 **16777216** 像素（16384 个 token × 32×32 像素）
            - QVQ 系列和其他 Qwen2.5-VL 系列：固定为 **12845056** 像素（16384 个 token × 28×28 像素）

            为 `false` 时，像素限制由 `max_pixels` 决定。
        vl_enable_image_hw_output:
          type: boolean
          default: false
          description: 是否在响应中返回缩放后图像的尺寸（`image_hw` 字段）。流式输出时在最后一个数据块中返回。适用于 Qwen-VL 系列模型。
    MultimodalParameters:
      type: object
      description: 多模态模型的可选生成参数。
      properties:
        result_format:
          type: string
          enum:
            - message
          default: message
          description: 返回数据的格式。多模态模型仅支持 `message`。
        temperature:
          type: number
          minimum: 0
          exclusiveMaximum: 2
          description: 采样温度。控制输出的多样性。取值范围：[0, 2)。QVQ 模型请勿修改默认温度值。
        top_p:
          type: number
          exclusiveMinimum: 0
          maximum: 1
          description: |-
            核采样阈值。取值范围：(0, 1.0]。

            **各模型默认值：**
            - Qwen3.5（非思考模式）、Qwen3-VL（非思考模式）、qwen-vl-max-2025-08-13：**0.8**
            - qwen-vl-plus 系列、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-2025-04-08、qwen2.5-vl-3b/7b/32b/72b-instruct：**0.001**
            - QVQ 系列、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15：**0.5**
            - Qwen3.5（思考模式）、Qwen3-VL（思考模式）：**0.95**

            QVQ 模型请勿修改默认 `top_p` 值。
        top_k:
          type: integer
          minimum: 0
          description: |-
            采样候选 token 集合的大小。必须 >= 0。

            **各模型默认值：**
            - QVQ 系列、qwen-vl-plus-2025-07-10、qwen-vl-plus-2025-08-15：**10**
            - 其他 Qwen-VL-Plus 系列、2025 年 8 月 13 日之前发布的 Qwen-VL-Max 模型：**1**
            - 所有其他模型：**20**

            QVQ 模型请勿修改默认 `top_k` 值。
        max_tokens:
          type: integer
          description: |-
            （即将废弃，新接入请使用 `max_completion_tokens`）生成的最大 token 数。

            **注意：** 对于 GLM-5.2 及之后的 GLM 系列模型，`max_tokens` 的行为与 `max_completion_tokens` 一致——它限制包含思维链在内的总输出长度，而非仅限制最终回复。建议对 GLM-5.2 系列模型直接使用 `max_completion_tokens` 以获得更明确的语义控制。
          deprecated: true
        max_completion_tokens:
          type: integer
          description: |-
            限制模型本次响应中输出的最大 Token 数，包含思维链。达到限制时，生成停止且 `finish_reason` 为 `length`。默认值与最大值均为模型的最大输出长度。

            与 `max_tokens` 的区别：`max_completion_tokens` 同时限制思考过程与最终响应的总长度，而 `max_tokens` 不限制思维链长度。思考类模型推荐使用 `max_completion_tokens`。

            **支持以下模型：**
            - 千问 Max：Qwen3.7-Max 及之后的模型
            - 千问 Plus：Qwen3.5-Plus 及之后的模型
            - 千问 Flash：Qwen3.5-Flash 及之后的模型
            - Kimi：kimi-k2.5 及之后的模型
            - GLM：glm-5 及其之后推出的GLM系列模型
            - MiniMax：MiniMax-M2.5 及之后的模型
            - DeepSeek：deepseek-v3、deepseek-r1、deepseek-r1-0528、deepseek-v3.1、deepseek-v3.2、deepseek-v3.2-exp、deepseek-v4-pro-0813、deepseek-v4-pro、deepseek-v4-flash 及之后的模型

            以上模型均不包含三方直供模型。实际输出 Token 数与设置值之间最多可能存在 10 个 Token 的误差。

            Java SDK 暂不支持该参数。通过 HTTP 调用时，请将 `max_completion_tokens` 放入 `parameters` 对象中。
        stream:
          type: boolean
          default: false
          description: "是否流式输出响应。HTTP 流式输出还需设置 `X-DashScope-SSE: enable` 请求头。"
        enable_thinking:
          type: boolean
          description: 是否为混合思考模型（Qwen3-VL）启用思考模式。思考内容通过 `reasoning_content` 返回。
        thinking_budget:
          type: integer
          description: Qwen3-VL 模型思考链的最大长度。
        repetition_penalty:
          type: number
          description: |-
            token 重复惩罚系数。必须为正数。1.0 表示不惩罚。

            使用 `qwen-vl-plus_2025-01-25` 模型进行文字识别时，请将 `repetition_penalty` 设为 1.0。QVQ 模型请勿修改默认 `repetition_penalty` 值。
        vl_high_resolution_images:
          type: boolean
          default: false
          description: |-
            是否启用高分辨率图像处理。启用后使用固定分辨率策略，`max_pixels` 被忽略。默认值：false。

            **启用时（true）的像素限制：**
            - Qwen3.5 系列、Qwen3-VL 系列、qwen-vl-max、qwen-vl-max-latest、qwen-vl-max-0813、qwen-vl-plus、qwen-vl-plus-latest、qwen-vl-plus-0815：固定为 **16777216** 像素
            - QVQ 系列和其他 Qwen2.5-VL 系列：固定为 **12845056** 像素

            为 `false` 时，像素限制由 `max_pixels` 决定。
        vl_enable_image_hw_output:
          type: boolean
          default: false
          description: 是否在响应中返回图像高度和宽度信息（`image_hw` 字段）。适用于 Qwen-VL 系列模型。
        seed:
          type: integer
          minimum: 0
          description: 随机种子，用于结果复现。取值范围：[0, 2³¹−1]。
        incremental_output:
          type: boolean
          default: false
          description: 流式输出时，是否仅返回新增的增量 token（true）还是返回到目前为止的完整累积文本（false）。
        stop:
          oneOf:
            - type: string
            - type: array
              items:
                oneOf:
                  - type: string
                  - type: integer
          description: 停止序列。当生成的文本包含指定的字符串或 token ID 时，生成立即停止。同一数组中不要混用字符串和 token ID。
        presence_penalty:
          type: number
          minimum: -2
          maximum: 2
          description: |-
            控制模型避免重复文本中已有内容的程度。取值范围：[-2.0, 2.0]。正值减少重复，负值增加重复。

            **各模型默认值：**
            - Qwen3.5（非思考模式）、QVQ 系列、qwen-vl-max 系列、qwen-vl-plus、Qwen3-VL（非思考模式）、qwen2.5-vl 系列：**1.5**
            - qwen-vl-plus-latest、qwen-vl-plus-2025-08-15：**1.2**
            - qwen-vl-plus-2025-01-25：**1.0**
            - 所有其他模型：**0.0**

            使用 `qwen-vl-plus-2025-01-25` 进行文字识别时，请将 `presence_penalty` 设为 1.5。QVQ 模型请勿修改默认值。
        logprobs:
          type: boolean
          default: false
          description: 是否返回输出 token 的对数概率。支持 qwen3-vl-plus 系列和 qwen3-vl-flash 系列（含稳定版本模型）以及 Qwen3 开源模型。
        top_logprobs:
          type: integer
          minimum: 0
          maximum: 5
          default: 0
          description: 每个生成步骤返回的最可能候选 token 数。有效值：0–5。仅在 `logprobs` 为 `true` 时生效。
    DashScopeResponse:
      type: object
      properties:
        status_code:
          type: integer
          description: 请求的状态码。`200` 表示成功。Java SDK 不返回此字段；调用失败时会抛出包含 status_code 的异常。
        request_id:
          type: string
          description: 此请求的唯一标识符。在 Java SDK 中为 `requestId`。
        code:
          type: string
          description: 错误码。请求成功时为空字符串。仅 Python SDK 返回此字段。
        message:
          type: string
          description: 可读的错误信息。请求成功时为空字符串。
        output:
          type: object
          description: 模型的输出。
          properties:
            text:
              type: string
              nullable: true
              description: 生成的文本。当 `result_format` 为 `text` 时返回。
            finish_reason:
              type: string
              nullable: true
              description: 生成停止的原因。当 `result_format` 为 `text` 时返回。取值：`null`（仍在生成中）、`stop`（自然结束或触发停止条件）、`length`（达到最大 token 数）、`tool_calls`（触发工具调用）。
            choices:
              type: array
              description: 输出选项。当 `result_format` 为 `message` 时返回。
              items:
                type: object
                properties:
                  finish_reason:
                    type: string
                    nullable: true
                    description: 生成停止的原因。取值：`null`（生成中）、`stop`、`length`、`tool_calls`。
                  message:
                    type: object
                    description: 助手的输出消息。
                    properties:
                      role:
                        type: string
                        description: 固定为 `assistant`。
                      content:
                        oneOf:
                          - type: string
                          - type: array
                            items:
                              type: object
                              properties:
                                text:
                                  type: string
                                  description: Qwen-VL 或 Qwen-Audio 模型的输出文本内容。
                                image_hw:
                                  type: array
                                  items:
                                    type: integer
                                  description: 启用 `vl_enable_image_hw_output` 时返回。图像输入：[高度, 宽度]（像素）。视频输入：空数组。
                            description: Qwen-VL/Qwen-Audio 输出的数组项。每项可包含 `text`（字符串）和 `image_hw`（[高度, 宽度] 像素数组，启用 `vl_enable_image_hw_output` 时返回）。
                        nullable: true
                        description: 消息内容。文本模型为字符串；Qwen-VL/Qwen-Audio 模型为数组。存在 `tool_calls` 时为空。
                      reasoning_content:
                        type: string
                        nullable: true
                        description: 深度思考内容。启用思考模式时返回。
                      tool_calls:
                        type: array
                        nullable: true
                        description: 模型请求的工具调用。当模型触发函数调用时返回。
                        items:
                          $ref: "#/components/schemas/ToolCall"
                  logprobs:
                    type: object
                    nullable: true
                    description: 此选项的对数概率信息。当 `logprobs` 为 `true` 时返回。
                    properties:
                      content:
                        type: array
                        description: 包含对数概率信息的 token 数组。
                        items:
                          type: object
                          properties:
                            token:
                              type: string
                            bytes:
                              type: array
                              items:
                                type: integer
                            logprob:
                              type: number
                              nullable: true
                            top_logprobs:
                              type: array
                              items:
                                type: object
                                properties:
                                  token:
                                    type: string
                                  bytes:
                                    type: array
                                    items:
                                      type: integer
                                  logprob:
                                    type: number
                                    nullable: true
        usage:
          type: object
          description: 此请求的 token 用量信息。
          properties:
            input_tokens:
              type: integer
              description: 用户输入的 token 数。
            output_tokens:
              type: integer
              description: 模型输出的 token 数。
            total_tokens:
              type: integer
              description: 总 token 数（输入 + 输出）。纯文本输入时返回。
            image_tokens:
              type: integer
              nullable: true
              description: 输入图像的 token 数。输入包含图像时返回。
            video_tokens:
              type: integer
              nullable: true
              description: 输入视频的 token 数。输入包含视频时返回。
            audio_tokens:
              type: integer
              nullable: true
              description: 输入音频的 token 数。输入包含音频时返回。
            input_tokens_details:
              type: object
              description: Qwen-VL 和 QVQ 模型的输入 token 明细。
              properties:
                text_tokens:
                  type: integer
                image_tokens:
                  type: integer
                video_tokens:
                  type: integer
            output_tokens_details:
              type: object
              description: 输出 token 明细。
              properties:
                text_tokens:
                  type: integer
                  description: 输出文本的 token 数。
                reasoning_tokens:
                  type: integer
                  description: 思考过程的 token 数。
            prompt_tokens_details:
              type: object
              description: 输入 token 的细粒度分类。
              properties:
                cached_tokens:
                  type: integer
                  description: 命中缓存的 token 数。详见[上下文缓存](/developer-guides/run-and-scale/context-cache)。
                cache_creation_input_tokens:
                  type: integer
                  description: 用于创建显式缓存的 token 数。
                cache_type:
                  type: string
                  description: 使用显式缓存时，值为 `ephemeral`。否则不返回。
                cache_creation:
                  type: object
                  description: 显式缓存创建的相关信息。
                  properties:
                    ephemeral_5m_input_tokens:
                      type: integer
                      description: 用于创建 5 分钟显式缓存的 token 数。
    DashScopeError:
      type: object
      properties:
        status_code:
          type: integer
          description: HTTP 状态码。
        request_id:
          type: string
          description: 用于问题排查的唯一请求标识符。
        code:
          type: string
          description: 机器可读的错误码。
        message:
          type: string
          description: 可读的错误信息。
````
