> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# MiniMax-稀宇科技

> 本文档介绍如何在千问AI平台平台调用稀宇科技（简称MiniMax）直供的模型推理服务。

## 服务开通

1. 前往[千问AI平台控制台](https://www.qianwenai.com/models)，搜索 MiniMax，找到 MiniMax 模型卡片，单击立即开通；
2. 在弹窗内确认开通及授权。

完成以上步骤即可调用MiniMax提供的 MiniMax 模型服务。

## 快速开始

API 使用前提：已开通服务并完成API Key配置。如果通过SDK调用，需要安装SDK。

<Tabs>
  <Tab title="OpenAI兼容">
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
          model="MiniMax/MiniMax-M2.7",
          messages=[{"role": "user", "content": "你是谁"}],
          stream=True,
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

        用户问我是谁。根据系统提示，我应该以"MiniMax-M2.7"的身份回应，并且提到我是由MiniMax公司开发的。

        这是一个简单的自我介绍问题，我应该简洁明了地回答。

        ====================完整回复====================

        你好！我是 **MiniMax-M2.7**，由 **MiniMax** 公司开发的AI助手。

        我可以帮助你回答问题、提供信息、进行对话等各种任务。有什么我可以帮助你的吗？
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
            model: 'MiniMax/MiniMax-M2.7',
            messages,
            stream: true,
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

        用户问我是谁。根据系统提示，我应该以"MiniMax-M2.7"的身份回应，并且提到我是由MiniMax公司开发的。

        这是一个简单的自我介绍问题，我应该简洁明了地回答。

        ====================完整回复====================

        你好！我是 **MiniMax-M2.7**，由 **MiniMax** 公司开发的AI助手。

        我可以帮助你回答问题、提供信息、进行对话等各种任务。有什么我可以帮助你的吗？
        ```
      </Tab>

      <Tab title="HTTP">
        ### 示例代码

        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "minimax/minimax-m2.7",
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
                    "message": {
                        "content": "\n\n你好！我是一个AI助手，由MiniMax公司开发。我的名字是MiniMax-M2.7。\n\n我可以帮助你回答问题、提供信息、进行对话、协助写作、分析问题等各种任务。有什么我可以帮助你的吗？",
                        "reasoning_content": "用户用中文问\"你是谁\"，意思是\"你是谁？\"或\"Who are you?\"\n\n我应该用中文回复，介绍我自己是一个AI助手。\n\n让我写一个简洁的自我介绍。",
                        "role": "assistant"
                    },
                    "finish_reason": "stop",
                    "index": 0,
                    "logprobs": null
                }
            ],
            "object": "chat.completion",
            "usage": {
                "prompt_tokens": 40,
                "completion_tokens": 84,
                "total_tokens": 124,
                "completion_tokens_details": {
                    "reasoning_tokens": 36
                }
            },
            "created": 1769161313,
            "system_fingerprint": null,
            "model": "minimax/minimax-m2.7",
            "id": "chatcmpl-30d4de0f-92fe-93d2-a1bf-e8153ae937df"
        }
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    <Warning>
      DashScope暂不支持MiniMax/MiniMax-M2.7，请使用OpenAI兼容方式调用MiniMax/MiniMax-M2.7。
    </Warning>

    <Tabs>
      <Tab title="Python">
        ### 示例代码

        ```python
        import os
        from dashscope import Generation

        # 初始化请求参数
        messages = [{"role": "user", "content": "你是谁？"}]

        completion = Generation.call(
          # 如果没有配置环境变量，请用千问AI平台API Key替换：api_key="sk-xxx"
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="MiniMax/MiniMax-M2.5",
          messages=messages,
          result_format="message",  # 设置结果格式为 message
          stream=True,              # 开启流式输出
          incremental_output=True,  # 开启增量输出
        )

        reasoning_content = ""  # 完整思考过程
        answer_content = ""     # 完整回复
        is_answering = False    # 是否进入回复阶段

        print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

        for chunk in completion:
          message = chunk.output.choices[0].message

          # 只收集思考内容
          if message.reasoning_content:
            if not is_answering:
              print(message.reasoning_content, end="", flush=True)
            reasoning_content += message.reasoning_content

          # 收到 content，开始进行回复
          if message.content:
            if not is_answering:
              print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
              is_answering = True
            print(message.content, end="", flush=True)
            answer_content += message.content
        ```

        ### 返回结果

        ```text
        ====================思考过程====================

        用户问我是谁。根据系统提示，我应该以"MiniMax-M2.1"的身份回应，并且提到我是由MiniMax公司开发的。

        这是一个简单的自我介绍问题，我应该简洁明了地回答。

        ====================完整回复====================

        你好！我是 **MiniMax-M2.1**，由 **MiniMax** 公司开发的AI助手。

        我可以帮助你回答问题、提供信息、进行对话等各种任务。有什么我可以帮助你的吗？
        ```
      </Tab>

      <Tab title="Java">
        ### 示例代码

        ```java
        // dashscope SDK的版本 >= 2.19.4
        import com.alibaba.dashscope.aigc.generation.Generation;
        import com.alibaba.dashscope.aigc.generation.GenerationParam;
        import com.alibaba.dashscope.aigc.generation.GenerationResult;
        import com.alibaba.dashscope.common.Message;
        import com.alibaba.dashscope.common.Role;
        import com.alibaba.dashscope.exception.ApiException;
        import com.alibaba.dashscope.exception.InputRequiredException;
        import com.alibaba.dashscope.exception.NoApiKeyException;
        import io.reactivex.Flowable;
        import java.lang.System;
        import java.util.Arrays;
        import org.slf4j.Logger;
        import org.slf4j.LoggerFactory;

        public class Main {
            private static final Logger logger = LoggerFactory.getLogger(Main.class);
            private static StringBuilder reasoningContent = new StringBuilder();
            private static StringBuilder finalContent = new StringBuilder();
            private static boolean isFirstPrint = true;

            private static void handleGenerationResult(GenerationResult message) {
                String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
                String content = message.getOutput().getChoices().get(0).getMessage().getContent();

                if (reasoning != null && !reasoning.isEmpty()) {
                    reasoningContent.append(reasoning);
                    if (isFirstPrint) {
                        System.out.println("====================思考过程====================");
                        isFirstPrint = false;
                    }
                    System.out.print(reasoning);
                }

                if (content != null && !content.isEmpty()) {
                    finalContent.append(content);
                    if (!isFirstPrint) {
                        System.out.println("\n====================完整回复====================");
                        isFirstPrint = true;
                    }
                    System.out.print(content);
                }
            }
            private static GenerationParam buildGenerationParam(Message userMsg) {
                return GenerationParam.builder()
                        // 若没有配置环境变量，请用千问AI平台API Key将下行替换为：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model("MiniMax/MiniMax-M2.5")
                        .incrementalOutput(true)
                        .resultFormat("message")
                        .messages(Arrays.asList(userMsg))
                        .build();
            }
            public static void streamCallWithMessage(Generation gen, Message userMsg)
                    throws NoApiKeyException, ApiException, InputRequiredException {
                GenerationParam param = buildGenerationParam(userMsg);
                Flowable<GenerationResult> result = gen.streamCall(param);
                result.blockingForEach(message -> handleGenerationResult(message));
            }

            public static void main(String[] args) {
                try {
                    Generation gen = new Generation();
                    Message userMsg = Message.builder().role(Role.USER.getValue()).content("你是谁？").build();
                    streamCallWithMessage(gen, userMsg);
                } catch (ApiException | NoApiKeyException | InputRequiredException e) {
                    logger.error("An exception occurred: {}", e.getMessage());
                }
                System.exit(0);
            }
        }
        ```

        ### 返回结果

        ```text
        ====================思考过程====================

        用户问我是谁。根据系统提示，我应该以"MiniMax-M2.1"的身份回应，并且提到我是由MiniMax公司开发的。

        这是一个简单的自我介绍问题，我应该简洁明了地回答。

        ====================完整回复====================

        你好！我是 **MiniMax-M2.1**，由 **MiniMax** 公司开发的AI助手。

        我可以帮助你回答问题、提供信息、进行对话等各种任务。有什么我可以帮助你的吗？
        ```
      </Tab>

      <Tab title="HTTP">
        ### 示例代码

        ```bash
        curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "minimax/minimax-m2.5",
            "input":{
                "messages":[
                    {
                        "role": "user",
                        "content": "你是谁？"
                    }
                ]
            },
            "parameters": {
                "result_format": "message"
            }
        }'
        ```

        ### 返回结果

        ```json
        {
            "output": {
                "choices": [
                    {
                        "finish_reason": "stop",
                        "message": {
                            "content": "用户用中文问\"你是谁？\"，这是一个简单的自我介绍问题。\n\n我需要用中文回答，介绍我是谁。根据系统提示，我是MiniMax-M2.1，由MiniMax构建的AI助手。\n\n让我简洁明了地回答这个问题。\n</think>\n\n你好！我是 MiniMax-M2.1，一个由 MiniMax 公司开发的 AI 助手。我可以帮助你回答问题、提供信息、进行对话等各种任务。有什么我可以帮你的吗？",
                            "reasoning_content": "",
                            "role": "assistant"
                        }
                    }
                ]
            },
            "usage": {
                "input_tokens": 41,
                "output_tokens": 87,
                "total_tokens": 128
            },
            "request_id": "0fba0c78-bda8-948e-a748-c5354a7a95cd"
        }
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

## 多模态调用示例

MiniMax/MiniMax-M3 不仅支持纯文本对话，还具备强大的多模态理解能力。本章节将介绍如何让模型理解图像和视频内容。

<Warning>
  MiniMax-M3 通过 `thinking` 参数控制思考模式，默认为自适应模式（`adaptive`）：

  - **非思考模式**（`thinking.type: "disabled"`）：直接输出结果，不包含推理过程
  - **自适应模式**（`thinking.type: "adaptive"` 或不设置）：模型自主判断是否需要思考，并输出推理过程（`reasoning_content`）
</Warning>

### 图像理解

图像理解功能让 MiniMax-M3 模型能够识别和分析图像内容。您可以传入单张或多张图像。

<Tabs>
  <Tab title="OpenAI兼容">
    <Note>
      `thinking` 非 OpenAI 标准参数，OpenAI Python SDK 通过 `extra_body` 传入，Node.js SDK 中作为顶层参数传入。
    </Note>

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
          model="MiniMax/MiniMax-M3",
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
          extra_body={"thinking": {"type": "adaptive"}}
        )

        if hasattr(completion.choices[0].message, 'reasoning_content') and completion.choices[0].message.reasoning_content:
          print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
          print(completion.choices[0].message.reasoning_content)

        print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
        print(completion.choices[0].message.content)
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

        const completion = await openai.chat.completions.create({
          model: 'MiniMax/MiniMax-M3',
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
          thinking: {"type": "adaptive"}
        });

        if (completion.choices[0].message.reasoning_content) {
          console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');
          console.log(completion.choices[0].message.reasoning_content);
        }

        console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
        console.log(completion.choices[0].message.content);
        ```
      </Tab>

      <Tab title="HTTP">
        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "minimax/minimax-m3",
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
            "thinking": {"type": "adaptive"}
        }'
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

### 视频理解

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
          model="MiniMax/MiniMax-M3",
          messages=[
            {
              "role": "user",
              "content": [
                {
                  "type": "video_url",
                  "video_url": {
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                  },
                  "fps": 2
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
            model: "MiniMax/MiniMax-M3",
            messages: [
              {
                role: "user",
                content: [
                  {
                    type: "video_url",
                    video_url: {
                      "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    },
                    fps: 2
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

      <Tab title="HTTP">
        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
          -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
          -H 'Content-Type: application/json' \
          -d '{
            "model": "minimax/minimax-m3",
            "messages": [
              {
                "role": "user",
                "content": [
                  {
                    "type": "video_url",
                    "video_url": {
                      "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                    },
                    "fps": 2
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
    - **传入方式**：支持通过公网 URL 或 Base64 编码传入。
    - **支持的图像格式**：PNG、JPEG、WEBP、GIF
    - **图像大小**：单张图片不超过 10MB。
  </Tab>

  <Tab title="视频文件">
    - **视频大小与时长**：视频文件不超过 50MB，时长不超过 30 分钟。
    - **视频格式**：MP4、AVI、MOV、MKV。
    - **音频理解**：不支持对视频文件的音频进行理解。
  </Tab>
</Tabs>

## 其它功能

| 模型                   | 流式输出 | 系统消息 | 联网搜索 | 工具调用 | 结构化输出 | 文件提取 | 上下文缓存 |
| -------------------- | ---- | ---- | ---- | ---- | ----- | ---- | ----- |
| MiniMax/MiniMax-M3   | ✓    | ✓    | ✓    | —    | —     | —    | ✓     |
| MiniMax/MiniMax-M2.7 | ✓    | ✓    | ✓    | —    | —     | —    | ✓     |
| MiniMax/MiniMax-M2.5 | ✓    | ✓    | ✓    | —    | —     | —    | ✓     |
| MiniMax/MiniMax-M2.1 | ✓    | ✓    | ✓    | —    | —     | —    | ✓     |

上下文缓存类型为隐式缓存，自动开启，与千问AI平台的隐式缓存服务有以下不同：

- MiniMax/MiniMax-M3、MiniMax/MiniMax-M2.7 命中缓存的输入 Token 折扣为 20%，MiniMax/MiniMax-M2.5、MiniMax/MiniMax-M2.1 折扣为 10%；缓存最少 Token 数为 512（千问AI平台为 256）。
- MiniMax/MiniMax-M3 不支持 `n` 参数（即不支持一次生成多条候选回复），`tool_choice` 仅支持 `none` 和 `auto`。

## 参数默认值

<Note>
  当前不支持修改以下参数。
</Note>

| 模型                   | temperature | top\_p |
| -------------------- | ----------- | ------ |
| MiniMax/MiniMax-M3   | 1.0         | 0.95   |
| MiniMax/MiniMax-M2.7 | 1.0         | 0.9    |
| MiniMax/MiniMax-M2.5 | 1.0         | 0.9    |
| MiniMax/MiniMax-M2.1 | 1.0         | 0.9    |

## 模型列表与计费

MiniMax-M3 为最新多模态推理模型，支持图像和视频理解，推荐使用；MiniMax-M2.7 擅长编程、文本摘要等任务。

模型上下文长度与价格信息请参见[千问AI平台控制台](https://www.qianwenai.com/models)。

按照模型的输入与输出 Token 数量计费。

## 错误码

如果模型调用失败并返回报错信息，请参见错误码文档进行解决。
