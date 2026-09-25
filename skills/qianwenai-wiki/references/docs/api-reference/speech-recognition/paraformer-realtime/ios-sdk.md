> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Paraformer 实时语音识别 iOS SDK

> 本文档提供了Paraformer实时语音识别iOS SDK的详细使用指南，帮助您将语音转换为文本。

## 快速开始

### 前提条件

- 已[获取API Key](/api-reference/preparation/api-key)并[配置到环境变量](/api-reference/preparation/export-api-key-env)
- 已下载iOS SDK（请联系服务支持获取下载链接）

### SDK集成

1. 解压下载的压缩包，找到 `nuisdk.framework`
2. 将 `nuisdk.framework` 拖入Xcode项目中，在 **Build Phases** → **Link Binary With Libraries** 中添加该framework
3. 将framework的Embed选项设置为 **Embed & Sign**
4. 打开 `example` 目录下的示例项目进行参考

示例代码中的主要类为 `DashParaformerSpeechTranscriberViewController`。

### 调用流程

<Steps>
  <Step title="初始化 SDK">
    调用 `nui_initialize` 完成SDK初始化，传入连接与控制参数。
  </Step>

  <Step title="设置参数">
    调用 `nui_set_params` 设置语音识别效果参数（模型、采样率、音频格式等）。
  </Step>

  <Step title="启动识别流程">
    调用 `nui_dialog_start` 启动识别流程。
  </Step>

  <Step title="开启录音设备">
    在 `onNuiAudioStateChanged` 回调中监听 `STATE_OPEN` 状态，收到后开启录音设备。
  </Step>

  <Step title="持续提供录音数据">
    在 `onNuiNeedAudioData` 回调中持续将录音数据填入提供的缓冲区。
  </Step>

  <Step title="监听事件并获取识别结果">
    在 `onNuiEventCallback` 回调中监听各类事件，并通过 `asr_result` 参数获取语音识别结果。
  </Step>

  <Step title="停止识别">
    调用 `nui_dialog_cancel` 停止识别，并监听 `EVENT_TRANSCRIBER_COMPLETE` 事件确认结束。
  </Step>

  <Step title="释放SDK资源">
    调用 `nui_release` 释放SDK资源。
  </Step>
</Steps>

## 连接与控制参数

通过 `nui_initialize` 方法传入以下JSON格式的连接参数：

```json
{
    "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

| 参数                   | 类型     | 必须 | 说明                                                                        |
| -------------------- | ------ | -- | ------------------------------------------------------------------------- |
| url                  | String | 是  | 固定为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`                    |
| apikey               | String | 是  | API Key，建议使用[临时API Key](/api-reference/more/generate-a-temporary-api-key) |
| service\_mode        | String | 是  | 实时语音识别固定为 `"1"`                                                           |
| device\_id           | String | 是  | 唯一终端用户标识字符串                                                               |
| debug\_path          | String | 否  | 日志文件路径，`save_log=YES` 时生效，本地最多保留两个日志文件                                    |
| save\_wav            | String | 否  | 是否保存调试音频。默认 `"false"`                                                     |
| max\_log\_file\_size | int    | 否  | 日志文件最大字节数。默认 `104857600`（100 MiB）                                         |
| log\_track\_level    | int    | 否  | 日志回调过滤级别。默认 `2`。取值：`0`=VERBOSE \~ `5`=NONE                                |

## 语音识别效果参数

通过 `nui_set_params` 方法传入以下JSON格式的识别参数：

```json
{
    "service_type": 4,
    "nls_config": {
        "model": "paraformer-realtime-v2",
        "sr_format": "pcm",
        "sample_rate": "16000"
    }
}
```

| 参数                                                | 类型             | 必须 | 说明                                                                                    |
| ------------------------------------------------- | -------------- | -- | ------------------------------------------------------------------------------------- |
| service\_type                                     | int            | 是  | 固定为 `4`                                                                               |
| nls\_config                                       | object         | 是  | 语音识别核心配置对象                                                                            |
| nls\_config.model                                 | string         | 是  | 语音识别模型名称                                                                              |
| nls\_config.sr\_format                            | string         | 是  | 音频格式，支持 `pcm` / `wav` / `opus`                                                        |
| nls\_config.sample\_rate                          | int            | 是  | 采样率（Hz），取值因模型而异                                                                       |
| nls\_config.disfluency\_removal\_enabled          | boolean        | 否  | 是否过滤语气词。默认 `false`                                                                    |
| nls\_config.language\_hints                       | array\[string] | 否  | 语言代码列表，支持 `zh` / `en` / `ja` / `yue` / `ko` / `de` / `fr` / `ru`                      |
| nls\_config.semantic\_punctuation\_enabled        | boolean        | 否  | 断句模式。默认 `false`（VAD断句）                                                                |
| nls\_config.max\_sentence\_silence                | int            | 否  | VAD静音阈值（ms）。默认 `800`，范围 `[200, 6000]`                                                 |
| nls\_config.multi\_threshold\_mode\_enabled       | boolean        | 否  | 防过长切割模式。默认 `false`                                                                    |
| nls\_config.punctuation\_prediction\_enabled      | boolean        | 否  | 自动添加标点。默认 `true`                                                                      |
| nls\_config.heartbeat                             | boolean        | 否  | 保持长连接。默认 `false`                                                                      |
| nls\_config.inverse\_text\_normalization\_enabled | boolean        | 否  | ITN逆文本正则化。默认 `true`                                                                   |
| nls\_config.vocabulary\_id                        | string         | 否  | 热词词表ID，适用于 v2 及以上模型。参见[自定义热词](/developer-guides/speech/improve-recognition-accuracy)  |
| nls\_config.resources                             | array\[object] | 否  | 热词资源配置，适用于 v1 模型。参见[热词管理](/api-reference/speech-recognition/custom-hotwords/http-api) |

### v1模型热词配置示例

```json
{
    "nls_config": {
        "resources": [
            {
                "resource_id": "xxxxxxxxxxxx",
                "resource_type": "asr_phrase"
            }
        ]
    }
}
```

## 关键接口

### NeoNui

#### nui\_initialize

初始化SDK，传入连接参数。

```objectivec
-(NuiResultCode) nui_initialize:(const char *)parameters
                       logLevel:(NuiSdkLogLevel)level
                        saveLog:(BOOL)save_log;
```

| 参数         | 类型             | 说明             |
| ---------- | -------------- | -------------- |
| parameters | const char\*   | JSON格式的连接参数字符串 |
| level      | NuiSdkLogLevel | 日志级别           |
| save\_log  | BOOL           | 是否保存日志到本地文件    |

返回值：`NuiResultCode` 错误码。

#### nui\_set\_params

设置语音识别效果参数。

```objectivec
-(NuiResultCode) nui_set_params:(const char *)params;
```

| 参数     | 类型           | 说明             |
| ------ | ------------ | -------------- |
| params | const char\* | JSON格式的识别参数字符串 |

返回值：`NuiResultCode` 错误码。

#### nui\_dialog\_start

启动语音识别流程。

```objectivec
-(NuiResultCode) nui_dialog_start:(NuiVadMode)vad_mode
                      dialogParam:(const char *)dialog_params;
```

| 参数             | 类型           | 说明                           |
| -------------- | ------------ | ---------------------------- |
| vad\_mode      | NuiVadMode   | 固定使用 `MODE_P2T`              |
| dialog\_params | const char\* | 可在此传入更新后的 apikey（临时Key过期时使用） |

`dialog_params` 示例：

```json
{
  "apikey": "st-****"
}
```

返回值：`NuiResultCode` 错误码。

#### nui\_dialog\_cancel

停止语音识别。

```objectivec
-(NuiResultCode) nui_dialog_cancel:(BOOL)force;
```

| 参数    | 类型   | 说明                                    |
| ----- | ---- | ------------------------------------- |
| force | BOOL | `YES`：立即结束，不等待最终识别结果；`NO`：等待完整识别结果后结束 |

返回值：`NuiResultCode` 错误码。

#### nui\_release

释放SDK资源。

```objectivec
-(NuiResultCode) nui_release;
```

返回值：`NuiResultCode` 错误码。

#### nui\_get\_version

获取SDK版本号。

```objectivec
-(const char*) nui_get_version;
```

返回值：当前SDK版本字符串。

#### nui\_get\_all\_response

获取完整的事件信息。

```objectivec
-(const char*) nui_get_all_response;
```

返回值：包含完整事件信息的JSON字符串。

### NeoNuiSdkDelegate

#### onNuiEventCallback

监听识别事件并获取识别结果。

```objectivec
-(void) onNuiEventCallback:(NuiCallbackEvent)nuiEvent
                    dialog:(long)dialog
                 kwsResult:(const char *)wuw
                 asrResult:(const char *)asr_result
                  ifFinish:(BOOL)finish
                   retCode:(int)code;
```

| 参数          | 类型               | 说明                                                                               |
| ----------- | ---------------- | -------------------------------------------------------------------------------- |
| nuiEvent    | NuiCallbackEvent | 事件类型，见下方事件列表                                                                     |
| dialog      | long             | 会话标识，可忽略                                                                         |
| wuw         | const char\*     | 唤醒词，实时识别场景可忽略                                                                    |
| asr\_result | const char\*     | 语音识别结果                                                                           |
| finish      | BOOL             | 是否为最终结果                                                                          |
| code        | int              | 错误码，仅在 `EVENT_ASR_ERROR` 时有效，参见[错误信息](/api-reference/preparation/error-messages) |

#### onNuiAudioStateChanged

监听录音设备状态变化。

```objectivec
-(void) onNuiAudioStateChanged:(NuiAudioState)state;
```

| NuiAudioState 取值 | 说明                |
| ---------------- | ----------------- |
| STATE\_OPEN      | 需要开启录音设备并开始录音     |
| STATE\_PAUSE     | 需要停止录音（暂停）        |
| STATE\_CLOSE     | SDK已释放，需要完全关闭录音设备 |

#### onNuiNeedAudioData

SDK请求录音数据时触发，需将录音数据填入提供的缓冲区。

```objectivec
-(int) onNuiNeedAudioData:(char *)audioData length:(int)len;
```

| 参数        | 类型     | 说明           |
| --------- | ------ | ------------ |
| audioData | char\* | 需要填充的音频数据缓冲区 |
| len       | int    | 需要填充的字节数     |

#### onNuiLogTrackCallback

接收SDK日志回调。

```objectivec
-(void) onNuiLogTrackCallback:(NuiSdkLogLevel)level
                   logMessage:(const char *)log;
```

| 参数    | 类型             | 说明   |
| ----- | -------------- | ---- |
| level | NuiSdkLogLevel | 日志级别 |
| log   | const char\*   | 日志内容 |

### NuiCallbackEvent 事件说明

| 事件                           | 说明                  |
| ---------------------------- | ------------------- |
| EVENT\_TRANSCRIBER\_STARTED  | 任务启动成功              |
| EVENT\_VAD\_START            | 任务启动后即触发，不代表检测到人声起点 |
| EVENT\_VAD\_END              | 检测到人声终点             |
| EVENT\_ASR\_PARTIAL\_RESULT  | 语音识别中间结果            |
| EVENT\_ASR\_ERROR            | 语音识别过程中出现错误         |
| EVENT\_MIC\_ERROR            | 因连续2秒未收到任何音频数据而触发   |
| EVENT\_SENTENCE\_END         | 检测到一句话结束，返回完整识别结果   |
| EVENT\_TRANSCRIBER\_COMPLETE | 语音识别结束              |
