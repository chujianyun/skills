> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Paraformer 实时语音识别 Java SDK

> 使用Java SDK接入Paraformer实时语音识别服务，支持非流式调用、基于回调的双向流式调用和基于Flowable的双向流式调用。

## 前提条件

- 开通服务：实时语音识别服务需要单独开通，详见[实时语音识别概述](/developer-guides/speech/asr-realtime)。
- 获取API Key：在使用前，您需要[获取API Key](/api-reference/preparation/api-key)并配置环境变量 `DASHSCOPE_API_KEY`。如需使用临时Token，请参考[临时Token](/api-reference/more/generate-a-temporary-api-key)。
- 安装Java SDK：参考[安装SDK](/api-reference/preparation/install-sdk)完成Maven依赖配置。

## 模型列表

|         | paraformer-realtime-v2（推荐） | paraformer-realtime-8k-v2（推荐） | paraformer-realtime-v1 | paraformer-realtime-8k-v1 |
| ------- | -------------------------- | ----------------------------- | ---------------------- | ------------------------- |
| 适用场景    | 直播、会议                      | 电话客服/8kHz                     | 直播、会议                  | 电话客服/8kHz                 |
| 采样率     | 任意                         | 8kHz                          | 16kHz                  | 8kHz                      |
| 语种      | 中文+英/日/韩/德/法/俄             | 中文                            | 中文                     | 中文                        |
| 标点符号预测  | 默认支持                       | 默认支持                          | 默认支持                   | 默认支持                      |
| ITN     | 默认支持                       | 默认支持                          | 默认支持                   | 默认支持                      |
| 定制热词    | 支持（vocabularyId）           | 支持（vocabularyId）              | 支持（phraseId）           | 支持（phraseId）              |
| 指定待识别语种 | language\_hints            | 不支持                           | 不支持                    | 不支持                       |
| 情感识别    | 不支持                        | 支持（仅isSentenceEnd=true时）      | 不支持                    | 不支持                       |

## 快速开始

安装DashScope Java SDK后，设置环境变量：

```bash
export DASHSCOPE_API_KEY="REDACTED"
```

SDK内部通过 `RecognitionParam.builder()` 构建参数，通过 `Recognition` 类发起识别任务。根据使用场景选择调用方式：

- **非流式调用**：适用于本地音频文件，调用阻塞直到文件读取完毕。
- **双向流式调用（基于回调）**：适用于麦克风等实时音频流，通过 `ResultCallback` 异步接收结果。
- **双向流式调用（基于Flowable）**：响应式编程风格，适用于RxJava生态。

<Warning>
  无论使用哪种调用方式，任务结束后**必须**调用 `recognizer.getDuplexApi().close(1000, "bye")` 关闭WebSocket连接，否则连接将无法正常释放。
</Warning>

## 非流式调用

调用 `recognizer.call(param, File)` 方法会阻塞线程，直到音频文件读取完毕并返回完整识别结果字符串。

```java
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import java.io.File;

public class Main {
  public static void main(String[] args) {
    Recognition recognizer = new Recognition();
    RecognitionParam param =
        RecognitionParam.builder()
            // .apiKey("yourApikey")
            .model("paraformer-realtime-v2")
            .format("wav")
            .sampleRate(16000)
            // "language_hints"只支持paraformer-realtime-v2模型
            .parameter("language_hints", new String[]{"zh", "en"})
            .build();
    try {
      System.out.println("识别结果：" + recognizer.call(param, new File("asr_example.wav")));
    } catch (Exception e) {
      e.printStackTrace();
    } finally {
      recognizer.getDuplexApi().close(1000, "bye");
    }
    System.out.println(
        "[Metric] requestId: "
            + recognizer.getLastRequestId()
            + ", first package delay ms: "
            + recognizer.getFirstPackageDelay()
            + ", last package delay ms: "
            + recognizer.getLastPackageDelay());
    System.exit(0);
  }
}
```

## 双向流式调用：基于回调

通过 `ResultCallback` 接口接收识别结果，`call(param, callback)` 不阻塞线程。调用后通过 `sendAudioFrame(ByteBuffer)` 持续推送音频帧，调用 `stop()` 等待识别完成。

以下示例从麦克风采集音频并进行实时识别：

```java
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
import com.alibaba.dashscope.common.ResultCallback;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.TargetDataLine;
import java.nio.ByteBuffer;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;

public class Main {
  public static void main(String[] args) throws InterruptedException {
    ExecutorService executorService = Executors.newSingleThreadExecutor();
    executorService.submit(new RealtimeRecognitionTask());
    executorService.shutdown();
    executorService.awaitTermination(1, TimeUnit.MINUTES);
    System.exit(0);
  }
}

class RealtimeRecognitionTask implements Runnable {
  @Override
  public void run() {
    RecognitionParam param = RecognitionParam.builder()
        // .apiKey("yourApikey")
        .model("paraformer-realtime-v2")
        .format("wav")
        .sampleRate(16000)
        .parameter("language_hints", new String[]{"zh", "en"})
        .build();
    Recognition recognizer = new Recognition();
    ResultCallback<RecognitionResult> callback = new ResultCallback<RecognitionResult>() {
      @Override
      public void onEvent(RecognitionResult result) {
        if (result.isSentenceEnd()) {
          System.out.println("Final Result: " + result.getSentence().getText());
        } else {
          System.out.println("Intermediate Result: " + result.getSentence().getText());
        }
      }
      @Override public void onComplete() { System.out.println("Recognition complete"); }
      @Override public void onError(Exception e) { System.out.println("RecognitionCallback error: " + e.getMessage()); }
    };
    try {
      recognizer.call(param, callback);
      AudioFormat audioFormat = new AudioFormat(16000, 16, 1, true, false);
      TargetDataLine targetDataLine = AudioSystem.getTargetDataLine(audioFormat);
      targetDataLine.open(audioFormat);
      targetDataLine.start();
      ByteBuffer buffer = ByteBuffer.allocate(1024);
      long start = System.currentTimeMillis();
      while (System.currentTimeMillis() - start < 50000) {
        int read = targetDataLine.read(buffer.array(), 0, buffer.capacity());
        if (read > 0) {
          buffer.limit(read);
          recognizer.sendAudioFrame(buffer);
          buffer = ByteBuffer.allocate(1024);
          Thread.sleep(20);
        }
      }
      recognizer.stop();
    } catch (Exception e) {
      e.printStackTrace();
    } finally {
      recognizer.getDuplexApi().close(1000, "bye");
    }
    System.out.println(
        "[Metric] requestId: "
            + recognizer.getLastRequestId()
            + ", first package delay ms: "
            + recognizer.getFirstPackageDelay()
            + ", last package delay ms: "
            + recognizer.getLastPackageDelay());
  }
}
```

## 双向流式调用：基于Flowable

通过 `streamCall(param, Flowable<ByteBuffer>)` 方法以响应式编程风格发起识别，返回 `Flowable<RecognitionResult>`。以下示例从麦克风采集音频，通过 `blockingForEach` 同步处理识别结果：

```java
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
import com.alibaba.dashscope.exception.NoApiKeyException;
import io.reactivex.BackpressureStrategy;
import io.reactivex.Flowable;
import javax.sound.sampled.AudioFormat;
import javax.sound.sampled.AudioSystem;
import javax.sound.sampled.TargetDataLine;
import java.nio.ByteBuffer;

public class Main {
  public static void main(String[] args) throws NoApiKeyException {
    Flowable<ByteBuffer> audioSource = Flowable.create(
        emitter -> {
          new Thread(() -> {
            try {
              AudioFormat audioFormat = new AudioFormat(16000, 16, 1, true, false);
              TargetDataLine targetDataLine = AudioSystem.getTargetDataLine(audioFormat);
              targetDataLine.open(audioFormat);
              targetDataLine.start();
              ByteBuffer buffer = ByteBuffer.allocate(1024);
              long start = System.currentTimeMillis();
              while (System.currentTimeMillis() - start < 50000) {
                int read = targetDataLine.read(buffer.array(), 0, buffer.capacity());
                if (read > 0) {
                  buffer.limit(read);
                  emitter.onNext(buffer);
                  buffer = ByteBuffer.allocate(1024);
                  Thread.sleep(20);
                }
              }
              emitter.onComplete();
            } catch (Exception e) {
              emitter.onError(e);
            }
          }).start();
        },
        BackpressureStrategy.BUFFER);

    Recognition recognizer = new Recognition();
    RecognitionParam param = RecognitionParam.builder()
        // .apiKey("yourApikey")
        .model("paraformer-realtime-v2")
        .format("pcm")
        .sampleRate(16000)
        .parameter("language_hints", new String[]{"zh", "en"})
        .build();

    recognizer.streamCall(param, audioSource).blockingForEach(result -> {
      if (result.isSentenceEnd()) {
        System.out.println("Final Result: " + result.getSentence().getText());
      } else {
        System.out.println("Intermediate Result: " + result.getSentence().getText());
      }
    });
    recognizer.getDuplexApi().close(1000, "bye");
    System.out.println(
        "[Metric] requestId: "
            + recognizer.getLastRequestId()
            + ", first package delay ms: "
            + recognizer.getFirstPackageDelay()
            + ", last package delay ms: "
            + recognizer.getLastPackageDelay());
    System.exit(0);
  }
}
```

## 高并发调用

在 DashScope Java SDK 中，采用了 OkHttp3 的连接池技术，以减少重复建立连接的开销。

## 请求参数

通过 `RecognitionParam.builder()` 构建请求参数：

| 参数                                    | 类型        | 默认值          | 必须 | 说明                                                                                                                                              |
| ------------------------------------- | --------- | ------------ | -- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| model                                 | String    | -            | 是  | 用于实时语音识别的模型                                                                                                                                     |
| sampleRate                            | Integer   | -            | 是  | 采样率（Hz）；v2任意，v1=16kHz，8k版=8kHz                                                                                                                  |
| format                                | String    | -            | 是  | pcm/wav/mp3/opus/speex/aac/amr；opus/speex需Ogg封装；wav需PCM编码；amr仅AMR-NB                                                                            |
| vocabularyId                          | String    | -            | 否  | 热词ID（v2及以上）；详见[自定义热词](/developer-guides/speech/improve-recognition-accuracy)和[热词管理](/api-reference/speech-recognition/custom-hotwords/http-api) |
| phraseId                              | String    | -            | 否  | 热词ID（v1系列）                                                                                                                                      |
| disfluencyRemovalEnabled              | boolean   | false        | 否  | 是否过滤语气词                                                                                                                                         |
| language\_hints                       | String\[] | \["zh","en"] | 否  | 指定语言代码；仅v2支持；通过parameter()或parameters()设置                                                                                                       |
| semantic\_punctuation\_enabled        | boolean   | false        | 否  | 开启语义断句（关闭VAD）；v2+；通过parameter()/parameters()设置                                                                                                  |
| max\_sentence\_silence                | Integer   | 800          | 否  | VAD断句静音阈值（ms），200-6000；v2+，VAD模式                                                                                                                |
| multi\_threshold\_mode\_enabled       | boolean   | false        | 否  | 防止VAD断句切割过长；v2+，VAD模式                                                                                                                           |
| punctuation\_prediction\_enabled      | boolean   | true         | 否  | 自动添加标点；v2+                                                                                                                                      |
| heartbeat                             | boolean   | false        | 否  | 长连接保持；SDK>=2.19.1；v2+                                                                                                                           |
| inverse\_text\_normalization\_enabled | boolean   | true         | 否  | ITN（中文数字→阿拉伯数字）；v2+                                                                                                                             |
| apiKey                                | String    | -            | 否  | 用户API Key                                                                                                                                       |

## 关键接口

### Recognition

| 方法                                                          | 参数                | 返回值                           | 描述                            |
| ----------------------------------------------------------- | ----------------- | ----------------------------- | ----------------------------- |
| `call(RecognitionParam, ResultCallback<RecognitionResult>)` | param, callback   | 无                             | 回调形式流式识别，不阻塞线程                |
| `call(RecognitionParam, File)`                              | param, file       | String                        | 非流式调用，阻塞直到读完文件                |
| `streamCall(RecognitionParam, Flowable<ByteBuffer>)`        | param, audioFrame | `Flowable<RecognitionResult>` | Flowable流式识别                  |
| `sendAudioFrame(ByteBuffer)`                                | audioFrame        | 无                             | 推送音频帧，建议每包100ms，1KB-16KB      |
| `stop()`                                                    | 无                 | 无                             | 停止识别，阻塞直到onComplete/onError触发 |
| `getDuplexApi().close(int, String)`                         | code, reason      | true                          | 关闭WebSocket连接，任务结束后必须调用       |
| `getLastRequestId()`                                        | 无                 | requestId                     | 获取requestId（v2.18.0+）         |
| `getFirstPackageDelay()`                                    | 无                 | 首包延迟                          | 任务完成后使用（v2.18.0+）             |
| `getLastPackageDelay()`                                     | 无                 | 尾包延迟                          | 任务完成后使用（v2.18.0+）             |

### 回调接口（ResultCallback）

| 方法                           | 参数     | 返回值 | 描述       |
| ---------------------------- | ------ | --- | -------- |
| `onEvent(RecognitionResult)` | result | 无   | 服务有回复时触发 |
| `onComplete()`               | 无      | 无   | 任务完成后触发  |
| `onError(Exception)`         | e      | 无   | 发生异常时触发  |

## 响应结果

### RecognitionResult

| 方法                | 返回值       | 描述          |
| ----------------- | --------- | ----------- |
| `getRequestId()`  | requestId | 获取requestId |
| `isSentenceEnd()` | boolean   | 判断句子是否结束    |
| `getSentence()`   | Sentence  | 获取单句信息      |

### 实时识别结果（Sentence）

| 方法                   | 返回值              | 描述                                                                               |
| -------------------- | ---------------- | -------------------------------------------------------------------------------- |
| `getBeginTime()`     | long（ms）         | 句子开始时间                                                                           |
| `getEndTime()`       | long（ms）         | 句子结束时间                                                                           |
| `getText()`          | String           | 识别文本                                                                             |
| `getWords()`         | `List<Word>`     | 字时间戳信息列表                                                                         |
| `getEmoTag()`        | String           | 当前句子情感（positive/negative/neutral）；仅paraformer-realtime-8k-v2，isSentenceEnd=true时 |
| `getEmoConfidence()` | Double\[0.0,1.0] | 情感置信度；仅paraformer-realtime-8k-v2                                                 |

### 字时间戳信息（Word）

| 方法                 | 返回值      | 描述    |
| ------------------ | -------- | ----- |
| `getBeginTime()`   | long（ms） | 字开始时间 |
| `getEndTime()`     | long（ms） | 字结束时间 |
| `getText()`        | String   | 识别的字  |
| `getPunctuation()` | String   | 标点    |

## 错误码

请参考[错误码](/api-reference/preparation/error-messages)文档了解错误码的含义和处理方法。

## 更多示例

更多调用示例请参考GitHub仓库中的[示例代码](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/speech-recognition)。

## 常见问题

<Accordion title="长时间静默如何保持长连接？">
  设置 `heartbeat=true` 参数（需SDK>=2.19.1，仅v2+支持），同时持续发送静默音频帧，保持WebSocket连接活跃。
</Accordion>

<Accordion title="如何将音频格式转换？">
  推荐使用FFmpeg进行音频格式转换：

  ```bash
  # 基础转换命令（万能模板）
  ffmpeg -i input_audio.ext -c:a 编码器名 -b:a 比特率 -ar 采样率 -ac 声道数 output.ext

  # WAV → MP3
  ffmpeg -i input.wav -c:a libmp3lame -q:a 0 output.mp3
  # MP3 → WAV (16bit PCM)
  ffmpeg -i input.mp3 -c:a pcm_s16le -ar 44100 -ac 2 output.wav
  # M4A → AAC
  ffmpeg -i input.m4a -c:a copy output.aac
  ffmpeg -i input.m4a -c:a aac -b:a 256k output.aac
  # FLAC → Opus
  ffmpeg -i input.flac -c:a libopus -b:a 128k -vbr on output.opus
  ```

  查看音频文件信息：

  ```bash
  ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.xxx
  ```
</Accordion>

<Accordion title="是否支持查看每句话时间范围？">
  支持。识别结果中每个句子（Sentence）都包含开始时间（`getBeginTime()`）和结束时间（`getEndTime()`），单位为毫秒。
</Accordion>

<Accordion title="如何识别本地文件？">
  有两种方式：

  1. **非流式调用**：直接传入文件路径，调用 `call(param, new File("path/to/file.wav"))` 方法。
  2. **流式调用**：将文件读取为二进制流，通过 `sendAudioFrame(ByteBuffer)` 分帧发送，或使用 `streamCall(param, audioSource)` 方式传入 `Flowable<ByteBuffer>`。
</Accordion>

<Accordion title="无法识别语音是什么原因？">
  请检查以下几点：

  - 确认 `format` 和 `sampleRate` 参数与实际音频文件一致
  - 如设置了 `language_hints`，确认指定的语种与音频实际语种匹配
  - 如识别效果不佳，可使用[自定义热词](/developer-guides/speech/improve-recognition-accuracy)提升特定词汇的识别准确率
</Accordion>
