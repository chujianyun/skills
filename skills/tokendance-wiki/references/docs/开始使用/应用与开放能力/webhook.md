# webhook

所有异步生成协议的提交接口都支持可选的 `X-Webhook-URL` 请求头。配置后，任务进入 `completed` 或 `failed` 状态时，我们会向该地址发出 `POST` 回调请求。

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Webhook-URL: https://hooks.example.com/token-dance/tasks?token=YOUR_SECRET" \
  -d '{
    "model": "YOUR_MODEL_ID",
    "content": [{"type": "text", "text": "夜空中的烟花倒映在湖面"}]
  }'
```

## 成功回调

任务成功时，回调请求会在 `artifacts` 中携带任务生成的产物链接：

```json
{
  "task_id": "upstream-task-id",
  "status": "completed",
  "artifacts": [
    {
      "artifact_name": "video",
      "url": "https://tokendance.space/gateway/resources/xxx",
      "expires_at": 1788499200
    }
  ]
}
```

- `task_id` 与提交接口返回的任务 ID 相同。
- `artifact_name` 是产物名称。
- `url` 是产物的下载链接。
- `expires_at` 是下载链接过期时间，使用 Unix 秒时间戳。存在该字段时，请在过期前下载或转存产物。

## 失败回调

任务失败时，回调请求会通过 `error` 字段返回任务失败的原因：

```json
{
  "task_id": "task_xxx",
  "status": "failed",
  "error": "任务生成失败"
}
```

Webhook 请求的 `Content-Type` 为 `application/json`。

## 更多信息

- 我们会按照 best-effort 原则向您发出调用通知，由于网络波动等原因调用失败时不会进行重试，因此需要高可靠性的应用应保留任务查询作为兜底。
- 回调地址必须是完整的公网 HTTPS URL，最长 2048 字节，不能包含 URL userinfo 或 fragment，也不能指向本机、私网、链路本地或保留地址。
