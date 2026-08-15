> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen Code

> 在 Qwen Code 中使用千问AI平台模型

Qwen Code 是一款 AI 编程助手，本文介绍如何在 Qwen Code（CLI 及 IDE 插件）中配置与使用千问AI平台 Token Plan 个人版或 Token Plan 团队版。

## 应用场景

Qwen Code 支持以下使用场景：

- **AI 编程辅助**：在终端通过自然语言完成代码生成、代码补全与代码审查，提升日常开发效率。
- **Web 开发**：提供目标网站截图，Qwen Code 自动解析页面结构并生成高还原度的前端代码。
- **视频制作**：给定开源项目仓库地址，一键生成专属宣传视频。

## 安装 Qwen Code

<Tabs>
  <Tab title="macOS / Linux">
    ```bash
    bash -c "$(curl -fsSL https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen.sh)" -s --source bailian
    ```
  </Tab>

  <Tab title="Windows">
    在任务栏搜索框里输入 `cmd`，选择**以管理员身份运行**，打开 `cmd` 窗口后运行以下命令安装 Qwen Code。

    ```bash
    curl -fsSL -o %TEMP%\install-qwen.bat https://qwen-code-assets.oss-cn-hangzhou.aliyuncs.com/installation/install-qwen.bat && %TEMP%\install-qwen.bat --source bailian
    ```

    <Warning>
      安装完成后，需**关闭并重新打开** `cmd` 窗口，以使环境变量生效。
    </Warning>
  </Tab>
</Tabs>

安装完成后，运行以下命令确认安装成功：

```bash
qwen --version
```

## 配置 Token Plan 个人版

启动 Qwen Code 后输入 `/auth`，依次选择**订阅计划** > **千问AI平台 Token Plan**，输入 Token Plan 个人版专属 [API Key](https://platform.qianwenai.com/home/billing/subscription/token-plan) 即可完成配置。可用模型请参考 Token Plan 个人版[支持的模型](/token-plan/team/token-plan-team-overview#支持的模型)。

<Accordion title="高级配置：通过 settings.json 配置文件">
  编辑或新建 `settings.json` 文件，将 `YOUR_API_KEY` 替换为 Token Plan 个人版专属 API Key。文件路径如下：

  - macOS/Linux：`~/.qwen/settings.json`
  - Windows：`C:\Users\<Windows用户名>\.qwen\settings.json`

  ```json
  {
    "env": {
      "QWENCLOUD_TOKEN_PLAN_API_KEY": "YOUR_API_KEY"
    },
    "modelProviders": {
      "openai": [
        {
          "id": "qwen3.8-max",
          "name": "[Token Plan 个人版] qwen3.8-max",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "qwen3.7-max",
          "name": "[Token Plan 个人版] qwen3.7-max",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "qwen3.7-plus",
          "name": "[Token Plan 个人版] qwen3.7-plus",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "qwen3.6-flash",
          "name": "[Token Plan 个人版] qwen3.6-flash",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "glm-5.2",
          "name": "[Token Plan 个人版] glm-5.2",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
        },
        {
          "id": "deepseek-v4-pro",
          "name": "[Token Plan 个人版] deepseek-v4-pro",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
        },
        {
          "id": "deepseek-v4-pro-0813",
          "name": "[Token Plan 个人版] deepseek-v4-pro-0813",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
        },
        {
          "id": "deepseek-v4-flash-0731",
          "name": "[Token Plan 个人版] deepseek-v4-flash-0731",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
        }
      ]
    }
  }
  ```

  <Warning>
    **qwen3.8-max 思考模式说明**：

    - thinking：支持开启和关闭（混合思考模式）。
    - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
    - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
  </Warning>
</Accordion>

## 配置 Token Plan 团队版

启动 Qwen Code 后输入 `/auth` 命令进行可视化配置。依次选择**订阅计划** > **千问AI平台 Token Plan**，输入 Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/billing/subscription/token-plan) 即可完成配置。可用模型请参考 Token Plan 团队版[支持的模型](/token-plan/team/token-plan-team-overview#支持的模型)。

<Accordion title="高级配置：通过 settings.json 配置文件">
  编辑或新建 `settings.json` 文件，将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 API Key。文件路径如下：

  - macOS/Linux：`~/.qwen/settings.json`
  - Windows：`C:\Users\<Windows用户名>\.qwen\settings.json`

  ```json
  {
    "env": {
      "QWENCLOUD_TOKEN_PLAN_API_KEY": "YOUR_API_KEY"
    },
    "modelProviders": {
      "openai": [
        {
          "id": "qwen3.8-max",
          "name": "[Token Plan 团队版] qwen3.8-max",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "qwen3.7-max",
          "name": "[Token Plan 团队版] qwen3.7-max",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "qwen3.7-plus",
          "name": "[Token Plan 团队版] qwen3.7-plus",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "qwen3.6-plus",
          "name": "[Token Plan 团队版] qwen3.6-plus",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "qwen3.6-flash",
          "name": "[Token Plan 团队版] qwen3.6-flash",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "deepseek-v4-pro",
          "name": "[Token Plan 团队版] deepseek-v4-pro",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
        },
        {
          "id": "deepseek-v4-pro-0813",
          "name": "[Token Plan 团队版] deepseek-v4-pro-0813",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
        },
        {
          "id": "deepseek-v4-flash",
          "name": "[Token Plan 团队版] deepseek-v4-flash",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
        },
        {
          "id": "deepseek-v4-flash-0731",
          "name": "[Token Plan 团队版] deepseek-v4-flash-0731",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
        },
        {
          "id": "deepseek-v3.2",
          "name": "[Token Plan 团队版] deepseek-v3.2",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
        },
        {
          "id": "kimi-k2.7-code",
          "name": "[Token Plan 团队版] kimi-k2.7-code",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "kimi-k2.6",
          "name": "[Token Plan 团队版] kimi-k2.6",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "kimi-k2.5",
          "name": "[Token Plan 团队版] kimi-k2.5",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "glm-5.2",
          "name": "[Token Plan 团队版] glm-5.2",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "glm-5.1",
          "name": "[Token Plan 团队版] glm-5.1",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "glm-5",
          "name": "[Token Plan 团队版] glm-5",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        },
        {
          "id": "MiniMax-M2.5",
          "name": "[Token Plan 团队版] MiniMax-M2.5",
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
        }
      ]
    },
    "security": {
      "auth": {
        "selectedType": "openai"
      }
    },
    "tokenPlan": {
      "region": "china"
    },
    "model": {
      "name": "qwen3.8-max"
    },
    "$version": 3
  }
  ```
</Accordion>

<Warning>
  **qwen3.8-max 思考模式说明**：

  - thinking：支持开启和关闭（混合思考模式）。
  - temperature：思考模式下默认值为 0.6；传入值小于 0.6 时自动调整为 0.6。
  - reasoning\_effort：控制推理深度，可选 xhigh、medium、low，默认 xhigh。
</Warning>

配置完成后，在项目目录下运行以下命令启动 Qwen Code，即可开始对话：

```bash
qwen
```

## 配置按量计费

启动 Qwen Code 后输入 `/auth`，选择**使用自己的 API Key** > **Standard API Key**，输入千问AI平台 [API Key](/developer-guides/administration/api-keys) 即可完成配置。可用模型请参考[支持的模型](/developer-guides/getting-started/text-generation-models)。

<Accordion title="高级配置：通过 settings.json 配置文件">
  编辑或新建 `settings.json` 文件，将 `YOUR_API_KEY` 替换为千问AI平台 API Key。文件路径如下：

  - macOS/Linux：`~/.qwen/settings.json`
  - Windows：`C:\Users\<Windows用户名>\.qwen\settings.json`

  `baseUrl` 设置如下：

| 配置项          | 说明                                                                             |
| ------------ | ------------------------------------------------------------------------------ |
| **Base URL** | `https://dashscope.aliyuncs.com/compatible-mode/v1`                            |
| **API Key**  | 千问AI平台 [API Key](/developer-guides/administration/api-keys)（格式为 `sk-ws-xxxxx`） |
| **可用模型**     | [支持的模型](/developer-guides/getting-started/text-generation-models)              |

  编辑 `settings.json`，写入以下配置：

  ```json
  {
    "env": {
      "QWENCLOUD_API_KEY": "YOUR_API_KEY"
    },
    "modelProviders": {
      "openai": [
        {
          "id": "qwen3.7-plus",
          "name": "[千问AI平台] qwen3.7-plus",
          "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
          "envKey": "QWENCLOUD_API_KEY",
          "generationConfig": {
            "extra_body": {
              "enable_thinking": true
            }
          }
        }
      ]
    },
    "security": {
      "auth": {
        "selectedType": "openai"
      }
    },
    "model": {
      "name": "qwen3.7-plus"
    },
    "$version": 3
  }
  ```

  如需添加[其他模型](/developer-guides/getting-started/text-generation-models)，在 `modelProviders.openai` 中以相同格式追加即可。
</Accordion>

## 常见命令

<Note>
  以下命令适用于 Qwen Code CLI，IDE 插件仅支持部分命令，请以实际使用为准。
</Note>

| 命令          | 说明                                      | 示例             |
| ----------- | --------------------------------------- | -------------- |
| `/model`    | 切换当前会话中使用的模型                            | `/model`       |
| `/auth`     | 更改认证方式                                  | `/auth`        |
| `/init`     | 分析当前目录并创建初始上下文文件（QWEN.md），用于定义项目级指令和上下文 | `/init`        |
| `/clear`    | 清除终端屏幕内容，开始全新对话                         | `/clear`       |
| `/compress` | 用摘要替换聊天历史以节省 Token                      | `/compress`    |
| `/settings` | 打开设置编辑器，可配置语言、主题等                       | `/settings`    |
| `/summary`  | 根据对话历史生成项目摘要                            | `/summary`     |
| `/resume`   | 恢复之前的对话会话                               | `/resume`      |
| `/stats`    | 显示当前会话的详细统计信息                           | `/stats`       |
| `/help`     | 显示可用命令的帮助信息                             | `/help` 或 `/?` |
| `/quit`     | 退出 Qwen Code                            | `/quit`        |

更多 Qwen Code 的进阶功能，可以参考 [Qwen Code 官方文档](https://qwenlm.github.io/qwen-code-docs/zh/users/features/commands/)。

## 切换模型

输入 `/model`，可在 Token Plan 团队版支持的模型间切换。

<Note>
  文本模型（如 qwen3.6-plus、glm-5 等）可直接使用。图像生成模型需通过 Skill 接入，参见下方"接入图像生成模型"章节。
</Note>

如果所需模型（如 `qwen3.6-plus`、`qwen3.6-flash`、`deepseek-v4-pro`、`kimi-k2.6`、`glm-5.1`）未出现在列表中，请按以下步骤更新 Qwen Code：

1. 输入 `/quit` 退出当前会话。
2. 执行 `npm install -g @qwen-code/qwen-code@latest` 命令更新 Qwen Code。
3. 重新执行 `qwen` 命令启动 Qwen Code。
4. 再次输入 `/model` 即可选择新添加的模型。

## 接入图像生成模型

通过 Qwen Code 的 Skill 机制，可以调用 Token Plan 团队版的图像生成模型（qwen-image-2.0、wan2.7-image 等）。

### 步骤一：创建 Skill

创建文件 `~/.qwen/skills/text-to-image/SKILL.md`，写入以下内容：

````plaintext
---
name: text-to-image
description: "调用 Token Plan 文生图模型，根据文字描述生成图像并保存到本地。当要求画图、生成图片时触发。"
---

# 文生图

根据文字描述调用 Token Plan 文生图模型生成图像。

## 可用模型

| 模型                 | 说明                 |
| ------------------ | ------------------ |
| qwen-image-2.0     | 默认。通用图像生成，擅长中文文本渲染 |
| qwen-image-2.0-pro | 画面质量更高，耗时略长        |
| wan2.7-image       | 多风格生成，默认输出 4 张     |
| wan2.7-image-pro   | 支持 4K 输出           |

## 可用尺寸

1024*1024（默认）、720*1280（竖版）、1280*720（横版）。
wan2.7-image-pro 额外支持 2048*2048、1440*2560、2560*1440。

## 执行步骤

1. 从用户输入中提取 prompt、模型（默认 qwen-image-2.0）、尺寸（默认 1024*1024）。

2. 调用 API：

```bash
curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $QWENCLOUD_TOKEN_PLAN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<模型>","input":{"messages":[{"role":"user","content":[{"text":"<prompt>"}]}]},"parameters":{"size":"<尺寸>"}}'
```

3. 从返回 JSON 的 output.choices[*].message.content[*].image 提取 URL，下载到当前目录。

4. 报告文件路径、使用的模型和尺寸。
````

### 步骤二：使用

在 Qwen Code 中直接描述需要生成的图像，Qwen Code 会自动识别并调用该 Skill。

## 使用 IDE 插件

Qwen Code 支持在 VS Code 中以插件方式使用，在 IDE 中提供 AI 编程能力。

<Tabs>
  <Tab title="VS Code">
    使用前请确保 VS Code 版本为 1.85.0 或更高版本。

    1. 打开 VS Code，在扩展市场中搜索 `Qwen Code Companion` 并安装。

    2. 编辑或新建 `settings.json` 文件，写入配置内容，将 `YOUR_API_KEY` 替换为 Token Plan 团队版专属 [API Key](https://platform.qianwenai.com/home/billing/subscription/token-plan)，文件路径如下：

       - macOS/Linux：`~/.qwen/settings.json`
       - Windows：`C:\Users\<Windows用户名>\.qwen\settings.json`

       <Note>
         CLI 和 IDE 插件共用同一个 settings.json。如果已按上方步骤完成配置，请跳过此步。
       </Note>

    ```json
    {
      "env": {
        "QWENCLOUD_TOKEN_PLAN_API_KEY": "YOUR_API_KEY"
      },
      "modelProviders": {
        "openai": [
          {
            "id": "qwen3.8-max",
            "name": "[Token Plan 团队版] qwen3.8-max",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
            "generationConfig": {
              "extra_body": {
                "enable_thinking": true
              }
            }
          },
          {
            "id": "qwen3.7-max",
            "name": "[Token Plan 团队版] qwen3.7-max",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
            "generationConfig": {
              "extra_body": {
                "enable_thinking": true
              }
            }
          },
          {
            "id": "qwen3.7-plus",
            "name": "[Token Plan 团队版] qwen3.7-plus",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
            "generationConfig": {
              "extra_body": {
                "enable_thinking": true
              }
            }
          },
          {
            "id": "qwen3.6-plus",
            "name": "[Token Plan 团队版] qwen3.6-plus",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
            "generationConfig": {
              "extra_body": {
                "enable_thinking": true
              }
            }
          },
          {
            "id": "qwen3.6-flash",
            "name": "[Token Plan 团队版] qwen3.6-flash",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
            "generationConfig": {
              "extra_body": {
                "enable_thinking": true
              }
            }
          },
          {
            "id": "deepseek-v4-pro",
            "name": "[Token Plan 团队版] deepseek-v4-pro",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "deepseek-v4-pro-0813",
            "name": "[Token Plan 团队版] deepseek-v4-pro-0813",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "deepseek-v4-flash",
            "name": "[Token Plan 团队版] deepseek-v4-flash",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "deepseek-v4-flash-0731",
            "name": "[Token Plan 团队版] deepseek-v4-flash-0731",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "deepseek-v3.2",
            "name": "[Token Plan 团队版] deepseek-v3.2",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
          },
          {
            "id": "kimi-k2.7-code",
            "name": "[Token Plan 团队版] kimi-k2.7-code",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
            "generationConfig": {
              "extra_body": {
                "enable_thinking": true
              }
            }
          },
          {
            "id": "kimi-k2.6",
            "name": "[Token Plan 团队版] kimi-k2.6",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
            "generationConfig": {
              "extra_body": {
                "enable_thinking": true
              }
            }
          },
          {
            "id": "kimi-k2.5",
            "name": "[Token Plan 团队版] kimi-k2.5",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
            "generationConfig": {
              "extra_body": {
                "enable_thinking": true
              }
            }
          },
          {
            "id": "glm-5.2",
            "name": "[Token Plan 团队版] glm-5.2",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
            "generationConfig": {
              "extra_body": {
                "enable_thinking": true
              }
            }
          },
          {
            "id": "glm-5.1",
            "name": "[Token Plan 团队版] glm-5.1",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
            "generationConfig": {
              "extra_body": {
                "enable_thinking": true
              }
            }
          },
          {
            "id": "glm-5",
            "name": "[Token Plan 团队版] glm-5",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY",
            "generationConfig": {
              "extra_body": {
                "enable_thinking": true
              }
            }
          },
          {
            "id": "MiniMax-M2.5",
            "name": "[Token Plan 团队版] MiniMax-M2.5",
            "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
            "envKey": "QWENCLOUD_TOKEN_PLAN_API_KEY"
          }
        ]
      },
      "security": {
        "auth": {
          "selectedType": "openai"
        }
      },
      "tokenPlan": {
        "region": "china"
      },
      "model": {
        "name": "qwen3.7-plus"
      },
      "$version": 3
    }
    ```

    3. 点击右上角图标启动 Qwen Code，通过输入或点击 `/`，选择 `Switch model` 切换模型。
  </Tab>
</Tabs>

## Qwen Code 桌面版

Qwen Code 桌面版是 Qwen Code 的 GUI 应用，内置 CLI 运行时，无需额外安装命令行工具。桌面版与 CLI 共用同一份`settings.json`配置文件，如果已通过 CLI 完成配置，桌面版无需额外设置即可直接使用。

前往[Qwen Code GitHub Releases](https://github.com/QwenLM/qwen-code/releases)页面，下载适用于您操作系统（macOS、Windows 或 Linux）的桌面版安装包。

## 使用案例

### 一句话复刻网站样式

指定目标网站截图，Qwen Code 自动解析页面结构，生成高还原度的前端代码。

<Expandable title="配置步骤">
  1. 安装并配置 Qwen Code（参见上方配置步骤）。
  2. 在终端输入 `qwen` 进入 Qwen Code。
  3. 输入以下内容安装插件，按 **↑** 选择 `ui-design` 完成安装。

  ```plaintext
  /extensions install wshobson/agents
  ```

  4. 输入以下内容安装 skill。

  ```plaintext
  查看我是否有find skills，没有就直接帮我安装：npx skills add https://github.com/vercel-labs/skills --skill find-skills -y -a qwen-code，然后从 wshobson/agents 帮我安装 web-component-design 到当前目录：npx skills add https://github.com/wshobson/agents --skill web-component-design -y
  ```

  5. 下载网站截图到项目目录，输入以下内容，将自动识别截图的布局、样式，生成网页代码。

  ```plaintext
  /skills web-component-design 根据这个技能，基于 @website.png 帮我复刻一个网页html，注意图片引用需有效。
  ```
</Expandable>

### 为开源项目制作宣传视频

给定开源项目仓库地址，即可一键生成专属宣传视频。

<Expandable title="配置步骤">
  1. 安装并配置 Qwen Code（参见上方配置步骤）。
  2. 在终端输入 `qwen` 进入 Qwen Code。
  3. 输入以下内容制作视频。

  ```plaintext
  基于这个技能 https://github.com/QwenLM/qwen-code-examples/blob/main/skills/oss-styles/SKILL.md，帮我为开源仓库：https://github.com/QwenLM/qwen-code 生成一个演示视频
  ```
</Expandable>

## 了解更多

- Qwen Code 的子智能体、MCP、Skills 等高级功能，请参见 [Qwen Code 官方文档](https://qwenlm.github.io/qwen-code-docs/zh/users/overview/)。
- Qwen Code 的使用案例，请参见[使用案例](https://qwenlm.github.io/qwen-code-docs/zh/showcase/)。

## 错误码

请参考[常见问题](/token-plan/faq#常见报错及解决方案)。

## 常见问题

- Token Plan 个人版：[Token Plan 常见问题](/token-plan/faq)
- Token Plan 团队版：[Token Plan 团队版常见问题](/token-plan/faq)
