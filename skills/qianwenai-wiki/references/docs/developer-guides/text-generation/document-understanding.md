> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 数据挖掘（Qwen-Doc）

> 使用 Qwen-Doc-Turbo 模型从文档中提取结构化数据，支持信息抽取、内容审核、分类打标和摘要生成。

数据挖掘模型专门针对信息抽取、内容审核、分类打标和摘要生成任务进行设计。相比通用对话模型，该模型能够快速且精确地输出规范的结构化数据（如JSON格式），解决通用对话模型返回不规范回复结构或提取信息不够准确的问题。

## 使用方式

Qwen-Doc-Turbo 支持通过以下三种方式从文件中提取信息，具体文件大小与类型限制请参考[限制](#限制)：

| 特性          | 文件URL（推荐）                     | 文件ID                                    | 纯文本                    |
| ----------- | ----------------------------- | --------------------------------------- | ---------------------- |
| **文件来源**    | 公网 URL                        | 本地文件（需先上传）                              | 字符串传入                  |
| **输入长度限制**  | 最多10个文件，支持大文件（最大输入253k Token） | 1个文件，支持大文件（最大输入253k Token）              | 9,000 Token以内          |
| **SDK 兼容性** | 仅限 `DashScope`                | 上传: `OpenAI`；调用: `OpenAI` 和 `DashScope` | `OpenAI` 和 `DashScope` |
| **核心优点**    | 无需上传至千问AI平台，支持批量调用            | 避免重复上传，适合复用                             | 无需文件管理                 |

## 前提条件

- 已[获取与配置 API Key](/api-reference/preparation/api-key)，并[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)。
- 如果通过SDK调用，还需要安装[OpenAI SDK](/api-reference/preparation/install-sdk)或[DashScope SDK](/api-reference/preparation/install-sdk)。

## 通过文件URL传入

通过文件URL直接提取结构化数据，支持最多10个文件同时处理。此处以传入[示例产品手册A](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251107/jockge/%E7%A4%BA%E4%BE%8B%E4%BA%A7%E5%93%81%E6%89%8B%E5%86%8CA.docx)与[示例产品手册B](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251107/ztwxzr/%E7%A4%BA%E4%BE%8B%E4%BA%A7%E5%93%81%E6%89%8B%E5%86%8CB.docx)文件并通过提示词约束模型以JSON格式返回所提取信息为例。

<Note>
  文件URL方式当前仅支持DashScope协议，可以选择使用DashScope Python SDK或者HTTP方式调用（如curl）。
</Note>

<CodeGroup>
  ```python Python
  import os
  import dashscope

  response = dashscope.Generation.call(
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model='qwen-doc-turbo',
    messages=[
      {"role": "system", "content": "You are a helpful assistant."},
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "从这两份产品手册中，提取所有产品信息，并整理成一个标准的JSON数组。每个对象需要包含：model(产品的型号)、name(产品的名称)、price(价格（去除货币符号和逗号）)"
          },
          {
            "type": "doc_url",
            "doc_url": [
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251107/jockge/%E7%A4%BA%E4%BE%8B%E4%BA%A7%E5%93%81%E6%89%8B%E5%86%8CA.docx",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251107/ztwxzr/%E7%A4%BA%E4%BE%8B%E4%BA%A7%E5%93%81%E6%89%8B%E5%86%8CB.docx"
            ],
            "file_parsing_strategy": "auto"
          }
        ]
      }
    ]
  )
  try:
    if response.status_code == 200:
      print(response.output.choices[0].message.content)
    else:
      print(f"请求失败，状态码: {response.status_code}")
      print(f"错误代码: {response.code}")
      print(f"错误信息: {response.message}")
  except Exception as e:
    print(f"发生错误: {e}")
  ```

  ```bash curl
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer $DASHSCOPE_API_KEY' \
  --header 'X-DashScope-SSE: enable' \
  --data '{
      "model": "qwen-doc-turbo",
      "input": {
          "messages": [
                  {
                      "role": "system",
                      "content": "You are a helpful assistant."
                  },
                  {
                      "role": "user",
                      "content": [
                          {
                              "type": "text",
                              "text": "从这两份产品手册中，提取所有产品信息，并整理成一个标准的JSON数组。每个对象需要包含：model(产品的型号)、name(产品的名称)、price(价格（去除货币符号和逗号）)"
                          },
                          {
                              "type": "doc_url",
                              "doc_url": [
                                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251107/jockge/%E7%A4%BA%E4%BE%8B%E4%BA%A7%E5%93%81%E6%89%8B%E5%86%8CA.docx",
                                  "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251107/ztwxzr/%E7%A4%BA%E4%BE%8B%E4%BA%A7%E5%93%81%E6%89%8B%E5%86%8CB.docx"
                              ],
                              "file_parsing_strategy": "auto"
                          }
                      ]
                  }
              ]
      }
  }'
  ```
</CodeGroup>

<Accordion title="响应示例">
  ```json
  [
    {
      "model": "pro-100",
      "name": "智能打印机",
      "price": "8999"
    },
    {
      "model": "pro-200",
      "name": "智能扫描仪",
      "price": "12999"
    },
    ...
    {
      "model": "sec-400",
      "name": "智能访客系统",
      "price": "9999"
    },
    {
      "model": "sec-500",
      "name": "智能停车管理",
      "price": "22999"
    }
  ]
  ```
</Accordion>

## 通过文件ID传入

### 上传文件

在运行以下代码前，请先点击[示例产品手册A](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251107/jockge/%E7%A4%BA%E4%BE%8B%E4%BA%A7%E5%93%81%E6%89%8B%E5%86%8CA.docx)下载文件，并将其放置在项目代码所在的目录中。通过OpenAI兼容接口上传到千问AI平台平台的安全存储空间，获取返回的`file-id`。有关文件上传接口的详细参数解释及调用方式，请参考[API文档](/api-reference/platform-api/file)页面进行了解。

<CodeGroup>
  ```python Python
  import os
  from pathlib import Path
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  file_object = client.files.create(file=Path("示例产品手册A.docx"), purpose="file-extract")
  # 打印file-id用于后续模型对话
  print(file_object.id)
  ```

  ```java Java
  import com.openai.client.OpenAIClient;
  import com.openai.client.okhttp.OpenAIOkHttpClient;
  import com.openai.models.files.*;

  import java.nio.file.Path;
  import java.nio.file.Paths;

  public class Main {
      public static void main(String[] args) {
          // 创建客户端，使用环境变量中的API密钥
          OpenAIClient client = OpenAIOkHttpClient.builder()
                  .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                  .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                  .build();
          // 设置文件路径,请根据实际需求修改路径与文件名
          Path filePath = Paths.get("src/main/java/org/example/示例产品手册A.docx");
          // 创建文件上传参数
          FileCreateParams fileParams = FileCreateParams.builder()
                  .file(filePath)
                  .purpose(FilePurpose.of("file-extract"))
                  .build();

          // 上传文件打印fileid
          FileObject fileObject = client.files().create(fileParams);
          // 打印file-id用于后续模型对话
          System.out.println(fileObject.id());
      }
  }
  ```

  ```bash curl
  curl --location --request POST 'https://dashscope.aliyuncs.com/compatible-mode/v1/files' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --form 'file=@"示例产品手册A.docx"' \
    --form 'purpose="file-extract"'
  ```
</CodeGroup>

运行以上代码，您可以得到本次上传文件对应的`file-id`。

### 通过文件ID传入信息并对话

将获取的 `file-id` 嵌入到System Message 中。第一条System Message用于设定角色向模型提问，后续的System Message用于传入 `file-id`，User Message包含针对文件的具体问题。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI, BadRequestError

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  try:
    completion = client.chat.completions.create(
      model="qwen-doc-turbo",
      messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        # 请将 '{FILE_ID}'替换为您实际对话场景所使用的 fileid
        {'role': 'system', 'content': 'fileid://{FILE_ID}'},
        {'role': 'user', 'content': '从这份产品手册中，提取所有产品信息，并整理成一个标准的JSON数组。每个对象需要包含：model(产品的型号)、name(产品的名称)、price(价格（去除货币符号和逗号）) '}
      ],
      # 本代码示例采用流式输出，以清晰和直观地展示模型输出过程
      stream=True,
      stream_options={"include_usage": True}
    )

    full_content = ""
    for chunk in completion:
      if chunk.choices and chunk.choices[0].delta.content:
        full_content += chunk.choices[0].delta.content
        print(chunk.model_dump())

    print(full_content)

  except BadRequestError as e:
    print(f"错误信息：{e}")
  ```

  ```java Java
  import com.openai.client.OpenAIClient;
  import com.openai.client.okhttp.OpenAIOkHttpClient;
  import com.openai.core.http.StreamResponse;
  import com.openai.models.chat.completions.*;

  public class Main {
      public static void main(String[] args) {
          // 创建客户端，使用环境变量中的API密钥
          OpenAIClient client = OpenAIOkHttpClient.builder()
                  // 若没有配置环境变量，请用千问AI平台API Key将下行替换为：.apiKey("sk-xxx");
                  .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                  .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                  .build();

          ChatCompletionCreateParams chatParams = ChatCompletionCreateParams.builder()
                  .addSystemMessage("You are a helpful assistant.")
                  // 请将 '{FILE_ID}'替换为您实际对话场景所使用的 fileid
                  .addSystemMessage("fileid://{FILE_ID}")
                  .addUserMessage("从这份产品手册中，提取所有产品信息，并整理成一个标准的JSON数组。每个对象需要包含：model(产品的型号)、name(产品的名称)、price(价格（去除货币符号和逗号）)")
                  .model("qwen-doc-turbo")
                  .build();

          try (StreamResponse<ChatCompletionChunk> streamResponse = client.chat().completions().createStreaming(chatParams)) {
              streamResponse.stream().forEach(chunk -> {
                  String content = chunk.choices().get(0).delta().content().orElse("");
                  if (!content.isEmpty()) {
                      System.out.print(content);
                  }
              });
          } catch (Exception e) {
              System.err.println("错误信息：" + e.getMessage());
          }
      }
  }
  ```

  ```bash curl
  curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
      "model": "qwen-doc-turbo",
      "messages": [
          {"role": "system","content": "You are a helpful assistant."},
          {"role": "system","content": "fileid://{FILE_ID}"},
          {"role": "user","content": "从这份产品手册中，提取所有产品信息，并整理成一个标准的JSON数组。每个对象需要包含：model(产品的型号)、name(产品的名称)、price(价格（去除货币符号和逗号）)"}
      ],
      "stream": true,
      "stream_options": {
          "include_usage": true
      }
  }'
  ```
</CodeGroup>

<Accordion title="完整示例：上传文件并调用模型">
  <CodeGroup>
    ```python Python
    import os
    import time
    from pathlib import Path
    from openai import OpenAI, BadRequestError

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    try:
      # 步骤1：上传文件
      file_object = client.files.create(file=Path("示例产品手册A.docx"), purpose="file-extract")
      file_id = file_object.id
      print(f"文件上传成功，file-id: {file_id}")

      # 步骤2：等待文件解析完成（可选，如果文件较大可能需要等待）
      # 如果文件仍在解析中，API会返回错误提示，此时需要重试
      max_retries = 10
      retry_count = 0

      while retry_count < max_retries:
        try:
          # 步骤3：使用file-id调用模型
          completion = client.chat.completions.create(
            model="qwen-doc-turbo",
            messages=[
              {'role': 'system', 'content': 'You are a helpful assistant.'},
              {'role': 'system', 'content': f'fileid://{file_id}'},
              {'role': 'user', 'content': '从这份产品手册中，提取所有产品信息，并整理成一个标准的JSON数组。每个对象需要包含：model(产品的型号)、name(产品的名称)、price(价格（去除货币符号和逗号）)'}
            ],
            stream=True,
            stream_options={"include_usage": True}
          )

          # 步骤4：处理模型输出
          full_content = ""
          for chunk in completion:
            if chunk.choices and chunk.choices[0].delta.content:
              full_content += chunk.choices[0].delta.content
              print(chunk.choices[0].delta.content, end='', flush=True)

          print(f"\n\n完整输出：\n{full_content}")
          break

        except BadRequestError as e:
          if "File parsing in progress" in str(e):
            retry_count += 1
            print(f"文件解析中，等待后重试 ({retry_count}/{max_retries})...")
            time.sleep(2)
          else:
            raise e

      if retry_count >= max_retries:
        print("文件解析超时，请稍后重试")

    except BadRequestError as e:
      print(f"错误信息：{e}")
    except Exception as e:
      print(f"发生错误：{e}")
    ```

    ```java Java
    import com.openai.client.OpenAIClient;
    import com.openai.client.okhttp.OpenAIOkHttpClient;
    import com.openai.core.http.StreamResponse;
    import com.openai.models.chat.completions.*;
    import com.openai.models.files.*;
    import java.nio.file.Path;
    import java.nio.file.Paths;
    import java.util.concurrent.TimeUnit;

    public class Main {
        public static void main(String[] args) {
            // 创建客户端
            OpenAIClient client = OpenAIOkHttpClient.builder()
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                    .build();

            try {
                // 步骤1：上传文件
                Path filePath = Paths.get("src/main/java/org/example/示例产品手册A.docx");
                FileCreateParams fileParams = FileCreateParams.builder()
                        .file(filePath)
                        .purpose(FilePurpose.of("file-extract"))
                        .build();

                FileObject fileObject = client.files().create(fileParams);
                String fileId = fileObject.id();
                System.out.println("文件上传成功，file-id: " + fileId);

                // 步骤2：等待文件解析并调用模型（最多重试10次）
                int maxRetries = 10;
                int retryCount = 0;
                boolean success = false;

                while (retryCount < maxRetries && !success) {
                    try {
                        // 步骤3：使用file-id调用模型
                        ChatCompletionCreateParams chatParams = ChatCompletionCreateParams.builder()
                                .addSystemMessage("You are a helpful assistant.")
                                .addSystemMessage("fileid://" + fileId)
                                .addUserMessage("从这份产品手册中，提取所有产品信息，并整理成一个标准的JSON数组。每个对象需要包含：model(产品的型号)、name(产品的名称)、price(价格（去除货币符号和逗号）)")
                                .model("qwen-doc-turbo")
                                .build();

                        // 步骤4：处理模型输出
                        try (StreamResponse<ChatCompletionChunk> streamResponse =
                                client.chat().completions().createStreaming(chatParams)) {
                            streamResponse.stream().forEach(chunk -> {
                                String content = chunk.choices().get(0).delta().content().orElse("");
                                if (!content.isEmpty()) {
                                    System.out.print(content);
                                }
                            });
                            System.out.println();
                            success = true;
                        }

                    } catch (Exception e) {
                        if (e.getMessage() != null && e.getMessage().contains("File parsing in progress")) {
                            retryCount++;
                            System.out.println("文件解析中，等待后重试 (" + retryCount + "/" + maxRetries + ")...");
                            TimeUnit.SECONDS.sleep(2);
                        } else {
                            throw e;
                        }
                    }
                }

                if (!success) {
                    System.out.println("文件解析超时，请稍后重试");
                }

            } catch (Exception e) {
                System.err.println("错误信息：" + e.getMessage());
                e.printStackTrace();
            }
        }
    }
    ```
  </CodeGroup>
</Accordion>

<Accordion title="响应示例">
  ```json
  [
    {
      "model": "pro-100",
      "name": "智能打印机",
      "price": "8999"
    },
    {
      "model": "pro-200",
      "name": "智能扫描仪",
      "price": "12999"
    },
    ...
    {
      "model": "sec-400",
      "name": "智能访客系统",
      "price": "9999"
    },
    {
      "model": "sec-500",
      "name": "智能停车管理",
      "price": "22999"
    }
  ]
  ```
</Accordion>

## 通过纯文本传入

除了通过 `file-id` 传入文件信息外，您还可以直接使用字符串传入文件内容。在此方法下，为避免模型混淆角色设定与文件内容，请确保在 `messages` 的第一条消息中添加用于角色设定的信息。

<Note>
  受限于API调用请求体大小，如果您的文本内容长度超过9,000 Token，请通过文件URL或文件ID传入信息对话。
</Note>

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI, BadRequestError

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  try:
    completion = client.chat.completions.create(
      model="qwen-doc-turbo",
      messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'system', 'content': '智能办公产品手册 版本：V2.0 发布日期：2024年1月 目录 1.1 产品概述...'},
        {'role': 'user', 'content': '从这份产品手册中，提取所有产品信息，并整理成一个标准的JSON数组。每个对象需要包含：model(产品的型号)、name(产品的名称)、price(价格（去除货币符号和逗号）)'}
      ],
      stream=True,
      stream_options={"include_usage": True}
    )

    full_content = ""
    for chunk in completion:
      if chunk.choices and chunk.choices[0].delta.content:
        full_content += chunk.choices[0].delta.content
        print(chunk.model_dump())

    print(full_content)

  except BadRequestError as e:
    print(f"错误信息：{e}")
  ```

  ```java Java
  import com.openai.client.OpenAIClient;
  import com.openai.client.okhttp.OpenAIOkHttpClient;
  import com.openai.core.http.StreamResponse;
  import com.openai.models.chat.completions.*;

  public class Main {
      public static void main(String[] args) {
          // 创建客户端，使用环境变量中的API密钥
          OpenAIClient client = OpenAIOkHttpClient.builder()
                  // 若没有配置环境变量，请用千问AI平台API Key将下行替换为：.apiKey("sk-xxx");
                  .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                  .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
                  .build();

          ChatCompletionCreateParams chatParams = ChatCompletionCreateParams.builder()
                  .addSystemMessage("You are a helpful assistant.")
                  .addSystemMessage("智能办公产品手册 版本：V2.0 发布日期：2024年1月 目录 1.1 产品概述...")
                  .addUserMessage("从这份产品手册中，提取所有产品信息，并整理成一个标准的JSON数组。每个对象需要包含：model(产品的型号)、name(产品的名称)、price(价格（去除货币符号和逗号）)")
                  .model("qwen-doc-turbo")
                  .build();

          try (StreamResponse<ChatCompletionChunk> streamResponse = client.chat().completions().createStreaming(chatParams)) {
              streamResponse.stream().forEach(chunk -> {
                  String content = chunk.choices().get(0).delta().content().orElse("");
                  if (!content.isEmpty()) {
                      System.out.print(content);
                  }
              });
          } catch (Exception e) {
              System.err.println("错误信息：" + e.getMessage());
          }
      }
  }
  ```

  ```bash curl
  curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
      "model": "qwen-doc-turbo",
      "messages": [
          {"role": "system","content": "You are a helpful assistant."},
          {"role": "system","content": "智能办公产品手册 版本：V2.0 发布日期：2024年1月 目录 1.1 产品概述..."},
          {"role": "user","content": "从这份产品手册中，提取所有产品信息，并整理成一个标准的JSON数组。每个对象需要包含：model(产品的型号)、name(产品的名称)、price(价格（去除货币符号和逗号）)"}
      ],
      "stream": true,
      "stream_options": {
          "include_usage": true
      }
  }'
  ```
</CodeGroup>

<Accordion title="响应示例">
  ```json
  [
    {
      "model": "pro-100",
      "name": "智能打印机",
      "price": "8999"
    },
    {
      "model": "pro-200",
      "name": "智能扫描仪",
      "price": "12999"
    },
    ...
    {
      "model": "sec-400",
      "name": "智能访客系统",
      "price": "9999"
    },
    {
      "model": "sec-500",
      "name": "智能停车管理",
      "price": "22999"
    }
  ]
  ```
</Accordion>

## 常见问题

<Accordion title="通过OpenAI文件兼容接口上传文件后，文件将被保存在何处？">
  所有通过OpenAI文件兼容接口上传的文件均将被保存在当前账号下的千问AI平台存储空间且不会产生任何费用，关于所上传文件的信息查询与管理请参考[OpenAI文件接口](/api-reference/platform-api/file)。
</Accordion>

<Accordion title="文件ID是否可以用于其他模型对话或功能调用？">
  文件ID目前仅能用于Qwen-Long、Qwen-Doc-Turbo模型对话以及[Batch接口批量调用](/developer-guides/text-generation/batch)。
</Accordion>

<Accordion title="通过文件URL方式上传时，文件解析策略（file_parsing_strategy）参数有什么不同？">
  当解析策略设置为 "auto" 时，系统会根据文件内容自动进行解析；当解析策略设置为 "text\_only" 时，系统将仅解析文字类内容；当解析策略设置为"text\_and\_images"时，系统将会解析所有图片与文本类内容，解析所需时间也会相应增加。
</Accordion>

<Accordion title="如何确定文件已经解析完成？">
  获取 file-id 后，您可以直接尝试使用该ID与模型进行对话。如果文件仍在解析中，API会返回相应的错误提示`File parsing in progress, please try again later.`，此时请稍后重试。如果模型调用成功并返回了回复，则表示文件已解析完成，可以正常使用。
</Accordion>

<Accordion title="文件上传后的解析过程是否会产生任何额外费用？">
  文档解析并不会产生任何额外费用。
</Accordion>

<Accordion title="解析模型返回的 JSON 时报错，如何处理？">
  模型返回的 `response.output.choices[0].message.content` 字段可能包含 Markdown 代码块标记（如 ` ```json ` 和 ` ``` ` 包裹）。在使用 `json.loads()` 解析前，需先去除 Markdown 标记，示例处理方式：

  ````python
  content = response.output.choices[0].message.content
  # 去除可能的 markdown 代码块标记
  if content.startswith("```"):
      lines = content.split("\n")
      content = "\n".join(lines[1:-1])  # 去掉首尾的 ``` 行
  data = json.loads(content)
  ````
</Accordion>

## API参考

关于Qwen-Doc-Turbo模型的输入与输出参数，请参考[DashScope chat](/api-reference/chat/dashscope)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](/api-reference/preparation/error-messages)进行解决。

## 限制

- **SDK 依赖**：
  - **文件URL (doc\_url)**: 文件URL方式当前仅支持DashScope协议，可以选择使用`DashScope Python SDK`或者HTTP方式调用（如curl）。
  - **上传文件 (file-id)**: 文件上传与管理操作**必须**使用 `OpenAI` 兼容 SDK。

- **文件上传与引用**：
  - **文件URL (`doc_url`)**: 单次请求最多支持 10 个文件URL，且传入的URL需确保公网可访问。
  - **上传文件 (`file-id`)**: 单个文件不超过 150MB。单个千问AI平台账号最多可上传 1 万个文件，总大小不超过 100GB，当前暂无有效期限制。单次请求最多引用 1 个文件。
    <Note>
      使用文件ID传入时，当文件数量或总大小达到任一上限时，新的文件上传请求将会失败。请参考[OpenAI兼容-File](/api-reference/platform-api/file)，及时删除不再需要的文件以释放配额，然后才能继续上传。
    </Note>
  - **支持格式**：TXT, DOC, DOCX, PDF, XLS, XLSX, MD, PPT, PPTX, JPG, JPEG, PNG, GIF, BMP。

- **API 输入**：
  - 通过`doc_url`或 `file-id` 引入信息时，上下文长度上限为 262,144 Token。
  - 直接在 `user` 或 `system` 消息中输入纯文本时，单条消息内容限制在 9,000 Token 以内。

- **API 输出**：
  - 最大输出长度为 32,768 Token。

- **文件共享**：
  - `file-id` 仅在生成它的千问AI平台账号内有效，不支持跨账号或通过 RAM 用户 API Key 调用。

- **限流**：关于模型的限流条件，请参见[限流](/developer-guides/administration/rate-limits)。
