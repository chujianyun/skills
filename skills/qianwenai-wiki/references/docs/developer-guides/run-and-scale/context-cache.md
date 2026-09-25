> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 上下文缓存

> 通过前缀复用降低成本

上下文缓存（Context cache）将重叠请求的公共前缀进行缓存，避免重复计算，从而在不影响回答质量的前提下加快响应速度、降低使用成本。

上下文缓存提供三种模式，适用于不同场景。请根据对便捷性、确定性和成本的需求选择合适的模式：

- [显式缓存](#explicit-cache)：需**手动开启**的缓存模式。对指定内容创建缓存，可实现确定性命中。缓存有效期为 5 分钟。创建缓存所用的 token 按标准输入 token 价格的 125% 计费，后续命中按标准价格的 10% 计费。
- [隐式缓存](#implicit-cache)：无需额外配置、无法关闭的自动模式，适用于追求便捷性的通用场景。系统**自动识别**并缓存请求的**公共前缀**，但**不保证命中**。命中部分按标准输入 token 价格的 20% 计费。
- [会话缓存](#session-cache)：专为使用 Responses API 的多轮对话场景设计。只需在请求头中添加 `x-dashscope-session-cache: enable`，服务端即自动缓存对话上下文。计费规则与显式缓存一致：创建缓存按标准输入 token 价格的 125% 计费，命中按 10% 计费。

| **项目**        | **显式缓存**            | **隐式缓存**            | **会话缓存**            |
| ------------- | ------------------- | ------------------- | ------------------- |
| 是否影响回答质量      | 无影响                 | 无影响                 | 无影响                 |
| 缓存创建 token 计费 | 标准输入 token 价格的 125% | 标准输入 token 价格的 100% | 标准输入 token 价格的 125% |
| 缓存命中 token 计费 | 标准输入 token 价格的 10%  | 标准输入 token 价格的 20%  | 标准输入 token 价格的 10%  |
| 最少缓存 token 数  | 1024                | 256                 | 1024                |
| 缓存有效期         | 5 分钟（命中后重置）         | 不保证，系统会定期清理未使用的缓存数据 | 5 分钟（命中后重置）         |

<Note>
  - 使用 Chat Completions API 或 DashScope API 时，显式缓存与隐式缓存互斥，单次请求只能使用其中一种模式。
  - 使用 Responses API 时，如果未开启会话缓存，且模型支持隐式缓存，则自动使用隐式缓存。
</Note>

<a id="explicit-cache" />

## 显式缓存

相较于隐式缓存，显式缓存需要手动创建且有额外开销，但能提供更高的缓存命中率和更低的访问延迟。

### 支持的模型

| 类别       | 模型                                                                                                              |
| -------- | --------------------------------------------------------------------------------------------------------------- |
| 千问 Max   | `qwen3.8-max`、`qwen3.7-max`、`qwen3.7-max-2026-06-08`、`qwen3.7-max-2026-05-20`、`qwen3.6-max-preview`、`qwen3-max` |
| 千问开源     | `qwen3.8-2.4t-a95b`                                                                                             |
| 千问 Plus  | `qwen3.7-plus`、`qwen3.7-plus-2026-05-26`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen3.5-plus-2026-04-20`、`qwen-plus`    |
| 千问 Flash | `qwen3.7-flash`、`qwen3.7-flash-2026-07-15`、`qwen3.6-flash`、`qwen3.5-flash`、`qwen-flash`                         |
| 千问 Coder | `qwen3-coder-plus`、`qwen3-coder-flash`                                                                          |
| 千问 VL    | `qwen3-vl-plus`、`qwen3-vl-flash`                                                                                |
| DeepSeek | `deepseek-v3.2`                                                                                                 |
| Kimi     | `kimi-k2.6`、`kimi-k2.5`、`kimi-k2.7-code`                                                                        |
| GLM      | `glm-5.1`                                                                                                       |

### 使用方式

在 `messages` 数组中添加 `"cache_control": {"type": "ephemeral"}` 标记。系统会从每个 `cache_control` 标记的位置向前检索最多 20 个 `content` 块，并尝试与已有的缓存块进行匹配。

<Note>
  单次请求最多支持四个缓存标记。
</Note>

- **缓存未命中**

  系统会使用从 `messages` 数组开头到 `cache_control` 标记之间的内容创建新的缓存块。缓存块有效期为 5 分钟。

  <Note>
    - 缓存创建发生在模型响应之后。建议等待创建请求完成后再发送后续请求。
    - 缓存块至少需要包含 1024 个 token。
  </Note>

- **缓存命中**

  系统会选择最长匹配的前缀作为命中的缓存块，并将该缓存块的有效期重置为 5 分钟。

示例：

<Steps>
  <Step title="发送第一个请求">
    发送一条包含超过 1024 个 token 的文本 A 的 system 消息，并添加缓存标记。

    ```json
    [{"role": "system", "content": [{"type": "text", "text": "A", "cache_control": {"type": "ephemeral"}}]}]
    ```

    系统创建第一个缓存块，称为缓存块 A。
  </Step>

  <Step title="发送第二个请求">
    发送如下结构的请求：

    ```json
    [
      {"role": "system", "content": "A"},
      // <其他消息>
      {"role": "user","content": [{"type": "text", "text": "B", "cache_control": {"type": "ephemeral"}}]}
    ]
    ```

    - 如果"其他消息"不超过 20 条，缓存块 A 被命中，有效期重置为 5 分钟。同时系统基于 A、其他消息和 B 创建新的缓存块。
    - 如果"其他消息"超过 20 条，缓存块 A 不会被命中。系统基于完整上下文（A + 其他消息 + B）创建新的缓存块。
  </Step>
</Steps>

### 快速开始

以下示例展示了缓存块的创建和命中过程。

<CodeGroup>
  ```python OpenAI 兼容
  from openai import OpenAI
  import os

  client = OpenAI(
    # 若未配置环境变量，请用 api_key="sk-xxx" 替换下行
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  # 模拟代码仓库内容。最小可缓存的 prompt 长度为 1024 个 token。
  long_text_content = "<Your Code Here>" * 400

  # 发送请求的函数
  def get_completion(user_input):
    messages = [
      {
        "role": "system",
        "content": [
          {
            "type": "text",
            "text": long_text_content,
            # 在此处放置 cache_control 标记，缓存从 messages 数组开头到此 content 块的所有内容。
            "cache_control": {"type": "ephemeral"},
          }
        ],
      },
      # 每次请求的提问内容不同。
      {
        "role": "user",
        "content": user_input,
      },
    ]
    completion = client.chat.completions.create(
      # 选择支持显式缓存的模型。
      model="qwen3.7-max",
      messages=messages,
    )
    return completion

  # 第一次请求
  first_completion = get_completion("这段代码的内容是什么？")
  print(f"第一次请求缓存创建 token 数: {first_completion.usage.prompt_tokens_details.cache_creation_input_tokens}")
  print(f"第一次请求缓存命中 token 数: {first_completion.usage.prompt_tokens_details.cached_tokens}")
  print("=" * 20)
  # 第二次请求，代码内容相同，仅更换了问题。
  second_completion = get_completion("如何优化这段代码？")
  print(f"第二次请求缓存创建 token 数: {second_completion.usage.prompt_tokens_details.cache_creation_input_tokens}")
  print(f"第二次请求缓存命中 token 数: {second_completion.usage.prompt_tokens_details.cached_tokens}")
  ```

  ```python DashScope
  import os
  import dashscope
  from dashscope import Generation
  dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

  # 模拟代码仓库内容。最小可缓存的 prompt 长度为 1024 个 token。
  long_text_content = "<Your Code Here>" * 400

  # 发送请求的函数
  def get_completion(user_input):
    messages = [
      {
        "role": "system",
        "content": [
          {
            "type": "text",
            "text": long_text_content,
            # 在此处放置 cache_control 标记，缓存从 messages 数组开头到此 content 块的所有内容。
            "cache_control": {"type": "ephemeral"},
          }
        ],
      },
      # 每次请求的提问内容不同。
      {
        "role": "user",
        "content": user_input,
      },
    ]
    response = Generation.call(
      # 若未配置环境变量，请用 api_key="sk-xxx" 替换下行
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      model="qwen3.7-max",
      messages=messages,
      result_format="message"
    )
    return response

  # 第一次请求
  first_completion = get_completion("这段代码的内容是什么？")
  print(f"第一次请求缓存创建 token 数: {first_completion.usage.prompt_tokens_details['cache_creation_input_tokens']}")
  print(f"第一次请求缓存命中 token 数: {first_completion.usage.prompt_tokens_details['cached_tokens']}")
  print("=" * 20)
  # 第二次请求，代码内容相同，仅更换了问题。
  second_completion = get_completion("如何优化这段代码？")
  print(f"第二次请求缓存创建 token 数: {second_completion.usage.prompt_tokens_details['cache_creation_input_tokens']}")
  print(f"第二次请求缓存命中 token 数: {second_completion.usage.prompt_tokens_details['cached_tokens']}")
  ```

  ```java Java
  // Java SDK 最低版本要求为 2.21.6
  import com.alibaba.dashscope.aigc.generation.Generation;
  import com.alibaba.dashscope.aigc.generation.GenerationParam;
  import com.alibaba.dashscope.aigc.generation.GenerationResult;
  import com.alibaba.dashscope.common.Message;
  import com.alibaba.dashscope.common.MessageContentText;
  import com.alibaba.dashscope.common.Role;
  import com.alibaba.dashscope.exception.ApiException;
  import com.alibaba.dashscope.exception.InputRequiredException;
  import com.alibaba.dashscope.exception.NoApiKeyException;

  import java.util.Arrays;
  import java.util.Collections;

  public class Main {
    private static final String MODEL = "qwen3.7-max";
    // 模拟代码仓库内容（重复 400 次以确保超过 1024 个 token）
    private static final String LONG_TEXT_CONTENT = generateLongText(400);
    private static String generateLongText(int repeatCount) {
      StringBuilder sb = new StringBuilder();
      for (int i = 0; i < repeatCount; i++) {
        sb.append("<Your Code Here>");
      }
      return sb.toString();
    }
    private static GenerationResult getCompletion(String userQuestion)
        throws NoApiKeyException, ApiException, InputRequiredException {
      Generation gen = new Generation("http", "https://dashscope.aliyuncs.com/api/v1");

      // 构建带缓存控制的 system 消息
      MessageContentText systemContent = MessageContentText.builder()
          .type("text")
          .text(LONG_TEXT_CONTENT)
          .cacheControl(MessageContentText.CacheControl.builder()
              .type("ephemeral") // 设置缓存类型
              .build())
          .build();

      Message systemMsg = Message.builder()
          .role(Role.SYSTEM.getValue())
          .contents(Collections.singletonList(systemContent))
          .build();
      Message userMsg = Message.builder()
          .role(Role.USER.getValue())
          .content(userQuestion)
          .build();

      // 构建请求参数
      GenerationParam param = GenerationParam.builder()
          .model(MODEL)
          .messages(Arrays.asList(systemMsg, userMsg))
          .resultFormat(GenerationParam.ResultFormat.MESSAGE)
          .build();
      return gen.call(param);
    }

    private static void printCacheInfo(GenerationResult result, String requestLabel) {
      System.out.printf("%s 缓存创建 token 数: %d%n", requestLabel, result.getUsage().getPromptTokensDetails().getCacheCreationInputTokens());
      System.out.printf("%s 缓存命中 token 数: %d%n", requestLabel, result.getUsage().getPromptTokensDetails().getCachedTokens());
    }

    public static void main(String[] args) {
      try {
        // 第一次请求
        GenerationResult firstResult = getCompletion("这段代码的内容是什么？");
        printCacheInfo(firstResult, "第一次请求");
        System.out.println(new String(new char[20]).replace('\0', '='));            // 第二次请求
        GenerationResult secondResult = getCompletion("如何优化这段代码？");
        printCacheInfo(secondResult, "第二次请求");
      } catch (NoApiKeyException | ApiException | InputRequiredException e) {
        System.err.println("API 调用失败: " + e.getMessage());
        e.printStackTrace();
      }
    }
  }
  ```

  ```python Anthropic 兼容
  import anthropic
  import os

  api_key = os.getenv("DASHSCOPE_API_KEY")
  client = anthropic.Anthropic(
    # 若未配置环境变量，请用 api_key="sk-xxx" 替换下行
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/apps/anthropic",
    default_headers={"Authorization": f"Bearer {api_key}"},
  )

  # 模拟代码仓库内容。最小可缓存的 prompt 长度为 1024 个 token。
  long_text_content = "<Your Code Here>" * 400

  # 发送请求的函数
  def get_completion(user_input):
    response = client.messages.create(
      model="qwen3.7-max",
      max_tokens=1024,
      system=[{
        "type": "text",
        "text": long_text_content,
        "cache_control": {"type": "ephemeral"},
      }],
      messages=[{"role": "user", "content": user_input}],
    )
    return response

  # 第一次请求
  first_completion = get_completion("这段代码的内容是什么")
  print(f"第一次请求创建缓存 Token：{first_completion.usage.cache_creation_input_tokens}")
  print(f"第一次请求命中缓存 Token：{first_completion.usage.cache_read_input_tokens}")
  print("=" * 20)
  # 第二次请求，代码内容相同，仅更换了问题。
  second_completion = get_completion("这段代码可以怎么优化")
  print(f"第二次请求创建缓存 Token：{second_completion.usage.cache_creation_input_tokens}")
  print(f"第二次请求命中缓存 Token：{second_completion.usage.cache_read_input_tokens}")
  ```
</CodeGroup>

对同一代码仓库的后续请求会复用已有的缓存块，从而获得更快的响应速度和更低的成本。

```plaintext
第一次请求缓存创建 token 数: 1605
第一次请求缓存命中 token 数: 0
====================
第二次请求缓存创建 token 数: 0
第二次请求缓存命中 token 数: 1605
```

### 使用多个缓存标记实现精细化控制

在复杂场景中，prompt 通常由多个复用频率不同的部分组成。您可以使用多个缓存标记来实现精细化控制。

例如，智能客服的 prompt 通常包括：

- **系统设定**：非常稳定，几乎不会改变。
- **外部知识**：半稳定。从知识库检索或调用工具获取，在一段连续对话中可能保持不变。
- **对话历史**：动态增长。
- **当前问题**：每次都不同。

如果将整个 prompt 作为一个单元缓存，任何微小的变化（如外部知识更新）都会导致缓存失效。

您可以在一个请求中设置最多四个缓存标记，为 prompt 的不同部分分别创建缓存块。这样可以提高命中率，实现精细化控制。

### 计费

显式缓存仅影响输入 token 的计费，规则如下：

- **缓存创建**：新创建的缓存内容按标准输入价格的 125% 计费。如果新缓存内容包含已有缓存作为前缀，则仅对增量部分收取创建费用（新缓存 token 数减去已有缓存 token 数）。

  例如，假设已有缓存块 A 包含 1200 个 token，新请求需要缓存内容 AB，共 1500 个 token，则前 1200 个 token 按缓存命中计费（标准价格的 10%），新增的 300 个 token 按缓存创建计费（标准价格的 125%）。

  <Note>
    可通过 `cache_creation_input_tokens` 参数查看用于缓存创建的 token 数。
  </Note>

- **缓存命中**：按标准输入价格的 10% 计费。

  <Note>
    可通过 `cached_tokens` 参数查看命中缓存的 token 数。
  </Note>

- **其他 token**：未命中任何缓存且未用于创建缓存的 token 按标准价格计费。

- **例外**：qwen3.8-max 的显式缓存命中价格不是标准输入单价的 10%，具体价格请参见[模型市场](https://www.qianwenai.com/models)（缓存创建价格仍为标准单价的 125%）。

### 可缓存内容

仅 `messages` 数组中的以下消息类型支持添加缓存标记：

- System 消息
- User 消息
- Assistant 消息
- Tool 消息（工具执行后的结果）

  <Note>
    如果请求中包含 `tools` 参数，在 `messages` 中添加缓存标记也会同时缓存请求中定义的工具描述。
  </Note>

例如，对于 system 消息，将 `content` 字段改为数组格式并添加 `cache_control` 字段：

```json
{
  "role": "system",
  "content": [
    {
      "type": "text",
      "text": "<您指定的 prompt>",
      "cache_control": {
        "type": "ephemeral"
      }
    }
  ]
}
```

其他消息类型的结构同理。

### 缓存限制

- 最小可缓存的 prompt 长度为 **1024** 个 token。
- 缓存使用向前前缀匹配策略。系统自动检查最近的 20 个 content 块。如果待匹配的内容与包含 `cache_control` 标记的消息之间相隔超过 20 个 content 块，则不会命中缓存。
- `type` 仅支持设置为 `ephemeral`，即有效期为 5 分钟。
- 单次请求最多可包含 4 个缓存标记。

  <Note>
    如果缓存标记超过四个，仅最后四个生效。
  </Note>

### 并行工具调用场景下的消息结构优化

在并行工具调用场景下，模型会一次返回多个 `tool_calls`，需逐一执行这些工具并将结果回传。如果将每个工具结果作为独立的 `tool` 消息传入，多条连续同角色消息会在消息数组中各自占据一个 `content` 块位置。当待匹配内容（如系统消息上的缓存标记）与最后一条 `tool` 消息之间的 `content` 块数量超过 20，缓存将无法命中。

**优化方案**：在发送请求前，将连续同角色的 `tool` 消息预先合并为一条消息 + 多个 `content` 块，减少消息数组中的块层级，降低超出 20 块回溯窗口的风险。

**合并前（分开传，不推荐）**

每个工具结果单独一条 `tool` 消息，多条消息分别占据独立的 `content` 块位置：

```python
# 并行工具调用后，逐条回传结果（不推荐）
# 若工具数量较多，连续tool消息可能使缓存标记超出20块回溯范围
messages.extend([
  {
    "role": "tool",
    "tool_call_id": "call_abc123",
    "content": "北京当前气温：25°C，晴"
  },
  {
    "role": "tool",
    "tool_call_id": "call_def456",
    "content": "当前时间：2024-01-15 14:30:00"
  },
  {
    "role": "tool",
    "tool_call_id": "call_ghi789",
    "content": "1 USD = 7.24 CNY"
  }
])
```

**合并后（合并传，推荐）**

将所有工具结果合并为一条消息 + 多个 `content` 块，并在最后一个 `content` 块添加 `cache_control` 标记：

```python
# 并行工具调用后，合并回传结果（推荐）
# 将所有tool结果收集为单条消息的content块，减少消息总量
tool_results = []
for tool_call in response.choices[0].message.tool_calls:
  # 执行各工具，获取返回结果
  result = execute_tool(tool_call.function.name, tool_call.function.arguments)
  tool_results.append({
    "type": "text",
    "text": result,
    "tool_call_id": tool_call.id
  })
# 在最后一个content块添加cache_control标记（稳定位置）
if tool_results:
  tool_results[-1]["cache_control"] = {"type": "ephemeral"}
# 合并为单条消息追加到消息数组
messages.append({
  "role": "tool",
  "content": tool_results
})
```

在消息数组的其他稳定位置（如系统消息末尾）可设置额外的 `cache_control` 标记，单次请求最多支持 4 个标记，合理分布可进一步提升缓存命中率。

### 使用示例

<Accordion title="对长文本提出不同问题">
  ```python
  from openai import OpenAI
  import os

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  # 模拟代码仓库内容
  long_text_content = "<Your Code Here>" * 400

  # 发送请求的函数
  def get_completion(user_input):
    messages = [
      {
        "role": "system",
        "content": [
          {
            "type": "text",
            "text": long_text_content,
            # 在此处放置 cache_control 标记，缓存从 prompt 开头到此 content 块结尾（即模拟的代码仓库内容）。
            "cache_control": {"type": "ephemeral"},
          }
        ],
      },
      {
        "role": "user",
        "content": user_input,
      },
    ]
    completion = client.chat.completions.create(
      # 选择支持显式缓存的模型。
      model="qwen3.7-max",
      messages=messages,
    )
    return completion

  # 第一次请求
  first_completion = get_completion("这段代码的内容是什么？")
  created_cache_tokens = first_completion.usage.prompt_tokens_details.cache_creation_input_tokens
  print(f"第一次请求缓存创建 token 数: {created_cache_tokens}")
  hit_cached_tokens = first_completion.usage.prompt_tokens_details.cached_tokens
  print(f"第一次请求缓存命中 token 数: {hit_cached_tokens}")
  print(f"第一次请求未命中且未缓存的 token 数: {first_completion.usage.prompt_tokens-created_cache_tokens-hit_cached_tokens}")
  print("=" * 20)
  # 第二次请求，代码内容相同，仅更换了问题。
  second_completion = get_completion("这段代码有哪些可以优化的地方？")
  created_cache_tokens = second_completion.usage.prompt_tokens_details.cache_creation_input_tokens
  print(f"第二次请求缓存创建 token 数: {created_cache_tokens}")
  hit_cached_tokens = second_completion.usage.prompt_tokens_details.cached_tokens
  print(f"第二次请求缓存命中 token 数: {hit_cached_tokens}")
  print(f"第二次请求未命中且未缓存的 token 数: {second_completion.usage.prompt_tokens-created_cache_tokens-hit_cached_tokens}")
  ```

  此示例将代码仓库内容作为前缀缓存。后续请求对同一仓库提出不同问题。

  ```plaintext
  第一次请求缓存创建 token 数: 1605
  第一次请求缓存命中 token 数: 0
  第一次请求未命中且未缓存的 token 数: 13
  ====================
  第二次请求缓存创建 token 数: 0
  第二次请求缓存命中 token 数: 1605
  第二次请求未命中且未缓存的 token 数: 15
  ```

  <Note>
    为保证模型性能，系统会附加少量内部 token，这些 token 按标准输入价格计费。详情请参见 [FAQ](#faq)。
  </Note>
</Accordion>

<Accordion title="连续多轮对话">
  在日常多轮对话场景中，您可以在每次请求的 messages 数组末尾的最后一条内容上添加缓存标记。从第二轮对话开始，每次请求都会命中并刷新上一轮创建的缓存块，同时创建新的缓存块。

  ```python
  from openai import OpenAI
  import os

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  system_prompt = "你是一个风趣的人。" * 400
  messages = [{"role": "system", "content": system_prompt}]

  def get_completion(messages):
    completion = client.chat.completions.create(
      model="qwen3.7-max",
      messages=messages,
    )
    return completion

  while True:
    user_input = input("请输入: ")
    messages.append({"role": "user", "content": [{"type": "text", "text": user_input, "cache_control": {"type": "ephemeral"}}]})
    completion = get_completion(messages)
    print(f"[AI 回复] {completion.choices[0].message.content}")
    messages.append(completion.choices[0].message)
    created_cache_tokens = completion.usage.prompt_tokens_details.cache_creation_input_tokens
    hit_cached_tokens = completion.usage.prompt_tokens_details.cached_tokens
    uncached_tokens = completion.usage.prompt_tokens - created_cache_tokens - hit_cached_tokens
    print(f"[缓存信息] 缓存创建 token 数: {created_cache_tokens}")
    print(f"[缓存信息] 缓存命中 token 数: {hit_cached_tokens}")
    print(f"[缓存信息] 未命中且未缓存的 token 数: {uncached_tokens}")
  ```

  运行上述代码并输入问题与模型交流。每个问题都会命中上一轮创建的缓存块。
</Accordion>

<a id="implicit-cache" />

## 隐式缓存

### 支持的模型

**文本生成模型**

| 类别                 | 模型                                                                                                                                                |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 千问 Max             | `qwen3.8-max`、`qwen3.7-max`、`qwen3.7-max-2026-06-08`、`qwen3.7-max-2026-05-20`、`qwen3-max`、`qwen3-max-preview`、`qwen-max`                          |
| 千问开源               | `qwen3.8-2.4t-a95b`                                                                                                                               |
| 千问 Plus            | `qwen3.7-plus`、`qwen3.7-plus-2026-05-26`、`qwen-plus`                                                                                              |
| 千问 Flash           | `qwen3.7-flash`、`qwen3.7-flash-2026-07-15`、`qwen-flash`                                                                                           |
| 千问 Turbo           | `qwen-turbo`                                                                                                                                      |
| 千问 Coder           | `qwen3-coder-plus`、`qwen3-coder-flash`                                                                                                            |
| DeepSeek（千问AI平台部署） | `deepseek-v4-pro-0813`、`deepseek-v4-pro`、`deepseek-v4-flash`、`deepseek-v4-flash-0731`、`deepseek-v3.2`、`deepseek-v3.1`、`deepseek-v3`、`deepseek-r1` |
| DeepSeek（快手万擎部署）   | `vanchin/deepseek-v4-pro`、`vanchin/deepseek-v3.2-think`、`vanchin/deepseek-v3.1-terminus`、`vanchin/deepseek-r1`、`vanchin/deepseek-v3`              |
| Kimi（千问AI平台部署）     | `kimi-k2.7-code`、`kimi-k2.6`、`kimi-k2.5`、`kimi-k2-thinking`、`Moonshot-Kimi-K2-Instruct`                                                           |
| Kimi（月之暗面部署）       | `kimi/kimi-k3`、`kimi/kimi-k2.7-code-highspeed`、`kimi/kimi-k2.7-code`、`kimi/kimi-k2.6`、`kimi/kimi-k2.5`                                            |
| GLM（千问AI平台部署）      | `glm-5.2`、`glm-5.1`、`glm-5`、`glm-4.7`、`glm-4.6`                                                                                                   |
| GLM（智谱部署）          | `ZHIPU/GLM-5.2`、`ZHIPU/GLM-5.1`、`ZHIPU/GLM-5`                                                                                                     |
| MiniMax（千问AI平台部署）  | `MiniMax-M2.5`、`MiniMax-M2.1`                                                                                                                     |
| MiniMax（稀宇科技部署）    | `MiniMax/MiniMax-M3`、`MiniMax/MiniMax-M2.7`、`MiniMax/MiniMax-M2.5`、`MiniMax/MiniMax-M2.1`                                                         |
| MiMo（小米部署）         | `xiaomi/mimo-v2.5-pro`                                                                                                                            |
| Stepfun（阶跃星辰部署）    | `stepfun/step-3.7-flash`                                                                                                                          |

<Note>
  智谱部署的 GLM、稀宇科技部署的 MiniMax 模型触发隐式缓存的最少 Token 数为 512，千问AI平台部署的模型为 256（Qwen3.7 系列模型约为 2000）。
</Note>

**视觉理解模型**：`qwen3-vl-plus`、`qwen3-vl-flash`、`qwen-vl-max`、`qwen-vl-plus`

**文档理解模型**：`qwen-doc-turbo`

### 工作原理

当您向支持隐式缓存的模型发送请求时，该功能自动开启。系统的工作流程如下：

1. **查找**：收到请求后，系统基于**前缀匹配**原则，在缓存中查找与请求 `messages` 数组内容的公共前缀。
2. **判定**：
   - 如果缓存命中，系统直接使用缓存结果进行后续推理。
   - 如果缓存未命中，系统正常处理请求，并将当前 prompt 的前缀存入缓存供后续请求使用。

<Note>
  系统会定期清理未使用的缓存数据，少于 256 个 token 的内容不会被缓存。命中率不保证为 100%——即使请求上下文完全相同，也可能发生缓存未命中的情况。
</Note>

### 提高命中率

隐式缓存通过识别不同请求之间重复的**前缀**内容来工作。要提高命中率，应**将静态内容放在 prompt 开头，将可变内容放在末尾**。

- **纯文本场景**：如果系统已缓存"ABCD"，请求"ABE"可以匹配"AB"前缀，而请求"BCD"则无法匹配任何缓存。
- **视觉理解场景**：
  - 对**同一张图片或视频**提出多个问题时：将图片或视频放在文本之前，有助于提高命中率。
  - 对**不同图片或视频**提出相同问题时：将文本放在图片或视频之前，有助于提高命中率。

### 计费

隐式缓存无额外费用。

当请求命中缓存时，命中的输入 token 按 `cached_token` 计费，折扣比例因模型来源不同而有差异；未命中缓存的输入 token 按标准 `input_token` 价格计费。输出 token 按标准价格计费。

- 千问AI平台部署的模型（deepseek-v4-pro-0813、deepseek-v4-pro、qwen3.8-max 除外）：`cached_token` 单价为 `input_token` 单价的 **20%**
- deepseek-v4-pro-0813、deepseek-v4-pro：`cached_token` 单价不是 `input_token` 单价的 20%，具体价格请参见[模型市场](https://www.qianwenai.com/models)
- qwen3.8-max：`cached_token` 单价不是 `input_token` 单价的 20%，具体价格请参见[模型市场](https://www.qianwenai.com/models)
- DeepSeek（快手万擎部署）：vanchin/deepseek-v4-pro 为 **8.33%**；vanchin/deepseek-v3.2-think 为 **10%**；vanchin/deepseek-v3.1-terminus、vanchin/deepseek-r1、vanchin/deepseek-v3 为 **40%**
- Kimi（月之暗面部署）：kimi/kimi-k3 为 **10%**；kimi/kimi-k2.6 为 **16.9%**；kimi/kimi-k2.5 为 **17.5%**
- GLM（智谱部署）：ZHIPU/GLM-5.1、ZHIPU/GLM-5 均为 **25%**
- MiniMax（稀宇科技部署）：MiniMax/MiniMax-M3、MiniMax/MiniMax-M2.7 为 **20%**，MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1 为 **10%**

示例：某请求包含 10,000 个输入 token，其中 5,000 个命中缓存：

- 未命中 token（5,000）：按单价的 100% 计费
- 命中 token（5,000）：按单价的 20% 计费

总输入成本相当于无缓存时的 60%：(50% x 100%) + (50% x 20%) = 60%。

![image.png](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4439916571/p893561.png)

您可以从[返回结果](#cache-hit-examples)的 `cached_tokens` 字段获取命中缓存的 token 数。

<Note>
  [OpenAI 兼容-Batch（文件输入）](/developer-guides/text-generation/batch)方式不享受缓存折扣。
</Note>

<a id="cache-hit-examples" />

### 缓存命中示例

#### 文本生成

在 `usage.prompt_tokens_details.cached_tokens` 中查看命中缓存的 token 数（属于 OpenAI 兼容的 `usage.prompt_tokens` 或 DashScope 的 `usage.input_tokens` 的一部分）。

<CodeGroup>
  ```json OpenAI 兼容
  {
    "choices": [
      {
        "message": {
          "role": "assistant",
          "content": "I am a super-large language model developed by Alibaba Cloud. My name is Qwen."
        },
        "finish_reason": "stop",
        "index": 0,
        "logprobs": null
      }
    ],
    "object": "chat.completion",
    "usage": {
      "prompt_tokens": 3019,
      "completion_tokens": 104,
      "total_tokens": 3123,
      "prompt_tokens_details": {
        "cached_tokens": 2048
      }
    },
    "created": 1735120033,
    "system_fingerprint": null,
    "model": "qwen-plus",
    "id": "chatcmpl-6ada9ed2-7f33-9de2-8bb0-78bd4035025a"
  }
  ```

  ```json DashScope
  {
    "status_code": 200,
    "request_id": "f3acaa33-e248-97bb-96d5-cbeed34699e1",
    "code": "",
    "message": "",
    "output": {
      "text": null,
      "finish_reason": null,
      "choices": [
        {
          "finish_reason": "stop",
          "message": {
            "role": "assistant",
            "content": "I am a large-scale language model from Alibaba Cloud. My name is Qwen. I can generate various types of text, such as articles, stories, poems, and stories, and can transform and expand them according to different scenarios and needs. In addition, I can answer various questions, provide help and solutions. If you have any questions or need help, please feel free to let me know, and I will do my best to provide support. Please note that continuously repeating the same content may not yield more detailed answers. We recommend that you provide more specific information or vary your questions so that I can better understand your needs."
          }
        }
      ]
    },
    "usage": {
      "input_tokens": 3019,
      "output_tokens": 101,
      "prompt_tokens_details": {
        "cached_tokens": 2048
      },
      "total_tokens": 3120
    }
  }
  ```

  ```json Anthropic 兼容
  {
    "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
    "type": "message",
    "role": "assistant",
    "content": [{"type": "text", "text": "这段内容是重复的占位文本"}],
    "model": "qwen3.7-max",
    "stop_reason": "end_turn",
    "usage": {
      "input_tokens": 82,
      "cache_creation_input_tokens": 0,
      "cache_read_input_tokens": 1536,
      "output_tokens": 14
    }
  }
  ```
</CodeGroup>

#### 视觉理解

在 `usage.prompt_tokens_details.cached_tokens`（属于 OpenAI 兼容的 `usage.prompt_tokens` 的一部分）或 `usage.cached_tokens`（属于 DashScope 的 `usage.input_tokens` 的一部分）中查看命中缓存的 token 数。

<Note>
  当前使用 `usage.cached_tokens` 的模型将来会升级为使用 `usage.prompt_tokens_details.cached_tokens`。
</Note>

<CodeGroup>
  ```json OpenAI 兼容
  {
    "id": "chatcmpl-3f3bf7d0-b168-9637-a245-dd0f946c700f",
    "choices": [
      {
        "finish_reason": "stop",
        "index": 0,
        "logprobs": null,
        "message": {
          "content": "This image shows a heartwarming scene of a woman and a dog interacting on a beach. The woman is wearing a plaid shirt and sitting on the sand, smiling as she interacts with the dog. The dog is a large, light-colored breed with a colorful collar, and its front paw is raised as if to shake hands or give a high-five to the woman. The background is a vast ocean and sky, with sunlight shining from the right side of the frame, adding a warm and peaceful atmosphere to the whole scene.",
          "refusal": null,
          "role": "assistant",
          "audio": null,
          "function_call": null,
          "tool_calls": null
        }
      }
    ],
    "created": 1744956927,
    "model": "qwen3-vl-plus",
    "object": "chat.completion",
    "service_tier": null,
    "system_fingerprint": null,
    "usage": {
      "completion_tokens": 93,
      "prompt_tokens": 1316,
      "total_tokens": 1409,
      "completion_tokens_details": null,
      "prompt_tokens_details": {
        "audio_tokens": null,
        "cached_tokens": 1152
      }
    }
  }
  ```

  ```json DashScope
  {
    "status_code": 200,
    "request_id": "06a8f3bb-d871-9db4-857d-2c6eeac819bc",
    "code": "",
    "message": "",
    "output": {
      "text": null,
      "finish_reason": null,
      "choices": [
        {
          "finish_reason": "stop",
          "message": {
            "role": "assistant",
            "content": [
              {
                "text": "This image shows a heartwarming scene of a woman and a dog interacting on a beach. The woman is wearing a plaid shirt and sitting on the sand, smiling as she interacts with the dog. The dog is a large breed with a colorful collar, and its front paw is raised as if to shake hands or give a high-five to the woman. The background is a vast ocean and sky, with sunlight shining from the right side of the frame, adding a warm and peaceful atmosphere to the whole scene."
              }
            ]
          }
        }
      ]
    },
    "usage": {
      "input_tokens": 1292,
      "output_tokens": 87,
      "input_tokens_details": {
        "text_tokens": 43,
        "image_tokens": 1249
      },
      "total_tokens": 1379,
      "output_tokens_details": {
        "text_tokens": 87
      },
      "image_tokens": 1249,
      "cached_tokens": 1152
    }
  }
  ```

  ```json Anthropic 兼容
  {
    "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
    "type": "message",
    "role": "assistant",
    "content": [{"type": "text", "text": "这张图片展示了一位女性和一只狗在海滩上互动的温馨场景。"}],
    "model": "qwen-vl-max",
    "stop_reason": "end_turn",
    "usage": {
      "input_tokens": 369,
      "cache_creation_input_tokens": 0,
      "cache_read_input_tokens": 896,
      "output_tokens": 28
    }
  }
  ```
</CodeGroup>

### 典型场景

1. **基于长文本的问答**

   适用于需要对同一长文本（如小说、教材或法律文件）进行多次请求的场景。

   **第一次请求的 message 数组**

```python
messages = [{"role": "system","content": "你是一位语文老师，可以帮助学生理解阅读材料。"},
  {"role": "user","content": "<文章内容> 这篇文章的主旨是什么？"}]
```

**后续请求的 message 数组**

```python
messages = [{"role": "system","content": "你是一位语文老师，可以帮助学生理解阅读材料。"},
  {"role": "user","content": "<文章内容> 请分析这篇文章的第三段。"}]
```

尽管问题不同，但引用的是同一篇文章。由于 system prompt 和文章内容保持不变，每次请求共享大量重叠前缀，因此缓存命中的可能性很高。

2. **代码自动补全**

   在代码自动补全场景中，模型基于已有的上下文自动补全代码。随着用户持续编码，代码的前缀部分保持不变。上下文缓存可以缓存前面的代码，从而提高补全速度。

3. **多轮对话**

   在多轮对话中，前几轮的对话历史都包含在 messages 数组中。因此每一轮请求都与上一轮共享相同的前缀，缓存命中的概率很高。

   **第一轮对话的 message 数组**

```python
messages=[{"role": "system","content": "You are a helpful assistant."},
  {"role": "user","content": "你是谁？"}]
```

**第二轮对话的 message 数组**

```python
messages=[{"role": "system","content": "You are a helpful assistant."},
  {"role": "user","content": "你是谁？"},
  {"role": "assistant","content": "我是通义千问，由阿里云开发。"},
  {"role": "user","content": "你能做什么？"}]
```

随着对话轮数增加，缓存带来的推理加速和成本降低效果越发显著。

4. **角色扮演或 few-shot 学习**

   在角色扮演或 few-shot 学习场景中，通常需要在 prompt 中包含大量信息来引导模型的输出格式。这会在不同请求间产生大量共享前缀。

   例如，如果您希望模型扮演一位营销专家，system prompt 中会包含大量文本信息。以下是两次请求的消息示例：

```python
system_prompt = """你是一位经验丰富的营销专家。请按以下格式为不同产品提供详细的营销建议：

1. 目标受众: xxx

2. 主要卖点: xxx

3. 营销渠道: xxx
...
12. 长期发展策略: xxx

请确保建议具体、可操作，且与产品特性高度相关。"""

# 第一次请求的用户消息，询问关于智能手表的营销建议
messages_1=[
  {"role": "system", "content": system_prompt},
  {"role": "user", "content": "请为一款新上市的智能手表提供营销建议。"}
]

# 第二次请求的用户消息，询问关于笔记本电脑的营销建议。由于 system_prompt 相同，缓存命中的概率很高。
messages_2=[
  {"role": "system", "content": system_prompt},
  {"role": "user", "content": "请为一款新上市的笔记本电脑提供营销建议。"}
]
```

借助上下文缓存，即使用户频繁更换询问的产品类型（如从智能手表切换到笔记本电脑），一旦命中缓存，系统就能快速响应。

5. **视频理解**

   在视频理解场景中，如果对同一视频提出多个问题，将 `video` 放在 `text` 之前可以提高缓存命中率。如果对不同视频提出相同问题，将 `text` 放在 `video` 之前可以提高缓存命中率。以下是对同一视频发出两次请求的消息示例：

````python
# 第一次请求的用户消息，询问视频内容
messages1 = [
  {"role":"system","content":[{"text": "You are a helpful assistant."}]},
  {"role": "user",
    "content": [
      {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250328/eepdcq/phase_change_480p.mov"},
      {"text": "这个视频的内容是什么？"}
    ]
  }
]

# 第二次请求的用户消息，询问视频时间戳。由于基于同一视频提问，将 video 放在 text 之前，缓存命中的概率很高。
messages2 = [
  {"role":"system","content":[{"text": "You are a helpful assistant."}]},
  {"role": "user",
    "content": [
      {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250328/eepdcq/phase_change_480p.mov"},
      {"text": "请描述视频中的一系列事件，并以 JSON 格式输出开始时间（start_time）、结束时间（end_time）和事件（event）。不要输出 ```json``` 代码段。"}
    ]
  }
]
````

<a id="session-cache" />

## 会话缓存

### 支持的模型

`qwen3.8-max`、`qwen3.7-max`、`qwen3.7-max-2026-06-08`、`qwen3.7-max-2026-05-20`、`qwen3-max`、`qwen3.7-plus`、`qwen3.7-plus-2026-05-26`、`qwen3.7-flash`、`qwen3.7-flash-2026-07-15`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen3.6-flash`、`qwen3.5-flash`、`qwen-plus`、`qwen-flash`、`qwen3-coder-plus`、`qwen3-coder-flash`

### 概述

会话缓存是一种面向使用 Responses API 进行多轮对话的缓存模式。与需要手动添加 `cache_control` 标记的显式缓存不同，会话缓存由服务端自动处理缓存逻辑。您只需通过 HTTP 请求头开启或关闭，然后像普通多轮对话一样进行调用即可。

<Note>
  当您使用 `previous_response_id` 进行多轮对话时，开启会话缓存可让服务端自动缓存对话上下文，从而降低推理延迟和使用成本。
</Note>

### 使用方式

在请求头中添加以下字段来控制会话缓存：

- `x-dashscope-session-cache: enable`：开启会话缓存。
- `x-dashscope-session-cache: disable`：关闭会话缓存。如果模型支持隐式缓存，则使用隐式缓存。

使用 SDK 时，可通过 `default_headers`（Python）或 `defaultHeaders`（Node.js）参数传递此请求头。使用 curl 时，通过 `-H` 参数传递。

### 代码示例

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    # 通过 default_headers 开启会话缓存
    default_headers={"x-dashscope-session-cache": "enable"}
  )

  # 构造超过 1024 个 token 的长文本，以确保触发缓存创建。
  # （如果不足 1024 个 token，则在累积的对话上下文超过 1024 个 token 时触发缓存创建。）
  long_context = "人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。" * 50

  # 第一轮对话
  response1 = client.responses.create(
    model="qwen3.7-plus",
    input=long_context + "\n\n基于以上背景知识，请简要介绍机器学习中的随机森林算法。",
  )
  print(f"第一轮回复: {response1.output_text}")

  # 第二轮对话：通过 previous_response_id 关联上下文。缓存由服务端自动处理。
  response2 = client.responses.create(
    model="qwen3.7-plus",
    input="它和 GBDT 的主要区别是什么？",
    extra_body={"previous_response_id": response1.id},
  )
  print(f"第二轮回复: {response2.output_text}")

  # 查看缓存命中状态
  usage = response2.usage
  print(f"输入 token 数: {usage.input_tokens}")
  print(f"缓存命中 token 数: {usage.prompt_tokens_details.cached_tokens}")
  ```

  ```javascript Node.js
  import OpenAI from "openai";

  const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    // 通过 defaultHeaders 开启会话缓存
    defaultHeaders: {"x-dashscope-session-cache": "enable"}
  });

  // 构造超过 1024 个 token 的长文本，以确保触发缓存创建。
  // （如果不足 1024 个 token，则在累积的对话上下文超过 1024 个 token 时触发缓存创建。）
  const longContext = "人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。".repeat(50);

  async function main() {
    // 第一轮对话
    const response1 = await openai.responses.create({
      model: "qwen3.7-plus",
      input: longContext + "\n\n基于以上背景知识，请简要介绍机器学习中的随机森林算法，包括基本原理和应用场景。"
    });
    console.log(`第一轮回复: ${response1.output_text}`);

    // 第二轮对话：通过 previous_response_id 关联上下文。缓存由服务端自动处理。
    const response2 = await openai.responses.create(
      {
        model: "qwen3.7-plus",
        input: "它和 GBDT 的主要区别是什么？",
      },
      {
        body: { previous_response_id: response1.id }
      }
    );
    console.log(`第二轮回复: ${response2.output_text}`);

    // 查看缓存命中状态
    console.log(`输入 token 数: ${response2.usage.input_tokens}`);
    console.log(`缓存命中 token 数: ${response2.usage.prompt_tokens_details.cached_tokens}`);
  }

  main();
  ```

  ```bash curl
  # 第一轮对话
  # 请将 input 替换为超过 1024 个 token 的长文本，以确保触发缓存创建。
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "x-dashscope-session-cache: enable" \
  -d '{
    "model": "qwen3.7-plus",
    "input": "人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。人工智能是计算机科学的一个重要分支，致力于研究和开发能够模拟、延伸和扩展人类智能的理论、方法、技术和应用系统。\n\n基于以上背景知识，请简要介绍机器学习中的随机森林算法，包括基本原理和应用场景。"
  }'

  # 第二轮对话 - 使用上一轮返回的 id 作为 previous_response_id
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "x-dashscope-session-cache: enable" \
  -d '{
    "model": "qwen3.7-plus",
    "input": "它和 GBDT 的主要区别是什么？",
    "previous_response_id": "response_id_from_the_first_turn"
  }'
  ```
</CodeGroup>

**第二轮响应示例（缓存命中）**

`cached_tokens` 字段显示命中缓存的 token 数：

```json
{
  "id": "145584fd-3dce-4890-99dc-e3896d7f5a42",
  "created_at": 1772440976.0,
  "error": null,
  "incomplete_details": null,
  "instructions": null,
  "metadata": null,
  "model": "qwen3.7-plus",
  "object": "response",
  "output": [
    {
      "id": "msg_62a4e323-d78c-46c7-8469-2ad50f8af4b1",
      "type": "reasoning",
      "content": null
    },
    {
      "id": "msg_560e34a6-1bdf-42ae-993e-590b38249146",
      "content": [
        {
          "annotations": [],
          "text": "Although both Random Forest and GBDT (Gradient Boosting Decision Tree) are ensemble algorithms based on decision trees, they have the following main differences:\n\n1.  **Different Ensemble Strategies**\n    *   **Random Forest**: Based on the **Bagging** idea. Each tree is trained independently, with no dependency between them.\n    *   **GBDT**: Based on the **Boosting** idea. The trees have a strong dependency relationship, where the next tree aims to fit the residuals (negative gradient) of the previous tree's prediction.\n\n2.  **Different Training Methods**\n    *   **Random Forest**: Supports **parallel training** because the trees are independent, which usually results in higher computational efficiency.\n    *   **GBDT**: Must be **trained serially** because the next tree depends on the output of the previous one, making it inherently difficult to parallelize (although engineering implementations like XGBoost have made parallel optimizations at the feature level).\n\n3.  **Different Optimization Objectives**\n    *   **Random Forest**: Mainly reduces **variance** by averaging multiple models to prevent overfitting and improve stability.\n    *   **GBDT**: Mainly reduces **bias** by progressively correcting errors to improve the model's fitting ability and accuracy.\n\n4.  **Sensitivity to Outliers**\n    *   **Random Forest**: Relatively robust and not sensitive to outliers.\n    *   **GBDT**: More sensitive to outliers because outliers produce large residuals, which affect the fitting direction of subsequent trees.\n\nIn summary, Random Forest excels in stability and parallel efficiency, while GBDT usually performs better in terms of accuracy but is more complex to tune and slower to train.",
          "type": "output_text"
        }
      ],
      "role": "assistant",
      "status": "completed",
      "type": "message"
    }
  ],
  "parallel_tool_calls": false,
  "temperature": null,
  "tool_choice": "auto",
  "tools": [],
  "top_p": null,
  "status": "completed",
  "usage": {
    "input_tokens": 1524,
    "input_tokens_details": {
      "cached_tokens": 1305
    },
    "output_tokens": 1534,
    "output_tokens_details": {
      "reasoning_tokens": 1187
    },
    "total_tokens": 3058
  }
}
```

第二轮对话的 `input_tokens` 为 1524，其中 `cached_tokens` 为 1305，说明第一轮的上下文被缓存命中，可以有效降低推理延迟和成本。

### 计费

会话缓存的计费规则与显式缓存一致：

- **缓存创建**：按标准输入 token 价格的 125% 计费。

- **缓存命中**：按标准输入 token 价格的 10% 计费。

  <Note>
    可通过 `usage.input_tokens_details.cached_tokens` 参数查看命中缓存的 token 数。
  </Note>

- **其他 token**：未命中且未用于创建缓存的 token 按标准价格计费。

### 限制

- 最小可缓存的 prompt 长度为 **1024** 个 token。
- 缓存有效期为 **5 分钟**，命中后重置。
- 仅适用于 Responses API，需配合 `previous_response_id` 参数进行多轮对话。
- 会话缓存与显式缓存、隐式缓存互斥。开启会话缓存时，其他两种模式不生效。

## FAQ

### 上下文缓存的有效期是多久（可以保留多长时间）？

上下文缓存的有效期取决于缓存类型：

- **显式缓存**：有效期为 5 分钟，且每次命中后会重新计时 5 分钟。若超过 5 分钟未被命中，系统将自动清理该缓存块。
- **隐式缓存**：由系统自动管理，无固定有效期。系统会定期清理长期未使用的缓存数据。

<Note>
  此处的有效期指通过 API 调用时上下文缓存的生命周期，与控制台"模型体验 / 模型调试"页面中展示的历史对话记录不是同一功能。
</Note>

### 如何关闭隐式缓存？

无法关闭。隐式缓存对所有支持的模型自动开启，因为它不影响回答质量，且在命中缓存时能降低成本、提升响应速度。

### 为什么创建了显式缓存却没有命中？

可能有以下原因：

- 缓存创建后 5 分钟内未被命中，系统在缓存块过期后将其清除。
- 如果最后一个 `content` 块与已有缓存块之间相隔超过 20 个 `content` 块，则不会命中缓存。建议创建新的缓存块。

### 命中显式缓存会重置有效期吗？

会。每次命中都会将该缓存块的有效期重置为 5 分钟。

### 显式缓存是否在不同账号之间共享？

不会。隐式缓存和显式缓存的数据都按账号隔离，不会跨账号共享。

### 显式缓存是否在不同模型之间共享？

不会。缓存数据按模型隔离，不会跨模型共享。

### 为什么 `input_tokens` 不等于 `cache_creation_input_tokens` + `cached_tokens`？

为了保证模型输出质量，后端服务会在用户提供的 prompt 之后附加少量 token（通常不超过 10 个）。这些 token 位于 `cache_control` 标记之后，因此不计入缓存创建或命中的 token 数，但会包含在总的 `input_tokens` 中。

### 如何查看一段时间内（按天/按周）的缓存命中 Token 数量？

可通过以下方式获取指定时间段内的缓存命中数据：

- **用量分析**：在千问AI平台控制台[用量分析](https://platform.qianwenai.com/home/analytics)页面，选择目标模型和时间范围，查看 `cache_tokens` 指标（支持按分钟/按小时精度统计）。
- **账单明细**：在千问AI平台控制台导出账单明细，按计费类型筛选“缓存命中”（`cache`）相关记录，按日期分组汇总，可获取每日的缓存命中 Token 计量数据。详细操作请参见[账单查询与费用管理](/resources/bill-query)。
