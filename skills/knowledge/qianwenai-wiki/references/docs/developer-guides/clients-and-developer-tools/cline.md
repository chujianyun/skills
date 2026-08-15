> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Cline

> 在 Cline 中使用千问AI平台模型

Cline 是一款 VSCode 智能编程插件，可以通过 Token Plan 个人版、Token Plan 团队版或按量计费接入千问AI平台。

## 安装 Cline

1. 下载并安装 [VSCode](https://code.visualstudio.com/)。
2. 打开 VSCode，在扩展商店搜索 `Cline` 并安装。

## 配置接入凭证

安装完成后，点击左侧边栏的 Cline 图标进入配置界面。点击 **Bring my own API key**，选择 **OpenAI Compatible** 作为 API Provider，根据所选方案填入对应参数。如果之前使用过 Cline，请点击右上角的设置按钮进入配置界面。

千问AI平台提供以下计费方案，根据需要选择：

- **Token Plan 个人版**：按 token 消耗抵扣个人 Credits。
- **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
- **按量计费**：按实际调用量后付费。

### Token Plan 个人版

| 配置项              | 说明                                                                                                 |
| ---------------- | -------------------------------------------------------------------------------------------------- |
| **API Provider** | 选择 **OpenAI Compatible**。                                                                          |
| **Base URL**     | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`                               |
| **API Key**      | 填入 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。                       |
| **Model ID**     | 填入 Token Plan 个人版[支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型)，如 `qwen3.8-max`。 |

### Token Plan 团队版

| 配置项              | 说明                                                                           |
| ---------------- | ---------------------------------------------------------------------------- |
| **API Provider** | 选择 **OpenAI Compatible**。                                                    |
| **Base URL**     | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`         |
| **API Key**      | 填入 Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。 |
| **Model ID**     | 填入 Token Plan 团队版[支持的模型](/token-plan/overview)，如 `qwen3.8-max`。              |

### 按量计费

| 配置项              | 说明                                                                   |
| ---------------- | -------------------------------------------------------------------- |
| **API Provider** | 选择 **OpenAI Compatible**。                                            |
| **Base URL**     | `https://dashscope.aliyuncs.com/compatible-mode/v1`                  |
| **API Key**      | 填入千问AI平台 [API Key](/developer-guides/administration/api-keys)。       |
| **Model ID**     | 填入[支持的模型](/developer-guides/getting-started/text-generation-models)。 |

如果使用 Qwen3（思考模式）或 QwQ 模型，需在设置界面点击 `MODEL CONFIGURATION`，勾选 **Enable R1 messages format**。

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

- 按量付费：[错误码排查](/api-reference/preparation/error-messages)
- Token Plan 个人版：[Token Plan 常见问题](/token-plan/faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)

### 报错 401 Incorrect API key provided

可能原因：

- API Key 与 Base URL 不匹配。两种计费方案的 API Key 不通用，请确认 API Key 和 Base URL 来自同一方案。

### 报错 400 InternalError.Algo.InvalidParameter

请在设置界面点击 `MODEL CONFIGURATION`，勾选 **Enable R1 messages format**。
