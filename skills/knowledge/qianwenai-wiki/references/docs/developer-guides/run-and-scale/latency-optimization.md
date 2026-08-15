> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 延迟优化

> 降低千问AI平台文本、图像、视频和语音模型的响应延迟

不同模态的延迟来源各不相同：文本生成主要取决于 token 数量和模型大小；图像和视频生成取决于渲染时间和任务队列深度；语音则取决于合成启动时间和流式缓冲区大小。本文分模态介绍优化策略，并深入讲解上下文缓存和流式输出等千问AI平台特性，帮助你显著降低文本工作负载的延迟。

## 文本生成：七个优化方向

### 1. 选择合适的模型

模型大小是推理速度的首要决定因素。较小的模型响应更快，单 token 成本更低。

| 场景           | 推荐模型          | 原因        |
| ------------ | ------------- | --------- |
| 复杂推理、开放式生成   | qwen3.8-max   | 质量最高，速度较慢 |
| 通用任务，速度与质量兼顾 | qwen3.7-plus  | 较好的平衡     |
| 分类、提取、摘要     | qwen3.5-flash | 快速且经济     |

切换到更小的模型时，可以通过更详细的提示词或 few-shot 示例来弥补质量差异。精心设计提示词的 qwen3.5-flash 在很多生产任务中可以媲美提示词简单的 qwen3.8-max。

### 2. 减少输出长度

输出生成是 LLM 调用中最慢的阶段——输出 token 数减半，总延迟大约减半。策略如下：

- **约束自然语言输出**：添加明确的长度指令（"用一句话回答"、"不超过 50 字"），或通过 few-shot 示例展示期望的简洁风格。
- **精简结构化输出**：如果模型返回 JSON，使用简短的字段名（用 `s` 代替 `sentiment_analysis_result`），省略可选字段。
- **设置硬性限制**：使用 `max_tokens` 限制输出长度，或用 `stop` 序列在特定分隔符处终止生成。

### 3. 精简输入 token

输入 token 对延迟的影响小于输出 token（输入减少 50% 大约带来 1-5% 的延迟改善），但在大规模场景下仍然重要：

- **筛选检索结果**：在 RAG 流水线中，按相关性对文本块排序和过滤后再发送给模型。去除网页内容中的 HTML 标签、样板文本和导航元素。
- **控制对话历史长度**：只保留最近几轮对话，或将早期历史压缩为一条精简的系统消息。
- **用 few-shot 示例替代冗长指令**：在提示词中加入典型示例，让模型学习你的格式规则和领域约束，比逐条写规则更高效。

### 4. 合并请求

每次 API 调用都会增加网络往返时间。如果你的工作流包含多个串行的 LLM 步骤，考虑合并它们：

- 让模型在一次调用中完成所有步骤，以 JSON 对象返回结果，每个步骤对应一个命名字段。
- 处理多个条目时，将它们批量放入一个提示词中（如"对这 10 条工单分类"），而不是发送 10 次单独请求。

### 5. 并行执行步骤

如果流水线中有相互独立的分支，可以并发执行。例如，同时需要摘要和翻译时，同时发起两个请求，而不是等一个完成再执行另一个。

对于其中一个分支高度可预测的串行步骤（如 95% 通过率的内容审核），可以**推测执行**：在审核完成前就启动下一步，仅在审核未通过时丢弃结果。

### 6. 提升感知速度

即使实际延迟不变，感知速度对用户体验也很重要：

- **流式输出响应**，让用户看到逐步生成的 token，而不是等待完整响应。关注**首 token 时间（TTFT）** 这一流式性能核心指标。参见[流式输出](/developer-guides/run-and-scale/streaming)。
- **分段处理输出**：如果需要对模型输出做后处理（如翻译或审核），将流式输出发送到后端，再将处理后的片段逐步推送到前端。
- **显示进度指示**：展示当前步骤（"正在搜索知识库..."、"正在生成回答..."），在多步骤工作流中保持用户参与感。

<Note>
  流式输出和分段处理通过持续返回生成片段，缩短用户等待时间，同时避免非流式调用在长文本生成时触发超时。进度指示虽不直接加速内容生成，但能通过提供即时反馈缓解用户等待焦虑，对提升用户满意度同样重要。
</Note>

### 7. 能不用 LLM 就别用

AI 应用中并非每个环节都需要模型调用：

- **固定回复**：确认消息、错误提示和标准免责声明可以硬编码。
- **预生成内容**：对于有限的输入空间（如下拉选项分类），可以离线生成回复并即时返回。
- **传统代码**：格式化、过滤、排序和聚合用常规代码比 LLM 更快、更可靠。

## 图像与视频生成

图像和视频 API 使用异步任务队列，延迟优化的重点在于减少渲染时间和高效轮询。

**图像生成**

- 当提示词已经足够完善时，关闭提示词改写（`prompt_extend`）可节省每次请求 3-5 秒。
- 迭代阶段使用较低分辨率（如 1024x1024 而非 2048x2048），仅在最终输出时提高分辨率。
- 用指数退避策略轮询任务完成状态——初始间隔 3 秒，逐步增加，设置 2 分钟超时。参见[文生图——上线注意事项](/developer-guides/image-generation/text-to-image#上线注意事项)了解生产模式。
- 多图生成（`n=4`）是并行处理的，延迟与 `n=1` 基本相同。不需要多个变体时使用 `n=1` 以节省成本，因为每张图单独计费。

**视频生成**

- 迭代阶段使用短时长（2-3 秒）和低分辨率（480P/720P），最终输出时再渲染完整时长和高分辨率。
- 提示词已经足够详细时，关闭提示词改写。
- 简单场景使用单镜头模式比多镜头模式更快。
- 将参考图片和视频托管在高速 CDN 上，减少上传和下载时间。

## 语音与音频

**文本转语音（TTS）**

- 使用流式输出，在第一个合成片段生成后的几毫秒内即可听到音频，无需等待整个文件。参见[实时流式合成](/developer-guides/speech/realtime-streaming)。
- 交互场景选择 `flash` 模型变体以获得最低延迟。
- 使用压缩输出格式（mp3、opus）减少数据传输时间。
- 对于 LLM 驱动的语音应用，将 LLM 的流式文本输出直接接入 TTS 流式输入，实现端到端低延迟。

**语音识别（ASR）**

- 实时转写使用 WebSocket 端点，而非 REST API。参见 [ASR 实时识别](/developer-guides/speech/asr-realtime)。
- 上传前压缩音频文件以减少传输时间。
- 大音频文件传入 URL 而非 Base64 编码数据，避免请求体膨胀。

## 上下文缓存

上下文缓存是千问AI平台针对文本和视觉模型最直接的延迟优化特性。当连续请求共享相同的提示词前缀时，服务器会复用缓存的计算结果而非重新处理这些 token，从而显著降低首 token 时间（TTFT）。图像生成、视频生成和语音 API 采用不同的定价模型，没有等价的缓存机制。

### 工作原理

模型从左到右处理提示词。如果新请求的前 N 个 token 匹配已缓存的前缀，这 N 个 token 将从缓存中读取——只有剩余 token 需要重新计算。

因此**提示词结构很重要**：将稳定内容（系统指令、参考文档、few-shot 示例）放在前面，将可变内容（用户消息、动态 RAG 结果）放在后面。

### 三种模式

| 模式       | 配置方式                            | 缓存有效期       | 命中价格      |
| -------- | ------------------------------- | ----------- | --------- |
| **显式缓存** | 在消息内容中添加 `cache_control` 标记     | 5 分钟（命中后重置） | 输入价格的 10% |
| **隐式缓存** | 无需配置——默认开启                      | 不保证         | 输入价格的 20% |
| **会话缓存** | 添加 HTTP header，使用 Responses API | 5 分钟（命中后重置） | 输入价格的 10% |

**隐式缓存**无需修改代码，自动惠及所有应用。当你需要可控内容的稳定命中率和更低价格时，使用**显式缓存**。基于 Responses API 构建的多轮对话机器人，使用**会话缓存**。

### 显式缓存示例

用 `cache_control` 标记需要缓存的内容。最小可缓存长度为 1024 个 token。

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
      model="qwen3-max",
      messages=[
        {
          "role": "system",
          "content": [
            {
              "type": "text",
              "text": "You are a helpful assistant specialized in answering questions about our product documentation. Here is the full reference manual:\n\n[... long reference document ...]",
              "cache_control": {"type": "ephemeral"}
            }
          ]
        },
        {
          "role": "user",
          "content": "How do I configure SSO?"
        }
      ]
    )

    print(completion.usage)
    # 检查 completion.usage.prompt_tokens_details.cached_tokens 确认缓存命中
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";

    const openai = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    });

    const completion = await openai.chat.completions.create({
      model: "qwen3-max",
      messages: [
        {
          role: "system",
          content: [
            {
              type: "text",
              text: "You are a helpful assistant specialized in answering questions about our product documentation. Here is the full reference manual:\n\n[... long reference document ...]",
              cache_control: { type: "ephemeral" }
            }
          ]
        },
        {
          role: "user",
          content: "How do I configure SSO?"
        }
      ]
    });

    console.log(completion.usage);
    // 检查 completion.usage.prompt_tokens_details.cached_tokens 确认缓存命中
    ```
  </Tab>

  <Tab title="curl">
    ```bash
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3-max",
        "messages": [
          {
            "role": "system",
            "content": [
              {
                "type": "text",
                "text": "You are a helpful assistant specialized in answering questions about our product documentation. Here is the full reference manual:\n\n[... long reference document ...]",
                "cache_control": {"type": "ephemeral"}
              }
            ]
          },
          {
            "role": "user",
            "content": "How do I configure SSO?"
          }
        ]
      }'
    ```
  </Tab>
</Tabs>

缓存命中时，响应的 usage 对象中会包含 `cached_tokens`：

```json
{
  "usage": {
    "prompt_tokens": 1520,
    "completion_tokens": 85,
    "total_tokens": 1605,
    "prompt_tokens_details": {
      "cached_tokens": 1480,
      "cache_creation_input_tokens": 0
    }
  }
}
```

### 提高缓存命中率的技巧

- **保持系统提示词稳定。** 缓存前缀的任何变化——哪怕一个字符——都会使缓存失效。对系统提示词进行版本管理，谨慎更新。
- **提示词结构：静态前缀 + 动态后缀。** 系统指令和参考文档放前面，用户输入和 RAG 上下文放后面，最大化请求间的重叠部分。
- **在 5 分钟窗口内发送请求。** 显式缓存和会话缓存在 5 分钟无活动后过期。对于低流量应用，可以定期发送保活请求。

完整指南包括会话缓存配置、支持模型和高级用法，参见[上下文缓存](/developer-guides/run-and-scale/context-cache)。

## 综合应用

大多数实际应用会组合使用上述多种策略。以下是典型 RAG 聊天机器人的决策框架：

| 瓶颈          | 症状                   | 建议措施                                |
| ----------- | -------------------- | ----------------------------------- |
| 首 token 慢   | TTFT 高，用户需要等待才能看到输出  | 启用流式输出；对系统提示词使用上下文缓存；检索/路由步骤使用更快的模型 |
| 输出生成慢       | token 流式输出速度慢；总响应时间长 | 用明确指令减少输出长度；如质量允许，使用更快的模型           |
| 串行 LLM 调用过多 | 多步流水线端到端延迟高          | 将步骤合并到一个提示词中；并行化独立步骤                |
| 提示词过大       | 延迟随文档/历史长度增长         | 筛选 RAG 结果；压缩历史；使用上下文缓存避免重复计算        |

### 非文本模态速查表

| 模态       | 主要延迟来源           | 首要优化                                |
| -------- | ---------------- | ----------------------------------- |
| **图像生成** | 渲染时间 + 队列等待      | 降低分辨率；关闭提示词改写；指数退避轮询                |
| **视频生成** | 渲染时间（与时长和分辨率成正比） | 迭代阶段用短时长 + 低分辨率；单镜头模式               |
| **TTS**  | 合成启动 + 数据传输      | 流式输出；flash 模型；压缩格式（mp3/opus）        |
| **ASR**  | 上传大小 + 处理时间      | 实时场景用 WebSocket 端点；大文件用 URL 输入；压缩音频 |

## 下一步

- [流式输出](/developer-guides/run-and-scale/streaming)——流式输出 token，缩短首次可见输出时间
- [上下文缓存](/developer-guides/run-and-scale/context-cache)——缓存模式详解、支持模型和定价
- [模型选择](/developer-guides/getting-started/model-selection)——对比模型能力、速度和定价
- [文生图——上线注意事项](/developer-guides/image-generation/text-to-image#上线注意事项)——图像生成的生产模式
- [实时流式 TTS](/developer-guides/speech/realtime-streaming)——低延迟流式语音合成
- [ASR 实时识别](/developer-guides/speech/asr-realtime)——基于 WebSocket 的实时语音识别
- [成本优化](/developer-guides/run-and-scale/cost-optimization)——与延迟优化互补的成本策略
