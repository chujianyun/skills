# TokenDance 词元跳动 文档索引

本文件由 `scripts/sync_wiki_docs.py` 生成。日常问答优先运行 `scripts/search_docs.py`，需要浏览主题结构时再读取本索引。

- 来源：<https://tokendance.space/docs>
- 文档数：91

## 顶层目录

- `开始使用`：13 篇
- `更新与支持`：4 篇
- `模型与协议`：56 篇
- `集成指南`：18 篇

## 目录树

```text
docs/
├── 开始使用
│   ├── 应用与开放能力
│   │   ├── Agent 支付.md
│   │   ├── webhook.md
│   │   ├── 应用归因.md
│   │   └── 开放平台 API.md
│   ├── 快速入门
│   │   ├── 平台介绍.md
│   │   ├── 快速开始.md
│   │   └── 用 AI 接入.md
│   ├── 访问与认证
│   │   ├── API 密钥.md
│   │   └── OAuth 式 API Key 授权.md
│   └── 路由与可用性
│       ├── 会话粘滞.md
│       ├── 供应商路由.md
│       ├── 模型降级.md
│       └── 请求限流.md
├── 更新与支持
│   ├── 产品更新
│   │   ├── 文档更新记录.md
│   │   └── 更新日志.md
│   └── 帮助与支持
│       ├── 常见问题.md
│       └── 联系我们.md
├── 模型与协议
│   ├── 厂商与模型实践
│   │   ├── Kimi
│   │   │   └── Kimi 使用指南.md
│   │   ├── MiniMax
│   │   │   └── MiniMax H3 使用指南.md
│   │   ├── 可灵
│   │   │   └── Kling 使用指南.md
│   │   └── 字节
│   │       ├── Seedance 使用指南.md
│   │       └── Seedream 使用指南.md
│   ├── 多模态协议
│   │   ├── 图像与视频
│   │   │   ├── Grok 视频生成.md
│   │   │   ├── Grsai 图片生成与编辑.md
│   │   │   ├── HappyHorse 视频合成.md
│   │   │   ├── MiniMax 视频生成 v2.md
│   │   │   ├── OpenAI Image Edits.md
│   │   │   ├── OpenAI Image Generations.md
│   │   │   ├── Vidu 参考生视频.md
│   │   │   ├── Vidu 图生视频.md
│   │   │   ├── Vidu 文生视频.md
│   │   │   ├── Vidu 首尾帧视频.md
│   │   │   ├── 可灵 Omni Video.md
│   │   │   ├── 可灵Omni V2.md
│   │   │   ├── 可灵动作控制.md
│   │   │   ├── 可灵图生视频 V2.md
│   │   │   ├── 可灵图生视频.md
│   │   │   ├── 可灵数字人.md
│   │   │   ├── 可灵文生视频 V2.md
│   │   │   ├── 可灵文生视频.md
│   │   │   ├── 可灵视频特效.md
│   │   │   ├── 字节 Ark Image Generations.md
│   │   │   ├── 字节 Seedance Generations.md
│   │   │   ├── 百炼多模态生成.md
│   │   │   ├── 视频超分.md
│   │   │   ├── 视频超分（Seedance 协议）.md
│   │   │   └── 阿里云 Wan3.0 视频生成.md
│   │   ├── 语音
│   │   │   ├── MiniMax T2A v2.md
│   │   │   ├── MiniMax T2A WebSocket.md
│   │   │   ├── MiniMax 声音复刻.md
│   │   │   ├── Qwen-Audio-3.0-ASR-Flash-Streaming.md
│   │   │   ├── Qwen3-ASR-Flash-Realtime.md
│   │   │   ├── Qwen3-ASR-Flash.md
│   │   │   ├── 可灵语音合成.md
│   │   │   ├── 豆包语音合成 WebSocket.md
│   │   │   └── 豆包语音合成.md
│   │   └── 音乐
│   │       ├── 音潮歌曲生成.md
│   │       └── 音潮歌词生成.md
│   ├── 检索与内容处理
│   │   ├── 搜索与网页读取
│   │   │   ├── DeepSeek 网页抓取.md
│   │   │   ├── DeepSeek 网页搜索.md
│   │   │   ├── UniFuncs 实时搜索.md
│   │   │   ├── UniFuncs 网页阅读.md
│   │   │   └── 博查联网搜索.md
│   │   ├── 文本重排
│   │   │   └── 阿里云 Qwen 文本重排.md
│   │   └── 文档解析
│   │       └── 智谱文档解析.md
│   ├── 结构化评估
│   │   └── TypeSafe Jev 结构化评估.md
│   ├── 选择模型与协议
│   │   ├── 协议总览.md
│   │   └── 模型与协议概览.md
│   └── 通用模型协议
│       ├── Anthropic
│       │   └── Anthropic Messages.md
│       ├── Google
│       │   └── Google GenerateContent.md
│       └── OpenAI
│           ├── OpenAI Chat Completions.md
│           ├── OpenAI Embeddings.md
│           └── OpenAI Responses.md
└── 集成指南
    ├── 客户端与平台
    │   ├── Alice.md
    │   ├── Cherry Studio.md
    │   ├── ima.copilot.md
    │   ├── Obsidian.md
    │   ├── QClaw.md
    │   ├── RikkaHub.md
    │   ├── TRAE Work.md
    │   └── Workbuddy 系列.md
    └── 编程与 Agent 工具
        ├── CC-Switch.md
        ├── Claude Code.md
        ├── Cline.md
        ├── Codex.md
        ├── DeepSeek Harness.md
        ├── GitHub Copilot.md
        ├── Hermes Agent.md
        ├── Neovate.md
        ├── OpenCode.md
        └── TRAE IDE.md
```

## 全部文档

| 路径 | 标题 | 摘要 / 关键词 | 来源 |
|---|---|---|---|
| `开始使用/应用与开放能力/Agent 支付.md` | Agent 支付 | 使用 API Key 创建充值会话，并在支付成功后继续调用 | [原文](<https://tokendance.space/docs/agent-payment.md>) |
| `开始使用/应用与开放能力/webhook.md` | webhook | 在异步任务结束时获取来自词元跳动的回调通知 | [原文](<https://tokendance.space/docs/async-webhook.md>) |
| `开始使用/应用与开放能力/应用归因.md` | 应用归因 | 通过 API Key 或单次请求将调用关联到你的应用 | [原文](<https://tokendance.space/docs/app-attribution.md>) |
| `开始使用/应用与开放能力/开放平台 API.md` | 开放平台 API | 通过 API Key 以编程方式管理账户 | [原文](<https://tokendance.space/docs/open-api.md>) |
| `开始使用/快速入门/平台介绍.md` | 平台介绍 | 一个 URL 调用所有大模型 | [原文](<https://tokendance.space/docs/principles.md>) |
| `开始使用/快速入门/快速开始.md` | 快速开始 | 三步即可通过词元跳动调用所有主流大模型 | [原文](<https://tokendance.space/docs/quickstart.md>) |
| `开始使用/快速入门/用 AI 接入.md` | 用 AI 接入 | 一键把接入任务交给 coding agent，并让 AI 自动发现所需文档 | [原文](<https://tokendance.space/docs/ai-integration.md>) |
| `开始使用/访问与认证/API 密钥.md` | API 密钥 | 创建、使用和管理你的 API Key | [原文](<https://tokendance.space/docs/api-keys.md>) |
| `开始使用/访问与认证/OAuth 式 API Key 授权.md` | OAuth 式 API Key 授权 | 通过 Authorization Code + S256 PKCE 让应用获得新 Key | [原文](<https://tokendance.space/docs/api-key-oauth.md>) |
| `开始使用/路由与可用性/会话粘滞.md` | 会话粘滞 | 多轮对话优先回到命中缓存的供应商端点，降低输入成本 | [原文](<https://tokendance.space/docs/session-affinity.md>) |
| `开始使用/路由与可用性/供应商路由.md` | 供应商路由 | 同一模型的多供应商智能路由、自动容错与显式偏好控制 | [原文](<https://tokendance.space/docs/provider-routing.md>) |
| `开始使用/路由与可用性/模型降级.md` | 模型降级 | 当首选模型不可用时自动切换到备选模型 | [原文](<https://tokendance.space/docs/model-fallbacks.md>) |
| `开始使用/路由与可用性/请求限流.md` | 请求限流 | 了解词元跳动的限流机制以及如何应对限流 | [原文](<https://tokendance.space/docs/rate-limits.md>) |
| `更新与支持/产品更新/文档更新记录.md` | 文档更新记录 | 查看厂商与模型实践文档的撰写时间和时效说明 | [原文](<https://tokendance.space/docs/docs-updates.md>) |
| `更新与支持/产品更新/更新日志.md` | 更新日志 | 了解模型、API、控制台和计费等产品变化 | [原文](<https://tokendance.space/docs/changelog.md>) |
| `更新与支持/帮助与支持/常见问题.md` | 常见问题 | 关于词元跳动的常见问题与解答 | [原文](<https://tokendance.space/docs/faq.md>) |
| `更新与支持/帮助与支持/联系我们.md` | 联系我们 | 如有任何问题或建议，欢迎加入交流群 | [原文](<https://tokendance.space/docs/contact.md>) |
| `模型与协议/厂商与模型实践/Kimi/Kimi 使用指南.md` | Kimi 使用指南 | 思考参数、采样约束、工具调用与多轮消息处理 | [原文](<https://tokendance.space/docs/kimi-thinking-models.md>) |
| `模型与协议/厂商与模型实践/MiniMax/MiniMax H3 使用指南.md` | MiniMax H3 使用指南 | 任务输入、参数联动、异步轮询与错误排查 | [原文](<https://tokendance.space/docs/minimax-video-generation.md>) |
| `模型与协议/厂商与模型实践/可灵/Kling 使用指南.md` | Kling 使用指南 | 模型选择、调用差异与官方资料 | [原文](<https://tokendance.space/docs/kling.md>) |
| `模型与协议/厂商与模型实践/字节/Seedance 使用指南.md` | Seedance 使用指南 | Seedance 常用参数、任务类型、异步轮询与错误排查 | [原文](<https://tokendance.space/docs/seedance-generations.md>) |
| `模型与协议/厂商与模型实践/字节/Seedream 使用指南.md` | Seedream 使用指南 | 调用 Seedream 系列图像生成模型 | [原文](<https://tokendance.space/docs/ark-image-generations.md>) |
| `模型与协议/多模态协议/图像与视频/Grok 视频生成.md` | Grok 视频生成 | 文生视频、单图图生、异步查询与下载 | [原文](<https://tokendance.space/docs/protocol-xai-video-generations.md>) |
| `模型与协议/多模态协议/图像与视频/Grsai 图片生成与编辑.md` | Grsai 图片生成与编辑 | 异步提交图片任务、参考图编辑与结果查询 | [原文](<https://tokendance.space/docs/protocol-grsai-generate.md>) |
| `模型与协议/多模态协议/图像与视频/HappyHorse 视频合成.md` | HappyHorse 视频合成 | 通义万相视频生成与编辑 | [原文](<https://tokendance.space/docs/protocol-happyhorse-video-synthesis.md>) |
| `模型与协议/多模态协议/图像与视频/MiniMax 视频生成 v2.md` | MiniMax 视频生成 v2 | MiniMax 新版视频生成协议 | [原文](<https://tokendance.space/docs/protocol-minimax-video-generation-v2.md>) |
| `模型与协议/多模态协议/图像与视频/OpenAI Image Edits.md` | OpenAI Image Edits | 使用 OpenAI 图像编辑协议修改图片 | [原文](<https://tokendance.space/docs/protocol-openai-image-edits.md>) |
| `模型与协议/多模态协议/图像与视频/OpenAI Image Generations.md` | OpenAI Image Generations | 使用 OpenAI 图像生成协议创建图片 | [原文](<https://tokendance.space/docs/protocol-openai-image-generations.md>) |
| `模型与协议/多模态协议/图像与视频/Vidu 参考生视频.md` | Vidu 参考生视频 | 使用参考图保持主体一致性 | [原文](<https://tokendance.space/docs/protocol-vidu-reference2video.md>) |
| `模型与协议/多模态协议/图像与视频/Vidu 图生视频.md` | Vidu 图生视频 | 通过图片和提示词生成视频 | [原文](<https://tokendance.space/docs/protocol-vidu-img2video.md>) |
| `模型与协议/多模态协议/图像与视频/Vidu 文生视频.md` | Vidu 文生视频 | 通过文本提示生成视频 | [原文](<https://tokendance.space/docs/protocol-vidu-text2video.md>) |
| `模型与协议/多模态协议/图像与视频/Vidu 首尾帧视频.md` | Vidu 首尾帧视频 | 根据首帧和尾帧生成视频 | [原文](<https://tokendance.space/docs/protocol-vidu-start-end2video.md>) |
| `模型与协议/多模态协议/图像与视频/可灵 Omni Video.md` | 可灵 Omni Video | 可灵多模态视频生成协议 | [原文](<https://tokendance.space/docs/protocol-kling-omni-video.md>) |
| `模型与协议/多模态协议/图像与视频/可灵Omni V2.md` | 可灵Omni V2 | Kling 4.0 Omni与输入视频计费 | [原文](<https://tokendance.space/docs/protocol-kling-omni-video-v2.md>) |
| `模型与协议/多模态协议/图像与视频/可灵动作控制.md` | 可灵动作控制 | 把动作参考视频中的人物动作与表情迁移到参考图片 | [原文](<https://tokendance.space/docs/protocol-kling-motion-control.md>) |
| `模型与协议/多模态协议/图像与视频/可灵图生视频 V2.md` | 可灵图生视频 V2 | Kling 4.0 图生视频与输入视频计费 | [原文](<https://tokendance.space/docs/protocol-kling-image2video-v2.md>) |
| `模型与协议/多模态协议/图像与视频/可灵图生视频.md` | 可灵图生视频 | 通过图片创建可灵视频任务 | [原文](<https://tokendance.space/docs/protocol-kling-image2video.md>) |
| `模型与协议/多模态协议/图像与视频/可灵数字人.md` | 可灵数字人 | 通过人物图片和音频生成数字人视频 | [原文](<https://tokendance.space/docs/protocol-kling-avatar.md>) |
| `模型与协议/多模态协议/图像与视频/可灵文生视频 V2.md` | 可灵文生视频 V2 | Kling 4.0 文生视频与输入视频计费 | [原文](<https://tokendance.space/docs/protocol-kling-text2video-v2.md>) |
| `模型与协议/多模态协议/图像与视频/可灵文生视频.md` | 可灵文生视频 | 通过文本提示创建可灵视频任务 | [原文](<https://tokendance.space/docs/protocol-kling-text2video.md>) |
| `模型与协议/多模态协议/图像与视频/可灵视频特效.md` | 可灵视频特效 | 按特效模板提交素材并生成视频 | [原文](<https://tokendance.space/docs/protocol-kling-video-effects.md>) |
| `模型与协议/多模态协议/图像与视频/字节 Ark Image Generations.md` | 字节 Ark Image Generations | 火山引擎原生图像生成协议 | [原文](<https://tokendance.space/docs/protocol-ark-image-generations.md>) |
| `模型与协议/多模态协议/图像与视频/字节 Seedance Generations.md` | 字节 Seedance Generations | Seedance 2.0、2.5 系列视频生成 | [原文](<https://tokendance.space/docs/protocol-seedance-generations.md>) |
| `模型与协议/多模态协议/图像与视频/百炼多模态生成.md` | 百炼多模态生成 | Qwen/Wan 图像生成、参考图编辑与短音频识别 | [原文](<https://tokendance.space/docs/protocol-dashscope-multimodal-generation.md>) |
| `模型与协议/多模态协议/图像与视频/视频超分.md` | 视频超分 | 把视频画质增强并超分到 720p、1080p 或 4k | [原文](<https://tokendance.space/docs/protocol-video-enhance.md>) |
| `模型与协议/多模态协议/图像与视频/视频超分（Seedance 协议）.md` | 视频超分（Seedance 协议） | 用支持火山方舟 seedance 协议的客户端把视频超分到 720p、1080p 或 4k | [原文](<https://tokendance.space/docs/protocol-video-enhance-seedance.md>) |
| `模型与协议/多模态协议/图像与视频/阿里云 Wan3.0 视频生成.md` | 阿里云 Wan3.0 视频生成 | 文生、图生、多模态参考和视频编辑 | [原文](<https://tokendance.space/docs/protocol-wan3-video-synthesis.md>) |
| `模型与协议/多模态协议/语音/MiniMax T2A WebSocket.md` | MiniMax T2A WebSocket | WebSocket 流式文本转语音 | [原文](<https://tokendance.space/docs/protocol-minimax-t2a-v2-ws.md>) |
| `模型与协议/多模态协议/语音/MiniMax T2A v2.md` | MiniMax T2A v2 | 同步文本转语音与 SSE 音频流 | [原文](<https://tokendance.space/docs/protocol-minimax-t2a-v2.md>) |
| `模型与协议/多模态协议/语音/MiniMax 声音复刻.md` | MiniMax 声音复刻 | 上传音频并创建可复用音色 | [原文](<https://tokendance.space/docs/protocol-minimax-voice-clone.md>) |
| `模型与协议/多模态协议/语音/Qwen-Audio-3.0-ASR-Flash-Streaming.md` | Qwen-Audio-3.0-ASR-Flash-Streaming | 通过 WebSocket 实时识别音频 | [原文](<https://tokendance.space/docs/protocol-qwen-audio-asr-streaming.md>) |
| `模型与协议/多模态协议/语音/Qwen3-ASR-Flash-Realtime.md` | Qwen3-ASR-Flash-Realtime | 通过 WebSocket 实时识别音频 | [原文](<https://tokendance.space/docs/protocol-qwen-asr-realtime.md>) |
| `模型与协议/多模态协议/语音/Qwen3-ASR-Flash.md` | Qwen3-ASR-Flash | 通过 Chat Completions 识别短音频 | [原文](<https://tokendance.space/docs/protocol-qwen3-asr-flash.md>) |
| `模型与协议/多模态协议/语音/可灵语音合成.md` | 可灵语音合成 | 将文本转换为音频，并供数字人视频引用 | [原文](<https://tokendance.space/docs/protocol-kling-tts.md>) |
| `模型与协议/多模态协议/语音/豆包语音合成 WebSocket.md` | 豆包语音合成 WebSocket | 双向流式输入文本，实时接收二进制音频 | [原文](<https://tokendance.space/docs/protocol-ark-tts-ws.md>) |
| `模型与协议/多模态协议/语音/豆包语音合成.md` | 豆包语音合成 | 单向流式语音合成，SSE 音频流 | [原文](<https://tokendance.space/docs/protocol-ark-tts.md>) |
| `模型与协议/多模态协议/音乐/音潮歌曲生成.md` | 音潮歌曲生成 | 提示词生歌、仿写、扩写、纯音乐与生成中播放 | [原文](<https://tokendance.space/docs/protocol-yinchao-song.md>) |
| `模型与协议/多模态协议/音乐/音潮歌词生成.md` | 音潮歌词生成 | 同步生成歌名与结构化歌词 | [原文](<https://tokendance.space/docs/protocol-yinchao-lyric-generate.md>) |
| `模型与协议/检索与内容处理/搜索与网页读取/DeepSeek 网页抓取.md` | DeepSeek 网页抓取 | 抓取单个网页，返回标题与 Markdown 正文 | [原文](<https://tokendance.space/docs/protocol-deepseek-web-fetch.md>) |
| `模型与协议/检索与内容处理/搜索与网页读取/DeepSeek 网页搜索.md` | DeepSeek 网页搜索 | 实时搜索网页，返回结构化结果与可选正文 | [原文](<https://tokendance.space/docs/protocol-deepseek-web-search.md>) |
| `模型与协议/检索与内容处理/搜索与网页读取/UniFuncs 实时搜索.md` | UniFuncs 实时搜索 | 执行实时联网搜索 | [原文](<https://tokendance.space/docs/protocol-unifuncs-web-search.md>) |
| `模型与协议/检索与内容处理/搜索与网页读取/UniFuncs 网页阅读.md` | UniFuncs 网页阅读 | 读取网页与文档正文 | [原文](<https://tokendance.space/docs/protocol-unifuncs-web-reader.md>) |
| `模型与协议/检索与内容处理/搜索与网页读取/博查联网搜索.md` | 博查联网搜索 | 查询网页、图片和视频搜索结果 | [原文](<https://tokendance.space/docs/protocol-bocha-web-search.md>) |
| `模型与协议/检索与内容处理/文本重排/阿里云 Qwen 文本重排.md` | 阿里云 Qwen 文本重排 | 使用阿里云百炼原生协议重排候选文本 | [原文](<https://tokendance.space/docs/protocol-qwen-text-rerank.md>) |
| `模型与协议/检索与内容处理/文档解析/智谱文档解析.md` | 智谱文档解析 | 将 PDF 或图片解析成结构化内容 | [原文](<https://tokendance.space/docs/protocol-zai-layout-parsing.md>) |
| `模型与协议/结构化评估/TypeSafe Jev 结构化评估.md` | TypeSafe Jev 结构化评估 | 一次请求评估 Noul、Choice、Score 等结构化问题 | [原文](<https://tokendance.space/docs/protocol-typesafe-systemone.md>) |
| `模型与协议/选择模型与协议/协议总览.md` | 协议总览 | 选择协议并查看全部独立调用文档 | [原文](<https://tokendance.space/docs/multi-protocol.md>) |
| `模型与协议/选择模型与协议/模型与协议概览.md` | 模型与协议概览 | 一个 API 访问所有主流大模型 | [原文](<https://tokendance.space/docs/models.md>) |
| `模型与协议/通用模型协议/Anthropic/Anthropic Messages.md` | Anthropic Messages | Claude 对话、视觉输入和工具调用 | [原文](<https://tokendance.space/docs/protocol-anthropic-messages.md>) |
| `模型与协议/通用模型协议/Google/Google GenerateContent.md` | Google GenerateContent | Gemini 文本与多模态调用 | [原文](<https://tokendance.space/docs/protocol-gemini-generate-content.md>) |
| `模型与协议/通用模型协议/OpenAI/OpenAI Chat Completions.md` | OpenAI Chat Completions | 文本对话、流式输出和工具调用 | [原文](<https://tokendance.space/docs/protocol-openai-chat-completions.md>) |
| `模型与协议/通用模型协议/OpenAI/OpenAI Embeddings.md` | OpenAI Embeddings | 文本向量化与批量嵌入 | [原文](<https://tokendance.space/docs/protocol-openai-embeddings.md>) |
| `模型与协议/通用模型协议/OpenAI/OpenAI Responses.md` | OpenAI Responses | Responses API 对话、推理和工具调用 | [原文](<https://tokendance.space/docs/protocol-openai-responses.md>) |
| `集成指南/客户端与平台/Alice.md` | Alice | 在 Alice 中接入词元跳动 | [原文](<https://tokendance.space/docs/alice.md>) |
| `集成指南/客户端与平台/Cherry Studio.md` | Cherry Studio | 在 Cherry Studio 中接入词元跳动 | [原文](<https://tokendance.space/docs/cherry-studio.md>) |
| `集成指南/客户端与平台/Obsidian.md` | Obsidian | 在 Obsidian 中接入词元跳动 | [原文](<https://tokendance.space/docs/obsidian.md>) |
| `集成指南/客户端与平台/QClaw.md` | QClaw | 在 QClaw 中接入词元跳动 | [原文](<https://tokendance.space/docs/qclaw.md>) |
| `集成指南/客户端与平台/RikkaHub.md` | RikkaHub | 在 RikkaHub 中接入词元跳动 | [原文](<https://tokendance.space/docs/rikkahub.md>) |
| `集成指南/客户端与平台/TRAE Work.md` | TRAE Work | 在 TRAE Work 中接入词元跳动 | [原文](<https://tokendance.space/docs/trae-work.md>) |
| `集成指南/客户端与平台/Workbuddy 系列.md` | Workbuddy 系列 | 在 Workbuddy 系列工具中接入词元跳动 | [原文](<https://tokendance.space/docs/workbuddy.md>) |
| `集成指南/客户端与平台/ima.copilot.md` | ima.copilot | 在 ima.copilot 中接入词元跳动 | [原文](<https://tokendance.space/docs/ima.md>) |
| `集成指南/编程与 Agent 工具/CC-Switch.md` | CC-Switch | 在 CC-Switch 中接入词元跳动 | [原文](<https://tokendance.space/docs/cc-switch.md>) |
| `集成指南/编程与 Agent 工具/Claude Code.md` | Claude Code | 在 Claude Code 中接入词元跳动 | [原文](<https://tokendance.space/docs/claude-code.md>) |
| `集成指南/编程与 Agent 工具/Cline.md` | Cline | 在 Cline 中接入词元跳动 | [原文](<https://tokendance.space/docs/cline.md>) |
| `集成指南/编程与 Agent 工具/Codex.md` | Codex | 通过 Responses API 在 Codex 中接入词元跳动 | [原文](<https://tokendance.space/docs/codex.md>) |
| `集成指南/编程与 Agent 工具/DeepSeek Harness.md` | DeepSeek Harness | 在 DeepSeek Harness 中接入词元跳动 | [原文](<https://tokendance.space/docs/deepseek-harness.md>) |
| `集成指南/编程与 Agent 工具/GitHub Copilot.md` | GitHub Copilot | 在 GitHub Copilot 中接入词元跳动 | [原文](<https://tokendance.space/docs/github-copilot.md>) |
| `集成指南/编程与 Agent 工具/Hermes Agent.md` | Hermes Agent | 在 Hermes Agent 中接入词元跳动 | [原文](<https://tokendance.space/docs/hermes-agent.md>) |
| `集成指南/编程与 Agent 工具/Neovate.md` | Neovate | 在 Neovate 中接入词元跳动 | [原文](<https://tokendance.space/docs/neovate.md>) |
| `集成指南/编程与 Agent 工具/OpenCode.md` | OpenCode | 在 OpenCode 中接入词元跳动 | [原文](<https://tokendance.space/docs/opencode.md>) |
| `集成指南/编程与 Agent 工具/TRAE IDE.md` | TRAE IDE | 在 TRAE IDE 中接入词元跳动 | [原文](<https://tokendance.space/docs/trae-ide.md>) |
