> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 意图理解（Tongyi-Intent-Detect）

> tongyi-intent-detect-v3 能够在百毫秒级时间内快速、准确地解析用户意图，并选择合适的工具来解决用户的问题。

## 模型概述

tongyi-intent-detect-v3 是千问AI平台提供的意图理解模型，专为快速意图解析和工具选择场景设计。该模型具备以下核心能力：

- **毫秒级意图解析**：在百毫秒级时间内完成用户意图识别
- **工具选择**：根据用户请求自动匹配并调用合适的工具
- **多轮对话支持**：当用户信息不足时，模型会主动追问以补全必要参数

## 使用方法

**前提条件**：已[获取 API Key](/api-reference/preparation/api-key)。如果通过 SDK 调用，需要安装最新版 SDK。

模型支持三种工作模式，通过 System Message 中的关键字控制：

| 模式        | 关键字                               | 输出内容               |
| --------- | --------------------------------- | ------------------ |
| 意图 + 函数调用 | `Response in INTENT_MODE.`        | 意图标签、工具调用信息、自然语言回复 |
| 仅意图识别     | `Just reply with the chosen tag.` | 意图分类标签             |
| 仅函数调用     | `Response in NORMAL_MODE.`        | 工具调用信息             |

### 意图 + 函数调用

同时输出意图标签和函数调用信息。您需要在 System Message 中声明 `Response in INTENT_MODE.` 并提供工具列表。

**System Message 格式**：

```text
You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:
{工具信息}
Response in INTENT_MODE.
```

**工具信息格式**：

```json
[
  {
    "name": "工具名称",
    "description": "工具描述",
    "parameters": {
      "type": "object",
      "properties": {
        "parameter_1": {
          "description": "参数描述",
          "type": "参数类型",
          "default": "默认值"
        }
      },
      "required": ["parameter_1"]
    }
  }
]
```

#### 请求示例

以下示例使用时间查询和天气查询两个工具：

<Tabs>
  <Tab title="OpenAI 兼容">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from openai import OpenAI

        # 定义工具
        tools = [
          {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
          },
          {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                }
              },
              "required": ["location"]
            }
          }
        ]

        tools_string = json.dumps(tools, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:
        {tools_string}
        Response in INTENT_MODE."""

        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        messages = [
          {'role': 'system', 'content': system_prompt},
          {'role': 'user', 'content': "杭州天气"}
        ]
        response = client.chat.completions.create(
          model="tongyi-intent-detect-v3",
          messages=messages
        )

        print(response.choices[0].message.content)
        ```
      </Tab>

      <Tab title="cURL">
        ```bash
        curl -X POST "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "tongyi-intent-detect-v3",
          "messages": [
            {
              "role": "system",
              "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:\n[{\"name\": \"get_current_time\", \"description\": \"当你想知道现在的时间时非常有用。\", \"parameters\": {}}, {\"name\": \"get_current_weather\", \"description\": \"当你想查询指定城市的天气时非常有用。\", \"parameters\": {\"type\": \"object\", \"properties\": {\"location\": {\"type\": \"string\", \"description\": \"城市或县区，比如北京市、杭州市、余杭区等。\"}}, \"required\": [\"location\"]}}]\nResponse in INTENT_MODE."
            },
            {
              "role": "user",
              "content": "杭州天气"
            }
          ]
        }'
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from dashscope import Generation

        # 定义工具
        tools = [
          {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
          },
          {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                }
              },
              "required": ["location"]
            }
          }
        ]

        tools_string = json.dumps(tools, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:
        {tools_string}
        Response in INTENT_MODE."""

        messages = [
          {'role': 'system', 'content': system_prompt},
          {'role': 'user', 'content': "杭州天气"}
        ]
        response = Generation.call(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="tongyi-intent-detect-v3",
          messages=messages,
          result_format="message"
        )

        print(response.output.choices[0].message.content)
        ```
      </Tab>

      <Tab title="cURL">
        ```bash
        curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation" \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "tongyi-intent-detect-v3",
          "input": {
            "messages": [
              {
                "role": "system",
                "content": "You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:\n[{\"name\": \"get_current_time\", \"description\": \"当你想知道现在的时间时非常有用。\", \"parameters\": {}}, {\"name\": \"get_current_weather\", \"description\": \"当你想查询指定城市的天气时非常有用。\", \"parameters\": {\"type\": \"object\", \"properties\": {\"location\": {\"type\": \"string\", \"description\": \"城市或县区，比如北京市、杭州市、余杭区等。\"}}, \"required\": [\"location\"]}}]\nResponse in INTENT_MODE."
              },
              {
                "role": "user",
                "content": "杭州天气"
              }
            ]
          },
          "parameters": {
            "result_format": "message"
          }
        }'
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

#### 响应示例

```text
<tags>
[function call, json response]
</tags><tool_call>
[{"name": "get_current_weather", "arguments": {"location": "杭州市"}}]
</tool_call><content>

</content>
```

#### 解析响应

使用以下 `parse_text` 函数解析返回的工具与参数信息：

```python
import re
import json

def parse_text(text):
  # 定义正则表达式模式来匹配 <tags>, <tool_call>, <content> 及其内容
  tags_pattern = r'<tags>(.*?)</tags>'
  tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
  content_pattern = r'<content>(.*?)</content>'
  # 使用正则表达式查找匹配的内容
  tags_match = re.search(tags_pattern, text, re.DOTALL)
  tool_call_match = re.search(tool_call_pattern, text, re.DOTALL)
  content_match = re.search(content_pattern, text, re.DOTALL)
  # 提取匹配的内容，如果没有匹配到则返回空字符串
  tags = tags_match.group(1).strip() if tags_match else ""
  tool_call_str = tool_call_match.group(1).strip() if tool_call_match else ""
  tool_call = json.loads(tool_call_str) if tool_call_str else []
  content = content_match.group(1).strip() if content_match else ""
  # 将提取的内容存储在字典中
  result = {
    "tags": tags,
    "tool_call": tool_call,
    "content": content
  }
  return result
```

解析后的输出：

```json
{
  "tags": "[function call, json response]",
  "tool_call": [
    {
      "name": "get_current_weather",
      "arguments": {
        "location": "杭州市"
      }
    }
  ],
  "content": ""
}
```

### 仅意图识别

只输出意图分类标签，不返回函数调用信息。您需要在 System Message 中提供意图列表，并声明 `Just reply with the chosen tag.`。

**System Message 格式**：

```text
You are Qwen, created by Alibaba Cloud. You are a helpful assistant.
You should choose one tag from the tag list:
{意图信息}
Just reply with the chosen tag.
```

**意图信息格式**：

```json
{
  "意图1": "意图1的描述",
  "意图2": "意图2的描述",
  "意图3": "意图3的描述"
}
```

#### 请求示例

<Tabs>
  <Tab title="OpenAI 兼容">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from openai import OpenAI

        intent_dict = {
          "play_game": "玩游戏",
          "email_querycontact": "电子邮件查询联系人",
          "general_quirky": "quirky",
          "email_addcontact": "电子邮件添加联系人",
          "takeaway_query": "外卖查询",
          "recommendation_locations": "地点推荐",
          "transport_traffic": "交通运输",
          "iot_cleaning": "物联网-吸尘器, 清洁器",
          "general_joke": "笑话",
          "lists_query": "查询列表/清单",
          "calendar_remove": "日历删除事件",
          "transport_taxi": "打车, 出租车预约",
          "qa_factoid": "事实性问答",
          "transport_ticket": "交通票据",
          "play_radio": "播放广播",
          "alarm_set": "设置闹钟",
        }

        intent_string = json.dumps(intent_dict, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant.
        You should choose one tag from the tag list:
        {intent_string}
        Just reply with the chosen tag."""

        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        messages = [
          {'role': 'system', 'content': system_prompt},
          {'role': 'user', 'content': "星期五早上九点叫醒我"}
        ]
        response = client.chat.completions.create(
          model="tongyi-intent-detect-v3",
          messages=messages
        )

        print(response.choices[0].message.content)
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from dashscope import Generation

        intent_dict = {
          "play_game": "玩游戏",
          "email_querycontact": "电子邮件查询联系人",
          "general_quirky": "quirky",
          "email_addcontact": "电子邮件添加联系人",
          "takeaway_query": "外卖查询",
          "recommendation_locations": "地点推荐",
          "transport_traffic": "交通运输",
          "iot_cleaning": "物联网-吸尘器, 清洁器",
          "general_joke": "笑话",
          "lists_query": "查询列表/清单",
          "calendar_remove": "日历删除事件",
          "transport_taxi": "打车, 出租车预约",
          "qa_factoid": "事实性问答",
          "transport_ticket": "交通票据",
          "play_radio": "播放广播",
          "alarm_set": "设置闹钟",
        }

        intent_string = json.dumps(intent_dict, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant.
        You should choose one tag from the tag list:
        {intent_string}
        Just reply with the chosen tag."""

        messages = [
          {'role': 'system', 'content': system_prompt},
          {'role': 'user', 'content': "周五早上九点叫醒我"}
        ]
        response = Generation.call(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="tongyi-intent-detect-v3",
          messages=messages,
          result_format="message"
        )

        print(response.output.choices[0].message.content)
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

#### 响应示例

```text
alarm_set
```

#### 提升意图识别的响应速度

为了提升响应速度，您可以将意图分类用单个大写字母指代。这样模型只需输出一个 Token，可以显著优化响应时间。

<Tabs>
  <Tab title="OpenAI 兼容">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from openai import OpenAI

        intent_dict = {
          "A": "玩游戏",
          "B": "电子邮件查询联系人",
          "C": "quirky",
          "D": "电子邮件添加联系人",
          "E": "外卖查询",
          "F": "地点推荐",
          "G": "交通运输",
          "H": "物联网-吸尘器, 清洁器",
          "I": "笑话",
          "J": "查询列表/清单",
          "K": "日历删除事件",
          "L": "打车, 出租车预约",
          "M": "事实性问答",
          "N": "交通票据",
          "O": "播放广播",
          "P": "设置闹钟",
        }

        intent_string = json.dumps(intent_dict, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant.
        You should choose one tag from the tag list:
        {intent_string}
        Just reply with the chosen tag."""

        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        messages = [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": "从北京去杭州最早的飞机是？"},
        ]
        response = client.chat.completions.create(
          model="tongyi-intent-detect-v3",
          messages=messages
        )

        print(response.choices[0].message.content)
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from dashscope import Generation

        intent_dict = {
          "A": "玩游戏",
          "B": "电子邮件查询联系人",
          "C": "quirky",
          "D": "电子邮件添加联系人",
          "E": "外卖查询",
          "F": "地点推荐",
          "G": "交通运输",
          "H": "物联网-吸尘器, 清洁器",
          "I": "笑话",
          "J": "查询列表/清单",
          "K": "日历删除事件",
          "L": "打车, 出租车预约",
          "M": "事实性问答",
          "N": "交通票据",
          "O": "播放广播",
          "P": "设置闹钟",
        }

        intent_string = json.dumps(intent_dict, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant.
        You should choose one tag from the tag list:
        {intent_string}
        Just reply with the chosen tag."""

        messages = [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": "从北京去杭州最早的飞机是？"},
        ]
        response = Generation.call(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="tongyi-intent-detect-v3",
          messages=messages,
          result_format="message",
        )

        print(response.output.choices[0].message.content)
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

运行代码后可以得到一个 Token 的意图分类结果：

```text
M
```

### 仅函数调用

只输出函数调用信息，不返回意图标签。您需要在 System Message 中声明 `Response in NORMAL_MODE.` 并提供工具列表。

**System Message 格式**：

```text
You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:
{工具信息}
Response in NORMAL_MODE.
```

工具信息格式与[意图 + 函数调用](#意图-函数调用)中相同。

#### 请求示例

<Tabs>
  <Tab title="OpenAI 兼容">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from openai import OpenAI

        # 定义工具
        tools = [
          {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
          },
          {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                }
              },
              "required": ["location"]
            }
          }
        ]

        tools_string = json.dumps(tools, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:
        {tools_string}
        Response in NORMAL_MODE."""

        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        messages = [
          {'role': 'system', 'content': system_prompt},
          {'role': 'user', 'content': "杭州天气"}
        ]
        response = client.chat.completions.create(
          model="tongyi-intent-detect-v3",
          messages=messages
        )

        print(response.choices[0].message.content)
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from dashscope import Generation

        # 定义工具
        tools = [
          {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {}
          },
          {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                }
              },
              "required": ["location"]
            }
          }
        ]

        tools_string = json.dumps(tools, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:
        {tools_string}
        Response in NORMAL_MODE."""

        messages = [
          {'role': 'system', 'content': system_prompt},
          {'role': 'user', 'content': "杭州天气"}
        ]
        response = Generation.call(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="tongyi-intent-detect-v3",
          messages=messages,
          result_format="message"
        )

        print(response.output.choices[0].message.content)
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

#### 响应示例

```text
<tool_call>
{"name": "get_current_weather", "arguments": {"location": "杭州市"}}
</tool_call>
```

#### 解析响应

使用以下函数解析仅函数调用模式的返回结果：

```python
import re

def parse_text(text):
  tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
  tool_call_match = re.search(tool_call_pattern, text, re.DOTALL)
  tool_call = tool_call_match.group(1).strip() if tool_call_match else ""
  return tool_call
```

解析后的输出：

```json
{"name": "get_current_weather", "arguments": {"location": "杭州市"}}
```

### 多轮对话

当用户未提供充足信息时，模型会主动追问，通过多轮对话采集到必要参数后再输出函数调用信息。

#### 意图 + 函数调用模式

<Tabs>
  <Tab title="OpenAI 兼容">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from openai import OpenAI

        # 定义工具
        tools = [
          {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {},
          },
          {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                }
              },
              "required": ["location"],
            },
          },
        ]

        tools_string = json.dumps(tools, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:
        {tools_string}
        Response in INTENT_MODE."""

        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        messages = [
          {"role": "system", "content": system_prompt},
          # 第一轮对话提出的问题
          {"role": "user", "content": "我想查天气"},
        ]
        response = client.chat.completions.create(
          model="tongyi-intent-detect-v3", messages=messages
        )

        print("查询问题：我想查天气")
        print("第一轮输出：\n")
        print(response.choices[0].message.content)
        messages.append(response.choices[0].message)
        # 第二轮对话提出的问题
        messages.append({"role": "user", "content": "杭州的"})
        response = client.chat.completions.create(
          model="tongyi-intent-detect-v3", messages=messages
        )
        print("\n查询问题：杭州的")
        print("第二轮输出：\n")
        print(response.choices[0].message.content)
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from dashscope import Generation

        # 定义工具
        tools = [
          {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {},
          },
          {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                }
              },
              "required": ["location"],
            },
          },
        ]

        tools_string = json.dumps(tools, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:
        {tools_string}
        Response in INTENT_MODE."""

        messages = [
          {"role": "system", "content": system_prompt},
          # 第一轮对话提出的问题
          {"role": "user", "content": "我想查天气"},
        ]
        response = Generation.call(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="tongyi-intent-detect-v3",
          messages=messages,
          result_format="message",
        )
        print("查询问题：我想查天气")
        print("第一轮输出：\n")
        print(response.output.choices[0].message.content)

        messages.append(
          {"role": "assistant", "content": response.output.choices[0].message.content}
        )
        # 第二轮对话提出的问题
        messages.append({"role": "user", "content": "杭州"})

        response = Generation.call(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="tongyi-intent-detect-v3",
          messages=messages,
          result_format="message",
        )
        print("\n查询问题：杭州")
        print("第二轮输出：\n")
        print(response.output.choices[0].message.content)
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

**响应示例**：

```text
查询问题：我想查天气
第一轮输出：

<tags>
[weather inquiry]
</tags><tool_call>
[]
</tool_call><content>
好的，请问您想查询哪个城市的天气呢？
</content>

查询问题：杭州
第二轮输出：

<tags>
[function call, json response]
</tags><tool_call>
[{"name": "get_current_weather", "arguments": {"location": "杭州"}}]
</tool_call><content>

</content>
```

#### 仅函数调用模式

<Tabs>
  <Tab title="OpenAI 兼容">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from openai import OpenAI

        # 定义工具
        tools = [
          {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {},
          },
          {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                }
              },
              "required": ["location"],
            },
          },
        ]

        tools_string = json.dumps(tools, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:
        {tools_string}
        Response in NORMAL_MODE."""

        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )
        messages = [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": "我想查天气"},
        ]
        response = client.chat.completions.create(
          model="tongyi-intent-detect-v3", messages=messages
        )

        messages.append(response.choices[0].message)
        print("查询问题：我想查天气")
        print("第一轮输出：\n")
        print(response.choices[0].message.content)
        messages.append({"role": "user", "content": "杭州"})
        response = client.chat.completions.create(
          model="tongyi-intent-detect-v3", messages=messages
        )
        print("\n查询问题：杭州")
        print("第二轮输出：\n")
        print(response.choices[0].message.content)
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import json
        from dashscope import Generation

        # 定义工具
        tools = [
          {
            "name": "get_current_time",
            "description": "当你想知道现在的时间时非常有用。",
            "parameters": {},
          },
          {
            "name": "get_current_weather",
            "description": "当你想查询指定城市的天气时非常有用。",
            "parameters": {
              "type": "object",
              "properties": {
                "location": {
                  "type": "string",
                  "description": "城市或县区，比如北京市、杭州市、余杭区等。",
                }
              },
              "required": ["location"],
            },
          },
        ]

        tools_string = json.dumps(tools, ensure_ascii=False)

        system_prompt = f"""You are Qwen, created by Alibaba Cloud. You are a helpful assistant. You may call one or more tools to assist with the user query. The tools you can use are as follows:
        {tools_string}
        Response in NORMAL_MODE."""

        messages = [
          {"role": "system", "content": system_prompt},
          {"role": "user", "content": "我想查天气"},
        ]
        response = Generation.call(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="tongyi-intent-detect-v3",
          messages=messages,
          result_format="message",
        )
        print("查询问题：我想查天气")
        print("第一轮输出：\n")
        print(response.output.choices[0].message.content)
        messages.append(
          {"role": "assistant", "content": response.output.choices[0].message.content}
        )
        messages.append({"role": "user", "content": "杭州"})
        response = Generation.call(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          model="tongyi-intent-detect-v3",
          messages=messages,
          result_format="message",
        )
        print("\n查询问题：杭州")
        print("第二轮输出：\n")
        print(response.output.choices[0].message.content)
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

**响应示例**：

```text
查询问题：我想查天气
第一轮输出：

请问您想查询哪个城市的天气呢？

查询问题：杭州
第二轮输出：

<tool_call>
{"name": "get_current_weather", "arguments": {"location": "杭州"}}
</tool_call>
```

## 常见问题

**Q：最多传入几个工具？**

建议传入不超过 10 个工具，否则模型调用工具的准确率可能会降低。

## API 参考

关于模型的输入与输出参数，请参见[文本生成 API 参考](/api-reference/chat/openai-chat)。
