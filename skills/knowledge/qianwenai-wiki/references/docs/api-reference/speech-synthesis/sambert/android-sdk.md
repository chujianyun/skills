> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sambert 语音合成 Android SDK

> 使用原生 SDK 将 Sambert 模型的实时文本转语音功能集成到 Android 应用中。

本文档提供了语音合成 Sambert Android SDK 的详细使用指南，帮助您将文本转换为高质量、富有表现力的语音。

**用户指南**：关于模型介绍和选型建议请参见[语音合成模型](/developer-guides/speech/tts-models)。

**在线体验**：暂不支持。

## 快速开始

1. **获取 API Key**：[获取 API Key](/api-reference/preparation/api-key)，为安全起见，推荐将 API Key 配置到环境变量。

   <Note>
     当需要为第三方应用或用户提供临时访问权限，或者希望严格控制敏感数据访问、删除等高风险操作时，建议使用[临时 API Key](/api-reference/more/generate-a-temporary-api-key)。临时 API Key 默认拥有 60 秒有效期，过期后需重新获取。
   </Note>

2. **下载 SDK 并运行示例代码**：

   - 下载最新 SDK 整合包。
   - 解压 ZIP 包。在 `app/libs` 目录中获取 AAR 格式 SDK，并添加到项目依赖。需要 Android CPP 接入时，使用 ZIP 包内的 `android_libs` 与 `android_include` 获取动态库和头文件。
   - 用 Android Studio 打开工程。示例代码位于 `DashSambertTtsActivity.java`，替换 API Key 后体验功能。

### 调用步骤

1. 初始化 SDK。
2. 按业务需求设置参数：通过 [tts\_initialize](#tts-initialize) 接口的 `ticket` 参数设置[连接与控制参数](#连接与控制参数)；通过 [setparamTts](#setparamtts) 接口设置[语音合成效果参数](#语音合成效果参数)。
3. 调用 [startTts](#starttts) 开始语音合成。
4. 在 [onTtsDataCallback](#onttsdatacallback-监听音频数据和时间戳信息) 回调中获取音频数据，建议使用流式播放。如需保存本地，按追加模式将音频写入同一文件，直到合成完成。
5. 任务结束后，调用 [tts\_release](#tts-release) 释放 SDK 资源。

## 请求参数

### 连接与控制参数

通过在 [tts\_initialize](#tts-initialize) 接口的 `ticket` 参数中传入一个 JSON 字符串来配置。

**参数示例**：以下为 JSON 字符串示例，参数未完整列出。请按实际需求在编码时补充：

```json
{
  "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
  "apikey": "sk-ws-****",
  "device_id": "my_device_id"
}
```

**参数说明**：

| 参数                  | 类型     | 是否必须 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------- | ------ | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `url`               | String | 是    | 服务地址，固定为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`。                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `apikey`            | String | 是    | API Key。建议使用时效性短、安全性更高的[临时 API Key](/api-reference/more/generate-a-temporary-api-key)，以降低长期有效 Key 泄露的风险。                                                                                                                                                                                                                                                                                                                                                                             |
| `mode_type`         | String | 是    | 模式类型。必须设置为字符串 `"2"`，代表在线语音合成模式。                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `device_id`         | String | 是    | 用于标识终端用户的唯一字符串，可设为应用内用户 ID 或客户端生成的设备唯一标识符。此 ID 主要用于日志追踪和问题排查。                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `debug_path`        | String | 否    | 日志文件的存储路径。此参数仅在调用 [tts\_initialize](#tts-initialize) 接口时将 `save_log` 设为 true 时生效。此时必须设置日志文件路径，否则将报错。本地最多保留两个日志文件。                                                                                                                                                                                                                                                                                                                                                                    |
| `max_log_file_size` | int    | 否    | 设定日志文件的最大字节数。此参数仅在调用 [tts\_initialize](#tts-initialize) 接口时将 `save_log` 设为 true 时生效。默认值：104857600（100 \* 1024 \* 1024 字节，即 100 MiB）。                                                                                                                                                                                                                                                                                                                                                 |
| `log_track_level`   | int    | 否    | 控制通过日志回调（[onTtsLogTrackCallback](#onttslogtrackcallback-监听追踪日志)）对外发送的日志内容的过滤级别。默认值：2。取值范围：0（LOG\_LEVEL\_VERBOSE）、1（LOG\_LEVEL\_DEBUG）、2（LOG\_LEVEL\_INFO）、3（LOG\_LEVEL\_WARNING）、4（LOG\_LEVEL\_ERROR）、5（LOG\_LEVEL\_NONE，表示关闭此功能）。注意：`log_track_level` 与 `log_level`（通过 [tts\_initialize](#tts-initialize) 接口设置）共同决定最终回调的日志。一条日志的级别数值必须同时大于或等于 `log_track_level` 和 `log_level` 的值，才会被回调。例如，`log_track_level` 设为 2（INFO），`log_level` 设为 3（WARNING），则只有 WARNING 及以上级别（数值 >=3）的日志才会被回调。 |

### 语音合成效果参数

通过 [setparamTts](#setparamtts) 接口进行设置。

| 参数                          | 类型     | 是否必须 | 说明                                                                                                                  |
| --------------------------- | ------ | ---- | ------------------------------------------------------------------------------------------------------------------- |
| `model`                     | String | 是    | 语音合成[模型](#模型列表)。                                                                                                    |
| `format`                    | String | 否    | 音频编码格式。支持 pcm、wav、mp3。默认值：pcm。                                                                                      |
| `volume`                    | String | 否    | 音量。默认值：50。取值范围：\[0, 100]。50 代表标准音量。音量大小与该值呈线性关系，0 为静音，100 为最大音量。                                                    |
| `sample_rate`               | String | 否    | 采样率（单位 Hz）。默认值：[模型](#模型列表)对应的默认采样率。推荐使用模型的默认值。若不匹配，服务端会进行重采样。                                                       |
| `rate`                      | String | 否    | 语速。默认值：1.0。取值范围：\[0.5, 2.0]。1.0 为标准语速，小于 1.0 则减慢，大于 1.0 则加快。                                                        |
| `pitch`                     | String | 否    | 音高。该值作为音高调节的乘数，但其与听感上的音高变化并非严格的线性或对数关系，建议通过测试选择合适的值。默认值：1.0。取值范围：\[0.5, 2.0]。1.0 为音色自然音高。大于 1.0 则音高变高，小于 1.0 则音高变低。 |
| `word_timestamp_enabled`    | String | 否    | 是否开启字级别时间戳。默认值：0。取值范围：1（开启）、0（关闭）。                                                                                  |
| `phoneme_timestamp_enabled` | String | 否    | 是否开启音素级别时间戳。此参数仅在 `word_timestamp_enabled` 设为 1（开启）时生效。默认值：0。取值范围：1（开启）、0（关闭）。                                      |
| `enable_audio_decoder`      | String | 否    | 是否开启内置音频解码器。默认值：0。取值范围：1（开启，当 format 为 mp3 时，设为 "1" 可开启 SDK 内置解码器，此时 onTtsDataCallback 将返回解码后的 PCM 数据）、0（关闭）。       |

## 关键接口

### NativeNui

#### tts\_initialize

初始化语音合成 SDK 实例。SDK 为单例模式，在调用 [tts\_release](#tts-release) 前禁止重复初始化。

<Warning>
  此接口会引起阻塞，应在非 UI 线程调用。
</Warning>

**方法签名**

```java
public synchronized int tts_initialize(INativeTtsCallback callback,
                                       String ticket,
                                       final Constants.LogLevel level,
                                       boolean save_log)
```

**参数说明**

| 参数         | 类型                                             | 说明                                                                                             |
| ---------- | ---------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `callback` | [INativeTtsCallback](#inativettscallback-监听回调) | 事件和数据回调接口的实现。                                                                                  |
| `ticket`   | String                                         | JSON 字符串，包含鉴权、连接和调试参数。参见[连接与控制参数](#连接与控制参数)。                                                   |
| `level`    | Constants.LogLevel                             | 控制 SDK 自身日志的打印级别。                                                                              |
| `save_log` | boolean                                        | 是否保存本地日志。若为 `true`，须在[连接与控制参数](#连接与控制参数)中通过 `debug_path` 指定路径，并可通过 `max_log_file_size` 设置文件大小。 |

**返回值说明**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### setparamTts

以键值对的形式设置[语音合成效果参数](#语音合成效果参数)。在 [startTts](#starttts) 之前调用。

**方法签名**

```java
public synchronized int setparamTts(String param, String value)
```

**参数说明**

| 参数      | 类型     | 说明                      |
| ------- | ------ | ----------------------- |
| `param` | String | [语音合成效果参数](#语音合成效果参数)名。 |
| `value` | String | [语音合成效果参数](#语音合成效果参数)值。 |

**返回值说明**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### getparamTts

获取参数值。主要用于错误排查。

**方法签名**

```java
public String getparamTts(String param);
```

**参数说明**

| 参数      | 类型     | 说明                     |
| ------- | ------ | ---------------------- |
| `param` | String | 参数。目前仅支持 "error\_msg"。 |

**返回值说明**

返回参数值。

---

#### startTts

启动语音合成任务。合成结果通过回调返回。

**方法签名**

```java
public synchronized int startTts(String priority, String taskid, String text)
```

**参数说明**

| 参数         | 类型     | 说明                           |
| ---------- | ------ | ---------------------------- |
| `priority` | String | 任务优先级。请将其设为 1。               |
| `taskid`   | String | 任务 ID。传入 `null` 时由 SDK 自动生成。 |
| `text`     | String | 待合成文本。                       |

**返回值说明**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### pauseTts

暂停当前语音合成任务。任务暂停后，可通过 [resumeTts](#resumetts) 恢复，或通过 [cancelTts](#canceltts) 彻底取消。在任务暂停期间，SDK 不支持启动新的合成任务。

<Note>
  此操作仅暂停从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。
</Note>

**方法签名**

```java
public synchronized int pauseTts()
```

**返回值说明**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### resumeTts

恢复处于暂停的语音合成任务。

**方法签名**

```java
public synchronized int resumeTts()
```

**返回值说明**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### cancelTts

取消合成任务。

<Note>
  此操作仅取消从服务端的数据拉取，播放器中已缓存的音频数据会继续播放。
</Note>

**方法签名**

```java
public synchronized int cancelTts(String taskid)
```

**参数说明**

| 参数       | 类型     | 说明                                       |
| -------- | ------ | ---------------------------------------- |
| `taskid` | String | 要取消的任务 ID。若传入 `null`，则取消所有正在暂停/进行中的合成任务。 |

**返回值说明**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

---

#### tts\_release

释放 SDK 所有内部资源，并强制终止所有正在进行的合成任务。此方法调用后，SDK 实例将变为不可用状态，如需再次使用，必须重新调用 [tts\_initialize](#tts-initialize) 进行初始化。

**方法签名**

```java
public synchronized int tts_release()
```

**返回值说明**

返回错误码，参见[错误码参考](/api-reference/preparation/error-messages)。

### INativeTtsCallback：监听回调

#### onTtsEventCallback：监听事件

**方法签名**

```java
void onTtsEventCallback(TtsEvent event, String task_id, int ret_code);
```

**参数说明**

| 参数         | 类型                         | 说明                                                                                   |
| ---------- | -------------------------- | ------------------------------------------------------------------------------------ |
| `event`    | [TtsEvent](#ttsevent-事件类型) | 回调事件。                                                                                |
| `task_id`  | String                     | 语音合成任务 ID。                                                                           |
| `ret_code` | int                        | 错误码，仅在事件 TTS\_EVENT\_ERROR 中有效。参见[错误码参考](/api-reference/preparation/error-messages)。 |

---

#### onTtsDataCallback：监听音频数据和时间戳信息

**方法签名**

```java
void onTtsDataCallback(String info, int info_len, byte[] data);
```

**参数说明**

| 参数         | 类型      | 说明                                                                         |
| ---------- | ------- | -------------------------------------------------------------------------- |
| `info`     | String  | JSON 格式的时间戳结果。[语音合成效果参数](#语音合成效果参数) `word_timestamp_enabled` 设为 `"1"` 时生效。 |
| `info_len` | int     | info 字段的数据长度，可忽略。                                                          |
| `data`     | byte\[] | 返回当前片段的音频数据。                                                               |

---

#### onTtsLogTrackCallback：监听追踪日志

此回调用于接收 SDK 内部的详细日志，方便进行问题定位和调试。

```java
default void onTtsLogTrackCallback(Constants.LogLevel level, String log)
```

### TtsEvent：事件类型

| 事件                 | 说明                                                   |
| ------------------ | ---------------------------------------------------- |
| TTS\_EVENT\_START  | 合成任务开始，即将有音频数据返回。                                    |
| TTS\_EVENT\_END    | 合成任务正常结束，所有音频数据已通过回调送出。                              |
| TTS\_EVENT\_CANCEL | 合成任务已取消。                                             |
| TTS\_EVENT\_PAUSE  | 合成任务已暂停。                                             |
| TTS\_EVENT\_RESUME | 合成任务已恢复。                                             |
| TTS\_EVENT\_ERROR  | 合成过程中发生错误。此时可通过 `getparamTts("error_msg")` 获取详细错误信息。 |

`TTS_EVENT_ERROR` 时错误响应结构示例：

```json
{
  "header": {
    "task_id": "xxxxxxxxx",
    "event": "task-failed",
    "error_code": "InvalidParameter",
    "error_message": "Please ensure input text is valid.",
    "attributes": {}
  },
  "payload": {}
}
```

## 模型列表

<Note>
  默认采样率代表当前模型的最佳采样率，缺省条件下默认按照该采样率输出，同时支持降采样或升采样。如知妙音色，默认采样率 16 kHz，使用时可以降采样到 8 kHz，但升采样到 48 kHz 时不会有额外效果提升。
</Note>

| 音色      | model 参数               | 时间戳支持 | 适用场景               | 特色     | 语言    | 默认采样率（Hz） |
| ------- | ---------------------- | ----- | ------------------ | ------ | ----- | --------- |
| 知楠      | sambert-zhinan-v1      | 是     | 通用场景               | 广告男声   | 中文+英文 | 48k       |
| 知琪      | sambert-zhiqi-v1       | 是     | 通用场景               | 温柔女声   | 中文+英文 | 48k       |
| 知厨      | sambert-zhichu-v1      | 是     | 新闻播报               | 舌尖男声   | 中文+英文 | 48k       |
| 知德      | sambert-zhide-v1       | 是     | 新闻播报               | 新闻男声   | 中文+英文 | 48k       |
| 知佳      | sambert-zhijia-v1      | 是     | 新闻播报               | 标准女声   | 中文+英文 | 48k       |
| 知茹      | sambert-zhiru-v1       | 是     | 新闻播报               | 新闻女声   | 中文+英文 | 48k       |
| 知倩      | sambert-zhiqian-v1     | 是     | 配音解说、新闻播报          | 资讯女声   | 中文+英文 | 48k       |
| 知祥      | sambert-zhixiang-v1    | 是     | 配音解说               | 磁性男声   | 中文+英文 | 48k       |
| 知薇      | sambert-zhiwei-v1      | 是     | 阅读产品简介             | 萝莉女声   | 中文+英文 | 48k       |
| 知浩      | sambert-zhihao-v1      | 是     | 通用场景               | 咨询男声   | 中文+英文 | 16k       |
| 知婧      | sambert-zhijing-v1     | 是     | 通用场景               | 严厉女声   | 中文+英文 | 16k       |
| 知茗      | sambert-zhiming-v1     | 是     | 通用场景               | 诙谐男声   | 中文+英文 | 16k       |
| 知墨      | sambert-zhimo-v1       | 是     | 通用场景               | 情感男声   | 中文+英文 | 16k       |
| 知娜      | sambert-zhina-v1       | 是     | 通用场景               | 浙普女声   | 中文+英文 | 16k       |
| 知树      | sambert-zhishu-v1      | 是     | 通用场景               | 资讯男声   | 中文+英文 | 16k       |
| 知莎      | sambert-zhistella-v1   | 是     | 通用场景               | 知性女声   | 中文+英文 | 16k       |
| 知婷      | sambert-zhiting-v1     | 是     | 通用场景               | 电台女声   | 中文+英文 | 16k       |
| 知笑      | sambert-zhixiao-v1     | 是     | 通用场景               | 资讯女声   | 中文+英文 | 16k       |
| 知雅      | sambert-zhiya-v1       | 是     | 通用场景               | 严厉女声   | 中文+英文 | 16k       |
| 知晔      | sambert-zhiye-v1       | 是     | 通用场景               | 青年男声   | 中文+英文 | 16k       |
| 知颖      | sambert-zhiying-v1     | 是     | 通用场景               | 软萌童声   | 中文+英文 | 16k       |
| 知媛      | sambert-zhiyuan-v1     | 是     | 通用场景               | 知心姐姐   | 中文+英文 | 16k       |
| 知悦      | sambert-zhiyue-v1      | 是     | 客服                 | 温柔女声   | 中文+英文 | 16k       |
| 知柜      | sambert-zhigui-v1      | 是     | 阅读产品简介             | 直播女声   | 中文+英文 | 16k       |
| 知硕      | sambert-zhishuo-v1     | 是     | 数字人                | 自然男声   | 中文+英文 | 16k       |
| 知妙（多情感） | sambert-zhimiao-emo-v1 | 是     | 阅读产品简介、数字人、直播      | 多种情感女声 | 中文+英文 | 16k       |
| 知猫      | sambert-zhimao-v1      | 是     | 阅读产品简介、配音解说、数字人、直播 | 直播女声   | 中文+英文 | 16k       |
| 知伦      | sambert-zhilun-v1      | 是     | 配音解说               | 悬疑解说   | 中文+英文 | 16k       |
| 知飞      | sambert-zhifei-v1      | 是     | 配音解说               | 激昂解说   | 中文+英文 | 16k       |
| 知达      | sambert-zhida-v1       | 是     | 新闻播报               | 标准男声   | 中文+英文 | 16k       |
| Camila  | sambert-camila-v1      | 否     | 通用场景               | 西班牙语女声 | 西班牙语  | 16k       |
| Perla   | sambert-perla-v1       | 否     | 通用场景               | 意大利语女声 | 意大利语  | 16k       |
| Indah   | sambert-indah-v1       | 否     | 通用场景               | 印尼语女声  | 印尼语   | 16k       |
| Clara   | sambert-clara-v1       | 否     | 通用场景               | 法语女声   | 法语    | 16k       |
| Hanna   | sambert-hanna-v1       | 否     | 通用场景               | 德语女声   | 德语    | 16k       |
| Beth    | sambert-beth-v1        | 是     | 通用场景               | 咨询女声   | 美式英文  | 16k       |
| Betty   | sambert-betty-v1       | 是     | 通用场景               | 客服女声   | 美式英文  | 16k       |
| Cally   | sambert-cally-v1       | 是     | 通用场景               | 自然女声   | 美式英文  | 16k       |
| Cindy   | sambert-cindy-v1       | 是     | 通用场景               | 对话女声   | 美式英文  | 16k       |
| Eva     | sambert-eva-v1         | 是     | 通用场景               | 陪伴女声   | 美式英文  | 16k       |
| Donna   | sambert-donna-v1       | 是     | 通用场景               | 教育女声   | 美式英文  | 16k       |
| Brian   | sambert-brian-v1       | 是     | 通用场景               | 客服男声   | 美式英文  | 16k       |
| Waan    | sambert-waan-v1        | 否     | 通用场景               | 泰语女声   | 泰语    | 16k       |
