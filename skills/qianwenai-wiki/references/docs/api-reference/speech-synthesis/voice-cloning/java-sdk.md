> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Java SDK

> Qwen-Audio-TTS/CosyVoice 声音复刻 Java SDK 参考（VoiceEnrollmentService）。

通过 DashScope Java SDK 的 `VoiceEnrollmentService` 类调用 Qwen-Audio-TTS/CosyVoice 声音复刻。该 SDK 仅覆盖声音复刻功能，CosyVoice 声音设计以及所有 Qwen 声音复刻/设计请使用 [HTTP API](/api-reference/speech-synthesis/voice-cloning/create-voice)。

**用户指南**：[声音复刻](/developer-guides/speech/voice-cloning)。

## 前提条件

- [API Key](/api-reference/preparation/api-key)
- [最新版 DashScope SDK](/api-reference/preparation/install-sdk)

## Service URL

创建服务前设置 base URL：

```java
import com.alibaba.dashscope.common.Constants;

Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
```

## VoiceEnrollmentService 类

**包路径**：`com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService`

管理 Qwen-Audio-TTS/CosyVoice 克隆音色的完整生命周期（创建、列表、查询、更新、删除）。

### 构造方法

```java
public VoiceEnrollmentService(String apiKey)
```

| 参数     | 类型     | 说明                 |
| ------ | ------ | ------------------ |
| apiKey | String | DashScope API Key。 |

### createVoice()

从音频创建克隆音色。

```java
public Voice createVoice(String targetModel, String prefix, String url,
                         VoiceEnrollmentParam customParam)
    throws NoApiKeyException, InputRequiredException
```

| 参数          | 类型                   | 必选 | 说明                                                                                                                            |
| ----------- | -------------------- | -- | ----------------------------------------------------------------------------------------------------------------------------- |
| targetModel | String               | 是  | 克隆音色绑定的语音合成模型。后续合成调用的 model 必须与此一致。                                                                                           |
| prefix      | String               | 是  | 音色名称前缀，仅限字母和数字，最长 10 个字符。                                                                                                     |
| url         | String               | 是  | 用于克隆的音频文件 URL，必须可公开访问。                                                                                                        |
| customParam | VoiceEnrollmentParam | 否  | 自定义参数，可通过 `parameter()` 方法指定 `language_hints`、`max_prompt_audio_length` 等。详见 [VoiceEnrollmentParam](#voiceenrollmentparam-类)。 |

**返回值**：`Voice` 对象，调用 `getVoiceId()` 获取音色 ID。

<Expandable title="示例">
  ```java
  import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
  import com.alibaba.dashscope.audio.ttsv2.enrollment.Voice;
  import com.alibaba.dashscope.common.Constants;

  Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";

  String apiKey = System.getenv("DASHSCOPE_API_KEY");
  VoiceEnrollmentService service = new VoiceEnrollmentService(apiKey);

  Voice voice = service.createVoice(
    "qwen-audio-3.0-tts-flash",
    "myvoice",
    "https://your-audio-url.wav",
    null
  );

  System.out.println("Created voice: " + voice.getVoiceId());
  ```
</Expandable>

### listVoice()

列出克隆音色，支持前缀过滤和分页。

```java
public Voice[] listVoice(String prefix, int pageIndex, int pageSize)
    throws NoApiKeyException, InputRequiredException
```

| 参数        | 类型     | 必选 | 说明         |
| --------- | ------ | -- | ---------- |
| prefix    | String | 否  | 按名称前缀过滤。   |
| pageIndex | int    | 否  | 页码，从 0 开始。 |
| pageSize  | int    | 否  | 每页条数。      |

**返回值**：`Voice[]` 音色对象数组。

<Expandable title="示例">
  ```java
  Voice[] voices = service.listVoice("myvoice", 0, 10);

  for (Voice v : voices) {
    System.out.println("Voice: " + v.getVoiceId());
  }
  ```
</Expandable>

### queryVoice()

查询指定克隆音色的详细信息。

```java
public Voice queryVoice(String voiceId)
    throws NoApiKeyException, InputRequiredException
```

| 参数      | 类型     | 必选 | 说明         |
| ------- | ------ | -- | ---------- |
| voiceId | String | 是  | 要查询的音色 ID。 |

**返回值**：`Voice` 对象，包含状态、目标模型等信息。

<Expandable title="示例">
  ```java
  Voice details = service.queryVoice("qwen-audio-3.0-tts-flash-myvoice-xxxxxx");

  System.out.println("Status: " + details.getStatus());
  ```
</Expandable>

### updateVoice()

用新音频更新已有克隆音色。

```java
public void updateVoice(String voiceId, String url)
    throws NoApiKeyException, InputRequiredException
public void updateVoice(String voiceId, String url, VoiceEnrollmentParam customParam)
    throws NoApiKeyException, InputRequiredException
```

| 参数          | 类型                   | 必选 | 说明                  |
| ----------- | -------------------- | -- | ------------------- |
| voiceId     | String               | 是  | 要更新的音色 ID。          |
| url         | String               | 是  | 新的音频文件 URL，必须可公开访问。 |
| customParam | VoiceEnrollmentParam | 否  | 可选参数。               |

<Expandable title="示例">
  ```java
  service.updateVoice(
    "qwen-audio-3.0-tts-flash-myvoice-xxxxxx",
    "https://new-audio-url.wav",
    null
  );

  System.out.println("Voice updated successfully");
  ```
</Expandable>

### deleteVoice()

删除克隆音色。

```java
public void deleteVoice(String voiceId)
    throws NoApiKeyException, InputRequiredException
```

| 参数      | 类型     | 必选 | 说明         |
| ------- | ------ | -- | ---------- |
| voiceId | String | 是  | 要删除的音色 ID。 |

<Expandable title="示例">
  ```java
  service.deleteVoice("qwen-audio-3.0-tts-flash-myvoice-xxxxxx");

  System.out.println("Voice deleted successfully");
  ```
</Expandable>

## 完整示例

### 创建音色

```java
import com.alibaba.dashscope.audio.ttsv2.enrollment.Voice;
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentParam;
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
import com.alibaba.dashscope.common.Constants;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import java.util.Arrays;

public class Main {
  private static final Logger logger = LoggerFactory.getLogger(Main.class);

  public static void main(String[] args) {
    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    String apiKey = System.getenv("DASHSCOPE_API_KEY");
    String targetModel = "qwen-audio-3.0-tts-flash";
    String prefix = "myvoice";
    String fileUrl = "https://your-audio-file-url";
    String cloneModelName = "voice-enrollment";
    try {
      VoiceEnrollmentService service = new VoiceEnrollmentService(apiKey);
      Voice myVoice = service.createVoice(
        targetModel,
        prefix,
        fileUrl,
        VoiceEnrollmentParam.builder()
          .model(cloneModelName)
          .parameter("language_hints", Arrays.asList("zh"))
          // .parameter("max_prompt_audio_length", 10.0f)
          // .parameter("enable_preprocess", false)
          // .parameter("enable_volume_normalization", "false")
          .build());
      logger.info("Voice creation submitted. Request ID: {}", service.getLastRequestId());
      logger.info("Generated Voice ID: {}", myVoice.getVoiceId());
    } catch (Exception e) {
      logger.error("Failed to create voice", e);
    }
  }
}
```

### 列表查询

```java
import com.alibaba.dashscope.audio.ttsv2.enrollment.Voice;
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
import com.alibaba.dashscope.common.Constants;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.Gson;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
  public static String apiKey = System.getenv("DASHSCOPE_API_KEY");
  private static String prefix = "myvoice";
  private static final Logger logger = LoggerFactory.getLogger(Main.class);

  public static void main(String[] args)
      throws NoApiKeyException, InputRequiredException {
    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    VoiceEnrollmentService service = new VoiceEnrollmentService(apiKey);
    Voice[] voices = service.listVoice(prefix, 0, 10);
    logger.info("List successful. Request ID: {}", service.getLastRequestId());
    logger.info("Voices Details: {}", new Gson().toJson(voices));
  }
}
```

### 查询音色详情

```java
import com.alibaba.dashscope.audio.ttsv2.enrollment.Voice;
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
import com.alibaba.dashscope.common.Constants;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.google.gson.Gson;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
  public static String apiKey = System.getenv("DASHSCOPE_API_KEY");
  private static String voiceId = "qwen-audio-3.0-tts-flash-myvoice-xxx";
  private static final Logger logger = LoggerFactory.getLogger(Main.class);

  public static void main(String[] args)
      throws NoApiKeyException, InputRequiredException {
    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    VoiceEnrollmentService service = new VoiceEnrollmentService(apiKey);
    Voice voice = service.queryVoice(voiceId);
    logger.info("Query successful. Request ID: {}", service.getLastRequestId());
    logger.info("Voice Details: {}", new Gson().toJson(voice));
  }
}
```

### 更新音色

```java
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
import com.alibaba.dashscope.common.Constants;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
  public static String apiKey = System.getenv("DASHSCOPE_API_KEY");
  private static String fileUrl = "https://your-audio-file-url";
  private static String voiceId = "qwen-audio-3.0-tts-flash-myvoice-xxx";
  private static final Logger logger = LoggerFactory.getLogger(Main.class);

  public static void main(String[] args)
      throws NoApiKeyException, InputRequiredException {
    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    VoiceEnrollmentService service = new VoiceEnrollmentService(apiKey);
    service.updateVoice(voiceId, fileUrl);
    logger.info("Update submitted. Request ID: {}", service.getLastRequestId());
  }
}
```

### 删除音色

```java
import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentService;
import com.alibaba.dashscope.common.Constants;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
  public static String apiKey = System.getenv("DASHSCOPE_API_KEY");
  private static String voiceId = "qwen-audio-3.0-tts-flash-myvoice-xxx";
  private static final Logger logger = LoggerFactory.getLogger(Main.class);

  public static void main(String[] args)
      throws NoApiKeyException, InputRequiredException {
    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    VoiceEnrollmentService service = new VoiceEnrollmentService(apiKey);
    service.deleteVoice(voiceId);
    logger.info("Deletion submitted. Request ID: {}", service.getLastRequestId());
  }
}
```

## VoiceEnrollmentParam 类

**包路径**：`com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentParam`

使用 Builder 模式构造 `createVoice()` 和 `updateVoice()` 的可选参数。

| Builder 方法                | 类型     | 说明                                                                                                                                                                                                      |
| ------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model(String)             | String | 声音复刻模型，固定为 `voice-enrollment`。                                                                                                                                                                          |
| parameter(String, Object) | Object | 设置自定义参数，如 `parameter("language_hints", Arrays.asList("zh"))`、`parameter("max_prompt_audio_length", 10.0f)`、`parameter("enable_preprocess", false)`、`parameter("enable_volume_normalization", "false")`。 |

### enable\_preprocess

| 参数                 | 类型      | 必选 | 说明                                                     |
| ------------------ | ------- | -- | ------------------------------------------------------ |
| enable\_preprocess | boolean | 否  | 是否启用音频预处理（降噪、增强、音量归一化）。有噪音的音频建议开启，干净音频建议关闭。默认：`false`。 |

### enable\_volume\_normalization

| 参数                            | 类型     | 必选 | 说明                                                                                                |
| ----------------------------- | ------ | -- | ------------------------------------------------------------------------------------------------- |
| enable\_volume\_normalization | String | 否  | 是否对用于声音复刻的样本音频进行音量归一化。取值为 `"true"` 或 `"false"`。开启后，使用所创建音色合成的音频，其音量可能与关闭该参数时创建的音色不同。默认：`"false"`。 |

<Expandable title="VoiceEnrollmentParam 示例">
  ```java
  import com.alibaba.dashscope.audio.ttsv2.enrollment.VoiceEnrollmentParam;
  import java.util.Arrays;

  VoiceEnrollmentParam param = VoiceEnrollmentParam.builder()
    .parameter("language_hints", Arrays.asList("zh"))
    // .parameter("max_prompt_audio_length", 10.0f)
    // .parameter("enable_preprocess", false)
    // .parameter("enable_volume_normalization", "false")
    .build();

  Voice voice = service.createVoice(
    "qwen-audio-3.0-tts-flash",
    "myvoice",
    "https://your-audio-url.wav",
    param
  );
  ```
</Expandable>
