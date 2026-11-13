# MiniMax H3 使用指南

本页记录通过 TokenDance 调用 MiniMax 视频生成时常见的任务输入、参数联动、异步轮询和错误排查。完整素材规格请查看 MiniMax 官方资料。

:::note
模型 ID 和可用协议以 TokenDance [模型列表](https://tokendance.space/models)为准。本文不维护模型推荐、价格或完整分辨率与素材上限。
:::

## 调用地址

| 操作 | 地址 |
|---|---|
| 创建 V2 任务 | `POST https://tokendance.space/gateway/minimax/v2/video_generation` |
| 查询 V2 任务 | `GET https://tokendance.space/gateway/minimax/v2/query/video_generation/{task_id}` |
| 鉴权 | `Authorization: Bearer YOUR_KEY` |

## 最短调用

```bash title="文生视频"
curl https://tokendance.space/gateway/minimax/v2/video_generation \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "resolution": "768P",
    "duration": 6,
    "ratio": "16:9",
    "content": [{
      "type": "text",
      "text": "一只纸船沿雨后街道向前漂流，低机位跟拍，柔和自然光。"
    }]
  }'
```

创建成功后保存响应中的 `task_id`。

## 高频参数问题

### 文生视频和图生视频的 `ratio`

| 输入方式 | `ratio` |
|---|---|
| 纯文本 | 必须传明确画幅，不能使用 `adaptive` |
| 首帧 / 首尾帧 | 由图片决定画幅，不要再传 `ratio` |
| 多模态参考 | 按目标模型和任务要求传入；报错时先检查素材角色 |

文生请求提示 `ratio` 错误时，检查是否漏传或误用了 `adaptive`；图生请求提示画幅冲突时，先删除 `ratio`。

### 首帧、尾帧和参考素材的 `role`

| 用途 | `role` |
|---|---|
| 首帧 | `first_frame` |
| 尾帧 | `last_frame` |
| 参考图片 | `reference_image` |
| 参考视频 | `reference_video` |
| 参考音频 | `reference_audio` |

```json title="首尾帧关键字段"
{
  "model": "MODEL_ID",
  "duration": 6,
  "content": [
    {"type": "text", "text": "人物从清晨走到黄昏，过渡自然。"},
    {"type": "image_url", "image_url": {"url": "https://example.com/start.jpg"}, "role": "first_frame"},
    {"type": "image_url", "image_url": {"url": "https://example.com/end.jpg"}, "role": "last_frame"}
  ]
}
```

首尾帧差异过大容易出现形变或生硬转场；这属于素材一致性问题，不应通过增加更多冲突参数解决。

### 素材 URL 为什么读取失败

素材 URL 必须允许服务端访问。优先检查：

- 是否需要登录或 Cookie。
- 是否使用短时签名且已经过期。
- 是否存在防盗链或来源限制。
- 文件格式、尺寸、时长和大小是否满足厂商当前要求。

完整数值限制变化较快，本文不重复维护；请通过页面顶部的官方资料核对。

## 创建、轮询与结果

```python title="Python"
import time
import requests

API_KEY = "YOUR_KEY"
BASE_URL = "https://tokendance.space/gateway/minimax/v2"
headers = {"Authorization": f"Bearer {API_KEY}"}

created = requests.post(
    f"{BASE_URL}/video_generation",
    headers=headers,
    json={
        "model": "MODEL_ID",
        "resolution": "768P",
        "duration": 6,
        "ratio": "16:9",
        "content": [{"type": "text", "text": "雨后街道，低机位跟拍。"}],
    },
    timeout=60,
)
created.raise_for_status()
task_id = created.json()["task_id"]

while True:
    response = requests.get(
        f"{BASE_URL}/query/video_generation/{task_id}",
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    task = response.json()["task"]
    if task["status"] == "succeeded":
        print(task["content"]["url"])
        break
    if task["status"] in {"failed", "cancelled", "expired"}:
        raise RuntimeError(task)
    time.sleep(10)
```

不要无间隔轮询。网络错误和 5xx 可以退避重试；业务失败任务不要原样无限创建。成功结果 URL 可能有时效，应及时转存。

## 常见错误

| 现象 | 优先检查 |
|---|---|
| 文生请求 `ratio` 报错 | 是否漏传画幅或使用了 `adaptive` |
| 图生请求画幅冲突 | 是否多传了 `ratio` |
| 素材无法读取 | URL 权限、有效期和厂商当前素材限制 |
| 任务长期排队或运行 | 是否保持合理轮询间隔；是否重复创建了同一任务 |
| 成功后找不到结果 | 是否读取查询响应中的 `task.content.url` |
| 下载地址失效 | 是否在成功后及时转存 |

## 官方与协议资料

- [MiniMax 视频生成官方指南](https://platform.minimax.cn/docs/guides/video-generation)
- [TokenDance MiniMax 视频生成 V2](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/MiniMax%20%E8%A7%86%E9%A2%91%E7%94%9F%E6%88%90%20v2.md)
