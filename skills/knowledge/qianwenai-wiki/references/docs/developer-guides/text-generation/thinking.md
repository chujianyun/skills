> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 思考模式

> 通过逐步推理解决复杂任务

Thinking（推理）模型在回答前先进行推理，输出 `reasoning_content`（Chat Completions / DashScope）或 `reasoning_text` 事件（Responses API）。模型支持两种推理模式：

- **混合模式**：通过 `enable_thinking` 逐请求开关推理。
- **纯推理模式**：始终进行推理，无法关闭。

## 支持的模型

<Accordion title="展开查看完整模型列表">
  ### Qwen3.8

  - **Max 系列**（混合模式，默认开启）：`qwen3.8-max`
  - **开源系列**（混合思考模式，**默认开启思考模式**）：`qwen3.8-2.4t-a95b`

  ### Qwen3.7

  - **Max 系列**（混合模式，默认开启）：`qwen3.7-max`、`qwen3.7-max-2026-06-08`、`qwen3.7-max-2026-05-20`
  - **Max 系列**（仅支持思考模式）：`qwen3.7-max-preview`、`qwen3.7-max-2026-05-17`
  - **Plus 系列**（混合模式，默认开启）：`qwen3.7-plus`、`qwen3.7-plus-2026-05-26`
  - **Flash 系列**（混合模式，默认开启，`thinking_budget` 上限 256K）：`qwen3.7-flash`、`qwen3.7-flash-2026-07-15`

  ### Qwen3.6

  - **Max 系列**（混合模式，默认开启）：`qwen3.6-max-preview`
  - **Plus 系列**（混合模式，默认开启）：`qwen3.6-plus`、`qwen3.6-plus-2026-04-02`
  - **Flash 系列**（混合模式，默认开启，`thinking_budget` 上限 128K）：`qwen3.6-flash`、`qwen3.6-flash-2026-04-16`
  - **开源版**：`qwen3.6-35b-a3b`

  ### Qwen3.5

  **商业版**

  - **Plus 系列**（混合模式，默认开启）：`qwen3.5-plus`、`qwen3.5-plus-2026-02-15`
  - **Flash 系列**（混合模式，默认开启）：`qwen3.5-flash`、`qwen3.5-flash-2026-02-23`

  **开源版**

  - 混合模式，默认开启：`qwen3.5-397b-a17b`、`qwen3.5-122b-a10b`、`qwen3.5-27b`、`qwen3.5-35b-a3b`

  ### Qwen3

  **商业版**

  - **Max 系列**（混合模式，默认关闭）：`qwen3-max`、`qwen3-max-2026-01-23`、`qwen3-max-preview`
  - **Plus 系列**（混合模式，默认关闭）：`qwen-plus`、`qwen-plus-latest`、`qwen-plus-2025-04-28` 及之后的快照版模型
  - **Flash 系列**（混合模式，默认关闭）：`qwen-flash`、`qwen-flash-2025-07-28` 及之后的快照版模型
  - **Turbo 系列**（混合模式，默认关闭）：`qwen-turbo` 及之后的快照版模型

  **开源版**

  - 混合模式，默认开启：`qwen3-235b-a22b`、`qwen3-32b`、`qwen3-30b-a3b`、`qwen3-14b`、`qwen3-8b`
  - 纯推理模式：`qwen3-next-80b-a3b-thinking`、`qwen3-235b-a22b-thinking-2507`、`qwen3-30b-a3b-thinking-2507`

  ### QwQ（基于 Qwen2.5）

  - 纯推理模式：`qwq-plus`

  ### DeepSeek

  **千问AI平台部署**

  - 混合模式，默认开启：`deepseek-v4-pro-0813`、`deepseek-v4-pro`、`deepseek-v4-flash`、`deepseek-v4-flash-0731`
  - 混合模式，默认关闭：`deepseek-v3.2`、`deepseek-v3.2-exp`、`deepseek-v3.1`
  - 纯推理模式：`deepseek-r1`、`deepseek-r1-0528`、DeepSeek-R1 蒸馏模型

  **硅基流动部署**

  - 混合模式，默认关闭：`siliconflow/deepseek-v3.2`、`siliconflow/deepseek-v3.1-terminus`
  - 纯推理模式：`siliconflow/deepseek-r1-0528`

  **快手万擎部署**

  - 混合模式，默认关闭：`vanchin/deepseek-v3.2-think`、`vanchin/deepseek-v3.1-terminus`
  - 纯推理模式：`vanchin/deepseek-r1`

  ### GLM

  - 混合模式，默认开启：`glm-5.2`、`glm-5.2-fast-preview`、`glm-5.1`、`glm-5`、`glm-4.7`、`glm-4.6`、`glm-4.5`、`glm-4.5-air`

  ### Kimi

  **千问AI平台部署**

  - 仅思考模式：`kimi-k2.7-code`
  - 混合模式，默认关闭：`kimi-k2.6`、`kimi-k2.5`
  - 纯推理模式：`kimi-k2-thinking`

  **月之暗面部署**

  - 仅思考模式：`kimi/kimi-k3`、`kimi/kimi-k2.7-code-highspeed`、`kimi/kimi-k2.7-code`
  - 混合模式，默认开启：`kimi/kimi-k2.6`、`kimi/kimi-k2.5`

  ### MiniMax

  **千问AI平台部署**

  - 纯推理模式：`MiniMax-M2.5`、`MiniMax-M2.1`

  **MiniMax 部署**

  - 混合思考模式：`MiniMax/MiniMax-M3`

  <Note>
    MiniMax/MiniMax-M3 通过 `thinking` 参数控制思考模式，取值为 `adaptive`（自适应，默认）或 `disabled`（关闭）。详细用法请参见 [MiniMax-稀宇科技](/developer-guides/third-party-models/minimax-minimaxi)。
  </Note>

  - 纯推理模式：`MiniMax/MiniMax-M2.7`、`MiniMax/MiniMax-M2.5`、`MiniMax/MiniMax-M2.1`

  ### Stepfun

  - 混合思考模式：`stepfun/step-3.7-flash`
</Accordion>

## 开启推理

<Tabs>
  <Tab title="OpenAI Chat Completions">
    <CodeGroup>
      ```python Python {8}
      import os
      from openai import OpenAI
      client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

      completion = client.chat.completions.create(
        model="qwen3.7-plus",
        messages=[{"role": "user", "content": "If 3x + 7 = 22, what is x?"}],
        extra_body={"enable_thinking": True},              # ← 开启推理
        stream=True,
      )
      for chunk in completion:
        if not chunk.choices:
          continue
        delta = chunk.choices[0].delta
        if hasattr(delta, "reasoning_content") and delta.reasoning_content:
          print(delta.reasoning_content, end="", flush=True)  # ← 阶段 1：推理过程
        if hasattr(delta, "content") and delta.content:
          print(delta.content, end="", flush=True)             # ← 阶段 2：最终回答
      ```

      ```javascript Node.js {7}
      import OpenAI from "openai";
      const client = new OpenAI({ apiKey: process.env.DASHSCOPE_API_KEY, baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1" });

      const stream = await client.chat.completions.create({
        model: "qwen3.7-plus",
        messages: [{ role: "user", content: "If 3x + 7 = 22, what is x?" }],
        enable_thinking: true,                             // ← 开启推理
        stream: true,
      });
      for await (const chunk of stream) {
        if (!chunk.choices?.length) continue;
        const delta = chunk.choices[0].delta;
        if (delta.reasoning_content)
          process.stdout.write(delta.reasoning_content); // ← 阶段 1：推理过程
        if (delta.content)
          process.stdout.write(delta.content);            // ← 阶段 2：最终回答
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" --no-buffer \
        -d '{"model":"qwen3.7-plus","messages":[{"role":"user","content":"If 3x + 7 = 22, what is x?"}],"stream":true,"enable_thinking":true}'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="OpenAI Responses API">
    推理内容通过 `response.reasoning_text.delta` 事件返回，随后通过 `response.output_text.delta` 返回最终回答。

    <CodeGroup>
      ```python Python {8}
      import os
      from openai import OpenAI
      client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

      stream = client.responses.create(
        model="qwen3.7-plus",
        input="If 3x + 7 = 22, what is x?",
        extra_body={"enable_thinking": True},              # ← 开启推理
        stream=True,
      )
      for chunk in stream:
        if chunk.type == "response.reasoning_text.delta":
          print(chunk.delta, end="", flush=True)         # ← 阶段 1：推理过程
        elif chunk.type == "response.output_text.delta":
          print(chunk.delta, end="", flush=True)         # ← 阶段 2：最终回答
      ```

      ```javascript Node.js {7}
      import OpenAI from "openai";
      const client = new OpenAI({ apiKey: process.env.DASHSCOPE_API_KEY, baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1" });

      const stream = await client.responses.create({
        model: "qwen3.7-plus",
        input: "If 3x + 7 = 22, what is x?",
        enable_thinking: true,                             // ← 开启推理
        stream: true,
      });
      for await (const chunk of stream) {
        if (chunk.type === "response.reasoning_text.delta")
          process.stdout.write(chunk.delta);             // ← 阶段 1：推理过程
        else if (chunk.type === "response.output_text.delta")
          process.stdout.write(chunk.delta);             // ← 阶段 2：最终回答
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" --no-buffer \
        -d '{"model":"qwen3.7-plus","input":"If 3x + 7 = 22, what is x?","stream":true,"enable_thinking":true}'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python {8,10}
      import dashscope
      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
      from dashscope import MultiModalConversation

      responses = MultiModalConversation.call(
        model="qwen3.7-plus",
        messages=[{"role": "user", "content": [{"text": "If 3x + 7 = 22, what is x?"}]}],
        enable_thinking=True,                              # ← 开启推理
        stream=True,
        incremental_output=True,                           # ← 推荐：仅返回新增 token
      )
      for chunk in responses:
        msg = chunk.output.choices[0].message
        if msg.reasoning_content:
          print(msg.reasoning_content, end="", flush=True)   # ← 阶段 1：推理过程
        if msg.content and msg.content[0].get("text"):
          print(msg.content[0]["text"], end="", flush=True)   # ← 阶段 2：最终回答
      ```

      ```java Java {5,15,16}
      import java.util.*;
      import com.alibaba.dashscope.aigc.multimodalconversation.*;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.utils.Constants;
      Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";

      // 需要 DashScope Java SDK 2.19.4+
      MultiModalMessage userMsg = MultiModalMessage.builder()
        .role(Role.USER.getValue())
        .content(List.of(Map.of("text", "If 3x + 7 = 22, what is x?")))
        .build();
      MultiModalConversationParam param = MultiModalConversationParam.builder()
        .apiKey(apiKey).model("qwen3.7-plus")
        .enableThinking(true)                              // ← 开启推理
        .incrementalOutput(true)                           // ← 推荐：仅返回新增 token
        .messages(Arrays.asList(userMsg))
        .build();
      conv.streamCall(param).blockingForEach(result -> {
        var msg = result.getOutput().getChoices().get(0).getMessage();
        if (msg.getReasoningContent() != null)
          System.out.print(msg.getReasoningContent());   // ← 阶段 1：推理过程
        if (msg.getContent() != null && !msg.getContent().isEmpty())
          System.out.print(msg.getContent().get(0).get("text"));  // ← 阶段 2：最终回答
      });
      ```

      ```bash curl
      curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -H "X-DashScope-SSE: enable" \
        -d '{"model":"qwen3.7-plus","input":{"messages":[{"role":"user","content":[{"text":"If 3x + 7 = 22, what is x?"}]}]},"parameters":{"enable_thinking":true,"incremental_output":true}}'
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## 控制推理深度

### Token 预算

使用 `thinking_budget` 限制推理 token 的最大数量。达到上限后，模型会停止推理并立即生成回答。适用于 Qwen3.8、Qwen3.7、Qwen3.6、Qwen3.5、Qwen3-VL、Qwen3、GLM（千问AI平台直供）、Kimi（千问AI平台直供）系列模型。仅适用于 Chat Completions 和 DashScope，Responses API 暂不支持。

<Tabs>
  <Tab title="OpenAI Chat Completions">
    ```python
    extra_body={"enable_thinking": True, "thinking_budget": 500}
    ```
  </Tab>

  <Tab title="DashScope">
    ```python
    enable_thinking=True,
    thinking_budget=500,
    ```
  </Tab>
</Tabs>

### reasoning\_effort

通过 `reasoning_effort` 参数以档位方式控制推理力度，无需手动指定 token 数。不同模型支持的可选值和默认值不同。以 `qwen3.8-max` 为例（可选值：`low`、`medium`、`xhigh`，默认 `xhigh`）：

<Tabs>
  <Tab title="OpenAI Chat Completions">
    ```python
    extra_body={"enable_thinking": True, "reasoning_effort": "medium"}
    ```
  </Tab>

  <Tab title="DashScope">
    ```python
    enable_thinking=True,
    reasoning_effort="medium",
    ```
  </Tab>
</Tabs>

<Warning>
  `qwen3.8-max` 不支持 `reasoning_effort` 与 `thinking_budget` 同时设置，同时传入会报错。两者均未设置时使用模型默认值。
</Warning>

<Note>
  该参数非 OpenAI 标准参数，通过 Python SDK 调用时请放入 `extra_body`。各模型支持的档位、默认值及与 `thinking_budget` 的映射关系详见 [API 参考文档](/api-reference/chat/openai-chat)。
</Note>

### 控制台体验深度思考

1. 登录千问AI平台控制台。
2. 在左侧导航栏选择**体验** > **文本模型**，进入模型体验中心。
3. 页面默认展示 Qwen3.7-Max 模型，也可单击模型名称，在下拉列表中选择其他 Qwen3 系列模型。
4. 在输入框底部单击**深度思考**，开启推理模式，查看模型的思考过程。
5. 切换到**模型调试**标签页，在配置面板中设置 `thinking_budget` 参数，控制思维链输出的最大 Token 数量，取值范围 1\~32768，默认值 4000。如需体验更多模型，可前往模型广场。

### Prompt 级控制

开启 `enable_thinking: true` 后，可在消息中添加 `/no_think` 跳过当次推理，用 `/think` 恢复。多条指令以最后一条为准。支持开源 Qwen3 混合模型和 `qwen-plus-2025-04-28`。

## 多轮对话中传递思考过程

多轮对话中，模型默认不会读取历史消息中 `messages` 数组里的 `reasoning_content`。将 `preserve_thinking` 设为 `true` 后，assistant 消息中的 `reasoning_content` 将被拼接到下一轮输入，让模型参考之前的推理过程。

<Warning>
  `preserve_thinking` 参数仅支持 `qwen3.8-max`（默认开启）、`qwen3.7-max`、`qwen3.7-max-2026-06-08`、`qwen3.7-max-2026-05-20`、`qwen3.7-max-preview`、`qwen3.7-max-2026-05-17`、`qwen3.7-plus`、`qwen3.7-plus-2026-05-26`、`qwen3.6-max-preview`、`qwen3.6-plus`、`qwen3.6-plus-2026-04-02`、`qwen3.7-flash`、`qwen3.7-flash-2026-07-15`、`kimi-k2.7-code`、`kimi-k2.6`（千问AI平台部署）、`kimi/kimi-k3`、`kimi/kimi-k2.7-code-highspeed`、`kimi/kimi-k2.7-code`、`kimi/kimi-k2.6`（月之暗面部署）。
</Warning>

<Tabs>
  <Tab title="OpenAI Chat Completions">
    ```python
    extra_body={"preserve_thinking": True}
    ```
  </Tab>

  <Tab title="DashScope">
    ```python
    preserve_thinking=True,
    ```
  </Tab>
</Tabs>

<Note>
  - `preserve_thinking` 非 OpenAI 标准参数，使用 Python SDK 需通过 `extra_body` 传入。
  - Java SDK 暂不支持 `preserve_thinking` 参数。通过 HTTP 调用时，请将 `preserve_thinking` 放入 `parameters` 对象中。
  - 启用后，历史对话中的 `reasoning_content` 会计入输入 Token 数量并计费。
</Note>

## 推理模式下的 function calling

开启推理后进行 [function calling](/developer-guides/tool-calling/function-calling)，模型会先推理应调用哪些工具、如何使用返回结果，再生成回答。响应中每次工具调用前都会包含 `reasoning_content`。

**要点**：

- 在 `tools` 数组的同时传入 `enable_thinking: true` 即可，无需额外配置。
- 在多轮工具调用流程中，将助手的 `reasoning_content` 一并回传。省略该字段会降低准确性。
- 流式输出先返回推理 token，再返回工具调用的增量数据。解析方式参见[流式输出中的工具调用](/developer-guides/run-and-scale/streaming#工具调用的流式输出)。
- `thinking_budget` 的用法与普通推理模式一致。

<Tip>
  推理模式在复杂工具编排场景中价值最大——多步推理选择工具、确定参数、解读结果。对于简单的单工具调用，额外开销可能不值得。
</Tip>

## 计费说明

思考内容按输出 token 计费。部分混合思考模型在思考与非思考模式下价格不同。模型在思考模式下若未输出思考过程，按非思考模式价格计费。

具体模型的思考模式定价请参见[模型市场](https://www.qianwenai.com/models)。

## 常见问题

<Accordion title="如何以非流式（同步）方式调用深度思考模型？">
  本文示例默认采用流式输出（推荐，可实时查看思考过程、避免长时间等待）。商业版深度思考模型（如 qwen-plus、qwen3-max、qwen-flash 等）也支持非流式（同步）输出，一次性返回完整的思考过程与回复。

  <Warning>
    将流式示例改为非流式时，请同步修改**结果解析代码**：非流式调用返回的是完整的响应对象（`completion`），**不能**再像流式示例那样通过 `for chunk in completion` 迭代（否则会报错 `'tuple' object has no attribute 'choices'`），而应直接读取 `completion.choices[0].message.reasoning_content`（思考过程）与 `completion.choices[0].message.content`（回复内容）。此外，`stream=False` 时不能设置 `stream_options` 参数。
  </Warning>

  以下以 OpenAI 兼容接口、非流式调用 qwen3.8-max 开启思考模式为例：

  ```python
  from openai import OpenAI
  import os
  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )
  completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=[{"role": "user", "content": "你是谁"}],
    extra_body={"enable_thinking": True},
    stream=False,
  )
  message = completion.choices[0].message
  print("=" * 20 + "思考过程" + "=" * 20 + "\n")
  print(getattr(message, "reasoning_content", "") or "")
  print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
  print(message.content)
  ```

  <Note>
    部分模型（如 qwen3-235b-a22b、qwen3-32b 等开源版）仅支持流式输出，非流式调用会报错 `parameter.enable_thinking only support stream call`，此类模型请使用流式调用。
  </Note>
</Accordion>

<Accordion title="qwen3.7-plus 调用响应慢如何排查？">
  qwen3.7-plus 属于混合思考模式模型，且默认开启思考模式。思考过程会生成大量推理 Token（实测占总输出 Token 的 60% 以上），因此单次调用的总耗时明显长于非思考模式。此时 Token 生成速度本身并无异常（实测约 52～54 Tokens/s），总耗时的差异主要来自思考过程产生的 Token 数量，而非模型或网络异常。

  排查与优化建议：

  - 确认是否开启了思考模式。qwen3.7-plus 默认开启，可根据响应中是否返回 `reasoning_content` 字段判断。
  - 查看响应用量中的 `completion_tokens` 与 `reasoning_tokens`。若 `reasoning_tokens` 占比较高，则总耗时长属于思考模式的预期表现。
  - 若无需思考过程，在请求中将 `enable_thinking` 设为 `false` 关闭思考模式。关闭后输出 Token 大幅减少，实测总耗时可降低 60%～75%。
  - 若需保留思考能力，可改用流式输出，以更快获得首个 Token 并实时查看思考过程，避免长时间等待完整响应。

  <Note>
    用量统计中展示的是单次调用的整体耗时（含思考 Token 的生成时间），并非单个 Token 的生成延迟。
  </Note>
</Accordion>

<Accordion title="使用第三方客户端调用深度思考模型时，输出思考标签后客户端断连怎么办？">
  该问题属于客户端侧问题，并非模型限制思考过程输出。千问AI平台通过`enable_thinking`参数控制思考模式开关，模型返回结果中的`reasoning_content`字段包含完整思考过程内容，模型侧会正常返回思考内容。断连通常由客户端网络波动或客户端版本兼容问题引起。

  排查步骤：

  - 检查客户端网络连接的稳定性。
  - 将客户端升级至最新版本。
  - 查看客户端日志，确认断连时间点与思考标签输出的关联。

  您也可以通过 DashScope API 直接调用模型，验证思考功能是否正常工作。
</Accordion>

<Accordion title="长提示词生成失败或超时怎么办？">
  使用长提示词调用模型时出现生成失败或响应超时，通常是因为开启了思考模式（`enable_thinking` 为 `true`）。思考模式会增加处理时间，长提示词场景下可能导致响应被截断或请求超时。

  - **关闭思考模式**：将 `enable_thinking` 设为 `false`，处理时间可从约 50 秒降至约 30 秒。
  - **开启流式输出**：将 `stream` 设为 `true`，避免非流式调用的超时限制。
  - **调大超时时间**：如需保留思考模式，请将客户端超时时间设为 180 秒以上。
</Accordion>

## 注意事项

- **部分模型必须使用流式输出**：Qwen3.6 Plus、Qwen3.5 Plus/Flash、Qwen3 Max、Qwen Plus/Flash/Turbo（商业版）以及 Qwen3.5 开源模型支持非流式输出。Qwen3 开源模型必须使用流式输出。始终建议使用流式输出以避免超时风险。
- **推理模式下不支持语音输出**（Qwen3-Omni）：文本和图片输入正常，但开启推理后无法输出语音。
