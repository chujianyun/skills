# Vidu 文生视频

异步协议——提交任务后需轮询，视频 URL 有效期 24 小时。

### 提交任务

```bash title="cURL"
curl https://tokendance.space/gateway/vidu/v2/text2video \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "style": "general",
    "prompt": "海上日出"
  }'
```

提交成功后从响应中拿到 `task_id`。

### 查询任务

```bash title="cURL"
curl https://tokendance.space/gateway/vidu/v2/tasks/TASK_ID/creations \
  -H "Authorization: Bearer YOUR_KEY"
```

任务完成后 `creations[].url` 即为视频下载链接。
