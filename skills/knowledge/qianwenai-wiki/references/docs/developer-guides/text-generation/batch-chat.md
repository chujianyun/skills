> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 批量推理

> 同步等待结果的批量对话接口，费用低至实时调用的 50%

对于数据标注、内容生成等无需实时响应的场景，实时推理 API 存在成本高、并发受限的问题。千问AI平台的 Batch Chat API 保持了与实时 API 一致的同步调用方式，您只需发起请求等待最终结果返回。目前该功能享有**官网限时 5 折优惠**，能将您的推理成本直接降低 50%。

<Note>
  本接口仅支持提交单个请求。如需一次性传入多个请求，可通过文件方式提交，详情请参考 [Batch（文件输入）](/developer-guides/text-generation/batch)。
</Note>

## 工作原理

1. **请求提交**：客户端发起请求并建立连接。
2. **连接保持**：请求进入队列排队，客户端保持连接等待。
3. **同步返回**：请求处理完成后，服务端通过之前保持的连接，将完整结果一次性返回给客户端。

<Note>
  如果超过最长等待时间，连接将自动断开并返回超时错误。
</Note>

## 适用范围

支持的模型：

- **[文本生成模型](/developer-guides/text-generation/quickstart)**：qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.7-flash、qwen3.6-plus、qwen3.6-flash、qwen3.5-plus、qwen3.5-flash、qwen3-max、qwen-plus、qwen-flash、deepseek-v3.2
- **[图像与视频理解模型](/developer-guides/multimodal/vision)**：qwen3.8-max、qwen3.7-plus、qwen3.7-flash、qwen3.6-plus、qwen3.6-flash、qwen3.5-plus、qwen3.5-flash、qwen3.5-omni-plus、qwen3-vl-plus、qwen3-vl-flash

<Warning>
  * 在 Batch 场景下，`qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.7-flash`、`qwen3.6-plus`、`qwen3.6-flash`、`qwen3.5-plus`、`qwen3.5-flash` 和 `qwen3.5-omni-plus` 单次请求的上下文 Token 数最大支持 256K。`qwen3.5-omni-plus` 不支持语音输出。
  * 部分模型支持思考模式，开启后会产生思考 `tokens` 导致成本增加。
  * `qwen3.8`、`qwen3.7`、`qwen3.6` 和 `qwen3.5` 系列模型默认开启思考模式。建议使用混合思考模型时，显式设置 `enable_thinking` 参数（`true` 开启 / `false` 关闭）。
  * 在 JSONL 请求体中，`enable_thinking` 为 `body` 的顶层参数，须与 `model` 同级传入，不能放在 `extra_body` 中。
</Warning>

## 如何使用

### 前提条件

- 已开通千问AI平台服务，并已[获取 API Key](/api-reference/preparation/api-key)。

  <Note>
    建议[配置 API Key 到环境变量](/api-reference/preparation/export-api-key-env)中以降低 API Key 的泄露风险。
  </Note>

- 若通过 OpenAI SDK 进行调用，需要安装 SDK：

```bash
pip3 install -U openai
```

### 步骤 1：配置 API 端点

只需修改 API 端点（`base_url`），即可轻松将现有的实时推理请求切换至批量推理。请根据调用方式，配置正确的 API 端点。

- **SDK 配置**：将 `base_url` 设置为 `https://batch.dashscope.aliyuncs.com/compatible-mode/v1`
- **HTTP 调用**：请求端点为 `POST https://batch.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions`

### 步骤 2：发起调用

此处以文本对话为例，展示如何调用 Batch Chat 接口。

请求的默认等待超时时间为 3600 秒（1 小时），在多数情况下无需额外配置。

<Note>
  下方示例展示如何主动设置一个自定义的超时时间（60-3600 秒）作为参考。
</Note>

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    # 若没有配置环境变量，可用 API Key 将下行替换为：api_key="sk-xxx"
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://batch.dashscope.aliyuncs.com/compatible-mode/v1",
  ).with_options(timeout=1800.0)  # 设置 1800 秒（30 分钟）的等待时间，最长 3600 秒

  completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "你是谁？"},
    ]
  )
  print(completion.choices[0].message.content)
  ```

  ```java Java
  import com.openai.client.OpenAIClient;
  import com.openai.client.okhttp.OpenAIOkHttpClient;
  import com.openai.models.chat.completions.ChatCompletion;
  import com.openai.models.chat.completions.ChatCompletionCreateParams;

  import java.time.Duration;

  public class Main {
    public static void main(String[] args) {
      OpenAIClient client = OpenAIOkHttpClient.builder()
        // 若没有配置环境变量，可用 API Key 将下行替换为：.apiKey("sk-xxx")
        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
        .baseUrl("https://batch.dashscope.aliyuncs.com/compatible-mode/v1")
        .timeout(Duration.ofSeconds(1800))  // 设置等待时间 1800 秒（半小时），最长 3600 秒
        .build();

      ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
        .addUserMessage("你是谁")
        .model("qwen-plus")
        .build();

      try {
        ChatCompletion chatCompletion = client.chat().completions().create(params);
        System.out.println(chatCompletion);
      } catch (Exception e) {
        System.err.println("Error occurred: " + e.getMessage());
        e.printStackTrace();
      }
    }
  }
  ```

  ```javascript Node.js
  import OpenAI from "openai";

  const openai = new OpenAI({
    // 若没有配置环境变量，请用 API Key 将下行替换为：apiKey: "sk-xxx"
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://batch.dashscope.aliyuncs.com/compatible-mode/v1",
    // 超时设置（单位：毫秒），最长支持 3,600,000 毫秒
    timeout: 1800 * 1000,
  });

  async function main() {
    const completion = await openai.chat.completions.create({
      model: "qwen-plus",
      messages: [
        { role: "system", content: "You are a helpful assistant." },
        { role: "user", content: "你是谁？" }
      ],
    });
    console.log(JSON.stringify(completion));
  }

  main();
  ```

  ```go Go
  package main

  import (
    "context"
    "os"
    "time"

    "github.com/openai/openai-go"
    "github.com/openai/openai-go/option"
  )

  func main() {
    client := openai.NewClient(
      option.WithAPIKey(os.Getenv("DASHSCOPE_API_KEY")),
      option.WithBaseURL("https://batch.dashscope.aliyuncs.com/compatible-mode/v1"),
    )
    // 设置超时时间：1800 秒 = 30 分钟，最长支持 3600 秒
    ctx, cancel := context.WithTimeout(context.Background(), 3600*time.Second)
    defer cancel()

    chatCompletion, err := client.Chat.Completions.New(
      ctx, openai.ChatCompletionNewParams{
        Messages: []openai.ChatCompletionMessageParamUnion{
          openai.UserMessage("你是谁"),
        },
        Model: "qwen-plus",
      },
    )

    if err != nil {
      panic(err.Error())
    }

    println(chatCompletion.Choices[0].Message.Content)
  }
  ```

  ```csharp C#（HTTP）
  using System;
  using System.Net.Http;
  using System.Net.Http.Headers;
  using System.Text;
  using System.Threading.Tasks;

  class Program
  {
    private static readonly HttpClient httpClient = new HttpClient
    {
      // 设置超时时间：1800 秒 = 30 分钟，最长支持 3600 秒
      Timeout = TimeSpan.FromSeconds(1800)
    };

    static async Task Main(string[] args)
    {
      // 若没有配置环境变量，请用 API Key 将下行替换为：string? apiKey = "sk-xxx";
      string? apiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY");

      if (string.IsNullOrEmpty(apiKey))
      {
        Console.WriteLine("API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。");
        return;
      }

      string url = "https://batch.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions";
      string jsonContent = @"{
        ""model"": ""qwen-plus"",
        ""messages"": [
          {
            ""role"": ""system"",
            ""content"": ""You are a helpful assistant.""
          },
          {
            ""role"": ""user"",
            ""content"": ""你是谁？""
          }
        ]
      }";

      string result = await SendPostRequestAsync(url, jsonContent, apiKey);
      Console.WriteLine(result);
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
          return $"请求失败: {response.StatusCode}";
        }
      }
    }
  }
  ```

  ```php PHP（HTTP）
  <?php
  $url = 'https://batch.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions';
  // 若没有配置环境变量，请用 API Key 将下行替换为：$apiKey = "sk-xxx";
  $apiKey = getenv('DASHSCOPE_API_KEY');
  $headers = [
    'Authorization: Bearer ' . $apiKey,
    'Content-Type: application/json'
  ];
  $data = [
    "model" => "qwen-plus",
    "messages" => [
      [
        "role" => "system",
        "content" => "You are a helpful assistant."
      ],
      [
        "role" => "user",
        "content" => "你是谁？"
      ]
    ]
  ];
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_POST, true);
  curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
  // 设置超时时间：1800 秒 = 30 分钟，最长支持 3600 秒
  curl_setopt($ch, CURLOPT_TIMEOUT, 1800);
  $response = curl_exec($ch);
  if (curl_errno($ch)) {
    echo 'Curl error: ' . curl_error($ch);
  }
  curl_close($ch);
  echo $response;
  ?>
  ```

  ```bash curl
  curl -X POST https://batch.dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    --max-time 1800 \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "qwen-plus",
      "messages": [
        {
          "role": "system",
          "content": "You are a helpful assistant."
        },
        {
          "role": "user",
          "content": "你是谁？"
        }
      ]
    }'
  ```
</CodeGroup>

**响应示例**

```json
{
  "created": 1763622152,
  "usage": {
    "completion_tokens": 79,
    "prompt_tokens": 22,
    "total_tokens": 101
  },
  "model": "qwen-plus",
  "id": "chatcmpl-daa344d2-60df-9b79-81a4-28c9a10a0a0e",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "我是千问，阿里巴巴集团旗下的超大规模语言模型。我能够回答问题、创作文字，如写故事、公文、邮件、剧本等，还能进行逻辑推理、编程，表达观点，玩游戏等。我支持多种语言，包括但不限于中文、英文、德语、法语、西班牙语等。如果你有任何问题或需要帮助，欢迎随时告诉我！"
      }
    }
  ],
  "object": "chat.completion"
}
```

## 使用限制

- **等待时间**：提交请求后，会同步等待结果，服务端最长会保持连接 3600 秒（1 小时）。可根据实际需求设置自定义超时时间，取值范围为 60-3600 秒。
- **并发限制**：单个账户为每个模型最多可维持 10,000 个等待中的请求。超出此限制的新请求将被拒绝并返回相应错误码，直到有请求完成并释放出可用位置。
- **调用速率**：单个账户提交请求的频率上限为 1000 QPS（10,000 次 / 10 秒）。

  <Note>
    此上限为系统设定的理论最大值。在实际调用中，API 的可用资源会受到整体系统负载的动态影响，建议您在代码中实现重试逻辑。
  </Note>

## 计费说明

- **计费单价**：按成功请求的输入和输出 Token 计费，目录价与对应模型实时调用价格一致。**官网限时为 Batch Chat 调用提供 5 折优惠，其最终费用为实时调用价格的 50%**，具体请参见[计费说明](/developer-guides/getting-started/pricing)。
- **计费范围**：仅对任务中成功执行的请求进行计费。任何失败的请求（包括系统错误或超时）均不计费。

<Note>
  * 批量推理为独立计费项，不支持免费额度等优惠，以及[上下文缓存](/developer-guides/run-and-scale/context-cache)等功能。
  * 部分模型（如 qwen3.8-max、qwen3.7-max、qwen3.7-plus 及 qwen3.6、qwen3.5 系列）默认开启思考模式，会产生额外的思考 tokens，并按输出 token 价格计费，导致成本增加。建议根据任务复杂度设置 `enable_thinking` 参数以控制成本，具体请参考[深度思考](/developer-guides/text-generation/thinking)。
</Note>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](/api-reference/preparation/error-messages)进行解决。

## 常见问题

**Batch Chat 请求耗时和实时 API 比较有区别吗？**

有区别。Batch Chat 请求需要排队等待调度，因此端到端耗时通常高于实时 API。请求在服务端最长等待时间为 1 小时，超时未执行将自动断开并返回错误。

**如何选择使用 Batch Chat 还是 Batch（文件输入）？**

当业务逻辑需要以 API 同步调用的方式、高并发地提交大量独立的对话请求时，选择 Batch Chat。当需要处理的是包含大量请求的单个大文件，并且可以接受异步获取结果文件，则选择 [Batch（文件输入）](/developer-guides/text-generation/batch)。

**Batch Chat 能保证请求全部完成吗？**

不保证。Batch Chat 使用的是 Batch 资源，完成情况取决于系统资源分配情况。如果系统资源繁忙，请求可能在队列中等待。若超过最长等待时间仍未被调度执行，连接将超时断开，此时请求不会被计费，可以稍后重试。

## 相关文档

- 查看模型实时调用的完整参数列表，请参阅 [OpenAI Chat](/api-reference/chat/openai-chat)。
- 如需通过提交文件进行批量处理，并异步获取结果，请参阅 [Batch（文件输入）](/developer-guides/text-generation/batch)。
