# Seedance 使用指南

本页只记录通过 TokenDance 调用 Seedance 时最容易出错的参数关系、异步流程和排查方法。完整能力与素材规格请查看厂商官方资料。

:::note
模型 ID 和可用协议以 TokenDance [模型列表](https://tokendance.space/models)为准。厂商参数发生变化时，本文优先保留会影响请求成功与否的约束，不维护模型推荐、价格或完整能力清单。
:::

## 调用地址

| 操作 | 地址 |
|---|---|
| 创建任务 | `POST https://tokendance.space/gateway/ark/v3/generations/tasks` |
| 查询任务 | `GET https://tokendance.space/gateway/ark/v3/generations/tasks/{TASK_ID}` |
| 鉴权 | `Authorization: Bearer YOUR_KEY` |

## 最短调用

```bash title="文生视频"
curl https://tokendance.space/gateway/ark/v3/generations/tasks \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "MODEL_ID",
    "content": [{
      "type": "text",
      "text": "雨后夜晚，一辆黄色出租车穿过霓虹街道，低机位跟拍，环境音自然。"
    }],
    "resolution": "720p",
    "ratio": "16:9",
    "duration": 8,
    "generate_audio": true
  }'
```

创建成功后保存响应中的 `id`，再查询任务：

```bash title="查询任务"
curl https://tokendance.space/gateway/ark/v3/generations/tasks/TASK_ID \
  -H "Authorization: Bearer YOUR_KEY"
```

任务成功时读取 `content.video_url`。下载地址可能有时效，应及时转存。

## 高频参数问题

### `ratio` 什么时候必须用 `adaptive`

| 输入方式 | `ratio` |
|---|---|
| 纯文本生成 | 传明确画幅，例如 `16:9` 或 `9:16` |
| 首帧 / 首尾帧 | 使用 `adaptive` |
| 视频编辑 | 使用 `adaptive` |
| 视频延长 | 使用 `adaptive` |

首帧、首尾帧、编辑和延长任务的画幅由输入素材决定。继续传固定画幅容易触发任务类型约束错误或导致画面拉伸。

### 图片和参考素材的 `role`

| 用途 | `role` |
|---|---|
| 首帧 | `first_frame` |
| 尾帧 | `last_frame` |
| 参考图片 | `reference_image` |
| 参考视频 | `reference_video` |
| 参考音频 | `reference_audio` |

首帧/首尾帧和全模态参考是不同任务形式，不要在同一请求中混用 `first_frame`、`last_frame` 与 `reference_*`。

```json title="首尾帧关键字段"
{
  "model": "MODEL_ID",
  "content": [
    {"type": "text", "text": "女孩转身看向镜头，动作连续自然。"},
    {"type": "image_url", "image_url": {"url": "https://example.com/start.jpg"}, "role": "first_frame"},
    {"type": "image_url", "image_url": {"url": "https://example.com/end.jpg"}, "role": "last_frame"}
  ],
  "ratio": "adaptive",
  "duration": 6
}
```

### `omni_reference_task_type`

任务意图明确时建议显式传入，避免模型自动判断后异步失败：

| 值 | 用途 | 关键条件 |
|---|---|---|
| `reference` | 多模态参考生成 | 使用至少一种 `reference_*` 素材 |
| `edit` | 修改已有视频 | 包含 `reference_video`；提示词明确写编辑、删除、替换等动作 |
| `extend` | 延长已有视频 | 包含 `reference_video`；提示词明确写向前或向后延长 |
| `auto` | 由模型判断 | 适合任务类型不明确的请求 |

编辑任务通常还需要 `ratio: "adaptive"` 和 `duration: -1`。厂商后续若调整任务类型参数，以官方资料为准。

```json title="编辑任务关键字段"
{
  "model": "MODEL_ID",
  "content": [
    {"type": "text", "text": "编辑视频1：删除右侧路牌，保留主体和镜头运动。"},
    {"type": "video_url", "video_url": {"url": "https://example.com/source.mp4"}, "role": "reference_video"}
  ],
  "omni_reference_task_type": "edit",
  "ratio": "adaptive",
  "duration": -1
}
```

### 素材在提示词中的编号

当请求中有多份素材时，使用“图片1”“视频1”“音频1”明确引用；序号按 `content` 中同类型素材出现的顺序计算。不要只写“参考素材”，否则模型无法判断每份素材的职责。

## 异步状态处理

生产代码至少处理以下状态：

| 状态 | 处理 |
|---|---|
| `queued` / `running` | 间隔轮询，不要无间隔请求 |
| `succeeded` | 读取并转存 `content.video_url` |
| `failed` | 记录错误信息和关键参数，修正后再创建 |

网络错误和 5xx 可以退避重试；业务失败不要原样无限重建。应保存业务 ID、任务 ID、模型、创建时间和最终状态。

## 常见错误

| 现象 | 优先检查 |
|---|---|
| `InvalidParameter.TaskTypeConstraint` | `ratio`、`duration`、素材 `role` 是否与任务类型冲突 |
| `InvalidParameter.TaskTypeMismatch` | `edit` / `extend` 是否与提示词意图一致 |
| 首帧画面拉伸或跳变 | 是否使用 `ratio: adaptive`；输入图片画幅是否差异过大 |
| 素材 URL 无法读取 | URL 是否公开、未过期并允许服务端访问 |
| 任务成功但视频无法播放 | 高规格结果可能使用 H.265/HEVC；换播放器或转码 |
| 下载地址失效 | 成功后是否及时转存到自己的对象存储 |

## 官方资料

- [Doubao Seedance 2.5 教程](https://console.volcengine.com/ark/region:cn-beijing/docs/82379/2607688?lang=zh)
- [Doubao Seedance 2.0 系列教程](https://console.volcengine.com/ark/region:cn-beijing/docs/82379/2291680?lang=zh)
- [TokenDance Seedance Generations 协议参考](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%AD%97%E8%8A%82%20Seedance%20Generations.md)
