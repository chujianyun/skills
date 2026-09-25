> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 声音设计 HTTP API

> 声音设计 HTTP API 概述，包含请求头、服务端点和音色状态说明。

声音设计 API 支持通过文字描述创建自定义音色，系统根据描述生成对应特征的合成声音。

**用户指南**：[声音设计](/developer-guides/speech/voice-design)。

## 服务端点

```
POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization
```

## 请求头

| 参数            | 类型     | 是否必选 | 说明                                    |
| ------------- | ------ | ---- | ------------------------------------- |
| Authorization | string | 是    | 鉴权令牌，格式为 `Bearer $DASHSCOPE_API_KEY`。 |
| Content-Type  | string | 是    | 固定为 `application/json`。               |

## 支持的模型

| 模型                            | 适用场景                | 支持的操作       |
| ----------------------------- | ------------------- | ----------- |
| `voice-enrollment`（CosyVoice） | CosyVoice 系列模型的声音设计 | 创建、查询、列表、删除 |
| `qwen-voice-design`（Qwen）     | Qwen-TTS 系列模型的声音设计  | 创建、查询、列表、删除 |

## 音色状态说明

| 状态           | 说明          |
| ------------ | ----------- |
| `DEPLOYING`  | 审核中/处理中。    |
| `OK`         | 审核通过，可正常使用。 |
| `UNDEPLOYED` | 审核未通过，不可使用。 |

## API 索引

### CosyVoice（`voice-enrollment`）

| 操作     | 页面                                                                             |
| ------ | ------------------------------------------------------------------------------ |
| 创建音色   | [创建设计音色](/api-reference/speech-synthesis/voice-design/cosyvoice/create-voice)  |
| 查询音色详情 | [查询设计音色](/api-reference/speech-synthesis/voice-design/cosyvoice/query-voice)   |
| 查询列表   | [查询设计音色列表](/api-reference/speech-synthesis/voice-design/cosyvoice/list-voices) |
| 删除音色   | [删除设计音色](/api-reference/speech-synthesis/voice-design/cosyvoice/delete-voice)  |

### Qwen（`qwen-voice-design`）

| 操作   | 页面                                                                   |
| ---- | -------------------------------------------------------------------- |
| 创建音色 | [创建设计音色](/api-reference/speech-synthesis/voice-design/create-voice)  |
| 查询列表 | [查询设计音色列表](/api-reference/speech-synthesis/voice-design/list-voices) |
| 查询详情 | [查询设计音色详情](/api-reference/speech-synthesis/voice-design/query-voice) |
| 删除音色 | [删除设计音色](/api-reference/speech-synthesis/voice-design/delete-voice)  |
