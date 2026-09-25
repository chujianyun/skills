> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# GLM-千问AI平台

> 通过API调用 GLM 系列模型进行对话。

<Warning>
  glm-4.6、glm-4.7 将于**2026年10月10日**下架。推荐转用：qwen3.7-plus、qwen3.8-max、qwen3.7-max、qwen3.7-flash。
</Warning>

## 快速开始

glm-5.2 和 glm-5.2-fast-preview 是 GLM 系列最新模型，上下文长度 1M，支持通过`enable_thinking`参数设置思考与非思考模式。运行以下代码快速调用思考模式的 glm-5.2 模型。

需要已获取API Key并完成环境配置。如果通过SDK调用，需要安装 OpenAI 或 DashScope SDK。

<Tabs>
  <Tab title="OpenAI兼容">
    <Note>
      `enable_thinking`非 OpenAI 标准参数，OpenAI Python SDK 通过 `extra_body`传入，Node.js SDK 作为顶层参数传入。
    </Note>

    <Tabs>
      <Tab title="Python">
        ### 示例代码

        ```python
        from openai import OpenAI
        import os

        # 初始化OpenAI客户端
        client = OpenAI(
          # 如果没有配置环境变量，请用千问AI平台API Key替换：api_key="sk-xxx"
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        messages = [{"role": "user", "content": "你是谁"}]
        completion = client.chat.completions.create(
          model="glm-5.2",
          messages=messages,
          # 通过 extra_body 设置 enable_thinking 开启思考模式
          extra_body={"enable_thinking": True},
          stream=True,
          stream_options={
            "include_usage": True
          },
        )

        reasoning_content = ""  # 完整思考过程
        answer_content = ""  # 完整回复
        is_answering = False  # 是否进入回复阶段
        print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

        for chunk in completion:
          if not chunk.choices:
            print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
            print(chunk.usage)
            continue

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

        让我仔细思考用户提出的这个看似简单但实际上很有深度的问题。

        从语言特点来看，用户使用的是中文，这意味着我应该用中文来回应。这是一个最基础的自我介绍问题，但背后可能包含着多层次的含义。

        首先需要明确的是，作为一个语言模型，我应该诚实地说明自己的身份和本质。我既不是人类，也不具备真正的情感意识，而是一个由深度学习技术训练的AI助手。这是最基本的事实。

        其次，考虑到用户可能的需求场景，他们或许想了解：
        1. 我能提供什么样的服务
        2. 我的专业领域是什么
        3. 我的局限性在哪里
        4. 如何与我更好地互动

        在回答中，我应该既表达友好和开放的态度，又保持专业和准确。要说明自己擅长的主要领域，比如知识问答、写作辅助、创意支持等，但同时也要坦诚地指出自己的局限性，比如缺乏真实的情感体验。

        此外，为了让回答更加完整，我还应该表达出愿意帮助用户解决问题的积极态度。可以适当引导用户提出更具体的问题，这样可以更好地展现自己的能力。

        考虑到这是一个开放式的开场白，回答时既要简洁明了，又要包含足够的信息量，让用户对我的基本情况有一个清晰的认识，同时为后续的对话奠定良好的基础。

        最后，语气应该保持谦逊和专业，既不过于技术化，也不显得过分随意，让用户感到舒适和自然。
        ====================完整回复====================

        我是智谱AI训练的GLM大语言模型，旨在为用户提供信息和帮助解决问题。我被设计用来理解和生成人类语言，可以回答问题、提供解释或参与各类话题讨论。

        我不会存储您的个人数据，我们的对话是匿名的。有什么我能帮您了解或探讨的话题吗？
        ====================Token 消耗====================

        CompletionUsage(completion_tokens=344, prompt_tokens=7, total_tokens=351, completion_tokens_details=None, prompt_tokens_details=None)
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
          try {
            const messages = [{ role: 'user', content: '你是谁' }];

            const stream = await openai.chat.completions.create({
              model: 'glm-5.2',
              messages,
              // 注意：在 Node.js SDK，enable_thinking 这样的非标准参数作为顶层属性传递，无需放在 extra_body 中
              enable_thinking: true,
              stream: true,
              stream_options: {
                include_usage: true
              },
            });

            console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');

            for await (const chunk of stream) {
              if (!chunk.choices?.length) {
                console.log('\n' + '='.repeat(20) + 'Token 消耗' + '='.repeat(20) + '\n');
                console.log(chunk.usage);
                continue;
              }

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
          } catch (error) {
            console.error('Error:', error);
          }
        }

        main();
        ```

        ### 返回结果

        ```text
        ====================思考过程====================

        让我仔细思考用户的问题"你是谁"。这需要从多个角度来分析和回应。

        首先，这是一个基础的身份认知问题。作为GLM大语言模型，需要准确表达自己的身份定位。应该清晰地说明自己是由智谱AI开发的AI助手。

        其次，思考用户提出这个问题的可能意图。他们可能是初次接触，想了解基本功能；也可能想确认是否能提供特定帮助；或者只是想测试回应方式。因此需要给出一个开放且友好的回答。

        还要考虑回答的完整性。除了身份介绍，也应该简要说明主要功能，如问答、创作、分析等，让用户了解可以如何使用这个助手。

        最后，要确保语气友好亲和，表达出乐于帮助的态度。可以用"很高兴为您服务"这样的表达，让用户感受到交流的温暖。

        基于这些思考，可以组织一个简洁明了的回答，既能回答用户问题，又能引导后续交流。
        ====================完整回复====================

        我是GLM，由智谱AI训练的大语言模型。我通过大规模文本数据训练，能够理解和生成人类语言，帮助用户回答问题、提供信息和进行对话交流。

        我会持续学习和改进，以提供更好的服务。很高兴能为您解答问题或提供帮助！有什么我能为您做的吗？
        ====================Token 消耗====================

        { prompt_tokens: 7, completion_tokens: 248, total_tokens: 255 }
        ```
      </Tab>

      <Tab title="HTTP">
        ### 示例代码

        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "glm-5.2",
            "messages": [
                {
                    "role": "user",
                    "content": "你是谁"
                }
            ],
            "stream": true,
            "stream_options": {
                "include_usage": true
            },
            "enable_thinking": true
        }'
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
          model="glm-5.2",
          messages=messages,
          result_format="message",  # 设置结果格式为 message
          enable_thinking=True,     # 开启思考模式
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
          if "reasoning_content" in message:
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

        print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
        print(chunk.usage)
        ```

        ### 返回结果

        ```text
        ====================思考过程====================

        让我仔细思考用户提出的"你是谁"这个问题。首先需要分析用户提问的意图，这可能是初次接触时的好奇，也可能是想了解我的具体功能和能力。

        从专业角度，我应该清晰地表达自己的身份 - 作为一个GLM大语言模型，需要说明自己的基本定位和主要功能。要避免过于技术化的表述，而是用通俗易懂的方式解释。

        同时，也要考虑到用户可能关心的一些实际问题，比如隐私保护、数据安全等。这些都是用户在使用AI服务时非常关注的点。

        另外，为了展现专业性和友好度，可以在介绍的基础上主动引导对话方向，询问用户是否需要特定的帮助。这样既能让用户更好地了解我，也能为后续对话做好铺垫。

        最后，要确保回答简洁明了，重点突出，让用户快速理解我的身份和用途。这样的回答既能满足用户的好奇心，又能展现专业性和服务意识。
        ====================完整回复====================

        我是智谱AI开发的GLM大语言模型，旨在通过自然语言处理技术为用户提供信息和帮助。我通过大规模文本数据训练，能够理解和生成人类语言，回答问题、提供知识支持和参与对话。

        我的设计目标是成为有用的AI助手，同时确保用户隐私和数据安全。我不存储用户的个人信息，并且会持续学习和改进以提供更优质的服务。

        有什么我能帮您解答的问题或需要协助的任务吗？
        ====================Token 消耗====================

        {"input_tokens": 8, "output_tokens": 269, "total_tokens": 277}
        ```
      </Tab>

      <Tab title="Java">
        ### 示例代码

        <Warning>
          DashScope Java SDK 版本需要不低于2.19.4。
        </Warning>

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

        public class Main {
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
              .model("glm-5.2")
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
              System.err.println("An exception occurred: " + e.getMessage());
            }
          }
        }
        ```

        ### 返回结果

        ```text
        ====================思考过程====================
        让我思考一下如何回答用户的问题。首先，这是一个关于身份识别的简单问题，需要清晰直接地回答。

        作为一个大语言模型，我应该准确说明自己的基本身份信息。这包括：
        - 名称：GLM
        - 开发者：智谱AI
        - 主要功能：语言理解和生成

        考虑到用户的提问可能源于初次接触，我需要用通俗易懂的方式介绍自己，避免使用过于技术性的术语。同时，也应该简要说明自己的主要能力，这样可以帮助用户更好地了解如何与我互动。

        我还应该以友好开放的态度表达，欢迎用户提出各种问题，这样可以为后续对话打下良好基础。不过介绍要简洁明了，不需要过于详细，以免给用户造成信息负担。

        最后，为了促进进一步交流，可以主动询问用户是否需要特定帮助，这样能够更好地服务于用户的实际需求。
        ====================完整回复====================
        我是GLM，由智谱AI开发的大语言模型。我通过海量文本数据训练而成，能够理解和生成人类语言，回答问题、提供信息和进行对话。

        我的设计目的是帮助用户解决问题、提供知识和支持各类语言任务。我会不断学习和更新，以提供更准确、有用的回答。

        有什么我能帮您解答或探讨的问题吗？
        ```
      </Tab>

      <Tab title="HTTP">
        ### 示例代码

        ```bash
        curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -H "X-DashScope-SSE: enable" \
        -d '{
            "model": "glm-5.2",
            "input":{
                "messages":[
                    {
                        "role": "user",
                        "content": "你是谁？"
                    }
                ]
            },
            "parameters":{
                "enable_thinking": true,
                "incremental_output": true,
                "result_format": "message"
            }
        }'
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
          model="glm-5.2",
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
            "model": "glm-5.2",
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

## 流式工具调用

glm-5.2、glm-5.2-fast-preview、glm-5.1、glm-5、glm-4.7、glm-4.6 支持`tool_stream`参数（boolean，默认`false`），仅在`stream`为`true`时生效。开启后，Function Calling 返回的 tool\_call 参数（arguments）会以流式增量方式逐步返回，而非等待完整生成后一次性返回。

`stream`与`tool_stream`的组合行为如下：

| **stream** | **tool\_stream** | **tool\_call 返回方式**                    |
| ---------- | ---------------- | -------------------------------------- |
| true       | true             | arguments 以增量方式分多个 chunk 返回            |
| true       | false（默认）        | arguments 在一个 chunk 中完整返回              |
| false      | true/false       | tool\_stream 不生效，arguments 在完整响应中一次性返回 |

<Tabs>
  <Tab title="OpenAI兼容">
    <Tabs>
      <Tab title="Python">
        ### 示例代码

        ```python
        from openai import OpenAI
        import os

        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        tools = [
          {
            "type": "function",
            "function": {
              "name": "get_weather",
              "description": "获取指定城市的天气信息",
              "parameters": {
                "type": "object",
                "properties": {
                  "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
              }
            }
          }
        ]

        messages = [{"role": "user", "content": "北京天气怎么样"}]

        completion = client.chat.completions.create(
          model="glm-5.2",
          tools=tools,
          messages=messages,
          extra_body={
            "tool_stream": True,
          },
          stream=True,
          stream_options={"include_usage": True},
        )

        for chunk in completion:
          if chunk.choices:
            delta = chunk.choices[0].delta
            if hasattr(delta, 'content') and delta.content:
              print(f"[content] {delta.content}")
            if hasattr(delta, 'tool_calls') and delta.tool_calls:
              for tc in delta.tool_calls:
                print(f"[tool_call] id={tc.id}, name={tc.function.name}, args={tc.function.arguments}")
            if chunk.choices[0].finish_reason:
              print(f"[finish_reason] {chunk.choices[0].finish_reason}")
          if not chunk.choices and chunk.usage:
            print(f"[usage] {chunk.usage}")
        ```
      </Tab>

      <Tab title="Node.js">
        ### 示例代码

        ```javascript
        import OpenAI from "openai";
        import process from 'process';

        const openai = new OpenAI({
          apiKey: process.env.DASHSCOPE_API_KEY,
          baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
        });

        const tools = [
          {
            type: "function",
            function: {
              name: "get_weather",
              description: "获取指定城市的天气信息",
              parameters: {
                type: "object",
                properties: {
                  city: { type: "string", description: "城市名称" }
                },
                required: ["city"]
              }
            }
          }
        ];

        async function main() {
          try {
            const stream = await openai.chat.completions.create({
              model: 'glm-5.2',
              messages: [{ role: 'user', content: '北京天气怎么样' }],
              tools: tools,
              tool_stream: true,
              stream: true,
              stream_options: {
                include_usage: true
              },
            });

            for await (const chunk of stream) {
              if (!chunk.choices?.length) {
                if (chunk.usage) {
                  console.log(`[usage] ${JSON.stringify(chunk.usage)}`);
                }
                continue;
              }

              const delta = chunk.choices[0].delta;

              if (delta.content) {
                console.log(`[content] ${delta.content}`);
              }

              if (delta.tool_calls) {
                for (const tc of delta.tool_calls) {
                  console.log(`[tool_call] id=${tc.id}, name=${tc.function.name}, args=${tc.function.arguments}`);
                }
              }

              if (chunk.choices[0].finish_reason) {
                console.log(`[finish_reason] ${chunk.choices[0].finish_reason}`);
              }
            }
          } catch (error) {
            console.error('Error:', error);
          }
        }

        main();
        ```
      </Tab>

      <Tab title="HTTP">
        ### 示例代码

        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "glm-5.2",
            "messages": [
                {
                    "role": "user",
                    "content": "北京天气怎么样"
                }
            ],
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "获取指定城市的天气信息",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "city": {"type": "string", "description": "城市名称"}
                            },
                            "required": ["city"]
                        }
                    }
                }
            ],
            "stream": true,
            "stream_options": {"include_usage": true},
            "tool_stream": true
        }'
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

        tools = [
          {
            "type": "function",
            "function": {
              "name": "get_weather",
              "description": "获取指定城市的天气信息",
              "parameters": {
                "type": "object",
                "properties": {
                  "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
              }
            }
          }
        ]

        messages = [{"role": "user", "content": "北京天气怎么样"}]

        completion = Generation.call(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="glm-5.2",
          messages=messages,
          tools=tools,
          result_format="message",
          stream=True,
          tool_stream=True,
          incremental_output=True,
        )

        for chunk in completion:
          msg = chunk.output.choices[0].message
          if msg.content:
            print(f"[content] {msg.content}")
          if "tool_calls" in msg and msg.tool_calls:
            for tc in msg.tool_calls:
              fn = tc.get("function", {})
              print(f"[tool_call] id={tc.get('id','')}, name={fn.get('name','')}, args={fn.get('arguments','')}")
          finish = chunk.output.choices[0].get("finish_reason", "")
          if finish and finish != "null":
            print(f"[finish_reason] {finish}")
        ```
      </Tab>

      <Tab title="HTTP">
        ### 示例代码

        ```bash
        curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -H "X-DashScope-SSE: enable" \
        -d '{
            "model": "glm-5.2",
            "input": {
                "messages": [
                    {
                        "role": "user",
                        "content": "北京天气怎么样"
                    }
                ]
            },
            "parameters": {
                "tools": [
                    {
                        "type": "function",
                        "function": {
                            "name": "get_weather",
                            "description": "获取指定城市的天气信息",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "city": {"type": "string", "description": "城市名称"}
                                },
                                "required": ["city"]
                            }
                        }
                    }
                ],
                "tool_stream": true,
                "incremental_output": true,
                "result_format": "message"
            }
        }'
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

## reasoning\_effort

glm-5.2、glm-5.2-fast-preview 和 glm-5.1 默认开启思考模式，模型会先输出思考过程（`reasoning_content`），再给出最终回答。通过 `reasoning_effort` 参数可以调整推理强度，取值越高思考越充分。**不同模型支持的可选取值不同**，传入不支持的取值会返回 `invalid_parameter_error` 错误，请按下表选择。

| 模型                   | reasoning\_effort 可选取值                                                                 |
| -------------------- | -------------------------------------------------------------------------------------- |
| glm-5.2              | `none`（不进行推理，`reasoning_tokens`=`0`）、`minimal`、`low`、`medium`、`high`、`xhigh`、`max`（最高） |
| glm-5.2-fast-preview | `none`（不进行推理，`reasoning_tokens`=`0`）、`minimal`、`low`、`medium`、`high`、`xhigh`、`max`（最高） |
| glm-5.1              | `none`、`minimal`、`low`、`medium`、`high`、`xhigh`（最高，不支持 max）                             |
| glm-5                | `none`、`minimal`、`low`、`medium`、`high`、`xhigh`（最高，不支持 max）                             |

<Note>
  如需关闭思考，可在 OpenAI 兼容与 DashScope 方式中传入 `enable_thinking`=`false`，该参数优先级高于 `reasoning_effort`。
</Note>

<Note>
  Anthropic 兼容方式不支持 `reasoning_effort` 参数。如需获取思考内容，请使用 Anthropic 原生 `thinking` 参数：`{"thinking":{"type":"enabled","budget_tokens":1024}}`，开启后响应 `content` 中会返回 `type` 为 `thinking` 的思考块。
</Note>

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
        completion = client.chat.completions.create(
          model="glm-5.2",
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
          model: "glm-5.2",
          messages: [{ role: "user", content: "9.9和9.11哪个大" }],
          reasoning_effort: "high",
        });
        console.log(completion.choices[0].message.content);
        ```
      </Tab>

      <Tab title="curl">
        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "glm-5.2",
          "messages": [{"role": "user", "content": "9.9和9.11哪个大"}],
          "reasoning_effort": "high"
        }'
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    ```python
    import os
    from dashscope import Generation
    response = Generation.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      model="glm-5.2",
      messages=[{"role": "user", "content": "9.9和9.11哪个大"}],
      reasoning_effort="high",
      result_format="message",
    )
    print(response.output.choices[0].message.content)
    ```
  </Tab>
</Tabs>

## clear\_thinking

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
          model="glm-5.2",
          messages=messages,
          extra_body={
            "enable_thinking": True,
            "clear_thinking": True,
          },
        )
        print(completion.usage.prompt_tokens)
        ```
      </Tab>

      <Tab title="curl">
        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "glm-5.2",
          "messages": [
            {"role": "user", "content": "请计算 15 * 23 是多少？"},
            {"role": "assistant", "content": "15 乘以 23 等于 345。", "reasoning_content": "15 * 23 = 345"},
            {"role": "user", "content": "那再加上 55 呢？"},
            {"role": "assistant", "content": "345 加上 55 等于 400。", "reasoning_content": "345 + 55 = 400"},
            {"role": "user", "content": "刚才的中间结果是多少？"}
          ],
          "enable_thinking": true,
          "clear_thinking": true
        }'
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    ```python
    import os
    from dashscope import Generation
    messages = [
      {"role": "user", "content": "请计算 15 * 23 是多少？"},
      {"role": "assistant", "content": "15 乘以 23 等于 345。", "reasoning_content": "15 * 23 = 345"},
      {"role": "user", "content": "那再加上 55 呢？"},
      {"role": "assistant", "content": "345 加上 55 等于 400。", "reasoning_content": "345 + 55 = 400"},
      {"role": "user", "content": "刚才的中间结果是多少？"},
    ]
    response = Generation.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      model="glm-5.2",
      messages=messages,
      result_format="message",
      enable_thinking=True,
      clear_thinking=True,
    )
    print(response.usage.input_tokens)
    ```
  </Tab>
</Tabs>

## 其它功能

| **模型**               | **多轮对话** | **Function Calling** | **联网搜索**  | **异步调用** | **前缀续写** | **上下文缓存**    |
| -------------------- | -------- | -------------------- | --------- | -------- | -------- | ------------ |
| glm-5.2              | ✓        | ✓                    | ✓（仅非思考模式） | —        | —        | ✓（仅支持隐式缓存）   |
| glm-5.2-fast-preview | ✓        | ✓                    | ✓（仅非思考模式） | —        | —        | ✓（仅支持隐式缓存）   |
| glm-5.1              | ✓        | ✓                    | ✓（仅非思考模式） | —        | —        | ✓（支持显式与隐式缓存） |
| glm-5                | ✓        | ✓                    | ✓（仅非思考模式） | —        | —        | ✓（仅支持隐式缓存）   |
| glm-4.7              | ✓        | ✓                    | ✓（仅非思考模式） | —        | —        | ✓（仅支持隐式缓存）   |
| glm-4.6              | ✓        | ✓                    | ✓（仅非思考模式） | —        | —        | ✓（仅支持隐式缓存）   |
| glm-4.5              | ✓        | ✓                    | ✓         | —        | —        | —            |
| glm-4.5-air          | ✓        | ✓                    | ✓         | —        | —        | —            |

## 参数默认值

| **模型**               | **enable\_thinking** | **temperature** | **top\_p** | **top\_k** | **repetition\_penalty** |
| -------------------- | -------------------- | --------------- | ---------- | ---------- | ----------------------- |
| glm-5.2              | true                 | 1.0             | 0.95       | 20         | 1.0                     |
| glm-5.2-fast-preview | true                 | 1.0             | 0.95       | 20         | 1.0                     |
| glm-5.1              | true                 | 1.0             | 0.95       | 20         | 1.0                     |
| glm-5                | true                 | 1.0             | 0.95       | 20         | 1.0                     |
| glm-4.7              | true                 | 1.0             | 0.95       | 20         | 1.0                     |
| glm-4.6              | true                 | 1.0             | 0.95       | 20         | 1.0                     |
| glm-4.5              | true                 | 0.6             | 0.95       | 20         | 1.0                     |
| glm-4.5-air          | true                 | 0.6             | 0.95       | 20         | 1.0                     |

## 注意事项

<Warning>
  云上部署的三方开源模型（如 glm-5.2）与模型官方对超参数的处理逻辑不同：模型官方会对超参数进行阈值校验，超出阈值时回退为默认值；云上部署的处理逻辑是直接透传用户传入的参数值，不做阈值校验。因此，不当设置超参数（如将 `repetition_penalty` 设为 `0.1`）可能导致非预期输出（如循环打印）。建议三方开源模型使用默认超参数值（请参见上方参数默认值表），不建议自定义传入。
</Warning>

## 模型列表与计费

GLM 系列模型是智谱AI专为智能体设计的混合推理模型，提供思考与非思考两种模式。

- glm-5.2：GLM 最新模型，上下文长度 1M，支持 Function Calling、结构化输出及隐式缓存。支持 OpenAI 兼容、DashScope 及 Anthropic 兼容接口调用。
- glm-5.2-fast-preview：glm-5.2模型的快速模式。

模型上下文长度与价格信息请参见千问AI平台控制台。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

## 错误码

如果执行报错，请参见错误码文档进行解决。
