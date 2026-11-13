# Kling 使用指南

可灵视频、语音、数字人与特效的调用要点。模型价格与可用服务商见各模型页；完整参数见下方协议文档。[本文 Markdown](Kling%20%E4%BD%BF%E7%94%A8%E6%8C%87%E5%8D%97.md)。

**适用范围：本文适用于 Kling 4.0、3.0 系列模型，并介绍语音、数字人与特效能力。**

## 模型与接口

请求中的 `model_name` 使用以下模型 ID，鉴权使用 TokenDance API Key。

| 模型 | 模型 ID | 适用能力 |
|---|---|---|
| [Kling: Video 4.0](https://tokendance.space/models/kling-4.0) | `kling-4.0` | V2 文生视频、图生视频、Omni 参考与编辑 |
| [Kling: Video 4.0 Flash](https://tokendance.space/models/kling-4.0-flash) | `kling-4.0-flash` | 同上，使用相同接口 |
| [Kling: Video 3.0](https://tokendance.space/models/kling-3.0) | `kling-3.0` | V1 文生视频、图生视频、动作控制 |
| [Kling: Video 3.0 Turbo](https://tokendance.space/models/kling-3.0-turbo) | `kling-3.0-turbo` | V1 文生视频、图生视频 |
| [Kling: Video 3.0 Omni](https://tokendance.space/models/kling-3.0-omni) | `kling-3.0-omni` | V1 Omni 参考与编辑 |
| [Kling: Kling TTS](https://tokendance.space/models/kling-tts) | `kling-tts` | 语音合成 |
| [Kling: Kling Avatar](https://tokendance.space/models/kling-avatar-image2video) | `kling-avatar-image2video` | 人物图片 + 音频生成数字人 |
| [Kling: Kling Video Effects](https://tokendance.space/models/kling-effects) | `kling-effects` | 模板特效 |

## 模型能力对比

参考可灵[官方能力地图](https://klingai.com/document-api/guides/capability-map/video)（[AI 阅读](https://klingai.com/document-api/guides/capability-map/video.md)）整理，4.0 分辨率按 TokenDance 当前支持范围展示。可调用的工作流见上表，其他规格以模型页及所选服务商为准。

| 能力 | 4.0 | 4.0 Flash | 3.0 | 3.0 Turbo | 3.0 Omni |
|---|---|---|---|---|---|
| 生成时长 | 3–30 秒 | 3–20 秒 | 3–15 秒 | 3–15 秒 | 3–15 秒 |
| 分辨率 | 720p / 1080p | 720p | 720p / 1080p / 4K | 720p / 1080p | 720p / 1080p / 4K |
| 文生 / 图生专用接口 | 支持 | 支持 | 支持 | 支持 | 使用 Omni 接口 |
| 首尾帧 | 支持 | 仅首帧 | 支持 | 仅首帧 | 支持（Omni） |
| 多关键帧 | 支持 | 不支持 | 不支持 | 不支持 | 不支持 |
| 全能参考 / 视频编辑 | 支持 | 支持 | 不支持 | 不支持 | 支持 |
| 视频参考上限 | ≤5 段，合计 ≤30 秒 | ≤5 段，合计 ≤20 秒 | — | — | 1 段，3–15.5 秒 |
| 动作控制接口 | — | — | 支持 | — | — |

需要多关键帧或长片段时选择 **4.0**；首帧驱动、优先生成速度时可选 **4.0 Flash** 或 **3.0 Turbo**；已有 3.0 工作流需要多模态参考与编辑时使用 **3.0 Omni**。

## Video 4.0

4.0 与 Flash 均使用 V2 接口。TokenDance 的 4.0 目前支持 720p、1080p，暂不支持 4K：

| 能力 | 提交路径 | 关键参数 |
|---|---|---|
| 文生视频 | `/gateway/kling/v2/text2video` | 顶层 `prompt` |
| 图生视频 | `/gateway/kling/v2/image2video` | 4.0 使用 `first_frame`、`middle_frame`、`last_frame`；Flash 仅 `first_frame`，均放入 `contents` |
| Omni 参考与编辑 | `/gateway/kling/v2/omni-video` | `refer_image` 参考图、`feature_video` 参考视频、`base_video` 待编辑视频 |

例如使用 Flash 参考人物与动作生成视频：

```bash
curl https://tokendance.space/gateway/kling/v2/omni-video \
  -H "Authorization: Bearer $TOKENDANCE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model_name": "kling-4.0-flash",
    "contents": [
      {"type": "prompt", "text": "保持 @person 的人物外观，参考 @motion 的动作节奏，在明亮室内完成同样动作。"},
      {"type": "refer_image", "url": "https://example.com/person.jpg", "id": "person"},
      {"type": "feature_video", "url": "https://example.com/motion.mp4", "id": "motion"}
    ],
    "settings": {
      "resolution": "720p",
      "duration": 5,
      "aspect_ratio": "16:9",
      "audio": "native"
    }
  }'
```

- 4.0 的 `settings.resolution` 可填 `720p` / `1080p`，`duration` 为 3–30 的整数秒数；Flash 使用 `720p`、3–20 秒。不要沿用旧版顶层 `image`、`mode`、`duration` 等视频参数。
- 素材 `id` 保持唯一，在提示词中用 `@id` 明确引用对象；视频素材仅用于 Omni。
- 4.0 Omni 的 `settings.audio` 为 `native` / `original`。

完整字段与素材约束见文末的 4.0、Flash 官方网页及 Markdown。

## Video 3.0

3.0 系列使用 V1 接口，按模型选择工作流：

| 模型 / 能力 | TokenDance 提交路径 | 协议说明 |
|---|---|---|
| 3.0 / Turbo 文生视频 | `/gateway/kling/v1/text2video` | [网页](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%E6%96%87%E7%94%9F%E8%A7%86%E9%A2%91.md) · [Markdown](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%E6%96%87%E7%94%9F%E8%A7%86%E9%A2%91.md) |
| 3.0 / Turbo 图生视频 | `/gateway/kling/v1/image2video` | [网页](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%E5%9B%BE%E7%94%9F%E8%A7%86%E9%A2%91.md) · [Markdown](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%E5%9B%BE%E7%94%9F%E8%A7%86%E9%A2%91.md) |
| 3.0 Omni 参考与编辑 | `/gateway/kling/v1/omni-video` | [网页](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%20Omni%20Video.md) · [Markdown](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%20Omni%20Video.md) |
| 3.0 动作控制 | `/gateway/kling/v1/motion-control` | [网页](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%E5%8A%A8%E4%BD%9C%E6%8E%A7%E5%88%B6.md) · [Markdown](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%E5%8A%A8%E4%BD%9C%E6%8E%A7%E5%88%B6.md) |

图生视频中，3.0 支持首尾帧，Turbo 仅首帧。3.0 Omni 的 `settings.audio` 使用 `off` / `on`；动作控制使用人物图片与动作参考视频，具体字段见对应协议说明。

## 其他能力

除视频生成外，还支持**语音合成**（将文本转为语音）、**数字人**（用人物图片和音频生成说话视频），以及**视频特效**（按模板将图片生成带特定效果的视频）。

| 能力 | TokenDance 提交路径 | 协议说明 |
|---|---|---|
| 语音合成 | `/gateway/kling/v1/audio/tts` | [网页](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E8%AF%AD%E9%9F%B3/%E5%8F%AF%E7%81%B5%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90.md) · [Markdown](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E8%AF%AD%E9%9F%B3/%E5%8F%AF%E7%81%B5%E8%AF%AD%E9%9F%B3%E5%90%88%E6%88%90.md) |
| 数字人 | `/gateway/kling/v1/videos/avatar/image2video` | [网页](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%E6%95%B0%E5%AD%97%E4%BA%BA.md) · [Markdown](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%E6%95%B0%E5%AD%97%E4%BA%BA.md) |
| 视频特效 | `/gateway/kling/v1/videos/effects` | [网页](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%E8%A7%86%E9%A2%91%E7%89%B9%E6%95%88.md) · [Markdown](../../%E5%A4%9A%E6%A8%A1%E6%80%81%E5%8D%8F%E8%AE%AE/%E5%9B%BE%E5%83%8F%E4%B8%8E%E8%A7%86%E9%A2%91/%E5%8F%AF%E7%81%B5%E8%A7%86%E9%A2%91%E7%89%B9%E6%95%88.md) |

- **语音合成**：`voice_id` 从[官方音色试听表](https://docs.qingque.cn/s/home/eZQDvafJ4vXQkP8T9ZPvmye8S?identityId=2E1MlYrrPk4)选择；`voice_language` 为 `zh` / `en`，文本最多 1000 字符，`voice_speed` 为 0.8–2.0。
- **数字人**：人物图片配合 `sound_file` 或 `audio_id`，两者选一；音频 2–300 秒，`mode` 为 `std` / `pro`。使用 TTS 音频 ID 前，确认当前数字人服务商能识别该资源。
- **视频特效**：从[官方模板中心](https://klingai.com/document-api/api/effects/templates)选择 `effect_scene`；单图传 `input.image`，双图传 `input.images`。模板供给以[模型页](https://tokendance.space/models/kling-effects)为准。

## 任务结果

异步接口在原提交路径后追加 `/{task_id}`，通过 GET 查询：

| 工作流 | 任务 ID | 成功状态 | 结果 URL |
|---|---|---|---|
| 3.0 / 4.0 视频、动作控制 | `data.id` | `data.status == succeeded` | `data.outputs[]` 中 `type == video` 的 `url` |
| 数字人、视频特效 | `data.task_id` | `data.task_status == succeed` | `data.task_result.videos[].url` |
| 语音合成（同步，无需查询） | — | `data.task_status == succeed` | `data.task_result.audios[].url` |

视频接口的 `data` 若为数组，先取首项，再读取上表字段。`submitted` / `processing` 为处理中，`failed` 为失败。提交超时先核实任务，避免重复生成；成功后及时转存结果。

## 官方资料

以下为可灵官网资料；通过 TokenDance 调用时，使用上文网关路径及模型 ID。更多资料见[官网文档索引](https://klingai.com/document-api/llms.txt)。

| 能力 | 人类阅读 | AI 阅读 |
|---|---|---|
| 视频模型能力地图 | [网页](https://klingai.com/document-api/guides/capability-map/video) | [Markdown](https://klingai.com/document-api/guides/capability-map/video.md) |
| 4.0 文生视频 | [网页](https://klingai.com/document-api/api/video/4-0/text-to-video) | [Markdown](https://klingai.com/document-api/api/video/4-0/text-to-video.md) |
| 4.0 图生视频 | [网页](https://klingai.com/document-api/api/video/4-0/image-to-video) | [Markdown](https://klingai.com/document-api/api/video/4-0/image-to-video.md) |
| 4.0 Omni / 编辑 | [网页](https://klingai.com/document-api/api/video/4-0/video-omni) | [Markdown](https://klingai.com/document-api/api/video/4-0/video-omni.md) |
| 4.0 Flash 文生视频 | [网页](https://klingai.com/document-api/api/video/4-0-flash/text-to-video) | [Markdown](https://klingai.com/document-api/api/video/4-0-flash/text-to-video.md) |
| 4.0 Flash 图生视频 | [网页](https://klingai.com/document-api/api/video/4-0-flash/image-to-video) | [Markdown](https://klingai.com/document-api/api/video/4-0-flash/image-to-video.md) |
| 4.0 Flash Omni / 编辑 | [网页](https://klingai.com/document-api/api/video/4-0-flash/video-omni) | [Markdown](https://klingai.com/document-api/api/video/4-0-flash/video-omni.md) |
| 3.0 文生视频 | [网页](https://klingai.com/document-api/api/video/3-0-omni/text-to-video) | [Markdown](https://klingai.com/document-api/api/video/3-0-omni/text-to-video.md) |
| 3.0 图生视频 | [网页](https://klingai.com/document-api/api/video/3-0-omni/image-to-video) | [Markdown](https://klingai.com/document-api/api/video/3-0-omni/image-to-video.md) |
| 3.0 Omni | [网页](https://klingai.com/document-api/api/video/3-0-omni/video-omni) | [Markdown](https://klingai.com/document-api/api/video/3-0-omni/video-omni.md) |
| 3.0 Turbo 文生视频 | [网页](https://klingai.com/document-api/api/video/3-0-turbo/text-to-video) | [Markdown](https://klingai.com/document-api/api/video/3-0-turbo/text-to-video.md) |
| 3.0 Turbo 图生视频 | [网页](https://klingai.com/document-api/api/video/3-0-turbo/image-to-video) | [Markdown](https://klingai.com/document-api/api/video/3-0-turbo/image-to-video.md) |
| 动作控制 | [网页](https://klingai.com/document-api/api/video/motion-control) | [Markdown](https://klingai.com/document-api/api/video/motion-control.md) |
| 语音合成 | [网页](https://klingai.com/document-api/api/video/avatar/text-to-speech) | [Markdown](https://klingai.com/document-api/api/video/avatar/text-to-speech.md) |
| 数字人 | [网页](https://klingai.com/document-api/api/video/avatar) | [Markdown](https://klingai.com/document-api/api/video/avatar.md) |
| 视频特效 | [网页](https://klingai.com/document-api/api/effects/video-effects) | [Markdown](https://klingai.com/document-api/api/effects/video-effects.md) |
| 4.0 自定义音色 | [网页](https://klingai.com/document-api/api/video/4-0/voice-customization) | [Markdown](https://klingai.com/document-api/api/video/4-0/voice-customization.md) |
| 4.0 提示词与使用手册 | [网页](https://klingai.com/document-api/api/usage-guide/kling-4-0) | [Markdown](https://klingai.com/document-api/api/usage-guide/kling-4-0.md) |

自定义音色、主体等资源 ID 需与所用服务商匹配，官网资源管理接口不代表 TokenDance 已开放同名接口。
