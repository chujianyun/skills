> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图片搜索

> 通过 Responses API 搜索图片

Responses API 提供两种内置图片搜索工具：**以文搜图**根据文字描述查找匹配的图片，**以图搜图**根据输入图片查找视觉上相似的图片。两种工具均返回 JSON 格式的结果数组和模型生成的分析。

这两种工具仅支持通过 Responses API 调用。

## 以文搜图

在互联网上搜索与文字描述匹配的图片，并由模型对搜索结果进行描述和分析。在 `tools` 参数中传入 `{"type": "web_search_image"}`，模型会根据输入内容自动判断是否触发搜索。

### 示例

<CodeGroup>
  ```python Python {14}
  import os
  import json
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
  )

  response = client.responses.create(
    model="qwen3.7-plus",
    input="找一张适合PPT封面的科技主题背景图",
    tools=[
      {
        "type": "web_search_image"
      }
    ]
  )

  for item in response.output:
    if item.type == "web_search_image_call":
      print(f"[工具调用] 以文搜图（状态：{item.status}）")
      if item.output:
        images = json.loads(item.output)
        print(f"  找到 {len(images)} 张图片：")
        for img in images[:5]:
          print(f"  [{img['index']}] {img['title']}")
          print(f"      {img['url']}")
        if len(images) > 5:
          print(f"  ... 共 {len(images)} 张图片")
    elif item.type == "message":
      print(f"\n[模型回复]")
      print(response.output_text)

  print(f"\n[Token 用量] 输入：{response.usage.input_tokens}，输出：{response.usage.output_tokens}，总计：{response.usage.total_tokens}")
  ```

  ```javascript Node.js {13}
  import OpenAI from "openai";
  import process from 'process';

  const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  });

  async function main() {
    const response = await openai.responses.create({
      model: "qwen3.7-plus",
      input: "找一张适合PPT封面的科技主题背景图",
      tools: [
        { type: "web_search_image" }
      ]
    });

    for (const item of response.output) {
      if (item.type === "web_search_image_call") {
        console.log(`[工具调用] 以文搜图（状态：${item.status}）`);
        if (item.output) {
          const images = JSON.parse(item.output);
          console.log(`  找到 ${images.length} 张图片：`);
          images.slice(0, 5).forEach(img => {
            console.log(`  [${img.index}] ${img.title}`);
            console.log(`      ${img.url}`);
          });
          if (images.length > 5) {
            console.log(`  ... 共 ${images.length} 张图片`);
          }
        }
      } else if (item.type === "message") {
        console.log(`\n[模型回复]`);
        console.log(response.output_text);
      }
    }

    console.log(`\n[Token 用量] 输入：${response.usage.input_tokens}，输出：${response.usage.output_tokens}，总计：${response.usage.total_tokens}`);
  }

  main();
  ```

  ```bash curl {7}
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.7-plus",
    "input": "找一张适合PPT封面的科技主题背景图",
    "tools": [
      {"type": "web_search_image"}
    ]
  }'
  ```
</CodeGroup>

输出示例：

```text
[工具调用] 以文搜图（状态：completed）
  找到 30 张图片：
  [1] Best Free Information Technology Background S Google Slides Themes ...
      https://image.slidesdocs.com/responsive-images/slides/0-technology-line-network-information-training-courseware-powerpoint-background_17825ea41f__960_540.jpg
  [2] Data Technology Blue Abstract Business Glow Powerpoint Background ...
      https://image.slidesdocs.com/responsive-images/background/data-technology-blue-abstract-business-glow-powerpoint-background_e667bfafcb__960_540.jpg
  ...

[模型回复]
以下是几张非常适合您PPT封面的科技主题背景图……

[Token 用量] 输入：4326，输出：645，总计：4971
```

### 响应格式

响应的 `output` 数组包含两种类型的元素：

| 类型                      | 说明                                                  |
| ----------------------- | --------------------------------------------------- |
| `web_search_image_call` | 原始搜索结果，为 JSON 数组。每个对象包含 `index`、`title` 和 `url` 字段。 |
| `message`               | 模型基于搜索结果生成的分析和推荐。                                   |

### 计费

以文搜图涉及两项费用：

<Note>
  以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
</Note>

| 费用类型  | 说明                                                                                         |
| ----- | ------------------------------------------------------------------------------------------ |
| 模型调用费 | 图片搜索结果会添加到提示中，增加输入 Token 数量，按模型标准费率计费。详见[计费说明](/developer-guides/getting-started/pricing)。 |
| 工具调用费 | 每 1,000 次调用 24 元。                                                                          |

## 以图搜图

根据输入图片在互联网上查找视觉上相似的图片，并由模型分析搜索结果。在 `tools` 参数中传入 `{"type": "image_search"}`，通过 `input_image` 内容类型提供图片。可选传入 `input_text` 消息，提供额外的搜索上下文。

### 示例

将示例代码中的 `image_url` 替换为可公开访问的图片 URL（OpenAI SDK 不支持本地文件路径）。

<CodeGroup>
  ```python Python {17}
  import os
  import json
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
  )

  input_content = [
    {"type": "input_text", "text": "查找与这张图风格相似的风景图"},
    {"type": "input_image", "image_url": "https://img.alicdn.com/imgextra/i4/O1CN01YbrnSS1qtmsAkw0Ud_!!6000000005554-2-tps-788-450.png"}
  ]

  response = client.responses.create(
    model="qwen3.7-plus",
    input=[{"role": "user", "content": input_content}],
    tools=[{"type": "image_search"}]
  )

  for item in response.output:
    if item.type == "image_search_call":
      print(f"[工具调用] 以图搜图（状态：{item.status}）")
      if item.output:
        images = json.loads(item.output)
        print(f"  找到 {len(images)} 张图片：")
        for img in images[:5]:
          print(f"  [{img['index']}] {img['title']}")
          print(f"      {img['url']}")
        if len(images) > 5:
          print(f"  ... 共 {len(images)} 张图片")
    elif item.type == "message":
      print(f"\n[模型回复]")
      print(response.output_text)

  print(f"\n[Token 用量] 输入：{response.usage.input_tokens}，输出：{response.usage.output_tokens}，总计：{response.usage.total_tokens}")
  ```

  ```javascript Node.js {20}
  import OpenAI from "openai";
  import process from 'process';

  const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  });

  async function main() {
    const response = await openai.responses.create({
      model: "qwen3.7-plus",
      input: [
        {
          role: "user",
          content: [
            { type: "input_text", text: "查找与这张图风格相似的风景图" },
            { type: "input_image", image_url: "https://img.alicdn.com/imgextra/i4/O1CN01YbrnSS1qtmsAkw0Ud_!!6000000005554-2-tps-788-450.png" }
          ]
        }
      ],
      tools: [{ type: "image_search" }]
    });

    for (const item of response.output) {
      if (item.type === "image_search_call") {
        console.log(`[工具调用] 以图搜图（状态：${item.status}）`);
        if (item.output) {
          const images = JSON.parse(item.output);
          console.log(`  找到 ${images.length} 张图片：`);
          images.slice(0, 5).forEach(img => {
            console.log(`  [${img.index}] ${img.title}`);
            console.log(`      ${img.url}`);
          });
          if (images.length > 5) {
            console.log(`  ... 共 ${images.length} 张图片`);
          }
        }
      } else if (item.type === "message") {
        console.log(`\n[模型回复]`);
        console.log(response.output_text);
      }
    }

    console.log(`\n[Token 用量] 输入：${response.usage.input_tokens}，输出：${response.usage.output_tokens}，总计：${response.usage.total_tokens}`);
  }

  main();
  ```

  ```bash curl {15}
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.7-plus",
    "input": [
      {
        "role": "user",
        "content": [
          {"type": "input_text", "text": "查找与这张图风格相似的风景图"},
          {"type": "input_image", "image_url": "https://img.alicdn.com/imgextra/i4/O1CN01YbrnSS1qtmsAkw0Ud_!!6000000005554-2-tps-788-450.png"}
        ]
      }
    ],
    "tools": [
      {"type": "image_search"}
    ]
  }'
  ```
</CodeGroup>

输出示例：

```text
[工具调用] 以图搜图（状态：completed）
  找到 2 张图片：
  [1] QingMing Festival Holiday Notice 2024
      https://www.healthcabin.net/blog/wp-content/uploads/2024/04/QingMing-Festival-Holiday-Notice-2024.jpg
  [2] Serene Asian Landscape Stone Bridge Reflecting in Misty Water
      https://thumbs.dreamstime.com/b/serene-asian-landscape-stone-bridge-reflecting-misty-water-tranquil-illustration-traditional-arch-spanning-lake-style-376972039.jpg

[模型回复]
好的，我已为您找到几张风格相似的风景图……

[Token 用量] 输入：2753，输出：181，总计：2934
```

### 响应格式

响应的 `output` 数组包含两种类型的元素：

| 类型                  | 说明                                                        |
| ------------------- | --------------------------------------------------------- |
| `image_search_call` | 工具调用结果，包含匹配图片的 JSON 数组。每个对象包含 `index`、`title` 和 `url` 字段。 |
| `message`           | 模型对搜索结果的分析，可通过 `response.output_text` 获取。                 |

### 计费

以图搜图涉及两项费用：

<Note>
  以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
</Note>

| 费用类型       | 说明                                                                                       |
| ---------- | ---------------------------------------------------------------------------------------- |
| 模型输入 Token | 搜索结果会追加到提示中，增加输入 Token 数量，按模型标准费率计费。详见[计费说明](/developer-guides/getting-started/pricing)。 |
| 工具调用费      | 每 1,000 次调用 48 元。                                                                        |

## 支持的模型

两种图片搜索工具支持相同的模型。仅支持通过 Responses API 调用。

### 推荐模型

为获得最佳工具调用效果，推荐使用以下模型：

- 千问Plus：Qwen3.7-Plus 系列、Qwen3.6-Plus 系列、Qwen3.5-Plus 系列
- 千问Max：qwen3.8-max、qwen3.7-max-2026-06-08

### 其他模型

以下模型也支持此工具调用，但效果不如推荐模型。

- 千问Flash：Qwen3.7-Flash 系列、Qwen3.6-Flash 系列、Qwen3.5-Flash 系列
- Qwen3.6 开源系列（qwen3.6-27b 除外）
- Qwen3.5 开源系列

## 流式输出

<Tip>
  流式输出的通用概念（SSE 协议、开启方式、计费和 Token 用量）请参阅[流式输出](/developer-guides/run-and-scale/streaming)。本节仅介绍图片搜索特有的流式行为。
</Tip>

图片搜索可能需要几秒钟。通过设置 `stream=True`（Python）或 `stream: true`（Node.js/curl）开启流式输出，可增量接收结果。响应按以下顺序发送事件：

| 事件类型                          | 触发时机     | 处理方式                                   |
| ----------------------------- | -------- | -------------------------------------- |
| `response.output_item.added`  | 工具调用开始   | 显示加载指示器。                               |
| `response.output_item.done`   | 工具调用完成   | 将 `event.item.output` 解析为 JSON，获取图片列表。 |
| `response.content_part.added` | 模型开始回复   | 准备渲染流式文本。                              |
| `response.output_text.delta`  | 模型发送文本片段 | 将 `event.delta` 追加到输出。                 |
| `response.completed`          | 完整响应就绪   | 读取最终 `usage` 统计信息。                     |

## 常见问题

### 支持哪些图片格式和输入方式？

请参阅[图片限制](/developer-guides/multimodal/vision#输入文件限制)了解支持的格式和大小限制，以及[文件输入方式](/developer-guides/multimodal/vision#文件传入方式)了解图片传入方法。

<Note>OpenAI SDK 不支持本地文件路径输入。</Note>

### 可以传入多少张图片？

所有图片和文本的 Token 总数不能超过模型的最大输入长度。模型每次搜索一张图片，但可在单次响应中多次调用该工具来处理多张图片。

<Note>搜索的图片数量由模型自行决定。</Note>

### 搜索返回多少条结果？

每次搜索返回的结果数量由模型决定，数量不固定，最多返回 100 张图片。
