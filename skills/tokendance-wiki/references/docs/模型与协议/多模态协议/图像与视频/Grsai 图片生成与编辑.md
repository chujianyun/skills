# Grsai 图片生成与编辑

Grsai 使用 `grsai:generate` 异步协议，图片生成和参考图编辑共用同一个提交接口。请在模型详情中选择支持该协议的模型；使用 Gemini 原生请求结构时，请参阅 [Gemini GenerateContent](../../%E9%80%9A%E7%94%A8%E6%A8%A1%E5%9E%8B%E5%8D%8F%E8%AE%AE/Google/Google%20GenerateContent.md)。

## 提交图片生成任务

```bash title="cURL"
curl "https://tokendance.space/gateway/grsai/v1/generate" \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "prompt": "一只戴着草帽的橘猫，水彩风格",
    "aspectRatio": "1:1",
    "imageSize": "1K",
    "replyType": "async"
  }'
```

提交成功后返回任务 ID，例如：

```json
{"id":"TASK_ID","status":"running"}
```

网关始终以异步方式提交 Grsai 任务。`imageSize`、`aspectRatio` 等参数的可用值取决于所选模型及上游能力，网关透传参数并返回上游校验结果。

## 使用参考图编辑

在同一接口的请求中加入 `images`。图片可以使用上游可访问的 URL，或 `data:image/png;base64,...` 格式的 Data URI。

```bash title="参考图编辑"
curl "https://tokendance.space/gateway/grsai/v1/generate" \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "prompt": "保留主体，将背景改为海边日落",
    "images": ["data:image/png;base64,REPLACE_WITH_IMAGE_BASE64"],
    "replyType": "async"
  }'
```

## 查询结果

使用同一用户的 API Key 查询任务。建议每隔 5 秒轮询一次，并在客户端设置总等待超时；进入终态后停止轮询。

```bash title="查询任务"
curl --get "https://tokendance.space/gateway/grsai/v1/result" \
  -H "Authorization: Bearer YOUR_KEY" \
  --data-urlencode "id=TASK_ID"
```

| status | 含义 | 后续操作 |
| --- | --- | --- |
| `running` | 任务处理中 | 稍后再次查询 |
| `succeeded` | 任务成功 | 读取 `results[].url` 获取图片 |
| `failed` | 任务失败 | 检查返回的错误信息 |
| `violation` | 上游内容审核未通过 | 根据错误信息调整请求 |

成功响应示意：

```json
{
  "id": "TASK_ID",
  "status": "succeeded",
  "results": [{"url": "https://example.com/generated-image.png"}]
}
```

返回的图片地址具有有效期，请及时下载保存。计费项为 `grsai:generate:images`，单位为张，按返回的有效图片数量计量；实际价格以模型端点定价为准。

## 管理员端点配置

选择 `grsai:generate` 后，端点表单使用异步协议配置，填写提交 URL 和轮询 URL。以 Grsai 上游为例：

| 字段 | 值 |
| --- | --- |
| 协议族 `family` | `async` |
| 提交 `url` | `https://grsai.dakka.com.cn/v1/api/generate` |
| 轮询 `poll_url` | `https://grsai.dakka.com.cn/v1/api/result` |

以上上游地址填写在该协议的 `protocol_settings` 条目中。客户端调用网关使用 `/grsai/v1/generate` 和 `/grsai/v1/result`；供应商地址中的 `/api` 仅属于上游路径。
