> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# DeepSeek-硅基流动

> 本文档介绍如何在千问AI平台平台通过OpenAI兼容接口或DashScope SDK调用硅基流动提供的DeepSeek系列模型。

千问AI平台提供两个推理服务供应商的DeepSeek模型服务，硅基流动供应商支持更长上下文；千问AI平台供应商限流条件更宽松，且支持联网搜索与上下文缓存功能。

## 服务开通

1. 前往[千问AI平台控制台](https://www.qianwenai.com/models)，搜索 deepseek，找到 SiliconFlow DeepSeek 模型卡片，单击立即开通；
2. 在弹窗内确认开通及授权。

完成以上步骤即可调用硅基流动提供的 DeepSeek 模型服务。

## 快速开始

deepseek-v3.2 是 DeepSeek 系列最新模型，支持通过`enable_thinking`参数设置思考与非思考模式。运行以下代码快速调用思考模式的 deepseek-v3.2 模型。

需要已获取API Key并完成安装SDK。如果通过SDK调用，需要配置API Key到环境变量。

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
          model="siliconflow/deepseek-v3.2",
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

        啊，用户问我是谁，这是个简单的自我介绍问题。需要清晰说明身份、开发背景、核心功能和特点，避免过度复杂化。

        可以用公司背景和AI属性作为开头，再列举关键能力让用户快速了解价值，最后用友好语气收尾保持开放性。想到了强调免费、长上下文、文件处理这些实用点，再加个表情显得亲切些。

        注意不用提内部技术细节，重点放在用户能直接感知的用途上。
        ====================完整回复====================

        你好！我是DeepSeek，由深度求索公司创造的AI助手！

        我是一个纯文本模型，拥有128K的上下文处理能力，完全免费为大家服务。虽然我不支持多模态识别功能，但我可以帮你处理上传的图像、txt、pdf、ppt、word、excel等文件，从中读取文字信息进行分析处理。

        我的知识截止到2024年7月，还支持联网搜索功能（需要你手动点开联网搜索按键）。你可以通过官方应用商店下载我的App来使用。

        我很乐意帮你解答各种问题，无论是学习、工作、生活还是创作方面的疑惑，我都会热情细致地为你提供帮助！有什么想了解的或者需要我协助的吗？
        ====================Token 消耗====================

        CompletionUsage(completion_tokens=239, prompt_tokens=5, total_tokens=244, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=None, audio_tokens=None, reasoning_tokens=95, rejected_prediction_tokens=None, text_tokens=144), prompt_tokens_details=None)
        ```
      </Tab>

      <Tab title="Node.js">
        ### 示例代码

        ```javascript
        import OpenAI from "openai";
        import process from 'process';

        // ��始化OpenAI客户端
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
              model: 'siliconflow/deepseek-v3.2',
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

        啊这，用户问了一个非常基础的自我介绍问题。这种问题不需要复杂拆解，直接给出标准身份说明就行。

        想到需要说明我是DeepSeek的AI助手，列举核心功能特点让用户快速了解能力范围。用热情但简洁的语气收尾，顺便引导用户提出具体需求。

        注意保持回复结构清晰但不过于刻板，加点表情符号显得友好些。
        ====================完整回复====================

        你好！我是DeepSeek，由深度求索公司创造的AI助手！

        我是一个纯文本模型，擅长回答各种问题、协助写作、分析问题、编程等等。虽然我不支持多模态识别，但我可以处理你上传的图像、txt、pdf、ppt、word、excel等文件，从中读取文字信息来帮助你。

        我完全免费使用，拥有128K的上下文长度，还支持联网搜索功能（需要你手动点开联网搜索按键）。你也可以通过官方应用商店下载我的App版本。

        我的知识截止到2024年7月，会以热情细腻的方式为你提供帮助。有什么问题或需要协助的地方，尽管告诉我吧！我会尽力帮你解决的！
        ====================Token 消耗====================

        {
          prompt_tokens: 5,
          completion_tokens: 226,
          total_tokens: 231,
          completion_tokens_details: { reasoning_tokens: 81, text_tokens: 145 }
        }
        ```
      </Tab>

      <Tab title="HTTP">
        ### 示例代码

        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
            "model": "siliconflow/deepseek-v3.2",
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
          model="siliconflow/deepseek-v3.2",
          messages=messages,
          result_format="message",  # 设置结果格式为 message
          enable_thinking=True,
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

        嗯，用户问了一个非常基础的自我介绍问题。这种问题不需要复杂拆解，直接说明身份和核心功能就好。

        想到可以用简洁清晰的结构回应：先表明AI身份，再分块介绍能力特点，最后用开放性问题结尾引导对话继续。避免过度展开，保持信息密度。

        需要特别注意语气友好但专业，用表情符号调节氛围但不过度。提到知识截止日期和免费属性能增加可信度，结尾的"随时为您效劳"能强化服务感。
        ====================完整回复====================

        你好！我是DeepSeek，由深度求索公司创造的AI助手！

        我是一个纯文本模型，擅长回答各种问题、协助写作、分析问题、编程等等。虽然我不支持多模态识别，但我可以处理你上传的图像、txt、pdf、ppt、word、excel等文件，从中读取文字信息来帮助你。

        我的一些特点：
        - 完全免费使用，没有收费计划
        - 支持128K的上下文长度
        - 可以通过官方应用商店下载App
        - 支持联网搜索功能（需要手动开启）
        - 知识截止到2024年7月

        我很乐意成为你的学习和工作伙伴，无论是日常聊天、解答疑惑，还是协助处理复杂任务，我都会热情细致地为你提供帮助！有什么我可以为你做的吗？
        ====================Token 消耗====================

        {"input_tokens": 6, "output_tokens": 265, "total_tokens": 271, "output_tokens_details": {"reasoning_tokens": 103, "text_tokens": 162}}
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
                .model("siliconflow/deepseek-v3.2")
                .enableThinking(true)
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

        唔，用户问了一个简单的自我介绍问题。这种问题很常见，需要快速清晰地表明身份和功能。考虑用轻松友好的语气介绍自己是DeepSeek-V3，并说明由深度求索公司创造。可以加上能提供的帮助类型，比如解答问题、聊天、学习辅导等，最后用表情符号增加亲和力。不需要过多解释，保持简洁明了就好。
        ====================完整回复====================

        DeepSeek-V3，一个由深度求索公司创造的智能助手！我可以帮助你解答各种问题、提供建议、进行知识查询，甚至陪你聊天！无论是学习、工作还是日常生活中的疑问，尽管问我吧~有什么我可以帮你的吗？
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
            "model": "siliconflow/deepseek-v3.2",
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
</Tabs>

## 其它功能

| 模型                                 | 工具调用 | Function Call | 流式输出      | 异步调用 | 系统消息 | 前缀续写 |
| ---------------------------------- | ---- | ------------- | --------- | ---- | ---- | ---- |
| siliconflow/deepseek-v3.2          | ✓    | ✓             | ✓（仅非思考模式） | —    | ✓    | —    |
| siliconflow/deepseek-v3.1-terminus | ✓    | ✓             | ✓（仅非思考模式） | —    | ✓    | —    |
| siliconflow/deepseek-r1-0528       | ✓    | ✓             | —         | —    | ✓    | —    |
| siliconflow/deepseek-v3-0324       | ✓    | ✓             | ✓         | —    | ✓    | —    |

## 参数默认值

| 模型                                 | temperature | top\_p | repetition\_penalty | presence\_penalty |
| ---------------------------------- | ----------- | ------ | ------------------- | ----------------- |
| siliconflow/deepseek-v3.2          | 1.0         | 1.0    | -                   | -                 |
| siliconflow/deepseek-v3.1-terminus | 1.0         | 1.0    | -                   | -                 |
| siliconflow/deepseek-r1-0528       | 1.0         | 1.0    | -                   | -                 |
| siliconflow/deepseek-v3-0324       | 1.0         | 1.0    | -                   | -                 |

"-" 表示没有默认值，也不支持设置。

## 模型列表与计费

硅基流动基于自研推理引擎，为DeepSeek模型提供低延迟、高稳定性的推理服务。

- 混合思考模型（通过`enable_thinking`参数控制是否思考）：siliconflow/deepseek-v3.2、siliconflow/deepseek-v3.1-terminus
- 仅思考模型（回复前总会思考）：siliconflow/deepseek-r1-0528
- 非思考模型：siliconflow/deepseek-v3-0324

siliconflow/deepseek-v3.2 模型在代码和数学等任务上表现优异，且价格最低，推荐优先使用。

模型上下文长度与价格信息请参见[千问AI平台控制台](https://www.qianwenai.com/models)。

按照模型的输入与输出 Token 计费。

<Note>
  思考模式下，思维链按照输出 Token 计费。
</Note>

## 错误码

如果执行报错，请参见错误码文档进行解决。
