> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图生视频：首帧

> 基于单张图片生成视频

- **基本设置**：根据模型选择时长和分辨率（参见"可用性"部分）。wan2.7 和 wan2.6 支持 2 至 15 秒的任意整数时长，wan2.5 仅支持 5 秒或 10 秒。模型还支持提示词改写和添加水印。
- **音频能力**：支持自动配音或上传音频实现音画同步。**（wan2.5 及更高版本支持）**
- **多镜头叙事**：生成包含多个镜头的视频，同时保持主体在各镜头间的一致性。**（wan2.6 和 wan2.7 支持）**

**快速链接**：[模型体验](https://platform.qianwenai.com/home/try-ai) **|** API 参考：[wan2.7](/api-reference/video-generation/wan27-image-to-video/create-task)，[wan2.6](/api-reference/video-generation/wan-image-to-video-first-frame/create-task)

## 快速开始

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入提示词**</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入首帧**</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输出视频（带音频的多镜头视频）**</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。
    </td>

    <td style={{verticalAlign: "top"}}>
      ![wan-i2v-haigui](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3937619671/p1047607.webp)
    </td>

    <td style={{verticalAlign: "top"}}>
      <video style={{display: "block", width: "100%"}} src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260121/oiiigs/wan-i2v-haigui-video.mp4" controls />
    </td>
  </tr>
</table>

调用 API 前，请先[获取 API Key](/api-reference/preparation/api-key)并[将 API Key 配置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请[安装 DashScope SDK](/api-reference/preparation/install-sdk)。

<Tabs>
  <Tab title="curl (wan2.7)">
    <Note>
      Wan 2.7 使用 `media` 数组来提供首帧图片，使用 `resolution` 代替像素尺寸，并在提示词中直接描述多镜头内容。
    </Note>

    ```bash
    # 第一步：创建任务，获取任务 ID
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.7-i2v",
      "input": {
        "prompt": "镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。",
        "media": [
          {
            "type": "first_frame",
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"
          }
        ]
      },
      "parameters": {
        "resolution": "1080P",
        "prompt_extend": true,
        "duration": 10
      }
    }'

    # 第二步：使用任务 ID 查询结果
    # 将 {task_id} 替换为上一步 API 返回的 task_id 值
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>

  <Tab title="curl (wan2.6)">
    ```bash
    # 第一步：创建任务，获取任务 ID
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.6-i2v-flash",
      "input": {
        "prompt": "镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"
      },
      "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "watermark": true,
        "duration": 10,
        "shot_type":"multi"
      }
    }'

    # 第二步：使用任务 ID 查询结果
    # 将 {task_id} 替换为上一步 API 返回的 task_id 值
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>
</Tabs>

<Note>
  **SDK 版本要求**：

  - **DashScope Python SDK**：1.25.8 或更高版本
  - **DashScope Java SDK**：2.22.6 或更高版本

  如果 SDK 版本过低，可能会遇到 "url error, please check url!" 等错误。请[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

<Accordion title="Python 和 Java SDK 示例（wan2.6）">
  <CodeGroup>
    ```python Python SDK
    import os
    from http import HTTPStatus
    from dashscope import VideoSynthesis
    import dashscope

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
    api_key = os.getenv("DASHSCOPE_API_KEY")

    print('请稍候...')
    rsp = VideoSynthesis.call(api_key=api_key,
                              model='wan2.6-i2v-flash',
                              prompt='镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。',
                              img_url="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp",
                              resolution="720P",
                              duration=10,
                              shot_type="multi",
                              prompt_extend=True,
                              watermark=True)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
      print("video_url:", rsp.output.video_url)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))
    ```

    ```java Java SDK
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.InputRequiredException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.alibaba.dashscope.utils.JsonUtils;
    import com.alibaba.dashscope.utils.Constants;

    public class Image2Video {

      static {
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
      }

      // 如果未配置环境变量，请将下行替换为您的 API Key：apiKey="sk-xxx"
      static String apiKey = System.getenv("DASHSCOPE_API_KEY");

      public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
            VideoSynthesisParam.builder()
                .apiKey(apiKey)
                .model("wan2.6-i2v-flash")
                .prompt("镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。")
                .imgUrl("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp")
                .duration(10)
                .resolution("720P")
                .shotType("multi")
                .promptExtend(true)
                .watermark(true)
                .build();
        System.out.println("请稍候...");
        VideoSynthesisResult result = vs.call(param);
        System.out.println(JsonUtils.toJson(result));
      }

      public static void main(String[] args) {
        try {
          image2video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
          System.out.println(e.getMessage());
        }
        System.exit(0);
      }
    }
    ```

    ```bash curl
    # 第一步：创建任务，获取任务 ID
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.6-i2v-flash",
      "input": {
        "prompt": "镜头从海龟下方缓缓上移，海龟悠然游动，腹部细节清晰可见。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260121/zlpocv/wan-i2v-haigui.webp"
      },
      "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "watermark": true,
        "duration": 10,
        "shot_type":"multi"
      }
    }'

    # 第二步：使用任务 ID 查询结果
    # 将 {task_id} 替换为上一步 API 返回的 task_id 值
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </CodeGroup>
</Accordion>

## 核心功能

### 多镜头视频

**支持模型**：`wan2.7-i2v`、`wan2.6-i2v-flash`、`wan2.6-i2v`。

**简介**：自动切换镜头，如从全景切换到特写。适用于 MV 等场景。

**参数配置**：

- **wan2.7**：在提示词中直接描述镜头（如 `Shot 1 [0-3 s]: ...`），无需设置 `shot_type` 参数。
- **wan2.6**：将 `shot_type` 设置为 `"multi"`。
- `prompt_extend`：必须设为 `true`，以启用智能改写来优化镜头描述。

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入提示词**</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入首帧**</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输出视频（wan2.6，多镜头视频）**</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。
    </td>

    <td style={{verticalAlign: "top"}}>
      ![rap](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/1682878571/p1011609.webp) <strong>输入音频</strong>：<audio style={{width: "100%"}} src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250925/taxesr/rap.mp3" controls />
    </td>

    <td style={{verticalAlign: "top"}}>
      <video style={{display: "block", width: "100%"}} src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251215/ofaaah/wan2.6.mp4" controls />
    </td>
  </tr>
</table>

<Note>
  请确保 DashScope SDK 为最新版本：

  - Python SDK：`1.25.8` 或更高版本
  - Java SDK：`2.22.6` 或更高版本

  [安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

<CodeGroup>
  ```python Python SDK
  import os
  from http import HTTPStatus
  from dashscope import VideoSynthesis
  import dashscope

  dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

  # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx"
  api_key = os.getenv("DASHSCOPE_API_KEY")

  def sample_async_call_i2v():
    # 异步调用，返回 task_id
    rsp = VideoSynthesis.async_call(api_key=api_key,
                    model='wan2.6-i2v-flash',
                    prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。',
                    img_url="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
                    audio_url="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3",
                    resolution="720P",
                    duration=10,
                    shot_type="multi", # 多镜头
                    prompt_extend=True,
                    watermark=True,
                    negative_prompt="",
                    seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
      print("task_id: %s" % rsp.output.task_id)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

    # 等待异步任务完成
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
      print(rsp.output.video_url)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

  if __name__ == '__main__':
    sample_async_call_i2v()
  ```

  ```java Java SDK
  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
  import com.alibaba.dashscope.exception.ApiException;
  import com.alibaba.dashscope.exception.InputRequiredException;
  import com.alibaba.dashscope.exception.NoApiKeyException;
  import com.alibaba.dashscope.utils.JsonUtils;
  import com.alibaba.dashscope.utils.Constants;

  public class Image2Video {
    static {
      Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 如果未配置环境变量，请将下行替换为您的 API Key：apiKey="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // 设置输入图片 URL
    static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";
    // 设置音频 URL
    static String audioUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3";

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
      VideoSynthesis vs = new VideoSynthesis();
      VideoSynthesisParam param =
          VideoSynthesisParam.builder()
              .apiKey(apiKey)
              .model("wan2.6-i2v-flash")
              .prompt("一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。")
              .imgUrl(imgUrl)
              .audioUrl(audioUrl)
              .shotType("multi")
              .duration(10)
              .resolution("720P")
              .negativePrompt("")
              .promptExtend(true)
              .watermark(true)
              .seed(12345)
              .build();
      // 异步调用
      VideoSynthesisResult task = vs.asyncCall(param);
      System.out.println(JsonUtils.toJson(task));
      System.out.println("请稍候...");

      // 获取结果
      VideoSynthesisResult result = vs.wait(task, apiKey);
      System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
      try {
        image2video();
      } catch (ApiException | NoApiKeyException | InputRequiredException e) {
        System.out.println(e.getMessage());
      }
      System.exit(0);
    }
  }
  ```

  ```bash curl
  # 第一步：创建任务，获取任务 ID
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    -H 'X-DashScope-Async: enable' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
    "model": "wan2.6-i2v-flash",
    "input": {
      "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。",
      "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
      "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
    },
    "parameters": {
      "resolution": "720P",
      "prompt_extend": true,
      "duration": 10,
      "shot_type":"multi"
    }
  }'

  # 第二步：使用任务 ID 查询结果
  # 将 {task_id} 替换为上一步 API 返回的 task_id 值
  curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY"
  ```
</CodeGroup>

### 音画同步

**支持模型**：`wan2.7-i2v`、`wan2.6-i2v-flash`、`wan2.6-i2v`、`wan2.5-i2v-preview`。

<Note>
  **wan2.7**：使用 `media` 数组中 `driving_audio` 类型来提供口型同步的音频。如果不提供音频，模型会自动生成音效。详见 [wan2.7 API 参考](/api-reference/video-generation/wan27-image-to-video/create-task)。
</Note>

**简介**：让照片中的人物开口说话或唱歌，嘴唇动作与音频保持同步。更多示例请参见[声音生成](/developer-guides/accuracy-tuning/video-generation)。

**参数配置**：

- **提供音频文件**：传入 `audio_url`，模型会根据音频文件对齐口型动作。
- **自动配音**：不传 `audio_url`，模型默认输出带音频的视频，会根据画面内容自动生成背景音效、音乐或人声。

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入提示词**</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入首帧**</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输出视频（带音频）**</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。
    </td>

    <td style={{verticalAlign: "top"}}>
      ![rap](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/1682878571/p1011609.webp) <strong>输入音频</strong>：<audio style={{width: "100%"}} src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250925/taxesr/rap.mp3" controls />
    </td>

    <td style={{verticalAlign: "top"}}>
      <video style={{display: "block", width: "100%"}} src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250925/yfwbhx/%E8%8B%B1%E6%96%87rap+%281%29.mp4" controls />
    </td>
  </tr>
</table>

<Note>
  请确保 DashScope SDK 为最新版本：

  - Python SDK：`1.25.8` 或更高版本
  - Java SDK：`2.22.6` 或更高版本

  [安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

<CodeGroup>
  ```python Python SDK
  import os
  from http import HTTPStatus
  from dashscope import VideoSynthesis
  import dashscope

  dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

  # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx"
  api_key = os.getenv("DASHSCOPE_API_KEY")

  def sample_async_call_i2v():
    # 异步调用，返回 task_id
    rsp = VideoSynthesis.async_call(api_key=api_key,
                    model='wan2.6-i2v-flash',
                    prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。',
                    img_url="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
                    audio_url="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3",
                    resolution="720P",
                    duration=10,
                    prompt_extend=True,
                    watermark=True,
                    negative_prompt="",
                    seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
      print("task_id: %s" % rsp.output.task_id)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

    # 等待异步任务完成
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
      print(rsp.output.video_url)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

  if __name__ == '__main__':
    sample_async_call_i2v()
  ```

  ```java Java SDK
  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
  import com.alibaba.dashscope.exception.ApiException;
  import com.alibaba.dashscope.exception.InputRequiredException;
  import com.alibaba.dashscope.exception.NoApiKeyException;
  import com.alibaba.dashscope.utils.JsonUtils;
  import com.alibaba.dashscope.utils.Constants;

  public class Image2Video {
    static {
      Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 如果未配置环境变量，请将下行替换为您的 API Key：apiKey="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    // 设置输入图片 URL
    static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";
    // 设置音频 URL
    static String audioUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3";

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
      VideoSynthesis vs = new VideoSynthesis();
      VideoSynthesisParam param =
          VideoSynthesisParam.builder()
              .apiKey(apiKey)
              .model("wan2.6-i2v-flash")
              .prompt("一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。")
              .imgUrl(imgUrl)
              .audioUrl(audioUrl)
              .duration(10)
              .resolution("720P")
              .negativePrompt("")
              .promptExtend(true)
              .watermark(true)
              .seed(12345)
              .build();
      // 异步调用
      VideoSynthesisResult task = vs.asyncCall(param);
      System.out.println(JsonUtils.toJson(task));
      System.out.println("请稍候...");

      // 获取结果
      VideoSynthesisResult result = vs.wait(task, apiKey);
      System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
      try {
        image2video();
      } catch (ApiException | NoApiKeyException | InputRequiredException e) {
        System.out.println(e.getMessage());
      }
      System.exit(0);
    }
  }
  ```
</CodeGroup>

**curl**

**第一步：创建任务，获取任务 ID**

<Tabs>
  <Tab title="提供音频文件">
    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.5-i2v-preview",
      "input": {
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
      },
      "parameters": {
        "resolution": "480P",
        "prompt_extend": true,
        "duration": 10
      }
    }'
    ```
  </Tab>

  <Tab title="自动配音">
    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.5-i2v-preview",
      "input": {
        "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。",
        "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
      },
      "parameters": {
        "resolution": "480P",
        "prompt_extend": true,
        "duration": 10
      }
    }'
    ```
  </Tab>
</Tabs>

**第二步：使用任务 ID 查询结果**

将 `{task_id}` 替换为上一步 API 返回的 `task_id` 值。

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 生成无音频视频

**支持模型**：`wan2.6-i2v-flash`、`wan2.2 及更早版本`。

**简介**：适用于不需要音频的纯视觉场景，如动态海报和无声短视频。

**参数配置**：

- `wan2.6-i2v-flash`：该模型默认生成带音频的视频。如需生成无音频视频，必须显式设置 `audio=false`。即使传入了 `audio_url`，只要 `audio=false`，输出的视频也是无声的。定价详情请参见 [wan2.6-i2v-flash 定价](https://www.qianwenai.com/models/wan2.6-i2v-flash)。
- `wan2.2 及更早版本`：这些模型默认生成无声视频，无需额外配置。

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**提示词**</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入首帧**</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输出视频（无音频）**</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      一只猫在草地上奔跑
    </td>

    <td style={{verticalAlign: "top"}}>
      ![image](https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2102998671/p1007038.png)
    </td>

    <td style={{verticalAlign: "top"}}>
      <video style={{display: "block", width: "100%"}} src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250418/oyxuch/29a2e615-6443-4647-bbe2-e26f345a3b26.mp4" controls />
    </td>
  </tr>
</table>

<Note>
  请确保 DashScope SDK 为最新版本：

  - Python SDK：`1.25.8` 或更高版本
  - Java SDK：`2.22.6` 或更高版本

  [安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

<CodeGroup>
  ```python Python SDK
  import os
  from http import HTTPStatus
  from dashscope import VideoSynthesis
  import dashscope

  dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

  # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx"
  api_key = os.getenv("DASHSCOPE_API_KEY")

  def sample_async_call_i2v():
    # 异步调用，返回 task_id
    rsp = VideoSynthesis.async_call(api_key=api_key,
                    model='wan2.6-i2v-flash',
                    prompt='一只猫在草地上奔跑',
                    img_url="https://cdn.translate.alibaba.com/r/wanx-demo-1.png",
                    audio=False,   # 必须显式设为 False 才能输出无音频视频
                    resolution="720P",
                    duration=5,
                    prompt_extend=True,
                    watermark=True,
                    negative_prompt="",
                    seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
      print("task_id: %s" % rsp.output.task_id)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

    # 等待异步任务完成
    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
      print(rsp.output.video_url)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

  if __name__ == '__main__':
    sample_async_call_i2v()
  ```

  ```java Java SDK
  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
  import com.alibaba.dashscope.exception.ApiException;
  import com.alibaba.dashscope.exception.InputRequiredException;
  import com.alibaba.dashscope.exception.NoApiKeyException;
  import com.alibaba.dashscope.utils.JsonUtils;
  import com.alibaba.dashscope.utils.Constants;

  public class Image2Video {
    static {
      Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 如果未配置环境变量，请将下行替换为您的 API Key：apiKey="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
      VideoSynthesis vs = new VideoSynthesis();
      VideoSynthesisParam param =
          VideoSynthesisParam.builder()
              .apiKey(apiKey)
              .model("wan2.6-i2v-flash")
              .prompt("一只猫在草地上奔跑")
              .imgUrl("https://cdn.translate.alibaba.com/r/wanx-demo-1.png")
              .audio(false)   /* 必须显式设为 false 才能输出无音频视频 */
              .duration(10)
              .resolution("720P")
              .negativePrompt("")
              .promptExtend(true)
              .watermark(true)
              .seed(12345)
              .build();
      // 异步调用
      VideoSynthesisResult task = vs.asyncCall(param);
      System.out.println(JsonUtils.toJson(task));
      System.out.println("请稍候...");

      // 获取结果
      VideoSynthesisResult result = vs.wait(task, apiKey);
      System.out.println(JsonUtils.toJson(result));
    }

    public static void main(String[] args) {
      try {
        image2video();
      } catch (ApiException | NoApiKeyException | InputRequiredException e) {
        System.out.println(e.getMessage());
      }
      System.exit(0);
    }
  }
  ```
</CodeGroup>

**curl**

**第一步：创建任务，获取任务 ID**

<Tabs>
  <Tab title="wan2.6-i2v-flash">
    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.6-i2v-flash",
      "input": {
        "prompt": "一只猫在草地上奔跑",
        "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"
      },
      "parameters": {
        "audio": false,
        "resolution": "720P",
        "prompt_extend": true,
        "watermark": true,
        "duration": 5
      }
    }'
    ```
  </Tab>

  <Tab title="wan2.2 及更早版本">
    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.2-i2v-plus",
      "input": {
        "prompt": "一只猫在草地上奔跑",
        "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"
      },
      "parameters": {
        "resolution": "480P",
        "prompt_extend": true
      }
    }'
    ```
  </Tab>
</Tabs>

**第二步：使用任务 ID 查询结果**

将 `{task_id}` 替换为上一步 API 返回的 `task_id` 值。

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 图片和音频输入方式

### 输入图片

- **数量**：1 张。
- **输入方式**：公网图片 URL、本地文件路径或 Base64 编码字符串。

<Accordion title="方式一：公网 URL（HTTP 接口、SDK）- 推荐">
  * **要求**：支持 HTTP 或 HTTPS 协议，请确保图片 URL 可通过公网直接访问。
  * **示例**："[https://example.com/img.png](https://example.com/img.png)"
</Accordion>

<Accordion title="方式二：本地文件路径（仅限 SDK）">
  Python 和 Java 的文件路径格式略有差异。在 Windows 上：Python 使用两个斜杠（`file://`），Java 使用三个（`file:///`）。请仔细参照以下规则。

  **Python SDK**：支持**绝对路径和相对路径**。文件路径规则如下：

| **操作系统**      | **输入文件路径**          | **示例（绝对路径）**                   | **示例（相对路径）**               |
| ------------- | ------------------- | ------------------------------ | -------------------------- |
| Linux / macOS | `file://` + 绝对或相对路径 | `file:///home/images/test.png` | `file://./images/test.png` |
| Windows       | `file://` + 绝对或相对路径 | `file://D:/images/test.png`    | `file://./images/test.png` |

  **Java SDK**：仅支持**绝对路径**。文件路径规则如下：

| **操作系统**      | **输入文件路径**        | **示例（绝对路径）**                   |
| ------------- | ----------------- | ------------------------------ |
| Linux / macOS | `file://` + 绝对路径  | `file:///home/images/test.png` |
| Windows       | `file:///` + 绝对路径 | `file:///D:/images/test.png`   |
</Accordion>

<Accordion title="方式三：Base64 编码字符串（HTTP 接口、SDK）">
  - **示例**：`data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABDg......`（示例仅作展示，内容已截断）。
  - **格式要求**：遵循 `data:<MIME_type>;base64,<base64_data>` 格式，其中：
    - `<base64_data>`：图片文件的 Base64 编码字符串。
    - `<MIME_type>`：图片的媒体类型，必须与文件格式对应。

| **图片格式** | **MIME 类型** |
| -------- | ----------- |
| JPEG     | image/jpeg  |
| JPG      | image/jpeg  |
| PNG      | image/png   |
| BMP      | image/bmp   |
| WEBP     | image/webp  |
</Accordion>

#### 示例代码：三种输入方式

<CodeGroup>
  ```python Python SDK
  import base64
  import os
  from http import HTTPStatus
  from dashscope import VideoSynthesis
  import mimetypes
  import dashscope

  dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

  # 如果未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx"
  api_key = os.getenv("DASHSCOPE_API_KEY")

  # --- 辅助函数：用于 Base64 编码 ---
  # 格式：data:{MIME_type};base64,{base64_data}
  def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
      raise ValueError("不支持或无法识别的图片格式")
    with open(file_path, "rb") as image_file:
      encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

  """
  图片输入方式：
  从以下三种方式中选择一种：

  1. 使用公网 URL - 适用于可公开访问的图片
  2. 使用本地文件 - 适用于本地开发和测试
  3. 使用 Base64 编码 - 适用于私有图片或需要加密传输的场景
  """

  # [方式一] 使用可公开访问的图片 URL
  # 示例：使用公网图片 URL
  img_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"

  # [方式二] 使用本地文件（支持绝对路径和相对路径）
  # 格式要求：file:// + 文件路径
  # 示例（绝对路径）：
  # img_url = "file://" + "/path/to/your/img.png"    # Linux/macOS
  # img_url = "file://" + "/C:/path/to/your/img.png"  # Windows
  # 示例（相对路径）：
  # img_url = "file://" + "./img.png"                # 相对于当前可执行文件的路径

  # [方式三] 使用 Base64 编码的图片
  # img_url = encode_file("./img.png")

  # 设置音频 URL
  audio_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"

  def sample_call_i2v():
    # 同步调用，直接返回结果
    print('请稍候...')
    rsp = VideoSynthesis.call(api_key=api_key,
                                model='wan2.6-i2v-flash',
                                prompt='一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。',
                                img_url=img_url,
                                audio_url=audio_url,
                                resolution="720P",
                                duration=10,
                                prompt_extend=True,
                                watermark=False,
                                negative_prompt="",
                                seed=12345)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
      print("video_url:", rsp.output.video_url)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' %
                (rsp.status_code, rsp.code, rsp.message))

  if __name__ == '__main__':
    sample_call_i2v()
  ```

  ```java Java SDK
  // Copyright (c) Alibaba, Inc. and its affiliates.

  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
  import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
  import com.alibaba.dashscope.exception.ApiException;
  import com.alibaba.dashscope.exception.InputRequiredException;
  import com.alibaba.dashscope.exception.NoApiKeyException;
  import com.alibaba.dashscope.utils.JsonUtils;
  import com.alibaba.dashscope.utils.Constants;

  import java.io.IOException;
  import java.nio.file.Files;
  import java.nio.file.Path;
  import java.nio.file.Paths;
  import java.util.Base64;
  import java.util.HashMap;
  import java.util.Map;

  public class Image2Video {

    static {
      Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    }

    // 如果未配置环境变量，请将下行替换为您的 API Key：apiKey="sk-xxx"
    static String apiKey = System.getenv("DASHSCOPE_API_KEY");

    /**
       * 图片输入方式：从以下三种方式中选择一种
       *
       * 1. 使用公网 URL - 适用于可公开访问的图片
       * 2. 使用本地文件 - 适用于本地开发和测试
       * 3. 使用 Base64 编码 - 适用于私有图片或需要加密传输的场景
       */

    // [方式一] 公网 URL
    static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";

    // [方式二] 本地文件路径（file://+绝对路径）
    // static String imgUrl = "file://" + "/your/path/to/img.png";    // Linux/macOS
    // static String imgUrl = "file://" + "/C:/your/path/to/img.png";  // Windows

    // [方式三] Base64 编码
    // static String imgUrl = Image2Video.encodeFile("/your/path/to/img.png");

    // 设置音频 URL
    static String audioUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3";

    public static void image2video() throws ApiException, NoApiKeyException, InputRequiredException {
      // 设置参数
      Map<String, Object> parameters = new HashMap<>();
      parameters.put("prompt_extend", true);
      parameters.put("watermark", false);
      parameters.put("seed", 12345);

      VideoSynthesis vs = new VideoSynthesis();
      VideoSynthesisParam param =
          VideoSynthesisParam.builder()
              .apiKey(apiKey)
              .model("wan2.6-i2v-flash")
              .prompt("一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。")
              .imgUrl(imgUrl)
              .audioUrl(audioUrl)
              .duration(10)
              .parameters(parameters)
              .resolution("720P")
              .negativePrompt("")
              .build();
      System.out.println("请稍候...");
      VideoSynthesisResult result = vs.call(param);
      System.out.println(JsonUtils.toJson(result));
    }

       /**
       * 将文件编码为 Base64 字符串
       * @param filePath 文件路径
       * @return Base64 字符串，格式为：data:{MIME_type};base64,{base64_data}
       */
    public static String encodeFile(String filePath) {
      Path path = Paths.get(filePath);
      if (!Files.exists(path)) {
        throw new IllegalArgumentException("文件不存在：" + filePath);
      }
      // 检测 MIME 类型
      String mimeType = null;
      try {
        mimeType = Files.probeContentType(path);
      } catch (IOException e) {
        throw new IllegalArgumentException("无法检测文件类型：" + filePath);
      }
      if (mimeType == null || !mimeType.startsWith("image/")) {
        throw new IllegalArgumentException("不支持或无法识别的图片格式");
      }
      // 读取文件内容并编码
      byte[] fileBytes = null;
      try{
        fileBytes = Files.readAllBytes(path);
      } catch (IOException e) {
        throw new IllegalArgumentException("无法读取文件内容：" + filePath);
      }

      String encodedString = Base64.getEncoder().encodeToString(fileBytes);
      return "data:" + mimeType + ";base64," + encodedString;
    }

    public static void main(String[] args) {
      try {
        image2video();
      } catch (ApiException | NoApiKeyException | InputRequiredException e) {
        System.out.println(e.getMessage());
      }
      System.exit(0);
    }
  }
  ```
</CodeGroup>

### 输入音频

- **数量**：1 个。
- **输入方式**：仅支持**可公开访问的 URL**（HTTP 或 HTTPS），不支持本地文件路径和 Base64 编码。
- **音频文件限制**：
  - 格式：wav、mp3
  - 时长：3–30 秒
  - 文件大小：最大 15 MB
  - 如果音频时长超过视频时长，音频会被截断；如果音频较短，剩余部分的视频将保持静音。

## 输出视频

- **数量**：1 个。
- **输出视频规格**：输出规格因模型而异，请参见[视频生成模型](/developer-guides/getting-started/video-models#全部模型)。
- **输出视频 URL 有效期**：24 小时。
- **输出视频尺寸**：由输入图片和 `resolution` 设置共同决定。
  - 模型会尽量保持输入图片的宽高比，同时将总像素数缩放到接近目标值。由于视频编码标准要求宽度和高度必须是 16 的倍数，模型会自动对尺寸进行微调。
  - 例如，如果输入图片为 750 x 1000（宽高比 3:4 = 0.75），且设置 resolution = "720P"（目标像素数约 920,000），最终输出可能为 816 x 1104（宽高比约 0.739，总像素数约 900,000），其中宽度和高度均为 16 的倍数。

## 已知限制

使用 `wan2.6-i2v-flash` 生成圆形物体连续旋转（如圆环、齿轮、表盘）的动画时，画面在约 3 秒后可能出现短暂卡顿（画面静止约 1 秒）。如需生成此类连续旋转效果，建议改用 [Wan 2.7 图生视频](/api-reference/video-generation/wan27-image-to-video/create-task)模型以规避此问题。

## 计费与限流

- 免费额度和单价请参见[模型定价](/developer-guides/getting-started/pricing)。
- 限流信息请参见 [Wan 系列](/developer-guides/administration/rate-limits)。
- 计费说明：
  - 按成功生成的视频**时长（秒）** 计费。
  - 调用失败或处理出错不会产生费用，也不会消耗[新用户免费额度](/resources/free-quota)。

## API 参考

- [Wan 2.7 图生视频 API 参考](/api-reference/video-generation/wan27-image-to-video/create-task)
- [Wan 2.6 图生视频（首帧）API 参考](/api-reference/video-generation/wan-image-to-video-first-frame/create-task)

## 常见问题

### 为什么不能直接设置视频宽高比（如 16:9）？

当前 API 不支持直接指定视频宽高比。您只能通过 `resolution` 参数设置视频的分辨率。

`resolution` 参数控制的是视频的总像素数，而非固定的宽高比。模型会优先保持输入首帧图片的原始宽高比，并进行微调以满足视频编码要求（宽度和高度必须是 16 的倍数）。

### SDK 报错："url error, please check url!"

请确认：

- DashScope Python SDK 版本为 `1.25.8` 或更高版本。
- DashScope Java SDK 版本为 `2.22.6` 或更高版本。

如果 SDK 版本过低，可能会遇到 "url error, please check url!" 错误。有关升级 SDK 的信息，请参见[升级 SDK](/api-reference/preparation/install-sdk)。
