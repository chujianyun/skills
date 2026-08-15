> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 获取 API Key

> 使用模型的第一步

## 创建 API Key

<Steps>
  <Step title="创建 API Key">
    前往 [API Key](https://platform.qianwenai.com/home/api-keys) 页面，点击**创建 API Key**。
  </Step>

  <Step title="添加描述">
    输入描述信息以便识别该 Key，然后点击**生成 API Key**。
  </Step>

  <Step title="复制 API Key">
    请立即复制并保存 API Key。出于安全考虑，完整的 Key 仅在创建时显示一次，之后列表中仅显示掩码版本。
  </Step>
</Steps>

## 使用 API Key

<Note>
  [Token Plan 用户](/token-plan/overview)请使用 [API Key](https://platform.qianwenai.com/home/api-keys) 页面中的专属 API Key（`sk-sp-xxxxx` 格式），不要使用此处的通用 API Key（`sk-ws-xxxxx` 格式）。
</Note>

- **方式一：在第三方工具中使用（如 [Chatbox](/developer-guides/clients-and-developer-tools/chatbox)）**

  在第三方工具中调用模型时，需要提供以下信息：

  - API Key（按上述步骤创建后获取）
  - Base URL：`https://dashscope.aliyuncs.com/compatible-mode/v1`
  - 模型名称（如 `qwen3.7-plus`）

- **方式二：通过代码调用**

  [将 API Key 设置为环境变量](/api-reference/preparation/export-api-key-env)，避免在源代码中硬编码。

<Note>
  通过代码或第三方工具调用模型时，除 API Key 外还需指定**服务端点**（对应 SDK 或 HTTP 请求中的 `base_url`）。千问AI平台同时提供 **OpenAI 兼容**与 **Anthropic 兼容**两种协议的接口，两种协议的 `base_url` 不同，请以对应接口文档中的说明为准：

  - OpenAI 兼容协议：[OpenAI 兼容-Chat](/api-reference/chat/openai-chat)
  - Anthropic 兼容协议：[Anthropic 兼容-Messages](/api-reference/chat/anthropic)
</Note>

切勿泄露 API Key，未经授权的使用会带来安全风险和经济损失。

## 管理 API Key

在 [API Key](https://platform.qianwenai.com/home/api-keys) 页面中，您可以：

- **搜索**：通过描述信息查找 Key。
- **编辑**：修改已有 Key 的描述信息。
- **删除**：永久删除 Key。删除后无法恢复，使用该 Key 的应用将停止运行。

## 有效期

API Key 永久有效，除非您手动删除。

## 常见问题

### 按量付费 API Key 与 Token Plan API Key 的区别

通用 API Key（`sk-ws-xxxxx`，早期创建的 Key 为 `sk-xxxxx`）按 API 调用量计费。Token Plan API Key（`sk-sp-xxxxx`）绑定订阅套餐，按 Credits（token 用量）计费。

### 用 echo 命令确认环境变量设置成功了，为什么运行代码还是提示找不到 API Key？

具体原因如下：

- 情况一：**没有设置永久性环境变量**。临时环境变量只在当前终端会话有效，对于已经启动的 IDE 或其他应用程序并不会生效。请参考[配置 API Key 到环境变量](/api-reference/preparation/export-api-key-env)设置永久性环境变量。
- 情况二：**没有重启 IDE、命令行工具或应用**。通常需要重启 IDE（如 VS Code）或命令行工具，使其能够加载最新的环境变量。如果在部署应用后设置了环境变量，可能需要重启应用服务。
- 情况三：**需要在配置文件添加环境变量**。如果您的应用是通过服务管理器（如 systemd、supervisord）启动的，可能需要在服务管理器的配置文件中添加环境变量。
- 情况四：**用了 sudo 命令**。`sudo` 默认不继承所有环境变量。可采用 `sudo -E python xx.py` 命令，其中 `-E` 参数确保环境变量被传递。
