> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 流式输出

> 逐 token 实时接收模型生成的文本。

## 启用流式输出

<Tabs>
  <Tab title="OpenAI Chat Completions">
    默认不返回用量信息。设置 `stream_options` 可在**最后一个 chunk** 中获取 token 用量。

    <CodeGroup>
      ```python Python {7,8}
      import os
      from openai import OpenAI
      client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

      completion = client.chat.completions.create(
        model="qwen3.7-plus",
        messages=[{"role": "user", "content": "Hi"}],
        stream=True,                              # ← 启用流式输出
        stream_options={"include_usage": True},    # ← 仅在最后一个 chunk 返回用量
      )
      for chunk in completion:
        if chunk.choices:
          print(chunk.choices[0].delta.content or "", end="", flush=True)
        elif chunk.usage:                         # ← 最后一个 chunk：仅含用量信息
          print(f"\nTokens: {chunk.usage.total_tokens}")
      ```

      ```javascript Node.js {7,8}
      import OpenAI from "openai";
      const client = new OpenAI({ apiKey: process.env.DASHSCOPE_API_KEY, baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1" });

      const stream = await client.chat.completions.create({
        model: "qwen3.7-plus",
        messages: [{ role: "user", content: "Hi" }],
        stream: true,                             // ← 启用流式输出
        stream_options: { include_usage: true },   // ← 在最后一个 chunk 返回用量
      });
      for await (const chunk of stream) {
        if (chunk.choices?.length > 0)
          process.stdout.write(chunk.choices[0]?.delta?.content || "");
        else if (chunk.usage)
          console.log(`\nTokens: ${chunk.usage.total_tokens}`);
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" --no-buffer \
        -d '{"model":"qwen3.7-plus","messages":[{"role":"user","content":"Hi"}],"stream":true,"stream_options":{"include_usage":true}}'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="OpenAI Responses API">
    <CodeGroup>
      ```python Python {6}
      import os
      from openai import OpenAI
      client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

      stream = client.responses.create(
        model="qwen3.7-plus",
        input="Hi",
        stream=True,                              # ← 启用流式输出
      )
      for event in stream:
        if event.type == "response.output_text.delta":
          print(event.delta, end="", flush=True)
        elif event.type == "response.completed":
          print(f"\nTokens: {event.response.usage.total_tokens}")
      ```

      ```javascript Node.js {6}
      import OpenAI from "openai";
      const client = new OpenAI({ apiKey: process.env.DASHSCOPE_API_KEY, baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1" });

      const stream = await client.responses.create({
        model: "qwen3.7-plus",
        input: "Hi",
        stream: true,                             // ← 启用流式输出
      });
      for await (const event of stream) {
        if (event.type === "response.output_text.delta")
          process.stdout.write(event.delta);
        else if (event.type === "response.completed")
          console.log(`\nTokens: ${event.response.usage.total_tokens}`);
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" --no-buffer \
        -d '{"model":"qwen3.7-plus","input":"Hi","stream":true}'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    与 OpenAI 兼容（仅在最后一个 chunk 返回用量）不同，DashScope 在**每个 chunk** 中都返回实时 token 用量，便于监控成本或提前终止请求。

    <Note>
      Qwen3.5 和 Qwen3.6 系列模型使用下方示例中的 `multimodal-generation` 端点。qwen-plus、qwen3-max 等早期模型使用 `text-generation` 端点。详见 [DashScope API 参考](/api-reference/chat/dashscope)。
    </Note>

    <CodeGroup>
      ```python Python {10,11}
      from http import HTTPStatus
      import dashscope
      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
      from dashscope import MultiModalConversation

      responses = MultiModalConversation.call(
        model="qwen3.7-plus",
        messages=[{"role": "user", "content": [{"text": "Hi"}]}],
        stream=True,                # ← 启用流式输出
        incremental_output=True,    # ← 推荐：每个 chunk 仅返回新增 token
      )
      for resp in responses:
        if resp.status_code == HTTPStatus.OK:
          content = resp.output.choices[0].message.content
          if content:
            print(content[0]["text"], end="", flush=True)
      ```

      ```java Java {12,14}
      import java.util.*;
      import com.alibaba.dashscope.aigc.multimodalconversation.*;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.utils.Constants;
      Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";

      MultiModalConversationParam param = MultiModalConversationParam.builder()
        .apiKey(apiKey).model("qwen3.7-plus")
        .messages(Arrays.asList(
          MultiModalConversationMessage.builder().role(Role.USER.getValue())
            .content(Arrays.asList(Collections.singletonMap("text", "Hi"))).build()))
        .incrementalOutput(true)    // ← 推荐：仅返回新增 token
        .build();
      new MultiModalConversation().streamCall(param)  // ← 使用 streamCall 而非 call
        .subscribe(msg -> System.out.print(
          msg.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text")));
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" -H "Content-Type: application/json" \
        -H "X-DashScope-SSE: enable" \
        -d '{"model":"qwen3.7-plus","input":{"messages":[{"role":"user","content":[{"text":"Hi"}]}]},"parameters":{"incremental_output":true}}'
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## 事件格式

每个 SSE 事件是一行 `data:`，内容为 JSON 格式的 chunk。最后一条 `data: [DONE]` 表示流结束。

```text
data: {"choices":[{"delta":{"content":"I am"},...,"finish_reason":null}],...}
data: {"choices":[{"delta":{"content":" Qwen"},...,"finish_reason":null}],...}
data: {"choices":[{"delta":{"content":""},...,"finish_reason":"stop"}],...}
data: [DONE]
```

## 思考模式下的流式输出

两阶段流式输出：先输出思考过程，再输出回答。

<Tabs>
  <Tab title="OpenAI Chat Completions">
    ```python
    for chunk in completion:
      delta = chunk.choices[0].delta
      if hasattr(delta, "reasoning_content") and delta.reasoning_content:
        print(delta.reasoning_content, end="", flush=True)  # ← 阶段 1：思考
      if hasattr(delta, "content") and delta.content:
        print(delta.content, end="", flush=True)             # ← 阶段 2：回答
    ```
  </Tab>

  <Tab title="OpenAI Responses API">
    ```python
    for event in stream:
      if event.type == "response.reasoning_text.delta":
        print(event.delta, end="", flush=True)              # ← 阶段 1：思考
      elif event.type == "response.output_text.delta":
        print(event.delta, end="", flush=True)              # ← 阶段 2：回答
    ```
  </Tab>

  <Tab title="DashScope">
    ```python
    for chunk in completion:
      msg = chunk.output.choices[0].message
      if msg.reasoning_content:   # ← 阶段 1：思考
        print(msg.reasoning_content, end="", flush=True)
      if msg.content:             # ← 阶段 2：回答
        print(msg.content, end="", flush=True)
    ```
  </Tab>
</Tabs>

-> 完整配置：[推理模式](/developer-guides/text-generation/thinking) | Qwen3-Omni：[音视频](/developer-guides/speech/multimodal-speech)

## 工具调用的流式输出

流式输出 [function calling](/developer-guides/tool-calling/function-calling) 响应时，工具调用的参数以增量 delta 形式到达，需要拼接完成后再解析 JSON。

<Tabs>
  <Tab title="Chat Completions">
    每个 chunk 的 `delta` 可能包含 `tool_calls[i].function.arguments`——一个 JSON 片段字符串。按 tool call 索引累积所有片段，流结束后再 `JSON.parse()` 完整字符串。

    ```python
    tool_args = {}
    for chunk in completion:
      delta = chunk.choices[0].delta
      if delta.tool_calls:
        for tc in delta.tool_calls:
          tool_args.setdefault(tc.index, "")
          tool_args[tc.index] += tc.function.arguments or ""
    # 流结束后：
    for idx, args_str in tool_args.items():
      parsed = json.loads(args_str)
    ```
  </Tab>

  <Tab title="Responses API">
    工具调用通过 `response.function_call_arguments.delta` 事件发送参数片段。持续拼接 delta，直到收到 `response.function_call_arguments.done` 事件。

    ```python
    args_buffer = ""
    for event in stream:
      if event.type == "response.function_call_arguments.delta":
        args_buffer += event.delta
      elif event.type == "response.function_call_arguments.done":
        parsed = json.loads(args_buffer)
        args_buffer = ""
    ```
  </Tab>
</Tabs>

<Tip>
  启用[思考模式](/developer-guides/text-generation/thinking)后，流式输出分为三个阶段：思考 token、工具调用 delta，以及（发送工具返回结果后的）最终回答。
</Tip>

## 注意事项

- **Nginx 代理**：设置 `proxy_buffering off`，否则 SSE 事件会被缓冲
- **高并发场景**：合理配置连接池大小，监控文件描述符数量
- **Web 前端**：使用 `ReadableStream` + `TextDecoderStream` 处理流
- **输出质量**：流式输出不影响响应质量
- **仅支持流式输出的模型**：QwQ 和 QVQ 仅支持流式输出，非流式调用会失败或返回空内容。

## 常见问题

**非流式调用和流式调用有什么区别？**

主要区别如下：

- **超时限制**：非流式调用的最大超时时间固定为 300 秒，如果模型在 300 秒内未完成生成，请求将超时失败。
- **输出结构**：非流式调用一次性返回完整的响应结果（单个 JSON 对象）。流式调用通过 SSE 协议逐步返回数据块（chunk），每个 chunk 包含部分生成内容，需要客户端拼接。
- **功能兼容**：两者均支持 JSON Mode、Function Call 等功能特性，功能上没有差异。

建议优先使用流式输出，可以避免超时问题并获得更好的用户体验。

**流式输出是否支持 JSON Mode（结构化输出）？**

支持。在请求中同时设置 `stream` 为 `true` 和 `response_format` 为 `{"type": "json_object"}` 即可。模型会以流式方式逐步返回 JSON 格式的内容片段，最终拼接后的完整输出为合法的 JSON。
