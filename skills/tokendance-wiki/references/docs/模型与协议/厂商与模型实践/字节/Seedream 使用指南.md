# Seedream 使用指南

本页只记录通过 TokenDance Ark 生图协议调用 Seedream 时常见的参数问题。模型能力、价格和完整规格以 TokenDance 模型页及厂商官方资料为准。

## 调用地址

| 项 | 值 |
|---|---|
| 完整接口 | `POST https://tokendance.space/gateway/ark/v3/images/generations` |
| 鉴权 | `Authorization: Bearer YOUR_KEY` |
| 协议 ID | `ark:image-generations` |

`model` 填写 TokenDance [模型列表](https://tokendance.space/models)中的模型 ID。

## 最短调用

```bash title="文生图"
curl https://tokendance.space/gateway/ark/v3/images/generations \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "prompt": "一只橙色复古收音机摆在木质书桌上，午后窗光，胶片质感。",
    "size": "2K",
    "response_format": "url",
    "output_format": "jpeg",
    "watermark": false
  }'
```

## 高频参数问题

### `image` 传字符串还是数组

- 文生图：不传 `image`。
- 单图生图：传图片 URL 或 Data URL 字符串。
- 多参考图：传图片数组，并在 `prompt` 中用“图1”“图2”说明各自用途。

```json title="多参考图关键字段"
{
  "model": "MODEL_ID",
  "prompt": "以图1的包袋为主体，融合图2的花纹和色彩。",
  "image": [
    "https://example.com/product.png",
    "https://example.com/pattern.png"
  ],
  "size": "2K"
}
```

图片 URL 必须允许服务端直接访问。使用需要登录、短时防盗链或已过期的地址时，通常会出现素材读取失败。

### `size` 使用档位还是像素

`size` 可以是模型支持的分辨率档位，也可能支持明确的 `宽x高`。不同模型的可选范围并不一致，不要在文档或业务代码中假设所有 Seedream 模型都支持同一组值。

如果接口提示尺寸错误：

1. 先改用模型页展示的标准分辨率档位。
2. 使用像素尺寸时检查宽高顺序和画幅比例。
3. 图生图出现拉伸时，先把输入图裁剪到目标画幅。

### `response_format` 和 `output_format` 的区别

| 参数 | 控制内容 |
|---|---|
| `response_format` | 结果如何返回：URL 或 Base64 数据 |
| `output_format` | 图片文件格式，例如 PNG 或 JPEG |
| `watermark` | 是否添加 AI 生成水印 |

`response_format: "url"` 时读取 `data[0].url`；使用 Base64 返回时读取对应的 Base64 字段。URL 可能有时效，生产环境应及时转存。

### 组图生成参数

支持组图的模型使用：

```json
{
  "sequential_image_generation": "auto",
  "sequential_image_generation_options": {
    "max_images": 4
  }
}
```

并非所有 Seedream 模型都支持组图。出现未知字段或能力不支持错误时，先从请求中删除这两个字段，再查看目标模型的协议能力。

### `stream` 与组图事件

只有支持流式生图的模型才能传 `stream: true`。常见事件包括单张成功、单张失败、整体完成和 `[DONE]`。生产代码不能在收到第一张图后就结束连接，应等待完成事件或流结束。

### 联网搜索工具

只有明确支持联网搜索的模型才能传：

```json
{
  "tools": [{"type": "web_search"}]
}
```

不要把 `tools` 作为所有生图请求的默认参数；模型不支持时应在适配层删除。

## 响应与用量

非流式响应主要读取 `data[]` 和 `usage`：

```json title="响应示意"
{
  "data": [{"url": "https://example.com/generated.png"}],
  "usage": {
    "generated_images": 1,
    "output_tokens": 100,
    "total_tokens": 100
  }
}
```

多图结果应遍历整个 `data` 数组，不要只读取 `data[0]`。

## 常见错误

| 现象 | 优先检查 |
|---|---|
| 图片读取失败 | URL 是否公开、未过期；Data URL 格式是否完整 |
| `size` 无效 | 目标模型是否支持该档位或像素尺寸 |
| 多参考图结果混乱 | 提示词是否明确引用“图1”“图2”及各自职责 |
| 组图或流式字段报错 | 目标模型是否支持对应能力；不支持时删除可选字段 |
| 返回 URL 失效 | 是否在任务完成后及时转存 |

## 协议资料

- [TokenDance Ark Image Generations 协议参考](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%AD%97%E8%8A%82%20Ark%20Image%20Generations.md)

具体模型支持的参数与取值范围仍应以 TokenDance 模型页和页面顶部所列官方文档的最新内容为准。
