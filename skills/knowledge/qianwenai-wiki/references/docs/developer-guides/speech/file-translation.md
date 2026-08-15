> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 音视频文件翻译

> 支持18种语言翻译

## 模型信息

| 模型                                   | 版本  | 上下文窗口         | 最大输入          | 最大输出         |
| ------------------------------------ | --- | ------------- | ------------- | ------------ |
| qwen3-livetranslate-flash            | 稳定版 | 53,248 tokens | 49,152 tokens | 4,096 tokens |
| qwen3-livetranslate-flash-2025-12-01 | 快照版 | 53,248 tokens | 49,152 tokens | 4,096 tokens |

<Note>
  qwen3-livetranslate-flash 当前与 qwen3-livetranslate-flash-2025-12-01 的能力一致。
</Note>

## 快速开始

### 前提条件

1. [获取 API Key](/api-reference/preparation/api-key)。
2. [将其设置为环境变量](/api-reference/preparation/export-api-key-env)。
3. （可选）如果使用 OpenAI SDK，请[安装 SDK](/api-reference/preparation/install-sdk)。

以下示例均使用 OpenAI 兼容的流式 API，通过 `translation_options` 设置源语言和目标语言。默认输入为音频。如需翻译视频文件，取消注释各示例中的视频输入代码块即可。

<Note>
  指定 `source_lang` 可提升翻译准确率。省略该参数则自动检测语言。
</Note>

<Tabs>
  <Tab title="Python">
    ```python
    import os
    from openai import OpenAI

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # --- 音频输入 ---
    messages = [
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
              "format": "wav",
            },
          }
        ],
      }
    ]

    # --- 视频输入（取消注释以使用） ---
    # messages = [
    #     {
    #         "role": "user",
    #         "content": [
    #             {
    #                 "type": "video_url",
    #                 "video_url": {
    #                     "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
    #                 },
    #             }
    #         ],
    #     },
    # ]

    completion = client.chat.completions.create(
      model="qwen3-livetranslate-flash",
      messages=messages,
      modalities=["text", "audio"],
      audio={"voice": "Cherry", "format": "wav"},
      stream=True,
      stream_options={"include_usage": True},
      # translation_options 不是 OpenAI 标准参数，需通过 extra_body 传递
      extra_body={"translation_options": {"source_lang": "zh", "target_lang": "en"}},
    )

    for chunk in completion:
      print(chunk)
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";

    const client = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    });

    // --- 音频输入 ---
    const messages = [
      {
        role: "user",
        content: [
          {
            type: "input_audio",
            input_audio: {
              data: "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
              format: "wav",
            },
          },
        ],
      },
    ];

    // --- 视频输入（取消注释以使用） ---
    // const messages = [
    //     {
    //         role: "user",
    //         content: [
    //             {
    //                 type: "video_url",
    //                 video_url: {
    //                     url: "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4",
    //                 },
    //             },
    //         ],
    //     },
    // ];

    async function main() {
      const completion = await client.chat.completions.create({
        model: "qwen3-livetranslate-flash",
        messages: messages,
        modalities: ["text", "audio"],
        audio: { voice: "Cherry", format: "wav" },
        stream: true,
        stream_options: { include_usage: true },
        translation_options: { source_lang: "zh", target_lang: "en" },
      });

      for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
      }
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "qwen3-livetranslate-flash",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "input_audio",
              "input_audio": {
                "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
                "format": "wav"
              }
            }
          ]
        }
      ],
      "modalities": ["text", "audio"],
      "audio": {
        "voice": "Cherry",
        "format": "wav"
      },
      "stream": true,
      "stream_options": {
        "include_usage": true
      },
      "translation_options": {
        "source_lang": "zh",
        "target_lang": "en"
      }
    }'
    ```
  </Tab>
</Tabs>

以上示例使用的是公开文件 URL。

## 发送 Base64 编码的本地文件

要翻译本地音频文件，需先将文件读取并编码为 Base64。以 data URI 格式传递数据：`data:audio/<format>;base64,<base64_data>`（例如 `data:audio/wav;base64,UklGRiQAAABXQVZFZm10...`）。

<Note>
  支持的音频格式：WAV、MP3、FLAC、AAC、OGG、OPUS、M4A、WMA、AMR。采样率：8kHz-48kHz。
</Note>

<Tabs>
  <Tab title="Python">
    ```python
    import os
    import base64
    from openai import OpenAI

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # 读取并编码本地音频文件
    with open("local_audio.wav", "rb") as f:
      audio_base64 = base64.b64encode(f.read()).decode("utf-8")

    completion = client.chat.completions.create(
      model="qwen3-livetranslate-flash",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "input_audio",
              "input_audio": {
                "data": f"data:audio/wav;base64,{audio_base64}",
                "format": "wav",
              },
            }
          ],
        }
      ],
      modalities=["text", "audio"],
      audio={"voice": "Cherry", "format": "wav"},
      stream=True,
      stream_options={"include_usage": True},
      extra_body={"translation_options": {"source_lang": "zh", "target_lang": "en"}},
    )

    for chunk in completion:
      print(chunk)
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";
    import { readFileSync } from "node:fs";

    const client = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    });

    // 读取并编码本地音频文件
    const audioBase64 = readFileSync("local_audio.wav").toString("base64");

    async function main() {
      const completion = await client.chat.completions.create({
        model: "qwen3-livetranslate-flash",
        messages: [
          {
            role: "user",
            content: [
              {
                type: "input_audio",
                input_audio: {
                  data: `data:audio/wav;base64,${audioBase64}`,
                  format: "wav",
                },
              },
            ],
          },
        ],
        modalities: ["text", "audio"],
        audio: { voice: "Cherry", format: "wav" },
        stream: true,
        stream_options: { include_usage: true },
        translation_options: { source_lang: "zh", target_lang: "en" },
      });

      for await (const chunk of completion) {
        console.log(JSON.stringify(chunk));
      }
    }

    main();
    ```
  </Tab>

  <Tab title="curl">
    ```bash
    # 将本地音频文件编码为 Base64
    AUDIO_BASE64=$(base64 < local_audio.wav)

    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "qwen3-livetranslate-flash",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "input_audio",
              "input_audio": {
                "data": "data:audio/wav;base64,'"$AUDIO_BASE64"'",
                "format": "wav"
              }
            }
          ]
        }
      ],
      "modalities": ["text", "audio"],
      "audio": {
        "voice": "Cherry",
        "format": "wav"
      },
      "stream": true,
      "stream_options": {
        "include_usage": true
      },
      "translation_options": {
        "source_lang": "zh",
        "target_lang": "en"
      }
    }'
    ```
  </Tab>
</Tabs>

## 请求参数

### 输入

`messages` 数组只能包含一条 `role` 为 `user` 的消息。`content` 字段用于传入待翻译的音频或视频：

- **音频**：将 `type` 设为 `input_audio`。在 `input_audio.data` 中提供文件 URL 或 data URI（例如 `data:audio/wav;base64,<base64_data>`），在 `input_audio.format` 中指定格式（例如 `wav`）。详见[发送 Base64 编码的本地文件](#发送-base64-编码的本地文件)。
- **视频**：将 `type` 设为 `video_url`。在 `video_url.url` 中提供文件 URL。

### 翻译选项

通过 `translation_options` 参数指定源语言和目标语言：

```json
"translation_options": {"source_lang": "zh", "target_lang": "en"}
```

在 Python SDK 中，`translation_options` 不是 OpenAI 标准参数，需通过 `extra_body` 传递：

```python
extra_body={"translation_options": {"source_lang": "zh", "target_lang": "en"}}
```

### 输出模态

通过 `modalities` 参数控制输出格式：

| `modalities` 值      | 输出                   |
| ------------------- | -------------------- |
| `["text"]`          | 仅翻译文本                |
| `["text", "audio"]` | 翻译文本和 Base64 编码的合成音频 |

输出包含音频时，需通过 `audio` 参数设置语音。可选语音见[支持的语音](#支持的语音)。

### 使用限制

- **仅支持单轮**：模型每次请求处理一条翻译，不支持多轮对话。
- **不支持 system 消息**：不支持 `system` 角色。
- **流式与非流式**：支持 `stream: true` 和 `stream: false`。
- **输出音频格式**：音频输出仅支持 `wav` 格式。
- **采样参数默认值**：默认采样参数（`temperature`、`top_p`、`top_k`、`presence_penalty`、`repetition_penalty`）已针对翻译准确率调优，修改可能导致输出质量下降。

## 解析响应

每个流式 `chunk` 对象包含：

- **文本**：`chunk.choices[0].delta.content`
- **音频**：`chunk.choices[0].delta.audio["data"]`（Base64 编码，24 kHz 采样率）

### 保存音频到文件

将流中的所有 Base64 音频片段拼接起来，待流结束后解码并保存。

<Tabs>
  <Tab title="Python">
    ```python
    import os
    from openai import OpenAI
    import base64
    import numpy as np
    import soundfile as sf

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    messages = [
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
              "format": "wav",
            },
          }
        ],
      }
    ]

    completion = client.chat.completions.create(
      model="qwen3-livetranslate-flash",
      messages=messages,
      modalities=["text", "audio"],
      audio={"voice": "Cherry", "format": "wav"},
      stream=True,
      stream_options={"include_usage": True},
      extra_body={"translation_options": {"source_lang": "zh", "target_lang": "en"}},
    )

    # 拼接 Base64 片段，流结束后解码
    audio_string = ""
    for chunk in completion:
      if chunk.choices:
        if hasattr(chunk.choices[0].delta, "audio"):
          try:
            audio_string += chunk.choices[0].delta.audio["data"]
          except Exception as e:
            print(chunk.choices[0].delta.audio["transcript"])
      else:
        print(chunk.usage)

    wav_bytes = base64.b64decode(audio_string)
    audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
    sf.write("output.wav", audio_np, samplerate=24000)
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";
    import { createWriteStream } from "node:fs";
    import { Writer } from "wav";

    const client = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    });

    const messages = [
      {
        role: "user",
        content: [
          {
            type: "input_audio",
            input_audio: {
              data: "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
              format: "wav",
            },
          },
        ],
      },
    ];

    const completion = await client.chat.completions.create({
      model: "qwen3-livetranslate-flash",
      messages: messages,
      modalities: ["text", "audio"],
      audio: { voice: "Cherry", format: "wav" },
      stream: true,
      stream_options: { include_usage: true },
      translation_options: { source_lang: "zh", target_lang: "en" },
    });

    // 拼接 Base64 片段，流结束后解码
    let audioString = "";
    for await (const chunk of completion) {
      if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        if (chunk.choices[0].delta.audio?.data) {
          audioString += chunk.choices[0].delta.audio.data;
        }
      } else {
        console.log(chunk.usage);
      }
    }

    // 保存为 WAV 文件
    async function saveAudio(base64Data, outputPath) {
      const wavBuffer = Buffer.from(base64Data, "base64");
      const writer = new Writer({
        sampleRate: 24000,
        channels: 1,
        bitDepth: 16,
      });
      const outputStream = createWriteStream(outputPath);
      writer.pipe(outputStream);
      writer.write(wavBuffer);
      writer.end();
      await new Promise((resolve, reject) => {
        outputStream.on("finish", resolve);
        outputStream.on("error", reject);
      });
      console.log(`Audio saved to ${outputPath}`);
    }

    saveAudio(audioString, "output.wav");
    ```
  </Tab>
</Tabs>

### 实时播放

逐个解码收到的 Base64 音频片段并直接播放。此方式需要依赖特定平台的音频库。

<Tabs>
  <Tab title="Python">
    先安装 `pyaudio`：

| 平台              | 安装命令                                                                          |
| --------------- | ----------------------------------------------------------------------------- |
| macOS           | `brew install portaudio && pip install pyaudio`                               |
| Ubuntu / Debian | `sudo apt-get install python-pyaudio python3-pyaudio` 或 `pip install pyaudio` |
| CentOS          | `sudo yum install -y portaudio portaudio-devel && pip install pyaudio`        |
| Windows         | `python -m pip install pyaudio`                                               |

    ```python
    import os
    from openai import OpenAI
    import base64
    import numpy as np
    import pyaudio
    import time

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    messages = [
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
              "format": "wav",
            },
          }
        ],
      }
    ]

    completion = client.chat.completions.create(
      model="qwen3-livetranslate-flash",
      messages=messages,
      modalities=["text", "audio"],
      audio={"voice": "Cherry", "format": "wav"},
      stream=True,
      stream_options={"include_usage": True},
      extra_body={"translation_options": {"source_lang": "zh", "target_lang": "en"}},
    )

    # 初始化 PyAudio 实现实时播放
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=24000, output=True)

    for chunk in completion:
      if chunk.choices:
        if hasattr(chunk.choices[0].delta, "audio"):
          try:
            audio_data = chunk.choices[0].delta.audio["data"]
            wav_bytes = base64.b64decode(audio_data)
            audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
            stream.write(audio_np.tobytes())
          except Exception as e:
            print(chunk.choices[0].delta.audio["transcript"])

    time.sleep(0.8)
    stream.stop_stream()
    stream.close()
    p.terminate()
    ```
  </Tab>

  <Tab title="Node.js">
    先安装依赖：

| 平台              | 安装命令                                                         |
| --------------- | ------------------------------------------------------------ |
| macOS           | `brew install portaudio && npm install speaker`              |
| Ubuntu / Debian | `sudo apt-get install libasound2-dev && npm install speaker` |
| Windows         | `npm install speaker`                                        |

    ```javascript
    import OpenAI from "openai";
    import Speaker from "speaker";

    const client = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    });

    const messages = [
      {
        role: "user",
        content: [
          {
            type: "input_audio",
            input_audio: {
              data: "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
              format: "wav",
            },
          },
        ],
      },
    ];

    const completion = await client.chat.completions.create({
      model: "qwen3-livetranslate-flash",
      messages: messages,
      modalities: ["text", "audio"],
      audio: { voice: "Cherry", format: "wav" },
      stream: true,
      stream_options: { include_usage: true },
      translation_options: { source_lang: "zh", target_lang: "en" },
    });

    // 实时播放音频
    const speaker = new Speaker({
      sampleRate: 24000,
      channels: 1,
      bitDepth: 16,
      signed: true,
    });

    for await (const chunk of completion) {
      if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
        if (chunk.choices[0].delta.audio?.data) {
          const pcmBuffer = Buffer.from(chunk.choices[0].delta.audio.data, "base64");
          speaker.write(pcmBuffer);
        }
      } else {
        console.log(chunk.usage);
      }
    }

    speaker.on("finish", () => console.log("Playback complete"));
    speaker.end();
    ```
  </Tab>
</Tabs>

## 计费

<Tabs>
  <Tab title="音频">
    音频 Token 消耗取决于音频特征（如采样率）。如需查看实际 Token 用量，将 `stream_options.include_usage` 设为 `true`，然后查看响应中的 `usage` 字段。

    <Note>
      不足 1 秒的音频按 1 秒计费。
    </Note>
  </Tab>

  <Tab title="视频">
    视频 Token 消耗包含两部分：

    - **音频 Token**：Token 消耗取决于音频特征（如采样率）。不足 1 秒的音频按 1 秒计费。
    - **视频 Token**：根据帧数和分辨率计算。公式如下：

    ```text
    video_tokens = ceil(frame_count / 2) x (height / 32) x (width / 32) + 2
    ```

    其中：

    - 帧采样率为 2 FPS，帧数限制在 \[4, 128] 范围内。
    - 高度和宽度调整为 32 像素的倍数，并动态缩放以适应总像素数限制。

    <Accordion title="计算视频 Token 的 Python 脚本">
      ```python
      # 安装：pip install opencv-python
      import math
      import cv2

      FRAME_FACTOR = 2
      IMAGE_FACTOR = 32
      MAX_RATIO = 200
      VIDEO_MIN_PIXELS = 128 * 32 * 32
      VIDEO_MAX_PIXELS = 768 * 32 * 32
      FPS = 2
      FPS_MIN_FRAMES = 4
      FPS_MAX_FRAMES = 128
      VIDEO_TOTAL_PIXELS = 16384 * 32 * 32

      def round_by_factor(number, factor):
        return round(number / factor) * factor

      def ceil_by_factor(number, factor):
        return math.ceil(number / factor) * factor

      def floor_by_factor(number, factor):
        return math.floor(number / factor) * factor

      def get_video(video_path):
        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        cap.release()
        return frame_height, frame_width, total_frames, video_fps

      def smart_nframes(total_frames, video_fps):
        min_frames = ceil_by_factor(FPS_MIN_FRAMES, FRAME_FACTOR)
        max_frames = floor_by_factor(min(FPS_MAX_FRAMES, total_frames), FRAME_FACTOR)
        duration = total_frames / video_fps if video_fps != 0 else 0
        if duration - int(duration) > (1 / FPS):
          total_frames = math.ceil(duration * video_fps)
        else:
          total_frames = math.ceil(int(duration) * video_fps)
        nframes = total_frames / video_fps * FPS
        nframes = int(min(min(max(nframes, min_frames), max_frames), total_frames))
        if not (FRAME_FACTOR <= nframes <= total_frames):
          raise ValueError(f"nframes should in interval [{FRAME_FACTOR}, {total_frames}], but got {nframes}.")
        return nframes

      def smart_resize(height, width, nframes, factor=IMAGE_FACTOR):
        min_pixels = VIDEO_MIN_PIXELS
        total_pixels = VIDEO_TOTAL_PIXELS
        max_pixels = max(min(VIDEO_MAX_PIXELS, total_pixels / nframes * FRAME_FACTOR), int(min_pixels * 1.05))
        if max(height, width) / min(height, width) > MAX_RATIO:
          raise ValueError(f"absolute aspect ratio must be smaller than {MAX_RATIO}, got {max(height, width) / min(height, width)}")
        h_bar = max(factor, round_by_factor(height, factor))
        w_bar = max(factor, round_by_factor(width, factor))
        if h_bar * w_bar > max_pixels:
          beta = math.sqrt((height * width) / max_pixels)
          h_bar = floor_by_factor(height / beta, factor)
          w_bar = floor_by_factor(width / beta, factor)
        elif h_bar * w_bar < min_pixels:
          beta = math.sqrt(min_pixels / (height * width))
          h_bar = ceil_by_factor(height * beta, factor)
          w_bar = ceil_by_factor(width * beta, factor)
        return h_bar, w_bar

      def video_token_calculate(video_path):
        height, width, total_frames, video_fps = get_video(video_path)
        nframes = smart_nframes(total_frames, video_fps)
        resized_height, resized_width = smart_resize(height, width, nframes)
        video_token = int(math.ceil(nframes / FPS) * resized_height / 32 * resized_width / 32)
        video_token += 2
        return video_token

      if __name__ == "__main__":
        video_path = "spring_mountain.mp4"  # 替换为你的视频路径
        video_token = video_token_calculate(video_path)
        print("video_tokens:", video_token)
      ```
    </Accordion>
  </Tab>
</Tabs>

Token 定价详见[选择模型](/developer-guides/getting-started/model-selection)。

## 支持的语言

以下语言代码可用于设置源语言和目标语言。部分目标语言仅支持文本输出。

| 语言代码 | 语言   | 支持的输出 |
| ---- | ---- | ----- |
| en   | 英语   | 音频、文本 |
| zh   | 中文   | 音频、文本 |
| ru   | 俄语   | 音频、文本 |
| fr   | 法语   | 音频、文本 |
| de   | 德语   | 音频、文本 |
| pt   | 葡萄牙语 | 音频、文本 |
| es   | 西班牙语 | 音频、文本 |
| it   | 意大利语 | 音频、文本 |
| id   | 印尼语  | 文本    |
| ko   | 韩语   | 音频、文本 |
| ja   | 日语   | 音频、文本 |
| vi   | 越南语  | 文本    |
| th   | 泰语   | 文本    |
| ar   | 阿拉伯语 | 文本    |
| yue  | 粤语   | 音频、文本 |
| hi   | 印地语  | 文本    |
| el   | 希腊语  | 文本    |
| tr   | 土耳其语 | 文本    |

## 支持的语音

输出包含合成音频时，需设置 `voice` 参数。

| 语音名称           | `voice` 参数 | 描述                       | 支持的语言                               |
| -------------- | ---------- | ------------------------ | ----------------------------------- |
| Cherry         | Cherry     | 开朗、友好、真诚的年轻女性。           | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
| Ethan          | Ethan      | 标准普通话，略带北方口音。阳光、温暖、充满活力。 | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
| Nofish         | Nofish     | 一位平翘舌不分的设计师。             | 中文、英语、法语、德语、俄语、意大利语、西班牙语、葡萄牙语、日语、韩语 |
| Shanghai-Jada  | Jada       | 风风火火的上海女人。               | 中文                                  |
| Beijing-Dylan  | Dylan      | 在北京胡同里长大的小伙子。            | 中文                                  |
| Sichuan-Sunny  | Sunny      | 来自四川的甜美女孩。               | 中文                                  |
| Tianjin-Peter  | Peter      | 天津相声演员风格（捧哏）。            | 中文                                  |
| Cantonese-Kiki | Kiki       | 来自香港的甜美闺蜜。               | 粤语                                  |
| Sichuan-Eric   | Eric       | 来自四川成都、特立独行的男性。          | 中文                                  |

## 替代方案：使用 Qwen-Omni

也可以使用 **Qwen-Omni**（`qwen3-omni-flash`）配合翻译提示词来翻译音视频文件。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  completion = client.chat.completions.create(
    model="qwen3-omni-flash",
    messages=[
      {
        "role": "user",
        "content": [
          {"type": "input_audio", "input_audio": {"data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav"}},
          {"type": "text", "text": "Translate this audio from English to Chinese."},
        ],
      }
    ],
    modalities=["text"],
    stream=True,
  )

  for chunk in completion:
    if chunk.choices and chunk.choices[0].delta.content:
      print(chunk.choices[0].delta.content, end="")
  ```

  ```bash cURL
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3-omni-flash",
    "messages": [{
      "role": "user",
      "content": [
        {"type": "input_audio", "input_audio": {"data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav"}},
        {"type": "text", "text": "Translate this audio from English to Chinese."}
      ]
    }],
    "modalities": ["text"],
    "stream": true
  }'
  ```
</CodeGroup>

<Tip>
  Qwen-Omni 的完整能力（包括多模态对话）详见[音视频文件理解](/developer-guides/speech/multimodal-speech)。
</Tip>

## 常见问题

### 输入视频文件时，翻译的是什么内容？

模型翻译的是视频中的音频轨道。视觉信息作为上下文参考，用于提升翻译准确率。

例如，音频内容为「This is a mask」时：

- 如果视频画面是医用口罩，模型会翻译为「这是一个医用口罩」。
- 如果视频画面是化装舞会面具，模型会翻译为「这是一个化装舞会面具」。

## API 参考

完整的输入输出参数说明，请参见[音视频翻译 API 参考](/api-reference/speech-translation/audio-video-translation-api)。
