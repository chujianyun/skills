<!-- Offline snapshot of the official Qianwen AI Platform llms.txt. Fetched 2026-08-15T09:38:55+00:00; 579 documents. -->

# 千问AI平台文档

> 千问AI平台提供通义千问大语言模型及多模态 AI 的 API 访问服务，涵盖文本生成、视觉理解、图像生成、视频生成、语音识别、语音合成、语音对话、向量化及重排序等能力，支持 OpenAI 兼容和 DashScope 两种接入方式。

## Token Plan

- [Token Plan 概述](https://platform.qianwenai.com/docs/token-plan/overview.md): Token Plan 是千问AI平台推出的 AI 大模型订阅服务，以 Credits 统一计量，支持多种 AI 编程和智能体工具。提供个人版和团队版两个版本，满足从个人开发者到企业团队的不同需求。
- [Token Plan 个人版](https://platform.qianwenai.com/docs/token-plan/personal/token-plan-personal-overview.md): Token Plan 个人版是面向个人开发者的 AI 大模型订阅服务，以 Credits 统一计量，支持文本、多模态模型及 Harness 工具，适配主流 AI 编程和智能体工具。
- [快速开始](https://platform.qianwenai.com/docs/token-plan/personal/token-plan-personal-quickstart.md): 三步完成 Token Plan 个人版订阅和接入
- [常见问题](https://platform.qianwenai.com/docs/token-plan/personal/token-plan-personal-faq.md): Token Plan 个人版的额度、购买、订阅和接入常见问题。
- [Token Plan 团队版](https://platform.qianwenai.com/docs/token-plan/team/token-plan-team-overview.md): AI 大模型订阅服务
- [快速开始](https://platform.qianwenai.com/docs/token-plan/team/token-plan-team-quickstart.md): 三步完成 Token Plan 团队版订阅和接入
- [团队管理](https://platform.qianwenai.com/docs/token-plan/team/team-management.md): 在 Token Plan 管理平台中添加和管理团队成员、分配和回收席位、配置 SSO 登录、监控 Credits 用量。
- [常见问题](https://platform.qianwenai.com/docs/token-plan/team/token-plan-team-faq.md): Token Plan 团队版常见问题汇总，涵盖购买、使用、计量和性能相关的问题解答。

## 最佳实践

- [接入 Harness 工具](https://platform.qianwenai.com/docs/token-plan/best-practices/built-in-tools.md): 通过 Qwen 模型内置 Harness 工具扩展 AI 编程工具的能力
- [接入多模态生成模型](https://platform.qianwenai.com/docs/token-plan/best-practices/multimodal-generation.md): Token Plan 中的图像生成、视频生成、语音合成模型需通过工具的扩展机制（Skill、Slash Command 或 Agent）接入
- [添加视觉理解能力](https://platform.qianwenai.com/docs/token-plan/best-practices/add-vision-skill.md): 为编程模型添加视觉能力

## 快速入门

- [基于千问AI平台构建应用](https://platform.qianwenai.com/docs/developer-guides/getting-started/introduction.md): 千问AI平台提供文本、视觉、语音及图像视频生成的 AI 模型，兼容 OpenAI SDK，支持函数调用与结构化输出，快速构建智能体应用。
- [首次调用千问API](https://platform.qianwenai.com/docs/developer-guides/getting-started/first-api-call.md): 本文引导您完成千问模型的首次API调用
- [选择模型](https://platform.qianwenai.com/docs/developer-guides/getting-started/model-selection.md): 根据使用场景选择合适的模型
- [计费说明](https://platform.qianwenai.com/docs/developer-guides/getting-started/pricing.md): API 按量计费说明

## 模型

- [文本生成模型](https://platform.qianwenai.com/docs/developer-guides/getting-started/text-generation-models.md): 选择适用于 AI 智能体、聊天机器人、文档处理等场景的模型。
- [文本生成](https://platform.qianwenai.com/docs/developer-guides/text-generation/quickstart.md): 发起第一次文本生成调用
- [前缀续写](https://platform.qianwenai.com/docs/developer-guides/text-generation/partial-mode.md): 从指定前缀继续生成内容
- [长上下文（Qwen-Long）](https://platform.qianwenai.com/docs/developer-guides/text-generation/qwen-long.md): 1000万Token上下文窗口，通过文件上传和引用机制处理超长文档
- [机器翻译（Qwen-MT）](https://platform.qianwenai.com/docs/developer-guides/text-generation/qwen-mt.md): 支持 92 种语言及术语干预
- [角色扮演（Qwen-Character）](https://platform.qianwenai.com/docs/developer-guides/text-generation/role-playing.md): NPC 与虚拟角色
- [数据挖掘（Qwen-Doc）](https://platform.qianwenai.com/docs/developer-guides/text-generation/document-understanding.md): 使用 Qwen-Doc-Turbo 模型从文档中提取结构化数据，支持信息抽取、内容审核、分类打标和摘要生成。
- [深入研究 (Qwen-Deep-Research)](https://platform.qianwenai.com/docs/developer-guides/text-generation/deep-research.md): 自动化多步研究与网络搜索
- [对话分析（Tongyi-Xiaomi-Analysis）](https://platform.qianwenai.com/docs/developer-guides/text-generation/dialogue-analysis.md): 通义晓蜜对话分析专注于对话信息抽取、场景分类、满意度判定等分析需求，擅长处理复杂业务逻辑的质检规则，支持自定义分析标准，具备强大的多轮对话理解和语义推理能力。
- [GUI-Plus 界面交互](https://platform.qianwenai.com/docs/developer-guides/text-generation/gui-interaction.md): GUI-Plus 模型基于屏幕截图和自然语言指令解析用户意图，转换为标准化的 GUI 操作
- [意图理解（Tongyi-Intent-Detect）](https://platform.qianwenai.com/docs/developer-guides/text-generation/intent-detect.md): tongyi-intent-detect-v3 能够在百毫秒级时间内快速、准确地解析用户意图，并选择合适的工具来解决用户的问题。
- [视觉理解模型](https://platform.qianwenai.com/docs/developer-guides/getting-started/vision-models.md): 选择适合图像分析、视频理解、OCR等场景的模型。
- [分析图像与视频](https://platform.qianwenai.com/docs/developer-guides/multimodal/vision.md): 基于视觉输入生成内容
- [文字提取](https://platform.qianwenai.com/docs/developer-guides/multimodal/ocr.md): 文档和表格的 OCR 识别
- [图像生成模型](https://platform.qianwenai.com/docs/developer-guides/getting-started/image-models.md): 选择适合文生图、图片编辑等场景的模型。
- [文生图](https://platform.qianwenai.com/docs/developer-guides/image-generation/text-to-image.md): 根据文本提示词生成图像。
- [图像编辑](https://platform.qianwenai.com/docs/developer-guides/image-generation/image-editing.md): 通过文本指令修改图片
- [图像编辑 - 万相2.7/2.6/2.5](https://platform.qianwenai.com/docs/developer-guides/image-generation/wan-image-editing.md): 万相图像编辑模型系列支持多图输入与多图输出，通过文本指令实现图像编辑、多图融合、主体特征保持、目标检测与分割等能力。
- [万相2.1 通用图像编辑](https://platform.qianwenai.com/docs/developer-guides/image-generation/wan21-image-editing.md): 使用万相-通用图像编辑模型，通过文本指令实现扩图、去水印、风格迁移、指令编辑、局部重绘等多种图像编辑任务。
- [涂鸦作画](https://platform.qianwenai.com/docs/developer-guides/image-generation/sketch-to-image.md): 根据手绘图加上任意文字描述，使用万相-涂鸦作画模型，即可轻松完成涂鸦作画。
- [图像局部重绘](https://platform.qianwenai.com/docs/developer-guides/image-generation/image-inpainting.md): 使用wanx-x-painting模型，根据原始图片、涂抹图和文本描述进行图像局部重绘
- [图像画面扩展](https://platform.qianwenai.com/docs/developer-guides/image-generation/image-out-painting.md): 使用 image-out-painting 模型调整图片尺寸或拓宽画面视野，支持按宽高比、按比例、按方向添加像素以及旋转扩图等多种扩图方式。
- [虚拟模特生成](https://platform.qianwenai.com/docs/developer-guides/image-generation/virtual-model.md): 万相-虚拟模特模型支持在保持真人实拍模特站姿不变的前提下，对拍摄背景图、模特进行替换，快速生成更多模特拍摄图。
- [鞋靴模特](https://platform.qianwenai.com/docs/developer-guides/image-generation/shoe-model.md): 输入模特模板图和鞋靴多视角图片，AI自动完成鞋靴试穿重绘生成。
- [创意海报生成](https://platform.qianwenai.com/docs/developer-guides/image-generation/creative-poster.md): 根据文字描述自动生成海报背景和文字排版，支持多种海报风格。
- [人物实例分割](https://platform.qianwenai.com/docs/developer-guides/image-generation/person-instance-segmentation.md): 识别图像中的不同人物对象，并画出每个对象边界的像素级掩码。
- [图像背景生成 - Wan](https://platform.qianwenai.com/docs/developer-guides/image-generation/background-generation.md): 使用万相图像背景生成模型为商品图像生成高质量背景，支持文本引导、图像引导以及边缘引导元素。
- [图像擦除补全](https://platform.qianwenai.com/docs/developer-guides/image-generation/image-erase-completion.md): 输入原图、待擦除区域掩码图像以及保留区域掩码图像，可以在保留原图背景的同时擦除指定图像区域。
- [视频生成模型](https://platform.qianwenai.com/docs/developer-guides/getting-started/video-models.md): 选择文生视频、图生视频、角色动画等场景的模型。
- [文生视频](https://platform.qianwenai.com/docs/developer-guides/video-generation/text-to-video.md): 通过文本生成视频
- [图生视频：首帧](https://platform.qianwenai.com/docs/developer-guides/video-generation/image-to-video.md): 基于单张图片生成视频
- [图生视频：首尾帧](https://platform.qianwenai.com/docs/developer-guides/video-generation/image-to-video-first-last.md): 根据两帧图片生成过渡视频
- [参考视频生成](https://platform.qianwenai.com/docs/developer-guides/video-generation/reference-video.md): 复刻动作与外观
- [通用视频编辑](https://platform.qianwenai.com/docs/developer-guides/video-generation/video-editing.md): 重绘、延展与编辑
- [语音识别模型](https://platform.qianwenai.com/docs/developer-guides/speech/speech-to-text-models.md): 选择适合实时字幕、音频转写等场景的语音识别模型。
- [实时语音识别](https://platform.qianwenai.com/docs/developer-guides/speech/asr-realtime.md): 将连续音频流实时转写为文字
- [录音文件转写](https://platform.qianwenai.com/docs/developer-guides/speech/asr.md): 将音视频文件转为文字
- [提升识别准确率](https://platform.qianwenai.com/docs/developer-guides/speech/improve-recognition-accuracy.md): 通过预编译热词、即时热词和上下文增强提升语音识别准确率。
- [语音合成模型](https://platform.qianwenai.com/docs/developer-guides/speech/tts-models.md): 选择适合语音合成、声音克隆和声音设计的模型。
- [实时语音合成](https://platform.qianwenai.com/docs/developer-guides/speech/realtime-streaming.md): 实时流式语音合成
- [非实时语音合成](https://platform.qianwenai.com/docs/developer-guides/speech/tts.md): 使用 Qwen3-TTS、CosyVoice 和 MiniMax 进行非实时语音合成
- [声音复刻](https://platform.qianwenai.com/docs/developer-guides/speech/voice-cloning.md): 声音复刻（Voice Cloning）只需提供一段 10~20 秒的音频样本，即可生成高度相似的定制音色，无需模型训练。
- [声音设计](https://platform.qianwenai.com/docs/developer-guides/speech/voice-design.md): 通过文本描述创建自定义音色，无需音频样本，支持 Qwen-TTS、CosyVoice 和 Qwen-Audio-TTS 模型。
- [SSML 与 LaTeX](https://platform.qianwenai.com/docs/developer-guides/speech/ssml.md): 通过 SSML 控制语速、停顿、发音等语音特征，或将 LaTeX 公式转换为自然语音
- [音乐生成](https://platform.qianwenai.com/docs/developer-guides/speech/music-generation.md): Fun-Music 支持通过提示词描述音乐风格和场景，或提供自定义歌词，生成带有男声或女声的中文/英文完整歌曲，也支持生成纯音乐。
- [语音到语音模型](https://platform.qianwenai.com/docs/developer-guides/speech/s2s-models.md): 为'语音输入 → 语音输出'场景（语音对话、语音翻译、同声传译等）选择模型。
- [实时音视频理解](https://platform.qianwenai.com/docs/developer-guides/speech/realtime-multimodal-speech.md): 通过 WebSocket 或 WebRTC 接入 Qwen-Omni 系列模型，实现音频和视频的低延迟实时对话。
- [音视频文件理解](https://platform.qianwenai.com/docs/developer-guides/speech/multimodal-speech.md): 文本+图像/音频输入
- [实时语音对话（Qwen-Audio-Realtime）](https://platform.qianwenai.com/docs/developer-guides/speech/qwen-audio-realtime.md): Qwen-Audio 是端到端实时语音交互大模型，支持低延迟语音对话，适用于语音助手、智能客服、AI 伴侣等场景。
- [实时音视频翻译](https://platform.qianwenai.com/docs/developer-guides/speech/realtime-translation.md): 2.8 秒延迟的流式同声传译
- [音视频文件翻译](https://platform.qianwenai.com/docs/developer-guides/speech/file-translation.md): 支持18种语言翻译
- [概述](https://platform.qianwenai.com/docs/developer-guides/realtime-api/overview.md): Realtime API 提供多种传输协议，针对性能、延迟、弱网对抗、接入成本等不同需求进行优化
- [SDK下载](https://platform.qianwenai.com/docs/developer-guides/realtime-api/sdk-download.md): 下载 AOQ SDK 和 WebSocket SDK
- [Token鉴权](https://platform.qianwenai.com/docs/developer-guides/realtime-api/token-auth.md): AOQ、WebRTC 和 WebSocket 三种协议的鉴权方式
- [接入模型与应用](https://platform.qianwenai.com/docs/developer-guides/realtime-api/connect-model.md): 通过 AOQ、WebRTC 或 WebSocket 接入模型的完整流程
- [通过WebRTC使用qwen3.5-omni-plus-realtime实现实时通话](https://platform.qianwenai.com/docs/developer-guides/realtime-api/webrtc-omni-realtime.md): 通过 WebRTC 协议使用 qwen3.5-omni-plus-realtime 模型实现实时通话
- [通过AOQ使用qwen3.5-omni-plus-realtime实现实时通话](https://platform.qianwenai.com/docs/developer-guides/realtime-api/aoq-omni-realtime.md): 通过 AOQ 协议使用 qwen3.5-omni-plus-realtime 模型实现实时通话
- [使用AOQ接入fun-asr-realtime实现实时语音识别](https://platform.qianwenai.com/docs/developer-guides/realtime-api/aoq-fun-asr-realtime.md): 通过 AOQ 接入 fun-asr-realtime，发送麦克风音频并实时接收语音识别结果。客户端代码以 Android Java 为例，AOQ 支持的其他平台使用相同的接口。
- [使用 AOQ 接入 Qwen-Audio 实现实时语音对话](https://platform.qianwenai.com/docs/developer-guides/realtime-api/aoq-audio-realtime.md): 通过 AOQ 接入 qwen-audio-3.0-realtime-plus，使用服务端 VAD 自动划分轮次，实现低延迟的实时语音对话。客户端代码以 Android Java 为例。
- [连接状态管理](https://platform.qianwenai.com/docs/developer-guides/realtime-api/connection-management.md): AOQ SDK 连接状态图、状态迁移规则和 API
- [媒体流发送管理](https://platform.qianwenai.com/docs/developer-guides/realtime-api/media-stream-control.md): AOQ SDK 媒体流发送的启停控制
- [音频常用功能介绍](https://platform.qianwenai.com/docs/developer-guides/realtime-api/audio-features.md): AOQ SDK 音频采集、播放、编解码配置
- [自定义音频播放](https://platform.qianwenai.com/docs/developer-guides/realtime-api/custom-audio-playback.md): 使用外部播放器播放 AOQ 返回的音频
- [自定义音频采集](https://platform.qianwenai.com/docs/developer-guides/realtime-api/custom-audio-capture.md): 使用外部音频源代替设备麦克风
- [视频常用功能介绍](https://platform.qianwenai.com/docs/developer-guides/realtime-api/video-features.md): AOQ SDK 视频采集、预览、编码配置
- [自定义视频输入](https://platform.qianwenai.com/docs/developer-guides/realtime-api/custom-video-input.md): 使用外部视频源代替设备摄像头
- [SDK简介](https://platform.qianwenai.com/docs/developer-guides/realtime-api/aoq-sdk-intro.md): AOQ SDK 平台支持与架构概述
- [Android SDK](https://platform.qianwenai.com/docs/developer-guides/realtime-api/android-sdk.md): AOQ Android SDK API 参考
- [iOS SDK](https://platform.qianwenai.com/docs/developer-guides/realtime-api/ios-sdk.md): AOQ iOS SDK API 参考
- [HarmonyOS SDK](https://platform.qianwenai.com/docs/developer-guides/realtime-api/harmonyos-sdk.md): AOQ HarmonyOS SDK API 参考
- [向量与重排模型](https://platform.qianwenai.com/docs/developer-guides/getting-started/embedding-models.md): 选择适用于语义搜索、RAG 检索、跨模态匹配和重排序的模型。
- [文本与多模态向量化](https://platform.qianwenai.com/docs/developer-guides/embeddings/embedding.md): 向量化模型可将文本、图像、视频等数据转换为数值向量，用于语义搜索、推荐、聚类、分类、异常检测等下游任务。
- [重排序](https://platform.qianwenai.com/docs/developer-guides/embeddings/reranking.md): 提升搜索精准度
- [函数调用](https://platform.qianwenai.com/docs/developer-guides/tool-calling/function-calling.md): 将模型连接到外部工具
- [联网搜索](https://platform.qianwenai.com/docs/developer-guides/tool-calling/web-search.md): 让模型响应基于实时网络数据——查询天气、股票价格、近期新闻等训练数据截止日期后的内容。
- [网页抓取](https://platform.qianwenai.com/docs/developer-guides/tool-calling/web-scraping.md): 抓取 URL 内容作为上下文
- [代码解释器](https://platform.qianwenai.com/docs/developer-guides/tool-calling/code-interpreter.md): 在沙箱中运行 Python 代码
- [图片搜索](https://platform.qianwenai.com/docs/developer-guides/tool-calling/image-search.md): 通过 Responses API 搜索图片
- [PDF理解](https://platform.qianwenai.com/docs/developer-guides/tool-calling/pdf-understanding.md): PDF文件通过VL模型解析
- [MCP](https://platform.qianwenai.com/docs/developer-guides/tool-calling/mcp.md): 在对话中使用外部工具
- [结构化输出](https://platform.qianwenai.com/docs/developer-guides/text-generation/structured-output.md): 让模型稳定返回合法 JSON，并可通过 JSON Schema 精确约束输出结构
- [思考模式](https://platform.qianwenai.com/docs/developer-guides/text-generation/thinking.md): 通过逐步推理解决复杂任务
- [批量调用](https://platform.qianwenai.com/docs/developer-guides/text-generation/batch.md): 异步批量处理请求，费用低至实时调用的 50%
- [批量推理](https://platform.qianwenai.com/docs/developer-guides/text-generation/batch-chat.md): 同步等待结果的批量对话接口，费用低至实时调用的 50%
- [DeepSeek-千问AI平台](https://platform.qianwenai.com/docs/developer-guides/third-party-models/deepseek.md): 通过OpenAI兼容接口或DashScope SDK调用千问AI平台提供的DeepSeek系列模型。
- [DeepSeek-硅基流动](https://platform.qianwenai.com/docs/developer-guides/third-party-models/deepseek-siliconflow.md): 本文档介绍如何在千问AI平台平台通过OpenAI兼容接口或DashScope SDK调用硅基流动提供的DeepSeek系列模型。
- [DeepSeek-快手万擎](https://platform.qianwenai.com/docs/developer-guides/third-party-models/deepseek-kuaishou.md): 本文档介绍如何在千问AI平台平台调用快手万擎直供的 DeepSeek 系列模型推理服务。
- [Kimi-千问AI平台](https://platform.qianwenai.com/docs/developer-guides/third-party-models/kimi.md): 本文档介绍如何调用千问AI平台部署的 Kimi 模型推理服务。
- [Kimi-月之暗面](https://platform.qianwenai.com/docs/developer-guides/third-party-models/kimi-moonshot.md): 本文档介绍如何在千问AI平台平台调用月之暗面（Moonshot AI）直供的模型推理服务。
- [GLM-千问AI平台](https://platform.qianwenai.com/docs/developer-guides/third-party-models/glm.md): 通过API调用 GLM 系列模型进行对话。
- [GLM-智谱](https://platform.qianwenai.com/docs/developer-guides/third-party-models/glm-zhipu.md): 本文档介绍如何在千问AI平台平台调用智谱（ZHIPU AI）直供的模型推理服务。
- [MiMo-小米](https://platform.qianwenai.com/docs/developer-guides/third-party-models/mimo.md): 通过API调用小米直供的 MiMo 系列模型进行对话。
- [MiniMax-千问AI平台](https://platform.qianwenai.com/docs/developer-guides/third-party-models/minimax.md): 本文档介绍如何调用千问AI平台部署的 MiniMax 模型推理服务。
- [MiniMax-稀宇科技](https://platform.qianwenai.com/docs/developer-guides/third-party-models/minimax-minimaxi.md): 本文档介绍如何在千问AI平台平台调用稀宇科技（简称MiniMax）直供的模型推理服务。
- [Stepfun-阶跃星辰](https://platform.qianwenai.com/docs/developer-guides/third-party-models/stepfun.md): 本文档介绍如何在千问AI平台调用阶跃星辰（Stepfun）直供的 Step 系列模型推理服务。
- [Vidu视频生成Prompt指南](https://platform.qianwenai.com/docs/developer-guides/third-party-models/vidu-prompt-guide.md): 本文涵盖从提示词公式、关键词词典到进阶案例的完整实践方法。

## 运行与扩展

- [多轮对话](https://platform.qianwenai.com/docs/developer-guides/run-and-scale/multi-turn.md): 管理对话上下文
- [上下文缓存](https://platform.qianwenai.com/docs/developer-guides/run-and-scale/context-cache.md): 通过前缀复用降低成本
- [流式输出](https://platform.qianwenai.com/docs/developer-guides/run-and-scale/streaming.md): 逐 token 实时接收模型生成的文本。

## 上线准备

- [模型调优](https://platform.qianwenai.com/docs/developer-guides/accuracy-tuning/overview.md): 在千问AI平台上提升文本、图像、视频、语音和视觉模型的输出准确性与一致性
- [文本生成微调](https://platform.qianwenai.com/docs/developer-guides/accuracy-tuning/text-generation.md): 设计高效的提示词
- [图像生成微调](https://platform.qianwenai.com/docs/developer-guides/accuracy-tuning/image-generation.md): 提升 Wan 图像生成效果
- [视频生成微调](https://platform.qianwenai.com/docs/developer-guides/accuracy-tuning/video-generation.md): 优化视频生成提示词的方法与技巧
- [语音识别最佳实践](https://platform.qianwenai.com/docs/developer-guides/accuracy-tuning/speech-recognition.md): 通过音频质量优化、词汇定制和后处理纠错，提升语音识别准确率。
- [显式缓存最佳实践](https://platform.qianwenai.com/docs/developer-guides/accuracy-tuning/explicit-cache-best-practice.md): 显式缓存通过在请求中添加缓存标记，确保相同输入内容确定性命中缓存，从而显著降低成本和延迟。
- [Token 计算](https://platform.qianwenai.com/docs/developer-guides/run-and-scale/token-counting.md): 了解文本、视觉和音频模型的 Token 用量及计费方式
- [延迟优化](https://platform.qianwenai.com/docs/developer-guides/run-and-scale/latency-optimization.md): 降低千问AI平台文本、图像、视频和语音模型的响应延迟
- [成本优化](https://platform.qianwenai.com/docs/developer-guides/run-and-scale/cost-optimization.md): 在保证输出质量的同时，降低文本、图像、视频和语音 API 调用费用
- [安全](https://platform.qianwenai.com/docs/developer-guides/run-and-scale/safety.md): 覆盖所有模态的内容审核、输入/输出防护与负责任的 AI 实践
- [异步任务管理](https://platform.qianwenai.com/docs/developer-guides/run-and-scale/async-task-management.md): 千问AI平台的两种异步模式：Task API 用于媒体生成，Batch API 用于大规模文本处理

## 管理

- [API Key](https://platform.qianwenai.com/docs/developer-guides/administration/api-keys.md): 创建和管理 API Key
- [业务空间](https://platform.qianwenai.com/docs/developer-guides/administration/workspace.md): 管理模型权限、速率限制和 API Key
- [限流](https://platform.qianwenai.com/docs/developer-guides/administration/rate-limits.md): 了解和管理 API 限流

## 集成

- [OpenClaw](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/openclaw.md): 在 OpenClaw 中使用千问AI平台模型
- [Hermes Agent](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/hermes-agent.md): 在 Hermes Agent 中使用千问AI平台模型
- [Claude Code](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/claude-code.md): 在 Claude Code 中使用千问AI平台模型
- [OpenCode](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/opencode.md): 在 OpenCode 中使用千问AI平台模型
- [Cursor](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/cursor.md): 在 Cursor 中使用千问AI平台模型
- [Codex](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/codex.md): 在 Codex 中使用千问AI平台模型
- [Qwen Code](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/qwen-code.md): 在 Qwen Code 中使用千问AI平台模型
- [QwenPaw](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/qwenpaw.md): 在 QwenPaw 中使用千问AI平台模型
- [Cherry Studio](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/cherry-studio.md): 在 Cherry Studio 中使用千问AI平台模型
- [Chatbox](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/chatbox.md): 在 Chatbox 中使用千问AI平台模型
- [Cline](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/cline.md): 在 Cline 中使用千问AI平台模型
- [Qoder](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/qoder.md): 在 Qoder 中使用千问AI平台模型
- [Qoder CN（原 Lingma）](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/lingma.md): 在 Qoder CN IDE 中使用千问AI平台模型
- [Kilo CLI](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/kilo-cli.md): 在 Kilo CLI 中使用千问AI平台模型
- [Postman](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/postman.md): API 测试工具
- [Dify](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/dify.md): 低代码 LLM 应用平台
- [其他 AI 工具](https://platform.qianwenai.com/docs/developer-guides/clients-and-developer-tools/other-tools.md): 兼容 OpenAI/Anthropic 协议的工具
- [用量分析](https://platform.qianwenai.com/docs/developer-guides/integrations/mlops-observability.md): 查看 Token 消耗、请求日志与性能指标

## 模型生产

- [数据集概览](https://platform.qianwenai.com/docs/developer-guides/datasets/overview.md): 在千问AI平台上管理用于模型微调和模型评测的数据集。
- [创建数据集](https://platform.qianwenai.com/docs/developer-guides/datasets/create-dataset.md): 上传训练数据或评测数据到千问AI平台，用于模型微调或模型评测。
- [管理数据集](https://platform.qianwenai.com/docs/developer-guides/datasets/manage-datasets.md): 在千问AI平台平台上发布、编辑和删除数据集。
- [模型微调概览](https://platform.qianwenai.com/docs/developer-guides/fine-tuning/overview.md): 通过千问AI平台的 SFT、DPO、CPT 微调 Qwen 模型，支持 LoRA 和全参训练模式。
- [创建微调任务](https://platform.qianwenai.com/docs/developer-guides/fine-tuning/create-fine-tuning-job.md): 在千问AI平台控制台中创建模型微调任务的步骤指南。
- [管理微调任务](https://platform.qianwenai.com/docs/developer-guides/fine-tuning/manage-fine-tuning-jobs.md): 在千问AI平台控制台中监控、管理和部署微调任务。
- [超参数参考](https://platform.qianwenai.com/docs/developer-guides/fine-tuning/hyperparameters.md): 千问AI平台微调超参数的参考说明与调参建议。
- [微调训练计费](https://platform.qianwenai.com/docs/developer-guides/fine-tuning/training-billing.md): 千问AI平台模型微调的训练计费规则、公式与各模型训练单价。
- [自定义模型概览](https://platform.qianwenai.com/docs/developer-guides/custom-models/overview.md): 查看和管理您在千问AI平台上微调的模型。
- [模型评测概览](https://platform.qianwenai.com/docs/developer-guides/evaluation/overview.md): 通过千问AI平台的模型评测功能，从多维度量化模型表现，支持 LLM 自动打分与人工标注两种方式。
- [评测维度](https://platform.qianwenai.com/docs/developer-guides/evaluation/evaluation-dimensions.md): 在千问AI平台上创建和管理评测维度，支持 LLM 数值打分、LLM 分类判定和人工标注三种类型。
- [评测任务](https://platform.qianwenai.com/docs/developer-guides/evaluation/evaluation-tasks.md): 在千问AI平台上创建评测任务，选择数据来源、评测模型和评测维度，量化模型输出质量。
- [创建部署](https://platform.qianwenai.com/docs/developer-guides/deployment/overview.md): 在千问AI平台上部署自定义模型，为生产工作负载创建专属推理服务。
- [管理部署](https://platform.qianwenai.com/docs/developer-guides/deployment/manage-deployments.md): 在千问AI平台上监控和管理模型部署的生命周期。

## 安全与合规

- [数据安全与隐私](https://platform.qianwenai.com/docs/developer-guides/security-compliance/data-security.md): 千问AI平台如何保护您的数据
- [审计与访问日志](https://platform.qianwenai.com/docs/developer-guides/security-compliance/audit-logs.md): 追踪 API 使用情况，满足合规要求
- [模型备案信息公示](https://platform.qianwenai.com/docs/developer-guides/security-compliance/model-filing.md): 千问AI平台接入大模型的算法备案号与大模型备案号公示
- [开源模型协议条款说明](https://platform.qianwenai.com/docs/developer-guides/security-compliance/open-source-model-terms.md): 千问AI平台平台开源模型的开源协议及许可证条款说明

## 开始使用

- [获取 API Key](https://platform.qianwenai.com/docs/api-reference/preparation/api-key.md): 使用模型的第一步
- [配置 API Key](https://platform.qianwenai.com/docs/api-reference/preparation/export-api-key-env.md): 避免在代码中硬编码密钥
- [安装 SDK](https://platform.qianwenai.com/docs/api-reference/preparation/install-sdk.md): Python、Java、Node.js 和 Go 环境配置
- [CLI 工具](https://platform.qianwenai.com/docs/api-reference/preparation/cli.md): 千问AI平台管理命令行工具，用于管理模型目录、账号、用量、账单、订阅和支持工单
- [错误信息](https://platform.qianwenai.com/docs/api-reference/preparation/error-messages.md): API 错误码参考

## 对话模型

- [OpenAI Chat API 参考](https://platform.qianwenai.com/docs/api-reference/chat/openai-chat.md): OpenAI 兼容的 Chat API
- [创建响应](https://platform.qianwenai.com/docs/api-reference/chat/openai-responses.md): 兼容 Responses API
- [获取响应](https://platform.qianwenai.com/docs/api-reference/chat/retrieve-response.md): 根据 Response ID 获取一个已完成的模型响应
- [删除响应](https://platform.qianwenai.com/docs/api-reference/chat/delete-response.md): 根据 Response ID 删除一个已存储的模型响应
- [获取输入项列表](https://platform.qianwenai.com/docs/api-reference/chat/list-input-items.md): 获取生成指定 Response 时所使用的输入项列表
- [Anthropic Messages API 参考](https://platform.qianwenai.com/docs/api-reference/chat/anthropic.md): 通过 Anthropic SDK 调用 Qwen 模型
- [DashScope API 参考](https://platform.qianwenai.com/docs/api-reference/chat/dashscope.md): 原生 SDK 与 HTTP API

## 图像生成 API

- [Qwen — 同步图像生成](https://platform.qianwenai.com/docs/api-reference/image-generation/qwen-text-to-image.md): 同步图像生成
- [Qwen — 异步图像生成（3.0系列）](https://platform.qianwenai.com/docs/api-reference/image-generation/qwen-text-to-image-30-async.md): qwen-image-3.0 系列模型的异步图像生成接口
- [Qwen — 异步图像生成](https://platform.qianwenai.com/docs/api-reference/image-generation/qwen-text-to-image-async.md): 异步图像生成
- [Qwen — 查询图像生成结果](https://platform.qianwenai.com/docs/api-reference/image-generation/qwen-text-to-image-task-query.md): 查询图像生成任务状态
- [Z-Image](https://platform.qianwenai.com/docs/api-reference/image-generation/z-image.md): 轻量快速图像生成
- [Wan v2 — 同步调用](https://platform.qianwenai.com/docs/api-reference/image-generation/wan-text-to-image-v2/synchronous.md): Wan 文生图同步接口
- [Wan v2 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/wan-text-to-image-v2/create-task.md): Wan 异步图像生成
- [Wan v2 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/wan-text-to-image-v2/query-result.md): 查询 Wan 图像生成任务状态
- [wanx-v1 — 创建文生图任务](https://platform.qianwenai.com/docs/api-reference/image-generation/wanx-v1-text-to-image/create-task.md): wanx-v1 异步图像生成
- [wanx-v1 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/wanx-v1-text-to-image/query-result.md): 查询 wanx-v1 图像生成任务状态
- [Qwen](https://platform.qianwenai.com/docs/api-reference/image-generation/qwen-image-editing.md): 通过文本编辑图片
- [Wan 2.7 — 同步调用](https://platform.qianwenai.com/docs/api-reference/image-generation/wan27-image-gen-edit/synchronous.md): Wan 2.7 同步图像生成与编辑
- [Wan 2.7 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/wan27-image-gen-edit/create-task.md): Wan 2.7 异步图像生成与编辑
- [Wan 2.7 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/wan27-image-gen-edit/query-result.md): 查询 Wan 2.7 图像任务状态
- [Wan 2.6 — 同步调用](https://platform.qianwenai.com/docs/api-reference/image-generation/wan26-image-gen-edit/synchronous.md): Wan 2.6 同步图像生成与编辑
- [Wan 2.6 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/wan26-image-gen-edit/create-task.md): Wan 2.6 异步图像生成与编辑
- [Wan 2.6 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/wan26-image-gen-edit/query-result.md): 查询 Wan 2.6 图像任务状态
- [Wan 2.5 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/wan25-general-image-editing/create-task.md): 异步 Wan 2.5 图像编辑
- [Wan 2.5 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/wan25-general-image-editing/query-result.md): 查询 Wan 2.5 图像编辑任务状态
- [Wan 2.1 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/wan21-general-image-editing/create-task.md): 异步 Wan 2.1 通用图像编辑
- [Wan 2.1 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/wan21-general-image-editing/query-result.md): 查询 Wan 2.1 图像编辑任务状态
- [创建图像生成任务](https://platform.qianwenai.com/docs/api-reference/image-generation/kling-image-generation/create-task.md): 提交可灵图像生成任务（文生图或参考图生图），获取 task_id 用于后续查询。
- [查询图像生成任务结果](https://platform.qianwenai.com/docs/api-reference/image-generation/kling-image-generation/query-result.md): 通过 task_id 轮询查询可灵图像生成任务的执行状态与生成图像。
- [可灵-主体ID列表](https://platform.qianwenai.com/docs/api-reference/image-generation/kling-subject-id-list.md): 可灵（Kling）图像生成和视频生成API支持的主体ID（element_id）完整列表及参考图。
- [Vidu -- 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/vidu-image-generation/create-task.md): 使用 Vidu 模型提交图像生成任务（文生图/参考图生图），异步生成图像。
- [Vidu -- 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/vidu-image-generation/query-result.md): 查询 Vidu 图像生成任务的状态与结果。
- [万相涂鸦作画 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/wanx-sketch-to-image/create-task.md): 提交涂鸦作画任务，获取任务 ID。
- [万相涂鸦作画 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/wanx-sketch-to-image/query-result.md): 通过任务 ID 查询涂鸦作画任务的状态和结果。
- [Wanx — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/wanx-x-painting/create-task.md): 异步 wanx-x-painting 图像局部重绘
- [Wanx — 查询局部重绘结果](https://platform.qianwenai.com/docs/api-reference/image-generation/wanx-x-painting/query-result.md): 查询 wanx-x-painting 图像局部重绘任务状态
- [人像风格重绘 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/wanx-style-repaint/create-task.md): 异步人像风格重绘
- [人像风格重绘 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/wanx-style-repaint/query-result.md): 查询人像风格重绘任务状态
- [图像画面扩展 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/image-out-painting/create-task.md): 创建图像画面扩展异步任务
- [图像画面扩展 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/image-out-painting/query-result.md): 查询图像画面扩展任务状态
- [虚拟模特 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/virtual-model/create-task.md): 提交虚拟模特试衣任务
- [虚拟模特 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/virtual-model/query-result.md): 查询虚拟模特任务的状态和结果
- [鞋靴模特 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/shoe-model/create-task.md): 异步鞋靴模特图像生成
- [鞋靴模特 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/shoe-model/query-result.md): 查询鞋靴模特图像生成任务状态
- [创意海报 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/creative-poster/create-task.md): 创意海报异步生成
- [创意海报 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/creative-poster/query-result.md): 查询创意海报生成任务状态
- [人物实例分割 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/person-instance-segmentation/create-task.md): 提交人物实例分割任务
- [人物实例分割 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/person-instance-segmentation/query-result.md): 查询人物实例分割任务的状态和结果
- [图像背景生成 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/background-generation/create-task.md): 提交图像背景生成异步任务
- [图像背景生成 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/background-generation/query-result.md): 查询图像背景生成任务的状态和结果
- [图像擦除补全 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/image-erase-completion/create-task.md): 异步提交图像擦除补全任务
- [图像擦除补全 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/image-erase-completion/query-result.md): 根据任务ID查询异步擦除补全任务的状态和结果
- [AI试衣 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/ai-tryon/create-task.md): 提交AI试衣任务
- [AI试衣 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/ai-tryon/query-result.md): 查询AI试衣任务的状态和结果
- [AI试衣精修 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/aitryon-refiner/create-task.md): 提交AI试衣-图片精修任务
- [AI试衣精修 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/aitryon-refiner/query-result.md): 查询AI试衣-图片精修任务的状态和结果
- [AI试衣-图片分割](https://platform.qianwenai.com/docs/api-reference/image-generation/aitryon-parsing.md): 从模特图或 AI 试衣图中分割出服装区域，支持上装、下装、连衣裙等类型
- [FaceChain — 图像检测](https://platform.qianwenai.com/docs/api-reference/image-generation/facechain-generation/facechain-face-detect.md): 检测图像中是否包含符合要求的人脸
- [人物形象训练 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/facechain-finetune/create-task.md): 提交 FaceChain 人物形象训练任务
- [人物形象训练 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/facechain-finetune/query-result.md): 查询 FaceChain 人物形象训练任务的状态和结果
- [人物写真生成 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/facechain-generation/create-task.md): 提交FaceChain人物写真生成任务
- [人物写真生成 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/facechain-generation/query-result.md): 查询FaceChain人物写真生成任务的状态和结果
- [文字变形 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/wordart-semantic/create-task.md): 提交文字变形异步任务
- [文字变形 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/wordart-semantic/query-result.md): 查询文字变形任务状态
- [创意文字纹理 — 创建任务](https://platform.qianwenai.com/docs/api-reference/image-generation/wordart-texture/create-task.md): 提交创意文字纹理生成异步任务
- [创意文字纹理 — 查询结果](https://platform.qianwenai.com/docs/api-reference/image-generation/wordart-texture/query-result.md): 查询创意文字纹理生成任务的状态和结果

## 视频生成 API

- [wan3.0-video 视频生成](https://platform.qianwenai.com/docs/api-reference/video-generation/wan30-video/create-task.md): wan3.0-video 全能参考视频生成模型。支持文生视频、首帧/首尾帧生视频、全能参考生视频、有声视频等能力。邀测中。
- [wan3.0-video 查询任务结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan30-video/query-result.md): 查询 wan3.0-video 视频生成任务的状态和结果。
- [HappyHorse -- 图生视频（首帧）](https://platform.qianwenai.com/docs/api-reference/video-generation/happyhorse-image-to-video/create-task.md): 提交 HappyHorse 图生视频任务（基于首帧）
- [HappyHorse -- 查询图生视频结果](https://platform.qianwenai.com/docs/api-reference/video-generation/happyhorse-image-to-video/query-result.md): 查询 HappyHorse 图生视频任务状态
- [Wan 2.7 — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/wan27-image-to-video/create-task.md): 提交图生视频任务（wan2.7）
- [Wan 2.7 — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan27-image-to-video/query-result.md): 查询 Wan 2.7 图生视频任务状态
- [Wan — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-image-to-video-first-frame/create-task.md): 提交图生视频任务
- [Wan — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-image-to-video-first-frame/query-result.md): 查询视频生成任务状态
- [Wan — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-image-to-video-first-last-frames/create-task.md): 提交首尾帧图生视频任务
- [Wan — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-image-to-video-first-last-frames/query-result.md): 查询视频生成任务状态
- [万相-视频特效列表](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-image-to-video-first-frame/video-effects.md): 万相视频特效模板完整列表，包含首帧和首尾帧模型支持的所有特效模板参数值、支持模型及输入图像建议。
- [Vidu — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/vidu-image-to-video/create-task.md): 提交一个基于首帧图像的 Vidu 图生视频任务。
- [Vidu — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/vidu-image-to-video/query-result.md): 查询 Vidu 图生视频任务的状态和结果。
- [Vidu — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/vidu-image-to-video-first-frame/create-task.md): 基于首帧图片提交 Vidu 图生视频异步任务
- [Vidu — 查询图生视频任务结果（基于首帧）](https://platform.qianwenai.com/docs/api-reference/video-generation/vidu-image-to-video-first-frame/query-result.md): 查询 Vidu 图生视频（基于首帧）任务状态，获取生成的视频
- [Vidu — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/vidu-start-end-to-video/create-task.md): 提交首尾帧生视频任务，使用 Vidu 模型基于首帧和尾帧图像生成过渡视频。
- [Vidu — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/vidu-start-end-to-video/query-result.md): 查询 Vidu 首尾帧生视频任务的状态与结果。
- [爱诗 PixVerse — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-image-to-video/create-task.md): 提交 PixVerse 图生视频任务
- [爱诗 PixVerse — 查询图生视频任务结果](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-image-to-video/query-result.md): 查询 PixVerse 图生视频任务状态
- [PixVerse — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-image-to-video-first-last/create-task.md): 提交 PixVerse 首尾帧图生视频任务
- [PixVerse — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-image-to-video-first-last/query-result.md): 查询 PixVerse 首尾帧图生视频任务状态
- [爱诗 PixVerse — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-image-to-video-first-frame/create-task.md): 基于首帧图片提交爱诗 PixVerse 图生视频异步任务
- [爱诗 PixVerse — 查询图生视频任务结果（基于首帧）](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-image-to-video-first-frame/query-result.md): 查询爱诗 PixVerse 图生视频（基于首帧）任务状态，获取生成的视频
- [HappyHorse -- 参考生视频](https://platform.qianwenai.com/docs/api-reference/video-generation/happyhorse-reference-to-video/create-task.md): 提交 HappyHorse 参考生视频任务
- [HappyHorse -- 查询参考生视频结果](https://platform.qianwenai.com/docs/api-reference/video-generation/happyhorse-reference-to-video/query-result.md): 查询 HappyHorse 参考生视频任务状态
- [Wan 2.7 — 参考素材生成视频](https://platform.qianwenai.com/docs/api-reference/video-generation/wan27-reference-to-video/create-task.md): 提交 Wan 2.7 参考素材生成视频任务
- [Wan 2.7 — 查询参考素材生成视频结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan27-reference-to-video/query-result.md): 查询 Wan 2.7 参考素材生成视频任务状态
- [Wan 2.6 — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-reference-to-video/create-task.md): 提交参考视频生成任务
- [Wan 2.6 — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-reference-to-video/query-result.md): 查询视频生成任务状态
- [PixVerse — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-reference-to-video/create-task.md): 提交 PixVerse 参考生视频任务
- [PixVerse — 查询参考生视频结果](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-reference-to-video/query-result.md): 查询 PixVerse 参考生视频任务状态
- [Vidu — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/vidu-reference-to-video/create-task.md): 使用 Vidu 模型提交参考视频生成任务。
- [Vidu — 查询参考视频生成结果](https://platform.qianwenai.com/docs/api-reference/video-generation/vidu-reference-to-video/query-result.md): 查询 Vidu 参考视频生成任务的状态和结果。
- [HappyHorse -- 文生视频](https://platform.qianwenai.com/docs/api-reference/video-generation/happyhorse-text-to-video/create-task.md): 提交 HappyHorse 文生视频任务
- [HappyHorse -- 查询文生视频结果](https://platform.qianwenai.com/docs/api-reference/video-generation/happyhorse-text-to-video/query-result.md): 查询 HappyHorse 文生视频任务状态
- [Wan 2.7 — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/wan27-text-to-video/create-task.md): 提交文本生成视频任务（wan2.7）
- [Wan 2.7 — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan27-text-to-video/query-result.md): 查询 Wan 2.7 文生视频任务状态
- [Wan — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-text-to-video/create-task.md): 提交文生视频任务（wan2.6 及更早版本）
- [Wan — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-text-to-video/query-result.md): 查询视频生成任务状态（wan2.6 及更早版本）
- [爱诗 PixVerse — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-text-to-video/create-task.md): 提交爱诗 PixVerse 文生视频异步任务
- [爱诗 PixVerse — 查询文生视频任务结果](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-text-to-video/query-result.md): 查询爱诗 PixVerse 文生视频任务状态，获取生成的视频
- [Vidu — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/vidu-text-to-video/create-task.md): 使用 Vidu 模型提交文生视频任务，异步生成视频。
- [Vidu — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/vidu-text-to-video/query-result.md): 查询 Vidu 文生视频任务的状态与生成结果。
- [HappyHorse -- 视频编辑](https://platform.qianwenai.com/docs/api-reference/video-generation/happyhorse-video-editing/create-task.md): 提交 HappyHorse 视频编辑任务
- [HappyHorse -- 查询视频编辑结果](https://platform.qianwenai.com/docs/api-reference/video-generation/happyhorse-video-editing/query-result.md): 查询 HappyHorse 视频编辑任务状态
- [Wan 2.7 — 视频编辑](https://platform.qianwenai.com/docs/api-reference/video-generation/wan27-video-editing/create-task.md): 提交视频编辑任务（wan2.7）
- [Wan 2.7 — 查询视频编辑结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan27-video-editing/query-result.md): 查询 Wan 2.7 视频编辑任务状态
- [Wan — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-general-video-editing/create-task.md): 提交视频编辑任务
- [Wan — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-general-video-editing/query-result.md): 查询视频编辑任务状态
- [爱诗 PixVerse — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-upscale/create-task.md): 提交 PixVerse 视频超清任务
- [爱诗 PixVerse — 查询视频超清任务结果](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-upscale/query-result.md): 查询 PixVerse 视频超清任务状态
- [可灵视频生成 — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/kling-video-generation/create-task.md): 提交可灵视频生成异步任务
- [可灵视频生成 — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/kling-video-generation/query-result.md): 查询可灵视频生成任务状态并获取视频
- [可灵-主体ID列表](https://platform.qianwenai.com/docs/api-reference/image-generation/kling-subject-id-list.md): 可灵（Kling）图像生成和视频生成API支持的主体ID（element_id）完整列表及参考图。
- [爱诗 PixVerse — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-motioncontrol/create-task.md): 提交 PixVerse 视频动作模仿任务
- [爱诗 PixVerse — 查询视频动作模仿任务结果](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-motioncontrol/query-result.md): 查询 PixVerse 视频动作模仿任务状态
- [Wan — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-image-to-animation/create-task.md): 提交动画生成任务
- [Wan — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-image-to-animation/query-result.md): 查询动画生成状态
- [Wan — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-video-character-swap/create-task.md): 提交视频角色替换任务
- [Wan — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-video-character-swap/query-result.md): 查询视频人物换脸任务状态
- [Wan 数字人图像检测](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-s2v/wan-s2v-detect.md): 检测图像是否符合 wan2.2-s2v 视频生成模型的人物图像规格要求
- [万相数字人 — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-s2v/create-task.md): 基于单张图片和音频，异步生成数字人视频
- [万相数字人 — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/wan-s2v/query-result.md): 查询 wan2.2-s2v 数字人视频生成任务状态和结果
- [AnimateAnyone — 图像检测](https://platform.qianwenai.com/docs/api-reference/video-generation/animate-anyone/wan-aa-detect.md): 检测图像是否符合 AnimateAnyone 视频生成模型的人物图像规格要求
- [AnimateAnyone 动作模板生成 — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/animate-anyone-template-gen/create-task.md): 提交 AnimateAnyone 动作模板生成任务
- [AnimateAnyone 动作模板生成 — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/animate-anyone-template-gen/query-result.md): 根据任务 ID 查询 AnimateAnyone 动作模板生成任务的状态和结果
- [AnimateAnyone — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/animate-anyone/create-task.md): 提交舞动人像视频生成任务
- [AnimateAnyone — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/animate-anyone/query-result.md): 查询舞动人像视频生成状态
- [EMO — 图像检测](https://platform.qianwenai.com/docs/api-reference/video-generation/emo-video/emo-detect.md): 检测图像是否符合 EMO 视频生成模型的人物肖像图片规范
- [悦动人像 EMO — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/emo-video/create-task.md): 提交悦动人像 EMO 唱演视频生成异步任务
- [悦动人像 EMO — 查询视频生成结果](https://platform.qianwenai.com/docs/api-reference/video-generation/emo-video/query-result.md): 查询悦动人像 EMO 视频生成任务状态，获取生成的视频
- [LivePortrait 图像检测](https://platform.qianwenai.com/docs/api-reference/video-generation/liveportrait-video/liveportrait-detect.md): 检测人物肖像图片是否符合 LivePortrait 视频生成模型的输入规范
- [灵动人像 LivePortrait — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/liveportrait-video/create-task.md): 提交灵动人像 LivePortrait 播报视频生成异步任务
- [灵动人像 LivePortrait — 查询视频生成结果](https://platform.qianwenai.com/docs/api-reference/video-generation/liveportrait-video/query-result.md): 查询灵动人像 LivePortrait 视频生成任务状态，获取生成的视频
- [爱诗 PixVerse — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-lipsync/create-task.md): 提交 PixVerse 视频对口型任务
- [爱诗 PixVerse — 查询视频对口型任务结果](https://platform.qianwenai.com/docs/api-reference/video-generation/pixverse-lipsync/query-result.md): 查询 PixVerse 视频对口型任务状态
- [声动人像 VideoRetalk — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/video-retalk/create-task.md): 提交声动人像 VideoRetalk 视频口型替换异步任务
- [声动人像 VideoRetalk — 查询视频口型替换任务结果](https://platform.qianwenai.com/docs/api-reference/video-generation/video-retalk/query-result.md): 查询声动人像 VideoRetalk 视频口型替换任务状态，获取生成的视频
- [Emoji — 图像检测](https://platform.qianwenai.com/docs/api-reference/video-generation/emoji-video/emoji-detect.md): 检测图像中的人物形象是否满足表情包 Emoji 视频生成模型的要求
- [表情包视频 Emoji — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/emoji-video/create-task.md): 提交表情包视频生成任务
- [表情包视频 Emoji — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/emoji-video/query-result.md): 查询表情包视频生成状态
- [视频风格重绘 — 创建任务](https://platform.qianwenai.com/docs/api-reference/video-generation/video-style-transform/create-task.md): 提交视频风格重绘任务
- [视频风格重绘 — 查询结果](https://platform.qianwenai.com/docs/api-reference/video-generation/video-style-transform/query-result.md): 查询视频风格重绘任务状态

## 3D 生成 API

- [Tripo -- 3D 生成](https://platform.qianwenai.com/docs/api-reference/3d-generation/create-task.md): 提交 Tripo 3D 生成任务
- [Tripo -- 查询 3D 生成结果](https://platform.qianwenai.com/docs/api-reference/3d-generation/query-result.md): 查询 Tripo 3D 生成任务状态

## 专项模型 API

- [Qwen-Deep-Research API 参考](https://platform.qianwenai.com/docs/api-reference/specialized-models/deep-research-api.md): Qwen-Deep-Research 深入研究模型的输入与输出参数说明
- [GUI-Plus OpenAI 兼容](https://platform.qianwenai.com/docs/api-reference/gui-plus/openai.md): 通过 OpenAI 兼容接口调用 GUI-Plus 界面交互专用模型。
- [GUI-Plus DashScope](https://platform.qianwenai.com/docs/api-reference/gui-plus/dashscope.md): 通过 DashScope 原生 HTTP API 调用 GUI-Plus 界面交互专用模型。
- [Qwen-MT 翻译模型](https://platform.qianwenai.com/docs/api-reference/specialized-models/qwen-mt/openai.md): 通过 OpenAI 兼容接口调用 Qwen-MT 翻译模型。
- [Qwen-MT 翻译模型](https://platform.qianwenai.com/docs/api-reference/specialized-models/qwen-mt/dashscope.md): 通过 DashScope 原生 HTTP API 调用 Qwen-MT 翻译模型。
- [Qwen-OCR 文字提取模型](https://platform.qianwenai.com/docs/api-reference/specialized-models/qwen-ocr/openai.md): 通过 OpenAI 兼容接口调用 Qwen-OCR 文字提取模型。
- [Qwen-OCR 文字提取模型](https://platform.qianwenai.com/docs/api-reference/specialized-models/qwen-ocr/dashscope.md): 通过 DashScope 原生 HTTP API 调用 Qwen-OCR 文字提取模型。

## 语音合成

- [Qwen-Audio-TTS/CosyVoice WebSocket API](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/cosyvoice/websocket-api.md): Qwen-Audio-TTS/CosyVoice 语音合成 WebSocket 接口协议
- [Qwen-Audio-TTS/CosyVoice 客户端事件](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/cosyvoice/client-events.md): Qwen-Audio-TTS/CosyVoice 实时语音合成 WebSocket 客户端事件参考
- [Qwen-Audio-TTS/CosyVoice 服务端事件](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/cosyvoice/server-events.md): Qwen-Audio-TTS/CosyVoice 实时语音合成 WebSocket 服务端事件参考
- [实时语音合成 Qwen-Audio-TTS/CosyVoice Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/cosyvoice/java-sdk.md): Qwen-Audio-TTS/CosyVoice 实时语音合成 Java SDK 参考文档
- [实时语音合成 Qwen-Audio-TTS/CosyVoice Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/cosyvoice/python-sdk.md): Qwen-Audio-TTS/CosyVoice 实时语音合成 Python SDK 参考文档
- [语音合成 Qwen-Audio-TTS/CosyVoice Android SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/cosyvoice/android-sdk.md): 使用原生 SDK 将 Qwen-Audio-TTS/CosyVoice 模型的实时文本转语音功能集成到 Android 应用中。
- [语音合成 Qwen-Audio-TTS/CosyVoice iOS SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/cosyvoice/ios-sdk.md): 使用 Qwen-Audio-TTS/CosyVoice iOS SDK 将文本实时合成为高质量语音，支持流式与一次性文本输入两种调用方式
- [Qwen-Audio-TTS 音色列表](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/qwen-audio-tts/voice-list.md): qwen-audio-3.0-tts-plus 与 qwen-audio-3.0-tts-flash 支持的系统音色与基础音色列表
- [音色列表](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/cosyvoice/voice-list.md): 系统预置音色列表
- [非实时语音合成 Qwen-Audio-TTS/CosyVoice HTTP API](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/cosyvoice-nrt/http-api.md): Qwen-Audio-TTS/CosyVoice 非实时语音合成 HTTP API 参考，支持非流式和流式（SSE）两种调用模式。
- [非实时语音合成 Qwen-Audio-TTS/CosyVoice Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/cosyvoice-nrt/python-sdk.md): Qwen-Audio-TTS/CosyVoice 非实时语音合成 Python SDK 参考，支持非流式和流式两种调用模式。
- [非实时语音合成 Qwen-Audio-TTS/CosyVoice Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/cosyvoice-nrt/java-sdk.md): Qwen-Audio-TTS/CosyVoice 非实时语音合成 Java SDK 参考，支持非流式和流式两种调用模式。
- [Sambert WebSocket API 参考](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/sambert/websocket.md): 通过 WebSocket 长连接实时合成 Sambert 语音，支持流式音频输出与字/音素级时间戳
- [Sambert 客户端事件](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/sambert/client-events.md): Sambert 实时语音合成 WebSocket 客户端事件参考
- [Sambert 服务端事件](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/sambert/server-events.md): Sambert 实时语音合成 WebSocket 服务端事件参考
- [语音合成 Sambert Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/sambert/java-sdk.md): 本文介绍语音合成 Sambert Java SDK 的参数和接口细节。
- [语音合成 Sambert Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/sambert/python-sdk.md): 本文介绍语音合成 Sambert Python SDK 的参数和接口细节。
- [Sambert 语音合成 Android SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/sambert/android-sdk.md): 使用原生 SDK 将 Sambert 模型的实时文本转语音功能集成到 Android 应用中。
- [语音合成 Sambert iOS SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/sambert/ios-sdk.md): 使用 Sambert iOS SDK 将文本实时合成为高质量语音，支持流式音频输出与字/音素级时间戳
- [Qwen-TTS-Realtime WebSocket API](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/qwen-tts-realtime/websocket-api.md): Qwen-TTS-Realtime WebSocket 连接协议、请求头和交互流程
- [Qwen-TTS client events](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/qwen-tts-realtime/client-events.md): WebSocket 客户端事件参考
- [Qwen-TTS server events](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/qwen-tts-realtime/server-events.md): WebSocket 服务端事件参考
- [Qwen-TTS realtime Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/qwen-tts-realtime/python-sdk.md): 实时语音合成 Python SDK
- [Qwen-TTS realtime Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/qwen-tts-realtime/java-sdk.md): 实时语音合成 Java SDK
- [语音合成](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/qwen-tts.md): Qwen-TTS API 参考
- [Qwen-TTS 音色列表](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/qwen-tts/voice-list.md): Qwen-TTS 实时与非实时语音合成支持的音色
- [MiniMax 语音合成 API 参考](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/minimax-tts.md): MiniMax 同步语音合成 API，支持非流式和 SSE 流式两种模式，将文本转换为音频。
- [声音复刻 HTTP API](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-cloning/overview.md): 声音复刻 HTTP API 概述，包含请求头、服务端点和音色状态说明。
- [创建克隆音色（CosyVoice）](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-cloning/cosyvoice/create-voice.md): 通过上传音频创建 CosyVoice 克隆音色。
- [查询克隆音色列表（CosyVoice）](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-cloning/cosyvoice/list-voices.md): 分页查询当前账号下的 CosyVoice 克隆音色列表。
- [查询克隆音色](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-cloning/cosyvoice/query-voice.md): 查询指定克隆音色的详情，包括状态、创建时间和原始音频。
- [更新克隆音色](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-cloning/cosyvoice/update-voice.md): 替换已有克隆音色的音频文件。音色 ID 保持不变。
- [删除克隆音色（CosyVoice）](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-cloning/cosyvoice/delete-voice.md): 删除指定的 CosyVoice 克隆音色。
- [创建克隆音色](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-cloning/create-voice.md): 上传音频创建克隆音色。无需训练，即时返回音色名称。
- [查询克隆音色列表](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-cloning/list-voices.md): 分页查询当前账号下的克隆音色列表。
- [删除克隆音色](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-cloning/delete-voice.md): 删除克隆音色并释放配额。
- [Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-cloning/java-sdk.md): Qwen-Audio-TTS/CosyVoice 声音复刻 Java SDK 参考（VoiceEnrollmentService）。
- [Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-cloning/python-sdk.md): Qwen-Audio-TTS/CosyVoice 声音复刻 Python SDK 参考（VoiceEnrollmentService）。
- [声音设计 HTTP API](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-design/overview.md): 声音设计 HTTP API 概述，包含请求头、服务端点和音色状态说明。
- [创建设计音色（CosyVoice）](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-design/cosyvoice/create-voice.md): 通过文字描述创建 CosyVoice 设计音色。
- [查询设计音色列表（CosyVoice）](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-design/cosyvoice/list-voices.md): 分页查询当前账号下的 CosyVoice 设计音色列表。
- [查询设计音色详情（CosyVoice）](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-design/cosyvoice/query-voice.md): 查询指定 CosyVoice 设计音色的详情，包括状态、创建时间等。
- [删除设计音色（CosyVoice）](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-design/cosyvoice/delete-voice.md): 删除指定的 CosyVoice 设计音色。
- [创建音色](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-design/create-voice.md): 通过文本描述创建自定义音色，并返回预览音频。
- [查询音色列表](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-design/list-voices.md): 分页查询账号下的声音列表。
- [查询音色详情](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-design/query-voice.md): 查询指定音色的详细信息。
- [删除音色](https://platform.qianwenai.com/docs/api-reference/speech-synthesis/voice-design/delete-voice.md): 删除音色并释放配额。

## 语音识别

- [Paraformer 实时语音识别 WebSocket API](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-realtime/websocket-api.md): 通过 WebSocket 连接使用 Paraformer 实时语音识别服务的完整 API 参考。
- [实时语音识别（Paraformer）客户端事件](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-realtime/client-events.md): Paraformer 实时语音识别服务中客户端通过 WebSocket 发送给服务端的客户端事件，包括 run-task（启动任务）和 finish-task（结束任务）。
- [实时语音识别（Paraformer）服务端事件](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-realtime/server-events.md): Paraformer 实时语音识别服务通过 WebSocket 推送给客户端的服务端事件，包括 task-started、result-generated、task-finished、task-failed 四类事件。
- [Paraformer 实时语音识别 Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-realtime/java-sdk.md): 使用Java SDK接入Paraformer实时语音识别服务，支持非流式调用、基于回调的双向流式调用和基于Flowable的双向流式调用。
- [Paraformer 实时语音识别 Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-realtime/python-sdk.md): 本文介绍Paraformer实时语音识别Python SDK的参数和接口细节。
- [Paraformer 实时语音识别 Android SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-realtime/android-sdk.md): 本文档提供了Paraformer实时语音识别Android SDK的详细使用指南，帮助您将语音转换为文本。
- [Paraformer 实时语音识别 iOS SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-realtime/ios-sdk.md): 本文档提供了Paraformer实时语音识别iOS SDK的详细使用指南，帮助您将语音转换为文本。
- [Paraformer 录音文件识别 RESTful API — 创建任务](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-asr-file/create-task.md): 提交 Paraformer 录音文件识别异步任务
- [Paraformer 录音文件识别 RESTful API — 查询结果](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-asr-file/query-result.md): 查询 Paraformer 录音文件识别任务的状态和结果
- [Paraformer 录音文件识别 Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-asr-file/java-sdk.md): 使用Java SDK接入Paraformer录音文件识别服务，支持批量提交音频URL进行异步转写，获取识别结果。
- [Paraformer 录音文件识别 Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-asr-file/python-sdk.md): 使用DashScope Python SDK调用Paraformer模型，对录音文件进行异步转写识别。
- [Paraformer 录音文件识别 Android SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-asr-file/android-sdk.md): 本文档提供了Paraformer录音文件识别Android SDK的详细使用指南，帮助您将语音转换为文本。
- [Paraformer 录音文件识别 iOS SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-asr-file/ios-sdk.md): 使用 iOS SDK（NuiSDK）接入 Paraformer 录音文件识别服务，支持同步和异步两种模式批量提交音频 URL 进行转写，获取识别结果。
- [录音文件识别最佳实践](https://platform.qianwenai.com/docs/api-reference/speech-recognition/paraformer-asr-file/best-practices.md): 使用 ffmpeg 对视频文件进行预处理，提取音轨并压缩，从而加快 Paraformer 录音文件识别的吞吐效率。
- [Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime 实时语音识别 Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-realtime/python-sdk.md): Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime 实时语音识别 Python SDK
- [Fun-ASR 实时语音识别 Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-realtime/java-sdk.md): 实时语音识别 Java SDK
- [Fun-ASR 实时语音识别 WebSocket API](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-realtime/websocket-api.md): 实时语音识别 WebSocket API
- [实时语音识别（Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime）客户端事件](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-realtime/client-events.md): Qwen-Audio-3.0-ASR-Flash-Streaming/Fun-ASR-Realtime 实时语音识别 WebSocket 客户端事件参考
- [实时语音识别（Fun-ASR）服务端事件](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-realtime/server-events.md): Fun-ASR 实时语音识别 WebSocket 服务端事件参考
- [Fun-ASR 实时语音识别 Android SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-realtime/android-sdk.md): 本文档提供了Fun-ASR实时语音识别Android SDK的详细使用指南，帮助您将语音转换为文本。
- [Fun-ASR 实时语音识别 iOS SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-realtime/ios-sdk.md): 本文档提供了Fun-ASR实时语音识别iOS SDK的详细使用指南，帮助您将语音转换为文本。
- [Fun-ASR 录音文件识别 Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-recording/python-sdk.md): 录音文件转写 Python SDK
- [Fun-ASR 录音文件识别 HTTP API](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-recording/restful-api.md): 录音文件转写 REST API
- [Fun-ASR 录音文件识别 Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-recording/java-sdk.md): 录音文件转写 Java SDK
- [Fun-ASR 录音文件识别 Android SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-recording/android-sdk.md): 本文档提供了Fun-ASR录音文件识别Android SDK的详细使用指南，帮助您将语音转换为文本。
- [Fun-ASR 录音文件识别 iOS SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/fun-asr-recording/ios-sdk.md): 使用 iOS SDK（NuiSDK）接入 Fun-ASR 录音文件识别服务，支持同步和异步两种模式批量提交音频 URL 进行转写，获取识别结果。
- [实时语音识别（Qwen-ASR-Realtime）WebSocket API](https://platform.qianwenai.com/docs/api-reference/speech-recognition/qwen-asr-realtime/websocket-api.md): Qwen-ASR-Realtime WebSocket 连接、请求头和交互流程
- [实时语音识别（Qwen-ASR-Realtime）客户端事件](https://platform.qianwenai.com/docs/api-reference/speech-recognition/qwen-asr-realtime/client-events.md): WebSocket 客户端事件参考
- [实时语音识别（Qwen-ASR-Realtime）服务端事件](https://platform.qianwenai.com/docs/api-reference/speech-recognition/qwen-asr-realtime/server-events.md): WebSocket 服务端事件参考
- [实时语音识别（Qwen-ASR-Realtime）Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/qwen-asr-realtime/python-sdk.md): Qwen ASR Python 流式识别
- [实时语音识别（Qwen-ASR-Realtime）Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/qwen-asr-realtime/java-sdk.md): Qwen ASR Java 集成指南
- [录音文件识别（Qwen-ASR）OpenAI 兼容](https://platform.qianwenai.com/docs/api-reference/speech-recognition/qwen-asr/openai.md): 通过 Chat API 进行语音识别
- [录音文件识别（Qwen-ASR）DashScope](https://platform.qianwenai.com/docs/api-reference/speech-recognition/qwen-asr/dashscope.md): 同步语音识别
- [录音文件识别（Qwen-ASR）DashScope 异步](https://platform.qianwenai.com/docs/api-reference/speech-recognition/qwen-asr/dashscope-async.md): 提交异步转写任务
- [录音文件识别（Qwen-ASR）查询结果](https://platform.qianwenai.com/docs/api-reference/speech-recognition/qwen-asr/query-result.md): 查询转写任务状态
- [定制热词 HTTP API](https://platform.qianwenai.com/docs/api-reference/speech-recognition/custom-hotwords/http-api.md): 通过HTTP API管理定制热词列表，包括创建、查询、更新和删除热词列表。
- [定制热词 Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/custom-hotwords/java-sdk.md): 通过Java SDK管理定制热词列表，包括创建、查询、更新和删除热词列表。
- [定制热词 Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-recognition/custom-hotwords/python-sdk.md): 通过Python SDK管理定制热词列表，包括创建、查询、更新和删除热词列表。

## 语音转语音

- [Qwen-Omni client events](https://platform.qianwenai.com/docs/api-reference/real-time-multimodal/client-events.md): WebSocket 客户端参考
- [Qwen-Omni server events](https://platform.qianwenai.com/docs/api-reference/real-time-multimodal/server-events.md): WebSocket 服务端事件参考
- [Qwen-Omni Python SDK](https://platform.qianwenai.com/docs/api-reference/real-time-multimodal/realtime-python-sdk.md): Qwen-Omni-Realtime Python SDK 接口参考
- [Qwen-Omni Java SDK](https://platform.qianwenai.com/docs/api-reference/real-time-multimodal/realtime-java-sdk.md): Qwen-Omni-Realtime Java SDK 接口说明
- [Qwen-Omni 声音复刻](https://platform.qianwenai.com/docs/api-reference/real-time-multimodal/voice-cloning.md): 声音复刻 API 参考：上传音频创建定制音色，用于 Qwen-Omni 对话
- [Qwen-Audio-Realtime WebSocket API](https://platform.qianwenai.com/docs/api-reference/qwen-audio-realtime/websocket-api.md): Qwen-Audio-Realtime WebSocket 连接协议、请求头、核心概念和交互流程
- [Qwen-Audio-Realtime 客户端事件](https://platform.qianwenai.com/docs/api-reference/qwen-audio-realtime/client-events.md): Qwen-Audio-Realtime API 客户端事件参考
- [Qwen-Audio-Realtime 服务端事件](https://platform.qianwenai.com/docs/api-reference/qwen-audio-realtime/server-events.md): Qwen-Audio-Realtime API 服务端事件参考
- [LiveTranslate client events](https://platform.qianwenai.com/docs/api-reference/speech-translation/livetranslate-realtime/client-events.md): WebSocket 客户端事件参考
- [LiveTranslate server events](https://platform.qianwenai.com/docs/api-reference/speech-translation/livetranslate-realtime/server-events.md): WebSocket 服务端事件参考
- [LiveTranslate Python SDK](https://platform.qianwenai.com/docs/api-reference/speech-translation/livetranslate-realtime/python-sdk.md): LiveTranslate Python SDK 参考文档
- [LiveTranslate Java SDK](https://platform.qianwenai.com/docs/api-reference/speech-translation/livetranslate-realtime/java-sdk.md): LiveTranslate Java SDK 参考文档
- [音视频翻译](https://platform.qianwenai.com/docs/api-reference/speech-translation/audio-video-translation-api.md): LiveTranslate API 参考

## 音乐生成

- [音乐生成（Fun-Music）](https://platform.qianwenai.com/docs/api-reference/music-generation/fun-music.md): 音乐生成 Fun-Music 模型 API 参考

## 图片翻译

- [创建图像翻译任务](https://platform.qianwenai.com/docs/api-reference/image-translation/qwen-mt-image/create-task.md): 提交 qwen-mt-image 图像翻译异步任务
- [查询任务结果](https://platform.qianwenai.com/docs/api-reference/image-translation/qwen-mt-image/query-result.md): 查询 qwen-mt-image 图像翻译任务状态和结果

## 文本向量

- [OpenAI 兼容文本向量](https://platform.qianwenai.com/docs/api-reference/text-embedding/openai-embedding.md): OpenAI 兼容的文本向量接口
- [DashScope 文本向量](https://platform.qianwenai.com/docs/api-reference/text-embedding/dashscope-embedding.md): DashScope embedding API

## 多模态向量

- [DashScope 多模态向量](https://platform.qianwenai.com/docs/api-reference/multimodal-embedding/dashscope-multimodal-embedding.md): 多模态向量化 API

## 重排序

- [OpenAI 兼容重排序](https://platform.qianwenai.com/docs/api-reference/rerank/openai-rerank.md): OpenAI 兼容的重排序 API
- [DashScope 重排序](https://platform.qianwenai.com/docs/api-reference/rerank/dashscope-rerank.md): DashScope 重排序 API

## 平台 API

- [对话管理](https://platform.qianwenai.com/docs/api-reference/platform-api/conversations.md): 自动管理的多轮对话上下文
- [创建 Conversation](https://platform.qianwenai.com/docs/api-reference/platform-api/conversations/create-conversation.md): 创建会话，可选择性地添加初始消息。
- [查询会话](https://platform.qianwenai.com/docs/api-reference/platform-api/conversations/retrieve-conversation.md): 根据会话 ID 查询会话详情。
- [更新对话](https://platform.qianwenai.com/docs/api-reference/platform-api/conversations/update-conversation.md): 更新会话的元数据。此操作会完全覆盖已有的元数据。
- [删除会话](https://platform.qianwenai.com/docs/api-reference/platform-api/conversations/delete-conversation.md): 删除会话。会话中的消息不会被删除。
- [添加消息](https://platform.qianwenai.com/docs/api-reference/platform-api/conversations/create-items.md): 向会话中添加消息。
- [查询消息列表](https://platform.qianwenai.com/docs/api-reference/platform-api/conversations/list-items.md): 查询会话中的消息列表。
- [查询消息](https://platform.qianwenai.com/docs/api-reference/platform-api/conversations/retrieve-item.md): 根据消息 ID 查询消息详情。
- [删除消息](https://platform.qianwenai.com/docs/api-reference/platform-api/conversations/delete-item.md): 从会话中删除指定消息。
- [文件管理](https://platform.qianwenai.com/docs/api-reference/platform-api/file.md): 文件管理 API
- [上传文件](https://platform.qianwenai.com/docs/api-reference/platform-api/file/upload-file.md): 上传文件用于文档解析或批量处理。账户最多可存储 10,000 个文件，总容量上限为 100 GB，文件永久有效，不会过期。
- [查询文件详情](https://platform.qianwenai.com/docs/api-reference/platform-api/file/retrieve-file.md): 通过文件 ID 查询文件详细信息。
- [查询文件列表](https://platform.qianwenai.com/docs/api-reference/platform-api/file/list-files.md): 列出账户下所有文件（包括已上传的文件和批量处理结果），支持按用途、创建时间筛选，并提供分页功能。
- [删除文件](https://platform.qianwenai.com/docs/api-reference/platform-api/file/delete-file.md): 通过文件 ID 删除指定文件。
- [创建 Batch](https://platform.qianwenai.com/docs/api-reference/platform-api/batch/create-batch.md): 创建批量任务，异步处理已上传输入文件中的所有请求。
- [查询 Batch](https://platform.qianwenai.com/docs/api-reference/platform-api/batch/retrieve-batch.md): 查询批量任务的状态，并在任务完成后获取输出文件 ID。
- [列出 Batch](https://platform.qianwenai.com/docs/api-reference/platform-api/batch/list-batches.md): 查询当前账号下的批量任务列表。结果按创建时间降序排列，仅返回最近 30 天的任务。
- [取消 Batch](https://platform.qianwenai.com/docs/api-reference/platform-api/batch/cancel-batch.md): 取消正在执行或排队中的批量任务。状态将先变为 `cancelling`（等待当前正在执行的请求完成），然后变为 `cancelled`。取消前已完成的请求仍会计费。

## 工具包与框架

- [OpenAI 兼容接口](https://platform.qianwenai.com/docs/api-reference/toolkitframework/openai-compatible/overview.md): 只需修改 base_url、api_key 和 model 三个参数，即可从 OpenAI 迁移到千问AI平台。

## 更多

- [生成临时 API Key](https://platform.qianwenai.com/docs/api-reference/more/generate-a-temporary-api-key.md): 短期有效的临时访问令牌
- [上传文件获取临时 URL](https://platform.qianwenai.com/docs/api-reference/more/upload-file-get-temporary-url.md): 将本地文件上传至免费临时存储空间并获取 oss:// 格式的临时 URL，供多模态、图像、视频或音频模型调用。
- [管理异步任务](https://platform.qianwenai.com/docs/api-reference/more/manage-asynchronous-tasks.md): 查询和管理异步任务
- [异步任务管理 API 参考](https://platform.qianwenai.com/docs/api-reference/more/async-task-management.md): 通过 HTTP API 查询单个异步任务结果、批量查询异步任务状态、以及取消异步任务的完整参考文档。
- [连接复用与连接池](https://platform.qianwenai.com/docs/api-reference/more/connection-pooling.md): 面向高并发场景的 HTTP 连接复用和 WebSocket 连接池配置指南。

## 计费

- [充值及查看余额](https://platform.qianwenai.com/docs/resources/billing-overview.md): 为账户充值并查看可用额度
- [免费额度](https://platform.qianwenai.com/docs/resources/free-quota.md): 新用户免费额度
- [使用和管理优惠券](https://platform.qianwenai.com/docs/resources/coupons.md): 查看、使用和管理您的优惠券
- [账单查询与费用管理](https://platform.qianwenai.com/docs/resources/bill-query.md): 查看按量付费账单、还款及成本管理
- [发票管理](https://platform.qianwenai.com/docs/resources/invoice.md): 申请、下载和管理千问AI平台消费发票

## 常见问题

- [账号与访问](https://platform.qianwenai.com/docs/resources/faq-account.md): API Key、权限、访问相关常见问题
- [计费与定价](https://platform.qianwenai.com/docs/resources/faq-billing.md): 付费和费用常见问题
- [文本生成常见问题](https://platform.qianwenai.com/docs/resources/faq-text-generation.md): 流式输出、上下文管理、上下文缓存、结构化输出、思考模式、函数调用和批量处理的常见问题。
- [图片与视频 FAQ](https://platform.qianwenai.com/docs/resources/faq-images-videos.md): 图片和视频生成的常见问题——计费、API 报错、模型差异、输入要求和输出 URL。
- [语音常见问题](https://platform.qianwenai.com/docs/resources/faq-audio-speech.md): CosyVoice 语音合成、Qwen-Omni 实时对话、Fun-ASR 语音识别的常见问题与解答。
- [向量与重排序 FAQ](https://platform.qianwenai.com/docs/resources/faq-embedding-reranking.md): 文本向量、多模态向量和重排序的常见问题——模型选择、维度、批量限制及使用场景。

## 更新日志

- [模型发布记录](https://platform.qianwenai.com/docs/changelog/models.md): 模型发布与更新记录
- [平台更新](https://platform.qianwenai.com/docs/changelog/platform.md): 功能与改进

## OpenAPI Specs

- [openapi-tripo-3d-generation](https://platform.qianwenai.com/docs/openapi-tripo-3d-generation.json): 使用 Tripo 模型通过文本、单张图像或多张图像生成 3D 模型。异步提交任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
- [openapi-anthropic](https://platform.qianwenai.com/docs/openapi-anthropic.json): 通过兼容 Anthropic 格式的 Messages API 调用 Qwen 模型，支持深度思考、工具调用、流式输出、图片视频理解和上下文缓存。  认证方式：通过 `x-api-key` 请求头或 `Authorization: Bearer` 请求头传入 API Key，二者选其一即可。
- [openapi-dashscope](https://platform.qianwenai.com/docs/openapi-dashscope.json): 通过 DashScope 原生 HTTP API 调用 Qwen 模型。支持文本和多模态模型、流式输出、工具调用和结构化输出。
- [openapi-openai-responses](https://platform.qianwenai.com/docs/openapi-openai-responses.json): 使用 OpenAI 兼容 Responses API 调用通义模型。支持内置工具、基于 `previous_response_id` 的多轮上下文管理，以及思考模式。
- [openapi-openai-chat](https://platform.qianwenai.com/docs/openapi-openai-chat.json): 通过 OpenAI 兼容接口调用通义千问模型，支持文本及多模态模型、流式输出、工具调用和结构化输出。
- [openapi-gui-plus-dashscope](https://platform.qianwenai.com/docs/openapi-gui-plus-dashscope.json): 通过 DashScope 原生 HTTP API 调用 GUI-Plus 界面交互专用模型，支持流式输出和多模态输入（图片）。
- [openapi-gui-plus-openai](https://platform.qianwenai.com/docs/openapi-gui-plus-openai.json): 通过 OpenAI 兼容接口调用 GUI-Plus 界面交互专用模型，支持流式输出和多模态输入（图片）。
- [openapi-ai-tryon](https://platform.qianwenai.com/docs/openapi-ai-tryon.json): AI试衣模型支持使用服饰平拍图片以及人物正面全身照，生成逼真的试衣效果图。提供两个模型：aitryon（基础版，生成更快）和 aitryon-plus（Plus版，在图像清晰度、布料纹理和 Logo 还原方面表现更出色，但生成耗时更长）。两个模型的接口参数完全一致，仅 model 字段不同。
- [openapi-aitryon-parsing](https://platform.qianwenai.com/docs/openapi-aitryon-parsing.json): 从模特图或AI试衣图中分割出服装区域，支持上装、下装、连衣裙等类型。
- [openapi-aitryon-refiner](https://platform.qianwenai.com/docs/openapi-aitryon-refiner.json): AI试衣-图片精修是一个后处理模型，可增强AI试衣生成图片的真实感与清晰度。
- [openapi-background-generation](https://platform.qianwenai.com/docs/openapi-background-generation.json): 本文介绍Wan-背景生成模型的输入输出参数。Wan-图像背景生成模型为主体商品生成背景图，适用于电商和海报场景。支持多种背景生成方法：文本引导、图像引导、文本与图像结合引导，以及文本、图像与边缘引导元素的综合应用。
- [openapi-creative-poster](https://platform.qianwenai.com/docs/openapi-creative-poster.json): 创意海报生成 API
- [openapi-facechain-finetune](https://platform.qianwenai.com/docs/openapi-facechain-finetune.json): 提交 FaceChain 人物形象训练任务，使用 1-10 张人像图片训练专属人像模型。训练完成后，使用 `finetuned_output` 中的模型名称调用人物写真生成 API 生成写真。
- [openapi-facechain-generation](https://platform.qianwenai.com/docs/openapi-facechain-generation.json): 基于 FaceChain 模型生成人物写真。支持两种模式：人物形象训练 LoRA 模式（需先完成人物形象训练）和人物形象免训练 TrainFree 模式（推荐，无需训练，一键极速生成）。
- [openapi-facechain-facedetect](https://platform.qianwenai.com/docs/openapi-facechain-facedetect.json): 人物图像检测 API。检测输入图像中是否包含人脸，用于人物写真生成前的图像筛选。
- [openapi-image-erase](https://platform.qianwenai.com/docs/openapi-image-erase.json): 图像擦除补全（image-erase-completion）API，可根据mask区域对原图进行擦除补全。
- [openapi-image-out-painting](https://platform.qianwenai.com/docs/openapi-image-out-painting.json): 图像画面扩展 API。支持旋转图像、等比例扩图、指定方向扩图、指定宽高比扩图。
- [openapi-kling-image-generation](https://platform.qianwenai.com/docs/openapi-kling-image-generation.json): 可灵图像生成模型支持文生图、参考图生图两种任务。
- [openapi-person-instance-segmentation](https://platform.qianwenai.com/docs/openapi-person-instance-segmentation.json): 人物实例分割 API。对输入图像中的每个人物实例进行分割，输出每个实例的分割掩码图像和可视化结果。
- [openapi-qwen-image-edit](https://platform.qianwenai.com/docs/openapi-qwen-image-edit.json): Qwen-Image 图像编辑 API，支持单图编辑、多图融合、风格迁移、文字编辑、元素操控等多种图像处理功能。
- [openapi-qwen-image](https://platform.qianwenai.com/docs/openapi-qwen-image.json): Qwen-Image 文生图 API，支持所有模型的同步调用，以及旧版模型的异步调用。
- [openapi-shoe-model](https://platform.qianwenai.com/docs/openapi-shoe-model.json): AI 鞋靴模特上脚效果图生成。上传模特模板图和鞋靴商品图，自动生成模特上脚效果图。
- [openapi-vidu-image-generation](https://platform.qianwenai.com/docs/openapi-vidu-image-generation.json): Vidu 参考生图模型支持文生图、图片编辑、参考图生图等任务。API 采用异步调用模式，包含"创建任务"和"查询结果"两个步骤。
- [openapi-virtual-model](https://platform.qianwenai.com/docs/openapi-virtual-model.json): 万相-虚拟模特可以对上传的真人实拍商品展示图进行智能生成，将其中的模特和背景替换为心仪的内容，在保持人物姿态不变的情况下，使用虚拟模特对商品进行更加精美、多样的展示。支持各种与模特产生互动的商品，如手持小商品、服装、鞋靴、配饰等。
- [openapi-wan-t2i-v2](https://platform.qianwenai.com/docs/openapi-wan-t2i-v2.json): 使用 Wan 文生图模型系列，根据文本描述生成图像。支持多种艺术风格和写实摄影效果，满足多样化的创意需求。本 API 采用异步任务模式：先通过 POST 请求提交任务，再通过 GET 请求轮询结果。
- [openapi-wan21-image-edit](https://platform.qianwenai.com/docs/openapi-wan21-image-edit.json): Wan 2.1 通用图像编辑 API。支持 10 种编辑功能：整图风格化、局部风格化、指令编辑、蒙版编辑、去水印、扩图、超分辨率、上色、涂鸦成图、卡通特征控制。
- [openapi-wan25-image-edit](https://platform.qianwenai.com/docs/openapi-wan25-image-edit.json): Wan2.5 通用图像编辑 API。通过文本提示词对图像进行编辑，保持主体一致性。支持单图编辑和多图融合，最多支持三张参考图。
- [openapi-wan26-image](https://platform.qianwenai.com/docs/openapi-wan26-image.json): Wan2.6 图像生成与编辑 API，支持多图输入、图像编辑及图文交织输出。
- [openapi-wan27-image](https://platform.qianwenai.com/docs/openapi-wan27-image.json): Wan2.7 图像生成与编辑 API，支持文生图、多图编辑、边界框交互式编辑以及图像集生成。
- [openapi-wanx-sketch-to-image](https://platform.qianwenai.com/docs/openapi-wanx-sketch-to-image.json): 本文介绍万相-涂鸦作画模型的API输入输出参数。万相-涂鸦作画通过手绘图案和文字描述，生成精美的涂鸦绘画作品。
- [openapi-wanx-style-repaint](https://platform.qianwenai.com/docs/openapi-wanx-style-repaint.json): 人像风格重绘模型支持将人物照片转换为多种预设或自定义的艺术风格。
- [openapi-wanx-v1-text-to-image](https://platform.qianwenai.com/docs/openapi-wanx-v1-text-to-image.json): 使用 wanx-v1 模型根据文本描述生成图像。本 API 采用异步任务模式：先通过 POST 请求提交任务，再通过 GET 请求轮询结果。
- [openapi-wanx-x-painting](https://platform.qianwenai.com/docs/openapi-wanx-x-painting.json): 图像局部重绘 API。根据用户输入的原始图片、掩码图和 prompt 提示词，在涂抹区域生成与文字描述相对应的内容，而涂抹区域外的部分则基本保持不变。
- [openapi-wordart-semantic](https://platform.qianwenai.com/docs/openapi-wordart-semantic.json): WordArt 锦书-文字变形 API
- [openapi-wordart-texture](https://platform.qianwenai.com/docs/openapi-wordart-texture.json): 创意文字纹理生成 API
- [openapi-z-image](https://platform.qianwenai.com/docs/openapi-z-image.json): Z-Image 文生图 API。
- [openapi-image-translation](https://platform.qianwenai.com/docs/openapi-image-translation.json): 千问-图像翻译模型（Qwen-MT-Image）可精准翻译图像中的文字，并保留原始排版。该模型还支持领域提示、敏感词过滤、术语干预等自定义功能。  HTTP API 采用异步模式，调用流程分两步： 1. **创建任务获取任务 ID**：发送 POST 请求创建任务，返回 task_id。 2. **根据任务 ID 查询结果**：使用 task_id 轮询任务状态，直到任务完成并获得图像 URL。
- [openapi-image](https://platform.qianwenai.com/docs/openapi-image.json): DashScope 图像 API，涵盖图像生成、图像编辑、专项图像任务及多模态向量嵌入。
- [openapi-fun-music](https://platform.qianwenai.com/docs/openapi-fun-music.json): 音乐生成 Fun-Music 模型的 API 参考文档，支持流式和非流式输出。
- [openapi-batch](https://platform.qianwenai.com/docs/openapi-batch.json): 通过文件上传提交批量推理任务，费用仅为实时 API 调用的50%。兼容 OpenAI 接口。
- [openapi-conversations](https://platform.qianwenai.com/docs/openapi-conversations.json): 自动管理多轮对话历史，支持跨设备、跨会话的上下文管理。
- [openapi-file](https://platform.qianwenai.com/docs/openapi-file.json): 上传并管理文件，用于文档解析或批量处理。
- [openapi-reranking](https://platform.qianwenai.com/docs/openapi-reranking.json): 对召回文档按语义相关度重新排序，提升 RAG 和检索系统的搜索精准度。
- [openapi-deep-research](https://platform.qianwenai.com/docs/openapi-deep-research.json): 通过 DashScope API 调用 Qwen-Deep-Research 深入研究模型。支持两步式调用流程（反问确认 + 深入研究）和流式输出。
- [openapi-translation](https://platform.qianwenai.com/docs/openapi-translation.json): 通过 OpenAI 兼容接口或 DashScope 原生接口调用 Qwen-MT 翻译模型。支持基础翻译、术语干预、翻译记忆和领域提示。
- [openapi-ocr](https://platform.qianwenai.com/docs/openapi-ocr.json): Qwen-OCR 文字提取模型的 API 参考文档，支持 OpenAI 兼容协议和 DashScope 协议。
- [openapi-paraformer-asr-file](https://platform.qianwenai.com/docs/openapi-paraformer-asr-file.json): Paraformer 录音文件识别 RESTful API。采用异步任务模式——先提交任务，再轮询查询结果。
- [openapi-qwen-asr](https://platform.qianwenai.com/docs/openapi-qwen-asr.json): Qwen-ASR 音频文件识别 API 参考文档，支持 OpenAI 兼容协议、DashScope 同步协议和 DashScope 异步协议。
- [openapi-qwen-tts](https://platform.qianwenai.com/docs/openapi-qwen-tts.json): Qwen 语音合成模型（Qwen-TTS、Qwen3-TTS-Flash、Qwen3-TTS-Instruct-Flash）的 API 参考文档，支持流式和非流式输出。
- [openapi-voice-cloning-cosyvoice](https://platform.qianwenai.com/docs/openapi-voice-cloning-cosyvoice.json)
- [openapi-voice-cloning-cosyvoice-delete](https://platform.qianwenai.com/docs/openapi-voice-cloning-cosyvoice-delete.json)
- [openapi-voice-cloning-cosyvoice-list](https://platform.qianwenai.com/docs/openapi-voice-cloning-cosyvoice-list.json)
- [openapi-voice-cloning-query](https://platform.qianwenai.com/docs/openapi-voice-cloning-query.json)
- [openapi-voice-cloning-update](https://platform.qianwenai.com/docs/openapi-voice-cloning-update.json)
- [openapi-voice-cloning](https://platform.qianwenai.com/docs/openapi-voice-cloning.json): 从音频克隆声音，用于 Qwen TTS 模型的语音合成。
- [openapi-voice-cloning-delete](https://platform.qianwenai.com/docs/openapi-voice-cloning-delete.json)
- [openapi-voice-cloning-list](https://platform.qianwenai.com/docs/openapi-voice-cloning-list.json)
- [openapi-voice-design-cosyvoice](https://platform.qianwenai.com/docs/openapi-voice-design-cosyvoice.json)
- [openapi-voice-cosyvoice-delete](https://platform.qianwenai.com/docs/openapi-voice-cosyvoice-delete.json)
- [openapi-voice-cosyvoice-list](https://platform.qianwenai.com/docs/openapi-voice-cosyvoice-list.json)
- [openapi-voice-cosyvoice-query](https://platform.qianwenai.com/docs/openapi-voice-cosyvoice-query.json)
- [openapi-voice-design](https://platform.qianwenai.com/docs/openapi-voice-design.json): 基于文字描述创建和管理自定义音色，供 Qwen TTS 模型使用。
- [openapi-voice-design-delete](https://platform.qianwenai.com/docs/openapi-voice-design-delete.json)
- [openapi-voice-design-list](https://platform.qianwenai.com/docs/openapi-voice-design-list.json)
- [openapi-voice-design-query](https://platform.qianwenai.com/docs/openapi-voice-design-query.json)
- [openapi-text-embedding](https://platform.qianwenai.com/docs/openapi-text-embedding.json): 文本向量模型 API 参考文档，支持 OpenAI 兼容协议和 DashScope 协议。
- [openapi-animate-anyone](https://platform.qianwenai.com/docs/openapi-animate-anyone.json): AnimateAnyone模型，可基于AnimateAnyone-template模型生成的动作模板，以及通过AnimateAnyone-detect模型检测的人物图像生成人物动作视频。本文档介绍了该模型提供的视频生成能力的API调用方法。
- [openapi-wan-aa-detect](https://platform.qianwenai.com/docs/openapi-wan-aa-detect.json): AnimateAnyone 图像检测 API。检测输入图像是否符合 AnimateAnyone 视频生成模型的人物图像规格要求。
- [openapi-animate-anyone-template-gen](https://platform.qianwenai.com/docs/openapi-animate-anyone-template-gen.json): AnimateAnyone动作模板生成模型，可基于人物运动视频提取人物动作，并生成可供AnimateAnyone视频生成模型使用的人物动作模板。本文档介绍了该模型提供的动作模板生成能力的API调用方法。
- [openapi-emo-video](https://platform.qianwenai.com/docs/openapi-emo-video.json): 基于人物肖像图片和音频，生成口型与音频同步的唱演视频。
- [openapi-emo-detect](https://platform.qianwenai.com/docs/openapi-emo-detect.json): EMO 图像检测 API。检测输入图像是否符合 EMO 视频生成模型的人物肖像图片规范。
- [openapi-emoji-video](https://platform.qianwenai.com/docs/openapi-emoji-video.json): 表情包emoji-v1模型可基于人物肖像图片和预设模板ID，生成人脸表情包视频。
- [openapi-emoji-detect](https://platform.qianwenai.com/docs/openapi-emoji-detect.json): 检测输入图像中的人物形象是否满足表情包 Emoji 模型的要求。检测通过后返回人脸区域及扩展后的动态表情区域坐标，供后续 Emoji 视频生成使用。
- [openapi-happyhorse-image-to-video](https://platform.qianwenai.com/docs/openapi-happyhorse-image-to-video.json): 使用 HappyHorse 模型以首帧图片为基础生成视频。异步提交任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
- [openapi-happyhorse-ref-to-video](https://platform.qianwenai.com/docs/openapi-happyhorse-ref-to-video.json): 使用 HappyHorse 模型传入多张参考图像生成视频。异步提交任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
- [openapi-happyhorse-text-to-video](https://platform.qianwenai.com/docs/openapi-happyhorse-text-to-video.json): 使用 HappyHorse 模型通过文本提示词生成视频。异步提交任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
- [openapi-happyhorse-video-editing](https://platform.qianwenai.com/docs/openapi-happyhorse-video-editing.json): 使用 HappyHorse 模型通过文本指令和参考图片编辑视频。异步提交任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
- [openapi-kling-video-generation](https://platform.qianwenai.com/docs/openapi-kling-video-generation.json): 可灵（Kling）视频生成异步 API，支持文生视频、图生视频（首帧/首尾帧）、参考生视频等多种模式。
- [openapi-liveportrait-video](https://platform.qianwenai.com/docs/openapi-liveportrait-video.json): 基于人物肖像图片和语音音频，生成口型与音频同步的播报视频。
- [openapi-liveportrait-detect](https://platform.qianwenai.com/docs/openapi-liveportrait-detect.json): LivePortrait-detect 模型，用于确认输入的人物肖像图片是否符合 LivePortrait 模型的输入规范。
- [openapi-pixverse-image-to-video](https://platform.qianwenai.com/docs/openapi-pixverse-image-to-video.json): 爱诗 PixVerse 图生视频模型根据输入图像和文本提示词，生成一段流畅的视频。API 采用异步调用方式：先 POST 创建任务获取 task_id，再 GET 轮询查询任务状态与结果。
- [openapi-pixverse-i2v-first-frame](https://platform.qianwenai.com/docs/openapi-pixverse-i2v-first-frame.json): 基于首帧图片生成视频。提交异步任务后，通过 `GET /tasks/{task_id}` 轮询结果。
- [openapi-pixverse-kf2v](https://platform.qianwenai.com/docs/openapi-pixverse-kf2v.json): 爱诗-首尾帧生视频模型基于首帧图像、尾帧图像和文本提示词，生成一段平滑过渡的视频。
- [openapi-pixverse-lipsync](https://platform.qianwenai.com/docs/openapi-pixverse-lipsync.json): 爱诗 PixVerse 视频对口型模型支持输入视频和音频（或 TTS 文本），生成与音频同步的对口型视频。API 采用异步调用方式：先 POST 创建任务获取 task_id，再 GET 轮询查询任务状态与结果。
- [openapi-pixverse-motioncontrol](https://platform.qianwenai.com/docs/openapi-pixverse-motioncontrol.json): 爱诗 PixVerse 视频动作模仿模型支持输入人物图片和动作参考视频，将视频中的动作迁移到目标角色上，生成角色复现相同动作的新视频。适用于动作模仿、编舞复刻、角色动画生成等场景。API 采用异步调用方式：先 POST 创建任务获取 task_id，再 GET 轮询查询任务状态与结果。
- [openapi-pixverse-ref-to-video](https://platform.qianwenai.com/docs/openapi-pixverse-ref-to-video.json): PixVerse 参考生视频模型支持传入多张参考图片或视频，通过文本提示词描述场景，将图片中的主体角色融合生成一段流畅的视频。支持通过 `@ref_name` 语法精确引用参考图中的主体。
- [openapi-pixverse-text-to-video](https://platform.qianwenai.com/docs/openapi-pixverse-text-to-video.json): 爱诗 PixVerse 文生视频模型基于文本提示词，生成一段流畅的视频。API 采用异步调用方式：先 POST 创建任务获取 task_id，再 GET 轮询查询任务状态与结果。
- [openapi-pixverse-upscale](https://platform.qianwenai.com/docs/openapi-pixverse-upscale.json): 爱诗 PixVerse 视频超清模型支持将输入视频进行超分辨率处理，固定输出 4K（3840×2160）分辨率视频。API 采用异步调用方式：先 POST 创建任务获取 task_id，再 GET 轮询查询任务状态与结果。
- [openapi-video-retalk](https://platform.qianwenai.com/docs/openapi-video-retalk.json): 基于人物视频和人声音频，生成人物讲话口型与输入音频相匹配的新视频。
- [openapi-video-style-transform](https://platform.qianwenai.com/docs/openapi-video-style-transform.json): 视频风格重绘 API。将真实视频转换为多种艺术风格（日式漫画、美式漫画、3D卡通等8种风格）。使用异步任务模式——提交任务后轮询获取结果。
- [openapi-vidu-image-to-video](https://platform.qianwenai.com/docs/openapi-vidu-image-to-video.json): 使用 Vidu 模型从图像生成视频（基于首帧）。采用异步任务提交模式——提交任务后轮询结果。
- [openapi-vidu-i2v-first-frame](https://platform.qianwenai.com/docs/openapi-vidu-i2v-first-frame.json): 基于首帧图片，使用 Vidu 模型生成视频。
- [openapi-vidu-reference-to-video](https://platform.qianwenai.com/docs/openapi-vidu-reference-to-video.json): Vidu-参考生视频模型支持传入参考图片和文本提示词，将图片中的主体角色融合到提示词描述的场景中，生成流畅的视频内容。API 采用异步调用模式，包含"创建任务"和"查询结果"两个步骤。
- [openapi-vidu-start-end-to-video](https://platform.qianwenai.com/docs/openapi-vidu-start-end-to-video.json): 基于首帧图像和尾帧图像生成平滑过渡视频。采用异步任务模式：提交任务后轮询获取结果。
- [openapi-vidu-text-to-video](https://platform.qianwenai.com/docs/openapi-vidu-text-to-video.json): Vidu 文生视频模型基于文本提示词，生成一段流畅的视频。API 采用异步调用模式，包含"创建任务"和"查询结果"两个步骤。
- [openapi-wan-video-editing](https://platform.qianwenai.com/docs/openapi-wan-video-editing.json): Wan 统一视频编辑 API，支持多模态输入（文本、图像、视频），提供五大核心能力：多图参考、视频重绘、局部编辑、视频续写和画面扩展。
- [openapi-wan-image-to-animation](https://platform.qianwenai.com/docs/openapi-wan-image-to-animation.json): 使用 wan2.2-animate-move 模型，将参考视频中的人物动作与表情迁移到输入图片，生成动画视频。
- [openapi-wan-i2v-first-frame](https://platform.qianwenai.com/docs/openapi-wan-i2v-first-frame.json): 使用 Wan 图像转视频模型，根据首帧图像和文字描述生成视频。支持音频同步、多镜头叙事以及多种分辨率规格。
- [openapi-wan-i2v-first-last](https://platform.qianwenai.com/docs/openapi-wan-i2v-first-last.json): 使用 Wan kf2v 模型，基于首帧图像、尾帧图像和文本提示词，生成过渡自然流畅的视频。
- [openapi-wan-ref-to-video](https://platform.qianwenai.com/docs/openapi-wan-ref-to-video.json): Wan 参考驱动视频生成 API，支持通过参考图片或视频结合多模态输入（文本、图片、视频）生成表演视频，覆盖单人或多人互动、多镜头叙事及音视频同步等场景。
- [openapi-wan-s2v](https://platform.qianwenai.com/docs/openapi-wan-s2v.json): 数字人 wan2.2-s2v 模型能基于单张图片和音频，生成动作自然的说话、唱歌或表演视频。
- [openapi-wan-s2v-detect](https://platform.qianwenai.com/docs/openapi-wan-s2v-detect.json): 万相数字人图像检测 API。检测输入图像是否符合 wan2.2-s2v 视频生成模型的人物图像规格要求。
- [openapi-wan-text-to-video](https://platform.qianwenai.com/docs/openapi-wan-text-to-video.json): Wan 文本生成视频 API。支持多模态输入（文字、图像、音频），可生成最长 15 秒、分辨率高达 1080P 的视频。采用异步任务模式——先提交任务，再轮询获取结果。
- [openapi-wan-character-swap](https://platform.qianwenai.com/docs/openapi-wan-character-swap.json): Wan 视频换脸 API。将视频中的主角替换为图片中的人物，同时保留原视频的场景、光线和色调。采用异步任务方式处理。
- [openapi-wan27-image-to-video](https://platform.qianwenai.com/docs/openapi-wan27-image-to-video.json): 基于 Wan 2.7 模型，从图片、音频和视频片段生成视频。以异步方式提交任务，然后通过 `GET /tasks/{task_id}` 轮询获取结果。
- [openapi-wan27-ref-to-video](https://platform.qianwenai.com/docs/openapi-wan27-ref-to-video.json): Wan 2.7 参考内容生视频 API。基于参考图片或视频生成表演视频，支持多模态输入（文本、图像、视频）。采用新协议，通过 media 数组传入参考内容，支持分辨率和比例参数配置，并提供增强版响应元数据。
- [openapi-wan27-text-to-video](https://platform.qianwenai.com/docs/openapi-wan27-text-to-video.json): 使用 Wan 2.7 模型从文本生成视频。提交异步任务后，通过轮询 `GET /tasks/{task_id}` 获取生成结果。
- [openapi-wan27-video-editing](https://platform.qianwenai.com/docs/openapi-wan27-video-editing.json): 基于 Wan 2.7 模型，通过多模态输入（文本、图片、视频）对视频进行编辑。提交异步任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
- [openapi-wan30-video](https://platform.qianwenai.com/docs/openapi-wan30-video.json): 万相 3.0 是全能参考视频生成模型（All-in-One），统一支持文生视频、图生视频（首帧/首尾帧）、参考生视频和参考文件生视频等多种用法，最长可生成30秒视频。提交异步任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
