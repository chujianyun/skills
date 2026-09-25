> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Paraformer 录音文件识别 iOS SDK

> 使用 iOS SDK（NuiSDK）接入 Paraformer 录音文件识别服务，支持同步和异步两种模式批量提交音频 URL 进行转写，获取识别结果。

## 前提条件

- 获取 API Key：在使用前，您需要[获取 API Key](/api-reference/preparation/api-key)并配置。如需使用临时 Token，请参考[临时 Token](/api-reference/more/generate-a-temporary-api-key)。
- 下载 SDK：前往官方渠道下载最新 SDK 整合包，将 NuiSDK 框架集成到您的 Xcode 项目中。

## 快速开始

### 调用步骤

<Tabs>
  <Tab title="同步模式">
    同步模式下，调用 `nui_file_trans_start` 后阻塞等待，直到识别结果通过 `onFileTransEventCallback` 回调返回。

    **步骤一：初始化 SDK**

    调用 `nui_initialize` 初始化 SDK，传入连接与控制参数：

    ```objectivec
    NeoNui *neoNui = [NeoNui instance];
    neoNui.delegate = self;

    const char *initParams = "{\"url\":\"wss://dashscope.aliyuncs.com/api-ws/v1/inference\","
                             "\"apikey\":\"st-****\","
                             "\"device_id\":\"my_device_id\","
                             "\"service_mode\":\"1\"}";

    NuiResultCode code = [neoNui nui_initialize:initParams
                                      logLevel:LOG_LEVEL_VERBOSE
                                       saveLog:NO];
    if (code != kNuiResultCode_OK) {
      NSLog(@"初始化失败: %d", code);
    }
    ```

    **步骤二：设置语音识别参数**

    调用 `nui_set_params` 设置识别参数：

    ```objectivec
    const char *asrParams = "{\"nls_config\":{"
                            "\"model\":\"paraformer-v2\","
                            "\"disfluency_removal_enabled\":false,"
                            "\"timestamp_alignment_enabled\":false}}";

    NuiResultCode code = [neoNui nui_set_params:asrParams];
    ```

    **步骤三：提交识别任务**

    调用 `nui_file_trans_start` 提交音频 URL 列表，同步等待结果：

    ```objectivec
    char taskId[64] = {0};
    const char *taskParams = "{\"file_urls\":["
        "\"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav\","
        "\"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav\"],"
        "\"async_request\":false,"
        "\"nls_config\":{"
        "\"model\":\"paraformer-v2\","
        "\"disfluency_removal_enabled\":false,"
        "\"timestamp_alignment_enabled\":false}}";

    NuiResultCode code = [neoNui nui_file_trans_start:taskParams task_id:taskId];
    NSLog(@"任务ID: %s", taskId);
    ```

    **步骤四：处理识别结果**

    实现 `NeoNuiSdkDelegate` 协议，在回调中处理结果：

    ```objectivec
    - (void)onFileTransEventCallback:(NuiCallbackEvent)nuiEvent
                           asrResult:(const char *)asr_result
                              taskId:(const char *)task_id
                            ifFinish:(BOOL)finish
                             retCode:(int)code {
      if (nuiEvent == EVENT_FILE_TRANS_RESULT && finish) {
        NSString *result = [NSString stringWithUTF8String:asr_result];
        NSLog(@"识别结果: %@", result);
      } else if (nuiEvent == EVENT_ASR_ERROR) {
        NSLog(@"识别错误，错误码: %d", code);
      }
    }
    ```

    **步骤五：释放 SDK 资源**

    识别完成后，调用 `nui_release` 释放资源：

    ```objectivec
    [neoNui nui_release];
    ```
  </Tab>

  <Tab title="异步模式">
    异步模式下，调用 `nui_file_trans_start` 提交任务后立即返回，通过轮询 `nui_file_trans_query` 获取结果。

    **步骤一：初始化 SDK**

    调用 `nui_initialize` 初始化 SDK，传入连接与控制参数：

    ```objectivec
    NeoNui *neoNui = [NeoNui instance];
    neoNui.delegate = self;

    const char *initParams = "{\"url\":\"wss://dashscope.aliyuncs.com/api-ws/v1/inference\","
                             "\"apikey\":\"st-****\","
                             "\"device_id\":\"my_device_id\","
                             "\"service_mode\":\"1\"}";

    NuiResultCode code = [neoNui nui_initialize:initParams
                                      logLevel:LOG_LEVEL_VERBOSE
                                       saveLog:NO];
    if (code != kNuiResultCode_OK) {
      NSLog(@"初始化失败: %d", code);
    }
    ```

    **步骤二：设置语音识别参数**

    调用 `nui_set_params` 设置识别参数：

    ```objectivec
    const char *asrParams = "{\"nls_config\":{"
                            "\"model\":\"paraformer-v2\","
                            "\"disfluency_removal_enabled\":false,"
                            "\"timestamp_alignment_enabled\":false}}";

    NuiResultCode code = [neoNui nui_set_params:asrParams];
    ```

    **步骤三：提交识别任务（异步）**

    调用 `nui_file_trans_start` 提交任务，`async_request` 设为 `true`，任务立即返回：

    ```objectivec
    char taskId[64] = {0};
    const char *taskParams = "{\"file_urls\":["
        "\"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav\","
        "\"https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav\"],"
        "\"async_request\":true,"
        "\"nls_config\":{"
        "\"model\":\"paraformer-v2\","
        "\"disfluency_removal_enabled\":false,"
        "\"timestamp_alignment_enabled\":false}}";

    NuiResultCode code = [neoNui nui_file_trans_start:taskParams task_id:taskId];
    NSLog(@"任务已提交，任务ID: %s", taskId);
    ```

    **步骤四：轮询查询结果**

    定期调用 `nui_file_trans_query` 查询任务进度，结果通过回调返回：

    ```objectivec
    // 定时轮询，建议间隔3秒
    dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 3 * NSEC_PER_SEC),
                   dispatch_get_main_queue(), ^{
      [neoNui nui_file_trans_query:taskId];
    });
    ```

    **步骤五：处理识别结果**

    实现 `NeoNuiSdkDelegate` 协议，在回调中处理结果：

    ```objectivec
    - (void)onFileTransEventCallback:(NuiCallbackEvent)nuiEvent
                           asrResult:(const char *)asr_result
                              taskId:(const char *)task_id
                            ifFinish:(BOOL)finish
                             retCode:(int)code {
      if (nuiEvent == EVENT_FILE_TRANS_QUERY_RESULT) {
        if (finish) {
          NSString *result = [NSString stringWithUTF8String:asr_result];
          NSLog(@"识别完成: %@", result);
        } else {
          NSLog(@"任务进行中，继续轮询...");
          // 继续轮询
          dispatch_after(dispatch_time(DISPATCH_TIME_NOW, 3 * NSEC_PER_SEC),
                         dispatch_get_main_queue(), ^{
            [neoNui nui_file_trans_query:task_id];
          });
        }
      } else if (nuiEvent == EVENT_ASR_ERROR) {
        NSLog(@"识别错误，错误码: %d", code);
      }
    }
    ```

    **步骤六：取消任务（可选）**

    如需取消尚未完成的任务，调用 `nui_file_trans_cancel`：

    ```objectivec
    [neoNui nui_file_trans_cancel:taskId];
    ```

    **步骤七：释放 SDK 资源**

    任务处理完毕后，调用 `nui_release` 释放资源：

    ```objectivec
    [neoNui nui_release];
    ```
  </Tab>
</Tabs>

## 请求参数

### 连接与控制参数

初始化时通过 `nui_initialize` 传入，JSON 格式示例：

```json
{
    "url": "wss://dashscope.aliyuncs.com/api-ws/v1/inference",
    "apikey": "st-****",
    "device_id": "my_device_id",
    "service_mode": "1"
}
```

| 参数                   | 类型     | 是否必须 | 说明                                                          |
| -------------------- | ------ | ---- | ----------------------------------------------------------- |
| url                  | String | 是    | 服务地址，固定为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference` |
| apikey               | String | 是    | API Key，建议使用临时 API Key                                      |
| service\_mode        | String | 是    | 运行模式，录音文件识别固定为 `"1"`                                        |
| device\_id           | String | 是    | 终端用户唯一标识符，用于日志追踪                                            |
| debug\_path          | String | 否    | 日志文件存储路径，`save_log=YES` 时必须设置                               |
| max\_log\_file\_size | int    | 否    | 日志文件最大字节数，默认 104857600（100 MiB）                             |
| log\_track\_level    | int    | 否    | 日志回调过滤级别，默认 2（INFO），取值范围 0–5                                |

### 语音识别效果参数

通过 `nui_set_params` 或 `nui_file_trans_start` 传入，JSON 格式示例：

```json
{
    "file_urls": [
        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav",
        "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_male2.wav"
    ],
    "async_request": false,
    "nls_config": {
        "model": "paraformer-v2",
        "disfluency_removal_enabled": false,
        "timestamp_alignment_enabled": false
    }
}
```

| 参数                                        | 类型              | 是否必须 | 说明                                                                                             |
| ----------------------------------------- | --------------- | ---- | ---------------------------------------------------------------------------------------------- |
| file\_urls                                | array\[string]  | 是    | 音视频文件转写 URL 列表，支持 HTTP/HTTPS，单次最多 100 个                                                        |
| async\_request                            | boolean         | 否    | 是否异步请求，默认 `false`                                                                              |
| apikey                                    | string          | 否    | 临时 API Key，用于更新认证信息                                                                            |
| nls\_config                               | object          | 是    | 语音识别核心配置对象                                                                                     |
| nls\_config.model                         | string          | 是    | 语音识别模型，参考[模型列表](/developer-guides/speech/speech-to-text-models)                                |
| nls\_config.language\_hints               | array\[string]  | 否    | 语言代码，仅 paraformer-v2 支持，默认 `["zh","en"]`                                                       |
| nls\_config.disfluency\_removal\_enabled  | boolean         | 否    | 是否过滤语气词，默认 `false`                                                                             |
| nls\_config.timestamp\_alignment\_enabled | boolean         | 否    | 是否启用时间戳校准，默认 `false`                                                                           |
| nls\_config.special\_word\_filter         | object          | 否    | 敏感词处理配置，详见下方说明                                                                                 |
| nls\_config.channel\_id                   | array\[integer] | 否    | 多音轨索引，默认 `[0]`                                                                                 |
| nls\_config.diarization\_enabled          | boolean         | 否    | 说话人分离，默认关闭。启用后识别结果中将显示 `speaker_id` 字段，用于区分不同说话人。仅适用于单声道音频。                                    |
| nls\_config.speaker\_count                | integer         | 否    | 说话人数量参考值，需 `diarization_enabled=true`，取值范围 \[2, 100]                                           |
| nls\_config.vocabulary\_id                | string          | 否    | 热词列表 ID，适用 paraformer-v2 及以上模型，参考[定制热词](/developer-guides/speech/improve-recognition-accuracy) |
| nls\_config.resources                     | array\[object]  | 否    | 热词资源配置，适用 paraformer-v1 模型，参考[定制热词](/developer-guides/speech/improve-recognition-accuracy)     |

**敏感词处理（special\_word\_filter）示例**：

```json
{
  "filter_with_signed": {
    "word_list": ["测试"]
  },
  "filter_with_empty": {
    "word_list": ["开始", "发生"]
  },
  "system_reserved_filter": true
}
```

**热词资源（nls\_config.resources）示例（适用v1模型）**：

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

NeoNui 是 iOS SDK 的核心类，提供录音文件识别的全部功能接口。

#### nui\_initialize

初始化 SDK，在调用其他接口前必须先调用此方法。

```objectivec
-(NuiResultCode) nui_initialize:(const char *)parameters
                       logLevel:(NuiSdkLogLevel)level
                        saveLog:(BOOL)save_log;
```

| 参数         | 类型             | 说明                                                |
| ---------- | -------------- | ------------------------------------------------- |
| parameters | const char \*  | 初始化参数 JSON 字符串，包含连接与控制参数                          |
| level      | NuiSdkLogLevel | 日志级别                                              |
| save\_log  | BOOL           | 是否将日志写入文件，`YES` 时需在 `parameters` 中设置 `debug_path` |

#### nui\_set\_params

设置语音识别效果参数，在 `nui_initialize` 后、`nui_file_trans_start` 前调用。

```objectivec
-(NuiResultCode) nui_set_params:(const char *)params;
```

| 参数     | 类型            | 说明                                  |
| ------ | ------------- | ----------------------------------- |
| params | const char \* | 语音识别参数 JSON 字符串，包含 `nls_config` 等配置 |

#### nui\_file\_trans\_start

提交录音文件识别任务。同步模式（`async_request=false`）下阻塞等待；异步模式（`async_request=true`）下立即返回任务 ID。

```objectivec
-(NuiResultCode) nui_file_trans_start:(const char *)params task_id:(char *)task_id;
```

| 参数       | 类型            | 说明                                                          |
| -------- | ------------- | ----------------------------------------------------------- |
| params   | const char \* | 任务参数 JSON 字符串，包含 `file_urls`、`async_request`、`nls_config` 等 |
| task\_id | char \*       | 输出参数，任务提交成功后返回任务 ID                                         |

#### nui\_file\_trans\_query

查询异步任务的识别进度和结果，结果通过 `onFileTransEventCallback` 回调返回。

```objectivec
-(NuiResultCode) nui_file_trans_query:(const char *)task_id;
```

| 参数       | 类型            | 说明                                |
| -------- | ------------- | --------------------------------- |
| task\_id | const char \* | 由 `nui_file_trans_start` 返回的任务 ID |

#### nui\_file\_trans\_cancel

取消尚未完成的异步识别任务。

```objectivec
-(NuiResultCode) nui_file_trans_cancel:(const char *)task_id;
```

| 参数       | 类型            | 说明         |
| -------- | ------------- | ---------- |
| task\_id | const char \* | 需要取消的任务 ID |

#### nui\_release

释放 SDK 资源，调用后不可再使用 SDK，如需继续使用须重新调用 `nui_initialize`。

```objectivec
-(NuiResultCode) nui_release;
```

#### nui\_get\_version

获取当前 SDK 版本号。

```objectivec
-(const char*) nui_get_version;
```

### NeoNuiSdkDelegate

识别事件回调协议，实现此协议以接收识别结果和日志信息。

#### onFileTransEventCallback

识别事件主回调，在识别状态变化时触发。

```objectivec
-(void) onFileTransEventCallback:(NuiCallbackEvent)nuiEvent
                       asrResult:(const char *)asr_result
                          taskId:(const char *)task_id
                        ifFinish:(BOOL)finish
                         retCode:(int)code;
```

| 参数          | 类型               | 说明                                                       |
| ----------- | ---------------- | -------------------------------------------------------- |
| nuiEvent    | NuiCallbackEvent | 事件类型，参考 NuiCallbackEvent 枚举                              |
| asr\_result | const char \*    | 识别结果 JSON 字符串，参考[识别结果说明](/developer-guides/speech/asr)   |
| task\_id    | const char \*    | 当前任务 ID                                                  |
| finish      | BOOL             | 识别是否已完成                                                  |
| code        | int              | 错误码，参考[错误码查询](/api-reference/preparation/error-messages) |

#### onFileTransLogTrackCallback

日志回调，用于接收 SDK 内部日志信息，通过 `log_track_level` 参数过滤。

```objectivec
-(void) onFileTransLogTrackCallback:(NuiSdkLogLevel)level
                         logMessage:(const char *)log;
```

| 参数    | 类型             | 说明      |
| ----- | -------------- | ------- |
| level | NuiSdkLogLevel | 日志级别    |
| log   | const char \*  | 日志内容字符串 |

### NuiCallbackEvent

识别回调事件类型枚举。

| 枚举值                               | 说明           |
| --------------------------------- | ------------ |
| EVENT\_FILE\_TRANS\_CONNECTED     | 连接服务成功       |
| EVENT\_FILE\_TRANS\_UPLOADED      | 上传待识别音频文件成功  |
| EVENT\_FILE\_TRANS\_QUERY\_RESULT | 查询任务结果（异步模式） |
| EVENT\_FILE\_TRANS\_RESULT        | 识别最终结果（同步模式） |
| EVENT\_ASR\_ERROR                 | 语音识别过程中出现错误  |
