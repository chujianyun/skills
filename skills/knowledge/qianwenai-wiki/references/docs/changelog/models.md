> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 模型发布记录

> 模型发布与更新记录

<Note>
  部分历史模型将于近期下线，请查看[模型下线机制说明](/changelog/model-deprecation)了解下线时间表与替代模型。
</Note>

<Update label="2026年8月13日">
  ### deepseek-v4-pro-0813

  旗舰级 MoE 大模型，总参1.6T、激活 49B，原生支持百万级超长上下文。依托海量高质量训练数据，具备顶尖数学逻辑、复杂推理、专业代码与长文本深度解析能力，适配高阶科研、复杂办公、深度智能代理等高难度场景。支持流式输出、深度思考、Function Calling、结构化输出、联网搜索与上下文缓存。详见 [DeepSeek](/developer-guides/third-party-models/deepseek)。

  ### qwen3.8-2.4t-a95b

  Qwen3.8-2.4T-A95B 是通义千问最新旗舰系列的开源版本，采用稀疏 MoE 架构，总参数 2.4 万亿，每步激活约 950 亿，配合混合注意力机制，支持 100 万 Token 上下文。模型默认开启思考模式，在编程、办公、科研和长周期 Agent 任务上实现显著提升。详见[文本生成模型](/developer-guides/getting-started/text-generation-models)。

  ### pixverse/pixverse-v6-r2v-omni

  V6-R2V-Omni 是 PixVerse 推出的融合参考生视频模型，支持图片+视频混合参考输入，智能融合多主体和动作信息，生成高质量视频。支持多种分辨率和宽高比输出。[API 参考](/api-reference/video-generation/pixverse-reference-to-video/create-task)
</Update>

<Update label="2026年8月6日">
  ### wan3.0-video

  万相3.0全能参考视频生成模型（All-in-One），邀测上架，统一支持文生视频、图生视频（首帧/首尾帧）和参考生视频等多种用法。[API 参考](/api-reference/video-generation/wan30-video/create-task)
</Update>

<Update label="2026年8月4日">
  ### qwen-image-3.0-pro、qwen-image-3.0

  Qwen-Image-3.0-Pro 系列模型，支持长文本输入与图中图密集排版，能够一次性精准生成报纸、分镜、菜单及试卷等复杂版面；具备 10 像素小字精准渲染能力，生动还原微表情、毛孔与发丝等摄影级细节，并支持 12 国语言、多种字体及主流网页、游戏界面的高保真仿真。qwen-image-3.0 为标准版，兼顾质量与速度。详见[千问-文生图](/api-reference/image-generation/qwen-text-to-image)、[千问-图像编辑](/api-reference/image-generation/qwen-image-editing)。
</Update>

<Update label="2026年8月3日">
  ### qwen3.8-max

  Qwen3.8 原生视觉语言系列 Max 模型，是通义千问迄今能力最强的旗舰模型，拥有 2.4 万亿参数，采用 MoE 架构，展现出与当前顶尖前沿模型相媲美的卓越性能，模型效果相较 3.7 系列显著提升。支持混合思考模式（默认开启），1M 上下文。详见[文本生成模型](/developer-guides/getting-started/text-generation-models)。
</Update>

<Update label="2026年8月1日">
  ### deepseek-v4-flash-0731

  高效轻量化MoE模型，总参284B，激活13B，原生支持百万超长上下文能力。推理速度快、延迟低、调用成本低廉，综合能力均衡，主打高并发、轻量化任务，适合日常对话、内容创作、基础 RAG、批量文案处理等普惠刚需场景。详见 [DeepSeek](/developer-guides/third-party-models/deepseek)。
</Update>

<Update label="2026年7月30日">
  ### Qwen-Audio-3.0-ASR-Flash 系列语音识别模型

  新增 Qwen-Audio-3.0-ASR-Flash-Streaming（实时）、Qwen-Audio-3.0-ASR-Flash-Filetrans（非实时）和 Qwen-Audio-3.0-ASR-Flash（非实时）系列模型：方言支持覆盖汉语七大方言（官话/吴/湘/赣/客/闽/粤）及 20+ 地区口音；古诗词识别优化，适用于文化教育、有声读物等场景；标点预测与文本归一化增强，数字/日期/金额自动转标准格式；支持中、英、日、韩等共 30 个语种；支持热词（预编译热词和即时热词）与 context 上下文，提升特定词汇识别准确率。详见[语音识别模型](/developer-guides/speech/speech-to-text-models)。
</Update>

<Update label="2026年7月25日">
  ### qwen3.7-flash、qwen3.7-flash-2026-07-15

  Qwen3.7 原生视觉语言系列 Flash 模型，相较 qwen3.6-flash 全面提升多模态理解与 Agent 执行能力。重点强化多模态基础能力，万物识别能力更强，真实世界感知与空间智能进一步提升；Search Agent、CI Agent 等多模态 Agent 场景能力显著升级，端到端任务执行更稳定；多模态 Coding 能力优化，vibe coding 体验更加流畅。
</Update>

<Update label="2026年7月17日">
  ### kimi/kimi-k3

  Kimi K3 是 Kimi 迄今能力最强的旗舰模型，拥有 2.8 万亿参数，原生支持视觉理解，并拥有 100 万 token 上下文窗口，面向长程编程、知识工作和推理等前沿智能场景而设计。详见 [Kimi-月之暗面](/developer-guides/third-party-models/kimi-moonshot)。
</Update>

<Update label="2026年7月16日">
  ### pixverse/pixverse-lipsync

  爱诗 PixVerse 视频对口型模型，支持输入视频和音频（或 TTS 文本），生成与音频同步的对口型视频。[API 参考](/api-reference/video-generation/pixverse-lipsync/create-task)

  ### pixverse/pixverse-motioncontrol

  爱诗 PixVerse 视频动作模仿模型，支持输入人物图片和动作参考视频，将视频中的动作迁移到目标角色上，生成角色复现相同动作的新视频。[API 参考](/api-reference/video-generation/pixverse-motioncontrol/create-task)

  ### pixverse/pixverse-upscale

  爱诗 PixVerse 视频超清模型，支持将输入视频进行超分辨率处理，固定输出 4K（3840×2160）分辨率视频。[API 参考](/api-reference/video-generation/pixverse-upscale/create-task)
</Update>

<Update label="2026年7月15日">
  ### qwen3.7-text-embedding

  Qwen3.7 多语言文本统一向量模型，相较 text-embedding-v4 在文本检索、聚类、分类性能大幅提升，MTEB 多语言、中英、Code 检索等评测效果提升 20%；支持 256\~2560 维用户自定义向量维度。详见[文本与多模态向量化](/developer-guides/embeddings/embedding)。
</Update>

<Update label="2026年7月14日">
  ### qwen-plus-character

  千问系列角色扮演模型，适合拟人化的角色扮演，同时优化了限定人设指令遵循、话题推进、倾听共情等能力，支持个性化角色的深度还原。[角色扮演（Qwen-Character）](/developer-guides/text-generation/role-playing)

  ### qwen-audio-3.0-realtime-plus、qwen-audio-3.0-realtime-flash

  Qwen-Audio端到端实时语音大模型兼顾语音推理能力与双工对话节奏，在保持流畅、自然的实时交互体验的同时，通过并行推理、全向流式等工程优化，有效控制端到端响应时延。[实时语音对话（Qwen-Audio-Realtime）](/developer-guides/speech/qwen-audio-realtime)

  ### qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash

  Qwen-Audio-TTS语音合成模型上线，新增更多小语种和中文方言支持，增强了指令遵循与细粒度标签控制能力，音质和表现力全面提升。其中 Plus 版本面向高品质专业场景，Flash 版本面向低延迟实时交互场景。[实时语音合成](/developer-guides/speech/realtime-streaming)
</Update>

<Update label="2026年7月13日">
  ### Vidu 图像生成系列

  由生数科技提供的 Vidu 系列图片生成 API 服务，支持文生图、参考图生图和图片编辑，对中英文字精准渲染、UI/图表等设计细节像素级还原。可用模型：`vidu/vidu-image_reference2image`、`vidu/viduq3-fast_reference2image`、`vidu/viduq2-pro_reference2image`、`vidu/viduq2-fast_reference2image`。[API 参考](/api-reference/image-generation/vidu-image-generation/create-task)

  ### vidu/viduq3-pro-fast\_img2video

  Vidu 图生视频旗舰极速版，最高支持 1080P，最长 16 秒。[API 参考](/api-reference/video-generation/vidu-image-to-video-first-frame/create-task)

  ### vidu/viduq3-ad\_reference2video

  Vidu 参考生视频广告版，面向广告行业，支持营销级智能切镜、运镜和音效直出。[API 参考](/api-reference/video-generation/vidu-reference-to-video/create-task)

  ### vidu/viduq3-drama\_reference2video

  Vidu 参考生视频精品剧版，角色一致性强、动效细腻、情绪表达真实，适合剧情向内容生产。[API 参考](/api-reference/video-generation/vidu-reference-to-video/create-task)
</Update>

<Update label="2026年7月1日">
  ### wan2.7-t2v-2026-06-12

  万相2.7文生视频模型快照版本，模型能力与 wan2.7-t2v 一致。详见[万相2.7-文生视频](/api-reference/video-generation/wan27-text-to-video/create-task)。

  ### wan2.7-r2v-2026-06-12

  万相2.7参考生视频模型快照版本，支持主体参考和音色定制，并可输入单张多宫格故事板直接生成剧本化视频。详见[万相2.7-参考生视频](/api-reference/video-generation/wan27-reference-to-video/create-task)。
</Update>

<Update label="2026年6月25日">
  ### qwen-image-2.0-pro-2026-06-22

  Qwen-Image-2.0 系列模型最新快照，融合图片生成与编辑能力。相较于 4 月 22 日快照，文字渲染能力进一步增强，支持最长 1k token 的指令输入；真实质感与写实场景细节刻画更加细腻；语义遵循能力更强。详见[千问-文生图](/api-reference/image-generation/qwen-text-to-image)、[千问-图像编辑](/api-reference/image-generation/qwen-image-editing)。
</Update>

<Update label="2026年6月22日">
  ### happyhorse-1.1-t2v

  HappyHorse 1.1 文生视频模型。支持生成带音频的 3-15 秒视频，分辨率 720P/1080P。[API 参考](/api-reference/video-generation/happyhorse-text-to-video/create-task)

  ### happyhorse-1.1-i2v

  HappyHorse 1.1 图生视频模型。支持生成带音频的 3-15 秒视频，分辨率 720P/1080P。[API 参考](/api-reference/video-generation/happyhorse-image-to-video/create-task)

  ### happyhorse-1.1-r2v

  HappyHorse 1.1 参考生视频模型。支持多张参考图像输入，生成带音频的 3-15 秒视频，分辨率 720P/1080P。[API 参考](/api-reference/video-generation/happyhorse-reference-to-video/create-task)

  ### happyhorse-1.0-video-edit

  HappyHorse 视频编辑模型，支持对视频进行风格化编辑和增强。[API 参考](/api-reference/video-generation/happyhorse-video-editing/create-task)
</Update>

<Update label="2026年6月18日">
  ### kimi/kimi-k2.7-code-highspeed

  月之暗面直供的高速编程模型，与 kimi/kimi-k2.7-code 功能完全一致，速度提升5\~6倍。详见 [Kimi-月之暗面](/developer-guides/third-party-models/kimi-moonshot)。
</Update>

<Update label="2026年6月17日">
  ### glm-5.2

  GLM-5.2 是智谱AI推出的面向长程任务（Long Horizon Task）设计的最新旗舰模型，支持 1M 超长上下文。拥有强大逻辑推理、长文本理解与代码生成能力，兼顾性能与推理效率；在多任务基准中表现优异，适用于智能交互、企业应用、开发辅助等场景。支持 OpenAI 兼容、DashScope 及 Anthropic 兼容接口调用。详见 [GLM-千问AI平台](/developer-guides/third-party-models/glm)。

  ### ZHIPU/GLM-5.2

  智谱AI直供的 glm-5.2 模型。详见 [GLM-智谱](/developer-guides/third-party-models/glm-zhipu)。

  ### fun-asr-flash-2026-06-15

  百聆2026年6月更新的大模型ASR版本，全面支持汉语传统七大方言体系（官话/吴/湘/赣/客/闽/粤），并适配 20+ 地区口音官话。针对中文古诗词的韵律、节奏与文言表达特点进行专项优化，提升对古诗词内容的识别准确率，适用于文化传承、教育讲解、有声读物等场景。优化标点预测与文本归一化能力，使输出文本更符合书面表达习惯，数字、日期、金额等信息自动转换为标准格式，增强内容的可读性与专业性。同时语种扩展至英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚、保加利亚语、克罗地亚语、斯洛伐克语等，共计30个语种。支持context上下文能力，可转写5分钟以内的音频。
</Update>

<Update label="2026年6月16日">
  ### qwen3.5-ocr

  千问文字提取模型，基于 Qwen3.5 架构，速度更快，效果更强。上下文长度扩展至 128K，支持多轮对话。信息抽取能力大幅提升，覆盖多种国内外卡证。详见[文字提取](/developer-guides/multimodal/ocr)。
</Update>

<Update label="2026年6月15日">
  ### kimi-k2.7-code

  Kimi 迄今最智能的 Coding 模型（仅思考模式），在长上下文中更可靠地遵循指令，能以更高的成功率完成编程任务。支持文本、图片与视频输入，支持显式缓存与隐式缓存。详见 [Kimi](/developer-guides/third-party-models/kimi)。

  ### kimi/kimi-k2.7-code

  月之暗面直供的 kimi-k2.7-code 模型。详见 [Kimi-月之暗面](/developer-guides/third-party-models/kimi-moonshot)。
</Update>

<Update label="2026年6月10日">
  ### qwen3.7-max-2026-06-08

  Qwen3.7系列中规模最大、综合能力最强的Max模型，相较于5月20日快照增加了视觉模态理解能力，能够感知真实世界场景，具备多模态交互混合智能体能力。
</Update>

<Update label="2026年6月8日">
  ### pixverse/pixverse-v6-r2v

  爱诗V6-参考生视频模型，参考多张图像生成视频。相较于v5.6全面升级，通用场景推荐使用。支持将一张多宫格分镜拼接图一键转化为视频。详见[爱诗-参考生视频](/api-reference/video-generation/pixverse-reference-to-video/create-task)。
</Update>

<Update label="2026年6月1日">
  ### qwen3.7-plus、qwen3.7-plus-2026-05-26

  千问3.7Plus系列，在强大文本能力的基础上全面升级了视觉-语言能力，同时保持了在编码、工具使用和生产力工作流方面的完整智能体能力。其核心特色为多模态交互混合智能体能力，能够感知真实世界场景、读取屏幕并操作 GUI、基于视觉参考生成代码、端到端导航移动应用。
</Update>

<Update label="2026年5月29日">
  ### vanchin/deepseek-v4-pro

  由快手万擎直供的 DeepSeek 模型推理服务。详见 [DeepSeek-快手万擎](/developer-guides/third-party-models/deepseek-kuaishou)。
</Update>

<Update label="2026年5月28日">
  ### stepfun/step-3.7-flash

  阶跃星辰直供的 Step 3.7 Flash 模型，Flash 档位新一代旗舰。在搜索、Agent、编码、多模态四大方向全面升级，深度检索与多模态图搜能力大幅增强，Agent 与工具调用能力显著提升，编码能力在 Flash 档位多项基准中表现优异，多模态理解能力对标头部旗舰。详见 [Stepfun-阶跃星辰](/developer-guides/third-party-models/stepfun)。
</Update>

<Update label="2026年5月25日">
  ### qwen3.7-max-preview、qwen3.7-max-2026-05-17

  Qwen Max 系列模型快照。仅支持纯文本输入，默认开启思考模式。
</Update>

<Update label="2026年5月22日">
  ### qwen3.5-livetranslate-flash-realtime

  Qwen3.5-LiveTranslate-Flash 的实时版本，一款高精度、高响应、高鲁棒性的多语言实时音视频同传大模型。依托 Qwen3.5-Omni 强大的基座能力，能听懂 60 种语言，会说 29 种语言。详见[实时音视频翻译](/developer-guides/speech/realtime-translation)。
</Update>

<Update label="2026年5月21日">
  ### qwen3.7-max、qwen3.7-max-2026-05-20

  Qwen Max 系列新一代旗舰模型。仅支持纯文本输入，默认开启思考模式，支持显式缓存，在编程、办公与生产力、长周期自主执行方面均能出色胜任各项任务。
</Update>

<Update label="2026年5月19日">
  ### MiMo-V2.5-Pro

  小米直供的 MiMo-V2.5-Pro 推理模型，在通用智能体能力、复杂软件工程以及长程任务等方面提升显著。详见 [MiMo](/developer-guides/third-party-models/mimo)。

  ### ZHIPU/GLM-5.1、ZHIPU/GLM-5

  智谱直供的 GLM-5、GLM-5.1 推理模型，适用于智能交互、企业应用及开发辅助等场景。详见 [GLM-智谱](/developer-guides/third-party-models/glm-zhipu)。
</Update>

<Update label="2026年5月15日">
  ## 正式上线

  千问AI平台正式上线。
</Update>
