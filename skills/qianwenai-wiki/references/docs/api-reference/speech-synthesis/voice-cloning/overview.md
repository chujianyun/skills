> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 声音复刻 HTTP API

> 声音复刻 HTTP API 概述，包含请求头、服务端点和音色状态说明。

声音复刻 API 支持通过上传音频创建自定义克隆音色，并管理音色的完整生命周期（创建、查询、更新、列表、删除）。

**用户指南**：[声音复刻](/developer-guides/speech/voice-cloning)。

## 服务端点

```
POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization
```

所有声音复刻操作（创建、查询、更新、列表、删除）共享同一端点，通过请求体中的 `action` 字段区分操作类型。

## 请求头

| 参数            | 类型     | 是否必选 | 说明                          |
| ------------- | ------ | ---- | --------------------------- |
| Authorization | string | 是    | `Bearer $DASHSCOPE_API_KEY` |
| Content-Type  | string | 是    | 固定为 `application/json`。     |

## 支持的模型

声音复刻支持两套 API：

| 模型                            | 适用场景                | 支持的操作          |
| ----------------------------- | ------------------- | -------------- |
| `voice-enrollment`（CosyVoice） | CosyVoice 系列模型的声音复刻 | 创建、查询、更新、列表、删除 |
| `qwen-voice-enrollment`（Qwen） | Qwen-TTS 系列模型的声音复刻  | 创建、列表、删除       |

<Note>
  两套 API 的操作互相独立：CosyVoice 创建的音色仅能用于 CosyVoice 合成，Qwen 创建的音色仅能用于 Qwen-TTS 合成。
</Note>

## 音色状态说明

创建音色后，系统会自动进行审核。音色状态可通过[查询音色详情](/api-reference/speech-synthesis/voice-cloning/cosyvoice/query-voice)接口获取。

| 状态           | 说明          |
| ------------ | ----------- |
| `DEPLOYING`  | 审核中/处理中。    |
| `OK`         | 审核通过，可正常使用。 |
| `UNDEPLOYED` | 审核未通过，不可使用。 |

## API 索引

### CosyVoice（`voice-enrollment`）

| 操作     | 页面                                                                              |
| ------ | ------------------------------------------------------------------------------- |
| 创建音色   | [创建克隆音色](/api-reference/speech-synthesis/voice-cloning/cosyvoice/create-voice)  |
| 查询音色详情 | [查询克隆音色](/api-reference/speech-synthesis/voice-cloning/cosyvoice/query-voice)   |
| 更新音色   | [更新克隆音色](/api-reference/speech-synthesis/voice-cloning/cosyvoice/update-voice)  |
| 查询列表   | [查询克隆音色列表](/api-reference/speech-synthesis/voice-cloning/cosyvoice/list-voices) |
| 删除音色   | [删除克隆音色](/api-reference/speech-synthesis/voice-cloning/cosyvoice/delete-voice)  |

### Qwen（`qwen-voice-enrollment`）

| 操作   | 页面                                                                    |
| ---- | --------------------------------------------------------------------- |
| 创建音色 | [创建克隆音色](/api-reference/speech-synthesis/voice-cloning/create-voice)  |
| 查询列表 | [查询克隆音色列表](/api-reference/speech-synthesis/voice-cloning/list-voices) |
| 删除音色 | [删除克隆音色](/api-reference/speech-synthesis/voice-cloning/delete-voice)  |
