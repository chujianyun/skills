> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 非实时语音合成 Qwen-Audio-TTS/CosyVoice Java SDK

> Qwen-Audio-TTS/CosyVoice 非实时语音合成 Java SDK 参考，支持非流式和流式两种调用模式。

本文介绍非实时语音合成 Qwen-Audio-TTS/CosyVoice 的 Java SDK 调用方法，支持非流式和流式两种调用模式。

**用户指南**：参见[非实时语音合成](/developer-guides/speech/tts)。

<Warning>
  该功能仅支持非实时调用，不支持 WebSocket 实时流式调用。如需实时合成，请使用 [CosyVoice WebSocket API](/api-reference/speech-synthesis/cosyvoice/websocket-api)。
</Warning>

## 前提条件

- 已[获取 API Key](/api-reference/preparation/api-key) 并将其[配置到环境变量](/api-reference/preparation/export-api-key-env)
- 已安装 DashScope Java SDK，建议[安装最新版](/api-reference/preparation/install-sdk)，SDK 版本需 ≥ 2.22.15

## HttpSpeechSynthesizer 类

**包路径**：`com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesizer`

**功能**：基于 HTTP 的语音合成，支持非流式和流式两种调用方式。

### 构造方法

```java
public HttpSpeechSynthesizer()
```

创建 HttpSpeechSynthesizer 实例，使用默认配置。SDK 会自动从环境变量 `DASHSCOPE_API_KEY` 或 `Constants.apiKey` 获取 API Key。

### callAndReturnAudio() - 非流式调用（返回音频数据）

**方法签名**：

```java
public ByteBuffer callAndReturnAudio(HttpSpeechSynthesisParam param)
    throws ApiException, NoApiKeyException, InputRequiredException
```

**参数说明**：

| 参数    | 类型                                                      | 说明                      |
| ----- | ------------------------------------------------------- | ----------------------- |
| param | [HttpSpeechSynthesisParam](#httpspeechsynthesisparam-类) | 语音合成参数对象，包含模型、文本、音色等配置。 |

**返回值**：`ByteBuffer`，包含完整的音频数据。可通过 `remaining()` 获取音频大小（字节）。

### call() - 非流式调用（返回音频 URL）

**方法签名**：

```java
public HttpSpeechSynthesisResult call(HttpSpeechSynthesisParam param)
    throws ApiException, NoApiKeyException, InputRequiredException
```

**参数说明**：

| 参数    | 类型                                                      | 说明        |
| ----- | ------------------------------------------------------- | --------- |
| param | [HttpSpeechSynthesisParam](#httpspeechsynthesisparam-类) | 语音合成参数对象。 |

**返回值**：`HttpSpeechSynthesisResult` 对象，通过 `getAudioInfo().getUrl()` 获取音频下载 URL，URL 有效期有限，可通过 `getAudioInfo().getExpiresAt()` 获取过期时间。

### streamCall() - 流式调用

**方法签名**：

```java
public void streamCall(HttpSpeechSynthesisParam param,
    ResultCallback<HttpSpeechSynthesisResult> callback)
    throws ApiException, NoApiKeyException, InputRequiredException
```

**参数说明**：

| 参数       | 类型                                                      | 说明                                                                 |
| -------- | ------------------------------------------------------- | ------------------------------------------------------------------ |
| param    | [HttpSpeechSynthesisParam](#httpspeechsynthesisparam-类) | 语音合成参数对象。                                                          |
| callback | ResultCallback\<HttpSpeechSynthesisResult>              | 回调对象，需实现 `onEvent`（接收音频分片）、`onComplete`（合成完成）、`onError`（错误处理）三个方法。 |

该方法为异步调用，音频数据通过回调函数分片返回，适用于对首包延迟有要求的场景。

**ResultCallback 回调方法**：

`com.alibaba.dashscope.common.ResultCallback` 是 DashScope SDK 提供的通用回调接口，需实现以下三个方法：

| 方法         | 参数                               | 说明                                                                                         |
| ---------- | -------------------------------- | ------------------------------------------------------------------------------------------ |
| onEvent    | HttpSpeechSynthesisResult result | 每接收到一个音频分片时触发。通过 `result.hasAudioData()` 判断是否包含音频数据，通过 `result.getAudioDataSize()` 获取分片大小。 |
| onComplete | 无                                | 语音合成完成时触发，表示所有音频分片已接收完毕。                                                                   |
| onError    | Exception e                      | 合成过程中发生错误时触发，可通过 `e.getMessage()` 获取错误信息。                                                  |

## HttpSpeechSynthesisParam 类

**包路径**：`com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisParam`

通过 Builder 模式构建参数对象。

<Note>
  部分参数没有专用的 Builder 方法，需要通过继承自父类的 `parameter(String key, Object value)` 方法或 `parameters(Map<String, Object>)` 方法进行设置，详见下表中的说明。
</Note>

**参数说明**：

| 方法                       | 类型      | 必填 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ------------------------ | ------- | -- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| model(String)            | String  | 是  | 语音合成模型。可选值：`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`、`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-plus`、`cosyvoice-v3-flash`、`cosyvoice-v2`                                                                                                                                                                                                                                                                 |
| text(String)             | String  | 是  | 待合成文本。支持 [SSML](/developer-guides/speech/ssml) 和 [LaTeX](/developer-guides/speech/ssml#latex-公式转语音) 格式输入。使用 SSML 时需设置 `enable_ssml=true`；使用 LaTeX 时无需额外配置                                                                                                                                                                                                                                                                            |
| voice(String)            | String  | 是  | 音色。可选值：系统音色（参见[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)）、声音复刻音色、声音设计音色（创建方法参见 [CosyVoice 声音复刻/设计 API](/api-reference/speech-synthesis/voice-cloning/create-voice)）                                                                                                                                                       |
| format(String)           | String  | 否  | 音频编码格式。默认值：`mp3`。可选值：`mp3`、`pcm`、`wav`、`opus`                                                                                                                                                                                                                                                                                                                                                                                        |
| sampleRate(int)          | int     | 否  | 音频采样率（Hz）。可选值：8000、16000、22050（默认）、24000、44100、48000                                                                                                                                                                                                                                                                                                                                                                                 |
| volume(int)              | int     | 否  | 音量。默认值：`50`。取值范围：\[0, 100]                                                                                                                                                                                                                                                                                                                                                                                                           |
| rate(float)              | float   | 否  | 语速。默认值：`1.0`。取值范围：\[0.5, 2.0]                                                                                                                                                                                                                                                                                                                                                                                                        |
| pitch(float)             | float   | 否  | 音调。默认值：`1.0`。取值范围：\[0.5, 2.0]                                                                                                                                                                                                                                                                                                                                                                                                        |
| enable\_ssml             | boolean | 否  | 是否开启 SSML 功能。当 `text` 使用 SSML 格式时需设为 `true`。默认为 `false`。仅 CosyVoice 系列模型支持，qwen-audio-3.0-tts-plus 和 qwen-audio-3.0-tts-flash 不支持。需通过 `.parameter("enable_ssml", true)` 设置                                                                                                                                                                                                                                                           |
| word\_timestamp\_enabled | boolean | 否  | 是否开启字级别时间戳。默认值：`false`。仅在流式输出模式下可用。支持的音色范围：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-flash、cosyvoice-v3-plus和cosyvoice-v2模型的复刻音色，以及[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标记为支持的系统音色。qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash及其他模型的复刻音色不支持此功能。需通过 `.parameter("word_timestamp_enabled", true)` 设置 |
| seed                     | int     | 否  | 随机数种子，用于复现相同合成结果。默认值：`0`。取值范围：\[0, 65535]。需通过 `.parameter("seed", 1234)` 设置                                                                                                                                                                                                                                                                                                                                                          |
| language\_hints          | List    | 否  | 指定语音合成的目标语言，提升合成效果。可选值：`zh`、`en`、`fr`、`de`、`ja`、`ko`、`ru`、`pt`、`th`、`id`、`vi`、`es`、`it`、`ms`、`fil`、`ar`。当前版本仅处理第一个元素，建议只传入一个值。需通过 `.parameter("language_hints", Arrays.asList("zh"))` 设置                                                                                                                                                                                                                                             |
| instruction              | String  | 否  | 设置指令，用于控制方言、情感或角色等合成效果。具体用法请参见[非实时语音合成](/developer-guides/speech/tts)。需通过 `.parameter("instruction", "...")` 设置                                                                                                                                                                                                                                                                                                                      |
| bit\_rate                | int     | 否  | 音频码率（kbps）。默认值：`32`。取值范围：\[6, 510]。仅在 `format` 为 `opus` 时支持。需通过 `.parameter("bit_rate", 32)` 设置                                                                                                                                                                                                                                                                                                                                      |
| enable\_aigc\_tag        | boolean | 否  | 是否在生成的音频中添加 AIGC 隐性标识。默认值：`false`。仅 qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v3-flash、cosyvoice-v3-plus、cosyvoice-v2 支持。需通过 `.parameter("enable_aigc_tag", true)` 设置                                                                                                                                                                                                                                               |
| aigc\_propagator         | String  | 否  | 设置 AIGC 隐性标识中的 `ContentPropagator` 字段。仅在 `enable_aigc_tag` 为 `true` 时生效。默认值：阿里云 UID。需通过 `.parameter("aigc_propagator", "xxxx")` 设置                                                                                                                                                                                                                                                                                                   |
| aigc\_propagate\_id      | String  | 否  | 设置 AIGC 隐性标识中的 `PropagateID` 字段。仅在 `enable_aigc_tag` 为 `true` 时生效。默认值：本次请求的 Request ID。需通过 `.parameter("aigc_propagate_id", "xxxx")` 设置                                                                                                                                                                                                                                                                                              |
| hot\_fix                 | Map     | 否  | 文本热修复配置，用于自定义指定词语的发音或文本替换。qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash、cosyvoice-v2 不支持。详见 [HTTP API hot\_fix 参数](/api-reference/speech-synthesis/cosyvoice/websocket-api#hot_fix)。需通过 `.parameter("hot_fix", hotFixMap)` 设置                                                                                                                                                                                                     |
| enable\_markdown\_filter | boolean | 否  | 是否启用 Markdown 过滤。启用后系统自动过滤 Markdown 标记符号。默认值：`false`。仅 cosyvoice-v3-flash 复刻音色支持。需通过 `.parameter("enable_markdown_filter", true)` 设置                                                                                                                                                                                                                                                                                                 |

## 示例代码

以下示例展示 Qwen-Audio-TTS/CosyVoice 语音合成的非流式和流式调用方式。运行前请确保已设置环境变量 `DASHSCOPE_API_KEY`。

<Warning>
  不同模型版本需使用对应版本的音色。例如 `qwen-audio-3.0-tts-flash` 和 `qwen-audio-3.0-tts-plus` 使用 `longanlingxi` 等音色，`cosyvoice-v3-flash` 和 `cosyvoice-v3-plus` 使用 `longanyang` 等音色，`cosyvoice-v2` 使用 `longxiaochun_v2` 等音色。更换模型时请同步更换为对应版本的音色。具体的模型与音色对应关系，请参见[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。
</Warning>

### 非流式调用

非流式调用会等待服务端合成完成后一次性返回结果。根据返回类型的不同，提供以下两种方式：

- `callAndReturnAudio()`：返回音频二进制数据（ByteBuffer），适用于直接保存或处理音频的场景。
- `call()`：返回音频 URL，适用于需要通过 URL 下载音频的场景。

```java
import com.alibaba.dashscope.audio.http_tts.AudioInfo;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisParam;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisResult;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesizer;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

public class CosyVoiceSyncExample {
  /**
   * 非流式调用示例一：返回音频数据（ByteBuffer）
   */
  public static void syncCallReturnAudio() {
    HttpSpeechSynthesizer synthesizer = new HttpSpeechSynthesizer();
    HttpSpeechSynthesisParam param =
        HttpSpeechSynthesisParam.builder()
            .model("qwen-audio-3.0-tts-flash")
            .text("我家的后面有一个很大的花园。")
            .voice("longanhuan_v3.6")
            .format("wav")
            .sampleRate(24000)
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .build();
    try {
      ByteBuffer audioData = synthesizer.callAndReturnAudio(param);
      if (audioData != null && audioData.hasRemaining()) {
        byte[] bytes = new byte[audioData.remaining()];
        audioData.get(bytes);
        try (FileOutputStream fos = new FileOutputStream("sync_output.wav")) {
          fos.write(bytes);
          System.out.println("Audio saved to sync_output.wav, size: "
              + bytes.length + " bytes");
        } catch (IOException e) {
          System.err.println("Failed to save audio: " + e.getMessage());
        }
      }
    } catch (ApiException | NoApiKeyException | InputRequiredException e) {
      System.err.println("Synthesis failed: " + e.getMessage());
    }
    System.exit(0);
  }

  /**
   * 非流式调用示例二：返回音频URL
   */
  public static void syncCallReturnUrl() {
    HttpSpeechSynthesizer synthesizer = new HttpSpeechSynthesizer();
    HttpSpeechSynthesisParam param =
        HttpSpeechSynthesisParam.builder()
            .model("qwen-audio-3.0-tts-flash")
            .text("我家的后面有一个很大的花园。")
            .voice("longanhuan_v3.6")
            .format("wav")
            .sampleRate(24000)
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .build();
    try {
      HttpSpeechSynthesisResult result = synthesizer.call(param);
      System.out.println("Request ID: " + result.getRequestId());
      if (result.hasAudioUrl()) {
        AudioInfo audioInfo = result.getAudioInfo();
        System.out.println("Audio URL: " + audioInfo.getUrl());
        System.out.println("Expires At: " + audioInfo.getExpiresAt());
        System.out.println("Remaining Time: "
            + audioInfo.getRemainingSeconds() + " seconds");
      }
    } catch (ApiException | NoApiKeyException | InputRequiredException e) {
      System.err.println("Synthesis failed: " + e.getMessage());
    }
  }

  public static void main(String[] args) {
    syncCallReturnUrl();
  }
}
```

### 流式调用

流式调用通过回调函数分片返回音频数据，无需等待合成完成即可开始处理，适用于对首包延迟有要求的实时播放场景。

```java
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisParam;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesisResult;
import com.alibaba.dashscope.audio.http_tts.HttpSpeechSynthesizer;
import com.alibaba.dashscope.common.ResultCallback;
import com.alibaba.dashscope.exception.ApiException;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.util.concurrent.CountDownLatch;

public class CosyVoiceStreamExample {
  public static void streamCallWithCallback() {
    HttpSpeechSynthesizer synthesizer = new HttpSpeechSynthesizer();
    HttpSpeechSynthesisParam param =
        HttpSpeechSynthesisParam.builder()
            .model("qwen-audio-3.0-tts-flash")
            .text("今天天气真好，适合出去玩。")
            .voice("longanhuan_v3.6")
            .format("wav")
            .sampleRate(24000)
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .build();
    CountDownLatch latch = new CountDownLatch(1);
    try (FileOutputStream fos = new FileOutputStream("output.wav")) {
      synthesizer.streamCall(param,
          new ResultCallback<HttpSpeechSynthesisResult>() {
            private int chunkCount = 0;

            @Override
            public void onEvent(HttpSpeechSynthesisResult result) {
              chunkCount++;
              if (result.hasAudioData()) {
                System.out.println("Received chunk #" + chunkCount
                    + ", size: " + result.getAudioDataSize() + " bytes");
                try {
                  fos.write(result.getAudioData());
                } catch (IOException e) {
                  System.err.println("Failed to write audio data: "
                      + e.getMessage());
                }
              }
              if (result.getRequestId() != null) {
                System.out.println("Request ID: " + result.getRequestId());
              }
            }

            @Override
            public void onComplete() {
              System.out.println("Synthesis completed, total chunks: "
                  + chunkCount);
              System.out.println("Audio saved to output.wav");
              latch.countDown();
            }

            @Override
            public void onError(Exception e) {
              System.err.println("Error during synthesis: " + e.getMessage());
              latch.countDown();
            }
          });
      latch.await();
    } catch (ApiException | NoApiKeyException
        | InputRequiredException | InterruptedException e) {
      System.err.println("Failed: " + e.getMessage());
    } catch (IOException e) {
      System.err.println("Failed to create output file: " + e.getMessage());
    }
  }

  public static void main(String[] args) {
    streamCallWithCallback();
    System.exit(0);
  }
}
```
