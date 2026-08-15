> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 语音识别模型

> 选择适合实时字幕、音频转写等场景的语音识别模型。

## 从闭源模型迁移到千问AI平台？

如果你正在使用 Whisper、Deepgram 或 Google 的语音识别服务，可参考下表选择对应的千问AI平台模型。

| 使用场景       | 闭源模型代表                           | 千问AI平台推荐                                                        |
| ---------- | -------------------------------- | --------------------------------------------------------------- |
| 实时识别       | Deepgram Nova-3、Google Chirp 3   | `qwen-audio-3.0-asr-flash-streaming`                            |
| 非实时 / 文件转写 | OpenAI gpt-4o-transcribe、Whisper | `qwen-audio-3.0-asr-flash-filetrans`、`qwen-audio-3.0-asr-flash` |

本文按"先选维度、再看模型"的顺序帮助您完成选型：先从"[选型决策维度](#选型决策维度)"（实时/非实时、专业术语、说话人分离、情感识别）确认场景；再到"[推荐模型](#推荐模型)"查看针对各场景的首选；如需更多版本可在"[全部模型](#全部模型)"按系列展开；最后到"[音频规格](#音频规格)"核对输入文件约束。各模型支持的语言（含方言）随附在"[全部模型](#全部模型)"的各系列子节内。

## 选型决策维度

从以下 4 个维度逐项确认，每个维度都会推荐适配的模型。

### 实时还是非实时？

实时是指在用户说话的同时输出识别结果，非实时是指录音结束后再进行转写。

- **实时（实时语音识别）**：基于 WebSocket 协议，音频流式输入，文本流式输出。适用于实时字幕、语音助手和会议转写。推荐使用 `qwen-audio-3.0-asr-flash-streaming`（热词、Prompt 上下文、多语种及方言）。

- **非实时（录音文件识别）**：基于 HTTP 协议，提交音频文件获取识别结果。适用于呼叫中心录音、播客和访谈等场景。推荐使用 `qwen-audio-3.0-asr-flash-filetrans`（热词、Prompt 上下文、说话人分离）。

Qwen-Audio-3.0-ASR-Flash-Streaming 和 Fun-ASR-Realtime 系列模型还支持通过 AOQ 协议接入；如果是客户端对接，且更看重稳定的延迟、弱网下的交互能力、实时双工的降噪与回声消除，可优先考虑 AOQ，协议对比与选型请参见 [Realtime API 概述](/developer-guides/realtime-api/overview)。

Qwen-Audio-3.0-ASR-Flash-Streaming、Qwen-Audio-3.0-ASR-Flash-Filetrans，以及 Fun-ASR 和 Qwen-ASR 的实时模型支持通过 DashScope SDK（Java、Python）接入。Qwen-Audio-3.0-ASR-Flash-Streaming、Qwen-Audio-3.0-ASR-Flash-Filetrans 和 Fun-ASR 模型还支持 Android、iOS SDK 接入，速度快。其他模型需根据对应的 WebSocket 或 HTTP 协议直接调用。

选择实时接入请参考[实时语音识别](/developer-guides/speech/asr-realtime)，选择非实时接入请参考[非实时语音识别](/developer-guides/speech/asr)。

### 处理专业术语

两种方式，按灵活性排序：

1. **Prompt 上下文注入** — 在系统提示词中描述您的领域背景，无需预配置。模型在每次请求时自适应。推荐使用 Qwen-Audio-3.0-ASR-Flash-Streaming、Qwen-Audio-3.0-ASR-Flash-Filetrans 和 Qwen-Audio-3.0-ASR-Flash 系列模型。

2. **热词** — 提供带权重的词汇表。推荐使用 Qwen-Audio-3.0-ASR-Flash-Streaming、Qwen-Audio-3.0-ASR-Flash-Filetrans 和 Qwen-Audio-3.0-ASR-Flash 系列模型。

### 说话人分离

Qwen-Audio-3.0-ASR-Flash-Filetrans 系列（`qwen-audio-3.0-asr-flash-filetrans`）以及 Fun-ASR 系列的非实时模型（`fun-asr`、`fun-asr-mtl`）支持说话人分离。如果您需要区分"谁说了什么"，推荐使用 `qwen-audio-3.0-asr-flash-filetrans`。

### 情感识别

Qwen-ASR 系列模型在转写的同时支持情感识别。推荐使用 `qwen3-asr-flash-realtime`（实时）或 `qwen3-asr-flash-filetrans`（非实时）。

## 推荐模型

以下为各场景下最推荐的模型，可前往模型广场查看详情。

| 模型ID                                 | 模式  | API       | 精度增强          | 情感识别 | 说话人分离 | 支持语言   | 音频最大时长/大小  |
| ------------------------------------ | --- | --------- | ------------- | ---- | ----- | ------ | ---------- |
| `qwen-audio-3.0-asr-flash-streaming` | 实时  | WebSocket | 热词、Prompt 上下文 | ✗    | ✗     | 多语种及方言 | 无限制        |
| `qwen-audio-3.0-asr-flash-filetrans` | 非实时 | HTTP      | 热词、Prompt 上下文 | ✗    | ✓     | 多语种及方言 | 12小时 / 2GB |

## 全部模型

<AccordionGroup>
  <Accordion title="Qwen-Audio-3.0-ASR-Flash-Streaming">
| 模型ID                                 | 模式 | API       | 精度增强          | 情感识别 | 说话人分离 | 支持语言   | 音频最大时长/大小 |
| ------------------------------------ | -- | --------- | ------------- | ---- | ----- | ------ | --------- |
| `qwen-audio-3.0-asr-flash-streaming` | 实时 | WebSocket | 热词、Prompt 上下文 | ✗    | ✗     | 多语种及方言 | 无限制       |

    **支持的语言**：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
  </Accordion>

  <Accordion title="Qwen-Audio-3.0-ASR-Flash-Filetrans">
| 模型ID                                 | 模式  | API  | 精度增强          | 情感识别 | 说话人分离 | 支持语言   | 音频最大时长/大小  |
| ------------------------------------ | --- | ---- | ------------- | ---- | ----- | ------ | ---------- |
| `qwen-audio-3.0-asr-flash-filetrans` | 非实时 | HTTP | 热词、Prompt 上下文 | ✗    | ✓     | 多语种及方言 | 12小时 / 2GB |

    **支持的语言**：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
  </Accordion>

  <Accordion title="Qwen-Audio-3.0-ASR-Flash">
| 模型ID                       | 模式  | API  | 精度增强          | 情感识别 | 说话人分离 | 支持语言   | 音频最大时长/大小 |
| -------------------------- | --- | ---- | ------------- | ---- | ----- | ------ | --------- |
| `qwen-audio-3.0-asr-flash` | 非实时 | HTTP | 热词、Prompt 上下文 | ✗    | ✗     | 多语种及方言 | 5分钟 / 2GB |

    **支持的语言**：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
  </Accordion>

  <Accordion title="Fun-ASR">
| 模型ID                                   | 模式  | API       | 精度增强       | 情感识别 | 说话人分离 | 支持语言     | 音频最大时长/大小  |
| -------------------------------------- | --- | --------- | ---------- | ---- | ----- | -------- | ---------- |
| `fun-asr-realtime`                     | 实时  | WebSocket | 热词         | ✗    | ✗     | 多语种及方言   | 无限制        |
| `fun-asr-realtime-2026-02-28`          | 实时  | WebSocket | 热词         | ✗    | ✗     | 中、英、日及方言 | 无限制        |
| `fun-asr-realtime-2025-11-07`          | 实时  | WebSocket | 热词         | ✗    | ✗     | 多语种及方言   | 无限制        |
| `fun-asr-realtime-2025-09-15`          | 实时  | WebSocket | 热词         | ✗    | ✗     | 中、英      | 无限制        |
| `fun-asr-flash-8k-realtime`            | 实时  | WebSocket | 热词         | ✗    | ✗     | 中文       | 无限制        |
| `fun-asr-flash-8k-realtime-2026-01-28` | 实时  | WebSocket | 热词         | ✗    | ✗     | 中文       | 无限制        |
| `fun-asr`                              | 非实时 | HTTP      | 热词         | ✗    | ✓     | 多语种及方言   | 12小时 / 2GB |
| `fun-asr-2025-11-07`                   | 非实时 | HTTP      | 热词         | ✗    | ✓     | 多语种及方言   | 12小时 / 2GB |
| `fun-asr-2025-08-25`                   | 非实时 | HTTP      | 热词         | ✗    | ✓     | 中、英      | 12小时 / 2GB |
| `fun-asr-mtl`                          | 非实时 | HTTP      | 热词         | ✗    | ✓     | 多语种及方言   | 12小时 / 2GB |
| `fun-asr-mtl-2025-08-25`               | 非实时 | HTTP      | 热词         | ✗    | ✓     | 多语种及方言   | 12小时 / 2GB |
| `fun-asr-flash-2026-06-15`             | 非实时 | HTTP      | Prompt 上下文 | ✗    | ✗     | 多语种及方言   | 5分钟 / 2GB  |

    **支持的语言（按版本）**：

    - **Fun-ASR-Realtime 主版本**（`fun-asr-realtime`、`fun-asr-realtime-2025-11-07`）：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
    - `fun-asr-realtime-2026-02-28`：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语
    - `fun-asr-realtime-2025-09-15`：中文（普通话）、英文
    - **Fun-ASR-Flash-Realtime（8K）**（`fun-asr-flash-8k-realtime`、`fun-asr-flash-8k-realtime-2026-01-28`）：中文
    - **Fun-ASR 主版本**（`fun-asr`、`fun-asr-2025-11-07`）：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
    - **Fun-ASR-Flash**（`fun-asr-flash-2026-06-15`）：中文（普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语；并支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等，包括河南、陕西、湖北、四川、重庆、云南、贵州、广东、广西、河北、天津、山东、安徽、南京、江苏、杭州、甘肃、宁夏等地区官话口音）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
    - `fun-asr-2025-08-25`：中文（普通话）、英文
    - **Fun-ASR（MTL）**（`fun-asr-mtl`、`fun-asr-mtl-2025-08-25`）：中文（普通话、粤语）、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语
  </Accordion>

  <Accordion title="Qwen-ASR">
| 模型ID                                   | 模式  | API             | 精度增强 | 情感识别 | 说话人分离 | 支持语言   | 音频最大时长/大小  |
| -------------------------------------- | --- | --------------- | ---- | ---- | ----- | ------ | ---------- |
| `qwen3-asr-flash-realtime`             | 实时  | WebSocket       | ✗    | ✓    | ✗     | 多语种及方言 | 无限制        |
| `qwen3-asr-flash-realtime-2026-02-10`  | 实时  | WebSocket       | ✗    | ✓    | ✗     | 多语种及方言 | 无限制        |
| `qwen3-asr-flash-realtime-2025-10-27`  | 实时  | WebSocket       | ✗    | ✓    | ✗     | 多语种及方言 | 无限制        |
| `qwen3-asr-flash-filetrans`            | 非实时 | HTTP            | ✗    | ✓    | ✗     | 多语种及方言 | 12小时 / 2GB |
| `qwen3-asr-flash-filetrans-2025-11-17` | 非实时 | HTTP            | ✗    | ✓    | ✗     | 多语种及方言 | 12小时 / 2GB |
| `qwen3-asr-flash`                      | 非实时 | HTTP（OpenAI 兼容） | ✗    | ✓    | ✗     | 多语种及方言 | 5分钟 / 10MB |
| `qwen3-asr-flash-2026-02-10`           | 非实时 | HTTP（OpenAI 兼容） | ✗    | ✓    | ✗     | 多语种及方言 | 5分钟 / 10MB |
| `qwen3-asr-flash-2025-09-08`           | 非实时 | HTTP（OpenAI 兼容） | ✗    | ✓    | ✗     | 多语种及方言 | 5分钟 / 10MB |

    **支持的语言**：所有 Qwen-ASR 系列模型（`qwen3-asr-flash-realtime`、`qwen3-asr-flash-filetrans`、`qwen3-asr-flash` 及其快照版）均支持相同的语言列表：中文（普通话、四川话、闽南语、吴语、粤语）、英语、日语、德语、韩语、俄语、法语、葡萄牙语、阿拉伯语、意大利语、西班牙语、印地语、印尼语、泰语、土耳其语、乌克兰语、越南语、捷克语、丹麦语、菲律宾语、芬兰语、冰岛语、马来语、挪威语、波兰语、瑞典语。
  </Accordion>

  <Accordion title="Paraformer">
    Paraformer 是较早一代的 ASR 模型，包括实时与非实时两类。若您的业务允许，建议迁移到前文推荐的 Fun-ASR 或 Qwen-ASR。

| 模型ID                        | API       | 说明                           |
| --------------------------- | --------- | ---------------------------- |
| `paraformer-realtime-v2`    | WebSocket | 实时识别，中、英、日、韩、德、法、俄           |
| `paraformer-realtime-v1`    | WebSocket | 实时识别，中、英、日、韩、德、法、俄           |
| `paraformer-realtime-8k-v2` | WebSocket | 实时识别，8kHz 电话场景，中文            |
| `paraformer-realtime-8k-v1` | WebSocket | 实时识别，8kHz 电话场景，中文            |
| `paraformer-v2`             | HTTP      | 录音文件识别，支持说话人分离，中、英、日、韩、德、法、俄 |
| `paraformer-8k-v2`          | HTTP      | 录音文件识别，8kHz 电话场景，中文          |
| `paraformer-v1`             | HTTP      | 录音文件识别，支持说话人分离，中、英、日、韩、德、法、俄 |
| `paraformer-8k-v1`          | HTTP      | 录音文件识别，8kHz 电话场景，中文          |
| `paraformer-mtl-v1`         | HTTP      | 录音文件识别，支持说话人分离，多语种           |

    **支持的语言（按版本）**：

    - `paraformer-realtime-v2`、`paraformer-v2`：中文（普通话、粤语、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、宁夏话、山西话、陕西话、山东话、四川话、天津话、江西话、云南话、上海话）、英文、日语、韩语、德语、法语、俄语
    - `paraformer-realtime-v1`、`paraformer-realtime-8k-v2`、`paraformer-realtime-8k-v1`、`paraformer-8k-v2`、`paraformer-8k-v1`：中文普通话
    - `paraformer-v1`：中文普通话、英文
    - `paraformer-mtl-v1`：中文（普通话、粤语、吴语、闽南语、东北话、甘肃话、贵州话、河南话、湖北话、湖南话、宁夏话、山西话、陕西话、山东话、四川话、天津话）、英文、日语、韩语、西班牙语、印尼语、法语、德语、意大利语、马来语
  </Accordion>

  <Accordion title="其他（即将下线）">
    以下模型已计划下线，仅供存量业务参考，请尽快迁移到推荐模型。

| 模型ID                | API       | 说明                 |
| ------------------- | --------- | ------------------ |
| `gummy-realtime-v1` | WebSocket | 实时识别，中、英及方言        |
| `gummy-chat-v1`     | WebSocket | 短音频实时识别（1分钟限制），多语种 |
| `sensevoice-v1`     | HTTP      | 录音文件识别，多语种         |
  </Accordion>
</AccordionGroup>

## 音频规格

下表汇总了**实时**和**非实时**两种模式下的音频规格（输入方式、格式、采样率、大小/时长）。各模型支持的语言（含方言）见上文"[全部模型](#全部模型)"内对应系列子节。

### 实时

| 模型ID                                                                                | 输入方式         | 音频格式                                         | 采样率                                                                                          | 大小/时长 |
| ----------------------------------------------------------------------------------- | ------------ | -------------------------------------------- | -------------------------------------------------------------------------------------------- | ----- |
| **Qwen-Audio-3.0-ASR-Flash-Streaming**（`qwen-audio-3.0-asr-flash-streaming` 系列）     | 二进制（Binary）流 | `pcm`、`wav`、`mp3`、`opus`、`speex`、`aac`、`amr` | 任意                                                                                           | 不限    |
| **Fun-ASR-Realtime**（`fun-asr-realtime` 系列）                                         | 二进制（Binary）流 | `pcm`、`wav`、`mp3`、`opus`、`speex`、`aac`、`amr` | 任意                                                                                           | 不限    |
| **Fun-ASR-Flash-8K-Realtime**（`fun-asr-flash-8k-realtime` 系列）                       | 二进制（Binary）流 | 同 Fun-ASR-Realtime                           | 8 kHz                                                                                        | 不限    |
| **Qwen-ASR-Realtime**（`qwen3-asr-flash-realtime` 系列）                                | 二进制（Binary）流 | `pcm`、`opus`                                 | 8 kHz、16 kHz                                                                                 | 不限    |
| **Paraformer-Realtime**（`paraformer-realtime-v2/v1`、`paraformer-realtime-8k-v2/v1`） | 二进制（Binary）流 | 同 Fun-ASR-Realtime                           | `paraformer-realtime-v2` 任意；`paraformer-realtime-v1` 16 kHz；`paraformer-realtime-8k-*` 8 kHz | 不限    |

所有实时模型均为**单声道**输入。

### 非实时

| 模型ID                                                                            | 输入方式                           | 音频格式                                                                                                      | 采样率                                                                            | 文件大小/时长                       |
| ------------------------------------------------------------------------------- | ------------------------------ | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | ----------------------------- |
| **Qwen-Audio-3.0-ASR-Flash-Filetrans**（`qwen-audio-3.0-asr-flash-filetrans` 系列） | 公网可访问的文件 URL，单次 1 个            | `aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv` | 任意                                                                             | ≤2 GB；≤12 小时（启用说话人分离建议 ≤2 小时） |
| **Qwen-Audio-3.0-ASR-Flash**（`qwen-audio-3.0-asr-flash` 系列）                     | URL / Base64，单次 1 个            | `aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv` | 任意                                                                             | ≤2 GB；≤5 分钟                   |
| **Fun-ASR**（`fun-asr`、`fun-asr-mtl` 系列）                                         | 公网可访问的文件 URL，单次 1 个            | `aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv` | 任意                                                                             | ≤2 GB；≤12 小时（启用说话人分离建议 ≤2 小时） |
| **Fun-ASR-Flash**（`fun-asr-flash-2026-06-15`）                                   | URL / Base64，单次 1 个            | `aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv` | 任意                                                                             | ≤2 GB；≤5 分钟                   |
| **Fun-ASR-Realtime**（`fun-asr-realtime`、`fun-asr-realtime-2026-02-28`）          | URL / Base64，单次 1 个            | `aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv` | 任意                                                                             | ≤2 GB；≤5 分钟                   |
| **Paraformer**（`paraformer-v2/v1`、`paraformer-mtl-v1`、`paraformer-8k-v2/v1`）    | 同 Fun-ASR                      | 同 Fun-ASR                                                                                                 | `paraformer-v2/v1` 任意；`paraformer-8k-*` 仅 8 kHz；`paraformer-mtl-v1` 16 kHz 及以上 | 同 Fun-ASR                     |
| **Qwen3-ASR-Flash-Filetrans**（`qwen3-asr-flash-filetrans` 系列）                   | 公网可访问的文件 URL，单次 1 个            | `aac`、`amr`、`avi`、`flac`、`flv`、`m4a`、`mkv`、`mov`、`mp3`、`mp4`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv` | `pcm` 必须 16 kHz；其他格式任意（服务端会重采样为 16 kHz 再识别）                                    | ≤2 GB；≤12 小时                  |
| **Qwen3-ASR-Flash**（`qwen3-asr-flash` 系列）                                       | URL / Base64 / 本地文件绝对路径，单次 1 个 | `aac`、`amr`、`avi`、`aiff`、`flac`、`flv`、`mkv`、`mp3`、`mpeg`、`ogg`、`opus`、`wav`、`webm`、`wma`、`wmv`            | `pcm` 必须 16 kHz；其他格式任意（服务端会重采样为 16 kHz 再识别）                                    | ≤10 MB；≤5 分钟                  |

<Tip>
  需要将语音翻译为其他语言？请参阅[语音翻译模型](/developer-guides/speech/s2s-models)，了解 LiveTranslate 和 Qwen-Omni 的实时与文件翻译能力。
</Tip>

## 了解更多

<CardGroup cols={2}>
  <Card title="实时语音识别" icon="MicrophoneOutlined" href="/developer-guides/speech/asr-realtime">
    流式输入音频，实时返回识别文本。
  </Card>

  <Card title="音频文件转写" icon="FileCodeOutlined" href="/developer-guides/speech/asr">
    通过异步 API 转写录音文件。
  </Card>

  <Card title="自定义热词" icon="ListLettersOutlined" href="/developer-guides/speech/improve-recognition-accuracy">
    提升专业术语的识别准确率。
  </Card>
</CardGroup>
