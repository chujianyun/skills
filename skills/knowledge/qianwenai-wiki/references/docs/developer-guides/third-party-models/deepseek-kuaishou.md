> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# DeepSeek-快手万擎

> 本文档介绍如何在千问AI平台平台调用快手万擎直供的 DeepSeek 系列模型推理服务。

## 服务开通

1. 前往[千问AI平台控制台](https://www.qianwenai.com/models)，搜索 vanchin/deepseek，找到 DeepSeek 模型卡片，单击立即开通；
2. 在弹窗内确认开通及授权。

完成以上步骤即可调用快手万擎提供的 DeepSeek 模型服务。

## 快速开始

API 使用前提：已开通服务并完成 API Key 配置。如果通过 SDK 调用，需要安装对应 SDK。

以下以 vanchin/deepseek-v4-pro 为例，展示如何通过 OpenAI 兼容方式开启思考模式进行流式输出。

<Tabs>
  <Tab title="Python">
    ### 示例代码

    ```python
    import os
    from openai import OpenAI

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
      model="vanchin/deepseek-v4-pro",
      messages=[{"role": "user", "content": "你是谁"}],
      stream=True,
      extra_body={"enable_thinking": True},
    )

    reasoning_content = ""  # 完整思考过程
    answer_content = ""     # 完整回复
    is_answering = False    # 是否进入回复阶段

    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

    for chunk in completion:
      if chunk.choices:
        delta = chunk.choices[0].delta
        # 只收集思考内容
        if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
          if not is_answering:
            print(delta.reasoning_content, end="", flush=True)
          reasoning_content += delta.reasoning_content
        # 收到content，开始进行回复
        if hasattr(delta, "content") and delta.content:
          if not is_answering:
            print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
            is_answering = True
          print(delta.content, end="", flush=True)
          answer_content += delta.content
    ```

    ### 返回结果

    ```text
    ====================思考过程====================

    嗯，用户问了一个简单的自我介绍问题。这是一个常见的开场白，不需要复杂拆解。

    直接说明身份和功能就行，保持友好热情的语气。可以用公司背景增加可信度，再简要列举核心能力让用户快速了解价值。

    结尾加上开放式的服务邀请，鼓励用户继续互动。不需要额外解释或延伸信息，避免让回答显得冗长。

    ====================完整回复====================

    你好！我是DeepSeek，由深度求索公司创造的AI助手。我是一个纯文本模型，擅长回答各种问题、协助分析、写作、编程等等。有什么我可以帮助你的吗？
    ```
  </Tab>

  <Tab title="Node.js">
    ### 示例代码

    ```javascript
    import OpenAI from "openai";
    import process from 'process';

    // 初始化OpenAI客户端
    const openai = new OpenAI({
      // 如果没有配置环境变量，请用千问AI平台API Key替换：apiKey: "sk-xxx"
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    });

    let reasoningContent = ''; // 完整思考过程
    let answerContent = ''; // 完整回复
    let isAnswering = false; // 是否进入回复阶段

    async function main() {
      const messages = [{ role: 'user', content: '你是谁' }];

      const stream = await openai.chat.completions.create({
        model: 'vanchin/deepseek-v4-pro',
        messages,
        stream: true,
        enable_thinking: true,
      });

      console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

      for await (const chunk of stream) {
        if (chunk.choices?.length) {
          const delta = chunk.choices[0].delta;
          // 只收集思考内容
          if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
            if (!isAnswering) {
              process.stdout.write(delta.reasoning_content);
            }
            reasoningContent += delta.reasoning_content;
          }

          // 收到content，开始进行回复
          if (delta.content !== undefined && delta.content) {
            if (!isAnswering) {
              console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
              isAnswering = true;
            }
            process.stdout.write(delta.content);
            answerContent += delta.content;
          }
        }
      }
    }

    main();
    ```

    ### 返回结果

    ```text
    ====================思考过程====================

    嗯，用户问了一个简单的自我介绍问题。这是一个常见的开场白，不需要复杂拆解。

    直接说明身份和功能就行，保持友好热情的语气。可以用公司背景增加可信度，再简要列举核心能力让用户快速了解价值。

    结尾加上开放式的服务邀请，鼓励用户继续互动。不需要额外解释或延伸信息，避免让回答显得冗长。

    ====================完整回复====================

    你好！我是DeepSeek，由深度求索公司创造的AI助手。我是一个纯文本模型，擅长回答各种问题、协助分析、写作、编程等等。有什么我可以帮助你的吗？
    ```
  </Tab>

  <Tab title="HTTP">
    ### 示例代码

    ```bash
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "vanchin/deepseek-v4-pro",
        "enable_thinking": true,
        "messages": [
            {
                "role": "user",
                "content": "你是谁"
            }
        ]
    }'
    ```

    ### 返回结果

    ```json
    {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": "你好！我是DeepSeek，由深度求索公司创造的AI助手。我是一个纯文本模型，擅长回答各种问题、协助分析、写作、编程等等。有什么我可以帮助你的吗？",
                    "reasoning_content": "嗯，用户问了一个简单的自我介绍问题。这是一个常见的开场白，不需要复杂拆解。\n\n直接说明身份和功能就行，保持友好热情的语气。可以用公司背景增加可信度，再简要列举核心能力让用户快速了解价值。\n\n结尾加上开放式的服务邀请，鼓励用户继续互动。不需要额外解释或延伸信息，避免让回答显得冗长。",
                    "role": "assistant"
                }
            }
        ],
        "created": 1775139549,
        "id": "as-j8iwhei6hm",
        "model": "vanchin/deepseek-v4-pro",
        "object": "chat.completion",
        "usage": {
            "completion_tokens": 213,
            "completion_tokens_details": {
                "reasoning_tokens": 75
            },
            "prompt_tokens": 11,
            "total_tokens": 224
        }
    }
    ```
  </Tab>
</Tabs>

## 推理强度（reasoning\_effort）

deepseek-v4-pro 和 deepseek-v4-flash 默认开启思考模式。通过 `reasoning_effort` 参数可以调整推理强度，可选值为 `high` 和 `max`，默认为 `high`。

<Note>
  设为 `low` 或 `medium` 时会映射为 `high`，设为 `xhigh` 时会映射为 `max`。
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
      model="vanchin/deepseek-v4-pro",
      messages=[{"role": "user", "content": "9.9和9.11哪个大"}],
      reasoning_effort="high",
    )

    print(completion.choices[0].message.content)
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";

    const openai = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    });

    const completion = await openai.chat.completions.create({
      model: "vanchin/deepseek-v4-pro",
      messages: [{ role: "user", content: "9.9和9.11哪个大" }],
      reasoning_effort: "high",
    });

    console.log(completion.choices[0].message.content);
    ```
  </Tab>

  <Tab title="HTTP">
    ```bash
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "vanchin/deepseek-v4-pro",
        "messages": [{"role": "user", "content": "9.9和9.11哪个大"}],
        "reasoning_effort": "high"
    }'
    ```
  </Tab>
</Tabs>

## 文字提取

### 示例代码

以下展示如何通过 OpenAI 兼容方式，输入图像URL调用 vanchin/deepseek-ocr 模型进行文字提取。

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
      model="vanchin/deepseek-ocr",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "image_url",
              "image_url": {
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg",
                "detail": "high",
              },
            },
            {
              "type": "text",
              "text": "Read all the text in the image.",
            },
          ],
        }
      ],
    )

    print(completion.choices[0].message.content)
    ```

    #### 返回结果

    ```text
    如果您使用Linux环境下的系统管理员，那么学会编写shell脚本将让你受益匪浅。本书并未细述安装Linux系统的每个步骤，但只要系统已安装好Linux并能运行起来，你就可以开始考虑如何让一些日常的系统管理任务实现自动化。这时shell脚本编程就能发挥作用了，这也正是本书的作用所在。本书将演示如何使用shell脚本来自动处理系统管理任务，包括从监测系统统计数据和数据文件到为你的老炼成报表。

    如果您是采用Linux爱好者，同样能从本书中获益。现今，用户很容易在诸多部件堆积而成的图形环境中迷失。大多数桌面Linux发行版都尽量向一般用户隐藏系统的内部细节。但有时你确实需要知道内部发生了什么。本书将告诉你如何启动Linux命令行以及接下来要做什么。通常，如果是执行一些简单任务（比scf文件管理），在命令行下操作要比在华丽的图形界面下方方便得多。在命令行下有大量的命令可供使用，本书将会展示如何使用它们。
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

    async function main() {
      const completion = await openai.chat.completions.create({
        model: 'vanchin/deepseek-ocr',
        messages: [
          {
            role: 'user',
            content: [
              {
                type: 'image_url',
                image_url: {
                  url: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg',
                  detail: 'high',
                },
              },
              {
                type: 'text',
                text: 'Read all the text in the image.',
              },
            ],
          },
        ],
      });

      console.log(completion.choices[0].message.content);
    }

    main();
    ```

    #### 返回结果

    ```text
    如果您使用Linux环境下的系统管理员，那么学会编写shell脚本将让你受益匪浅。本书并未细述安装Linux系统的每个步骤，但只要系统已安装好Linux并能运行起来，你就可以开始考虑如何让一些日常的系统管理任务实现自动化。这时shell脚本编程就能发挥作用了，这也正是本书的作用所在。本书将演示如何使用shell脚本来自动处理系统管理任务，包括从监测系统统计数据和数据文件到为你的老炼成报表。

    如果您是采用Linux爱好者，同样能从本书中获益。现今，用户很容易在诸多部件堆积而成的图形环境中迷失。大多数桌面Linux发行版都尽量向一般用户隐藏系统的内部细节。但有时你确实需要知道内部发生了什么。本书将告诉你如何启动Linux命令行以及接下来要做什么。通常，如果是执行一些简单任务（比scf文件管理），在命令行下操作要比在华丽的图形界面下方方便得多。在命令行下有大量的命令可供使用，本书将会展示如何使用它们。
    ```
  </Tab>

  <Tab title="HTTP">
    ```bash
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "vanchin/deepseek-ocr",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/ctdzex/biaozhun.jpg",
                            "detail": "high"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Read all the text in the image."
                    }
                ]
            }
        ]
    }'
    ```

    #### 返回结果

    ```json
    {
        "choices": [
            {
                "finish_reason": "stop",
                "index": 0,
                "message": {
                    "content": " 如果您使用Linux环境下的系统管理员，那么学会编写shell脚本将让你受益匪浅。本书并未细述安装Linux系统的每个步骤，但只要系统已安装好Linux并能运行起来，你就可以开始考虑如何让一些日常的系统管理任务实现自动化。这时shell脚本编程就能发挥作用了，这也正是本书的作用所在。本书将演示如何使用shell脚本来自动处理系统管理任务，包括从监测系统统计数据和数据文件到为你的老炼成报表。\n\n如果您是采用Linux爱好者，同样能从本书中获益。现今，用户很容易在诸多部件堆积而成的图形环境中迷失。大多数桌面Linux发行版都尽量向一般用户隐藏系统的内部细节。但有时你确实需要知道内部发生了什么。本书将告诉你如何启动Linux命令行以及接下来要做什么。通常，如果是执行一些简单任务（比scf文件管理），在命令行下操作要比在华丽的图形界面下方方便得多。在命令行下有大量的命令可供使用，本书将会展示如何使用它们。",
                    "role": "assistant"
                }
            }
        ],
        "created": 1775181785,
        "id": "defa065808104e4a880272f86543f961",
        "model": "vanchin/deepseek-ocr",
        "object": "chat.completion",
        "usage": {
            "completion_tokens": 198,
            "prompt_tokens": 498,
            "reasoning_tokens": 0,
            "total_tokens": 696
        }
    }
    ```
  </Tab>
</Tabs>

### 文件传入方式

- 公网 URL：一个公网可访问的图像地址，支持 HTTP 或 HTTPS 协议。
- Base64 编码：将图像文件转换为 Base64 编码字符串。

### 图像限制

图像的大小、分辨率、格式及数量均无硬性限制，实际处理能力取决于引擎资源。建议合理控制单次请求的数据量，以获得最佳响应速度。

## 其它功能

| 模型                             | 流式输出 | 异步调用 | Function Call | 联网搜索 | 系统消息 | 思考模式 | 上下文缓存 |
| ------------------------------ | ---- | ---- | ------------- | ---- | ---- | ---- | ----- |
| vanchin/deepseek-v4-pro        | -    | -    | -             | -    | -    | -    | -     |
| vanchin/deepseek-v3.2-think    | -    | -    | -             | -    | -    | -    | -     |
| vanchin/deepseek-v3.1-terminus | -    | -    | -             | -    | -    | -    | -     |
| vanchin/deepseek-r1            | -    | -    | -             | -    | -    | -    | -     |
| vanchin/deepseek-v3            | -    | -    | -             | -    | -    | -    | -     |
| vanchin/deepseek-ocr           | -    | -    | -             | -    | -    | -    | -     |

<Note>
  由于功能支持情况依赖于 conref 引用内容（无法本地解析），请参考千问AI平台控制台获取各模型的具体功能支持详情。
</Note>

vanchin/deepseek-v4-pro 不支持以下参数：`repetition_penalty`、`preserve_thinking`、`thinking_budget`、`tool_stream`、`enable_code_interpreter`、`seed`、`logprobs`、`top_logprobs`、`enable_search`、`search_options`、`skill`。

支持的参数中，部分参数取值范围与千问AI平台部署版本不一致：

| 参数  | 千问AI平台   | DeepSeek-V4-Pro |
| --- | -------- | --------------- |
| `n` | 取值范围 1-4 | 思考模式下仅支持取值为 1   |

- 除 vanchin/deepseek-ocr 外，其他模型均支持上下文缓存（隐式缓存，自动开启），缓存命中时的输入价格折扣为：
  - vanchin/deepseek-v4-pro：按输入价格的 8.33% 计费
  - vanchin/deepseek-v3.2-think：按输入价格的 10% 计费
  - vanchin/deepseek-v3.1-terminus、vanchin/deepseek-r1、vanchin/deepseek-v3：按输入价格的 40% 计费

## 参数默认值

| 模型                             | temperature | top\_p | enable\_thinking | detail                   |
| ------------------------------ | ----------- | ------ | ---------------- | ------------------------ |
| vanchin/deepseek-v4-pro        | 0.6         | 0.95   | true             | -                        |
| vanchin/deepseek-v3.2-think    | 0.6         | 0.95   | false            | -                        |
| vanchin/deepseek-v3.1-terminus | 0.7         | 0.95   | false            | -                        |
| vanchin/deepseek-r1            | 1.0         | 0.8    | -（仅支持思考模式）       | -                        |
| vanchin/deepseek-v3            | 1.0         | 1.0    | -（不支持思考模式）       | -                        |
| vanchin/deepseek-ocr           | 1.0         | 1.0    | -（不支持思考模式）       | auto（可取值为：auto、high、low） |

## 模型列表与计费

vanchin/deepseek-v4-pro 模型兼顾高计算效率与卓越推理能力，推荐使用。若用于文字识别任务，可使用快手万擎提供的deepseek-ocr 模型。

模型上下文长度与价格信息请参见[千问AI平台控制台](https://www.qianwenai.com/models)。

按照模型的输入与输出 Token 数量计费。

## 错误码

如果模型调用失败并返回报错信息，请参见错误码进行解决。
