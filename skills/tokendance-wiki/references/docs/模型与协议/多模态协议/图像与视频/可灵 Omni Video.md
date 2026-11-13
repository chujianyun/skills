# 可灵 Omni Video

<!-- model-detail-quickstart:start -->

可灵 Omni Video 采用异步生成：提交任务后，使用返回的任务 ID 查询结果。

### 提交任务

```bash title="cURL"
curl https://tokendance.space/gateway/kling/v1/omni-video \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "MODEL_ID",
    "contents": [
      {"type": "prompt", "text": "一名舞者站在雨后的街道上，镜头缓慢向前推进"}
    ],
    "settings": {
      "resolution": "720p",
      "aspect_ratio": "16:9",
      "duration": 7,
      "audio": "off"
    }
  }'
```

### 查询任务

将 `TASK_ID` 替换为提交响应中的 `data.id`：

```bash title="cURL"
curl https://tokendance.space/gateway/kling/v1/omni-video/TASK_ID \
  -H "Authorization: Bearer YOUR_KEY"
```

任务成功后，视频地址位于 `data[0].outputs[]` 中 `type` 为 `video` 的结果的 `url`。请及时下载或转存。

[可灵 Omni Video 官方文档](https://www.klingai.com/document-api/apiReference/model/OmniVideo)

<!-- model-detail-quickstart:end -->
