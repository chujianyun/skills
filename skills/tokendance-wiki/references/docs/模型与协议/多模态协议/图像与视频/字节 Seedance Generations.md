# 字节 Seedance Generations

<!-- model-detail-quickstart:start -->

异步协议——提交任务后需轮询，视频 URL 有效期为 24 小时。

### 提交任务

#### 文生视频

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "content": [{"type": "text", "text": "夜空中的烟花倒映在湖面"}],
    "resolution": "720p",
    "ratio": "16:9",
    "duration": 5
  }'
```

#### 图生视频（首帧）

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "content": [
      {"type": "text", "text": "猫咪朝镜头挥爪"},
      {"type": "image_url", "image_url": {"url": "https://example.com/cat.jpg"}, "role": "first_frame"}
    ],
    "resolution": "720p",
    "ratio": "adaptive",
    "duration": 5
  }'
```

#### 图生视频（首尾帧）

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "content": [
      {"type": "text", "text": "镜头从城市街道平稳移动到河岸"},
      {"type": "image_url", "image_url": {"url": "https://example.com/start.jpg"}, "role": "first_frame"},
      {"type": "image_url", "image_url": {"url": "https://example.com/end.jpg"}, "role": "last_frame"}
    ],
    "resolution": "720p",
    "ratio": "adaptive",
    "duration": 5
  }'
```

#### 全模态参考生视频

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "content": [
      {"type": "text", "text": "参考角色形象和镜头运动，生成一支有环境音的短片"},
      {"type": "image_url", "image_url": {"url": "https://example.com/character.jpg"}, "role": "reference_image"},
      {"type": "video_url", "video_url": {"url": "https://example.com/camera.mp4"}, "role": "reference_video"},
      {"type": "audio_url", "audio_url": {"url": "https://example.com/ambience.mp3"}, "role": "reference_audio"}
    ],
    "resolution": "720p",
    "ratio": "16:9",
    "duration": 10
  }'
```

### 查询任务

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_KEY"
```

任务完成后，响应中的 `content.video_url` 是视频下载链接。[查看完整协议说明和版本差异](%E5%AD%97%E8%8A%82%20Seedance%20Generations.md)。

<!-- model-detail-quickstart:end -->

Seedance Generations 是异步视频生成协议：先提交任务，再通过任务 ID 轮询结果。生成成功后，请在 24 小时内下载或转存视频。

### 调用地址

| 操作 | 方法与地址 |
| --- | --- |
| 提交任务 | `POST https://tokendance.space/gateway/ark/v3/generations/tasks` |
| 查询任务 | `GET https://tokendance.space/gateway/ark/v3/generations/tasks/{TASK_ID}` |

`model` 填写 TokenDance 模型列表中的模型 ID，例如 `seedance-2.0-mini` 或 `seedance-2.5`。建议把 `resolution`、`ratio`、`duration` 等参数直接写在请求体中，以便在提交时获得明确的参数校验结果。

### Seedance 2.0、2.5 系列

Seedance 2.0、2.5 系列均支持文生视频、首帧/首尾帧生视频、全模态参考生视频、视频编辑和延长。Seedance 2.5 进一步提升了生成时长、参考素材数量和编辑控制能力。

完整字段定义与上游能力说明请参阅[火山方舟视频生成 API 官方文档](https://console.volcengine.com/ark/region:cn-beijing/docs/82379/1520757?projectName=default&lang=zh)。TokenDance 调用时仍需使用本页的 TokenDance 地址、API Key 和模型 ID。

#### Seedance 2.5 能力与输入限制

| 项目 | Seedance 2.5 说明 |
| --- | --- |
| 参考图片 | 最多 30 张；单张小于 30 MB；支持 URL 或 Base64 |
| 参考视频 | 最多 10 个；单个 2～30 秒，编辑任务为 4～30 秒；全部参考视频总时长不超过 30 秒；单个不超过 200 MB |
| 参考音频 | 最多 10 段；单段 2～30 秒；全部参考音频总时长不超过 30 秒；单段不超过 15 MB；支持仅输入音频 |
| 输出分辨率 | `480p`、`720p`、`1080p`；其中 1080p 为 10bit、H.265/HEVC 编码 |
| 输出时长 | `4`～`30` 秒，或 `-1` 让模型自动适配 |
| 输出格式 | `mp4`（默认）或 `mov`；编辑、延长和专业后期场景推荐 `mov` |
| 声音 | `generate_audio` 默认为 `true`，可生成有声或无声视频 |

#### 与 Seedance 2.0 的区别

Seedance 2.5 的主要升级是更长的生成时长、更大的多模态素材容量，以及更精确的视频编辑能力，并非所有规格都高于 Seedance 2.0。

| 对比项 | Seedance 2.5 | Seedance 2.0 系列 |
| --- | --- | --- |
| 单次生成时长 | 4～30 秒 | 4～15 秒 |
| 参考素材数量 | 最多 30 张图片、10 个视频、10 段音频 | 最多 9 张图片、3 个视频、3 段音频 |
| 仅输入音频 | 支持 | 不支持，需同时提供图片或视频 |
| 视频编辑与延长 | 支持通过 `omni_reference_task_type` 显式指定参考生成、编辑或延长任务 | 支持全模态参考、编辑和延长，但不支持该任务类型参数 |
| 输出分辨率 | 最高 1080p；1080p 为 10bit、H.265/HEVC 编码 | Seedance 2.0 最高支持 4K；Seedance 2.0 Fast、Mini 最高支持 720p |
| 模型选择 | 适合长叙事、多素材参考和复杂编辑 | 2.0 侧重最高生成品质；Fast 兼顾速度与成本；Mini 侧重更低成本 |

选择建议：长视频、多素材参考或复杂编辑优先使用 Seedance 2.5；明确需要 4K 输出时选择 Seedance 2.0；更看重生成速度或成本时，可选择 Seedance 2.0 Fast 或 Mini。

能力差异以[Seedance 2.5 官方教程](https://console.volcengine.com/ark/region:cn-beijing/docs/82379/2607688?lang=zh)和[Seedance 2.0 系列官方教程](https://console.volcengine.com/ark/region:cn-beijing/docs/82379/2291680?lang=zh)为准。

#### 任务类型与参数约束

全模态任务建议显式设置 `omni_reference_task_type`，让不兼容的参数尽量在提交任务时直接报错。

| 任务 | `omni_reference_task_type` | 必要输入 | 参数要求 |
| --- | --- | --- | --- |
| 参考生成 | `reference` | 至少一个 `reference_image`、`reference_video` 或 `reference_audio` | `ratio`、`duration` 可按需要设置 |
| 视频编辑 | `edit` | 至少一个 `reference_video`，提示词需明确编辑意图 | `ratio` 必须为 `adaptive`，`duration` 必须为 `-1`，参考视频须为 4～30 秒 |
| 视频延长 | `extend` | 至少一个 `reference_video`，提示词需明确向前或向后延长 | `ratio` 必须为 `adaptive` |
| 自动判断 | `auto` | 按实际任务提供参考素材 | 为兼容编辑与延长，推荐 `ratio: "adaptive"`、`duration: -1` |

首帧/首尾帧生视频与全模态参考生视频是互斥场景，不要在同一请求中混用 `first_frame` / `last_frame` 和 `reference_image` / `reference_video` / `reference_audio`。

#### Seedance 2.5 全模态参考示例

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedance-2.5",
    "content": [
      {"type": "text", "text": "参考图片中的角色与视频中的运镜，制作一支有环境音的夏日短片"},
      {"type": "image_url", "image_url": {"url": "https://example.com/character.png"}, "role": "reference_image"},
      {"type": "video_url", "video_url": {"url": "https://example.com/camera.mp4"}, "role": "reference_video"},
      {"type": "audio_url", "audio_url": {"url": "https://example.com/ambience.mp3"}, "role": "reference_audio"}
    ],
    "omni_reference_task_type": "reference",
    "resolution": "720p",
    "ratio": "16:9",
    "duration": 15,
    "generate_audio": true,
    "output_format": "mp4"
  }'
```

#### Seedance 2.5 视频编辑示例

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "seedance-2.5",
    "content": [
      {"type": "text", "text": "编辑视频：把天空改成晚霞，保留原有镜头运动和声音"},
      {"type": "video_url", "video_url": {"url": "https://example.com/source.mov"}, "role": "reference_video"}
    ],
    "omni_reference_task_type": "edit",
    "resolution": "1080p",
    "ratio": "adaptive",
    "duration": -1,
    "generate_audio": true,
    "output_format": "mov"
  }'
```

### 基础调用示例

以下示例使用 `MODEL_ID` 代表当前模型详情页中的模型 ID。不同版本支持的分辨率、时长和输入素材数量可能不同，请以模型页面展示为准。

#### 文生视频

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "content": [{"type": "text", "text": "夜空中的烟花倒映在湖面"}],
    "resolution": "720p",
    "ratio": "16:9",
    "duration": 5
  }'
```

#### 图生视频（首帧）

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "content": [
      {"type": "text", "text": "猫咪朝镜头挥爪，镜头缓慢推进"},
      {"type": "image_url", "image_url": {"url": "https://example.com/cat.jpg"}, "role": "first_frame"}
    ],
    "resolution": "720p",
    "ratio": "adaptive",
    "duration": 5
  }'
```

#### 图生视频（首尾帧）

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "content": [
      {"type": "text", "text": "镜头从城市街道平稳移动到河岸"},
      {"type": "image_url", "image_url": {"url": "https://example.com/start.jpg"}, "role": "first_frame"},
      {"type": "image_url", "image_url": {"url": "https://example.com/end.jpg"}, "role": "last_frame"}
    ],
    "resolution": "720p",
    "ratio": "adaptive",
    "duration": 5
  }'
```

### 查询任务

```bash title="cURL"
curl https://tokendance.space/gateway/ark/v3/generations/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_KEY"
```

常见状态包括 `queued`、`running`、`succeeded` 和 `failed`。任务成功后，响应中的 `content.video_url` 是视频下载链接；如失败，请查看响应中的错误信息并优先核对任务类型、素材角色、`ratio` 和 `duration`。
