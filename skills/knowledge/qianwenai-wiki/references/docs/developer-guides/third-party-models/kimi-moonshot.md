> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Kimi-月之暗面

> 本文档介绍如何在千问AI平台平台调用月之暗面（Moonshot AI）直供的模型推理服务。

## 服务开通

1. 前往[千问AI平台控制台](https://www.qianwenai.com/models)，搜索 Kimi，找到 Kimi 模型卡片，单击立即开通；
2. 在弹窗内确认开通及授权。

完成以上步骤即可调用月之暗面提供的 Kimi 模型服务。

## 快速开始

**前提条件**

- 需要已开通千问AI平台服务并完成API Key的创建
- 如果通过SDK调用，需要安装对应SDK

kimi 系列模型均支持输入文本、图像或视频：

1. kimi/kimi-k2.7-code-highspeed 与 kimi/kimi-k2.7-code 功能完全一致，速度提升5\~6倍。
2. kimi/kimi-k3、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code 为仅思考模型。
3. kimi/kimi-k2.6、kimi/kimi-k2.5 可通过 `enable_thinking` 参数控制思考模式，默认开启思考模式：
   - **思考模式**（`enable_thinking: true`）：模型会输出详细的推理过程（`reasoning_content`）
   - **非思考模式**（`enable_thinking: false` 或不设置）：直接输出结果，不包含推理过程

除 kimi/kimi-k2.5 外，其他模型均支持通过 `preserve_thinking` 参数在多轮对话中传递思考过程，详情请参见[多轮对话中传递思考过程](/developer-guides/text-generation/thinking#多轮对话中传递思考过程)。

以下示例演示如何调用思考模式的 kimi/kimi-k3 模型进行文本生成。

<Tabs>
  <Tab title="OpenAI兼容">
    <Note>
      `reasoning_effort` 非 OpenAI 标准参数，OpenAI Python SDK 通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入。
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
          model="kimi/kimi-k3",
          messages=[{"role": "user", "content": "1+1等于多少？"}],
          # 通过 extra_body 设置 reasoning_effort 开启思考模式
          extra_body={"reasoning_effort": "max"}
        )

        msg = completion.choices[0].message

        if getattr(msg, "reasoning_content", None):
          print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
          print(msg.reasoning_content or "")
        print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
        print(msg.content)
        ```

        **返回结果**

        ```text
        ====================思考过程====================

        用户问了一个简单的数学问题："1+1等于多少？"

        这是一个非常基础的算术问题，答案是2。

        我应该直接、清晰地回答这个问题。虽然用户用中文提问，但答案是一个通用的数学事实。

        回答结构：
        1. 直接给出答案：2
        2. 可以简要说明这是基本的算术运算

        不需要过度复杂化，保持简洁明了。

        ====================完整回复====================

        1+1等于**2**。

        这是最基本的算术运算，两个单位相加得到两个单位。
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
          model: "kimi/kimi-k3",
          messages,
          extra_body: { reasoning_effort: "max" },
        });

        const msg = response.choices[0].message;
        if (msg.reasoning_content) {
          console.log("\n" + "=".repeat(20) + "思考过程" + "=".repeat(20) + "\n");
          console.log(msg.reasoning_content || "");
        }
        console.log("\n" + "=".repeat(20) + "完整回复" + "=".repeat(20) + "\n");
        console.log(msg.content);
        ```

        **返回结果**

        ```text
        ====================思考过程====================

        用户问了一个简单的数学问题："1+1等于多少？"

        这是一个非常基础的算术问题，答案是2。

        我应该直接、清晰地回答这个问题。虽然用户用中文提问，但答案是一个通用的数学事实。

        回答结构：
        1. 直接给出答案：2
        2. 可以简要说明这是基本的算术运算

        不需要过度复杂化，保持简洁明了。

        ====================完整回复====================

        1+1等于**2**。

        这是最基本的算术运算，两个单位相加得到两个单位。
        ```
      </Tab>

      <Tab title="curl">
        ```bash
        curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
        --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
        --header 'Content-Type: application/json' \
        --data '{
            "model": "kimi/kimi-k3",
            "messages":[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": "1+1等于多少？"
                }
            ],
            "reasoning_effort": "max"
        }'
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

## 多模态调用示例

Kimi 系列模型不仅支持纯文本对话，还具备强大的多模态理解能力。本章节将介绍如何让模型理解图像和视频内容。

<Warning>
  图像/视频文件仅支持通过公网URL传入，不支持 Base64 编码。
</Warning>

### 图像理解

图像理解功能让 Kimi 模型能够识别和分析图像内容。您可以传入单张或多张图像。图像文件的限制请参见[文件限制](#文件限制)。

<Tabs>
  <Tab title="OpenAI兼容">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        from openai import OpenAI

        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        # 单图传入示例（开启思考模式）
        completion = client.chat.completions.create(
          model="kimi/kimi-k2.6",
          messages=[
            {
              "role": "user",
              "content": [
                {"type": "text", "text": "图中描绘的是什么景象?"},
                {
                  "type": "image_url",
                  "image_url": {
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                  }
                }
              ]
            }
          ],
          extra_body={"enable_thinking":True}  # 开启思考模式
        )

        # 输出思考过程
        if hasattr(completion.choices[0].message, 'reasoning_content') and completion.choices[0].message.reasoning_content:
          print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
          print(completion.choices[0].message.reasoning_content)

        # 输出回复内容
        print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
        print(completion.choices[0].message.content)

        # 多图传入示例（开启思考模式，取消注释使用）
        # completion = client.chat.completions.create(
        #     model="kimi/kimi-k2.6",
        #     messages=[
        #         {
        #             "role": "user",
        #             "content": [
        #                 {"type": "text", "text": "这些图描绘了什么内容？"},
        #                 {
        #                     "type": "image_url",
        #                     "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}
        #                 },
        #                 {
        #                     "type": "image_url",
        #                     "image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"}
        #                 }
        #             ]
        #         }
        #     ],
        #     extra_body={"enable_thinking":True}
        # )
        #
        # # 输出思考过程和回复
        # if hasattr(completion.choices[0].message, 'reasoning_content') and completion.choices[0].message.reasoning_content:
        #     print("\n思考过程：\n" + completion.choices[0].message.reasoning_content)
        # print("\n完整回复：\n" + completion.choices[0].message.content)
        ```
      </Tab>

      <Tab title="Node.js">
        ```javascript
        import OpenAI from "openai";
        import process from 'process';

        const openai = new OpenAI({
          apiKey: process.env.DASHSCOPE_API_KEY,
          baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
        });

        // 单图传入示例（开启思考模式）
        const completion = await openai.chat.completions.create({
          model: 'kimi/kimi-k2.6',
          messages: [
            {
              role: 'user',
              content: [
                { type: 'text', text: '图中描绘的是什么景象?' },
                {
                  type: 'image_url',
                  image_url: {
                    url: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg'
                  }
                }
              ]
            }
          ],
          enable_thinking: true  // 开启思考模式
        });

        // 输出思考过程
        if (completion.choices[0].message.reasoning_content) {
          console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');
          console.log(completion.choices[0].message.reasoning_content);
        }

        // 输出回复内容
        console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
        console.log(completion.choices[0].message.content);

        // 多图传入示例（开启思考模式，取消注释使用）
        // const multiCompletion = await openai.chat.completions.create({
        //     model: 'kimi-k2.5',
        //     messages: [
        //         {
        //             role: 'user',
        //             content: [
        //                 { type: 'text', text: '这些图描绘了什么内容？' },
        //                 {
        //                     type: 'image_url',
        //                     image_url: { url: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg' }
        //                 },
        //                 {
        //                     type: 'image_url',
        //                     image_url: { url: 'https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png' }
        //                 }
        //             ]
        //         }
        //     ],
        //     enable_thinking: true
        // });
        //
        // // 输出思考过程和回复
        // if (multiCompletion.choices[0].message.reasoning_content) {
        //     console.log('\n思考过程：\n' + multiCompletion.choices[0].message.reasoning_content);
        // }
        // console.log('\n完整回复：\n' + multiCompletion.choices[0].message.content);
        ```
      </Tab>

      <Tab title="curl">
        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "kimi/kimi-k2.6",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "图中描绘的是什么景象?"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                            }
                        }
                    ]
                }
            ],
            "enable_thinking": true
        }'

        # 多图输入示例（取消注释使用）
        # curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        # -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        # -H "Content-Type: application/json" \
        # -d '{
        #     "model": "kimi/kimi-k2.6",
        #     "messages": [
        #         {
        #             "role": "user",
        #             "content": [
        #                 {
        #                     "type": "text",
        #                     "text": "这些图描绘了什么内容？"
        #                 },
        #                 {
        #                     "type": "image_url",
        #                     "image_url": {
        #                         "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
        #                     }
        #                 },
        #                 {
        #                     "type": "image_url",
        #                     "image_url": {
        #                         "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"
        #                     }
        #                 }
        #             ]
        #         }
        #     ],
        #     "enable_thinking": true
        # }'
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

### 视频理解

视频文件的限制请参见[文件限制](#文件限制)。

<Tabs>
  <Tab title="OpenAI兼容">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        from openai import OpenAI

        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        completion = client.chat.completions.create(
          model="kimi/kimi-k2.6",
          messages=[
            {
              "role": "user",
              "content": [
                # 直接传入视频文件时，请将type的值设置为video_url
                {
                  "type": "video_url",
                  "video_url": {
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                  }
                },
                {
                  "type": "text",
                  "text": "这段视频的内容是什么?"
                }
              ]
            }
          ]
        )

        print(completion.choices[0].message.content)
        ```
      </Tab>

      <Tab title="Node.js">
        ```javascript
        import OpenAI from "openai";

        const openai = new OpenAI({
          apiKey: process.env.DASHSCOPE_API_KEY,
          baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
        });

        async function main() {
          const response = await openai.chat.completions.create({
            model: "kimi/kimi-k2.6",
            messages: [
              {
                role: "user",
                content: [
                  // 直接传入视频文件时，请将type的值设置为video_url
                  {
                    type: "video_url",
                    video_url: {
                      "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    }
                  },
                  {
                    type: "text",
                    text: "这段视频的内容是什么?"
                  }
                ]
              }
            ]
          });

          console.log(response.choices[0].message.content);
        }

        main();
        ```
      </Tab>

      <Tab title="curl">
        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
          -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
          -H 'Content-Type: application/json' \
          -d '{
            "model": "kimi/kimi-k2.6",
            "messages": [
              {
                "role": "user",
                "content": [
                  {
                    "type": "video_url",
                    "video_url": {
                      "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    },
                    "fps":2
                  },
                  {
                    "type": "text",
                    "text": "这段视频的内容是什么?"
                  }
                ]
              }
            ]
          }'
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

### 文件限制

<Tabs>
  <Tab title="图像文件">
    - **图像分辨率：** 建议图像分辨率不超过4k (4096\*2160)
    - **支持的图像格式：** PNG、JPEG、WEBP、GIF
    - **图像大小与图像数量：** 无限制，但需确保请求的文本和图像的大小不超过 100M。
  </Tab>

  <Tab title="视频文件">
    - **视频大小与视频时长：** 无限制，但需确保请求的文本和视频的大小不超过 100M。
    - **视频格式：** MP4、MPEG、MOV、AVI、X-FLV、MPG、WEBM、WMV、3GPP。
    - **视频尺寸：** 无特定限制，建议不超过2K，再高的分辨率只会增加处理时间，也不会对模型理解的效果有提升。
    - **音频理解：** 不支持对视频文件的音频进行理解。
  </Tab>
</Tabs>

## 其它功能

| 模型                            | 流式输出 | Function Call | 思考模式 | 联网搜索 | 上下文缓存 | 工具调用 |
| ----------------------------- | ---- | ------------- | ---- | ---- | ----- | ---- |
| kimi/kimi-k3                  | ✓    | ✓             | ✓    | —    | ✓     | ✓    |
| kimi/kimi-k2.7-code-highspeed | ✓    | ✓             | ✓    | —    | ✓     | ✓    |
| kimi/kimi-k2.7-code           | ✓    | ✓             | ✓    | —    | ✓     | ✓    |
| kimi/kimi-k2.6                | ✓    | ✓             | ✓    | —    | ✓     | ✓    |
| kimi/kimi-k2.5                | ✓    | ✓             | ✓    | —    | ✓     | ✓    |

以上模型支持上下文缓存（隐式缓存，自动开启）：

- kimi/kimi-k3 命中缓存的输入Token按输入价格的10%计费
- kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code 命中缓存的输入Token按输入价格的20.0%计费
- kimi/kimi-k2.6 命中缓存的输入Token按输入价格的16.9%计费
- kimi/kimi-k2.5 命中缓存的输入Token按输入价格的17.5%计费

## 参数默认值

| 模型                            | tool\_choice    | preserve\_thinking | reasoning\_effort | temperature        | top\_p | repetition\_penalty | presence\_penalty | stream\_options |
| ----------------------------- | --------------- | ------------------ | ----------------- | ------------------ | ------ | ------------------- | ----------------- | --------------- |
| kimi/kimi-k3                  | auto            | 默认关闭               | max               | 1                  | 0.95   | 0.0                 | -                 | 仅支持设置为`true`    |
| kimi/kimi-k2.7-code-highspeed | auto            | 默认开启               | -                 | 1.0                | 0.95   | 0.0                 | 0.0               | 仅支持设置为`true`    |
| kimi/kimi-k2.7-code           | auto            | 默认开启               | -                 | 1.0                | 0.95   | 0.0                 | 0.0               | 仅支持设置为`true`    |
| kimi/kimi-k2.6                | 思考模式/非思考模式：auto | 默认关闭               | -                 | 思考模式：1.0；非思考模式：0.6 | 0.95   | 0.0                 | 思考模式/非思考模式：0.0    | 仅支持设置为`true`    |
| kimi/kimi-k2.5                | 思考模式/非思考模式：auto | 默认关闭               | -                 | 思考模式：1.0；非思考模式：0.6 | 0.95   | 0.0                 | 思考模式/非思考模式：0.0    | 仅支持设置为`true`    |

- `stream_options` 仅支持设置为 `true`，`temperature`、`top_p`、`repetition_penalty`、`presence_penalty` 不支持设置为其他值；
- kimi/kimi-k3 支持 `reasoning_effort` 参数，唯一支持值为 `max`。
- 在思考模式下，使用 Kimi 模型进行工具调用时：必须在每轮 assistant 消息中保留 `reasoning_content` 字段；对于 `tool_choice` 参数，`kimi/kimi-k3` 支持 `auto`/`none`/`required` 三档，其他模型不支持 `required`，传入会报错。`kimi/kimi-k3` 支持动态加载工具，详细用法请参见[动态加载工具](https://platform.kimi.com/docs/guide/use-dynamic-tool-loading)。
- "-"表示没有默认值，也不支持设置。

## 模型列表与计费

模型上下文长度与价格信息请参见[千问AI平台控制台](https://www.qianwenai.com/models)。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

## 错误码

如果执行报错，请参见错误码文档进行解决。
