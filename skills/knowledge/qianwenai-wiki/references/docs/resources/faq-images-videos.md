> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图片与视频 FAQ

> 图片和视频生成的常见问题——计费、API 报错、模型差异、输入要求和输出 URL。

<a id="debugging" />

## 调试

### 如何在本地调试图片 API？

图片 API 支持标准 HTTP 调用，本地测试步骤如下：

1. [开通模型服务并获取 API Key](/developer-guides/getting-started/first-api-call)，然后[将 API Key 设为环境变量](/api-reference/preparation/export-api-key-env)。
2. 在图片 API 文档中找到 `curl` 命令，在终端（macOS/Linux）中运行，或使用 Postman、Apifox 等 API 平台（Windows）。

<Expandable title="示例：文生图的 curl 命令">
  ```bash
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.1-t2i-turbo",
    "input": {
      "prompt": "A flower shop with exquisite windows, a beautiful wooden door, and flowers on display"
    },
    "parameters": {
      "size": "1024*1024",
      "n": 1
    }
  }'
  ```
</Expandable>

<Note>
  使用 API 平台时，请将 `Authorization` 请求头中的 `$DASHSCOPE_API_KEY` 替换为您的实际 API Key，例如 `Bearer sk-ws-xxxxxx`。
</Note>

---

<a id="billing-rate-limits" />

## 计费与限流

### 图片模型如何计费？

每个图片模型都有免费额度，且可能按图计价。免费额度和限流在千问AI平台账号下共享。仅成功生成的输出图片计费——输入图片和失败请求不消耗额度，也不产生费用。

详见[计费概述](/resources/billing-overview)。

### "限时免费"是什么意思？

模型处于公测阶段。免费额度用完后，模型将不可用。

### 如何获取免费额度？

开通千问AI平台时自动获得免费额度，有效期 90 天。详见[新用户免费额度](/resources/free-quota)。

### 视频模型如何计费？

视频生成按成功生成的视频时长计费，失败的任务不收费。

---

<a id="api-errors" />

## API 报错

常见的图片 API 报错：

| 错误码                              | 错误信息                                  | 常见原因                  |
| -------------------------------- | ------------------------------------- | --------------------- |
| `BadRequest.InputDownloadFailed` | Reference image download failed       | 图片 URL 错误、不可访问或有访问限制  |
| `InvalidParameter`               | Required body invalid                 | 请求体中包含客户端无法解析的中文字符    |
| （下载超时）                           | Download the media resource timed out | 中国大陆以外地区与服务端点之间的网络不稳定 |

### `BadRequest.InputDownloadFailed`："Reference image download failed"

```json
{
  "request_id": "657f0d1b-76d0-9e3e-b6d6-xxxxxx",
  "output": {
    "task_id": "5e6fa974-9a25-4271-8659-xxxxxx",
    "task_status": "FAILED",
    "code": "BadRequest.InputDownloadFailed",
    "message": "Reference image download failed, please check image url."
  }
}
```

**原因**： 图片 URL 错误、不可访问或有访问限制。服务在处理过程中会下载图片，下载失败则任务失败。

**解决方法**： 确保 URL 完整且可公开访问。如果图片需要鉴权，请上传至公共存储（如 OSS），然后使用新的 URL。

### `InvalidParameter`："Required body invalid"

```json
{
  "request_id": "d306ae65-3f6d-9d6c-acfb-xxxxxx",
  "code": "InvalidParameter",
  "message": "Required body invalid, please check the request body format."
}
```

**原因**： `curl` 请求体中包含客户端无法正确解析的中文字符。

**解决方法**： 在终端（macOS/Linux 原生支持 UTF-8）中运行 `curl` 命令，或使用 Postman、Apifox 等 HTTP 平台。

### 中国大陆以外地区的资源下载超时

```text
Download the media resource timed out during the data inspection process
```

**原因**： 图片存储区域（中国大陆以外）与服务端点之间的网络不稳定，导致下载超时。

**解决方法**： 将图片存储在与服务端点连接稳定的区域，并配置加速。下载超时时长不可配置。

---

<a id="wan26-image" />

## Wan2.6 图片生成与编辑

**API**： [同步调用](/api-reference/image-generation/wan26-image-gen-edit/synchronous)、[创建任务](/api-reference/image-generation/wan26-image-gen-edit/create-task)、[查询结果](/api-reference/image-generation/wan26-image-gen-edit/query-result)

### Wan2.6 支持哪些图片编辑模式？

Wan2.6 通过 `enable_interleave` 参数控制两种模式：

- **图片编辑**（`enable_interleave=false`，默认）：编辑图片、风格迁移或生成主体一致的图片。输入：1–4 张图片。输出：1–4 张图片。
- **图文交错输出**（`enable_interleave=true`）：生成图文混合内容。输入：0–1 张图片。必须使用流式输出。

### 图片输入有什么要求？

- **格式**： JPEG、JPG、PNG（不支持 Alpha 通道）、BMP、WEBP。
- **分辨率**： 宽和高各在 240 到 8,000 像素之间。
- **文件大小**： 单张不超过 10 MB。
- **图片数量**： 编辑模式：1–4 张。交错模式：0–1 张。

### 如何通过 Base64 编码传入图片？

可以用 Base64 编码字符串替代公开 URL，格式为 `data:{mime_type};base64,{base64_data}`（例如 `data:image/jpeg;base64,/9j/4AAQ...`）。

### 如何使用图文交错输出模式？

图文交错输出（`enable_interleave=true`）必须使用流式输出，需同时设置：

1. `X-DashScope-Sse` 请求头为 `enable`
2. `parameters.stream` 为 `true`

通过 `max_images`（1–5，默认 5）控制生成图片的最大数量。该模式下 `n` 必须为 1。

### 支持哪些输出分辨率？

**图片编辑模式**： 使用 `1K`（默认，约 `1280*1280`）或 `2K`（约 `2048*2048`）自动匹配输入比例，或在 `[768*768, 2048*2048]` 范围内指定具体的 `width*height`。

**交错模式**： 尺寸在 `[768*768, 1280*1280]` 范围内。推荐值：`1280*1280`、`800*1200`、`1200*800`、`960*1280`、`1280*960`、`720*1280`、`1280*720`、`1344*576`。

### 生成的图片 URL 有效期多久？

生成的图片 URL 有效期为 **24 小时**，请在生成后及时下载。

---

<a id="qwen-text-to-image" />

## Qwen 文生图

**API**： [Qwen text-to-image](/api-reference/image-generation/qwen-text-to-image)

### 是否应该启用 `prompt_extend` 参数？

对简单提示词建议启用（默认开启），可提升生成质量。如果需要精确控制、已有详细描述或对延迟敏感，建议关闭（设为 `false`）。详见[图片提示词指南](/developer-guides/accuracy-tuning/image-generation)。

### Qwen-Image 各模型有什么区别？

**统一图片生成与编辑模型**：

- `qwen-image-3.0-pro`（推荐）：长文本输入与复杂版面生成，10 像素小字精准渲染，12 国语言与 20+ 字体。仅支持同步调用。
- `qwen-image-3.0`（推荐）：3.0 标准版，兼顾质量与速度。仅支持同步调用。
- `qwen-image-2.0-pro`：上一代，专业文字渲染，细粒度真实感，语义一致性更强。仅支持同步调用。
- `qwen-image-2.0`：上一代，高质量生成，速度快于 qwen-image-2.0-pro。仅支持同步调用。

**文生图模型**：

- `qwen-image-max`：相比 qwen-image-plus，真实感更强、纹理和细节更丰富。
- `qwen-image-plus` / `qwen-image`：能力相同。`qwen-image-plus` 为当前推荐选项；`qwen-image` 保留以兼容旧版。

---

<a id="qwen-image-editing" />

## Qwen 图片编辑

**API**： [Qwen image editing](/api-reference/image-generation/qwen-image-editing)

### Qwen 图片编辑模型支持哪些语言？

模型官方支持简体中文和英文，其他语言可能可用但不保证效果。

### Qwen 图片编辑的图片输入要求是什么？

- **格式**： JPG、JPEG、PNG、BMP、TIFF、WEBP、GIF（仅取第一帧）。输出固定为 PNG。
- **分辨率**： 宽和高在 384 到 3072 像素之间。超出范围可能导致输出模糊或增加处理时间。
- **文件大小**： 单张不超过 10 MB。
- **图片数量**： 每次请求 1 到 3 张。

### 如何通过 Base64 编码传入图片？

可以用 Base64 编码字符串替代 URL，格式为 `data:{mime_type};base64,{base64_data}`（例如 `data:image/jpeg;base64,/9j/4AAQ...`）。完整示例请参见 API 参考中的代码示例。

---

<a id="z-image" />

## Z-Image

### 如何查看模型调用指标？

模型调用指标（调用次数、成功率）在生成任务完成一小时后可在[用量分析](https://platform.qianwenai.com/home/analytics)页面查看。另见：[账单查询与费用管理](/resources/bill-query)。

---

<a id="video-generation" />

## 视频生成

**API**： [文生视频](/developer-guides/video-generation/text-to-video)、[图生视频](/developer-guides/video-generation/image-to-video)、[图生视频（首尾帧）](/developer-guides/video-generation/image-to-video-first-last)、[视频编辑](/developer-guides/video-generation/video-editing)

### 图生视频的图片输入要求是什么？

- **格式**： JPEG、JPG、PNG、WEBP 等常见格式。
- **大小**： 单张不超过 10 MB。
- **URL**： 必须是可公开访问的 HTTP(S) URL。服务在生成时会下载图片。

`wan2.6` 和 `wan2.5` 的要求有所不同——请参阅所用模型的 API 参考。

### 视频生成需要多长时间？

视频生成是异步的。提交任务后，每 10–30 秒轮询查询端点，直到状态从 `PENDING` 或 `RUNNING` 变为 `SUCCEEDED` 或 `FAILED`。生成时间取决于视频时长、分辨率和队列负载，通常需要一到数分钟。

### 生成的视频 URL 有效期多久？

生成的视频 URL 有效期为 **24 小时**，请在任务成功后及时下载。
