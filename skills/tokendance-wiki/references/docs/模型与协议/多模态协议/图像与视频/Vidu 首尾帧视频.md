# Vidu 首尾帧视频

异步协议——提交任务后需轮询，视频 URL 有效期 24 小时。

### 提交任务

```bash title="cURL"
curl https://tokendance.space/gateway/vidu/v2/start-end2video \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "images": ["https://example.com/start.jpg", "https://example.com/end.jpg"],
    "prompt": "镜头平移"
  }'
```

### 查询任务

```bash title="cURL"
curl https://tokendance.space/gateway/vidu/v2/tasks/TASK_ID/creations \
  -H "Authorization: Bearer YOUR_KEY"
```
