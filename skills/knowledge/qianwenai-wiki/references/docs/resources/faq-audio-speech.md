> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 语音常见问题

> CosyVoice 语音合成、Qwen-Omni 实时对话、Fun-ASR 语音识别的常见问题与解答。

<a id="cosyvoice-synthesis" />

## CosyVoice 实时语音合成

**API 参考**：[Python SDK](/api-reference/speech-synthesis/cosyvoice/python-sdk)、[Java SDK](/api-reference/speech-synthesis/cosyvoice/java-sdk)、[WebSocket API](/api-reference/speech-synthesis/cosyvoice/websocket-api)

### 发音不准确怎么办？

使用 [SSML](/developer-guides/speech/ssml)，必要时添加 [`phoneme` 标签](/developer-guides/speech/ssml)指定读音。

### 如何获取计费字符数？

- **Python — 非流式**：参见[字符计费规则](/api-reference/speech-synthesis/cosyvoice/python-sdk#字符计数规则)。
- **Python — 流式/回调**：解析 `on_event` [ResultCallback](/api-reference/speech-synthesis/cosyvoice/python-sdk#回调接口-resultcallback) 返回的 JSON，读取 `usage.characters` 字段——取**最后一条**消息的值。
- **Python — 日志**：设置 `DASHSCOPE_LOGGING_LEVEL=debug`，从最后一行日志中读取 `characters` 值。
- **Java — 非流式**：参见[字符计费规则](/api-reference/speech-synthesis/cosyvoice/java-sdk#字符计数规则)。
- **Java — 其他模式**：调用 [SpeechSynthesisResult](/api-reference/speech-synthesis/cosyvoice/java-sdk#响应) 的 `getUsage().getCharacters()`——取**最后一次**返回值。
- **WebSocket**：读取 [result-generated](/api-reference/speech-synthesis/cosyvoice/websocket-api#2-结果已生成事件-result-generated) 事件中的 `payload.usage.characters`。

### 为什么 TTS 使用 WebSocket 而非 HTTP？（WebSocket）

服务端需要主动推送音频和合成进度，WebSocket 适合低延迟流式合成场景。

### 如何获取请求 ID？

- **Python**：通过 `on_event` JSON 获取，或调用 [SpeechSynthesizer](/api-reference/speech-synthesis/cosyvoice/python-sdk#speechsynthesizer-类) 的 `get_last_request_id`。
- **Java**：调用 [SpeechSynthesisResult](/api-reference/speech-synthesis/cosyvoice/java-sdk#响应) 的 `getRequestId()`，或调用 [SpeechSynthesizer](/api-reference/speech-synthesis/cosyvoice/java-sdk#speechsynthesizer-类) 的 `getLastRequestId`。
- **WebSocket**：从 [result-generated](/api-reference/speech-synthesis/cosyvoice/websocket-api#2-结果已生成事件-result-generated) 或 [task-finished](/api-reference/speech-synthesis/cosyvoice/websocket-api#3-任务已完成事件-task-finished) 事件中获取。

### SSML 不生效怎么办？

1. 确认符合 [SSML 使用限制](/developer-guides/speech/ssml)。
2. 升级到[最新版 SDK](/api-reference/preparation/install-sdk)。
3. **SDK**：SSML 仅支持 **`call` / 非流式**调用，不支持纯 `streaming_call` 模式。
4. **WebSocket**：参见 [SSML 支持说明](/api-reference/speech-synthesis/cosyvoice/websocket-api#ssml-支持)。

### 音频无法播放怎么办？

1. **文件播放**：确保输出**格式**与文件扩展名一致，使用兼容的播放器。
2. **流式播放**：MP3/Opus 格式需使用**流式播放器**（FFmpeg、PyAudio、`AudioFormat`、`MediaSource`）。持续追加音频数据块，首个数据块可能仅包含 WAV/MP3 文件头。

### 播放卡顿怎么办？

缩短文本发送间隔；**回调函数保持轻量**（将耗时操作移出 WebSocket 线程）；确保网络稳定。

### 合成耗时过长怎么办？

避免分段之间的长时间停顿。正常情况下首包延迟约 **500 ms**，RTF **\< 1**。

### 末尾文本丢失或没有返回语音？

- **Python**：调用 [SpeechSynthesizer](/api-reference/speech-synthesis/cosyvoice/python-sdk#speechsynthesizer-类) 的 `streaming_complete`。
- **Java**：调用 [SpeechSynthesizer](/api-reference/speech-synthesis/cosyvoice/java-sdk#speechsynthesizer-类) 的 `streamingComplete`。
- **WebSocket**：发送 [finish-task](/api-reference/speech-synthesis/cosyvoice/websocket-api#3-结束指令-finish-task-instruction) 指令。

### 音频混乱或出现杂音？（WebSocket）

[run-task](/api-reference/speech-synthesis/cosyvoice/websocket-api#1-启动指令-run-task-instruction)、[continue-task](/api-reference/speech-synthesis/cosyvoice/websocket-api#2-续传指令-continue-task-instruction) 和 [finish-task](/api-reference/speech-synthesis/cosyvoice/websocket-api#3-结束指令-finish-task-instruction) 必须使用同一个 `task_id`，且不能乱序发送。

### WebSocket 连接关闭，报错 1007 或认证失败（WebSocket）

- **1007**：检查 JSON 格式和必填字段；`payload.input` 只能为 `{}` 或文本。
- **401/403**：检查 API Key / [排查认证失败问题](/api-reference/speech-synthesis/cosyvoice/websocket-api#排查认证失败)。

### SSL 或 `WebSocketApp` 报错（Python）

配置 CA 证书路径（`SSL_CERT_FILE`），或修复 macOS 证书路径问题。如果出现 `WebSocketApp` 的 `AttributeError`，重新安装 **websocket-client**（先 `pip uninstall websocket-client websocket`，再 `pip install websocket-client`）。详见 [CosyVoice Python SDK](/api-reference/speech-synthesis/cosyvoice/python-sdk)。

### 如何限制 API Key 仅用于 CosyVoice？

参见[业务空间](/developer-guides/administration/workspace)。

### 更多 CosyVoice 问题

[CosyVoice GitHub Q\&A](https://github.com/aliyun/alibabacloud-bailian-speech-demo/blob/master/docs/QA/cosyvoice.md)。

---

<a id="qwen-omni-realtime" />

## Qwen-Omni Realtime

**API 参考**：[Python SDK](/api-reference/real-time-multimodal/realtime-python-sdk)、[Java SDK](/api-reference/real-time-multimodal/realtime-java-sdk)、[Client events](/api-reference/real-time-multimodal/client-events)、[Server events](/api-reference/real-time-multimodal/server-events)

### 输入音频和图像如何对齐？

**以音频为时间轴。** 图像在发送时附加到对应时间点，会话过程中可随时开关视频输入。

### 推荐的输入速率是多少？

图像约 **2 fps**，音频包间隔约 **100 ms**。

### `turn_detection` 开启和关闭有什么区别？

**开启 `turn_detection`**（服务端 VAD）：

- 自动检测发言结束，**自动触发**推理，返回文本/音频响应。
- 模型响应期间可继续输入，响应结束后自动回到监听状态。
- **打断（Barge-in）**：在播放过程中说话会**中断**当前响应，回到输入状态。

**关闭 `turn_detection`**：

- 需要手动结束输入轮次，调用 **`commit`** 和 **`create_response`** / `createResponse`。
- 模型响应期间需**暂停**音频和视频输入，响应结束后再恢复。
- 使用 **`cancel_response`** / `cancelResponse` 中断响应。

<Note>
  开启 `turn_detection` 后，仍然可以手动调用 `commit`、`create_response` 和 `cancel_response`。
</Note>

### 为什么 `input_audio_transcription` 需要使用其他模型？

Omni 的设计目标是**响应**输入，而非专用的 **ASR** 转写管线。如需逐字转写，请使用专门的语音识别模型。

---

<a id="common-audio-issues" />

## 常见音频问题

识别问题通常由**容器格式与编码不匹配**或 **`sample_rate` / `format` 参数错误**导致。请验证音频的实际编码格式，不能仅依据文件扩展名判断。

### 使用 FFmpeg 转换音频格式

使用 [FFmpeg](https://ffmpeg.org/ffmpeg.html) 将音频转码为支持的格式。

```bash
ffmpeg -i input_audio.ext -c:a encoder_name -b:a bit_rate -ar sample_rate -ac number_of_channels output.ext

ffmpeg -i input.wav -c:a libmp3lame -q:a 0 output.mp3
ffmpeg -i input.mp3 -c:a pcm_s16le -ar 44100 -ac 2 output.wav
ffmpeg -i input.m4a -c:a copy output.aac
ffmpeg -i input.m4a -c:a aac -b:a 256k output.aac
ffmpeg -i input.flac -c:a libopus -b:a 128k -vbr on output.opus
```

### 查看容器格式、编码、采样率和声道数

使用 [ffprobe](https://ffmpeg.org/ffprobe.html)：

```bash
ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 input.xxx
```

根据输出结果设置 `format`、`sample_rate` / `sampleRate` 和声道数。

---

<a id="fun-asr-realtime" />

## Fun-ASR 实时语音识别

**API 参考**：[Python SDK](/api-reference/speech-recognition/fun-asr-realtime/python-sdk)、[Java SDK](/api-reference/speech-recognition/fun-asr-realtime/java-sdk)、[WebSocket](/api-reference/speech-recognition/fun-asr-realtime/websocket-api)

### 长时间静默时如何保持连接？

将 `heartbeat` 设为 true，并持续发送**静音音频**。

使用 FFmpeg 生成静音音频：

```bash
# 生成 1 秒 16kHz 单声道的静音音频
ffmpeg -f lavfi -i anullsrc=r=16000:cl=mono -t 1 -acodec pcm_s16le silent.wav
```

也可以使用 Audacity 或 Adobe Audition 创建静音片段。

### 如何识别本地音频文件？

- **Python**：使用 [Recognition 类](/api-reference/speech-recognition/fun-asr-realtime/python-sdk#recognition-类)的 `call` 方法进行完整文件识别（[非流式](/api-reference/speech-recognition/fun-asr-realtime/python-sdk#非流式调用)），或使用 `send_audio_frame` 进行流式识别（[双向流式](/api-reference/speech-recognition/fun-asr-realtime/python-sdk#双向流式调用)）。
- **Java**：使用 `call`（[非流式](/api-reference/speech-recognition/fun-asr-realtime/java-sdk#非流式调用)），或使用 `sendAudioFrame` / `streamCall`（[回调模式](/api-reference/speech-recognition/fun-asr-realtime/java-sdk#双向流式调用-基于回调) / [Flowable 模式](/api-reference/speech-recognition/fun-asr-realtime/java-sdk#双向流式调用-基于-flowable)流式识别）。

### 为什么使用 WebSocket 而非 HTTP？（WebSocket）

WebSocket 支持全双工通信，HTTP 请求/响应模式无法满足连续实时音频传输的需求。

### 语音识别不出来怎么办？

1. 确保 `format` 和 `sample_rate` / `sampleRate` 与实际音频匹配。参见[常见音频问题](#common-audio-issues)。
2. 确保 `language_hints`（Python）/ `languageHints`（Java）与实际语种一致。
3. 对于专业术语、产品名称或需要精确识别的专有名词，使用**自定义热词**功能。参见[自定义热词](/developer-guides/speech/improve-recognition-accuracy)。

---

<a id="fun-asr-file-transcription" />

## Fun-ASR 录音文件转写

**API 参考**：[Python SDK](/api-reference/speech-recognition/fun-asr-recording/python-sdk)、[RESTful API](/api-reference/speech-recognition/fun-asr-recording/restful-api)、[Java SDK](/api-reference/speech-recognition/fun-asr-recording/java-sdk)

### 是否支持 Base64 编码的音频？

不支持。仅支持**公网可访问的 HTTP(S) URL**，不支持 Base64、原始二进制上传或本地路径。

### 如何将音频托管到公网 URL？

<Accordion title="1. 选择存储方式">
  - **对象存储（推荐）**：支持公共读或签名 URL，可配合 CDN 加速。
  - **Web 服务器**：适合小规模测试的 HTTPS 服务。
  - **CDN**：适合高并发场景。
</Accordion>

<Accordion title="2. 上传文件">
  - **对象存储**：创建 Bucket，上传文件，设置**公共读**或生成临时访问链接。
  - **Web 服务器**：放置到 Web 服务目录（例如 `/var/www/html/audio/`）。
</Accordion>

<Accordion title="3. 获取公网 URL">
  - 对象存储：`https://<bucket>.<region>.aliyuncs.com/<object-key>` 或自定义域名。
  - Web 服务器：`https://your-domain.com/audio/file.mp3`
  - CDN：`https://cdn.your-domain.com/audio/file.mp3`
</Accordion>

<Accordion title="4. 验证 URL">
  通过浏览器或 `curl`/Postman 访问——确认返回 HTTP 200 且音频可正常播放。
</Accordion>

另见[使用限制](/api-reference/speech-recognition/fun-asr-recording/python-sdk#限制条件)。

### 识别需要多长时间？

任务状态流转为 **PENDING** → **RUNNING** → **SUCCEEDED** 或 **FAILED**。排队时间取决于系统负载和文件时长。

### 轮询后为什么获取不到结果？

可能触发了**频率限制**——检查响应内容并适当增加轮询间隔。

### OSS 临时 URL 无法访问怎么办？（REST）

设置请求头 `X-DashScope-OssResourceResolve` 为 `enable`。

<Note>
  此方式适用于直接调用 REST API 的场景。官方 Java/Python SDK 可能不支持此请求头，建议优先使用稳定的公网 URL。
</Note>

### 音频识别不出来怎么办？

检查音频格式和采样率，使用 ffprobe 排查，参见[常见音频问题](#common-audio-issues)。
