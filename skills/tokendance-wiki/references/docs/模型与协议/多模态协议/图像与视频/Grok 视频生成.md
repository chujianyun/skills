# Grok 视频生成

<!-- model-detail-quickstart:start -->

### 文生视频

```bash title="cURL"
curl https://tokendance.space/gateway/v1/videos/generations \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "prompt": "一只小猫在阳光下伸懒腰，镜头缓缓推进",
    "duration": 5,
    "resolution": "480p",
    "generate_audio": false
  }'
```

### 图生视频

```bash title="cURL"
curl https://tokendance.space/gateway/v1/videos/generations \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "prompt": "镜头缓缓推进，星空流动",
    "image": {"url": "https://docs.x.ai/assets/api-examples/video/milkyway-still.png"},
    "duration": 5,
    "resolution": "480p",
    "generate_audio": false
  }'
```

### 查询任务

将 `REQUEST_ID` 替换为提交响应中的 `request_id`，每隔 5 秒查询一次：

```bash title="cURL"
curl https://tokendance.space/gateway/v1/videos/REQUEST_ID \
  -H "Authorization: Bearer YOUR_KEY"
```

`status` 为 `pending` 时继续等待，`failed` 时查看 `error`；`done` 时从 `video.url` 获取视频地址。

### 下载视频

将 `VIDEO_URL` 替换为返回的完整 `video.url`，请及时下载：

```bash title="cURL"
curl -L "VIDEO_URL" -o video.mp4
```

[xAI 视频生成官方文档](https://docs.x.ai/developers/model-capabilities/video/generation)

<!-- model-detail-quickstart:end -->
