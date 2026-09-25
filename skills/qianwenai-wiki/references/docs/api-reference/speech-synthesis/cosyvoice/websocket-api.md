> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Audio-TTS/CosyVoice WebSocket API

> Qwen-Audio-TTS/CosyVoice 语音合成 WebSocket 接口协议

CosyVoice 文本转语音的 WebSocket 接口参数与协议。DashScope SDK 仅支持 Java 和 Python，其他语言请使用 WebSocket 接口。

**用户指南**： 模型概览和音色选择，参见[语音合成](/developer-guides/speech/tts)。

WebSocket 支持全双工通信。客户端与服务器通过一次握手建立持久连接，然后实时相互推送数据。

常用的 WebSocket 库：

- Go: `gorilla/websocket`
- PHP: `Ratchet`
- Node.js: `ws`

<Note>
  **CosyVoice 模型仅支持 WebSocket，不支持 HTTP REST API。** 使用 HTTP 请求（POST、GET）会返回 InvalidParameter 或 URL 错误。
</Note>

## 前提条件

获取 [API Key](/api-reference/preparation/api-key)。

## 模型与定价

参见[语音合成](/developer-guides/speech/tts)。

## 文本与格式限制

### 文本长度限制

每条[续传指令](#2-续传指令-continue-task-instruction)最多发送 20,000 个字符。所有续传指令的累计字符数不得超过 200,000。

### 字符计数规则

- 中文字符（简体、繁体、日文汉字、韩文汉字）按 2 个字符计算。其他字符（标点、字母、数字、假名/谚文）按 1 个字符计算。
- SSML 标签不计入字符数。
- 示例：
  - `"你好"` → 2 + 2 = 4 个字符
  - `"中A文123"` → 2 + 1 + 2 + 1 + 1 + 1 = 8 个字符
  - `"中文。"` → 2 + 2 + 1 = 5 个字符
  - `"中 文。"` → 2 + 1 + 2 + 1 = 6 个字符
  - `"<speak>你好</speak>"` → 2 + 2 = 4 个字符

### 编码格式

使用 UTF-8 编码。

### 数学表达式支持

数学表达式解析功能适用于 cosyvoice-v3-flash 和 cosyvoice-v3-plus，涵盖常见的中小学数学内容，包括基本运算、代数和几何。

<Note>
  该功能仅支持中文。
</Note>

详见[将 LaTeX 公式转为语音（仅中文）](/developer-guides/speech/ssml#latex-公式转语音)。

### [SSML](/developer-guides/speech/ssml) 支持

使用 SSML 需同时满足以下条件：

1. **模型**： 仅 cosyvoice-v3-flash 和 cosyvoice-v3-plus 支持 SSML。
2. **音色**： 使用支持 SSML 的音色：
   - 所有克隆音色（通过音色克隆 API 创建）。
   - [音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标记为支持 SSML 的系统音色。
   <Note>
     不支持 SSML 的系统音色（如部分基础音色）即使开启了 `enable_ssml`，仍会返回错误 "SSML text is not supported at the moment!"。
   </Note>
3. **参数**： 在[启动指令](#1-启动指令-run-task-instruction)中将 `enable_ssml` 设置为 `true`。

然后通过[续传指令](#2-续传指令-continue-task-instruction)发送 SSML 格式的文本。完整示例参见[快速开始](/developer-guides/speech/ssml)。

## 交互流程

![交互流程](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/8014313771/CAEQVBiBgIDKu4Tc5hkiIGRhYzBkZDc1OTFjNDQwMTY4YjY2YTI4NGZhNzY5Y2I04709861_20241015153444.149.svg)

客户端到服务器的消息为[指令](#指令-客户端到服务器)，服务器到客户端的消息为 JSON [事件](#事件-服务器到客户端)或二进制音频流。

交互序列：

1. 建立 WebSocket 连接。
2. 发送[启动指令](#1-启动指令-run-task-instruction)开始任务。
3. 等待收到[任务已启动事件](#1-任务已启动事件-task-started)后再继续。
4. 发送文本：

   按顺序发送一条或多条[续传指令](#2-续传指令-continue-task-instruction)。服务器收到完整句子后，返回[结果已生成事件](#2-结果已生成事件-result-generated)和音频流。文本长度约束参见[续传指令](#2-续传指令-continue-task-instruction)中的 `text` 字段。

   <Note>
     按顺序发送多条[续传指令](#2-续传指令-continue-task-instruction)提交文本片段。服务器会自动将文本按句子分段：

     - 完整句子会立即合成。
     - 不完整的句子会缓存，直到收到完整句子。不完整句子不会返回音频。

     收到[结束指令](#3-结束指令-finish-task-instruction)后，服务器会强制合成所有缓存内容。
   </Note>
5. 通过 `binary` 通道接收音频流。
6. 发送完所有文本后，发送[结束指令](#3-结束指令-finish-task-instruction)。继续接收音频流。不要跳过此步骤，否则音频末尾可能丢失。
7. 从服务器接收[任务已完成事件](#3-任务已完成事件-task-finished)。
8. 关闭 WebSocket 连接。

建议复用 WebSocket 连接来执行多个任务，而非每次都新建连接。参见[连接开销与复用](#连接开销与复用)。

<Note>
  保持 task\_id 一致：单个任务中的**启动指令、所有续传指令和结束指令**必须使用同一个 **task\_id**。

  **task\_id 不匹配会导致**：

  - 音频推送乱序。
  - 语音内容错位。
  - 任务状态异常，可能无法收到任务已完成事件。
  - 计费失败或使用量统计不准确。

  **最佳实践**：

  - 发送启动指令时生成唯一的 task\_id（如 UUID）。
  - 将 task\_id 存入变量。
  - 后续所有续传指令和结束指令使用该 task\_id。
  - 收到任务已完成事件后，为下一个任务生成新的 task\_id。
</Note>

## 客户端实现要点

### 服务端与客户端职责

**服务端职责**

服务端按顺序推送完整的音频流，无需处理音频排序或完整性。

**客户端职责**

1. **读取并拼接所有音频片段**

   服务端将音频拆分为多个二进制帧。接收所有帧并拼接：

```python
# Python：拼接音频片段
with open("output.mp3", "ab") as f:  # 追加模式
  f.write(audio_chunk)  # audio_chunk 为每个接收到的二进制音频片段
```

```javascript
// JavaScript：拼接音频片段
const audioChunks = [];
ws.onmessage = (event) => {
  if (event.data instanceof Blob) {
    audioChunks.push(event.data);  // 收集所有音频片段
  }
};
// 任务完成后合并音频
const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
```

2. **保持完整的 WebSocket 生命周期**

   从发送[启动指令](#1-启动指令-run-task-instruction)到接收[任务已完成事件](#3-任务已完成事件-task-finished)期间，不要断开连接。常见错误：

   - 音频未接收完毕就关闭连接，导致音频不完整。
   - 忘记发送[结束指令](#3-结束指令-finish-task-instruction)，导致文本缓存未处理。
   - 页面跳转或应用后台化时未处理 WebSocket 心跳保活。

   <Note>
     移动端（Flutter、iOS、Android）进入后台时需要特殊网络处理。在后台任务或服务中保持 WebSocket 连接，或返回前台时重新初始化。
   </Note>

3. **ASR → LLM → TTS 流程中的文本完整性**

   确保传入 TTS 的文本完整：

   - 等待 LLM 生成完整句子后再发送[续传指令](#2-续传指令-continue-task-instruction)，而非逐字流式传输。
   - 流式合成时，按自然句边界（句号、问号）发送文本。
   - LLM 生成完成后，务必发送[结束指令](#3-结束指令-finish-task-instruction)，避免末尾内容丢失。

### 平台特定提示

- **Flutter**： 在 `dispose` 方法中关闭连接，防止使用 `web_socket_channel` 时内存泄漏。处理应用生命周期事件（如 `AppLifecycleState.paused`）以应对后台切换。
- **Web（浏览器）**： 部分浏览器限制 WebSocket 连接数量。多个任务复用同一个连接。使用 `beforeunload` 在页面关闭前关闭连接。
- **移动端（iOS/Android 原生）**： 应用进入后台时，操作系统可能暂停或终止网络连接。使用后台任务或前台服务保持 WebSocket 活跃，或返回前台时重新初始化任务。

## URL

```plaintext
wss://dashscope.aliyuncs.com/api-ws/v1/inference
```

<Note>
  **常见 URL 错误**：

  - **协议错误**： 使用 `wss://`，不要使用 `http://` 或 `https://`。
  - **认证参数放在 URL 中**： 不要在 URL 中放置 Authorization（如 `?Authorization=bearer YOUR_API_KEY`）。应在 HTTP 握手头中设置。参见[请求头](#请求头)。
  - **多余的路径片段**： 不要在 URL 后拼接模型名或其他参数。模型在[启动指令](#1-启动指令-run-task-instruction)的 `payload.model` 中指定。
</Note>

## 请求头

| 参数                         | 类型     | 必填 | 描述                                   |
| -------------------------- | ------ | -- | ------------------------------------ |
| Authorization              | string | 是  | 认证令牌。格式：`bearer $DASHSCOPE_API_KEY`。 |
| user-agent                 | string | 否  | 客户端标识，用于来源追踪。                        |
| X-DashScope-WorkSpace      | string | 否  | 千问AI平台业务空间 ID。                       |
| X-DashScope-DataInspection | string | 否  | 数据合规检查。默认 `enable`。非必需不要设置。          |

<Note>
  **认证时机**

  认证发生在 WebSocket 握手阶段，而非发送[启动指令](#1-启动指令-run-task-instruction)时。如果 Authorization 头缺失或无效，服务器会以 HTTP 401 或 403 拒绝握手。客户端库通常将其报告为 WebSocketBadStatus 异常。
</Note>

### 排查认证失败

如果 WebSocket 连接失败：

1. **检查 API Key 格式**： 确认 Authorization 头使用 `bearer $DASHSCOPE_API_KEY` 格式，`bearer` 与 Key 之间有空格。
2. **验证 API Key 有效性**： 查看 [API Key](https://platform.qianwenai.com/home/api-keys) 页面，确认 Key 处于激活状态且已授权 CosyVoice 模型。
3. **检查头设置位置**： 在 WebSocket 握手时设置 Authorization 头。各语言示例：
   - Python (websockets)：`extra_headers={"Authorization": f"bearer {api_key}"}`
   - JavaScript：浏览器原生 WebSocket API 不支持自定义头。使用服务端代理或其他库（如 ws）。
   - Go (gorilla/websocket)：`header.Add("Authorization", fmt.Sprintf("bearer %s", apiKey))`
4. **测试网络连通性**： 使用 curl 或 Postman 调用其他支持 HTTP 的 DashScope API，验证 API Key 是否有效。

### 浏览器中使用 WebSocket

浏览器 `new WebSocket(url)` API **在握手时不支持自定义请求头**（包括 Authorization）。无法直接从前端的代码认证。

**解决方案：使用后端代理**

1. 从后端（Node.js、Java 或 Python）连接 CosyVoice，后端可以设置 Authorization 头。
2. 前端通过 WebSocket 连接到你的后端，后端转发消息到 CosyVoice。
3. 这样可以隐藏 API Key，同时可以添加认证、日志或限流等功能。

<Warning>
  不要将 API Key 硬编码在前端代码中。Key 泄露可能导致账户被盗用、产生意外费用或数据泄露。
</Warning>

**示例代码**：

其他语言可参考以下示例实现相同逻辑，或使用 AI 工具转换。

- 前端（原生 Web）+ 后端（Node.js Express）：[cosyvoiceNodeJs\_en.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/amhrik/cosyvoiceNodeJs_en.zip)
- 前端（原生 Web）+ 后端（Python Flask）：[cosyvoiceFlask\_en.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/dxnvac/cosyvoiceFlask_en.zip)

## 指令 (客户端到服务器)

指令是以 WebSocket 文本帧发送的 JSON 消息，用于控制任务生命周期。

按以下顺序发送指令：

1. **发送**[启动指令](#1-启动指令-run-task-instruction)
   - 启动任务。
   - 后续所有[续传指令](#2-续传指令-continue-task-instruction)和[结束指令](#3-结束指令-finish-task-instruction)使用相同的 `task_id`。
2. **发送**[续传指令](#2-续传指令-continue-task-instruction)
   - 发送待合成的文本。
   - 仅在收到[任务已启动事件](#1-任务已启动事件-task-started)后发送。
3. **发送**[结束指令](#3-结束指令-finish-task-instruction)
   - 结束任务。
   - 在所有续传指令发送完成后发送。

<a id="1-启动指令-run-task-instruction" />

### 1. 启动指令 (run-task instruction): 启动任务

启动文本转语音任务。在此配置音色、采样率等参数。

<Note>
  - **发送时机**： WebSocket 连接建立后发送。
  - **不要在此发送文本。** 文本通过[续传指令](#2-续传指令-continue-task-instruction)发送。
  - **input 字段必填**，但值必须为 `{}`。省略会导致 InvalidParameter 错误（`"Missing required parameter 'payload.input'! Please follow the protocol!"`）。
</Note>

**示例**：

```json
{
  "header": {
    "action": "run-task",
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
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
      "pitch": 1
    },
    "input": {}
  }
}
```

`header` **参数**：

| 参数               | 类型     | 必填 | 描述                                                                                                                        |
| ---------------- | ------ | -- | ------------------------------------------------------------------------------------------------------------------------- |
| header.action    | string | 是  | 固定值："run-task"。                                                                                                           |
| header.task\_id  | string | 是  | 32 位 UUID。连字符可选（如 `"2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx"` 或 `"2bf83b9abaeb4fda8d9axxxxxxxxxxxx"`）。多数语言提供内置的 UUID 生成 API。 |
| header.streaming | string | 是  | 固定值："duplex"。                                                                                                             |

Python 生成 task\_id 示例：

```python
import uuid

def generateTaskId(self):
  # 生成随机 UUID
  return uuid.uuid4().hex
```

后续所有[续传指令](#2-续传指令-continue-task-instruction)和[结束指令](#3-结束指令-finish-task-instruction)使用同一个 task\_id。

`payload` **参数**：

| 参数                  | 类型     | 必填 | 描述                                                                         |
| ------------------- | ------ | -- | -------------------------------------------------------------------------- |
| payload.task\_group | string | 是  | 固定值："audio"。                                                               |
| payload.task        | string | 是  | 固定值："tts"。                                                                 |
| payload.function    | string | 是  | 固定值："SpeechSynthesizer"。                                                   |
| payload.model       | string | 是  | 文本转语音模型。参见[音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。    |
| payload.input       | object | 是  | **必填，但在启动指令中必须为空（`{}`）。** 文本通过[续传指令](#2-续传指令-continue-task-instruction)发送。 |

<Note>
  **常见错误**： 省略 input 字段或添加意外字段（如 mode、content）会导致 "InvalidParameter: task can not be null" 或连接关闭（WebSocket 码 1007）。
</Note>

**payload.parameters 参数**：

| 参数                       | 类型             | 必填 | 描述                                                                                                                       |
| ------------------------ | -------------- | -- | ------------------------------------------------------------------------------------------------------------------------ |
| text\_type               | string         | 是  | 固定值："PlainText"。                                                                                                         |
| voice                    | string         | 是  | 用于合成的音色。参见[音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)查看可用的系统音色。                                         |
| format                   | string         | 否  | 音频格式。支持 pcm、wav、mp3（默认）和 opus。opus 格式可通过 `bit_rate` 调整码率。                                                                |
| sample\_rate             | integer        | 否  | 采样率（Hz）。默认 22050。可选值：8000、16000、22050、24000、44100、48000。                                                                 |
| volume                   | integer        | 否  | 音量。默认 50。范围 \[0, 100]，线性缩放。0 为静音，100 为最大音量。                                                                              |
| rate                     | float          | 否  | 语速。默认 1.0。范围 \[0.5, 2.0]。小于 1.0 减慢语速，大于 1.0 加快。                                                                          |
| pitch                    | float          | 否  | 音调倍数。默认 1.0。范围 \[0.5, 2.0]。与感知音调的关系并非严格线性，建议测试选择合适的值。                                                                    |
| enable\_ssml             | boolean        | 否  | 是否启用 SSML。设为 `true` 时仅允许发送一条[续传指令](#2-续传指令-continue-task-instruction)。                                                   |
| bit\_rate                | int            | 否  | 音频码率（Opus 格式），单位 kbps。默认 32。范围 \[6, 510]。                                                                                |
| word\_timestamp\_enabled | boolean        | 否  | 是否启用词级时间戳。默认 false。仅支持[音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标记为支持的系统音色。                           |
| seed                     | int            | 否  | 生成的随机种子。相同种子且参数一致时，输出结果可复现。默认 0。范围 \[0, 65535]。                                                                          |
| language\_hints          | array\[string] | 否  | 合成目标语言。可选值：zh、en、fr、de、ja、ko、ru、pt、th、id、vi。该字段为数组，但仅处理第一个元素。                                                            |
| instruction              | string         | 否  | 控制合成效果，如方言、情感或说话风格。仅支持[音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)中标记为支持 Instruct 的系统音色。最大长度 100 个字符。    |
| enable\_aigc\_tag        | boolean        | 否  | 是否在生成的音频中嵌入不可见的 AIGC 标识符。设为 true 时，标识符会嵌入 WAV、MP3 和 Opus 格式中。默认 false。cosyvoice-v3-flash 和 cosyvoice-v3-plus 支持。         |
| aigc\_propagator         | string         | 否  | 设置 AIGC 标识符中的 `ContentPropagator` 字段。仅在 `enable_aigc_tag` 为 `true` 时生效。默认 UID。cosyvoice-v3-flash 和 cosyvoice-v3-plus 支持。 |
| aigc\_propagate\_id      | string         | 否  | 设置 AIGC 标识符中的 `PropagateID` 字段。仅在 `enable_aigc_tag` 为 `true` 时生效。默认为当前请求 ID。cosyvoice-v3-flash 和 cosyvoice-v3-plus 支持。   |
| hot\_fix                 | object         | 否  | 文本热补丁配置。合成前自定义发音或替换文本。仅 cosyvoice-v3-flash 支持。                                                                           |
| enable\_markdown\_filter | boolean        | 否  | 是否启用 Markdown 过滤。合成前移除输入文本中的 Markdown 符号。默认 false。仅 cosyvoice-v3-flash 支持。                                               |

启用 word\_timestamp\_enabled 后，时间戳会出现在**结果已生成事件**中：

```json
{
  "header": {
    "task_id": "3f39be22-efbd-4844-91d5-xxxxxxxxxxxx",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "index": 0,
        "words": [
          {
            "text": "bed",
            "begin_index": 0,
            "end_index": 1,
            "begin_time": 280,
            "end_time": 640
          }
        ]
      }
    }
  }
}
```

cosyvoice-v3-flash 克隆音色的 instruction 示例：

```plaintext
请用粤语说话。（支持的方言：粤语、东北、甘肃、贵州、河南、湖北、江西、闽南、宁夏、山西、陕西、山东、上海话、四川、天津、云南。）
请尽可能大声地说一句话。
请尽可能慢地说一句话。
请尽可能快地说一句话。
请非常轻柔地说一句话。
你能说慢一点吗？
你能说得非常快吗？
你能说非常慢吗？
你能说快一点吗？
请非常生气地说一句话。
请非常开心地说一句话。
请非常害怕地说一句话。
请非常伤心地说一句话。
请非常惊讶地说一句话。
请尽量听起来坚定一些。
请尽量听起来生气一些。
请使用亲切的语气。
请用冰冷的语气说话。
请用威严的语气说话。
我想体验自然的语气。
我想看看你怎么表达威胁。
我想看看你怎么表达智慧。
我想看看你怎么表达诱惑。
我想听你生动地说话。
我想听你充满热情地说话。
我想听你沉稳地说话。
我想听你充满自信地说话。
你能兴奋地和我说话吗？
你能表现出傲慢的情绪吗？
你能表现出优雅的情绪吗？
你能愉快地回答问题吗？
你能给出温柔的情感表达吗？
你能用平静的语气和我说话吗？
你能深入地回答我吗？
你能用粗犷的态度和我说话吗？
用阴险的声音告诉我答案。
用坚定的声音告诉我答案。
用自然友好的聊天风格叙述。
用广播剧播客的语气说话。
```

cosyvoice-v3-flash 系统音色的 instruction 必须使用固定格式，参见[音色列表](/api-reference/speech-synthesis/cosyvoice/voice-list)。

<a id="hot_fix" />

hot\_fix 示例：

```json
"hot_fix": {
  "pronunciation": [
  {"weather": "tian1 qi4"}
  ],
  "replace": [
  {"today": "jin1 tian1"}
  ]
}
```

<a id="2-续传指令-continue-task-instruction" />

### 2. 续传指令 (continue-task instruction)

发送待合成的文本。可以一次性发送全部文本，也可以按顺序拆分为多条指令发送。

<Note>
  **发送时机**： 收到[任务已启动事件](#1-任务已启动事件-task-started)后。
</Note>

<Note>
  文本片段之间的间隔不能超过 23 秒，否则会返回 "request timeout after 23 seconds" 错误。如果没有更多文本需要发送，请发送[结束指令](#3-结束指令-finish-task-instruction)结束任务。23 秒超时由服务端强制执行，无法修改。
</Note>

**示例**：

```json
{
  "header": {
    "action": "continue-task",
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "streaming": "duplex"
  },
  "payload": {
    "input": {
      "text": "床前明月光，疑是地上霜。"
    }
  }
}
```

`header` **参数**：

| 参数               | 类型     | 必填 | 描述                                                     |
| ---------------- | ------ | -- | ------------------------------------------------------ |
| header.action    | string | 是  | 固定值："continue-task"。                                   |
| header.task\_id  | string | 是  | 必须与[启动指令](#1-启动指令-run-task-instruction)中的 task\_id 一致。 |
| header.streaming | string | 是  | 固定值："duplex"。                                          |

`payload` **参数**：

| 参数         | 类型     | 必填 | 描述      |
| ---------- | ------ | -- | ------- |
| input.text | string | 是  | 待合成的文本。 |

<a id="3-结束指令-finish-task-instruction" />

### 3. 结束指令 (finish-task instruction): 结束任务

结束任务。**务必发送此指令**，否则：

- **音频不完整**： 服务器不会强制合成缓存中的句子，导致音频末尾丢失。
- **连接超时**： 最后一条[续传指令](#2-续传指令-continue-task-instruction)后等待超过 23 秒会触发超时。
- **计费问题**： 使用量信息可能不准确。

<Note>
  **发送时机**： 所有[续传指令](#2-续传指令-continue-task-instruction)发送完成后**立即**发送。不要等待音频播放完成——这可能导致超时。
</Note>

**示例**：

```json
{
  "header": {
    "action": "finish-task",
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "streaming": "duplex"
  },
  "payload": {
    "input": {}
  }
}
```

`header` **参数**：

| 参数               | 类型     | 必填 | 描述                                                     |
| ---------------- | ------ | -- | ------------------------------------------------------ |
| header.action    | string | 是  | 固定值："finish-task"。                                     |
| header.task\_id  | string | 是  | 必须与[启动指令](#1-启动指令-run-task-instruction)中的 task\_id 一致。 |
| header.streaming | string | 是  | 固定值："duplex"。                                          |

`payload` **参数**：

| 参数            | 类型     | 必填 | 描述        |
| ------------- | ------ | -- | --------- |
| payload.input | object | 是  | 固定值：`{}`。 |

## 事件 (服务器到客户端)

事件是服务器发送的 JSON 消息，标记任务生命周期的各个阶段。

<Note>
  二进制音频单独发送，不包含在任何事件中。
</Note>

<a id="1-任务已启动事件-task-started" />

### 1. 任务已启动事件 (task-started event)

确认任务已启动。仅在收到此事件后才能发送[续传指令](#2-续传指令-continue-task-instruction)或[结束指令](#3-结束指令-finish-task-instruction)，否则任务会失败。

`task-started` 事件的 `payload` 为空。

**示例**：

```json
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-started",
    "attributes": {}
  },
  "payload": {}
}
```

`header` **参数**：

| 参数              | 类型     | 描述                  |
| --------------- | ------ | ------------------- |
| header.event    | string | 固定值："task-started"。 |
| header.task\_id | string | 客户端生成的任务 ID。        |

<a id="2-结果已生成事件-result-generated" />

### 2. 结果已生成事件 (result-generated event)

发送[续传指令](#2-续传指令-continue-task-instruction)和[结束指令](#3-结束指令-finish-task-instruction)期间，服务器会持续返回 `result-generated` 事件和二进制音频帧。

每个 `result-generated` 事件包含当前句子索引。音频数据以二进制帧形式在事件之间到达。一个句子对应多个二进制音频帧。按顺序接收并追加到同一个文件中。

**示例**：

```json
{
  "header": {
    "task_id": "3f2d5c86-0550-45c0-801f-xxxxxxxxxx",
    "event": "result-generated",
    "attributes": {}
  },
  "payload": {
    "output": {
      "sentence": {
        "index": 0,
        "words": []
      }
    },
    "usage": {
      "characters": 11
    }
  }
}
```

`header` **参数**：

| 参数                | 类型     | 描述                      |
| ----------------- | ------ | ----------------------- |
| header.event      | string | 固定值："result-generated"。 |
| header.task\_id   | string | 客户端生成的任务 ID。            |
| header.attributes | object | 附加属性——通常为空。             |

`payload` **参数**：

| 参数                                         | 类型      | 描述                                                                                  |
| ------------------------------------------ | ------- | ----------------------------------------------------------------------------------- |
| payload.output.type                        | string  | 句子事件类型。值为 `sentence-begin`（句子开始）、`sentence-synthesis`（句子合成中）或 `sentence-end`（句子结束）。 |
| payload.output.sentence.index              | integer | 句子编号，从 0 开始。                                                                        |
| payload.output.sentence.words              | array   | 词信息数组。                                                                              |
| payload.output.sentence.words.text         | string  | 词文本。                                                                                |
| payload.output.sentence.words.begin\_index | integer | 词在句子中的起始位置，从 0 开始计数。                                                                |
| payload.output.sentence.words.end\_index   | integer | 词在句子中的结束位置，从 1 开始计数。                                                                |
| payload.output.sentence.words.begin\_time  | integer | 词音频的起始时间戳，单位毫秒。                                                                     |
| payload.output.sentence.words.end\_time    | integer | 词音频的结束时间戳，单位毫秒。                                                                     |
| payload.output.original\_text              | string  | 当前句子的原始文本。仅在 `type` 为 `sentence-begin` 或 `sentence-end` 时出现。                        |
| payload.usage.characters                   | integer | 截至目前的累计计费字符数。`usage` 字段仅在 `type` 为 `sentence-end` 的事件中出现，请以最后一次出现的值为准。              |

<a id="3-任务已完成事件-task-finished" />

### 3. 任务已完成事件 (task-finished event)

标记任务结束。

任务结束后，可以关闭 WebSocket 连接或复用它发送新的[启动指令](#1-启动指令-run-task-instruction)（参见[连接开销与复用](#连接开销与复用)）。

**示例**：

```json
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-finished",
    "attributes": {}
  },
  "payload": {
    "output": {}
  }
}
```

`header` **参数**：

| 参数              | 类型     | 描述                   |
| --------------- | ------ | -------------------- |
| header.event    | string | 固定值："task-finished"。 |
| header.task\_id | string | 客户端生成的任务 ID。         |

<a id="4-任务失败事件-task-failed" />

### 4. 任务失败事件 (task-failed event)

表示任务失败。关闭 WebSocket 连接并查看错误信息。

**示例**：

```json
{
  "header": {
    "task_id": "2bf83b9a-baeb-4fda-8d9a-xxxxxxxxxxxx",
    "event": "task-failed",
    "error_code": "InvalidParameter",
    "error_message": "[tts:]Engine return error code: 418",
    "attributes": {}
  },
  "payload": {}
}
```

`header` **参数**：

| 参数                    | 类型     | 描述                 |
| --------------------- | ------ | ------------------ |
| header.event          | string | 固定值："task-failed"。 |
| header.task\_id       | string | 客户端生成的任务 ID。       |
| header.error\_code    | string | 错误类型。              |
| header.error\_message | string | 详细错误原因。            |

## 任务中断

流式合成过程中，可以提前中断当前任务（如用户取消播放），使用以下方式之一：

| 中断方式   | 服务端行为                              | 使用场景                        |
| ------ | ---------------------------------- | --------------------------- |
| 关闭连接   | 立即停止合成。丢弃未发送的音频。不返回任务已完成事件。连接无法复用。 | **立即停止**： 用户取消播放、切换内容或退出应用。 |
| 发送结束指令 | 强制合成缓存中的文本。返回剩余音频和任务已完成事件。连接可复用。   | **优雅结束**： 停止发送文本但接收所有缓存音频。  |

## 连接开销与复用

WebSocket 服务支持连接复用。

发送[启动指令](#1-启动指令-run-task-instruction)启动任务，发送[结束指令](#3-结束指令-finish-task-instruction)结束任务。收到[任务已完成事件](#3-任务已完成事件-task-finished)后，复用同一个连接发送新的启动指令。

<Note>
  1. 仅在收到[任务已完成事件](#3-任务已完成事件-task-finished)后发送新的[启动指令](#1-启动指令-run-task-instruction)。
  2. 同一个连接上的不同任务使用不同的 task\_id。
  3. 失败的任务会触发[任务失败事件](#4-任务失败事件-task-failed)并关闭连接（无法复用）。
  4. 连接空闲 60 秒后超时断开。
</Note>

## 性能与并发

### 并发限制

参见[限速](/developer-guides/administration/rate-limits)。

如需提高并发配额，请联系客服。配额调整需要审核，通常需要 1-3 个工作日。

<Note>
  **最佳实践**： 复用 WebSocket 连接来执行多个任务。参见[连接开销与复用](#连接开销与复用)。
</Note>

### 连接延迟

**典型连接时间**：

- 跨境连接：1-3 秒。极少数情况下 10-30 秒。

**排查连接过慢（>30 秒）**：

1. **网络延迟**： 检查跨境连接质量或 ISP 性能。
2. **DNS 过慢**： 尝试使用公共 DNS（8.8.8.8）或为 dashscope.aliyuncs.com 配置本地 hosts 文件。
3. **TLS 握手**： 升级到 TLS 1.2 或更高版本。
4. **代理/防火墙**： 企业网络可能阻止或限制 WebSocket 连接。

**排查工具**：

- 使用 Wireshark 或 tcpdump 分析 TCP 握手、TLS 握手和 WebSocket Upgrade 的耗时。
- 使用 curl 测试 HTTP 延迟：`curl -w "@curl-format.txt" -o /dev/null -s https://dashscope.aliyuncs.com`

### 音频生成速度

- 实时率（RTF）：0.1-0.5 倍实时（1 秒音频需要 0.1-0.5 秒生成）。实际速度因模型、文本长度和服务器负载而异。
- 首包延迟：发送续传指令到收到首个音频片段需 200-800 毫秒。

## 示例代码

基础连通性示例。请根据实际业务场景实现生产级逻辑。建议使用异步编程同时发送和接收：

1. **连接**： 使用 WebSocket 库的 connect 函数，携带[请求头](#请求头)和[URL](#url)建立连接。

2. **监听消息**： 服务器推送二进制音频和[事件](#事件-服务器到客户端)：

   **事件**：

   - **task-started**： 任务已启动。仅在此之后发送[续传指令](#2-续传指令-continue-task-instruction)或[结束指令](#3-结束指令-finish-task-instruction)。
   - **result-generated**： 发送[续传指令](#2-续传指令-continue-task-instruction)或[结束指令](#3-结束指令-finish-task-instruction)后持续返回。
   - **task-finished**： 任务完成。关闭连接。
   - **task-failed**： 任务失败。关闭连接并检查错误。

   **二进制音频**：

   - MP3/Opus 流式播放：使用流式播放器（FFmpeg、PyAudio、AudioFormat、MediaSource）。不要逐帧播放。
   - 保存完整音频：以追加模式将帧写入同一个文件。
   - WAV/MP3：仅首帧包含头部信息，后续帧仅有音频数据。

3. **发送指令**： 从独立线程向服务器发送指令。

4. **关闭连接**： 完成、出错或收到[任务已完成事件](#3-任务已完成事件-task-finished)/[任务失败事件](#4-任务失败事件-task-failed)后关闭。

<Tabs>
  <Tab title="Go">
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
      wsURL      = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/"
      outputFile = "output.mp3"
    )

    func main() {
      // 如果未设置环境变量，替换下一行为: apiKey := "YOUR_API_KEY"
      apiKey := os.Getenv("DASHSCOPE_API_KEY")

      // 清空输出文件
      os.Remove(outputFile)
      os.Create(outputFile)

      // 连接 WebSocket
      header := make(http.Header)
      header.Add("X-DashScope-DataInspection", "enable")
      header.Add("Authorization", fmt.Sprintf("bearer %s", apiKey))

      conn, resp, err := websocket.DefaultDialer.Dial(wsURL, header)
      if err != nil {
        if resp != nil {
          fmt.Printf("Connection failed HTTP status code: %d\n", resp.StatusCode)
        }
        fmt.Println("Connection failed:", err)
        return
      }
      defer conn.Close()

      // 生成任务 ID
      taskID := uuid.New().String()
      fmt.Printf("Generated task ID: %s\n", taskID)

      // 发送启动指令
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
            // 如果 enable_ssml 为 true，仅允许发送一条续传指令。否则会返回"Text request limit violated, expected 1."
            "enable_ssml": false,
          },
          "input": map[string]interface{}{},
        },
      }

      runTaskJSON, _ := json.Marshal(runTaskCmd)
      fmt.Printf("Sent run-task instruction: %s\n", string(runTaskJSON))

      err = conn.WriteMessage(websocket.TextMessage, runTaskJSON)
      if err != nil {
        fmt.Println("Failed to send run-task:", err)
        return
      }

      textSent := false

      // 处理消息
      for {
        messageType, message, err := conn.ReadMessage()
        if err != nil {
          fmt.Println("Failed to read message:", err)
          break
        }

        // 处理二进制消息
        if messageType == websocket.BinaryMessage {
          fmt.Printf("Received binary message, length: %d\n", len(message))
          file, _ := os.OpenFile(outputFile, os.O_APPEND|os.O_WRONLY|os.O_CREATE, 0644)
          file.Write(message)
          file.Close()
          continue
        }

        // 处理文本消息
        messageStr := string(message)
        fmt.Printf("Received text message: %s\n", strings.ReplaceAll(messageStr, "\n", ""))

        // 简易 JSON解析获取事件类型
        var msgMap map[string]interface{}
        if json.Unmarshal(message, &msgMap) == nil {
          if header, ok := msgMap["header"].(map[string]interface{}); ok {
            if event, ok := header["event"].(string); ok {
              fmt.Printf("Event type: %s\n", event)

              switch event {
              case "task-started":
                fmt.Println("=== Received task-started event ===")

                if !textSent {
                  // 发送续传指令

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
                    fmt.Printf("Sent continue-task instruction: %s\n", string(continueTaskJSON))

                    err = conn.WriteMessage(websocket.TextMessage, continueTaskJSON)
                    if err != nil {
                      fmt.Println("Failed to send continue-task:", err)
                      return
                    }
                  }

                  textSent = true

                  // 发送结束指令前延迟
                  time.Sleep(500 * time.Millisecond)

                  // 发送结束指令
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
                  fmt.Printf("Sent finish-task instruction: %s\n", string(finishTaskJSON))

                  err = conn.WriteMessage(websocket.TextMessage, finishTaskJSON)
                  if err != nil {
                    fmt.Println("Failed to send finish-task:", err)
                    return
                  }
                }

              case "task-finished":
                fmt.Println("=== Task completed ===")
                return

              case "task-failed":
                fmt.Println("=== Task failed ===")
                if header["error_message"] != nil {
                  fmt.Printf("Error message: %s\n", header["error_message"])
                }
                return

              case "result-generated":
                fmt.Println("Received result-generated event")
              }
            }
          }
        }
      }
    }

    ```
  </Tab>

  <Tab title="C#">
    ```csharp
    using System.Net.WebSockets;
    using System.Text;
    using System.Text.Json;

    class Program {
      // 如果未设置环境变量，替换下一行为: private static readonly string ApiKey = "REDACTED"
      private static readonly string ApiKey = Environment.GetEnvironmentVariable("DASHSCOPE_API_KEY") ?? throw new InvalidOperationException("DASHSCOPE_API_KEY environment variable is not set.");

      private const string WebSocketUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/";
      // 输出文件路径
      private const string OutputFilePath = "output.mp3";

      // WebSocket 客户端
      private static ClientWebSocket _webSocket = new ClientWebSocket();
      // 取消令牌源
      private static CancellationTokenSource _cancellationTokenSource = new CancellationTokenSource();
      // 任务 ID
      private static string? _taskId;
      // 任务已启动标志
      private static TaskCompletionSource<bool> _taskStartedTcs = new TaskCompletionSource<bool>();

      static async Task Main(string[] args) {
        try {
          // 清空输出文件
          ClearOutputFile(OutputFilePath);

          // 连接 WebSocket 服务
          await ConnectToWebSocketAsync(WebSocketUrl);

          // 开始接收消息
          Task receiveTask = ReceiveMessagesAsync();

          // 发送启动指令
          _taskId = GenerateTaskId();
          await SendRunTaskCommandAsync(_taskId);

          // 等待任务已启动事件
          await _taskStartedTcs.Task;

          // 发送续传指令
          string[] texts = {
            "床前明月光",
            "疑是地上霜",
            "举头望明月",
            "低头思故乡"
          };
          foreach (string text in texts) {
            await SendContinueTaskCommandAsync(text);
          }

          // 发送结束指令
          await SendFinishTaskCommandAsync(_taskId);

          // 等待接收任务完成
          await receiveTask;

          Console.WriteLine("Task completed. Connection closed.");
        } catch (OperationCanceledException) {
          Console.WriteLine("Task canceled.");
        } catch (Exception ex) {
          Console.WriteLine($"Error: {ex.Message}");
        } finally {
          _cancellationTokenSource.Cancel();
          _webSocket.Dispose();
        }
      }

      private static void ClearOutputFile(string filePath) {
        if (File.Exists(filePath)) {
          File.WriteAllText(filePath, string.Empty);
          Console.WriteLine("Output file cleared.");
        } else {
          Console.WriteLine("Output file does not exist. No action needed.");
        }
      }

      private static async Task ConnectToWebSocketAsync(string url) {
        var uri = new Uri(url);
        if (_webSocket.State == WebSocketState.Connecting || _webSocket.State == WebSocketState.Open) {
          return;
        }

        // 设置 WebSocket 请求头
        _webSocket.Options.SetRequestHeader("Authorization", $"bearer {ApiKey}");
        _webSocket.Options.SetRequestHeader("X-DashScope-DataInspection", "enable");

        try {
          await _webSocket.ConnectAsync(uri, _cancellationTokenSource.Token);
          Console.WriteLine("Successfully connected to WebSocket service.");
        } catch (OperationCanceledException) {
          Console.WriteLine("WebSocket connection canceled.");
        } catch (Exception ex) {
          Console.WriteLine($"WebSocket connection failed: {ex.Message}");
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
            // 如果 enable_ssml 为 true，仅允许发送一条续传指令。否则会返回"Text request limit violated, expected 1."
            enable_ssml = false
          },
          input = new { }
        });

        await SendJsonMessageAsync(command);
        Console.WriteLine("Sent run-task instruction.");
      }

      private static async Task SendContinueTaskCommandAsync(string text) {
        if (_taskId == null) {
          throw new InvalidOperationException("Task ID not initialized.");
        }

        var command = CreateCommand("continue-task", _taskId, "duplex", new {
          input = new {
            text
          }
        });

        await SendJsonMessageAsync(command);
        Console.WriteLine("Sent continue-task instruction.");
      }

      private static async Task SendFinishTaskCommandAsync(string taskId) {
        var command = CreateCommand("finish-task", taskId, "duplex", new {
          input = new { }
        });

        await SendJsonMessageAsync(command);
        Console.WriteLine("Sent finish-task instruction.");
      }

      private static async Task SendJsonMessageAsync(string message) {
        var buffer = Encoding.UTF8.GetBytes(message);
        try {
          await _webSocket.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, _cancellationTokenSource.Token);
        } catch (OperationCanceledException) {
          Console.WriteLine("Message send canceled.");
        }
      }

      private static async Task ReceiveMessagesAsync() {
        while (_webSocket.State == WebSocketState.Open) {
          var response = await ReceiveMessageAsync();
          if (response != null) {
            var eventStr = response.RootElement.GetProperty("header").GetProperty("event").GetString();
            switch (eventStr) {
              case "task-started":
                Console.WriteLine("Task started.");
                _taskStartedTcs.TrySetResult(true);
                break;
              case "task-finished":
                Console.WriteLine("Task completed.");
                _cancellationTokenSource.Cancel();
                break;
              case "task-failed":
                Console.WriteLine("Task failed: " + response.RootElement.GetProperty("header").GetProperty("error_message").GetString());
                _cancellationTokenSource.Cancel();
                break;
              default:
                // 在此处理 result-generated
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
            Console.WriteLine("Received binary data...");

            // 保存二进制数据到文件
            using (var fileStream = new FileStream(OutputFilePath, FileMode.Append)) {
              fileStream.Write(buffer, 0, result.Count);
            }

            return null;
          }

          string message = Encoding.UTF8.GetString(buffer, 0, result.Count);
          return JsonDocument.Parse(message);
        } catch (OperationCanceledException) {
          Console.WriteLine("Message receive canceled.");
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
  </Tab>

  <Tab title="PHP">
    **composer.json**：

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

    **代码**：

    ```php
    <?php

    require __DIR__ . '/vendor/autoload.php';

    use Ratchet\Client\Connector;
    use React\EventLoop\Loop;
    use React\Socket\Connector as SocketConnector;

    // 如果未设置环境变量，替换下一行为: $api_key = "REDACTED"
    $api_key = getenv("DASHSCOPE_API_KEY");
    $websocket_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference/'; // WebSocket 服务器地址
    $output_file = 'output.mp3'; // 输出文件路径

    $loop = Loop::get();

    if (file_exists($output_file)) {
        // 清空文件内容
        file_put_contents($output_file, '');
    }

    // 创建自定义连接器
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
        echo "Connected to WebSocket server\n";

        // 生成任务 ID
        $taskId = generateTaskId();

        // 发送启动指令
        sendRunTaskMessage($conn, $taskId);

        // 定义发送续传指令的函数
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
            echo "Preparing to send continue-task instruction: " . $continueTaskMessage . "\n";
            $conn->send($continueTaskMessage);
            $continueTaskCount++;
          }
          echo "Number of continue-task instructions sent: " . $continueTaskCount . "\n";

          // 发送结束指令
          sendFinishTaskMessage($conn, $taskId);
        };

        // 任务已启动事件标志
        $taskStarted = false;

        // 监听消息
        $conn->on('message', function($msg) use ($conn, $sendContinueTask, $loop, &$taskStarted, $taskId, $output_file) {
          if ($msg->isBinary()) {
            // 将二进制数据写入本地文件
            file_put_contents($output_file, $msg->getPayload(), FILE_APPEND);
          } else {
            // 处理非二进制消息
            $response = json_decode($msg, true);

            if (isset($response['header']['event'])) {
              handleEvent($conn, $response, $sendContinueTask, $loop, $taskId, $taskStarted);
            } else {
              echo "Unknown message format\n";
            }
          }
        });

        // 监听连接关闭
        $conn->on('close', function($code = null, $reason = null) {
          echo "Connection closed\n";
          if ($code !== null) {
            echo "Close code: " . $code . "\n";
          }
          if ($reason !== null) {
            echo "Close reason: " . $reason . "\n";
          }
        });
    }, function ($e) {
        echo "Cannot connect: {$e->getMessage()}\n";
    });

    $loop->run();

    /**
      * 生成任务 ID
      * @return string
      */
    function generateTaskId(): string {
        return bin2hex(random_bytes(16));
    }

    /**
      * 发送启动指令
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
              // 如果 enable_ssml 为 true，仅允许发送一条续传指令。否则会返回"Text request limit violated, expected 1."
              "enable_ssml" => false
            ],
            "input" => (object) []
          ]
        ]);
        echo "Preparing to send run-task instruction: " . $runTaskMessage . "\n";
        $conn->send($runTaskMessage);
        echo "run-task instruction sent\n";
    }

    /**
      * 读取音频文件
      * @param string $filePath
      * @return bool|string
      */
    function readAudioFile(string $filePath) {
        $voiceData = file_get_contents($filePath);
        if ($voiceData === false) {
          echo "Cannot read audio file\n";
        }
        return $voiceData;
    }

    /**
      * 拆分音频数据
      * @param string $data
      * @param int $chunkSize
      * @return array
      */
    function splitAudioData(string $data, int $chunkSize): array {
        return str_split($data, $chunkSize);
    }

    /**
      * 发送结束指令
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
        echo "Preparing to send finish-task instruction: " . $finishTaskMessage . "\n";
        $conn->send($finishTaskMessage);
        echo "finish-task instruction sent\n";
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
            echo "Task started. Sending continue-task instructions...\n";
            $taskStarted = true;
            // 发送续传指令
            $sendContinueTask();
            break;
          case 'result-generated':
            // 收到 result-generated 事件
            break;
          case 'task-finished':
            echo "Task completed\n";
            $conn->close();
            break;
          case 'task-failed':
            echo "Task failed\n";
            echo "Error code: " . $response['header']['error_code'] . "\n";
            echo "Error message: " . $response['header']['error_message'] . "\n";
            $conn->close();
            break;
          case 'error':
            echo "Error: " . $response['payload']['message'] . "\n";
            break;
          default:
            echo "Unknown event: " . $response['header']['event'] . "\n";
            break;
        }

        // 任务完成后关闭连接
        if ($response['header']['event'] == 'task-finished') {
          // 等待 1 秒确保所有数据传输完成
          $loop->addTimer(1, function() use ($conn) {
            $conn->close();
            echo "Client closed connection\n";
          });
        }

        // 未收到任务已启动事件时关闭连接
        if (!$taskStarted && in_array($response['header']['event'], ['task-failed', 'error'])) {
          $conn->close();
        }
    }
    ```
  </Tab>

  <Tab title="Node.js">
    安装依赖：

    ```sh
    npm install ws
    npm install uuid
    ```

    ```javascript
    const WebSocket = require('ws');
    const fs = require('fs');
    const uuid = require('uuid').v4;

    // 如果未设置环境变量，替换下一行为: const apiKey = "REDACTED"
    const apiKey = process.env.DASHSCOPE_API_KEY;
    const url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference/';
    // 输出文件路径
    const outputFilePath = 'output.mp3';

    // 清空输出文件
    fs.writeFileSync(outputFilePath, '');

    // 创建 WebSocket 客户端
    const ws = new WebSocket(url, {
      headers: {
      Authorization: `bearer ${apiKey}`,
      'X-DashScope-DataInspection': 'enable'
      }
    });

    let taskStarted = false;
    let taskId = uuid();

    ws.on('open', () => {
      console.log('Connected to WebSocket server');

      // 发送启动指令
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
        enable_ssml: false // 启用 SSML。如果为 true，仅允许发送一条续传指令。否则会返回"Text request limit violated, expected 1."
          },
          input: {}
      }
      });
      ws.send(runTaskMessage);
      console.log('Sent run-task message');
    });

    const fileStream = fs.createWriteStream(outputFilePath, { flags: 'a' });
    ws.on('message', (data, isBinary) => {
      if (isBinary) {
      // 将二进制数据写入文件
      fileStream.write(data);
      } else {
      const message = JSON.parse(data);

      switch (message.header.event) {
          case 'task-started':
        taskStarted = true;
        console.log('Task started');
        // 发送续传指令
        sendContinueTasks(ws);
        break;
          case 'task-finished':
        console.log('Task completed');
        ws.close();
        fileStream.end(() => {
          console.log('File stream closed');
        });
        break;
          case 'task-failed':
        console.error('Task failed: ', message.header.error_message);
        ws.close();
        fileStream.end(() => {
          console.log('File stream closed');
        });
        break;
          default:
        // 在此处理 result-generated
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
        console.log(`Sent continue-task, text: ${text}`);
          }
      }, index * 1000); // 每秒发送一次
      });

      // 发送结束指令
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
          console.log('Sent finish-task');
      }
      }, texts.length * 1000 + 1000); // 最后一条续传指令后 1 秒发送
    }

    ws.on('close', () => {
      console.log('Disconnected from WebSocket server');
    });
    ```
  </Tab>

  <Tab title="Java">
    **pom.xml**：

    ```xml
    <dependencies>
      <!-- WebSocket 客户端 -->
      <dependency>
        <groupId>org.java-websocket</groupId>
        <artifactId>Java-WebSocket</artifactId>
        <version>1.5.3</version>
      </dependency>

      <!-- JSON 处理 -->
      <dependency>
        <groupId>com.fasterxml.jackson.core</groupId>
        <artifactId>jackson-databind</artifactId>
        <version>2.13.0</version>
      </dependency>
    </dependencies>
    ```

    **build.gradle**：

    ```gradle
    // 省略其他代码
    dependencies {
      // WebSocket 客户端
      implementation 'org.java-websocket:Java-WebSocket:1.5.3'
      // JSON 处理
      implementation 'com.fasterxml.jackson.core:jackson-databind:2.13.0'
    }
    // 省略其他代码
    ```

    **代码**：

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
        System.out.println("Connection successful");

        // 发送启动指令
        // 如果 enable_ssml 为 true，仅允许发送一条续传指令。否则会返回"Text request limit violated, expected 1."
        String runTaskCommand = "{ \"header\": { \"action\": \"run-task\", \"task_id\": \"" + taskId + "\", \"streaming\": \"duplex\" }, \"payload\": { \"task_group\": \"audio\", \"task\": \"tts\", \"function\": \"SpeechSynthesizer\", \"model\": \"cosyvoice-v3-flash\", \"parameters\": { \"text_type\": \"PlainText\", \"voice\": \"longanyang\", \"format\": \"mp3\", \"sample_rate\": 22050, \"volume\": 50, \"rate\": 1, \"pitch\": 1, \"enable_ssml\": false }, \"input\": {} }}";
        send(runTaskCommand);
      }

      @Override
      public void onMessage(String message) {
        System.out.println("Received server message: " + message);
        try {
          // 解析 JSON 消息
          Map<String, Object> messageMap = new ObjectMapper().readValue(message, Map.class);

          if (messageMap.containsKey("header")) {
            Map<String, Object> header = (Map<String, Object>) messageMap.get("header");

            if (header.containsKey("event")) {
              String event = (String) header.get("event");

              if ("task-started".equals(event)) {
                System.out.println("Received task-started event");

                List<String> texts = Arrays.asList(
                    "床前明月光，疑是地上霜",
                    "举头望明月，低头思故乡"
                );

                for (String text : texts) {
                  // 发送续传指令
                  sendContinueTask(text);
                }

                // 发送结束指令
                sendFinishTask();
              } else if ("task-finished".equals(event)) {
                System.out.println("Received task-finished event");
                taskFinished = true;
                closeConnection();
              } else if ("task-failed".equals(event)) {
                System.out.println("Task failed: " + message);
                closeConnection();
              }
            }
          }
        } catch (Exception e) {
          System.err.println("Exception occurred: " + e.getMessage());
        }
      }

      @Override
      public void onMessage(ByteBuffer message) {
        System.out.println("Received binary audio data size: " + message.remaining());

        try (FileOutputStream fos = new FileOutputStream(outputFile, true)) {
          byte[] buffer = new byte[message.remaining()];
          message.get(buffer);
          fos.write(buffer);
          System.out.println("Audio data written to local file " + outputFile);
        } catch (IOException e) {
          System.err.println("Failed to write audio data to local file: " + e.getMessage());
        }
      }

      @Override
      public void onClose(int code, String reason, boolean remote) {
        System.out.println("Connection closed: " + reason + " (" + code + ")");
      }

      @Override
      public void onError(Exception ex) {
        System.err.println("Error: " + ex.getMessage());
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
          // 如果未设置环境变量，替换下一行为: String apiKey = "REDACTED"
          String apiKey = System.getenv("DASHSCOPE_API_KEY");
          if (apiKey == null || apiKey.isEmpty()) {
            System.err.println("Set DASHSCOPE_API_KEY environment variable");
            return;
          }

          Map<String, String> headers = new HashMap<>();
          headers.put("Authorization", "bearer " + apiKey);
          TTSWebSocketClient client = new TTSWebSocketClient(new URI("wss://dashscope.aliyuncs.com/api-ws/v1/inference/"), headers);

          client.connect();

          while (!client.isClosed() && !client.taskFinished) {
            Thread.sleep(1000);
          }
        } catch (Exception e) {
          System.err.println("Failed to connect to WebSocket service: " + e.getMessage());
          e.printStackTrace();
        }
      }
    }
    ```
  </Tab>

  <Tab title="Python">
    安装依赖：

    ```bash
    pip uninstall websocket-client
    pip uninstall websocket
    pip install websocket-client
    ```

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
        api_key (str): 用于认证的 API Key
        uri (str): WebSocket 服务地址
      """
        self.api_key = api_key  # 替换为你的 API Key
        self.uri = uri  # 替换为你的 WebSocket 地址
        self.task_id = str(uuid.uuid4())  # 生成唯一的任务 ID
        self.output_file = f"output_{int(time.time())}.mp3"  # 输出音频文件路径
        self.ws = None  # WebSocketApp 实例
        self.task_started = False  # 是否已收到任务已启动事件
        self.task_finished = False  # 是否已收到任务已完成或任务失败事件

      def on_open(self, ws):
        """
      连接建立时的回调
      发送启动指令开始语音合成
      """
        print("WebSocket connected")

        # 构建启动指令
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
              # 如果 enable_ssml 为 True，仅允许发送一条续传指令。否则会返回"Text request limit violated, expected 1."
              "enable_ssml": False
            },
            "input": {}
          }
        }

        # 发送启动指令
        ws.send(json.dumps(run_task_cmd))
        print("Sent run-task instruction")

      def on_message(self, ws, message):
        """
      收到消息时的回调
      分别处理文本和二进制消息
      """
        if isinstance(message, str):
          # 处理 JSON 文本消息
          try:
            msg_json = json.loads(message)
            print(f"Received JSON message: {msg_json}")

            if "header" in msg_json:
              header = msg_json["header"]

              if "event" in header:
                event = header["event"]

                if event == "task-started":
                  print("Task started")
                  self.task_started = True

                  # 发送续传指令
                  texts = [
                    "床前明月光，疑是地上霜",
                    "举头望明月，低头思故乡"
                  ]

                  for text in texts:
                    self.send_continue_task(text)

                  # 所有续传指令后发送结束指令
                  self.send_finish_task()

                elif event == "task-finished":
                  print("Task completed")
                  self.task_finished = True
                  self.close(ws)

                elif event == "task-failed":
                  error_msg = msg_json.get("error_message", "Unknown error")
                  print(f"Task failed: {error_msg}")
                  self.task_finished = True
                  self.close(ws)

          except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {e}")
        else:
          # 处理二进制消息（音频数据）
          print(f"Received binary message, size: {len(message)} bytes")
          with open(self.output_file, "ab") as f:
            f.write(message)
          print(f"Audio data written to local file {self.output_file}")

      def on_error(self, ws, error):
        """发生错误时的回调"""
        print(f"WebSocket error: {error}")

      def on_close(self, ws, close_status_code, close_msg):
        """连接关闭时的回调"""
        print(f"WebSocket closed: {close_msg} ({close_status_code})")

      def send_continue_task(self, text):
        """发送续传指令，包含待合成的文本"""
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
        print(f"Sent continue-task instruction, text: {text}")

      def send_finish_task(self):
        """发送结束指令，结束语音合成"""
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
        print("Sent finish-task instruction")

      def close(self, ws):
        """手动关闭连接"""
        if ws and ws.sock and ws.sock.connected:
          ws.close()
          print("Manually closed connection")

      def run(self):
        """启动 WebSocket 客户端"""
        # 设置请求头（认证）
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

        print("Listening for WebSocket messages...")
        self.ws.run_forever()  # 启动持久连接

    # 使用示例
    if __name__ == "__main__":
      # 如果未设置环境变量，替换下一行为: API_KEY = "REDACTED"
      API_KEY = os.environ.get("DASHSCOPE_API_KEY")
      SERVER_URI = "wss://dashscope.aliyuncs.com/api-ws/v1/inference/"  # 替换为你的 WebSocket 地址

      client = TTSClient(API_KEY, SERVER_URI)
      client.run()
    ```
  </Tab>
</Tabs>
