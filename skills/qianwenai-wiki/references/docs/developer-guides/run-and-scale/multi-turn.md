> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 多轮对话

> 管理对话上下文

Qwen API 是无状态的，不会保存对话历史。要实现多轮对话，您需要在每次请求中传递对话历史。此外，您还可以使用截断、摘要和检索等策略来高效管理上下文并降低 Token 消耗。

<Note>
  本文介绍如何通过 Responses API、OpenAI 兼容 Chat Completions 或 DashScope API 实现多轮对话，并提供上下文管理策略。
</Note>

## 工作原理

要实现多轮对话，您需要维护一个 `messages` 数组。每轮对话中，将用户的最新提问和模型的回复追加到该数组中，然后将更新后的数组作为下一次请求的输入。

以下示例展示了对话过程中 `messages` 数组的变化：

<Steps>
  <Step title="第一轮">
    将用户的提问添加到 `messages` 数组中。

    ```json
    // 使用文本模型
    [
      {"role": "user", "content": "推荐一部关于太空探索的科幻电影。"}
    ]

    // 使用多模态模型，例如 Qwen-VL
    // {"role": "user",
    //       "content": [{"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"}},
    //                   {"type": "text", "text": "图片中展示了哪些商品？"}]
    // }
    ```
  </Step>

  <Step title="第二轮">
    将模型的回复和用户的最新提问添加到 `messages` 数组中。

    ```json
    // 使用文本模型
    [
      {"role": "user", "content": "推荐一部关于太空探索的科幻电影。"},
      {"role": "assistant", "content": "推荐《XXX》，这是一部经典的科幻作品。"},
      {"role": "user", "content": "这部电影的导演是谁？"}
    ]

    // 使用多模态模型，例如 Qwen-VL
    //[
    //    {"role": "user", "content": [
    //                    {"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"}},
    //                   {"type": "text", "text": "图片中展示了哪些商品？"}]},
    //    {"role": "assistant", "content": "图片中展示了三件商品：一条浅蓝色背带裤、一件蓝白条纹短袖衬衫和一双白色运动鞋。"},
    //    {"role": "user", "content": "它们是什么风格的？"}
    //]
    ```
  </Step>
</Steps>

## 快速开始

<Tabs>
  <Tab title="Responses API">
    Responses API 简化了多轮对话的实现。通过传递 `previous_response_id` 即可自动关联上下文，无需手动管理消息历史。如需更高级的会话管理，请参见[使用 Conversations](#使用-conversations)。

    <Note>
      请使用响应的 `id`（UUID 格式，如 `f0dbb153-117f-9bbf-8176-5284b47f3xxx`）作为 `previous_response_id`。不要使用 `output` 数组中消息的 `id`（如 `msg_56c860c4-3ad8-4a96-8553-d2f94c259xxx`）。响应 `id` 的有效期为 7 天。
    </Note>

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      # 第一轮
      response1 = client.responses.create(
        model="qwen3.7-plus",
        input="我叫小明，请记住我的名字。"
      )
      print(f"第一轮回复：{response1.output_text}")

      # 第二轮 - 使用 previous_response_id 关联上下文
      response2 = client.responses.create(
        model="qwen3.7-plus",
        input="你还记得我的名字吗？",
        previous_response_id=response1.id
      )
      print(f"第二轮回复：{response2.output_text}")
      ```

      ```javascript Node.js
      import OpenAI from "openai";

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      async function main() {
        // 第一轮
        const response1 = await openai.responses.create({
          model: "qwen3.7-plus",
          input: "我叫小明，请记住我的名字。"
        });
        console.log(`第一轮回复：${response1.output_text}`);

        // 第二轮 - 使用 previous_response_id 关联上下文
        const response2 = await openai.responses.create({
          model: "qwen3.7-plus",
          input: "你还记得我的名字吗？",
          previous_response_id: response1.id
        });
        console.log(`第二轮回复：${response2.output_text}`);
      }

      main();
      ```

      ```bash curl
      # 第一轮
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3.7-plus",
        "input": "我叫小明，请记住我的名字。"
      }'

      # 第二轮 - 使用第一轮响应中的 id 作为 previous_response_id
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3.7-plus",
        "input": "你还记得我的名字吗？",
        "previous_response_id": "response_id_from_first_round"
      }'
      ```
    </CodeGroup>

    **响应示例（第二轮）**：

    ```json
    {
      "id": "f0dbb153-117f-9bbf-8176-5284b47f3xxx",
      "model": "qwen3.7-plus",
      "status": "completed",
      "output": [
        {
          "type": "message",
          "role": "assistant",
          "content": [
            {
              "type": "output_text",
              "text": "当然记得，小明！有什么我可以帮您的吗？"
            }
          ]
        }
      ],
      "usage": {
        "input_tokens": 78,
        "output_tokens": 16,
        "total_tokens": 94
      }
    }
    ```
  </Tab>

  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      def get_response(messages):
        client = OpenAI(
          # 如果没有配置环境变量，请用 API Key 替换下行: api_key="sk-xxx",
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        completion = client.chat.completions.create(model="qwen3.7-plus", messages=messages)
        return completion

      # 初始化 messages 数组
      messages = [
        {
          "role": "system",
          "content": """你是千问AI平台手机商店的销售，负责向用户推荐手机。手机有两个参数：屏幕尺寸（包括 6.1 英寸、6.5 英寸和 6.7 英寸）和分辨率（包括 2K 和 4K）。
          每次只能向用户询问一个参数。如果用户提供的信息不完整，你需要追问以获取缺失的参数。当所有参数收集完毕后，你必须说：我已了解您的购买意向，请稍等。""",
        }
      ]
      assistant_output = "欢迎光临千问AI平台手机商店，请问您需要什么尺寸的手机？"
      print(f"模型输出：{assistant_output}\n")
      while "我已了解您的购买意向" not in assistant_output:
        user_input = input("请输入：")
        # 将用户的提问添加到 messages 列表
        messages.append({"role": "user", "content": user_input})
        assistant_output = get_response(messages).choices[0].message.content
        # 将模型的回复添加到 messages 列表
        messages.append({"role": "assistant", "content": assistant_output})
        print(f"模型输出：{assistant_output}")
        print("\n")
      ```

      ```javascript Node.js
      import OpenAI from "openai";
      import { createInterface } from 'readline/promises';

      const BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1";
      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: BASE_URL
      });

      async function getResponse(messages) {
        try {
          const completion = await openai.chat.completions.create({
            model: "qwen3.7-plus",
            messages: messages,
          });
          return completion.choices[0].message.content;
        } catch (error) {
          console.error("获取回复时出错：", error);
          throw error;  // 抛出异常，由上层处理
        }
      }

      // 初始化 messages 数组
      const messages = [
        {
          "role": "system",
          "content": `你是千问AI平台手机商店的销售，负责向用户推荐手机。手机有两个参数：屏幕尺寸（包括 6.1 英寸、6.5 英寸和 6.7 英寸）和分辨率（包括 2K 和 4K）。
          每次只能向用户询问一个参数。如果用户提供的信息不完整，你需要追问以获取缺失的参数。当所有参数收集完毕后，你必须说：我已了解您的购买意向，请稍等。`,
        }
      ];

      let assistant_output = "欢迎光临千问AI平台手机商店，请问您需要什么尺寸的手机？";
      console.log(assistant_output);

      const readline = createInterface({
        input: process.stdin,
        output: process.stdout
      });

      (async () => {
        while (!assistant_output.includes("我已了解您的购买意向")) {
          const user_input = await readline.question("请输入：");
          messages.push({ role: "user", content: user_input});
          try {
            const response = await getResponse(messages);
            assistant_output = response;
            messages.push({ role: "assistant", content: assistant_output });
            console.log(assistant_output);
            console.log("\n");
          } catch (error) {
            console.error("获取回复时出错：", error);
          }
        }
        readline.close();
      })();
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3.7-plus",
        "messages":[
          {
            "role": "system",
            "content": "You are a helpful assistant."
          },
          {
            "role": "user",
            "content": "你好"
          },
          {
            "role": "assistant",
            "content": "你好！有什么我可以帮您的吗？"
          },
          {
            "role": "user",
            "content": "你能做什么？"
          }
        ]
      }'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python
      import os
      from dashscope import Generation
      import dashscope
      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      def get_response(messages):
        response = Generation.call(
          # 如果没有配置环境变量，请用 API Key 替换下行: api_key="sk-xxx",
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="qwen-plus",
          messages=messages,
          result_format="message",
        )
        return response

      messages = [
        {
          "role": "system",
          "content": """你是千问AI平台手机商店的销售，负责向用户推荐手机。手机有两个参数：屏幕尺寸（包括 6.1 英寸、6.5 英寸和 6.7 英寸）和分辨率（包括 2K 和 4K）。
          每次只能向用户询问一个参数。如果用户提供的信息不完整，你需要追问以获取缺失的参数。当所有参数收集完毕后，你必须说：我已了解您的购买意向，请稍等。""",
        }
      ]

      assistant_output = "欢迎光临千问AI平台手机商店，请问您需要什么尺寸的手机？"
      print(f"模型输出：{assistant_output}\n")
      while "我已了解您的购买意向" not in assistant_output:
        user_input = input("请输入：")
        # 将用户的提问添加到 messages 列表
        messages.append({"role": "user", "content": user_input})
        assistant_output = get_response(messages).output.choices[0].message.content
        # 将模型的回复添加到 messages 列表
        messages.append({"role": "assistant", "content": assistant_output})
        print(f"模型输出：{assistant_output}")
        print("\n")
      ```

      ```java Java
      import java.util.ArrayList;
      import java.util.List;
      import com.alibaba.dashscope.aigc.generation.Generation;
      import com.alibaba.dashscope.aigc.generation.GenerationParam;
      import com.alibaba.dashscope.aigc.generation.GenerationResult;
      import com.alibaba.dashscope.common.Message;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.InputRequiredException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import java.util.Scanner;
      import com.alibaba.dashscope.protocol.Protocol;

      public class Main {
        public static GenerationParam createGenerationParam(List<Message> messages) {
          return GenerationParam.builder()
              // 如果没有配置环境变量，请用 API Key 替换下行: .apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen-plus")
              .messages(messages)
              .resultFormat(GenerationParam.ResultFormat.MESSAGE)
              .build();
        }
        public static GenerationResult callGenerationWithMessages(GenerationParam param) throws ApiException, NoApiKeyException, InputRequiredException {
          Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");
          return gen.call(param);
        }
        public static void main(String[] args) {
          try {
            List<Message> messages = new ArrayList<>();
            messages.add(createMessage(Role.SYSTEM, "You are a helpful assistant."));
            for (int i = 0; i < 3;i++) {
              Scanner scanner = new Scanner(System.in);
              System.out.print("请输入：");
              String userInput = scanner.nextLine();
              if ("exit".equalsIgnoreCase(userInput)) {
                break;
              }
              messages.add(createMessage(Role.USER, userInput));
              GenerationParam param = createGenerationParam(messages);
              GenerationResult result = callGenerationWithMessages(param);
              System.out.println("模型输出："+result.getOutput().getChoices().get(0).getMessage().getContent());
              messages.add(result.getOutput().getChoices().get(0).getMessage());
            }
          } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            e.printStackTrace();
          }
          System.exit(0);
        }
        private static Message createMessage(Role role, String content) {
          return Message.builder().role(role.getValue()).content(content).build();
        }
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen-plus",
        "input":{
          "messages":[
            {
              "role": "system",
              "content": "You are a helpful assistant."
            },
            {
              "role": "user",
              "content": "你好"
            },
            {
              "role": "assistant",
              "content": "你好！有什么我可以帮您的吗？"
            },
            {
              "role": "user",
              "content": "你能做什么？"
            }
          ]
        }
      }'
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## 多模态模型

<Note>
  - 本节适用于 Qwen3-VL 和 Qwen3.5 等多模态模型。`Qwen-Omni` 请参见[非实时](/developer-guides/speech/multimodal-speech)。
  - Qwen3-Omni-Captioner 专为单轮任务设计，不支持多轮对话。
</Note>

多模态模型的多轮对话与文本模型有以下区别：

- **用户消息的构造**：多模态模型的用户消息除了文本外，还可以包含图像、音频等多模态信息。
- **DashScope SDK 接口**：使用 DashScope Python SDK 时，需调用 `MultiModalConversation` 类；使用 DashScope Java SDK 时，同样调用 `MultiModalConversation` 类。

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python
      from openai import OpenAI
      import os

      client = OpenAI(
        # 如果没有配置环境变量，请用 API Key 替换下行: api_key="sk-xxx"
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
      )
      messages = [
        {
          "role": "user",
          "content": [
            {
              "type": "image_url",
              "image_url": {
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
              },
            },
            {"type": "text", "text": "图片中展示了哪些商品？"},
          ],
        }
      ]
      completion = client.chat.completions.create(
        model="qwen3-vl-plus",  # 您可以替换为其他多模态模型，并根据需要修改 messages
        messages=messages,
      )
      print(f"第一轮输出：{completion.choices[0].message.content}")

      assistant_message = completion.choices[0].message
      messages.append(assistant_message.model_dump())
      messages.append({
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "它们是什么风格的？"
          }
        ]
      })
      completion = client.chat.completions.create(
        model="qwen3-vl-plus",
        messages=messages,
        )

      print(f"第二轮输出：{completion.choices[0].message.content}")
      ```

      ```javascript Node.js
      import OpenAI from "openai";

      const openai = new OpenAI(
        {
          // 如果没有配置环境变量，请用 API Key 替换下行: apiKey: "sk-xxx",
          apiKey: process.env.DASHSCOPE_API_KEY,
          baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
        }
      );

      let messages = [
        {
        role: "user", content: [
          { type: "image_url", image_url: { "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png" } },
          { type: "text", text: "图片中展示了哪些商品？" },
        ]
      }]
      async function main() {
        let response = await openai.chat.completions.create({
          model: "qwen3-vl-plus",   // 您可以替换为其他多模态模型，并根据需要修改 messages
          messages: messages
        });
        console.log(`第一轮输出：${response.choices[0].message.content}`);
        messages.push(response.choices[0].message);
        messages.push({"role": "user", "content": "用一首诗描述这个场景"});
        response = await openai.chat.completions.create({
          model: "qwen3-vl-plus",
          messages: messages
        });
        console.log(`第二轮输出：${response.choices[0].message.content}`);
      }

      main()
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "model": "qwen3-vl-plus",
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "image_url",
                "image_url": {
                  "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
                }
              },
              {
                "type": "text",
                "text": "图片中展示了哪些商品？"
              }
            ]
          },
          {
            "role": "assistant",
            "content": [
              {
                "type": "text",
                "text": "图片中展示了三件商品：一条浅蓝色背带裤、一件蓝白条纹短袖衬衫和一双白色运动鞋。"
              }
            ]
          },
          {
            "role": "user",
            "content": [
              {
                "type": "text",
                "text": "它们是什么风格的？"
              }
            ]
          }
        ]
      }'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python
      import os
      from dashscope import MultiModalConversation
      import dashscope
      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      messages = [
        {
          "role": "user",
          "content": [
            {
              "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"
            },
            {"text": "图片中展示了哪些商品？"},
          ],
        }
      ]
      response = MultiModalConversation.call(
        # 如果没有配置环境变量，请用 API Key 替换下行: api_key="sk-xxx",
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3-vl-plus',  # 您可以替换为其他多模态模型，并根据需要修改 messages
        messages=messages
        )

      print(f"模型第一轮输出：{response.output.choices[0].message.content[0]['text']}")
      messages.append(response['output']['choices'][0]['message'])
      user_msg = {"role": "user", "content": [{"text": "它们是什么风格的？"}]}
      messages.append(user_msg)
      response = MultiModalConversation.call(
        # 如果没有配置环境变量，请用 API Key 替换下行: api_key="sk-xxx",
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3-vl-plus',
        messages=messages
        )

      print(f"模型第二轮输出：{response.output.choices[0].message.content[0]['text']}")
      ```

      ```java Java
      import java.util.ArrayList;
      import java.util.Arrays;
      import java.util.Collections;
      import java.util.List;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;

      public class Main {
        static {
          Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
        }
        private static final String modelName = "qwen3-vl-plus";  // 您可以替换为其他多模态模型，并根据需要修改 messages
        public static void MultiRoundConversationCall() throws ApiException, NoApiKeyException, UploadFileException {
          MultiModalConversation conv = new MultiModalConversation();
          MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
              .content(Arrays.asList(Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"),
                  Collections.singletonMap("text", "图片中展示了哪些商品？"))).build();
          List<MultiModalMessage> messages = new ArrayList<>();
          messages.add(userMessage);
          MultiModalConversationParam param = MultiModalConversationParam.builder()
              // 如果没有配置环境变量，请用 API Key 替换下行: .apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model(modelName)
              .messages(messages)
              .build();
          MultiModalConversationResult result = conv.call(param);
          System.out.println("第一轮输出："+result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));        // 将结果添加到对话中
          messages.add(result.getOutput().getChoices().get(0).getMessage());
          MultiModalMessage msg = MultiModalMessage.builder().role(Role.USER.getValue())
              .content(Arrays.asList(Collections.singletonMap("text", "它们是什么风格的？"))).build();
          messages.add(msg);
          param.setMessages((List)messages);
          result = conv.call(param);
          System.out.println("第二轮输出："+result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));    }

        public static void main(String[] args) {
          try {
            MultiRoundConversationCall();
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
          System.exit(0);
        }
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "model": "qwen3-vl-plus",
        "input":{
          "messages":[
            {
              "role": "user",
              "content": [
                {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251031/ownrof/f26d201b1e3f4e62ab4a1fc82dd5c9bb.png"},
                {"text": "图片中展示了哪些商品？"}
              ]
            },
            {
              "role": "assistant",
              "content": [
                {"text": "图片中展示了三件商品：一条浅蓝色背带裤、一件蓝白条纹短袖衬衫和一双白色运动鞋。"}
              ]
            },
            {
              "role": "user",
              "content": [
                {"text": "它们是什么风格的？"}
              ]
            }
          ]
        }
      }'
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## 思考模型

思考模型会返回两个字段：`reasoning_content`（思考过程）和 `content`（最终回复）。更新 messages 数组时，只需保留 `content` 字段，忽略 `reasoning_content` 字段。

```json
[
  {"role": "user", "content": "推荐一部关于太空探索的科幻电影。"},
  {"role": "assistant", "content": "推荐《XXX》，这是一部经典的科幻作品。"},
  {"role": "user", "content": "这部电影的导演是谁？"}
]
```

<Note>
  将助手消息添加到 `messages` 数组时，请不要包含 `reasoning_content` 字段，否则会导致请求报错。
</Note>

<Note>
  关于思考模型的更多信息，请参见[深度思考](/developer-guides/text-generation/thinking)和[视觉理解](/developer-guides/multimodal/vision)。Qwen3-Omni-Flash（思考模式）的多轮对话请参见[非实时](/developer-guides/speech/multimodal-speech)。
</Note>

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python
      from openai import OpenAI
      import os

      # 初始化 OpenAI 客户端
      client = OpenAI(
        # 如果没有配置环境变量，请用 API Key 替换下行: api_key="sk-xxx"
        api_key = os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
      )

      messages = []
      conversation_idx = 1
      while True:
        reasoning_content = ""  # 定义完整思考过程
        answer_content = ""     # 定义完整回复
        is_answering = False   # 判断是否结束思考过程并开始回复
        print("="*20+f"第 {conversation_idx} 轮对话"+"="*20)
        conversation_idx += 1
        user_msg = {"role": "user", "content": input("请输入：")}
        messages.append(user_msg)
        # 创建聊天补全请求
        completion = client.chat.completions.create(
          # 您可以根据需要替换为其他深度思考模型
          model="qwen3.7-plus",
          messages=messages,
          extra_body={"enable_thinking": True},
          stream=True,
          # stream_options={
          #     "include_usage": True
          # }
        )
        print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
        for chunk in completion:
          # 如果 chunk.choices 为空，打印用量信息
          if not chunk.choices:
            print("\n用量信息：")
            print(chunk.usage)
          else:
            delta = chunk.choices[0].delta
            # 打印思考过程
            if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
              print(delta.reasoning_content, end='', flush=True)
              reasoning_content += delta.reasoning_content
            else:
              # 开始回复
              if delta.content != "" and is_answering is False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
              # 打印回复内容
              print(delta.content, end='', flush=True)
              answer_content += delta.content
        # 将模型回复内容添加到上下文
        messages.append({"role": "assistant", "content": answer_content})
        print("\n")
      ```

      ```javascript Node.js
      import OpenAI from "openai";
      import process from 'process';
      import readline from 'readline/promises';

      // 初始化 readline 接口
      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
      });

      // 初始化 OpenAI 客户端
      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY, // 从环境变量读取
        baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
      });

      let reasoningContent = '';
      let answerContent = '';
      let isAnswering = false;
      let messages = [];
      let conversationIdx = 1;

      async function main() {
        while (true) {
          console.log("=".repeat(20) + `第 ${conversationIdx} 轮对话` + "=".repeat(20));
          conversationIdx++;

          // 读取用户输入
          const userInput = await rl.question("请输入：");
          messages.push({ role: 'user', content: userInput });

          // 重置状态
          reasoningContent = '';
          answerContent = '';
          isAnswering = false;

          try {
            const stream = await openai.chat.completions.create({
              // 您可以根据需要替换为其他深度思考模型
              model: 'qwen3.7-plus',
              messages: messages,
              enable_thinking: true,
              stream: true,
              // stream_options:{
              //     include_usage: true
              // }
            });

            console.log("\n" + "=".repeat(20) + "思考过程" + "=".repeat(20) + "\n");

            for await (const chunk of stream) {
              if (!chunk.choices?.length) {
                console.log('\n用量信息：');
                console.log(chunk.usage);
                continue;
              }

              const delta = chunk.choices[0].delta;

              // 处理思考过程
              if (delta.reasoning_content) {
                process.stdout.write(delta.reasoning_content);
                reasoningContent += delta.reasoning_content;
              }

              // 处理正式回复
              if (delta.content) {
                if (!isAnswering) {
                  console.log('\n' + "=".repeat(20) + "完整回复" + "=".repeat(20) + "\n");
                  isAnswering = true;
                }
                process.stdout.write(delta.content);
                answerContent += delta.content;
              }
            }

            // 将完整回复添加到消息历史
            messages.push({ role: 'assistant', content: answerContent });
            console.log("\n");

          } catch (error) {
            console.error('错误：', error);
          }
        }
      }

      // 启动程序
      main().catch(console.error);
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3.7-plus",
        "messages": [
          {
            "role": "user",
            "content": "你好"
          },
          {
            "role": "assistant",
            "content": "你好！很高兴见到你，有什么我可以帮你的吗？"
          },
          {
            "role": "user",
            "content": "你是谁？"
          }
        ],
        "stream": true,
        "stream_options": {
          "include_usage": true
        },
        "enable_thinking": true
      }'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python
      import os
      from dashscope import MultiModalConversation
      import dashscope
      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      messages = []
      conversation_idx = 1
      while True:
        print("=" * 20 + f"第 {conversation_idx} 轮对话" + "=" * 20)
        conversation_idx += 1
        user_msg = {"role": "user", "content": [{"text": input("请输入：")}]}
        messages.append(user_msg)
        response = MultiModalConversation.call(
          # 如果没有配置环境变量，请用 API Key 替换下行: api_key="sk-xxx",
          api_key=os.getenv('DASHSCOPE_API_KEY'),
          # qwen3.7-plus 需要使用多模态接口。qwen3-max、qwen-plus 等请使用 Generation.call。
          model="qwen3.7-plus",
          messages=messages,
          enable_thinking=True,
          result_format="message",
          stream=True,
          incremental_output=True
        )
        # 定义完整思考过程
        reasoning_content = ""
        # 定义完整回复
        answer_content = ""
        # 判断是否结束思考过程并开始回复
        is_answering = False
        print("=" * 20 + "思考过程" + "=" * 20)
        for chunk in response:
          # 如果思考过程和回复都为空，则跳过
          if (chunk.output.choices[0].message.content == "" and
            chunk.output.choices[0].message.reasoning_content == ""):
            pass
          else:
            # 如果当前是思考过程
            if (chunk.output.choices[0].message.reasoning_content != "" and
              chunk.output.choices[0].message.content == ""):
              print(chunk.output.choices[0].message.reasoning_content, end="",flush=True)
              reasoning_content += chunk.output.choices[0].message.reasoning_content
            # 如果当前是正式回复
            elif chunk.output.choices[0].message.content != "":
              if not is_answering:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20)
                is_answering = True
              print(chunk.output.choices[0].message.content, end="",flush=True)
              answer_content += chunk.output.choices[0].message.content
        # 将模型回复内容添加到上下文
        messages.append({"role": "assistant", "content": answer_content})
        print("\n")
        # 如需打印完整的思考过程和回复，可取消以下代码的注释
        # print("=" * 20 + "完整思考过程" + "=" * 20 + "\n")
        # print(f"{reasoning_content}")
        # print("=" * 20 + "完整回复" + "=" * 20 + "\n")
        # print(f"{answer_content}")
      ```

      ```java Java
      // DashScope SDK 版本 >= 2.19.4
      import java.util.Arrays;
      import java.util.ArrayList;
      import java.util.Collections;
      import java.util.List;
      import org.slf4j.Logger;
      import org.slf4j.LoggerFactory;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import io.reactivex.Flowable;
      import com.alibaba.dashscope.utils.Constants;

      public class Main {
        static {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        }
        private static final Logger logger = LoggerFactory.getLogger(Main.class);
        private static StringBuilder reasoningContent = new StringBuilder();
        private static StringBuilder finalContent = new StringBuilder();
        private static boolean isFirstPrint = true;

        private static void handleResult(MultiModalConversationResult message) {
          if (message != null && message.getOutput() != null
            && message.getOutput().getChoices() != null
            && !message.getOutput().getChoices().isEmpty()
            && message.getOutput().getChoices().get(0) != null
            && message.getOutput().getChoices().get(0).getMessage() != null) {

            String reasoning = message.getOutput().getChoices().get(0).getMessage().getReasoningContent();
            List<java.util.Map<String, Object>> contentList = message.getOutput().getChoices().get(0).getMessage().getContent();
            String content = "";
            if (contentList != null && !contentList.isEmpty() && contentList.get(0).containsKey("text")) {
              content = String.valueOf(contentList.get(0).get("text"));
            }

            if (reasoning != null && !reasoning.isEmpty()) {
              reasoningContent.append(reasoning);
              if (isFirstPrint) {
                System.out.println("====================思考过程====================");
                isFirstPrint = false;
              }
              System.out.print(reasoning);
            }

            if (!content.isEmpty()) {
              finalContent.append(content);
              if (!isFirstPrint) {
                System.out.println("\n====================完整回复====================");
                isFirstPrint = true;
              }
              System.out.print(content);
            }
          }
        }

        public static void main(String[] args) {
          try {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMsg1 = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "你好"))).build();
            MultiModalMessage assistantMsg = MultiModalMessage.builder().role(Role.ASSISTANT.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "你好！很高兴见到你，有什么我可以帮你的吗？"))).build();
            MultiModalMessage userMsg2 = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(Collections.singletonMap("text", "你是谁"))).build();
            List<MultiModalMessage> messages = new ArrayList<>(Arrays.asList(userMsg1, assistantMsg, userMsg2));
            MultiModalConversationParam param = MultiModalConversationParam.builder()
                // 如果没有配置环境变量，请用 API Key 替换下行: .apiKey("sk-xxx")
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                // qwen3.7-plus 需要使用多模态接口。qwen3-max、qwen-plus 等请使用 Generation。
                .model("qwen3.7-plus")
                .enableThinking(true)
                .messages(messages)
                .incrementalOutput(true)
                .build();
            Flowable<MultiModalConversationResult> result = conv.streamCall(param);
            result.doOnError(throwable -> logger.error("错误：{}", throwable.getMessage(), throwable))
                .blockingForEach(Main::handleResult);
          } catch (ApiException | NoApiKeyException e) {
            logger.error("发生异常：{}", e.getMessage(), e);
          } catch (Exception e) {
            logger.error("发生未知错误：{}", e.getMessage(), e);
          } finally {
            System.exit(0);
          }
        }
      }
      ```

      ```bash curl
      # qwen3.7-plus 需要使用多模态接口。qwen3-max、qwen-plus 等请使用 text-generation/generation。
      curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -H "X-DashScope-SSE: enable" \
      -d '{
        "model": "qwen3.7-plus",
        "input":{
          "messages":[
            {
              "role": "user",
              "content": [{"text": "你好"}]
            },
            {
              "role": "assistant",
              "content": [{"text": "你好！很高兴见到你，有什么我可以帮你的吗？"}]
            },
            {
              "role": "user",
              "content": [{"text": "你是谁？"}]
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
    </CodeGroup>
  </Tab>
</Tabs>

## 使用 Conversations

`previous_response_id` 适用于简单的链式对话。如果需要服务端会话管理、跨设备上下文延续或手动控制消息，可以使用 Conversations API 的 `conversation` 参数。

### 创建会话并对话

首先通过 Conversations API 创建一个会话，然后将 `conversation` 参数和 `instructions`（系统提示词）传入 `responses.create`。服务端会自动管理上下文。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  # 创建会话
  conversation = client.conversations.create()

  # 第一轮
  response1 = client.responses.create(
    conversation=conversation.id,
    model="qwen3.7-plus",
    instructions="你是一位旅行顾问，擅长推荐旅行目的地。",
    input="推荐一个适合夏季旅行的城市。",
  )
  print(f"第一轮回复：{response1.output_text}")

  # 第二轮 - 服务端自动管理上下文
  response2 = client.responses.create(
    conversation=conversation.id,
    model="qwen3.7-plus",
    instructions="你是一位旅行顾问，擅长推荐旅行目的地。",
    input="那里有什么必尝的美食？",
  )
  print(f"第二轮回复：{response2.output_text}")
  ```

  ```javascript Node.js
  import OpenAI from "openai";

  const client = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
  });

  async function main() {
    // 创建会话
    const conversation = await client.conversations.create();

    // 第一轮
    const response1 = await client.responses.create({
      conversation: conversation.id,
      model: "qwen3.7-plus",
      instructions: "你是一位旅行顾问，擅长推荐旅行目的地。",
      input: "推荐一个适合夏季旅行的城市。",
    });
    console.log("第一轮回复：", response1.output_text);

    // 第二轮 - 服务端自动管理上下文
    const response2 = await client.responses.create({
      conversation: conversation.id,
      model: "qwen3.7-plus",
      instructions: "你是一位旅行顾问，擅长推荐旅行目的地。",
      input: "那里有什么必尝的美食？",
    });
    console.log("第二轮回复：", response2.output_text);
  }

  main();
  ```

  ```bash curl
  # 创建会话
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/conversations \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'

  # 第一轮 - 使用上面返回的 conversation id
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.7-plus",
    "instructions": "你是一位旅行顾问，擅长推荐旅行目的地。",
    "input": "推荐一个适合夏季旅行的城市。",
    "conversation": "conversation_id_from_above"
  }'

  # 第二轮 - 使用相同的 conversation id
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.7-plus",
    "instructions": "你是一位旅行顾问，擅长推荐旅行目的地。",
    "input": "那里有什么必尝的美食？",
    "conversation": "conversation_id_from_above"
  }'
  ```
</CodeGroup>

### 向会话中添加消息

您可以手动向会话中添加消息（如补充用户消息或外部知识）。

<CodeGroup>
  ```python Python
  items = client.conversations.items.create(
    "conv_xxx",  # 替换为您的 conversation id
    items=[
      {
        "type": "message",
        "role": "user",
        "content": [{"type": "input_text", "text": "补充信息：我更喜欢海滨城市。"}],
      }
    ],
  )
  print(items.data)
  ```

  ```javascript Node.js
  const items = await client.conversations.items.create(
    "conv_xxx",  // 替换为您的 conversation id
    {
      items: [
        {
          type: "message",
          role: "user",
          content: [{ type: "input_text", text: "补充信息：我更喜欢海滨城市。" }]
        }
      ]
    }
  );
  console.log(items.data);
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx/items \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "type": "message",
        "role": "user",
        "content": [{
          "type": "input_text",
          "text": "补充信息：我更喜欢海滨城市。"
        }]
      }
    ]
  }'
  ```
</CodeGroup>

### 查看对话历史

列出会话中的所有消息，查看完整的对话历史。

<CodeGroup>
  ```python Python
  items = client.conversations.items.list("conv_xxx")  # 替换为您的 conversation id
  print(items.data)
  ```

  ```javascript Node.js
  const items = await client.conversations.items.list("conv_xxx");  // 替换为您的 conversation id
  console.log(items.data);
  ```

  ```bash curl
  curl -X GET "https://dashscope.aliyuncs.com/compatible-mode/v1/conversations/conv_xxx/items?limit=20&order=asc" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
  ```
</CodeGroup>

### 注意事项

- **ID 有效期**：响应 `id` 和会话中的消息有效期为 7 天。`conversation` 本身不过期，可持续使用，但其中过期的消息将不再参与上下文。建议通过 `instructions` 参数传递系统指令，而非通过创建会话时的 items，以避免系统指令因过期而丢失。
- **正确的 ID 来源**：请使用响应的顶层 `id`，而非 `output` 数组中消息的 `id`。
- **跨轮上下文**：每次传入 `previous_response_id` 时，系统会自动关联从首轮对话到当前轮次的完整上下文。
- **互斥性**：`previous_response_id` 和 `conversation` 不能同时使用，否则会报错 `[400] INVALID_REQUEST: Mutually exclusive parameters: Ensure you are only providing one of: previous_response_id or conversation.`

### 如何选择？

| 方式                     | 适用场景                    |
| ---------------------- | ----------------------- |
| `previous_response_id` | 简单的链式多轮对话，无需创建独立会话      |
| `conversation`         | 服务端会话管理、跨设备上下文延续、手动增删消息 |

更多 Conversations API 操作（更新会话、删除会话、删除消息等），请参见 [Conversations](/api-reference/platform-api/conversations)。

## 正式使用

多轮对话会消耗大量 Token，且可能超出模型的上下文限制。请使用以下策略管理上下文并控制成本。

### 1. 上下文管理

`messages` 数组会随着对话轮次增长，可能超出 Token 限制。

#### 1.1. 上下文截断

当对话历史过长时，只保留最近 N 轮对话。这种方法实现简单，但会丢失早期的对话信息。

#### 1.2. 滚动摘要

为了在不丢失核心信息的前提下动态压缩对话历史、控制上下文长度，可以随着对话推进对上下文进行摘要：

a. 当对话历史达到一定长度（如最大上下文长度的 70%）时，提取较早的部分（如前半段），单独调用模型生成该部分的"记忆摘要"。

b. 构造下一次请求时，用"记忆摘要"替换冗长的对话历史，并拼接最近几轮对话。

#### 1.3. 向量化检索

滚动摘要可能导致部分信息丢失。为了让模型能从大量对话历史中回忆相关信息，可以从线性传递上下文切换为按需检索：

a. 每轮对话结束后，将对话内容存入向量数据库。

b. 用户提问时，基于相似度检索相关的对话记录。

c. 将检索到的对话记录与最新的用户输入合并后发送给模型。

### 2. 成本控制

每轮对话的输入 Token 都会增加，导致成本上升。

#### 2.1. 减少输入 Token

使用上述上下文管理策略来减少输入 Token，从而降低成本。

#### 2.2. 使用支持上下文缓存的模型

`messages` 数组会被重复处理和计费。[上下文缓存](/developer-guides/run-and-scale/context-cache)（适用于 Qwen-Max、Qwen-Plus、Qwen-Flash 和 Qwen-Coder 等部分 Qwen 模型）可以降低成本并提升响应速度。

<Note>
  上下文缓存功能自动启用，无需修改代码。
</Note>

## 错误码

如果调用失败，请参见[错误信息](/api-reference/preparation/error-messages)。
