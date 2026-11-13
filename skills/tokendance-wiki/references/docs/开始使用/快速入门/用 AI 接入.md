# 用 AI 接入

把 [https://tokendance.space/docs/ai-integration.md](%E7%94%A8%20AI%20%E6%8E%A5%E5%85%A5.md) 交给
coding agent，它可以从这里了解 TokenDance 的接入能力、找到详细文档，并根据当前项目选择方案。

## 从这里开始 {#start-here}

Agent 应先读取文档索引，再选择当前任务需要的专题 Markdown：

- 文档索引：[https://tokendance.space/llms.txt](https://tokendance.space/llms.txt)
- 全部文档正文：[https://tokendance.space/llms-full.txt](https://tokendance.space/llms-full.txt)
- 实时模型目录：[https://tokendance.space/gateway/v1/models](https://tokendance.space/gateway/v1/models)

`llms.txt` 列出了所有公开文档及其独立 Markdown 地址。实时模型目录返回当前可用的模型 ID 和
`supported_protocols`；模型与协议能力应以这里的实时结果为准。

## 接入 TokenDance {#integration}

TokenDance 是多模型、多供应商网关，支持 OpenAI、Anthropic、Google GenAI 以及图像、视频、语音等多种
协议。同一个 TokenDance API Key 可以用于平台支持的协议。

已有项目通常可以继续使用当前 SDK，再调整 TokenDance 所需的配置。不同协议的 SDK、base URL、端点和参数
并不完全相同，Agent 应从多协议总览选择对应的独立文档：

[https://tokendance.space/docs/multi-protocol.md](../../%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E9%80%89%E6%8B%A9%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E5%8D%8F%E8%AE%AE%E6%80%BB%E8%A7%88.md)

## 获取 API Key {#api-key}

API Key 可以来自以下方式：

- 复用用户已经配置的 TokenDance API Key；
- 让用户在控制台创建，使用与管理方式见
  [https://tokendance.space/docs/api-keys.md](../%E8%AE%BF%E9%97%AE%E4%B8%8E%E8%AE%A4%E8%AF%81/API%20%E5%AF%86%E9%92%A5.md)；
- CLI、桌面客户端或第三方产品可以通过 OAuth 式授权，在用户确认后获得一个新的 API Key，详见
  [https://tokendance.space/docs/api-key-oauth.md](../%E8%AE%BF%E9%97%AE%E4%B8%8E%E8%AE%A4%E8%AF%81/OAuth%20%E5%BC%8F%20API%20Key%20%E6%8E%88%E6%9D%83.md)。

Agent 根据产品形态和项目已有能力决定使用哪种方式。OAuth 参数、回调模式、PKCE、Key 配置和异常处理均以
OAuth 式授权专题文档为准。产品持有授权 Key 时，可以按其中的 `TokenDance-Recovery-Action` 响应头处理充值、
重新授权与周期额度刷新。

如果调用因余额不足而失败，Agent 可以引导用户完成充值并在到账后重试，详见
[https://tokendance.space/docs/agent-payment.md](../%E5%BA%94%E7%94%A8%E4%B8%8E%E5%BC%80%E6%94%BE%E8%83%BD%E5%8A%9B/Agent%20%E6%94%AF%E4%BB%98.md)。

## 可选的应用归因 {#app-attribution}

如果你希望 TokenDance 识别并记录哪些模型调用来自你的应用，可以使用应用归因。归因信息既可以从 API Key
自动继承，也可以在每次请求中显式传递；App URL 是归因的唯一要素：

[https://tokendance.space/docs/app-attribution.md](../%E5%BA%94%E7%94%A8%E4%B8%8E%E5%BC%80%E6%94%BE%E8%83%BD%E5%8A%9B/%E5%BA%94%E7%94%A8%E5%BD%92%E5%9B%A0.md)

App URL 不是模型调用的必需参数。

## 由 Agent 选择方案 {#decision}

Agent 应结合项目已有的 SDK、协议、配置方式、Secret 管理、部署边界和用户目标决定最终实现。本文只提供
入口和平台能力；实际参数、接口行为和安全规则应从 `llms.txt` 中对应的专题文档获取。
