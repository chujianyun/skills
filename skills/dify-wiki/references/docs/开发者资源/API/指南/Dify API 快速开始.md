# Dify API 快速开始

> 获取 API 密钥、发起第一个请求，并找到你的应用类型对应的接口

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/api-reference/guides/get-started.md)。

在 Dify 中发布的每个应用都同时是一个 REST API，知识库也是如此。你可在自己的后端用 API 密钥调用终端用户所使用的同一个应用。

## 获取 API 密钥

> [!WARNING]
>
> 只在后端调用 API。嵌入前端代码或客户端应用中的密钥可能被提取和滥用。

* 应用密钥：在应用内部创建 API 密钥。该密钥仅作用于这一个应用，且一个密钥可服务你的所有终端用户。

  > [!NOTE]
  >
  > 调用时以每人各自的 `user` 值区分不同的人。详见 [终端用户身份](%E7%BB%88%E7%AB%AF%E7%94%A8%E6%88%B7%E8%BA%AB%E4%BB%BD.md)。

* 知识库密钥：详见 [知识库 API](API%20%E6%A6%82%E8%A7%88/%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md) 指南。

## 发起第一个请求

大多数请求都通过 Bearer 令牌携带密钥。Dify Cloud 的基础 URL 为 `https://api.dify.ai/v1`；自部署时，替换为你实例的 API 基础 URL。

最快的第一个请求无需写代码：打开 [获取应用基本信息](../%E5%BA%94%E7%94%A8%20API/%E5%BA%94%E7%94%A8%E9%85%8D%E7%BD%AE/%E8%8E%B7%E5%8F%96%E5%BA%94%E7%94%A8%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF.md)，点击 **试一试**，把密钥粘贴到 **Authorization** 字段，再按 **发送**。它适用于所有应用类型。

在终端中发起同样的调用：

```bash theme={null}
curl https://api.dify.ai/v1/info \
  -H "Authorization: Bearer $DIFY_API_KEY"
```

收到如下响应即说明密钥有效，同时能看到它所属的应用：

```json theme={null}
{
  "name": "My Chat App",
  "description": "A helpful assistant",
  "tags": ["assistant"],
  "mode": "chat",
  "author_name": "Dify Team"
}
```

如果用的是知识库 API 密钥，详见 [知识库 API](API%20%E6%A6%82%E8%A7%88/%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md) 指南。

## 找到你的应用类型对应的接口

每种应用类型的完整 API 见其概览页：

* [Chatflow](API%20%E6%A6%82%E8%A7%88/Chatflow%20%E5%BA%94%E7%94%A8%20API.md)（`advanced-chat`）
* [Workflow](API%20%E6%A6%82%E8%A7%88/Workflow%20%E5%BA%94%E7%94%A8%20API.md)（`workflow`）
* [Agent](API%20%E6%A6%82%E8%A7%88/Agent%20API.md)（`agent`）
* [Chatbot 和旧版 Agent](API%20%E6%A6%82%E8%A7%88/%E5%AF%B9%E8%AF%9D%E5%9E%8B%E5%BA%94%E7%94%A8%20API.md)（`chat`、`agent-chat`）
* [文本生成应用](API%20%E6%A6%82%E8%A7%88/%E6%96%87%E6%9C%AC%E7%94%9F%E6%88%90%E5%BA%94%E7%94%A8%20API.md)（`completion`）
* [知识库](API%20%E6%A6%82%E8%A7%88/%E7%9F%A5%E8%AF%86%E5%BA%93/%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md)
