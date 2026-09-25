> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Cursor

> 在 Cursor 中使用千问AI平台模型

Cursor 是一款 AI 驱动的代码编辑器，可以通过按量计费、Token Plan 个人版或 Token Plan 团队版接入千问AI平台。

## 安装 Cursor

通过 [Cursor 官网](https://cursor.com/features)下载并安装 Cursor。

<Warning>
  需要 Cursor Pro 或更高版本订阅。免费版仅支持 Auto 模式，无法使用自定义模型。
</Warning>

## 配置接入凭证

在 Cursor 中，点击设置图标，进入 **Cursor Settings** > **Models**。开启 **OpenAI API Key** 和 **Override OpenAI Base URL**，根据所选方案填入对应的 API Key、Base URL 和模型名称。

千问AI平台提供以下计费方案，根据需要选择：

- **Token Plan 个人版**：按 token 消耗抵扣个人 Credits。
- **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
- **按量计费**：按实际调用量后付费。

### Token Plan 个人版

| 配置项          | 说明                                                                             |
| ------------ | ------------------------------------------------------------------------------ |
| **API Key**  | Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)       |
| **Base URL** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`           |
| **可用模型**     | Token Plan 个人版[支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型) |

### Token Plan 团队版

| 配置项          | 说明                                                                                                                                                                              |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API Key**  | Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/api-keys)                                                                                                        |
| **Base URL** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`                                                                                                            |
| **可用模型**     | Token Plan 团队版[支持的模型](/token-plan/overview)。部分模型名称需调整：kimi-k2.6 写为 **kimi-k2-6**，kimi-k2.5 写为 **kimi-k2-5**，glm-5.2 写为 **glm-5-2**，glm-5.1 写为 **glm-5-1**，glm-5 写为 **glm-5-0**。 |

### 按量计费

| 配置项          | 说明                                                                                                                                                                                                      |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **API Key**  | 千问AI平台 [API Key](/developer-guides/administration/api-keys)                                                                                                                                             |
| **Base URL** | `https://dashscope.aliyuncs.com/compatible-mode/v1`                                                                                                                                                     |
| **可用模型**     | 填入[支持的模型](/developer-guides/getting-started/text-generation-models)。部分模型名称需调整：kimi-k2.6 写为 **kimi-k2-6**，kimi-k2.5 写为 **kimi-k2-5**，glm-5.2 写为 **glm-5-2**，glm-5.1 写为 **glm-5-1**，glm-5 写为 **glm-5-0**。 |

在 **Add or search model** 中输入模型名称（如 `qwen3.6-plus`），点击 **Add Custom Model**，然后在对话面板中选择该模型即可开始使用。

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

- 按量付费：[错误码排查](/api-reference/preparation/error-messages)
- Token Plan 个人版：[Token Plan 常见问题](/token-plan/personal/token-plan-personal-faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)

### 在 Cursor 中无法调用已添加的模型

报错信息：

- The model xxx does not work with your current plan or api key.
- Named models unavailable Free plans can only use Auto. Switch to Auto or upgrade plans to continue.

**原因**：Cursor 免费版仅支持 Auto 模式，不支持调用自定义模型。

**解决方案**：请升级至 **Cursor Pro 及以上套餐**。

### 配置完成后找不到添加的模型

请在聊天面板点击并关闭 **Auto** 模式，在模型下拉栏选择所需模型。

### 调用模型报错 "We're having trouble connecting to the model provider." 或 "Unauthorized User API key"

请逐项排查：

- 检查 API Key、Base URL 和模型名称是否与所选计费方案一致。不同方案的凭证不通用。
- 部分模型名称与 Cursor 内置模型名冲突，需使用别名。请参考上方可用模型中的说明。
