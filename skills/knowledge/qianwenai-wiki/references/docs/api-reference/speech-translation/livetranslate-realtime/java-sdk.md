> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# LiveTranslate Java SDK

> LiveTranslate Java SDK 参考文档

**用户指南**： 教程和完整示例请参见[实时翻译](/developer-guides/speech/realtime-translation)。

## 前提条件

1. [安装SDK](/api-reference/preparation/install-sdk)，确保DashScope SDK版本不低于2.22.5。
2. [获取API Key](/api-reference/preparation/api-key)。

## 配置概览

三个 Builder 对象控制一个翻译会话：

```text
OmniRealtimeParam          --> 连接配置：模型、端点、API Key
  +-- OmniRealtimeConfig   --> 会话配置：音频格式、音色、输出模态
       +-- OmniRealtimeTranslationParam  --> 翻译配置：目标语言、自定义术语
```

将 `OmniRealtimeParam` 传入构造函数。连接成功后，调用 `updateSession()` 并传入 `OmniRealtimeConfig` 来设置音频和翻译选项。如果不调用 `updateSession()`，则使用默认值。

## 请求参数

### OmniRealtimeParam

使用 `OmniRealtimeParam.builder()` 构建连接参数。

<Accordion title="示例代码">
  ```java
  OmniRealtimeParam param = OmniRealtimeParam.builder()
    .model("qwen3.5-livetranslate-flash-realtime")
    .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
    // 如果未设置环境变量，请将下一行替换为您的 API Key：.apikey("YOUR_API_KEY")
    .apikey(System.getenv("DASHSCOPE_API_KEY"))
    .build();
  ```
</Accordion>

| 参数       | 类型       | 必选 | 说明                                                                                           |
| -------- | -------- | -- | -------------------------------------------------------------------------------------------- |
| `model`  | `String` | 是  | 模型名称。推荐使用 `qwen3.5-livetranslate-flash-realtime`。`qwen3-livetranslate-flash-realtime` 为旧版模型。 |
| `url`    | `String` | 是  | WebSocket 端点。使用 `wss://dashscope.aliyuncs.com/api-ws/v1/realtime`。                           |
| `apikey` | `String` | 否  | API key。默认读取 `DASHSCOPE_API_KEY` 环境变量。                                                       |

### OmniRealtimeConfig

使用 `OmniRealtimeConfig.builder()` 构建会话参数，然后调用 `conversation.updateSession(config)`。

<Accordion title="示例代码">
  ```java
  // 设置自定义翻译术语
  Map<String, Object> phrases = new HashMap<>();
  phrases.put("人工智能", "Artificial Intelligence");
  phrases.put("机器学习", "Machine Learning");

  OmniRealtimeConfig config = OmniRealtimeConfig.builder()
    .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
    .voice("Tina")
    .inputAudioFormat(OmniRealtimeAudioFormat.PCM_16000HZ_MONO_16BIT)
    .outputAudioFormat(OmniRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT)
    .InputAudioTranscription("qwen3-asr-flash-realtime")
    .translationConfig(OmniRealtimeTranslationParam.builder()
      .language("en")
      .corpus(OmniRealtimeTranslationParam.Corpus.builder()
        .phrases(phrases)
        .build())
      .build())
    .build();

  conversation.updateSession(config);
  ```
</Accordion>

| 参数                        | 类型                             | 必选 | 说明                                                                                                                                                                                                                         |
| ------------------------- | ------------------------------ | -- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `modalities`              | `List<OmniRealtimeModality>`   | 否  | 输出模态。默认值：`[AUDIO, TEXT]`。设置为 `[TEXT]` 则仅输出文本。                                                                                                                                                                              |
| `voice`                   | `String`                       | 否  | 合成语音的音色。Qwen3.5-LiveTranslate-Flash-Realtime 默认音色为 `Tina`，Qwen3-LiveTranslate-Flash-Realtime 默认音色为 `Cherry`。参见[支持的音色](/developer-guides/speech/realtime-translation#支持的音色)。                                                |
| `inputAudioFormat`        | `OmniRealtimeAudioFormat`      | 否  | 输入音频格式。默认值：`PCM_16000HZ_MONO_16BIT`。                                                                                                                                                                                       |
| `outputAudioFormat`       | `OmniRealtimeAudioFormat`      | 否  | 输出音频格式。默认值：`PCM_24000HZ_MONO_16BIT`。                                                                                                                                                                                       |
| `InputAudioTranscription` | `String`                       | 否  | 用于转录输入语音的 ASR 模型。设置为 `qwen3-asr-flash-realtime` 可在翻译的同时接收源语言转录结果。注意：此方法名首字母大写（`InputAudioTranscription`），调用时请严格按此拼写。                                                                                                       |
| `translationConfig`       | `OmniRealtimeTranslationParam` | 否  | 翻译配置。参见下方 OmniRealtimeTranslationParam。                                                                                                                                                                                    |
| `enableTurnDetection`     | `boolean`                      | 否  | 是否启用 VAD（语音活动检测）。默认值：`true`，启用 VAD 模式，服务端自动检测语音起止并自动触发翻译。设为 `false` 切换为 Manual 模式，由客户端通过 `commit()` 方法手动提交音频。详细参数说明见[客户端事件](/api-reference/speech-translation/livetranslate-realtime/client-events)中的 `turn_detection` 描述。 |

### OmniRealtimeTranslationParam

使用 `OmniRealtimeTranslationParam.builder()` 构建翻译参数。

<Accordion title="示例代码">
  ```java
  // 设置翻译术语
  Map<String, Object> phrases = new HashMap<>();
  phrases.put("Inteligencia Artificial", "Artificial Intelligence");  // 源语言词汇：目标语言译文
  phrases.put("Aprendizaje Automático", "Machine Learning");

  OmniRealtimeTranslationParam translationParam = OmniRealtimeTranslationParam.builder()
    .language("en")  // 目标语言代码
    .corpus(OmniRealtimeTranslationParam.Corpus.builder()
      .phrases(phrases)
      .build())
    .build();
  ```
</Accordion>

| 参数               | 类型                                    | 必选 | 说明                                                                              |
| ---------------- | ------------------------------------- | -- | ------------------------------------------------------------------------------- |
| `language`       | `String`                              | 否  | 目标语言代码。默认值：`en`。参见[支持的语种](/developer-guides/speech/realtime-translation#支持的语种)。 |
| `corpus`         | `OmniRealtimeTranslationParam.Corpus` | 否  | 热词配置，用于提升特定词汇的翻译准确性。                                                            |
| `corpus.phrases` | `Map<String, Object>`                 | 否  | 热词映射表。key 为源语言词汇，value 为目标语言对应翻译。示例：`{"人工智能": "Artificial Intelligence"}`       |

## 关键接口

### OmniRealtimeConversation

管理 WebSocket 连接和音频流。

**Import**：`com.alibaba.dashscope.audio.omni.OmniRealtimeConversation`

| 方法                                                                                 | 说明                                                                                                                                                                                                                                                           |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `OmniRealtimeConversation(OmniRealtimeParam param, OmniRealtimeCallback callback)` | 创建会话，传入连接参数和事件回调。                                                                                                                                                                                                                                            |
| `void connect()`                                                                   | 建立 WebSocket 连接。触发 [session.created](/api-reference/speech-translation/livetranslate-realtime/server-events) 和 [session.updated](/api-reference/speech-translation/livetranslate-realtime/server-events) 事件。可能抛出 `NoApiKeyException`、`InterruptedException`。 |
| `void updateSession(OmniRealtimeConfig config)`                                    | 更新会话配置。触发 [session.updated](/api-reference/speech-translation/livetranslate-realtime/server-events) 事件。未指定的参数使用默认值。                                                                                                                                          |
| `void appendAudio(String audioBase64)`                                             | 发送 Base64 编码的音频数据块。服务端自动检测语音边界并触发翻译。                                                                                                                                                                                                                         |
| `void commit()`                                                                    | Manual 模式下，提交此前通过 `appendAudio` 方法追加到云端缓冲区的音频，服务端收到后自动开始生成翻译响应。VAD 模式下无需调用此方法，服务端会自动提交。触发 [input\_audio\_buffer.committed](/api-reference/speech-translation/livetranslate-realtime/server-events) 事件。                                                       |
| `void clearAppendedAudio()`                                                        | 清空当前云端缓冲区中尚未提交的音频数据。触发 [input\_audio\_buffer.cleared](/api-reference/speech-translation/livetranslate-realtime/server-events) 事件。                                                                                                                            |
| `void endSession()`                                                                | 结束会话。服务端会完成进行中的翻译，然后发送 [session.finished](/api-reference/speech-translation/livetranslate-realtime/server-events) 事件。可能抛出 `InterruptedException`。                                                                                                            |
| `void close(int code, String reason)`                                              | 停止任务并关闭 WebSocket 连接。                                                                                                                                                                                                                                        |
| `String getSessionId()`                                                            | 返回会话 ID。                                                                                                                                                                                                                                                     |
| `String getResponseId()`                                                           | 返回最新服务端响应的响应 ID。                                                                                                                                                                                                                                             |
| `long getFirstTextDelay()`                                                         | 返回最新响应的首次文本延迟（毫秒）。                                                                                                                                                                                                                                           |
| `long getFirstAudioDelay()`                                                        | 返回最新响应的首次音频延迟（毫秒）。                                                                                                                                                                                                                                           |

### OmniRealtimeCallback

处理 WebSocket 上的服务端事件。继承此类并实现各方法。

**Import**：`com.alibaba.dashscope.audio.omni.OmniRealtimeCallback`

| 方法                                               | 参数                                                                                                    | 说明                                 |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------- | ---------------------------------- |
| `void onOpen()`                                  | 无                                                                                                     | WebSocket 连接建立时调用。                 |
| `abstract void onEvent(JsonObject message)`      | `message`：包含[服务端事件](/api-reference/speech-translation/livetranslate-realtime/server-events)的 JSON 对象。 | 每收到一个服务端事件时调用。解析 `type` 字段以识别事件类型。 |
| `abstract void onClose(int code, String reason)` | `code`：WebSocket 状态码。`reason`：关闭原因描述。                                                                 | WebSocket 关闭时调用。                   |

`onEvent` 中的常见事件类型：

| 事件类型                                                    | 说明                                                                        |
| ------------------------------------------------------- | ------------------------------------------------------------------------- |
| `input_audio_buffer.speech_started`                     | 检测到音频流中的语音。                                                               |
| `input_audio_buffer.speech_stopped`                     | 检测到语音片段结束。                                                                |
| `conversation.item.input_audio_transcription.completed` | 源语言转录就绪。通过 `message.get("transcript")` 读取。需要设置 `InputAudioTranscription`。 |
| `response.audio_transcript.done`                        | 翻译文本就绪。通过 `message.get("transcript")` 读取。                                 |
| `response.audio.delta`                                  | 翻译音频数据块可用。通过 `message.get("delta")` 读取 Base64 编码的音频。                      |
| `error`                                                 | 发生错误。通过 `message.get("error").getAsJsonObject().get("message")` 读取详情。     |

## 完整示例

以下示例展示如何从麦克风实时录音并进行翻译。

<Accordion title="麦克风实时翻译示例代码">
  ```java
  import com.alibaba.dashscope.audio.omni.*;
  import com.alibaba.dashscope.exception.NoApiKeyException;
  import com.google.gson.JsonObject;
  import javax.sound.sampled.*;
  import java.util.*;
  import java.util.concurrent.atomic.AtomicBoolean;

  public class Main {
    private static final int INPUT_CHUNK_SIZE = 3200;
    private static final int OUTPUT_CHUNK_SIZE = 4800;
    private static final AtomicBoolean running = new AtomicBoolean(true);
    private static SourceDataLine speaker;

    public static void main(String[] args) throws InterruptedException {
      String apiKey = System.getenv("DASHSCOPE_API_KEY");
      if (apiKey == null || apiKey.isEmpty()) {
        System.err.println("请设置环境变量 DASHSCOPE_API_KEY");
        System.exit(1);
      }

      OmniRealtimeParam param = OmniRealtimeParam.builder()
        .model("qwen3.5-livetranslate-flash-realtime")
        .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
        .apikey(apiKey)
        .build();

      OmniRealtimeCallback callback = new OmniRealtimeCallback() {
        @Override
        public void onOpen() {
          System.out.println("[连接已建立]");
        }

        @Override
        public void onEvent(JsonObject message) {
          String type = message.get("type").getAsString();
          switch (type) {
            case "input_audio_buffer.speech_started":
              System.out.println("====== 检测到语音输入 ======");
              break;
            case "input_audio_buffer.speech_stopped":
              System.out.println("====== 语音输入结束 ======");
              break;
            case "conversation.item.input_audio_transcription.completed":
              String originalText = message.get("transcript").getAsString();
              System.out.println("[原文] " + originalText);
              break;
            case "response.audio_transcript.done":
              String translatedText = message.get("transcript").getAsString();
              System.out.println("[翻译结果] " + translatedText);
              break;
            case "response.audio.delta":
              String audioB64 = message.get("delta").getAsString();
              byte[] audioBytes = Base64.getDecoder().decode(audioB64);
              if (speaker != null) {
                speaker.write(audioBytes, 0, audioBytes.length);
              }
              break;
            case "error":
              JsonObject error = message.get("error").getAsJsonObject();
              System.err.println("[错误] " + error.get("message").getAsString());
              break;
          }
        }

        @Override
        public void onClose(int code, String reason) {
          System.out.println("[连接已关闭] code: " + code + ", reason: " + reason);
        }
      };

      OmniRealtimeConversation conversation = new OmniRealtimeConversation(param, callback);

      try {
        AudioFormat speakerFormat = new AudioFormat(24000, 16, 1, true, false);
        DataLine.Info speakerInfo = new DataLine.Info(SourceDataLine.class, speakerFormat);
        speaker = (SourceDataLine) AudioSystem.getLine(speakerInfo);
        speaker.open(speakerFormat, OUTPUT_CHUNK_SIZE * 4);
        speaker.start();

        AudioFormat micFormat = new AudioFormat(16000, 16, 1, true, false);
        DataLine.Info micInfo = new DataLine.Info(TargetDataLine.class, micFormat);
        if (!AudioSystem.isLineSupported(micInfo)) {
          System.err.println("麦克风不可用");
          System.exit(1);
        }
        TargetDataLine microphone = (TargetDataLine) AudioSystem.getLine(micInfo);
        microphone.open(micFormat);
        microphone.start();

        conversation.connect();

        Map<String, Object> phrases = new HashMap<>();
        phrases.put("人工智能", "Artificial Intelligence");
        phrases.put("机器学习", "Machine Learning");

        OmniRealtimeConfig config = OmniRealtimeConfig.builder()
          .modalities(Arrays.asList(OmniRealtimeModality.AUDIO, OmniRealtimeModality.TEXT))
          .voice("Tina")
          .inputAudioFormat(OmniRealtimeAudioFormat.PCM_16000HZ_MONO_16BIT)
          .outputAudioFormat(OmniRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT)
          .InputAudioTranscription("qwen3-asr-flash-realtime")
          .translationConfig(OmniRealtimeTranslationParam.builder()
            .language("en")
            .corpus(OmniRealtimeTranslationParam.Corpus.builder()
              .phrases(phrases)
              .build())
            .build())
          .build();

        conversation.updateSession(config);

        Runtime.getRuntime().addShutdownHook(new Thread(() -> {
          System.out.println("\n[正在退出...]");
          running.set(false);
          microphone.stop();
          microphone.close();
          speaker.stop();
          speaker.close();
          try {
            conversation.endSession();
          } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
          }
          conversation.close(1000, "用户停止");
        }));

        System.out.println("[开始实时翻译] 请对着麦克风说话，按 Ctrl+C 退出");

        byte[] buffer = new byte[INPUT_CHUNK_SIZE];
        while (running.get()) {
          int bytesRead = microphone.read(buffer, 0, buffer.length);
          if (bytesRead > 0) {
            conversation.appendAudio(Base64.getEncoder().encodeToString(buffer));
          }
        }
      } catch (NoApiKeyException e) {
        System.err.println("API Key 错误: " + e.getMessage());
      } catch (Exception e) {
        System.err.println("发生异常: " + e.getMessage());
        e.printStackTrace();
      }
    }
  }
  ```
</Accordion>

## 相关参考

- [Qwen-LiveTranslate 模型概览](/developer-guides/speech/realtime-translation) -- 支持的语言、音色和功能
- [服务端事件参考](/api-reference/speech-translation/livetranslate-realtime/server-events) -- 事件类型、JSON Schema 和错误码
- [安装 DashScope SDK](/api-reference/preparation/install-sdk) -- 安装和依赖配置
- [获取 API Key](/api-reference/preparation/api-key) -- API Key 的创建和管理
