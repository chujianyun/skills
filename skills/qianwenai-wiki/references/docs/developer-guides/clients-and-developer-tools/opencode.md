> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# OpenCode

> 在 OpenCode 中使用千问AI平台模型

OpenCode 是一款终端 AI 编程工具，可以通过按量计费、Token Plan 个人版或 Token Plan 团队版接入千问AI平台。

## 安装 OpenCode

1. 安装 [Node.js](https://nodejs.org/en/download/)（v18.0 或更高版本）。

2. 在终端中执行以下命令安装 OpenCode：

```bash
npm install -g opencode-ai
```

运行以下命令验证安装。若有版本号输出，则表示安装成功。

```bash
opencode -v
```

## 配置接入凭证

使用文本编辑器打开：

- macOS / Linux：`~/.config/opencode/opencode.json`
- Windows：`C:\Users\<用户名>\.config\opencode\opencode.json`

根据所选方案写入对应配置：

- **Token Plan 个人版**：个人订阅，按 token 消耗抵扣 Credits。
- **Token Plan 团队版**：按坐席订阅，按 token 消耗抵扣 Credits。
- **按量计费**：按实际调用量后付费。

### Token Plan 个人版

需先购买 Token Plan 个人版套餐且套餐处于有效期内。可在 [Token Plan 个人版页面](https://platform.qianwenai.com/pricing/token-plan) 购买套餐。

将 `YOUR_API_KEY` 替换为 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/pricing/token-plan)。可用模型请参考 Token Plan 个人版[支持的模型](/token-plan/overview)。

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "bailian-token-plan-personal": {
      "npm": "@ai-sdk/anthropic",
      "name": "Alibaba Cloud Model Studio",
      "options": {
        "baseURL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1",
        "apiKey": "YOUR_API_KEY"
      },
      "models": {
        "qwen3.8-max": {
          "name": "Qwen3.8 Max",
          "reasoning": true,
          "limit": {
            "context": 983616,
            "output": 131072
          },
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "effort": "xhigh"
          }
        },
        "qwen3.7-max": {
          "name": "Qwen3.7 Max",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "qwen3.7-plus": {
          "name": "Qwen3.7 Plus",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "qwen3.6-plus": {
          "name": "Qwen3.6 Plus",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "qwen3.6-flash": {
          "name": "Qwen3.6 Flash",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        }
      }
    }
  }
}
```

<Warning>
  **qwen3.8-max 思考模式说明**：

  - thinking：支持开启和关闭（混合思考模式）。
  - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
  - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
</Warning>

### Token Plan 团队版

需先购买 Token Plan 团队版套餐且套餐处于有效期内。可在 [Token Plan 团队版页面](https://platform.qianwenai.com/pricing/token-plan) 购买套餐。

将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 [API Key](/token-plan/overview)。可用模型请参考 Token Plan 团队版[支持的模型](/token-plan/overview)。

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "bailian-token-plan": {
      "npm": "@ai-sdk/anthropic",
      "name": "Alibaba Cloud Model Studio",
      "options": {
        "baseURL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1",
        "apiKey": "YOUR_API_KEY"
      },
      "models": {
        "qwen3.8-max": {
          "name": "Qwen3.8 Max",
          "reasoning": true,
          "limit": {
            "context": 983616,
            "output": 131072
          },
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "effort": "xhigh"
          }
        },
        "qwen3.7-max": {
          "name": "Qwen3.7 Max",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "qwen3.7-plus": {
          "name": "Qwen3.7 Plus",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "qwen3.6-plus": {
          "name": "Qwen3.6 Plus",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "qwen3.6-flash": {
          "name": "Qwen3.6 Flash",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "deepseek-v4-pro": {
          "name": "DeepSeek V4 Pro"
        },
        "deepseek-v4-pro-0813": {
          "name": "DeepSeek V4 Pro 0813"
        },
        "deepseek-v4-flash": {
          "name": "DeepSeek V4 Flash"
        },
        "deepseek-v4-flash-0731": {
          "name": "DeepSeek V4 Flash 0731"
        },
        "deepseek-v3.2": {
          "name": "DeepSeek V3.2"
        },
        "kimi-k2.7-code": {
          "name": "Kimi K2.7 Code",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "kimi-k2.6": {
          "name": "Kimi K2.6",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "kimi-k2.5": {
          "name": "Kimi K2.5",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "glm-5.2": {
          "name": "GLM-5.2",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "glm-5.1": {
          "name": "GLM-5.1",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "glm-5": {
          "name": "GLM-5",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "MiniMax-M2.5": {
          "name": "MiniMax M2.5"
        }
      }
    }
  }
}
```

<Warning>
  **qwen3.8-max 思考模式说明**：

  - thinking：支持开启和关闭（混合思考模式）。
  - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
  - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
</Warning>

### 按量计费

将 `YOUR_API_KEY` 替换为千问AI平台 [API Key](/developer-guides/administration/api-keys)。可用模型请参考 [Anthropic 兼容 API](/api-reference/chat/anthropic)。

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "bailian-payg": {
      "npm": "@ai-sdk/anthropic",
      "name": "Alibaba Cloud Model Studio",
      "options": {
        "baseURL": "https://dashscope.aliyuncs.com/apps/anthropic/v1",
        "apiKey": "YOUR_API_KEY"
      },
      "models": {
        "qwen3.7-max": {
          "name": "Qwen3.7 Max",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "qwen3.7-plus": {
          "name": "Qwen3.7 Plus",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "qwen3.6-plus": {
          "name": "Qwen3.6 Plus",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "deepseek-v3.2": {
          "name": "DeepSeek V3.2"
        }
      }
    }
  }
}
```

## 验证配置

保存配置后，重启 OpenCode，输入 `/models`，搜索 `Alibaba Cloud Model Studio`，选择需要使用的模型即可开始对话。

<Note>
  图像生成模型需通过 Agent 接入，参见[接入图像生成模型](#接入图像生成模型)。
</Note>

## 接入图像生成模型

通过 OpenCode 的 Agent 机制，可以调用 Token Plan 团队版的图像生成模型（qwen-image-2.0、wan2.7-image 等）。

### 步骤一：创建 Agent

在项目根目录创建 `.opencode/agents/text-to-image.md`，写入以下内容：

````
---
description: "调用 Token Plan 文生图模型，根据文字描述生成图像。当要求画图、生成图片时使用。"
mode: subagent
tools:
  bash: true
  write: false
  edit: false
---
根据文字描述调用 Token Plan 文生图 API 生成图像。

## 执行步骤

1. 从用户输入中提取 prompt（图像描述）、model（默认 qwen-image-2.0）、size（默认 1024*1024）。

2. 使用 bash 执行 curl 命令生成图像：

```bash
RESPONSE=$(curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $TOKEN_PLAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<模型>","input":{"messages":[{"role":"user","content":[{"text":"<prompt>"}]}]},"parameters":{"size":"<尺寸>"}}')
echo "$RESPONSE"
```

3. 从返回 JSON 中提取 output.choices[*].message.content[*].image 的 URL，下载到当前目录。

4. 返回图片文件路径。

## 可用模型
- qwen-image-2.0（默认）— 通用，擅长中文文本渲染
- qwen-image-2.0-pro — 质量更高
- wan2.7-image — 多风格，默认出 4 张
- wan2.7-image-pro — 支持 4K

## 可用尺寸
1024*1024、720*1280、1280*720
````

### 步骤二：配置环境变量

确保环境变量 `TOKEN_PLAN_API_KEY` 已设置为 Token Plan 团队版专属 API Key。可在 shell 配置文件（如 `~/.bashrc` 或 `~/.zshrc`）中添加：

```bash
export TOKEN_PLAN_API_KEY="REDACTED"
```

### 步骤三：使用

在 OpenCode 中直接描述需要生成的图像（如"画一只猫"），OpenCode 会自动调用该 Agent。

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

- 按量计费：[错误码排查](/api-reference/preparation/error-messages)
- Token Plan 个人版：[Token Plan 个人版常见问题](/token-plan/faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)
