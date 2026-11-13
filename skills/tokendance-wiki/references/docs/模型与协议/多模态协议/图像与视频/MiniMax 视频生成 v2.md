# MiniMax 视频生成 v2

异步协议——提交任务后需轮询，视频 URL 有效期 24 小时。

### 提交任务

#### 文生视频

`content` 只有 `text` 时为文生视频，此时 `ratio` 必填且不能为 `adaptive`。

```bash title="cURL"
curl https://tokendance.space/gateway/minimax/v2/video_generation \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "resolution": "768P",
    "duration": 6,
    "ratio": "16:9",
    "content": [{"type": "text", "text": "女人坐在咖啡馆里抬头看向窗外，镜头推进拍到街道，暖色调"}]
  }'
```

#### 图生视频（首帧 / 首尾帧）

宽高比由图片决定，不用传 `ratio`。只传一张且不填 `role` 时按首帧处理。

```bash title="cURL"
curl https://tokendance.space/gateway/minimax/v2/video_generation \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "resolution": "768P",
    "duration": 6,
    "content": [
      {"type": "text", "text": "小女孩慢慢长大"},
      {"type": "image_url", "image_url": {"url": "https://example.com/start.jpg"}, "role": "first_frame"},
      {"type": "image_url", "image_url": {"url": "https://example.com/end.jpg"}, "role": "last_frame"}
    ]
  }'
```

#### 多模态参考生视频

参考图、参考视频、参考音频可任意组合，但至少要有一个参考视频或图片。

```bash title="cURL"
curl https://tokendance.space/gateway/minimax/v2/video_generation \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "resolution": "768P",
    "duration": 8,
    "content": [
      {"type": "text", "text": "男子走在古巷中，镜头从肩后跟拍"},
      {"type": "image_url", "image_url": {"url": "https://example.com/face.jpg"}, "role": "reference_image"},
      {"type": "video_url", "video_url": {"url": "https://example.com/move.mp4"}, "role": "reference_video"},
      {"type": "audio_url", "audio_url": {"url": "https://example.com/bgm.mp3"}, "role": "reference_audio"}
    ]
  }'
```

### 查询任务

```bash title="cURL"
curl https://tokendance.space/gateway/minimax/v2/query/video_generation/TASK_ID \
  -H "Authorization: Bearer YOUR_KEY"
```

`task.status` 为 `queued` / `running` / `succeeded` / `failed` / `cancelled` / `expired`。
任务完成后响应中 `task.content.url` 为视频下载链接。
