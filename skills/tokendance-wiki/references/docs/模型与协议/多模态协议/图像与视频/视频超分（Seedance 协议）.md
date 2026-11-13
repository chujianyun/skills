# 视频超分（Seedance 协议）

<!-- model-detail-quickstart:start -->

支持火山方舟 seedance 协议的客户端，把 `model` 换成本模型、在 `content` 中放入 1 个待超分的视频即可。
成片下载地址有效期为 24 小时。

### 提交任务

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "content": [
      {"type": "video_url", "video_url": {"url": "https://example.com/input.mp4"}, "role": "reference_video"}
    ],
    "resolution": "1080p"
  }'
```

`resolution` 是目标分辨率，可选 `720p`、`1080p`、`4k`；档位约束画面高度，宽度按源视频比例缩放。
`content` 只能包含 1 个 `video_url`，`role` 可省略或填 `reference_video`；视频必须能从公网直接下载，不支持 `asset://`。
提交成功后返回任务 ID：

```json
{"id": "TASK_ID"}
```

### 查询任务

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_KEY"
```

`status` 依次经过 `queued`、`running`，最终为 `succeeded` 或 `failed`。任务成功后，`content.video_url`
是成片下载地址：

```json
{
  "id": "TASK_ID",
  "status": "succeeded",
  "content": {"video_url": "https://tokendance.space/gateway/resources/..."},
  "resolution": "1080p",
  "duration": 10,
  "created_at": 1792152359,
  "updated_at": 1792152417
}
```

任务失败时 `status` 为 `failed`，`error.message` 是失败原因，例如源视频无法下载。

<!-- model-detail-quickstart:end -->

### 与 Seedance 生视频的差异

视频超分只用到 Seedance 请求的一个子集：

| 请求内容 | 处理方式 |
| --- | --- |
| 1 个 `video_url` | 作为待超分的源视频 |
| `resolution` | 目标分辨率，可选 `720p`、`1080p`、`4k`，也可写在提示词里，如 `--rs 1080p` |
| 文本提示词、`ratio`、`duration`、`generate_audio` 等生成参数 | 忽略 |
| `image_url`、`audio_url` 等其他内容，或多个 `video_url` | 拒绝提交 |

查询响应只返回 `id`、`status`、`content.video_url`、`resolution`、`duration`、`created_at`、`updated_at`
和失败时的 `error`，不返回 `usage`。也可以使用[视频超分协议](%E8%A7%86%E9%A2%91%E8%B6%85%E5%88%86.md)调用，计费与能力相同。

按源视频时长计费，单价随目标分辨率变化，任务完成后按实际时长结算。创建接口没有客户端幂等键，
网络超时后不要自动重试 `POST`，否则可能重复创建并计费。
