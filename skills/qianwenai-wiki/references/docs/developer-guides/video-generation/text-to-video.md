> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文生视频

> 通过文本生成视频

Wan 文生视频模型支持**多模态输入**（文本和音频），可生成最长 15 秒、最高 1080P 分辨率的视频。

- **核心能力**：支持整数时长（2-15 秒）、自定义视频分辨率（720P 或 1080P）、画面比例控制、提示词改写和水印功能。
- **音频能力**：支持自动配音或自定义音频文件，实现音画同步。**（wan2.5 及以上版本支持）**
- **多镜头叙事**：生成包含多个镜头的视频，同时保持主体在镜头切换间的一致性。**（wan2.6 和 wan2.7 支持）**

**快速入口**： [模型体验](https://platform.qianwenai.com/home/try-ai) **|** API 参考：[wan2.7](/api-reference/video-generation/wan27-text-to-video/create-task)、[wan2.6](/api-reference/video-generation/wan-text-to-video/create-task) **|** [提示词指南](/developer-guides/accuracy-tuning/video-generation)

## 快速开始

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingRight: "12px"}}>**输入提示词**</th>
    <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingLeft: "12px"}}>**输出视频（多镜头，带音频）**</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      一段紧张刺激的侦探追查故事，展现电影级叙事能力。第1个镜头\[0-3秒] 全景：雨夜的纽约街头，霓虹灯闪烁，一位身穿黑色风衣的侦探快步行走。第2个镜头\[3-6秒] 中景：侦探进入一栋老旧建筑，雨水打湿了他的外套，门在他身后缓缓关闭。第3个镜头\[6-9秒] 特写：侦探的眼神坚毅专注，远处传来警笛声，他微微皱眉思考。第4个镜头\[9-12秒] 中景：侦探在昏暗走廊中小心前行，手电筒照亮前方。第5个镜头\[12-15秒] 特写：侦探发现关键线索，脸上露出恍然大悟的表情。
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      <video style={{display: "block", width: "100%"}} src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260126/desnzy/wan-t2v-demo.mp4" controls />
    </td>
  </tr>
</table>

调用 API 前，请先[获取 API Key](/api-reference/preparation/api-key)，然后[将 API Key 设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 DashScope SDK](/api-reference/preparation/install-sdk)。

<Note>
  Wan 2.7 使用 `resolution` + `ratio` 代替 `size`，并在提示词中直接描述多镜头（无需 `shot_type` 参数）。
</Note>

**第 1 步：创建任务，获取 task ID**

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
  -H 'X-DashScope-Async: enable' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
  "model": "wan2.7-t2v-2026-06-12",
  "input": {
    "prompt": "一段紧张刺激的侦探追查故事，展现电影级叙事能力。第1个镜头[0-3秒] 全景：雨夜的纽约街头，霓虹灯闪烁，一位身穿黑色风衣的侦探快步行走。第2个镜头[3-6秒] 中景：侦探进入一栋老旧建筑，雨水打湿了他的外套，门在他身后缓缓关闭。第3个镜头[6-9秒] 特写：侦探的眼神坚毅专注，远处传来警笛声，他微微皱眉思考。第4个镜头[9-12秒] 中景：侦探在昏暗走廊中小心前行，手电筒照亮前方。第5个镜头[12-15秒] 特写：侦探发现关键线索，脸上露出恍然大悟的表情。"
  },
  "parameters": {
    "resolution": "1080P",
    "ratio": "16:9",
    "prompt_extend": true,
    "duration": 15
  }
}'
```

**第 2 步：通过 task ID 查询结果**

将 `task_id` 替换为上一步 API 返回的 `task_id` 值。

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<Accordion title="wan2.6 示例（Python SDK、Java SDK、curl）">
  如需使用 SDK，请先[安装 DashScope SDK](/api-reference/preparation/install-sdk)。

  <Tabs>
    <Tab title="Python SDK">
      <Warning>
        运行以下代码前，请确认 DashScope Python SDK 版本不低于 `1.25.8`。

        版本过低可能报错 "url error, please check url!"。[安装 SDK](/api-reference/preparation/install-sdk)。
      </Warning>

      ```python
      import os
      from http import HTTPStatus
      from dashscope import VideoSynthesis
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
      api_key = os.getenv("DASHSCOPE_API_KEY")  # 如果未设置环境变量，请将此行替换为：api_key="sk-xxx"

      print('please wait...')
      rsp = VideoSynthesis.call(api_key=api_key,
                                  model='wan2.6-t2v',
                                  prompt='一段紧张刺激的侦探追查故事，展现电影级叙事能力。第1个镜头[0-3秒] 全景：雨夜的纽约街头，霓虹灯闪烁，一位身穿黑色风衣的侦探快步行走。第2个镜头[3-6秒] 中景：侦探进入一栋老旧建筑，雨水打湿了他的外套，门在他身后缓缓关闭。第3个镜头[6-9秒] 特写：侦探的眼神坚毅专注，远处传来警笛声，他微微皱眉思考。第4个镜头[9-12秒] 中景：侦探在昏暗走廊中小心前行，手电筒照亮前方。第5个镜头[12-15秒] 特写：侦探发现关键线索，脸上露出恍然大悟的表情。',
                                  size="1280*720",
                                  duration=15,
                                  shot_type="multi",
                                  prompt_extend=True,
                                  watermark=True)
      print(rsp)
      if rsp.status_code == HTTPStatus.OK:
        print("video_url:", rsp.output.video_url)
      else:
        print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))
      ```
    </Tab>

    <Tab title="Java SDK">
      <Warning>
        运行以下代码前，请确认 DashScope Java SDK 版本不低于 `2.22.6`。

        版本过低可能报错 "url error, please check url!"。[安装 SDK](/api-reference/preparation/install-sdk)。
      </Warning>

      ```java
      import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
      import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
      import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.InputRequiredException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.utils.JsonUtils;
      import com.alibaba.dashscope.utils.Constants;

      public class Text2Video {

        static {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        }

        // 如果未设置环境变量，请将下面一行替换为：apiKey="sk-xxx"
        static String apiKey = System.getenv("DASHSCOPE_API_KEY");

        public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
          VideoSynthesis vs = new VideoSynthesis();
          VideoSynthesisParam param =
              VideoSynthesisParam.builder()
                  .apiKey(apiKey)
                  .model("wan2.6-t2v")
                  .prompt("一段紧张刺激的侦探追查故事，展现电影级叙事能力。第1个镜头[0-3秒] 全景：雨夜的纽约街头，霓虹灯闪烁，一位身穿黑色风衣的侦探快步行走。第2个镜头[3-6秒] 中景：侦探进入一栋老旧建筑，雨水打湿了他的外套，门在他身后缓缓关闭。第3个镜头[6-9秒] 特写：侦探的眼神坚毅专注，远处传来警笛声，他微微皱眉思考。第4个镜头[9-12秒] 中景：侦探在昏暗走廊中小心前行，手电筒照亮前方。第5个镜头[12-15秒] 特写：侦探发现关键线索，脸上露出恍然大悟的表情。")
                  .duration(15)
                  .size("1280*720")
                  .shotType("multi")
                  .promptExtend(true)
                  .watermark(true)
                  .build();
          System.out.println("please wait...");
          VideoSynthesisResult result = vs.call(param);
          System.out.println(JsonUtils.toJson(result));
        }

        public static void main(String[] args) {
          try {
            text2Video();
          } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.out.println(e.getMessage());
          }
          System.exit(0);
        }
      }
      ```
    </Tab>

    <Tab title="curl">
      **第 1 步：创建任务，获取 task ID**

      ```bash
      curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
        -H 'X-DashScope-Async: enable' \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H 'Content-Type: application/json' \
        -d '{
        "model": "wan2.6-t2v",
        "input": {
          "prompt": "一段紧张刺激的侦探追查故事，展现电影级叙事能力。第1个镜头[0-3秒] 全景：雨夜的纽约街头，霓虹灯闪烁，一位身穿黑色风衣的侦探快步行走。第2个镜头[3-6秒] 中景：侦探进入一栋老旧建筑，雨水打湿了他的外套，门在他身后缓缓关闭。第3个镜头[6-9秒] 特写：侦探的眼神坚毅专注，远处传来警笛声，他微微皱眉思考。第4个镜头[9-12秒] 中景：侦探在昏暗走廊中小心前行，手电筒照亮前方。第5个镜头[12-15秒] 特写：侦探发现关键线索，脸上露出恍然大悟的表情。"
        },
        "parameters": {
          "size": "1280*720",
          "prompt_extend": true,
          "watermark": true,
          "duration": 15,
          "shot_type":"multi"
        }
      }'
      ```

      **第 2 步：通过 task ID 查询结果**

      将 `task_id` 替换为上一步 API 返回的 `task_id` 值。

      ```bash
      curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY"
      ```
    </Tab>
  </Tabs>
</Accordion>

**输出示例**

<Note>
  `video_url` 有效期为 24 小时，请及时下载视频。
</Note>

```json
{
  "request_id": "c1209113-8437-424f-a386-xxxxxx",
  "output": {
    "task_id": "966cebcd-dedc-4962-af88-xxxxxx",
    "task_status": "SUCCEEDED",
    "video_url": "https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx",
         ...
  },
  ...
}
```

## 核心能力

### 多镜头视频

**支持模型**：`wan2.7`、`wan2.6 系列`。

**说明**：模型会自动切换镜头（例如从全景切换到特写），适用于音乐 MV 等场景。

**参数说明**：

- **wan2.7**：在提示词中直接描述镜头（如 `Shot 1 [0-3 s]: ...`），无需 `shot_type` 参数。
- **wan2.6**：将 `shot_type` 设为 `"multi"`。
- `prompt_extend`：设为 `true`（启用提示词改写以优化镜头描述）。

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingRight: "12px"}}>**输入提示词**</th>
    <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingLeft: "12px"}}>**输出视频（多镜头视频）**</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      展现未来科技与自然和谐共存的美好愿景。第1个镜头\[0-2秒] 未来城市的空中花园全景，悬浮植物在微风中摇曳。第2个镜头\[2-4秒] 机器人园丁正在精心修剪植物，动作精准而优雅。第3个镜头\[4-7秒] 阳光透过透明穹顶洒下，照亮整个花园，展现科技与自然的完美融合。第4个镜头\[7-10秒] 镜头拉远，展现整个未来城市的壮观景象，空中花园只是其中的一部分。
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      <video style={{display: "block", width: "100%"}} src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260126/bczhoy/wan-i2v-video-multi.mp4" controls />
    </td>
  </tr>
</table>

<Tabs>
  <Tab title="Python SDK">
    <Note>
      请确认 DashScope Python SDK 版本不低于 `1.25.8`。[安装 SDK](/api-reference/preparation/install-sdk)。
    </Note>

    ```python
    import os
    from http import HTTPStatus
    from dashscope import VideoSynthesis
    import dashscope

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    # 如果未设置环境变量，请将下面一行替换为：api_key="sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")

    def sample_async_call_t2v():
      # 异步调用，返回 task_id
      rsp = VideoSynthesis.async_call(api_key=api_key,
                      model='wan2.6-t2v',
                      prompt='展现未来科技与自然和谐共存的美好愿景。第1个镜头[0-2秒] 未来城市的空中花园全景，悬浮植物在微风中摇曳。第2个镜头[2-4秒] 机器人园丁正在精心修剪植物，动作精准而优雅。第3个镜头[4-7秒] 阳光透过透明穹顶洒下，照亮整个花园，展现科技与自然的完美融合。第4个镜头[7-10秒] 镜头拉远，展现整个未来城市的壮观景象，空中花园只是其中的一部分。',
                      size='1280*720',
                      shot_type="multi",  # 多镜头
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
      sample_async_call_t2v()
    ```
  </Tab>

  <Tab title="Java SDK">
    <Note>
      请确认 DashScope Java SDK 版本不低于 `2.22.6`。[安装 SDK](/api-reference/preparation/install-sdk)。
    </Note>

    ```java
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.InputRequiredException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.alibaba.dashscope.utils.JsonUtils;
    import com.alibaba.dashscope.utils.Constants;

    public class Text2Video {
      static {
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
      }

      // 如果未设置环境变量，请将下面一行替换为：apiKey="sk-xxx"
      static String apiKey = System.getenv("DASHSCOPE_API_KEY");

      public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
            VideoSynthesisParam.builder()
                .apiKey(apiKey)
                .model("wan2.6-t2v")
                .prompt("展现未来科技与自然和谐共存的美好愿景。第1个镜头[0-2秒] 未来城市的空中花园全景，悬浮植物在微风中摇曳。第2个镜头[2-4秒] 机器人园丁正在精心修剪植物，动作精准而优雅。第3个镜头[4-7秒] 阳光透过透明穹顶洒下，照亮整个花园，展现科技与自然的完美融合。第4个镜头[7-10秒] 镜头拉远，展现整个未来城市的壮观景象，空中花园只是其中的一部分。")
                .negativePrompt("")
                .size("1280*720")
                .shotType("multi")
                .duration(10)
                .promptExtend(true)
                .watermark(true)
                .seed(12345)
                .build();
        // 异步调用
        VideoSynthesisResult task = vs.asyncCall(param);
        System.out.println(JsonUtils.toJson(task));
        System.out.println("please wait...");

        // 获取结果
        VideoSynthesisResult result = vs.wait(task, apiKey);
        System.out.println(JsonUtils.toJson(result));
      }

      public static void main(String[] args) {
        try {
          text2Video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
          System.out.println(e.getMessage());
        }
        System.exit(0);
      }
    }
    ```
  </Tab>

  <Tab title="curl">
    **第 1 步：创建任务，获取 task ID**

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.6-t2v",
      "input": {
        "prompt": "展现未来科技与自然和谐共存的美好愿景。第1个镜头[0-2秒] 未来城市的空中花园全景，悬浮植物在微风中摇曳。第2个镜头[2-4秒] 机器人园丁正在精心修剪植物，动作精准而优雅。第3个镜头[4-7秒] 阳光透过透明穹顶洒下，照亮整个花园，展现科技与自然的完美融合。第4个镜头[7-10秒] 镜头拉远，展现整个未来城市的壮观景象，空中花园只是其中的一部分。"
      },
      "parameters": {
        "size": "1280*720",
        "prompt_extend": true,
        "duration": 10,
        "shot_type":"multi"
      }
    }'
    ```

    **第 2 步：通过 task ID 查询结果**

    将 `task_id` 替换为上一步 API 返回的 `task_id` 值。

    ```bash
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>
</Tabs>

### 音画同步

**支持模型**：`wan2.7`、`wan2.6 系列`、`wan2.5 系列`。

**说明**：让画面中的角色说话或唱歌，口型与音频精确匹配。更多示例请参阅[视频生成音频指南](/developer-guides/accuracy-tuning/video-generation)。

**参数说明**：

- **传入音频文件**：通过 `audio_url` 传入音频，模型将口型与音频对齐。
- **自动配音**：默认生成带音频的视频，无需传入 `audio_url`。模型会根据场景自动生成背景音效、音乐或人声。

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingRight: "12px"}}>**输入示例**</th>
    <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingLeft: "12px"}}>**输出视频（带音频视频）**</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <strong>输入提示词</strong>: Shot from a low angle, in a medium close-up, with warm tones, mixed lighting (the practical light from the desk lamp blends with the overcast light from the window), side lighting, and a central composition. In a classic detective office, wooden bookshelves are filled with old case files and ashtrays. A green desk lamp illuminates a case file spread out in the center of the desk. A fox, wearing a dark brown trench coat and a light gray fedora, sits in a leather chair, its fur crimson, its tail resting lightly on the edge, its fingers slowly turning yellowed pages. Outside, a steady drizzle falls beneath a blue sky, streaking the glass with meandering streaks. It slowly raises its head, its ears twitching slightly, its amber eyes gazing directly at the camera, its mouth clearly moving as it speaks in a smooth, cynical voice: <strong>'The case was cold, colder than a fish in winter. But every chicken has its secrets, and I, for one, intended to find them '</strong>. <strong>输入音频</strong>: <audio style={{width: "100%"}} src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250929/ajcbjm/%E7%8B%90%E7%8B%B8.mp3" controls />
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      <video style={{display: "block", width: "100%"}} src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251218/yqyrak/wan2.6-intl+%281%29.mp4" controls />
    </td>
  </tr>
</table>

<Tabs>
  <Tab title="Python SDK">
    <Note>
      请确认 DashScope Python SDK 版本不低于 `1.25.8`。[安装 SDK](/api-reference/preparation/install-sdk)。
    </Note>

    ```python
    import os
    from http import HTTPStatus
    from dashscope import VideoSynthesis
    import dashscope

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    # 如果未设置环境变量，请将下面一行替换为：api_key="sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")

    def sample_async_call_t2v():
      # 异步调用，返回 task_id
      rsp = VideoSynthesis.async_call(api_key=api_key,
                      model='wan2.6-t2v',
                      prompt="Shot from a low angle, in a medium close-up, with warm tones, mixed lighting (the practical light from the desk lamp blends with the overcast light from the window), side lighting, and a central composition. In a classic detective office, wooden bookshelves are filled with old case files and ashtrays. A green desk lamp illuminates a case file spread out in the center of the desk. A fox, wearing a dark brown trench coat and a light gray fedora, sits in a leather chair, its fur crimson, its tail resting lightly on the edge, its fingers slowly turning yellowed pages. Outside, a steady drizzle falls beneath a blue sky, streaking the glass with meandering streaks. It slowly raises its head, its ears twitching slightly, its amber eyes gazing directly at the camera, its mouth clearly moving as it speaks in a smooth, cynical voice: 'The case was cold, colder than a fish in winter. But every chicken has its secrets, and I, for one, intended to find them '.",
                      audio_url='https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250929/stjqnq/%E7%8B%90%E7%8B%B8.mp3',
                      size='1280*720',
                      duration=10,
                      shot_type="multi",  # 多镜头
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
      sample_async_call_t2v()
    ```
  </Tab>

  <Tab title="Java SDK">
    <Note>
      请确认 DashScope Java SDK 版本不低于 `2.22.6`。[安装 SDK](/api-reference/preparation/install-sdk)。
    </Note>

    ```java
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.InputRequiredException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.alibaba.dashscope.utils.JsonUtils;
    import com.alibaba.dashscope.utils.Constants;

    public class Text2Video {
      static {
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
      }

      // 如果未设置环境变量，请将下面一行替换为：apiKey="sk-xxx"
      static String apiKey = System.getenv("DASHSCOPE_API_KEY");

      public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
            VideoSynthesisParam.builder()
                .apiKey(apiKey)
                .model("wan2.6-t2v")
                .prompt("Shot from a low angle, in a medium close-up, with warm tones, mixed lighting (the practical light from the desk lamp blends with the overcast light from the window), side lighting, and a central composition. In a classic detective office, wooden bookshelves are filled with old case files and ashtrays. A green desk lamp illuminates a case file spread out in the center of the desk. A fox, wearing a dark brown trench coat and a light gray fedora, sits in a leather chair, its fur crimson, its tail resting lightly on the edge, its fingers slowly turning yellowed pages. Outside, a steady drizzle falls beneath a blue sky, streaking the glass with meandering streaks. It slowly raises its head, its ears twitching slightly, its amber eyes gazing directly at the camera, its mouth clearly moving as it speaks in a smooth, cynical voice: 'The case was cold, colder than a fish in winter. But every chicken has its secrets, and I, for one, intended to find them '.")
                .audioUrl("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250929/stjqnq/%E7%8B%90%E7%8B%B8.mp3")
                .negativePrompt("")
                .size("1280*720")
                .shotType("multi")
                .duration(10)
                .promptExtend(true)
                .watermark(true)
                .seed(12345)
                .build();
        // 异步调用
        VideoSynthesisResult task = vs.asyncCall(param);
        System.out.println(JsonUtils.toJson(task));
        System.out.println("please wait...");

        // 获取结果
        VideoSynthesisResult result = vs.wait(task, apiKey);
        System.out.println(JsonUtils.toJson(result));
      }

      public static void main(String[] args) {
        try {
          text2Video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
          System.out.println(e.getMessage());
        }
        System.exit(0);
      }
    }
    ```
  </Tab>

  <Tab title="curl">
    **第 1 步：创建任务，获取 task ID**

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.6-t2v",
      "input": {
        "prompt": "Shot from a low angle, in a medium close-up, with warm tones, mixed lighting (the practical light from the desk lamp blends with the overcast light from the window), side lighting, and a central composition. In a classic detective office, wooden bookshelves are filled with old case files and ashtrays. A green desk lamp illuminates a case file spread out in the center of the desk. A fox, wearing a dark brown trench coat and a light gray fedora, sits in a leather chair, its fur crimson, its tail resting lightly on the edge, its fingers slowly turning yellowed pages. Outside, a steady drizzle falls beneath a blue sky, streaking the glass with meandering streaks. It slowly raises its head, its ears twitching slightly, its amber eyes gazing directly at the camera, its mouth clearly moving as it speaks in a smooth, cynical voice: \"The case was cold, colder than a fish in winter. But every chicken has its secrets, and I, for one, intended to find them \". ",
        "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250929/stjqnq/%E7%8B%90%E7%8B%B8.mp3"
      },
      "parameters": {
        "size": "1280*720",
        "prompt_extend": true,
        "duration": 10,
        "shot_type":"multi"
      }
    }'
    ```

    **第 2 步：通过 task ID 查询结果**

    将 `task_id` 替换为上一步 API 返回的 `task_id` 值。

    ```bash
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>
</Tabs>

### 生成无声视频

**支持模型**：`wan2.2 系列`、`wan2.1 系列`。

**说明**：适用于动态海报、无声短视频等纯视觉场景。

**参数说明**：wan2.2 及更早版本默认输出无声视频，无需额外配置。

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingRight: "12px"}}>**输入提示词**</th>
    <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingLeft: "12px"}}>**输出视频（无声视频）**</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      低对比度，在一个复古的70年代风格地铁站里，街头音乐家在昏暗的色彩和粗糙的质感中演奏。他穿着旧式夹克，手持吉他，专注地弹奏。通勤者匆匆走过，一小群人渐渐聚拢聆听。镜头慢慢向右移动，捕捉到乐器声与城市喧嚣交织的场景，背景中有老式的地铁标志和斑驳的墙面。
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      <video style={{display: "block", width: "100%"}} src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250806/sxjvix/text2video.mp4" controls />
    </td>
  </tr>
</table>

<Tabs>
  <Tab title="Python SDK">
    <Note>
      请确认 DashScope Python SDK 版本不低于 `1.25.8`。[安装 SDK](/api-reference/preparation/install-sdk)。
    </Note>

    ```python
    import os
    from http import HTTPStatus
    from dashscope import VideoSynthesis
    import dashscope

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    # 如果未设置环境变量，请将下面一行替换为：api_key="sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")

    def sample_async_call_t2v():
      # 异步调用，返回 task_id
      rsp = VideoSynthesis.async_call(api_key=api_key,
                      model='wan2.2-t2v-plus',
                      prompt='低对比度，在一个复古的70年代风格地铁站里，街头音乐家在昏暗的色彩和粗糙的质感中演奏。他穿着旧式夹克，手持吉他，专注地弹奏。通勤者匆匆走过，一小群人渐渐聚拢聆听。镜头慢慢向右移动，捕捉到乐器声与城市喧嚣交织的场景，背景中有老式的地铁标志和斑驳的墙面。',
                      prompt_extend=True,
                      size='832*480',
                      negative_prompt="",
                      watermark=True,
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
      sample_async_call_t2v()
    ```
  </Tab>

  <Tab title="Java SDK">
    <Note>
      请确认 DashScope Java SDK 版本不低于 `2.22.6`。[安装 SDK](/api-reference/preparation/install-sdk)。
    </Note>

    ```java
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
    import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.InputRequiredException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.alibaba.dashscope.utils.JsonUtils;
    import com.alibaba.dashscope.utils.Constants;

    public class Text2Video {
      static {
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
      }

      // 如果未设置环境变量，请将下面一行替换为：apiKey="sk-xxx"
      static String apiKey = System.getenv("DASHSCOPE_API_KEY");

      public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
        VideoSynthesis vs = new VideoSynthesis();
        VideoSynthesisParam param =
            VideoSynthesisParam.builder()
                .apiKey(apiKey)
                .model("wan2.2-t2v-plus")
                .prompt("低对比度，在一个复古的70年代风格地铁站里，街头音乐家在昏暗的色彩和粗糙的质感中演奏。他穿着旧式夹克，手持吉他，专注地弹奏。通勤者匆匆走过，一小群人渐渐聚拢聆听。镜头慢慢向右移动，捕捉到乐器声与城市喧嚣交织的场景，背景中有老式的地铁标志和斑驳的墙面。")
                .size("832*480")
                .promptExtend(true)
                .watermark(true)
                .seed(12345)
                .build();
        // 异步调用
        VideoSynthesisResult task = vs.asyncCall(param);
        System.out.println(JsonUtils.toJson(task));
        System.out.println("please wait...");

        // 获取结果
        VideoSynthesisResult result = vs.wait(task, apiKey);
        System.out.println(JsonUtils.toJson(result));
      }

      public static void main(String[] args) {
        try {
          text2Video();
        } catch (ApiException | NoApiKeyException | InputRequiredException e) {
          System.out.println(e.getMessage());
        }
        System.exit(0);
      }
    }
    ```
  </Tab>

  <Tab title="curl">
    **第 1 步：创建任务，获取 task ID**

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wan2.2-t2v-plus",
      "input": {
        "prompt": "低对比度，在一个复古的70年代风格地铁站里，街头音乐家在昏暗的色彩和粗糙的质感中演奏。他穿着旧式夹克，手持吉他，专注地弹奏。通勤者匆匆走过，一小群人渐渐聚拢聆听。镜头慢慢向右移动，捕捉到乐器声与城市喧嚣交织的场景，背景中有老式的地铁标志和斑驳的墙面。"
      },
      "parameters": {
        "size": "832*480",
        "prompt_extend": true,
        "watermark": true
      }
    }'
    ```

    **第 2 步：通过 task ID 查询结果**

    将 `task_id` 替换为上一步 API 返回的 `task_id` 值。

    ```bash
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>
</Tabs>

## 输入音频

- **文件数量**：1 个。
- **输入方式**：
  - **公网 URL**：支持 HTTP 或 HTTPS 协议。

## 输出视频

- **文件数量**：1 个。
- **格式**：MP4。各模型的输出规格详见[视频生成模型](/developer-guides/getting-started/video-models#全部模型)。
- **URL 有效期**：24 小时。
- **分辨率设置**：
  - **wan2.7**：通过 `resolution` 和 `ratio` 设置。例如 `resolution=1080P` + `ratio=16:9` 输出 **1920x1080** 视频。
  - **wan2.6 及更早版本**：通过 `size` 参数设置。例如 `size=1280*720` 输出 **16:9** 视频。

## 计费与限流

- 免费额度和定价详情，请参阅[模型调用计费](/developer-guides/getting-started/pricing)。
- 模型限流信息，请参阅[限流](/developer-guides/administration/rate-limits)。
- 计费说明：
  - 输入免费，输出按成功生成的**视频秒数**计费。
  - 模型调用失败或处理出错不计费，也不消耗[免费额度](/resources/free-quota)。

## API 参考

- [Wan 2.7 文生视频 API 参考](/api-reference/video-generation/wan27-text-to-video/create-task)
- [Wan 2.6 文生视频 API 参考](/api-reference/video-generation/wan-text-to-video/create-task)

## 常见问题

### 如何设置视频画面比例（例如 16:9）？

**wan2.7**：直接使用 `ratio` 参数（如 `"16:9"`、`"9:16"`、`"1:1"`、`"4:3"`、`"3:4"`），配合 `resolution`（`"720P"` 或 `"1080P"`）使用。

**wan2.6 及更早版本**：通过 `size` 参数指定视频分辨率（像素），系统自动计算画面比例。例如 `size=1280*720` 输出 **16:9** 视频。

### SDK 报错："url error, please check url!"

请检查以下事项：

- DashScope Python SDK 版本是否不低于 `1.25.8`。
- DashScope Java SDK 版本是否不低于 `2.22.6`。

版本过低会出现 "url error, please check url!" 错误。[升级 SDK](/api-reference/preparation/install-sdk)。

### 调用失败，提示 "Model not exist"？

请排查以下问题：

- 模型名称是否拼写正确？

支持的模型列表请参阅[视频生成模型](/developer-guides/getting-started/video-models)。
