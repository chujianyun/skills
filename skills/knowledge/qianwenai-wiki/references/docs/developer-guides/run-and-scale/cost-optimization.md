> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 成本优化

> 在保证输出质量的同时，降低文本、图像、视频和语音 API 调用费用

千问AI平台各模态采用不同的计费方式：文本模型按 token 计费，图像生成按图片数量计费，视频生成按输出时长计费，TTS 按字符数计费，ASR 按音频时长计费。本文介绍多种实用的降本策略，适用于所有模态，且不会影响输出质量。各策略可单独使用，也可组合使用以获得更大的成本优势。

## 优化 API 用量

最直接的降本方式是减少每个任务的资源消耗：

- **合并 API 调用**：如果需要发送多个小请求，可以合并为一次调用。例如，在一个 prompt 中同时对十个条目做分类，而不是发送十次单独的请求。
- **精简 prompt**：删除系统 prompt 中的冗余指令，将对话历史限制在最近几轮，并设置 `max_tokens` 防止输出过长。
- **按任务复杂度选择模型**：仅在确实需要高级推理能力时使用高性能模型（如 qwen3.8-max）。对于分类、信息提取或摘要等简单任务，轻量级模型（如 qwen3.5-flash）即可胜任，费用仅为前者的一小部分。模型能力对比详见[模型概览](/developer-guides/getting-started/model-selection)。

这些做法通常也能提升响应速度。更多延迟优化技巧请参阅[延迟优化](/developer-guides/run-and-scale/latency-optimization)。

### 优化非文本 API 用量

**图像生成**

- 多数图像模型按图片数量计费，与分辨率无关，但降低分辨率可以缩短生成时间。
- qwen-image-3.0 系列例外：输出单价按输出分辨率分档（1k / 2k），且输入图像也单独计费。如对成本敏感，可将输出像素面积控制在 2,250,000 以内以落入 1k 档，并减少输入图片数量。详见[计费说明](/developer-guides/getting-started/pricing)。
- 控制 `n`（每次请求生成的图片数量），每张图片单独计费。
- 如果已有精心编写的 prompt，可在生产环境中关闭 prompt 改写功能（`prompt_extend`），避免不必要的处理开销。

**视频生成**

- 迭代阶段使用短时长、低分辨率（480P/720P）。大多数模型要求最少 5 秒；wan2.6 模型支持最短 2 秒。仅在最终输出时使用高分辨率（如 15 秒 1080P）。
- 预览和社交媒体内容通常 480P 或 720P 即可，非必要不选 1080P。
- 多次生成时复用参考图片和视频，避免重复上传。

**语音**

- 根据场景选择合适的 TTS 模型：`flash` 版本是简单旁白最经济的选择，`instruct` 模型适用于需要情感表达或精细控制的场景。详见[语音合成](/developer-guides/speech/tts)。
- 将多段短文本合并为一次 TTS 调用，避免大量小请求。
- 使用 ASR 时，提交前压缩音频文件可缩短上传时间。注意 ASR 按音频时长计费，压缩不影响费用。

## 批量调用

批量调用仅适用于文本生成模型。如果您的任务不需要实时响应，批量调用可节省 **50%** 的 token 费用。您只需将请求打包为 JSONL 文件，作为单个作业提交，处理完成后下载结果——通常在 24 小时内完成。

常见应用场景：

- 离线评测与基准测试
- 批量分类或数据标注
- 大规模 embedding 生成

支持的模型：qwen-max、qwen-plus、qwen-flash、qwen-turbo。

[开始使用批量调用](/developer-guides/text-generation/batch)

## 上下文缓存

上下文缓存仅适用于文本和视觉模型。当多个请求共享相同的前缀内容（如长系统 prompt、参考文档或对话历史）时，上下文缓存可降低输入 token 费用。它避免了对重复内容的冗余计算，同时提升速度和降低成本。

千问AI平台提供三种缓存模式：

| 模式       | 工作原理                     | 缓存命中费用      |
| -------- | ------------------------ | ----------- |
| **显式缓存** | 手动标记需要缓存的内容，保证 5 分钟内命中。  | 标准输入价格的 10% |
| **隐式缓存** | 自动生效，无需配置。系统自动识别公共前缀。    | 标准输入价格的 20% |
| **会话缓存** | 专为 Responses API 多轮对话设计。 | 标准输入价格的 10% |

[开始使用上下文缓存](/developer-guides/run-and-scale/context-cache)

<Note>
  批量调用和上下文缓存的折扣不能在同一请求中叠加使用。
</Note>

## 成本对比

<Note>
  以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
</Note>

以下示例展示了使用 qwen3.5-plus 处理 1000 万输入 token + 500 万输出 token 的假设场景下，各策略的费用对比：

| 策略                        | 输入费用                         | 输出费用           | 合计         |
| ------------------------- | ---------------------------- | -------------- | ---------- |
| **标准计费**                  | 10M x 0.8 = 8元               | 5M x 4.8 = 24元 | **32元**    |
| **批量调用**（5 折）             | 10M x 0.4 = 4元               | 5M x 2.4 = 12元 | **16元**    |
| **上下文缓存**（80% 缓存命中率，隐式缓存） | 2M x 0.8 + 8M x 0.16 = 2.88元 | 5M x 4.8 = 24元 | **26.88元** |

<Note>
  实际节省金额取决于缓存命中率、prompt 结构和模型选择。完整价格表请参阅[定价](/developer-guides/getting-started/pricing)。
</Note>

### 非文本成本优化示例

下表展示了参数选择对非文本模态费用的影响：

| 模态       | 基准方案                     | 优化方案                                       | 节省方式                  |
| -------- | ------------------------ | ------------------------------------------ | --------------------- |
| **图像生成** | 100 次调用，每次 n=4（计费 400 张） | 100 次调用，每次 n=1（计费 100 张）                   | 只生成需要的图片；关闭 prompt 改写 |
| **视频生成** | 10 个视频，1080P，每个 15 秒     | 迭代阶段 10 个 720P 5 秒视频 + 最终 2 个 1080P 15 秒视频 | 预览用低分辨率；仅最终版本用高分辨率    |
| **TTS**  | 10,000 字符，使用 instruct 模型 | 10,000 字符，使用 flash 模型                      | 选择满足质量要求的最低成本模型       |

各模态和模型的单价详见[定价](/developer-guides/getting-started/pricing)。

## 后续阅读

- [定价](/developer-guides/getting-started/pricing)——了解计费模式和模型费率
- [批量调用](/developer-guides/text-generation/batch)——批量 API 使用指南
- [上下文缓存](/developer-guides/run-and-scale/context-cache)——缓存模式及使用详情
- [图像模型](/developer-guides/getting-started/image-models)——图像生成模型与定价
- [视频模型](/developer-guides/getting-started/video-models)——视频生成模型与定价
- [语音合成](/developer-guides/speech/tts)——TTS 模型选择与成本考量
- [延迟优化](/developer-guides/run-and-scale/latency-optimization)——同时兼顾降本的延迟优化策略
