> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 函数调用

> 将模型连接到外部工具

Function calling 使大语言模型能够调用外部工具（如 API、数据库或自定义函数）来回答自身无法解决的问题。您定义工具，模型决定何时调用，应用程序执行调用。

## 工作原理

Function calling 通过应用程序和模型之间的多步交互，使大语言模型能够调用外部工具。

1. **发起第一次模型调用**

应用程序向模型发送请求，请求中包含用户问题和模型可调用的工具列表。

2. **接收模型的工具调用指令（工具名称和输入参数）**

如果模型判断需要调用工具，会返回一个 JSON 格式的指令，告诉应用程序要执行哪个函数以及传递哪些参数。

> 如果不需要调用工具，模型会直接返回自然语言回复。

3. **在应用程序中执行工具**

接收到工具指令后，应用程序执行工具并获取输出结果。

4. **发起第二次模型调用**

获取工具输出后，将其添加到模型的上下文（messages）中，然后再次调用模型。

5. **接收模型的最终回复**

模型结合工具输出和用户问题，生成自然语言回复。

以下流程图展示了整体工作流程：

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/8226342771/CAEQUxiBgMCR3fao4RkiIDY0YmY0NWU2NzM0MzQ3NWU5OWY1ZWRjM2Y2MWI4NTMx4358988_20240409160230.951.svg)

## 支持的模型

所有通用文本生成模型均支持 function calling，包括第三方模型（DeepSeek、Kimi、GLM、MiniMax）。视觉模型中，Qwen3-VL、qwen3.5-omni-plus、qwen3.5-omni-flash 和 qwen3-omni-flash 也支持该功能。Qwen-Omni-Realtime 系列（qwen3.5-omni-plus-realtime、qwen3.5-omni-flash-realtime）和 Qwen-Audio-Realtime 系列（qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash）也支持工具调用，通过 WebSocket 协议调用。完整列表请参阅[模型列表](/developer-guides/getting-started/text-generation-models)。

<Warning>
  调用 GLM 系列模型的 Function Calling 时，需在请求中传入 `extra_body={"tool_stream": True}`，否则模型不会返回 tool\_calls，工具调用不生效。
</Warning>

> 在思考模式下，使用 kimi/kimi-k3、kimi/kimi-k2.7-code-highspeed、kimi/kimi-k2.7-code、kimi/kimi-k2.6、kimi/kimi-k2.5 进行工具调用时，需在每轮 assistant 消息中保留 `reasoning_content` 字段；`tool_choice` 支持 `"auto"`（默认）、`"none"`，kimi/kimi-k3 还支持 `"required"`，否则会报错。

## 快速开始

本节通过一个天气查询场景演示 function calling 的使用方法。

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python
      from openai import OpenAI
      from datetime import datetime
      import json
      import os
      import random

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )
      # 模拟用户问题
      USER_QUESTION = "北京天气怎么样？"
      # 定义工具列表
      tools = [
        {
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "description": "当你需要查询某个城市的天气时使用。",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "城市名称，如北京、纽约等。",
                }
              },
              "required": ["location"],
            },
          },
        },
      ]

      # 模拟天气查询工具
      def get_current_weather(arguments):
        weather_conditions = ["sunny", "cloudy", "rainy"]
        random_weather = random.choice(weather_conditions)
        location = arguments["location"]
        return f"{location} is {random_weather} today."

      # 封装模型调用函数
      def get_response(messages):
        completion = client.chat.completions.create(
          model="qwen3.8-max",
          messages=messages,
          tools=tools,
        )
        return completion

      messages = [{"role": "user", "content": USER_QUESTION}]
      response = get_response(messages)
      assistant_output = response.choices[0].message
      if assistant_output.content is None:
        assistant_output.content = ""
      messages.append(assistant_output)
      # 如果不需要调用工具，直接输出回复
      if assistant_output.tool_calls is None:
        print(f"无需调用天气工具。直接回复：{assistant_output.content}")
      else:
        # 进入工具调用循环
        while assistant_output.tool_calls is not None:
          tool_call = assistant_output.tool_calls[0]
          tool_call_id = tool_call.id
          func_name = tool_call.function.name
          arguments = json.loads(tool_call.function.arguments)
          print(f"调用工具 [{func_name}]，参数：{arguments}")
          # 执行工具
          tool_result = get_current_weather(arguments)
          # 构建工具响应消息
          tool_message = {
            "role": "tool",
            "tool_call_id": tool_call_id,
            "content": tool_result,
          }
          print(f"工具返回结果：{tool_message['content']}")
          messages.append(tool_message)
          # 再次调用模型，获取自然语言回复
          response = get_response(messages)
          assistant_output = response.choices[0].message
          if assistant_output.content is None:
            assistant_output.content = ""
          messages.append(assistant_output)
        print(f"最终回复：{assistant_output.content}")
      ```

      ```javascript Node.js
      import OpenAI from 'openai';

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
      });

      const tools = [
        {
          type: "function",
          function: {
            name: "get_current_weather",
            description: "当你需要查询某个城市的天气时使用。",
            parameters: {
              type: "object",
              properties: {
                location: {
                  type: "string",
                  description: "城市名称，如北京、纽约等。",
                },
              },
              required: ["location"],
            },
          },
        },
      ];

      const getCurrentWeather = (args) => {
        const weatherConditions = ["sunny", "cloudy", "rainy"];
        const randomWeather = weatherConditions[Math.floor(Math.random() * weatherConditions.length)];
        const location = args.location;
        return `${location} is ${randomWeather} today.`;
      };

      const getResponse = async (messages) => {
        const response = await openai.chat.completions.create({
          model: "qwen3.8-max",
          messages: messages,
          tools: tools,
        });
        return response;
      };

      const main = async () => {
        const input = "北京天气怎么样？";

        let messages = [
          {
            role: "user",
            content: input,
          }
        ];
        let response = await getResponse(messages);
        let assistantOutput = response.choices[0].message;
        if (!assistantOutput.content) assistantOutput.content = "";
        messages.push(assistantOutput);
        if (!assistantOutput.tool_calls) {
          console.log(`无需调用天气工具。直接回复：${assistantOutput.content}`);
        } else {
          while (assistantOutput.tool_calls) {
            const toolCall = assistantOutput.tool_calls[0];
            const toolCallId = toolCall.id;
            const funcName = toolCall.function.name;
            const funcArgs = JSON.parse(toolCall.function.arguments);
            console.log(`调用工具 [${funcName}]，参数：`, funcArgs);
            const toolResult = getCurrentWeather(funcArgs);
            const toolMessage = {
              role: "tool",
              tool_call_id: toolCallId,
              content: toolResult,
            };
            console.log(`工具返回结果：${toolMessage.content}`);
            messages.push(toolMessage);
            response = await getResponse(messages);
            assistantOutput = response.choices[0].message;
            if (!assistantOutput.content) assistantOutput.content = "";
            messages.push(assistantOutput);
          }
          console.log(`最终回复：${assistantOutput.content}`);
        }
      };

      main().catch(console.error);
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <Note>
      `qwen3.8-max` 使用 `MultiModalConversation` 接口。`qwen-plus` 和 `qwen3-max` 等模型使用 `Generation` 接口，示例请参阅[文本生成快速开始](/developer-guides/text-generation/quickstart)。
    </Note>

    <CodeGroup>
      ```python Python
      import os
      from dashscope import MultiModalConversation
      import dashscope
      import json
      import random
      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      # 1. 定义工具列表
      tools = [
        {
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "description": "当你需要查询某个城市的天气时使用。",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "城市名称，如北京、纽约等。",
                }
              },
              "required": ["location"],
            },
          },
        }
      ]

      # 2. 模拟天气查询工具
      def get_current_weather(arguments):
        weather_conditions = ["sunny", "cloudy", "rainy"]
        random_weather = random.choice(weather_conditions)
        location = arguments["location"]
        return f"{location} is {random_weather} today."

      # 3. 封装模型调用函数
      def get_response(messages):
        response = MultiModalConversation.call(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="qwen3.8-max",
          messages=messages,
          tools=tools,
        )
        return response

      # 4. 初始化对话历史
      messages = [
        {
          "role": "user",
          "content": "北京天气怎么样？"
        }
      ]

      # 5. 第一次模型调用
      response = get_response(messages)
      assistant_output = response.output.choices[0].message
      messages.append(assistant_output)

      # 6. 判断是否需要调用工具
      if "tool_calls" not in assistant_output or not assistant_output["tool_calls"]:
        print(f"无需调用工具。直接回复：{assistant_output['content'][0]['text']}")
      else:
        # 7. 进入工具调用循环
        while "tool_calls" in assistant_output and assistant_output["tool_calls"]:
          tool_call = assistant_output["tool_calls"][0]
          func_name = tool_call["function"]["name"]
          arguments = json.loads(tool_call["function"]["arguments"])
          tool_call_id = tool_call.get("id")
          print(f"调用工具 [{func_name}]，参数：{arguments}")
          tool_result = get_current_weather(arguments)
          tool_message = {
            "role": "tool",
            "content": tool_result,
            "tool_call_id": tool_call_id
          }
          print(f"工具返回结果：{tool_message['content']}")
          messages.append(tool_message)
          response = get_response(messages)
          assistant_output = response.output.choices[0].message
          messages.append(assistant_output)
        # 8. 输出最终自然语言回复
        print(f"最终回复：{assistant_output['content'][0]['text']}")
      ```

      ```java Java
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.tools.FunctionDefinition;
      import com.alibaba.dashscope.tools.ToolCallBase;
      import com.alibaba.dashscope.tools.ToolCallFunction;
      import com.alibaba.dashscope.tools.ToolFunction;
      import com.alibaba.dashscope.utils.Constants;
      import com.alibaba.dashscope.utils.JsonUtils;
      import com.fasterxml.jackson.databind.JsonNode;
      import com.fasterxml.jackson.databind.ObjectMapper;

      import java.util.ArrayList;
      import java.util.Arrays;
      import java.util.Collections;
      import java.util.List;
      import java.util.Random;

      public class Main {
          static {
              Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
          }

          public static String getCurrentWeather(String arguments) {
              try {
                  ObjectMapper objectMapper = new ObjectMapper();
                  JsonNode argsNode = objectMapper.readTree(arguments);
                  String location = argsNode.get("location").asText();
                  List<String> weatherConditions = Arrays.asList("sunny", "cloudy", "rainy");
                  String randomWeather = weatherConditions.get(new Random().nextInt(weatherConditions.size()));
                  return location + " is " + randomWeather + " today.";
              } catch (Exception e) {
                  return "无法解析 location 参数。";
              }
          }

          public static void main(String[] args) {
              try {
                  String weatherParamsSchema =
                          "{\"type\":\"object\",\"properties\":{\"location\":{\"type\":\"string\",\"description\":\"城市名称，如北京、纽约等。\"}},\"required\":[\"location\"]}";

                  FunctionDefinition weatherFunction = FunctionDefinition.builder()
                          .name("get_current_weather")
                          .description("当你需要查询某个城市的天气时使用。")
                          .parameters(JsonUtils.parseString(weatherParamsSchema).getAsJsonObject())
                          .build();
                  MultiModalConversation conv = new MultiModalConversation();
                  String userInput = "北京天气怎么样？";

                  List<MultiModalMessage> messages = new ArrayList<>();
                  messages.add(MultiModalMessage.builder()
                          .role(Role.USER.getValue())
                          .content(List.of(Collections.singletonMap("text", userInput)))
                          .build());

                  MultiModalConversationParam param = MultiModalConversationParam.builder()
                          .model("qwen3.8-max")
                          .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                          .messages(messages)
                          .tools(Arrays.asList(ToolFunction.builder().function(weatherFunction).build()))
                          .build();

                  MultiModalConversationResult result = conv.call(param);
                  MultiModalMessage assistantOutput = result.getOutput().getChoices().get(0).getMessage();
                  messages.add(assistantOutput);

                  if (assistantOutput.getToolCalls() == null || assistantOutput.getToolCalls().isEmpty()) {
                      System.out.println("无需调用天气工具。直接回复：" + assistantOutput.getContent().get(0).get("text"));
                  } else {
                      while (assistantOutput.getToolCalls() != null && !assistantOutput.getToolCalls().isEmpty()) {
                          ToolCallBase toolCall = assistantOutput.getToolCalls().get(0);
                          ToolCallFunction functionCall = (ToolCallFunction) toolCall;
                          String funcName = functionCall.getFunction().getName();
                          String arguments = functionCall.getFunction().getArguments();
                          System.out.println("调用工具 [" + funcName + "]，参数：" + arguments);

                          String toolResult = getCurrentWeather(arguments);
                          MultiModalMessage toolMessage = MultiModalMessage.builder()
                                  .role("tool")
                                  .toolCallId(toolCall.getId())
                                  .content(List.of(Collections.singletonMap("text", toolResult)))
                                  .build();
                          System.out.println("工具返回结果：" + toolMessage.getContent().get(0).get("text"));
                          messages.add(toolMessage);

                          param.setMessages(messages);
                          result = conv.call(param);
                          assistantOutput = result.getOutput().getChoices().get(0).getMessage();
                          messages.add(assistantOutput);
                      }
                      System.out.println("最终回复：" + assistantOutput.getContent().get(0).get("text"));
                  }

              } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.err.println("Error: " + e.getMessage());
              } catch (Exception e) {
                  e.printStackTrace();
              }
          }
      }
      ```
    </CodeGroup>

    运行代码后输出如下：

    ```text Output
    调用工具 [get_current_weather]，参数：{'location': 'Beijing'}
    工具返回结果：Beijing is cloudy today.
    最终回复：今天北京的天气是多云。
    ```
  </Tab>
</Tabs>

## 工具 schema 参考

每个工具是一个 JSON 对象，结构如下：

```json
{
  "type": "function",
  "function": {
    "name": "get_current_weather",
    "description": "当你需要查询某个城市的天气时使用。",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "城市名称，如北京、纽约等。"
        }
      },
      "required": ["location"]
    }
  }
}
```

| 字段                               | 说明                                     |
| -------------------------------- | -------------------------------------- |
| `type`                           | 固定为 `"function"`。                      |
| `function.name`                  | 函数名称，必须与应用程序中实际执行的函数名一致。               |
| `function.description`           | 工具的用途描述。模型根据该描述判断是否调用工具。               |
| `function.parameters`            | JSON Schema 对象，描述函数的输入参数。如果函数无需输入，可省略。 |
| `function.parameters.properties` | 每个键为参数名称，值描述参数的类型和用途。                  |
| `function.parameters.required`   | 必填参数名称的数组。                             |

<Tip>
  编写清晰、具体的描述。模型依赖 `description` 字段来选择正确的工具并提取正确的参数。
</Tip>

## 工具调用行为控制

### 并行工具调用

默认情况下，模型每次响应只返回一个工具调用。如果用户的请求需要多个独立的工具调用（如"北京和上海的天气分别怎么样？"），可将 `parallel_tool_calls` 设为 `true`：

<CodeGroup>
  ```python Python
  completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    tools=tools,
    parallel_tool_calls=True
  )
  ```

  ```javascript Node.js
  const completion = await openai.chat.completions.create({
    model: "qwen3.8-max",
    messages: messages,
    tools: tools,
    parallel_tool_calls: true
  });
  ```
</CodeGroup>

此时 `tool_calls` 数组会包含多个条目：

```json
{
  "role": "assistant",
  "tool_calls": [
    {
      "function": { "name": "get_current_weather", "arguments": "{\"location\": \"Beijing\"}" },
      "index": 0, "id": "call_c2d8a3a2...", "type": "function"
    },
    {
      "function": { "name": "get_current_weather", "arguments": "{\"location\": \"Shanghai\"}" },
      "index": 1, "id": "call_dc7f2f67...", "type": "function"
    }
  ]
}
```

<Note>
  仅在任务相互独立时使用并行工具调用。如果任务之间存在依赖关系（如工具 A 的输入依赖工具 B 的输出），请使用快速开始中的 while 循环串行调用工具。
</Note>

### 强制工具调用（tool\_choice）

`tool_choice` 参数控制模型是否调用工具。默认值为 `"auto"`（由模型自行决定）。

- **强制调用指定工具**：将 `tool_choice` 设为 `{"type": "function", "function": {"name": "get_current_weather"}}`。模型跳过工具选择，始终调用指定函数。

- **禁止调用工具**：将 `tool_choice` 设为 `"none"`。模型直接回复，不调用任何工具。

<CodeGroup>
  ```python Python
  # 强制调用指定工具
  completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "get_current_weather"}},
    extra_body={"enable_thinking": False}
  )

  # 禁止调用工具
  completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
    tools=tools,
    tool_choice="none"
  )
  ```

  ```javascript Node.js
  // 强制调用指定工具
  const completion = await openai.chat.completions.create({
    model: "qwen3.8-max",
    messages: messages,
    tools: tools,
    tool_choice: {type: "function", function: {name: "get_current_weather"}},
    enable_thinking: false
  });

  // 禁止调用工具
  const completion2 = await openai.chat.completions.create({
    model: "qwen3.8-max",
    messages: messages,
    tools: tools,
    tool_choice: "none"
  });
  ```
</CodeGroup>

<Note>
  `qwen3.7-plus` 等模型默认开启思考模式。思考模式下 `tool_choice` 仅支持 `"auto"` 或 `"none"`。要强制调用指定工具，需先将 `enable_thinking` 设为 `false` 关闭思考模式。
</Note>

> 在汇总工具输出时，需移除 `tool_choice` 参数。否则 API 仍会返回工具调用信息，而非自然语言回复。

## 多轮对话

用户可能在第一轮问"北京天气怎么样？"，第二轮接着问"上海呢？"。如果没有第一轮的上下文，模型无法判断应调用哪个工具。在多轮对话中，每轮结束后保留 messages 数组，然后添加新的用户消息并再次调用 function calling。messages 结构如下：

```json
[
  "系统消息 -- 引导模型调用工具的策略",
  "用户消息 -- 用户问题",
  "助手消息 -- 模型返回的工具调用信息",
  "工具消息 -- 工具输出结果",
  "助手消息 -- 模型对工具调用信息的总结",
  "用户消息 -- 用户的第二个问题"
]
```

## 流式输出

<Tip>
  关于流式输出的基本概念（SSE 协议、如何开启流式、计费和 Token 用量），请参阅[流式输出](/developer-guides/run-and-scale/streaming)。
</Tip>

在 function calling 中使用流式输出时，工具调用信息会分块返回：

- **工具函数名称**：在第一个 chunk 中返回。
- **工具调用参数**：在后续 chunk 中增量返回。

在解析 JSON 之前，需先拼接参数片段。在请求中添加 `stream=True`，然后拼接各个 chunk：

<CodeGroup>
  ```python Python
  tool_calls = {}
  for response_chunk in stream:
    delta_tool_calls = response_chunk.choices[0].delta.tool_calls
    if delta_tool_calls:
      for tool_call_chunk in delta_tool_calls:
        call_index = tool_call_chunk.index
        tool_call_chunk.function.arguments = tool_call_chunk.function.arguments or ""
        if call_index not in tool_calls:
          tool_calls[call_index] = tool_call_chunk
        else:
          tool_calls[call_index].function.arguments += tool_call_chunk.function.arguments
  print(tool_calls[0].model_dump_json())
  ```

  ```javascript Node.js
  const toolCalls = {};
  for await (const responseChunk of stream) {
    const deltaToolCalls = responseChunk.choices[0]?.delta?.tool_calls;
    if (deltaToolCalls) {
      for (const toolCallChunk of deltaToolCalls) {
        const index = toolCallChunk.index;
        toolCallChunk.function.arguments = toolCallChunk.function.arguments || "";
        if (!toolCalls[index]) {
          toolCalls[index] = { ...toolCallChunk };
          if (!toolCalls[index].function) {
              toolCalls[index].function = { name: '', arguments: '' };
          }
        }
        else if (toolCallChunk.function?.arguments) {
          toolCalls[index].function.arguments += toolCallChunk.function.arguments;
        }
      }
    }
  }
  console.log(JSON.stringify(toolCalls[0]));
  ```
</CodeGroup>

构建第二次模型调用的 assistant 消息时，将 `tool_calls` 字段替换为拼接后的完整内容。

## Responses API

[Responses API](/api-reference/chat/openai-responses) 的工具调用响应格式有所不同。工具调用不是通过 assistant 消息中的 `tool_calls` 返回，而是以 `function_call` 条目出现在 `output` 数组中。

**第 1 步 -- 在请求中传入工具定义**：

```python Python
from openai import OpenAI
import os

client = OpenAI(
  api_key=os.getenv("DASHSCOPE_API_KEY"),
  base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

tools = [
  {
    "type": "function",
    "name": "get_current_weather",
    "description": "当你需要查询某个城市的天气时使用。",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "城市名称，如北京、纽约等。",
        }
      },
      "required": ["location"],
    },
  },
]

response = client.responses.create(
  model="qwen3.8-max",
  tools=tools,
  input="北京天气怎么样？",
)
```

**第 2 步 -- 解析 function\_call 输出项**：

响应的 `output` 数组包含一个 `function_call` 条目：

```json
{
  "type": "function_call",
  "id": "fc_12345",
  "call_id": "call_xxx",
  "name": "get_current_weather",
  "arguments": "{\"location\": \"Beijing\"}"
}
```

**第 3 步 -- 返回工具执行结果**：

执行函数后，通过 `function_call_output` 条目将结果传回：

```python Python
tool_result = get_current_weather({"location": "Beijing"})
response = client.responses.create(
  model="qwen3.8-max",
  tools=tools,
  input=[
    {"type": "message", "role": "user", "content": "北京天气怎么样？"},
    response.output[0],  # function_call 条目
    {
      "type": "function_call_output",
      "call_id": response.output[0].call_id,
      "output": tool_result,
    },
  ],
)
print(response.output_text)
```

<Note>
  在 Responses API 中，工具定义采用扁平结构（`name` 和 `parameters` 在顶层），而非 Chat Completions 中嵌套的 `function` 包装。详见 [Responses API](/api-reference/chat/openai-responses)。
</Note>

## Qwen-Omni

在工具信息获取阶段，`Qwen3.5-Omni` 和 `Qwen3-Omni-Flash` 与其他模型有两点不同：

- **必须使用流式输出**： 获取工具信息时需设置 `stream=True`。

- **建议仅输出文本**： 设置 `modalities=["text"]` 以避免工具选择阶段产生不必要的音频输出。

> 关于 Qwen-Omni 模型的详细信息，请参阅[音视频文件理解](/developer-guides/speech/multimodal-speech)。

<CodeGroup>
  ```python Python
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
        "name": "get_current_weather",
        "description": "当你需要查询某个城市的天气时使用。",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "城市名称，如北京、纽约等。",
            }
          },
          "required": ["location"],
        },
      },
    },
  ]

  completion = client.chat.completions.create(
    model="qwen3-omni-flash",
    messages=[{"role": "user", "content": "北京天气怎么样？"}],
    modalities=["text"],
    stream=True,
    tools=tools
  )

  for chunk in completion:
    if chunk.choices:
      delta = chunk.choices[0].delta
      print(delta.tool_calls)
  ```

  ```javascript Node.js
  import { OpenAI } from "openai";

  const openai = new OpenAI(
    {
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
  );
  const tools = [
    {
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "description": "当你需要查询某个城市的天气时使用。",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "城市名称，如北京、纽约等。"
            }
          },
          "required": ["location"]
        }
      }
    }
  ];

  const stream = await openai.chat.completions.create({
    model: "qwen3-omni-flash",
    messages: [
      {
        "role": "user",
        "content": "北京天气怎么样？"
      }],
    stream: true,
    modalities: ["text"],
    tools: tools
  });

  for await (const chunk of stream) {
    if (chunk.choices?.length){
      const delta = chunk.choices[0].delta;
      console.log(delta.tool_calls);
    }
  }
  ```
</CodeGroup>

运行代码后输出如下：

```text Output
[ChoiceDeltaToolCall(index=0, id='call_391c8e5787bc4972a388aa', function=ChoiceDeltaToolCallFunction(arguments=None, name='get_current_weather'), type='function')]
[ChoiceDeltaToolCall(index=0, id='call_391c8e5787bc4972a388aa', function=ChoiceDeltaToolCallFunction(arguments=' {"location": "Beijing"}', name=None), type='function')]
None
```

参数 chunk 的拼接方法请参阅上方流式输出章节。

### Qwen-Omni-Realtime

Qwen3.5-Omni-Plus-Realtime、Qwen3.5-Omni-Flash-Realtime 系列支持工具调用，适用于语音对话场景，通过 DashScope SDK 或 WebSocket 原生协议调用。建立 WebSocket 连接后，通过 `session.update` 传入工具定义即可进入交互流程。

<Note>
  Qwen-Omni-Realtime 系列不支持 `tool_choice` 和 `parallel_tool_calls` 参数。
</Note>

> 详细代码示例请参阅[实时语音对话](/developer-guides/speech/realtime-multimodal-speech)。

## 思考模式

深度思考模型在生成工具调用之前会先进行推理。设置 `enable_thinking=True` 可查看模型的推理过程。响应中会在工具调用之前包含 `reasoning_content`：

1. 模型输出 `reasoning_content`，展示其对用户意图的分析、工具选择和参数规划过程。
2. 模型随后正常输出 `tool_calls`。

在后续请求中传回 assistant 消息时，必须包含 `reasoning_content` 字段。

<Note>
  开启思考模式后，`tool_choice` 参数仅支持 `"auto"`（默认）或 `"none"`。
</Note>

```python Python
completion = client.chat.completions.create(
  model="qwen3.8-max",  # 使用支持思考的模型
  messages=messages,
  tools=tools,
  extra_body={"enable_thinking": True},
  stream=True,
)
```

包含 `reasoning_content` 处理的完整流式解析代码，请参阅[思考模式](/developer-guides/text-generation/thinking)。

## 最佳实践

- **测试工具选择准确率**：构建贴合实际场景的评估数据集，跟踪工具选择准确率、参数提取准确率和端到端成功率。
- **优化工具描述**：当模型选错工具或提取错误参数时，先改进描述和 system prompt，再考虑升级模型。
- **控制候选工具数量**：传给模型的工具不超过 20 个。对于大型工具库，使用路由层（语义搜索、关键词过滤或轻量级 LLM 路由）进行预筛选。
- **遵循最小权限原则**：默认使用只读工具。不要让模型直接执行危险操作（代码执行、文件删除、资金转账）。
- **写操作需人工确认**：模型可以生成操作请求，但不可逆操作（发送邮件、修改数据）应要求用户确认。
- **设置超时并提供降级回复**：为每个步骤设置独立超时。失败时返回明确提示，如"抱歉，当前无法获取该信息，请稍后重试。"
- **在 UI 中展示进度**：工具执行开始时显示类似"正在为您查询天气..."的提示。

## 通过 system message 传递工具信息

<Accordion title="替代方案：在 system prompt 中嵌入工具信息">
  推荐使用 `tools` 参数（本指南通篇使用的方式）。如果需要直接控制工具提示词，可使用以下模板将工具定义嵌入 system message：

  ```python Python
  import os
  from openai import OpenAI
  import json

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  tools = [
    {
      "type": "function",
      "function": {
        "name": "get_current_time",
        "description": "当你需要知道当前时间时使用。",
        "parameters": {}
      }
    },
    {
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "description": "当你需要查询某个城市的天气时使用。",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "城市名称，如北京、纽约等。"
            }
          },
          "required": ["location"]
        }
      }
    }
  ]

  custom_prompt = "You are a helpful assistant."
  tools_content = "\n".join(json.dumps(tool, ensure_ascii=False) for tool in tools)

  system_prompt = f"""{custom_prompt}

  # Tools

  You may call one or more functions to assist with the user query.

  You are provided with function signatures within <tools></tools> XML tags:
  <tools>
  {tools_content}
  </tools>

  For each function call, return a json object with function name and arguments within <tool_call></tool_call> XML tags:
  <tool_call>
  {{"name": <function-name>, "arguments": <args-json-object>}}
  </tool_call>"""

  messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": "现在几点了？"}
  ]

  completion = client.chat.completions.create(
    model="qwen3.8-max",
    messages=messages,
  )
  print(completion.choices[0].message.content)
  ```

  运行代码后，使用 XML 解析器从 `<tool_call>` 和 `</tool_call>` 标签之间提取工具调用信息。
</Accordion>

## 计费

除 messages 数组中的 Token 外，工具描述也会计入输入 Token，作为 prompt 的一部分计费。

## 错误码

调用失败时，请参阅[错误信息](/api-reference/preparation/error-messages)。
