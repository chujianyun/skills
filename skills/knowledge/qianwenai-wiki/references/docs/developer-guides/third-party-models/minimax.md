> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# MiniMax-千问AI平台

> 本文档介绍如何调用千问AI平台部署的 MiniMax 模型推理服务。

<Warning>
  MiniMax-M2.1 将于**2026年10月10日**下架。推荐转用：qwen3.7-plus、qwen3.8-max、qwen3.7-max、qwen3.7-flash。
</Warning>

## 快速开始

API 使用前提：已开通千问AI平台服务并完成 API Key 配置。如果通过 SDK 调用，需要安装对应 SDK。

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
          model="MiniMax-M2.5",
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

        用户用中文问"你是谁"，意思是"你是谁？"或"Who are you?"

        我应该用中文回复，介绍自己是一个AI助手。
        ====================完整回复====================

        你好！我是 MiniMax-M2.5，一个AI助手。我可以帮助你回答问题、提供信息、进行对话等。有什么我可以帮你的吗？
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
            model: 'MiniMax-M2.5',
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

        用户用中文问"你是谁"，意思是"你是谁？"或"Who are you?"

        我应该用中文回复，介绍自己是一个AI助手。
        ====================完整回复====================

        你好！我是 MiniMax-M2.5，一个AI助手。我可以帮助你回答问题、提供信息、进行对话等。有什么我可以帮你的吗？
        ```
      </Tab>

      <Tab title="HTTP">
        ### 示例代码

        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "MiniMax-M2.5",
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
                        "content": "你好！我是 MiniMax-M2.5，一个由 MiniMax 公司开发的 AI 助手。我可以帮助你回答问题、提供信息、进行对话，以及完成各种文字相关的任务。有什么我可以帮助你的吗？",
                        "reasoning_content": "用户用中文问\"你是谁\"，意思是\"你是谁？\"或\"Who are you?\"\n\n我应该用中文回复，介绍自己。",
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
                "completion_tokens": 72,
                "total_tokens": 112,
                "completion_tokens_details": {
                    "reasoning_tokens": 26
                },
                "prompt_tokens_details": {
                    "cached_tokens": 0
                }
            },
            "created": 1771944590,
            "system_fingerprint": null,
            "model": "MiniMax-M2.5",
            "id": "chatcmpl-b1277a9c-52da-9de7-988a-d5c063d83xxx"
        }
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
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
          model="MiniMax-M2.5",
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

        用户用中文问"你是谁"，意思是"你是谁？"或"Who are you?"

        我应该用中文回复，介绍自己是一个AI助手。
        ====================完整回复====================

        你好！我是 MiniMax-M2.5，一个AI助手。我可以帮助你回答问题、提供信息、进行对话等。有什么我可以帮你的吗？
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
                .model("MiniMax-M2.5")
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

        用户用中文问"你是谁"，意思是"你是谁？"或"Who are you?"

        我应该用中文回复，介绍自己是一个AI助手。
        ====================完整回复====================

        你好！我是 MiniMax-M2.5，一个AI助手。我可以帮助你回答问题、提供信息、进行对话等。有什么我可以帮你的吗？
        ```
      </Tab>

      <Tab title="HTTP">
        ### 示例代码

        ```bash
        curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "MiniMax-M2.5",
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
                            "content": "你好！我是 MiniMax-M2.5，由 MiniMax 公司开发的 AI 助手。我可以帮助你回答问题、提供信息、进行对话等。有什么我可以帮你的吗？",
                            "reasoning_content": "用户用中文问\"你是谁？\"，意思是\"Who are you?\"\n\n我应该用中文回答，介绍自己。我应该说明我是MiniMax-M2.5，由MiniMax公司开发的AI助手。",
                            "role": "assistant"
                        }
                    }
                ]
            },
            "usage": {
                "input_tokens": 41,
                "output_tokens": 79,
                "output_tokens_details": {
                    "reasoning_tokens": 39
                },
                "prompt_tokens_details": {
                    "cached_tokens": 0
                },
                "total_tokens": 120
            },
            "request_id": "1bbd770e-564a-4601-83fc-3bf639423xxx"
        }
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Anthropic兼容">
    <Tabs>
      <Tab title="Python">
        ### 示例代码

        ```python
        import anthropic
        import os

        client = anthropic.Anthropic(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/apps/anthropic",
        )

        message = client.messages.create(
          model="MiniMax-M2.5",
          max_tokens=1024,
          messages=[
            {"role": "user", "content": "你是谁"}
          ],
          stream=True,
        )

        for event in message:
          if event.type == "content_block_delta":
            if hasattr(event.delta, "thinking"):
              print(event.delta.thinking, end="", flush=True)
            if hasattr(event.delta, "text"):
              print(event.delta.text, end="", flush=True)
        ```
      </Tab>

      <Tab title="HTTP">
        ### 示例代码

        ```bash
        curl -X POST https://dashscope.aliyuncs.com/apps/anthropic/v1/messages \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -H "anthropic-version: 2023-06-01" \
        -d '{
            "model": "MiniMax-M2.5",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": "你是谁"
                }
            ]
        }'
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

## 其它功能

| 模型           | 联网搜索 | 文件解析 | Function Call | Tool Use | 结构化输出 | 异步调用 | 上下文缓存      |
| ------------ | ---- | ---- | ------------- | -------- | ----- | ---- | ---------- |
| MiniMax-M2.5 | ✓    | ✓    | ✓             | —        | ✓     | —    | ✓（仅支持隐式缓存） |
| MiniMax-M2.1 | ✓    | ✓    | ✓             | —        | ✓     | —    | —          |

## 参数默认值

| 模型           | temperature | top\_p | presence\_penalty |
| ------------ | ----------- | ------ | ----------------- |
| MiniMax-M2.5 | 1.0         | 0.95   | 0.0               |
| MiniMax-M2.1 | 1.0         | 0.95   | 0.0               |

## 模型列表与计费

MiniMax-M2.5 模型擅长编程、办公、文本摘要等任务，且输出速度快，推荐使用。

模型上下文长度与价格信息请参见[千问AI平台控制台](https://www.qianwenai.com/models)。

按照模型的输入与输出 Token 数量计费。

## 错误码

如果模型调用失败并返回报错信息，请参见错误码文档进行解决。
