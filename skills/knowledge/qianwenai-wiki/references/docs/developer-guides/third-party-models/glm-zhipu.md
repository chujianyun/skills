> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# GLM-智谱

> 本文档介绍如何在千问AI平台平台调用智谱（ZHIPU AI）直供的模型推理服务。

## 服务开通

1. 前往[千问AI平台控制台](https://www.qianwenai.com/models)，搜索 GLM，找到智谱直供的 GLM 模型卡片，单击立即开通；
2. 在弹窗内确认开通及授权。

完成以上步骤即可调用智谱提供的 GLM 模型服务。

## 快速开始

**前提条件**

- 需要已开通千问AI平台服务并完成API Key的创建
- 如果通过SDK调用，需要安装对应SDK

glm-5.2 是 GLM 系列最新模型，支持真正可用的 1M 上下文。ZHIPU/GLM-5.2、ZHIPU/GLM-5.1、ZHIPU/GLM-5 支持通过 `enable_thinking` 参数设置思考与非思考模式：

- **思考模式**（`enable_thinking: true`，默认）：模型会输出详细的推理过程（`reasoning_content`）
- **非思考模式**（`enable_thinking: false`）：直接输出结果，不包含推理过程

以下示例演示如何调用思考模式的 ZHIPU/GLM-5.2 模型进行文本生成。

<Tabs>
  <Tab title="OpenAI兼容">
    <Note>
      `enable_thinking` 非 OpenAI 标准参数，OpenAI Python SDK 通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入。
    </Note>

    <Tabs>
      <Tab title="Python">
        ```python
        from openai import OpenAI
        import os

        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        completion = client.chat.completions.create(
          model="ZHIPU/GLM-5.2",
          messages=[{"role": "user", "content": "1+1等于多少？"}],
          # reasoning_effort 控制思考深度，可选值：max（默认）、high、none
          extra_body={"enable_thinking": True, "reasoning_effort": "max"}
        )

        msg = completion.choices[0].message

        if getattr(msg, "reasoning_content", None):
          print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
          print(msg.reasoning_content or "")
        print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
        print(msg.content)
        ```
      </Tab>

      <Tab title="Node.js">
        ```javascript
        import OpenAI from "openai";
        import process from 'process';

        const client = new OpenAI({
          apiKey: process.env.DASHSCOPE_API_KEY,
          baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
        });

        const messages = [
          { role: "system", content: "You are a helpful assistant." },
          { role: "user", content: "1+1等于多少？" },
        ];

        const response = await client.chat.completions.create({
          model: "ZHIPU/GLM-5.2",
          messages,
          enable_thinking: true,
          // reasoning_effort 控制思考深度，可选值：max（默认）、high、none
          reasoning_effort: 'max',
        });

        const msg = response.choices[0].message;

        if (msg.reasoning_content) {
          console.log("\n" + "=".repeat(20) + "思考过程" + "=".repeat(20) + "\n");
          console.log(msg.reasoning_content);
        }
        console.log("\n" + "=".repeat(20) + "完整回复" + "=".repeat(20) + "\n");
        console.log(msg.content);
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    ```python
    import dashscope
    import os

    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

    response = dashscope.Generation.call(
      model="ZHIPU/GLM-5.2",
      messages=[{"role": "user", "content": "1+1等于多少？"}],
      enable_thinking=True,
      result_format="message"
    )

    msg = response.output.choices[0].message

    if hasattr(msg, "reasoning_content") and msg.reasoning_content:
      print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
      print(msg.reasoning_content)
    print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
    print(msg.content)
    ```
  </Tab>
</Tabs>

## 清除历史思考（clear\_thinking）

`clear_thinking` 参数用于控制多轮对话中是否将历史轮次的 `reasoning_content`（思考过程）作为上下文输入给模型。仅 GLM 系列模型支持。

- `true`：忽略历史轮次的 `reasoning_content`，仅使用可见文本、工具调用与结果等非推理内容作为上下文输入，可降低上下文长度与成本。
- `false`（默认）：保留历史轮次的 `reasoning_content` 并随上下文一同提供给模型。若希望启用 Preserved Thinking，必须在 messages 中完整、未修改、按原顺序透传历史 `reasoning_content`，缺失、裁剪、改写或重排会导致效果下降或无法生效。

<Note>
  该参数只影响跨轮次的历史思考内容，不改变模型在当前轮次内是否产生/输出思考。
</Note>

以下示例使用同一组多轮 messages（`assistant` 消息中携带 `reasoning_content`）。设置 `clear_thinking`=`true` 后，历史思考内容不会被计入上下文，因此 `prompt_tokens` 少于 `false`（默认）的情况，实际数值取决于历史 `reasoning_content` 的长度。

<Tabs>
  <Tab title="OpenAI兼容">
    <Tabs>
      <Tab title="Python">
        ```python
        from openai import OpenAI
        import os
        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        messages = [
          {"role": "user", "content": "请计算 15 * 23 是多少？"},
          {"role": "assistant", "content": "15 乘以 23 等于 345。", "reasoning_content": "15 * 23 = 345"},
          {"role": "user", "content": "那再加上 55 呢？"},
          {"role": "assistant", "content": "345 加上 55 等于 400。", "reasoning_content": "345 + 55 = 400"},
          {"role": "user", "content": "刚才的中间结果是多少？"},
        ]
        completion = client.chat.completions.create(
          model="ZHIPU/GLM-5.2",
          messages=messages,
          extra_body={
            "thinking": {
              "type": "enabled",
              "clear_thinking": False  # False = 保留思考内容
            }
          }
        )
        print(completion.usage.prompt_tokens)  # true 时少于 false
        ```
      </Tab>

      <Tab title="curl">
        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ZHIPU/GLM-5.2",
          "messages": [
            {"role": "user", "content": "请计算 15 * 23 是多少？"},
            {"role": "assistant", "content": "15 乘以 23 等于 345。", "reasoning_content": "15 * 23 = 345"},
            {"role": "user", "content": "那再加上 55 呢？"},
            {"role": "assistant", "content": "345 加上 55 等于 400。", "reasoning_content": "345 + 55 = 400"},
            {"role": "user", "content": "刚才的中间结果是多少？"}
          ],
          "thinking": {
            "type": "enabled",
            "clear_thinking": false
          }
        }'
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

## 其它功能

| **模型**        | **多轮对话** | **Function Calling** | **联网搜索**  | **上下文缓存** | **思考深度控制**           |
| ------------- | -------- | -------------------- | --------- | --------- | -------------------- |
| ZHIPU/GLM-5.2 | ✓        | ✓                    | ✓（仅非思考模式） | ✓         | ✓（reasoning\_effort） |
| ZHIPU/GLM-5.1 | ✓        | ✓                    | ✓（仅非思考模式） | ✓         | ✗                    |
| ZHIPU/GLM-5   | ✓        | ✓                    | ✓（仅非思考模式） | ✓         | ✗                    |

## 参数默认值

| **模型**        | **enable\_thinking** | **temperature** | **top\_p** | **top\_k** | **repetition\_penalty** |
| ------------- | -------------------- | --------------- | ---------- | ---------- | ----------------------- |
| ZHIPU/GLM-5.2 | true                 | 1.0             | 0.95       | —          | —                       |
| ZHIPU/GLM-5.1 | true                 | 1.0             | 0.95       | 20         | 1.0                     |
| ZHIPU/GLM-5   | true                 | 1.0             | 0.95       | 20         | 1.0                     |

## 模型列表与计费

ZHIPU/GLM-5.2、ZHIPU/GLM-5.1、ZHIPU/GLM-5 是智谱AI直供的混合推理模型，适用于智能交互、企业应用及开发辅助等场景。

模型上下文长度与价格信息请参见千问AI平台控制台。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

## 错误码

如果执行报错，请参见错误码文档进行解决。
