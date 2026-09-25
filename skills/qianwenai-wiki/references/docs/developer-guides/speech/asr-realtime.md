> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音识别

> 将连续音频流实时转写为文字

实时语音识别服务接收音频流并实时转写为带标点的文本，适用于直播字幕、在线会议、语音聊天、智能助手等场景。

## 概述

实现低延迟音频到文本转换。

- 支持普通话及粤语、四川话等多种方言的高精度语音识别
- 具备应对复杂声学环境的能力，支持自动语种检测与智能非人声过滤
- 支持惊讶、平静、愉快、悲伤、厌恶、愤怒、恐惧等多种情绪状态识别
- 支持热词定制，可提升特定词汇的识别准确率
- 支持上下文增强，通过配置上下文提高识别准确率
- 支持时间戳输出，生成结构化识别结果
- 灵活采样率与多种音频格式，适配不同录音环境

批量场景（会议转写、通话分析、字幕生成等）可使用[非实时语音识别](/developer-guides/speech/asr)。各模型选型建议请参见[语音识别模型](/developer-guides/speech/speech-to-text-models)。

<Tip>
  模型可用性、支持语言和功能对比，请参见[语音转文字模型](/developer-guides/speech/speech-to-text-models)。
</Tip>

## 快速开始

<Tabs>
  <Tab title="Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime">
    更多代码示例，请参见 [GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

    [获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装](/api-reference/preparation/install-sdk)。如果通过 AOQ 协议接入 Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime，需要下载并集成 AOQ 客户端 SDK，详见 [AOQ SDK 简介](/developer-guides/realtime-api/aoq-sdk-intro)。

    该模型除 WebSocket 协议外，还支持通过 AOQ 协议接入；如果是客户端对接，且更看重稳定的延迟、弱网下的交互能力、实时双工的降噪与回声消除，可优先考虑 AOQ，协议对比与选型请参见[模型/应用支持力度](/developer-guides/realtime-api/overview#模型支持力度)。

    ### 模型可用性

    <Note>
      以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
    </Note>

| **模型**                                                   | **版本** | **单价**     | **免费额度** [(说明)](/resources/free-quota) |
| -------------------------------------------------------- | ------ | ---------- | -------------------------------------- |
| fun-asr-realtime <br /> 当前版本：fun-asr-realtime-2025-11-07 | 稳定版    | 0.00033元/秒 | 36,000 秒（10 小时）<br /> 有效期 90 天         |
| fun-asr-realtime-2025-11-07                              | 快照版    | 0.00033元/秒 | 36,000 秒（10 小时）<br /> 有效期 90 天         |

    - **支持语言**：普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语，以及中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等地区的普通话口音——涵盖河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地。同时支持英语和日语。
    - **采样率**：16 kHz
    - **音频格式**：pcm、wav、mp3、opus、speex、aac、amr

    ### 从麦克风实时识别

    从麦克风采集音频并实时输出识别结果。

    <CodeGroup>
      ```java Java
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
              // 如果未配置环境变量，请将下一行替换为您的 API Key：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .format("pcm")
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
                // 将录制的音频数据发送至流式识别服务
                recognizer.sendAudioFrame(buffer);
                buffer = ByteBuffer.allocate(1024);
                // 限制录音速率，短暂休眠以防止 CPU 占用过高
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

      ```python Python
      import os
      import signal  # 用于处理键盘事件（按 Ctrl+C 停止录音）
      import sys

      import dashscope
      import pyaudio
      from dashscope.audio.asr import *

      mic = None
      stream = None

      # 设置录音参数
      sample_rate = 16000  # 采样率（Hz）
      channels = 1  # 单声道
      dtype = 'int16'  # 数据类型
      format_pcm = 'pcm'  # 音频数据格式
      block_size = 3200  # 每个缓冲区的帧数

      # 实时语音识别回调
      class Callback(RecognitionCallback):
        def on_open(self) -> None:
          global mic
          global stream
          print('RecognitionCallback open.')
          mic = pyaudio.PyAudio()
          stream = mic.open(format=pyaudio.paInt16,
                                channels=1,
                                rate=16000,
                                input=True)

        def on_close(self) -> None:
          global mic
          global stream
          print('RecognitionCallback close.')
          stream.stop_stream()
          stream.close()
          mic.terminate()
          stream = None
          mic = None

        def on_complete(self) -> None:
          print('RecognitionCallback completed.')  # 识别完成

        def on_error(self, message) -> None:
          print('RecognitionCallback task_id: ', message.request_id)
          print('RecognitionCallback error: ', message.message)
          # 如果音频流正在运行则停止并关闭
          if 'stream' in globals() and stream.active:
            stream.stop()
            stream.close()
          # 强制退出程序
          sys.exit(1)

        def on_event(self, result: RecognitionResult) -> None:
          sentence = result.get_sentence()
          if 'text' in sentence:
            print('RecognitionCallback text: ', sentence['text'])
            if RecognitionResult.is_sentence_end(sentence):
              print(
                'RecognitionCallback sentence end, request_id:%s, usage:%s'
                % (result.get_request_id(), result.get_usage(sentence)))

      def signal_handler(sig, frame):
        print('Ctrl+C pressed, stop recognition ...')
        # 停止识别
        recognition.stop()
        print('Recognition stopped.')
        print(
          '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
          .format(
            recognition.get_last_request_id(),
            recognition.get_first_package_delay(),
            recognition.get_last_package_delay(),
          ))
        # 强制退出程序
        sys.exit(0)

      # 主函数
      if __name__ == '__main__':
        # 如果未配置环境变量，请将下一行替换为您的 API Key：dashscope.api_key = "sk-xxx"
        dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

        dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

        # 创建识别回调
        callback = Callback()

        # 以异步模式调用识别服务，可自定义识别参数，如 model、format、sample_rate 等
        recognition = Recognition(
          model='qwen-audio-3.0-asr-flash-streaming',
          format=format_pcm,
          # 支持 'pcm'、'wav'、'opus'、'speex'、'aac'、'amr'，详见文档
          sample_rate=sample_rate,
          # 支持 8000、16000
          semantic_punctuation_enabled=False,
          callback=callback)

        # 开始识别
        recognition.start()

        signal.signal(signal.SIGINT, signal_handler)
        print("Press 'Ctrl+C' to stop recording and recognition...")
        # 创建键盘监听，直到按下 Ctrl+C

        while True:
          if stream:
            data = stream.read(3200, exception_on_overflow=False)
            recognition.send_audio_frame(data)
          else:
            break

        recognition.stop()
      ```
    </CodeGroup>

    <Note>
      运行 Python 示例前，请先执行 `pip install pyaudio` 安装第三方音频播放和采集套件。pyaudio 依赖 portaudio 库：Ubuntu/Debian 执行 `sudo apt-get install libportaudio2 portaudio19-dev`，macOS 执行 `brew install portaudio`。
    </Note>

    ### 识别本地音频文件

    该功能用于识别并转写本地音频文件，适合需要近实时处理短音频的场景，如语音聊天、语音指令、语音输入和语音搜索。

    <Note>
      以下示例使用的音频文件为 [asr\_example.wav](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250805/nzeaaw/asr_example.wav)。
    </Note>

    <CodeGroup>
      ```java Java
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
          executorService.submit(new RealtimeRecognitionTask(Paths.get(System.getProperty("user.dir"), "asr_example.wav")));
          executorService.shutdown();

          // 等待所有任务完成
          executorService.awaitTermination(1, TimeUnit.MINUTES);
          System.exit(0);
        }

        public static void warmUp() {
          try {
            // 使用轻量级 GET 请求预建连接
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
              // 如果未配置环境变量，请将下一行替换为您的 API Key：.apiKey("sk-xxx")
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
            // 请将路径替换为您的音频文件路径
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

      ```python Python
      import os
      import time
      import dashscope
      from dashscope.audio.asr import *

      # 如果未设置环境变量，请将下一行替换为您的 API Key：dashscope.api_key = "sk-xxx"
      dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

      dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

      from datetime import datetime

      def get_timestamp():
        now = datetime.now()
        formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
        return formatted_timestamp

      class Callback(RecognitionCallback):
        def on_complete(self) -> None:
          print(get_timestamp() + ' Recognition completed')  # 识别完成

        def on_error(self, result: RecognitionResult) -> None:
          print('Recognition task_id: ', result.request_id)
          print('Recognition error: ', result.message)
          exit(0)

        def on_event(self, result: RecognitionResult) -> None:
          sentence = result.get_sentence()
          if 'text' in sentence:
            print(get_timestamp() + ' RecognitionCallback text: ', sentence['text'])
          if RecognitionResult.is_sentence_end(sentence):
            print(get_timestamp() +
                        'RecognitionCallback sentence end, request_id:%s, usage:%s'
                        % (result.get_request_id(), result.get_usage(sentence)))

      callback = Callback()

      recognition = Recognition(model='qwen-audio-3.0-asr-flash-streaming',
                                format='wav',
                                sample_rate=16000,
                                callback=callback)

      try:
        audio_data: bytes = None
        f = open("asr_example.wav", 'rb')
        if os.path.getsize("asr_example.wav"):
          # 将整个文件读入缓冲区
          file_buffer = f.read()
          f.close()
          print("Start Recognition")
          recognition.start()

          # 以 3200 字节为单位分块发送数据
          buffer_size = len(file_buffer)
          offset = 0
          chunk_size = 3200

          while offset < buffer_size:
            # 计算当前块的大小
            remaining_bytes = buffer_size - offset
            current_chunk_size = min(chunk_size, remaining_bytes)

            # 从缓冲区提取当前块
            audio_data = file_buffer[offset:offset + current_chunk_size]

            # 发送音频帧
            recognition.send_audio_frame(audio_data)
            # 更新偏移量
            offset += current_chunk_size

            # 添加延迟以模拟实时传输
            time.sleep(0.1)

          recognition.stop()
        else:
          raise Exception(
            'The supplied file was empty (zero bytes long)')
      except Exception as e:
        raise e

      print(
        '[Metric] requestId: {}, first package delay ms: {}, last package delay ms: {}'
        .format(
          recognition.get_last_request_id(),
          recognition.get_first_package_delay(),
          recognition.get_last_package_delay(),
        ))
      ```
    </CodeGroup>

    #### WebSocket API

    以下示例演示如何通过原生 WebSocket 连接发送本地音频文件并获取识别结果。

    <Note>
      以下示例使用的音频文件为 [asr\_example.wav](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241114/mgiguo/asr_example.wav)。
    </Note>

    **安装依赖**

    <CodeGroup>
      ```bash Python
      pip uninstall websocket-client
      pip uninstall websocket
      pip install websocket-client
      ```

      ```xml Maven
      <dependency>
        <groupId>org.java-websocket</groupId>
        <artifactId>Java-WebSocket</artifactId>
        <version>1.5.6</version>
      </dependency>
      <dependency>
        <groupId>org.json</groupId>
        <artifactId>json</artifactId>
        <version>20240303</version>
      </dependency>
      ```

      ```gradle Gradle
      implementation 'org.java-websocket:Java-WebSocket:1.5.6'
      implementation 'org.json:json:20240303'
      ```
    </CodeGroup>

    <Warning>
      请勿将示例代码文件命名为 `websocket.py`，否则可能出现以下错误：`AttributeError: module 'websocket' has no attribute 'WebSocketApp'. Did you mean: 'WebSocket'?`
    </Warning>

    <CodeGroup>
      ```python Python
      # pip install websocket-client
      import os
      import json
      import time
      import uuid
      import threading
      import websocket

      # 若没有配置环境变量，请用 API Key 将下行替换为：api_key = "sk-xxx"
      api_key = os.environ.get('DASHSCOPE_API_KEY')
      url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'
      audio_file = 'asr_example.wav'  # 替换为您的音频文件路径

      TASK_ID = uuid.uuid4().hex[:32]
      task_started = False

      def send_run_task(ws):
        run_task_message = {
          'header': {
            'action': 'run-task',
            'task_id': TASK_ID,
            'streaming': 'duplex'
          },
          'payload': {
            'task_group': 'audio',
            'task': 'asr',
            'function': 'recognition',
            'model': 'qwen-audio-3.0-asr-flash-streaming',
            'parameters': {
              'sample_rate': 16000,
              'format': 'wav'
            },
            'input': {}
          }
        }
        ws.send(json.dumps(run_task_message))

      def send_finish_task(ws):
        finish_task_message = {
          'header': {
            'action': 'finish-task',
            'task_id': TASK_ID,
            'streaming': 'duplex'
          },
          'payload': {
            'input': {}
          }
        }
        ws.send(json.dumps(finish_task_message))

      def send_audio_stream(ws):
        chunk_size = 3200  # 100ms @ 16kHz 16bit 单声道
        try:
          with open(audio_file, 'rb') as f:
            while True:
              chunk = f.read(chunk_size)
              if not chunk:
                break
              ws.send(chunk, opcode=websocket.ABNF.OPCODE_BINARY)
              time.sleep(0.1)
          print('音频流结束')
          send_finish_task(ws)
        except Exception as e:
          print('读取音频文件错误：', e)
          ws.close()

      def on_open(ws):
        print('连接到服务器')
        send_run_task(ws)

      def on_message(ws, data):
        global task_started
        message = json.loads(data)
        event = message['header']['event']
        if event == 'task-started':
          print('任务开始')
          task_started = True
          threading.Thread(target=send_audio_stream, args=(ws,), daemon=True).start()
        elif event == 'result-generated':
          print('识别结果：', message['payload']['output']['sentence']['text'])
          if message['payload'].get('usage'):
            print('任务计费时长（秒）：', message['payload']['usage']['duration'])
        elif event == 'task-finished':
          print('任务完成')
          ws.close()
        elif event == 'task-failed':
          print('任务失败：', message['header'].get('error_message'))
          ws.close()
        else:
          print('未知事件：', event)

      def on_close(ws, close_status_code, close_msg):
        if not task_started:
          print('任务未启动，关闭连接')

      def on_error(ws, error):
        print('WebSocket错误：', error)

      if __name__ == '__main__':
        ws = websocket.WebSocketApp(
          url,
          header={'Authorization': f'bearer {api_key}'},
          on_open=on_open,
          on_message=on_message,
          on_error=on_error,
          on_close=on_close
        )
        ws.run_forever()
      ```

      ```java Java
      import org.java_websocket.client.WebSocketClient;
      import org.java_websocket.handshake.ServerHandshake;
      import org.json.JSONObject;
      import java.net.URI;
      import java.nio.ByteBuffer;
      import java.nio.file.Files;
      import java.nio.file.Paths;
      import java.util.UUID;
      import java.util.concurrent.atomic.AtomicBoolean;

      public class FunASRRealtimeClient {
          // 若没有配置环境变量，请用 API Key 将下行替换为：private static final String API_KEY = "sk-xxx";
          private static final String API_KEY = System.getenv().getOrDefault("DASHSCOPE_API_KEY", "sk-xxx");
          private static final String URL = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
          private static final String AUDIO_FILE = "asr_example.wav";
          private static final String MODEL = "qwen-audio-3.0-asr-flash-streaming";
          private static final String TASK_ID = UUID.randomUUID().toString().replace("-", "").substring(0, 32);
          private static final AtomicBoolean taskStarted = new AtomicBoolean(false);
          private static WebSocketClient client;

          public static void main(String[] args) throws Exception {
              client = new WebSocketClient(new URI(URL)) {
                  @Override
                  public void onOpen(ServerHandshake handshake) {
                      System.out.println("连接到服务器");
                      sendRunTask();
                  }
                  @Override
                  public void onMessage(String data) {
                      JSONObject message = new JSONObject(data);
                      String event = message.getJSONObject("header").getString("event");
                      switch (event) {
                          case "task-started":
                              System.out.println("任务开始");
                              taskStarted.set(true);
                              new Thread(FunASRRealtimeClient::sendAudioStream).start();
                              break;
                          case "result-generated":
                              JSONObject payload = message.getJSONObject("payload");
                              String text = payload.getJSONObject("output").getJSONObject("sentence").getString("text");
                              System.out.println("识别结果：" + text);
                              if (payload.has("usage")) {
                                  System.out.println("任务计费时长（秒）：" + payload.getJSONObject("usage").get("duration"));
                              }
                              break;
                          case "task-finished":
                              System.out.println("任务完成");
                              close();
                              break;
                          case "task-failed":
                              String errMsg = message.getJSONObject("header").optString("error_message");
                              System.err.println("任务失败：" + errMsg);
                              close();
                              break;
                          default:
                              System.out.println("未知事件：" + event);
                      }
                  }
                  @Override
                  public void onClose(int code, String reason, boolean remote) {
                      if (!taskStarted.get()) {
                          System.err.println("任务未启动，关闭连接");
                      }
                  }
                  @Override
                  public void onError(Exception ex) {
                      System.err.println("WebSocket错误：" + ex.getMessage());
                  }
              };
              client.addHeader("Authorization", "bearer " + API_KEY);
              client.connectBlocking();
          }

          private static void sendRunTask() {
              JSONObject runTask = new JSONObject()
                      .put("header", new JSONObject()
                              .put("action", "run-task")
                              .put("task_id", TASK_ID)
                              .put("streaming", "duplex"))
                      .put("payload", new JSONObject()
                              .put("task_group", "audio")
                              .put("task", "asr")
                              .put("function", "recognition")
                              .put("model", MODEL)
                              .put("parameters", new JSONObject()
                                      .put("sample_rate", 16000)
                                      .put("format", "wav"))
                              .put("input", new JSONObject()));
              client.send(runTask.toString());
          }

          private static void sendAudioStream() {
              int chunkSize = 3200;
              try {
                  byte[] audio = Files.readAllBytes(Paths.get(AUDIO_FILE));
                  int offset = 0;
                  while (offset < audio.length) {
                      int end = Math.min(offset + chunkSize, audio.length);
                      byte[] chunk = new byte[end - offset];
                      System.arraycopy(audio, offset, chunk, 0, end - offset);
                      client.send(ByteBuffer.wrap(chunk));
                      offset = end;
                      Thread.sleep(100);
                  }
                  System.out.println("音频流结束");
                  sendFinishTask();
              } catch (Exception e) {
                  System.err.println("读取音频文件错误：" + e.getMessage());
                  client.close();
              }
          }

          private static void sendFinishTask() {
              JSONObject finishTask = new JSONObject()
                      .put("header", new JSONObject()
                              .put("action", "finish-task")
                              .put("task_id", TASK_ID)
                              .put("streaming", "duplex"))
                      .put("payload", new JSONObject()
                              .put("input", new JSONObject()));
              client.send(finishTask.toString());
          }
      }
      ```
    </CodeGroup>
  </Tab>

  <Tab title="Qwen3-ASR-Flash-Realtime">
    <Tabs>
      <Tab title="DashScope SDK">
        <Steps>
          <Step title="安装 SDK">
            [安装 SDK](/api-reference/preparation/install-sdk)。请确保 DashScope SDK 版本不低于 2.22.5（Java）或 1.25.6（Python）。
          </Step>

          <Step title="获取 API Key">
            [获取 API Key](/api-reference/preparation/api-key)。为安全起见，建议将 API Key 设置为环境变量，避免硬编码在代码中。
          </Step>

          <Step title="运行示例代码">
            <CodeGroup>
              ```java Java
              import com.alibaba.dashscope.audio.omni.*;
              import com.alibaba.dashscope.exception.NoApiKeyException;
              import com.google.gson.JsonObject;
              import org.slf4j.Logger;
              import org.slf4j.LoggerFactory;

              import javax.sound.sampled.LineUnavailableException;
              import java.io.File;
              import java.io.FileInputStream;
              import java.util.Base64;
              import java.util.Collections;
              import java.util.concurrent.CountDownLatch;
              import java.util.concurrent.atomic.AtomicReference;

              public class Qwen3AsrRealtimeUsage {
                private static final Logger log = LoggerFactory.getLogger(Qwen3AsrRealtimeUsage.class);
                private static final int AUDIO_CHUNK_SIZE = 1024; // 音频块大小（字节）
                private static final int SLEEP_INTERVAL_MS = 30;  // 休眠间隔（毫秒）

                public static void main(String[] args) throws InterruptedException, LineUnavailableException {
                  CountDownLatch finishLatch = new CountDownLatch(1);

                  OmniRealtimeParam param = OmniRealtimeParam.builder()
                      .model("qwen3-asr-flash-realtime")
                      .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                      // 如果未配置环境变量，请将下一行替换为您的 API Key：.apikey("sk-xxx")
                      .apikey(System.getenv("DASHSCOPE_API_KEY"))
                      .build();

                  OmniRealtimeConversation conversation = null;
                  final AtomicReference<OmniRealtimeConversation> conversationRef = new AtomicReference<>(null);
                  conversation = new OmniRealtimeConversation(param, new OmniRealtimeCallback() {
                    @Override
                    public void onOpen() {
                      System.out.println("connection opened");
                    }
                    @Override
                    public void onEvent(JsonObject message) {
                      String type = message.get("type").getAsString();
                      switch(type) {
                        case "session.created":
                          System.out.println("start session: " + message.get("session").getAsJsonObject().get("id").getAsString());
                          break;
                        case "conversation.item.input_audio_transcription.completed":
                          System.out.println("transcription: " + message.get("transcript").getAsString());
                          finishLatch.countDown();
                          break;
                        case "input_audio_buffer.speech_started":
                          System.out.println("======VAD Speech Start======");
                          break;
                        case "input_audio_buffer.speech_stopped":
                          System.out.println("======VAD Speech Stop======");
                          break;
                        case "conversation.item.input_audio_transcription.text":
                          System.out.println("transcription: " + message.get("text").getAsString());
                          break;
                        default:
                          break;
                      }
                    }
                    @Override
                    public void onClose(int code, String reason) {
                      System.out.println("connection closed code: " + code + ", reason: " + reason);
                    }
                  });
                  conversationRef.set(conversation);
                  try {
                    conversation.connect();
                  } catch (NoApiKeyException e) {
                    throw new RuntimeException(e);
                  }

                  OmniRealtimeTranscriptionParam transcriptionParam = new OmniRealtimeTranscriptionParam();
                  transcriptionParam.setLanguage("zh");
                  transcriptionParam.setInputAudioFormat("pcm");
                  transcriptionParam.setInputSampleRate(16000);

                  OmniRealtimeConfig config = OmniRealtimeConfig.builder()
                      .modalities(Collections.singletonList(OmniRealtimeModality.TEXT))
                      .transcriptionConfig(transcriptionParam)
                      .build();
                  conversation.updateSession(config);

                  String filePath = "your_audio_file.pcm";
                  File audioFile = new File(filePath);
                  if (!audioFile.exists()) {
                    log.error("Audio file not found: {}", filePath);
                    return;
                  }

                  try (FileInputStream audioInputStream = new FileInputStream(audioFile)) {
                    byte[] audioBuffer = new byte[AUDIO_CHUNK_SIZE];
                    int bytesRead;
                    int totalBytesRead = 0;

                    log.info("Starting to send audio data from: {}", filePath);

                    // 分块读取并发送音频数据
                    while ((bytesRead = audioInputStream.read(audioBuffer)) != -1) {
                      totalBytesRead += bytesRead;
                      String audioB64 = Base64.getEncoder().encodeToString(audioBuffer);
                      // 将音频块发送至会话
                      conversation.appendAudio(audioB64);

                      // 短暂延迟以模拟实时音频流
                      Thread.sleep(SLEEP_INTERVAL_MS);
                    }

                    log.info("Finished sending audio data. Total bytes sent: {}", totalBytesRead);

                  } catch (Exception e) {
                    log.error("Error sending audio from file: {}", filePath, e);
                  }

                  // 发送 session.finish，等待会话结束后关闭连接
                  conversation.endSession();
                  log.info("Task finished");

                  System.exit(0);
                }
              }
              ```

              ```python Python
              import logging
              import os
              import base64
              import signal
              import sys
              import time
              import dashscope
              from dashscope.audio.qwen_omni import *
              from dashscope.audio.qwen_omni.omni_realtime import TranscriptionParams

              def setup_logging():
                """配置日志。"""
                logger = logging.getLogger('dashscope')
                logger.setLevel(logging.DEBUG)
                handler = logging.StreamHandler(sys.stdout)
                handler.setLevel(logging.DEBUG)
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                logger.addHandler(handler)
                logger.propagate = False
                return logger

              def init_api_key():
                """初始化 API Key。"""
                # 如果未配置环境变量，请将下一行替换为您的 API Key：dashscope.api_key = "sk-xxx"
                dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY', 'YOUR_API_KEY')
                if dashscope.api_key == 'YOUR_API_KEY':
                  print('[Warning] Using placeholder API key, set DASHSCOPE_API_KEY environment variable.')

              class MyCallback(OmniRealtimeCallback):
                """处理实时识别回调。"""
                def __init__(self, conversation):
                  self.conversation = conversation
                  self.handlers = {
                    'session.created': self._handle_session_created,
                    'conversation.item.input_audio_transcription.completed': self._handle_final_text,
                    'conversation.item.input_audio_transcription.text': self._handle_stash_text,
                    'input_audio_buffer.speech_started': lambda r: print('======Speech Start======'),
                    'input_audio_buffer.speech_stopped': lambda r: print('======Speech Stop======')
                  }

                def on_open(self):
                  print('Connection opened')

                def on_close(self, code, msg):
                  print(f'Connection closed, code: {code}, msg: {msg}')

                def on_event(self, response):
                  try:
                    handler = self.handlers.get(response['type'])
                    if handler:
                      handler(response)
                  except Exception as e:
                    print(f'[Error] {e}')

                def _handle_session_created(self, response):
                  print(f"Start session: {response['session']['id']}")

                def _handle_final_text(self, response):
                  print(f"Final recognized text: {response['transcript']}")

                def _handle_stash_text(self, response):
                  print(f"Got stash result: {response['stash']}")

              def read_audio_chunks(file_path, chunk_size=3200):
                """分块读取音频文件。"""
                with open(file_path, 'rb') as f:
                  while chunk := f.read(chunk_size):
                    yield chunk

              def send_audio(conversation, file_path, delay=0.1):
                """发送音频数据。"""
                if not os.path.exists(file_path):
                  raise FileNotFoundError(f"Audio file {file_path} does not exist.")

                print("Processing audio file... Press 'Ctrl+C' to stop.")
                for chunk in read_audio_chunks(file_path):
                  audio_b64 = base64.b64encode(chunk).decode('ascii')
                  conversation.append_audio(audio_b64)
                  time.sleep(delay)

              def main():
                setup_logging()
                init_api_key()

                audio_file_path = "./your_audio_file.pcm"
                conversation = OmniRealtimeConversation(
                  model='qwen3-asr-flash-realtime',
                  url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime',
                  callback=MyCallback(conversation=None)  # 临时传入 None，稍后注入
                )

                # 将 self 注入回调
                conversation.callback.conversation = conversation

                def handle_exit(sig, frame):
                  print('Ctrl+C pressed, exiting...')
                  conversation.close()
                  sys.exit(0)

                signal.signal(signal.SIGINT, handle_exit)

                conversation.connect()

                transcription_params = TranscriptionParams(
                  language='zh',
                  sample_rate=16000,
                  input_audio_format="pcm"
                )

                conversation.update_session(
                  output_modalities=[MultiModality.TEXT],
                  enable_input_audio_transcription=True,
                  transcription_params=transcription_params
                )

                try:
                  send_audio(conversation, audio_file_path)
                  # 发送 session.finish，等待会话结束后关闭连接
                  conversation.end_session()
                except Exception as e:
                  print(f"Error occurred: {e}")
                finally:
                  conversation.close()
                  print("Audio processing completed.")

              if __name__ == '__main__':
                main()
              ```
            </CodeGroup>
          </Step>
        </Steps>
      </Tab>

      <Tab title="WebSocket API">
        以下示例演示如何通过 WebSocket 连接发送本地音频文件并获取识别结果。

        <Steps>
          <Step title="获取 API Key">
            [获取 API Key](/api-reference/preparation/api-key)。为安全起见，建议将 API Key 设置为环境变量。
          </Step>

          <Step title="安装依赖">
            **Python**：

            运行示例前，请安装以下依赖：

            ```bash
            pip uninstall websocket-client
            pip uninstall websocket
            pip install websocket-client
            ```

            <Warning>
              请勿将示例代码文件命名为 `websocket.py`，否则可能出现以下错误：AttributeError: module 'websocket' has no attribute 'WebSocketApp'. Did you mean: 'WebSocket'?
            </Warning>

            **Java**：

            添加 Java-WebSocket 依赖：

            <CodeGroup>
              ```xml Maven
              <dependency>
                <groupId>org.java-websocket</groupId>
                <artifactId>Java-WebSocket</artifactId>
                <version>1.5.6</version>
              </dependency>
              ```

              ```gradle Gradle
              implementation 'org.java-websocket:Java-WebSocket:1.5.6'
              ```
            </CodeGroup>

            **Node.js**：

            ```bash
            npm install ws
            ```
          </Step>

          <Step title="编写并运行代码">
            实现完整的鉴权、连接、发送音频和接收结果流程。详情请参见[交互流程](/developer-guides/speech/asr-realtime#interaction-flow-qwen-asr-realtime)。

            <CodeGroup>
              ```python Python
              # pip install websocket-client
              import os
              import time
              import json
              import threading
              import base64
              import websocket
              import logging
              import logging.handlers
              from datetime import datetime

              logger = logging.getLogger(__name__)
              logger.setLevel(logging.DEBUG)

              # 如果未配置环境变量，请将下一行替换为您的 API Key：API_KEY="sk-xxx"
              API_KEY = os.environ.get("DASHSCOPE_API_KEY", "sk-xxx")
              QWEN_MODEL = "qwen3-asr-flash-realtime"
              baseUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime"
              url = f"{baseUrl}?model={QWEN_MODEL}"
              print(f"Connecting to server: {url}")

              # 注意：非 VAD 模式下，连续发送音频的累计时长不得超过 60 秒
              enableServerVad = True
              is_running = True  # 添加运行标志

              headers = [
                "Authorization: Bearer " + API_KEY,
                "OpenAI-Beta: realtime=v1"
              ]

              def init_logger():
                formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(message)s')
                f_handler = logging.handlers.RotatingFileHandler(
                  "omni_tester.log", maxBytes=100 * 1024 * 1024, backupCount=3
                )
                f_handler.setLevel(logging.DEBUG)
                f_handler.setFormatter(formatter)

                console = logging.StreamHandler()
                console.setLevel(logging.DEBUG)
                console.setFormatter(formatter)

                logger.addHandler(f_handler)
                logger.addHandler(console)

              def on_open(ws):
                logger.info("Connected to server.")

                # 会话更新事件
                event_manual = {
                  "event_id": "event_123",
                  "type": "session.update",
                  "session": {
                    "modalities": ["text"],
                    "input_audio_format": "pcm",
                    "sample_rate": 16000,
                    "input_audio_transcription": {
                      # 语言标识符，可选。如有明确的语言信息，请设置此项
                      "language": "zh"
                    },
                    "turn_detection": None
                  }
                }
                event_vad = {
                  "event_id": "event_123",
                  "type": "session.update",
                  "session": {
                    "modalities": ["text"],
                    "input_audio_format": "pcm",
                    "sample_rate": 16000,
                    "input_audio_transcription": {
                      "language": "zh"
                    },
                    "turn_detection": {
                      "type": "server_vad",
                      "threshold": 0.0,
                      "silence_duration_ms": 400
                    }
                  }
                }
                if enableServerVad:
                  logger.info(f"Sending event: {json.dumps(event_vad, indent=2)}")
                  ws.send(json.dumps(event_vad))
                else:
                  logger.info(f"Sending event: {json.dumps(event_manual, indent=2)}")
                  ws.send(json.dumps(event_manual))

              def on_message(ws, message):
                global is_running
                try:
                  data = json.loads(message)
                  logger.info(f"Received event: {json.dumps(data, ensure_ascii=False, indent=2)}")
                  if data.get("type") == "session.finished":
                    logger.info(f"Final transcript: {data.get('transcript')}")
                    logger.info("Closing WebSocket connection after session finished...")
                    is_running = False  # 停止音频发送线程
                    ws.close()
                except json.JSONDecodeError:
                  logger.error(f"Failed to parse message: {message}")

              def on_error(ws, error):
                logger.error(f"Error: {error}")

              def on_close(ws, close_status_code, close_msg):
                logger.info(f"Connection closed: {close_status_code} - {close_msg}")

              def send_audio(ws, local_audio_path):
                time.sleep(3)  # 等待会话更新完成
                global is_running

                with open(local_audio_path, 'rb') as audio_file:
                  logger.info(f"Start reading the file: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
                  while is_running:
                    audio_data = audio_file.read(3200)  # 约 0.1 秒的 PCM16/16kHz 数据
                    if not audio_data:
                      logger.info(f"Finished reading the file: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")
                      if ws.sock and ws.sock.connected:
                        if not enableServerVad:
                          commit_event = {
                            "event_id": "event_789",
                            "type": "input_audio_buffer.commit"
                          }
                          ws.send(json.dumps(commit_event))
                        finish_event = {
                          "event_id": "event_987",
                          "type": "session.finish"
                        }
                        ws.send(json.dumps(finish_event))
                      break

                    if not ws.sock or not ws.sock.connected:
                      logger.info("The WebSocket is closed. Stop sending audio.")
                      break

                    encoded_data = base64.b64encode(audio_data).decode('utf-8')
                    eventd = {
                      "event_id": f"event_{int(time.time() * 1000)}",
                      "type": "input_audio_buffer.append",
                      "audio": encoded_data
                    }
                    ws.send(json.dumps(eventd))
                    logger.info(f"Sending audio event: {eventd['event_id']}")
                    time.sleep(0.1)  # 模拟实时采集

              # 初始化日志
              init_logger()
              logger.info(f"Connecting to WebSocket server at {url}...")

              local_audio_path = "your_audio_file.pcm"
              ws = websocket.WebSocketApp(
                url,
                header=headers,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
              )

              thread = threading.Thread(target=send_audio, args=(ws, local_audio_path))
              thread.start()
              ws.run_forever()
              ```

              ```java Java
              import org.java_websocket.client.WebSocketClient;
              import org.java_websocket.handshake.ServerHandshake;
              import org.json.JSONObject;

              import java.net.URI;
              import java.nio.file.Files;
              import java.nio.file.Paths;
              import java.util.Base64;
              import java.util.concurrent.atomic.AtomicBoolean;
              import java.util.logging.*;

              public class QwenASRRealtimeClient {

                private static final Logger logger = Logger.getLogger(QwenASRRealtimeClient.class.getName());
                // 如果未配置环境变量，请将下一行替换为您的 API Key：private static final String API_KEY = "sk-xxx"
                private static final String API_KEY = System.getenv().getOrDefault("DASHSCOPE_API_KEY", "sk-xxx");
                private static final String MODEL = "qwen3-asr-flash-realtime";

                // 控制是否启用 VAD 模式
                private static final boolean enableServerVad = true;

                private static final AtomicBoolean isRunning = new AtomicBoolean(true);
                private static WebSocketClient client;

                public static void main(String[] args) throws Exception {
                  initLogger();

                  String baseUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime";
                  String url = baseUrl + "?model=" + MODEL;
                  logger.info("Connecting to server: " + url);

                  client = new WebSocketClient(new URI(url)) {
                    @Override
                    public void onOpen(ServerHandshake handshake) {
                      logger.info("Connected to server.");
                      sendSessionUpdate();
                    }

                    @Override
                    public void onMessage(String message) {
                      try {
                        JSONObject data = new JSONObject(message);
                        String eventType = data.optString("type");

                        logger.info("Received event: " + data.toString(2));

                        // 收到 finish 事件时，停止发送线程并关闭连接
                        if ("session.finished".equals(eventType)) {
                          logger.info("Final transcript: " + data.optString("transcript"));
                          logger.info("Closing WebSocket connection after session finished...");

                          isRunning.set(false); // 停止音频发送线程
                          if (this.isOpen()) {
                            this.close(1000, "ASR finished");
                          }
                        }
                      } catch (Exception e) {
                        logger.severe("Failed to parse message: " + message);
                      }
                    }

                    @Override
                    public void onClose(int code, String reason, boolean remote) {
                      logger.info("Connection closed: " + code + " - " + reason);
                    }

                    @Override
                    public void onError(Exception ex) {
                      logger.severe("Error: " + ex.getMessage());
                    }
                  };

                  // 添加请求头
                  client.addHeader("Authorization", "Bearer " + API_KEY);
                  client.addHeader("OpenAI-Beta", "realtime=v1");

                  client.connectBlocking(); // 阻塞直到连接建立

                  // 替换为需要识别的音频文件路径
                  String localAudioPath = "your_audio_file.pcm";
                  Thread audioThread = new Thread(() -> {
                    try {
                      sendAudio(localAudioPath);
                    } catch (Exception e) {
                      logger.severe("Audio sending thread error: " + e.getMessage());
                    }
                  });
                  audioThread.start();
                }

                /** 会话更新事件（启用/禁用 VAD）。 */
                private static void sendSessionUpdate() {
                  JSONObject eventNoVad = new JSONObject()
                      .put("event_id", "event_123")
                      .put("type", "session.update")
                      .put("session", new JSONObject()
                          .put("modalities", new String[]{"text"})
                          .put("input_audio_format", "pcm")
                          .put("sample_rate", 16000)
                          .put("input_audio_transcription", new JSONObject()
                              .put("language", "zh"))
                          .put("turn_detection", JSONObject.NULL) // 手动模式
                      );

                  JSONObject eventVad = new JSONObject()
                      .put("event_id", "event_123")
                      .put("type", "session.update")
                      .put("session", new JSONObject()
                          .put("modalities", new String[]{"text"})
                          .put("input_audio_format", "pcm")
                          .put("sample_rate", 16000)
                          .put("input_audio_transcription", new JSONObject()
                              .put("language", "zh"))
                          .put("turn_detection", new JSONObject()
                              .put("type", "server_vad")
                              .put("threshold", 0.0)
                              .put("silence_duration_ms", 400))
                      );

                  if (enableServerVad) {
                    logger.info("Sending event (VAD):\n" + eventVad.toString(2));
                    client.send(eventVad.toString());
                  } else {
                    logger.info("Sending event (Manual):\n" + eventNoVad.toString(2));
                    client.send(eventNoVad.toString());
                  }
                }

                /** 发送音频文件流。 */
                private static void sendAudio(String localAudioPath) throws Exception {
                  Thread.sleep(3000); // 等待会话就绪
                  byte[] allBytes = Files.readAllBytes(Paths.get(localAudioPath));
                  logger.info("Start reading the file.");

                  int offset = 0;
                  while (isRunning.get() && offset < allBytes.length) {
                    int chunkSize = Math.min(3200, allBytes.length - offset);
                    byte[] chunk = new byte[chunkSize];
                    System.arraycopy(allBytes, offset, chunk, 0, chunkSize);
                    offset += chunkSize;

                    if (client != null && client.isOpen()) {
                      String encoded = Base64.getEncoder().encodeToString(chunk);
                      JSONObject eventd = new JSONObject()
                          .put("event_id", "event_" + System.currentTimeMillis())
                          .put("type", "input_audio_buffer.append")
                          .put("audio", encoded);

                      client.send(eventd.toString());
                      logger.info("Sending audio event: " + eventd.getString("event_id"));
                    } else {
                      break; // 避免断连后继续发送
                    }

                    Thread.sleep(100); // 模拟实时发送
                  }

                  logger.info("Finished reading the file.");

                  if (client != null && client.isOpen()) {
                    // 非 VAD 模式需要发送 commit
                    if (!enableServerVad) {
                      JSONObject commitEvent = new JSONObject()
                          .put("event_id", "event_789")
                          .put("type", "input_audio_buffer.commit");
                      client.send(commitEvent.toString());
                      logger.info("Sent commit event for manual mode.");
                    }

                    JSONObject finishEvent = new JSONObject()
                        .put("event_id", "event_987")
                        .put("type", "session.finish");
                    client.send(finishEvent.toString());
                    logger.info("Sent finish event.");
                  }
                }

                /** 初始化日志。 */
                private static void initLogger() {
                  logger.setLevel(Level.ALL);
                  Logger rootLogger = Logger.getLogger("");
                  for (Handler h : rootLogger.getHandlers()) {
                    rootLogger.removeHandler(h);
                  }

                  Handler consoleHandler = new ConsoleHandler();
                  consoleHandler.setLevel(Level.ALL);
                  consoleHandler.setFormatter(new SimpleFormatter());
                  logger.addHandler(consoleHandler);
                }
              }
              ```

              ```javascript Node.js
              /**
               * Qwen-ASR Realtime WebSocket 客户端（Node.js 版本）
               * 功能：
               * - 支持 VAD 模式和手动模式
               * - 发送 session.update 启动会话
               * - 持续发送 input_audio_buffer.append 音频块
               * - 手动模式下发送 input_audio_buffer.commit
               * - 发送 session.finish 事件
               * - 收到 session.finished 事件后关闭连接
               */

              import WebSocket from 'ws';
              import fs from 'fs';

              // ===== 配置 =====
              // 如果未配置环境变量，请将下一行替换为您的 API Key：const API_KEY = "sk-xxx"
              const API_KEY = process.env.DASHSCOPE_API_KEY || 'sk-xxx';
              const MODEL = 'qwen3-asr-flash-realtime';
              const enableServerVad = true; // true 为 VAD 模式，false 为手动模式
              const localAudioPath = 'your_audio_file.pcm'; // PCM16、16 kHz 音频文件路径

              const baseUrl = 'wss://dashscope.aliyuncs.com/api-ws/v1/realtime';
              const url = `${baseUrl}?model=${MODEL}`;

              console.log(`Connecting to server: ${url}`);

              // ===== 状态控制 =====
              let isRunning = true;

              // ===== 建立连接 =====
              const ws = new WebSocket(url, {
                headers: {
                  'Authorization': `Bearer ${API_KEY}`,
                  'OpenAI-Beta': 'realtime=v1'
                }
              });

              // ===== 事件绑定 =====
              ws.on('open', () => {
                console.log('[WebSocket] Connected to server.');
                sendSessionUpdate();
                // 启动音频发送线程
                sendAudio(localAudioPath);
              });

              ws.on('message', (message) => {
                try {
                  const data = JSON.parse(message);
                  console.log('[Received Event]:', JSON.stringify(data, null, 2));

                  // 收到 finish 事件
                  if (data.type === 'session.finished') {
                    console.log(`[Final Transcript] ${data.transcript}`);
                    console.log('[Action] Closing WebSocket connection after session finished...');

                    if (ws.readyState === WebSocket.OPEN) {
                      ws.close(1000, 'ASR finished');
                    }
                  }
                } catch (e) {
                  console.error('[Error] Failed to parse message:', message);
                }
              });

              ws.on('close', (code, reason) => {
                console.log(`[WebSocket] Connection closed: ${code} - ${reason}`);
              });

              ws.on('error', (err) => {
                console.error('[WebSocket Error]', err);
              });

              // ===== 会话更新 =====
              function sendSessionUpdate() {
                const eventNoVad = {
                  event_id: 'event_123',
                  type: 'session.update',
                  session: {
                    modalities: ['text'],
                    input_audio_format: 'pcm',
                    sample_rate: 16000,
                    input_audio_transcription: {
                      language: 'zh'
                    },
                    turn_detection: null
                  }
                };

                const eventVad = {
                  event_id: 'event_123',
                  type: 'session.update',
                  session: {
                    modalities: ['text'],
                    input_audio_format: 'pcm',
                    sample_rate: 16000,
                    input_audio_transcription: {
                      language: 'zh'
                    },
                    turn_detection: {
                      type: 'server_vad',
                      threshold: 0.0,
                      silence_duration_ms: 400
                    }
                  }
                };

                if (enableServerVad) {
                  console.log('[Send Event] VAD Mode:\n', JSON.stringify(eventVad, null, 2));
                  ws.send(JSON.stringify(eventVad));
                } else {
                  console.log('[Send Event] Manual Mode:\n', JSON.stringify(eventNoVad, null, 2));
                  ws.send(JSON.stringify(eventNoVad));
                }
              }

              // ===== 发送音频文件流 =====
              function sendAudio(audioPath) {
                setTimeout(() => {
                  console.log(`[File Read Start] ${audioPath}`);
                  const buffer = fs.readFileSync(audioPath);

                  let offset = 0;
                  const chunkSize = 3200; // 约 0.1 秒的 PCM16 音频

                  function sendChunk() {
                    if (!isRunning) return;
                    if (offset >= buffer.length) {
                      isRunning = false; // 停止发送音频
                      console.log('[File Read End]');
                      if (ws.readyState === WebSocket.OPEN) {
                        if (!enableServerVad) {
                          const commitEvent = {
                            event_id: 'event_789',
                            type: 'input_audio_buffer.commit'
                          };
                          ws.send(JSON.stringify(commitEvent));
                          console.log('[Send Commit Event]');
                        }

                        const finishEvent = {
                          event_id: 'event_987',
                          type: 'session.finish'
                        };
                        ws.send(JSON.stringify(finishEvent));
                        console.log('[Send Finish Event]');
                      }

                      return;
                    }

                    if (ws.readyState !== WebSocket.OPEN) {
                      console.log('[Stop] WebSocket is not open.');
                      return;
                    }

                    const chunk = buffer.slice(offset, offset + chunkSize);
                    offset += chunkSize;

                    const encoded = chunk.toString('base64');
                    const appendEvent = {
                      event_id: `event_${Date.now()}`,
                      type: 'input_audio_buffer.append',
                      audio: encoded
                    };

                    ws.send(JSON.stringify(appendEvent));
                    console.log(`[Send Audio Event] ${appendEvent.event_id}`);

                    setTimeout(sendChunk, 100); // 模拟实时发送
                  }

                  sendChunk();
                }, 3000); // 等待会话配置完成
              }
              ```
            </CodeGroup>
          </Step>
        </Steps>
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

## 上线部署

### 提升识别准确率

- **选择采样率匹配的模型**：对于 8 kHz 电话音频，请直接使用 8 kHz 模型，而非将其上采样至 16 kHz 后再识别。上采样会导致信息失真，影响识别效果。
- **使用自定义词汇功能**：针对业务专有名词、人名、品牌名等，可配置自定义词汇，显著提升识别准确率。详情请参见[自定义词汇](/developer-guides/speech/improve-recognition-accuracy)。
- **优化输入音频质量**：尽量使用高质量麦克风，保证较高的信噪比（SNR）和无回声的录音环境。在应用层，可集成降噪（如 RNNoise）和声学回声消除（AEC）等算法对音频进行预处理，获取更干净的信号。
- **指定识别语言**：对于多语言模型，若在调用时能预先确定音频语言，有助于模型快速收敛，避免发音相似的语言之间产生混淆，从而提升准确率。

### 敏感词过滤

敏感词过滤可对识别结果中的敏感词执行替换或移除，适用于客服质检、内容合规、字幕审核等场景。

- **支持范围**：仅 Fun-ASR。
- **使用限制**：最多支持设置 32 个敏感词。
- **默认行为**：未传入 `special_word_filter` 参数时，不会对敏感词进行过滤。

`special_word_filter` 是 JSON 对象，包含三个子字段：

- `filter_with_signed.word_list`：字符串数组，列出需要被替换为等长 `*` 的敏感词。例如 `["测试"]`，「帮我测试一下」会变成「帮我\*\*一下」。
- `filter_with_empty.word_list`：字符串数组，列出需要从结果中完全移除的敏感词。例如 `["开始"]`，「比赛这就要开始了吗」会变成「比赛这就要了吗」。
- `system_reserved_filter`：布尔值，默认 `false`。是否启用敏感词过滤功能。

配置示例：

```json
{
  "special_word_filter": {
    "filter_with_signed": {
      "word_list": ["测试"]
    },
    "filter_with_empty": {
      "word_list": ["开始", "发生"]
    },
    "system_reserved_filter": true
  }
}
```

不同 SDK 暴露上述参数的命名习惯不同（如字典 key、对象属性、方法等），完整字段对照请参见 [Fun-ASR 实时语音识别 API 参考](/api-reference/speech-recognition/fun-asr-realtime/client-events)。

### 设置容错策略

- **客户端断线重连**：客户端应实现自动重连机制，以应对网络抖动。对于 Python SDK，建议：
  1. 捕获异常：在 `Callback` 类中实现 `on_error` 方法。网络错误或其他异常发生时，`dashscope` SDK 会调用此方法。
  2. 通知状态：`on_error` 触发时，设置重连信号。在 Python 中，可使用线程安全标志 `threading.Event`。
  3. 重连循环：将主逻辑包裹在 `for` 循环中（例如重试 3 次）。检测到重连信号时，中断当前识别、清理资源，并在等待数秒后重启循环以建立新连接。
- **设置心跳防止连接断开**：为保持与服务器的持久连接，请将 `heartbeat` 参数设置为 `true`。即使音频长时间静音，也能确保连接不中断。
- **限流**：调用模型接口时，请注意遵守模型的[限流](/developer-guides/administration/rate-limits)规则。

<a id="core-usage-context-biasing-qwen-asr" />

## 核心功能：上下文增强（Qwen-ASR）

通过提供上下文，可优化特定领域词汇的识别效果，例如人名、地名和产品术语。

**长度限制**： 上下文内容不得超过 **10,000** 个 token。

**使用方式**：

- WebSocket API：在 [session.update](/api-reference/speech-recognition/qwen-asr-realtime/client-events) 事件中设置 `session.input_audio_transcription.corpus.text` 参数。
- Python SDK：设置 `corpus_text` 参数。
- Java SDK：设置 `corpusText` 参数。

**支持的文本类型（包含但不限于）**：

- 各类分隔符格式的热词列表，如：热词1、热词2、热词3、热词4
- 任意格式和长度的文本段落或章节
- 混合内容：词汇列表与段落的任意组合
- 无关或无意义的文本，包括乱码。该功能容错性强，几乎不受无关文本的负面影响。

**示例**：

某段音频的正确转写结果为："你了解哪些投行圈的内部黑话？首先是九大外资投行，即 Bulge Bracket，BB……"

| 无上下文增强                                                                                 | 有上下文增强                                                                |
| -------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| 无上下文增强时，部分投行名称可能被误识。例如，"Bulge Bracket"被识别为"鸟石"。识别结果："你了解哪些投行圈的内部黑话？首先是九大外资投行，即鸟石，BB……" | 有上下文增强时，投行名称被正确识别。识别结果："你了解哪些投行圈的内部黑话？首先是九大外资投行，即 Bulge Bracket，BB……" |

如需实现上述效果，可将以下任意一种内容添加至上下文：

- 词汇列表：
  - 词汇列表 1：

```plaintext
Bulge Bracket, Boutique, Middle Market, domestic securities firms
```

- 词汇列表 2：

```plaintext
Bulge Bracket Boutique Middle Market domestic securities firms
```

- 词汇列表 3：

```plaintext
['Bulge Bracket', 'Boutique', 'Middle Market', 'domestic securities firms']
```

- 自然语言：

```plaintext
Investment Banking Categories Revealed!
Recently, many friends from Australia have asked me, what exactly is an investment bank? Today, I'll explain it. For international students, investment banks can be mainly divided into four categories: Bulge Bracket, Boutique, Middle Market, and domestic securities firms.
Bulge Bracket Investment Banks: These are what we often call the nine major investment banks, including Goldman Sachs, Morgan Stanley, etc. These large banks are enormous in both business scope and scale.
Boutique Investment Banks: These banks are relatively small but highly specialized in their business areas. For example, Lazard, Evercore, etc., have deep professional knowledge and experience in specific fields.
Middle Market Investment Banks: This type of bank mainly serves medium-sized companies, providing services such as mergers and acquisitions, and IPOs. Although not as large as the major banks, they have a high influence in specific markets.
Domestic Securities Firms: With the rise of the Chinese market, domestic securities firms are also playing an increasingly important role in the international market.
In addition, there are some Position and business divisions, you can refer to the relevant charts. I hope this information helps you better understand investment banking and prepare for your future career!
```

- 含干扰信息的自然语言：部分文本与识别内容无关，例如以下示例中的人名列表。

```plaintext
Investment Banking Categories Revealed!
Recently, many friends from Australia have asked me, what exactly is an investment bank? Today, I'll explain it. For international students, investment banks can be mainly divided into four categories: Bulge Bracket, Boutique, Middle Market, and domestic securities firms.
Bulge Bracket Investment Banks: These are what we often call the nine major investment banks, including Goldman Sachs, Morgan Stanley, etc. These large banks are enormous in both business scope and scale.
Boutique Investment Banks: These banks are relatively small but highly specialized in their business areas. For example, Lazard, Evercore, etc., have deep professional knowledge and experience in specific fields.
Middle Market Investment Banks: This type of bank mainly serves medium-sized companies, providing services such as mergers and acquisitions, and IPOs. Although not as large as the major banks, they have a high influence in specific markets.
Domestic Securities Firms: With the rise of the Chinese market, domestic securities firms are also playing an increasingly important role in the international market.
In addition, there are some Position and business divisions, you can refer to the relevant charts. I hope this information helps you better understand investment banking and prepare for your future career!
Wang Haoxuan, Li Zihan, Zhang Jingxing, Liu Xinyi, Chen Junjie, Yang Siyuan, Zhao Yutong, Huang Zhiqiang, Zhou Zimo, Wu Yajing, Xu Ruoxi, Sun Haoran, Hu Jinyu, Zhu Chenxi, Guo Wenbo, He Jingshu, Gao Yuhang, Lin Yifei,
Zheng Xiaoyan, Liang Bowen, Luo Jiaqi, Song Mingzhe, Xie Wanting, Tang Ziqian, Han Mengyao, Feng Yiran, Cao Qinxue, Deng Zirui, Xiao Wangshu, Xu Jiashu,
Cheng Yinuo, Yuan Zhiruo, Peng Haoyu, Dong Simiao, Fan Jingyu, Su Zijin, Lv Wenxuan, Jiang Shihan, Ding Muchen,
Wei Shuyao, Ren Tianyou, Jiang Yichen, Hua Qingyu, Shen Xinghe, Fu Jinyu, Yao Xingchen, Zhong Lingyu, Yan Licheng, Jin Ruoshui, Taoranting, Qi Shaoshang, Xue Zhilan, Zou Yunfan, Xiong Ziang, Bai Wenfeng, Yi Qianfan
```

## API 参考

<Tabs>
  <Tab title="Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime">
    - [Fun-ASR 实时语音识别 API 参考](/api-reference/speech-recognition/fun-asr-realtime/python-sdk)
    - [AOQ 客户端 API](/developer-guides/realtime-api/aoq-sdk-intro)（适用于 Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime）
  </Tab>

  <Tab title="Qwen3-ASR-Flash-Realtime">
    [实时语音识别 API 参考](/api-reference/speech-recognition/qwen-asr-realtime/python-sdk)
  </Tab>
</Tabs>

<a id="interaction-flow-qwen-asr-realtime" />

## 交互流程（Qwen-ASR-Realtime）

Qwen 实时语音识别通过 WebSocket 流式传输音频。提供两种模式：[VAD 模式（默认）](#vad-mode-default) 和[手动模式](#manual-mode)。

### URL

将 `<model_name>` 替换为您的[模型](/developer-guides/speech/speech-to-text-models)名称。

```http
wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=<model_name>
```

### 请求头

```http
"Authorization": "Bearer $DASHSCOPE_API_KEY"
```

<a id="vad-mode-default" />

### VAD 模式（默认）

服务端检测语音边界并自动分句。客户端流式推送音频，服务端在每句话结束时返回识别结果。适合对话和会议转写场景。

**启用方式**： 在 [`session.update`](/api-reference/speech-recognition/qwen-asr-realtime/client-events) 事件中设置 `session.turn_detection`。

![VAD 模式交互流程](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5305458671/CAEQUxiBgMDxw_SV3hkiIDIxZDVlODkyYWRiNDQ0YWJiNWFkYjZhNTgwMzc1MjUw5812623_20251022102739.334.svg)

- 客户端发送 [`input_audio_buffer.append`](/api-reference/speech-recognition/qwen-asr-realtime/client-events)，向缓冲区追加音频。

- 服务端检测到语音时，返回 [`input_audio_buffer.speech_started`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。

  <Note>
    若客户端在此事件之前发送了 [`session.finish`](/api-reference/speech-recognition/qwen-asr-realtime/client-events)，服务端将返回 [`session.finished`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)，客户端须断开连接。
  </Note>

- 客户端继续发送 [`input_audio_buffer.append`](/api-reference/speech-recognition/qwen-asr-realtime/client-events)。

- 所有音频发送完毕后，客户端发送 [`session.finish`](/api-reference/speech-recognition/qwen-asr-realtime/client-events) 结束会话。

- 服务端检测到语音结束时，返回 [`input_audio_buffer.speech_stopped`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。

- 服务端返回 [`input_audio_buffer.committed`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。

- 服务端返回 [`conversation.item.created`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。

- 服务端返回 [`conversation.item.input_audio_transcription.text`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)，包含实时转写结果。

- 服务端返回 [`conversation.item.input_audio_transcription.completed`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)，包含最终转写结果。

- 识别完成后，服务端返回 [`session.finished`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)，客户端须断开连接。

<a id="manual-mode" />

### 手动模式

由客户端控制分句：发送一句话完整的音频后，再发送 [`input_audio_buffer.commit`](/api-reference/speech-recognition/qwen-asr-realtime/client-events)。适合客户端已知句子边界的场景，例如聊天应用中的语音消息。

**启用方式**： 在 [`session.update`](/api-reference/speech-recognition/qwen-asr-realtime/client-events) 事件中将 `session.turn_detection` 设置为 `null`。

![手动模式交互流程](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5305458671/CAEQUxiBgID0ovyV3hkiIGQyZGZiNDJkMDVhOTQxYjBiMmM2OWJjY2M3MjFjNGVh5812623_20251022102739.334.svg)

- 客户端发送 [`input_audio_buffer.append`](/api-reference/speech-recognition/qwen-asr-realtime/client-events)，向缓冲区追加音频。

- 客户端发送 [`input_audio_buffer.commit`](/api-reference/speech-recognition/qwen-asr-realtime/client-events)，创建新的用户消息。

- 客户端发送 [`session.finish`](/api-reference/speech-recognition/qwen-asr-realtime/client-events) 结束会话。

- 服务端返回 [`input_audio_buffer.committed`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)。

- 服务端返回 [`conversation.item.input_audio_transcription.text`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)，包含实时转写结果。

- 服务端返回 [`conversation.item.input_audio_transcription.completed`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)，包含最终转写结果。

- 识别完成后，服务端返回 [`session.finished`](/api-reference/speech-recognition/qwen-asr-realtime/server-events)，客户端须断开连接。

## 备选方案：使用 Qwen-Omni

您也可以使用 **Qwen-Omni**（`qwen3-omni-flash-realtime`）通过 WebSocket 进行实时语音识别。Qwen-Omni 是一个能理解音频的大语言模型——您可以通过系统提示词提供领域上下文，而无需使用热词列表。

**适合使用 Omni 进行 ASR 的场景**： 输入音频干净（麦克风、语音通话），且需要通过提示词处理特定领域术语。

**适合使用专用 ASR 模型的场景**： 音频嘈杂或混合（含背景音乐的会议、含音效的视频），或需要热词、说话人分离、时间戳等功能。

<Warning>
  Qwen-Omni 会处理所有音频内容，而不仅仅是语音。音乐、打字声或环境噪声可能产生描述性文字而非转写结果。对于混合音频，请提前使用 VAD 隔离语音，或改用专用 ASR 模型。
</Warning>

**ASR 提示词模板**：

```python
messages = [
  {"role": "system", "content": "Transcribe the following audio exactly as spoken. Output only the transcription text. Ignore non-speech sounds."},
  {"role": "user", "content": [{"type": "input_audio", "input_audio": {"data": audio_data, "format": "wav"}}]}
]
```

<Tip>
  Qwen-Omni-Realtime 使用 WebSocket 进行双向流式传输。完整的 API 和 SDK 参考，请参见[实时对话](/developer-guides/speech/realtime-multimodal-speech)。
</Tip>
