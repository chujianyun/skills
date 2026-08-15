> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Token 计算

> 了解文本、视觉和音频模型的 Token 用量及计费方式

Token 是千问AI平台上文本和视觉模型的基本计费与上下文管理单位。了解 Token 的计算方式有助于估算成本、控制上下文长度并优化 Prompt。音频和图像生成模型使用不同的计费单位（秒、字符或图片数），本文也会一并介绍。

## 文本 Token

文本模型将输入和输出切分为子词（subword）单元。**粗略估算**：1 个 Token 约等于 **4 个英文字符**，或**约 1.5 个中文字符**。实际数量取决于分词器和词表。

### 从 API 响应中读取 Token 用量

每次文本生成响应都包含 `usage` 对象，其中有精确的 Token 计数：

```json
{
  "usage": {
    "prompt_tokens": 34,
    "completion_tokens": 89,
    "total_tokens": 123
  }
}
```

使用[上下文缓存](/developer-guides/run-and-scale/context-cache)时，会返回更多细节：

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

使用[推理模式](/developer-guides/text-generation/thinking)时，响应中会包含推理 Token：

```json
{
  "usage": {
    "prompt_tokens": 50,
    "completion_tokens": 300,
    "total_tokens": 350,
    "completion_tokens_details": {
      "reasoning_tokens": 245
    }
  }
}
```

<Note>
  推理 Token 计入 `completion_tokens`，按输出 Token 费率计费。对于复杂推理任务，推理 Token 可能会显著增加总 Token 用量。
</Note>

### 发送请求前估算 Token 数

在调用 API 之前，可以直接使用分词器估算 Token 数量。Qwen 模型使用兼容 tiktoken 的分词器：

```python
# pip install tiktoken
import tiktoken

# 使用 Qwen 分词器
encoding = tiktoken.get_encoding("o200k_base")
tokens = encoding.encode("Your prompt text here")
print(f"Token count: {len(tokens)}")
```

<Tip>
  Token 估算有助于控制上下文窗口和预估成本。如需精确数值，请以 API 响应中的 `usage` 字段为准。
</Tip>

## 视觉 Token

视觉模型（Qwen-VL 系列）将图片和视频帧与文本一起转换为 Token。Token 数量取决于图片分辨率。

### 图片 Token 计算公式

```
image_tokens = ceil(height / 28) × ceil(width / 28) / 4 + 2
```

其中：

- 图片会被缩放至 `max_pixels`（默认 1003520 像素）范围内，保持宽高比，尺寸四舍五入到 28 的倍数
- `/ 4` 对应视觉编码器中的 2×2 像素合并操作
- `+ 2` 为 `<vision_bos>` 和 `<vision_eos>` 两个特殊 Token

**示例**：一张 1024×1024 的图片 ≈ `(1008/28) × (1008/28) / 4 + 2` = **326 个 Token**。

### Python 估算图片 Token

```python
import math

def estimate_image_tokens(width, height, max_pixels=1003520, min_pixels=3136):
  """估算 Qwen 视觉模型的图片 Token 数量。"""
  # 缩放至像素预算范围内
  total_pixels = width * height
  if total_pixels > max_pixels:
    scale = math.sqrt(max_pixels / total_pixels)
    width = int(width * scale)
    height = int(height * scale)

  # 取整到 28 的最近倍数
  width = max(28, round(width / 28) * 28)
  height = max(28, round(height / 28) * 28)

  # 计算 Token 数
  return (height // 28) * (width // 28) // 4 + 2

# 示例
print(estimate_image_tokens(1024, 1024))   # ~326 tokens
print(estimate_image_tokens(1920, 1080))   # ~326 tokens
print(estimate_image_tokens(4096, 4096))   # ~326 tokens（缩放后）
```

### 高分辨率模式

启用 `vl_high_resolution_images` 可以以更高保真度处理图片（每个 Token 块对应 28×28 像素，而非默认的等效比率）。这会增加 Token 数量（每张图片最高可达 16,384 个 Token），但能提升细节识别能力，适用于 OCR 或小字识别等场景。

### 视频 Token

视频输入会被采样为独立帧，每帧使用相同的图片公式计算 Token。视频总 Token 数等于所有采样帧的 Token 之和。帧采样率取决于模型和视频时长。

## 音频计费单位

音频 API 不使用 Token，而是按时长或字符数计费：

| API           | 计费单位 | 说明          |
| ------------- | ---- | ----------- |
| **语音识别（ASR）** | 音频秒数 | 按输入音频的秒数计费  |
| **语音合成（TTS）** | 字符数  | 按输入文本的字符数计费 |
| **语音对话**      | 音频秒数 | 因模型而异       |

ASR 和 TTS 的响应不包含 `usage.prompt_tokens` 字段。当前单价请查看[定价](/developer-guides/getting-started/pricing)页面。

## 图像与视频生成计费

图像和视频生成 API 同样不使用 Token：

| API      | 计费单位  | 说明                                                            |
| -------- | ----- | ------------------------------------------------------------- |
| **图像生成** | 按张计费  | 每张生成图片单独计费。多数模型与分辨率无关；qwen-image-3.0 系列的输出单价按分辨率分档，且输入图片也单独计费 |
| **视频生成** | 按视频秒数 | 按输出视频的时长和分辨率计费                                                |

<Note>
  图像生成 API 的响应中，`usage` 字段包含图片张数而非 Token 计数。多数模型返回 `image_count`，且 `input_tokens`、`output_tokens` 可能显示为 `0`；qwen-image-3.0 系列改为返回 `input_image_count`、`output_image_count` 以及 `input_image_type`、`output_image_type` 计费档位。
</Note>

## 成本估算

文本/视觉 API 调用的成本估算公式：

```
cost = (input_tokens × 输入单价) + (output_tokens × 输出单价)
```

缓存 Token 按折扣费率计费（显式缓存按原价的 10% 收费，隐式缓存按原价的 20% 收费）。各模型单价请查看[定价](/developer-guides/getting-started/pricing)，降低成本的方法请查看[成本优化](/developer-guides/run-and-scale/cost-optimization)。

## 上下文窗口限制

每个模型都有最大上下文窗口，限制总输入 Token 数：

| 模型            | 最大输入 Token | 最大输出 Token |
| ------------- | ---------- | ---------- |
| qwen3.8-max   | 1M         | 131K       |
| qwen3.7-max   | 1M         | 64K        |
| qwen3.7-plus  | 1M         | 64K        |
| qwen3.5-flash | 1M         | 64K        |
| qwen3-max     | 256K       | 64K        |

当输入接近上下文限制时，可以考虑：

- 在[多轮对话](/developer-guides/run-and-scale/multi-turn)中裁剪历史消息
- 使用[上下文缓存](/developer-guides/run-and-scale/context-cache)减少重复计算（不会减少 Token 数，但能降低成本和延迟）
- 将较早的上下文压缩为精简的系统消息

## 后续阅读

- [定价](/developer-guides/getting-started/pricing) — 各模型 Token 费率及计费详情
- [成本优化](/developer-guides/run-and-scale/cost-optimization) — 减少 Token 用量和开支
- [上下文缓存](/developer-guides/run-and-scale/context-cache) — 缓存重复的 Prompt 前缀，降低成本和延迟
- [视觉理解](/developer-guides/multimodal/vision) — 图片和视频 Token 计算详解
