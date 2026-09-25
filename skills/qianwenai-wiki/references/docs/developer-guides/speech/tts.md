> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 非实时语音合成

> 使用 Qwen3-TTS、CosyVoice 和 MiniMax 进行非实时语音合成

非实时语音合成通过 HTTP API 将文本转换为语音，适用于有声读物、课件配音、内容生产等对延迟不敏感的场景。支持 Qwen-TTS、CosyVoice 和 MiniMax 多种模型系列，提供丰富音色、多语言支持、声音复刻与声音设计等能力。

## 支持的模型

调用以下模型时需使用 [API Key](https://platform.qianwenai.com/home/api-keys)：

- **Qwen3-TTS-Instruct-Flash**
- **Qwen3-TTS-VD**
- **Qwen3-TTS-VC**
- **Qwen3-TTS-Flash**
- **cosyvoice-v3-plus**
- **cosyvoice-v3-flash**
- **MiniMax**（MiniMax-Speech-02-HD）

模型 ID 和快照版本详见[语音合成模型](/developer-guides/speech/tts-models)。

<Note>
  CosyVoice 使用 DashScope WebSocket SDK（`dashscope.audio.tts_v2` 中的 `SpeechSynthesizer`），而非 Qwen3-TTS 所用的 HTTP REST API。如需使用 CosyVoice 进行实时流式合成，请参见[实时语音合成](/developer-guides/speech/realtime-streaming)。
</Note>

## 快速开始

<Tabs>
  <Tab title="Qwen3-TTS">
    **前提条件**

    - [获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。
    - 如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。Java SDK 需要 2.21.9+ 版本，Python SDK 需要 1.24.6+ 版本。

    <Note>
      在 DashScope Python SDK 中，`SpeechSynthesizer` 接口已替换为 `MultiModalConversation`。升级时只需替换接口名称，其他参数完全兼容。
    </Note>

    #### 使用系统音色

    使用[系统音色](#系统音色)进行语音合成。

    **非流式输出**

    通过返回的 `url` 获取合成后的音频文件，该 URL 有效期为 24 小时。

    Java 需要导入 Gson 依赖。如果使用 Maven 或 Gradle，按如下方式添加依赖：

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

    <CodeGroup>
      ```python Python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      text = "Today is a wonderful day to build something people love!"
      # 使用 SpeechSynthesizer 接口：dashscope.audio.qwen_tts.SpeechSynthesizer.call(...)
      response = dashscope.MultiModalConversation.call(
        # 如需使用指令控制，请将模型替换为 qwen3-tts-instruct-flash。
        model="qwen3-tts-flash",
        # 如未配置环境变量，请将下行替换为：api_key = "sk-xxx"
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        voice="Cherry",
        language_type="English", # 建议与文本语言保持一致，以确保发音正确、语调自然。
        # 如需使用指令控制，请取消以下注释，并将模型替换为 qwen3-tts-instruct-flash。
        # instructions='Speak quickly with a noticeable rising intonation, suitable for introducing fashion products.',
        # optimize_instructions=True,
        stream=False
      )
      print(response)
      ```

      ```java Java
      import com.alibaba.dashscope.aigc.multimodalconversation.AudioParameters;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.protocol.Protocol;
      import com.alibaba.dashscope.utils.Constants;

      import java.io.FileOutputStream;
      import java.io.InputStream;
      import java.net.URL;

      public class Main {
        // 如需使用指令控制，请将 MODEL 替换为 qwen3-tts-instruct-flash。
        private static final String MODEL = "qwen3-tts-flash";
        public static void call() throws ApiException, NoApiKeyException, UploadFileException {
          MultiModalConversation conv = new MultiModalConversation();
          MultiModalConversationParam param = MultiModalConversationParam.builder()
              // 如未配置环境变量，请将下行替换为：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model(MODEL)
              .text("Today is a wonderful day to build something people love!")
              .voice(AudioParameters.Voice.CHERRY)
              .languageType("English") // 建议与文本语言保持一致，以确保发音正确、语调自然。
              // 如需使用指令控制，请取消以下注释，并将模型替换为 qwen3-tts-instruct-flash。
              // .parameter("instructions","Speak quickly with a noticeable rising intonation, suitable for introducing fashion products.")
              // .parameter("optimize_instructions",true)
              .build();
          MultiModalConversationResult result = conv.call(param);
          String audioUrl = result.getOutput().getAudio().getUrl();
          System.out.print(audioUrl);

          // 下载音频文件到本地
          try (InputStream in = new URL(audioUrl).openStream();
                   FileOutputStream out = new FileOutputStream("downloaded_audio.wav")) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = in.read(buffer)) != -1) {
              out.write(buffer, 0, bytesRead);
            }
            System.out.println("\n音频文件已下载到本地：downloaded_audio.wav");
          } catch (Exception e) {
            System.out.println("\n下载音频文件出错：" + e.getMessage());
          }
        }
        public static void main(String[] args) {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
          try {
            call();
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
          System.exit(0);
        }
      }
      ```

      ```bash cURL
      curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "model": "qwen3-tts-flash",
        "input": {
          "text": "Today is a wonderful day to build something people love!",
          "voice": "Cherry",
          "language_type": "English"
        }
      }'
      ```
    </CodeGroup>

    **流式输出**

    以 Base64 格式流式输出音频数据。最后一个数据包包含完整音频文件的 URL。

    <CodeGroup>
      ```python Python
      # coding=utf-8
      #
      # pyaudio 安装说明：
      # APPLE Mac OS X
      #   brew install portaudio
      #   pip install pyaudio
      # Debian/Ubuntu
      #   sudo apt-get install python-pyaudio python3-pyaudio
      #   或
      #   pip install pyaudio
      # CentOS
      #   sudo yum install -y portaudio portaudio-devel && pip install pyaudio
      # Microsoft Windows
      #   python -m pip install pyaudio

      import os
      import dashscope
      import pyaudio
      import time
      import base64
      import numpy as np

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      p = pyaudio.PyAudio()
      # 创建音频流
      stream = p.open(format=pyaudio.paInt16,
              channels=1,
              rate=24000,
              output=True)

      text = "Today is a wonderful day to build something people love!"
      response = dashscope.MultiModalConversation.call(
        # 如未配置环境变量，请将下行替换为：api_key = "sk-xxx"
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        # 如需使用指令控制，请将模型替换为 qwen3-tts-instruct-flash。
        model="qwen3-tts-flash",
        text=text,
        voice="Cherry",
        language_type="English", # 建议与文本语言保持一致，以确保发音正确、语调自然。
        # 如需使用指令控制，请取消以下注释，并将模型替换为 qwen3-tts-instruct-flash。
        # instructions='Speak quickly with a noticeable rising intonation, suitable for introducing fashion products.',
        # optimize_instructions=True,
        stream=True
      )

      for chunk in response:
        if chunk.output is not None:
            audio = chunk.output.audio
            if audio.data is not None:
                wav_bytes = base64.b64decode(audio.data)
                audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
                # 直接播放音频数据
                stream.write(audio_np.tobytes())
            if chunk.output.finish_reason == "stop":
                print("finish at: {} ", chunk.output.audio.expires_at)
      time.sleep(0.8)
      # 清理资源
      stream.stop_stream()
      stream.close()
      p.terminate()
      ```

      ```java Java
      // 安装最新版本的 DashScope SDK
      import com.alibaba.dashscope.aigc.multimodalconversation.AudioParameters;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.protocol.Protocol;
      import com.alibaba.dashscope.utils.Constants;
      import io.reactivex.Flowable;
      import javax.sound.sampled.*;
      import java.util.Base64;

      public class Main {
        // 如需使用指令控制，请将 MODEL 替换为 qwen3-tts-instruct-flash。
        private static final String MODEL = "qwen3-tts-flash";
        public static void streamCall() throws ApiException, NoApiKeyException, UploadFileException {
          MultiModalConversation conv = new MultiModalConversation();
          MultiModalConversationParam param = MultiModalConversationParam.builder()
              // 如未配置环境变量，请将下行替换为：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model(MODEL)
              .text("Today is a wonderful day to build something people love!")
              .voice(AudioParameters.Voice.CHERRY)
              .languageType("English") // 建议与文本语言保持一致，以确保发音正确、语调自然。
              // 如需使用指令控制，请取消以下注释，并将模型替换为 qwen3-tts-instruct-flash。
              // .parameter("instructions","Speak quickly with a noticeable rising intonation, suitable for introducing fashion products.")
              // .parameter("optimize_instructions",true)
              .build();
          Flowable<MultiModalConversationResult> result = conv.streamCall(param);
          result.blockingForEach(r -> {
            try {
              // 1. 获取 Base64 编码的音频数据
              String base64Data = r.getOutput().getAudio().getData();
              byte[] audioBytes = Base64.getDecoder().decode(base64Data);

              // 2. 配置音频格式（根据 API 返回的格式调整）
              AudioFormat format = new AudioFormat(
                  AudioFormat.Encoding.PCM_SIGNED,
                  24000, // 采样率（需与 API 返回的格式一致）
                  16,    // 音频位深度
                  1,     // 声道数
                  2,     // 帧大小（位深度 / 8）
                  24000, // 数据传输速率（需与采样率一致）
                  false  // 是否压缩
              );

              // 3. 实时播放音频数据
              DataLine.Info info = new DataLine.Info(SourceDataLine.class, format);
              try (SourceDataLine line = (SourceDataLine) AudioSystem.getLine(info)) {
                if (line != null) {
                  line.open(format);
                  line.start();
                  line.write(audioBytes, 0, audioBytes.length);
                  line.drain();
                }
              }
            } catch (LineUnavailableException e) {
              e.printStackTrace();
            }
          });
        }
        public static void main(String[] args) {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
          try {
            streamCall();
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
          System.exit(0);
        }
      }
      ```

      ```bash cURL
      curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -H 'X-DashScope-SSE: enable' \
      -d '{
        "model": "qwen3-tts-flash",
        "input": {
          "text": "Today is a wonderful day to build something people love!",
          "voice": "Cherry",
          "language_type": "English"
        }
      }'
      ```
    </CodeGroup>

    #### 使用克隆音色

    声音克隆不提供预览音频。将克隆音色应用于语音合成后才能评估效果。

    以下示例基于非流式输出代码，将 `voice` 参数替换为克隆音色。

    - **关键原则**：声音克隆所用的模型（`target_model`）必须与语音合成所用的模型（`model`）一致，否则合成将失败。
    - 本示例使用本地音频文件 `voice.mp3` 进行声音克隆，运行代码时请替换该路径。

    Java 需要添加 Gson 依赖。如果使用 Maven 或 Gradle，按如下方式添加依赖：

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

    <Warning>
      使用声音克隆生成的自定义音色进行语音合成时，请按如下方式设置 voice 参数：

      ```java
      MultiModalConversationParam param = MultiModalConversationParam.builder()
              .parameter("voice", "your_voice") // 将 voice 参数替换为克隆生成的自定义音色
              .build();
      ```
    </Warning>

    <CodeGroup>
      ```python Python
      import os
      import requests
      import base64
      import pathlib
      import dashscope

      # ======= 常量配置 =======
      DEFAULT_TARGET_MODEL = "qwen3-tts-vc-2026-01-22"  # 声音克隆和语音合成使用同一模型
      DEFAULT_PREFERRED_NAME = "guanyu"
      DEFAULT_AUDIO_MIME_TYPE = "audio/mpeg"
      VOICE_FILE_PATH = "voice.mp3"  # 用于声音克隆的本地音频文件相对路径

      def create_voice(file_path: str,
                       target_model: str = DEFAULT_TARGET_MODEL,
                       preferred_name: str = DEFAULT_PREFERRED_NAME,
                       audio_mime_type: str = DEFAULT_AUDIO_MIME_TYPE) -> str:
        """
        创建音色并返回 voice 参数。
        """
        # 如未配置环境变量，请将下行替换为：api_key = "sk-xxx"
        api_key = os.getenv("DASHSCOPE_API_KEY")

        file_path_obj = pathlib.Path(file_path)
        if not file_path_obj.exists():
          raise FileNotFoundError(f"音频文件不存在：{file_path}")

        base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
        data_uri = f"data:{audio_mime_type};base64,{base64_str}"

        url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
        payload = {
          "model": "qwen-voice-enrollment", # 请勿修改此值
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
          raise RuntimeError(f"创建音色失败：{resp.status_code}, {resp.text}")

        try:
          return resp.json()["output"]["voice"]
        except (KeyError, ValueError) as e:
          raise RuntimeError(f"解析音色响应失败：{e}")

      if __name__ == '__main__':
        dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

        text = "How's the weather today?"
        # 使用 SpeechSynthesizer 接口：dashscope.audio.qwen_tts.SpeechSynthesizer.call(...)
        response = dashscope.MultiModalConversation.call(
          model=DEFAULT_TARGET_MODEL,
          # 如未配置环境变量，请将下行替换为：api_key = "sk-xxx"
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          text=text,
          voice=create_voice(VOICE_FILE_PATH), # 将 voice 参数替换为克隆生成的自定义音色
          stream=False
        )
        print(response)
      ```

      ```java Java
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.utils.Constants;
      import com.google.gson.Gson;
      import com.google.gson.JsonObject;

      import java.io.*;
      import java.net.HttpURLConnection;
      import java.net.URL;
      import java.nio.file.*;
      import java.nio.charset.StandardCharsets;
      import java.util.Base64;

      public class Main {
        // ===== 常量定义 =====
        // 声音克隆和语音合成使用同一模型
        private static final String TARGET_MODEL = "qwen3-tts-vc-2026-01-22";
        private static final String PREFERRED_NAME = "guanyu";
        // 用于声音克隆的本地音频文件相对路径
        private static final String AUDIO_FILE = "voice.mp3";
        private static final String AUDIO_MIME_TYPE = "audio/mpeg";

        // 生成 data URI
        public static String toDataUrl(String filePath) throws IOException {
          byte[] bytes = Files.readAllBytes(Paths.get(filePath));
          String encoded = Base64.getEncoder().encodeToString(bytes);
          return "data:" + AUDIO_MIME_TYPE + ";base64," + encoded;
        }

        // 调用 API 创建音色
        public static String createVoice() throws Exception {
          // 如未配置环境变量，请将下行替换为：String apiKey = "sk-xxx"
          String apiKey = System.getenv("DASHSCOPE_API_KEY");

          String jsonPayload =
              "{"
                  + "\"model\": \"qwen-voice-enrollment\"," // 请勿修改此值
                  + "\"input\": {"
                  +     "\"action\": \"create\","
                  +     "\"target_model\": \"" + TARGET_MODEL + "\","
                  +     "\"preferred_name\": \"" + PREFERRED_NAME + "\","
                  +     "\"audio\": {"
                  +         "\"data\": \"" + toDataUrl(AUDIO_FILE) + "\""
                  +     "}"
                  + "}"
                  + "}";

          String url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization";
          HttpURLConnection con = (HttpURLConnection) new URL(url).openConnection();
          con.setRequestMethod("POST");
          con.setRequestProperty("Authorization", "Bearer " + apiKey);
          con.setRequestProperty("Content-Type", "application/json");
          con.setDoOutput(true);

          try (OutputStream os = con.getOutputStream()) {
            os.write(jsonPayload.getBytes(StandardCharsets.UTF_8));
          }

          int status = con.getResponseCode();
          System.out.println("HTTP 状态码：" + status);

          try (BufferedReader br = new BufferedReader(
              new InputStreamReader(status >= 200 && status < 300 ? con.getInputStream() : con.getErrorStream(),
                  StandardCharsets.UTF_8))) {
            StringBuilder response = new StringBuilder();
            String line;
            while ((line = br.readLine()) != null) {
              response.append(line);
            }
            System.out.println("响应内容：" + response);

            if (status == 200) {
              JsonObject jsonObj = new Gson().fromJson(response.toString(), JsonObject.class);
              return jsonObj.getAsJsonObject("output").get("voice").getAsString();
            }
            throw new IOException("创建音色失败：" + status + " - " + response);
          }
        }

        public static void call() throws Exception {
          MultiModalConversation conv = new MultiModalConversation();
          MultiModalConversationParam param = MultiModalConversationParam.builder()
              // 如未配置环境变量，请将下行替换为：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model(TARGET_MODEL)
              .text("How's the weather today?")
              .parameter("voice", createVoice()) // 将 voice 参数替换为克隆生成的自定义音色
              .build();
          MultiModalConversationResult result = conv.call(param);
          String audioUrl = result.getOutput().getAudio().getUrl();
          System.out.print(audioUrl);

          // 下载音频文件到本地
          try (InputStream in = new URL(audioUrl).openStream();
                   FileOutputStream out = new FileOutputStream("downloaded_audio.wav")) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = in.read(buffer)) != -1) {
              out.write(buffer, 0, bytesRead);
            }
            System.out.println("\n音频文件已下载到本地：downloaded_audio.wav");
          } catch (Exception e) {
            System.out.println("\n下载音频文件出错：" + e.getMessage());
          }
        }
        public static void main(String[] args) {
          try {
            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
            call();
          } catch (Exception e) {
            System.out.println(e.getMessage());
          }
          System.exit(0);
        }
      }
      ```
    </CodeGroup>

    #### 使用设计音色

    声音设计会返回预览音频。请先试听预览确认效果满意后再用于合成，以降低成本。

    <Steps>
      <Step title="生成自定义音色并预览效果">
        如果对效果满意，请继续下一步；否则，请重新生成。

        Java 需要导入 Gson 依赖。如果使用 Maven 或 Gradle，按如下方式添加依赖：

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

        <Warning>
          使用声音设计生成的自定义音色进行语音合成时，必须按如下方式设置 voice 参数：

          ```java
          MultiModalConversationParam param = MultiModalConversationParam.builder()
                  .parameter("voice", "your_voice") // 将 voice 参数替换为声音设计生成的自定义音色
                  .build();
          ```
        </Warning>

        <CodeGroup>
          ```python Python
          import requests
          import base64
          import os

          def create_voice_and_play():
            # 如未配置环境变量，请将下行替换为：api_key = "sk-xxx"
            api_key = os.getenv("DASHSCOPE_API_KEY")

            if not api_key:
              print("错误：未找到 DASHSCOPE_API_KEY 环境变量，请先设置 API key。")
              return None, None, None

            # 准备请求数据
            headers = {
              "Authorization": f"Bearer {api_key}",
              "Content-Type": "application/json"
            }

            data = {
              "model": "qwen-voice-design",
              "input": {
                "action": "create",
                "target_model": "qwen3-tts-vd-2026-01-26",
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
              # 发送请求
              response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=60  # 添加超时设置
              )

              if response.status_code == 200:
                result = response.json()

                # 获取音色名称
                voice_name = result["output"]["voice"]
                print(f"音色名称：{voice_name}")

                # 获取预览音频数据
                base64_audio = result["output"]["preview_audio"]["data"]

                # 解码 Base64 音频数据
                audio_bytes = base64.b64decode(base64_audio)

                # 将音频文件保存到本地
                filename = f"{voice_name}_preview.wav"

                # 将音频数据写入本地文件
                with open(filename, 'wb') as f:
                  f.write(audio_bytes)

                print(f"音频已保存到本地文件：{filename}")
                print(f"文件路径：{os.path.abspath(filename)}")

                return voice_name, audio_bytes, filename
              else:
                print(f"请求失败，状态码：{response.status_code}")
                print(f"响应内容：{response.text}")
                return None, None, None

            except requests.exceptions.RequestException as e:
              print(f"网络请求出错：{e}")
              return None, None, None
            except KeyError as e:
              print(f"响应数据格式错误，缺少必需字段：{e}")
              print(f"响应内容：{response.text if 'response' in locals() else '无响应'}")
              return None, None, None
            except Exception as e:
              print(f"发生未知错误：{e}")
              return None, None, None

          if __name__ == "__main__":
            print("开始创建音色...")
            voice_name, audio_data, saved_filename = create_voice_and_play()

            if voice_name:
              print(f"\n成功创建音色 '{voice_name}'")
              print(f"音频文件已保存为：'{saved_filename}'")
              print(f"文件大小：{os.path.getsize(saved_filename)} 字节")
            else:
              print("\n音色创建失败")
          ```

          ```java Java
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
              // 如未配置环境变量，请将下行替换为：String apiKey = "sk-xxx"
              String apiKey = System.getenv("DASHSCOPE_API_KEY");

              // 创建 JSON 请求体字符串
              String jsonBody = "{\n" +
                  "    \"model\": \"qwen-voice-design\",\n" +
                  "    \"input\": {\n" +
                  "        \"action\": \"create\",\n" +
                  "        \"target_model\": \"qwen3-tts-vd-2026-01-26\",\n" +
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

                // 设置请求方法和请求头
                connection.setRequestMethod("POST");
                connection.setRequestProperty("Authorization", "Bearer " + apiKey);
                connection.setRequestProperty("Content-Type", "application/json");
                connection.setDoOutput(true);
                connection.setDoInput(true);

                // 发送请求体
                try (OutputStream os = connection.getOutputStream()) {
                  byte[] input = jsonBody.getBytes("UTF-8");
                  os.write(input, 0, input.length);
                  os.flush();
                }

                // 获取响应
                int responseCode = connection.getResponseCode();
                if (responseCode == HttpURLConnection.HTTP_OK) {
                  // 读取响应内容
                  StringBuilder response = new StringBuilder();
                  try (BufferedReader br = new BufferedReader(
                      new InputStreamReader(connection.getInputStream(), "UTF-8"))) {
                    String responseLine;
                    while ((responseLine = br.readLine()) != null) {
                      response.append(responseLine.trim());
                    }
                  }

                  // 解析 JSON 响应
                  JsonObject jsonResponse = JsonParser.parseString(response.toString()).getAsJsonObject();
                  JsonObject outputObj = jsonResponse.getAsJsonObject("output");
                  JsonObject previewAudioObj = outputObj.getAsJsonObject("preview_audio");

                  // 获取音色名称
                  String voiceName = outputObj.get("voice").getAsString();
                  System.out.println("音色名称：" + voiceName);

                  // 获取 Base64 编码的音频数据
                  String base64Audio = previewAudioObj.get("data").getAsString();

                  // 解码 Base64 音频数据
                  byte[] audioBytes = Base64.getDecoder().decode(base64Audio);

                  // 将音频保存到本地文件
                  String filename = voiceName + "_preview.wav";
                  saveAudioToFile(audioBytes, filename);

                  System.out.println("音频已保存到本地文件：" + filename);

                } else {
                  // 读取错误响应
                  StringBuilder errorResponse = new StringBuilder();
                  try (BufferedReader br = new BufferedReader(
                      new InputStreamReader(connection.getErrorStream(), "UTF-8"))) {
                    String responseLine;
                    while ((responseLine = br.readLine()) != null) {
                      errorResponse.append(responseLine.trim());
                    }
                  }

                  System.out.println("请求失败，状态码：" + responseCode);
                  System.out.println("错误响应：" + errorResponse.toString());
                }

              } catch (Exception e) {
                System.err.println("请求过程中出错：" + e.getMessage());
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
                System.out.println("音频已保存到：" + file.getAbsolutePath());
              } catch (IOException e) {
                System.err.println("保存音频文件时出错：" + e.getMessage());
                e.printStackTrace();
              }
            }
          }
          ```
        </CodeGroup>
      </Step>

      <Step title="使用自定义音色进行语音合成">
        使用上一步生成的自定义音色进行非流式语音合成。

        本示例基于非流式输出代码，将 `voice` 参数替换为声音设计生成的自定义音色。如需流式合成，请参见[快速开始](#快速开始)。

        **关键原则**：声音设计所用的模型（`target_model`）必须与后续语音合成所用的模型（`model`）一致，否则合成将失败。

        <CodeGroup>
          ```python Python
          import os
          import dashscope

          if __name__ == '__main__':
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            text = "How is the weather today?"
            response = dashscope.MultiModalConversation.call(
              model="qwen3-tts-vd-2026-01-26",
              # 如未配置环境变量，请将下行替换为：api_key = "sk-xxx"
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              text=text,
              voice="myvoice", # 将 voice 参数替换为声音设计生成的自定义音色
              stream=False
            )
            print(response)
          ```

          ```java Java
          import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
          import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
          import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
          import com.alibaba.dashscope.exception.ApiException;
          import com.alibaba.dashscope.exception.NoApiKeyException;
          import com.alibaba.dashscope.exception.UploadFileException;

          import com.alibaba.dashscope.utils.Constants;
          import java.io.FileOutputStream;
          import java.io.InputStream;
          import java.net.URL;

          public class Main {
            private static final String MODEL = "qwen3-tts-vd-2026-01-26";
            public static void call() throws ApiException, NoApiKeyException, UploadFileException {
              MultiModalConversation conv = new MultiModalConversation();
              MultiModalConversationParam param = MultiModalConversationParam.builder()
                  // 如未配置环境变量，请将下行替换为：.apiKey("sk-xxx")
                  .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                  .model(MODEL)
                  .text("Today is a wonderful day to build something people love!")
                  .parameter("voice", "myvoice") // 将 voice 参数替换为声音设计生成的自定义音色
                  .build();
              MultiModalConversationResult result = conv.call(param);
              String audioUrl = result.getOutput().getAudio().getUrl();
              System.out.print(audioUrl);

              // 下载音频文件到本地
              try (InputStream in = new URL(audioUrl).openStream();
                       FileOutputStream out = new FileOutputStream("downloaded_audio.wav")) {
                byte[] buffer = new byte[1024];
                int bytesRead;
                while ((bytesRead = in.read(buffer)) != -1) {
                  out.write(buffer, 0, bytesRead);
                }
                System.out.println("\n音频文件已下载到本地：downloaded_audio.wav");
              } catch (Exception e) {
                System.out.println("\n下载音频文件出错：" + e.getMessage());
              }
            }
            public static void main(String[] args) {
              try {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                call();
              } catch (ApiException | NoApiKeyException | UploadFileException e) {
                System.out.println(e.getMessage());
              }
              System.exit(0);
            }
          }
          ```
        </CodeGroup>
      </Step>
    </Steps>
  </Tab>

  <Tab title="CosyVoice">
    **前提条件**

    - [获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。
    - 如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。

    ##### 将合成音频保存到文件

    向 CosyVoice 发送完整文本并接收完整的合成音频。可用音色请参见[音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。

    <Tabs>
      <Tab title="Python">
        ```python
        # coding=utf-8

        import os
        import dashscope
        from dashscope.audio.tts_v2 import *

        # 如未配置环境变量，请将下行替换为：dashscope.api_key = "sk-xxx"
        dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

        dashscope.base_websocket_api_url='wss://dashscope.aliyuncs.com/api-ws/v1/inference'

        # 模型
        # cosyvoice-v3-flash/cosyvoice-v3-plus：使用 longanyang 等音色。
        # 每个音色支持不同的语言。合成日语、韩语等非中文语言时，请选择支持对应语言的音色。详见 CosyVoice 音色列表。
        model = "cosyvoice-v3-flash"
        # 音色
        voice = "longanyang"

        # 实例化 SpeechSynthesizer，在构造函数中传入 model 和 voice 等请求参数。
        synthesizer = SpeechSynthesizer(model=model, voice=voice)
        # 发送待合成的文本并获取二进制音频。
        audio = synthesizer.call("How is the weather today?")
        # 首次发送文本时会建立 WebSocket 连接，首包延迟包含连接建立时间。
        print('[Metric] Request ID: {}, First packet delay: {} ms'.format(
          synthesizer.get_last_request_id(),
          synthesizer.get_first_package_delay()))

        # 将音频保存到本地。
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
          // cosyvoice-v3-flash/cosyvoice-v3-plus：使用 longanyang 等音色。
          // 每个音色支持不同的语言。合成日语、韩语等非中文语言时，请选择支持对应语言的音色。详见 CosyVoice 音色列表。
          private static String model = "cosyvoice-v3-flash";
          // 音色
          private static String voice = "longanyang";

          public static void streamAudioDataToSpeaker() {
            // 请求参数
            SpeechSynthesisParam param =
                SpeechSynthesisParam.builder()
                    // 如未配置环境变量，请将下行替换为：.apiKey("sk-xxx")
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model(model) // 模型
                    .voice(voice) // 音色
                    .build();

            // 同步模式：禁用回调（第二个参数为 null）。
            SpeechSynthesizer synthesizer = new SpeechSynthesizer(param, null);
            ByteBuffer audio = null;
            try {
              // 阻塞直到音频返回。
              audio = synthesizer.call("How is the weather today?");
            } catch (Exception e) {
              throw new RuntimeException(e);
            } finally {
              // 任务结束时关闭 WebSocket 连接。
              synthesizer.getDuplexApi().close(1000, "bye");
            }
            if (audio != null) {
              // 将音频数据保存到本地文件 "output.mp3"。
              File file = new File("output.mp3");
              // 首次发送文本时会建立 WebSocket 连接，首包延迟包含连接建立时间。
              System.out.println(
                  "[Metric] Request ID: "
                      + synthesizer.getLastRequestId()
                      + ", First packet delay (ms): "
                      + synthesizer.getFirstPackageDelay());
              try (FileOutputStream fos = new FileOutputStream(file)) {
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
      </Tab>
    </Tabs>

    如需使用 CosyVoice 进行实时流式合成，请参见[实时语音合成](/developer-guides/speech/realtime-streaming)。
  </Tab>
</Tabs>

## 指令控制

通过自然语言指令控制音高、语速、情感和音色，无需调整音频参数。

**支持的模型**：仅 Qwen3-TTS-Instruct-Flash 系列。

**使用方式**：在 `instructions` 参数中指定指令。示例："语速快，语调上扬明显，适合时尚产品介绍。"

**支持的语言**：仅中文和英文。

**长度限制**：最多 1600 个 Token。

**适用场景**：

- 有声书和广播剧配音
- 广告和宣传视频配音
- 游戏角色和动画配音
- 情感智能语音助手
- 纪录片和新闻播报

**编写高质量音色描述**

**核心原则**

1. 具体明确：使用"低沉"、"清脆"、"快节奏"等描述性词汇，避免使用"好听"、"正常"等模糊词汇。
2. 多维描述：结合音高、语速、情感等多个维度，避免仅使用"高音"等单一维度描述。
3. 客观描述：聚焦物理和感知特征，而非个人喜好。使用"高亢有力"而非"我最喜欢的声音"。
4. 原创描述：描述声音特质，不要要求模仿特定人物。模型不支持直接模仿。
5. 简洁精炼：确保每个词都有意义，避免重复的近义词或无意义的修饰词。

**维度描述参考**：可组合多个维度，创造更丰富的音频效果。

| 维度 | 示例                            |
| -- | ----------------------------- |
| 音高 | 高、中、低、高亢、低沉                   |
| 语速 | 快、中、慢、快节奏、慢节奏                 |
| 情感 | 欢快、平静、温柔、严肃、活泼、沉稳、舒缓          |
| 特征 | 磁性、清脆、沙哑、醇厚、甜美、深沉、有力          |
| 用途 | 新闻播报、广告配音、有声书、动画角色、语音助手、纪录片旁白 |

**示例**

- 标准播报风格：吐字清晰准确，字正腔圆。
- 渐进情绪效果：音量从正常对话迅速提升到大喊，性格直爽、容易激动，情绪表达丰富。
- 特殊情绪状态：抽泣的语气导致发音略微含糊沙哑，哭腔中带有明显的紧张感。
- 广告配音风格：音调高、语速适中、充满活力和感染力，适合广告配音。
- 温柔舒缓风格：语速缓慢，音调温柔甜美，语气舒缓温暖，如同关心你的朋友。

## 情感与富语言标签

Qwen-Audio-TTS 系列模型支持在待合成文本（`text` 参数）中直接嵌入情感与富语言标签，用于控制语音的情感表达或在指定位置插入拟声效果（如笑声、叹息等），无需调整复杂的音频参数即可生成更具表现力的语音。

<Warning>
  **支持的模型**：仅 `qwen-audio-3.0-tts-plus` 和 `qwen-audio-3.0-tts-flash`。
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

## 方言

本节介绍如何让模型用**中文方言**（如河南话、四川话等）输出语音。不同模型和音色类型的设置方式不同。

**Qwen-Audio-TTS**

- **系统音色**：在 [Qwen-Audio-TTS 音色列表](/api-reference/speech-synthesis/qwen-audio-tts/voice-list) 中选择以下任一种音色：
  - 支持方言的系统音色，无需额外设置即可输出对应方言。
  - 支持[指令控制](#指令控制)且可指定方言的音色，通过指令文本指定方言。
- **声音复刻音色**：通过[指令控制](#指令控制)功能设置，例如指令文本写 `请用河南话表达`。
- **声音设计音色**：暂不支持方言。

**具体支持哪些方言**：参见 Qwen-Audio-TTS 中各模型的语言支持说明。

**CosyVoice**

- **系统音色**：在 [CosyVoice 音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list) 中选择以下任一种音色：
  - 支持方言的系统音色（例如 `longshange_v3`），无需额外设置即可输出对应方言。
  - 支持[指令控制](#指令控制)且可指定方言的音色（例如 `longanhuan_v3`），通过指令文本指定方言。
- **声音复刻音色**：通过[指令控制](#指令控制)功能设置，例如指令文本写 `请用河南话表达`。
- **声音设计音色**：暂不支持方言。

**具体支持哪些方言**：参见 CosyVoice 中各模型的语言支持说明。

**示例**：以 `cosyvoice-v3-flash` + `longanhuan_v3` 音色，通过指令文本 `"请用河南话表达。"` 输出河南话语音。

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "cosyvoice-v3-flash",
    "input": {
      "text": "叫你去买盐，你买回来一袋面，这不是弄啥嘞吗！",
      "voice": "longanhuan_v3",
      "format": "wav",
      "sample_rate": 24000,
      "instruction": "请用河南话表达。"
    }
}'
```

**Qwen-TTS**

- **系统音色**：使用支持方言的系统音色，参见 [Qwen-TTS 音色列表](/api-reference/speech-synthesis/qwen-tts/voice-list)。
- **声音复刻音色**：不支持方言。
- **声音设计音色**：不支持方言。

**具体支持哪些方言**：参见 Qwen3-TTS 中各模型的语言支持说明。

## 自定义音色

Qwen3-TTS 支持声音克隆（Qwen3-TTS-VC）和声音设计（Qwen3-TTS-VD）。API 参考请参见[声音克隆 (Qwen)](/api-reference/speech-synthesis/voice-cloning/create-voice) 和[声音设计 (Qwen)](/api-reference/speech-synthesis/voice-design/create-voice)。

## API 参考

- [语音合成 - Qwen API 参考](/api-reference/speech-synthesis/qwen-tts)
- [CosyVoice - Python SDK](/api-reference/speech-synthesis/cosyvoice/python-sdk)
- [CosyVoice - Java SDK](/api-reference/speech-synthesis/cosyvoice/java-sdk)
- [CosyVoice - WebSocket API](/api-reference/speech-synthesis/cosyvoice/websocket-api)
- [声音克隆 API 参考](/api-reference/speech-synthesis/voice-cloning/create-voice)
- [声音设计 API 参考](/api-reference/speech-synthesis/voice-design/create-voice)

## 系统音色

支持的音色清单、模型兼容性与试听见 [Qwen-TTS 音色列表](/api-reference/speech-synthesis/qwen-tts/voice-list)。

## 常见问题

**Q：音频文件 URL 的有效期是多久？**

音频文件 URL 在 24 小时后过期。

## 了解更多

- [实时语音合成（CosyVoice 和 Qwen-TTS-Realtime）](/developer-guides/speech/realtime-streaming) — 使用 WebSocket 进行实时流式语音合成
- [CosyVoice 音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)
- [Qwen-TTS 音色列表](/api-reference/speech-synthesis/qwen-tts/voice-list)
