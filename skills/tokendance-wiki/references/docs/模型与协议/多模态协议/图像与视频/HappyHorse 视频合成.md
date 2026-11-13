# HappyHorse 视频合成

异步协议——提交任务后需轮询。

### 提交任务

#### 文生视频

```bash title="cURL"
curl https://tokendance.space/gateway/alibaba/happyhorse/v1/video-synthesis \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
    "model": "MODEL_ID",
    "input": {"prompt": "夜空中的烟花"},
    "parameters": {
      "resolution": "720P",
      "ratio": "16:9",
      "duration": 5
    }
  }'
```

#### 图生视频

```bash title="cURL"
curl https://tokendance.space/gateway/alibaba/happyhorse/v1/video-synthesis \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
    "model": "MODEL_ID",
    "input": {
      "prompt": "猫咪挥爪",
      "media": [
        {"type": "first_frame", "url": "https://example.com/cat.jpg"}
      ]
    },
    "parameters": {"resolution": "720P", "duration": 5}
  }'
```

#### 参考生视频

```bash title="cURL"
curl https://tokendance.space/gateway/alibaba/happyhorse/v1/video-synthesis \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
    "model": "MODEL_ID",
    "input": {
      "prompt": "参考图风格",
      "media": [
        {"type": "reference_image", "url": "https://example.com/ref1.jpg"},
        {"type": "reference_image", "url": "https://example.com/ref2.jpg"}
      ]
    },
    "parameters": {"resolution": "720P", "ratio": "16:9", "duration": 5}
  }'
```

#### 视频编辑

```bash title="cURL"
curl https://tokendance.space/gateway/alibaba/happyhorse/v1/video-synthesis \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
    "model": "MODEL_ID",
    "input": {
      "prompt": "把动作改成跳跃",
      "media": [
        {"type": "video", "url": "https://example.com/source.mp4"}
      ]
    },
    "parameters": {"resolution": "720P"}
  }'
```

### 查询任务

```bash title="cURL"
curl https://tokendance.space/gateway/alibaba/happyhorse/v1/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_KEY"
```

任务完成后响应中 `output.video_url` 为视频下载链接。
