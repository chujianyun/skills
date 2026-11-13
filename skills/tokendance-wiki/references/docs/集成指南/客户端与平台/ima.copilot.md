# ima.copilot

[ima.copilot](https://watcha.cn/products/ima?ref=tokendance-docs) 是腾讯推出的以知识库为核心的 AI 工作台，支持智能搜索、阅读与写作。配置词元跳动后，即可在 ima.copilot 中调用词元跳动上支持 OpenAI 协议的模型，费用从词元跳动额度扣除，所有请求记录在 [调用日志](https://tokendance.space/activity) 中。更多信息请访问 [观猹产品主页](https://watcha.cn/products/ima?ref=tokendance-docs)。

## 配置 {#configuration}

1. 创建 Copilot 后，点击**选择模型** → **添加自定义模型**，进入模型设置页，并在下拉列表最底部点击**自定义**。

   :::images
   ![ima.copilot 进入模型设置 1](../../../assets/docs/integrations/ima/ima-1.png)
   ![ima.copilot 进入模型设置 2](../../../assets/docs/integrations/ima/ima-2.png)
   ![ima.copilot 进入模型设置 3](../../../assets/docs/integrations/ima/ima-3.png)
   :::

2. 在自定义配置表单中填写：
   - **API 接口地址**：`https://tokendance.space/gateway/v1/chat/completions`
   - **API Key**：你的词元跳动 API Key
   - **模型名称**：词元跳动上的模型 ID，如 `deepseek-v4-flash-0731`

   :::images
   ![ima.copilot 填写接口信息](../../../assets/docs/integrations/ima/ima-4.png)
   :::

::: note
模型 ID 以词元跳动 [模型列表](https://tokendance.space/models) 中的为准，且需支持 OpenAI 协议。

ima.copilot 需要填写完整请求地址： `hhttps://tokendance.space/gateway/v1/chat/completions`。
:::

## 常见问题 {#troubleshooting}

- **404 / 路径错误**：检查 API 接口地址是否重复拼接了 `/chat/completions`；若未来版本升级软件自动追加该路径，则 Base URL 只填到 `/v1`。
- **鉴权失败**：确认 API Key 正确，且没有填错字段。
- **模型不存在**：模型 ID 需与词元跳动模型列表中的 ID 一致，且支持 OpenAI 协议。

## 相关文档 {#related}

- [多协议支持](../../%E6%A8%A1%E5%9E%8B%E4%B8%8E%E5%8D%8F%E8%AE%AE/%E9%80%9A%E7%94%A8%E6%A8%A1%E5%9E%8B%E5%8D%8F%E8%AE%AE/OpenAI/OpenAI%20Chat%20Completions.md) — OpenAI 协议详情
- [API 密钥](../../%E5%BC%80%E5%A7%8B%E4%BD%BF%E7%94%A8/%E8%AE%BF%E9%97%AE%E4%B8%8E%E8%AE%A4%E8%AF%81/API%20%E5%AF%86%E9%92%A5.md) — 创建和管理密钥
- [模型](https://tokendance.space/models) — 查看支持 OpenAI 协议的模型
