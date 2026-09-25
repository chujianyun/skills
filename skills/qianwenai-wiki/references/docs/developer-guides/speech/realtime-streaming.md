> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 实时语音合成

> 实时流式语音合成

实时语音合成将文本实时转换为自然语音。千问AI平台提供 CosyVoice、Qwen-TTS 和 Sambert 系列模型，支持流式输入输出，并提供声音复刻、声音设计及精细化音频控制能力，适用于语音助手、有声读物、智能客服等场景。

## 核心功能

- 实时生成高保真语音，支持中英等多语种自然发声
- 提供[声音复刻](/api-reference/speech-synthesis/voice-cloning/create-voice)与[声音设计](/api-reference/speech-synthesis/voice-design/create-voice)两种音色定制方式
- 支持流式输入输出，首包延迟低，适用于实时对话场景
- 可调节语速、语调、音量与码率，精细控制语音表现
- 兼容主流音频格式（PCM、WAV、MP3、Opus），最高支持48kHz采样率输出
- 支持[指令控制](#指令控制)，可通过自然语言指令控制语音表现力（仅Qwen-TTS Instruct系列及部分CosyVoice模型）

## 适用范围

**支持的模型**：

调用以下模型时，请使用 [API Key](https://platform.qianwenai.com/home/api-keys)：

- **CosyVoice**: cosyvoice-v3.5-plus, cosyvoice-v3.5-flash, cosyvoice-v3-plus, cosyvoice-v3-flash, cosyvoice-v2, cosyvoice-v1
- **Qwen-TTS**: qwen3-tts-flash-realtime, qwen3-tts-instruct-flash-realtime, qwen3-tts-vd-realtime, qwen3-tts-vc-realtime, qwen-tts-realtime
- **Sambert**: 详情请参见 [Sambert 模型列表](/api-reference/speech-synthesis/sambert/java-sdk#模型列表)

完整的模型列表和版本信息，请参见[语音合成模型列表](/developer-guides/speech/tts-models)。

## 快速开始

在编写代码前，请根据业务场景选择合适的调用方式：

| 调用方式                  | 适用场景                  | 流式支持 |
| --------------------- | --------------------- | ---- |
| 非流式（同步）               | 批量任务、短文本、生成完整音频文件     | 否    |
| 流式输出（单向）              | 对首包延迟敏感的实时应用          | 是    |
| 流式输入+输出（双向，WebSocket） | 对话式AI、LLM语音输出、交互式语音助手 | 是    |

如需最低延迟，推荐使用流式输出搭配 PCM 格式。PCM 无需编码开销，可直接送入音频设备播放。

下面是调用API的示例代码。更多常用场景的代码示例，请参见 [GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。如果通过 AOQ 协议接入 CosyVoice 系列模型，需要下载并集成 AOQ 客户端 SDK，详见 [AOQ SDK 简介](/developer-guides/realtime-api/aoq-sdk-intro)。

CosyVoice 系列模型除 WebSocket 协议外，还支持通过 AOQ 协议接入；如果是客户端对接，且更看重稳定的延迟、弱网下的交互能力、实时双工的降噪与回声消除，可优先考虑 AOQ，协议对比与选型请参见[模型/应用支持力度](/developer-guides/realtime-api/overview#模型支持力度)。

<Tabs>
  <Tab title="Qwen-Audio-TTS">
    以下示例演示如何使用系统音色进行语音合成。如需使用[指令控制](#指令控制)功能，请通过 `instruction` 参数设置指令。

    <Tabs>
      <Tab title="Python">
        ```python
        # coding=utf-8
        import os
        import dashscope
        from dashscope.audio.tts_v2 import *

        # 如果未配置环境变量，请将下行替换为您的 API Key：dashscope.api_key = "sk-xxx"
        dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')
        dashscope.base_websocket_api_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'
        # 模型
        # qwen-audio-3.0-tts-flash/qwen-audio-3.0-tts-plus：使用 longanhuan_v3.6 等音色。
        model = "qwen-audio-3.0-tts-flash"
        # 音色
        voice = "longanhuan_v3.6"
        # 实例化 SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
        synthesizer = SpeechSynthesizer(model=model, voice=voice)
        # 发送待合成文本，获取二进制音频
        audio = synthesizer.call("今天天气怎么样？")
        # 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
        print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
            synthesizer.get_last_request_id(),
            synthesizer.get_first_package_delay()))
        # 将音频保存至本地
        with open('output.mp3', 'wb') as f:
          f.write(audio)
        ```
      </Tab>

      <Tab title="Java">
        ```java
        import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
        import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
        import com.alibaba.dashscope.utils.Constants;
        import java.io.File;
        import java.io.FileOutputStream;
        import java.io.IOException;
        import java.nio.ByteBuffer;

        public class Main {
            // 模型
            // qwen-audio-3.0-tts-flash/qwen-audio-3.0-tts-plus：使用 longanhuan_v3.6 等音色。
            // 每个音色支持的语言不同，合成日语、韩语等非中文语言时，需选择支持对应语言的音色。详见音色列表。
            private static String model = "qwen-audio-3.0-tts-flash";
            // 音色
            private static String voice = "longanhuan_v3.6";

            public static void streamAudioDataToSpeaker() {
                // 请求参数
                SpeechSynthesisParam param =
                        SpeechSynthesisParam.builder()
                                // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
                                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                                .model(model) // 模型
                                .voice(voice) // 音色
                                .build();
                // 同步模式：禁用回调（第二个参数为null）
                SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
                ByteBuffer audio = null;
                try {
                    // 阻塞直至音频返回
                    audio = synthesizer.call("今天天气怎么样？");
                } catch (Exception e) {
                    throw new RuntimeException(e);
                } finally {
                    // 任务结束关闭websocket连接
                    synthesizer.getDuplexApi().close(1000, "bye");
                }
                if (audio != null) {
                    // 将音频数据保存到本地文件"output.mp3"中
                    File file = new File("output.mp3");
                    // 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
                    // 注意：getFirstPackageDelay() 需要 dashscope-sdk-java 2.18.0 及以上版本
                    System.out.println(
                            "[Metric] requestId为："
                                    + synthesizer.getLastRequestId()
                                    + "首包延迟（毫秒）为："
                                    + synthesizer.getFirstPackageDelay());
                    try (FileOutputStream fos = new FileOutputStream(file)) {
                        fos.write(audio.array());
                    } catch (IOException e) {
                        throw new RuntimeException(e);
                    }
                }
            }

            public static void main(String[] args) {
                streamAudioDataToSpeaker();
                System.exit(0);
            }
        }
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="CosyVoice">
    <Note>
      `cosyvoice-v3.5-plus` 和 `cosyvoice-v3.5-flash` 模型专门用于声音设计和声音复刻场景（无系统音色）。在使用它们进行语音合成之前，请先参见[CosyVoice声音复刻/设计API](/api-reference/speech-synthesis/voice-cloning/create-voice)创建目标音色。创建完成后，只需将代码中的 `voice` 字段更新为您的音色 ID，并将 `model` 字段指定为对应模型，即可正常运行。
    </Note>

    更多代码示例请参见 [GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo)。

    <Tabs>
      <Tab title="使用系统音色进行语音合成">
        以下示例演示如何使用系统音色（参见[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)）进行语音合成。如需非实时合成（发送完整文本，接收完整音频），请参见[非实时语音合成](/developer-guides/speech/tts)。

        ### 将大模型生成的文本实时转为语音并播放

        将 Qwen 模型（qwen3.5-flash）的输出文本实时合成语音，并在本地设备播放。

        <Tabs>
          <Tab title="Python">
            运行 Python 示例前，请通过 pip 安装第三方音频播放库。

            ```python
            # coding=utf-8
            # pyaudio 安装说明：
            # APPLE Mac OS X
            #   brew install portaudio
            #   pip install pyaudio
            # Debian/Ubuntu
            #   sudo apt-get install python-pyaudio python3-pyaudio
            #   or
            #   pip install pyaudio
            # CentOS
            #   sudo yum install -y portaudio portaudio-devel && pip install pyaudio
            # Microsoft Windows
            #   python -m pip install pyaudio

            import os
            import pyaudio
            import dashscope
            from dashscope.audio.tts_v2 import *

            from http import HTTPStatus
            from dashscope import Generation

            # 如果未配置环境变量，请将下行替换为您的 API Key：dashscope.api_key = "sk-xxx"
            dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

            dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

            # cosyvoice-v3-flash/cosyvoice-v3-plus：可选用 longanyang 等音色。
            # 每种音色支持的语言不同。合成日语、韩语等非中文语言时，请选择支持相应语言的音色。详见 CosyVoice 音色列表。
            model = "cosyvoice-v3-flash"
            voice = "longanyang"

            class Callback(ResultCallback):
              _player = None
              _stream = None

              def on_open(self):
                print("websocket is open.")
                self._player = pyaudio.PyAudio()
                self._stream = self._player.open(
                  format=pyaudio.paInt16, channels=1, rate=22050, output=True
                )

              def on_complete(self):
                print("speech synthesis task complete successfully.")

              def on_error(self, message: str):
                print(f"speech synthesis task failed, {message}")

              def on_close(self):
                print("websocket is closed.")
                # 停止播放
                self._stream.stop_stream()
                self._stream.close()
                self._player.terminate()

              def on_event(self, message):
                print(f"recv speech synthsis message {message}")

              def on_data(self, data: bytes) -> None:
                print("audio result length:", len(data))
                self._stream.write(data)

            def synthesizer_with_llm():
              callback = Callback()
              synthesizer = SpeechSynthesizer(
                model=model,
                voice=voice,
                format=AudioFormat.PCM_22050HZ_MONO_16BIT,
                callback=callback,
              )

              messages = [{"role": "user", "content": "Please introduce yourself"}]
              responses = Generation.call(
                model="qwen3.5-flash",
                messages=messages,
                result_format="message",  # 设置返回格式为 message
                stream=True,  # 启用流式输出
                incremental_output=True,  # 启用增量输出
              )
              for response in responses:
                if response.status_code == HTTPStatus.OK:
                  print(response.output.choices[0]["message"]["content"], end="")
                  synthesizer.streaming_call(response.output.choices[0]["message"]["content"])
                else:
                  print(
                    "Request id: %s, Status code: %s, error code: %s, error message: %s"
                    % (
                      response.request_id,
                      response.status_code,
                      response.code,
                      response.message,
                    )
                  )
              synthesizer.streaming_complete()
              print('requestId: ', synthesizer.get_last_request_id())

            if __name__ == "__main__":
              synthesizer_with_llm()
            ```
          </Tab>

          <Tab title="Java">
            ```java
            import com.alibaba.dashscope.aigc.generation.Generation;
            import com.alibaba.dashscope.aigc.generation.GenerationParam;
            import com.alibaba.dashscope.aigc.generation.GenerationResult;
            import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
            import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
            import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
            import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
            import com.alibaba.dashscope.common.Message;
            import com.alibaba.dashscope.common.ResultCallback;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.protocol.Protocol;
            import com.alibaba.dashscope.utils.Constants;

            import javax.sound.sampled.*;
            import java.util.Arrays;
            import java.util.concurrent.CountDownLatch;

            public class Main {
              private static String ttsModel = "cosyvoice-v3-flash";
              private static String voice = "longanyang";

              public static void synthesizerWithLlm() throws Exception {
                CountDownLatch latch = new CountDownLatch(1);

                // 配置音频播放（PCM 22050 Hz，单声道，16 位）
                AudioFormat audioFormat = new AudioFormat(22050, 16, 1, true, false);
                DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);
                SourceDataLine speakers = (SourceDataLine) AudioSystem.getLine(info);
                speakers.open(audioFormat);
                speakers.start();

                // 配置 TTS 回调
                ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
                  @Override
                  public void onEvent(SpeechSynthesisResult result) {
                    if (result.getAudioFrame() != null) {
                      byte[] audio = result.getAudioFrame().array();
                      speakers.write(audio, 0, audio.length);
                    }
                  }

                  @Override
                  public void onComplete() {
                    System.out.println("Speech synthesis completed.");
                    latch.countDown();
                  }

                  @Override
                  public void onError(Exception e) {
                    System.err.println("TTS error: " + e.getMessage());
                    latch.countDown();
                  }
                };

                // 初始化 TTS 合成器
                SpeechSynthesisParam ttsParam = SpeechSynthesisParam.builder()
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model(ttsModel)
                    .voice(voice)
                    .format(SpeechSynthesisAudioFormat.PCM_22050HZ_MONO_16BIT)
                    .build();
                SpeechSynthesizer synthesizer = new SpeechSynthesizer(ttsParam, callback);

                // 将 Qwen 大模型文本流式传入 TTS
                Generation gen = new Generation(
                    Protocol.HTTP.getValue(),
                    "https://dashscope.aliyuncs.com/api/v1");
                Message userMsg = Message.builder()
                    .role(Role.USER.getValue())
                    .content("Please introduce yourself")
                    .build();
                GenerationParam llmParam = GenerationParam.builder()
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model("qwen3.5-flash")
                    .messages(Arrays.asList(userMsg))
                    .resultFormat(GenerationParam.ResultFormat.MESSAGE)
                    .incrementalOutput(true)
                    .build();

                // 将大模型输出流式传入 TTS
                gen.streamCall(llmParam).blockingForEach(result -> {
                  String text = result.getOutput().getChoices().get(0).getMessage().getContent();
                  if (text != null && !text.isEmpty()) {
                    System.out.print(text);
                    synthesizer.streamingCall(text);
                  }
                });

                // 完成 TTS 合成
                synthesizer.streamingComplete();
                latch.await();

                // 释放资源
                speakers.drain();
                speakers.close();
                synthesizer.getDuplexApi().close(1000, "bye");
              }

              public static void main(String[] args) throws Exception {
                Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
                synthesizerWithLlm();
                System.exit(0);
              }
            }
            ```
          </Tab>
        </Tabs>

        ### 通过回调函数流式接收音频

        发送完整文本，通过回调函数增量接收音频数据。适用于短文本场景，可在不阻塞主线程的情况下实现低延迟音频输出。

        <Tabs>
          <Tab title="Python">
            ```python
            # coding=utf-8

            import os
            import dashscope
            from dashscope.audio.tts_v2 import *

            from datetime import datetime

            def get_timestamp():
              now = datetime.now()
              formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
              return formatted_timestamp

            # 如果未配置环境变量，请取消下一行注释并替换为你的 API Key：dashscope.api_key = "sk-xxx"
            dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

            dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

            # 模型
            model = "cosyvoice-v3-flash"
            # 音色
            voice = "longanyang"

            # 定义回调接口
            class Callback(ResultCallback):
              _player = None
              _stream = None

              def on_open(self):
                self.file = open("output.mp3", "wb")
                print("连接已建立：" + get_timestamp())

              def on_complete(self):
                print("语音合成完成，已接收全部结果：" + get_timestamp())
                # 仅在 on_complete 触发后才可调用 get_first_package_delay
                # 首次请求的首包延迟包含 WebSocket 建连时间
                print('[Metric] requestId: {}, first-package delay: {} ms'.format(
                  synthesizer.get_last_request_id(),
                  synthesizer.get_first_package_delay()))

              def on_error(self, message: str):
                print(f"语音合成错误：{message}")

              def on_close(self):
                print("连接已关闭：" + get_timestamp())
                self.file.close()

              def on_event(self, message):
                pass

              def on_data(self, data: bytes) -> None:
                print(get_timestamp() + " 音频二进制数据长度：" + str(len(data)))
                self.file.write(data)

            callback = Callback()

            # 实例化 SpeechSynthesizer，在构造方法中传入 model、voice 等请求参数
            synthesizer = SpeechSynthesizer(
              model=model,
              voice=voice,
              callback=callback,
            )

            # 发送待合成文本，通过回调接口的 on_data 方法实时获取二进制音频
            synthesizer.call("How is the weather today?")
            ```
          </Tab>

          <Tab title="Java">
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

                // 实现 ResultCallback 接口
                ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
                  @Override
                  public void onEvent(SpeechSynthesisResult result) {
                    if (result.getAudioFrame() != null) {
                      // 在此添加音频处理逻辑
                      System.out.println(TimeUtils.getTimestamp() + " 已接收音频");
                    }
                  }

                  @Override
                  public void onComplete() {
                    System.out.println(TimeUtils.getTimestamp() + " 接收完成，语音合成结束。");
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
                        // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model)
                        .voice(voice)
                        .build();
                // 将回调作为第二个参数传入，启用异步模式
                SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
                // 非阻塞调用：立即返回 null，结果通过 onEvent 回调获取
                try {
                  synthesizer.call("What's the weather like today?");
                  latch.await();
                } catch (Exception e) {
                  throw new RuntimeException(e);
                } finally {
                  // 任务完成后关闭 WebSocket 连接
                  synthesizer.getDuplexApi().close(1000, "bye");
                }
                // 首次调用的首包延迟包含 WebSocket 建连时间
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
          </Tab>
        </Tabs>

        ### 流式文本实时合成

        增量发送文本片段，通过回调函数实时接收音频数据。这种双向流式方式适用于长文本或与大语言模型集成等文本分段到达的场景。

        <Tabs>
          <Tab title="Python">
            ```python
            # coding=utf-8
            #
            # PyAudio 安装说明：
            # macOS 系统：
            #   brew install portaudio
            #   pip install pyaudio
            # Debian/Ubuntu 系统：
            #   sudo apt-get install python-pyaudio python3-pyaudio
            #   或
            #   pip install pyaudio
            # CentOS 系统：
            #   sudo yum install -y portaudio portaudio-devel && pip install pyaudio
            # Windows 系统：
            #   python -m pip install pyaudio

            import os
            import time
            import pyaudio
            import dashscope
            from dashscope.api_entities.dashscope_response import SpeechSynthesisResponse
            from dashscope.audio.tts_v2 import *

            from datetime import datetime

            def get_timestamp():
              now = datetime.now()
              formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
              return formatted_timestamp

            # 如果未配置环境变量，请取消下一行注释并替换为你的 API Key：dashscope.api_key = "sk-xxx"
            dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

            dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

            # 模型
            model = "cosyvoice-v3-flash"
            # 音色
            voice = "longanyang"

            # 定义回调接口
            class Callback(ResultCallback):
              _player = None
              _stream = None

              def on_open(self):
                print("连接已建立：" + get_timestamp())
                self._player = pyaudio.PyAudio()
                self._stream = self._player.open(
                  format=pyaudio.paInt16, channels=1, rate=22050, output=True
                )

              def on_complete(self):
                print("语音合成完成，已接收全部结果：" + get_timestamp())

              def on_error(self, message: str):
                print(f"语音合成错误：{message}")

              def on_close(self):
                print("连接已关闭：" + get_timestamp())
                # 停止播放器
                self._stream.stop_stream()
                self._stream.close()
                self._player.terminate()

              def on_event(self, message):
                pass

              def on_data(self, data: bytes) -> None:
                print(get_timestamp() + " 音频二进制数据长度：" + str(len(data)))
                self._stream.write(data)

            callback = Callback()

            test_text = [
              "流式文本语音合成 SDK，",
              "可以将输入文本",
              "转换为二进制音频数据。",
              "相较于非流式语音合成，",
              "流式合成具有更优的实时性能。",
              "用户在输入的同时即可听到近乎同步的音频输出，",
              "大幅提升交互体验",
              "并减少等待时间。",
              "非常适合与大语言模型（LLM）集成，",
              "将文本流式传输进行语音合成。",
            ]

            # 实例化 SpeechSynthesizer，在构造方法中传入 model、voice 等请求参数
            synthesizer = SpeechSynthesizer(
              model=model,
              voice=voice,
              format=AudioFormat.PCM_22050HZ_MONO_16BIT,
              callback=callback,
            )

            # 流式发送文本进行合成，通过回调接口的 on_data 方法实时获取二进制音频
            for text in test_text:
              synthesizer.streaming_call(text)
              time.sleep(0.1)
            # 结束流式语音合成
            synthesizer.streaming_complete()

            # 首次请求的首包延迟包含 WebSocket 建连时间
            print('[Metric] requestId: {}, first-package delay: {} ms'.format(
              synthesizer.get_last_request_id(),
              synthesizer.get_first_package_delay()))
            ```
          </Tab>

          <Tab title="Java">
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
              private static String[] textArray = {"流式文本语音合成 SDK，",
                  "可以将输入文本", "转换为二进制音频数据。", "相较于非流式语音合成，",
                  "流式合成具有更优的实时性能。", "用户在输入的同时即可听到近乎同步的音频输出，",
                  "大幅提升交互体验，", "并减少等待时间。",
                  "非常适合与大语言模型", "（LLM）集成，",
                  "将文本流式传输进行语音合成。"};
              private static String model = "cosyvoice-v3-flash";
              private static String voice = "longanyang";

              public static void streamAudioDataToSpeaker() {
                // 配置回调
                ResultCallback<SpeechSynthesisResult> callback = new ResultCallback<SpeechSynthesisResult>() {
                  @Override
                  public void onEvent(SpeechSynthesisResult result) {
                    if (result.getAudioFrame() != null) {
                      // 在此添加音频处理逻辑
                      System.out.println(TimeUtils.getTimestamp() + " 已接收音频");
                    }
                  }

                  @Override
                  public void onComplete() {
                    System.out.println(TimeUtils.getTimestamp() + " 接收完成，语音合成结束。");
                  }

                  @Override
                  public void onError(Exception e) {
                    System.out.println("发生异常：" + e.toString());
                  }
                };

                // 请求参数
                SpeechSynthesisParam param =
                    SpeechSynthesisParam.builder()
                        // 如果未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model(model)
                        .voice(voice)
                        .format(SpeechSynthesisAudioFormat
                            .PCM_22050HZ_MONO_16BIT) // 流式合成请使用 PCM 或 MP3 格式
                        .build();
                SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, callback);
                try {
                  for (String text : textArray) {
                    // 发送文本片段，音频通过 onEvent 实时返回
                    synthesizer.streamingCall(text);
                  }
                  // 等待流式合成完成
                  synthesizer.streamingComplete();
                } catch (Exception e) {
                  throw new RuntimeException(e);
                } finally {
                  // 任务完成后关闭 WebSocket 连接
                  synthesizer.getDuplexApi().close(1000, "bye");
                }

                // 首次调用的首包延迟包含 WebSocket 建连时间
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
          </Tab>
        </Tabs>
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Qwen-TTS-Realtime">
    **SDK 版本要求**：Python SDK 1.25.11 及以上；Java SDK 2.22.7 及以上。更多代码示例请参见 [GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni)。

    运行代码前，请先[获取 API Key](/api-reference/preparation/api-key) 并[安装 SDK](/api-reference/preparation/install-sdk)。

    <Tabs>
      <Tab title="使用系统音色进行语音合成">
        可用音色请参见[支持的音色列表](#系统音色)。

        如需使用[指令控制](#指令控制)功能，请将 `model` 参数替换为 `qwen3-tts-instruct-flash-realtime`，并通过 `instructions` 参数设置指令。

        <Tabs>
          <Tab title="DashScope SDK">
            <Tabs>
              <Tab title="Python">
                **Server commit 模式**：

                <CodeGroup>
                  ```python Python
                  import os
                  import base64
                  import threading
                  import time
                  import dashscope
                  from dashscope.audio.qwen_tts_realtime import *

                  qwen_tts_realtime: QwenTtsRealtime = None
                  text_to_synthesize = [
                    'Right? I love supermarkets like this.',
                    'Especially during Chinese New Year,',
                    'I go shopping at supermarkets.',
                    'And I feel',
                    'absolutely thrilled!',
                    'I want to buy so many things!'
                  ]

                  DO_VIDEO_TEST = False

                  def init_dashscope_api_key():
                    """
                      设置 DashScope API Key。详细信息请参见：
                      https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
                    """

                    dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')  # 如未设置环境变量，请替换为：dashscope.api_key = "sk-xxx"

                  class MyCallback(QwenTtsRealtimeCallback):
                    def __init__(self):
                      self.complete_event = threading.Event()
                      self.file = open('result_24k.pcm', 'wb')

                    def on_open(self) -> None:
                      print('连接已建立，初始化播放器')

                    def on_close(self, close_status_code, close_msg) -> None:
                      self.file.close()
                      print('连接已关闭，状态码：{}，消息：{}，销毁播放器'.format(close_status_code, close_msg))

                    def on_event(self, response: str) -> None:
                      try:
                        global qwen_tts_realtime
                        type = response['type']
                        if 'session.created' == type:
                          print('会话已开始：{}'.format(response['session']['id']))
                        if 'response.audio.delta' == type:
                          recv_audio_b64 = response['delta']
                          self.file.write(base64.b64decode(recv_audio_b64))
                        if 'response.done' == type:
                          print(f'response {qwen_tts_realtime.get_last_response_id()} done')
                        if 'session.finished' == type:
                          print('会话已结束')
                          self.complete_event.set()
                      except Exception as e:
                        print('[错误] {}'.format(e))
                        return

                    def wait_for_finished(self):
                      self.complete_event.wait()

                  if __name__  == '__main__':
                    init_dashscope_api_key()

                    print('正在初始化...')

                    callback = MyCallback()

                    qwen_tts_realtime = QwenTtsRealtime(
                      # 如需使用指令控制功能，请将模型替换为 qwen3-tts-instruct-flash-realtime
                      model='qwen3-tts-flash-realtime',
                      callback=callback,
                      url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
                      )

                    qwen_tts_realtime.connect()
                    qwen_tts_realtime.update_session(
                      voice = 'Cherry',
                      response_format = AudioFormat.PCM_24000HZ_MONO_16BIT,
                      # 如需使用指令控制功能，请取消以下注释并将模型替换为 qwen3-tts-instruct-flash-realtime
                      # instructions='语速较快，语调上扬，适合介绍时尚产品。',
                      # optimize_instructions=True,
                      mode = 'server_commit'
                    )
                    for text_chunk in text_to_synthesize:
                      print(f'发送文本：{text_chunk}')
                      qwen_tts_realtime.append_text(text_chunk)
                      time.sleep(0.1)
                    qwen_tts_realtime.finish()
                    callback.wait_for_finished()
                    print('[Metric] session: {}, first audio delay: {}'.format(
                            qwen_tts_realtime.get_session_id(),
                            qwen_tts_realtime.get_first_audio_delay(),
                            ))
                  ```
                </CodeGroup>

                **Commit 模式**：

                <CodeGroup>
                  ```python Python
                  import base64
                  import os
                  import threading
                  import dashscope
                  from dashscope.audio.qwen_tts_realtime import *

                  qwen_tts_realtime: QwenTtsRealtime = None
                  text_to_synthesize = [
                    'This is the first sentence.',
                    'This is the second sentence.',
                    'This is the third sentence.',
                  ]

                  DO_VIDEO_TEST = False

                  def init_dashscope_api_key():
                    """
                      设置 DashScope API Key。详细信息请参见：
                      https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
                    """

                    dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')  # 如未设置环境变量，请替换为：dashscope.api_key = "sk-xxx"

                  class MyCallback(QwenTtsRealtimeCallback):
                    def __init__(self):
                      super().__init__()
                      self.response_counter = 0
                      self.complete_event = threading.Event()
                      self.file = open(f'result_{self.response_counter}_24k.pcm', 'wb')

                    def reset_event(self):
                      self.response_counter += 1
                      self.file = open(f'result_{self.response_counter}_24k.pcm', 'wb')
                      self.complete_event = threading.Event()

                    def on_open(self) -> None:
                      print('连接已建立，初始化播放器')

                    def on_close(self, close_status_code, close_msg) -> None:
                      print('连接已关闭，状态码：{}，消息：{}，销毁播放器'.format(close_status_code, close_msg))

                    def on_event(self, response: str) -> None:
                      try:
                        global qwen_tts_realtime
                        type = response['type']
                        if 'session.created' == type:
                          print('会话已开始：{}'.format(response['session']['id']))
                        if 'response.audio.delta' == type:
                          recv_audio_b64 = response['delta']
                          self.file.write(base64.b64decode(recv_audio_b64))
                        if 'response.done' == type:
                          print(f'response {qwen_tts_realtime.get_last_response_id()} done')
                          self.complete_event.set()
                          self.file.close()
                        if 'session.finished' == type:
                          print('会话已结束')
                          self.complete_event.set()
                      except Exception as e:
                        print('[错误] {}'.format(e))
                        return

                    def wait_for_response_done(self):
                      self.complete_event.wait()

                  if __name__  == '__main__':
                    init_dashscope_api_key()

                    print('正在初始化...')

                    callback = MyCallback()

                    qwen_tts_realtime = QwenTtsRealtime(
                      # 如需使用指令控制功能，请将模型替换为 qwen3-tts-instruct-flash-realtime
                      model='qwen3-tts-flash-realtime',
                      callback=callback,
                      url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
                      )

                    qwen_tts_realtime.connect()
                    qwen_tts_realtime.update_session(
                      voice = 'Cherry',
                      response_format = AudioFormat.PCM_24000HZ_MONO_16BIT,
                      # 如需使用指令控制功能，请取消以下注释并将模型替换为 qwen3-tts-instruct-flash-realtime
                      # instructions='语速较快，语调上扬，适合介绍时尚产品。',
                      # optimize_instructions=True,
                      mode = 'commit'
                    )
                    print(f'发送文本：{text_to_synthesize[0]}')
                    qwen_tts_realtime.append_text(text_to_synthesize[0])
                    qwen_tts_realtime.commit()
                    callback.wait_for_response_done()
                    callback.reset_event()

                    print(f'发送文本：{text_to_synthesize[1]}')
                    qwen_tts_realtime.append_text(text_to_synthesize[1])
                    qwen_tts_realtime.commit()
                    callback.wait_for_response_done()
                    callback.reset_event()

                    print(f'发送文本：{text_to_synthesize[2]}')
                    qwen_tts_realtime.append_text(text_to_synthesize[2])
                    qwen_tts_realtime.commit()
                    callback.wait_for_response_done()

                    qwen_tts_realtime.finish()
                    print('[Metric] session: {}, first audio delay: {}'.format(
                            qwen_tts_realtime.get_session_id(),
                            qwen_tts_realtime.get_first_audio_delay(),
                            ))
                  ```
                </CodeGroup>
              </Tab>

              <Tab title="Java">
                **Server commit 模式**：

                <CodeGroup>
                  ```java Java
                  import com.alibaba.dashscope.audio.qwen_tts_realtime.*;
                  import com.alibaba.dashscope.exception.NoApiKeyException;
                  import com.google.gson.JsonObject;
                  import javax.sound.sampled.LineUnavailableException;
                  import javax.sound.sampled.SourceDataLine;
                  import javax.sound.sampled.AudioFormat;
                  import javax.sound.sampled.DataLine;
                  import javax.sound.sampled.AudioSystem;
                  import java.io.FileNotFoundException;
                  import java.io.IOException;
                  import java.util.Base64;
                  import java.util.Queue;
                  import java.util.concurrent.CountDownLatch;
                  import java.util.concurrent.atomic.AtomicReference;
                  import java.util.concurrent.ConcurrentLinkedQueue;
                  import java.util.concurrent.atomic.AtomicBoolean;

                  public class Main {
                    static String[] textToSynthesize = {
                        "Right? I just really love this kind of supermarket",
                        "Especially during the New Year",
                        "Going to the supermarket",
                        "Makes me feel",
                        "Super, super happy!",
                        "I want to buy so many things!"
                    };

                    // 实时 PCM 音频播放器类
                    public static class RealtimePcmPlayer {
                      private int sampleRate;
                      private SourceDataLine line;
                      private AudioFormat audioFormat;
                      private Thread decoderThread;
                      private Thread playerThread;
                      private AtomicBoolean stopped = new AtomicBoolean(false);
                      private Queue<String> b64AudioBuffer = new ConcurrentLinkedQueue<>();
                      private Queue<byte[]> RawAudioBuffer = new ConcurrentLinkedQueue<>();

                      // 构造方法：初始化音频格式和音频输出线路
                      public RealtimePcmPlayer(int sampleRate) throws LineUnavailableException {
                        this.sampleRate = sampleRate;
                        this.audioFormat = new AudioFormat(this.sampleRate, 16, 1, true, false);
                        DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);
                        line = (SourceDataLine) AudioSystem.getLine(info);
                        line.open(audioFormat);
                        line.start();
                        decoderThread = new Thread(new Runnable() {
                          @Override
                          public void run() {
                            while (!stopped.get()) {
                              String b64Audio = b64AudioBuffer.poll();
                              if (b64Audio != null) {
                                byte[] rawAudio = Base64.getDecoder().decode(b64Audio);
                                RawAudioBuffer.add(rawAudio);
                              } else {
                                try {
                                  Thread.sleep(100);
                                } catch (InterruptedException e) {
                                  throw new RuntimeException(e);
                                }
                              }
                            }
                          }
                        });
                        playerThread = new Thread(new Runnable() {
                          @Override
                          public void run() {
                            while (!stopped.get()) {
                              byte[] rawAudio = RawAudioBuffer.poll();
                              if (rawAudio != null) {
                                try {
                                  playChunk(rawAudio);
                                } catch (IOException e) {
                                  throw new RuntimeException(e);
                                } catch (InterruptedException e) {
                                  throw new RuntimeException(e);
                                }
                              } else {
                                try {
                                  Thread.sleep(100);
                                } catch (InterruptedException e) {
                                  throw new RuntimeException(e);
                                }
                              }
                            }
                          }
                        });
                        decoderThread.start();
                        playerThread.start();
                      }

                      // 播放音频片段，阻塞至播放完成
                      private void playChunk(byte[] chunk) throws IOException, InterruptedException {
                        if (chunk == null || chunk.length == 0) return;

                        int bytesWritten = 0;
                        while (bytesWritten < chunk.length) {
                          bytesWritten += line.write(chunk, bytesWritten, chunk.length - bytesWritten);
                        }
                        int audioLength = chunk.length / (this.sampleRate*2/1000);
                        // 等待缓冲区中的音频播放完毕
                        Thread.sleep(audioLength - 10);
                      }

                      public void write(String b64Audio) {
                        b64AudioBuffer.add(b64Audio);
                      }

                      public void cancel() {
                        b64AudioBuffer.clear();
                        RawAudioBuffer.clear();
                      }

                      public void waitForComplete() throws InterruptedException {
                        while (!b64AudioBuffer.isEmpty() || !RawAudioBuffer.isEmpty()) {
                          Thread.sleep(100);
                        }
                        line.drain();
                      }

                      public void shutdown() throws InterruptedException {
                        stopped.set(true);
                        decoderThread.join();
                        playerThread.join();
                        if (line != null && line.isRunning()) {
                          line.drain();
                          line.close();
                        }
                      }
                    }

                    public static void main(String[] args) throws InterruptedException, LineUnavailableException, FileNotFoundException {
                      QwenTtsRealtimeParam param = QwenTtsRealtimeParam.builder()
                          // 如需使用指令控制功能，请将模型替换为 qwen3-tts-instruct-flash-realtime
                          .model("qwen3-tts-flash-realtime")
                          .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                          .apikey(System.getenv("DASHSCOPE_API_KEY"))
                          .build();
                      AtomicReference<CountDownLatch> completeLatch = new AtomicReference<>(new CountDownLatch(1));
                      final AtomicReference<QwenTtsRealtime> qwenTtsRef = new AtomicReference<>(null);

                      // 创建实时音频播放器实例
                      RealtimePcmPlayer audioPlayer = new RealtimePcmPlayer(24000);

                      QwenTtsRealtime qwenTtsRealtime = new QwenTtsRealtime(param, new QwenTtsRealtimeCallback() {
                        @Override
                        public void onOpen() {
                          // 处理连接建立事件
                        }
                        @Override
                        public void onEvent(JsonObject message) {
                          String type = message.get("type").getAsString();
                          switch(type) {
                            case "session.created":
                              // 处理会话创建事件
                              break;
                            case "response.audio.delta":
                              String recvAudioB64 = message.get("delta").getAsString();
                              // 实时播放音频
                              audioPlayer.write(recvAudioB64);
                              break;
                            case "response.done":
                              // 处理响应完成事件
                              break;
                            case "session.finished":
                              // 处理会话结束事件
                              completeLatch.get().countDown();
                            default:
                              break;
                          }
                        }
                        @Override
                        public void onClose(int code, String reason) {
                          // 处理连接关闭事件
                        }
                      });
                      qwenTtsRef.set(qwenTtsRealtime);
                      try {
                        qwenTtsRealtime.connect();
                      } catch (NoApiKeyException e) {
                        throw new RuntimeException(e);
                      }
                      QwenTtsRealtimeConfig config = QwenTtsRealtimeConfig.builder()
                          .voice("Cherry")
                          .responseFormat(QwenTtsRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT)
                          .mode("server_commit")
                          // 如需使用指令控制功能，请取消以下注释并将模型替换为 qwen3-tts-instruct-flash-realtime。
                          // .instructions("")
                          // .optimizeInstructions(true)
                          .build();
                      qwenTtsRealtime.updateSession(config);
                      for (String text:textToSynthesize) {
                        qwenTtsRealtime.appendText(text);
                        Thread.sleep(100);
                      }
                      qwenTtsRealtime.finish();
                      completeLatch.get().await();
                      qwenTtsRealtime.close();

                      // 等待音频播放完成后关闭播放器
                      audioPlayer.waitForComplete();
                      audioPlayer.shutdown();
                      System.exit(0);
                    }
                  }
                  ```
                </CodeGroup>

                **Commit 模式**：

                <CodeGroup>
                  ```java Java
                  import com.alibaba.dashscope.audio.qwen_tts_realtime.*;
                  import com.alibaba.dashscope.exception.NoApiKeyException;
                  import com.google.gson.JsonObject;
                  import javax.sound.sampled.LineUnavailableException;
                  import javax.sound.sampled.SourceDataLine;
                  import javax.sound.sampled.AudioFormat;
                  import javax.sound.sampled.DataLine;
                  import javax.sound.sampled.AudioSystem;
                  import java.io.File;
                  import java.io.FileNotFoundException;
                  import java.io.FileOutputStream;
                  import java.io.IOException;
                  import java.util.Base64;
                  import java.util.Queue;
                  import java.util.Scanner;
                  import java.util.concurrent.CountDownLatch;
                  import java.util.concurrent.atomic.AtomicReference;
                  import java.util.concurrent.ConcurrentLinkedQueue;
                  import java.util.concurrent.atomic.AtomicBoolean;

                  public class commit {
                    // 实时 PCM 音频播放器类
                    public static class RealtimePcmPlayer {
                      private int sampleRate;
                      private SourceDataLine line;
                      private AudioFormat audioFormat;
                      private Thread decoderThread;
                      private Thread playerThread;
                      private AtomicBoolean stopped = new AtomicBoolean(false);
                      private Queue<String> b64AudioBuffer = new ConcurrentLinkedQueue<>();
                      private Queue<byte[]> RawAudioBuffer = new ConcurrentLinkedQueue<>();

                      // 构造方法：初始化音频格式和音频输出线路
                      public RealtimePcmPlayer(int sampleRate) throws LineUnavailableException {
                        this.sampleRate = sampleRate;
                        this.audioFormat = new AudioFormat(this.sampleRate, 16, 1, true, false);
                        DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);
                        line = (SourceDataLine) AudioSystem.getLine(info);
                        line.open(audioFormat);
                        line.start();
                        decoderThread = new Thread(new Runnable() {
                          @Override
                          public void run() {
                            while (!stopped.get()) {
                              String b64Audio = b64AudioBuffer.poll();
                              if (b64Audio != null) {
                                byte[] rawAudio = Base64.getDecoder().decode(b64Audio);
                                RawAudioBuffer.add(rawAudio);
                              } else {
                                try {
                                  Thread.sleep(100);
                                } catch (InterruptedException e) {
                                  throw new RuntimeException(e);
                                }
                              }
                            }
                          }
                        });
                        playerThread = new Thread(new Runnable() {
                          @Override
                          public void run() {
                            while (!stopped.get()) {
                              byte[] rawAudio = RawAudioBuffer.poll();
                              if (rawAudio != null) {
                                try {
                                  playChunk(rawAudio);
                                } catch (IOException e) {
                                  throw new RuntimeException(e);
                                } catch (InterruptedException e) {
                                  throw new RuntimeException(e);
                                }
                              } else {
                                try {
                                  Thread.sleep(100);
                                } catch (InterruptedException e) {
                                  throw new RuntimeException(e);
                                }
                              }
                            }
                          }
                        });
                        decoderThread.start();
                        playerThread.start();
                      }

                      // 播放音频片段，阻塞至播放完成
                      private void playChunk(byte[] chunk) throws IOException, InterruptedException {
                        if (chunk == null || chunk.length == 0) return;

                        int bytesWritten = 0;
                        while (bytesWritten < chunk.length) {
                          bytesWritten += line.write(chunk, bytesWritten, chunk.length - bytesWritten);
                        }
                        int audioLength = chunk.length / (this.sampleRate*2/1000);
                        // 等待缓冲区中的音频播放完毕
                        Thread.sleep(audioLength - 10);
                      }

                      public void write(String b64Audio) {
                        b64AudioBuffer.add(b64Audio);
                      }

                      public void cancel() {
                        b64AudioBuffer.clear();
                        RawAudioBuffer.clear();
                      }

                      public void waitForComplete() throws InterruptedException {
                        // 等待缓冲区中所有音频数据播放完毕
                        while (!b64AudioBuffer.isEmpty() || !RawAudioBuffer.isEmpty()) {
                          Thread.sleep(100);
                        }
                        // 等待音频输出线路播放完毕
                        line.drain();
                      }

                      public void shutdown() throws InterruptedException {
                        stopped.set(true);
                        decoderThread.join();
                        playerThread.join();
                        if (line != null && line.isRunning()) {
                          line.drain();
                          line.close();
                        }
                      }
                    }

                    public static void main(String[] args) throws InterruptedException, LineUnavailableException, FileNotFoundException {
                      Scanner scanner = new Scanner(System.in);

                      QwenTtsRealtimeParam param = QwenTtsRealtimeParam.builder()
                      // To use the instruction control feature, replace the model with qwen3-tts-instruct-flash-realtime.
                      .model("qwen3-tts-flash-realtime")
                      .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                      .apikey(System.getenv("DASHSCOPE_API_KEY"))
                      .build();

                      AtomicReference<CountDownLatch> completeLatch = new AtomicReference<>(new CountDownLatch(1));

                      // 创建实时播放器实例
                      RealtimePcmPlayer audioPlayer = new RealtimePcmPlayer(24000);

                      final AtomicReference<QwenTtsRealtime> qwenTtsRef = new AtomicReference<>(null);
                      QwenTtsRealtime qwenTtsRealtime = new QwenTtsRealtime(param, new QwenTtsRealtimeCallback() {
                        //            File file = new File("result_24k.pcm");
                        //            FileOutputStream fos = new FileOutputStream(file);
                        @Override
                        public void onOpen() {
                          System.out.println("connection opened");
                          System.out.println("Enter text and press Enter to send. Enter 'quit' to exit the program.");
                        }
                        @Override
                        public void onEvent(JsonObject message) {
                          String type = message.get("type").getAsString();
                          switch(type) {
                            case "session.created":
                            System.out.println("start session: " + message.get("session").getAsJsonObject().get("id").getAsString());
                            break;
                            case "response.audio.delta":
                            String recvAudioB64 = message.get("delta").getAsString();
                            byte[] rawAudio = Base64.getDecoder().decode(recvAudioB64);
                            //                            fos.write(rawAudio);
                            // 实时播放音频
                            audioPlayer.write(recvAudioB64);
                            break;
                            case "response.done":
                            System.out.println("response done");
                            // 等待音频播放完成
                            try {
                              audioPlayer.waitForComplete();
                            } catch (InterruptedException e) {
                              throw new RuntimeException(e);
                            }
                            // 准备接收下一次输入
                            completeLatch.get().countDown();
                            break;
                            case "session.finished":
                            System.out.println("session finished");
                            if (qwenTtsRef.get() != null) {
                              System.out.println("[Metric] response: " + qwenTtsRef.get().getResponseId() +
                              ", first audio delay: " + qwenTtsRef.get().getFirstAudioDelay() + " ms");
                            }
                            completeLatch.get().countDown();
                            default:
                            break;
                          }
                        }
                        @Override
                        public void onClose(int code, String reason) {
                          System.out.println("connection closed code: " + code + ", reason: " + reason);
                          try {
                            //                    fos.close();
                            // 等待播放完成后关闭播放器
                            audioPlayer.waitForComplete();
                            audioPlayer.shutdown();
                          } catch (InterruptedException e) {
                            throw new RuntimeException(e);
                          }
                        }
                      });
                      qwenTtsRef.set(qwenTtsRealtime);
                      try {
                        qwenTtsRealtime.connect();
                      } catch (NoApiKeyException e) {
                        throw new RuntimeException(e);
                      }
                      QwenTtsRealtimeConfig config = QwenTtsRealtimeConfig.builder()
                      .voice("Cherry")
                      .responseFormat(QwenTtsRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT)
                      .mode("commit")
                      // 如需使用指令控制功能，请取消以下注释并将模型替换为 qwen3-tts-instruct-flash-realtime。
                      // .instructions("")
                      // .optimizeInstructions(true)
                      .build();
                      qwenTtsRealtime.updateSession(config);

                      // 循环读取用户输入
                      while (true) {
                        System.out.print("Enter the text to synthesize: ");
                        String text = scanner.nextLine();

                        // 用户输入 quit 时退出程序
                        if ("quit".equalsIgnoreCase(text.trim())) {
                          System.out.println("Closing the connection...");
                          qwenTtsRealtime.finish();
                          completeLatch.get().await();
                          break;
                        }

                        // 用户输入为空则跳过
                        if (text.trim().isEmpty()) {
                          continue;
                        }

                        // 重新初始化 CountDownLatch
                        completeLatch.set(new CountDownLatch(1));

                        // 发送文本
                        qwenTtsRealtime.appendText(text);
                        qwenTtsRealtime.commit();

                        // 等待当前合成完成
                        completeLatch.get().await();
                      }

                      // 清理资源
                      audioPlayer.waitForComplete();
                      audioPlayer.shutdown();
                      scanner.close();
                      System.exit(0);
                    }
                  }
                  ```
                </CodeGroup>
              </Tab>
            </Tabs>
          </Tab>

          <Tab title="WebSocket API">
            <Steps>
              <Step title="准备运行环境">
                根据您的操作系统安装 pyaudio。

                <Tabs>
                  <Tab title="macOS">
                    ```bash
                    brew install portaudio && pip install pyaudio
                    ```
                  </Tab>

                  <Tab title="Debian/Ubuntu">
                    ```bash
                    sudo apt-get install python3-pyaudio

                    or

                    pip install pyaudio
                    ```
                  </Tab>

                  <Tab title="CentOS">
                    ```bash
                    sudo yum install -y portaudio portaudio-devel && pip install pyaudio
                    ```
                  </Tab>

                  <Tab title="Windows">
                    ```powershell
                    pip install pyaudio
                    ```
                  </Tab>
                </Tabs>

                然后通过 pip 安装 WebSocket 依赖：

                ```bash
                pip install websocket-client==1.8.0 websockets
                ```
              </Step>

              <Step title="创建客户端">
                在本地新建名为 `tts_realtime_client.py` 的 Python 文件，将以下代码复制到文件中：

                <Accordion title="tts_realtime_client.py">
                  ```python
                  # -- coding: utf-8 --

                  import asyncio
                  import websockets
                  import json
                  import base64
                  import time
                  from typing import Optional, Callable, Dict, Any
                  from enum import Enum

                  class SessionMode(Enum):
                    SERVER_COMMIT = "server_commit"
                    COMMIT = "commit"

                  class TTSRealtimeClient:
                    """
                    TTS Realtime API 客户端。

                    该类提供了连接 TTS Realtime API、发送文本数据、接收音频输出以及管理 WebSocket 连接的方法。

                    Attributes:
                      base_url (str):
                        Realtime API 的基础 URL。
                      api_key (str):
                        用于身份验证的 API Key。
                      voice (str):
                        服务端用于语音合成的音色。
                      mode (SessionMode):
                        会话模式，server_commit 或 commit。
                      audio_callback (Callable[[bytes], None]):
                        接收音频数据的回调函数。
                      language_type(str)
                        合成语音的语言。可选值：Chinese, English, German, Italian, Portuguese, Spanish, Japanese, Korean, French, Russian, Auto
                    """

                    def __init__(
                        self,
                        base_url: str,
                        api_key: str,
                        voice: str = "Cherry",
                        mode: SessionMode = SessionMode.SERVER_COMMIT,
                        audio_callback: Optional[Callable[[bytes], None]] = None,
                      language_type: str = "Auto"):
                      self.base_url = base_url
                      self.api_key = api_key
                      self.voice = voice
                      self.mode = mode
                      self.ws = None
                      self.audio_callback = audio_callback
                      self.language_type = language_type

                      # 当前响应状态
                      self._current_response_id = None
                      self._current_item_id = None
                      self._is_responding = False
                      self._response_done_future = None

                    async def connect(self) -> None:
                      """建立与 TTS Realtime API 的 WebSocket 连接。"""
                      headers = {
                        "Authorization": f"Bearer {self.api_key}"
                      }

                      self.ws = await websockets.connect(self.base_url, additional_headers=headers)

                      # 设置默认会话配置
                      await self.update_session({
                        "mode": self.mode.value,
                        "voice": self.voice,
                        # 取消以下两行的注释，并将 server_commit.py 或 commit.py 中的 model 替换为 qwen3-tts-instruct-flash-realtime，即可使用指令控制功能
                        # "instructions": "Speak quickly with a noticeably rising intonation, suitable for introducing fashion products.",
                        # "optimize_instructions": true
                        "language_type": self.language_type,
                        "response_format": "pcm",
                        "sample_rate": 24000
                      })

                    async def send_event(self, event) -> None:
                      """向服务端发送事件。"""
                      event['event_id'] = "event_" + str(int(time.time() * 1000))
                      print(f"Sending event: type={event['type']}, event_id={event['event_id']}")
                      await self.ws.send(json.dumps(event))

                    async def update_session(self, config: Dict[str, Any]) -> None:
                      """更新会话配置。"""
                      event = {
                        "type": "session.update",
                        "session": config
                      }
                      print("Updating session configuration: ", event)
                      await self.send_event(event)

                    async def append_text(self, text: str) -> None:
                      """向 API 发送文本数据。"""
                      event = {
                        "type": "input_text_buffer.append",
                        "text": text
                      }
                      await self.send_event(event)

                    async def commit_text_buffer(self) -> None:
                      """提交文本缓冲区以触发处理。"""
                      event = {
                        "type": "input_text_buffer.commit"
                      }
                      await self.send_event(event)

                    async def clear_text_buffer(self) -> None:
                      """清空文本缓冲区。"""
                      event = {
                        "type": "input_text_buffer.clear"
                      }
                      await self.send_event(event)

                    async def finish_session(self) -> None:
                      """结束会话。"""
                      event = {
                        "type": "session.finish"
                      }
                      await self.send_event(event)

                    async def wait_for_response_done(self):
                      """等待 response.done 事件"""
                      if self._response_done_future:
                        await self._response_done_future

                    async def handle_messages(self) -> None:
                      """处理来自服务端的消息。"""
                      try:
                        async for message in self.ws:
                          event = json.loads(message)
                          event_type = event.get("type")

                          if event_type != "response.audio.delta":
                            print(f"Received event: {event_type}")

                          if event_type == "error":
                            print("Error: ", event.get('error', {}))
                            continue
                          elif event_type == "session.created":
                            print("Session created, ID: ", event.get('session', {}).get('id'))
                          elif event_type == "session.updated":
                            print("Session updated, ID: ", event.get('session', {}).get('id'))
                          elif event_type == "input_text_buffer.committed":
                            print("Text buffer committed, item ID: ", event.get('item_id'))
                          elif event_type == "input_text_buffer.cleared":
                            print("Text buffer cleared")
                          elif event_type == "response.created":
                            self._current_response_id = event.get("response", {}).get("id")
                            self._is_responding = True
                            # 创建新的 Future 以等待 response.done
                            self._response_done_future = asyncio.Future()
                            print("Response created, ID: ", self._current_response_id)
                          elif event_type == "response.output_item.added":
                            self._current_item_id = event.get("item", {}).get("id")
                            print("Output item added, ID: ", self._current_item_id)
                          # 处理音频增量数据
                          elif event_type == "response.audio.delta" and self.audio_callback:
                            audio_bytes = base64.b64decode(event.get("delta", ""))
                            self.audio_callback(audio_bytes)
                          elif event_type == "response.audio.done":
                            print("Audio generation completed")
                          elif event_type == "response.done":
                            self._is_responding = False
                            self._current_response_id = None
                            self._current_item_id = None
                            # 将 Future 标记为完成
                            if self._response_done_future and not self._response_done_future.done():
                              self._response_done_future.set_result(True)
                            print("Response completed")
                          elif event_type == "session.finished":
                            print("Session ended")

                      except websockets.exceptions.ConnectionClosed:
                        print("Connection closed")
                      except Exception as e:
                        print("Error handling messages: ", str(e))

                    async def close(self) -> None:
                      """关闭 WebSocket 连接。"""
                      if self.ws:
                        await self.ws.close()
                  ```
                </Accordion>
              </Step>

              <Step title="选择语音合成模式">
                Realtime API 支持两种模式：

                - **Server commit 模式**：客户端只需发送文本，服务端自动判断文本分句和合成时机。适用于无需手动控制合成过程的低延迟场景，如 GPS 导航。
                - **Commit 模式**：先将文本添加到缓冲区，再触发服务端合成指定文本。适用于需要精细控制停顿和断句的场景，如新闻播报。

                <Tabs>
                  <Tab title="Server commit 模式">
                    在 `tts_realtime_client.py` 所在目录下新建名为 `server_commit.py` 的 Python 文件，将以下代码复制到文件中：

                    <Accordion title="server_commit.py">
                      ```python
                      import os
                      import asyncio
                      import logging
                      import wave
                      from tts_realtime_client import TTSRealtimeClient, SessionMode
                      import pyaudio

                      # QwenTTS 服务配置
                      # 将 model 替换为 qwen3-tts-instruct-flash-realtime 并取消 tts_realtime_client.py 中指令相关代码的注释，即可使用指令控制功能
                      URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime"
                      # 未配置环境变量时，请替换为您的千问AI平台 API Key：API_KEY="sk-xxx"
                      API_KEY = os.getenv("DASHSCOPE_API_KEY")

                      if not API_KEY:
                        raise ValueError("Please set DASHSCOPE_API_KEY environment variable")

                      # 收集音频数据
                      _audio_chunks = []
                      # 实时播放设置
                      _AUDIO_SAMPLE_RATE = 24000
                      _audio_pyaudio = pyaudio.PyAudio()
                      _audio_stream = None  # Will be opened at runtime

                      def _audio_callback(audio_bytes: bytes):
                        """TTSRealtimeClient 音频回调：实时播放并缓存"""
                        global _audio_stream
                        if _audio_stream is not None:
                          try:
                            _audio_stream.write(audio_bytes)
                          except Exception as exc:
                            logging.error(f"PyAudio playback error: {exc}")
                        _audio_chunks.append(audio_bytes)
                        logging.info(f"Received audio chunk: {len(audio_bytes)} bytes")

                      def _save_audio_to_file(filename: str = "output.wav", sample_rate: int = 24000) -> bool:
                        """将收集到的音频数据保存为 WAV 文件"""
                        if not _audio_chunks:
                          logging.warning("No audio data to save")
                          return False

                        try:
                          audio_data = b"".join(_audio_chunks)
                          with wave.open(filename, 'wb') as wav_file:
                            wav_file.setnchannels(1)  # 单声道
                            wav_file.setsampwidth(2)  # 16-bit
                            wav_file.setframerate(sample_rate)
                            wav_file.writeframes(audio_data)
                          logging.info(f"Audio saved to: {filename}")
                          return True
                        except Exception as exc:
                          logging.error(f"Failed to save audio: {exc}")
                          return False

                      async def _produce_text(client: TTSRealtimeClient):
                        """向服务端发送文本片段"""
                        text_fragments = [
                          "千问AI平台是一个集模型开发与应用构建于一体的平台。",
                          "Both developers and business personnel can deeply participate in designing and building model applications.",
                          "You can develop a model application in just 5 minutes through simple UI operations,",
                          "or train a custom model within hours, allowing you to focus more on application innovation.",
                        ]

                        logging.info("Sending text fragments…")
                        for text in text_fragments:
                          logging.info(f"Sending fragment: {text}")
                          await client.append_text(text)
                          await asyncio.sleep(0.1)  # 片段之间的短暂延迟

                        # 等待服务端完成内部处理后再结束会话
                        await asyncio.sleep(1.0)
                        await client.finish_session()

                      async def _run_demo():
                        """运行完整示例"""
                        global _audio_stream
                        # 打开 PyAudio 输出流
                        _audio_stream = _audio_pyaudio.open(
                          format=pyaudio.paInt16,
                          channels=1,
                          rate=_AUDIO_SAMPLE_RATE,
                          output=True,
                          frames_per_buffer=1024
                        )

                        client = TTSRealtimeClient(
                          base_url=URL,
                          api_key=API_KEY,
                          voice="Cherry",
                          mode=SessionMode.SERVER_COMMIT,
                          audio_callback=_audio_callback
                        )

                        # 建立连接
                        await client.connect()

                        # 并行执行消息处理和文本发送
                        consumer_task = asyncio.create_task(client.handle_messages())
                        producer_task = asyncio.create_task(_produce_text(client))

                        await producer_task  # 等待文本发送完成

                        # 等待 response.done
                        await client.wait_for_response_done()

                        # 关闭连接并取消消费者任务
                        await client.close()
                        consumer_task.cancel()

                        # 关闭音频流
                        if _audio_stream is not None:
                          _audio_stream.stop_stream()
                          _audio_stream.close()
                        _audio_pyaudio.terminate()

                        # 保存音频数据
                        os.makedirs("outputs", exist_ok=True)
                        _save_audio_to_file(os.path.join("outputs", "qwen_tts_output.wav"))

                      def main():
                        """同步入口"""
                        logging.basicConfig(
                          level=logging.INFO,
                          format='%(asctime)s [%(levelname)s] %(message)s',
                          datefmt='%Y-%m-%d %H:%M:%S'
                        )
                        logging.info("Starting QwenTTS Realtime Client demo…")
                        asyncio.run(_run_demo())

                      if __name__ == "__main__":
                        main()
                      ```
                    </Accordion>

                    运行 `server_commit.py`，即可实时收听 Realtime API 生成的音频。
                  </Tab>

                  <Tab title="Commit 模式">
                    在 `tts_realtime_client.py` 所在目录下新建名为 `commit.py` 的 Python 文件，将以下代码复制到文件中：

                    <Accordion title="commit.py">
                      ```python
                      import os
                      import asyncio
                      import logging
                      import wave
                      from tts_realtime_client import TTSRealtimeClient, SessionMode
                      import pyaudio

                      # QwenTTS 服务配置
                      # 将 model 替换为 qwen3-tts-instruct-flash-realtime 并取消 tts_realtime_client.py 中指令相关代码的注释，即可使用指令控制功能
                      URL = "wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime"
                      # 未配置环境变量时，请替换为您的千问AI平台 API Key：API_KEY="sk-xxx"
                      API_KEY = os.getenv("DASHSCOPE_API_KEY")

                      if not API_KEY:
                        raise ValueError("Please set DASHSCOPE_API_KEY environment variable")

                      # 收集音频数据
                      _audio_chunks = []
                      _AUDIO_SAMPLE_RATE = 24000
                      _audio_pyaudio = pyaudio.PyAudio()
                      _audio_stream = None

                      def _audio_callback(audio_bytes: bytes):
                        """TTSRealtimeClient 音频回调：实时播放并缓存"""
                        global _audio_stream
                        if _audio_stream is not None:
                          try:
                            _audio_stream.write(audio_bytes)
                          except Exception as exc:
                            logging.error(f"PyAudio playback error: {exc}")
                        _audio_chunks.append(audio_bytes)
                        logging.info(f"Received audio chunk: {len(audio_bytes)} bytes")

                      def _save_audio_to_file(filename: str = "output.wav", sample_rate: int = 24000) -> bool:
                        """将收集到的音频数据保存为 WAV 文件"""
                        if not _audio_chunks:
                          logging.warning("No audio data to save")
                          return False

                        try:
                          audio_data = b"".join(_audio_chunks)
                          with wave.open(filename, 'wb') as wav_file:
                            wav_file.setnchannels(1)  # 单声道
                            wav_file.setsampwidth(2)  # 16-bit
                            wav_file.setframerate(sample_rate)
                            wav_file.writeframes(audio_data)
                          logging.info(f"Audio saved to: {filename}")
                          return True
                        except Exception as exc:
                          logging.error(f"Failed to save audio: {exc}")
                          return False

                      async def _user_input_loop(client: TTSRealtimeClient):
                        """Continuously get user input and send text. When user enters empty text, send commit event and end current session"""
                        print("Enter text (press Enter directly to send commit event and end current session, press Ctrl+C or Ctrl+D to exit entire program):")

                        while True:
                          try:
                            user_text = input("> ")
                            if not user_text:  # User entered empty input
                              # Empty input signifies end of conversation: submit buffer -> end session -> break loop
                              logging.info("Empty input, sending commit event and ending current session")
                              await client.commit_text_buffer()
                              # Wait briefly for server to process commit to prevent losing audio from premature session end
                              await asyncio.sleep(0.3)
                              await client.finish_session()
                              break  # Exit user input loop directly, no need to press Enter again
                            else:
                              logging.info(f"Sending text: {user_text}")
                              await client.append_text(user_text)

                          except EOFError:  # User pressed Ctrl+D
                            break
                          except KeyboardInterrupt:  # User pressed Ctrl+C
                            break

                        # End session
                        logging.info("Ending session...")
                      async def _run_demo():
                        """运行完整示例"""
                        global _audio_stream
                        # 打开 PyAudio 输出流
                        _audio_stream = _audio_pyaudio.open(
                          format=pyaudio.paInt16,
                          channels=1,
                          rate=_AUDIO_SAMPLE_RATE,
                          output=True,
                          frames_per_buffer=1024
                        )

                        client = TTSRealtimeClient(
                          base_url=URL,
                          api_key=API_KEY,
                          voice="Cherry",
                          mode=SessionMode.COMMIT,  # Change to COMMIT mode
                          audio_callback=_audio_callback
                        )

                        # 建立连接
                        await client.connect()

                        # Execute message handling and user input in parallel
                        consumer_task = asyncio.create_task(client.handle_messages())
                        producer_task = asyncio.create_task(_user_input_loop(client))

                        await producer_task  # Wait for user input to complete

                        # 等待 response.done
                        await client.wait_for_response_done()

                        # 关闭连接并取消消费者任务
                        await client.close()
                        consumer_task.cancel()

                        # 关闭音频流
                        if _audio_stream is not None:
                          _audio_stream.stop_stream()
                          _audio_stream.close()
                        _audio_pyaudio.terminate()

                        # 保存音频数据
                        os.makedirs("outputs", exist_ok=True)
                        _save_audio_to_file(os.path.join("outputs", "qwen_tts_output.wav"))

                      def main():
                        logging.basicConfig(
                          level=logging.INFO,
                          format='%(asctime)s [%(levelname)s] %(message)s',
                          datefmt='%Y-%m-%d %H:%M:%S'
                        )
                        logging.info("Starting QwenTTS Realtime Client demo…")
                        asyncio.run(_run_demo())

                      if __name__ == "__main__":
                        main()
                      ```
                    </Accordion>

                    运行 `commit.py`，输入多段文本进行合成。直接按回车（不输入文本）即可通过扬声器收听 Realtime API 返回的音频。
                  </Tab>
                </Tabs>
              </Step>
            </Steps>
          </Tab>
        </Tabs>
      </Tab>

      <Tab title="使用复刻音色">
        声音复刻服务不提供预览音频，请通过语音合成接口测试和评估效果。建议先使用短文本进行初步测试。

        本示例基于"server commit 模式"代码修改，将 `voice` 参数替换为复刻音色。

        - **关键原则**：声音复刻模型（`target_model`）必须与语音合成模型（`model`）匹配，否则合成会失败。
        - 示例使用本地音频文件 `voice.mp3` 进行声音复刻，运行代码时请替换为实际文件。

        <Tabs>
          <Tab title="Python">
            ```python
            # coding=utf-8
            # Installation instructions for pyaudio:
            # APPLE Mac OS X
            #   brew install portaudio
            #   pip install pyaudio
            # Debian/Ubuntu
            #   sudo apt-get install python-pyaudio python3-pyaudio
            #   or
            #   pip install pyaudio
            # CentOS
            #   sudo yum install -y portaudio portaudio-devel && pip install pyaudio
            # Microsoft Windows
            #   python -m pip install pyaudio

            import pyaudio
            import os
            import requests
            import base64
            import pathlib
            import threading
            import time
            import dashscope  # DashScope Python SDK version must be at least 1.23.9
            from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat

            # ======= Constants =======
            DEFAULT_TARGET_MODEL = "qwen3-tts-vc-realtime-2026-01-15"  # Use the same model for voice cloning and speech synthesis
            DEFAULT_PREFERRED_NAME = "guanyu"
            DEFAULT_AUDIO_MIME_TYPE = "audio/mpeg"
            VOICE_FILE_PATH = "voice.mp3"  # Relative path to local audio file for voice cloning

            TEXT_TO_SYNTHESIZE = [
              'Right? I really love this kind of supermarket,',
              'especially during Chinese New Year',
              'when I go shopping',
              'I feel',
              'super super happy!',
              'I want to buy so many things!'
            ]

            def create_voice(file_path: str,
                      target_model: str = DEFAULT_TARGET_MODEL,
                      preferred_name: str = DEFAULT_PREFERRED_NAME,
                      audio_mime_type: str = DEFAULT_AUDIO_MIME_TYPE) -> str:
              """
              Create voice and return voice parameter
              """
              # Replace with your 千问AI平台 API Key if environment variable is not configured: api_key = "sk-xxx"
              api_key = os.getenv("DASHSCOPE_API_KEY")

              file_path_obj = pathlib.Path(file_path)
              if not file_path_obj.exists():
                raise FileNotFoundError(f"Audio file not found: {file_path}")

              base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
              data_uri = f"data:{audio_mime_type};base64,{base64_str}"

              url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
              payload = {
                "model": "qwen-voice-enrollment", # Do not modify this value
                "input": {
                  "action": "create",
                  "target_model": target_model,
                  "preferred_name": preferred_name,
                  "audio": {"data": data_uri}
                }
              }
              headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
              }

              resp = requests.post(url, json=payload, headers=headers)
              if resp.status_code != 200:
                raise RuntimeError(f"Voice creation failed: {resp.status_code}, {resp.text}")

              try:
                return resp.json()["output"]["voice"]
              except (KeyError, ValueError) as e:
                raise RuntimeError(f"Failed to parse voice response: {e}")

            def init_dashscope_api_key():
              """
              Initialize DashScope SDK API Key
              """
              # Replace with your 千问AI平台 API Key if environment variable is not configured: dashscope.api_key = "sk-xxx"
              dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

            # ======= Callback class =======
            class MyCallback(QwenTtsRealtimeCallback):
              """
              Custom TTS streaming callback
              """
              def __init__(self):
                self.complete_event = threading.Event()
                self._player = pyaudio.PyAudio()
                self._stream = self._player.open(
                  format=pyaudio.paInt16, channels=1, rate=24000, output=True
                )

              def on_open(self) -> None:
                print('[TTS] Connection established')

              def on_close(self, close_status_code, close_msg) -> None:
                self._stream.stop_stream()
                self._stream.close()
                self._player.terminate()
                print(f'[TTS] Connection closed code={close_status_code}, msg={close_msg}')

              def on_event(self, response: dict) -> None:
                try:
                  event_type = response.get('type', '')
                  if event_type == 'session.created':
                    print(f'[TTS] Session started: {response["session"]["id"]}')
                  elif event_type == 'response.audio.delta':
                    audio_data = base64.b64decode(response['delta'])
                    self._stream.write(audio_data)
                  elif event_type == 'response.done':
                    print(f'[TTS] Response completed, Response ID: {qwen_tts_realtime.get_last_response_id()}')
                  elif event_type == 'session.finished':
                    print('[TTS] Session ended')
                    self.complete_event.set()
                except Exception as e:
                  print(f'[Error] Error handling callback event: {e}')

              def wait_for_finished(self):
                self.complete_event.wait()

            # ======= Main execution logic =======
            if __name__ == '__main__':
              init_dashscope_api_key()
              print('[System] Initializing Qwen TTS Realtime ...')

              callback = MyCallback()
              qwen_tts_realtime = QwenTtsRealtime(
                model=DEFAULT_TARGET_MODEL,
                callback=callback,
                url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
              )
              qwen_tts_realtime.connect()

              qwen_tts_realtime.update_session(
                voice=create_voice(VOICE_FILE_PATH), # Replace voice parameter with cloned custom voice
                response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
                mode='server_commit'
              )

              for text_chunk in TEXT_TO_SYNTHESIZE:
                print(f'[Sending text]: {text_chunk}')
                qwen_tts_realtime.append_text(text_chunk)
                time.sleep(0.1)

              qwen_tts_realtime.finish()
              callback.wait_for_finished()

              print(f'[Metric] session_id={qwen_tts_realtime.get_session_id()}, '
                      f'first_audio_delay={qwen_tts_realtime.get_first_audio_delay()}s')

            ```
          </Tab>

          <Tab title="Java">
            需要导入 Gson 依赖。如果使用 Maven 或 Gradle，请按如下方式添加依赖：

            <Tabs>
              <Tab title="Maven">
                在 `pom.xml` 中添加以下内容：

                ```xml
                <!-- https://mvnrepository.com/artifact/com.google.code.gson/gson -->
                <dependency>
                  <groupId>com.google.code.gson</groupId>
                  <artifactId>gson</artifactId>
                  <version>2.13.1</version>
                </dependency>
                ```
              </Tab>

              <Tab title="Gradle">
                在 `build.gradle` 中添加以下内容：

                ```gradle
                // https://mvnrepository.com/artifact/com.google.code.gson/gson
                implementation("com.google.code.gson:gson:2.13.1")
                ```
              </Tab>
            </Tabs>

            ```java
            import com.alibaba.dashscope.audio.qwen_tts_realtime.*;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.google.gson.Gson;
            import com.google.gson.JsonObject;

            import javax.sound.sampled.*;
            import java.io.*;
            import java.net.HttpURLConnection;
            import java.net.URL;
            import java.nio.file.*;
            import java.nio.charset.StandardCharsets;
            import java.util.Base64;
            import java.util.Queue;
            import java.util.concurrent.CountDownLatch;
            import java.util.concurrent.atomic.AtomicReference;
            import java.util.concurrent.ConcurrentLinkedQueue;
            import java.util.concurrent.atomic.AtomicBoolean;

            public class Main {
              // ===== Constants =====
              // Use the same model for voice cloning and speech synthesis
              private static final String TARGET_MODEL = "qwen3-tts-vc-realtime-2026-01-15";
              private static final String PREFERRED_NAME = "guanyu";
              // Relative path to local audio file for voice cloning
              private static final String AUDIO_FILE = "voice.mp3";
              private static final String AUDIO_MIME_TYPE = "audio/mpeg";
              private static String[] textToSynthesize = {
                  "Right? I really love this kind of supermarket",
                  "especially during Chinese New Year",
                  "when I go shopping",
                  "I feel",
                  "super super happy!",
                  "I want to buy so many things!"
              };

              // Generate data URI
              public static String toDataUrl(String filePath) throws IOException {
                byte[] bytes = Files.readAllBytes(Paths.get(filePath));
                String encoded = Base64.getEncoder().encodeToString(bytes);
                return "data:" + AUDIO_MIME_TYPE + ";base64," + encoded;
              }

              // Call API to create voice
              public static String createVoice() throws Exception {
                // Replace with your 千问AI平台 API Key if environment variable is not configured: String apiKey = "sk-xxx"
                String apiKey = System.getenv("DASHSCOPE_API_KEY");

                String jsonPayload =
                    "{"
                        + "\"model\": \"qwen-voice-enrollment\"," // Do not modify this value
                        + "\"input\": {"
                        +     "\"action\": \"create\","
                        +     "\"target_model\": \"" + TARGET_MODEL + "\","
                        +     "\"preferred_name\": \"" + PREFERRED_NAME + "\","
                        +     "\"audio\": {"
                        +         "\"data\": \"" + toDataUrl(AUDIO_FILE) + "\""
                        +     "}"
                        + "}"
                        + "}";

                HttpURLConnection con = (HttpURLConnection) new URL("https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization").openConnection();
                con.setRequestMethod("POST");
                con.setRequestProperty("Authorization", "Bearer " + apiKey);
                con.setRequestProperty("Content-Type", "application/json");
                con.setDoOutput(true);

                try (OutputStream os = con.getOutputStream()) {
                  os.write(jsonPayload.getBytes(StandardCharsets.UTF_8));
                }

                int status = con.getResponseCode();
                System.out.println("HTTP status code: " + status);

                try (BufferedReader br = new BufferedReader(
                    new InputStreamReader(status >= 200 && status < 300 ? con.getInputStream() : con.getErrorStream(),
                        StandardCharsets.UTF_8))) {
                  StringBuilder response = new StringBuilder();
                  String line;
                  while ((line = br.readLine()) != null) {
                    response.append(line);
                  }
                  System.out.println("Response content: " + response);

                  if (status == 200) {
                    JsonObject jsonObj = new Gson().fromJson(response.toString(), JsonObject.class);
                    return jsonObj.getAsJsonObject("output").get("voice").getAsString();
                  }
                  throw new IOException("Voice creation failed: " + status + " - " + response);
                }
              }

              // 实时 PCM 音频播放器类
              public static class RealtimePcmPlayer {
                private int sampleRate;
                private SourceDataLine line;
                private AudioFormat audioFormat;
                private Thread decoderThread;
                private Thread playerThread;
                private AtomicBoolean stopped = new AtomicBoolean(false);
                private Queue<String> b64AudioBuffer = new ConcurrentLinkedQueue<>();
                private Queue<byte[]> RawAudioBuffer = new ConcurrentLinkedQueue<>();

                // Constructor to initialize audio format and audio line
                public RealtimePcmPlayer(int sampleRate) throws LineUnavailableException {
                  this.sampleRate = sampleRate;
                  this.audioFormat = new AudioFormat(this.sampleRate, 16, 1, true, false);
                  DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);
                  line = (SourceDataLine) AudioSystem.getLine(info);
                  line.open(audioFormat);
                  line.start();
                  decoderThread = new Thread(new Runnable() {
                    @Override
                    public void run() {
                      while (!stopped.get()) {
                        String b64Audio = b64AudioBuffer.poll();
                        if (b64Audio != null) {
                          byte[] rawAudio = Base64.getDecoder().decode(b64Audio);
                          RawAudioBuffer.add(rawAudio);
                        } else {
                          try {
                            Thread.sleep(100);
                          } catch (InterruptedException e) {
                            throw new RuntimeException(e);
                          }
                        }
                      }
                    }
                  });
                  playerThread = new Thread(new Runnable() {
                    @Override
                    public void run() {
                      while (!stopped.get()) {
                        byte[] rawAudio = RawAudioBuffer.poll();
                        if (rawAudio != null) {
                          try {
                            playChunk(rawAudio);
                          } catch (IOException e) {
                            throw new RuntimeException(e);
                          } catch (InterruptedException e) {
                            throw new RuntimeException(e);
                          }
                        } else {
                          try {
                            Thread.sleep(100);
                          } catch (InterruptedException e) {
                            throw new RuntimeException(e);
                          }
                        }
                      }
                    }
                  });
                  decoderThread.start();
                  playerThread.start();
                }

                // Play an audio chunk and block until playback completes
                private void playChunk(byte[] chunk) throws IOException, InterruptedException {
                  if (chunk == null || chunk.length == 0) return;

                  int bytesWritten = 0;
                  while (bytesWritten < chunk.length) {
                    bytesWritten += line.write(chunk, bytesWritten, chunk.length - bytesWritten);
                  }
                  int audioLength = chunk.length / (this.sampleRate*2/1000);
                  // Wait for audio in buffer to finish playing
                  Thread.sleep(audioLength - 10);
                }

                public void write(String b64Audio) {
                  b64AudioBuffer.add(b64Audio);
                }

                public void cancel() {
                  b64AudioBuffer.clear();
                  RawAudioBuffer.clear();
                }

                public void waitForComplete() throws InterruptedException {
                  while (!b64AudioBuffer.isEmpty() || !RawAudioBuffer.isEmpty()) {
                    Thread.sleep(100);
                  }
                  line.drain();
                }

                public void shutdown() throws InterruptedException {
                  stopped.set(true);
                  decoderThread.join();
                  playerThread.join();
                  if (line != null && line.isRunning()) {
                    line.drain();
                    line.close();
                  }
                }
              }

              public static void main(String[] args) throws Exception {
                QwenTtsRealtimeParam param = QwenTtsRealtimeParam.builder()
                    .model(TARGET_MODEL)
                    .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                    // Replace with your 千问AI平台 API Key if environment variable is not configured: .apikey("sk-xxx")
                    .apikey(System.getenv("DASHSCOPE_API_KEY"))
                    .build();
                AtomicReference<CountDownLatch> completeLatch = new AtomicReference<>(new CountDownLatch(1));
                final AtomicReference<QwenTtsRealtime> qwenTtsRef = new AtomicReference<>(null);

                // Create real-time audio player instance
                RealtimePcmPlayer audioPlayer = new RealtimePcmPlayer(24000);

                QwenTtsRealtime qwenTtsRealtime = new QwenTtsRealtime(param, new QwenTtsRealtimeCallback() {
                  @Override
                  public void onOpen() {
                    // Handle connection established
                  }
                  @Override
                  public void onEvent(JsonObject message) {
                    String type = message.get("type").getAsString();
                    switch(type) {
                      case "session.created":
                        // Handle session created
                        break;
                      case "response.audio.delta":
                        String recvAudioB64 = message.get("delta").getAsString();
                        // Play audio in real time
                        audioPlayer.write(recvAudioB64);
                        break;
                      case "response.done":
                        // Handle response completed
                        break;
                      case "session.finished":
                        // Handle session finished
                        completeLatch.get().countDown();
                      default:
                        break;
                    }
                  }
                  @Override
                  public void onClose(int code, String reason) {
                    // Handle connection closed
                  }
                });
                qwenTtsRef.set(qwenTtsRealtime);
                try {
                  qwenTtsRealtime.connect();
                } catch (NoApiKeyException e) {
                  throw new RuntimeException(e);
                }
                QwenTtsRealtimeConfig config = QwenTtsRealtimeConfig.builder()
                    .voice(createVoice()) // Replace voice parameter with cloned custom voice
                    .responseFormat(QwenTtsRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT)
                    .mode("server_commit")
                    .build();
                qwenTtsRealtime.updateSession(config);
                for (String text:textToSynthesize) {
                  qwenTtsRealtime.appendText(text);
                  Thread.sleep(100);
                }
                qwenTtsRealtime.finish();
                completeLatch.get().await();

                // Wait for audio playback to complete and shut down player
                audioPlayer.waitForComplete();
                audioPlayer.shutdown();
                System.exit(0);
              }
            }
            ```
          </Tab>
        </Tabs>
      </Tab>

      <Tab title="使用设计音色">
        声音设计功能会返回预览音频数据。请先试听预览音频，确认效果满足预期后再用于语音合成。

        <Steps>
          <Step title="生成自定义音色并预览效果">
            如果对效果满意，请继续下一步；否则重新生成。

            <Tabs>
              <Tab title="Python">
                ```python
                import requests
                import base64
                import os

                def create_voice_and_play():
                  # If the environment variable is not set, replace the following line with your API key: api_key = "sk-xxx"
                  api_key = os.getenv("DASHSCOPE_API_KEY")

                  if not api_key:
                    print("Error: DASHSCOPE_API_KEY environment variable not found. Please set the API key first.")
                    return None, None, None

                  # Prepare request data
                  headers = {
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json"
                  }

                  data = {
                    "model": "qwen-voice-design",
                    "input": {
                      "action": "create",
                      "target_model": "qwen3-tts-vd-realtime-2026-01-15",
                      "voice_prompt": "A composed middle-aged male announcer with a deep, rich and magnetic voice, a steady speaking speed and clear articulation, is suitable for news broadcasting or documentary commentary.",
                      "preview_text": "Dear listeners, hello everyone. Welcome to the evening news.",
                      "preferred_name": "announcer",
                      "language": "en"
                    },
                    "parameters": {
                      "sample_rate": 24000,
                      "response_format": "wav"
                    }
                  }

                  url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"

                  try:
                    # Send the request
                    response = requests.post(
                      url,
                      headers=headers,
                      json=data,
                      timeout=60  # Add a timeout setting
                    )

                    if response.status_code == 200:
                      result = response.json()

                      # Get the voice name
                      voice_name = result["output"]["voice"]
                      print(f"Voice name: {voice_name}")

                      # Get the preview audio data
                      base64_audio = result["output"]["preview_audio"]["data"]

                      # Decode the Base64 audio data
                      audio_bytes = base64.b64decode(base64_audio)

                      # Save the audio file locally
                      filename = f"{voice_name}_preview.wav"

                      # Write the audio data to a local file
                      with open(filename, 'wb') as f:
                        f.write(audio_bytes)

                      print(f"Audio saved to local file: {filename}")
                      print(f"File path: {os.path.abspath(filename)}")

                      return voice_name, audio_bytes, filename
                    else:
                      print(f"Request failed with status code: {response.status_code}")
                      print(f"Response content: {response.text}")
                      return None, None, None

                  except requests.exceptions.RequestException as e:
                    print(f"A network request error occurred: {e}")
                    return None, None, None
                  except KeyError as e:
                    print(f"Response data format error, missing required field: {e}")
                    print(f"Response content: {response.text if 'response' in locals() else 'No response'}")
                    return None, None, None
                  except Exception as e:
                    print(f"An unknown error occurred: {e}")
                    return None, None, None

                if __name__ == "__main__":
                  print("Starting to create voice...")
                  voice_name, audio_data, saved_filename = create_voice_and_play()

                  if voice_name:
                    print(f"\nSuccessfully created voice '{voice_name}'")
                    print(f"Audio file saved as: '{saved_filename}'")
                    print(f"File size: {os.path.getsize(saved_filename)} bytes")
                  else:
                    print("\nVoice creation failed")
                ```
              </Tab>

              <Tab title="Java">
                需要导入 Gson 依赖。如果使用 Maven 或 Gradle，请按如下方式添加依赖：

                <Tabs>
                  <Tab title="Maven">
                    在 `pom.xml` 中添加以下内容：

                    ```xml
                    <!-- https://mvnrepository.com/artifact/com.google.code.gson/gson -->
                    <dependency>
                      <groupId>com.google.code.gson</groupId>
                      <artifactId>gson</artifactId>
                      <version>2.13.1</version>
                    </dependency>
                    ```
                  </Tab>

                  <Tab title="Gradle">
                    在 `build.gradle` 中添加以下内容：

                    ```gradle
                    // https://mvnrepository.com/artifact/com.google.code.gson/gson
                    implementation("com.google.code.gson:gson:2.13.1")
                    ```
                  </Tab>
                </Tabs>

                ```java
                import com.google.gson.JsonObject;
                import com.google.gson.JsonParser;
                import java.io.*;
                import java.net.HttpURLConnection;
                import java.net.URL;
                import java.util.Base64;

                public class Main {
                  public static void main(String[] args) {
                    Main example = new Main();
                    example.createVoice();
                  }

                  public void createVoice() {
                    // If the environment variable is not set, replace the following line with your API key: String apiKey = "sk-xxx"
                    String apiKey = System.getenv("DASHSCOPE_API_KEY");

                    // Create the JSON request body string
                    String jsonBody = "{\n" +
                        "    \"model\": \"qwen-voice-design\",\n" +
                        "    \"input\": {\n" +
                        "        \"action\": \"create\",\n" +
                        "        \"target_model\": \"qwen3-tts-vd-realtime-2026-01-15\",\n" +
                        "        \"voice_prompt\": \"A composed middle-aged male announcer with a deep, rich and magnetic voice, a steady speaking speed and clear articulation, is suitable for news broadcasting or documentary commentary.\",\n" +
                        "        \"preview_text\": \"Dear listeners, hello everyone. Welcome to the evening news.\",\n" +
                        "        \"preferred_name\": \"announcer\",\n" +
                        "        \"language\": \"en\"\n" +
                        "    },\n" +
                        "    \"parameters\": {\n" +
                        "        \"sample_rate\": 24000,\n" +
                        "        \"response_format\": \"wav\"\n" +
                        "    }\n" +
                        "}";

                    HttpURLConnection connection = null;
                    try {
                      URL url = new URL("https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization");
                      connection = (HttpURLConnection) url.openConnection();

                      // Set the request method and headers
                      connection.setRequestMethod("POST");
                      connection.setRequestProperty("Authorization", "Bearer " + apiKey);
                      connection.setRequestProperty("Content-Type", "application/json");
                      connection.setDoOutput(true);
                      connection.setDoInput(true);

                      // Send the request body
                      try (OutputStream os = connection.getOutputStream()) {
                        byte[] input = jsonBody.getBytes("UTF-8");
                        os.write(input, 0, input.length);
                        os.flush();
                      }

                      // Get the response
                      int responseCode = connection.getResponseCode();
                      if (responseCode == HttpURLConnection.HTTP_OK) {
                        // Read the response content
                        StringBuilder response = new StringBuilder();
                        try (BufferedReader br = new BufferedReader(
                            new InputStreamReader(connection.getInputStream(), "UTF-8"))) {
                          String responseLine;
                          while ((responseLine = br.readLine()) != null) {
                            response.append(responseLine.trim());
                          }
                        }

                        // Parse the JSON response
                        JsonObject jsonResponse = JsonParser.parseString(response.toString()).getAsJsonObject();
                        JsonObject outputObj = jsonResponse.getAsJsonObject("output");
                        JsonObject previewAudioObj = outputObj.getAsJsonObject("preview_audio");

                        // Get the voice name
                        String voiceName = outputObj.get("voice").getAsString();
                        System.out.println("Voice name: " + voiceName);

                        // Get the Base64-encoded audio data
                        String base64Audio = previewAudioObj.get("data").getAsString();

                        // Decode the Base64 audio data
                        byte[] audioBytes = Base64.getDecoder().decode(base64Audio);

                        // Save the audio to a local file
                        String filename = voiceName + "_preview.wav";
                        saveAudioToFile(audioBytes, filename);

                        System.out.println("Audio saved to local file: " + filename);

                      } else {
                        // Read the error response
                        StringBuilder errorResponse = new StringBuilder();
                        try (BufferedReader br = new BufferedReader(
                            new InputStreamReader(connection.getErrorStream(), "UTF-8"))) {
                          String responseLine;
                          while ((responseLine = br.readLine()) != null) {
                            errorResponse.append(responseLine.trim());
                          }
                        }

                        System.out.println("Request failed with status code: " + responseCode);
                        System.out.println("Error response: " + errorResponse.toString());
                      }

                    } catch (Exception e) {
                      System.err.println("An error occurred during the request: " + e.getMessage());
                      e.printStackTrace();
                    } finally {
                      if (connection != null) {
                        connection.disconnect();
                      }
                    }
                  }

                  private void saveAudioToFile(byte[] audioBytes, String filename) {
                    try {
                      File file = new File(filename);
                      try (FileOutputStream fos = new FileOutputStream(file)) {
                        fos.write(audioBytes);
                      }
                      System.out.println("Audio saved to: " + file.getAbsolutePath());
                    } catch (IOException e) {
                      System.err.println("An error occurred while saving the audio file: " + e.getMessage());
                      e.printStackTrace();
                    }
                  }
                }
                ```
              </Tab>
            </Tabs>
          </Step>

          <Step title="使用自定义音色进行语音合成">
            本示例参考 DashScope SDK 使用系统音色进行语音合成的"server commit 模式"示例代码，将 `voice` 参数替换为声音设计生成的自定义音色。

            **关键原则**：声音设计使用的模型（`target_model`）必须与后续语音合成使用的模型（`model`）相同，否则合成会失败。

            <Tabs>
              <Tab title="Python">
                ```python
                # coding=utf-8
                # Installation instructions for pyaudio:
                # APPLE Mac OS X
                #   brew install portaudio
                #   pip install pyaudio
                # Debian/Ubuntu
                #   sudo apt-get install python-pyaudio python3-pyaudio
                #   or
                #   pip install pyaudio
                # CentOS
                #   sudo yum install -y portaudio portaudio-devel && pip install pyaudio
                # Microsoft Windows
                #   python -m pip install pyaudio

                import pyaudio
                import os
                import base64
                import threading
                import time
                import dashscope  # DashScope Python SDK version must be 1.23.9 or later
                from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat

                # ======= Constant Configuration =======
                TEXT_TO_SYNTHESIZE = [
                  'Right? I really like this kind of supermarket,',
                  'especially during the New Year.',
                  'Going to the supermarket',
                  'just makes me feel',
                  'super, super happy!',
                  'I want to buy so many things!'
                ]

                def init_dashscope_api_key():
                  """
                  Initialize the API Key for the DashScope SDK.
                  """
                  # If the environment variable is not set, replace the following line with your API key: dashscope.api_key = "sk-xxx"
                  dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

                # ======= Callback Class =======
                class MyCallback(QwenTtsRealtimeCallback):
                  """
                  Custom TTS streaming callback.
                  """
                  def __init__(self):
                    self.complete_event = threading.Event()
                    self._player = pyaudio.PyAudio()
                    self._stream = self._player.open(
                      format=pyaudio.paInt16, channels=1, rate=24000, output=True
                    )

                  def on_open(self) -> None:
                    print('[TTS] Connection established')

                  def on_close(self, close_status_code, close_msg) -> None:
                    self._stream.stop_stream()
                    self._stream.close()
                    self._player.terminate()
                    print(f'[TTS] Connection closed, code={close_status_code}, msg={close_msg}')

                  def on_event(self, response: dict) -> None:
                    try:
                      event_type = response.get('type', '')
                      if event_type == 'session.created':
                        print(f'[TTS] Session started: {response["session"]["id"]}')
                      elif event_type == 'response.audio.delta':
                        audio_data = base64.b64decode(response['delta'])
                        self._stream.write(audio_data)
                      elif event_type == 'response.done':
                        print(f'[TTS] Response complete, Response ID: {qwen_tts_realtime.get_last_response_id()}')
                      elif event_type == 'session.finished':
                        print('[TTS] Session finished')
                        self.complete_event.set()
                    except Exception as e:
                      print(f'[Error] Exception processing callback event: {e}')

                  def wait_for_finished(self):
                    self.complete_event.wait()

                # ======= Main Execution Logic =======
                if __name__ == '__main__':
                  init_dashscope_api_key()
                  print('[System] Initializing Qwen TTS Realtime ...')

                  callback = MyCallback()
                  qwen_tts_realtime = QwenTtsRealtime(
                    # Use the same model for voice design and speech synthesis
                    model="qwen3-tts-vd-realtime-2026-01-15",
                    callback=callback,
                    url='wss://dashscope.aliyuncs.com/api-ws/v1/realtime'
                  )
                  qwen_tts_realtime.connect()

                  qwen_tts_realtime.update_session(
                    voice="myvoice", # Replace the voice parameter with the custom voice generated by voice design
                    response_format=AudioFormat.PCM_24000HZ_MONO_16BIT,
                    mode='server_commit'
                  )

                  for text_chunk in TEXT_TO_SYNTHESIZE:
                    print(f'[Sending text]: {text_chunk}')
                    qwen_tts_realtime.append_text(text_chunk)
                    time.sleep(0.1)

                  qwen_tts_realtime.finish()
                  callback.wait_for_finished()

                  print(f'[Metric] session_id={qwen_tts_realtime.get_session_id()}, '
                          f'first_audio_delay={qwen_tts_realtime.get_first_audio_delay()}s')
                ```
              </Tab>

              <Tab title="Java">
                ```java
                import com.alibaba.dashscope.audio.qwen_tts_realtime.*;
                import com.alibaba.dashscope.exception.NoApiKeyException;
                import com.google.gson.JsonObject;

                import javax.sound.sampled.*;
                import java.io.*;
                import java.util.Base64;
                import java.util.Queue;
                import java.util.concurrent.CountDownLatch;
                import java.util.concurrent.atomic.AtomicReference;
                import java.util.concurrent.ConcurrentLinkedQueue;
                import java.util.concurrent.atomic.AtomicBoolean;

                public class Main {
                  // ===== Constant Definitions =====
                  private static String[] textToSynthesize = {
                      "Right? I really like this kind of supermarket,",
                      "especially during the New Year.",
                      "Going to the supermarket",
                      "just makes me feel",
                      "super, super happy!",
                      "I want to buy so many things!"
                  };

                  // Real-time audio player class
                  public static class RealtimePcmPlayer {
                    private int sampleRate;
                    private SourceDataLine line;
                    private AudioFormat audioFormat;
                    private Thread decoderThread;
                    private Thread playerThread;
                    private AtomicBoolean stopped = new AtomicBoolean(false);
                    private Queue<String> b64AudioBuffer = new ConcurrentLinkedQueue<>();
                    private Queue<byte[]> RawAudioBuffer = new ConcurrentLinkedQueue<>();

                    // Constructor initializes audio format and audio line
                    public RealtimePcmPlayer(int sampleRate) throws LineUnavailableException {
                      this.sampleRate = sampleRate;
                      this.audioFormat = new AudioFormat(this.sampleRate, 16, 1, true, false);
                      DataLine.Info info = new DataLine.Info(SourceDataLine.class, audioFormat);
                      line = (SourceDataLine) AudioSystem.getLine(info);
                      line.open(audioFormat);
                      line.start();
                      decoderThread = new Thread(new Runnable() {
                        @Override
                        public void run() {
                          while (!stopped.get()) {
                            String b64Audio = b64AudioBuffer.poll();
                            if (b64Audio != null) {
                              byte[] rawAudio = Base64.getDecoder().decode(b64Audio);
                              RawAudioBuffer.add(rawAudio);
                            } else {
                              try {
                                Thread.sleep(100);
                              } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                              }
                            }
                          }
                        }
                      });
                      playerThread = new Thread(new Runnable() {
                        @Override
                        public void run() {
                          while (!stopped.get()) {
                            byte[] rawAudio = RawAudioBuffer.poll();
                            if (rawAudio != null) {
                              try {
                                playChunk(rawAudio);
                              } catch (IOException e) {
                                throw new RuntimeException(e);
                              } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                              }
                            } else {
                              try {
                                Thread.sleep(100);
                              } catch (InterruptedException e) {
                                throw new RuntimeException(e);
                              }
                            }
                          }
                        }
                      });
                      decoderThread.start();
                      playerThread.start();
                    }

                    // Plays an audio chunk and blocks until playback is complete
                    private void playChunk(byte[] chunk) throws IOException, InterruptedException {
                      if (chunk == null || chunk.length == 0) return;

                      int bytesWritten = 0;
                      while (bytesWritten < chunk.length) {
                        bytesWritten += line.write(chunk, bytesWritten, chunk.length - bytesWritten);
                      }
                      int audioLength = chunk.length / (this.sampleRate*2/1000);
                      // Wait for the audio in the buffer to finish playing
                      Thread.sleep(audioLength - 10);
                    }

                    public void write(String b64Audio) {
                      b64AudioBuffer.add(b64Audio);
                    }

                    public void cancel() {
                      b64AudioBuffer.clear();
                      RawAudioBuffer.clear();
                    }

                    public void waitForComplete() throws InterruptedException {
                      while (!b64AudioBuffer.isEmpty() || !RawAudioBuffer.isEmpty()) {
                        Thread.sleep(100);
                      }
                      line.drain();
                    }

                    public void shutdown() throws InterruptedException {
                      stopped.set(true);
                      decoderThread.join();
                      playerThread.join();
                      if (line != null && line.isRunning()) {
                        line.drain();
                        line.close();
                      }
                    }
                  }

                  public static void main(String[] args) throws Exception {
                    QwenTtsRealtimeParam param = QwenTtsRealtimeParam.builder()
                        // Use the same model for voice design and speech synthesis
                        .model("qwen3-tts-vd-realtime-2026-01-15")
                        .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
                        // If the environment variable is not set, replace the following line with your API key: .apikey("sk-xxx")
                        .apikey(System.getenv("DASHSCOPE_API_KEY"))
                        .build();
                    AtomicReference<CountDownLatch> completeLatch = new AtomicReference<>(new CountDownLatch(1));
                    final AtomicReference<QwenTtsRealtime> qwenTtsRef = new AtomicReference<>(null);

                    // Create a real-time audio player instance
                    RealtimePcmPlayer audioPlayer = new RealtimePcmPlayer(24000);

                    QwenTtsRealtime qwenTtsRealtime = new QwenTtsRealtime(param, new QwenTtsRealtimeCallback() {
                      @Override
                      public void onOpen() {
                        // Handling for when the connection is established
                      }
                      @Override
                      public void onEvent(JsonObject message) {
                        String type = message.get("type").getAsString();
                        switch(type) {
                          case "session.created":
                            // Handling for when the session is created
                            break;
                          case "response.audio.delta":
                            String recvAudioB64 = message.get("delta").getAsString();
                            // Play audio in real time
                            audioPlayer.write(recvAudioB64);
                            break;
                          case "response.done":
                            // Handling for when the response is complete
                            break;
                          case "session.finished":
                            // Handling for when the session is finished
                            completeLatch.get().countDown();
                          default:
                            break;
                        }
                      }
                      @Override
                      public void onClose(int code, String reason) {
                        // Handling for when the connection is closed
                      }
                    });
                    qwenTtsRef.set(qwenTtsRealtime);
                    try {
                      qwenTtsRealtime.connect();
                    } catch (NoApiKeyException e) {
                      throw new RuntimeException(e);
                    }
                    QwenTtsRealtimeConfig config = QwenTtsRealtimeConfig.builder()
                        .voice("myvoice") // Replace the voice parameter with the custom voice generated by voice design
                        .responseFormat(QwenTtsRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT)
                        .mode("server_commit")
                        .build();
                    qwenTtsRealtime.updateSession(config);
                    for (String text:textToSynthesize) {
                      qwenTtsRealtime.appendText(text);
                      Thread.sleep(100);
                    }
                    qwenTtsRealtime.finish();
                    completeLatch.get().await();

                    // Wait for audio playback to complete and shut down the player
                    audioPlayer.waitForComplete();
                    audioPlayer.shutdown();
                    System.exit(0);
                  }
                }
                ```
              </Tab>
            </Tabs>
          </Step>
        </Steps>
      </Tab>
    </Tabs>

    更多示例代码请参见 [GitHub](https://github.com/aliyun/alibabacloud-bailian-speech-demo/tree/master/samples/conversation/omni)。
  </Tab>
</Tabs>

## 进阶功能

### Qwen-TTS 交互模式

Qwen-TTS Realtime API 提供两种 WebSocket 交互模式，通过 `session.mode` 参数切换：

- **server\_commit 模式**：服务端智能处理文本分段和合成时机，适合大段文本的连续合成场景。客户端只需持续追加文本，无需关注切分和提交。
- **commit 模式**：客户端主动提交文本缓冲区以触发合成，适合需要精确控制合成时机的场景（如对话式 AI 逐轮合成）。

详细的 WebSocket 事件生命周期和连接复用方式，请参见[实时语音合成-千问API参考](/api-reference/speech-synthesis/qwen-tts-realtime/client-events)。

### 交互流程

<Tabs>
  <Tab title="CosyVoice">
    CosyVoice 使用基于 WebSocket 的流式协议。协议详情请参见 [CosyVoice WebSocket API 参考](/api-reference/speech-synthesis/cosyvoice/websocket-api)。
  </Tab>

  <Tab title="Qwen-TTS-Realtime">
    ![Qwen-TTS interaction flow](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2678667571/p992312.svg)

    #### 连接 API

    使用 Qwen-TTS-Realtime 需要建立 WebSocket 连接，参数如下：

| Parameter         | Value                                                                |
| ----------------- | -------------------------------------------------------------------- |
| **WebSocket URL** | `wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=<model_name>` |
| **认证方式**          | 在 `Authorization` 请求头中使用 Bearer token                                |
| **模型参数**          | 将 `<model_name>` 替换为支持的模型。详见[支持的模型](#适用范围)。                          |

    ```bash
    # Example connection URL
    wss://dashscope.aliyuncs.com/api-ws/v1/realtime?model=qwen3-tts-flash-realtime
    ```

    完整代码示例请参见[快速开始](#快速开始)。

    <Tabs>
      <Tab title="服务端提交模式">
        将 `session.update` 事件的 `session.mode` 属性设置为 `"server_commit"` 以启用此模式。服务端会智能处理文本分割和合成时机。

        **交互流程**：

        1. 客户端发送 `session.update` 事件。服务端返回 `session.created` 和 `session.updated` 事件。
        2. 客户端发送 `input_text_buffer.append` 事件，将文本追加到服务端缓冲区。
        3. 服务端智能处理文本分割和合成时机，返回 `response.created`、`response.output_item.added`、`response.content_part.added` 和 `response.audio.delta` 事件。
        4. 完成响应后，服务端返回 `response.audio.done`、`response.content_part.done`、`response.output_item.done` 和 `response.done`。
        5. 服务端返回 `session.finished` 结束会话。

| 生命周期    | 客户端事件                                   | 服务端事件                                         |
| ------- | --------------------------------------- | --------------------------------------------- |
| 会话初始化   | `session.update` 会话配置                   | `session.created` 会话已创建                       |
|         |                                         | `session.updated` 会话配置已更新                     |
| 用户文本输入  | `input_text_buffer.append` 向服务端追加文本     |                                               |
|         | `input_text_buffer.commit` 立即合成服务端缓存的文本 |                                               |
|         | `session.finish` 通知服务端不再有文本输入           | `input_text_buffer.committed` 服务端已接收提交的文本     |
| 服务端音频输出 | 无                                       | `response.created` 服务端开始生成响应                  |
|         |                                         | `response.output_item.added` 响应中有新的输出内容       |
|         |                                         | `response.content_part.added` 助手消息中添加了新的输出内容  |
|         |                                         | `response.audio.delta` 模型生成的增量音频              |
|         |                                         | `response.content_part.done` 助手消息的文本或音频内容流已完成 |
|         |                                         | `response.output_item.done` 助手消息的整个输出项流已完成    |
|         |                                         | `response.audio.done` 音频生成完成                  |
|         |                                         | `response.done` 响应完成                          |
      </Tab>

      <Tab title="客户端提交模式">
        将 `session.update` 事件的 `session.mode` 属性设置为 `"commit"` 以启用此模式。客户端需要主动将文本缓冲区提交给服务端以获取响应。

        **交互流程**：

        1. 客户端发送 `session.update` 事件。服务端返回 `session.created` 和 `session.updated` 事件。
        2. 客户端发送 `input_text_buffer.append` 事件，将文本追加到服务端缓冲区。
        3. 客户端发送 `input_text_buffer.commit` 事件将缓冲区提交给服务端，并发送 `session.finish` 事件表示不再有文本输入。
        4. 服务端返回 `response.created`，开始生成响应。
        5. 服务端返回 `response.output_item.added`、`response.content_part.added` 和 `response.audio.delta` 事件。
        6. 完成响应后，服务端返回 `response.audio.done`、`response.content_part.done`、`response.output_item.done` 和 `response.done`。
        7. 服务端返回 `session.finished` 结束会话。

| 生命周期    | 客户端事件                                 | 服务端事件                                         |
| ------- | ------------------------------------- | --------------------------------------------- |
| 会话初始化   | `session.update` 会话配置                 | `session.created` 会话已创建                       |
|         |                                       | `session.updated` 会话配置已更新                     |
| 用户文本输入  | `input_text_buffer.append` 向缓冲区追加文本   |                                               |
|         | `input_text_buffer.commit` 将缓冲区提交给服务端 |                                               |
|         | `input_text_buffer.clear` 清空缓冲区       | `input_text_buffer.committed` 服务端已接收提交的文本     |
| 服务端音频输出 | 无                                     | `response.created` 服务端开始生成响应                  |
|         |                                       | `response.output_item.added` 响应中有新的输出内容       |
|         |                                       | `response.content_part.added` 助手消息中添加了新的输出内容  |
|         |                                       | `response.audio.delta` 模型生成的增量音频              |
|         |                                       | `response.content_part.done` 助手消息的文本或音频内容流已完成 |
|         |                                       | `response.output_item.done` 助手消息的整个输出项流已完成    |
|         |                                       | `response.audio.done` 音频生成完成                  |
|         |                                       | `response.done` 响应完成                          |
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

### 指令控制

<Tabs>
  <Tab title="Qwen-Audio-TTS">
    **支持的模型**：`qwen-audio-3.0-tts-plus`、`qwen-audio-3.0-tts-flash`

    系统音色和声音复刻音色：均可输入任意指令。
  </Tab>

  <Tab title="CosyVoice">
    **支持的模型**：`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-flash`

    - `cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`：无系统音色，仅支持使用声音设计或声音复刻音色，可输入任意指令控制合成效果（如情感、语速等）。
    - `cosyvoice-v3-flash` 的声音设计或声音复刻音色：可输入任意指令控制合成效果。
    - `cosyvoice-v3-flash` 的系统音色：指令必须使用固定格式和内容，详情请参见[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。

    **支持语言**：

    - `cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`：中文、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语
    - `cosyvoice-v3-flash`：中文、英文、法语、德语、日语、韩语、俄语

    **长度限制**：100 字符。汉字（包括简体/繁体汉字、日文汉字和韩文汉字）按 2 个字符计算，其他所有字符（如标点符号、字母、数字、日韩文假名/谚文等）均按 1 个字符计算。
  </Tab>

  <Tab title="Qwen-TTS-Realtime">
    通过自然语言描述来控制语气、语速、情感和声音特征，无需设置音频参数。

    - **支持模型**：仅 Qwen3-TTS-Instruct-Flash-Realtime 模型支持。
    - **使用方式**：通过 `instructions` 参数指定指令内容，例如："语速较快，语调明显上扬，适合介绍时尚产品。"
    - **支持语言**：描述文本仅支持中文和英文。
    - **长度限制**：不超过 1600 个 token。

    **适用场景**：

    - 有声书和广播剧配音
    - 广告和宣传视频配音
    - 游戏角色和动画配音
    - 情感智能语音助手
    - 纪录片和新闻播报

    **如何撰写高质量的声音描述**

    **核心原则**：

    - **具体而非模糊**：使用描述具体声音特征的词汇，如"低沉""清脆""语速快"等。避免使用缺乏信息的主观词汇，如"好听""普通"。
    - **多维度而非单一维度**：好的描述通常结合多个维度（如下文所述：音高、语速、情感等）。单一维度的描述（如仅用"高音"）过于宽泛，无法生成独特的效果。
    - **客观而非主观**：聚焦于声音本身的物理和感知特征，而非个人偏好。例如，使用"略高音调带有活力"而非"我最喜欢的声音"。
    - **原创而非模仿**：描述声音特征，而非要求模仿特定人物（如明星或演员）。此类请求存在版权风险，且模型不支持直接模仿。
    - **简洁而非冗余**：确保每个词都有意义。避免重复同义词或使用无意义的强调词（如"非常非常好听的声音"）。

    **描述维度参考**：结合多个维度可以创造更丰富的表现效果。

| 维度 | 描述示例                          |
| -- | ----------------------------- |
| 音高 | 高、中、低、偏高、偏低                   |
| 语速 | 快、中、慢、偏快、偏慢                   |
| 情感 | 欢快、沉稳、温柔、严肃、活泼、冷静、舒缓          |
| 特征 | 磁性、清脆、沙哑、醇厚、甜美、浑厚、有力          |
| 用途 | 新闻播报、广告配音、有声书、动画角色、语音助手、纪录片解说 |

    **示例**：

    - **标准播报风格**：发音清晰准确，吐字圆润
    - **情绪递进效果**：音量从正常对话迅速增大到呼喊，性格直爽，容易激动和表现力强
    - **特殊情绪状态**：因哭泣导致发音略显含混，略带沙哑，带有明显的哭腔紧张感
    - **广告配音风格**：音调偏高，语速适中，充满活力和感染力，适合广告
    - **温柔舒缓风格**：语速偏慢，语调温柔甜美，像好友一样关怀温暖
  </Tab>
</Tabs>

### 方言

让模型用**中文方言**（如河南话、四川话、粤语等）输出语音。不同模型和音色类型的设置方式不同。

<Tabs>
  <Tab title="Qwen-Audio-TTS">
    - **系统音色**：在[Qwen-Audio-TTS音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)中选择以下任一种音色：
      - 支持方言的系统音色，无需额外设置即可输出对应方言。
      - 支持[指令控制](#指令控制)且可指定方言的音色，通过指令文本指定方言。
    - **声音复刻音色**：通过[指令控制](#指令控制)功能设置，例如指令文本写 `请用河南话表达`。

    **具体支持哪些方言**：参见[语音合成模型列表](/developer-guides/speech/tts-models)中各 Qwen-Audio-TTS 模型“支持的语言”。
  </Tab>

  <Tab title="CosyVoice">
    - **系统音色**：在[CosyVoice音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中选择以下任一种音色：
      - 支持方言的系统音色（例如 `longshange_v3`），无需额外设置即可输出对应方言。
      - 支持[指令控制](#指令控制)且可指定方言的音色（例如 `longanhuan_v3`），通过指令文本指定方言。
    - **声音复刻音色**：通过[指令控制](#指令控制)功能设置，例如指令文本写 `请用河南话表达`。
    - **声音设计音色**：暂不支持方言。

    **具体支持哪些方言**：参见[语音合成模型列表](/developer-guides/speech/tts-models)中各 CosyVoice 模型“支持的语言”。

    **示例**：以 `cosyvoice-v3-flash` + `longanhuan_v3` 音色，通过指令文本 `"请用河南话表达。"` 输出河南话语音。

    ```python
    # coding=utf-8
    import os
    import dashscope
    from dashscope.audio.tts_v2 import *
    # 获取API Key：https://platform.qianwenai.com/home/api-keys
    # 若没有配置环境变量，请将下行替换为：dashscope.api_key = "sk-xxx"
    dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')
    dashscope.base_websocket_api_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'
    # 模型
    # 不同模型版本需要使用对应版本的音色：
    # cosyvoice-v3-flash/cosyvoice-v3-plus：使用longanyang等音色。
    # cosyvoice-v2：使用longxiaochun_v2等音色。
    # 不同语言选择对应音色
    model = "cosyvoice-v3-flash"
    # 音色
    voice = "longanhuan_v3"
    # 实例化SpeechSynthesizer，并在构造方法中传入模型（model）、音色（voice）等请求参数
    synthesizer = SpeechSynthesizer(model=model, voice=voice, instruction="请用河南话表达。")
    # 发送待合成文本，获取二进制音频
    audio = synthesizer.call("叫你去买盐，你买回来一袋面，这不是弄啥嘞吗！")
    # 首次发送文本时需建立 WebSocket 连接，因此首包延迟会包含连接建立的耗时
    print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
      synthesizer.get_last_request_id(),
      synthesizer.get_first_package_delay()))
    # 将音频保存至本地
    with open('output.mp3', 'wb') as f:
      f.write(audio)
    ```
  </Tab>

  <Tab title="Qwen-TTS">
    - **系统音色**：使用支持方言的系统音色，参见[Qwen-TTS音色列表](/api-reference/speech-synthesis/qwen-tts/voice-list)。
    - **声音复刻音色**：不支持方言。
    - **声音设计音色**：不支持方言。

    **具体支持哪些方言**：参见[语音合成模型列表](/developer-guides/speech/tts-models)中各 Qwen3-TTS 模型“支持的语言”。
  </Tab>
</Tabs>

### 情感与富语言标签

Qwen-Audio-TTS 系列模型支持在待合成文本（`text` 参数）中直接嵌入情感与富语言标签，用于控制语音的情感表达或在指定位置插入拟声效果（如笑声、叹息等），无需调整复杂的音频参数即可生成更具表现力的语音。

<Warning>
  **支持的模型**：仅 `qwen-audio-3.0-tts-plus` 和 `qwen-audio-3.0-tts-flash`。

  **限制**：仅支持单向流式模式。
</Warning>

**控制类标签**

控制类标签用于设定语音的情感或风格。将标签写在文本中，标签会作用于其后的所有文本，直到遇到下一个控制类标签，或因句子较长被自动切分为止。

| 标签                         | 说明           |
| -------------------------- | ------------ |
| `[sad]`                    | 悲伤           |
| `[amazed]`                 | 惊叹           |
| `[deep and loud shouting]` | 深沉大声呐喊       |
| `[trembling]`              | 颤抖           |
| `[angry]`                  | 愤怒           |
| `[excited]`                | 兴奋           |
| `[sarcastic]`              | 讽刺           |
| `[curious]`                | 好奇           |
| `[like dracula]`           | 德古拉风格（低沉、阴森） |
| `[bored]`                  | 无聊           |
| `[tired]`                  | 疲惫           |
| `[singing]`                | 唱歌           |
| `[scornful]`               | 轻蔑           |
| `[shouting]`               | 大喊           |
| `[asmr]`                   | ASMR 轻柔耳语    |
| `[panicked]`               | 恐慌           |
| `[mischievously]`          | 调皮           |
| `[empathetic]`             | 共情           |
| `[whispers]`               | 耳语           |
| `[reluctantly]`            | 不情愿          |
| `[crying]`                 | 哭泣           |
| `[serious]`                | 严肃           |
| `[very slowly]`            | 非常缓慢地说话      |
| `[very fast]`              | 非常快速地说话      |

**富语言类标签**

富语言类标签用于在文本的当前位置插入一段拟声效果，不影响前后文本的情感风格。

| 标签                | 说明    |
| ----------------- | ----- |
| `[gasp]`          | 倒吸一口气 |
| `[sighing]`       | 叹息    |
| `[clears throat]` | 清嗓    |
| `[giggles]`       | 咯咯笑   |
| `[laughing]`      | 大笑    |
| `[cough]`         | 咳嗽    |
| `[snorts]`        | 哼声、嗤笑 |

**使用示例**

以下示例展示如何在 `text` 参数中组合使用控制类标签和富语言类标签：

`[excited]今天的天气真不错！[laughing]我们一起出去玩吧！`

上述文本中，`[excited]` 是控制类标签，作用于其后的所有文本，使语音带有兴奋的情感；`[laughing]` 是富语言类标签，在该位置插入一段笑声效果后继续合成后续文本。

您也可以在同一段文本中切换不同情感：

`[serious]请注意安全事项。[excited]好了，现在让我们开始吧！`

其中 `[serious]` 控制第一句为严肃语气，`[excited]` 从第二句起切换为兴奋语气。

### 取消任务

在实时语音合成过程中，如果需要中断当前轮次合成，可以发送取消指令。取消后服务端会立即结束当前任务并返回结束事件，您可在当前 WebSocket 连接上继续发起新的合成任务，无需重新建立连接。

**使用方式**：

- **Python SDK**：1.26.4 及以上版本，调用 `SpeechSynthesizer.streaming_cancel()`。
- **Java SDK**：2.22.26 及以上版本，调用 `SpeechSynthesizer.streamingCancel()`。
- **WebSocket 原始协议**：发送 `finish-task` 事件，并在 `input` 中设置 `directive=cancel`。

<Warning>
  **模型限制**：Qwen-Audio-TTS 系列模型的所有模型都支持该功能；CosyVoice 系列模型仅 v2 及以上版本支持该功能。
</Warning>

### WebSocket 原始协议调用

以下示例展示如何通过 WebSocket 原始协议直连服务端，适用于不使用 DashScope SDK 的场景。此为最小可运行实现，WebSocket 协议请参见各模型的 API 参考。

<Tabs>
  <Tab title="CosyVoice">
    <AccordionGroup>
      <Accordion title="Go">
        ```go
        package main
        import (
            "encoding/json"
            "fmt"
            "net/http"
            "os"
            "strings"
            "time"
            "github.com/google/uuid"
            "github.com/gorilla/websocket"
        )
        const (
            wsURL      = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"
            outputFile = "output.mp3"
        )
        func main() {
            // 获取API Key：https://platform.qianwenai.com/home/api-keys
            // 若没有配置环境变量，请将下行替换为：apiKey := "sk-xxx"
            apiKey := os.Getenv("DASHSCOPE_API_KEY")
            // 清空输出文件
            os.Remove(outputFile)
            os.Create(outputFile)
            // 连接WebSocket
            header := make(http.Header)
            header.Add("X-DashScope-DataInspection", "enable")
            header.Add("Authorization", fmt.Sprintf("bearer %s", apiKey))
            conn, resp, err := websocket.DefaultDialer.Dial(wsURL, header)
            if err != nil {
                if resp != nil {
                    fmt.Printf("连接失败 HTTP状态码: %d\n", resp.StatusCode)
                }
                fmt.Println("连接失败:", err)
                return
            }
            defer conn.Close()
            // 生成任务ID
            taskID := uuid.New().String()
            fmt.Printf("生成任务ID: %s\n", taskID)
            // 发送run-task事件
            runTaskCmd := map[string]interface{}{
                "header": map[string]interface{}{
                    "action":    "run-task",
                    "task_id":   taskID,
                    "streaming": "duplex",
                },
                "payload": map[string]interface{}{
                    "task_group": "audio",
                    "task":       "tts",
                    "function":   "SpeechSynthesizer",
                    "model":      "cosyvoice-v3-flash",
                    "parameters": map[string]interface{}{
                        "text_type":   "PlainText",
                        "voice":       "longanyang",
                        "format":      "mp3",
                        "sample_rate": 22050,
                        "volume":      50,
                        "rate":        1,
                        "pitch":       1,
                        // 如果enable_ssml设为true，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
                        "enable_ssml": false,
                    },
                    "input": map[string]interface{}{},
                },
            }
            runTaskJSON, _ := json.Marshal(runTaskCmd)
            fmt.Printf("发送run-task事件: %s\n", string(runTaskJSON))
            err = conn.WriteMessage(websocket.TextMessage, runTaskJSON)
            if err != nil {
                fmt.Println("发送run-task失败:", err)
                return
            }
            textSent := false
            // 处理消息
            for {
                messageType, message, err := conn.ReadMessage()
                if err != nil {
                    fmt.Println("读取消息失败:", err)
                    break
                }
                // 处理二进制消息
                if messageType == websocket.BinaryMessage {
                    fmt.Printf("收到二进制消息，长度: %d\n", len(message))
                    file, _ := os.OpenFile(outputFile, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)
                    file.Write(message)
                    file.Close()
                    continue
                }
                // 处理文本消息
                messageStr := string(message)
                fmt.Printf("收到文本消息: %s\n", strings.ReplaceAll(messageStr, "\n", ""))
                // 简单解析JSON获取event类型
                var msgMap map[string]interface{}
                if json.Unmarshal(message, &msgMap) == nil {
                    if header, ok := msgMap["header"].(map[string]interface{}); ok {
                        if event, ok := header["event"].(string); ok {
                            fmt.Printf("事件类型: %s\n", event)
                            switch event {
                            case "task-started":
                                fmt.Println("=== 收到task-started事件 ===")
                                if !textSent {
                                    // 发送continue-task事件
                                    texts := []string{"床前明月光，疑是地上霜。", "举头望明月，低头思故乡。"}
                                    for _, text := range texts {
                                        continueTaskCmd := map[string]interface{}{
                                            "header": map[string]interface{}{
                                                "action":    "continue-task",
                                                "task_id":   taskID,
                                                "streaming": "duplex",
                                            },
                                            "payload": map[string]interface{}{
                                                "input": map[string]interface{}{
                                                    "text": text,
                                                },
                                            },
                                        }
                                        continueTaskJSON, _ := json.Marshal(continueTaskCmd)
                                        fmt.Printf("发送continue-task事件: %s\n", string(continueTaskJSON))
                                        err = conn.WriteMessage(websocket.TextMessage, continueTaskJSON)
                                        if err != nil {
                                            fmt.Println("发送continue-task失败:", err)
                                            return
                                        }
                                    }
                                    textSent = true
                                    // 延迟发送finish-task
                                    time.Sleep(500 * time.Millisecond)
                                    // 发送finish-task事件
                                    finishTaskCmd := map[string]interface{}{
                                        "header": map[string]interface{}{
                                            "action":    "finish-task",
                                            "task_id":   taskID,
                                            "streaming": "duplex",
                                        },
                                        "payload": map[string]interface{}{
                                            "input": map[string]interface{}{},
                                        },
                                    }
                                    finishTaskJSON, _ := json.Marshal(finishTaskCmd)
                                    fmt.Printf("发送finish-task事件: %s\n", string(finishTaskJSON))
                                    err = conn.WriteMessage(websocket.TextMessage, finishTaskJSON)
                                    if err != nil {
                                        fmt.Println("发送finish-task失败:", err)
                                        return
                                    }
                                }
                            case "task-finished":
                                fmt.Println("=== 任务完成 ===")
                                return
                            case "task-failed":
                                fmt.Println("=== 任务失败 ===")
                                if header["error_message"] != nil {
                                    fmt.Printf("错误信息: %s\n", header["error_message"])
                                }
                                return
                            case "result-generated":
                                fmt.Println("收到result-generated事件")
                            }
                        }
                    }
                }
            }
        }
        ```
      </Accordion>

      <Accordion title="C#">
        ```csharp
        using System.Net.WebSockets;
        using System.Text;
        using System.Text.Json;
        class Program {
            // 获取API Key：https://platform.qianwenai.com/home/api-keys
            // 若没有配置环境变量，请将下行替换为：private static readonly string ApiKey = "sk-xxx"
            private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");
            private const string WebSocketUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
            // 输出文件路径
            private const string OutputFilePath = "output.mp3";
            // WebSocket客户端
            private static ClientWebSocket _webSocket = new ClientWebSocket();
            // 取消令牌源
            private static CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();
            // 任务ID
            private static string? _taskId;
            // 任务是否已启动
            private static TaskCompletionSource<bool> _taskStartedTcs = new TaskCompletionSource<bool>();
            static async Task Main(string[] args) {
                try {
                    // 清空输出文件
                    ClearOutputFile(OutputFilePath);
                    // 连接WebSocket服务
                    await ConnectToWebSocketAsync(WebSocketUrl);
                    // 启动接收消息的任务
                    Task receiveTask = ReceiveMessagesAsync();
                    // 发送run-task事件
                    _taskId = GenerateTaskId();
                    await SendRunTaskCommandAsync(_taskId);
                    // 等待task-started事件
                    await _taskStartedTcs.Task;
                    // 持续发送continue-task事件
                    string[] texts = {
                        "床前明月光",
                        "疑是地上霜",
                        "举头望明月",
                        "低头思故乡"
                    };
                    foreach (string text in texts) {
                        await SendContinueTaskCommandAsync(text);
                    }
                    // 发送finish-task事件
                    await SendFinishTaskCommandAsync(_taskId);
                    // 等待接收任务完成
                    await receiveTask;
                    Console.WriteLine("任务完成，连接已关闭。");
                } catch (OperationCanceledException) {
                    Console.WriteLine("任务被取消。");
                } catch (Exception ex) {
                    Console.WriteLine($"发生错误：{ex.Message}");
                } finally {
                    _cancellationTokenSource.Cancel();
                    _webSocket.Dispose();
                }
            }
            private static void ClearOutputFile(string filePath) {
                if (File.Exists(filePath)) {
                    File.WriteAllText(filePath, string.Empty);
                    Console.WriteLine("输出文件已清空。");
                } else {
                    Console.WriteLine("输出文件不存在，无需清空。");
                }
            }
            private static async Task ConnectToWebSocketAsync(string url) {
                var uri = new Uri(url);
                if (_webSocket.State == WebSocketState.Connecting || _webSocket.State == WebSocketState.Open) {
                    return;
                }
                // 设置WebSocket连接的头部信息
                _webSocket.Options.SetRequestHeader("Authorization", $"bearer {ApiKey}");
                _webSocket.Options.SetRequestHeader("X-DashScope-DataInspection", "enable");
                try {
                    await _webSocket.ConnectAsync(uri, _cancellationTokenSource.Token);
                    Console.WriteLine("已成功连接到WebSocket服务。");
                } catch (OperationCanceledException) {
                    Console.WriteLine("WebSocket连接被取消。");
                } catch (Exception ex) {
                    Console.WriteLine($"WebSocket连接失败: {ex.Message}");
                    throw;
                }
            }
            private static async Task SendRunTaskCommandAsync(string taskId) {
                var command = CreateCommand("run-task", taskId, "duplex", new {
                    task_group = "audio",
                    task = "tts",
                    function = "SpeechSynthesizer",
                    model = "cosyvoice-v3-flash",
                    parameters = new
                    {
                        text_type = "PlainText",
                        voice = "longanyang",
                        format = "mp3",
                        sample_rate = 22050,
                        volume = 50,
                        rate = 1,
                        pitch = 1,
                        // 如果enable_ssml设为true，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
                        enable_ssml = false
                    },
                    input = new { }
                });
                await SendJsonMessageAsync(command);
                Console.WriteLine("已发送run-task事件。");
            }
            private static async Task SendContinueTaskCommandAsync(string text) {
                if (_taskId == null) {
                    throw new InvalidOperationException("任务ID未初始化。");
                }
                var command = CreateCommand("continue-task", _taskId, "duplex", new {
                    input = new {
                        text
                    }
                });
                await SendJsonMessageAsync(command);
                Console.WriteLine("已发送continue-task事件。");
            }
            private static async Task SendFinishTaskCommandAsync(string taskId) {
                var command = CreateCommand("finish-task", taskId, "duplex", new {
                    input = new { }
                });
                await SendJsonMessageAsync(command);
                Console.WriteLine("已发送finish-task事件。");
            }
            private static async Task SendJsonMessageAsync(string message) {
                var buffer = Encoding.UTF8.GetBytes(message);
                try {
                    await _webSocket.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, _cancellationTokenSource.Token);
                } catch (OperationCanceledException) {
                    Console.WriteLine("消息发送被取消。");
                }
            }
            private static async Task ReceiveMessagesAsync() {
                while (_webSocket.State == WebSocketState.Open) {
                    var response = await ReceiveMessageAsync();
                    if (response != null) {
                        var eventStr = response.RootElement.GetProperty("header").GetProperty("event").GetString();
                        switch (eventStr) {
                            case "task-started":
                                Console.WriteLine("任务已启动。");
                                _taskStartedTcs.TrySetResult(true);
                                break;
                            case "task-finished":
                                Console.WriteLine("任务已完成。");
                                _cancellationTokenSource.Cancel();
                                break;
                            case "task-failed":
                                Console.WriteLine("任务失败：" + response.RootElement.GetProperty("header").GetProperty("error_message").GetString());
                                _cancellationTokenSource.Cancel();
                                break;
                            default:
                                // result-generated可在此处理
                                break;
                        }
                    }
                }
            }
            private static async Task<JsonDocument?> ReceiveMessageAsync() {
                var buffer = new byte[1024 * 4];
                var segment = new ArraySegment<byte>(buffer);
                try {
                    WebSocketReceiveResult result = await _webSocket.ReceiveAsync(segment, _cancellationTokenSource.Token);
                    if (result.MessageType == WebSocketMessageType.Close) {
                        await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Closing", _cancellationTokenSource.Token);
                        return null;
                    }
                    if (result.MessageType == WebSocketMessageType.Binary) {
                        // 处理二进制数据
                        Console.WriteLine("接收到二进制数据...");
                        // 将二进制数据保存到文件
                        using (var fileStream = new FileStream(OutputFilePath, FileMode.Append)) {
                            fileStream.Write(buffer, 0, result.Count);
                        }
                        return null;
                    }
                    string message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                    return JsonDocument.Parse(message);
                } catch (OperationCanceledException) {
                    Console.WriteLine("消息接收被取消。");
                    return null;
                }
            }
            private static string GenerateTaskId() {
                return Guid.NewGuid().ToString("N").Substring(0, 32);
            }
            private static string CreateCommand(string action, string taskId, string streaming, object payload) {
                var command = new {
                    header = new {
                        action,
                        task_id = taskId,
                        streaming
                    },
                    payload
                };
                return JsonSerializer.Serialize(command);
            }
        }
        ```
      </Accordion>

      <Accordion title="PHP">
        示例代码目录结构为：

        ```text
        my-php-project/
        ├── composer.json
        ├── vendor/
        └── index.php
        ```

        composer.json内容如下，相关依赖的版本号请根据实际情况自行决定：

        ```json
        {
            "require": {
                "react/event-loop": "^1.3",
                "react/socket": "^1.11",
                "react/stream": "^1.2",
                "react/http": "^1.1",
                "ratchet/pawl": "^0.4"
            },
            "autoload": {
                "psr-4": {
                    "App\\": "src/"
                }
            }
        }
        ```

        index.php内容如下：

        ```php
        <?php
        require __DIR__ . '/vendor/autoload.php';
        use Ratchet\Client\Connector;
        use React\EventLoop\Loop;
        use React\Socket\Connector as SocketConnector;
        // 获取API Key：https://platform.qianwenai.com/home/api-keys
        // 若没有配置环境变量，请将下行替换为：$api_key = "sk-xxx"
        $api_key = getenv("DASHSCOPE_API_KEY");
        $websocket_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'; // WebSocket服务器地址
        $output_file = 'output.mp3'; // 输出文件路径
        $loop = Loop::get();
        if (file_exists($output_file)) {
            // 清空文件内容
            file_put_contents($output_file, '');
        }
        // 创建自定义的连接器
        $socketConnector = new SocketConnector($loop, [
            'tcp' => [
                'bindto' => '0.0.0.0:0',
            ],
            'tls' => [
                'verify_peer' => false,
                'verify_peer_name' => false,
            ],
        ]);
        $connector = new Connector($loop, $socketConnector);
        $headers = [
            'Authorization' => 'bearer ' . $api_key,
            'X-DashScope-DataInspection' => 'enable'
        ];
        $connector($websocket_url, [], $headers)->then(function ($conn) use ($loop, $output_file) {
            echo "连接到WebSocket服务器\n";
            // 生成任务ID
            $taskId = generateTaskId();
            // 发送 run-task 事件
            sendRunTaskMessage($conn, $taskId);
            // 定义发送 continue-task 事件的函数
            $sendContinueTask = function() use ($conn, $loop, $taskId) {
                // 待发送的文本
                $texts = ["床前明月光", "疑是地上霜", "举头望明月", "低头思故乡"];
                $continueTaskCount = 0;
                foreach ($texts as $text) {
                    $continueTaskMessage = json_encode([
                        "header" => [
                            "action" => "continue-task",
                            "task_id" => $taskId,
                            "streaming" => "duplex"
                        ],
                        "payload" => [
                            "input" => [
                                "text" => $text
                            ]
                        ]
                    ]);
                    echo "准备发送continue-task事件: " . $continueTaskMessage . "\n";
                    $conn->send($continueTaskMessage);
                    $continueTaskCount++;
                }
                echo "发送的continue-task事件个数为：" . $continueTaskCount . "\n";
                // 发送 finish-task 事件
                sendFinishTaskMessage($conn, $taskId);
            };
            // 标记是否收到 task-started 事件
            $taskStarted = false;
            // 监听消息
            $conn->on('message', function($msg) use ($conn, $sendContinueTask, $loop, &$taskStarted, $taskId, $output_file) {
                if ($msg->isBinary()) {
                    // 写入二进制数据到本地文件
                    file_put_contents($output_file, $msg->getPayload(), FILE_APPEND);
                } else {
                    // 处理非二进制消息
                    $response = json_decode($msg, true);
                    if (isset($response['header']['event'])) {
                        handleEvent($conn, $response, $sendContinueTask, $loop, $taskId, $taskStarted);
                    } else {
                        echo "未知的消息格式\n";
                    }
                }
            });
            // 监听连接关闭
            $conn->on('close', function($code = null, $reason = null) {
                echo "连接已关闭\n";
                if ($code !== null) {
                    echo "关闭代码: " . $code . "\n";
                }
                if ($reason !== null) {
                    echo "关闭原因：" . $reason . "\n";
                }
            });
        }, function ($e) {
            echo "无法连接：{$e->getMessage()}\n";
        });
        $loop->run();
        /**
         * 生成任务ID
         * @return string
         */
        function generateTaskId(): string {
            return bin2hex(random_bytes(16));
        }
        /**
         * 发送 run-task 事件
         * @param $conn
         * @param $taskId
         */
        function sendRunTaskMessage($conn, $taskId) {
            $runTaskMessage = json_encode([
                "header" => [
                    "action" => "run-task",
                    "task_id" => $taskId,
                    "streaming" => "duplex"
                ],
                "payload" => [
                    "task_group" => "audio",
                    "task" => "tts",
                    "function" => "SpeechSynthesizer",
                    "model" => "cosyvoice-v3-flash",
                    "parameters" => [
                        "text_type" => "PlainText",
                        "voice" => "longanyang",
                        "format" => "mp3",
                        "sample_rate" => 22050,
                        "volume" => 50,
                        "rate" => 1,
                        "pitch" => 1,
                        // 如果enable_ssml设为true，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
                        "enable_ssml" => false
                    ],
                    "input" => (object) []
                ]
            ]);
            echo "准备发送run-task事件: " . $runTaskMessage . "\n";
            $conn->send($runTaskMessage);
            echo "run-task事件已发送\n";
        }
        /**
         * 读取音频文件
         * @param string $filePath
         * @return bool|string
         */
        function readAudioFile(string $filePath) {
            $voiceData = file_get_contents($filePath);
            if ($voiceData === false) {
                echo "无法读取音频文件\n";
            }
            return $voiceData;
        }
        /**
         * 分割音频数据
         * @param string $data
         * @param int $chunkSize
         * @return array
         */
        function splitAudioData(string $data, int $chunkSize): array {
            return str_split($data, $chunkSize);
        }
        /**
         * 发送 finish-task 事件
         * @param $conn
         * @param $taskId
         */
        function sendFinishTaskMessage($conn, $taskId) {
            $finishTaskMessage = json_encode([
                "header" => [
                    "action" => "finish-task",
                    "task_id" => $taskId,
                    "streaming" => "duplex"
                ],
                "payload" => [
                    "input" => (object) []
                ]
            ]);
            echo "准备发送finish-task事件: " . $finishTaskMessage . "\n";
            $conn->send($finishTaskMessage);
            echo "finish-task事件已发送\n";
        }
        /**
         * 处理事件
         * @param $conn
         * @param $response
         * @param $sendContinueTask
         * @param $loop
         * @param $taskId
         * @param $taskStarted
         */
        function handleEvent($conn, $response, $sendContinueTask, $loop, $taskId, &$taskStarted) {
            switch ($response['header']['event']) {
                case 'task-started':
                    echo "任务开始，发送continue-task事件...\n";
                    $taskStarted = true;
                    // 发送 continue-task 事件
                    $sendContinueTask();
                    break;
                case 'result-generated':
                    // 收到result-generated事件
                    break;
                case 'task-finished':
                    echo "任务完成\n";
                    $conn->close();
                    break;
                case 'task-failed':
                    echo "任务失败\n";
                    echo "错误代码：" . $response['header']['error_code'] . "\n";
                    echo "错误信息：" . $response['header']['error_message'] . "\n";
                    $conn->close();
                    break;
                case 'error':
                    echo "错误：" . $response['payload']['message'] . "\n";
                    break;
                default:
                    echo "未知事件：" . $response['header']['event'] . "\n";
                    break;
            }
            // 如果任务已完成，关闭连接
            if ($response['header']['event'] == 'task-finished') {
                // 等待1秒以确保所有数据都已传输完毕
                $loop->addTimer(1, function() use ($conn) {
                    $conn->close();
                    echo "客户端关闭连接\n";
                });
            }
            // 如果没有收到 task-started 事件，关闭连接
            if (!$taskStarted && in_array($response['header']['event'], ['task-failed', 'error'])) {
                $conn->close();
            }
        }
        ```
      </Accordion>

      <Accordion title="Node.js">
        需安装相关依赖：

        ```sh
        npm install ws
        npm install uuid
        ```

        示例代码如下：

        ```javascript
        const WebSocket = require('ws');
        const fs = require('fs');
        const uuid = require('uuid').v4;
        // 获取API Key：https://platform.qianwenai.com/home/api-keys
        // 若没有配置环境变量，请将下行替换为：const apiKey = "sk-xxx"
        const apiKey = process.env.DASHSCOPE_API_KEY;
        const url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference';
        // 输出文件路径
        const outputFilePath = 'output.mp3';
        // 清空输出文件
        fs.writeFileSync(outputFilePath, '');
        // 创建WebSocket客户端
        const ws = new WebSocket(url, {
          headers: {
            Authorization: `bearer ${apiKey}`,
            'X-DashScope-DataInspection': 'enable'
          }
        });
        let taskStarted = false;
        let taskId = uuid();
        ws.on('open', () => {
          console.log('已连接到WebSocket服务器');
          // 发送run-task事件
          const runTaskMessage = JSON.stringify({
            header: {
              action: 'run-task',
              task_id: taskId,
              streaming: 'duplex'
            },
            payload: {
              task_group: 'audio',
              task: 'tts',
              function: 'SpeechSynthesizer',
              model: 'cosyvoice-v3-flash',
              parameters: {
                text_type: 'PlainText',
                voice: 'longanyang', // 音色
                format: 'mp3', // 音频格式
                sample_rate: 22050, // 采样率
                volume: 50, // 音量
                rate: 1, // 语速
                pitch: 1, // 音调
                enable_ssml: false // 是否开启SSML功能。如果enable_ssml设为true，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
              },
              input: {}
            }
          });
          ws.send(runTaskMessage);
          console.log('已发送run-task消息');
        });
        const fileStream = fs.createWriteStream(outputFilePath, { flags: 'a' });
        ws.on('message', (data, isBinary) => {
          if (isBinary) {
            // 写入二进制数据到文件
            fileStream.write(data);
          } else {
            const message = JSON.parse(data);
            switch (message.header.event) {
              case 'task-started':
                taskStarted = true;
                console.log('任务已开始');
                // 发送continue-task事件
                sendContinueTasks(ws);
                break;
              case 'task-finished':
                console.log('任务已完成');
                ws.close();
                fileStream.end(() => {
                  console.log('文件流已关闭');
                });
                break;
              case 'task-failed':
                console.error('任务失败：', message.header.error_message);
                ws.close();
                fileStream.end(() => {
                  console.log('文件流已关闭');
                });
                break;
              default:
                // 可以在这里处理result-generated
                break;
            }
          }
        });
        function sendContinueTasks(ws) {
          const texts = [
            '床前明月光，',
            '疑是地上霜。',
            '举头望明月，',
            '低头思故乡。'
          ];
          texts.forEach((text, index) => {
            setTimeout(() => {
              if (taskStarted) {
                const continueTaskMessage = JSON.stringify({
                  header: {
                    action: 'continue-task',
                    task_id: taskId,
                    streaming: 'duplex'
                  },
                  payload: {
                    input: {
                      text: text
                    }
                  }
                });
                ws.send(continueTaskMessage);
                console.log(`已发送continue-task，文本：${text}`);
              }
            }, index * 1000); // 每隔1秒发送一次
          });
          // 发送finish-task事件
          setTimeout(() => {
            if (taskStarted) {
              const finishTaskMessage = JSON.stringify({
                header: {
                  action: 'finish-task',
                  task_id: taskId,
                  streaming: 'duplex'
                },
                payload: {
                  input: {}
                }
              });
              ws.send(finishTaskMessage);
              console.log('已发送finish-task');
            }
          }, texts.length * 1000 + 1000); // 在所有continue-task事件发送完毕后1秒发送
        }
        ws.on('close', () => {
          console.log('已断开与WebSocket服务器的连接');
        });
        ```
      </Accordion>

      <Accordion title="Java">
        建议使用 Java DashScope SDK 进行开发，请参见 [Java SDK](/api-reference/speech-synthesis/cosyvoice/java-sdk)。

        以下是 Java WebSocket 直连示例，运行前请导入以下依赖：

        - `Java-WebSocket`
        - `jackson-databind`

        推荐使用Maven或Gradle管理依赖包，其配置如下：

        <CodeGroup>
          ```xml pom.xml
          <dependencies>
              <!-- WebSocket Client -->
              <dependency>
                  <groupId>org.java-websocket</groupId>
                  <artifactId>Java-WebSocket</artifactId>
                  <version>1.5.3</version>
              </dependency>
              <!-- JSON Processing -->
              <dependency>
                  <groupId>com.fasterxml.jackson.core</groupId>
                  <artifactId>jackson-databind</artifactId>
                  <version>2.13.0</version>
              </dependency>
          </dependencies>
          ```

          ```groovy build.gradle
          // 省略其它代码
          dependencies {
            // WebSocket Client
            implementation 'org.java-websocket:Java-WebSocket:1.5.3'
            // JSON Processing
            implementation 'com.fasterxml.jackson.core:jackson-databind:2.13.0'
          }
          // 省略其它代码
          ```
        </CodeGroup>

        Java代码如下：

        ```java
        import com.fasterxml.jackson.databind.ObjectMapper;
        import org.java_websocket.client.WebSocketClient;
        import org.java_websocket.handshake.ServerHandshake;
        import java.io.FileOutputStream;
        import java.io.IOException;
        import java.net.URI;
        import java.nio.ByteBuffer;
        import java.util.*;
        public class TTSWebSocketClient extends WebSocketClient {
            private final String taskId = UUID.randomUUID().toString();
            private final String outputFile = "output_" + System.currentTimeMillis() + ".mp3";
            private boolean taskFinished = false;
            public TTSWebSocketClient(URI serverUri, Map<String, String> headers) {
                super(serverUri, headers);
            }
            @Override
            public void onOpen(ServerHandshake serverHandshake) {
                System.out.println("连接成功");
                // 发送run-task事件
                // 如果enable_ssml设为true，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
                String runTaskCommand = "{ \"header\": { \"action\": \"run-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"task_group\": \"audio\", \"task\": \"tts\", \"function\": \"SpeechSynthesizer\", \"model\": \"cosyvoice-v3-flash\", \"parameters\": { \"text_type\": \"PlainText\", \"voice\": \"longanyang\", \"format\": \"mp3\", \"sample_rate\": 22050, \"volume\": 50, \"rate\": 1, \"pitch\": 1, \"enable_ssml\": false }, \"input\": {} }}";
                send(runTaskCommand);
            }
            @Override
            public void onMessage(String message) {
                System.out.println("收到服务端返回的消息：" + message);
                try {
                    // Parse JSON message
                    Map<String, Object> messageMap = new ObjectMapper().readValue(message, Map.class);
                    if (messageMap.containsKey("header")) {
                        Map<String, Object> header = (Map<String, Object>) messageMap.get("header");
                        if (header.containsKey("event")) {
                            String event = (String) header.get("event");
                            if ("task-started".equals(event)) {
                                System.out.println("收到服务端返回的task-started事件");
                                List<String> texts = Arrays.asList(
                                        "床前明月光，疑是地上霜",
                                        "举头望明月，低头思故乡"
                                );
                                for (String text : texts) {
                                    // 发送continue-task事件
                                    sendContinueTask(text);
                                }
                                // 发送finish-task事件
                                sendFinishTask();
                            } else if ("task-finished".equals(event)) {
                                System.out.println("收到服务端返回的task-finished事件");
                                taskFinished = true;
                                closeConnection();
                            } else if ("task-failed".equals(event)) {
                                System.out.println("任务失败：" + message);
                                closeConnection();
                            }
                        }
                    }
                } catch (Exception e) {
                    System.err.println("出现异常：" + e.getMessage());
                }
            }
            @Override
            public void onMessage(ByteBuffer message) {
                System.out.println("收到的二进制音频数据大小为：" + message.remaining());
                try (FileOutputStream fos = new FileOutputStream(outputFile, true)) {
                    byte[] buffer = new byte[message.remaining()];
                    message.get(buffer);
                    fos.write(buffer);
                    System.out.println("音频数据已写入本地文件" + outputFile + "中");
                } catch (IOException e) {
                    System.err.println("音频数据写入本地文件失败：" + e.getMessage());
                }
            }
            @Override
            public void onClose(int code, String reason, boolean remote) {
                System.out.println("连接关闭：" + reason + " (" + code + ")");
            }
            @Override
            public void onError(Exception ex) {
                System.err.println("报错：" + ex.getMessage());
                ex.printStackTrace();
            }
            private void sendContinueTask(String text) {
                String command = "{ \"header\": { \"action\": \"continue-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"input\": { \"text\": \"" + text + "\" } }}";
                send(command);
            }
            private void sendFinishTask() {
                String command = "{ \"header\": { \"action\": \"finish-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"input\": {} }}";
                send(command);
            }
            private void closeConnection() {
                if (!isClosed()) {
                    close();
                }
            }
            public static void main(String[] args) {
                try {
                    // 获取API Key：https://platform.qianwenai.com/home/api-keys
                    // 若没有配置环境变量，请将下行替换为：String apiKey = "sk-xxx"
                    String apiKey = System.getenv("DASHSCOPE_API_KEY");
                    if (apiKey == null || apiKey.isEmpty()) {
                        System.err.println("请设置 DASHSCOPE_API_KEY 环境变量");
                        return;
                    }
                    Map<String, String> headers = new HashMap<>();
                    headers.put("Authorization", "bearer " + apiKey);
                    TTSWebSocketClient client = new TTSWebSocketClient(new URI("wss://dashscope.aliyuncs.com/api-ws/v1/inference"), headers);
                    client.connect();
                    while (!client.isClosed() && !client.taskFinished) {
                        Thread.sleep(1000);
                    }
                } catch (Exception e) {
                    System.err.println("连接WebSocket服务失败：" + e.getMessage());
                    e.printStackTrace();
                }
            }
        }
        ```
      </Accordion>

      <Accordion title="Python">
        建议使用 Python DashScope SDK 进行开发，请参见 [Python SDK](/api-reference/speech-synthesis/cosyvoice/python-sdk)。

        以下是 Python WebSocket 直连示例，运行前请导入以下依赖：

        ```bash
        pip uninstall websocket-client
        pip uninstall websocket
        pip install websocket-client
        ```

        <Warning>
          请不要将运行示例代码的Python文件命名为“websocket.py”，否则会报错（AttributeError: module 'websocket' has no attribute 'WebSocketApp'. Did you mean: 'WebSocket'?）。
        </Warning>

        ```python
        import websocket
        import json
        import uuid
        import os
        import time
        class TTSClient:
          def __init__(self, api_key, uri):
            """
          初始化 TTSClient 实例
          参数:
            api_key (str): 鉴权用的 API Key
            uri (str): WebSocket 服务地址
          """
            self.api_key = api_key  # 替换为你的 API Key
            self.uri = uri  # 替换为你的 WebSocket 地址
            self.task_id = str(uuid.uuid4())  # 生成唯一任务 ID
            self.output_file = f"output_{int(time.time())}.mp3"  # 输出音频文件路径
            self.ws = None  # WebSocketApp 实例
            self.task_started = False  # 是否收到 task-started
            self.task_finished = False  # 是否收到 task-finished / task-failed
          def on_open(self, ws):
            """
          WebSocket 连接建立时回调函数
          发送 run-task 事件开启语音合成任务
          """
            print("WebSocket 已连接")
            # 构造 run-task 事件
            run_task_cmd = {
              "header": {
                "action": "run-task",
                "task_id": self.task_id,
                "streaming": "duplex"
              },
              "payload": {
                "task_group": "audio",
                "task": "tts",
                "function": "SpeechSynthesizer",
                "model": "cosyvoice-v3-flash",
                "parameters": {
                  "text_type": "PlainText",
                  "voice": "longanyang",
                  "format": "mp3",
                  "sample_rate": 22050,
                  "volume": 50,
                  "rate": 1,
                  "pitch": 1,
                  # 如果enable_ssml设为True，只允许发送一次continue-task事件，否则会报错“Text request limit violated, expected 1.”
                  "enable_ssml": False
                },
                "input": {}
              }
            }
            # 发送 run-task 事件
            ws.send(json.dumps(run_task_cmd))
            print("已发送 run-task 事件")
          def on_message(self, ws, message):
            """
          接收到消息时的回调函数
          区分文本和二进制消息处理
          """
            if isinstance(message, str):
              # 处理 JSON 文本消息
              try:
                msg_json = json.loads(message)
                print(f"收到 JSON 消息: {msg_json}")
                if "header" in msg_json:
                  header = msg_json["header"]
                  if "event" in header:
                    event = header["event"]
                    if event == "task-started":
                      print("任务已启动")
                      self.task_started = True
                      # 发送 continue-task 事件
                      texts = [
                        "床前明月光，疑是地上霜",
                        "举头望明月，低头思故乡"
                      ]
                      for text in texts:
                        self.send_continue_task(text)
                      # 所有 continue-task 发送完成后发送 finish-task
                      self.send_finish_task()
                    elif event == "task-finished":
                      print("任务已完成")
                      self.task_finished = True
                      self.close(ws)
                    elif event == "task-failed":
                      error_msg = msg_json.get("error_message", "未知错误")
                      print(f"任务失败: {error_msg}")
                      self.task_finished = True
                      self.close(ws)
              except json.JSONDecodeError as e:
                print(f"JSON 解析失败: {e}")
            else:
              # 处理二进制消息（音频数据）
              print(f"收到二进制消息，大小: {len(message)} 字节")
              with open(self.output_file, "ab") as f:
                f.write(message)
              print(f"已将音频数据写入本地文件{self.output_file}中")
          def on_error(self, ws, error):
            """发生错误时的回调"""
            print(f"WebSocket 出错: {error}")
          def on_close(self, ws, close_status_code, close_msg):
            """连接关闭时的回调"""
            print(f"WebSocket 已关闭: {close_msg} ({close_status_code})")
          def send_continue_task(self, text):
            """发送 continue-task 事件，附带要合成的文本内容"""
            cmd = {
              "header": {
                "action": "continue-task",
                "task_id": self.task_id,
                "streaming": "duplex"
              },
              "payload": {
                "input": {
                  "text": text
                }
              }
            }
            self.ws.send(json.dumps(cmd))
            print(f"已发送 continue-task 事件，文本内容: {text}")
          def send_finish_task(self):
            """发送 finish-task 事件，结束语音合成任务"""
            cmd = {
              "header": {
                "action": "finish-task",
                "task_id": self.task_id,
                "streaming": "duplex"
              },
              "payload": {
                "input": {}
              }
            }
            self.ws.send(json.dumps(cmd))
            print("已发送 finish-task 事件")
          def close(self, ws):
            """主动关闭连接"""
            if ws and ws.sock and ws.sock.connected:
              ws.close()
              print("已主动关闭连接")
          def run(self):
            """启动 WebSocket 客户端"""
            # 设置请求头部（鉴权）
            header = {
              "Authorization": f"bearer {self.api_key}",
              "X-DashScope-DataInspection": "enable"
            }
            # 创建 WebSocketApp 实例
            self.ws = websocket.WebSocketApp(
              self.uri,
              header=header,
              on_open=self.on_open,
              on_message=self.on_message,
              on_error=self.on_error,
              on_close=self.on_close
            )
            print("正在监听 WebSocket 消息...")
            self.ws.run_forever()  # 启动长连接监听
        # 示例使用方式
        if __name__ == "__main__":
          # 获取API Key：https://platform.qianwenai.com/home/api-keys
          # 若没有配置环境变量，请将下行替换为：API_KEY = "sk-xxx"
          API_KEY = os.environ.get("DASHSCOPE_API_KEY")
          SERVER_URI = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"  # 替换为你的 WebSocket 地址
          client = TTSClient(API_KEY, SERVER_URI)
          client.run()
        ```
      </Accordion>
    </AccordionGroup>
  </Tab>

  <Tab title="Sambert">
    <AccordionGroup>
      <Accordion title="Go">
        ```go
        package main
        import (
            "encoding/json"
            "fmt"
            "net/http"
            "os"
            "time"
            "github.com/google/uuid"
            "github.com/gorilla/websocket"
        )
        const (
            wsURL      = "wss://dashscope.aliyuncs.com/api-ws/v1/inference" // WebSocket服务器地址
            outputFile = "output.mp3"                                        // 输出文件路径
        )
        func main() {
            // 若没有将API Key配置到环境变量，可将下行替换为：apiKey := "your_api_key"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            apiKey := os.Getenv("DASHSCOPE_API_KEY")
            // 检查并清空输出文件
            if err := clearOutputFile(outputFile); err != nil {
                fmt.Println("清空输出文件失败：", err)
                return
            }
            // 连接WebSocket服务
            conn, err := connectWebSocket(apiKey)
            if err != nil {
                fmt.Println("连接WebSocket失败：", err)
                return
            }
            defer closeConnection(conn)
            // 创建一个通道用于接收任务完成的通知
            done := make(chan struct{})
            // 启动异步接收消息的goroutine
            go receiveMessage(conn, done)
            // 发送run-task指令
            if err := sendRunTaskMsg(conn); err != nil {
                fmt.Println("发送run-task指令失败：", err)
                return
            }
            // 等待任务完成或超时
            select {
            case <-done:
                fmt.Println("任务结束")
            case <-time.After(5 * time.Minute):
                fmt.Println("任务超时")
            }
        }
        // 定义消息结构体
        type Message struct {
            Header  Header  `json:"header"`
            Payload Payload `json:"payload"`
        }
        // 定义头部信息
        type Header struct {
            Action       string                 `json:"action,omitempty"`
            TaskID       string                 `json:"task_id"`
            Streaming    string                 `json:"streaming,omitempty"`
            Event        string                 `json:"event,omitempty"`
            ErrorCode    string                 `json:"error_code,omitempty"`
            ErrorMessage string                 `json:"error_message,omitempty"`
            Attributes   map[string]interface{} `json:"attributes"`
        }
        // 定义负载信息
        type Payload struct {
            Model      string     `json:"model,omitempty"`
            TaskGroup  string     `json:"task_group,omitempty"`
            Task       string     `json:"task,omitempty"`
            Function   string     `json:"function,omitempty"`
            Input      Input      `json:"input,omitempty"`
            Parameters Parameters `json:"parameters,omitempty"`
            Output     Output     `json:"output,omitempty"`
            Usage      Usage      `json:"usage,omitempty"`
        }
        // 定义输入信息
        type Input struct {
            Text string `json:"text"`
        }
        // 定义参数信息
        type Parameters struct {
            TextType                string  `json:"text_type"`
            Format                  string  `json:"format"`
            SampleRate              int     `json:"sample_rate"`
            Volume                  int     `json:"volume"`
            Rate                    float64 `json:"rate"`
            Pitch                   float64 `json:"pitch"`
            WordTimestampEnabled    bool    `json:"word_timestamp_enabled"`
            PhonemeTimestampEnabled bool    `json:"phoneme_timestamp_enabled"`
        }
        // 定义输出信息
        type Output struct {
            Sentence Sentence `json:"sentence"`
        }
        // 定义句子信息
        type Sentence struct {
            BeginTime int    `json:"begin_time"`
            EndTime   int    `json:"end_time"`
            Words     []Word `json:"words"`
        }
        // 定义单词信息
        type Word struct {
            Text      string    `json:"text"`
            BeginTime int       `json:"begin_time"`
            EndTime   int       `json:"end_time"`
            Phonemes  []Phoneme `json:"phonemes"`
        }
        // 定义音素信息
        type Phoneme struct {
            BeginTime int    `json:"begin_time"`
            EndTime   int    `json:"end_time"`
            Text      string `json:"text"`
            Tone      int    `json:"tone"`
        }
        // 定义使用信息
        type Usage struct {
            Characters int `json:"characters"`
        }
        func receiveMessage(conn *websocket.Conn, done chan struct{}) {
            for {
                msgType, message, err := conn.ReadMessage()
                if err != nil {
                    fmt.Println("解析服务器消息失败：", err)
                    close(done)
                    break
                }
                if msgType == websocket.BinaryMessage {
                    // 处理二进制音频流
                    if err := writeBinaryDataToFile(message, outputFile); err != nil {
                        fmt.Println("写入二进制数据失败：", err)
                        close(done)
                        break
                    }
                    fmt.Println("音频片段已写入本地文件")
                } else {
                    // 处理文本消息
                    var msg Message
                    if err := json.Unmarshal(message, &msg); err != nil {
                        fmt.Println("解析事件失败：", err)
                        continue
                    }
                    if handleMessage(conn, msg, done) {
                        break
                    }
                }
            }
        }
        func handleMessage(conn *websocket.Conn, msg Message, done chan struct{}) bool {
            switch msg.Header.Event {
            case "task-started":
                fmt.Println("任务已启动")
            case "result-generated":
            // 如需获取附加消息，可在此处添加相应代码
            case "task-finished":
                fmt.Println("任务已完成")
                close(done)
                return true
            case "task-failed":
                if msg.Header.ErrorMessage != "" {
                    fmt.Printf("任务失败：%s\n", msg.Header.ErrorMessage)
                } else {
                    fmt.Println("未知原因导致任务失败")
                }
                close(done)
                return true
            default:
                fmt.Printf("预料之外的事件：%v\n", msg)
                close(done)
            }
            return false
        }
        func sendRunTaskMsg(conn *websocket.Conn) error {
            runTaskMsg, err := generateRunTaskMsg()
            if err != nil {
                return err
            }
            if err := conn.WriteMessage(websocket.TextMessage, []byte(runTaskMsg)); err != nil {
                return err
            }
            return nil
        }
        func generateRunTaskMsg() (string, error) {
            runTaskMessage := Message{
                Header: Header{
                    Action:    "run-task",
                    TaskID:    uuid.New().String(),
                    Streaming: "out",
                },
                Payload: Payload{
                    Model:     "sambert-zhichu-v1",
                    TaskGroup: "audio",
                    Task:      "tts",
                    Function:  "SpeechSynthesizer",
                    Input: Input{
                        Text: "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。",
                    },
                    Parameters: Parameters{
                        TextType:                "PlainText",
                        Format:                  "mp3",
                        SampleRate:              16000,
                        Volume:                  50,
                        Rate:                    1.0,
                        Pitch:                   1.0,
                        WordTimestampEnabled:    true,
                        PhonemeTimestampEnabled: true,
                    },
                },
            }
            runTaskMsgJSON, err := json.Marshal(runTaskMessage)
            return string(runTaskMsgJSON), err
        }
        func connectWebSocket(apiKey string) (*websocket.Conn, error) {
            header := make(http.Header)
            header.Add("X-DashScope-DataInspection", "enable")
            header.Add("Authorization", fmt.Sprintf("bearer %s", apiKey))
            conn, _, err := websocket.DefaultDialer.Dial(wsURL, header)
            if err != nil {
                fmt.Println("连接WebSocket失败：", err)
                return nil, err
            }
            return conn, nil
        }
        func writeBinaryDataToFile(data []byte, filePath string) error {
            file, err := os.OpenFile(filePath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
            if err != nil {
                return err
            }
            defer file.Close()
            _, err = file.Write(data)
            return err
        }
        func closeConnection(conn *websocket.Conn) {
            if conn != nil {
                conn.Close()
            }
        }
        func clearOutputFile(filePath string) error {
            file, err := os.OpenFile(filePath, os.O_TRUNC|os.O_CREATE|os.O_WRONLY, 0644)
            if err != nil {
                return err
            }
            file.Close()
            return nil
        }
        ```
      </Accordion>

      <Accordion title="C#">
        ```csharp
        using System.Net.WebSockets;
        using System.Text;
        using System.Text.Json;
        class Program {
            // 若没有将API Key配置到环境变量，可将下行替换为：private const string ApiKey="REDACTED"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
            private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");
            private const string WebSocketUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference"; // WebSocket服务器地址
            private const string OutputFilePath = "output.mp3"; // 输出文件路径
            static async Task Main(string[] args) {
                var ws = new ClientWebSocket();
                try {
                    // 1. 连接WebSocket服务，鉴权
                    await ConnectWithAuth(ws, WebSocketUrl);
                    // 2. 启动接收消息的线程
                    var receiveTask = ReceiveMessages(ws);
                    // 3. 发送run-task指令
                    string textToSynthesize = "白日依山尽，黄河入海流。欲穷千里目，更上一层楼。";
                    string taskId = GenerateTaskId();
                    await SendRunTaskCommand(ws, textToSynthesize, taskId);
                    // 4. 等待接收任务完成
                    await receiveTask;
                } catch (Exception ex) {
                    Console.WriteLine($"错误：{ex.Message}");
                } finally {
                    if (ws.State == WebSocketState.Open) {
                        await ws.CloseAsync(WebSocketCloseStatus.NormalClosure, "关闭连接", CancellationToken.None);
                    }
                }
            }
            private static async Task ConnectWithAuth(ClientWebSocket ws, string url) {
                var uri = new Uri(url);
                ws.Options.SetRequestHeader("Authorization", $"bearer {ApiKey}");
                ws.Options.SetRequestHeader("X-DashScope-DataInspection", "enable");
                await ws.ConnectAsync(uri, CancellationToken.None);
                Console.WriteLine("已连接到WebSocket服务器。");
            }
            private static string GenerateTaskId() {
                return Guid.NewGuid().ToString("N");
            }
            private static async Task SendRunTaskCommand(ClientWebSocket ws, string text, string taskId) {
                var command = CreateRunTaskCommand(text, taskId);
                var buffer = Encoding.UTF8.GetBytes(command);
                await ws.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, CancellationToken.None);
                Console.WriteLine("已发送run-task指令。");
            }
            private static string CreateRunTaskCommand(string text, string taskId) {
                var command = new {
                    header = new {
                        action = "run-task",
                        task_id = taskId,
                        streaming = "out"
                    },
                    payload = new {
                        model = "sambert-zhichu-v1",
                        task_group = "audio",
                        task = "tts",
                        function = "SpeechSynthesizer",
                        input = new {
                            text = text
                        },
                        parameters = new {
                            text_type = "PlainText",
                            format = "mp3",
                            sample_rate = 16000,
                            volume = 50,
                            rate = 1,
                            pitch = 1,
                            word_timestamp_enabled = true,
                            phoneme_timestamp_enabled = true
                        }
                    }
                };
                return JsonSerializer.Serialize(command);
            }
            private static async Task ReceiveMessages(ClientWebSocket ws) {
                var buffer = new byte[1024 * 4];
                var fs = new FileStream(OutputFilePath, FileMode.Create, FileAccess.Write);
                bool taskStarted = false;
                bool taskFinished = false;
                while (ws.State == WebSocketState.Open && !taskFinished) {
                    var result = await ws.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
                    switch (result.MessageType) {
                        case WebSocketMessageType.Text:
                            var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                            var jsonMessage = JsonSerializer.Deserialize<JsonElement>(message);
                            ProcessTextMessage(jsonMessage, ref taskStarted, ref taskFinished);
                            break;
                        case WebSocketMessageType.Binary:
                            if (taskStarted) {
                                await fs.WriteAsync(buffer, 0, result.Count);
                                Console.WriteLine("收到音频数据。");
                            }
                            break;
                        case WebSocketMessageType.Close:
                            Console.WriteLine("服务器关闭了连接。");
                            taskFinished = true;
                            break;
                    }
                }
                fs.Close();
            }
            private static void ProcessTextMessage(JsonElement jsonMessage, ref bool taskStarted, ref bool taskFinished) {
                if (jsonMessage.TryGetProperty("header", out JsonElement header) && header.TryGetProperty("event", out JsonElement eventToken)) {
                    var eventType = eventToken.GetString();
                    switch (eventType) {
                        case "task-started":
                            taskStarted = true;
                            Console.WriteLine("任务开始。");
                            break;
                        case "result-generated":
                            // 如需获取附加消息，可在此处添加相应代码
                            break;
                        case "task-finished":
                            taskFinished = true;
                            Console.WriteLine("任务完成。");
                            break;
                        case "task-failed":
                            taskFinished = true;
                            Console.WriteLine("任务失败。");
                            break;
                    }
                }
            }
        }
        ```
      </Accordion>

      <Accordion title="PHP">
        示例代码目录结构为：

        ```text
        my-php-project/
        ├── composer.json
        ├── vendor/
        └── index.php
        ```

        composer.json内容如下，相关依赖的版本号请根据实际情况自行决定：

        ```json
        {
            "require": {
                "react/event-loop": "^1.3",
                "react/socket": "^1.11",
                "react/stream": "^1.2",
                "react/http": "^1.1",
                "ratchet/pawl": "^0.4"
            },
            "autoload": {
                "psr-4": {
                    "App\\": "src/"
                }
            }
        }
        ```

        index.php内容如下：

        ```php
        <?php
        require 'vendor/autoload.php';
        use Ratchet\Client\Connector;
        use React\EventLoop\Loop;
        use React\Socket\Connector as SocketConnector;
        # 若没有将API Key配置到环境变量，可将下行替换为：$api_key="REDACTED"。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        $api_key = getenv("DASHSCOPE_API_KEY");
        $websocket_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'; // WebSocket服务器地址
        $output_file = 'output.mp3'; // 输出文件路径
        $loop = Loop::get();
        if (file_exists($output_file)) {
            // 清空文件内容
            file_put_contents($output_file, '');
            echo "文件已清空\n";
        }
        // 创建自定义的连接器
        $socketConnector = new SocketConnector($loop, [
            'tcp' => [
                'bindto' => '0.0.0.0:0',
            ],
            'tls' => [
                'verify_peer' => false,
                'verify_peer_name' => false,
            ],
        ]);
        $connector = new Connector($loop, $socketConnector);
        $headers = [
            'Authorization' => 'bearer ' . $api_key,
            'X-DashScope-DataInspection' => 'enable'
        ];
        // 连接WebSocket服务
        $connector($websocket_url, [], $headers)
            ->then(function ($conn) use ($output_file) {
                echo "连接成功\n";
                // 异步接收WebSocket消息
                $conn->on('message', function ($msg) use ($conn, $output_file) {
                    if ($msg->isBinary()) {
                        // 写入二进制数据到本地文件
                        file_put_contents($output_file, $msg->getPayload(), FILE_APPEND);
                        echo "二进制数据写入文件\n";
                    } else {
                        $data = json_decode($msg, true);
                        switch ($data['header']['event']) {
                            case 'task-started':
                                echo "任务开始\n";
                                break;
                            case 'result-generated':
                                // 如需获取附加消息，可在此处添加相应代码
                                break;
                            case 'task-finished':
                                echo "任务完成\n";
                                $conn->close();
                                break;
                            case 'task-failed':
                                echo "任务失败：" . $data['header']['error_message'] . "\n";
                                $conn->close();
                                break;
                            default:
                                echo "未知事件：" . $msg . "\n";
                        }
                    }
                });
                // 监听连接关闭
                $conn->on('close', function($code = null, $reason = null) {
                    echo "连接已关闭\n";
                    if ($code !== null) {
                        echo "关闭代码：" . $code . "\n";
                    }
                    if ($reason !== null) {
                        echo "关闭原因：" . $reason . "\n";
                    }
                });
                // 发送run-task指令
                $conn->send(json_encode([
                    'header' => [
                        'action' => 'run-task',
                        'task_id' => bin2hex(random_bytes(16)),
                        'streaming' => 'out'
                    ],
                    'payload' => [
                        'model' => 'sambert-zhichu-v1',
                        'task_group' => 'audio',
                        'task' => 'tts',
                        'function' => 'SpeechSynthesizer',
                        'input' => [
                            'text' => '床前明月光，疑是地上霜。举头望明月，低头思故乡。'
                        ],
                        'parameters' => [
                            'text_type' => 'PlainText',
                            'format' => 'mp3',
                            'sample_rate' => 16000,
                            'volume' => 50,
                            'rate' => 1,
                            'pitch' => 1,
                            'word_timestamp_enabled' => true,
                            'phoneme_timestamp_enabled' => true
                        ]
                    ]
                ]));
                echo "run-task指令已发送\n";
            }, function (Exception $e) {
                echo "连接失败：{$e->getMessage()}\n";
                file_put_contents('error.log', $e->getMessage() . "\n", FILE_APPEND);
            });
        $loop->run();
        ```
      </Accordion>

      <Accordion title="Node.js">
        需安装相关依赖：

        ```sh
        npm install ws
        npm install uuid
        ```

        示例代码如下：

        ```javascript
        const WebSocket = require('ws');
        const fs = require('fs');
        const { v4: uuidv4 } = require('uuid');
        // 若没有将API Key配置到环境变量，可将下行替换为：apiKey = 'REDACTED'。不建议在生产环境中直接将API Key硬编码到代码中，以减少API Key泄露风险。
        const apiKey = process.env.DASHSCOPE_API_KEY;
        const wsUrl = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'; // WebSocket服务器地址
        const outputFilePath = 'output.mp3'; // 替换为您的音频文件路径
        async function main() {
          await checkAndClearOutputFile(outputFilePath);
          createWebSocketConnection();
        }
        const fileStream = fs.createWriteStream(outputFilePath, { flags: 'a' });
        function createWebSocketConnection() {
          const ws = new WebSocket(wsUrl, {
            headers: {
              Authorization: `bearer ${apiKey}`,
              'X-DashScope-DataInspection': 'enable'
            }
          });
          ws.on('open', () => {
            console.log('已连接到WebSocket服务器');
            sendRunTaskMessage(ws);
          });
          ws.on('message', (data, isBinary) => handleWebSocketMessage(data, isBinary, ws));
          ws.on('error', (error) => console.error('WebSocket错误:', error));
          ws.on('close', () => console.log('WebSocket连接已关闭'));
          return ws;
        }
        function sendRunTaskMessage(ws) {
          const taskId = uuidv4();
          const runTaskMessage = {
            header: {
              action: 'run-task',
              task_id: taskId,
              streaming: 'out'
            },
            payload: {
              model: 'sambert-zhichu-v1',
              task_group: 'audio',
              task: 'tts',
              function: 'SpeechSynthesizer',
              input: {
                text: '白日依山尽，黄河入海流。欲穷千里目，更上一层楼。'
              },
              parameters: {
                text_type: 'PlainText',
                format: 'mp3',
                sample_rate: 16000,
                volume: 50,
                rate: 1,
                pitch: 1,
                word_timestamp_enabled: true,
                phoneme_timestamp_enabled: true
              }
            }
          };
          ws.send(JSON.stringify(runTaskMessage));
          console.log('run-task指令已发送');
        }
        function handleWebSocketMessage(data, isBinary, ws) {
          if (isBinary) {
            fileStream.write(data);
          } else {
            const message = JSON.parse(data);
            handleWebSocketEvent(message, ws);
          }
        }
        function handleWebSocketEvent(message, ws) {
          switch (message.header.event) {
            case 'task-started':
              console.log('任务已启动');
              break;
            case 'result-generated':
              console.log('结果已生成');
              break;
            case 'task-finished':
              console.log('任务已完成');
              ws.close();
              fileStream.end(() => {
                console.log('文件流已关闭');
              });
              break;
            case 'task-failed':
              console.error('任务失败：', message.header.error_message);
              ws.close();
              fileStream.end(() => {
                console.log('文件流已关闭');
              });
              break;
            default:
              console.log('未知事件：', message.header.event);
          }
        }
        function checkAndClearOutputFile(filePath) {
          return new Promise((resolve, reject) => {
            fs.access(filePath, fs.F_OK, (err) => {
              if (!err) {
                fs.truncate(filePath, 0, (truncateErr) => {
                  if (truncateErr) return reject(truncateErr);
                  console.log('文件已清空');
                  resolve();
                });
              } else {
                fs.open(filePath, 'w', (openErr) => {
                  if (openErr) return reject(openErr);
                  console.log('文件已创建');
                  resolve();
                });
              }
            });
          });
        }
        main().catch(console.error);
        ```
      </Accordion>
    </AccordionGroup>
  </Tab>
</Tabs>

## 声音定制

<Tabs>
  <Tab title="CosyVoice">
    ### 声音复刻：输入音频格式要求

    高质量的输入音频是实现优秀复刻效果的基础。

| 项目       | 要求                                                                                                                      |
| -------- | ----------------------------------------------------------------------------------------------------------------------- |
| **支持格式** | WAV（16-bit）、MP3、M4A                                                                                                     |
| **音频时长** | 推荐：10\~20秒。最长：60秒。                                                                                                      |
| **文件大小** | ≤ 10 MB                                                                                                                 |
| **采样率**  | ≥ 16 kHz                                                                                                                |
| **声道**   | 单声道或立体声。立体声音频仅处理第一声道，请确保第一声道包含清晰的人声。                                                                                    |
| **内容**   | 音频必须包含至少5秒的连续、清晰人声，不含背景音。其余部分仅允许短暂停顿（≤ 2秒）。整段音频应无背景音乐、噪音或其他人声，以确保核心语音内容的高质量。请使用正常说话的音频作为输入，不要上传歌曲或演唱音频，以确保复刻效果的准确性和可用性。 |

    ### 声音设计：编写高质量的声音描述

    #### 限制条件

    编写声音描述（`voice_prompt`）时，请遵循以下技术约束：

    - **长度限制**：`voice_prompt` 的内容不得超过500个字符。
    - **支持语言**：描述文本仅支持中文和英文。

    #### 核心原则

    `voice_prompt` 用于引导模型生成具有特定特征的声音。

    编写声音描述时，请遵循以下核心原则：

    - **具体而非模糊**：使用能够描绘具体声音特质的词语，如"低沉"、"清脆"、"语速偏快"。避免使用"好听"、"普通"等主观且缺乏信息量的词汇。
    - **多维而非单一**：优秀的描述通常结合多个维度（如性别、年龄、情感等）。单一维度的描述（如仅"女声"）过于宽泛，难以生成特色鲜明的效果。
    - **客观而非主观**：专注于声音本身的物理和感知特征，而不是个人喜好。例如，用"音调偏高，带有活力"代替"我最喜欢的声音"。
    - **原创而非模仿**：请描述声音的特质，而不是要求模仿特定人物（如名人、演员）。此类请求涉及版权风险，且模型不支持直接模仿。
    - **简洁而非冗余**：确保每个词都有其意义。避免重复使用同义词或无意义的强调词（如"非常非常棒的声音"）。

    #### 描述维度参考

| 维度 | 示例                                                    |
| -- | ----------------------------------------------------- |
| 性别 | 男性、女性、中性                                              |
| 年龄 | 儿童（5-12岁）、青少年（13-18岁）、青年（19-35岁）、中年（36-55岁）、老年（55岁以上） |
| 音调 | 高、中、低、偏高、偏低                                           |
| 语速 | 快、中、慢、偏快、偏慢                                           |
| 情感 | 欢快、沉稳、温柔、严肃、活泼、冷酷、舒缓                                  |
| 特质 | 磁性、清脆、沙哑、浑厚、甜美、浓郁、有力                                  |
| 用途 | 新闻播报、广告配音、有声读物、动画角色、语音助手、纪录片解说                        |

    #### 示例对比

    **好的案例**：

    - "年轻活泼的女声，语速较快，带有明显的上扬语调，适合介绍时尚产品。"
      - *分析*：该描述结合了年龄、性格、语速和语调，并指定了使用场景，形成了清晰的声音画像。
    - "沉稳的中年男声，语速偏慢，低沉而富有磁性，适合新闻播报或纪录片解说。"
      - *分析*：该描述清晰定义了性别、年龄段、语速、音质和用途。
    - "可爱的童声，约8岁女孩，说话略带稚气，适合动画角色配音。"
      - *分析*：该描述精准定位了年龄和声音特质（稚气），且有明确用途。
    - "温柔知性的女性，约30岁，语气平和，适合有声读物朗读。"
      - *分析*：该描述通过"知性"、"平和"等词有效传达了声音的情感和风格。

    **不好的案例及改进建议**：

| 不好的案例         | 主要问题                | 改进建议                                      |
| ------------- | ------------------- | ----------------------------------------- |
| "好听的声音"       | 描述过于模糊和主观，缺乏可操作的细节。 | 添加具体维度，如"音色清亮的年轻女声，语调轻柔"。                 |
| "像某明星的声音"     | 涉及版权风险，模型不支持直接模仿。   | 提取声音特征进行描述，如"成熟、磁性、语速沉稳的男声"。              |
| "非常非常非常好听的女声" | 描述冗余，重复用词无法帮助定义声音。  | 去除重复，添加有效描述，如"20\~24岁的女声，音色轻快，语调活泼，音质甜美"。 |
| 123456        | 无效输入，无法解析为声音特征。     | 请提供有意义的文字描述，参见上方推荐示例。                     |
  </Tab>

  <Tab title="Qwen-TTS-Realtime">
    Qwen3-TTS 支持声音克隆（Qwen3-TTS-VC）和声音设计（Qwen3-TTS-VD）。详见[声音克隆](/api-reference/speech-synthesis/voice-cloning/create-voice)指南。
  </Tab>
</Tabs>

## 连接复用（WebSocket）

WebSocket 连接支持复用：一个合成任务结束后，无需重新建立连接即可开启下一个任务。

复用流程：

- **Qwen-Audio-TTS / CosyVoice / Sambert**：客户端发送 `finish-task`，服务端返回 `task-finished` 后，可重新发送 `run-task` 开启新任务。
- **Qwen-TTS**：客户端发送 `session.finish`，服务端返回 `session.finished` 后，可建立新会话开启下一个任务。

**取消任务后复用**：对于 Qwen-Audio-TTS / CosyVoice，如果使用 `cancel` 指令取消当前任务，服务端返回 `task-finished` 后，同样可以在当前连接上重新发送 `run-task` 开启新任务。详情请参见[取消任务](#取消任务)。

<Warning>
  - 必须等服务端返回结束事件（`task-finished` 或 `session.finished`）后才可发起新任务。
  - CosyVoice 和 Sambert 在复用连接中的不同任务需要使用不同的 `task_id`。
  - 任务失败时服务端返回错误事件并关闭连接，该连接不可复用。
  - 任务结束后 60 秒无新任务，连接自动断开。
</Warning>

各模型事件说明请参见对应的 [API 参考](#api-参考)。

## 高并发最佳实践

DashScope SDK 内置池化机制，可复用 WebSocket 连接和合成对象，避免频繁创建销毁带来的开销。

<Tabs>
  <Tab title="CosyVoice">
    **前提条件**：

    - [获取API Key](/api-reference/preparation/api-key)
    - 已安装符合版本要求的 DashScope SDK，建议[安装最新版](/api-reference/preparation/install-sdk)：
      - Python SDK：版本 ≥ 1.25.2
      - Java SDK：版本 ≥ 2.16.6

    <Tabs>
      <Tab title="Python SDK">
        Python SDK 通过 `SpeechSynthesizerObjectPool` 管理和复用 `SpeechSynthesizer` 对象。

        对象池在初始化时即创建指定数量的 `SpeechSynthesizer` 实例并建立 WebSocket 连接，获取对象时可直接发起请求，降低首包延迟。归还后连接保持活跃，等待下次复用。

        #### 实现步骤

        1. 安装依赖：安装 DashScope 依赖（`pip install -U dashscope`）。
        2. 创建并配置对象池。

           对象池大小推荐设为峰值并发数的 1.5\~2 倍，且不应超过账户的 QPS 限制。

           创建全局单例对象池（初始化时建立连接，有一定耗时）：

        ```python
        from dashscope.audio.tts_v2 import SpeechSynthesizerObjectPool
        synthesizer_object_pool = SpeechSynthesizerObjectPool(max_size=20)
        import dashscope
        dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"
        ```

        <Warning>
          - 在对象池场景中，`SpeechSynthesizerObjectPool` 在初始化时即按当前全局 `dashscope.api_key` 与服务端建立 WebSocket 连接。apiKey 仅在 WebSocket 建连握手时写入 `Authorization` 请求头用于鉴权，后续任务消息（如 `run-task`）本身不携带 apiKey。**池创建后修改 `dashscope.api_key` 不会影响池内已建连接**——`borrow_synthesizer` 取出的对象（包括归还后再次复用的对象）仍使用握手时的 apiKey，新值会被静默忽略，可能导致身份、配额或计费归属与预期不一致。注意：`borrow_synthesizer` 也不支持通过参数指定 apiKey。
          - 如确需使用多个不同的 API Key，请为每个 API Key 维护**独立的** `SpeechSynthesizerObjectPool` **实例**。
        </Warning>

        3. 从对象池中获取 `SpeechSynthesizer` 对象。

           如果当前未归还的对象数已超过池容量，系统会额外创建新对象。此类对象需重新建立连接，不具备复用效果。

        ```python
        speech_synthesizer = connectionPool.borrow_synthesizer(
          model='cosyvoice-v3-flash',
          voice='longanyang',
          seed=12382,
          callback=synthesizer_callback
        )
        ```

        4. 进行语音合成。调用 `SpeechSynthesizer` 对象的 `call` 或 `streaming_call` 方法进行语音合成。
        5. 归还 `SpeechSynthesizer` 对象。任务结束后归还对象以供复用。不要归还未完成任务或任务失败的对象。

        ```python
        connectionPool.return_synthesizer(speech_synthesizer)
        ```

        <Accordion title="完整代码">
          <Warning>
            复制使用前请注意：`SpeechSynthesizerObjectPool` 在初始化时即按当前全局 `dashscope.api_key` 与服务端建立 WebSocket 连接并完成鉴权；**池创建后再修改 `dashscope.api_key` 不会影响池内已建连接**，新值会被静默忽略。多 API Key 场景请为每个 API Key 维护独立的池实例。详见上文重要说明。
          </Warning>

          ```python
          # !/usr/bin/env python3
          # Copyright (C) Alibaba Group. All Rights Reserved.
          # MIT License (https://opensource.org/licenses/MIT)
          import os
          import time
          import threading
          import dashscope
          from dashscope.audio.tts_v2 import *
          USE_CONNECTION_POOL = True
          text_to_synthesize = [
            '第一句、欢迎使用阿里巴巴语音合成服务。',
            '第二句、欢迎使用阿里巴巴语音合成服务。',
            '第三句、欢迎使用阿里巴巴语音合成服务。',
          ]
          connectionPool = None
          def init_dashscope_api_key():
            '''
            Set your DashScope API-key. More information:
            https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/PREREQUISITES.md
            '''
            if 'DASHSCOPE_API_KEY' in os.environ:
              dashscope.api_key = os.environ[
                'DASHSCOPE_API_KEY']  # load API-key from environment variable DASHSCOPE_API_KEY
            else:
              dashscope.api_key = 'REDACTED'  # set API-key manually
          def synthesis_text_to_speech_and_play_by_streaming_mode(text, task_id):
            global USE_CONNECTION_POOL, connectionPool
            '''
            Synthesize speech with given text by streaming mode, async call and play the synthesized audio in real-time.
            '''
            complete_event = threading.Event()
            # Define a callback to handle the result
            class Callback(ResultCallback):
              def on_open(self):
                # when using object pool, on_open will be called after task start
                self.file = open(f'result_{task_id}.mp3', 'wb')
                print(f'[task_{task_id}] start')
              def on_complete(self):
                print(f'[task_{task_id}] speech synthesis task complete successfully.')
                complete_event.set()
              def on_error(self, message: str):
                print(f'[task_{task_id}] speech synthesis task failed, {message}')
              def on_close(self):
                # when using object pool, on_open will be called after task finished
                print(f'[task_{task_id}] finished')
              def on_event(self, message):
                # print(f'recv speech synthsis message {message}')
                pass
              def on_data(self, data: bytes) -> None:
                # send to player
                # save audio to file
                self.file.write(data)
            # Call the speech synthesizer callback
            synthesizer_callback = Callback()
            # Initialize the speech synthesizer
            # you can customize the synthesis parameters, like voice, format, sample_rate or other parameters
            if USE_CONNECTION_POOL:
              speech_synthesizer = connectionPool.borrow_synthesizer(
                model='cosyvoice-v3-flash',
                voice='longanyang',
                seed=12382,
                callback=synthesizer_callback
              )
            else:
              speech_synthesizer = SpeechSynthesizer(model='cosyvoice-v3-flash',
                                 voice='longanyang',
                                 seed=12382,
                                 callback=synthesizer_callback)
            try:
              speech_synthesizer.call(text)
            except Exception as e:
              print(f'[task_{task_id}] speech synthesis task failed, {e}')
              if USE_CONNECTION_POOL:
                # close the synthesizer connection manually if task failed when using connection pool.
                speech_synthesizer.close()
              return
            print('[task_{}] Synthesized text: {}'.format(task_id, text))
            complete_event.wait()
            print('[task_{}][Metric] requestId: {}, first package delay ms: {}'.format(
              task_id,
              speech_synthesizer.get_last_request_id(),
              speech_synthesizer.get_first_package_delay()))
            if USE_CONNECTION_POOL:
              connectionPool.return_synthesizer(speech_synthesizer)
          # main function
          if __name__ == '__main__':
            # 必须先设置 dashscope.api_key 和 base_websocket_api_url，再创建 SpeechSynthesizerObjectPool。
            # 池在初始化时即按当前全局 dashscope.api_key 建立 WebSocket 连接，
            # 池创建后再修改 dashscope.api_key 不会影响池内已建连接。
            dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'
            init_dashscope_api_key()
            if USE_CONNECTION_POOL:
              print('creating connection pool')
              start_time = time.time() * 1000
              connectionPool = SpeechSynthesizerObjectPool(max_size=3)
              end_time = time.time() * 1000
              print('connection pool created, cost: {} ms'.format(end_time - start_time))
            task_thread_list = []
            for task_id in range(3):
              thread = threading.Thread(
                target=synthesis_text_to_speech_and_play_by_streaming_mode,
                args=(text_to_synthesize[task_id], task_id))
              task_thread_list.append(thread)
            for task_thread in task_thread_list:
              task_thread.start()
            for task_thread in task_thread_list:
              task_thread.join()
            if USE_CONNECTION_POOL:
              connectionPool.shutdown()
          ```
        </Accordion>

        #### 资源管理与异常处理

        - 任务成功：当语音合成任务正常完成时，必须调用 `connectionPool.return_synthesizer(speech_synthesizer)` 将 `SpeechSynthesizer` 对象归还到池中，以便复用。

          <Warning>
            不要归还未完成任务或任务失败的 `SpeechSynthesizer` 对象。
          </Warning>

        - 任务失败：当 SDK 内部或业务逻辑抛出异常导致任务中断时，主动关闭底层的 WebSocket 连接：`speech_synthesizer.close()`。

        - 在所有语音合成任务完成后，要通过如下方式关闭对象池：`connectionPool.shutdown()`。

        - 在服务出现 TaskFailed 报错时，不需要额外处理。
      </Tab>

      <Tab title="Java SDK">
        Java SDK 通过内置的连接池和自定义的对象池协同工作，实现最佳性能。

        - 连接池：SDK 内部集成的 OkHttp3 连接池，负责管理和复用底层的 WebSocket 连接，减少网络握手开销。此功能默认开启。
        - 对象池：基于 `commons-pool2` 实现，用于维护一组已预先建立好连接的 `SpeechSynthesizer` 对象。从池中获取对象可消除连接建立的延迟，显著降低首包延迟。

        #### 实现步骤

        1. 添加依赖。根据项目构建工具，在依赖配置文件中添加 dashscope-sdk-java 和 commons-pool2。以 Maven 和 Gradle 为例，配置如下：

        <CodeGroup>
          ```xml Maven
          <dependency>
              <groupId>com.alibaba</groupId>
              <artifactId>dashscope-sdk-java</artifactId>
              <!-- 请将 'the-latest-version' 替换为2.16.9及以上版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
              <version>the-latest-version</version>
          </dependency>
          <dependency>
              <groupId>org.apache.commons</groupId>
              <artifactId>commons-pool2</artifactId>
              <!-- 请将 'the-latest-version' 替换为最新版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/org.apache.commons/commons-pool2 -->
              <version>the-latest-version</version>
          </dependency>
          ```

          ```groovy Gradle
          dependencies {
              // 请将 'the-latest-version' 替换为2.16.6及以上版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
              implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
              // 请将 'the-latest-version' 替换为最新版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/org.apache.commons/commons-pool2
              implementation group: 'org.apache.commons', name: 'commons-pool2', version: 'the-latest-version'
          }
          ```
        </CodeGroup>

        2. 配置连接池。通过环境变量配置连接池关键参数：

| 环境变量                                           | 描述                                                             |
| ---------------------------------------------- | -------------------------------------------------------------- |
| DASHSCOPE\_CONNECTION\_POOL\_SIZE              | 连接池大小。推荐值：峰值并发数的 2 倍以上。默认值：32。                                 |
| DASHSCOPE\_MAXIMUM\_ASYNC\_REQUESTS            | 最大异步请求数。推荐值：与 `DASHSCOPE_CONNECTION_POOL_SIZE` 保持一致。默认值：32。    |
| DASHSCOPE\_MAXIMUM\_ASYNC\_REQUESTS\_PER\_HOST | 单主机最大异步请求数。推荐值：与 `DASHSCOPE_CONNECTION_POOL_SIZE` 保持一致。默认值：32。 |

        3. 配置对象池。通过环境变量配置对象池大小：

| 环境变量                        | 描述                                  |
| --------------------------- | ----------------------------------- |
| COSYVOICE\_OBJECTPOOL\_SIZE | 对象池大小。推荐值：峰值并发数的 1.5 至 2 倍。默认值：500。 |

        <Warning>
          - 对象池的大小（`COSYVOICE_OBJECTPOOL_SIZE`）必须小于或等于连接池的大小（`DASHSCOPE_CONNECTION_POOL_SIZE`）。否则，当对象池请求对象时，若连接池已满，会导致调用线程阻塞，等待可用连接。
          - 对象池大小不应超过账户的 QPS（每秒查询率）限制。
        </Warning>

        通过如下代码创建对象池：

        ```java
        class CosyvoiceObjectPool {
            // 。。。这里省略其它代码，完整示例请参见完整代码
            public static GenericObjectPool<SpeechSynthesizer> getInstance() {
                lock.lock();
                if (synthesizerPool == null) {
                    // 您可以在这里设置对象池的大小。或在环境变量COSYVOICE_OBJECTPOOL_SIZE中设置。
                    // 建议设置为服务器最大并发连接数的1.5到2倍。
                    int objectPoolSize = getObjectivePoolSize();
                    SpeechSynthesizerObjectFactory speechSynthesizerObjectFactory =
                            new SpeechSynthesizerObjectFactory();
                    GenericObjectPoolConfig<SpeechSynthesizer> config =
                            new GenericObjectPoolConfig<>();
                    config.setMaxTotal(objectPoolSize);
                    config.setMaxIdle(objectPoolSize);
                    config.setMinIdle(objectPoolSize);
                    synthesizerPool =
                            new GenericObjectPool<>(speechSynthesizerObjectFactory, config);
                }
                lock.unlock();
                return synthesizerPool;
            }
        }
        ```

        4. 从对象池中获取 `SpeechSynthesizer` 对象。如果当前未归还的对象数量已超过对象池的最大容量，系统会额外创建一个新的 `SpeechSynthesizer` 对象。此类新创建的对象需要重新进行初始化并建立 WebSocket 连接，无法利用对象池的既有连接资源，因此不具备复用效果。

        ```java
        synthesizer = CosyvoiceObjectPool.getInstance().borrowObject();
        ```

        5. 进行语音合成。从对象池借出 `SpeechSynthesizer` 对象后，需先调用 `updateParamAndCallback(param, callback)` 关联本次任务的参数与回调，再调用 `streamingCall` 或 `call` 方法进行语音合成。

           <Warning>
             - 在对象池场景中，`updateParamAndCallback` 会被**多次调用**（每次借出对象时都需调用一次，用于切换该次任务的回调和任务级参数，如 `voice`、`format` 等）。**多次调用时传入的 `apiKey` 必须始终相同**。`updateParamAndCallback` 只更新当前 `SpeechSynthesizer` 实例的本地字段，不会重建底层 WebSocket 连接；而 SDK 仅在 WebSocket 建连握手时将 `apiKey` 写入 `Authorization` 请求头用于鉴权，后续任务消息（如 `run-task`）本身不携带 `apiKey`。因此只要复用的连接未断开，传入新的 `apiKey` 不会被发送到服务端，请求实际仍会使用连接首次握手时的 `apiKey`，可能导致身份、配额或计费归属与预期不一致。
             - 如确需使用多个不同的 API Key，请为每个 API Key 维护**独立的对象池实例**。
           </Warning>

        6. 归还 `SpeechSynthesizer` 对象。语音合成任务结束后，归还 `SpeechSynthesizer` 对象，以便后续任务可以复用该对象。不要归还未完成任务或任务失败的对象。

        ```java
        CosyvoiceObjectPool.getInstance().returnObject(synthesizer);
        ```

        <Accordion title="完整代码">
          <Warning>
            复制使用前请注意：对象池场景下多次调用 `updateParamAndCallback` 时传入的 apiKey **必须始终相同**——SDK 不会更新已建立连接的 apiKey，传入不同的 apiKey 不会生效。多 API Key 场景请为每个 API Key 维护独立的对象池实例。详见上文重要说明。
          </Warning>

          ```java
          import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
          import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisAudioFormat;
          import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesisParam;
          import com.alibaba.dashscope.audio.ttsv2.SpeechSynthesizer;
          import com.alibaba.dashscope.common.ResultCallback;
          import com.alibaba.dashscope.exception.NoApiKeyException;
          import com.alibaba.dashscope.utils.Constants;
          import lombok.extern.slf4j.Slf4j;
          import org.apache.commons.pool2.BasePooledObjectFactory;
          import org.apache.commons.pool2.PooledObject;
          import org.apache.commons.pool2.impl.DefaultPooledObject;
          import org.apache.commons.pool2.impl.GenericObjectPool;
          import org.apache.commons.pool2.impl.GenericObjectPoolConfig;
          import java.time.LocalDateTime;
          import java.util.concurrent.ExecutorService;
          import java.util.concurrent.Executors;
          import java.util.concurrent.TimeUnit;
          import java.util.concurrent.locks.Lock;
          /**
           * 您需要在项目中引入org.apache.commons.pool2和DashScope相关的包。
           *
           * DashScope SDK 2.16.6及后续版本针对高并发场景进行了优化，
           * DashScope SDK 2.16.6之前的版本不推荐在高并发场景下使用。
           *
           *
           * 在对TTS服务进行高并发调用之前，
           * 请通过以下环境变量配置连接池的相关参数。
           *
           * DASHSCOPE_MAXIMUM_ASYNC_REQUESTS
           * DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST
           * DASHSCOPE_CONNECTION_POOL_SIZE
           *
           */
          class SpeechSynthesizerObjectFactory
                  extends BasePooledObjectFactory<SpeechSynthesizer> {
              public SpeechSynthesizerObjectFactory() {
                  super();
              }
              @Override
              public SpeechSynthesizer create() throws Exception {
                  return new SpeechSynthesizer();
              }
              @Override
              public PooledObject<SpeechSynthesizer> wrap(SpeechSynthesizer obj) {
                  return new DefaultPooledObject<>(obj);
              }
          }
          class CosyvoiceObjectPool {
              public static GenericObjectPool<SpeechSynthesizer> synthesizerPool;
              public static String COSYVOICE_OBJECTPOOL_SIZE_ENV = "COSYVOICE_OBJECTPOOL_SIZE";
              public static int DEFAULT_OBJECT_POOL_SIZE = 500;
              private static Lock lock = new java.util.concurrent.locks.ReentrantLock();
              public static int getObjectivePoolSize() {
                  try {
                      Integer n = Integer.parseInt(System.getenv(COSYVOICE_OBJECTPOOL_SIZE_ENV));
                      System.out.println("Using Object Pool Size In Env: "+ n);
                      return n;
                  } catch (NumberFormatException e) {
                      System.out.println("Using Default Object Pool Size: "+ DEFAULT_OBJECT_POOL_SIZE);
                      return DEFAULT_OBJECT_POOL_SIZE;
                  }
              }
              public static GenericObjectPool<SpeechSynthesizer> getInstance() {
                  lock.lock();
                  if (synthesizerPool == null) {
                      // 您可以在这里设置对象池的大小。或在环境变量COSYVOICE_OBJECTPOOL_SIZE中设置。
                      // 建议设置为服务器最大并发连接数的1.5到2倍。
                      int objectPoolSize = getObjectivePoolSize();
                      SpeechSynthesizerObjectFactory speechSynthesizerObjectFactory =
                              new SpeechSynthesizerObjectFactory();
                      GenericObjectPoolConfig<SpeechSynthesizer> config =
                              new GenericObjectPoolConfig<>();
                      config.setMaxTotal(objectPoolSize);
                      config.setMaxIdle(objectPoolSize);
                      config.setMinIdle(objectPoolSize);
                      synthesizerPool =
                              new GenericObjectPool<>(speechSynthesizerObjectFactory, config);
                  }
                  lock.unlock();
                  return synthesizerPool;
              }
          }
          class SynthesizeTaskWithCallback implements Runnable {
              String[] textArray;
              String requestId;
              long timeCost;
              public SynthesizeTaskWithCallback(String[] textArray) {
                  this.textArray = textArray;
              }
              @Override
              public void run() {
                  SpeechSynthesizer synthesizer = null;
                  long startTime = System.currentTimeMillis();
                  // if recv onError
                  final boolean[] hasError = {false};
                  try {
                      class ReactCallback extends ResultCallback<SpeechSynthesisResult> {
                          ReactCallback() {}
                          @Override
                          public void onEvent(SpeechSynthesisResult message) {
                              if (message.getAudioFrame() != null) {
                                  try {
                                      byte[] bytesArray = message.getAudioFrame().array();
                                      System.out.println("收到音频，音频文件流length为：" + bytesArray.length);
                                  } catch (Exception e) {
                                      throw new RuntimeException(e);
                                  }
                              }
                          }
                          @Override
                          public void onComplete() {}
                          @Override
                          public void onError(Exception e) {
                              System.out.println(e.getMessage());
                              e.printStackTrace();
                              hasError[0] = true;
                          }
                      }
                      SpeechSynthesisParam param =
                              SpeechSynthesisParam.builder()
                                      .model("cosyvoice-v3-flash")
                                      .voice("longanyang")
                                      // 获取API Key：https://platform.qianwenai.com/home/api-keys
                                      // 若没有配置环境变量，请将下行替换为：.apiKey("sk-xxx")
                                      .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                                      .format(SpeechSynthesisAudioFormat
                                              .MP3_22050HZ_MONO_256KBPS) // 流式合成使用PCM或者MP3
                                      .build();
                      try {
                          synthesizer = CosyvoiceObjectPool.getInstance().borrowObject();
                          // 注意：对象池场景下，多次调用 updateParamAndCallback 时传入的 apiKey 必须始终相同；SDK 不会更新已建立连接的 apiKey，传入不同的 apiKey 不会生效。详见上文“进行语音合成”步骤的重要说明。
                          synthesizer.updateParamAndCallback(param, new ReactCallback());
                          for (String text : textArray) {
                              synthesizer.streamingCall(text);
                          }
                          Thread.sleep(20);
                          synthesizer.streamingComplete(60000);
                          requestId = synthesizer.getLastRequestId();
                      } catch (Exception e) {
                          System.out.println("Exception e: " + e.toString());
                          hasError[0] = true;
                      }
                  } catch (Exception e) {
                      hasError[0] = true;
                      throw new RuntimeException(e);
                  }
                  if (synthesizer != null) {
                      try {
                          if (hasError[0] == true) {
                              // 如果出现异常，则关闭连接并在对象池中禁用该对象。
                              synthesizer.getDuplexApi().close(1000, "bye");
                              CosyvoiceObjectPool.getInstance().invalidateObject(synthesizer);
                          } else {
                              // 如果任务正常结束，则归还对象。
                              CosyvoiceObjectPool.getInstance().returnObject(synthesizer);
                          }
                      } catch (Exception e) {
                          throw new RuntimeException(e);
                      }
                      long endTime = System.currentTimeMillis();
                      timeCost = endTime - startTime;
                      System.out.println("[线程 " + Thread.currentThread() + "] 语音合成任务结束。耗时 " + timeCost + " ms, RequestId " + requestId);
                  }
              }
          }
          @Slf4j
          public class SynthesizeTextToSpeechWithCallbackConcurrently {
              public static void checkoutEnv(String envName, int defaultSize) {
                  if (System.getenv(envName) != null) {
                      System.out.println("[ENV CHECK]: " + envName + " "
                              + System.getenv(envName));
                  } else {
                      System.out.println("[ENV CHECK]: " + envName
                              + " Using Default which is " + defaultSize);
                  }
              }
              public static void main(String[] args)
                      throws InterruptedException, NoApiKeyException {
                  Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";
                  // Check for connection pool env
                  checkoutEnv("DASHSCOPE_CONNECTION_POOL_SIZE", 32);
                  checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS", 32);
                  checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST", 32);
                  checkoutEnv(CosyvoiceObjectPool.COSYVOICE_OBJECTPOOL_SIZE_ENV, CosyvoiceObjectPool.DEFAULT_OBJECT_POOL_SIZE);
                  int runTimes = 3;
                  // Create the pool of SpeechSynthesis objects
                  ExecutorService executorService = Executors.newFixedThreadPool(runTimes);
                  for (int i = 0; i < runTimes; i++) {
                      // Record the task submission time
                      LocalDateTime submissionTime = LocalDateTime.now();
                      executorService.submit(new SynthesizeTaskWithCallback(new String[] {
                              "床前明月光，", "疑似地上霜。", "举头望明月，", "低头思故乡。"}));
                  }
                  // Shut down the ExecutorService and wait for all tasks to complete
                  executorService.shutdown();
                  executorService.awaitTermination(1, TimeUnit.MINUTES);
                  System.exit(0);
              }
          }
          ```
        </Accordion>

        #### 推荐配置

        以下配置基于在指定规格的阿里云服务器上仅运行 CosyVoice 语音合成服务的测试结果。过高的并发数可能导致任务处理延迟。其中单机并发数指的是同一时刻正在运行的 CosyVoice 语音合成任务数，也可以理解为工作线程数。

| 机器配置（阿里云） | 单机最大并发数 | 对象池大小 | 连接池大小 |
| --------- | ------- | ----- | ----- |
| 4核8GiB    | 100     | 500   | 2000  |
| 8核16GiB   | 150     | 500   | 2000  |
| 16核32GiB  | 200     | 500   | 2000  |

        #### 资源管理与异常处理

        - 任务成功：当语音合成任务正常完成时，必须调用 GenericObjectPool 的 returnObject 方法将 `SpeechSynthesizer` 对象归还到池中，以便复用。在当前代码中，对应 `CosyvoiceObjectPool.getInstance().returnObject(synthesizer)`。

          <Warning>
            不要归还未完成任务或任务失败的 `SpeechSynthesizer` 对象。
          </Warning>

        - 任务失败：当 SDK 内部或业务逻辑抛出异常导致任务中断时，必须执行以下两个操作：
          1. 主动关闭底层的 WebSocket 连接。
          2. 从对象池中废弃该对象，防止被再次使用。

        ```java
        // 在当前代码中对应如下内容
        // 关闭连接
        synthesizer.getDuplexApi().close(1000, "bye");
        // 在对象池中废弃出现异常的synthesizer
        CosyvoiceObjectPool.getInstance().invalidateObject(synthesizer);
        ```

        - 在服务出现 TaskFailed 报错时，不需要额外处理。

        #### 调用预热与耗时统计说明

        在对 DashScope Java SDK 进行并发调用延迟等性能评估时，建议先执行充分的预热操作，确保测量结果反映稳定状态下的真实性能，避免初始连接耗时导致数据偏差。

        **连接复用机制**：DashScope Java SDK 通过全局单例的连接池高效管理和复用 WebSocket 连接，旨在减少频繁建连和断连的开销，提升高并发场景下的处理能力。该机制的工作特点如下：

        - **按需创建**：SDK 不会在服务启动时预创建 WebSocket 连接，而是在首次调用时按需建立。
        - **限时复用**：请求完成后，连接将在池中保留最多 60 秒以备复用。
          - 若 60 秒内有新请求，将复用现有连接，避免重复握手开销。
          - 若连接空闲超过 60 秒，将被自动关闭以释放资源。

        **预热的重要性**：在以下场景中，连接池中可能没有可复用的活跃连接，导致请求需要新建连接：

        - 应用刚启动，尚未发起任何调用。
        - 服务空闲时间超过 60 秒，池中连接已因超时而关闭。

        在这些场景下，首次请求需完成 WebSocket 建连（TCP 握手、TLS 协商、协议升级），延迟显著高于后续复用连接的请求。若未预热，性能测试结果会因包含建连耗时而产生偏差。

        **SDK 侧延迟与实际首包延迟的区别**：SDK 侧打印的首包延迟（如通过 `get_first_package_delay()` 获取的值）包含了 WebSocket 建联和网络传输等耗时，并不等同于模型服务的实际首包延迟。实际首包延迟是指从服务端收到 `run-task` 指令到返回第一个 `result-generated` 事件的时间间隔，该值可通过服务端日志查看。在高并发场景下，由于大量连接的建立和资源调度，SDK 侧打印的延迟数值可能显著高于服务端的实际首包延迟。如果观察到 SDK 报告的首包延迟较高，建议：

        - 对比服务端日志中的首包延迟（从 `run-task` 到首个 `result-generated`），确认模型推理性能是否正常。
        - 使用上述对象池或连接池机制进行预热，消除 WebSocket 建连开销，使 SDK 侧打印的延迟更接近实际首包延迟。

        **推荐做法**：为获取可靠的性能数据，在正式进行性能压测或延迟统计前，请遵循以下预热步骤：

        1. 模拟正式测试的并发级别，提前发起一定数量的调用（例如，持续 1-2 分钟），以充分填充连接池。
        2. 确认连接池已建立并维持足够的活跃连接后，再开始正式的性能数据采集。

        通过合理的预热，可使 SDK 连接池进入稳定复用状态，从而测量出更具代表性的延迟指标，真实反映服务在线上平稳运行时的性能。

        #### Java SDK 常见异常

        <AccordionGroup>
          <Accordion title="异常 1、业务流量平稳，但是服务器 TCP 连接数持续上升">
            **出错原因：**

            **类型一：** 每一个 SDK 对象创建时都会申请一个连接。如果没有使用对象池，每一次任务结束后对象都被析构。此时这一个连接将进入无引用状态，需要等待 61s 秒后服务端报错连接超时才会真正断开，这会导致这个连接在 61 秒内不可复用。

            在高并发场景下，新的任务在发现没有可复用连接时会创建新连接，会造成如下后果：

            1. 连接数持续上升。
            2. 由于连接数过多，服务器资源不足，服务器卡顿。
            3. 连接池被打满、新任务由于启动时需要等待可用连接而阻塞。

            **类型二：** 对象池配置的 MaxIdle 小于 MaxTotal，导致在对象闲置时，超过 MaxIdle 的对象被销毁，从而造成连接泄漏。泄漏的连接需要等待 61 秒超时后断连，同类型一造成连接数持续上升。

            **解决方法**：

            对于类型一，使用对象池解决。

            对于类型二，检查对象池配置参数，设置 MaxIdle 和 MaxTotal 相等，关闭对象池自动销毁策略解决。
          </Accordion>

          <Accordion title="异常 2、任务耗时比正常调用多 60 秒">
            同“**异常 1**”，连接池已经达到最大连接限制，新的任务需要等待无引用状态的连接 61 秒触发超时后才可以获得连接。
          </Accordion>

          <Accordion title="异常 3、服务启动时任务慢，之后慢慢恢复正常">
            **出错原因**：在高并发调用时，同一个对象会复用同一个 WebSocket 连接，因此 WebSocket 连接只会在服务启动时创建。需要注意的是，任务启动阶段如果立刻开始较高并发调用，同时创建过多的 WebSocket 连接会导致阻塞。

            **解决方法**：启动服务后逐步提升并发量，或增加预热任务。
          </Accordion>

          <Accordion title="异常 4、服务端报错 Invalid action('run-task')! Please follow the protocol!">
            **出错原因**：这是由于出现了客户端报错后，服务端不知道客户端出错，连接处于任务中状态。此时连接和对象被复用并开启下一个任务，导致流程错误，下一个任务失败。

            **解决方法**：在抛出异常后主动关闭 WebSocket 连接后归还对象池。
          </Accordion>

          <Accordion title="异常 5、业务流量平稳，调用量出现异常尖刺">
            **出错原因**：同时创建过多 WebSocket 连接导致阻塞，但业务流量持续打进来，导致任务短时间积压，并且在阻塞后所有积压任务立刻调用。这会造成调用量尖刺，并且有可能造成瞬时超过账号的并发数限制导致部分任务失败、服务器卡顿等。

            这种瞬间创建过多 WebSocket 的情况多发生于：

            - 服务启动阶段
            - 网络出现异常，大量 WebSocket 连接同时中断重连
            - 某一时刻出现大量服务端报错，导致大量 WebSocket 重连。常见报错如并发数超过账号限制（“Requests rate limit exceeded, please try again later.”）。

            **解决方法**：

            1. 检查网络情况。
            2. 排查尖刺前是否出现大量其他服务端报错。
            3. 提高账号并发限制。
            4. 调小对象池和连接池大小，通过对象池上限限制最大并发数。
            5. 提升服务器配置或扩充机器数。
          </Accordion>

          <Accordion title="异常 6、随着并发数提升，所有任务都变慢">
            **解决方法**：

            1. 检查是否已经达到网络带宽上限。
            2. 检查实际并发数是否已经过高。
          </Accordion>
        </AccordionGroup>
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Sambert">
    Sambert 仅 Java SDK 内置了池化机制，Python SDK 暂不支持。

    **前提条件**：

    - [获取API Key](/api-reference/preparation/api-key)
    - 已安装符合版本要求的 DashScope Java SDK，建议[安装最新版](/api-reference/preparation/install-sdk)，SDK 版本需 ≥ 2.16.6。

    #### 推荐配置

    连接池和对象池不是越多越好，过少或过多都会导致程序运行变慢。建议根据服务器实际规格配置。在服务器上只运行 Sambert 语音合成服务的情况下，进行测试后得到了如下推荐配置供参考：

| 常见机器配置（阿里云） | 单机最大并发数 | 对象池大小 | 连接池大小 |
| ----------- | ------- | ----- | ----- |
| 4核8GiB      | 600     | 1200  | 2000  |

    单机并发数指的是同一时刻正在运行的 Sambert 语音合成任务的数量，也可以理解为工作线程数。

    <Warning>
      在高并发调用时，同一个对象会复用同一个 WebSocket 连接，因此 WebSocket 连接只会在服务启动时创建。同时创建过多的 WebSocket 连接会导致阻塞，启动服务时应逐步提高单机并发数。
    </Warning>

    #### 可配置参数

    **连接池**：DashScope Java SDK 使用了 OkHttp3 提供的连接池来复用 WebSocket 连接，从而减少频繁创建 WebSocket 连接的耗时和资源开销。连接池是 DashScope SDK 默认开启的优化项，需要根据使用场景配置连接池大小。请在运行 Java 服务前，通过环境变量的方式提前按需配置好连接池的相关参数。连接池配置参数如下：

| 环境变量                                           | 描述                                      |
| ---------------------------------------------- | --------------------------------------- |
| DASHSCOPE\_CONNECTION\_POOL\_SIZE              | 配置连接池大小。默认值为 32。推荐配置为峰值并发数的 2 倍以上。      |
| DASHSCOPE\_MAXIMUM\_ASYNC\_REQUESTS            | 配置最大异步请求数。默认值为 32。推荐配置为和连接池大小一致。        |
| DASHSCOPE\_MAXIMUM\_ASYNC\_REQUESTS\_PER\_HOST | 配置单 host 最大异步请求数。默认值为 32。推荐配置为和连接池大小一致。 |

    **对象池**：推荐使用对象池的方式来复用 `SpeechSynthesizer` 对象，这样可以进一步降低反复创建和销毁对象带来的内存和时间开销。请在运行 Java 服务前，通过环境变量或代码的方式提前按需配置好对象池的大小。对象池配置参数如下：

| 环境变量                      | 描述                                                                  |
| ------------------------- | ------------------------------------------------------------------- |
| SAMBERT\_OBJECTPOOL\_SIZE | 对象池大小。推荐配置为峰值并发数的 1.5\~2 倍。对象池大小需要小于或等于连接池大小，否则会出现对象等待连接的情况，导致调用阻塞。 |

    关于如何配置环境变量，可参考[设置环境变量](/api-reference/preparation/export-api-key-env)。

    #### 示例代码

    以下为使用资源池的示例代码。其中，对象池为全局单例对象。

    - 每个主账号默认每秒可提交 3 个 Sambert 语音合成任务。如需开通更高 QPS 请[联系我们](https://smartservice.console.aliyun.com/service/create-ticket)。
    - 需要在项目中引入 DashScope 和 org.apache.commons.pool2 相关的包，DashScope 要求版本号 >= 2.16.9。

    <CodeGroup>
      ```xml Maven
      <dependency>
          <groupId>com.alibaba</groupId>
          <artifactId>dashscope-sdk-java</artifactId>
          <!-- 请将 'the-latest-version' 替换为2.16.9及以上版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java -->
          <version>the-latest-version</version>
      </dependency>
      <dependency>
          <groupId>org.apache.commons</groupId>
          <artifactId>commons-pool2</artifactId>
          <!-- 请将 'the-latest-version' 替换为最新版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/org.apache.commons/commons-pool2 -->
          <version>the-latest-version</version>
      </dependency>
      ```

      ```groovy Gradle
      dependencies {
          // 请将 'the-latest-version' 替换为2.16.9及以上版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
          implementation group: 'com.alibaba', name: 'dashscope-sdk-java', version: 'the-latest-version'
          // 请将 'the-latest-version' 替换为最新版本，可在如下链接查询相关版本号：https://mvnrepository.com/artifact/org.apache.commons/commons-pool2
          implementation group: 'org.apache.commons', name: 'commons-pool2', version: 'the-latest-version'
      }
      ```
    </CodeGroup>

    示例代码中，不同的线程通过等待随机时间来避免同时创建过多的 WebSocket 连接。

    <Accordion title="完整代码">
      ```java
      import com.alibaba.dashscope.audio.tts.SpeechSynthesisAudioFormat;
      import com.alibaba.dashscope.audio.tts.SpeechSynthesisParam;
      import com.alibaba.dashscope.audio.tts.SpeechSynthesisResult;
      import com.alibaba.dashscope.audio.tts.SpeechSynthesizer;
      import com.alibaba.dashscope.common.ResultCallback;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import lombok.extern.slf4j.Slf4j;
      import org.apache.commons.pool2.BasePooledObjectFactory;
      import org.apache.commons.pool2.PooledObject;
      import org.apache.commons.pool2.impl.DefaultPooledObject;
      import org.apache.commons.pool2.impl.GenericObjectPool;
      import org.apache.commons.pool2.impl.GenericObjectPoolConfig;
      import java.util.Random;
      import java.util.concurrent.CountDownLatch;
      import java.util.concurrent.ExecutorService;
      import java.util.concurrent.Executors;
      import java.util.concurrent.TimeUnit;
      import java.util.concurrent.locks.Lock;
      import com.alibaba.dashscope.utils.Constants;
      /**
       * Before making high-concurrency calls to the TTS service,
       * please configure the connection pool size through following environment
       * variables.
       *
       * DASHSCOPE_MAXIMUM_ASYNC_REQUESTS=2000
       * DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST=2000
       * DASHSCOPE_CONNECTION_POOL_SIZE=2000
       *
       * The default is 32, and it is recommended to set it to 2 times the maximum
       * concurrent connections of a single server.
       */
      @Slf4j
      public class SynthesizeTextToSpeechUsingSambertConcurrently {
          public static void checkoutEnv(String envName, int defaultSize) {
              if (System.getenv(envName) != null) {
                  System.out.println("[ENV CHECK]: " + envName + " "
                          + System.getenv(envName));
              } else {
                  System.out.println("[ENV CHECK]: " + envName
                          + " Using Default which is " + defaultSize);
              }
          }
          public static void main(String[] args)
                  throws InterruptedException, NoApiKeyException {
              Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              // Check for connection pool env
              checkoutEnv("DASHSCOPE_CONNECTION_POOL_SIZE", 32);
              checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS", 32);
              checkoutEnv(SambertObjectPool.SAMBERT_OBJECTPOOL_SIZE_ENV, SambertObjectPool.DEFAULT_CONNECTION_POOL_SIZE);
              checkoutEnv("DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST", 32);
              // Record task start time
              int runTimes = 1;
              // Create the pool of SpeechSynthesis objects
              ExecutorService executorService = Executors.newFixedThreadPool(runTimes);
              for (int i = 0; i < runTimes; i++) {
                  executorService.submit(new SynthesizeTask(new String[]{
                          "床前明月光，",
                          "疑似地上霜。",
                          "举头望明月，",
                          "低头思故乡。"
                  }));
              }
              // Shut down the ExecutorService and wait for all tasks to complete
              executorService.shutdown();
              executorService.awaitTermination(1, TimeUnit.MINUTES);
              System.exit(0);
          }
      }
      class SpeechSynthesizerObjectFactory
              extends BasePooledObjectFactory<SpeechSynthesizer> {
          public SpeechSynthesizerObjectFactory() {
              super();
          }
          @Override
          public SpeechSynthesizer create() throws Exception {
              return new SpeechSynthesizer();
          }
          @Override
          public PooledObject<SpeechSynthesizer> wrap(SpeechSynthesizer obj) {
              return new DefaultPooledObject<>(obj);
          }
      }
      class SambertObjectPool {
          public static GenericObjectPool<SpeechSynthesizer> synthesizerPool;
          public static String SAMBERT_OBJECTPOOL_SIZE_ENV = "SAMBERT_OBJECTPOOL_SIZE";
          public static int DEFAULT_CONNECTION_POOL_SIZE = 500;
          private static Lock lock = new java.util.concurrent.locks.ReentrantLock();
          public static int getObjectivePoolSize() {
              try {
                  Integer n = Integer.parseInt(System.getenv(SAMBERT_OBJECTPOOL_SIZE_ENV));
                  return n;
              } catch (NumberFormatException e) {
                  return DEFAULT_CONNECTION_POOL_SIZE;
              }
          }
          public static GenericObjectPool<SpeechSynthesizer> getInstance() {
              lock.lock();
              if (synthesizerPool == null) {
                  // You can set the object pool size here. or in environment variable
                  // SAMBERT_OBJECTPOOL_SIZE It is recommended to set it to 1.5 to 2 times
                  // your server's maximum concurrent connections.
                  int objectPoolSize = getObjectivePoolSize();
                  SpeechSynthesizerObjectFactory speechSynthesizerObjectFactory =
                          new SpeechSynthesizerObjectFactory();
                  GenericObjectPoolConfig<SpeechSynthesizer> config =
                          new GenericObjectPoolConfig<>();
                  config.setMaxTotal(objectPoolSize);
                  config.setMaxIdle(objectPoolSize);
                  config.setMinIdle(objectPoolSize);
                  synthesizerPool =
                          new GenericObjectPool<>(speechSynthesizerObjectFactory, config);
              }
              lock.unlock();
              return synthesizerPool;
          }
      }
      class SynthesizeTask implements Runnable {
          String[] textList;
          String requestId;
          long timeCost;
          public SynthesizeTask(String[] textList) {
              this.textList = textList;
          }
          @Override
          public void run() {
              // sleep random time before start task, avoid creating too much websocket at the same time.
              Random random = new Random();
              try {
                  Thread.sleep(random.nextInt(30*1000));
              } catch (InterruptedException e) {
                  throw new RuntimeException(e);
              }
              for (String text:textList) {
                  SpeechSynthesizer synthesizer = null;
                  long startTime = System.currentTimeMillis();
                  try {
                      CountDownLatch latch = new CountDownLatch(1);
                      class ReactCallback extends ResultCallback<SpeechSynthesisResult> {
                          ReactCallback() {}
                          @Override
                          public void onEvent(SpeechSynthesisResult message) {
                              if (message.getAudioFrame() != null) {
                                  try {
                                      byte[] bytesArray = message.getAudioFrame().array();
                                  } catch (Exception e) {
                                      throw new RuntimeException(e);
                                  }
                              }
                          }
                          @Override
                          public void onComplete() {
                              latch.countDown();
                          }
                          @Override
                          public void onError(Exception e) {
                              System.out.println(e.getMessage());
                              e.printStackTrace();
                              latch.countDown();
                          }
                      }
                      SpeechSynthesisParam param =
                              SpeechSynthesisParam.builder()
                                      .model("sambert-zhichu-v1")
                                      .format(SpeechSynthesisAudioFormat.MP3) // 使用PCM或者MP3
                                      .text(text)
                                      .enablePhonemeTimestamp(true)
                                      .enableWordTimestamp(true)
                                      // 若没有配置环境变量，请将下行替换为：.apiKey("sk-xxx")
                                      .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                                      .build();
                      try {
                          synthesizer = SambertObjectPool.getInstance().borrowObject();
                          synthesizer.call(param, new ReactCallback());
                          try {
                              latch.await();
                          } catch (InterruptedException e) {
                              throw new RuntimeException(e);
                          }
                          requestId = synthesizer.getLastRequestId();
                      } catch (Exception e) {
                          System.out.println("Exception e: " + e.toString());
                          synthesizer.getSyncApi().close(1000, "bye");
                      }
                  } catch (Exception e) {
                      throw new RuntimeException(e);
                  } finally {
                      if (synthesizer != null) {
                          try {
                              // Return the SpeechSynthesizer object to the pool
                              SambertObjectPool.getInstance().returnObject(synthesizer);
                          } catch (Exception e) {
                              e.printStackTrace();
                          }
                      }
                  }
                  long endTime = System.currentTimeMillis();
                  timeCost = endTime - startTime;
                  System.out.println("[线程" + Thread.currentThread() + "] 语音合成任务:(" + text + ")结束。耗时" + timeCost + "ms, RequestId" + requestId);
              }
          }
      }
      ```
    </Accordion>

    ##### 异常处理

    - 在服务出现 TaskFailed 报错时，不需要额外处理。
    - 如果在语音合成中途，客户端出现错误（如 SDK 内部异常或业务逻辑异常）导致语音合成任务未完成，则需要主动关闭连接。关闭连接方法如下：

    ```java
    // 将下面这段代码放在try-catch块中
    synthesizer.getSyncApi().close(1000, "bye");
    ```

    #### 常见异常

    <AccordionGroup>
      <Accordion title="异常 1、业务流量平稳，但是服务器 TCP 连接数持续上升">
        **出错原因：**

        **类型一：** 每一个 SDK 对象创建时都会申请一个连接。如果没有使用对象池，每一次任务结束后对象都被析构。此时这一个连接将进入无引用状态，需要等待 61s 秒后服务端报错连接超时才会真正断开，这会导致这个连接在 61 秒内不可复用。

        在高并发场景下，新的任务在发现没有可复用连接时会创建新连接，会造成如下后果：

        1. 连接数持续上升。
        2. 由于连接数过多，服务器资源不足，服务器卡顿。
        3. 连接池被打满、新任务由于启动时需要等待可用连接而阻塞。

        **类型二：** 对象池配置的 MaxIdle 小于 MaxTotal，导致在对象闲置时，超过 MaxIdle 的对象被销毁，从而造成连接泄漏。泄漏的连接需要等待 61 秒超时后断连，同类型一造成连接数持续上升。

        **解决方法**：

        对于类型一，使用对象池解决。

        对于类型二，检查对象池配置参数，设置 MaxIdle 和 MaxTotal 相等，关闭对象池自动销毁策略解决。
      </Accordion>

      <Accordion title="异常 2、任务耗时比正常调用多 60 秒">
        同“**异常 1**”，连接池已经达到最大连接限制，新的任务需要等待无引用状态的连接 61 秒触发超时后才可以获得连接。
      </Accordion>

      <Accordion title="异常 3、服务启动时任务慢，之后慢慢恢复正常">
        **出错原因**：在高并发调用时，同一个对象会复用同一个 WebSocket 连接，因此 WebSocket 连接只会在服务启动时创建。需要注意的是，任务启动阶段如果立刻开始较高并发调用，同时创建过多的 WebSocket 连接会导致阻塞。

        **解决方法**：启动服务后逐步提升并发量，或增加预热任务。
      </Accordion>

      <Accordion title="异常 4、服务端报错 Invalid action('run-task')! Please follow the protocol!">
        **出错原因**：这是由于出现了客户端报错后，服务端不知道客户端出错，连接处于任务中状态。此时连接和对象被复用并开启下一个任务，导致流程错误，下一个任务失败。

        **解决方法**：在抛出异常后主动关闭 WebSocket 连接后归还对象池。
      </Accordion>

      <Accordion title="异常 5、业务流量平稳，调用量出现异常尖刺">
        **出错原因**：同时创建过多 WebSocket 连接导致阻塞，但业务流量持续打进来，导致任务短时间积压，并且在阻塞后所有积压任务立刻调用。这会造成调用量尖刺，并且有可能造成瞬时超过账号的并发数限制导致部分任务失败、服务器卡顿等。

        这种瞬间创建过多 WebSocket 的情况多发生于：

        - 服务启动阶段
        - 网络出现异常，大量 WebSocket 连接同时中断重连
        - 某一时刻出现大量服务端报错，导致大量 WebSocket 重连。常见报错如并发数超过账号限制（“Requests rate limit exceeded, please try again later.”）。

        **解决方法**：

        1. 检查网络情况。
        2. 排查尖刺前是否出现大量其他服务端报错。
        3. 提高账号并发限制。
        4. 调小对象池和连接池大小，通过对象池上限限制最大并发数。
        5. 提升服务器配置或扩充机器数。
      </Accordion>

      <Accordion title="异常 6、随着并发数提升，所有任务都变慢">
        **解决方法**：

        1. 检查是否已经达到网络带宽上限。
        2. 检查实际并发数是否已经过高。
      </Accordion>
    </AccordionGroup>
  </Tab>
</Tabs>

## API 参考

<Tabs>
  <Tab title="Qwen-Audio-TTS">
    Qwen-Audio-TTS 与 CosyVoice 使用相同的 API，仅需替换 `model` 和 `voice` 参数：

    - [语音合成 API 参考](/api-reference/speech-synthesis/cosyvoice/python-sdk)
    - [声音复刻/设计 API 参考](/api-reference/speech-synthesis/voice-cloning/create-voice)
  </Tab>

  <Tab title="CosyVoice">
    - [语音合成 API 参考](/api-reference/speech-synthesis/cosyvoice/python-sdk)
    - [声音复刻/设计 API 参考](/api-reference/speech-synthesis/voice-cloning/create-voice)
    - [AOQ 客户端 API](/developer-guides/realtime-api/aoq-sdk-intro)（适用于 CosyVoice 系列模型）
  </Tab>

  <Tab title="Qwen-TTS-Realtime">
    - [实时流式语音合成 API 参考](/api-reference/speech-synthesis/qwen-tts-realtime/client-events)
    - [声音克隆 API 参考](/api-reference/speech-synthesis/voice-cloning/create-voice)
    - [声音设计 API 参考](/api-reference/speech-synthesis/voice-design/create-voice)
  </Tab>
</Tabs>

## 系统音色

<Tabs>
  <Tab title="Qwen-Audio-TTS">
    [Qwen-Audio-TTS 音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list)
  </Tab>

  <Tab title="CosyVoice">
    [CosyVoice voice list](/api-reference/speech-synthesis/cosyvoice/voice-list)
  </Tab>

  <Tab title="Qwen-TTS-Realtime">
    [Qwen-TTS 音色列表](/api-reference/speech-synthesis/qwen-tts/voice-list)
  </Tab>
</Tabs>

## 常见问题

<AccordionGroup>
  <Accordion title="语音合成发音错误怎么办？多音字如何控制发音？">
    - 将多音字替换为同音的其他汉字，快速解决发音问题。
    - 使用 [SSML](/developer-guides/speech/ssml) 标记语言控制发音：Sambert 和 CosyVoice 均支持 SSML。
  </Accordion>

  <Accordion title="使用复刻音色生成的音频无声音如何排查？">
    1. **确认音色状态**：调用 [CosyVoice 声音复刻/设计 API](/api-reference/speech-synthesis/voice-cloning/create-voice) 接口，确认音色的 `status` 是否为 `OK`。
    2. **检查模型版本一致性**：确保复刻音色时使用的 `target_model` 参数与语音合成时的 `model` 参数完全一致。例如复刻时使用 `cosyvoice-v3-plus`，合成时也必须使用 `cosyvoice-v3-plus`。
    3. **验证源音频质量**：检查复刻音色时使用的源音频是否符合 [CosyVoice 声音复刻/设计 API](/api-reference/speech-synthesis/voice-cloning/create-voice) 的音频要求（音频时长 10-20 秒、音质清晰、无背景噪音）。
    4. **检查请求参数**：确认语音合成请求中的 `voice` 参数已设置为复刻音色的 ID。
  </Accordion>

  <Accordion title="声音复刻后合成效果不稳定或语音不完整怎么办？">
    如果复刻音色后合成的语音出现以下问题：

    - 语音播放不完整，只读出部分文字
    - 合成效果不稳定，时好时坏
    - 语音中包含异常停顿或静音段

    可能原因：源音频质量不符合要求。

    解决方案：请检查源音频是否符合 [CosyVoice 声音复刻/设计 API](/api-reference/speech-synthesis/voice-cloning/create-voice) 中的音频要求，建议重新录制。
  </Accordion>

  <Accordion title="为什么语音合成的实际时长与 WAV 文件显示的时长不一致？">
    语音合成采用流式机制，边合成边返回数据，因此保存的 WAV 文件头中的时长是预估值，存在一定误差。如需精确时长，可将 `format` 设置为 `pcm`，待获取完整合成结果后自行添加 WAV 文件头信息。
  </Accordion>

  <Accordion title="为什么音频无法播放？">
    请按以下场景逐一排查：

    - **音频保存为完整文件（如 xx.mp3）的情况**
      - 音频格式一致性：请求参数中的音频格式须与文件后缀一致（如参数为 `wav` 则文件须为 `.wav`）。
      - 播放器兼容性：确认播放器支持该音频的格式和采样率。
    - **流式播放音频的情况**
      - 将音频流保存为完整文件，尝试用播放器播放。如果文件无法播放，请参考场景 1 的排查方法。
      - 如果文件可正常播放，则问题在流式播放实现。请确认播放器支持流式播放（如 ffmpeg、pyaudio、AudioFormat、MediaSource 等）。
  </Accordion>

  <Accordion title="为什么音频播放卡顿？">
    请按以下步骤逐一排查：

    - 检查文本发送速度：确保发送间隔合理，避免上段音频播完后下段文本尚未到达。
    - 检查回调函数性能：
      - 确认回调函数中无阻塞性业务逻辑。
      - 回调运行在 WebSocket 线程，阻塞会影响数据接收。建议将音频数据写入独立缓冲区，在其他线程中处理。
    - 检查网络稳定性：网络波动可能导致音频传输中断或延迟。
  </Accordion>

  <Accordion title="语音合成耗时较长是什么原因？">
    请按以下步骤排查：

    - 检查输入间隔：如果是流式合成，确认文本发送间隔是否过长，过长会导致合成总时长增加。
    - 分析性能指标：
      - 首包延迟：正常约 500ms。
      - RTF（实时率 = 合成总耗时 / 音频时长）：正常应小于 1.0。
  </Accordion>

  <Accordion title="合成的音频中读出了文本里的特殊符号怎么办？">
    Qwen-TTS 系列模型可能将文本中的部分特殊符号（如 Markdown 加粗标记 `**`）合成为语音。可通过以下方式处理：

    1. 调用前对文本进行预处理，去除特殊符号。
    2. 改用 CosyVoice 模型。
  </Accordion>

  <Accordion title="如何限制 API Key 仅用于语音合成服务（权限隔离）？">
    通过新建业务空间并仅授权特定模型，可限制 API Key 的使用范围。请参见[业务空间](/developer-guides/administration/workspace)。
  </Accordion>

  <Accordion title="子业务空间的 API Key 能否调用 CosyVoice 模型？">
    默认业务空间下，所有模型均可调用。

    子业务空间下，需要为 API Key 对应的子业务空间进行模型授权。请参见[业务空间](/developer-guides/administration/workspace)。
  </Accordion>
</AccordionGroup>
