> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# OpenClaw

> 在 OpenClaw 中使用千问AI平台模型

OpenClaw（昵称"龙虾"）是一个开源的个人 AI 助手平台，支持通过多种消息渠道与 AI 交互。

## 安装 OpenClaw

1. **安装或更新 Node.js**

   在终端运行以下命令查看当前 Node.js 版本（需 v22.19.0 或更高版本）。如果提示"找不到命令"，说明未安装；如果显示版本号低于 v22.19.0，说明需要更新。

```bash
node -v
```

访问 [nodejs.org](https://nodejs.org/en/download/)，在页面中选择"LTS"且版本号 >= 22.x.x，根据系统下载安装包。

2. **执行安装命令**

<Tabs>
  <Tab title="macOS/Linux">
    按 Command + Space 打开终端，运行：

    ```bash
    curl -fsSL https://openclaw.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows">
    在任务栏搜索框输入 `PowerShell`，选择以管理员身份运行，执行：

    ```powershell
    iwr -useb https://openclaw.ai/install.ps1 | iex
    ```
  </Tab>
</Tabs>

3. **完成 Onboarding Wizard 配置**

   安装结束后会自动出现提示信息，请根据提示完成配置：

| 配置项                                                           | 配置内容                            |
| ------------------------------------------------------------- | ------------------------------- |
| I understand this is powerful and inherently risky. Continue? | 选择 "Yes"                        |
| Onboarding mode                                               | 选择 "QuickStart"                 |
| Model/auth provider                                           | 选择 "Skip for now"，后续可以配置        |
| Filter models by provider                                     | 选择 "All providers"              |
| Default model                                                 | 使用默认配置                          |
| Select channel (QuickStart)                                   | 选择 "Skip for now"，后续可以配置        |
| Configure skills now? (recommended)                           | 选择 "No"，后续可以配置                  |
| Enable hooks?                                                 | 按空格键选中 "Skip for now"，按回车键进入下一步 |
| How do you want to hatch your bot?                            | 选择 "Do this later"              |

## 配置 Token Plan 个人版

将 `YOUR_API_KEY` 替换为 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。可用模型包括 qwen3.8-max、qwen3.7-max、qwen3.7-plus、qwen3.6-flash、glm-5.2、deepseek-v4-pro、deepseek-v4-flash-0731，完整列表请参考 Token Plan 个人版[支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型)。

| 配置项          | 说明                                                                             |
| ------------ | ------------------------------------------------------------------------------ |
| **API Key**  | Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)       |
| **Base URL** | `https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`               |
| **可用模型**     | Token Plan 个人版[支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型) |

配置文件位于 `~/.openclaw/openclaw.json`，OpenClaw 启动时会自动读取。

<Note>
  示例禁用了网关鉴权（`auth.mode: none`），仅适合单机本地使用。如需共享或远程访问，请运行 `openclaw doctor --fix` 启用 token 鉴权。
</Note>

**首次配置**：复制以下内容到配置文件，将 `YOUR_API_KEY` 替换为 Token Plan 个人版 API Key。

**已有配置**：若需保留已有配置，请勿直接全量替换，详见[已有配置如何安全修改](#已有配置如何安全修改)。

```json
{
  "meta": {
    "lastTouchedVersion": "2026.2.1",
    "lastTouchedAt": "2026-02-03T08:20:00.000Z"
  },
  "models": {
    "mode": "merge",
    "providers": {
      "bailian-token-plan": {
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
        "apiKey": "YOUR_API_KEY",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "qwen3.8-max",
            "name": "qwen3.8-max",
            "reasoning": true,
            "input": ["text", "image"],
            "contextWindow": 983616,
            "maxTokens": 131072,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "qwen3.7-max",
            "name": "qwen3.7-max",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 1000000,
            "maxTokens": 65536,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "qwen3.7-plus",
            "name": "qwen3.7-plus",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 1000000,
            "maxTokens": 65536,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "qwen3.6-flash",
            "name": "qwen3.6-flash",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 1000000,
            "maxTokens": 32768,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "glm-5.2",
            "name": "glm-5.2",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 1000000,
            "maxTokens": 16384,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "deepseek-v4-pro",
            "name": "deepseek-v4-pro",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 163840,
            "maxTokens": 32768,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          },
          {
            "id": "deepseek-v4-pro-0813",
            "name": "deepseek-v4-pro-0813",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 163840,
            "maxTokens": 32768,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          },
          {
            "id": "deepseek-v4-flash-0731",
            "name": "deepseek-v4-flash-0731",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 1000000,
            "maxTokens": 393216,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "bailian-token-plan/qwen3.8-max"
      },
      "models": {
        "bailian-token-plan/qwen3.8-max": {},
        "bailian-token-plan/qwen3.7-max": {},
        "bailian-token-plan/qwen3.7-plus": {},
        "bailian-token-plan/qwen3.6-flash": {},
        "bailian-token-plan/glm-5.2": {},
        "bailian-token-plan/deepseek-v4-pro": {},
        "bailian-token-plan/deepseek-v4-pro-0813": {},
        "bailian-token-plan/deepseek-v4-flash-0731": {}
      }
    }
  },
  "gateway": {
    "mode": "local",
    "auth": { "mode": "none" }
  }
}
```

<Warning>
  **qwen3.8-max 思考模式说明**：

  - thinking：支持开启和关闭（混合思考模式）。
  - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
  - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
</Warning>

## 配置 Token Plan 团队版

<Note>
  示例禁用了网关鉴权（`auth.mode: none`），仅适合单机本地使用。如需共享或远程访问，请运行 `openclaw doctor --fix` 启用 token 鉴权。
</Note>

<Tabs>
  <Tab title="通过终端修改">
    1. 在终端执行以下命令打开配置文件：

    ```bash
    nano ~/.openclaw/openclaw.json
    ```

    2. **首次配置**：复制以下内容到配置文件，将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 API Key。

       **已有配置**：若需保留已有配置，请勿直接全量替换，详见[已有配置如何安全修改](#已有配置如何安全修改)。

    ```json
    {
      "models": {
        "mode": "merge",
        "providers": {
          "qwencloud-token-plan": {
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.8-max",
                "name": "qwen3.8-max",
                "reasoning": true,
                "input": ["text", "image"],
                "contextWindow": 983616,
                "maxTokens": 131072,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.7-max",
                "name": "qwen3.7-max",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.7-plus",
                "name": "qwen3.7-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.6-flash",
                "name": "qwen3.6-flash",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "deepseek-v4-pro",
                "name": "deepseek-v4-pro",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v4-pro-0813",
                "name": "deepseek-v4-pro-0813",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v4-flash",
                "name": "deepseek-v4-flash",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v4-flash-0731",
                "name": "deepseek-v4-flash-0731",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 1000000,
                "maxTokens": 393216,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v3.2",
                "name": "deepseek-v3.2",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "kimi-k2.7-code",
                "name": "kimi-k2.7-code",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "kimi-k2.6",
                "name": "kimi-k2.6",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "kimi-k2.5",
                "name": "kimi-k2.5",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-5.2",
                "name": "glm-5.2",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 1000000,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-5.1",
                "name": "glm-5.1",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 204800,
                "maxTokens": 131072,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "qwencloud-token-plan/qwen3.8-max"
          },
          "models": {
            "qwencloud-token-plan/qwen3.8-max": {},
            "qwencloud-token-plan/qwen3.7-max": {},
            "qwencloud-token-plan/qwen3.7-plus": {},
            "qwencloud-token-plan/qwen3.6-plus": {},
            "qwencloud-token-plan/qwen3.6-flash": {},
            "qwencloud-token-plan/deepseek-v4-pro": {},
            "qwencloud-token-plan/deepseek-v4-pro-0813": {},
            "qwencloud-token-plan/deepseek-v4-flash": {},
            "qwencloud-token-plan/deepseek-v4-flash-0731": {},
            "qwencloud-token-plan/deepseek-v3.2": {},
            "qwencloud-token-plan/kimi-k2.7-code": {},
            "qwencloud-token-plan/kimi-k2.6": {},
            "qwencloud-token-plan/kimi-k2.5": {},
            "qwencloud-token-plan/glm-5.2": {},
            "qwencloud-token-plan/glm-5.1": {},
            "qwencloud-token-plan/glm-5": {},
            "qwencloud-token-plan/MiniMax-M2.5": {}
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": { "mode": "none" }
      }
    }
    ```

    <Note>
      如需添加更多模型，请在 `providers.qwencloud-token-plan.models` 中添加模型定义，在 `agents.defaults.models` 中添加 `"qwencloud-token-plan/模型ID": {}` 条目。可用模型请参考 Token Plan 团队版[支持的模型](/token-plan/overview)。
    </Note>

    3. 保存文件并退出，运行以下命令使配置生效：

    ```bash
    openclaw gateway restart
    ```
  </Tab>

  <Tab title="通过网页浏览器修改">
    1. 在终端运行以下命令启动 Web UI：

    ```bash
    openclaw dashboard
    ```

    2. 在左侧菜单依次选择**配置 > Settings > Advanced**，单击 **Open** 打开配置编辑界面。

       - **首次配置**：复制以下内容替换已有内容。
       - **已有配置**：若需保留已有配置，请勿直接全量替换，详见[已有配置如何安全修改](#已有配置如何安全修改)。

       将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 API Key：

    ```json
    {
      "models": {
        "mode": "merge",
        "providers": {
          "qwencloud-token-plan": {
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.8-max",
                "name": "qwen3.8-max",
                "reasoning": true,
                "input": ["text", "image"],
                "contextWindow": 983616,
                "maxTokens": 131072,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.7-max",
                "name": "qwen3.7-max",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.7-plus",
                "name": "qwen3.7-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "qwen3.6-flash",
                "name": "qwen3.6-flash",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 1000000,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "deepseek-v4-pro",
                "name": "deepseek-v4-pro",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v4-pro-0813",
                "name": "deepseek-v4-pro-0813",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v4-flash",
                "name": "deepseek-v4-flash",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v4-flash-0731",
                "name": "deepseek-v4-flash-0731",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 1000000,
                "maxTokens": 393216,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              },
              {
                "id": "deepseek-v3.2",
                "name": "deepseek-v3.2",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "kimi-k2.7-code",
                "name": "kimi-k2.7-code",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 32768,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "kimi-k2.6",
                "name": "kimi-k2.6",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "kimi-k2.5",
                "name": "kimi-k2.5",
                "reasoning": false,
                "input": ["text", "image"],
                "contextWindow": 262144,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-5.2",
                "name": "glm-5.2",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 1000000,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-5.1",
                "name": "glm-5.1",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 202752,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 204800,
                "maxTokens": 131072,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "qwencloud-token-plan/qwen3.8-max"
          },
          "models": {
            "qwencloud-token-plan/qwen3.8-max": {},
            "qwencloud-token-plan/qwen3.7-max": {},
            "qwencloud-token-plan/qwen3.7-plus": {},
            "qwencloud-token-plan/qwen3.6-plus": {},
            "qwencloud-token-plan/qwen3.6-flash": {},
            "qwencloud-token-plan/deepseek-v4-pro": {},
            "qwencloud-token-plan/deepseek-v4-pro-0813": {},
            "qwencloud-token-plan/deepseek-v4-flash": {},
            "qwencloud-token-plan/deepseek-v4-flash-0731": {},
            "qwencloud-token-plan/deepseek-v3.2": {},
            "qwencloud-token-plan/kimi-k2.7-code": {},
            "qwencloud-token-plan/kimi-k2.6": {},
            "qwencloud-token-plan/kimi-k2.5": {},
            "qwencloud-token-plan/glm-5.2": {},
            "qwencloud-token-plan/glm-5.1": {},
            "qwencloud-token-plan/glm-5": {},
            "qwencloud-token-plan/MiniMax-M2.5": {}
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": { "mode": "none" }
      }
    }
    ```

    3. 在 Web UI 配置页面单击保存按钮，完成配置修改。运行以下命令重启网关使配置生效：

    ```bash
    openclaw gateway restart
    ```

    <Note>
      保存成功后，apiKey 将显示为 `__OPENCLAW_REDACTED__`。这是脱敏保护，仅用于前端界面隐藏，不影响实际调用。
    </Note>
  </Tab>
</Tabs>

<Warning>
  **qwen3.8-max 思考模式说明**：

  - thinking：支持开启和关闭（混合思考模式）。
  - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
  - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
</Warning>

## 配置按量计费

将 `YOUR_API_KEY` 替换为千问AI平台 [API Key](/developer-guides/administration/api-keys)（格式为 `sk-ws-xxxxx`）。可用模型请参考[模型市场](https://www.qianwenai.com/models)。

| 配置项          | 说明                                                                            |
| ------------ | ----------------------------------------------------------------------------- |
| **API Key**  | 千问AI平台 [API Key](/developer-guides/administration/api-keys)，格式为 `sk-ws-xxxxx` |
| **Base URL** | `https://dashscope.aliyuncs.com/apps/anthropic`                               |
| **可用模型**     | [模型市场](https://www.qianwenai.com/models)中支持的模型                                |

<Tabs>
  <Tab title="通过终端修改">
    1. 在终端执行以下命令打开配置文件：

    ```bash
    nano ~/.openclaw/openclaw.json
    ```

    2. **首次配置**：复制以下内容到配置文件，将 `YOUR_API_KEY` 替换为千问AI平台 API Key。

       **已有配置**：若需保留已有配置，请勿直接全量替换，详见[已有配置如何安全修改](#已有配置如何安全修改)。

    ```json
    {
      "models": {
        "mode": "merge",
        "providers": {
          "qwencloud": {
            "baseUrl": "https://dashscope.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.7-plus",
                "name": "qwen3.7-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "compat": {
                  "thinkingFormat": "openai"
                }
              },
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "compat": {
                  "thinkingFormat": "openai"
                }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": false,
                "input": ["text"],
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "contextWindow": 204800,
                "maxTokens": 131072
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": false,
                "input": ["text"],
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "contextWindow": 202752,
                "maxTokens": 16384,
                "compat": {
                  "thinkingFormat": "openai"
                }
              },
              {
                "id": "deepseek-v3.2",
                "name": "deepseek-v3.2",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "qwencloud/qwen3.7-plus"
          },
          "models": {
            "qwencloud/qwen3.7-plus": {},
            "qwencloud/qwen3.6-plus": {},
            "qwencloud/MiniMax-M2.5": {},
            "qwencloud/glm-5": {},
            "qwencloud/deepseek-v3.2": {}
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": { "mode": "none" }
      }
    }
    ```

    3. 保存文件并退出，运行以下命令使配置生效：

    ```bash
    openclaw gateway restart
    ```
  </Tab>

  <Tab title="通过网页浏览器修改">
    1. 在终端执行以下命令打开 OpenClaw 操作界面（地址通常为 `http://127.0.0.1:xxxx`）：

    ```bash
    openclaw dashboard
    ```

    2. 在左侧菜单栏中选择**配置 > Settings > Advanced**，单击 **Open**。

       - **首次配置**：复制以下内容到输入框，替换已有内容。
       - **已有配置**：若需保留已有配置，请勿直接全量替换，详见[已有配置如何安全修改](#已有配置如何安全修改)。

       将 `YOUR_API_KEY` 替换为千问AI平台 API Key：

    ```json
    {
      "models": {
        "mode": "merge",
        "providers": {
          "qwencloud": {
            "baseUrl": "https://dashscope.aliyuncs.com/apps/anthropic",
            "apiKey": "YOUR_API_KEY",
            "api": "anthropic-messages",
            "models": [
              {
                "id": "qwen3.7-plus",
                "name": "qwen3.7-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "compat": {
                  "thinkingFormat": "openai"
                }
              },
              {
                "id": "qwen3.6-plus",
                "name": "qwen3.6-plus",
                "reasoning": false,
                "input": ["text", "image"],
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "contextWindow": 1000000,
                "maxTokens": 65536,
                "compat": {
                  "thinkingFormat": "openai"
                }
              },
              {
                "id": "MiniMax-M2.5",
                "name": "MiniMax-M2.5",
                "reasoning": false,
                "input": ["text"],
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "contextWindow": 204800,
                "maxTokens": 131072
              },
              {
                "id": "glm-5",
                "name": "glm-5",
                "reasoning": false,
                "input": ["text"],
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "contextWindow": 202752,
                "maxTokens": 16384,
                "compat": {
                  "thinkingFormat": "openai"
                }
              },
              {
                "id": "deepseek-v3.2",
                "name": "deepseek-v3.2",
                "reasoning": false,
                "input": ["text"],
                "contextWindow": 163840,
                "maxTokens": 16384,
                "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
                "compat": { "thinkingFormat": "openai" }
              }
            ]
          }
        }
      },
      "agents": {
        "defaults": {
          "model": {
            "primary": "qwencloud/qwen3.7-plus"
          },
          "models": {
            "qwencloud/qwen3.7-plus": {},
            "qwencloud/qwen3.6-plus": {},
            "qwencloud/MiniMax-M2.5": {},
            "qwencloud/glm-5": {},
            "qwencloud/deepseek-v3.2": {}
          }
        }
      },
      "gateway": {
        "mode": "local",
        "auth": { "mode": "none" }
      }
    }
    ```

    3. 在 Web UI 配置页面单击保存按钮，完成配置修改。运行以下命令重启网关使配置生效：

    ```bash
    openclaw gateway restart
    ```

    <Note>
      保存成功后，apiKey 将显示为 `__OPENCLAW_REDACTED__`。这是脱敏保护，仅用于前端界面隐藏，不影响实际调用。
    </Note>
  </Tab>
</Tabs>

## 使用 OpenClaw

支持通过网页浏览器和终端命令行的方式使用 OpenClaw。

<Tabs>
  <Tab title="网页浏览器">
    新开一个终端，运行以下命令，浏览器将自动打开 OpenClaw 的操作界面：

    ```bash
    openclaw dashboard
    ```

    界面打开后即可开始对话。
  </Tab>

  <Tab title="终端命令行">
    新开一个终端，运行以下命令：

    ```bash
    openclaw tui
    ```

    界面启动后即可开始对话。
  </Tab>
</Tabs>

## 常见命令

| 命令              | 说明                                    | 示例                   |
| --------------- | ------------------------------------- | -------------------- |
| `/help`         | 显示可用命令的快速摘要                           | `/help`              |
| `/status`       | 查看当前模型、会话、网关等状态信息                     | `/status`            |
| `/model <模型名称>` | 切换当前会话使用的模型                           | `/model qwen3.7-max` |
| `/new`          | 开始一个新会话                               | `/new`               |
| `/compact`      | 压缩对话历史，释放上下文窗口空间                      | `/compact`           |
| `/think <级别>`   | 设置思考（推理）深度级别，可选 off、low、medium、high 等 | `/think high`        |
| `/skills`       | 展示全部可用的 Skill                         | `/skills`            |

## 切换模型

**在当前会话切换模型（临时有效）**

在终端输入 `openclaw tui`，进入 OpenClaw 终端命令行，使用 `/model <模型名称>` 在当前会话中切换模型：

```bash
/model qwen3.7-max
```

界面返回提示"model set to qwen3.7-max"即表示生效。

**切换默认模型（永久有效）**

如需在每次新会话中使用指定模型，修改配置文件中的 `agents.defaults.model.primary` 字段为目标模型，然后重启网关：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "qwencloud-token-plan/qwen3.6-plus"
      }
    }
  }
}
```

```bash
openclaw gateway restart
```

<Note>
  文本模型（如 qwen3.6-plus、glm-5 等）可直接使用。图像生成模型需通过自定义 Skill 接入，参见[接入多模态生成模型](/token-plan/best-practices/multimodal-generation)。
</Note>

## 常见问题

**如何查看已配置的模型？**

在终端输入 `openclaw tui`，进入 OpenClaw 终端命令行，接着输入 `/model` 查看模型列表。按回车键选中模型，按 Esc 键退出模型列表。

---

**报错 API rate limit reached 怎么办？**

请按以下顺序排查：

1. **OpenClaw 配置错误**：若 Base URL 或模型提供商配置有误，导致请求未进入 Token Plan 团队版专属通道，而是被路由到通用 API 调用，从而触发限流。

   - 若使用千问AI平台模型 团队版套餐，请核对配置文件中的 `models`、`agents`、`gateway`（含嵌套字段），确保与文档配置一致。例如：模型服务提供商的结构为 `{ "models": { "providers": { "qwencloud-token-plan": {...} } } }`。
   - 若当前未使用千问AI平台模型 团队版套餐，建议切换至 Token Plan 团队版以获取专属额度。

2. **超出套餐限额**：在 Token Plan 团队版页面查看套餐用量情况。

3. **尝试重置 API Key**：若完成上述排查后问题仍未解决，请前往 Token Plan 团队版页面重置 API Key。

---

**报错"HTTP 401: Incorrect API key provided."、"No API key found for provider xxx"或"HTTP 401: invalid\_iam\_token"怎么办？**

可能原因：

1. API Key 无效、过期、为空、格式错误，或与端点环境不匹配。请检查 API Key 是否为 Token Plan 团队版套餐专属 Key，复制完整且无空格；确认订阅状态有效。

2. OpenClaw 的历史配置缓存导致配置错误。请删除 `~/.openclaw/agents/main/agent/models.json` 文件中的 `providers` 配置项，并重启 OpenClaw。

3. `invalid_iam_token` 表示 API Key 经 IAM 鉴权校验失败。常见场景：API Key 已被吊销或禁用、API Key 与 Base URL 不匹配、使用 STS 临时凭证且已过期。请核对 API Key 与 Base URL 配置正确，并确认 API Key 状态正常。

---

**报错 device identity required 怎么办？**

详细报错信息：

```plaintext
http://127.0.0.1:18791/15:05:56 [ws] closed before connect conn=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx remote=127.0.0.1 fwd=n/a origin=n/a host=127.0.0.1:18789 ua=n/a code=1008 reason=device identity required
```

**原因**：客户端连接网关时未提供设备身份信息，通常由以下原因导致：

- 首次打开浏览器访问地址，尚未完成设备配对。
- 浏览器缓存被清除，设备密钥丢失。
- 重装或升级 OpenClaw 后，`~/.openclaw/identity/` 目录下的密钥文件缺失。

**解决方法**：在终端执行以下命令，允许当前设备连接并重新生成浏览器访问地址：

```bash
openclaw devices approve --latest
openclaw dashboard --no-open
```

如果仍未解决，先清除异常的设备记录再重试：

```bash
openclaw devices clear --pending --yes
openclaw dashboard --no-open
```

执行 `openclaw devices list`，确认设备显示在 Paired 列表中即为正常。

---

### 没有主动使用 OpenClaw，但仍产生了 Token 消耗

**原因：** OpenClaw 内置心跳机制（Heartbeat），网关运行期间会按固定间隔（默认 30 分钟）自动调用已配置的模型，检查是否有待处理任务。每次心跳都会消耗少量 Token。

**如何确认：** 查看 `~/.openclaw/agents/main/sessions/` 目录下的会话记录文件（.jsonl），其中包含 `[OpenClaw heartbeat poll]` 标记的心跳调用记录。

**解决方法：**

- **停止网关**：不使用时执行 `openclaw gateway stop`，心跳随即停止。
- **增大心跳间隔**：在 `~/.openclaw/openclaw.json` 中设置 `agents.defaults.heartbeat.every`，例如 `"2h"` 表示每 2 小时一次。

---

### 已有配置如何安全修改？

<Warning>
  请勿直接全量覆盖配置文件。直接"全部替换"会覆盖掉自定义配置，请进行局部修改。
</Warning>

可以选择以下方式完成配置：

- **若 OpenClaw 可正常对话**：直接在 OpenClaw 对话中输入以下指令完成配置合并。
- **若 OpenClaw 未配置模型或无法对话**：参考上方"配置 Token Plan 团队版"章节完成首次配置。

在 OpenClaw 对话中输入以下指令（将 `YOUR_API_KEY` 替换为实际的 API Key）：

```plaintext
请在 OpenClaw 中接入 Token Plan 团队版，步骤如下：
1. 打开配置文件：~/.openclaw/openclaw.json
2. 找到或创建以下字段，合并配置（保留原有配置不变，若字段不存在则新增）：
{
  "models": {
    "mode": "merge",
    "providers": {
      "qwencloud-token-plan": {
        "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic",
        "apiKey": "YOUR_API_KEY",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "qwen3.8-max",
            "name": "qwen3.8-max",
            "reasoning": true,
            "input": ["text", "image"],
            "contextWindow": 983616,
            "maxTokens": 131072,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "qwen3.7-max",
            "name": "qwen3.7-max",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 1000000,
            "maxTokens": 65536,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "qwen3.7-plus",
            "name": "qwen3.7-plus",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 1000000,
            "maxTokens": 65536,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "qwen3.6-plus",
            "name": "qwen3.6-plus",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 1000000,
            "maxTokens": 65536,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "qwen3.6-flash",
            "name": "qwen3.6-flash",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 1000000,
            "maxTokens": 32768,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "deepseek-v4-pro",
            "name": "deepseek-v4-pro",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 163840,
            "maxTokens": 32768,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          },
          {
            "id": "deepseek-v4-pro-0813",
            "name": "deepseek-v4-pro-0813",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 163840,
            "maxTokens": 32768,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          },
          {
            "id": "deepseek-v4-flash",
            "name": "deepseek-v4-flash",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 163840,
            "maxTokens": 16384,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          },
          {
            "id": "deepseek-v4-flash-0731",
            "name": "deepseek-v4-flash-0731",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 1000000,
            "maxTokens": 393216,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          },
          {
            "id": "deepseek-v3.2",
            "name": "deepseek-v3.2",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 163840,
            "maxTokens": 16384,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "kimi-k2.7-code",
            "name": "kimi-k2.7-code",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 262144,
            "maxTokens": 32768,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "kimi-k2.6",
            "name": "kimi-k2.6",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 262144,
            "maxTokens": 16384,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "kimi-k2.5",
            "name": "kimi-k2.5",
            "reasoning": false,
            "input": ["text", "image"],
            "contextWindow": 262144,
            "maxTokens": 16384,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "glm-5.2",
            "name": "glm-5.2",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 1000000,
            "maxTokens": 16384,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "glm-5.1",
            "name": "glm-5.1",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 202752,
            "maxTokens": 16384,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "glm-5",
            "name": "glm-5",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 202752,
            "maxTokens": 16384,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "compat": { "thinkingFormat": "openai" }
          },
          {
            "id": "MiniMax-M2.5",
            "name": "MiniMax-M2.5",
            "reasoning": false,
            "input": ["text"],
            "contextWindow": 204800,
            "maxTokens": 131072,
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "qwencloud-token-plan/qwen3.8-max"
      },
      "models": {
        "qwencloud-token-plan/qwen3.8-max": {},
        "qwencloud-token-plan/qwen3.7-max": {},
        "qwencloud-token-plan/qwen3.7-plus": {},
        "qwencloud-token-plan/qwen3.6-plus": {},
        "qwencloud-token-plan/qwen3.6-flash": {},
        "qwencloud-token-plan/deepseek-v4-pro": {},
        "qwencloud-token-plan/deepseek-v4-pro-0813": {},
        "qwencloud-token-plan/deepseek-v4-flash": {},
        "qwencloud-token-plan/deepseek-v4-flash-0731": {},
        "qwencloud-token-plan/deepseek-v3.2": {},
        "qwencloud-token-plan/kimi-k2.7-code": {},
        "qwencloud-token-plan/kimi-k2.6": {},
        "qwencloud-token-plan/kimi-k2.5": {},
        "qwencloud-token-plan/glm-5.2": {},
        "qwencloud-token-plan/glm-5.1": {},
        "qwencloud-token-plan/glm-5": {},
        "qwencloud-token-plan/MiniMax-M2.5": {}
      }
    }
  },
  "gateway": {
    "mode": "local"
  }
}
3. 保存配置文件
4. 运行openclaw gateway restart，重启OpenClaw的网关，使配置生效。
```

配置完成后，新开一个 OpenClaw 会话，输入 `openclaw models status` 验证配置是否生效。重启网关后，已有会话可能无法正常对话，请重启会话。
