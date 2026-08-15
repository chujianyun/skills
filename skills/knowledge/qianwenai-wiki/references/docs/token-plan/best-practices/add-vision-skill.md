> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 添加视觉理解能力

> 为编程模型添加视觉能力

Token Plan 支持的部分模型（qwen3.7-plus 等）原生支持视觉理解，可直接处理图片输入。对于 glm-5、MiniMax-M2.5 等纯文本模型，可通过添加本地 Skill 使其获得视觉能力。

<Note>
  运行图片理解 Skill 会消耗 Token Plan Credits，无其他收费项。
</Note>

## 前提条件

1. 已订阅 [Token Plan](https://platform.qianwenai.com/pricing/token-plan)。
2. 已在 AI 工具中完成接入配置，且能正常对话，详情请参见[接入客户端/开发工具](/developer-guides/clients-and-developer-tools/claude-code)。

## 视觉支持情况

| 模型                                                                                | 是否支持视觉 | 说明                           |
| --------------------------------------------------------------------------------- | ------ | ---------------------------- |
| qwen3.8-max、qwen3.7-plus、qwen3.6-plus、kimi-k2.5 等                                 | 是      | 无需额外配置，可直接传入图片               |
| qwen3-max-2026-01-23、qwen3-coder-next、qwen3-coder-plus、glm-5、glm-4.7、MiniMax-M2.5 | 否      | 需通过 Skill 或 Agent 辅助模型获得视觉能力 |

## 方法 1：直接使用视觉模型（推荐）

qwen3.7-plus 等模型具备视觉理解能力。如果经常需要处理图片，直接切换到这些模型是最简单、推荐的做法。

| 工具          | 模型切换方式                                                                                     |
| ----------- | ------------------------------------------------------------------------------------------ |
| Claude Code | `/model qwen3.7-plus` 或 `/model qwen3.6-plus` 或 `/model qwen3.5-plus` 或 `/model kimi-k2.5` |
| OpenCode    | `/models` 然后搜索并选择 `qwen3.7-plus` 或 `qwen3.6-plus` 或 `qwen3.5-plus` 或 `kimi-k2.5`           |
| Qwen Code   | `/model` 然后选择 `qwen3.7-plus` 或 `qwen3.6-plus` 或 `qwen3.5-plus` 或 `kimi-k2.5`               |

更多编程工具中的模型切换方式请参考[接入客户端/开发工具](/developer-guides/clients-and-developer-tools/claude-code)。切换后可直接在对话中引用图片路径，或拖拽/粘贴图片。

## 方法 2：通过 Skill 或 Agent 添加视觉能力

如需使用 glm-5、MiniMax-M2.5 等不支持视觉的模型处理图片，可通过配置 Skill 或 Agent 实现。

<Tabs>
  <Tab title="Claude Code">
    ### 添加 Skill

    1. 在项目目录下的 `.claude` 文件夹中新建 `skills/image-analyzer` 目录：

    ```bash
    mkdir -p .claude/skills/image-analyzer
    ```

    2. 在该目录下创建 `SKILL.md` 文件，并写入以下内容：

    ```markdown
    ---
    name: image-analyzer
    description: 帮助没有视觉能力的模型进行图像理解。当需要分析图像内容、提取图片中的信息、文字、界面元素，或理解截图、图表、架构图等任何视觉内容时，使用此技能，传入图片路径即可获得描述信息。
    model: qwen3.7-plus
    ---
    qwen3.7-plus具有视觉理解能力，请直接使用qwen3.7-plus模型进行图片理解。
    ```

    3. 创建完成后的目录结构如下：

    ```text
    .claude/
    └── skills/
      └── image-analyzer/
        └── SKILL.md
    ```

    ### 开始使用

    1. 在项目目录下运行 `claude` 启动 Claude Code，并运行 `/model glm-5` 切换到 `glm-5` 模型。
    2. 在对话中引用图片路径并提问，例如：`请加载image-analyzer skill，描述一下 screenshot.png 中的内容。`
  </Tab>

  <Tab title="OpenCode">
    ### 添加 Agent

    1. 在项目目录下的 `.opencode` 文件夹中新建 `agents` 目录：

    ```bash
    mkdir -p .opencode/agents
    ```

    2. 在该目录下创建 `image-analyzer.md` 文件，并写入以下内容：

    <Note>
      model 字段必须使用 OpenCode 配置文件中定义的 provider 和模型名称。参考 [OpenCode](/developer-guides/clients-and-developer-tools/opencode) 文档的配置示例，应为 `bailian-token-plan/qwen3.7-plus`。
    </Note>

    ```markdown
    ---
    description: Analyzes images using a vision-capable model. Use this agent when the user needs to understand image content, extract information from screenshots, diagrams, UI mockups, or any visual content. Invoke with @image-analyzer followed by the image path and your question.
    mode: subagent
    model: bailian-token-plan/qwen3.7-plus
    tools:
      write: false
      edit: false
    ---
    You have vision capabilities. Analyze the provided image and return a clear, structured description focused on what the user is asking about.
    ```

    3. 创建完成后的目录结构如下：

    ```text
    .opencode/
    └── agents/
      └── image-analyzer.md
    ```

    ### 开始使用

    1. 在项目目录下运行 `opencode` 启动 OpenCode，并切换到 `glm-5` 模型。
    2. 通过 `@` 唤起 `image-analyzer` 并提问，例如：`@image-analyzer，描述一下 screenshot.png 中的内容。`
  </Tab>
</Tabs>

## 常见问题

<Accordion title="OpenCode + 视觉理解模型为什么无法理解图片？">
  **原因**：OpenCode 默认不启用模型的视觉能力，需要在配置文件中显式声明 `modalities` 参数。

  **解决方案**：在 OpenCode 配置文件的模型定义中添加 `modalities` 字段，将 `input` 设为 `["text", "image"]`，如下所示：

  <Note>
    将 sk-sp-xxx 替换为 Token Plan API Key。
  </Note>

  ```json
  {
    "$schema": "https://opencode.ai/config.json",
    "provider": {
      "bailian-token-plan": {
        "npm": "@ai-sdk/anthropic",
        "name": "Model Studio Token Plan",
        "options": {
          "baseURL": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "apiKey": "sk-sp-xxx"
        },
        "models": {
          "qwen3.6-plus": {
            "name": "Qwen3.6 Plus",
            "modalities": {
              "input": [
                "text",
                "image"
              ],
              "output": [
                "text"
              ]
            },
            "options": {
              "thinking": {
                "type": "enabled",
                "budgetTokens": 1024
              }
            }
          },
          "qwen3.5-plus": {
            "name": "Qwen3.5 Plus",
            "modalities": {
              "input": [
                "text",
                "image"
              ],
              "output": [
                "text"
              ]
            },
            "options": {
              "thinking": {
                "type": "enabled",
                "budgetTokens": 1024
              }
            }
          },
          "kimi-k2.5": {
            "name": "Kimi K2.5",
            "modalities": {
              "input": [
                "text",
                "image"
              ],
              "output": [
                "text"
              ]
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
</Accordion>

<Accordion title="OpenClaw + 视觉理解模型为什么无法理解图片？">
  **原因**：OpenClaw 需要通过配置文件中的 input 字段来判断模型是否支持视觉能力。

  **解决方案**：

  1. 在 `~/.openclaw/openclaw.json` 配置文件中，确保模型定义包含 `"input": ["text", "image"]` 字段。

  ```json
  {
    "models": {
      "mode": "merge",
      "providers": {
        "bailian": {
          "baseUrl": "https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
          "apiKey": "YOUR_API_KEY",
          "api": "openai-completions",
          "models": [
            {
              "id": "qwen3.6-plus",
              "name": "qwen3.6-plus",
              "reasoning": false,
              "input": ["text", "image"],
              "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
              "contextWindow": 1000000,
              "maxTokens": 65536
            },
            {
              "id": "qwen3.5-plus",
              "name": "qwen3.5-plus",
              "reasoning": false,
              "input": ["text", "image"],
              "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
              "contextWindow": 1000000,
              "maxTokens": 65536
            },
            {
              "id": "kimi-k2.5",
              "name": "kimi-k2.5",
              "reasoning": false,
              "input": ["text", "image"],
              "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
              "contextWindow": 262144,
              "maxTokens": 32768
            }
          ]
        }
      }
    },
    "agents": {
      "defaults": {
        "model": {
          "primary": "bailian/qwen3.6-plus"
        },
        "models": {
          "bailian/qwen3.6-plus": {},
          "bailian/qwen3.5-plus": {},
          "bailian/kimi-k2.5": {}
        }
      }
    },
    "gateway": {
      "mode": "local"
    }
  }
  ```

  2. 修改配置后，需要清除 OpenClaw 的模型缓存并重启，否则旧的配置仍会生效。

  ```bash
  rm ~/.openclaw/agents/main/agent/models.json
  openclaw gateway restart
  ```
</Accordion>
