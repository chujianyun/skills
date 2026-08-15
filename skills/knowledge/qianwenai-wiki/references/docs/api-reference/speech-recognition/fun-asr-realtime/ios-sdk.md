> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Fun-ASR 实时语音识别 iOS SDK

> 本文档提供了Fun-ASR实时语音识别iOS SDK的详细使用指南，帮助您将语音转换为文本。

**使用指南**： 模型选择请参见[实时语音识别](/developer-guides/speech/asr-realtime)。

## 快速开始

### 前提条件

- 已[获取API Key](/api-reference/preparation/api-key)并[配置到环境变量](/api-reference/preparation/export-api-key-env)
- 已下载iOS SDK（请联系服务支持获取下载链接）

### SDK集成

1. 解压下载的压缩包，找到 `nuisdk.framework`
2. 将 `nuisdk.framework` 拖入Xcode项目中，在 **Build Phases** → **Link Binary With Libraries** 中添加该framework
3. 在 **General** → **Frameworks, Libraries, and Embedded Content** 中将 `nuisdk.framework` 设置为 **Embed & Sign**
4. 打开 `example` 目录下的示例项目进行参考

示例代码中的主要类为 `DashFunAsrSpeechTranscriberViewController`。

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
        "model": "fun-asr-realtime",
        "sr_format": "pcm",
        "sample_rate": "16000",
        "parameters": {
            "speech_noise_threshold": 0.0
        }
    }
}
```

| 参数                                              | 类型             | 必须 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------------------------------- | -------------- | -- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| service\_type                                   | int            | 是  | 固定为 `4`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| nls\_config                                     | object         | 是  | 语音识别核心配置对象                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| nls\_config.model                               | string         | 是  | 语音识别模型名称                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| nls\_config.sr\_format                          | string         | 是  | 音频格式，支持 `pcm` / `wav` / `opus`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| nls\_config.sample\_rate                        | int            | 是  | 采样率（Hz）。8k 模型仅支持 8000 Hz，其他模型支持任意采样率。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| nls\_config.semantic\_punctuation\_enabled      | boolean        | 否  | 断句模式。默认 `false`（VAD断句）                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| nls\_config.max\_sentence\_silence              | int            | 否  | VAD静音阈值（ms）。默认 `800`，范围 `[200, 6000]`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| nls\_config.multi\_threshold\_mode\_enabled     | boolean        | 否  | 防过长切割模式。默认 `false`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| nls\_config.heartbeat                           | boolean        | 否  | 保持长连接。默认 `false`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| nls\_config.vocabulary\_id                      | string         | 否  | 热词词表ID。参见[自定义热词](/developer-guides/speech/improve-recognition-accuracy)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| nls\_config.language\_hints                     | array\[string] | 否  | 识别语言代码。不设置时自动检测语言。不同模型支持的语言代码如下：<br /> **fun-asr-realtime、fun-asr-realtime-2025-11-07**：`zh`（中文）、`en`（英文）、`ja`（日语）、`ko`（韩语）、`vi`（越南语）、`th`（泰语）、`id`（印尼语）、`ms`（马来语）、`tl`（菲律宾语）、`hi`（印地语）、`ar`（阿拉伯语）、`fr`（法语）、`de`（德语）、`es`（西班牙语）、`pt`（葡萄牙语）、`ru`（俄语）、`it`（意大利语）、`nl`（荷兰语）、`sv`（瑞典语）、`da`（丹麦语）、`fi`（芬兰语）、`no`（挪威语）、`el`（希腊语）、`pl`（波兰语）、`cs`（捷克语）、`hu`（匈牙利语）、`ro`（罗马尼亚语）、`bg`（保加利亚语）、`hr`（克罗地亚语）、`sk`（斯洛伐克语）<br /> **fun-asr-realtime-2026-02-28**：`zh`（中文）、`en`（英文）、`ja`（日语）<br /> **fun-asr-realtime-2025-09-15**：`zh`（中文）、`en`（英文）<br /> **fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28**：`zh`（中文） |
| nls\_config.parameters                          | object         | 否  | 配置其他参数，内容为JSON Object格式                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| nls\_config.parameters.speech\_noise\_threshold | float          | 否  | 语音噪声检测阈值，用于调节VAD灵敏度。取值范围：`[-1.0, 1.0]`。接近 -1：更多噪声可能被识别为语音；接近 +1：部分语音可能被过滤为噪声                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |

<Warning>
  `speech_noise_threshold` 是高级参数，微小的调整会显著影响识别质量。建议以 0.1 为步长逐步调整，并充分测试。
</Warning>

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
