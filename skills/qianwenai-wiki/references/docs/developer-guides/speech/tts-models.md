> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 语音合成模型

> 选择适合语音合成、声音克隆和声音设计的模型。

选择模型前，先确定两个问题：是否需要自定义音色（还是内置音色即可），以及是否需要实时流式输出。

## 从闭源模型迁移到千问AI平台？

如果你正在使用 ElevenLabs、OpenAI 或 Google 的语音合成服务，可参考下表选择对应的模型：

| 使用场景         | 闭源模型代表                           | 推荐                                                           |
| ------------ | -------------------------------- | ------------------------------------------------------------ |
| 内置音色 / 标准合成  | OpenAI gpt-4o-tts、Google Chirp 3 | `qwen-audio-3.0-tts-plus`                                    |
| 自定义音色 / 声音复刻 | ElevenLabs Multilingual v3       | `qwen-audio-3.0-tts-flash`（声音复刻）、`cosyvoice-v3.5-plus`（声音设计） |

## 内置音色还是自定义音色？

### 内置音色

从音色库中选择一个音色，即可开始合成语音。

- **Qwen-Audio-TTS** — 通过 WebSocket/HTTP 调用，支持声音复刻和指令控制
- **CosyVoice** — 音色库丰富，合成质量高，选定音色即可使用
- **Qwen3-TTS** — 低延迟流式输出；使用 `-instruct` 变体可通过自然语言控制语速、情感和风格
- **MiniMax** — 支持混合音色和情感风格调节，适合社交、播客等场景

<Note>
  CosyVoice 系列模型还支持通过 AOQ 协议接入；如果是客户端对接，且更看重稳定的延迟、弱网下的交互能力、实时双工的降噪与回声消除，可优先考虑 AOQ，协议对比与选型请参见 [Realtime API 概述](/developer-guides/realtime-api/overview)。
</Note>

### 自定义音色

音色库中没有满意的音色？

- **声音克隆（Voice Cloning）** — 基于音频样本复现特定人物的声音。适用于需要匹配目标音色的场景。Qwen-Audio-TTS、CosyVoice、Qwen3-TTS 和 MiniMax 均支持声音克隆。
- **声音设计（Voice Design）** — 通过文字描述生成全新音色（例如"温暖低沉的女声"）。适用于无音频样本但需要品牌专属音色的场景。

## 控制语音效果

三种方式，按灵活性由高到低排列：

1. **指令控制**（CosyVoice 系列：`cosyvoice-v3.5-plus`、`cosyvoice-v3.5-flash`、`cosyvoice-v3-flash`；Qwen-TTS 系列：`qwen3-tts-instruct-flash`、`qwen3-tts-instruct-flash-realtime`）— 用自然语言描述期望的朗读效果，可逐次调整语速、情感和风格。灵活性最高。

2. **声音设计**（`qwen3-tts-vd-*`）— 通过文字描述生成自定义音色。适合在没有音频样本的情况下打造品牌音色。

3. **声音克隆**（`qwen3-tts-vc-*`）— 基于音频样本复现已有声音。适合需要匹配特定人物音色的场景。

## 推荐模型

| 模型                                 | 系列             | 流式输出 | 自定义音色 | 指令控制 |
| ---------------------------------- | -------------- | ---- | ----- | ---- |
| `qwen-audio-3.0-tts-plus`          | Qwen-Audio-TTS | ✓    | ✓     | ✓    |
| `cosyvoice-v3-plus`                | CosyVoice      | ✓    | —     | —    |
| `MiniMax/speech-2.8-hd`            | MiniMax        | ✓    | ✓     | —    |
| `qwen3-tts-flash`                  | Qwen3-TTS      | ✓    | —     | —    |
| `qwen3-tts-flash-realtime`         | Qwen3-TTS      | ✓    | —     | —    |
| `qwen3-tts-instruct-flash`         | Qwen3-TTS      | ✓    | —     | ✓    |
| `qwen3-tts-vc-realtime-2026-01-15` | Voice Cloning  | ✓    | ✓     | —    |
| `qwen3-tts-vd-realtime-2026-01-15` | Voice Design   | ✓    | ✓     | —    |

## 全部模型

<AccordionGroup>
  <Accordion title="Qwen-Audio-TTS">
| 模型                         | 流式输出 | 自定义音色 | 指令控制 |
| -------------------------- | ---- | ----- | ---- |
| `qwen-audio-3.0-tts-plus`  | ✓    | ✓     | ✓    |
| `qwen-audio-3.0-tts-flash` | ✓    | ✓     | ✓    |
  </Accordion>

  <Accordion title="CosyVoice">
| 模型                     | 流式输出 | 自定义音色 | 指令控制 |
| ---------------------- | ---- | ----- | ---- |
| `cosyvoice-v3.5-plus`  | ✓    | —     | ✓    |
| `cosyvoice-v3.5-flash` | ✓    | —     | ✓    |
| `cosyvoice-v3-plus`    | ✓    | —     | —    |
| `cosyvoice-v3-flash`   | ✓    | —     | ✓    |
  </Accordion>

  <Accordion title="Qwen3-TTS">
| 模型                                  | 流式输出 | 自定义音色 | 指令控制 |
| ----------------------------------- | ---- | ----- | ---- |
| `qwen3-tts-flash`                   | ✓    | —     | —    |
| `qwen3-tts-flash-realtime`          | ✓    | —     | —    |
| `qwen3-tts-instruct-flash`          | ✓    | —     | ✓    |
| `qwen3-tts-instruct-flash-realtime` | ✓    | —     | ✓    |
  </Accordion>

  <Accordion title="MiniMax">
| 模型                         | 流式输出 | 自定义音色 | 指令控制 |
| -------------------------- | ---- | ----- | ---- |
| `MiniMax/speech-2.8-hd`    | ✓    | ✓     | —    |
| `MiniMax/speech-02-hd`     | ✓    | ✓     | —    |
| `MiniMax/speech-2.8-turbo` | ✓    | ✓     | —    |
| `MiniMax/speech-02-turbo`  | ✓    | ✓     | —    |
  </Accordion>

  <Accordion title="声音克隆与设计">
| 模型                                 | 流式输出 | 自定义音色 | 指令控制 |
| ---------------------------------- | ---- | ----- | ---- |
| `qwen3-tts-vc-2026-01-22`          | ✗    | ✓     | —    |
| `qwen3-tts-vc-realtime-2026-01-15` | ✓    | ✓     | —    |
| `qwen3-tts-vd-2026-01-26`          | ✗    | ✓     | —    |
| `qwen3-tts-vd-realtime-2026-01-15` | ✓    | ✓     | —    |
| `qwen-voice-enrollment`            | ✗    | ✓     | —    |
| `qwen-voice-design`                | ✗    | ✓     | —    |
  </Accordion>

  <Accordion title="旧版模型">
    上一代模型。新项目建议使用上述最新版本。

| 模型                                             | 系列                | 流式输出 | 自定义音色 | 指令控制 |
| ---------------------------------------------- | ----------------- | ---- | ----- | ---- |
| `qwen3-tts-flash-2025-11-27`                   | Qwen3-TTS         | ✓    | —     | —    |
| `qwen3-tts-flash-2025-09-18`                   | Qwen3-TTS         | ✓    | —     | —    |
| `qwen3-tts-flash-realtime-2025-11-27`          | Qwen3-TTS         | ✓    | —     | —    |
| `qwen3-tts-flash-realtime-2025-09-18`          | Qwen3-TTS         | ✓    | —     | —    |
| `qwen3-tts-instruct-flash-2026-01-26`          | Qwen3-TTS         | ✓    | —     | ✓    |
| `qwen3-tts-instruct-flash-realtime-2026-01-22` | Qwen3-TTS         | ✓    | —     | ✓    |
| `qwen3-tts-vc-realtime-2025-11-27`             | Voice Cloning     | ✓    | ✓     | —    |
| `qwen3-tts-vd-realtime-2025-12-16`             | Voice Design      | ✓    | ✓     | —    |
| `qwen-tts`                                     | Qwen-TTS          | ✓    | —     | —    |
| `qwen-tts-latest`                              | Qwen-TTS          | ✓    | —     | —    |
| `qwen-tts-2025-05-22`                          | Qwen-TTS          | ✓    | —     | —    |
| `qwen-tts-2025-04-10`                          | Qwen-TTS          | ✓    | —     | —    |
| `qwen-tts-realtime`                            | Qwen-TTS-Realtime | ✓    | —     | —    |
| `qwen-tts-realtime-latest`                     | Qwen-TTS-Realtime | ✓    | —     | —    |
| `qwen-tts-realtime-2025-07-15`                 | Qwen-TTS-Realtime | ✓    | —     | —    |
| `cosyvoice-v2`                                 | CosyVoice         | ✓    | —     | —    |
| `cosyvoice-v1`                                 | CosyVoice         | ✓    | —     | —    |
  </Accordion>
</AccordionGroup>

## 了解更多

<CardGroup cols={2}>
  <Card title="语音合成指南" icon="TextSizeOutlined" href="/developer-guides/speech/tts">
    了解如何通过 API 使用语音合成模型。
  </Card>

  <Card title="实时流式合成指南" icon="TextSizeOutlined" href="/developer-guides/speech/realtime-streaming">
    通过 WebSocket 使用实时语音合成模型。
  </Card>

  <Card title="CosyVoice 音色列表" icon="FileInvoiceOutlined" href="/api-reference/speech-synthesis/cosyvoice/voice-list">
    浏览 CosyVoice 音色库和试听样本。
  </Card>

  <Card title="Qwen-TTS 音色列表" icon="FileInvoiceOutlined" href="/api-reference/speech-synthesis/qwen-tts/voice-list#qwen-tts非实时语音合成音色列表">
    浏览 Qwen-TTS 非流式模型的系统音色。
  </Card>

  <Card title="Qwen-TTS-Realtime 音色列表" icon="FileInvoiceOutlined" href="/api-reference/speech-synthesis/qwen-tts/voice-list#qwen-tts实时语音合成音色列表">
    浏览 Qwen-TTS-Realtime 流式模型的系统音色。
  </Card>

  <Card title="声音克隆" icon="FileInvoiceOutlined" href="/api-reference/speech-synthesis/voice-cloning/create-voice">
    基于音频样本克隆声音。
  </Card>

  <Card title="MiniMax API 参考" icon="FileInvoiceOutlined" href="/api-reference/speech-synthesis/minimax-tts">
    查看 MiniMax 语音合成模型的调用参数。
  </Card>
</CardGroup>
