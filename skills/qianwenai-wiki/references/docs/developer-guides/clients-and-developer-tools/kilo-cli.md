> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Kilo CLI

> 在 Kilo CLI 中使用千问AI平台模型

Kilo CLI 是 Kilo Code 的命令行客户端，可以通过按量计费、Token Plan 个人版或 Token Plan 团队版接入千问AI平台。接入 Kilo CLI 需要修改配置文件 `~/.config/kilo/config.json` 中的模型提供商。

## 安装 Kilo CLI

1. 安装 [Node.js](https://nodejs.org/en/download/)（v18.0 或更高版本）。

2. 在终端中执行以下命令安装 Kilo CLI：

```bash
npm install -g @kilocode/cli
```

运行以下命令验证安装。若有版本号输出，则表示安装成功。

```bash
kilo --version
```

## 配置 Token Plan 个人版

需先购买 Token Plan 个人版套餐且套餐处于有效期内。可在 [Token Plan 个人版页面](https://platform.qianwenai.com/pricing/token-plan)购买套餐。

将 `YOUR_API_KEY` 替换为 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。可用模型请参考 Token Plan 个人版[支持的模型](/token-plan/personal/token-plan-personal-overview#支持的模型)。

使用文本编辑器打开 `~/.config/kilo/config.json`，写入以下配置：

```json
{
  "$schema": "https://kilo.ai/config.json",
  "provider": {
    "qwencloud-token-plan-personal": {
      "npm": "@ai-sdk/anthropic",
      "name": "千问AI平台 (Token Plan 个人版)",
      "options": {
        "baseURL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1",
        "apiKey": "YOUR_API_KEY"
      },
      "models": {
        "qwen3.8-max": {
          "name": "Qwen3.8 Max",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 262144
            }
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
        "glm-5.2": {
          "name": "GLM-5.2",
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
        "deepseek-v4-flash-0731": {
          "name": "DeepSeek V4 Flash 0731"
        }
      }
    }
  }
}
```

<Note>
  **qwen3.8-max 思考模式说明**：

  - thinking：支持开启和关闭（混合思考模式）。
  - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
  - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
</Note>

## 配置 Token Plan 团队版

需先购买 Token Plan 团队版套餐且套餐处于有效期内。可在 [Token Plan 团队版页面](https://platform.qianwenai.com/pricing/token-plan)购买套餐。

将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/api-keys)。可用模型请参考 Token Plan 团队版[支持的模型](/token-plan/team/token-plan-team-overview#支持的模型)。

使用文本编辑器打开 `~/.config/kilo/config.json`，写入以下配置：

```json
{
  "$schema": "https://kilo.ai/config.json",
  "provider": {
    "qwencloud-token-plan": {
      "npm": "@ai-sdk/anthropic",
      "name": "千问AI平台 (Token Plan)",
      "options": {
        "baseURL": "https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic/v1",
        "apiKey": "YOUR_API_KEY"
      },
      "models": {
        "qwen3.8-max": {
          "name": "Qwen3.8 Max",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 262144
            }
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
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "kimi-k2.6": {
          "name": "Kimi K2.6",
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 8192
            }
          }
        },
        "kimi-k2.5": {
          "name": "Kimi K2.5",
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

<Note>
  **qwen3.8-max 思考模式说明**：

  - thinking：支持开启和关闭（混合思考模式）。
  - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
  - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
</Note>

## 配置按量计费

将 `YOUR_API_KEY` 替换为千问AI平台 [API Key](/developer-guides/administration/api-keys)。可用模型请参考[支持的模型](/developer-guides/getting-started/text-generation-models)。

| 配置项          | 说明                                                                             |
| ------------ | ------------------------------------------------------------------------------ |
| **Base URL** | `https://dashscope.aliyuncs.com/compatible-mode/v1`                            |
| **API Key**  | 千问AI平台 [API Key](/developer-guides/administration/api-keys)（格式为 `sk-ws-xxxxx`） |
| **可用模型**     | [支持的模型](/developer-guides/getting-started/text-generation-models)              |

使用文本编辑器打开 `~/.config/kilo/config.json`，写入以下配置：

```json
{
  "$schema": "https://kilo.ai/config.json",
  "provider": {
    "qwencloud": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "千问AI平台",
      "options": {
        "baseURL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "YOUR_API_KEY"
      },
      "models": {
        "qwen3.7-plus": {
          "name": "Qwen3.7 Plus",
          "modalities": {
            "input": ["text", "image"],
            "output": ["text"]
          },
          "options": {
            "thinking": {
              "type": "enabled",
              "budgetTokens": 1024
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
              "budgetTokens": 1024
            }
          }
        }
      }
    }
  }
}
```

如需添加[其他模型](/developer-guides/getting-started/text-generation-models)，在 `models` 中以相同格式追加即可。

## 使用 Kilo CLI

1. 配置完成后，重启 Kilo CLI，输入 `/models`，搜索 `千问AI平台`，选择需要使用的模型。

2. 开始对话。

更多 Kilo CLI 使用技巧及常见命令请参考 [Kilo Code 官方文档](https://kilo.ai/docs/code-with-ai/platforms/cli)。

## 常见问题

### 错误码

配置过程中遇到报错，请参考对应计费方案的常见问题文档：

- 按量计费：[错误码排查](/api-reference/preparation/error-messages)
- Token Plan 个人版：[Token Plan 个人版常见问题](/token-plan/personal/token-plan-personal-faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)
