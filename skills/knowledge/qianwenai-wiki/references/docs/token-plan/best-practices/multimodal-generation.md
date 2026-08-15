> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 接入多模态生成模型

> Token Plan 中的图像生成、视频生成、语音合成模型需通过工具的扩展机制（Skill、Slash Command 或 Agent）接入

## 示例：在 Claude Code 中接入图像生成模型

以 Claude Code 为例，通过 Slash Command 接入图像生成模型。其他工具的接入方式类似，区别在于扩展机制和配置文件路径不同。

### 步骤一：创建 Slash Command

将套餐 API Key（以`sk-sp-`为前缀）配置为环境变量`$ANTHROPIC_AUTH_TOKEN`，供后续 curl 鉴权使用。

在项目根目录创建 `.claude/commands/text-to-image.md`，写入以下内容：

````plaintext
调用 Token Plan 文生图 API，根据描述生成图片。

用户需求：$ARGUMENTS

## 步骤

1. 从用户需求中提取 prompt（图片描述）、model、size（默认 1024*1024）。若用户明确指定了模型（如"模型=wan2.7-image"或"用 wan2.7-image 画"），必须严格使用用户指定的模型名，不要回退到默认模型；仅当用户未指定模型时才使用默认 qwen-image-2.0。常用图像生成模型有 qwen-image-2.0、qwen-image-2.0-pro、wan2.7-image、wan2.7-image-pro 等，完整列表以千问AI平台模型列表为准。

2. 调用 API 生成图片（使用 Bash 工具执行 curl）：

```
curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<model>",
    "input": {
      "messages": [{"role":"user","content":[{"text":"<prompt>"}]}]
    },
    "parameters": {"size":"<size>"}
  }'
```

3. 从返回 JSON 的 output.choices[*].message.content[*].image 中提取图片 URL。

4. 用 curl -s -o "generated_$(date +%Y%m%d_%H%M%S).png" "<URL>" 下载到当前目录。

5. 向用户展示生成的图片文件路径。
````

### 步骤二：生成图片

在 Claude Code 中输入 `/text-to-image 画一只猫`。如需使用默认模型以外的图像生成模型，在指令中写明模型名即可，例如`/text-to-image 用 wan2.7-image 画一只猫`。

## 示例：在 Claude Code 中接入视频生成模型

以 Claude Code 为例，通过 Slash Command 接入视频生成模型。视频生成为异步接口，流程为"提交任务 → 轮询状态 → 下载视频"。

### 步骤一：创建 Slash Command

将套餐 API Key（以`sk-sp-`为前缀）配置为环境变量`$ANTHROPIC_AUTH_TOKEN`，供后续 curl 鉴权使用。

在项目根目录创建`.claude/commands/text-to-video.md`，写入以下内容：

````plaintext
调用 Token Plan 文生视频 API，根据描述生成视频并自动下载到本地。
用户需求：$ARGUMENTS
## 步骤
1. 从用户需求中提取 prompt（视频描述）、model（默认 happyhorse-1.1-t2v）、resolution（默认 720P）、ratio（默认 16:9）、duration（默认 5 秒）。若用户明确指定了模型（如"模型=happyhorse-1.0-t2v"），必须严格使用用户指定的模型名。
2. 使用 Bash 工具执行以下脚本，一次性完成提交任务、等待完成、下载视频：
```bash
#!/bin/bash
set -e
TASK_RESPONSE=$(curl -s -X POST "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis" \
  -H "X-DashScope-Async: enable" \
  -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "<model>",
    "input": {"prompt": "<prompt>"},
    "parameters": {"resolution": "<resolution>", "ratio": "<ratio>", "duration": <duration>}
  }')
TASK_ID=$(echo "$TASK_RESPONSE" | grep -o '"task_id":"[^"]*"' | head -1 | cut -d'"' -f4)
if [ -z "$TASK_ID" ]; then echo "提交失败: $TASK_RESPONSE"; exit 1; fi
echo "任务已提交，ID: $TASK_ID，等待生成..."
while true; do
  sleep 15
  STATUS_RESPONSE=$(curl -s "https://token-plan.cn-beijing.maas.aliyuncs.com/api/v1/tasks/$TASK_ID" \
    -H "Authorization: Bearer $ANTHROPIC_AUTH_TOKEN")
  STATUS=$(echo "$STATUS_RESPONSE" | grep -o '"task_status":"[^"]*"' | cut -d'"' -f4)
  if [ "$STATUS" = "SUCCEEDED" ]; then
    VIDEO_URL=$(echo "$STATUS_RESPONSE" | grep -o '"video_url":"[^"]*"' | cut -d'"' -f4)
    OUTPUT="generated_$(date +%Y%m%d_%H%M%S).mp4"
    curl -s -o "$OUTPUT" "$VIDEO_URL"
    echo "视频已下载: $(pwd)/$OUTPUT"
    exit 0
  elif [ "$STATUS" = "FAILED" ]; then
    echo "生成失败: $STATUS_RESPONSE"; exit 1
  fi
  echo "生成中..."
done
```
3. 向用户展示生成的视频文件路径。
````

### 步骤二：生成视频

在 Claude Code 中输入`/text-to-video 一只白色的猫在阳台上晒太阳`。如需使用其他视频生成模型，在指令中写明模型名即可，例如`/text-to-video 用 happyhorse-1.1-r2v 生成一只猫跳跃的视频`。

其他工具的配置方式与图像生成相同，将配置内容保存到下方[其他工具](#其他工具)表格中对应路径的 `text-to-video.md`（或 `SKILL.md`）即可。

## 示例：在 Claude Code 中接入语音合成模型

以 Claude Code 为例，通过 Slash Command 接入语音合成模型 qwen-audio-3.0-tts-plus。语音合成使用 DashScope WebSocket 接口，需安装 DashScope Python SDK。

### 步骤一：安装依赖

```bash
pip install dashscope
```

### 步骤二：创建 Slash Command

将套餐 API Key（以`sk-sp-`为前缀）配置为环境变量`$ANTHROPIC_AUTH_TOKEN`，供后续鉴权使用。

在项目根目录创建 `.claude/commands/text-to-speech.md`，写入以下内容：

````plaintext
调用 Token Plan 语音合成 API，将文本转为语音文件。

用户需求：$ARGUMENTS

## 步骤

1. 从用户需求中提取 text（要朗读的文本）、voice（音色，默认 longxiaochun）。若用户指定了音色则使用指定音色。

2. 使用 Bash 工具执行以下 Python 脚本生成音频：

```python
import os
import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer, AudioFormat
from datetime import datetime

dashscope.api_key = os.environ.get("ANTHROPIC_AUTH_TOKEN")
dashscope.base_websocket_api_url = "wss://token-plan.cn-beijing.maas.aliyuncs.com/api-ws/v1/inference"

synthesizer = SpeechSynthesizer(
  model="qwen-audio-3.0-tts-plus",
  voice="<voice>",
  format=AudioFormat.MP3_22050HZ_MONO_256KBPS,
)

audio = synthesizer.call("<text>")
filename = f"speech_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
with open(filename, "wb") as f:
  f.write(audio)
print(f"音频已保存: {filename}")
```

3. 向用户展示生成的音频文件路径。
````

### 步骤三：生成语音

在 Claude Code 中输入 `/text-to-speech 今天天气真不错，适合出去散步`。如需指定音色，在指令中写明即可，例如`/text-to-speech 用 longxiaochun 朗读：欢迎使用千问AI平台`。

## 其他工具

不同工具的扩展机制和配置文件路径如下表所示，该表为支持扩展机制的主流 AI 编程工具示例。将图像生成示例中的配置内容保存到对应路径即可。

| 工具           | 扩展机制          | 配置文件路径                                                   |
| ------------ | ------------- | -------------------------------------------------------- |
| Claude Code  | Slash Command | `.claude/commands/text-to-image.md`                      |
| Codex        | Skill         | `~/.codex/skills/token-plan-image/SKILL.md`              |
| Qwen Code    | Skill         | `~/.qwen/skills/text-to-image/SKILL.md`                  |
| OpenCode     | Agent         | `.opencode/agents/text-to-image.md`                      |
| OpenClaw     | Skill         | `~/.openclaw/workspace/skills/token-plan-image/SKILL.md` |
| Hermes Agent | Skill         | `~/.hermes/skills/media/text-to-image/SKILL.md`          |
| Qoder        | Skill         | `~/.qoder/skills/text-to-image/SKILL.md`                 |

<Note>
  Skill 类工具（Codex、Qwen Code、OpenClaw、Hermes Agent、Qoder）需要在配置文件开头添加 YAML front matter：
</Note>

```plaintext
---
name: "token-plan-image"
description: "调用 Token Plan 文生图模型，根据文字描述生成图片。当用户要求画图、生成图片时激活。"
---

（... 与上述图像生成示例相同的内容 ...）
```
