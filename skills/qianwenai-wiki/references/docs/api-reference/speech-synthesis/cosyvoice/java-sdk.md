> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音合成 Qwen-Audio-TTS/CosyVoice Java SDK

> Qwen-Audio-TTS/CosyVoice 实时语音合成 Java SDK 参考文档

模型概览和音色选择请参见[语音合成](/developer-guides/speech/tts)。

## 服务端点

SDK 默认服务端点为 `wss://dashscope.aliyuncs.com/api-ws/v1/inference`。如需修改，可在初始化前设置 `Constants.baseWebsocketApiUrl`。

## 前提条件

- 登录千问AI平台并[创建 API Key](/api-reference/preparation/api-key)。建议[将其导出为环境变量](/api-reference/preparation/export-api-key-env)，避免硬编码。

<Note>
  如需向第三方应用提供临时访问权限，或对敏感操作进行严格管控，可使用[临时认证令牌](/api-reference/more/generate-a-temporary-api-key)。临时令牌 60 秒后过期，可有效降低泄露风险。在代码中用临时令牌替换 API Key 即可。
</Note>

- [安装最新版 DashScope SDK](/api-reference/preparation/install-sdk)。

## 模型与计费

请参见[语音合成](/developer-guides/speech/tts)。

## 文本与格式限制

### 文本长度限制

- [非流式](#非流式调用)、[单向流式](#单向流式调用)或 Flowable 单向流式：单次请求最多 20,000 字符。
- [双向流式](#双向流式调用)或 Flowable 双向流式：单次请求最多 20,000 字符，累计最多 200,000 字符。

### 字符计数规则

- 中文汉字（简体、繁体、日文汉字、韩文汉字）每个计 2 个字符。其他字符（标点、字母、数字、假名、韩文字母）每个计 1 个字符。
- SSML 标签不计入文本长度。
- 示例：
  - `"你好"` → 2（汉字）+ 2（汉字）= 4 字符
  - `"中A文123"` → 2（汉字）+ 1（A）+ 2（汉字）+ 1（1）+ 1（2）+ 1（3）= 8 字符
  - `"中文。"` → 2（汉字）+ 2（汉字）+ 1（句号）= 5 字符
  - `"中 文。"` → 2（汉字）+ 1（空格）+ 2（汉字）+ 1（句号）= 6 字符
  - `"<speak>你好</speak>"` → 2（汉字）+ 2（汉字）= 4 字符

### 编码格式

使用 UTF-8 编码。

### 数学表达式

cosyvoice-v3-flash 和 cosyvoice-v3-plus 支持数学表达式解析，覆盖常见的中小学数学内容，包括基本运算、代数和几何。

<Note>
  该功能仅支持中文。
</Note>

请参见[将 LaTeX 公式转为语音（仅限中文）](/developer-guides/speech/ssml#latex-公式转语音)。

### SSML 支持

SSML 适用于 cosyvoice-v3-flash 和 cosyvoice-v3-plus 上的自定义音色（声音设计或声音克隆），以及[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标注支持 SSML 的系统音色。

使用要求：

- [DashScope SDK](/api-reference/preparation/install-sdk) 2.20.3 或更高版本。
- 仅支持[非流式](#非流式调用)和[单向流式](#单向流式调用)调用（[SpeechSynthesizer](#speechsynthesizer-类) 的 `call` 方法）。不支持[双向流式](#双向流式调用)调用（`streamingCall`）和 [Flowable 调用](#flowable-调用)。
- 将包含 SSML 的文本传给 `call` 方法即可，用法与普通文本相同。

## 快速开始

[SpeechSynthesizer 类](#speechsynthesizer-类)支持以下调用方式：

- **非流式**：发送完整文本，返回完整音频。阻塞式调用，适合短文本。
- **单向流式**：发送完整文本，通过回调返回音频。非阻塞式调用，适合对延迟敏感的短文本场景。
- **双向流式**：逐步发送文本片段，通过回调实时返回音频。非阻塞式调用，适合对延迟敏感的长文本场景。

### 非流式调用

同步发送文本，返回完整音频结果。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/7378862771/CAEQVBiBgMDcgq3A5RkiIDgyZjYzZDRkYWExODQwYjdhMGZlZTVjOTc3MWU1YTBm4709861_20241015153444.149.svg)

实例化 [SpeechSynthesizer](#speechsynthesizer-类)，绑定[请求参数](#请求参数)，然后调用 `call` 方法获取二进制音频数据。文本上限：20,000 字符。

<Warning>
  每次调用 `call` 前需重新初始化 `SpeechSynthesizer` 实例。
</Warning>

<Accordion title="点击查看完整示例">
  ```java
  import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
  import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
  import com.alibaba.dashscope.utils.Constants;

  import java.io.File;
  import java.io.FileOutputStream;
  import java.io.IOException;
  import java.nio.ByteBuffer;

  public class Main {
    private static String model = "cosyvoice-v3-flash";
    private static String voice = "longanyang";

    public static void streamAudioDataToSpeaker() {
      SpeechSynthesisParam param =
          SpeechSynthesisParam.builder()
              // 如果未配置环境变量，请将下一行替换为：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model(model)
              .voice(voice)
              .build();

      // 同步模式：将回调（第二个参数）设为 null。
      SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
      ByteBuffer audio = null;
      try {
        // 阻塞直到音频返回。
        audio = synthesizer.call("今天天气怎么样？");
      } catch (Exception e) {
        throw new RuntimeException(e);
      } finally {
        // 任务完成后关闭 WebSocket 连接。
        synthesizer.getDuplexApi().close(1000, "bye");
      }
      if (audio != null) {
        File file = new File("output.mp3");
        // 首次调用的首包延迟包含 WebSocket 建连时间。
        System.out.println(
            "[Metric] Request ID: "
                + synthesizer.getLastRequestId()
                + ", First-packet latency (ms): "
                + synthesizer.getFirstPackageDelay());
        try (FileOutputStream fos = new FileOutputStream(file)) {
          // call() 返回的 ByteBuffer position=0 且 remaining=capacity，array() 返回完整音频数据。
          fos.write(audio.array());
        } catch (IOException e) {
          throw new RuntimeException(e);
        }
      }
    }

    public static void main(String[] args) {
      Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
      streamAudioDataToSpeaker();
      System.exit(0);
    }
  }
  ```
</Accordion>

### 单向流式调用

异步提交文本，通过 `ResultCallback` 增量接收音频数据。

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/8378862771/CAEQVBiBgIDs8q_A5RkiIGQ3YzdkNDJkMWI1NjQwOGZhN2FkMWJjYmMwOTJkMjZj4709861_20241015153444.149.svg)

实例化 [SpeechSynthesizer](#speechsynthesizer-类)，绑定[请求参数](#请求参数)和 [ResultCallback](#resultcallback-接口)，然后调用 `call` 方法。通过 `onEvent` 实时获取音频。文本上限：20,000 字符。

<Warning>
  每次调用 `call` 前需重新初始化 `SpeechSynthesizer` 实例。
</Warning>

<Accordion title="点击查看完整示例">
  ```java
  import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
  import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
  import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
  import com.alibaba.dashscope.common.ResultCallback;
  import com.alibaba.dashscope.utils.Constants;

  import java.time.LocalDateTime;
  import java.time.format.DateTimeFormatter;
  import java.util.concurrent.CountDownLatch;

  class TimeUtils {
    private static final DateTimeFormatter formatter =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    public static String getTimestamp() {
      return LocalDateTime.now().format(formatter);
    }
  }

  public class Main {
    private static String model = "cosyvoice-v3-flash";
    private static String voice = "longanyang";

    public static void streamAudioDataToSpeaker() {
      CountDownLatch latch = new CountDownLatch(1);

      // 实现 ResultCallback 接口。
      ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
        @Override
        public void onEvent(SpeechSynthesisResult result) {
          // System.out.println("收到消息: " + result);
          if (result.getAudioFrame() != null) {
            // 在此添加音频处理逻辑。
            System.out.println(TimeUtils.getTimestamp() + " 收到音频");
          }
        }

        @Override
        public void onComplete() {
          System.out.println(TimeUtils.getTimestamp() + " 收到完成信号，语音合成结束。");
          latch.countDown();
        }

        @Override
        public void onError(Exception e) {
          System.out.println("发生异常：" + e.toString());
          latch.countDown();
        }
      };

      SpeechSynthesisParam param =
          SpeechSynthesisParam.builder()
              // 如果未配置环境变量，请将下一行替换为：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model(model)
              .voice(voice)
              .build();
      // 将回调作为第二个参数传入，启用异步模式。
      SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
      // 非阻塞：立即返回 null，结果通过 onEvent 回调返回。
      try {
        synthesizer.call("今天天气怎么样？");
        latch.await();
      } catch (Exception e) {
        throw new RuntimeException(e);
      } finally {
        // 任务完成后关闭 WebSocket 连接。
        synthesizer.getDuplexApi().close(1000, "bye");
      }
      // 首次调用的首包延迟包含 WebSocket 建连时间。
      System.out.println(
          "[Metric] Request ID: "
              + synthesizer.getLastRequestId()
              + ", First-packet latency (ms): "
              + synthesizer.getFirstPackageDelay());
    }

    public static void main(String[] args) {
      Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
      streamAudioDataToSpeaker();
      System.exit(0);
    }
  }
  ```
</Accordion>

### 双向流式调用

分多次发送文本片段，通过 `ResultCallback` 增量接收音频。

<Note>
  - 多次调用 `streamingCall` 提交文本片段。服务端自动分句：完整句子立即合成，不完整的句子会缓存直到补全。调用 `streamingComplete()` 可强制合成所有缓存文本。

  - 文本片段发送间隔不得超过 23 秒，否则会触发超时错误。发送完毕后请调用 `streamingComplete()`。

    > 23 秒的服务端超时不可在客户端修改。
</Note>

![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/8378862771/CAEQVBiBgIDK2LPA5RkiIDdkMTYyMTBlODdjYzRmM2Y5NDc0OWM2MmVlNjAzMDRi4709861_20241015153444.149.svg)

<Steps>
  <Step title="实例化 SpeechSynthesizer">
    实例化 [SpeechSynthesizer](#speechsynthesizer-类)，绑定[请求参数](#请求参数)和 [ResultCallback](#resultcallback-接口)。
  </Step>

  <Step title="发送文本流">
    多次调用 `streamingCall` 分段发送文本。服务端通过 `onEvent` 实时返回音频。

    每次 `streamingCall` 的文本片段上限：20,000 字符。所有片段累计上限：200,000 字符。
  </Step>

  <Step title="完成合成">
    调用 `streamingComplete` 完成合成。该方法会阻塞直到 `onComplete` 或 `onError` 触发。

    务必调用此方法，否则尾部文本可能无法被合成。
  </Step>
</Steps>

<Accordion title="点击查看完整示例">
  ```java
  import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
  import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
  import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
  import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
  import com.alibaba.dashscope.common.ResultCallback;
  import com.alibaba.dashscope.utils.Constants;

  import java.time.LocalDateTime;
  import java.time.format.DateTimeFormatter;

  class TimeUtils {
    private static final DateTimeFormatter formatter =
        DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

    public static String getTimestamp() {
      return LocalDateTime.now().format(formatter);
    }
  }

  public class Main {
    private static String[] textArray = {"流式语音合成 SDK ",
        "可以将输入文本 ", "转换为二进制音频数据。", "相比非流式合成，",
        "流式合成具有更好的实时性。", "您几乎可以在输入文本的同时听到音频输出，",
        "这极大地提升了用户体验 ", "并减少了等待时间。",
        "这非常适合使用大型 ", "语言模型（LLM）",
        "从文本流中合成语音的应用场景。"};
    private static String model = "cosyvoice-v3-flash";
    private static String voice = "longanyang";

    public static void streamAudioDataToSpeaker() {
      // 配置回调。
      ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
        @Override
        public void onEvent(SpeechSynthesisResult result) {
          // System.out.println("收到消息: " + result);
          if (result.getAudioFrame() != null) {
            // 在此添加音频处理逻辑。
            System.out.println(TimeUtils.getTimestamp() + " 收到音频");
          }
        }

        @Override
        public void onComplete() {
          System.out.println(TimeUtils.getTimestamp() + " 收到完成信号，语音合成结束。");
        }

        @Override
        public void onError(Exception e) {
          System.out.println("发生异常：" + e.toString());
        }
      };

      // 请求参数
      SpeechSynthesisParam param =
          SpeechSynthesisParam.builder()
              // 如果未配置环境变量，请将下一行替换为：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model(model)
              .voice(voice)
              .format(SpeechSynthesisAudioFormat
                  .PCM_22050HZ_MONO_16BIT) // 流式合成请使用 PCM 或 MP3 格式。
              .build();
      SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
      try {
        for (String text : textArray) {
          // 发送文本片段，音频通过 onEvent 实时返回。
          synthesizer.streamingCall(text);
        }
        // 等待流式合成完成。
        synthesizer.streamingComplete();
      } catch (Exception e) {
        throw new RuntimeException(e);
      } finally {
        // 任务完成后关闭 WebSocket 连接。
        synthesizer.getDuplexApi().close(1000, "bye");
      }

      // 首次调用的首包延迟包含 WebSocket 建连时间。
      System.out.println(
          "[Metric] Request ID: "
              + synthesizer.getLastRequestId()
              + ", First-packet latency (ms): "
              + synthesizer.getFirstPackageDelay());
    }

    public static void main(String[] args) {
      Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
      streamAudioDataToSpeaker();
      System.exit(0);
    }
  }
  ```
</Accordion>

### Flowable 调用

Flowable 是 Apache 2.0 协议下的开源响应式编程框架，详情请参见 [Flowable API 文档](https://reactivex.io/RxJava/2.x/javadoc/)。使用前请先集成 RxJava 库并了解响应式编程基础。

<Tabs>
  <Tab title="单向流式调用">
    通过 Flowable 对象的 `blockingForEach` 方法阻塞获取每个 `SpeechSynthesisResult`。所有流式数据返回后，也可通过 `getAudioFrame` 获取完整结果。

    <Accordion title="点击查看完整示例">
      ```java
      import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
      import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.utils.Constants;

      import java.time.LocalDateTime;
      import java.time.format.DateTimeFormatter;

      class TimeUtils {
        private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

        public static String getTimestamp() {
          return LocalDateTime.now().format(formatter);
        }
      }

      public class Main {
        private static String model = "cosyvoice-v3-flash";
        private static String voice = "longanyang";

        public static void streamAudioDataToSpeaker() throws NoApiKeyException {
          SpeechSynthesisParam param =
              SpeechSynthesisParam.builder()
                  // 如果未配置环境变量，请将下一行替换为：.apiKey("sk-xxx")
                  .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                  .model(model)
                  .voice(voice)
                  .build();
          SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
          synthesizer.callAsFlowable("今天天气怎么样？").blockingForEach(result -> {
            // System.out.println("收到消息: " + result);
            if (result.getAudioFrame() != null) {
              // 在此添加音频处理逻辑。
              System.out.println(TimeUtils.getTimestamp() + " 收到音频");
            }
          });
          // 任务完成后关闭 WebSocket 连接。
          synthesizer.getDuplexApi().close(1000, "bye");
          // 首次调用的首包延迟包含 WebSocket 建连时间。
          System.out.println(
              "[Metric] Request ID: "
                  + synthesizer.getLastRequestId()
                  + ", First-packet latency (ms): "
                  + synthesizer.getFirstPackageDelay());
        }

        public static void main(String[] args) throws NoApiKeyException {
          Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
          streamAudioDataToSpeaker();
          System.exit(0);
        }
      }
      ```
    </Accordion>
  </Tab>

  <Tab title="双向流式调用">
    使用 Flowable 对象作为文本流输入，并通过返回的 Flowable 的 `blockingForEach` 获取每个 `SpeechSynthesisResult`。所有流式数据返回后，也可通过 `getAudioFrame` 获取完整结果。

    <Accordion title="点击查看完整示例">
      ```java
      import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
      import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.utils.Constants;
      import io.reactivex.BackpressureStrategy;
      import io.reactivex.Flowable;

      import java.time.LocalDateTime;
      import java.time.format.DateTimeFormatter;

      class TimeUtils {
        private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

        public static String getTimestamp() {
          return LocalDateTime.now().format(formatter);
        }
      }

      public class Main {
        private static String[] textArray = {"流式语音合成 SDK ",
            "可以将输入文本 ", "转换为二进制音频数据。", "相比非流式合成，",
            "流式合成具有更好的实时性。", "您几乎可以在输入文本的同时听到音频输出，",
            "这极大地提升了用户体验 ", "并减少了等待时间。",
            "这非常适合使用大型 ", "语言模型（LLM）",
            "从文本流中合成语音的应用场景。"};
        private static String model = "cosyvoice-v3-flash";
        private static String voice = "longanyang";

        public static void streamAudioDataToSpeaker() throws NoApiKeyException {
          // 模拟流式输入。
          Flowable<String> textSource = Flowable.create(emitter -> {
            new Thread(() -> {
              for (int i = 0; i < textArray.length; i++) {
                emitter.onNext(textArray[i]);
                try {
                  Thread.sleep(1000);
                } catch (InterruptedException e) {
                  throw new RuntimeException(e);
                }
              }
              emitter.onComplete();
            }).start();
          }, BackpressureStrategy.BUFFER);

          // 请求参数
          SpeechSynthesisParam param =
              SpeechSynthesisParam.builder()
                  // 如果未配置环境变量，请将下一行替换为：.apiKey("sk-xxx")
                  .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                  .model(model)
                  .voice(voice)
                  .build();
          SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
          synthesizer.streamingCallAsFlowable(textSource).blockingForEach(result -> {
            if (result.getAudioFrame() != null) {
              // 在此添加音频播放逻辑。
              System.out.println(
                  TimeUtils.getTimestamp() +
                      " 二进制音频大小: " + result.getAudioFrame().capacity());
            }
          });
          synthesizer.getDuplexApi().close(1000, "bye");
          // 首次调用的首包延迟包含 WebSocket 建连时间。
          System.out.println(
              "[Metric] Request ID: "
                  + synthesizer.getLastRequestId()
                  + ", First-packet latency (ms): "
                  + synthesizer.getFirstPackageDelay());
        }

        public static void main(String[] args) throws NoApiKeyException {
          Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
          streamAudioDataToSpeaker();
          System.exit(0);
        }
      }
      ```
    </Accordion>
  </Tab>
</Tabs>

### 高并发调用

DashScope Java SDK 使用 OkHttp3 连接池来减少连接开销。请参见[高并发管理](/api-reference/more/connection-pooling)。

## 请求参数

通过 SpeechSynthesisParam 的链式方法配置 model、voice 等参数，将配置好的对象传给 [SpeechSynthesizer](#speechsynthesizer-类) 构造函数。

<Accordion title="点击查看示例">
  ```java
  SpeechSynthesisParam param = SpeechSynthesisParam.builder()
    .model("cosyvoice-v3-flash")
    .voice("longanyang")
    .format(SpeechSynthesisAudioFormat.WAV_8000HZ_MONO_16BIT) // 音频格式和采样率
    .volume(50) // 音量：[0, 100]
    .speechRate(1.0f) // 语速：[0.5, 2]
    .pitchRate(1.0f) // 音调：[0.5, 2]
    .build();
  ```
</Accordion>

| 参数                       | 类型          | 是否必选 | 说明                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ------------------------ | ----------- | ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model                    | String      | 是    | 语音合成模型。所有可选项请参见[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| voice                    | String      | 是    | 合成使用的音色。可用的系统音色请参见[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| format                   | enum        | 否    | 音频格式和采样率。默认：22.05 kHz 的 MP3。默认采样率为音色最佳采样率，支持降采样和升采样。<br /><br />支持的格式：<ul><li>所有模型：<ul><li>SpeechSynthesisAudioFormat.WAV\_8000HZ\_MONO\_16BIT：WAV，8 kHz</li><li>SpeechSynthesisAudioFormat.WAV\_16000HZ\_MONO\_16BIT：WAV，16 kHz</li><li>SpeechSynthesisAudioFormat.WAV\_22050HZ\_MONO\_16BIT：WAV，22.05 kHz</li><li>SpeechSynthesisAudioFormat.WAV\_24000HZ\_MONO\_16BIT：WAV，24 kHz</li><li>SpeechSynthesisAudioFormat.WAV\_44100HZ\_MONO\_16BIT：WAV，44.1 kHz</li><li>SpeechSynthesisAudioFormat.WAV\_48000HZ\_MONO\_16BIT：WAV，48 kHz</li><li>SpeechSynthesisAudioFormat.MP3\_8000HZ\_MONO\_128KBPS：MP3，8 kHz</li><li>SpeechSynthesisAudioFormat.MP3\_16000HZ\_MONO\_128KBPS：MP3，16 kHz</li><li>SpeechSynthesisAudioFormat.MP3\_22050HZ\_MONO\_256KBPS：MP3，22.05 kHz</li><li>SpeechSynthesisAudioFormat.MP3\_24000HZ\_MONO\_256KBPS：MP3，24 kHz</li><li>SpeechSynthesisAudioFormat.MP3\_44100HZ\_MONO\_256KBPS：MP3，44.1 kHz</li><li>SpeechSynthesisAudioFormat.MP3\_48000HZ\_MONO\_256KBPS：MP3，48 kHz</li><li>SpeechSynthesisAudioFormat.PCM\_8000HZ\_MONO\_16BIT：PCM，8 kHz</li><li>SpeechSynthesisAudioFormat.PCM\_16000HZ\_MONO\_16BIT：PCM，16 kHz</li><li>SpeechSynthesisAudioFormat.PCM\_22050HZ\_MONO\_16BIT：PCM，22.05 kHz</li><li>SpeechSynthesisAudioFormat.PCM\_24000HZ\_MONO\_16BIT：PCM，24 kHz</li><li>SpeechSynthesisAudioFormat.PCM\_44100HZ\_MONO\_16BIT：PCM，44.1 kHz</li><li>SpeechSynthesisAudioFormat.PCM\_48000HZ\_MONO\_16BIT：PCM，48 kHz</li></ul></li><li>Opus（需 DashScope 2.21.0+）。可通过 `bit_rate` 调整比特率：<ul><li>SpeechSynthesisAudioFormat.OGG\_OPUS\_8KHZ\_MONO\_32KBPS：Opus，8 kHz，32 kbps</li><li>SpeechSynthesisAudioFormat.OGG\_OPUS\_16KHZ\_MONO\_16KBPS：Opus，16 kHz，16 kbps</li><li>SpeechSynthesisAudioFormat.OGG\_OPUS\_16KHZ\_MONO\_32KBPS：Opus，16 kHz，32 kbps</li><li>SpeechSynthesisAudioFormat.OGG\_OPUS\_16KHZ\_MONO\_64KBPS：Opus，16 kHz，64 kbps</li><li>SpeechSynthesisAudioFormat.OGG\_OPUS\_24KHZ\_MONO\_16KBPS：Opus，24 kHz，16 kbps</li><li>SpeechSynthesisAudioFormat.OGG\_OPUS\_24KHZ\_MONO\_32KBPS：Opus，24 kHz，32 kbps</li><li>SpeechSynthesisAudioFormat.OGG\_OPUS\_24KHZ\_MONO\_64KBPS：Opus，24 kHz，64 kbps</li><li>SpeechSynthesisAudioFormat.OGG\_OPUS\_48KHZ\_MONO\_16KBPS：Opus，48 kHz，16 kbps</li><li>SpeechSynthesisAudioFormat.OGG\_OPUS\_48KHZ\_MONO\_32KBPS：Opus，48 kHz，32 kbps</li><li>SpeechSynthesisAudioFormat.OGG\_OPUS\_48KHZ\_MONO\_64KBPS：Opus，48 kHz，64 kbps</li></ul></li></ul> |
| volume                   | int         | 否    | 音量。默认：50。范围：\[0, 100]。线性缩放，0 为静音，100 为最大音量。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| speechRate               | float       | 否    | 语速。默认：1.0。范围：\[0.5, 2.0]。小于 1.0 语速减慢，大于 1.0 语速加快。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| pitchRate                | float       | 否    | 音调倍率。默认：1.0。范围：\[0.5, 2.0]。与感知音高的关系非线性：大于 1.0 升高音调，小于 1.0 降低音调。建议实际测试以找到合适的值。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| bit\_rate                | int         | 否    | Opus 格式的音频比特率（kbps）。默认：32。范围：\[6, 510]。<br /><br />通过 `SpeechSynthesisParam` 的 `parameter` 或 `parameters` 方法设置。请参见下方示例。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| enableWordTimestamp      | boolean     | 否    | 是否启用字级时间戳。默认：false。适用于 cosyvoice-v3-flash、cosyvoice-v3-plus 和 cosyvoice-v2 模型的复刻音色，以及[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标注支持此功能的系统音色。<br /><br />时间戳结果仅通过回调接口返回。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| seed                     | int         | 否    | 随机种子。不同的种子产生不同的合成结果，相同种子和相同参数可复现相同输出。默认：0。范围：\[0, 65535]。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| languageHints            | List        | 否    | 合成目标语言。当数字、缩写或符号的发音不准确，或不常见语种需要改善时使用。可选值：zh（中文）、en（英语）、fr（法文）、de（德文）、ja（日文）、ko（韩文）、ru（俄文）、pt（葡萄牙文）、th（泰文）、id（印尼文）、vi（越南文）、es（西班牙语）、it（意大利语）、ms（马来西亚语）、fil（菲律宾语）、ar（阿拉伯语）。**注意**：此参数为数组，但仅处理第一个元素，请只传入一个值。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| instruction              | String      | 否    | 通过指令控制方言、情感或说话风格。适用于[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标注支持 Instruct 的系统音色。**最大长度**：100 字符。请参见下方指令示例。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| enable\_aigc\_tag        | boolean     | 否    | 在音频中添加不可见的 AIGC 标识。设为 true 时，在支持的格式（WAV、MP3、Opus）中嵌入不可见标识。默认：false。cosyvoice-v3-flash 和 cosyvoice-v3-plus 支持。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| aigc\_propagator         | String      | 否    | 设置 AIGC 标识中的 `ContentPropagator` 字段，用于标识内容传播者。仅在 `enable_aigc_tag` 为 true 时生效。默认：UID。cosyvoice-v3-flash 和 cosyvoice-v3-plus 支持。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| aigc\_propagate\_id      | String      | 否    | 设置 AIGC 标识中的 `PropagateID` 字段，用于唯一标识一次传播行为。仅在 `enable_aigc_tag` 为 true 时生效。默认：当前请求 ID。cosyvoice-v3-flash 和 cosyvoice-v3-plus 支持。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| hotFix                   | ParamHotFix | 否    | 文本热补丁配置。可自定义特定词语的发音或在合成前替换文本。仅 cosyvoice-v3-flash 支持。请参见下方 hotFix 示例。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| enable\_markdown\_filter | boolean     | 否    | 合成前移除输入文本中的 Markdown 符号，防止其被朗读。默认：false。仅 cosyvoice-v3-flash 支持。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

### 设置 `bit_rate`

<Tabs>
  <Tab title="使用 parameter()">
    ```java
    SpeechSynthesisParam param = SpeechSynthesisParam.builder()
      .model("cosyvoice-v3-flash")
      .voice("longanyang")
      .parameter("bit_rate", 32)
      .build();
    ```
  </Tab>

  <Tab title="使用 parameters()">
    ```java
    SpeechSynthesisParam param = SpeechSynthesisParam.builder()
      .model("cosyvoice-v3-flash")
      .voice("longanyang")
      .parameters(Collections.singletonMap("bit_rate", 32))
      .build();
    ```
  </Tab>
</Tabs>

### 设置 `enable_aigc_tag`

<Tabs>
  <Tab title="使用 parameter()">
    ```java
    SpeechSynthesisParam param = SpeechSynthesisParam.builder()
      .model("cosyvoice-v3-flash")
      .voice("longanyang")
      .parameter("enable_aigc_tag", true)
      .build();
    ```
  </Tab>

  <Tab title="使用 parameters()">
    ```java
    SpeechSynthesisParam param = SpeechSynthesisParam.builder()
      .model("cosyvoice-v3-flash")
      .voice("longanyang")
      .parameters(Collections.singletonMap("enable_aigc_tag", true))
      .build();
    ```
  </Tab>
</Tabs>

### 设置 `aigc_propagator`

<Tabs>
  <Tab title="使用 parameter()">
    ```java
    SpeechSynthesisParam param = SpeechSynthesisParam.builder()
      .model("cosyvoice-v3-flash")
      .voice("longanyang")
      .parameter("enable_aigc_tag", true)
      .parameter("aigc_propagator", "xxxx")
      .build();
    ```
  </Tab>

  <Tab title="使用 parameters()">
    ```java
    Map<String, Object> map = new HashMap();
    map.put("enable_aigc_tag", true);
    map.put("aigc_propagator", "xxxx");

    SpeechSynthesisParam param = SpeechSynthesisParam.builder()
      .model("cosyvoice-v3-flash")
      .voice("longanyang")
      .parameters(map)
      .build();
    ```
  </Tab>
</Tabs>

### 设置 `aigc_propagate_id`

<Tabs>
  <Tab title="使用 parameter()">
    ```java
    SpeechSynthesisParam param = SpeechSynthesisParam.builder()
      .model("cosyvoice-v3-flash")
      .voice("longanyang")
      .parameter("enable_aigc_tag", true)
      .parameter("aigc_propagate_id", "xxxx")
      .build();
    ```
  </Tab>

  <Tab title="使用 parameters()">
    ```java
    Map<String, Object> map = new HashMap();
    map.put("enable_aigc_tag", true);
    map.put("aigc_propagate_id", "xxxx");

    SpeechSynthesisParam param = SpeechSynthesisParam.builder()
      .model("cosyvoice-v3-flash")
      .voice("longanyang")
      .parameters(map)
      .build();
    ```
  </Tab>
</Tabs>

### 设置 `enable_markdown_filter`

<Tabs>
  <Tab title="使用 parameter()">
    ```java
    SpeechSynthesisParam param = SpeechSynthesisParam.builder()
      .model("cosyvoice-v3-flash")
      .voice("longanhuan_v3.6") // 音色
      .parameter("enable_markdown_filter", true)
      .build();
    ```
  </Tab>

  <Tab title="使用 parameters()">
    ```java
    Map<String, Object> map = new HashMap();
    map.put("enable_markdown_filter", true);

    SpeechSynthesisParam param = SpeechSynthesisParam.builder()
      .model("cosyvoice-v3-flash")
      .voice("longanhuan_v3.6") // 音色
      .parameters(map)
      .build();
    ```
  </Tab>
</Tabs>

### `instruction` 示例

**cosyvoice-v3-flash**：

- 克隆音色：可使用任意自然语言指令控制合成效果。

  指令示例：

```plaintext
请用粤语说话。（支持的方言：粤语、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南语、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话。）
请尽可能大声地说一句话。
请尽可能慢地说一句话。
请尽可能快地说一句话。
请用很轻的声音说一句话。
你能说慢一点吗？
你能说得非常快吗？
你能说得非常慢吗？
你能说快一点吗？
请用非常生气的语气说一句话。
请用非常开心的语气说一句话。
请用非常恐惧的语气说一句话。
请用非常悲伤的语气说一句话。
请用非常惊讶的语气说一句话。
请尽量用坚定的语气说话。
请尽量用愤怒的语气说话。
请用亲切的语气说话。
请用冷淡的语气说话。
请用威严的语气说话。
我想体验自然的语气。
我想看看你怎么表达威胁。
我想看看你怎么表达智慧。
我想看看你怎么表达诱惑。
我想听你用活泼的方式说话。
我想听你用充满激情的方式说话。
我想听你用沉稳的方式说话。
我想听你用自信的方式说话。
你能用兴奋的情绪跟我说话吗？
你能展示一下傲慢的情绪吗？
你能展示一下优雅的情绪吗？
你能开心地回答这个问题吗？
你能做一个温柔的情绪示范吗？
你能用平静的语气跟我说话吗？
你能用深沉的方式回答我吗？
你能用粗犷的态度跟我说话吗？
用阴森的声音告诉我答案。
用坚韧的声音告诉我答案。
用自然友好的聊天风格来叙述。
用广播剧播客的语气来朗读。
```

- 系统音色：指令必须使用固定格式。详情请参见[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)、[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。

### `hotFix` 示例

```java
List<ParamHotFix.PronunciationItem> pronunciationItems = new ArrayList<>();
pronunciationItems.add(new ParamHotFix.PronunciationItem("天气", "tian1 qi4"));

List<ParamHotFix.ReplaceItem> replaceItems = new ArrayList<>();
replaceItems.add(new ParamHotFix.ReplaceItem("今天", "今日"));

ParamHotFix paramHotFix = new ParamHotFix();
paramHotFix.setPronunciation(pronunciationItems);
paramHotFix.setReplace(replaceItems);

SpeechSynthesisParam param = SpeechSynthesisParam.builder()
  .model("cosyvoice-v3-flash")
  .voice("longanhuan_v3.6") // 音色
  .hotFix(paramHotFix)
  .build();
```

## 核心接口

### `SpeechSynthesizer` 类

通过 `import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;` 导入。

| 接口/方法                                                                                                  | 参数                                                                                                                        | 返回值                               | 说明                                                                                                                                                                         |
| ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------- | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `public SpeechSynthesizer(SpeechSynthesisParam param, ResultCallback<SpeechSynthesisResult> callback)` | `param`：[请求参数](#请求参数)。`callback`：流式调用传 [ResultCallback](#resultcallback-接口)，非流式/Flowable 调用传 `null`。                      | `SpeechSynthesizer` 实例            | 构造函数。[单向流式](#单向流式调用)或[双向流式](#双向流式调用)调用时将 callback 设为 [ResultCallback](#resultcallback-接口)；[非流式](#非流式调用)或 [Flowable](#flowable-调用) 调用时设为 null。                              |
| `public ByteBuffer call(String text)`                                                                  | `text`：待合成文本（UTF-8）。                                                                                                      | `ByteBuffer` 或 `null`             | 将文本（纯文本或 [SSML](/developer-guides/speech/ssml)）转换为语音。未设置 callback 时：阻塞直到完成。设置了 callback 时：立即返回 null，结果通过 `onEvent` 返回。                                                     |
| `public void streamingCall(String text)`                                                               | `text`：待合成文本（UTF-8）。                                                                                                      | 无                                 | 发送文本进行流式合成。不支持 SSML。可多次调用以分段发送文本，结果通过 `onEvent` 返回。请参见[双向流式调用](#双向流式调用)。                                                                                                   |
| `public void streamingComplete() throws RuntimeException`                                              | 无                                                                                                                         | 无                                 | 结束流式合成。阻塞直到合成完成、会话中断或 10 分钟超时。请参见[双向流式调用](#双向流式调用)。                                                                                                                        |
| `public void streamingCancel()`                                                                        | 无                                                                                                                         | 无                                 | 取消当前轮次的双向流式语音合成任务。调用后 SDK 立即结束当前任务，可在当前连接上继续发起新的合成任务，无需重新初始化 `SpeechSynthesizer` 实例。需 Java SDK 版本不低于 2.22.26。Qwen-Audio-TTS 系列模型的所有模型都支持该功能，CosyVoice 系列模型仅 v2 及以上版本支持该功能。 |
| `public Flowable<SpeechSynthesisResult> callAsFlowable(String text)`                                   | `text`：待合成文本（UTF-8）。                                                                                                      | `Flowable<SpeechSynthesisResult>` | 将非流式文本输入转为流式语音输出。不支持 SSML。请参见 [Flowable 调用](#flowable-调用)。                                                                                                                 |
| `boolean getDuplexApi().close(int code, String reason)`                                                | code：WebSocket 关闭码。reason：关闭原因。请参见 [The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455#section-7.1.5)。 | true                              | 每次任务完成后关闭 WebSocket 连接以防止连接泄漏。连接复用请参见[高并发管理](/api-reference/more/connection-pooling)。                                                                                      |
| `public Flowable<SpeechSynthesisResult> streamingCallAsFlowable(Flowable<String> textStream)`          | `textStream`：封装待合成文本的 Flowable。                                                                                           | `Flowable<SpeechSynthesisResult>` | 将流式文本输入转为流式语音输出。不支持 SSML。请参见 [Flowable 调用](#flowable-调用)。                                                                                                                  |
| `public String getLastRequestId()`                                                                     | 无                                                                                                                         | 上一次任务的请求 ID。                      | 通过 `call`、`streamingCall`、`callAsFlowable` 或 `streamingCallAsFlowable` 启动新任务后获取请求 ID。                                                                                      |
| `public long getFirstPackageDelay()`                                                                   | 无                                                                                                                         | 首包延迟（毫秒）。                         | 获取从发送文本到收到首个音频包的时间。请在任务完成后调用。                                                                                                                                              |

<Warning>
  **使用须知**：

  - 每次调用 `call` 前需重新初始化 `SpeechSynthesizer` 实例。
  - [双向流式](#双向流式调用)调用时务必调用 `streamingComplete`，否则可能丢失合成语音。
</Warning>

**影响首包延迟的因素**：

- WebSocket 建连（首次调用）
- 音色加载时间（不同音色有差异）
- 服务负载（高峰时段排队）
- 网络延迟

**典型延迟**：

- 复用连接且音色已加载：约 500 ms
- 首次连接或切换音色：1,500-2,000 ms

如果延迟持续超过 2,000 ms：

1. 使用连接池预建连接（高并发场景）。
2. 检查网络质量。
3. 避开高峰时段。

### `ResultCallback` 接口

在[单向流式](#单向流式调用)或[双向流式](#双向流式调用)调用中通过 `ResultCallback` 获取合成结果。通过 `import com.alibaba.dashscope.common.ResultCallback;` 导入。

<Accordion title="点击查看示例">
  ```java
  ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
    @Override
    public void onEvent(SpeechSynthesisResult result) {
      System.out.println("Request ID: " + result.getRequestId());
      // 实时处理音频片段（如播放或写入缓冲区）。
    }

    @Override
    public void onComplete() {
      System.out.println("任务完成");
      // 处理合成完成逻辑（如释放播放器）。
    }

    @Override
    public void onError(Exception e) {
      System.out.println("任务失败：" + e.getMessage());
      // 处理异常（网络错误或服务端错误码）。
    }
  };
  ```
</Accordion>

| 接口/方法                                               | 参数                                 | 返回值 | 说明                                                                                               |
| --------------------------------------------------- | ---------------------------------- | --- | ------------------------------------------------------------------------------------------------ |
| `public void onEvent(SpeechSynthesisResult result)` | `result`：SpeechSynthesisResult 实例。 | 无   | 服务端推送音频数据时触发。通过 [SpeechSynthesisResult](#响应) 的 `getAudioFrame` 获取二进制音频，通过 `getUsage` 获取当前已计费字符数。 |
| `public void onComplete()`                          | 无                                  | 无   | 所有合成数据返回后触发。                                                                                     |
| `public void onError(Exception e)`                  | `e`：异常信息。                          | 无   | 发生异常时触发。请在此方法中实现异常日志记录和资源清理。                                                                     |

## 响应

服务端返回二进制音频数据：

- [非流式](#非流式调用)：处理 `call` 返回的 `ByteBuffer`。
- [单向流式](#单向流式调用)或[双向流式](#双向流式调用)：处理 `onEvent` 中的 `SpeechSynthesisResult` 参数。

`SpeechSynthesisResult` 核心接口：

| 接口/方法                                    | 参数 | 返回值                             | 说明                                                                                                                                                                                                                                                                                                                                                                 |
| ---------------------------------------- | -- | ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `public ByteBuffer getAudioFrame()`      | 无  | 二进制音频数据                         | 返回当前片段的二进制音频。如果没有新数据则可能为空。可将多个片段拼接为完整文件，也可使用流式播放器逐段播放。                                                                                                                                                                                                                                                                                                             |
| `public String getRequestId()`           | 无  | 请求 ID                           | 获取任务请求 ID。当 `getAudioFrame` 返回数据时，此方法返回 `null`。                                                                                                                                                                                                                                                                                                                    |
| `public SpeechSynthesisUsage getUsage()` | 无  | `SpeechSynthesisUsage` 或 `null` | 通过 `getCharacters()` 返回当前已计费字符数。以最后一次收到的值为准。                                                                                                                                                                                                                                                                                                                       |
| `public Sentence getTimestamp()`         | 无  | `Sentence` 或 `null`             | 当 `enableWordTimestamp` 为 true 时返回时间戳数据。`Sentence` 方法：`getBeginTime`（句子开始时间，ms）、`getEndTime`（句子结束时间，ms）、`getWords`（返回 `List<Word>`）。`Word` 方法：`getText`、`getBeginIndex`、`getEndIndex`、`getBeginTime`、`getEndTime`、`getPhonemes`（返回 `List<Phoneme>`，可能为空）。`Phoneme` 方法：`getBeginTime`、`getEndTime`、`getText`、`getTone`（音调：英文中 0/1/2 分别为轻音/重音/次重音；拼音中 1-5 分别为一声至轻声）。 |

<Warning>
  流式合成使用压缩格式（MP3、Opus）时，请使用流式播放器。逐帧播放会导致解码失败。

  常用的流式播放器包括 FFmpeg、PyAudio（Python）、AudioFormat（Java）和 MediaSource（JavaScript）。

  拼接音频为完整文件时，请使用追加模式写入。WAV 和 MP3 流式音频中，仅首帧包含头信息。
</Warning>

## 更多示例

更多示例请参见 [GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。
