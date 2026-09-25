> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Hermes Agent

> 在 Hermes Agent 中使用千问AI平台模型

## 安装 Hermes Agent

1. 在终端中执行以下命令，安装脚本会自动安装 Python、Git 等依赖。

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

<Note>
  Windows 不支持原生安装，请先安装 [WSL2](https://learn.microsoft.com/en-us/windows/wsl/install)，在 WSL2 中运行以上命令。
</Note>

2. 安装完成后，重新加载终端环境。

```bash
source ~/.bashrc    # 如果使用 zsh，改为 source ~/.zshrc
```

3. 验证安装是否成功。

```bash
hermes --version
```

若输出版本号，则安装成功。

## 配置接入凭证

通过 `hermes config set` 命令配置 Base URL 和 API Key，支持以下计费方案：

- **Token Plan 个人版**：个人订阅，按 token 消耗抵扣 Credits。
- **Token Plan 团队版**：按席位订阅，Token 消耗从 Credits 中扣减。
- **按量计费**：按实际用量后付费。

<Note>
  本文示例均使用 **Anthropic 兼容协议**：Base URL 以 `/apps/anthropic` 结尾，并将 `api_mode` 设为 `anthropic_messages`。Hermes Agent 同样支持 **OpenAI 兼容协议**：将 Base URL 结尾的 `/apps/anthropic` 替换为 `/compatible-mode/v1`，并删除 `api_mode` 配置项即可。例如按量计费的 OpenAI 兼容 Base URL 为 `https://dashscope.aliyuncs.com/compatible-mode/v1`。

  除命令行版外，Hermes Agent 还提供桌面版（Hermes Desktop）。可从 [Hermes 官网](https://hermes-agent.nousresearch.com/)下载安装包，或在命令行版安装完成后运行 `hermes desktop` 启动。桌面版与命令行版共用同一份 `~/.hermes/config.yaml` 配置文件，接入参数与本文一致；在桌面版中以自定义端点（Custom Endpoint）方式接入时，请使用上述 OpenAI 兼容 Base URL。
</Note>

## 配置 Token Plan 个人版

将 `YOUR_API_KEY` 替换为 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。可用模型：qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-flash、glm-5.2、deepseek-v4-pro，完整列表请参考 Token Plan 个人版[支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型)。

```bash
hermes config set model.provider custom
hermes config set model.base_url https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic
hermes config set model.api_mode anthropic_messages
hermes config set model.api_key YOUR_API_KEY
hermes config set model.default qwen3.8-max
```

以上命令将配置写入 `~/.hermes/config.yaml`。也可以直接编辑该文件，写入以下内容：

<Expandable title="config.yaml 配置示例">
  ```yaml
  model:
    default: qwen3.8-max
    provider: custom
    base_url: https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic
    api_mode: anthropic_messages
    api_key: YOUR_API_KEY
  ```
</Expandable>

<Warning>
  **qwen3.8-max 思考模式说明**：

  - thinking：支持开启和关闭（混合思考模式）。
  - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
  - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
</Warning>

## 配置 Token Plan 团队版

将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。可用模型请参考 Token Plan 团队版[支持的模型](/token-plan/team/token-plan-team-overview#支持的模型)。

```bash
hermes config set model.provider custom
hermes config set model.base_url https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic
hermes config set model.api_mode anthropic_messages
hermes config set model.api_key YOUR_API_KEY
hermes config set model.default qwen3.8-max
```

以上命令将配置写入 `~/.hermes/config.yaml`。也可以直接编辑该文件，写入以下内容：

<Expandable title="config.yaml 配置示例">
  ```yaml
  model:
    default: qwen3.8-max
    provider: custom
    base_url: https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic
    api_mode: anthropic_messages
    api_key: YOUR_API_KEY
  ```
</Expandable>

<Warning>
  **qwen3.8-max 思考模式说明**：

  - thinking：支持开启和关闭（混合思考模式）。
  - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
  - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
</Warning>

## 配置按量计费

将 `YOUR_API_KEY` 替换为千问AI平台 [API Key](/developer-guides/administration/api-keys)。可用模型请参考[支持的模型](/developer-guides/getting-started/text-generation-models)。

| 配置项          | 说明                                                                             |
| ------------ | ------------------------------------------------------------------------------ |
| **Base URL** | `https://dashscope.aliyuncs.com/apps/anthropic`                                |
| **API Key**  | 千问AI平台 [API Key](/developer-guides/administration/api-keys)（格式为 `sk-ws-xxxxx`） |
| **可用模型**     | [支持的模型](/developer-guides/getting-started/text-generation-models)              |

```bash
hermes config set model.provider alibaba
hermes config set model.base_url https://dashscope.aliyuncs.com/apps/anthropic
hermes config set model.api_mode anthropic_messages
hermes config set model.api_key YOUR_API_KEY
hermes config set model.default qwen3.7-max
```

以上命令将配置写入 `~/.hermes/config.yaml`。也可以直接编辑该文件，写入以下内容：

<Expandable title="config.yaml 配置示例">
  ```yaml
  model:
    default: qwen3.7-max
    provider: alibaba
    base_url: https://dashscope.aliyuncs.com/apps/anthropic
    api_mode: anthropic_messages
    api_key: YOUR_API_KEY
  ```
</Expandable>

## 切换模型

配置完成后，可以通过 `-m` 参数在对话时切换模型。

```bash
hermes chat -m qwen3.7-max
```

也可以通过 `hermes config set` 修改默认模型：

```bash
hermes config set model.default qwen3.7-max
```

Token Plan 团队版支持的模型详见 Token Plan 团队版概述。

<Note>
  文本模型（如 qwen3.6-plus、glm-5 等）可直接使用。图像生成模型需通过 Skill 接入，参见下方「接入图像生成模型」章节。
</Note>

## 接入图像生成模型

通过 Hermes Agent 的 Skill 机制，可以调用 Token Plan 团队版的图像生成模型（qwen-image-2.0、wan2.7-image 等）。

### 步骤一：配置环境变量

将 Token Plan 团队版专属 API Key 设置为环境变量 `TOKEN_PLAN_API_KEY`。

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export TOKEN_PLAN_API_KEY="REDACTED"
```

### 步骤二：创建 Skill

创建文件 `~/.hermes/skills/media/text-to-image/SKILL.md`，写入以下内容：

````
---
name: text-to-image
description: "Generates images from text descriptions using Token Plan multimodal generation API (qwen-image-2.0, wan2.7-image, etc.). Triggers when the user asks to draw, generate, or create an image."
version: 1.0.0
---

# Text-to-Image Generation

Generate images from text prompts via the Token Plan DashScope-compatible API.

## Trigger

Activate this skill when the user requests image generation.

## Pipeline

1. Extract parameters: prompt, model (default: qwen-image-2.0), size (default: 1024*1024).
2. Call the API:

```bash
curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $TOKEN_PLAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<model>",
    "input": {"messages": [{"role": "user", "content": [{"text": "<prompt>"}]}]},
    "parameters": {"size": "<size>"}
  }'
```

3. From the response JSON, extract `output.choices[*].message.content[*].image` URLs and download.
4. Report the saved file path to the user.

## Models

| Model              | Notes                                    |
| ------------------ | ---------------------------------------- |
| qwen-image-2.0     | Default, good at Chinese text rendering  |
| qwen-image-2.0-pro | Higher quality                           |
| wan2.7-image       | Multi-style, returns 4 images by default |
| wan2.7-image-pro   | Supports 4K output                       |

## Sizes

1024*1024, 720*1280, 1280*720. wan2.7-image-pro supports 2048*2048.
````

### 步骤三：使用

在 Hermes Agent 中描述图像需求（如"画一只猫"），Hermes Agent 会自动调用 text-to-image Skill 生成图片。

## 验证配置

执行以下命令，发送一条测试消息。

```bash
hermes chat -q "你好"
```

如果返回正常的 AI 回复，则配置成功。

如需进入交互式对话模式，直接执行：

```bash
hermes
```

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

- 按量付费：[错误码排查](/api-reference/preparation/error-messages)
- Token Plan 个人版：[Token Plan 常见问题](/token-plan/personal/token-plan-personal-faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)
