> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 概述

> Realtime API 提供多种传输协议，针对性能、延迟、弱网对抗、接入成本等不同需求进行优化

Realtime API 提供多种传输协议，针对性能、延迟、弱网对抗、接入成本等不同需求进行优化，供开发者灵活选择。

Realtime API 支持**AOQ（AI over QUIC）**、**WebRTC**和**WebSocket**三种传输协议，开发者可以根据业务场景灵活选择。

| **维度**  | **AOQ**                   | **WebRTC**      | **WebSocket**           |
| ------- | ------------------------- | --------------- | ----------------------- |
| 适用场景    | AI 多模态实时交互、弱网场景、混合数据传输    | 浏览器端互动、传统音视频通话  | 服务端集成、快速原型验证            |
| 浏览器兼容性  | 不支持                       | 原生支持            | 原生支持                    |
| 接入难度    | 低                         | 中等              | 极低                      |
| 弱网对抗    | 极致                        | 良好              | 差                       |
| 数据类型    | 音视频 + 文本                  | 音视频 + 文本        | 文本/音频/图像                |
| 建连速度    | 快                         | 慢               | 慢                       |
| 回声消除/降噪 | 内置                        | 内置              | 无，需客户端自行处理              |
| AI 场景适配 | 原生为 AI 多模态数据特征深度定制        | 传统设计，AI 场景需额外适配 | 基础，适合纯文本或低实时性场景         |
| 端侧平台支持  | Android / iOS / HarmonyOS | 浏览器、移动端         | 全平台（任何支持 WebSocket 的环境） |

开发者可根据实际需求选择协议方案：

- **AOQ 方案**：适合对延迟、弱网对抗、多模态数据传输有极致要求的 AI 实时交互场景，同时内置回声消除和降噪能力，尤其是移动端原生应用。
- **WebRTC 方案**：适合需要浏览器原生支持、已有 WebRTC 基础设施的传统音视频通话场景，内置回声消除和降噪能力。
- **WebSocket 方案**：适合服务端集成、快速原型验证、对接入门槛要求极低的场景。通过 DashScope SDK 可快速实现实时语音对话。

## 模型支持力度

不同协议对模型的支持情况如下：

| **类型** | **模型**                                                     | **AOQ** | **WebRTC** | **WebSocket** |
| ------ | ---------------------------------------------------------- | ------- | ---------- | ------------- |
| 实时全模态  | qwen3.5-omni-plus-realtime                                 | 支持      | 支持         | 支持            |
| 实时全模态  | qwen3.5-omni-flash-realtime                                | 支持      | 支持         | 支持            |
| 实时语音翻译 | qwen3.5-livetranslate-flash-realtime                       | 支持      | 支持         | 支持            |
| 实时语音识别 | Qwen-Audio-3.0-ASR-Flash-Streaming、Fun-ASR-Realtime系列模型    | 支持      | 不支持        | 支持            |
| 实时语音合成 | CosyVoice系列模型                                              | 支持      | 不支持        | 支持            |
| 实时语音合成 | qwen-audio-3.0-tts-flash、qwen-audio-3.0-tts-plus           | 支持      | 不支持        | 支持            |
| 实时语音对话 | qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash | 支持      | 支持         | 支持            |

<Note>
  模型的名称、上下文、价格、快照版本等信息请参见[千问AI平台控制台](https://platform.qianwenai.com/home)；并发限流条件请参考[限流](/developer-guides/administration/rate-limits)。
</Note>

## 最佳实践

- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](/developer-guides/realtime-api/webrtc-omni-realtime)
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](/developer-guides/realtime-api/aoq-omni-realtime)
- [使用AOQ接入qwen-audio-3.0-realtime-plus实现实时语音对话](/developer-guides/realtime-api/aoq-audio-realtime)
- [使用AOQ接入fun-asr-realtime实现实时语音识别](/developer-guides/realtime-api/aoq-fun-asr-realtime)
