> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Fun-ASR 实时语音识别 Java SDK

> 实时语音识别 Java SDK

**使用指南**： 模型概述和选型请参见[实时语音识别](/developer-guides/speech/asr-realtime)。

## 快速开始

[Recognition 类](#recognition-类)提供三种调用方式：

- **非流式调用**：一次性返回完整结果，适用于预录制音频。
- **双向流式调用**：边输入音频边实时返回结果，适用于麦克风采集或需要即时反馈的场景。

### 非流式调用

传入本地文件，同步获取转写结果。此调用会阻塞当前线程。

实例化 [Recognition 类](#recognition-类)，调用 `call` 方法并传入[请求参数](#请求参数)和音频文件。

<Accordion title="点击查看完整示例">
  ```java
  import com.alibaba.dashscope.audio.asr.recognition.Recognition;
  import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
  import com.alibaba.dashscope.utils.Constants;

  import java.io.File;

  public class Main {
    public static void main(String[] args) {
      Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
      // 创建 Recognition 实例
      Recognition recognizer = new Recognition();
      // 创建 RecognitionParam
      RecognitionParam param =
          RecognitionParam.builder()
              .model("qwen-audio-3.0-asr-flash-streaming")
              // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .format("wav")
              .sampleRate(16000)
              .parameter("language_hints", new String[]{"zh", "en"})
              .build();

      try {
        System.out.println("Recognition result: " + recognizer.call(param, new File("{YOUR_AUDIO_FILE}")));
      } catch (Exception e) {
        e.printStackTrace();
      } finally {
        // 任务完成后关闭 WebSocket 连接
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
</Accordion>

### 双向流式调用: 基于回调

通过实现回调接口实时接收识别结果。

<Steps>
  <Step title="启动流式识别">
    实例化 [Recognition 类](#recognition-类)，调用 `call` 方法并传入[请求参数](#请求参数)和[回调接口 (ResultCallback)](#回调接口-resultcallback)。
  </Step>

  <Step title="发送音频流">
    反复调用 `sendAudioFrame` 发送音频片段（来自文件或麦克风）。服务端通过 `onEvent` 回调返回识别结果。

    每次发送约 100 ms 时长的音频片段，大小为 1-16 KB。
  </Step>

  <Step title="结束识别">
    调用 `stop` 结束识别。此方法会阻塞直到 `onComplete` 或 `onError` 被调用。
  </Step>
</Steps>

<Accordion title="点击查看完整示例">
  <Tabs>
    <Tab title="从麦克风识别语音">
      ```java
      import com.alibaba.dashscope.audio.asr.recognition.Recognition;
      import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
      import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
      import com.alibaba.dashscope.common.ResultCallback;
      import com.alibaba.dashscope.utils.Constants;

      import javax.sound.sampled.AudioFormat;
      import javax.sound.sampled.AudioSystem;
      import javax.sound.sampled.TargetDataLine;

      import java.nio.ByteBuffer;
      import java.util.concurrent.ExecutorService;
      import java.util.concurrent.Executors;
      import java.util.concurrent.TimeUnit;

      public class Main {
        public static void main(String[] args) throws InterruptedException {
          Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
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
              .model("qwen-audio-3.0-asr-flash-streaming")
              // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .format("wav")
              .sampleRate(16000)
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

            @Override
            public void onComplete() {
              System.out.println("Recognition complete");
            }

            @Override
            public void onError(Exception e) {
              System.out.println("RecognitionCallback error: " + e.getMessage());
            }
          };
          try {
            recognizer.call(param, callback);
            // 创建音频格式
            AudioFormat audioFormat = new AudioFormat(16000, 16, 1, true, false);
            // 根据格式匹配默认录音设备
            TargetDataLine targetDataLine =
                AudioSystem.getTargetDataLine(audioFormat);
            targetDataLine.open(audioFormat);
            // 开始录音
            targetDataLine.start();
            ByteBuffer buffer = ByteBuffer.allocate(1024);
            long start = System.currentTimeMillis();
            // 录制 50 秒并实时转写
            while (System.currentTimeMillis() - start < 50000) {
              int read = targetDataLine.read(buffer.array(), 0, buffer.capacity());
              if (read > 0) {
                buffer.limit(read);
                // 将录制的音频数据发送给流式识别服务
                recognizer.sendAudioFrame(buffer);
                buffer = ByteBuffer.allocate(1024);
                // 录音速率有限，短暂休眠以避免 CPU 占用过高
                Thread.sleep(20);
              }
            }
            recognizer.stop();
          } catch (Exception e) {
            e.printStackTrace();
          } finally {
            // 任务完成后关闭 WebSocket 连接
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
    </Tab>

    <Tab title="识别本地音频文件">
      ```java
      import com.alibaba.dashscope.api.GeneralApi;
      import com.alibaba.dashscope.audio.asr.recognition.Recognition;
      import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
      import com.alibaba.dashscope.audio.asr.recognition.RecognitionResult;
      import com.alibaba.dashscope.base.HalfDuplexParamBase;
      import com.alibaba.dashscope.common.GeneralListParam;
      import com.alibaba.dashscope.common.ResultCallback;
      import com.alibaba.dashscope.protocol.GeneralServiceOption;
      import com.alibaba.dashscope.protocol.HttpMethod;
      import com.alibaba.dashscope.protocol.Protocol;
      import com.alibaba.dashscope.protocol.StreamingMode;
      import com.alibaba.dashscope.utils.Constants;

      import java.io.FileInputStream;
      import java.nio.ByteBuffer;
      import java.nio.file.Path;
      import java.nio.file.Paths;
      import java.time.LocalDateTime;
      import java.time.format.DateTimeFormatter;
      import java.util.concurrent.ExecutorService;
      import java.util.concurrent.Executors;
      import java.util.concurrent.TimeUnit;

      class TimeUtils {
        private static final DateTimeFormatter formatter =
            DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSS");

        public static String getTimestamp() {
          return LocalDateTime.now().format(formatter);
        }
      }

      public class Main {
        public static void main(String[] args) throws InterruptedException {
          Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
          // 在实际应用中，仅在程序启动时调用一次此方法
          warmUp();

          ExecutorService executorService = Executors.newSingleThreadExecutor();
          executorService.submit(new RealtimeRecognitionTask(Paths.get(System.getProperty("user.dir"), "{YOUR_AUDIO_FILE}")));
          executorService.shutdown();

          // 等待所有任务完成
          executorService.awaitTermination(1, TimeUnit.MINUTES);
          System.exit(0);
        }

        public static void warmUp() {
          try {
            // 轻量级 GET 请求，用于建立连接
            GeneralServiceOption warmupOption = GeneralServiceOption.builder()
                .protocol(Protocol.HTTP)
                .httpMethod(HttpMethod.GET)
                .streamingMode(StreamingMode.OUT)
                .path("assistants")
                .build();

            warmupOption.setBaseHttpUrl(Constants.baseHttpApiUrl);
            GeneralApi<HalfDuplexParamBase> api = new GeneralApi<>();
            api.get(GeneralListParam.builder().limit(1L).build(), warmupOption);
          } catch (Exception e) {
            // 预热失败时允许重试
          }
        }
      }

      class RealtimeRecognitionTask implements Runnable {
        private Path filepath;

        public RealtimeRecognitionTask(Path filepath) {
          this.filepath = filepath;
        }

        @Override
        public void run() {
          RecognitionParam param = RecognitionParam.builder()
              .model("qwen-audio-3.0-asr-flash-streaming")
              // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .format("wav")
              .sampleRate(16000)
              .build();
          Recognition recognizer = new Recognition();

          String threadName = Thread.currentThread().getName();

          ResultCallback<RecognitionResult> callback = new ResultCallback<RecognitionResult>() {
            @Override
            public void onEvent(RecognitionResult message) {
              if (message.isSentenceEnd()) {

                System.out.println(TimeUtils.getTimestamp()+" "+
                    "[process " + threadName + "] Final Result:" + message.getSentence().getText());
              } else {
                System.out.println(TimeUtils.getTimestamp()+" "+
                    "[process " + threadName + "] Intermediate Result: " + message.getSentence().getText());
              }
            }

            @Override
            public void onComplete() {
              System.out.println(TimeUtils.getTimestamp()+" "+"[" + threadName + "] Recognition complete");
            }

            @Override
            public void onError(Exception e) {
              System.out.println(TimeUtils.getTimestamp()+" "+
                  "[" + threadName + "] RecognitionCallback error: " + e.getMessage());
            }
          };

          try {
            recognizer.call(param, callback);
            // 请替换为您的音频文件路径
            System.out.println(TimeUtils.getTimestamp()+" "+"[" + threadName + "] Input file_path is: " + this.filepath);
            // 读取文件并分块发送音频
            FileInputStream fis = new FileInputStream(this.filepath.toFile());
            byte[] allData = new byte[fis.available()];
            int ret = fis.read(allData);
            fis.close();

            int sendFrameLength = 3200;
            for (int i = 0; i * sendFrameLength < allData.length; i ++) {
              int start = i * sendFrameLength;
              int end = Math.min(start + sendFrameLength, allData.length);
              ByteBuffer byteBuffer = ByteBuffer.wrap(allData, start, end - start);
              recognizer.sendAudioFrame(byteBuffer);
              Thread.sleep(100);
            }

            System.out.println(TimeUtils.getTimestamp()+" "+LocalDateTime.now());
            recognizer.stop();
          } catch (Exception e) {
            e.printStackTrace();
          } finally {
            // 任务完成后关闭 WebSocket 连接
            recognizer.getDuplexApi().close(1000, "bye");
          }

          System.out.println(
              "["
                  + threadName
                  + "][Metric] requestId: "
                  + recognizer.getLastRequestId()
                  + ", first package delay ms: "
                  + recognizer.getFirstPackageDelay()
                  + ", last package delay ms: "
                  + recognizer.getLastPackageDelay());
        }
      }
      ```
    </Tab>
  </Tabs>
</Accordion>

### 双向流式调用: 基于 Flowable

使用 Flowable 工作流实时接收识别结果。

Flowable 是 RxJava 提供的响应式流类型，支持背压机制。详见 [Flowable API 参考](http://reactivex.io/RxJava/2.x/javadoc/)。

<Accordion title="点击查看完整示例">
  调用 `streamCall` 启动识别，返回 `Flowable<RecognitionResult>`。使用 `blockingForEach` 或 `subscribe` 处理结果。

  `streamCall` 需要以下参数：

  - `RecognitionParam`：模型、采样率和音频格式
  - `Flowable<ByteBuffer>`：音频流

  ```java
  import com.alibaba.dashscope.audio.asr.recognition.Recognition;
  import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
  import com.alibaba.dashscope.exception.NoApiKeyException;
  import com.alibaba.dashscope.utils.Constants;
  import io.reactivex.BackpressureStrategy;
  import io.reactivex.Flowable;

  import javax.sound.sampled.AudioFormat;
  import javax.sound.sampled.AudioSystem;
  import javax.sound.sampled.TargetDataLine;
  import java.nio.ByteBuffer;

  public class Main {
    public static void main(String[] args) throws NoApiKeyException {
      Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
      // 创建 Flowable<ByteBuffer>
      Flowable<ByteBuffer> audioSource =
          Flowable.create(
              emitter -> {
                new Thread(
                    () -> {
                      try {
                        // 创建音频格式
                        AudioFormat audioFormat = new AudioFormat(16000, 16, 1, true, false);
                        // 根据格式匹配默认录音设备
                        TargetDataLine targetDataLine =
                            AudioSystem.getTargetDataLine(audioFormat);
                        targetDataLine.open(audioFormat);
                        // 开始录音
                        targetDataLine.start();
                        ByteBuffer buffer = ByteBuffer.allocate(1024);
                        long start = System.currentTimeMillis();
                        // 录制 50 秒并实时转写
                        while (System.currentTimeMillis() - start < 50000) {
                          int read = targetDataLine.read(buffer.array(), 0, buffer.capacity());
                          if (read > 0) {
                            buffer.limit(read);
                            // 将录制的音频数据发送给流式识别服务
                            emitter.onNext(buffer);
                            buffer = ByteBuffer.allocate(1024);
                            // 录音速率有限，短暂休眠以避免 CPU 占用过高
                            Thread.sleep(20);
                          }
                        }
                        // 通知转写完成
                        emitter.onComplete();
                      } catch (Exception e) {
                        emitter.onError(e);
                      }
                    })
                    .start();
              },
              BackpressureStrategy.BUFFER);

      // 创建 Recognition 实例
      Recognition recognizer = new Recognition();
      // 创建 RecognitionParam，通过 audioFrame 参数传入 Flowable<ByteBuffer>
      RecognitionParam param = RecognitionParam.builder()
          .model("qwen-audio-3.0-asr-flash-streaming")
          // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
          .apiKey(System.getenv("DASHSCOPE_API_KEY"))
          .format("pcm")
          .sampleRate(16000)
          .build();

      // 调用流式接口
      recognizer
          .streamCall(param, audioSource)
          .blockingForEach(
              result -> {
                // 订阅输出结果
                if (result.isSentenceEnd()) {
                  System.out.println("Final Result: " + result.getSentence().getText());
                } else {
                  System.out.println("Intermediate Result: " + result.getSentence().getText());
                }
              });
      // 任务完成后关闭 WebSocket 连接
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
</Accordion>

### 高并发调用

SDK 使用 OkHttp3 连接池来减少开销。详见[高并发管理](/api-reference/more/connection-pooling)。

## 请求参数

使用 `RecognitionParam` 的构建器方法配置模型、采样率和音频格式，然后将配置好的对象传给 `call` 或 `streamCall`。

<Accordion title="点击查看示例">
  ```java
  RecognitionParam param = RecognitionParam.builder()
    .model("qwen-audio-3.0-asr-flash-streaming")
    .format("pcm")
    .sampleRate(16000)
    .parameter("language_hints", new String[]{"zh", "en"})
    .build();
  ```
</Accordion>

| **参数**                           | **类型**    | **默认值** | **必选** | **说明**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| -------------------------------- | --------- | ------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| model                            | String    | -       | 是      | 用于实时语音识别的[支持的模型](/developer-guides/speech/speech-to-text-models)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| sampleRate                       | Integer   | -       | 是      | 音频采样率，单位 Hz。fun-asr-realtime 支持 16000 Hz。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| format                           | String    | -       | 是      | 音频格式。支持：pcm、wav、mp3、opus、speex、aac、amr。 <br /> **注意**： opus/speex 必须使用 Ogg 封装。wav 必须为 PCM 编码。amr 仅支持 AMR-NB。                                                                                                                                                                                                                                                                                                                                                                                                                          |
| vocabularyId                     | String    | -       | 否      | 自定义词表 ID。参见[自定义热词](/developer-guides/speech/improve-recognition-accuracy)。默认不设置。                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| semantic\_punctuation\_enabled   | boolean   | false   | 否      | 标点模式。`true`：语义标点（精度更高，适用于会议场景）。`false`（默认）：VAD 标点（延迟更低，适用于交互场景）。                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| max\_sentence\_silence           | Integer   | 1300    | 否      | VAD 断句静音阈值，单位毫秒。语音后的静音时长超过此值时断句。当 `semantic_punctuation_enabled` 为 `true` 时，该参数不作为返回 `sentence_end` 的判定依据，但设置过低可能影响识别效果。取值范围：\[200, 6000]。                                                                                                                                                                                                                                                                                                                                                                                            |
| multi\_threshold\_mode\_enabled  | boolean   | false   | 否      | 防止 VAD 过早切分长句。仅在 `semantic_punctuation_enabled` 为 `false` 时生效。                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| punctuation\_prediction\_enabled | boolean   | true    | 否      | 自动为识别结果添加标点符号，固定为 true，不支持修改。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| heartbeat                        | boolean   | false   | 否      | 是否启用心跳包。`true`：在持续发送静音音频的情况下，可保持与服务端的连接不中断。`false`（默认）：即使持续发送静音音频，连接也将在一定时间后因超时而断开。 <br /> <Note>需要 SDK 2.19.1 或更高版本。</Note>                                                                                                                                                                                                                                                                                                                                                                                                          |
| language\_hints                  | String\[] | -       | 否      | 识别语言代码。不设置则自动检测。支持的语言代码：<ul><li>fun-asr-realtime、fun-asr-realtime-2025-11-07：zh（中文）、en（英文）、ja（日语）、ko（韩语）、vi（越南语）、th（泰语）、id（印尼语）、ms（马来语）、tl（菲律宾语）、hi（印地语）、ar（阿拉伯语）、fr（法语）、de（德语）、es（西班牙语）、pt（葡萄牙语）、ru（俄语）、it（意大利语）、nl（荷兰语）、sv（瑞典语）、da（丹麦语）、fi（芬兰语）、no（挪威语）、el（希腊语）、pl（波兰语）、cs（捷克语）、hu（匈牙利语）、ro（罗马尼亚语）、bg（保加利亚语）、hr（克罗地亚语）、sk（斯洛伐克语）</li><li>fun-asr-realtime-2026-02-28：zh（中文）、en（英文）、ja（日语）</li><li>fun-asr-realtime-2025-09-15：zh（中文）、en（英文）</li><li>fun-asr-flash-8k-realtime、fun-asr-flash-8k-realtime-2026-01-28：zh（中文）</li></ul> |
| speech\_noise\_threshold         | float     | -       | 否      | VAD 灵敏度。取值范围：\[-1.0, 1.0]。接近 -1：更多噪音被识别为语音。接近 +1：部分语音被过滤为噪音。 <br /> **注意**： 高级参数，调整会显著影响识别质量。请充分测试，并根据音频环境小幅调整（步长 0.1）。                                                                                                                                                                                                                                                                                                                                                                                                               |
| special\_word\_filter            | String    | -       | 否      | 敏感词过滤配置，仅 Fun-ASR 支持。最多支持设置 32 个敏感词。参见[敏感词过滤](#敏感词过滤)。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| apiKey                           | String    | -       | 否      | 您的 API Key。                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| input                            | Map       | -       | 否      | 输入对象，用于传入对话上下文（context）。上下文用于辅助识别、提升专有词汇的识别准确率。使用方法详见[提升识别准确率](/developer-guides/speech/improve-recognition-accuracy)。仅 `fun-asr-realtime` 和 `fun-asr-realtime-2025-11-07` 模型支持。                                                                                                                                                                                                                                                                                                                                                      |

<Warning>
  - 上下文消息（`input_text` 和 `text` 类型）各最多 5 条，超出时保留最近的 5 条。
  - 每轮上下文文本总长度不超过 400 个字符，超出部分从末尾截断。
  - 上下文消息必须按对话轮次排列，每轮中 `user`（`input_text` 类型）必须在对应的 `assistant`（`text` 类型）之前。
</Warning>

`input` 通过 `RecognitionParam` 的 `parameter` 方法传入：

```java
Map<String, Object> userContent = new HashMap<>();
userContent.put("type", "input_text");
userContent.put("text", "你好啊");

Map<String, Object> userMessage = new HashMap<>();
userMessage.put("role", "user");
userMessage.put("content", Collections.singletonList(userContent));

Map<String, Object> assistantContent = new HashMap<>();
assistantContent.put("type", "text");
assistantContent.put("text", "你好啊，我是通义千问，有什么可以帮助你的？");

Map<String, Object> assistantMessage = new HashMap<>();
assistantMessage.put("role", "assistant");
assistantMessage.put("content", Collections.singletonList(assistantContent));

List<Map<String, Object>> context = Arrays.asList(userMessage, assistantMessage);
Map<String, Object> input = new HashMap<>();
input.put("context", context);

RecognitionParam param = RecognitionParam.builder()
  .model("qwen-audio-3.0-asr-flash-streaming")
  .format("pcm")
  .sampleRate(16000)
  .parameter("input", input)
  .build();
```

<Note>
  对于 `RecognitionParam` 构建器中未直接提供的参数（如 `semantic_punctuation_enabled`、`heartbeat` 和 `language_hints`），请使用 `parameter` 或 `parameters` 方法：

  <Tabs>
    <Tab title="使用 parameter 方法设置">
      ```java
      RecognitionParam param = RecognitionParam.builder()
        .model("qwen-audio-3.0-asr-flash-streaming")
        .format("pcm")
        .sampleRate(16000)
        .parameter("semantic_punctuation_enabled", true)
        .build();
      ```
    </Tab>

    <Tab title="使用 parameters 方法设置">
      ```java
      RecognitionParam param = RecognitionParam.builder()
        .model("qwen-audio-3.0-asr-flash-streaming")
        .format("pcm")
        .sampleRate(16000)
        .parameters(Collections.singletonMap("semantic_punctuation_enabled", true))
        .build();
      ```
    </Tab>
  </Tabs>
</Note>

<a id="敏感词过滤" />

### 敏感词过滤

敏感词过滤可对识别结果中的敏感词执行替换或移除，适用于客服质检、内容合规、字幕审核等场景。仅 Fun-ASR 支持，最多支持设置 32 个敏感词。未传入 `special_word_filter` 参数时，不会对敏感词进行过滤。

`special_word_filter` 为 JSON 对象，包含三个子字段：

- `filter_with_signed.word_list`：字符串数组，列出需要被替换为等长 `*` 的敏感词。例如 `["测试"]`，"帮我测试一下"会变成"帮我\*\*一下"。
- `filter_with_empty.word_list`：字符串数组，列出需要从结果中完全移除的敏感词。例如 `["开始"]`，"比赛这就要开始了吗"会变成"比赛这就要了吗"。
- `system_reserved_filter`：布尔值，默认 `false`。是否启用敏感词过滤功能。

<Tabs>
  <Tab title="使用 parameter 方法设置">
    ```java
    JSONObject root = new JSONObject();
    root.put("system_reserved_filter", true);

    JSONObject root1 = new JSONObject();
    JSONArray array1 = new JSONArray();
    array1.put("开始");
    array1.put("进行");
    root1.put("word_list", array1);

    JSONObject root2 = new JSONObject();
    JSONArray array2 = new JSONArray();
    array2.put("测试");
    root2.put("word_list", array2);

    root.put("filter_with_empty", root1);
    root.put("filter_with_signed", root2);

    RecognitionParam param = RecognitionParam.builder()
      .model("qwen-audio-3.0-asr-flash-streaming")
      .format("pcm")
      .sampleRate(16000)
      .parameter("special_word_filter", root.toString())
      .build();
    ```
  </Tab>

  <Tab title="使用 parameters 方法设置">
    ```java
    JSONObject root = new JSONObject();
    root.put("system_reserved_filter", true);

    JSONObject root1 = new JSONObject();
    JSONArray array1 = new JSONArray();
    array1.put("开始");
    array1.put("进行");
    root1.put("word_list", array1);

    JSONObject root2 = new JSONObject();
    JSONArray array2 = new JSONArray();
    array2.put("测试");
    root2.put("word_list", array2);

    root.put("filter_with_empty", root1);
    root.put("filter_with_signed", root2);

    RecognitionParam param = RecognitionParam.builder()
      .model("qwen-audio-3.0-asr-flash-streaming")
      .format("pcm")
      .sampleRate(16000)
      .parameters(Collections.singletonMap("special_word_filter", root.toString()))
      .build();
    ```
  </Tab>
</Tabs>

## 核心接口

### `Recognition` 类

导入：`import com.alibaba.dashscope.audio.asr.recognition.Recognition;`

| **接口/方法**                                                                                                | **参数**                                                                                                                                     | **返回值**                       | **说明**                                                                                                                                   |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| `public void call(RecognitionParam param, final ResultCallback<RecognitionResult> callback)`             | `param`：[请求参数](#请求参数) <br /> `callback`：[回调接口 (ResultCallback)](#回调接口-resultcallback)                                                      | 无                             | 基于回调的流式识别，不阻塞当前线程。                                                                                                                       |
| `public String call(RecognitionParam param, File file)`                                                  | `param`：[请求参数](#请求参数) <br /> `file`：待识别的音频文件                                                                                               | 识别结果                          | 非流式调用，传入本地文件。阻塞直到处理完成。文件必须可读。                                                                                                            |
| `public Flowable<RecognitionResult> streamCall(RecognitionParam param, Flowable<ByteBuffer> audioFrame)` | `param`：[请求参数](#请求参数) <br /> `audioFrame`：`Flowable<ByteBuffer>` 实例                                                                        | `Flowable<RecognitionResult>` | 基于 Flowable 的流式识别。                                                                                                                       |
| `public void sendAudioFrame(ByteBuffer audioFrame)`                                                      | `audioFrame`：二进制音频流 (`ByteBuffer`)                                                                                                         | 无                             | 发送一个音频片段。每个数据包约 100 ms 时长，大小 1-16 KB。结果通过 [ResultCallback](#回调接口-resultcallback) 的 `onEvent` 方法返回。                                       |
| `public void stop()`                                                                                     | 无                                                                                                                                          | 无                             | 停止识别。阻塞直到 `onComplete` 或 `onError` 被调用。                                                                                                  |
| `boolean getDuplexApi().close(int code, String reason)`                                                  | `code`：WebSocket 关闭码 <br /> `reason`：关闭原因 <br /> 参见 [The WebSocket Protocol](https://datatracker.ietf.org/doc/html/rfc6455#section-7.1.5)。 | `true`                        | 每个任务完成后关闭 WebSocket 连接以防止泄漏（异常情况下也需关闭）。先通过 `getDuplexApi()` 获取连接对象后调用 `close`。如需复用连接，请参见[高并发管理](/api-reference/more/connection-pooling)。 |
| `public String getLastRequestId()`                                                                       | 无                                                                                                                                          | requestId                     | 获取当前任务的请求 ID。需在 `call` 或 `streamCall` 启动任务后调用。 <br /> <Note>需要 SDK 2.18.0 或更高版本。</Note>                                                  |
| `public long getFirstPackageDelay()`                                                                     | 无                                                                                                                                          | 首包延迟                          | 获取从发送第一个音频包到收到第一个结果的延迟。需在任务完成后调用。 <br /> <Note>需要 SDK 2.18.0 或更高版本。</Note>                                                               |
| `public long getLastPackageDelay()`                                                                      | 无                                                                                                                                          | 尾包延迟                          | 获取从发送 `stop` 到最后一个结果返回的时间。需在任务完成后调用。 <br /> <Note>需要 SDK 2.18.0 或更高版本。</Note>                                                            |

### 回调接口 (`ResultCallback`)

在[双向流式调用](#双向流式调用-基于回调)中，实现回调方法来处理服务端返回的结果。

继承 `ResultCallback<RecognitionResult>` 并实现其方法。`RecognitionResult` 封装了服务端响应。

SDK 支持连接复用，因此没有 `onClose` 或 `onOpen` 方法。

<Accordion title="示例" defaultOpen>
  ```java
  ResultCallback<RecognitionResult> callback = new ResultCallback<RecognitionResult>() {
    @Override
    public void onEvent(RecognitionResult result) {
      System.out.println("RequestId is: " + result.getRequestId());
      // 在此处实现语音识别结果的处理逻辑
    }

    @Override
    public void onComplete() {
      System.out.println("Task complete");
    }

    @Override
    public void onError(Exception e) {
      System.out.println("Task failed: " + e.getMessage());
    }
  };
  ```
</Accordion>

| **接口/方法**                                       | **参数**                                                           | **返回值** | **说明**      |
| ----------------------------------------------- | ---------------------------------------------------------------- | ------- | ----------- |
| `public void onEvent(RecognitionResult result)` | `result`：[实时识别结果 (RecognitionResult)](#实时识别结果-recognitionresult) | 无       | 服务端返回结果时调用。 |
| `public void onComplete()`                      | 无                                                                | 无       | 识别成功完成时调用。  |
| `public void onError(Exception e)`              | `e`：异常信息                                                         | 无       | 发生错误时调用。    |

## 响应结果

### 实时识别结果 (`RecognitionResult`)

`RecognitionResult` 表示单条识别结果。

| **接口/方法**                        | **参数** | **返回值**                    | **说明**             |
| -------------------------------- | ------ | -------------------------- | ------------------ |
| `public String getRequestId()`   | 无      | requestId                  | 获取请求 ID。           |
| `public boolean isSentenceEnd()` | 无      | 句子是否结束                     | 返回当前句子是否已结束（最终结果）。 |
| `public Sentence getSentence()`  | 无      | [Sentence](#句子信息-sentence) | 获取包含时间戳和文本的句子信息。   |

### 句子信息 (`Sentence`)

| **接口/方法**                      | **参数** | **返回值**                          | **说明**     |
| ------------------------------ | ------ | -------------------------------- | ---------- |
| `public Long getBeginTime()`   | 无      | 句子开始时间，单位毫秒                      | 返回句子的开始时间。 |
| `public Long getEndTime()`     | 无      | 句子结束时间，单位毫秒                      | 返回句子的结束时间。 |
| `public String getText()`      | 无      | 识别文本                             | 返回识别出的文本。  |
| `public List<Word> getWords()` | 无      | [词时间戳信息 (Word)](#词时间戳信息-word) 列表 | 返回词级时间戳信息。 |

### 词时间戳信息 (`Word`)

| **接口/方法**                        | **参数** | **返回值**    | **说明**    |
| -------------------------------- | ------ | ---------- | --------- |
| `public long getBeginTime()`     | 无      | 词开始时间，单位毫秒 | 返回词的开始时间。 |
| `public long getEndTime()`       | 无      | 词结束时间，单位毫秒 | 返回词的结束时间。 |
| `public String getText()`        | 无      | 词          | 返回识别出的词。  |
| `public String getPunctuation()` | 无      | 标点         | 返回标点符号。   |
