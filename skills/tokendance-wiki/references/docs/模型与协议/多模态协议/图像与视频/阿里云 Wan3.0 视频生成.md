# 阿里云 Wan3.0 视频生成

<!-- model-detail-quickstart:start -->

异步协议——提交任务后需使用返回的 `task_id` 轮询，生成结果 URL 有效期为 24 小时。

### 提交任务

#### 文生视频

```bash title="cURL"
curl https://tokendance.space/gateway/alibaba/wan3/v1/video-synthesis \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "input": {
      "prompt": "一只纸飞机在明亮的蓝天中平稳飞过，电影感运镜"
    },
    "parameters": {
      "resolution": "720P",
      "ratio": "16:9",
      "duration": 5,
      "audio": false,
      "watermark": false
    }
  }'
```

提交成功后，从响应的 `output.task_id` 取得任务 ID。创建接口没有客户端幂等键，网络超时后不要自动重试
`POST`，否则可能重复创建并计费。

### 查询任务

```bash title="cURL"
curl https://tokendance.space/gateway/alibaba/wan3/v1/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_KEY"
```

任务完成后，`output.task_status` 为 `SUCCEEDED`，`output.video_url` 是带签名的视频下载地址。

<!-- model-detail-quickstart:end -->

Wan3.0 支持文生视频、首帧/首尾帧生视频、多模态参考和视频编辑。

### 调用地址

| 操作 | 方法与地址 |
| --- | --- |
| 创建任务 | `POST https://tokendance.space/gateway/alibaba/wan3/v1/video-synthesis` |
| 查询任务 | `GET https://tokendance.space/gateway/alibaba/wan3/v1/tasks/{TASK_ID}` |

调用 TokenDance 时不需要发送 `X-DashScope-Async`，Gateway 会按 Wan3 Endpoint 的上游协议自动添加异步
请求头。提交响应中的 `task_id` 有效期为 24 小时；保存它并轮询查询接口，不要重复调用创建接口。

### 更多生成模式

#### 首帧生视频

```bash title="cURL"
curl https://tokendance.space/gateway/alibaba/wan3/v1/video-synthesis \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "input": {
      "prompt": "猫咪朝镜头挥爪，镜头缓慢推进",
      "media": [
        {"type": "first_frame", "url": "https://example.com/cat.png"}
      ]
    },
    "parameters": {
      "resolution": "720P",
      "ratio": "adaptive",
      "duration": 5,
      "audio": true,
      "watermark": false
    }
  }'
```

#### 首尾帧生视频

```bash title="cURL"
curl https://tokendance.space/gateway/alibaba/wan3/v1/video-synthesis \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "input": {
      "prompt": "镜头从清晨的城市街道平滑过渡到黄昏河岸",
      "media": [
        {"type": "first_frame", "url": "https://example.com/start.png"},
        {"type": "last_frame", "url": "https://example.com/end.png"}
      ]
    },
    "parameters": {
      "resolution": "720P",
      "ratio": "adaptive",
      "duration": 5,
      "audio": false,
      "watermark": false
    }
  }'
```

#### 多模态参考与视频编辑

`reference_image`、`reference_video` 和 `reference_audio` 可以组合使用。它们在各自类型中的数组顺序对应
提示词里的“图片 1”“视频 1”“音频 1”。下面的请求可以用于参考生成；把提示词改成明确的修改指令时，
也可用于视频编辑或延长：

```bash title="cURL"
curl https://tokendance.space/gateway/alibaba/wan3/v1/video-synthesis \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "input": {
      "prompt": "参考图片 1 的角色、视频 1 的运镜和音频 1 的节奏生成一支短片",
      "media": [
        {"type": "reference_image", "url": "https://example.com/character.png"},
        {"type": "reference_video", "url": "https://example.com/camera.mp4"},
        {"type": "reference_audio", "url": "https://example.com/rhythm.mp3"}
      ]
    },
    "parameters": {
      "resolution": "720P",
      "ratio": "16:9",
      "duration": 10,
      "audio": true,
      "prompt_extend": true,
      "watermark": false
    }
  }'
```

图片可使用公网 HTTP/HTTPS URL 或完整的 Base64 data URI，例如
`data:image/png;base64,<BASE64_DATA>`。视频和音频使用上游可访问的 URL。Wan3.0 还支持一个 `file` 或一个
`link` 作为参考；两者不能同时传，使用时应显式设置 `prompt_extend: true`。

### 素材限制

| 类型 | 数量与主要限制 |
| --- | --- |
| `first_frame` | 最多 1 张图片 |
| `last_frame` | 最多 1 张图片，需和首帧模式配合 |
| `reference_image` | 最多 10 张；支持 JPEG/JPG/PNG/BMP/WEBP URL 或 Base64 |
| `reference_video` | 最多 5 段；单段 1～15 秒，总时长不超过 15 秒；MP4 或 MOV |
| `reference_audio` | 最多 5 段；单段 1～15 秒，总时长不超过 15 秒；WAV 或 MP3 |
| `file` | 最多 1 个，不可与 `link` 同时使用 |
| `link` | 最多 1 个公开网页，不可与 `file` 同时使用 |

首帧/尾帧模式与 `reference_*`、`file`、`link` 参考模式互斥，不要在同一个 `media` 数组中混用。Gateway
会原样转发素材与供应商参数；格式、可访问性、数量和组合最终由所选 Endpoint 的上游校验。

### 生成参数

| 参数 | 说明 |
| --- | --- |
| `resolution` | `480P`、`720P`、`1080P`，省略时默认为 `1080P` |
| `ratio` | `adaptive`、`16:9`、`4:3`、`1:1`、`3:4`、`9:16` |
| `duration` | 无参考视频时为 2～30 秒；`-1` 表示智能时长；有参考视频时输入与输出总时长不超过 30 秒 |
| `audio` | 是否生成包含声音的视频；示例中显式指定，避免依赖上游默认值 |
| `seed` | `-1` 或 0～2147483647；相同 seed 不保证结果逐帧一致 |
| `prompt_extend` | 是否对提示词进行智能改写；短提示词或 `file`/`link` 参考建议开启 |
| `watermark` | 是否添加水印；示例中显式设为 `false` |

### 任务状态与结果

创建成功只表示上游接受了任务，不代表视频已经生成。建议从 5 秒间隔开始轮询同一个 `task_id`，并对查询
请求使用退避；不要通过重新创建任务来处理长时间运行或下载失败。

| `output.task_status` | 含义 |
| --- | --- |
| `PENDING` | 等待处理 |
| `RUNNING` | 正在生成 |
| `SUCCEEDED` | 已完成，可读取 `output.video_url` |
| `FAILED`、`CANCELED`、`UNKNOWN` | 失败，查看 `output.message` |

`output.video_url` 是有效期为 24 小时的 Gateway 签名代理地址。下载遇到瞬时网络错误时可以重试同一个
下载 URL，不要重新创建视频任务。

### 用量与计费

Wan3.0 按总计费视频秒数和输出分辨率计费。无参考视频时通常等于生成视频时长；传入参考视频时，完成响应
中的总量包含输入参考视频时长和输出视频时长。TokenDance 对应计费项为：

```text
wan3:video-seconds
```

提交时会根据请求参数预扣，任务成功后按上游最终 `usage.duration` 退补；若上游只返回拆分字段，则使用
`usage.input_video_duration + usage.output_video_duration`。任务失败会释放预扣。参考图片和参考音频不会
单独增加视频秒数。

完整字段与最新模型限制请参阅[阿里云百炼 Wan3.0 视频生成 API](https://help.aliyun.com/zh/model-studio/wan3-video-generation-api-reference)。
