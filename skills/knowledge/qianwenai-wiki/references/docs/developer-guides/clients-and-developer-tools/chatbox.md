> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Chatbox

> 在 Chatbox 中使用千问AI平台模型

Chatbox 是一款跨平台 AI 客户端应用，可以通过 Token Plan 个人版、Token Plan 团队版或按量计费接入千问AI平台。

## 下载安装 Chatbox

前往 [Chatbox 官网](https://chatboxai.app/zh)，根据操作系统下载并安装，或直接使用网页版。

## 配置接入凭证

点击 Chatbox 页面左下方的**设置**，点击**模型提供方**，点击底部的**添加**。在弹窗中填写**名称**，**API 模式**选择 **OpenAI API 兼容**，点击**添加**。然后根据所选方案，填入对应的 API 密钥和 API 主机。

千问AI平台提供以下计费方案，根据需要选择：

- **Token Plan 个人版**：按 token 消耗抵扣个人 Credits。
- **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
- **按量计费**：按实际调用量后付费。

### Token Plan 个人版

| 配置项        | 说明                                                                                                                     |
| ---------- | ---------------------------------------------------------------------------------------------------------------------- |
| **API 密钥** | 填入 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。                                           |
| **API 主机** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。API 路径无需填写。                                       |
| **模型**     | 点击**新建**，在**模型 ID**中填入 Token Plan 个人版[支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型)，如 `qwen3.8-max`。 |

### Token Plan 团队版

| 配置项        | 说明                                                                               |
| ---------- | -------------------------------------------------------------------------------- |
| **API 密钥** | 填入 Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。     |
| **API 主机** | `https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`。API 路径无需填写。 |
| **模型**     | 点击**新建**，在**模型 ID**中填入模型名称。可用模型请参考 Token Plan 团队版[支持的模型](/token-plan/overview)。  |

### 按量计费

| 配置项        | 说明                                                                                       |
| ---------- | ---------------------------------------------------------------------------------------- |
| **API 密钥** | 填入千问AI平台 [API Key](/developer-guides/administration/api-keys)。                           |
| **API 主机** | `https://dashscope.aliyuncs.com/compatible-mode/v1`。API 路径无需填写。                          |
| **模型**     | 点击**新建**，在**模型 ID**中填入[支持的模型](/developer-guides/getting-started/text-generation-models)。 |

## 验证配置

完成配置后，在对话框输入"你好"并发送，模型正常返回响应即配置成功。

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

- 按量计费：[错误码排查](/api-reference/preparation/error-messages)
- Token Plan 个人版：[Token Plan 常见问题](/token-plan/faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)
