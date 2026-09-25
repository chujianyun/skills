> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 音视频文件理解

> 文本+图像/音频输入

## 快速开始

**前提条件**

- [获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。
- Qwen-Omni 仅支持 OpenAI 兼容方式调用。[安装 SDK](/api-reference/preparation/install-sdk)。OpenAI Python SDK 版本要求 1.52.0+，Node.js SDK 版本要求 4.68.0+。

本示例向 Qwen-Omni API 发送文本提示词，返回包含文本和音频的流式响应。

<CodeGroup>
  ```python Python
  import os
  import base64
  import soundfile as sf
  import numpy as np
  from openai import OpenAI

  # 1. 初始化客户端
  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 确保环境变量已配置
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  # 2. 发起请求
  try:
    completion = client.chat.completions.create(
      model="qwen3.5-omni-plus",
      messages=[{"role": "user", "content": "你是谁？"}],
      modalities=["text", "audio"],  # 指定文本和音频输出
      audio={"voice": "Tina", "format": "wav"},
      stream=True,  # 必须设为 True
      stream_options={"include_usage": True},
    )

    # 3. 处理流式响应并解码音频
    print("模型回复：")
    audio_base64_string = ""
    for chunk in completion:
      # 处理文本部分
      if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")

      # 收集音频部分
      if chunk.choices and hasattr(chunk.choices[0].delta, "audio") and chunk.choices[0].delta.audio:
        audio_base64_string += chunk.choices[0].delta.audio.get("data", "")

    # 4. 保存音频文件
    if audio_base64_string:
      wav_bytes = base64.b64decode(audio_base64_string)
      audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
      sf.write("audio_assistant.wav", audio_np, samplerate=24000)
      print("\n音频文件已保存至: audio_assistant.wav")

  except Exception as e:
    print(f"请求失败: {e}")
  ```

  ```javascript Node.js
  // 运行前准备：
  // Windows/Mac/Linux 通用：
  // 1. 确保已安装 Node.js（建议版本 >= 14）
  // 2. 执行以下命令安装必要依赖：
  //    npm install openai wav

  import OpenAI from "openai";
  import { createWriteStream } from 'node:fs';
  import { Writer } from 'wav';

  // 定义音频转换函数：将 Base64 字符串转换并保存为标准 WAV 音频文件
  async function convertAudio(audioString, audioPath) {
    try {
      // 将 Base64 字符串解码为 Buffer
      const wavBuffer = Buffer.from(audioString, 'base64');
      // 创建 WAV 文件写入流
      const writer = new Writer({
        sampleRate: 24000,  // 采样率
        channels: 1,        // 单声道
        bitDepth: 16        // 16 位深度
      });
      // 创建输出文件流并建立管道连接
      const outputStream = createWriteStream(audioPath);
      writer.pipe(outputStream);

      // 写入 PCM 数据并结束写入
      writer.write(wavBuffer);
      writer.end();

      // 使用 Promise 等待文件写入完成
      await new Promise((resolve, reject) => {
        outputStream.on('finish', resolve);
        outputStream.on('error', reject);
      });

      // 添加额外等待时间以确保音频完整性
      await new Promise(resolve => setTimeout(resolve, 800));

      console.log(`\n音频文件已成功保存为 ${audioPath}`);
    } catch (error) {
      console.error('处理过程中发生错误:', error);
    }
  }

  //  1. 初始化客户端
  const openai = new OpenAI(
    {
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
  );
  // 2. 发起请求
  const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",
    messages: [
      {
        "role": "user",
        "content": "你是谁？"
      }],
    stream: true,
    stream_options: {
      include_usage: true
    },
    modalities: ["text", "audio"],
    audio: { voice: "Tina", format: "wav" }
  });

  let audioString = "";
  console.log("模型回复：")

  // 3. 处理流式响应并解码音频
  for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
      // 处理文本内容
      if (chunk.choices[0].delta.content) {
        process.stdout.write(chunk.choices[0].delta.content);
      }
      // 处理音频内容
      if (chunk.choices[0].delta.audio) {
        if (chunk.choices[0].delta.audio["data"]) {
          audioString += chunk.choices[0].delta.audio["data"];
        }
      }
    }
  }
  // 4. 保存音频文件
  convertAudio(audioString, "audio_assistant.wav");
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-omni-plus",
    "messages": [
      {
        "role": "user",
        "content": "你是谁？"
      }
    ],
    "stream":true,
    "stream_options":{
      "include_usage":true
    },
    "modalities":["text","audio"],
    "audio":{"voice":"Tina","format":"wav"}
  }'
  ```
</CodeGroup>

<Accordion title="响应示例">
  运行 `Python` 或 `Node.js` 代码后，将返回文本响应，并在代码文件所在目录下保存一个名为 `audio_assistant.wav` 的音频文件。

  ```json
  模型回复：
  I am a large language model developed by Alibaba Cloud. My name is Qwen. How can I help you?
  ```

  运行 `HTTP` 代码会直接在 `audio` 字段中返回文本和 Base64 编码的音频数据。

  ```json
  data: {"choices":[{"delta":{"content":"I"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1757647879,"system_fingerprint":null,"model":"qwen3.5-omni-plus","id":"chatcmpl-a68eca3b-c67e-4666-a72f-73c0b4919860"}
  data: {"choices":[{"delta":{"content":" am"},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1757647879,"system_fingerprint":null,"model":"qwen3.5-omni-plus","id":"chatcmpl-a68eca3b-c67e-4666-a72f-73c0b4919860"}
  ......
  data: {"choices":[{"delta":{"audio":{"data":"/v8AAAAAAAAAAAAAAA...","expires_at":1757647879,"id":"audio_a68eca3b-c67e-4666-a72f-73c0b4919860"}},"finish_reason":null,"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1757647879,"system_fingerprint":null,"model":"qwen3.5-omni-plus","id":"chatcmpl-a68eca3b-c67e-4666-a72f-73c0b4919860"}
  data: {"choices":[{"finish_reason":"stop","delta":{"content":""},"index":0,"logprobs":null}],"object":"chat.completion.chunk","usage":null,"created":1764763585,"system_fingerprint":null,"model":"qwen3.5-omni-plus","id":"chatcmpl-e8c82e9e-073e-4289-a786-a20eb444ac9c"}
  data: {"choices":[],"object":"chat.completion.chunk","usage":{"prompt_tokens":207,"completion_tokens":103,"total_tokens":310,"completion_tokens_details":{"audio_tokens":83,"text_tokens":20},"prompt_tokens_details":{"text_tokens":207}},"created":1757940330,"system_fingerprint":null,"model":"qwen3.5-omni-plus","id":"chatcmpl-9cdd5a26-f9e9-4eff-9dcc-93a878165afc"}
  ```
</Accordion>

<a id="supported-languages" />

## 支持的语言

<Accordion title="Qwen3.5-Omni 支持的语言">
  **输入语言（74 种）**： 中文、英语、德语、法语、意大利语、捷克语、印尼语、泰语、韩语、波兰语、日语、越南语、芬兰语、葡萄牙语、西班牙语、荷兰语、俄语、马来语、加泰罗尼亚语、瑞典语、土耳其语、乌克兰语、罗马尼亚语、斯洛伐克语、丹麦语、冰岛语、挪威语（博克马尔）、马其顿语、希腊语、匈牙利语、加利西亚语、菲律宾语、克罗地亚语、波斯尼亚语、斯洛文尼亚语、保加利亚语、哈萨克语、白俄罗斯语、拉脱维亚语、爱沙尼亚语、阿塞拜疆语、维吾尔语、斯瓦希里语、印地语、世界语、柯尔克孜语、塔吉克语、宿务语、南非语、阿拉伯语、立陶宛语、爪哇语、孟加拉语、波斯语、希伯来语、旁遮普语、古吉拉特语、蒙古语、阿斯图里亚斯语、卡纳达语、马拉地语、国际语、马拉雅拉姆语、马耳他语、新挪威语、泰卢固语、乌尔都语、格鲁吉亚语、巴斯克语、泰米尔语、奥里亚语、塞尔维亚语、毛利语

  **输入方言（39 种）**： 东北话、贵州话、粤语、河南话、香港粤语、上海话、陕西话、天津话、台湾话、云南话、安徽话、福建话、甘肃话、广东话、湖北话、湖南话、江西话、山东话、山西话、四川话、广西话、海南话、重庆话、长沙话、杭州话、合肥话、银川话、郑州话、沈阳话、温州话、武汉话、昆明话、太原话、南昌话、济南话、兰州话、南京话、客家话、闽南语

  **输出语言（29 种）**： 中文、英语、德语、意大利语、葡萄牙语、西班牙语、日语、韩语、法语、俄语、泰语、印度尼西亚语、阿拉伯语、越南语、土耳其语、芬兰语、波兰语、印地语、荷兰语、捷克语、乌尔都语、他加禄语、瑞典语、丹麦语、希伯来语、冰岛语、马来语、挪威语、波斯语

  **输出方言（7 种）**： 四川话、北京话、天津话、南京话、陕西话、粤语、闽南语
</Accordion>

<Accordion title="Qwen3-Omni-Flash 支持的语言">
  **输入/输出语言（11 种）**： 中文、英语、德语、法语、意大利语、泰语、韩语、日语、俄语、西班牙语、葡萄牙语

  **输入/输出方言（8 种）**： 四川话、上海话、粤语、闽南语、陕西话、南京话、天津话、北京话
</Accordion>

关于模型名称、上下文长度、定价和快照版本，请参阅[模型列表](/developer-guides/getting-started/model-selection)。关于并发请求限制，请参阅[限流](/developer-guides/administration/rate-limits)。

## 模型效果

### 音视频内容分析

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingRight: "12px", paddingBottom: "8px"}}>输入</th>
    <th style={{textAlign: "left", paddingLeft: "12px", paddingBottom: "8px"}}>输出</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <video src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260323/bjdunv/wan-t2v-demo.mp4" controls style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      对这个视频生成一段全面的、带时间戳的描述。
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      **00:00.000 - 00:02.500** A rain-soaked city street fills the widescreen frame. Long-exposure photography creates streaks of red and blue car lights on wet pavement. A solitary man in a dark knee-length trench coat and light shirt with a tie walks toward the camera along the right sidewalk.

      **00:12.300 - 00:14.533** The camera tilts down. Inside a flashlight beam, a yellowed, aged single sheet lies in a shallow puddle, edges charred and corners curled. The man kneels, extending gloved fingers toward the document; ripples spread outward as his hand nears.

      *仅展示部分时间戳。*
    </td>
  </tr>
</table>

### 多方言理解

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingRight: "12px", paddingBottom: "8px"}}>输入</th>
    <th style={{textAlign: "left", paddingLeft: "12px", paddingBottom: "8px"}}>输出</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <video src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/cnzfqz/%E9%9F%B3%E9%A2%91%E7%90%86%E8%A7%A3-%E5%A4%9A%E8%AF%AD%E8%A8%80_compressed.mp4" controls style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      描述不同中国方言歌手的音色特征、情感状态和完整歌词。
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      This audio features rap performances by singers from various regions of China. **Hangzhou dialect (Wu)** -- The male singer's voice is soft and gentle, with the distinctive smoothness and warmth of Wu dialect. His intonation rises and falls gently, and his rhythm is light and quick, creating a relaxed storytelling effect. **Emotional state:** Relaxed, comfortable, and full of everyday life. He describes Hangzhou's slow-paced lifestyle and urban changes, expressing affection for his hometown.

      *仅展示部分结果。*
    </td>
  </tr>
</table>

### 歌词字幕生成

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingRight: "12px", paddingBottom: "8px"}}>输入</th>
    <th style={{textAlign: "left", paddingLeft: "12px", paddingBottom: "8px"}}>输出</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <video src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/xysfyy/%E9%9F%B3%E9%A2%91%E7%90%86%E8%A7%A3-%E6%AD%8C%E8%AF%8D%E5%88%86%E6%9E%90_compressed.mp4" controls style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      转录歌曲歌词并为每一行提供时间戳。
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      \[00:00:12,680 --> 00:00:16,960] Cat thread sways past moonlight on trees. \[00:00:18,400 --> 00:00:22,800] Radiators hum 1998 chart hits. \[00:00:24,160 --> 00:00:28,080] Time parts the mist-like heat waves. \[00:00:28,920 --> 00:00:33,000] Neon from the screen shines on my nose bridge. ... \[00:04:09,000 --> 00:04:10,020] (End)

      *仅展示部分结果。*
    </td>
  </tr>
</table>

### 音视频编程

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingRight: "12px", paddingBottom: "8px"}}>Demo 1</th>
    <th style={{textAlign: "left", paddingLeft: "12px", paddingBottom: "8px"}}>Demo 2</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <video src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/gjyydn/%E9%9F%B3%E8%A7%86%E9%A2%91%E7%BC%96%E7%A8%8B-01.mp4" controls style={{display: "block", width: "100%"}} />
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      <video src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260330/fyybth/%E9%9F%B3%E8%A7%86%E9%A2%91%E7%BC%96%E7%A8%8B-02.mp4" controls style={{display: "block", width: "100%"}} />
    </td>
  </tr>
</table>

## 使用方法

### 流式输出

Qwen-Omni 的所有请求必须设置 `stream=True`。

### 模型配置

根据您的使用场景配置参数、提示词和音视频长度，以平衡成本、速度和质量。

<Tabs>
  <Tab title="音视频理解">
| 使用场景          | 建议视频长度 | 建议提示词        | 建议 max\_pixels 值    |
| ------------- | ------ | ------------ | ------------------- |
| 快速浏览，低成本      | ≤60 分钟 | 50 字以内的简单提示词 | 230,400             |
| 内容提取（长视频分段）   | ≤60 分钟 | 50 字以内的简单提示词 | 921,600 至 2,073,600 |
| 标准分析（短视频标签）   | ≤4 分钟  | 使用下方的结构化提示词  | 921,600 至 2,073,600 |
| 精细分析（多人/复杂场景） | ≤2 分钟  | 使用下方的结构化提示词  | 2,073,600           |

    <Accordion title="音视频理解的推荐结构化提示词">
      ````text
      Provide a detailed description of the video.
      It should explicitly include three sections:
      1. A structured chronological storyline of **every noticeable audio and visual details**
      2. A structured list of all visible text. For each text element, include start timestamp, end timestamp, the exact text content, the appearance characteristics. If no text appears, explicitly state so.
      3. A structured speech-to-text transcription, include speaker（Corresponding to the character or voice‑over in Section 1, including their accent and tone）, exact spoken content, start timestamp, end timestamp, and speaking state (prosody, emotion, and style). If no speech appears, explicitly state so.
      Aside from these three required sections, you are free to organize any additional content in any way you find helpful. This additional content can include global information about the entire video or localized information about specific moments. You may choose the topic of this extra content freely.
      Output Format:
      ```
      ## Storyline
      <xx:xx.xxx> - <xx:xx.xxx>
      <an unstructured long paragraph in natural language describing what happened during this period, blending both audio and video details.>
      <xx:xx.xxx> - <xx:xx.xxx>
      <an unstructured long paragraph in natural language describing what happened during this period, blending both audio and video details.>
      <xx:xx.xxx> - <xx:xx.xxx>
      <an unstructured long paragraph in natural language describing what happened during this period, blending both audio and video details.>
      ...
      ## Visible Text
      <xx:xx.xxx> - <xx:xx.xxx>
      "<element>": <appearance>
      "<element>": <appearance>
      <xx:xx.xxx> - <xx:xx.xxx>
      "<element>": <appearance>
      "<element>": <appearance>
      "<element>": <appearance>
      <xx:xx.xxx> - <xx:xx.xxx>
      "<element>": <appearance>
      ...
      ## Speakers and Transcript
      Speaker profiles:
      <speaker> - <profile>
      <speaker> - <profile>
      <speaker> - <profile>
      ...
      <xx:xx.xxx> - <xx:xx.xxx>
      Speaker: <speaker>
      State: <description>
      Content: "<content>"
      <xx:xx.xxx> - <xx:xx.xxx>
      Speaker: <speaker>
      State: <description>
      Content: "<content>"
      <xx:xx.xxx> - <xx:xx.xxx>
      Speaker: <speaker>
      State: <description>
      Content: "<content>"
      ...
      ## <another section>
      <paragraphs>
      ## <another section>
      <paragraphs>
      ...
      ```
      ````
    </Accordion>

    <Note>对长视频进行精细描述时，请先进行分段处理。</Note>
  </Tab>

  <Tab title="音频理解">
    通过控制音频长度和提示词复杂度来平衡成本和质量。

| 使用场景          | 建议音频长度 | 建议提示词        |
| ------------- | ------ | ------------ |
| 快速浏览，低成本      | ≤60 分钟 | 50 字以内的简单提示词 |
| 内容提取（长音频分段）   | ≤60 分钟 | 50 字以内的简单提示词 |
| 标准分析（音频标签）    | ≤2 分钟  | 使用下方的结构化提示词  |
| 精细分析（多人/复杂场景） | ≤1 分钟  | 使用下方的结构化提示词  |

    <Accordion title="音频理解的推荐结构化提示词">
      ````text
      Provide a detailed description of the audio.

      It should explicitly include two sections:

      1. A structured chronological storyline of **every noticeable audio details**
      2. A structured speech-to-text transcription, include speaker（Corresponding to the character or voice‑over in Section 1, including their accent and tone）, exact spoken content, start timestamp, end timestamp, and speaking state (prosody, emotion, and style). If no speech appears, explicitly state so.

      Aside from these two required components, you are free to organize any additional content in any way you find helpful. This additional content can include global information about the entire audio or localized information about specific moments. You may choose the topic of this extra content freely.

      Output Format:

      ```
      ## Storyline

      <xx:xx.xxx> - <xx:xx.xxx>
      <an unstructured long paragraph in natural language describing what happened during this period, blending both audio details.>

      <xx:xx.xxx> - <xx:xx.xxx>
      <an unstructured long paragraph in natural language describing what happened during this period, blending both audio details.>

      <xx:xx.xxx> - <xx:xx.xxx>
      <an unstructured long paragraph in natural language describing what happened during this period, blending both audio details.>

      ...

      ...

      ## Speakers and Transcript

      Speaker profiles:
      <speaker> - <profile>
      <speaker> - <profile>
      <speaker> - <profile>
      ...

      <xx:xx.xxx> - <xx:xx.xxx>
      Speaker: <speaker>
      State: <description>
      Content: "<content>"

      <xx:xx.xxx> - <xx:xx.xxx>
      Speaker: <speaker>
      State: <description>
      Content: "<content>"

      <xx:xx.xxx> - <xx:xx.xxx>
      Speaker: <speaker>
      State: <description>
      Content: "<content>"

      ...

      ## <another section>

      <paragraphs>

      ## <another section>

      <paragraphs>

      ...
      ```
      ````
    </Accordion>

    <Note>对长音频进行精细描述时，请先进行分段处理。</Note>
  </Tab>
</Tabs>

## 思考模式

<Tip>关于启用/禁用、流式输出和 `thinking_budget`，请参阅[思考](/developer-guides/text-generation/thinking)。</Tip>

Qwen3-Omni-Flash 是混合思考模型（`enable_thinking` 默认为 `false`）。Qwen-Omni-Turbo 不支持思考模式。

在思考模式下，请设置 `modalities: ["text"]` — 启用思考时不支持音频输出。

## 联网搜索

Qwen3.5-Omni 系列支持联网搜索，可获取实时信息并进行推理。通过 `enable_search` 参数启用联网搜索，并将 `search_strategy` 设置为 `agent`。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  try:
    completion = client.chat.completions.create(
      model="qwen3.5-omni-plus",
      messages=[{
        "role": "user",
        "content": "请查询今天的日期和星期几，并告诉我今天有哪些重要节日。"
      }],
      stream=True,
      stream_options={"include_usage": True},
      extra_body={
        "enable_search": True,
        "search_options": {
          "search_strategy": "agent"
        }
      }
    )

    print("模型回复（包含实时信息）：")
    for chunk in completion:
      if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
    print()

  except Exception as e:
    print(f"请求失败: {e}")
  ```

  ```javascript Node.js
  import OpenAI from "openai";

  const openai = new OpenAI({
    apiKey: process.env.DASHSCOPE_API_KEY,
    baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
  });

  const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",
    messages: [{
      "role": "user",
      "content": "请查询今天的日期和星期几，并告诉我今天有哪些重要节日。"
    }],
    stream: true,
    stream_options: {
      include_usage: true
    },
    extra_body: {
      enable_search: true,
      search_options: {
        search_strategy: "agent"
      }
    }
  });

  console.log("模型回复（包含实时信息）：");

  for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
      if (chunk.choices[0].delta.content) {
        process.stdout.write(chunk.choices[0].delta.content);
      }
    }
  }
  console.log();
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-omni-plus",
    "messages": [
      {
        "role": "user",
        "content": "请查询今天的日期和星期几，并告诉我今天有哪些重要节日。"
      }
    ],
    "stream": true,
    "stream_options": {
      "include_usage": true
    },
    "enable_search": true,
    "search_options": {
      "search_strategy": "agent"
    }
  }'
  ```
</CodeGroup>

<Note>
  - 联网搜索仅支持 **Qwen3.5-Omni** 系列。`search_strategy` 参数仅接受 `agent`。
  - 有关 `agent` 策略的计费信息，请参阅[计费](/developer-guides/getting-started/pricing)。
</Note>

## 多模态输入

### 视频和文本输入

您可以通过[图片列表](#图片列表格式)或[视频文件](#视频文件格式-可理解视频中的音频)输入视频。如果输入视频文件，模型还可以理解视频中的音频。

以下示例代码使用互联网上的视频URL。如需输入本地视频，请参阅[输入Base64编码的本地文件](#输入base64编码的本地文件)。所有调用均需使用流式输出。

#### 视频文件格式 (可理解视频中的音频)

- **文件数量**：
  - Qwen3.5-Omni 系列：使用公开URL最多512个文件；使用Base64编码最多250个文件。
  - Qwen3-Omni-Flash 和 Qwen-Omni-Turbo 系列：仅允许一个文件。
- **文件大小**：
  - Qwen3.5-Omni：最大2 GB，最长1小时。
  - Qwen3-Omni-Flash：最大256 MB，最长150秒。
  - Qwen-Omni-Turbo：最大150 MB，最长40秒。
- **文件格式**： MP4、AVI、MKV、MOV、FLV、WMV等。
- 视频文件中的视觉信息和音频信息分别计费。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "video_url",
            "video_url": {
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
            },
          },
          {"type": "text", "text": "这个视频讲了什么？"},
        ],
      },
    ],
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    stream=True,
    stream_options={"include_usage": True},
  )

  for chunk in completion:
    if chunk.choices:
      print(chunk.choices[0].delta)
    else:
      print(chunk.usage)
  ```

  ```javascript Node.js
  import OpenAI from "openai";

  const openai = new OpenAI(
    {
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
  );
  const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",
    messages: [
      {
        "role": "user",
        "content": [{
          "type": "video_url",
          "video_url": { "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4" },
        },
        { "type": "text", "text": "这个视频讲了什么？" }]
      }],
    stream: true,
    stream_options: {
      include_usage: true
    },
    modalities: ["text", "audio"],
    audio: { voice: "Tina", format: "wav" }
  });

  for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
      console.log(chunk.choices[0].delta);
    } else {
      console.log(chunk.usage);
    }
  }
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-omni-plus",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "video_url",
            "video_url": {
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
            }
          },
          {
            "type": "text",
            "text": "这个视频讲了什么"
          }
        ]
      }
    ],
    "stream":true,
    "stream_options": {
      "include_usage": true
    },
    "modalities":["text","audio"],
    "audio":{"voice":"Tina","format":"wav"}
  }'
  ```
</CodeGroup>

#### 图片列表格式

**图片数量**

- Qwen3.5-Omni：最少2张，最多2048张。
- Qwen3-Omni-Flash：最少2张，最多128张。
- Qwen-Omni-Turbo：最少4张，最多80张。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "video",
            "video": [
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg",
            ],
          },
          {"type": "text", "text": "描述这个视频中展示的过程"},
        ],
      }
    ],
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    stream=True,
    stream_options={"include_usage": True},
  )

  for chunk in completion:
    if chunk.choices:
      print(chunk.choices[0].delta)
    else:
      print(chunk.usage)
  ```

  ```javascript Node.js
  import OpenAI from "openai";

  const openai = new OpenAI(
    {
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
  );
  const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",
    messages: [{
      role: "user",
      content: [
        {
          type: "video",
          video: [
            "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
            "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
            "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
            "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"
          ]
        },
        {
          type: "text",
          text: "描述这个视频中展示的过程"
        }
      ]
    }],
    stream: true,
    stream_options: {
      include_usage: true
    },
    modalities: ["text", "audio"],
    audio: { voice: "Tina", format: "wav" }
  });

  for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
      console.log(chunk.choices[0].delta);
    } else {
      console.log(chunk.usage);
    }
  }
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-omni-plus",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "video",
            "video": [
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"
            ]
          },
          {
            "type": "text",
            "text": "描述这个视频中展示的过程"
          }
        ]
      }
    ],
    "stream": true,
    "stream_options": {
      "include_usage": true
    },
    "modalities": ["text", "audio"],
    "audio": {
      "voice": "Tina",
      "format": "wav"
    }
  }'
  ```
</CodeGroup>

### 音频和文本输入

- **文件数量**：
  - Qwen3.5-Omni 系列：使用公开URL最多2048个文件；使用Base64编码最多250个文件。
  - Qwen3-Omni-Flash 和 Qwen-Omni-Turbo 系列：仅允许一个文件。
- **文件大小**：
  - Qwen3.5-Omni：最大2 GB，最长3小时。
  - Qwen3-Omni-Flash：最大100 MB，最长20分钟。
  - Qwen-Omni-Turbo：最大10 MB，最长3分钟。
- **文件格式**： 支持AMR、WAV、3GP、3GPP、AAC、MP3等主流格式。

如需输入本地音频文件，请参阅[输入Base64编码的本地文件](#输入base64编码的本地文件)。所有调用均需使用流式输出。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav",
              "format": "wav",
            },
          },
          {"type": "text", "text": "这段音频讲了什么"},
        ],
      },
    ],
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    stream=True,
    stream_options={"include_usage": True},
  )

  for chunk in completion:
    if chunk.choices:
      print(chunk.choices[0].delta)
    else:
      print(chunk.usage)
  ```

  ```javascript Node.js
  import OpenAI from "openai";

  const openai = new OpenAI(
    {
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
  );
  const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",
    messages: [
      {
        "role": "user",
        "content": [{
          "type": "input_audio",
          "input_audio": { "data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav", "format": "wav" },
        },
        { "type": "text", "text": "这段音频讲了什么" }]
      }],
    stream: true,
    stream_options: {
      include_usage: true
    },
    modalities: ["text", "audio"],
    audio: { voice: "Tina", format: "wav" }
  });

  for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
      console.log(chunk.choices[0].delta);
    } else {
      console.log(chunk.usage);
    }
  }
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-omni-plus",
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
          },
          {
            "type": "text",
            "text": "这段音频讲了什么"
          }
        ]
      }
    ],
    "stream":true,
    "stream_options":{
      "include_usage":true
    },
    "modalities":["text","audio"],
    "audio":{"voice":"Tina","format":"wav"}
  }'
  ```
</CodeGroup>

### 图片和文本输入

Qwen-Omni 模型支持多张图片输入。输入图片的要求如下：

- **图片数量**：

  - 通过**公开URL**传入：每次请求最多 **2048** 张图片。
  - 通过**Base64编码**字符串传入：每次请求最多 **250** 张图片。

  除上述每次请求的限制外，**所有**图片和**所有**文本的token总数必须**小于**模型的最大输入长度。
- **图片大小**：
  - Qwen3.5 系列：每个图片文件不超过20 MB。
  - Qwen3-Omni-Flash 和 Qwen-Omni-Turbo 系列：每个图片文件不超过10 MB。
- 图片的宽度和高度必须大于10像素。宽高比不得超过200:1或1:200。
- 支持的图片类型请参阅[视觉和视频理解](/developer-guides/multimodal/vision)。

以下示例代码使用互联网上的图片URL。如需输入本地图片，请参阅[输入Base64编码的本地文件](#输入base64编码的本地文件)。所有调用均需使用流式输出。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "image_url",
            "image_url": {
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
            },
          },
          {"type": "text", "text": "图片中描绘了什么场景？"},
        ],
      },
    ],
    # 设置输出数据模态。当前支持两种：["text","audio"] 和 ["text"]。
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    # stream 必须设置为 True，否则会报错。
    stream=True,
    stream_options={
      "include_usage": True
    }
  )

  for chunk in completion:
    if chunk.choices:
      print(chunk.choices[0].delta)
    else:
      print(chunk.usage)
  ```

  ```javascript Node.js
  import OpenAI from "openai";

  const openai = new OpenAI(
    {
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
  );
  const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",
    messages: [
      {
        "role": "user",
        "content": [{
          "type": "image_url",
          "image_url": { "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg" },
        },
        { "type": "text", "text": "图片中描绘了什么场景？" }]
      }],
    stream: true,
    stream_options: {
      include_usage: true
    },
    modalities: ["text", "audio"],
    audio: { voice: "Tina", format: "wav" }
  });

  for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
      console.log(chunk.choices[0].delta);
    } else {
      console.log(chunk.usage);
    }
  }
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
      "model": "qwen3.5-omni-plus",
      "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "image_url",
            "image_url": {
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
            }
          },
          {
            "type": "text",
            "text": "图片中描绘了什么场景？"
          }
        ]
      }
    ],
      "stream":true,
      "stream_options":{
          "include_usage":true
      },
      "modalities":["text","audio"],
      "audio":{"voice":"Tina","format":"wav"}
  }'
  ```
</CodeGroup>

## 多轮对话

使用 Qwen-Omni 模型的多轮对话功能时，请注意以下事项：

- Assistant消息：messages数组中的assistant消息仅支持文本数据。
- User消息：一条user消息可以包含文本和另一种模态的数据。在多轮对话中，您可以在不同的user消息中使用不同的模态。

<CodeGroup>
  ```python Python
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3",
              "format": "mp3",
            },
          },
          {"type": "text", "text": "这段音频讲了什么"},
        ],
      },
      {
        "role": "assistant",
        "content": [{"type": "text", "text": "这段音频的内容是：欢迎来到千问AI平台"}],
      },
      {
        "role": "user",
        "content": [{"type": "text", "text": "你能介绍一下这家公司吗？"}],
      },
    ],
    # 设置输出数据模态。当前支持两种：["text","audio"] 和 ["text"]。
    modalities=["text"],
    # stream 必须设置为 True，否则会报错。
    stream=True,
    stream_options={"include_usage": True},
  )

  for chunk in completion:
    if chunk.choices:
      print(chunk.choices[0].delta)
    else:
      print(chunk.usage)
  ```

  ```javascript Node.js
  import OpenAI from "openai";

  const openai = new OpenAI(
    {
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
  );
  const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",
    messages: [
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3",
              "format": "mp3",
            },
          },
          { "type": "text", "text": "这段音频讲了什么" },
        ],
      },
      {
        "role": "assistant",
        "content": [{ "type": "text", "text": "这段音频的内容是：欢迎来到千问AI平台" }],
      },
      {
        "role": "user",
        "content": [{ "type": "text", "text": "你能介绍一下这家公司吗？" }]
      }],
    stream: true,
    stream_options: {
      include_usage: true
    },
    modalities: ["text"]
  });

  for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
      console.log(chunk.choices[0].delta);
    } else {
      console.log(chunk.usage);
    }
  }
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3.5-omni-plus",
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
            }
          },
          {
            "type": "text",
            "text": "这段音频讲了什么"
          }
        ]
      },
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": "这段音频的内容是：欢迎来到千问AI平台"
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "你能介绍一下这家公司吗？"
          }
        ]
      }
    ],
    "stream": true,
    "stream_options": {
      "include_usage": true
    },
    "modalities": ["text"]
  }'
  ```
</CodeGroup>

## 解析Base64编码的音频数据输出

Qwen-Omni 模型的音频输出是以流式方式传输的Base64编码数据。您可以使用字符串变量逐步累积每个片段的Base64数据。流式传输完成后，解码最终字符串即可创建音频文件。您也可以在接收到每个片段时实时解码并播放。

<CodeGroup>
  ```python Python
  # pyaudio 安装说明:
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
  from openai import OpenAI
  import base64
  import numpy as np
  import soundfile as sf

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )

  completion = client.chat.completions.create(
    model="qwen3.5-omni-plus",
    messages=[{"role": "user", "content": "你是谁"}],
    # 设置输出数据模态。当前支持两种：["text","audio"] 和 ["text"]。
    modalities=["text", "audio"],
    audio={"voice": "Tina", "format": "wav"},
    # stream 必须设置为 True，否则会报错。
    stream=True,
    stream_options={"include_usage": True},
  )

  # 方法一：生成完成后解码
  audio_string = ""
  for chunk in completion:
    if chunk.choices:
      if hasattr(chunk.choices[0].delta, "audio"):
        try:
          audio_string += chunk.choices[0].delta.audio["data"]
        except Exception as e:
          print(chunk.choices[0].delta.content)
    else:
      print(chunk.usage)

  wav_bytes = base64.b64decode(audio_string)
  audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
  sf.write("audio_assistant_py.wav", audio_np, samplerate=24000)

  # 方法二：边生成边解码（使用方法二时请注释掉方法一的代码）
  # # 初始化 PyAudio
  # import pyaudio
  # import time
  # p = pyaudio.PyAudio()
  # # 创建音频流
  # stream = p.open(format=pyaudio.paInt16,
  #                 channels=1,
  #                 rate=24000,
  #                 output=True)

  # for chunk in completion:
  #     if chunk.choices:
  #         if hasattr(chunk.choices[0].delta, "audio"):
  #             try:
  #                 audio_string = chunk.choices[0].delta.audio["data"]
  #                 wav_bytes = base64.b64decode(audio_string)
  #                 audio_np = np.frombuffer(wav_bytes, dtype=np.int16)
  #                 # 直接播放音频数据
  #                 stream.write(audio_np.tobytes())
  #             except Exception as e:
  #                 print(chunk.choices[0].delta.content)

  # time.sleep(0.8)
  # # 清理资源
  # stream.stop_stream()
  # stream.close()
  # p.terminate()
  ```

  ```javascript Node.js
  // 运行前的准备工作:
  // Windows/Mac/Linux 通用:
  // 1. 确保已安装 Node.js（建议版本 >= 14）
  // 2. 运行以下命令安装必要的依赖:
  //    npm install openai wav
  //
  // 如需使用实时播放功能（方法二），还需要:
  // Windows:
  //    npm install speaker
  // Mac:
  //    brew install portaudio
  //    npm install speaker
  // Linux (Ubuntu/Debian):
  //    sudo apt-get install libasound2-dev
  //    npm install speaker

  import OpenAI from "openai";

  const openai = new OpenAI(
    {
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    }
  );
  const completion = await openai.chat.completions.create({
    model: "qwen3.5-omni-plus",
    messages: [
      {
        "role": "user",
        "content": "你是谁"
      }],
    stream: true,
    stream_options: {
      include_usage: true
    },
    modalities: ["text", "audio"],
    audio: { voice: "Tina", format: "wav" }
  });

  // 方法一：生成完成后解码
  // 需要安装：npm install wav
  import { createWriteStream } from 'node:fs';  // node:fs 是 Node.js 内置模块，无需安装
  import { Writer } from 'wav';

  async function convertAudio(audioString, audioPath) {
    try {
      // 将Base64字符串解码为Buffer
      const wavBuffer = Buffer.from(audioString, 'base64');
      // 创建WAV文件写入流
      const writer = new Writer({
        sampleRate: 24000,  // 采样率
        channels: 1,        // 单声道
        bitDepth: 16        // 16位深度
      });
      // 创建输出文件流并建立管道连接
      const outputStream = createWriteStream(audioPath);
      writer.pipe(outputStream);

      // 写入PCM数据并结束写入
      writer.write(wavBuffer);
      writer.end();

      // 使用Promise等待文件写入完成
      await new Promise((resolve, reject) => {
        outputStream.on('finish', resolve);
        outputStream.on('error', reject);
      });

      // 添加额外等待时间以确保音频完整性
      await new Promise(resolve => setTimeout(resolve, 800));

      console.log(`音频文件已成功保存为 ${audioPath}`);
    } catch (error) {
      console.error('处理过程中发生错误:', error);
    }
  }

  let audioString = "";
  for await (const chunk of completion) {
    if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
      if (chunk.choices[0].delta.audio) {
        if (chunk.choices[0].delta.audio["data"]) {
          audioString += chunk.choices[0].delta.audio["data"];
        }
      }
    } else {
      console.log(chunk.usage);
    }
  }
  // 执行转换
  convertAudio(audioString, "audio_assistant_mjs.wav");

  // 方法二：实时生成并播放
  // 您必须先按照上述系统说明安装必要组件。
  // import Speaker from 'speaker'; // 导入音频播放库

  // // 创建 speaker 实例（配置与WAV文件参数一致）
  // const speaker = new Speaker({
  //     sampleRate: 24000,  // 采样率
  //     channels: 1,        // 声道数
  //     bitDepth: 16,       // 位深度
  //     signed: true        // 有符号PCM
  // });
  // for await (const chunk of completion) {
  //     if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
  //         if (chunk.choices[0].delta.audio) {
  //             if (chunk.choices[0].delta.audio["data"]) {
  //                 const pcmBuffer = Buffer.from(chunk.choices[0].delta.audio.data, 'base64');
  //                 // 直接写入 speaker 进行播放
  //                 speaker.write(pcmBuffer);
  //             }
  //         }
  //     } else {
  //         console.log(chunk.usage);
  //     }
  // }
  // speaker.on('finish', () => console.log('播放完成'));
  // speaker.end(); // 根据API流的实际结束情况调用
  ```
</CodeGroup>

## 输入Base64编码的本地文件

<Tabs>
  <Tab title="图片">
    本示例使用本地保存的文件 [eagle.png](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/zgfeuf/eagle.png)。

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI
      import base64

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      #  Base64编码格式
      def encode_image(image_path):
        with open(image_path, "rb") as image_file:
          return base64.b64encode(image_file.read()).decode("utf-8")

      base64_image = encode_image("eagle.png")

      completion = client.chat.completions.create(
        model="qwen3.5-omni-plus",
        messages=[
          {
            "role": "user",
            "content": [
              {
                "type": "image_url",
                "image_url": {"url": f"data:image/png;base64,{base64_image}"},
              },
              {"type": "text", "text": "图片中描绘了什么场景？"},
            ],
          },
        ],
        # 设置输出数据模态。当前支持两种：["text","audio"] 和 ["text"]。
        modalities=["text", "audio"],
        audio={"voice": "Tina", "format": "wav"},
        # stream 必须设置为 True，否则会报错。
        stream=True,
        stream_options={"include_usage": True},
      )

      for chunk in completion:
        if chunk.choices:
          print(chunk.choices[0].delta)
        else:
          print(chunk.usage)
      ```

      ```javascript Node.js
      import OpenAI from "openai";
      import { readFileSync } from 'fs';

      const openai = new OpenAI(
        {
          apiKey: process.env.DASHSCOPE_API_KEY,
          baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
        }
      );

      const encodeImage = (imagePath) => {
        const imageFile = readFileSync(imagePath);
        return imageFile.toString('base64');
      };
      const base64Image = encodeImage("eagle.png")

      const completion = await openai.chat.completions.create({
        model: "qwen3.5-omni-plus",
        messages: [
          {
            "role": "user",
            "content": [{
              "type": "image_url",
              "image_url": { "url": `data:image/png;base64,${base64Image}` },
            },
            { "type": "text", "text": "图片中描绘了什么场景？" }]
          }],
        stream: true,
        stream_options: {
          include_usage: true
        },
        modalities: ["text", "audio"],
        audio: { voice: "Tina", format: "wav" }
      });

      for await (const chunk of completion) {
        if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
          console.log(chunk.choices[0].delta);
        } else {
          console.log(chunk.usage);
        }
      }
      ```
    </CodeGroup>
  </Tab>

  <Tab title="音频">
    本示例使用本地保存的文件 [welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250430/vicmsy/welcome.mp3)。

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI
      import base64
      import numpy as np
      import soundfile as sf
      import requests

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      def encode_audio(audio_path):
        with open(audio_path, "rb") as audio_file:
          return base64.b64encode(audio_file.read()).decode("utf-8")

      base64_audio = encode_audio("welcome.mp3")

      completion = client.chat.completions.create(
        model="qwen3.5-omni-plus",
        messages=[
          {
            "role": "user",
            "content": [
              {
                "type": "input_audio",
                "input_audio": {
                  "data": f"data:;base64,{base64_audio}",
                  "format": "mp3",
                },
              },
              {"type": "text", "text": "这段音频讲了什么"},
            ],
          },
        ],
        # 设置输出数据模态。当前支持两种：["text","audio"] 和 ["text"]。
        modalities=["text", "audio"],
        audio={"voice": "Tina", "format": "wav"},
        # stream 必须设置为 True，否则会报错。
        stream=True,
        stream_options={"include_usage": True},
      )

      for chunk in completion:
        if chunk.choices:
          print(chunk.choices[0].delta)
        else:
          print(chunk.usage)
      ```

      ```javascript Node.js
      import OpenAI from "openai";
      import { readFileSync } from 'fs';

      const openai = new OpenAI(
        {
          apiKey: process.env.DASHSCOPE_API_KEY,
          baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
        }
      );

      const encodeAudio = (audioPath) => {
        const audioFile = readFileSync(audioPath);
        return audioFile.toString('base64');
      };
      const base64Audio = encodeAudio("welcome.mp3")

      const completion = await openai.chat.completions.create({
        model: "qwen3.5-omni-plus",
        messages: [
          {
            "role": "user",
            "content": [{
              "type": "input_audio",
              "input_audio": { "data": `data:;base64,${base64Audio}`, "format": "mp3" },
            },
            { "type": "text", "text": "这段音频讲了什么" }]
          }],
        stream: true,
        stream_options: {
          include_usage: true
        },
        modalities: ["text", "audio"],
        audio: { voice: "Tina", format: "wav" }
      });

      for await (const chunk of completion) {
        if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
          console.log(chunk.choices[0].delta);
        } else {
          console.log(chunk.usage);
        }
      }
      ```
    </CodeGroup>
  </Tab>

  <Tab title="视频文件">
    本示例使用本地文件 [spring\_mountain.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250430/ngisno/spring_mountain.mp4)。

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI
      import base64
      import numpy as np
      import soundfile as sf

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      #  Base64编码格式
      def encode_video(video_path):
        with open(video_path, "rb") as video_file:
          return base64.b64encode(video_file.read()).decode("utf-8")

      base64_video = encode_video("spring_mountain.mp4")

      completion = client.chat.completions.create(
        model="qwen3.5-omni-plus",
        messages=[
          {
            "role": "user",
            "content": [
              {
                "type": "video_url",
                "video_url": {"url": f"data:;base64,{base64_video}"},
              },
              {"type": "text", "text": "她在唱什么？"},
            ],
          },
        ],
        # 设置输出数据模态。当前支持两种：["text","audio"] 和 ["text"]。
        modalities=["text", "audio"],
        audio={"voice": "Tina", "format": "wav"},
        # stream 必须设置为 True，否则会报错。
        stream=True,
        stream_options={"include_usage": True},
      )

      for chunk in completion:
        if chunk.choices:
          print(chunk.choices[0].delta)
        else:
          print(chunk.usage)
      ```

      ```javascript Node.js
      import OpenAI from "openai";
      import { readFileSync } from 'fs';

      const openai = new OpenAI(
        {
          apiKey: process.env.DASHSCOPE_API_KEY,
          baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
        }
      );

      const encodeVideo = (videoPath) => {
        const videoFile = readFileSync(videoPath);
        return videoFile.toString('base64');
      };
      const base64Video = encodeVideo("spring_mountain.mp4")

      const completion = await openai.chat.completions.create({
        model: "qwen3.5-omni-plus",
        messages: [
          {
            "role": "user",
            "content": [{
              "type": "video_url",
              "video_url": { "url": `data:;base64,${base64Video}` },
            },
            { "type": "text", "text": "她在唱什么？" }]
          }],
        stream: true,
        stream_options: {
          include_usage: true
        },
        modalities: ["text", "audio"],
        audio: { voice: "Tina", format: "wav" }
      });

      for await (const chunk of completion) {
        if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
          console.log(chunk.choices[0].delta);
        } else {
          console.log(chunk.usage);
        }
      }
      ```
    </CodeGroup>
  </Tab>

  <Tab title="图片列表（作为视频）">
    本示例使用本地文件 [football1.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/spqrrx/football1.jpg)、[football2.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/vtnhyr/football2.jpg)、[football3.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250430/enmhbp/football3.jpg) 和 [football4.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250430/ognmyc/football4.jpg)。

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI
      import base64
      import numpy as np
      import soundfile as sf

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      #  Base64编码格式
      def encode_image(image_path):
        with open(image_path, "rb") as image_file:
          return base64.b64encode(image_file.read()).decode("utf-8")

      base64_image_1 = encode_image("football1.jpg")
      base64_image_2 = encode_image("football2.jpg")
      base64_image_3 = encode_image("football3.jpg")
      base64_image_4 = encode_image("football4.jpg")

      completion = client.chat.completions.create(
        model="qwen3.5-omni-plus",
        messages=[
          {
            "role": "user",
            "content": [
              {
                "type": "video",
                "video": [
                  f"data:image/jpeg;base64,{base64_image_1}",
                  f"data:image/jpeg;base64,{base64_image_2}",
                  f"data:image/jpeg;base64,{base64_image_3}",
                  f"data:image/jpeg;base64,{base64_image_4}",
                ],
              },
              {"type": "text", "text": "描述这个视频中的过程。"},
            ],
          }
        ],
        # 设置输出数据模态。当前支持两种：["text","audio"] 和 ["text"]。
        modalities=["text", "audio"],
        audio={"voice": "Tina", "format": "wav"},
        # stream 必须设置为 True，否则会报错。
        stream=True,
        stream_options={"include_usage": True},
      )

      for chunk in completion:
        if chunk.choices:
          print(chunk.choices[0].delta)
        else:
          print(chunk.usage)
      ```

      ```javascript Node.js
      import OpenAI from "openai";
      import { readFileSync } from 'fs';

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      const encodeImage = (imagePath) => {
        const imageFile = readFileSync(imagePath);
        return imageFile.toString('base64');
      };
      const base64Image1 = encodeImage("football1.jpg")
      const base64Image2 = encodeImage("football2.jpg")
      const base64Image3 = encodeImage("football3.jpg")
      const base64Image4 = encodeImage("football4.jpg")

      const completion = await openai.chat.completions.create({
        model: "qwen3.5-omni-plus",
        messages: [{
          role: "user",
          content: [
            {
              type: "video",
              video: [
                `data:image/jpeg;base64,${base64Image1}`,
                `data:image/jpeg;base64,${base64Image2}`,
                `data:image/jpeg;base64,${base64Image3}`,
                `data:image/jpeg;base64,${base64Image4}`
              ]
            },
            {
              type: "text",
              text: "描述这个视频中的过程。"
            }
          ]
        }],
        stream: true,
        stream_options: {
          include_usage: true
        },
        modalities: ["text", "audio"],
        audio: { voice: "Tina", format: "wav" }
      });

      for await (const chunk of completion) {
        if (Array.isArray(chunk.choices) && chunk.choices.length > 0) {
          console.log(chunk.choices[0].delta);
        } else {
          console.log(chunk.usage);
        }
      }
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## API参考

Qwen-Omni的输入和输出参数，请参见 [Chat completions API](/api-reference/chat/openai-chat)。

## 计费与限流

**计费规则**

Qwen-Omni根据不同模态（如音频、图像和视频）的token数量进行计费。详细价格请参见[计费](/developer-guides/getting-started/pricing)。

<Accordion title="音频、图像和视频转换为token的规则">
  **音频**

  - Qwen3.5-Omni 系列：输入音频总 token 数 = 音频时长（秒）x 7；输出音频总 token 数 = 音频时长（秒）x 12.5
  - Qwen3-Omni-Flash：输入与输出音频的总 token 数 = 音频时长（秒）x 12.5
  - Qwen-Omni-Turbo：输入与输出音频的总 token 数 = 音频时长（秒）x 25

  若音频时长不足1秒，按1秒计算。

  **图像**

  - `Qwen3.5-Omni 系列` 和 `Qwen3-Omni-Flash`：每 `32 x 32` 像素对应1个token。
  - `Qwen-Omni-Turbo`：每 `28 x 28` 像素对应1个token。

  Qwen3.5-Omni 系列一张图最少需要 24 个 token，其他模型最少需要 4 个 token；默认最多支持 1280 个 token。Qwen3.5-Omni 系列支持通过 `vl_high_resolution_images` 参数提升图片分辨率上限至 16384 个 token（Qwen-Omni-Turbo、Qwen3-Omni-Flash 不支持该参数）。可使用以下代码，传入图像路径即可估算单张图片消耗的 token 总量：

  ```python
  import math
  from PIL import Image  # pip install Pillow

  # ============ 模型参数配置（按需修改） ============

  # 图像因子：Qwen3.5-Omni系列、Qwen3-Omni-Flash 为 32；Qwen-Omni-Turbo 为 28
  IMAGE_FACTOR = 32

  # Token 下限：Qwen3.5-Omni系列为 24；Qwen-Omni-Turbo、Qwen3-Omni-Flash 为 4
  MIN_TOKENS = 24

  # 高分辨率模式（仅 Qwen3.5-Omni 系列支持，Qwen-Omni-Turbo 和 Qwen3-Omni-Flash 不支持）
  # True  → Token 上限 16384
  # False → Token 上限 1280（默认）
  VL_HIGH_RESOLUTION_IMAGES = False

  # ============ 像素范围（由上方参数自动计算） ============

  MIN_PIXELS = MIN_TOKENS * IMAGE_FACTOR * IMAGE_FACTOR
  MAX_PIXELS = (16384 if VL_HIGH_RESOLUTION_IMAGES else 1280) * IMAGE_FACTOR * IMAGE_FACTOR

  def smart_resize(height, width, factor=IMAGE_FACTOR,
                   min_pixels=MIN_PIXELS, max_pixels=MAX_PIXELS):
    """将图像宽高对齐到 factor 整数倍，并缩放到 [min_pixels, max_pixels] 范围内。"""
    h_bar = max(factor, round(height / factor) * factor)
    w_bar = max(factor, round(width / factor) * factor)

    if h_bar * w_bar > max_pixels:
      beta = math.sqrt((height * width) / max_pixels)
      h_bar = math.floor(height / beta / factor) * factor
      w_bar = math.floor(width / beta / factor) * factor
    elif h_bar * w_bar < min_pixels:
      beta = math.sqrt(min_pixels / (height * width))
      h_bar = math.ceil(height * beta / factor) * factor
      w_bar = math.ceil(width * beta / factor) * factor

    return h_bar, w_bar

  def token_calculate(image_path=''):
    if len(image_path) > 0:
      image = Image.open(image_path)
      height = image.height
      width = image.width
      print(f"缩放前尺寸：{width}x{height}")
      resized_h, resized_w = smart_resize(height, width)
      token = int(resized_h * resized_w / (IMAGE_FACTOR * IMAGE_FACTOR)) + 2
      print(f"缩放后尺寸：{resized_w}x{resized_h}，Token 数：{token}")
      return token
    else:
      raise ValueError("图像路径不能为空。请提供有效的图像文件路径")

  if __name__ == "__main__":
    token = token_calculate(image_path="xxx/test.jpg")
  ```

  **视频**

  视频文件会生成两种类型的token：`video_tokens`（视觉）和 `audio_tokens`（音频）。

  - `video_tokens`

  计算过程较为复杂。详情请参见以下代码：

  ```python
  # 使用前请安装：pip install opencv-python
  import math
  import os
  import logging
  import cv2

  # 固定参数
  FRAME_FACTOR = 2

  # 对于 Qwen3.5-Omni 和 Qwen3-Omni-Flash，IMAGE_FACTOR 为 32
  IMAGE_FACTOR = 32

  # 对于 Qwen-Omni-Turbo，IMAGE_FACTOR 为 28
  # IMAGE_FACTOR = 28

  # 视频帧宽高比
  MAX_RATIO = 200

  # 视频帧像素下限。对于 Qwen3.5-Omni 和 Qwen3-Omni-Flash：128 * 32 * 32
  VIDEO_MIN_PIXELS = 128 * 32 * 32
  # 对于 Qwen-Omni-Turbo
  # VIDEO_MIN_PIXELS = 128 * 28 * 28

  # 视频帧像素上限。对于 Qwen3.5-Omni 和 Qwen3-Omni-Flash：768 * 32 * 32
  VIDEO_MAX_PIXELS = 768 * 32 * 32
  # 对于 Qwen-Omni-Turbo：
  # VIDEO_MAX_PIXELS = 768 * 28 * 28

  FPS = 2
  # 最少抽帧数
  FPS_MIN_FRAMES = 4

  # 最多抽帧数
  # Qwen3.5-Omni 和 Qwen3-Omni-Flash 的最大抽帧数：128
  # Qwen-Omni-Turbo 的最大抽帧数：80
  FPS_MAX_FRAMES = 128

  # 视频输入的最大像素值。对于 Qwen3.5-Omni 和 Qwen3-Omni-Flash：16384 * 32 * 32
  VIDEO_TOTAL_PIXELS = 16384 * 32 * 32
  # 对于 Qwen-Omni-Turbo：
  # VIDEO_TOTAL_PIXELS = 16384 * 28 * 28

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
    video_token += 2  # 视觉标记
    return video_token

  if __name__ == "__main__":
    video_path = "spring_mountain.mp4"  # 你的视频路径
    video_token = video_token_calculate(video_path)
    print("video_tokens:", video_token)
  ```

  - `audio_tokens`
    - Qwen3.5-Omni 系列：输入音频总 token 数 = 音频时长（秒）x 7；输出音频总 token 数 = 音频时长（秒）x 12.5
    - Qwen3-Omni-Flash：输入与输出音频的总 token 数 = 音频时长（秒）x 12.5
    - Qwen-Omni-Turbo：输入与输出音频的总 token 数 = 音频时长（秒）x 25
    - 若音频时长不足1秒，按1秒计算。
</Accordion>

**免费额度**

有关如何领取、查询和使用免费额度的更多信息，请参见[新用户免费额度](/resources/free-quota)。

**限流**

有关模型限流规则和常见问题，请参见[限流](/developer-guides/administration/rate-limits)。

## 错误码

如果调用失败，请参见[错误信息](/api-reference/preparation/error-messages)。

## 音色列表

<Note>
  要使用某个音色，请将 `voice` 请求参数设置为下表中 **voice 参数** 列对应的值。
</Note>

### qwen3.5-omni

| 音色名称              | `voice` 参数  | 描述                           | 支持的语言                                                                                                                                                                                                                                                                           |
| ----------------- | ----------- | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tina              | Tina        | 声音像温热的奶茶——甜蜜舒适，解决问题时又干练利落    | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Cindy             | Cindy       | 一个来自台湾的甜美少女                  | Chinese (Taiwanese accent), English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian |
| Liora Mira        | Liora Mira  | 温柔的声音，在日常生活中编织温暖             | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Sunnybobi         | Sunnybobi   | 开朗活泼、有点社恐的邻家女孩               | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Raymond           | Raymond     | 声音清澈、爱点外卖的宅男                 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Ethan             | Ethan       | 标准普通话，略带北方口音。明亮、温暖、充满活力、富有朝气 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Theo Calm         | Theo Calm   | 于沉默中传递理解，用话语治愈心灵             | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Serena            | Serena      | 温柔的年轻女性                      | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Harvey            | Harvey      | 声音承载着时间的厚度——深沉、醇厚，带着咖啡和旧书的气息 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Maia              | Maia        | 知性与温柔的融合                     | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Evan              | Evan        | 大学生——青春可爱                    | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Qiao              | Qiao        | 不仅仅是可爱——表面甜美，内心个性十足          | Chinese (Taiwanese accent), English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian |
| Momo              | Momo        | 调皮捣蛋——来给你带来好心情               | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Wil               | Wil         | 一个来自深圳、说话带港台腔的年轻人            | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Angel             | Angel       | 略带台湾腔——非常甜美                  | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Li Cassian        | Li Cassian  | 说话克制——三分沉默，七分察言观色            | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Mia               | Mia         | 一位用治愈声音分享慢生活美学的生活艺术家         | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Joyner            | Joyner      | 搞笑、夸张、接地气                    | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Gold              | Gold        | 一位来自美国西海岸的黑人说唱歌手             | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Katerina          | Katerina    | 成熟、富有掌控力的声音，节奏丰富、共鸣深沉        | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Ryan              | Ryan        | 充满能量的演绎，极具戏剧张力——写实与力度并存      | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Jennifer          | Jennifer    | 高品质、电影级的美式女声                 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Aiden             | Aiden       | 一位擅长烹饪的美国年轻人                 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Mione             | Mione       | 成熟、聪慧的英国邻家女孩                 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Sichuan - Sunny   | Sunny       | 一个甜到心坎的四川妹子                  | Chinese (Sichuan dialect), English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian  |
| Beijing - Dylan   | Dylan       | 一个在北京胡同长大的年轻人                | Chinese (Beijing dialect), English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian  |
| Sichuan - Eric    | Eric        | 一个来自成都的活泼四川小伙                | Chinese (Sichuan dialect), English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian  |
| Tianjin - Peter   | Peter       | 天津相声演员——专业捧哏                 | Chinese (Tianjin dialect), English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian  |
| Joseph Chen       | Joseph Chen | 一位长期旅居东南亚的华侨，声音温暖而怀旧         | Chinese (Hokkien), English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian          |
| Shaanxi - Marcus  | Marcus      | 脸宽话少，心诚嗓沉——最正宗的陕西味道          | Chinese (Shaanxi dialect), English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian  |
| Nanjing - Li      | Li          | 一个脾气暴躁的大叔                    | Chinese (Nanjing dialect), English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian  |
| Cantonese - Rocky | Rocky       | 风趣幽默的网络聊天伙伴                  | Chinese (Cantonese), English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian        |
| Sohee             | Sohee       | 温暖、开朗、情感丰富的韩国姐姐              | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Lenn              | Lenn        | 内心理性、细节叛逆——一个穿西装听后朋克的德国青年    | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Ono Anna          | Ono Anna    | 聪明、活泼的青梅竹马                   | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Sonrisa           | Sonrisa     | 一位温暖、外向的拉丁美洲女性               | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Bodega            | Bodega      | 一位热情洋溢的西班牙男性                 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Emilien           | Emilien     | 一位浪漫的法国大哥哥                   | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Andre             | Andre       | 富有磁性、自然而稳重的男声                | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Radio Gol         | Radio Gol   | 一位充满激情的足球解说员，用诗意般的语言讲述比赛     | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Alek              | Alek        | 冷如俄罗斯精神——却温暖如大衣内的羊毛          | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Rizky             | Rizky       | 一位嗓音独特的印尼年轻人                 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Roya              | Roya        | 一个运动系女孩，内心自由奔放               | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Arda              | Arda        | 不高不低——干净、清脆、温暖柔和             | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Hana              | Hana        | 一位成熟的越南女性，热爱养狗               | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Dolce             | Dolce       | 一个慵懒随性的意大利男人                 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Jakub             | Jakub       | 来自波兰小镇的魅力文艺青年                | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Griet             | Griet       | 一位成熟的荷兰文艺女性                  | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Eliska            | Eliska      | 每一个字都承载着中欧的匠心与温度             | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Marina            | Marina      | 在多元文化城市长大的女孩                 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Siiri             | Siiri       | 内敛温柔——语速如静湖般平缓               | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Ingrid            | Ingrid      | 来自挪威乡村的女性                    | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Sigga             | Sigga       | 来自冰岛小镇的知性年轻女性                | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Bea               | Bea         | 一个爱喝咖啡的甜美菲律宾女性               | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |
| Chloe             | Chloe       | 一个马来西亚上班族                    | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean, Thai, Indonesian, Arabic, Vietnamese, Turkish, Finnish, Polish, Hindi, Dutch, Czech, Urdu, Tagalog, Swedish, Danish, Hebrew, Icelandic, Malay, Norwegian, Persian                    |

### qwen3-omni-flash-2025-12-01

| 音色名称               | `voice` 参数 | 描述                                     | 支持的语言                                                                                             |
| ------------------ | ---------- | -------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Cherry             | Cherry     | 阳光、积极、友好、自然的年轻女性                       | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Serena             | Serena     | 温柔的年轻女性                                | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Ethan              | Ethan      | 标准普通话，略带北方口音。阳光、温暖、充满活力、朝气蓬勃           | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Chelsie            | Chelsie    | 二次元虚拟女友                                | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Momo               | Momo       | 调皮捣蛋，为你带来欢乐                            | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Vivian             | Vivian     | 自信可爱，有点小脾气                             | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Moon               | Moon       | 毫不费力的酷飒月白                              | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Maia               | Maia       | 知性与温柔的融合                               | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Kai                | Kai        | 耳朵的舒缓音频SPA                             | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Nofish             | Nofish     | 一个分不清平翘舌的设计师                           | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Bella              | Bella      | 喝酒不打人的小姑娘                              | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Jennifer           | Jennifer   | 高品质电影级美式英语女声                           | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Ryan               | Ryan       | 节奏感十足，戏剧张力爆棚，真实与紧张并存                   | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Katerina           | Katerina   | 韵律丰富、令人难忘的成熟女声                         | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Aiden              | Aiden      | 一个擅长烹饪的美式英语年轻男性                        | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Mia                | Mia        | 温柔如春水，乖顺如初雪                            | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Mochi              | Mochi      | 聪明伶俐的青年——童真未褪，却已智慧初现                   | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Bellona            | Bellona    | 有力、清澈的声音赋予角色生命——激昂到令人热血沸腾              | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Vincent            | Vincent    | 独特的沙哑烟嗓——只需一句台词便能唤起千军万马与英雄传说           | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Bunny              | Bunny      | 可爱溢出的小女孩                               | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Neil               | Neil       | 平直的基线语调搭配精准清晰的发音——最专业的新闻主播             | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Elias              | Elias      | 保持学术严谨的同时运用叙事技巧，将复杂知识转化为易于消化的学习模块      | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Arthur             | Arthur     | 朴实、接地气的声音浸透着岁月与烟草的气息——慢悠悠地展开乡村故事与奇闻趣事  | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Nini               | Nini       | 柔软黏人的声音，像甜甜的糯米糕                        | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Ebona              | Ebona      | 她的低语像一把生锈的钥匙，在你脑海最深处缓缓转动               | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Seren              | Seren      | 温柔舒缓的声音帮你更快入眠。晚安，好梦                    | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Pip                | Pip        | 调皮捣蛋、充满童趣的小男孩                          | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Stella             | Stella     | 平时是甜到发齁的迷糊少女音——但喊出战斗口号时，瞬间散发出坚定不移的爱与正义 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Bodega             | Bodega     | 一个热情奔放的西班牙男人                           | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Sonrisa            | Sonrisa    | 开朗外向的拉丁美洲女性                            | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Alek               | Alek       | 冷如俄罗斯精神，却温暖如大衣内的羊毛                     | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Dolce              | Dolce      | 一个慵懒随性的意大利男人                           | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Sohee              | Sohee      | 温暖开朗、情感丰富的韩国姐姐                         | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Lenn               | Lenn       | 内心理性，细节叛逆——穿西装听后朋克的德国青年                | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Emilien            | Emilien    | 浪漫的法国大哥哥                               | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Andre              | Andre      | 富有磁性、自然沉稳的男声                           | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Shanghai - Jada    | Jada       | 语速飞快、精力充沛的上海阿姨                         | Shanghainese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean    |
| Beijing - Dylan    | Dylan      | 在北京胡同里长大的年轻人                           | Beijing dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |
| Sichuan - Sunny    | Sunny      | 甜到心坎里的四川妹子                             | Sichuan dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |
| Nanjing - Li       | Li         | 一位有耐心的瑜伽老师                             | Nanjing dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |
| Shaanxi - Marcus   | Marcus     | 脸盘子宽、话不多、心实在、根子深的汉子                    | Shaanxi dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |
| Southern Min - Roy | Roy        | 幽默直爽、生动活泼的台湾男人                         | Southern Min, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean    |
| Tianjin - Peter    | Peter      | 天津范儿相声演员兼职业美食评论家                       | Tianjin dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |
| Cantonese - Rocky  | Rocky      | 幽默风趣的实况解说男                             | Cantonese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean       |
| Cantonese - Kiki   | Kiki       | 甜美的香港闺蜜                                | Cantonese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean       |
| Sichuan - Eric     | Eric       | 在人群中总是最出挑的成都四川人                        | Sichuan dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |

### qwen3-omni-flash and qwen3-omni-flash-2025-09-15

| 音色名称               | `voice` 参数 | 描述                                | 支持的语言                                                                                             |
| ------------------ | ---------- | --------------------------------- | ------------------------------------------------------------------------------------------------- |
| Cherry             | Cherry     | 阳光、积极、友好、自然的年轻女性                  | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Ethan              | Ethan      | 标准普通话，略带北方口音。阳光、温暖、充满活力、朝气蓬勃      | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Nofish             | Nofish     | 一个分不清平翘舌的设计师                      | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Jennifer           | Jennifer   | 高品质电影级美式英语女声                      | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Ryan               | Ryan       | 节奏感十足，戏剧张力爆棚，真实与紧张并存              | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Katerina           | Katerina   | 韵律丰富、令人难忘的成熟女声                    | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Elias              | Elias      | 保持学术严谨的同时运用叙事技巧，将复杂知识转化为易于消化的学习模块 | Chinese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean         |
| Shanghai - Jada    | Jada       | 语速飞快、精力充沛的上海阿姨                    | Shanghainese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean    |
| Beijing - Dylan    | Dylan      | 在北京胡同里长大的年轻人                      | Beijing dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |
| Sichuan - Sunny    | Sunny      | 甜到心坎里的四川妹子                        | Sichuan dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |
| Nanjing - Li       | Li         | 一位有耐心的瑜伽老师                        | Nanjing dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |
| Shaanxi - Marcus   | Marcus     | 脸盘子宽、话不多、心实在、根子深的汉子               | Shaanxi dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |
| Southern Min - Roy | Roy        | 幽默直爽、生动活泼的台湾男人                    | Southern Min, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean    |
| Tianjin - Peter    | Peter      | 天津范儿相声演员兼职业美食评论家                  | Tianjin dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |
| Cantonese - Rocky  | Rocky      | 幽默风趣的实况解说男                        | Cantonese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean       |
| Cantonese - Kiki   | Kiki       | 甜美的香港闺蜜                           | Cantonese, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean       |
| Sichuan - Eric     | Eric       | 在人群中总是最出挑的成都四川人                   | Sichuan dialect, English, French, German, Russian, Italian, Spanish, Portuguese, Japanese, Korean |

### Qwen-Omni-Turbo

| 音色名称    | `voice` 参数 | 描述                           | 支持的语言            |
| ------- | ---------- | ---------------------------- | ---------------- |
| Cherry  | Cherry     | 阳光、积极、友好、自然的年轻女性             | Chinese, English |
| Serena  | Serena     | 温柔的年轻女性                      | Chinese, English |
| Ethan   | Ethan      | 标准普通话，略带北方口音。阳光、温暖、充满活力、朝气蓬勃 | Chinese, English |
| Chelsie | Chelsie    | 二次元虚拟女友                      | Chinese, English |

### 开源 Qwen-Omni 模型

| 音色名称    | `voice` 参数 | 描述                           | 支持的语言            |
| ------- | ---------- | ---------------------------- | ---------------- |
| Ethan   | Ethan      | 标准普通话，略带北方口音。阳光、温暖、充满活力、朝气蓬勃 | Chinese, English |
| Chelsie | Chelsie    | 二次元虚拟女友                      | Chinese, English |
