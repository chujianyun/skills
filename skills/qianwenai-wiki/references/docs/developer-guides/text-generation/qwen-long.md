> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 长上下文（Qwen-Long）

> 1000万Token上下文窗口，通过文件上传和引用机制处理超长文档

处理超长文本文档时，标准大型语言模型会因上下文窗口限制而失败。Qwen-Long 模型提供 1000 万 Token 的上下文长度，通过文件上传和引用机制处理大规模数据。

## 使用方式

Qwen-Long 处理长文档分为以下两个步骤：文件上传与 API 调用。

1. **文件上传与解析**：
   - 通过 API 上传文件，文件格式与大小限制请参考[支持格式](#限制)。
   - 上传成功后，系统返回一个当前账号下的**唯一** `file-id`并开始解析。文件上传、存储以及解析本身不产生费用。

2. **API 调用与计费**：
   - 在调用模型时，通过在 `system` 消息中引用一个或多个 `file-id`。
   - 模型根据 `file-id` 关联的文本内容进行推理。
   - **每次** API 调用都会将所引用文件内容 Token 数计入该次请求的**输入Token**。

此机制避免了在每次请求中传输庞大的文件内容，但需留意其计费方式。

## 快速开始

### 前提条件

- 已[获取API Key](/api-reference/preparation/api-key)，并[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)。
- 如果通过SDK调用，还需要安装[OpenAI SDK](/api-reference/preparation/install-sdk#安装-openai-python-sdk)。

### 文档上传

以 `千问AI平台手机系列产品介绍.docx` 为例，通过OpenAI兼容接口上传到千问AI平台平台的安全存储空间，获取返回的`file-id`。有关文档上传接口的详细参数解释及调用方式，请参考[API文档](/api-reference/platform-api/file)页面进行了解。

<CodeGroup>
  ```python Python
  import os
  from pathlib import Path
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  file_object = client.files.create(file=Path("千问AI平台手机系列产品介绍.docx"), purpose="file-extract")
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
      OpenAIClient client = OpenAIOkHttpClient.builder()
          // 若没有配置环境变量，请用千问AI平台API Key将下行替换为：.apiKey("sk-xxx")
          .apiKey(System.getenv("DASHSCOPE_API_KEY"))
          .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
          .build();
      // 设置文件路径,请根据实际需求修改路径与文件名
      Path filePath = Paths.get("src/main/java/org/example/千问AI平台手机系列产品介绍.docx");
      // 创建文件上传参数
      FileCreateParams fileParams = FileCreateParams.builder()
          .file(filePath)
          .purpose(FilePurpose.of("file-extract"))
          .build();

      // 上传文件打印fileid
      FileObject fileObject = client.files().create(fileParams);
      System.out.println(fileObject.id());
    }
  }
  ```

  ```bash curl
  curl --location --request POST 'https://dashscope.aliyuncs.com/compatible-mode/v1/files' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --form 'file=@"千问AI平台手机系列产品介绍.docx"' \
    --form 'purpose="file-extract"'
  ```
</CodeGroup>

运行以上代码，您可以得到本次上传文件对应的`file-id`。

### 通过文件ID传入信息并对话

将获取的 `file-id` 嵌入到System Message 中。第一条System Message用于设定角色向模型提问，后续的System Message用于传入 `file-id`，User Message包含针对文档的具体问题。

<Note>
  较长的文档可能会需要相对更长的时间完成解析，请耐心等待解析完成后进行调用。
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
    # 请将 FILE_ID 替换为您实际对话场景所使用的 fileid
    FILE_ID = "file-fe-xxx"
    completion = client.chat.completions.create(
      model="qwen-long",
      messages=[
        # sys1: 角色定义
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        # sys2: 文档内容（纯文本或file-id）
        {'role': 'system', 'content': f'fileid://{FILE_ID}'},
        # 当请求中包含第 2 条system message时，user消息内容长度限制在 9,000 Token 以内
        {'role': 'user', 'content': '这篇文章讲了什么？'}
      ],
      stream=True,
      stream_options={"include_usage": True}
    )

    full_content = ""
    for chunk in completion:
      if chunk.choices and chunk.choices[0].delta.content:
        full_content += chunk.choices[0].delta.content
        print(chunk.model_dump())

      if chunk.usage:
        print(f"总计 tokens: {chunk.usage.total_tokens}")

    print(full_content)

  except BadRequestError as e:
    print(f"错误信息：{e}")
    print("请参考文档：/api-reference/preparation/error-messages")
  ```

  ```java Java
  import com.openai.client.OpenAIClient;
  import com.openai.client.okhttp.OpenAIOkHttpClient;
  import com.openai.core.http.StreamResponse;
  import com.openai.models.chat.completions.*;

  public class Main {
    public static void main(String[] args) {
      OpenAIClient client = OpenAIOkHttpClient.builder()
          // 若没有配置环境变量，请用千问AI平台API Key将下行替换为：.apiKey("sk-xxx")
          .apiKey(System.getenv("DASHSCOPE_API_KEY"))
          .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
          .build();

      ChatCompletionCreateParams chatParams = ChatCompletionCreateParams.builder()
          //sys1: 角色定义
          .addSystemMessage("You are a helpful assistant.")
          //sys2: 文档内容（纯文本或file-id）
          //请将 '{FILE_ID}'替换为您实际对话场景所使用的 fileid。
          .addSystemMessage("fileid://{FILE_ID}")
          //当请求中包含第 2 条system message时，user消息内容长度限制在 9,000 Token 以内
          .addUserMessage("这篇文章讲了什么？")
          .model("qwen-long")
          .build();

      StringBuilder fullResponse = new StringBuilder();

      try (StreamResponse<ChatCompletionChunk> streamResponse = client.chat().completions().createStreaming(chatParams)) {
        streamResponse.stream().forEach(chunk -> {
          System.out.println(chunk);
          String content = chunk.choices().get(0).delta().content().orElse("");
          if (!content.isEmpty()) {
            fullResponse.append(content);
          }
        });
        System.out.println(fullResponse);
      } catch (Exception e) {
        System.err.println("错误信息：" + e.getMessage());
        System.err.println("请参考文档：/api-reference/preparation/error-messages");
      }
    }
  }
  ```

  ```bash curl
  curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
      "model": "qwen-long",
      "messages": [
          {"role": "system","content": "You are a helpful assistant."},
          {"role": "system","content": "fileid://file-fe-xxx"},
          {"role": "user","content": "这篇文章讲了什么？"}
      ],
      "stream": true,
      "stream_options": {
          "include_usage": true
      }
  }'
  ```
</CodeGroup>

## 传入多个文档

您可以在一条System Message中传入多个`file-id`，以便在一次请求中处理多个文档；也可以在`messages`中添加新的System Message以补充新的文档信息。

### 传入多文档

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI, BadRequestError

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )
  try:
    # 请将 FILE_ID1 和 FILE_ID2 替换为您实际对话场景所使用的 fileid。
    FILE_ID1 = "file-fe-xxx1"
    FILE_ID2 = "file-fe-xxx2"
    completion = client.chat.completions.create(
      model="qwen-long",
      messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'system', 'content': f"fileid://{FILE_ID1},fileid://{FILE_ID2}"},
        {'role': 'user', 'content': '这几篇文章讲了什么？'}
      ],
      stream=True,
      stream_options={"include_usage": True}
    )

    full_content = ""
    for chunk in completion:
      if chunk.choices and chunk.choices[0].delta.content:
        full_content += chunk.choices[0].delta.content
        print(chunk.model_dump())

      if chunk.usage:
        print(f"总计 tokens: {chunk.usage.total_tokens}")

    print(full_content)

  except BadRequestError as e:
    print(f"错误信息：{e}")
    print("请参考文档：/api-reference/preparation/error-messages")
  ```

  ```java Java
  import com.openai.client.OpenAIClient;
  import com.openai.client.okhttp.OpenAIOkHttpClient;
  import com.openai.core.http.StreamResponse;
  import com.openai.models.chat.completions.*;

  public class Main {
    public static void main(String[] args) {
      OpenAIClient client = OpenAIOkHttpClient.builder()
          .apiKey(System.getenv("DASHSCOPE_API_KEY"))
          .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
          .build();

      ChatCompletionCreateParams chatParams = ChatCompletionCreateParams.builder()
          .addSystemMessage("You are a helpful assistant.")
          //请将 '{FILE_ID1}' 和 '{FILE_ID2}' 替换为您实际对话场景所使用的 fileid。
          .addSystemMessage("fileid://{FILE_ID1},fileid://{FILE_ID2}")
          .addUserMessage("这两篇文章讲了什么？")
          .model("qwen-long")
          .build();

      StringBuilder fullResponse = new StringBuilder();

      try (StreamResponse<ChatCompletionChunk> streamResponse = client.chat().completions().createStreaming(chatParams)) {
        streamResponse.stream().forEach(chunk -> {
          System.out.println(chunk);
          String content = chunk.choices().get(0).delta().content().orElse("");
          if (!content.isEmpty()) {
            fullResponse.append(content);
          }
        });
        System.out.println("\n完整回复内容：");
        System.out.println(fullResponse);
      } catch (Exception e) {
        System.err.println("错误信息：" + e.getMessage());
        System.err.println("请参考文档：/api-reference/preparation/error-messages");
      }
    }
  }
  ```

  ```bash curl
  curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
      "model": "qwen-long",
      "messages": [
          {"role": "system","content": "You are a helpful assistant."},
          {"role": "system","content": "fileid://file-fe-xxx1,fileid://file-fe-xxx2"},
          {"role": "user","content": "这两篇文章讲了什么？"}
      ],
      "stream": true,
      "stream_options": {
          "include_usage": true
      }
  }'
  ```
</CodeGroup>

### 追加文档

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI, BadRequestError

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )
  # 初始化messages列表
  # 请将 FILE_ID1 替换为您实际对话场景所使用的 fileid。
  FILE_ID1 = "file-fe-xxx1"
  messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'system', 'content': f'fileid://{FILE_ID1}'},
    {'role': 'user', 'content': '这篇文章讲了什么？'}
  ]

  try:
    # 第一轮响应
    completion_1 = client.chat.completions.create(
      model="qwen-long",
      messages=messages,
      stream=False
    )
    print(f"第一轮响应：{completion_1.choices[0].message.model_dump()}")
  except BadRequestError as e:
    print(f"错误信息：{e}")
    print("请参考文档：/api-reference/preparation/error-messages")

  # 构造assistant_message
  assistant_message = {
    "role": "assistant",
    "content": completion_1.choices[0].message.content}

  # 将assistant_message添加到messages中
  messages.append(assistant_message)

  # 将追加文档的fileid添加到messages中
  # 请将 FILE_ID2 替换为您实际对话场景所使用的 fileid。
  FILE_ID2 = "file-fe-xxx2"
  system_message = {'role': 'system', 'content': f'fileid://{FILE_ID2}'}
  messages.append(system_message)

  # 添加用户问题
  messages.append({'role': 'user', 'content': '这两篇文章讨论的方法有什么异同点？'})

  # 追加文档后的响应
  completion_2 = client.chat.completions.create(
    model="qwen-long",
    messages=messages,
    stream=True,
    stream_options={
      "include_usage": True
    }
  )

  print("追加文档后的响应：")
  for chunk in completion_2:
    print(chunk.model_dump())
  ```

  ```java Java
  import com.openai.client.OpenAIClient;
  import com.openai.client.okhttp.OpenAIOkHttpClient;
  import com.openai.models.chat.completions.*;
  import com.openai.core.http.StreamResponse;

  import java.util.ArrayList;
  import java.util.List;

  public class Main {
    public static void main(String[] args) {
      OpenAIClient client = OpenAIOkHttpClient.builder()
          .apiKey(System.getenv("DASHSCOPE_API_KEY"))
          .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
          .build();
      // 初始化messages列表
      List<ChatCompletionMessageParam> messages = new ArrayList<>();

      // 添加用于角色设定的信息
      ChatCompletionSystemMessageParam roleSet = ChatCompletionSystemMessageParam.builder()
          .content("You are a helpful assistant.")
          .build();
      messages.add(ChatCompletionMessageParam.ofSystem(roleSet));

      // 请将 '{FILE_ID1}' 替换为您实际对话场景所使用的 fileid。
      ChatCompletionSystemMessageParam systemMsg1 = ChatCompletionSystemMessageParam.builder()
          .content("fileid://{FILE_ID1}")
          .build();
      messages.add(ChatCompletionMessageParam.ofSystem(systemMsg1));

      // 用户提问消息（USER角色）
      ChatCompletionUserMessageParam userMsg1 = ChatCompletionUserMessageParam.builder()
          .content("请总结文章内容")
          .build();
      messages.add(ChatCompletionMessageParam.ofUser(userMsg1));

      // 构造第一轮请求并处理异常
      ChatCompletion completion1;
      try {
        completion1 = client.chat().completions().create(
            ChatCompletionCreateParams.builder()
                .model("qwen-long")
                .messages(messages)
                .build()
        );
      } catch (Exception e) {
        System.err.println("请求出错，请查看错误码对照网页：");
        System.err.println("/api-reference/preparation/error-messages");
        System.err.println("错误详情：" + e.getMessage());
        e.printStackTrace();
        return;
      }

      // 第一轮响应
      String firstResponse = completion1 != null ? completion1.choices().get(0).message().content().orElse("") : "";
      System.out.println("第一轮响应：" + firstResponse);

      // 构造AssistantMessage
      ChatCompletionAssistantMessageParam assistantMsg = ChatCompletionAssistantMessageParam.builder()
          .content(firstResponse)
          .build();
      messages.add(ChatCompletionMessageParam.ofAssistant(assistantMsg));

      // 请将 '{FILE_ID2}' 替换为您实际对话场景所使用的 fileid。
      ChatCompletionSystemMessageParam systemMsg2 = ChatCompletionSystemMessageParam.builder()
          .content("fileid://{FILE_ID2}")
          .build();
      messages.add(ChatCompletionMessageParam.ofSystem(systemMsg2));

      // 第二轮用户提问（USER角色）
      ChatCompletionUserMessageParam userMsg2 = ChatCompletionUserMessageParam.builder()
          .content("请对比两篇文章的结构差异")
          .build();
      messages.add(ChatCompletionMessageParam.ofUser(userMsg2));

      StringBuilder fullResponse = new StringBuilder();
      try (StreamResponse<ChatCompletionChunk> streamResponse = client.chat().completions().createStreaming(
          ChatCompletionCreateParams.builder()
              .model("qwen-long")
              .messages(messages)
              .build())) {

        streamResponse.stream().forEach(chunk -> {
          String content = chunk.choices().get(0).delta().content().orElse("");
          if (!content.isEmpty()) {
            fullResponse.append(content);
          }
        });
        System.out.println("\n最终响应：");
        System.out.println(fullResponse.toString().trim());
      } catch (Exception e) {
        System.err.println("错误信息：" + e.getMessage());
        System.err.println("请参考文档：/api-reference/preparation/error-messages");
      }
    }
  }
  ```

  ```bash curl
  curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
      "model": "qwen-long",
      "messages": [
          {"role": "system","content": "You are a helpful assistant."},
          {"role": "system","content": "fileid://file-fe-xxx1"},
          {"role": "user","content": "这篇文章讲了什么？"},
          {"role": "assistant","content": "这篇文章介绍了..."},
          {"role": "system","content": "fileid://file-fe-xxx2"},
          {"role": "user","content": "这两篇文章讨论的方法有什么异同点？"}
      ],
      "stream": true,
      "stream_options": {
          "include_usage": true
      }
  }'
  ```
</CodeGroup>

## 通过纯文本传入信息

除了通过 `file-id` 传入文档信息外，您还可以直接使用字符串传入文档内容。在此方法下，为避免模型混淆角色设定与文档内容，请确保在 `messages` 的第一条消息中添加用于角色设定的信息。

<Note>
  受限于API调用请求体大小，如果您的文本内容长度超过100万Token，请通过文件ID传入信息对话。
</Note>

### 简单示例

您可以直接将文档内容输入System Message中。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )
  completion = client.chat.completions.create(
    model="qwen-long",
    messages=[
      {'role': 'system', 'content': 'You are a helpful assistant.'},
      {'role': 'system', 'content': '千问AI平台手机产品介绍 千问AI平台X1 ——————畅享极致视界：搭载6.7英寸1440 x 3200像素超清屏幕...'},
      {'role': 'user', 'content': '文章讲了什么？'}
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
  ```

  ```java Java
  import com.openai.client.OpenAIClient;
  import com.openai.client.okhttp.OpenAIOkHttpClient;
  import com.openai.core.http.StreamResponse;
  import com.openai.models.chat.completions.*;

  public class Main {
    public static void main(String[] args) {
      OpenAIClient client = OpenAIOkHttpClient.builder()
          .apiKey(System.getenv("DASHSCOPE_API_KEY"))
          .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
          .build();

      ChatCompletionCreateParams chatParams = ChatCompletionCreateParams.builder()
          .addSystemMessage("You are a helpful assistant.")
          .addSystemMessage("千问AI平台手机产品介绍 千问AI平台X1 ——————畅享极致视界：搭载6.7英寸1440 x 3200像素超清屏幕...")
          .addUserMessage("这篇文章讲了什么？")
          .model("qwen-long")
          .build();

      StringBuilder fullResponse = new StringBuilder();

      try (StreamResponse<ChatCompletionChunk> streamResponse = client.chat().completions().createStreaming(chatParams)) {
        streamResponse.stream().forEach(chunk -> {
          System.out.println(chunk);
          String content = chunk.choices().get(0).delta().content().orElse("");
          if (!content.isEmpty()) {
            fullResponse.append(content);
          }
        });
        System.out.println(fullResponse);
      } catch (Exception e) {
        System.err.println("错误信息：" + e.getMessage());
        System.err.println("请参考文档：/api-reference/preparation/error-messages");
      }
    }
  }
  ```

  ```bash curl
  curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
      "model": "qwen-long",
      "messages": [
          {"role": "system","content": "You are a helpful assistant."},
          {"role": "system","content": "千问AI平台X1 —— 畅享极致视界：搭载6.7英寸1440 x 3200像素超清屏幕，搭配120Hz刷新率，..."},
          {"role": "user","content": "这篇文章讲了什么？"}
      ],
      "stream": true,
      "stream_options": {
          "include_usage": true
      }
  }'
  ```
</CodeGroup>

### 传入多文档

当您在本轮对话需要传入多个文档时，可以将文档内容放在不同的System Message中。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )
  completion = client.chat.completions.create(
    model="qwen-long",
    messages=[
      {'role': 'system', 'content': 'You are a helpful assistant.'},
      {'role': 'system', 'content': '千问AI平台X1————畅享极致视界：搭载6.7英寸1440 x 3200像素超清屏幕，搭配120Hz刷新率...'},
      {'role': 'system', 'content': '星尘S9 Pro —— 创新视觉盛宴：突破性6.9英寸1440 x 3088像素屏下摄像头设计...'},
      {'role': 'user', 'content': '这两篇文章讨论的产品有什么异同点？'}
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
  ```

  ```java Java
  import com.openai.client.OpenAIClient;
  import com.openai.client.okhttp.OpenAIOkHttpClient;
  import com.openai.core.http.StreamResponse;
  import com.openai.models.chat.completions.*;

  public class Main {
    public static void main(String[] args) {
      OpenAIClient client = OpenAIOkHttpClient.builder()
          .apiKey(System.getenv("DASHSCOPE_API_KEY"))
          .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
          .build();

      ChatCompletionCreateParams chatParams = ChatCompletionCreateParams.builder()
          .addSystemMessage("You are a helpful assistant.")
          .addSystemMessage("千问AI平台手机产品介绍 千问AI平台X1 ——————畅享极致视界：搭载6.7英寸1440 x 3200像素超清屏幕...")
          .addSystemMessage("星尘S9 Pro —— 创新视觉盛宴：突破性6.9英寸1440 x 3088像素屏下摄像头设计...")
          .addUserMessage("这两篇文章讨论的产品有什么异同点？")
          .model("qwen-long")
          .build();

      StringBuilder fullResponse = new StringBuilder();

      try (StreamResponse<ChatCompletionChunk> streamResponse = client.chat().completions().createStreaming(chatParams)) {
        streamResponse.stream().forEach(chunk -> {
          System.out.println(chunk);
          String content = chunk.choices().get(0).delta().content().orElse("");
          if (!content.isEmpty()) {
            fullResponse.append(content);
          }
        });
        System.out.println(fullResponse);
      } catch (Exception e) {
        System.err.println("错误信息：" + e.getMessage());
        System.err.println("请参考文档：/api-reference/preparation/error-messages");
      }
    }
  }
  ```

  ```bash curl
  curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
      "model": "qwen-long",
      "messages": [
          {"role": "system","content": "You are a helpful assistant."},
          {"role": "system","content": "千问AI平台X1 —— 畅享极致视界：搭载6.7英寸1440 x 3200像素超清屏幕，搭配120Hz刷新率..."},
          {"role": "system","content": "星尘S9 Pro —— 创新视觉盛宴：突破性6.9英寸1440 x 3088像素屏下摄像头设计..."},
          {"role": "user","content": "这两篇文章讨论的产品有什么异同点？"}
      ],
      "stream": true,
      "stream_options": {
          "include_usage": true
      }
  }'
  ```
</CodeGroup>

### 追加文档

在您与模型的交互过程中，可能需要补充新的文档信息。您可以在Messages 数组中添加新的文档内容到System Message中来实现这一效果。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI, BadRequestError

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )
  # 初始化messages列表
  messages = [
    {'role': 'system', 'content': 'You are a helpful assistant.'},
    {'role': 'system', 'content': '千问AI平台X1 —— 畅享极致视界：搭载6.7英寸1440 x 3200像素超清屏幕，搭配120Hz刷新率...'},
    {'role': 'user', 'content': '这篇文章讲了什么？'}
  ]

  try:
    # 第一轮响应
    completion_1 = client.chat.completions.create(
      model="qwen-long",
      messages=messages,
      stream=False
    )
    print(f"第一轮响应：{completion_1.choices[0].message.model_dump()}")
  except BadRequestError as e:
    print(f"错误信息：{e}")
    print("请参考文档：/api-reference/preparation/error-messages")

  # 构造assistant_message
  assistant_message = {
    "role": "assistant",
    "content": completion_1.choices[0].message.content}

  # 将assistant_message添加到messages中
  messages.append(assistant_message)
  # 将追加文档内容添加到messages中
  system_message = {
    'role': 'system',
    'content': '星尘S9 Pro —— 创新视觉盛宴：突破性6.9英寸1440 x 3088像素屏下摄像头设计，带来无界视觉享受...'
  }
  messages.append(system_message)

  # 添加用户问题
  messages.append({
    'role': 'user',
    'content': '这两篇文章讨论的产品有什么异同点？'
  })

  # 追加文档后的响应
  completion_2 = client.chat.completions.create(
    model="qwen-long",
    messages=messages,
    stream=True,
    stream_options={"include_usage": True}
  )

  print("追加文档后的响应：")
  for chunk in completion_2:
    print(chunk.model_dump())
  ```

  ```java Java
  import com.openai.client.OpenAIClient;
  import com.openai.client.okhttp.OpenAIOkHttpClient;
  import com.openai.models.chat.completions.*;
  import com.openai.core.http.StreamResponse;

  import java.util.ArrayList;
  import java.util.List;

  public class Main {
    public static void main(String[] args) {
      OpenAIClient client = OpenAIOkHttpClient.builder()
          .apiKey(System.getenv("DASHSCOPE_API_KEY"))
          .baseUrl("https://dashscope.aliyuncs.com/compatible-mode/v1")
          .build();
      // 初始化messages列表
      List<ChatCompletionMessageParam> messages = new ArrayList<>();

      // 添加用于角色设定的信息
      ChatCompletionSystemMessageParam roleSet = ChatCompletionSystemMessageParam.builder()
          .content("You are a helpful assistant.")
          .build();
      messages.add(ChatCompletionMessageParam.ofSystem(roleSet));

      // 第一轮传入内容
      ChatCompletionSystemMessageParam systemMsg1 = ChatCompletionSystemMessageParam.builder()
          .content("千问AI平台X1 —— 畅享极致视界：搭载6.7英寸1440 x 3200像素超清屏幕，搭配120Hz刷新率,256GB存储空间，12GB RAM,5000mAh长续航...")
          .build();
      messages.add(ChatCompletionMessageParam.ofSystem(systemMsg1));

      // 用户提问消息（USER角色）
      ChatCompletionUserMessageParam userMsg1 = ChatCompletionUserMessageParam.builder()
          .content("请总结文章内容")
          .build();
      messages.add(ChatCompletionMessageParam.ofUser(userMsg1));

      // 构造第一轮请求并处理异常
      ChatCompletion completion1;
      try {
        completion1 = client.chat().completions().create(
            ChatCompletionCreateParams.builder()
                .model("qwen-long")
                .messages(messages)
                .build()
        );
      } catch (Exception e) {
        System.err.println("错误信息：" + e.getMessage());
        System.err.println("请参考文档：/api-reference/preparation/error-messages");
        e.printStackTrace();
        return;
      }

      // 第一轮响应
      String firstResponse = completion1 != null ? completion1.choices().get(0).message().content().orElse("") : "";
      System.out.println("第一轮响应：" + firstResponse);

      // 构造AssistantMessage
      ChatCompletionAssistantMessageParam assistantMsg = ChatCompletionAssistantMessageParam.builder()
          .content(firstResponse)
          .build();
      messages.add(ChatCompletionMessageParam.ofAssistant(assistantMsg));

      // 第二轮传入内容
      ChatCompletionSystemMessageParam systemMsg2 = ChatCompletionSystemMessageParam.builder()
          .content("星尘S9 Pro —— 创新视觉盛宴：突破性6.9英寸1440 x 3088像素屏下摄像头设计，带来无界视觉享受...")
          .build();
      messages.add(ChatCompletionMessageParam.ofSystem(systemMsg2));

      // 第二轮用户提问（USER角色）
      ChatCompletionUserMessageParam userMsg2 = ChatCompletionUserMessageParam.builder()
          .content("请对比两篇描述的结构差异")
          .build();
      messages.add(ChatCompletionMessageParam.ofUser(userMsg2));

      StringBuilder fullResponse = new StringBuilder();
      try (StreamResponse<ChatCompletionChunk> streamResponse = client.chat().completions().createStreaming(
          ChatCompletionCreateParams.builder()
              .model("qwen-long")
              .messages(messages)
              .build())) {

        streamResponse.stream().forEach(chunk -> {
          String content = chunk.choices().get(0).delta().content().orElse("");
          if (!content.isEmpty()) {
            fullResponse.append(content);
          }
        });
        System.out.println("\n最终响应：");
        System.out.println(fullResponse.toString().trim());
      } catch (Exception e) {
        System.err.println("错误信息：" + e.getMessage());
        System.err.println("请参考文档：/api-reference/preparation/error-messages");
      }
    }
  }
  ```

  ```bash curl
  curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header "Content-Type: application/json" \
  --data '{
      "model": "qwen-long",
      "messages": [
          {"role": "system","content": "You are a helpful assistant."},
          {"role": "system","content": "千问AI平台X1 —— 畅享极致视界：搭载6.7英寸1440 x 3200像素超清屏幕，搭配120Hz刷新率..."},
          {"role": "user","content": "这篇文章讲了什么？"},
          {"role": "system","content": "星尘S9 Pro —— 创新视觉盛宴：突破性6.9英寸1440 x 3088像素屏下摄像头设计，带来无界视觉享受..."},
          {"role": "user","content": "这两篇文章讨论的产品有什么异同点"}
      ],
      "stream": true,
      "stream_options": {
          "include_usage": true
      }
  }'
  ```
</CodeGroup>

## 常见问题

1. **Qwen-Long模型是否支持批量提交任务？**

   是的，Qwen-Long兼容 [OpenAI Batch 接口](/developer-guides/text-generation/batch)并按照实时调用费用的 50% 来进行计费出账。该接口支持以文件方式批量提交任务，任务会以**异步**形式执行，并在完成或达到最长等待时间时返回结果。

2. **通过OpenAI文件兼容接口上传文件后，文件将被保存在何处？**

   所有通过OpenAI文件兼容接口上传的文件均将被保存在当前账号下的千问AI平台存储空间且不会产生任何费用，关于所上传文件的信息查询与管理请参考[OpenAI文件接口](/api-reference/platform-api/file#接口列表)。

3. **`qwen-long-2025-01-25` 是什么？**

   这是一个版本快照标识。它代表模型在某个时间点的功能和性能冻结版本，提供比 latest 版更高的稳定性。它不代表到期日。

4. **如何确定文件已经解析完成？**

   推荐通过**查询文件状态**来确认解析进度，无需反复试调用：调用查询文件信息（retrieve）接口获取文件对象，查看其 `status` 字段——`processing` 表示仍在解析中，`processed` 表示解析完成、可以引用调用，`error` 表示解析失败；当 `status` 为 `processed` 后即可正常调用。查询文件信息接口的详细说明请参考 [OpenAI 文件接口](/api-reference/platform-api/file)。此外，也可以直接尝试使用该 `file-id` 与模型进行对话：若文件尚未解析完成，系统将返回错误码 400，并提示 "`File parsing in progress, please try again later.`"；若模型调用成功并返回了回复内容，则表示文件已解析完成。

5. **如何确保模型输出标准格式的 JSON 字符串？**

   `qwen-long`及其所有快照版本均支持[结构化输出](/developer-guides/text-generation/structured-output)功能。可以通过指定一个JSON Schema，使模型按照定义的结构以合法的JSON格式返回。

## API参考

关于Qwen-Long模型的输入与输出参数，请参考[千问AI平台 Chat API 详情](/api-reference/chat/openai-chat)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](/api-reference/preparation/error-messages)进行解决。

## 限制

- **SDK 依赖**：
  - 文件上传、删除、查询等管理操作**必须**使用 OpenAI 兼容 SDK。
  - 模型调用可使用 OpenAI 兼容 SDK 或 Dashscope SDK。

- **文件上传**：
  - 支持格式：TXT, DOCX, PDF, XLSX, EPUB, MOBI, MD, CSV, JSON, BMP, PNG, JPG/JPEG, GIF。
  - 文件大小：图片格式文件上限 20MB，其他格式文件上限 150MB。
  - 账户配额：单个账户最多上传 1 万个文件，总大小不超过 100GB。当文件数量或总大小达到任一上限时，新的文件上传请求将会失败。请先参考[OpenAI兼容-File](/api-reference/platform-api/file#上线建议)，删除不再需要的文件以释放配额，然后才能继续上传。
  - 存储有效期：当前暂无有效期限制。

- **API 输入**：
  - 第 1 条 `system` 消息用于角色定义，第 2 条 `system` 消息用于传入文档内容或 `fileid://xxx`，`user` 消息用于用户提问。
  - 通过 `file-id` 引用时，单次请求最多引用 100 个文件。
  - 当请求中包含第 2 条`system` 消息（即存在两个 system 消息）时，`user`消息的内容长度不得超过 9,000 Token。仅当请求中不存在第 2 条 system 消息时，user 消息才不受此限制。
  - 总上下文长度上限为 1000 万 Token。

- **API 输出**：
  - 最大输出长度为 32,768 Token。

- **文件共享**：
  - `file-id` 仅在生成它的当前千问AI平台账号内有效，不支持跨账号或通过 RAM 用户 API Key 调用。

- **限流**：关于模型的限流条件，请参见[限流](/developer-guides/administration/rate-limits)。
