> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 语音到语音模型

> 为'语音输入 → 语音输出'场景（语音对话、语音翻译、同声传译等）选择模型。

<Note>
  本文档面向"语音 → 语音"场景。如需视觉理解、音视频分析、内容审核等更广泛的多模态能力，请参考[全模态](/developer-guides/getting-started/vision-models)。
</Note>

## 从闭源模型迁移到千问AI平台？

如果你正在使用 OpenAI Realtime 或 Gemini Live，可参考下表选择千问AI平台对位模型。

|           | 闭源模型代表                              | 千问AI平台推荐                               |
| --------- | ----------------------------------- | -------------------------------------- |
| 高能力实时对话   | OpenAI GPT Realtime、Gemini 3.1 Live | `qwen-audio-3.0-realtime-plus`         |
| 成本敏感对话    | OpenAI gpt-4o-mini Realtime         | `qwen-audio-3.0-realtime-flash`        |
| 实时翻译 / 同传 | Gemini 3.1 Live                     | `qwen3.5-livetranslate-flash-realtime` |

## S2S 与 Pipeline 对比

构建语音应用有两种方式：

|      | S2S                     | Pipeline（ASR + LLM + TTS） |
| ---- | ----------------------- | ------------------------- |
| 延迟   | 低 — 单模型，流式输出            | 较高 — 需经过 3 个串行环节          |
| 音频理解 | 端到端 — 能感知语气、情感并做出相应回应   | 先转文字再处理 — 音频细节丢失          |
| 语音定制 | 通过 system prompt 选择预设音色 | 支持声音克隆、声音设计（CosyVoice）    |

- **选择 S2S**：适用于交互式对话、低延迟、需要感知音频情绪的场景。请继续阅读本页。
- **选择 Pipeline**：适用于需要自定义音色，或希望为每个环节分别选择最佳 ASR、LLM 和 TTS 的场景。

本文档继续介绍 S2S 单模型路线（Omni、Livetranslate）。如选择 Pipeline 路线，分别在以下文档中挑选三个组件：

- **ASR（语音识别）**：[语音识别](/developer-guides/speech/speech-to-text-models)
- **LLM（大语言模型）**：[文本生成](/developer-guides/getting-started/text-generation-models)
- **TTS（语音合成）**：[语音合成](/developer-guides/speech/tts-models)

## 实时还是文件？

- **实时（WebSocket）**— 适用于实时语音交互场景：语音助手、呼叫中心、同声传译。音频流式输入，语音流式输出。

- **文件（HTTP）**— 适用于可以牺牲延迟换取更好效果的场景：视频配音、播客翻译、离线内容处理。文件模式下还支持 Function Calling、联网搜索、思考模式、视频上下文等附带能力（详见下方"S2S 单模型的附带能力"）。

## 按场景选模型（S2S 单模型路线）

以下场景均针对 S2S 单模型路线。Pipeline 路线请按上述链接分别在 ASR / LLM / TTS 文档中选型。

| 场景                                      | 推荐模型                                   | API       |
| --------------------------------------- | -------------------------------------- | --------- |
| 语音助手 / 客服对话                             | `qwen-audio-3.0-realtime-plus`         | WebSocket |
| 成本敏感的对话                                 | `qwen-audio-3.0-realtime-flash`        | WebSocket |
| 同声传译 / 直播翻译                             | `qwen3.5-livetranslate-flash-realtime` | WebSocket |
| 视频配音 / 播客翻译                             | `qwen3-livetranslate-flash`            | HTTP      |
| 视频分析 / 批量打标（需要思考模式）                     | `qwen3-omni-flash`                     | HTTP      |
| 语义 VAD 语音助手 / 智能客服（支持 Function Calling） | `qwen-audio-3.0-realtime-plus`         | WebSocket |

## S2S 单模型的附带能力

以下能力由 Qwen3.5-Omni / Qwen3-Omni 模型在 S2S 单模型路线下直接提供；其中 Function Calling 也可由 Qwen-Audio Realtime 提供。Qwen-Audio Realtime 不支持联网搜索和思考模式。Pipeline 路线中，对应能力需要由其中的 LLM 等组件分别支持。

### Function calling

让模型根据听到和看到的内容执行操作 -- 查询知识库、查询日程、触发工作流。使用 Qwen3.5 Omni（WebSocket 与 HTTP 模式）、Qwen3 Omni（HTTP 模式）或 Qwen-Audio Realtime（WebSocket 模式）。

<Note>
  Qwen3.5-Omni / Qwen3-Omni 实时（WebSocket）模式和 Livetranslate 模型不支持此功能。
</Note>

### 联网搜索

让模型检索实时信息，回答关于时事、股价、天气等问题。使用 Qwen3.5 Omni（HTTP 和 WebSocket），包括 Plus 和 Flash 系列。模型自主决定是否搜索。Qwen-Audio Realtime 不支持此功能。

<Note>
  Qwen3-Omni-Flash 和 Livetranslate 模型不支持此功能。
</Note>

### 思考模式

当回答质量比延迟更重要时，使用 Qwen3 Omni（HTTP 模式）。模型在回复前会逐步推理，适用于视频分析、批量打标等场景。Qwen-Audio Realtime 不支持此功能。

<Note>
  思考模式下不支持生成语音。
</Note>

## 翻译

以下模型系列均支持语音翻译：

- **Qwen3.5-Livetranslate** — 支持 60 种语言互译，其中 29 种支持音频+文本输出、31 种仅支持文本输出，覆盖中文、英语、法语、德语、俄语、日语、韩语、西班牙语、葡萄牙语、阿拉伯语等主流语种。
- **Qwen3-Livetranslate** — 支持 18 种语言 + 5 种中文方言，约 3 秒延迟，开箱即用。文件模式支持输入视频以获得上下文感知的翻译精度。其中 7 种语言仅输出文本（不输出语音）。
- **Qwen3.5-Omni** — 支持 29 种输出语言 + 7 种中文方言。音视频理解能力更强，支持联网搜索。可通过 system prompt 注入术语和领域上下文。支持实时和文件两种模式。
- **Qwen3-Omni-Flash** — 支持 11 种输出语言 + 8 种中文方言。可通过 system prompt 注入术语和领域上下文，适用于专业领域翻译。支持实时和文件两种模式。成本更低。

<Tip>
  快速上手选 Qwen3.5-Livetranslate（60 种语言，约 3 秒延迟）；追求最佳质量和最广语言覆盖选 Qwen3.5-Omni；控制成本选 Qwen3-Omni-Flash。
</Tip>

<Accordion title="支持的语言">
| 语言      | Qwen3.5-Livetranslate | Qwen3-Livetranslate | Qwen3.5-Omni | Qwen3-Omni-Flash |
| ------- | --------------------- | ------------------- | ------------ | ---------------- |
| 英语      | ✓                     | ✓                   | ✓            | ✓                |
| 中文（普通话） | ✓                     | ✓                   | ✓            | ✓                |
| + 粤语    | 仅文本                   | ✓                   | ✓            | ✓                |
| + 四川话   | ✓                     | ✓                   | ✓            | ✓                |
| + 上海话   | ✓                     | ✓                   | ✓            | ✓                |
| + 北京话   | ✓                     | ✓                   | ✓            | ✓                |
| + 天津话   | ✓                     | ✓                   | ✓            | ✓                |
| + 南京话   | —                     | —                   | ✓            | ✓                |
| + 陕西话   | —                     | —                   | ✓            | ✓                |
| + 闽南语   | —                     | —                   | ✓            | ✓                |
| 法语      | ✓                     | ✓                   | ✓            | ✓                |
| 德语      | ✓                     | ✓                   | ✓            | ✓                |
| 俄语      | ✓                     | ✓                   | ✓            | ✓                |
| 意大利语    | ✓                     | ✓                   | ✓            | ✓                |
| 西班牙语    | ✓                     | ✓                   | ✓            | ✓                |
| 葡萄牙语    | ✓                     | ✓                   | ✓            | ✓                |
| 日语      | ✓                     | ✓                   | ✓            | ✓                |
| 韩语      | ✓                     | ✓                   | ✓            | ✓                |
| 阿拉伯语    | ✓                     | 仅文本                 | ✓            | —                |
| 泰语      | ✓                     | 仅文本                 | ✓            | ✓                |
| 越南语     | ✓                     | 仅文本                 | ✓            | —                |
| 印尼语     | ✓                     | 仅文本                 | ✓            | —                |
| 土耳其语    | ✓                     | 仅文本                 | ✓            | —                |
| 印地语     | ✓                     | 仅文本                 | ✓            | —                |
| 马来语     | ✓                     | —                   | ✓            | —                |
| 荷兰语     | ✓                     | —                   | ✓            | —                |
| 乌尔都语    | ✓                     | —                   | ✓            | —                |
| 挪威语     | ✓                     | —                   | ✓            | —                |
| 瑞典语     | ✓                     | —                   | ✓            | —                |
| 丹麦语     | ✓                     | —                   | ✓            | —                |
| 希伯来语    | ✓                     | —                   | ✓            | —                |
| 芬兰语     | ✓                     | —                   | ✓            | —                |
| 波兰语     | ✓                     | —                   | ✓            | —                |
| 冰岛语     | ✓                     | —                   | ✓            | —                |
| 捷克语     | ✓                     | —                   | ✓            | —                |
| 菲律宾语    | ✓                     | —                   | ✓            | —                |
| 波斯语     | ✓                     | —                   | ✓            | —                |
| 希腊语     | 仅文本                   | 仅文本                 | —            | —                |
| 南非荷兰语   | 仅文本                   | —                   | —            | —                |
| 阿斯图里亚斯语 | 仅文本                   | —                   | —            | —                |
| 白俄罗斯语   | 仅文本                   | —                   | —            | —                |
| 保加利亚语   | 仅文本                   | —                   | —            | —                |
| 孟加拉语    | 仅文本                   | —                   | —            | —                |
| 波斯尼亚语   | 仅文本                   | —                   | —            | —                |
| 加泰罗尼亚语  | 仅文本                   | —                   | —            | —                |
| 宿务语     | 仅文本                   | —                   | —            | —                |
| 爱沙尼亚语   | 仅文本                   | —                   | —            | —                |
| 加利西亚语   | 仅文本                   | —                   | —            | —                |
| 古吉拉特语   | 仅文本                   | —                   | —            | —                |
| 克罗地亚语   | 仅文本                   | —                   | —            | —                |
| 匈牙利语    | 仅文本                   | —                   | —            | —                |
| 爪哇语     | 仅文本                   | —                   | —            | —                |
| 哈萨克语    | 仅文本                   | —                   | —            | —                |
| 卡纳达语    | 仅文本                   | —                   | —            | —                |
| 柯尔克孜语   | 仅文本                   | —                   | —            | —                |
| 拉脱维亚语   | 仅文本                   | —                   | —            | —                |
| 马其顿语    | 仅文本                   | —                   | —            | —                |
| 马拉雅拉姆语  | 仅文本                   | —                   | —            | —                |
| 马拉地语    | 仅文本                   | —                   | —            | —                |
| 旁遮普语    | 仅文本                   | —                   | —            | —                |
| 罗马尼亚语   | 仅文本                   | —                   | —            | —                |
| 斯洛伐克语   | 仅文本                   | —                   | —            | —                |
| 斯洛文尼亚语  | 仅文本                   | —                   | —            | —                |
| 斯瓦希里语   | 仅文本                   | —                   | —            | —                |
| 塔吉克语    | 仅文本                   | —                   | —            | —                |
| 阿塞拜疆语   | 仅文本                   | —                   | —            | —                |
| 乌克兰语    | 仅文本                   | —                   | —            | —                |

  ✓ = 音频 + 文本输出。"仅文本" = 该语言不支持音频输出。Qwen3.5-Livetranslate 共支持 60 种语言（29 种音频+文本，31 种仅文本）。

  Qwen3.5-Omni 共支持 113 种输入语言/方言。详见[完整列表](/developer-guides/speech/multimodal-speech#supported-languages)。

  旧版 `qwen-omni-turbo` 仅支持中文和英语。
</Accordion>

## 推荐模型

下表列出每个系列的常用入口模型。如需锁定特定日期版本（用于版本回归或稳定性需求），请见下方"所有模型"。

| 模型                                     | API       | 输入          | Function calling | 联网搜索 | 思考模式 | 翻译  |
| -------------------------------------- | --------- | ----------- | ---------------- | ---- | ---- | --- |
| `qwen3.5-omni-plus-realtime`           | WebSocket | 文本、音频、图像、视频 | —                | ✓    | —    | 29种 |
| `qwen3.5-omni-plus`                    | HTTP      | 文本、音频、图像、视频 | ✓                | ✓    | —    | 29种 |
| `qwen3.5-omni-flash-realtime`          | WebSocket | 文本、音频、图像、视频 | —                | ✓    | —    | 29种 |
| `qwen3.5-omni-flash`                   | HTTP      | 文本、音频、图像、视频 | ✓                | ✓    | —    | 29种 |
| `qwen3-omni-flash-realtime`            | WebSocket | 文本、音频、图像、视频 | —                | —    | —    | 11种 |
| `qwen3-omni-flash`                     | HTTP      | 文本、音频、图像、视频 | ✓                | —    | ✓    | 11种 |
| `qwen3.5-livetranslate-flash-realtime` | WebSocket | 音频          | —                | —    | —    | 60种 |
| `qwen3.5-livetranslate-flash`          | HTTP      | 音频、视频       | —                | —    | —    | 18种 |

## 所有模型

<AccordionGroup>
  <Accordion title="Qwen-Audio">
| 模型                              | API       | 输入    | Function calling | 联网搜索 | 思考模式 | 翻译 |
| ------------------------------- | --------- | ----- | ---------------- | ---- | ---- | -- |
| `qwen-audio-3.0-realtime-plus`  | WebSocket | 音频、文本 | 支持               | —    | —    | —  |
| `qwen-audio-3.0-realtime-flash` | WebSocket | 音频、文本 | 支持               | —    | —    | —  |
  </Accordion>

  <Accordion title="Qwen3.5-Omni">
| 模型                                       | API       | 输入          | Function calling | 联网搜索 | 思考模式 | 批量 |
| ---------------------------------------- | --------- | ----------- | ---------------- | ---- | ---- | -- |
| `qwen3.5-omni-plus-realtime`             | WebSocket | 文本、音频、图像、视频 | —                | ✓    | —    | —  |
| `qwen3.5-omni-plus-realtime-2026-03-15`  | WebSocket | 文本、音频、图像、视频 | —                | ✓    | —    | —  |
| `qwen3.5-omni-flash-realtime`            | WebSocket | 文本、音频、图像、视频 | —                | ✓    | —    | —  |
| `qwen3.5-omni-flash-realtime-2026-03-15` | WebSocket | 文本、音频、图像、视频 | —                | ✓    | —    | —  |
| `qwen3.5-omni-plus`                      | HTTP      | 文本、音频、图像、视频 | ✓                | ✓    | —    | —  |
| `qwen3.5-omni-plus-2026-03-15`           | HTTP      | 文本、音频、图像、视频 | ✓                | ✓    | —    | —  |
| `qwen3.5-omni-flash`                     | HTTP      | 文本、音频、图像、视频 | ✓                | ✓    | —    | —  |
| `qwen3.5-omni-flash-2026-03-15`          | HTTP      | 文本、音频、图像、视频 | ✓                | ✓    | —    | —  |
  </Accordion>

  <Accordion title="Qwen3-Omni-Flash">
| 模型                                     | API       | 输入          | Function calling | 联网搜索 | 思考模式 | 批量 |
| -------------------------------------- | --------- | ----------- | ---------------- | ---- | ---- | -- |
| `qwen3-omni-flash-realtime`            | WebSocket | 文本、音频、图像、视频 | —                | —    | —    | —  |
| `qwen3-omni-flash-realtime-2025-12-01` | WebSocket | 文本、音频、图像、视频 | —                | —    | —    | —  |
| `qwen3-omni-flash-realtime-2025-09-15` | WebSocket | 文本、音频、图像、视频 | —                | —    | —    | —  |
| `qwen3-omni-flash`                     | HTTP      | 文本、音频、图像、视频 | ✓                | —    | ✓    | —  |
| `qwen3-omni-flash-2025-12-01`          | HTTP      | 文本、音频、图像、视频 | ✓                | —    | ✓    | —  |
| `qwen3-omni-flash-2025-09-15`          | HTTP      | 文本、音频、图像、视频 | ✓                | —    | ✓    | —  |
  </Accordion>

  <Accordion title="Qwen3.5-Livetranslate">
| 模型                                                | API       | 输入 | 语言数 |
| ------------------------------------------------- | --------- | -- | --- |
| `qwen3.5-livetranslate-flash-realtime`            | WebSocket | 音频 | 60  |
| `qwen3.5-livetranslate-flash-realtime-2026-05-19` | WebSocket | 音频 | 60  |
  </Accordion>

  <Accordion title="Qwen3-Livetranslate">
| 模型                                              | API       | 输入    | 语言数 |
| ----------------------------------------------- | --------- | ----- | --- |
| `qwen3-livetranslate-flash-realtime`（旧版）        | WebSocket | 音频    | 18  |
| `qwen3-livetranslate-flash-realtime-2025-09-22` | WebSocket | 音频    | 18  |
| `qwen3-livetranslate-flash`                     | HTTP      | 音频、视频 | 18  |
| `qwen3-livetranslate-flash-2025-12-01`          | HTTP      | 音频、视频 | 18  |
  </Accordion>

  <Accordion title="旧版模型">
    以下模型不再更新。新项目请使用 Qwen3.5-Omni 或 Qwen3-Omni-Flash。

| 模型                                    | 输入          | API       |
| ------------------------------------- | ----------- | --------- |
| `qwen2.5-omni-7b`                     | 文本、音频、图像、视频 | HTTP      |
| `qwen-omni-turbo`                     | 文本、音频、图像、视频 | HTTP      |
| `qwen-omni-turbo-latest`              | 文本、音频、图像、视频 | HTTP      |
| `qwen-omni-turbo-2025-03-26`          | 文本、音频、图像、视频 | HTTP      |
| `qwen-omni-turbo-2025-01-19`          | 文本、音频、图像、视频 | HTTP      |
| `qwen-omni-turbo-realtime`            | 文本、音频       | WebSocket |
| `qwen-omni-turbo-realtime-latest`     | 文本、音频       | WebSocket |
| `qwen-omni-turbo-realtime-2025-05-08` | 文本、音频       | WebSocket |
  </Accordion>
</AccordionGroup>

## 下一步

选定模型后，参考对应的调用文档：

- Qwen-Audio Realtime（WebSocket，实时语音对话）→ [实时语音对话](/developer-guides/speech/qwen-audio-realtime)
- Qwen3.5-Omni / Qwen3-Omni（WebSocket，实时）→ [实时多模态语音](/developer-guides/speech/realtime-multimodal-speech)
- Qwen3.5-Omni / Qwen3-Omni（HTTP，文件）→ [多模态语音](/developer-guides/speech/multimodal-speech)
- Qwen3.5-Livetranslate（WebSocket，实时）→ [实时翻译](/developer-guides/speech/realtime-translation)
- Qwen3-Livetranslate（HTTP，文件）→ [文件翻译](/developer-guides/speech/file-translation)

## 了解更多

<CardGroup cols={2}>
  <Card title="实时对话" icon="MicrophoneOutlined" href="/developer-guides/speech/realtime-multimodal-speech">
    构建实时多模态语音助手。
  </Card>

  <Card title="文件对话" icon="FileCodeOutlined" href="/developer-guides/speech/multimodal-speech">
    处理音频和视频文件并生成语音输出。
  </Card>

  <Card title="实时翻译" icon="TranslationOutlined" href="/developer-guides/speech/realtime-translation">
    实时跨语言语音翻译。
  </Card>

  <Card title="文件翻译" icon="TransformOutlined" href="/developer-guides/speech/file-translation">
    翻译音频和视频文件。
  </Card>
</CardGroup>
