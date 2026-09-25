> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Codex

> 在 Codex 中使用千问AI平台模型

Codex 是 OpenAI 推出的终端 AI 编程助手。可通过 Token Plan 个人版、Token Plan 团队版或按量计费接入千问AI平台。

## 安装 Codex

1. 安装或更新 [Node.js](https://nodejs.org/en/download/)（v18.0 或更高版本）。

2. 在终端中执行以下命令安装 Codex。

```bash
npm install -g @openai/codex
```

执行以下命令验证安装。

```bash
codex --version
```

## 配置接入凭证

接入需要编辑配置文件 `~/.codex/config.toml` 并配置环境变量 `OPENAI_API_KEY`。根据所选计费方案替换对应值，千问AI平台提供以下计费方案：

### 配置模型元数据

使用自定义模型（如 qwen3.8-max）时，需要配置模型元数据文件，使 Codex 正确识别模型的上下文窗口、推理深度等参数。

1. 新建文件 `~/.codex/model-catalog.local.json`，写入以下内容：

```json
{
  "models": [
    {
      "slug": "qwen3.8-max",
      "display_name": "qwen3.8-max",
      "description": "DashScope model: qwen3.8-max",
      "default_reasoning_level": "xhigh",
      "supported_reasoning_levels": [
        {
          "effort": "low",
          "description": "Fast responses with lighter reasoning"
        },
        {
          "effort": "medium",
          "description": "Greater reasoning depth for complex problems"
        },
        {
          "effort": "xhigh",
          "description": "Extra high reasoning depth for complex problems"
        }
      ],
      "context_window": 983616,
      "effective_context_window_percent": 95,
      "supports_parallel_tool_calls": false,
      "supports_image_detail_original": true,
      "input_modalities": ["text", "image"],
      "shell_type": "default",
      "visibility": "list",
      "supported_in_api": true,
      "priority": 1,
      "base_instructions": "",
      "support_verbosity": false,
      "supports_reasoning_summaries": false,
      "experimental_supported_tools": [],
      "truncation_policy": {
        "mode": "bytes",
        "limit": 10000
      }
    }
  ]
}
```

2. 在 `~/.codex/config.toml` 中添加以下配置，指向元数据文件：

```plaintext
model_catalog_json = "~/.codex/model-catalog.local.json"
```

### Token Plan 个人版

`model` 请选择支持的模型，可用模型包括 qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-flash、glm-5.2、deepseek-v4-pro、deepseek-v4-flash-0731。将 `OPENAI_API_KEY` 环境变量设置为 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。

#### Responses API（qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash）

qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-plus 和 qwen3.6-flash 支持 Responses API，可使用最新版 Codex。

```plaintext
model_provider = "Model_Studio_Token_Plan_Personal"
model = "qwen3.8-max"
[model_providers.Model_Studio_Token_Plan_Personal]
name = "Model_Studio_Token_Plan_Personal"
base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "responses"
```

#### Chat/Completions API（其他模型）

其他模型需通过 Chat/Completions API 接入，需安装旧版本 Codex，如 0.80.0：

```bash
npm install -g @openai/codex@0.80.0
```

```plaintext
model_provider = "Model_Studio_Token_Plan_Personal"
model = "glm-5"
[model_providers.Model_Studio_Token_Plan_Personal]
name = "Model_Studio_Token_Plan_Personal"
base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "chat"
```

#### 配置环境变量

将 `OPENAI_API_KEY` 环境变量设置为 Token Plan 个人版专属 API Key。

<Tabs>
  <Tab title="macOS">
    1. 在终端中执行以下命令，查看默认 Shell 类型。

    ```bash
    echo $SHELL
    ```

    2. 根据 Shell 类型设置环境变量：

    <Tabs>
      <Tab title="zsh">
        ```bash
        # 将 YOUR_API_KEY 替换为 Token Plan 个人版 API Key
        echo 'export OPENAI_API_KEY="REDACTED"' >> ~/.zshrc
        ```
      </Tab>

      <Tab title="bash">
        ```bash
        # 将 YOUR_API_KEY 替换为 Token Plan 个人版 API Key
        echo 'export OPENAI_API_KEY="REDACTED"' >> ~/.bash_profile
        ```
      </Tab>
    </Tabs>

    3. 在终端中执行下列命令，使环境变量生效。

    <Tabs>
      <Tab title="zsh">
        ```bash
        source ~/.zshrc
        ```
      </Tab>

      <Tab title="bash">
        ```bash
        source ~/.bash_profile
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Windows">
    <Tabs>
      <Tab title="CMD">
        1. 在 CMD 中运行以下命令，设置环境变量。

        ```powershell
        REM 将 YOUR_API_KEY 替换为 Token Plan 个人版 API Key
        setx OPENAI_API_KEY "YOUR_API_KEY"
        ```

        2. 打开一个新的 CMD 窗口，运行以下命令，检查环境变量是否生效。

        ```powershell
        echo %OPENAI_API_KEY%
        ```
      </Tab>

      <Tab title="PowerShell">
        1. 在 PowerShell 中运行以下命令，设置环境变量。

        ```powershell
        # 将 YOUR_API_KEY 替换为 Token Plan 个人版 API Key
        [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_API_KEY", [EnvironmentVariableTarget]::User)
        ```

        2. 打开一个新的 PowerShell 窗口，运行以下命令，检查环境变量是否生效。

        ```powershell
        echo $env:OPENAI_API_KEY
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

<Note>
  **qwen3.8-max 思考模式说明**：

  - thinking：支持开启和关闭（混合思考模式）。
  - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
  - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
</Note>

### Token Plan 团队版

`model` 请选择支持的模型。将 `OPENAI_API_KEY` 环境变量设置为 Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。

<Note>
  文本模型（如 qwen3.6-plus、glm-5 等）可直接使用。图像生成模型需通过 Skill 接入，参见[接入图像生成模型](#接入图像生成模型)。
</Note>

#### Responses API（qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash）

qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-plus 和 qwen3.6-flash 支持 Responses API，可使用最新版 Codex。

```plaintext
model_provider = "Model_Studio_Token_Plan"
model = "qwen3.8-max"
[model_providers.Model_Studio_Token_Plan]
name = "Model_Studio_Token_Plan"
base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "responses"
```

#### Chat/Completions API（其他模型）

其他模型需通过 Chat/Completions API 接入，需安装旧版本 Codex，如 0.80.0：

```plaintext
model_provider = "Model_Studio_Token_Plan"
model = "glm-5"
[model_providers.Model_Studio_Token_Plan]
name = "Model_Studio_Token_Plan"
base_url = "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "chat"
```

### 配置环境变量

将配置文件中的 `OPENAI_API_KEY` 环境变量设置为 Token Plan 团队版专属 API Key。

<Tabs>
  <Tab title="macOS">
    1. 在终端中执行以下命令，查看默认 Shell 类型。

    ```bash
    echo $SHELL
    ```

    2. 根据 Shell 类型设置环境变量，命令如下：

    <Tabs>
      <Tab title="zsh">
        ```bash
        # 将 YOUR_API_KEY 替换为 Token Plan 团队版 API Key
        echo 'export OPENAI_API_KEY="REDACTED"' >> ~/.zshrc
        ```
      </Tab>

      <Tab title="bash">
        ```bash
        # 将 YOUR_API_KEY 替换为 Token Plan 团队版 API Key
        echo 'export OPENAI_API_KEY="REDACTED"' >> ~/.bash_profile
        ```
      </Tab>
    </Tabs>

    3. 在终端中执行下列命令，使环境变量生效。

    <Tabs>
      <Tab title="zsh">
        ```bash
        source ~/.zshrc
        ```
      </Tab>

      <Tab title="bash">
        ```bash
        source ~/.bash_profile
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Windows">
    <Tabs>
      <Tab title="CMD">
        1. 在 CMD 中运行以下命令，设置环境变量。

        ```powershell
        REM 将 YOUR_API_KEY 替换为 Token Plan 团队版 API Key
        setx OPENAI_API_KEY "YOUR_API_KEY"
        ```

        2. 打开一个新的 CMD 窗口，运行以下命令，检查环境变量是否生效。

        ```powershell
        echo %OPENAI_API_KEY%
        ```
      </Tab>

      <Tab title="PowerShell">
        1. 在 PowerShell 中运行以下命令，设置环境变量。

        ```powershell
        # 将 YOUR_API_KEY 替换为 Token Plan 团队版 API Key
        [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_API_KEY", [EnvironmentVariableTarget]::User)
        ```

        2. 打开一个新的 PowerShell 窗口，运行以下命令，检查环境变量是否生效。

        ```powershell
        echo $env:OPENAI_API_KEY
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

<Note>
  **qwen3.8-max 思考模式说明**：

  - thinking：支持开启和关闭（混合思考模式）。
  - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
  - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
</Note>

## 接入图像生成模型

通过 Codex 的 Skill 机制，可以调用 Token Plan 团队版的图像生成模型（qwen-image-2.0、wan2.7-image 等）。

### 步骤一：创建 Skill

创建文件 `~/.codex/skills/token-plan-image/SKILL.md`，完整复制以下内容并粘贴。

````plaintext
---
name: "token-plan-image"
description: "Generate images from text descriptions using Token Plan's image generation API (qwen-image-2.0, wan2.7-image, etc.). Activate when the user asks to draw, generate, or create an image."
---

# Token Plan Image Generation

Generate images from text prompts via the Token Plan API.

## When to use

Activate this skill when the user requests image generation.

## Pipeline

1. Extract parameters from the user's request: prompt, model (default: qwen-image-2.0), size (default: 1024*1024).
2. Call the API with curl:

```bash
curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"MODEL_NAME","input":{"messages":[{"role":"user","content":[{"text":"PROMPT_TEXT"}]}]},"parameters":{"size":"IMAGE_SIZE"}}'
```

3. Extract the image URL from the response JSON (located at output.choices[].message.content[].image).
4. Download the image with curl and report the saved file path to the user.

## Important

Do NOT attempt to view or read the generated image file. The model does not support image input and will error. Only report the file path.
````

### 步骤二：使用

在 Codex 中描述图像需求，Codex 会自动调用 token-plan-image Skill 生成图片。

## 使用 Codex

1. 新建一个终端，执行以下命令进入 Codex。

```bash
codex
```

2. 开始对话。

## 配置按量计费

将 `OPENAI_API_KEY` 环境变量设置为千问AI平台 [API Key](/developer-guides/administration/api-keys)。可用模型请参考[支持的模型](/developer-guides/getting-started/text-generation-models)。

| 配置项          | 说明                                                                                                      |
| ------------ | ------------------------------------------------------------------------------------------------------- |
| **Base URL** | `https://dashscope.aliyuncs.com/compatible-mode/v1`                                                     |
| **API Key**  | 千问AI平台 [API Key](/developer-guides/administration/api-keys)（格式为 `sk-ws-xxxxx`），设为 `OPENAI_API_KEY` 环境变量 |
| **可用模型**     | [支持的模型](/developer-guides/getting-started/text-generation-models)                                       |

按量计费支持 Responses API 和 Chat/Completions API 两种接入方式，请根据使用的模型选择：

### Responses API

适用于支持 [OpenAI Responses API](/api-reference/chat/openai-responses) 的模型（如 qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash），可使用最新版 Codex。

```plaintext
model_provider = "Model_Studio"
model = "qwen3.7-max"
[model_providers.Model_Studio]
name = "Model_Studio"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "responses"
```

### Chat/Completions API

适用于仅支持 Chat/Completions API 的模型，需安装 Codex 0.80.0：

```plaintext
model_provider = "Model_Studio"
model = "qwen3.6-plus"
[model_providers.Model_Studio]
name = "Model_Studio"
base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
env_key = "OPENAI_API_KEY"
wire_api = "chat"
```

### 配置环境变量

<Tabs>
  <Tab title="macOS">
    1. 在终端中执行以下命令，查看默认 Shell 类型。

    ```bash
    echo $SHELL
    ```

    2. 根据 Shell 类型设置环境变量：

    <Tabs>
      <Tab title="Zsh">
        ```bash
        # 将 YOUR_API_KEY 替换为千问AI平台 API Key
        echo 'export OPENAI_API_KEY="REDACTED"' >> ~/.zshrc
        ```
      </Tab>

      <Tab title="Bash">
        ```bash
        # 将 YOUR_API_KEY 替换为千问AI平台 API Key
        echo 'export OPENAI_API_KEY="REDACTED"' >> ~/.bash_profile
        ```
      </Tab>
    </Tabs>

    3. 执行以下命令使环境变量生效。

    <Tabs>
      <Tab title="Zsh">
        ```bash
        source ~/.zshrc
        ```
      </Tab>

      <Tab title="Bash">
        ```bash
        source ~/.bash_profile
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Windows">
    <Tabs>
      <Tab title="CMD">
        1. 在 CMD 中运行以下命令，设置环境变量。

        ```powershell
        REM 将 YOUR_API_KEY 替换为千问AI平台 API Key
        setx OPENAI_API_KEY "YOUR_API_KEY"
        ```

        2. 打开一个新的 CMD 窗口，运行以下命令检查环境变量是否生效。

        ```powershell
        echo %OPENAI_API_KEY%
        ```
      </Tab>

      <Tab title="PowerShell">
        1. 在 PowerShell 中运行以下命令，设置环境变量。

        ```powershell
        # 将 YOUR_API_KEY 替换为千问AI平台 API Key
        [Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "YOUR_API_KEY", [EnvironmentVariableTarget]::User)
        ```

        2. 打开一个新的 PowerShell 窗口，运行以下命令检查环境变量是否生效。

        ```powershell
        echo $env:OPENAI_API_KEY
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

## 常见问题

### 第三方工具提示"不支持国内模型"或"检查被拒 / Bad request (400)"怎么办？

**原因**：部分第三方管理工具（如 CC-Switch）在切换供应商时会发起"健康检查/连接测试"探测请求，该探测请求的格式与 Codex 实际调用的请求格式不同，千问AI平台网关可能因此返回 400 Bad request 并提示"检查被拒"，工具据此显示"不支持国内模型"。此提示仅代表健康检查探测未通过，**并不代表千问AI平台不支持国内模型，也不影响 Codex 的实际使用。**

<Note>千问AI平台支持通过 Codex 使用 qwen3.7-max、qwen3.7-plus、qwen3.6-plus、qwen3.6-flash、glm-5 等国内模型，配置方式详见上文[配置接入凭证](#配置接入凭证)。</Note>

**解决方案**：建议参照上文配置说明，直接在 `~/.codex/config.toml` 中完成配置，无需依赖第三方工具的健康检查结果；配置完成后参照[使用 Codex](#使用-codex)启动 Codex，若能正常进入对话界面即表示可正常使用国内模型。

### 报错 wire\_api 配置问题怎么办？

**原因**：Codex 新版本不再支持 `wire_api = "chat"` 配置。根据版本不同，可能出现以下报错：

- `wire_api = "chat" is no longer supported`
- `unknown configuration field wire_api`

**解决方案**：

- 报错 `wire_api = "chat" is no longer supported`：将配置文件中的 `wire_api` 改为 `responses`，并确认 `base_url` 配置正确。详见上文[配置接入凭证](#配置接入凭证)中对应方案的配置示例。
- 报错 `unknown configuration field wire_api`：从配置文件 `~/.codex/config.toml` 的对应 provider 节中删除 `wire_api` 字段。

### 报错 unexpected status 401 Unauthorized 怎么办？

**原因**：

- 误用了其他方案的 API Key（Token Plan 个人版、Token Plan 团队版和按量计费的 API Key 互不相通）
- 订阅过期
- API Key 复制不完整、有空格或拼写错误

**解决方案**：

- 确认使用的是所选方案的专属 API Key。
- 前往对应方案的管理页面确认订阅是否过期。
- 重新复制 API Key，确保完整且无空格。
- 如以上均正常仍报错，可在对应方案的管理页面重置 API Key，重置后请使用新 API Key 进行配置。

### 报错 unexpected status 404 Not Found 怎么办？

**原因**：配置文件中的 `base_url` 或 `wire_api` 填写错误。

**解决方案**：确认 `base_url` 和 `wire_api` 与所选方案的配置一致。参见上文[配置接入凭证](#配置接入凭证)中对应方案的配置示例。

### 报错 stream disconnected before completion: stream closed before response.completed 怎么办？

**原因**：Codex 与服务端的流式连接在响应完成前断开。常见于以下场景：

- 对话线程过长，Codex 触发上下文压缩时请求失败
- 网络不稳定，SSE 或 WebSocket 连接中途断开
- 服务端过载或触发限流，提前终止连接

**解决方案**：

- 开启新的对话线程，避免单个线程积累过多上下文。
- 检查网络连接是否稳定，关闭 VPN 或代理后重试。
- 等待一段时间后重试，Codex 内置了自动重试机制，多数情况下重试可恢复。

### 报错 429 请求超频或额度用尽怎么办？

**原因**：429 错误有以下两种情形：

- **请求超频**（`429 Requests rate limit exceeded`）：短时间内请求过于密集。
- **限额用尽**（`429 Allocated quota exceeded` 或 `Your token-plan 1-week quota has been exhausted`）：Token Plan 个人版的 7 天限额触顶。

**解决方案**：

- 请求超频：等待一分钟后重试，降低请求频率。
- 限额用尽：等待 7 天窗口周期结束后额度自动重置；或购买用量包（用量包额度不受窗口限额约束）；或升级套餐。注意：报错信息中的重置时间（如 `The quota will reset at HH:MM:SS UTC`）以协调世界时（UTC）为准，换算为北京时间（CST）需加 8 小时。
