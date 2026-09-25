> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 参考视频生成

> 复刻动作与外观

- **角色复刻**：从参考图片或视频中复制角色外观。如果参考素材是视频，模型还能复刻语音音色。
- **多角色互动**：最多支持五个角色同时出镜，实现自然对话和互动。
- **多镜头叙事**：通过智能多镜头调度，保持角色在不同镜头间的一致性。
- **声音克隆**（wan2.7）：提供 `reference_voice` 音频文件，可独立设置语音音色，不依赖参考视频中的声音。

**快捷链接**：API 参考：[wan2.7](/api-reference/video-generation/wan27-reference-to-video/create-task)、[wan2.6](/api-reference/video-generation/wan-reference-to-video/create-task) | [提示词指南](/developer-guides/accuracy-tuning/video-generation)

## 支持的模型

| **模型**                     | **特性**                             | **输入**      | **输出**                                |
| -------------------------- | ---------------------------------- | ----------- | ------------------------------------- |
| wan2.7-r2v-2026-06-12 `推荐` | 音频同步、多角色、声音克隆、首帧控制、`media` 数组输入    | 文本、图片、视频、音频 | 720P 或 1080P，2-15 秒，30 fps，MP4（H.264） |
| wan2.6-r2v-flash           | 有声或无声视频、单人或多人、多镜头叙事、音画同步。速度快、性价比高。 | 文本、图片、视频    | 720P 或 1080P，2-10 秒，30 fps，MP4（H.264） |
| wan2.6-r2v                 | 有声视频、多角色参考视频生成、多镜头叙事、音画同步          | 文本、图片、视频    | 720P 或 1080P，2-10 秒，30 fps，MP4（H.264） |

## 前提条件

在[千问AI平台](https://platform.qianwenai.com/)获取 DashScope API Key，并设置为环境变量：

```bash
export DASHSCOPE_API_KEY="REDACTED"
```

## 工作原理

Reference-to-video 任务以异步方式运行：

<Steps>
  <Step title="提交任务">
    通过 POST 请求发送模型名称、提示词、参考素材 URL 和参数。API 返回一个 `task_id`。
  </Step>

  <Step title="轮询结果">
    使用 `task_id` 通过 GET 请求查询任务状态。当状态为 `SUCCEEDED` 时，响应中包含生成视频的 URL。
  </Step>
</Steps>

| **任务状态**    | **说明**                               |
| ----------- | ------------------------------------ |
| `PENDING`   | 任务排队中                                |
| `RUNNING`   | 视频生成中                                |
| `SUCCEEDED` | 生成完成，可在 `output.video_url` 中获取视频 URL |
| `FAILED`    | 生成失败，查看 `message` 了解详情               |

输出视频的 URL 在 **24 小时**后过期，请在此之前下载或转存。

## 快速开始

提交一个 reference-to-video 任务并轮询结果。

<Tabs>
  <Tab title="curl (wan2.7)">
    Wan 2.7 通过 `media` 数组提供参考素材。在提示词中使用 `Video N` 或 `Image N` 引用角色（图片和视频分开编号）。

    **第 1 步：提交任务**

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.7-r2v-2026-06-12",
      "input": {
        "prompt": "Video 2 holds Image 3 and plays a soothing American country ballad in a coffee shop, while Video 1 smiles, watches Video 2, and slowly walks towards him",
        "media": [
          {"type": "reference_video", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4"},
          {"type": "reference_video", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4"},
          {"type": "reference_image", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"}
        ]
      },
      "parameters": {
        "resolution": "720P",
        "duration": 10,
        "prompt_extend": false,
        "watermark": true
      }
    }'
    ```

    **第 2 步：通过任务 ID 获取结果**

    将 `{task_id}` 替换为上一步 API 调用返回的 `task_id` 值。

    ```bash
    curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```

    <Note>
      **与 wan2.6 的主要区别**：wan2.7 使用 `media` 数组代替 `reference_urls`，角色引用方式为 `Video 1`/`Image 1`（而非 `character1`），使用 `resolution`+`ratio` 代替 `size`，支持 `reference_voice` 声音克隆，且 `watermark` 默认值为 `false`。
    </Note>
  </Tab>

  <Tab title="curl (wan2.6)">
    **第 1 步：提交任务**

    ```bash
    curl -s --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.6-r2v-flash",
      "input": {
        "prompt": "character1 gives an enthusiastic product introduction to camera, smiling and gesturing naturally.",
        "reference_urls": ["https://example.com/presenter.mp4"]
      },
      "parameters": {
        "size": "1280*720",
        "duration": 5
      }
    }'
    ```

    **第 2 步：轮询结果**

    将 `{task_id}` 替换为第 1 步响应中的 `task_id`。

    ```bash
    curl -s https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>
</Tabs>

**示例输出**

任务成功后，响应中包含视频 URL：

```json
{
  "output": {
    "task_id": "your-task-id",
    "task_status": "SUCCEEDED",
    "submit_time": "2026-01-01 12:00:00.000",
    "scheduled_time": "2026-01-01 12:00:01.000",
    "end_time": "2026-01-01 12:01:00.000",
    "orig_prompt": "...",
    "video_url": "https://dashscope-result.aliyuncs.com/..."
  },
  "usage": {
    "duration": 10,
    "input_video_duration": 5,
    "output_video_duration": 10,
    "video_count": 1,
    "audio": true,
    "SR": 720
  },
  "request_id": "abc123"
}
```

完整的 Python 示例（含内置轮询），请参阅[多角色互动](#多角色互动)。

## 参数说明

### wan2.7-r2v-2026-06-12

| **参数**                     | **类型**  | **必选** | **说明**                                                                             |
| -------------------------- | ------- | ------ | ---------------------------------------------------------------------------------- |
| `model`                    | string  | 是      | `"wan2.7-r2v-2026-06-12"`                                                          |
| `input.prompt`             | string  | 是      | 最多 5,000 个字符。使用 `Video 1`/`Image 1` 按 `media` 数组中的顺序引用角色（图片和视频分开计数）。               |
| `input.media`              | array   | 是      | 1-5 个元素。每个元素包含 `type`（`reference_image`、`reference_video` 或 `first_frame`）和 `url`。 |
| `input.negative_prompt`    | string  | 否      | 最多 500 个字符。指定需要排除的内容。                                                              |
| `input.reference_voice`    | string  | 否      | 音频文件 URL（WAV/MP3 格式，1-10 秒，最大 15 MB），用于声音克隆。会覆盖参考视频中的音频。                           |
| `parameters.resolution`    | string  | 否      | `"720P"` 或 `"1080P"`（默认）。                                                          |
| `parameters.ratio`         | string  | 否      | `"16:9"`（默认）、`"9:16"`、`"1:1"`、`"4:3"`、`"3:4"`。提供 `first_frame` 时此参数被忽略。            |
| `parameters.duration`      | integer | 否      | 仅图片参考时为 2-15，包含视频参考时为 2-10。默认值：5。                                                  |
| `parameters.prompt_extend` | boolean | 否      | 通过 LLM 改写提示词。默认值：`true`。                                                           |
| `parameters.watermark`     | boolean | 否      | 默认值：`false`。                                                                       |
| `parameters.seed`          | integer | 否      | 取值范围：0 到 2,147,483,647。                                                            |

#### 角色引用方式（wan2.7）

每个 media 元素根据其位置映射到一个角色标识符。**图片和视频分开计数**：

```json
"media": [
  {"type": "reference_video", "url": "https://example.com/person-a.mp4"},   // Video 1
  {"type": "reference_video", "url": "https://example.com/person-b.mp4"},   // Video 2
  {"type": "reference_image", "url": "https://example.com/guitar.png"}      // Image 3
]
```

在提示词中使用这些标识符：*"Video 1 plays guitar while Video 2 sings along, holding Image 3."*

### wan2.6 模型

| **参数**                 | **类型**  | **必选** | **说明**                                                                                                            |
| ---------------------- | ------- | ------ | ----------------------------------------------------------------------------------------------------------------- |
| `model`                | string  | 是      | `"wan2.6-r2v-flash"` 或 `"wan2.6-r2v"`                                                                             |
| `input.prompt`         | string  | 是      | 描述场景的文本提示词。按 `reference_urls` 中 URL 的顺序，使用 `character1`、`character2` 等引用角色。                                       |
| `input.reference_urls` | array   | 是      | 最多 5 个 URL，指向参考图片或视频。每个参考素材应包含单个角色。                                                                               |
| `parameters.size`      | string  | 否      | 输出分辨率。例如 `"1280*720"`（16:9）。所有选项请参阅 [API 参考](/api-reference/video-generation/wan-reference-to-video/create-task)。 |
| `parameters.duration`  | integer | 否      | 输出视频时长（秒）。                                                                                                        |
| `parameters.audio`     | boolean | 否      | `true` 生成有声视频，`false` 生成无声视频。默认值：`true`。仅 `wan2.6-r2v-flash` 支持无声视频。                                              |
| `parameters.shot_type` | string  | 否      | `"multi"` 多镜头切换，`"single"` 固定视角。                                                                                  |
| `parameters.watermark` | boolean | 否      | `true` 添加水印。                                                                                                      |

### 参考素材输入限制

| **类型**      | **数量上限** | **说明**                   |
| ----------- | -------- | ------------------------ |
| 图片          | 5        | 人物、物体或背景                 |
| 视频          | 3        | 适合角色或物体参考。避免使用背景或空场景的视频。 |
| 合计（图片 + 视频） | 5        | 所有参考素材的总数上限              |

输入方式：公开 URL（HTTP 或 HTTPS）。

#### 角色引用方式（wan2.6）

每个参考 URL 根据其在 `reference_urls` 数组中的位置映射到一个角色标识符：

```json
"reference_urls": [
  "https://example.com/person-a.mp4",   // character1
  "https://example.com/person-b.mp4",   // character2
  "https://example.com/guitar.png"      // character3
]
```

在提示词中使用这些标识符：*"character1 plays guitar while character2 sings along, holding character3."*

## 多角色互动

最多支持五个角色同时出镜，实现自然对话和互动——适用于采访、对话、教程等场景。

**支持的模型**：所有模型。

将 `shot_type` 设为 `multi` 可实现动态多镜头切换，设为 `single` 则使用固定视角。

### 示例：四参考素材场景

**提示词**：*"character2 sits on a chair by the window, holding character3, and plays a soothing American country folk song next to character4. character1 says to character2: 'that sounds great'"*

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入**</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**类型**</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**参考角色**</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      [wan-r2v-role1.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/kkogqc/wan-r2v-role1.mp4)
    </td>

    <td style={{verticalAlign: "top"}}>
      视频
    </td>

    <td style={{verticalAlign: "top"}}>
      character1（人物）
    </td>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      [wan-r2v-role2.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/eywute/wan-r2v-role2.mp4)
    </td>

    <td style={{verticalAlign: "top"}}>
      视频
    </td>

    <td style={{verticalAlign: "top"}}>
      character2（人物）
    </td>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      <img alt="wan-r2v-object4" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/1030170771/p1052555.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      图片
    </td>

    <td style={{verticalAlign: "top"}}>
      character3（物体）
    </td>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      <img alt="wan-r2v-backgroud5" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/1030170771/p1052556.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      图片
    </td>

    <td style={{verticalAlign: "top"}}>
      character4（背景）
    </td>
  </tr>
</table>

**输出**：[多镜头有声视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/iwyntz/wan-r2v-result-6.mp4)

### 示例：双人对话

**提示词**：*"character1 says to character2: 'I'll rely on you tomorrow morning!' character2 replies: 'You can count on me!'"*

| **输入**                                                                                                                                       | **类型** | **参考角色**   |
| -------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ---------- |
| [compressed-video (1).mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260107/jrinkp/compressed-video+%281%29.mp4) | 视频     | character1 |
| [compressed-video.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260107/gmdugu/compressed-video.mp4)             | 视频     | character2 |

**输出**：[多镜头有声视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260107/fypjmn/compressed-video+%282%29.mp4)

### 示例代码（curl）

所有示例均使用 `X-DashScope-Async: enable` 请求头提交异步任务。

**第 1 步：提交任务**

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
  -H 'X-DashScope-Async: enable' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
  "model": "wan2.6-r2v-flash",
  "input": {
    "prompt": "Character2 sits on a chair by the window, holding character3, and plays a soothing American country folk song next to character4. Character1 says to Character2: \"that sounds great\"",
    "reference_urls": [
      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/aacgyk/wan-r2v-role1.mp4",
      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/mmizqq/wan-r2v-role2.mp4",
      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png",
      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
    ]
  },
  "parameters": {
    "size": "1280*720",
    "duration": 10,
    "audio": true,
    "shot_type": "multi",
    "watermark": true
  }
}'
```

**第 2 步：获取结果**

将 `<task-id>` 替换为第 1 步响应中的 `task_id`。

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/<task-id> \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 示例代码（Python）

以下示例提交一个多角色任务，并轮询直到获取结果。

```python
import os
import time
import requests

API_KEY = os.environ.get("DASHSCOPE_API_KEY")
BASE_URL = "https://dashscope.aliyuncs.com/api/v1"

headers = {
  "Authorization": f"Bearer {API_KEY}",
  "Content-Type": "application/json",
  "X-DashScope-Async": "enable",
}

# 第 1 步：提交任务
payload = {
  "model": "wan2.6-r2v-flash",
  "input": {
    "prompt": (
      'Character2 sits on a chair by the window, holding character3, '
      'and plays a soothing American country folk song next to character4. '
      'Character1 says to Character2: "that sounds great"'
    ),
    "reference_urls": [
      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/aacgyk/wan-r2v-role1.mp4",
      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/mmizqq/wan-r2v-role2.mp4",
      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png",
      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png",
    ],
  },
  "parameters": {
    "size": "1280*720",
    "duration": 10,
    "audio": True,
    "shot_type": "multi",
    "watermark": True,
  },
}

response = requests.post(
  f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
  headers=headers,
  json=payload,
)
result = response.json()
task_id = result["output"]["task_id"]
print(f"任务已提交: {task_id}")

# 第 2 步：轮询结果
poll_headers = {"Authorization": f"Bearer {API_KEY}"}

while True:
  status_response = requests.get(
    f"{BASE_URL}/tasks/{task_id}", headers=poll_headers
  )
  status = status_response.json()
  task_status = status["output"]["task_status"]

  if task_status == "SUCCEEDED":
    video_url = status["output"]["video_url"]
    print(f"视频已生成: {video_url}")
    break
  elif task_status == "FAILED":
    print(f"任务失败: {status['output'].get('message', '未知错误')}")
    break
  else:
    print(f"状态: {task_status} -- 等待 10 秒...")
    time.sleep(10)
```

## 单角色表演

从单个参考视频或图片创建跨场景的完整角色表演——适用于个人品牌、产品代言、培训教学等场景。

**支持的模型**：所有模型。

在 `reference_urls` 中传入单个 URL，并在提示词中使用 `character1`。建议将 `shot_type` 设为 `multi`。

### 示例：节日开箱视频

**提示词**：*"Create a festive holiday unboxing experience. Shot 1 \[0-2s]: Character1 sits by a beautifully decorated Christmas tree with twinkling lights, holding a wrapped gift box with elegant red and gold wrapping. Shot 2 \[2-4s]: Close-up as Character1 carefully unwraps the gift, revealing premium skincare products inside. Shot 3 \[4-6s]: Character1 applies the product with delight, saying: 'This holiday glow is exactly what I wanted!' Shot 4 \[6-10s]: Character1 admires their radiant skin in a handheld mirror, surrounded by festive decorations, ending with a warm smile to camera."*

| **输入**                                                                                                                             | **输出**                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| [wan-r2v-role-4.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/mjgmzx/wan-r2v-role-4.mp4)（参考视频） | [多镜头有声视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/dpeuyu/wan-r2v-result-4.mp4) |

### 示例代码（curl）

**第 1 步：提交任务**

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
  -H 'X-DashScope-Async: enable' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
  "model": "wan2.6-r2v-flash",
  "input": {
    "prompt": "Create a festive holiday unboxing experience.Shot 1 [0-2s]: Character1 sits by a beautifully decorated Christmas tree with twinkling lights, holding a wrapped gift box with elegant red and gold wrapping. Shot 2 [2-4s]: Close-up as Character1 carefully unwraps the gift, revealing premium skincare products inside. Shot 3 [4-6s]: Character1 applies the product with delight, saying: \"This holiday glow is exactly what I wanted!\" Shot 4 [6-10s]: Character1 admires their radiant skin in a handheld mirror, surrounded by festive decorations, ending with a warm smile to camera.",
    "reference_urls":["https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/mjgmzx/wan-r2v-role-4.mp4"]
  },
  "parameters": {
    "size": "1280*720",
    "duration": 10,
    "shot_type":"multi",
    "watermark": true
  }
}'
```

**第 2 步：获取结果**

将 `<task-id>` 替换为第 1 步响应中的 `task_id`。

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/<task-id> \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 无声视频生成

创建不含音频的纯画面视频——适用于动态海报、无声短视频等场景。

**支持的模型**：仅 `wan2.6-r2v-flash`。

将 `audio` 设为 `false`。

### 示例：无声舞蹈视频

**提示词**：*"character1 drinks bubble tea while dancing spontaneously to the music."*

| **输入**                                                                                                                             | **输出**                                                                                                           |
| ---------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| [wan-r2v-role-1.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/wduhcj/wan-r2v-role-1.mp4)（参考视频） | [无声视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260205/yqhean/wan-r2v-result-5.mp4) |

### 示例代码（curl）

**第 1 步：提交任务**

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
  -H 'X-DashScope-Async: enable' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
  "model": "wan2.6-r2v-flash",
  "input": {
    "prompt": "character1 drinks bubble tea while dancing spontaneously to the music.",
    "reference_urls":["https://cdn.wanx.aliyuncs.com/static/demo-wan26/vace.mp4"]
  },
  "parameters": {
    "size": "1280*720",
    "duration": 5,
    "shot_type":"multi",
    "audio": false,
    "watermark": true
  }
}'
```

**第 2 步：获取结果**

将 `<task-id>` 替换为第 1 步响应中的 `task_id`。

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/<task-id> \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 输出规格

| **属性**  | **详情**                                                                   |
| ------- | ------------------------------------------------------------------------ |
| 视频数量    | 每个任务 1 个                                                                 |
| 格式      | MP4（H.264，30 fps）                                                        |
| 分辨率     | wan2.7：通过 `resolution` + `ratio` 设置。wan2.6：通过 `size` 参数设置（如 `1280*720`）。 |
| URL 有效期 | 24 小时                                                                    |

### 响应字段

| **字段**                        | **说明**                                      |
| ----------------------------- | ------------------------------------------- |
| `output.task_id`              | 任务标识符，用于轮询状态。                               |
| `output.task_status`          | `PENDING`、`RUNNING`、`SUCCEEDED` 或 `FAILED`。 |
| `output.video_url`            | 生成视频的 URL。`task_status` 为 `SUCCEEDED` 时可用。  |
| `output.orig_prompt`          | 原始输入提示词。                                    |
| `usage.duration`              | 输出视频时长（秒）。                                  |
| `usage.input_video_duration`  | 输入视频总时长（秒）。                                 |
| `usage.output_video_duration` | 输出视频时长（秒）。                                  |
| `usage.video_count`           | 生成的视频数量（固定为 1）。                             |
| `usage.audio`                 | 输出视频是否包含音频。                                 |
| `usage.SR`                    | 分辨率级别（720 或 1080）。                          |

## 计费与限流

- 免费额度和定价信息，请参阅[模型调用计费](/developer-guides/getting-started/pricing)。
- 限流信息，请参阅[限流](/developer-guides/administration/rate-limits)。

### 计费规则

| **项目** | **是否计费** | **计量单位**                            |
| ------ | -------- | ----------------------------------- |
| 输入图片   | 否        | --                                  |
| 输入视频   | 是        | 按秒计费                                |
| 输出视频   | 是        | 按秒计费                                |
| 失败任务   | 否        | 不消耗[新用户免费额度](/resources/free-quota) |

有声视频和无声视频定价不同。例如，`wan2.6-r2v-flash` 的有声和无声视频各有独立费率。

**总计费时长** = 输入视频时长（上限 5 秒） + 输出视频时长

### 输入视频时长计费方式

5 秒上限在所有参考素材（图片和视频合计）间平均分配。每个视频的计费时长为 `min(实际时长, 截断上限)`。图片不计费。

| **参考素材数量** | **每个视频的截断上限** |
| ---------- | ------------- |
| 1          | 5 秒           |
| 2          | 2.5 秒         |
| 3          | 1.65 秒        |
| 4          | 1.25 秒        |
| 5          | 1 秒           |

**示例**：3 个参考素材（1 张图片 + 2 个视频），每个视频截断上限为 1.65 秒：

计费输入时长 = `min(视频 1 时长, 1.65 秒)` + `min(视频 2 时长, 1.65 秒)`。图片不计费。

## API 参考

- [wan2.7 reference-to-video API 参考](/api-reference/video-generation/wan27-reference-to-video/create-task)
- [wan2.6 reference-to-video API 参考](/api-reference/video-generation/wan-reference-to-video/create-task)

## 常见问题

### 如何设置视频宽高比？

**wan2.7**：使用 `ratio` 参数（`16:9`、`9:16`、`1:1`、`4:3`、`3:4`）。提供 `first_frame` 图片时，宽高比自动从图片推断。

**wan2.6**：使用 `size` 参数。每个分辨率对应固定的宽高比——例如 `size=1280*720` 生成 **16:9** 的视频。

### 如何在提示词中引用角色？

**wan2.7**：使用 `Video N` 或 `Image N` 标识符。图片和视频分开计数：

```json
"media": [
  {"type": "reference_video", "url": "https://example.com/girl.mp4"},   // Video 1
  {"type": "reference_image", "url": "https://example.com/clock.png"}   // Image 2
]
```

**wan2.6**：使用 `character1`、`character2` 等——标识符与 `reference_urls` 中 URL 的顺序一一对应：

```json
"reference_urls": [
  "https://example.com/girl.mp4",   // character1
  "https://example.com/clock.png"   // character2
]
```

### 任务失败怎么办？

轮询任务状态接口。如果 `task_status` 为 `FAILED`，响应中的 `message` 字段会描述错误原因。常见原因包括无效的参考 URL、不支持的文件格式或超过限流。失败任务不计费。
