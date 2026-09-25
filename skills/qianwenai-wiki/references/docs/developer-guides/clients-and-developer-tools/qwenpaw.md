> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# QwenPaw

> 在 QwenPaw 中使用千问AI平台模型

QwenPaw（原 CoPaw）是 AgentScope 团队开源的个人 AI 助手，支持本地或云端部署，可通过 Token Plan 个人版、Token Plan 团队版或按量计费接入千问AI平台。

## 安装 QwenPaw

推荐 pip 包或一键安装脚本。Docker、桌面端、ModelScope 在线运行等方式参考 [QwenPaw 官方文档](https://qwenpaw.agentscope.io/)。

<Tabs>
  <Tab title="一键脚本">
    脚本自动安装 uv、创建虚拟环境并下载依赖，无需手动配置 Python。根据操作系统选择对应命令：

    - macOS / Linux：

    ```bash
    curl -fsSL https://qwenpaw.agentscope.io/install.sh | bash
    ```

    - Windows（CMD）：

    ```bash
    curl -fsSL https://qwenpaw.agentscope.io/install.bat -o install.bat && install.bat
    ```

    - Windows（PowerShell）：

    ```powershell
    irm https://qwenpaw.agentscope.io/install.ps1 | iex
    ```

    安装完成后，在新终端执行：

    ```bash
    qwenpaw init --defaults
    qwenpaw app
    ```
  </Tab>

  <Tab title="pip 安装">
    需 Python 3.10 \~ 3.13：

    ```bash
    pip install qwenpaw
    qwenpaw init --defaults
    qwenpaw app
    ```
  </Tab>
</Tabs>

启动后访问 `http://127.0.0.1:8088/` 打开 QwenPaw Console。

## 配置接入凭证

在 Console 点击**设置** > **模型**，根据计费方案配置对应的提供商。

### Token Plan 个人版

进入内置的 **Aliyun Token Plan** 提供商**设置**页面，填入 API Key。

| 配置项        | 说明                                                                                                                  |
| ---------- | ------------------------------------------------------------------------------------------------------------------- |
| **API 密钥** | 填入 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。                                        |
| **模型**     | 已预设常用模型。新增模型点击**添加模型**，**模型 ID** 填入 Token Plan 个人版[支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型)。 |

### Token Plan 团队版

进入内置的 **Aliyun Token Plan** 提供商**设置**页面，填入 API Key。

| 配置项        | 说明                                                                                                          |
| ---------- | ----------------------------------------------------------------------------------------------------------- |
| **API 密钥** | 填入 Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/billing/subscription/token-plan)。         |
| **模型**     | 已预设常用模型。新增模型点击**添加模型**，**模型 ID** 填入 Token Plan 团队版[支持的模型](/token-plan/team/token-plan-team-overview#支持的模型)。 |

### 按量计费

进入内置的 **DashScope** 提供商**设置**页面，填入 API Key。

| 配置项        | 说明                                                                                                    |
| ---------- | ----------------------------------------------------------------------------------------------------- |
| **API 密钥** | 填入[千问AI平台 API Key](/api-reference/preparation/api-key)。                                               |
| **基础 URL** | `https://dashscope.aliyuncs.com/compatible-mode/v1`                                                   |
| **模型**     | 已预设常用模型。新增模型点击**添加模型**，**模型 ID** 填入[支持的模型](/developer-guides/getting-started/text-generation-models)。 |

## 设置默认模型

进入**设置** > **模型** > **默认LLM**选择模型并**保存**。聊天页面右上角下拉菜单可临时切换当前会话的提供商和模型。

## 常见问题

### 错误码

按计费方案排查：

- 按量计费：[错误码排查](/api-reference/preparation/error-messages)
- Token Plan 个人版：[Token Plan 个人版常见问题](/token-plan/faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)

### 报错 401 Incorrect API key provided

可能原因：

- 两种计费方案的 API Key 不通用，确认与基础 URL 来自同一方案。

### 长对话或工具调用时报错上下文超限

在该模型的提供商**设置**页面展开**进阶配置**，按 JSON 格式调整 `max_tokens` 等生成参数后保存：

```json
{
  "temperature": 0.7,
  "top_p": 0.9,
  "max_tokens": 4096
}
```
