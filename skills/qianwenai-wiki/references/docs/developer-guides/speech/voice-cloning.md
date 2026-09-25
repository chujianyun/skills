> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 声音复刻

> 声音复刻（Voice Cloning）只需提供一段 10~20 秒的音频样本，即可生成高度相似的定制音色，无需模型训练。

声音复刻适用于个性化语音助手、品牌专属播报、有声内容定制化等场景。

## 概述

千问AI平台平台提供以下模型系列的声音复刻能力：

- **Qwen-Audio-TTS**/**CosyVoice**：通过 DashScope SDK 或 HTTP API 创建音色，支持实时与非实时语音合成。
- **MiniMax**：通过 HTTP API 创建音色，仅支持非实时语音合成。
- **Qwen-Audio-Realtime**：Qwen-Audio-Realtime 是实时语音对话模型（非语音合成模型），声音复刻用于自定义对话模型回复时的 TTS 音色。通过 DashScope SDK 或 HTTP API 创建音色。
- **Qwen-TTS**：通过 HTTP API 创建音色，支持实时与非实时语音合成。

如需了解各模型系列的详细对比和选型建议，请参见[语音合成](/developer-guides/speech/tts-models)。

## 前提条件

1. 已[配置 API Key](/api-reference/preparation/api-key)并将其[设置到环境变量](/api-reference/preparation/export-api-key-env)。
2. 如果通过 DashScope SDK 调用，需要[安装最新版 SDK](/api-reference/preparation/install-sdk)。
3. **准备音频文件**：音频需符合[音频要求](#音频要求)。

## 快速开始

声音复刻的使用分为以下三步：

1. **准备音频**：准备一段符合[音频要求](#音频要求)的音频文件。
2. **创建音色**：调用声音复刻接口上传音频创建音色，通过 `target_model` 指定绑定的语音合成模型。
3. **使用音色合成语音**：调用语音合成接口，传入创建音色时返回的音色 ID。

### Qwen-TTS 声音复刻

示例使用本地音频文件 `voice.mp3`，运行时请替换为实际路径。

<Warning>
  创建音色时的 `target_model` 必须与语音合成时使用的模型完全一致，否则合成将失败。
</Warning>

#### 双向流式合成（实时）

适用于 Qwen3-TTS-VC-Realtime 模型。参数详情见[实时流式语音合成](/developer-guides/speech/realtime-streaming)。

<Tabs>
  <Tab title="Python">
    ```python
    # pyaudio 安装方式：
    #   macOS:   brew install portaudio && pip install pyaudio
    #   Ubuntu:  sudo apt-get install python3-pyaudio  (或 pip install pyaudio)
    #   CentOS:  sudo yum install -y portaudio portaudio-devel && pip install pyaudio
    #   Windows: python -m pip install pyaudio

    import pyaudio
    import os
    import requests
    import base64
    import pathlib
    import threading
    import time
    import dashscope
    from dashscope.audio.qwen_tts_realtime import QwenTtsRealtime, QwenTtsRealtimeCallback, AudioFormat

    TARGET_MODEL = "qwen3-tts-vc-realtime-2026-01-15"
    VOICE_FILE = "voice.mp3"  # 替换为你的音频文件

    TEXT_TO_SYNTHESIZE = [
      'Today we explore the wonders of speech synthesis.',
      'Each voice carries a unique character.',
      'With voice cloning, you can bring any text to life.',
      "Let's create something amazing together."
    ]

    def create_voice(file_path: str) -> str:
      """创建克隆声音并返回声音标识符。"""
      api_key = os.getenv("DASHSCOPE_API_KEY")
      file_path_obj = pathlib.Path(file_path)
      base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
      data_uri = f"data:audio/mpeg;base64,{base64_str}"

      response = requests.post(
        "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
          "model": "qwen-voice-enrollment",
          "input": {
            "action": "create",
            "target_model": TARGET_MODEL,
            "preferred_name": "myvoice",
            "audio": {"data": data_uri}
          }
        }
      )
      return response.json()["output"]["voice"]

    class MyCallback(QwenTtsRealtimeCallback):
      def __init__(self):
        self.complete_event = threading.Event()
        self._player = pyaudio.PyAudio()
        self._stream = self._player.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

      def on_event(self, response: dict) -> None:
        if response.get("type") == "response.audio.delta":
          audio_data = base64.b64decode(response["delta"])
          self._stream.write(audio_data)
        elif response.get("type") == "session.finished":
          self.complete_event.set()

    if __name__ == "__main__":
      dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
      callback = MyCallback()
      tts = QwenTtsRealtime(model=TARGET_MODEL, callback=callback,
                            url="wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
      tts.connect()
      tts.update_session(voice=create_voice(VOICE_FILE),
                         response_format=AudioFormat.PCM_24000HZ_MONO_16BIT, mode="server_commit")

      for text in TEXT_TO_SYNTHESIZE:
        tts.append_text(text)
        time.sleep(0.1)

      tts.finish()
      callback.complete_event.wait()
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import com.alibaba.dashscope.audio.qwen_tts_realtime.*;
    import com.google.gson.Gson;
    import com.google.gson.JsonObject;
    import java.io.*;
    import java.net.HttpURLConnection;
    import java.net.URL;
    import java.nio.file.*;
    import java.util.Base64;
    import java.util.concurrent.CountDownLatch;

    public class Main {
      private static final String TARGET_MODEL = "qwen3-tts-vc-realtime-2026-01-15";
      private static final String AUDIO_FILE = "voice.mp3";  // 替换为你的音频文件

      public static String createVoice() throws Exception {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        byte[] bytes = Files.readAllBytes(Paths.get(AUDIO_FILE));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        String dataUri = "data:audio/mpeg;base64," + encoded;

        String jsonPayload = "{\"model\":\"qwen-voice-enrollment\",\"input\":{"
            + "\"action\":\"create\",\"target_model\":\"" + TARGET_MODEL + "\","
            + "\"preferred_name\":\"myvoice\",\"audio\":{\"data\":\"" + dataUri + "\"}}}";

        HttpURLConnection con = (HttpURLConnection) new URL(
            "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization").openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Authorization", "Bearer " + apiKey);
        con.setRequestProperty("Content-Type", "application/json");
        con.setDoOutput(true);
        try (OutputStream os = con.getOutputStream()) {
          os.write(jsonPayload.getBytes("UTF-8"));
        }

        BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream(), "UTF-8"));
        StringBuilder response = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) response.append(line);
        return new Gson().fromJson(response.toString(), JsonObject.class)
            .getAsJsonObject("output").get("voice").getAsString();
      }

      public static void main(String[] args) throws Exception {
        CountDownLatch latch = new CountDownLatch(1);
        QwenTtsRealtimeParam param = QwenTtsRealtimeParam.builder()
            .model(TARGET_MODEL)
            .url("wss://dashscope.aliyuncs.com/api-ws/v1/realtime")
            .apikey(System.getenv("DASHSCOPE_API_KEY"))
            .build();

        QwenTtsRealtime tts = new QwenTtsRealtime(param, new QwenTtsRealtimeCallback() {
          public void onEvent(JsonObject msg) {
            if (msg.get("type").getAsString().equals("session.finished")) latch.countDown();
          }
        });
        tts.connect();

        QwenTtsRealtimeConfig config = QwenTtsRealtimeConfig.builder()
            .voice(createVoice())
            .responseFormat(QwenTtsRealtimeAudioFormat.PCM_24000HZ_MONO_16BIT)
            .mode("server_commit").build();
        tts.updateSession(config);

        for (String text : new String[]{
            "Today we explore the wonders of speech synthesis.",
            "Each voice carries a unique character.",
            "With voice cloning, you can bring any text to life.",
            "Let's create something amazing together."}) {
          tts.appendText(text);
          Thread.sleep(100);
        }
        tts.finish();
        latch.await();
      }
    }
    ```
  </Tab>
</Tabs>

#### 非流式合成

适用于 Qwen3-TTS-VC 模型。详见 [Qwen TTS](/api-reference/speech-synthesis/qwen-tts)。

<Tabs>
  <Tab title="Python">
    ```python
    import os
    import requests
    import base64
    import pathlib
    import dashscope

    TARGET_MODEL = "qwen3-tts-vc-2026-01-22"
    VOICE_FILE = "voice.mp3"

    def create_voice(file_path: str) -> str:
      api_key = os.getenv("DASHSCOPE_API_KEY")
      base64_str = base64.b64encode(pathlib.Path(file_path).read_bytes()).decode()
      data_uri = f"data:audio/mpeg;base64,{base64_str}"

      response = requests.post(
        "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
          "model": "qwen-voice-enrollment",
          "input": {"action": "create", "target_model": TARGET_MODEL,
                    "preferred_name": "myvoice", "audio": {"data": data_uri}}
        }
      )
      return response.json()["output"]["voice"]

    if __name__ == "__main__":
      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
      response = dashscope.MultiModalConversation.call(
        model=TARGET_MODEL,
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text="Today we explore the wonders of speech synthesis.",
        voice=create_voice(VOICE_FILE),
        stream=False
      )
      print(response)
    ```
  </Tab>

  <Tab title="cURL">
    **步骤一：创建音色**

    ```bash
    # 将 voice.mp3 替换为实际音频文件路径

    AUDIO_BASE64=$(base64 -i voice.mp3)

    curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
        "model": "qwen-voice-enrollment",
        "input": {
            "action": "create",
            "target_model": "qwen3-tts-vc-2026-01-22",
            "preferred_name": "guanyu",
            "audio": {"data": "data:audio/mpeg;base64,'$AUDIO_BASE64'"}
        }
    }'
    ```

    **步骤二：使用复刻音色合成语音**

    将上一步返回的 `voice` 值填入以下请求中。

    ```bash
    # 将 YOUR_VOICE_ID 替换为上一步返回的 voice 值

    curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
        "model": "qwen3-tts-vc-2026-01-22",
        "input": {
            "text": "今天天气怎么样？",
            "voice": "YOUR_VOICE_ID"
        }
    }'
    ```
  </Tab>

  <Tab title="Java">
    ```java
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
      private static final String TARGET_MODEL = "qwen3-tts-vc-2026-01-22";
      private static final String AUDIO_FILE = "voice.mp3";  // 替换为你的音频文件

      public static String createVoice() throws Exception {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        byte[] bytes = Files.readAllBytes(Paths.get(AUDIO_FILE));
        String encoded = Base64.getEncoder().encodeToString(bytes);
        String dataUri = "data:audio/mpeg;base64," + encoded;

        String jsonPayload = "{\"model\":\"qwen-voice-enrollment\",\"input\":{"
            + "\"action\":\"create\",\"target_model\":\"" + TARGET_MODEL + "\","
            + "\"preferred_name\":\"myvoice\",\"audio\":{\"data\":\"" + dataUri + "\"}}}";

        HttpURLConnection con = (HttpURLConnection) new URL(
            "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization").openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Authorization", "Bearer " + apiKey);
        con.setRequestProperty("Content-Type", "application/json");
        con.setDoOutput(true);
        try (OutputStream os = con.getOutputStream()) {
          os.write(jsonPayload.getBytes(StandardCharsets.UTF_8));
        }

        BufferedReader br = new BufferedReader(new InputStreamReader(con.getInputStream(), StandardCharsets.UTF_8));
        StringBuilder response = new StringBuilder();
        String line;
        while ((line = br.readLine()) != null) response.append(line);
        return new Gson().fromJson(response.toString(), JsonObject.class)
            .getAsJsonObject("output").get("voice").getAsString();
      }

      public static void main(String[] args) {
        try {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
          MultiModalConversation conv = new MultiModalConversation();
          MultiModalConversationParam param = MultiModalConversationParam.builder()
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model(TARGET_MODEL)
              .text("Today we explore the wonders of speech synthesis.")
              .parameter("voice", createVoice())
              .build();
          MultiModalConversationResult result = conv.call(param);
          String audioUrl = result.getOutput().getAudio().getUrl();
          System.out.println("Audio URL: " + audioUrl);

          // 下载音频
          try (InputStream in = new URL(audioUrl).openStream();
               FileOutputStream out = new FileOutputStream("output.wav")) {
            byte[] buffer = new byte[1024];
            int bytesRead;
            while ((bytesRead = in.read(buffer)) != -1) {
              out.write(buffer, 0, bytesRead);
            }
            System.out.println("音频已保存至 output.wav");
          }
        } catch (Exception e) {
          System.out.println("Error: " + e.getMessage());
        }
        System.exit(0);
      }
    }
    ```
  </Tab>
</Tabs>

### Qwen-Audio-TTS 声音复刻

**步骤一：创建音色**

调用声音复刻 API 上传音频并创建音色。`url` 参数传入音频文件的可访问 URL 地址，`prefix` 参数作为音色名称前缀。

```bash
# 将 url 替换为实际音频文件的可访问地址

curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "qwen-audio-3.0-tts-flash",
        "prefix": "myvoice",
        "url": "https://your-audio-url.wav"
    }
}'
```

**步骤二：使用复刻音色合成语音**

将上一步返回的 `voice_id` 值填入以下请求中。

```python
# coding=utf-8
import dashscope
from dashscope.audio.tts_v2 import *
import os

dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')
# 声音复刻、语音合成要使用相同的模型
model = "qwen-audio-3.0-tts-flash"
# 将 voice 参数替换为声音复刻生成的专属音色
voice = "voice_id"

synthesizer = SpeechSynthesizer(model=model, voice=voice)
audio = synthesizer.call("今天天气怎么样？")
print('[Metric] requestId为：{}，首包延迟为：{}毫秒'.format(
    synthesizer.get_last_request_id(),
    synthesizer.get_first_package_delay()))

with open('output.mp3', 'wb') as f:
    f.write(audio)
```

### Qwen-Audio-Realtime 声音复刻

<Note>
  Qwen-Audio-Realtime 是实时语音对话模型（非语音合成模型），声音复刻用于自定义对话模型回复时的 TTS 音色，音频要求与 Qwen-Audio-TTS 相同。
</Note>

**步骤一：创建音色**

通过 HTTP API 调用声音复刻接口，上传音频并创建音色。`target_model` 参数填入实时语音对话模型名称，`prefix` 参数作为音色名称前缀。

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "qwen-audio-3.0-realtime-plus",
        "prefix": "myvoice",
        "url": "https://your-audio-url.wav"
    }
}'
```

**步骤二：在实时语音对话中使用复刻音色**

将上一步返回的 `voice_id` 填入实时语音对话 `session.update` 事件的 `voice` 参数中。

```json
{
    "type": "session.update",
    "session": {
        "voice": "qwen-audio-3.0-realtime-plus-myvoice-xxxxxx"
    }
}
```

### CosyVoice 声音复刻

CosyVoice 声音复刻通过专用的声音复刻 API 进行操作，同样遵循"创建音色 - 使用音色合成"的流程。

**步骤一：创建音色**

调用声音复刻 API 上传音频并创建音色。`url` 参数传入音频文件的可访问 URL 地址，`prefix` 参数作为音色名称前缀。

```bash
# 将 url 替换为实际音频文件的可访问地址

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "voice-enrollment",
    "input": {
        "action": "create_voice",
        "target_model": "cosyvoice-v3-plus",
        "prefix": "myvoice",
        "url": "https://your-audio-url.wav",
        "language_hints": ["zh"]
    }
}'
```

**步骤二：使用复刻音色合成语音**

将上一步返回的 `voice` 值填入以下请求中。

```bash
# 将 YOUR_VOICE_ID 替换为上一步返回的 voice 值

curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "cosyvoice-v3-plus",
    "input": {
      "text": "今天天气怎么样？",
      "voice": "YOUR_VOICE_ID",
      "format": "wav",
      "sample_rate": 24000
    }
}'
```

### MiniMax 音色复刻

<Note>
  以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
</Note>

提交复刻请求后，系统会生成一段试听音频（按同步语音合成单价计费）。首次使用复刻音色进行语音合成时，需支付 9.9 元音色解锁费用。

**步骤一：创建音色**

调用音色复刻 API 上传音频并创建音色。`voice_id` 参数用于指定新音色的 ID，`audio_url` 参数传入音频文件的可访问 URL 地址。

```bash
# 将 audio_url 替换为实际音频文件的可访问地址
# 将 voice_id 替换为自定义的音色 ID

curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H 'Content-Type: application/json; charset=utf-8' \
-d '{
    "input": {
      "action": "voice_clone",
      "voice_id": "my-custom-voice",
      "audio_url": "https://your-audio-url.wav",
      "text": "你说是什么就是什么"
    },
    "model": "minimax/speech-2.8-turbo"
  }'
```

**步骤二：使用复刻音色合成语音**

将上一步指定的 `voice_id` 值填入以下请求中。

```bash
# 将 voice_id 替换为上一步指定的音色 ID

curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
  "model": "minimax/speech-2.8-turbo",
  "input": {
    "text": "今天天气怎么样？",
    "voice_setting": {
      "voice_id": "my-custom-voice",
      "speed": 1,
      "vol": 1,
      "pitch": 0
    },
    "audio_setting": {
      "sample_rate": 32000,
      "bitrate": 128000,
      "format": "mp3",
      "channel": 1
    }
  }
}'
```

## 音频要求

输入音频的质量直接决定复刻效果。不同模型系列对音频的具体要求有所差异，请按照目标模型的要求准备音频样本。

<Tabs>
  <Tab title="Qwen-Audio-TTS / Qwen-Audio-Realtime">
| 项目       | 要求                                                                                                                                                  |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **支持格式** | WAV（16bit）、MP3、M4A                                                                                                                                  |
| **音频时长** | 推荐 10\~20 秒，最长不超过 60 秒                                                                                                                              |
| **文件大小** | 不超过 10 MB                                                                                                                                           |
| **采样率**  | 16 kHz 及以上                                                                                                                                          |
| **声道**   | 单声道或双声道。双声道音频仅处理首声道，请确保首声道包含有效人声。                                                                                                                   |
| **内容**   | 音频必须包含至少 5 秒连续清晰的朗读内容（无背景音），其余部分仅允许短暂停顿（不超过 2 秒）。整段音频应避免出现背景音乐、环境噪音或其他人声。请使用正常语速的说话音频，不要上传歌曲或唱歌录音。                                                  |
| **支持语言** | 中文（普通话、广东话、重庆话、东北话、甘肃话、贵州话、浙江话、河北话、河南话、湖北话、湖南话、江西话、宁波话、宁夏话、青岛话、陕西话、山西话、山东话、上海话、四川话、云南话）、英语、日语、韩语、俄语、法语、德语、葡萄牙语、泰语、印尼语、越南语、西班牙语、意大利语、马来西亚语、菲律宾语、阿拉伯语 |
  </Tab>

  <Tab title="CosyVoice">
| 项目       | 要求                                                                                                 |
| -------- | -------------------------------------------------------------------------------------------------- |
| **支持格式** | WAV（16bit）、MP3、M4A                                                                                 |
| **音频时长** | 推荐 10\~20 秒，最长不超过 60 秒                                                                             |
| **文件大小** | 不超过 10 MB                                                                                          |
| **采样率**  | 16 kHz 及以上                                                                                         |
| **声道**   | 单声道或双声道。双声道音频仅处理首声道，请确保首声道包含有效人声。                                                                  |
| **内容**   | 音频必须包含至少 5 秒连续清晰的朗读内容（无背景音），其余部分仅允许短暂停顿（不超过 2 秒）。整段音频应避免出现背景音乐、环境噪音或其他人声。请使用正常语速的说话音频，不要上传歌曲或唱歌录音。 |
| **支持语言** | 因驱动音色的语音合成模型（通过 `target_model` 参数指定）而异，详见下方说明                                                      |

    **各模型支持的语言**：

    - **cosyvoice-v1、cosyvoice-v2**：中文（普通话）、英文
    - **cosyvoice-v3-flash**：中文（普通话、广东话、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话）、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语
    - **cosyvoice-v3-plus**：中文（普通话、广东话、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话）、英文、法语、德语、日语、韩语、俄语
    - **cosyvoice-v3.5-plus、cosyvoice-v3.5-flash**：中文（普通话、广东话、东北话、甘肃话、贵州话、河南话、湖北话、江西话、闽南话、宁夏话、山西话、陕西话、山东话、上海话、四川话、天津话、云南话）、英文、法语、德语、日语、韩语、俄语、葡萄牙语、泰语、印尼语、越南语
  </Tab>

  <Tab title="Qwen-TTS">
| 项目       | 要求                                                                                                 |
| -------- | -------------------------------------------------------------------------------------------------- |
| **支持格式** | WAV（16bit）、MP3、M4A                                                                                 |
| **音频时长** | 推荐 10\~20 秒，最长不超过 60 秒                                                                             |
| **文件大小** | 不超过 10 MB                                                                                          |
| **采样率**  | 24 kHz 及以上                                                                                         |
| **声道**   | 单声道                                                                                                |
| **内容**   | 音频必须包含至少 3 秒连续清晰的朗读内容（无背景音），其余部分仅允许短暂停顿（不超过 2 秒）。整段音频应避免出现背景音乐、环境噪音或其他人声。请使用正常语速的说话音频，不要上传歌曲或唱歌录音。 |
| **支持语言** | 中文、英文、德语、意大利语、葡萄牙语、西班牙语、日语、韩语、法语、俄语                                                                |
  </Tab>

  <Tab title="MiniMax">
| 项目       | 要求                                                                                 |
| -------- | ---------------------------------------------------------------------------------- |
| **支持格式** | MP3、M4A、WAV                                                                        |
| **音频时长** | 不低于 10 秒，最长不超过 5 分钟                                                                |
| **文件大小** | 不超过 20 MB                                                                          |
| **内容**   | 音频应包含连续清晰的朗读内容（无背景音），停顿时长不超过 2 秒。整段音频应避免出现背景音乐、环境噪音或其他人声。请使用正常语速的说话音频，不要上传歌曲或唱歌录音。 |
| **支持语言** | 无特殊限制                                                                              |
  </Tab>
</Tabs>

<Tip>
  为获得最佳复刻效果，建议参照[录音建议](#录音建议)准备样本。
</Tip>

## 录音建议

高质量的输入音频是获得优质复刻效果的基础。以下从录音设备、录音环境、录音文案和操作流程四个方面提供建议。

### 录音设备

可使用手机、数字录音笔、专业录音机等。建议使用支持高采样率（24 kHz 及以上）录音的设备，以满足音频要求。

### 录音环境

**场地**

- 建议在 10 平方米以内的小型封闭空间录音。
- 优先选择配有吸音材料（如吸音棉、地毯、窗帘）的房间。
- 避免空旷大厅、会议室、教室等高混响场所。

**噪音控制**

- 室外噪音：关闭门窗，避免交通、施工等干扰。
- 室内噪音：关闭空调、风扇、日光灯镇流器等设备；可通过手机录制环境音并放大播放，识别潜在噪音源。

**混响控制**

- 混响会导致声音模糊、清晰度下降。
- 减少光滑表面反射：拉上窗帘、打开衣柜门、铺放衣物或床单覆盖桌面/柜面。
- 利用不规则物体（如书架、软包家具）实现声波漫反射。

### 录音文案

- 内容无特殊限制，建议与目标应用场景一致。
- 避免短句（如"你好"、"是的"），应使用完整句子。
- 保持语义连贯，朗读时避免频繁停顿（建议至少连续 3 秒无中断）。
- 录音的开头和结尾部分应保持与中间段落一致的语速，避免因开头或结尾语速过快导致复刻后语音合成时出现卡顿现象。
- 可加入适当情绪表达（如温暖、亲切、严肃），避免机械朗读。
- 不包含敏感词汇（如政治、色情、暴力相关内容），否则会导致复刻失败。

### 操作建议

以普通卧室为例：

1. 关闭门窗，隔绝外部噪音。
2. 关闭空调、电扇等电器。
3. 拉上窗帘，减少玻璃反射。
4. 在桌面铺放衣物或毛毯，降低桌面反射。
5. 提前熟悉文案，设定角色语气，自然演绎。
6. 与录音设备保持约 10 厘米距离，避免喷麦或信号过弱。

## 管理自定义音色

音色创建完成后，您可以通过 API 对已有音色进行查询和管理（Qwen-Audio-TTS、Qwen-Audio-Realtime、Qwen-TTS 和 CosyVoice 支持）。Qwen-Audio-Realtime 的音色查询与删除接口与 Qwen-Audio-TTS 完全相同。

MiniMax 仅支持创建音色，不支持查询和删除等音色管理操作。

- **查询音色列表**：获取当前账号下所有自定义音色的列表。
- **查询音色详情**：查看指定音色的详细信息，如创建时间、绑定的语音合成模型等。
- **删除音色**：删除不再需要的自定义音色，释放配额。

各模型的 API 接口和参数详情请参见 [API 参考](#api-参考)。

## 适用范围

支持的模型：

- **Qwen-Audio-TTS**：qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash
- **Qwen-Audio-Realtime**：qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash
- **CosyVoice**：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash、cosyvoice-v2、cosyvoice-v1
- **MiniMax**：MiniMax/speech-2.8-hd、MiniMax/speech-02-hd、MiniMax/speech-2.8-turbo、MiniMax/speech-02-turbo
- **Qwen-TTS**：
  - **Qwen3-TTS-VC-Realtime**：qwen3-tts-vc-realtime-2026-01-15（最新快照版）、qwen3-tts-vc-realtime-2025-11-27（快照版）
  - **Qwen3-TTS-VC**：qwen3-tts-vc-2026-01-22（最新快照版）

## 常见问题

### Q：创建音色后可以用于不同的语音合成模型吗？

不可以。音色在创建时通过 `target_model` 绑定到特定的语音合成模型，不能跨模型使用。如果您需要在多个模型上使用同一段音频的声音，请为每个模型分别创建音色。

### Q：复刻音色的有效期是多久？

Qwen-Audio-TTS、Qwen-Audio-Realtime、Qwen-TTS 和 CosyVoice 创建的音色默认长期有效，但长时间未使用的音色可能会被系统清理。建议妥善保存音色 ID，需要时可通过查询接口确认音色是否仍然可用。

### Q：音频质量不好会影响复刻效果吗？

会的。输入音频的质量直接影响复刻效果。背景噪音、混响、多人声等问题都会降低复刻音色的相似度和自然度。建议参照[音频要求](#音频要求)和[录音建议](#录音建议)准备样本。

## API 参考

[声音复刻 API](/api-reference/speech-synthesis/voice-cloning/create-voice)
