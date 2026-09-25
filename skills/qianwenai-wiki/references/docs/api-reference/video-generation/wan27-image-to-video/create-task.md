> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.7 — 创建任务

> 提交图生视频任务（wan2.7）

支持从图片、音频和视频片段生成最长 15 秒、最高 1080P 分辨率的视频，可选音频同步和首末帧控制。

## 与 wan2.6 的区别

- **统一 API**：首帧、首末帧、视频续写共用同一接口，通过 `media` 数组区分，无需调用不同 API。
- **音视频同步**：提供 `driving_audio` 文件可实现口型同步；未提供时，模型自动生成匹配的音效。
- **分辨率控制**：通过 `resolution`（720P/1080P）设置分辨率，取代原来的像素级 `size` 参数。
- **更长提示词**：最多支持 5,000 字符（原为 800）。
- **负向提示词位置调整**：移至 `input.negative_prompt`，不再使用 `parameters.negative_prompt`。
- **水印默认关闭**：`watermark` 默认为 `false`（原为 `true`）。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: Wan 2.7 图像转视频 API
  description: 基于 Wan 2.7 模型，从图片、音频和视频片段生成视频。以异步方式提交任务，然后通过 `GET /tasks/{task_id}` 轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createWan27ImageToVideo
      summary: 创建图像转视频任务
      description: 提交图像转视频任务，返回用于轮询的 `task_id`。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 必须设置为 `enable`，表示以异步方式提交任务。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Wan27ImageToVideoRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 首帧 + 音频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.7-i2v",
              "input": {
                "prompt": "A scene of urban fantasy art. A dynamic graffiti art character. A boy made of spray paint comes to life on a concrete wall. He sings an English rap song at high speed while striking a classic, energetic rapper pose. The scene is set under an urban railway bridge at night. The light comes from a single street lamp, creating a cinematic atmosphere full of high energy and amazing detail. The audio of the video consists entirely of the rap, with no other dialogue or noise.",
                "media": [
                  {
                    "type": "first_frame",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
                  },
                  {
                    "type": "driving_audio",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
                  }
                ]
              },
              "parameters": {
                "resolution": "720P",
                "duration": 10,
                "prompt_extend": true,
                "watermark": true
              }
            }'
        - lang: curl
          label: cURL - 首帧与尾帧
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.7-i2v",
              "input": {
                "prompt": "Realistic style, a small black cat looks up at the sky curiously. The camera angle gradually rises from eye level, finally capturing its curious gaze from a top-down view.",
                "media": [
                  {
                    "type": "first_frame",
                    "url": "https://wanx.alicdn.com/material/20250318/first_frame.png"
                  },
                  {
                    "type": "last_frame",
                    "url": "https://wanx.alicdn.com/material/20250318/last_frame.png"
                  }
                ]
              },
              "parameters": {
                "resolution": "720P",
                "duration": 10,
                "prompt_extend": false,
                "watermark": true
              }
            }'
        - lang: curl
          label: cURL - 视频续生
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.7-i2v",
              "input": {
                "prompt": "A girl takes a selfie in the mirror, then leaves with her backpack.",
                "media": [
                  {
                    "type": "first_clip",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4"
                  }
                ]
              },
              "parameters": {
                "resolution": "720P",
                "duration": 10,
                "prompt_extend": true,
                "watermark": true
              }
            }'
        - lang: python
          label: Python - 同步调用
          source: |-
            # -*- coding: utf-8 -*-
            from http import HTTPStatus
            from dashscope import VideoSynthesis
            import dashscope
            import os
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            # 若没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
            api_key = os.getenv("DASHSCOPE_API_KEY")
            media = [
                {
                    "type": "first_frame",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
                },
                {
                    "type": "driving_audio",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
                }
            ]
            def sample_sync_call():
                print('----sync call, please wait a moment----')
                rsp = VideoSynthesis.call(
                    api_key=api_key,
                    model="wan2.7-i2v-2026-04-25",
                    media=media,
                    resolution="720P",
                    duration=10,
                    watermark=True,
                    prompt="一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。",
                )
                if rsp.status_code == HTTPStatus.OK:
                    print(rsp.output.video_url)
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))
            if __name__ == '__main__':
                sample_sync_call()
        - lang: python
          label: Python - 异步调用
          source: |-
            # -*- coding: utf-8 -*-
            from http import HTTPStatus
            from dashscope import VideoSynthesis
            import dashscope
            import os
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            # 若没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
            api_key = os.getenv("DASHSCOPE_API_KEY")
            media = [
                {
                    "type": "first_frame",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
                },
                {
                    "type": "driving_audio",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
                }
            ]
            def sample_async_call():
                # 提交异步任务，立即返回任务信息
                rsp = VideoSynthesis.async_call(
                    api_key=api_key,
                    model="wan2.7-i2v-2026-04-25",
                    media=media,
                    resolution="720P",
                    duration=10,
                    watermark=True,
                    prompt="一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。",
                )
                print(rsp)
                if rsp.status_code == HTTPStatus.OK:
                    print("task_id: %s" % rsp.output.task_id)
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))
                # 查询任务状态
                status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
                if status.status_code == HTTPStatus.OK:
                    print(status.output.task_status)
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (status.status_code, status.code, status.message))
                # 等待任务完成
                rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
                print(rsp)
                if rsp.status_code == HTTPStatus.OK:
                    print(rsp.output.video_url)
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))
            if __name__ == '__main__':
                sample_async_call()
        - lang: java
          label: Java - 同步调用
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;
            import java.util.ArrayList;
            import java.util.List;
            public class Image2Video {
                static {
                            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                }
                // 若没有配置环境变量，请用API Key将下行替换为：apiKey="sk-xxx"
                    static String apiKey = System.getenv("DASHSCOPE_API_KEY");
                public static void syncCall() {
                    VideoSynthesis videoSynthesis = new VideoSynthesis();
                    final String prompt = "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。";
                    List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png")
                                .type("first_frame")
                                .build());
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3")
                                .type("driving_audio")
                                .build());
                    }};
                    VideoSynthesisParam param =
                            VideoSynthesisParam.builder()
                                    .apiKey(apiKey)
                                    .model("wan2.7-i2v-2026-04-25")
                                    .prompt(prompt)
                                    .media(media)
                                    .watermark(true)
                                    .duration(10)
                                    .resolution("720P")
                                    .build();
                    VideoSynthesisResult result = null;
                    try {
                        System.out.println("---sync call, please wait a moment----");
                        result = videoSynthesis.call(param);
                    } catch (ApiException | NoApiKeyException e){
                        throw new RuntimeException(e.getMessage());
                    } catch (InputRequiredException e) {
                        throw new RuntimeException(e);
                    }
                    System.out.println(JsonUtils.toJson(result));
                }
                public static void main(String[] args) {
                    syncCall();
                }
            }
        - lang: java
          label: Java - 异步调用
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;
            import java.util.ArrayList;
            import java.util.List;
            public class Image2Video {
                static {
                            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                }
                // 若没有配置环境变量，请用API Key将下行替换为：apiKey="sk-xxx"
                    static String apiKey = System.getenv("DASHSCOPE_API_KEY");
                public static void asyncCall() {
                    VideoSynthesis videoSynthesis = new VideoSynthesis();
                    final String prompt = "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由他的rap构成，没有其他对话或杂音。";
                    List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png")
                                .type("first_frame")
                                .build());
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3")
                                .type("driving_audio")
                                .build());
                    }};
                    VideoSynthesisParam param =
                            VideoSynthesisParam.builder()
                                    .apiKey(apiKey)
                                    .model("wan2.7-i2v-2026-04-25")
                                    .prompt(prompt)
                                    .media(media)
                                    .watermark(true)
                                    .duration(10)
                                    .resolution("720P")
                                    .build();
                    VideoSynthesisResult result = null;
                    try {
                        System.out.println("---async call, please wait a moment----");
                        result = videoSynthesis.asyncCall(param);
                    } catch (ApiException | NoApiKeyException e){
                        throw new RuntimeException(e.getMessage());
                    } catch (InputRequiredException e) {
                        throw new RuntimeException(e);
                    }
                    System.out.println(JsonUtils.toJson(result));
                    String taskId = result.getOutput().getTaskId();
                    System.out.println("taskId=" + taskId);
                    try {
                        result = videoSynthesis.wait(taskId, apiKey);
                    } catch (ApiException | NoApiKeyException e){
                        throw new RuntimeException(e.getMessage());
                    }
                    System.out.println(JsonUtils.toJson(result));
                    System.out.println(JsonUtils.toJson(result.getOutput()));
                }
                public static void main(String[] args) {
                    asyncCall();
                }
            }
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan27ImageToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型标识符。可选值：`wan2.7-i2v`（主线版本，持续更新）、`wan2.7-i2v-2026-04-25`（快照版本，能力与主线一致）。
          enum:
            - wan2.7-i2v
            - wan2.7-i2v-2026-04-25
          example: wan2.7-i2v
        input:
          type: object
          required:
            - media
          description: 视频生成的输入数据。
          properties:
            prompt:
              type: string
              description: 描述希望生成的视频内容，支持中英文，最多 5,000 个字符（超出自动截断）。
              example: A kitten runs on the grass.
            negative_prompt:
              type: string
              description: 描述不希望出现在视频中的内容（如 `低质量、模糊、多余手指`），支持中英文，最多 500 个字符（超出自动截断）。
              example: low resolution, error, worst quality, low quality, deformed, extra fingers, bad proportions
            media:
              type: array
              description: |-
                视频生成所需的参考素材，每个元素指定 `type` 和 `url`，每种 `type` 最多出现一次。

                支持的组合：
                - `first_frame`
                - `first_frame` + `driving_audio`
                - `first_frame` + `last_frame`
                - `first_frame` + `last_frame` + `driving_audio`
                - `first_clip`
                - `first_clip` + `last_frame`
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    description: |-
                      素材类型。

                      - `first_frame`：首帧图片，支持 JPEG/JPG/PNG/BMP/WEBP，每边 240-8000 px，宽高比 1:8 至 8:1，最大 20 MB。
                      - `last_frame`：尾帧图片，限制与 `first_frame` 相同。
                      - `driving_audio`：用于口型同步或语音驱动动画的音频，支持 WAV/MP3，时长 2-30 秒，最大 15 MB。若不提供，模型将自动生成配套音效。
                      - `first_clip`：用于续生的输入视频，支持 MP4/MOV，时长 2-10 秒，每边 240-4096 px，宽高比 1:8 至 8:1，最大 100 MB。
                    enum:
                      - first_frame
                      - last_frame
                      - driving_audio
                      - first_clip
                  url:
                    type: string
                    format: uri
                    description: 素材的公开访问 URL（HTTP/HTTPS）。
        parameters:
          $ref: "#/components/schemas/Wan27ImageToVideoParameters"
    Wan27ImageToVideoParameters:
      type: object
      description: 视频生成参数。
      properties:
        resolution:
          type: string
          description: 视频清晰度档位。模型会自动缩放输出分辨率并保持输入素材的宽高比，分辨率越高费用越高。
          enum:
            - 720P
            - 1080P
          default: 1080P
        duration:
          type: integer
          description: 视频时长（秒），取整数，范围 2-15，时长越长费用越高，按秒计费。对于视频续生（`first_clip`），此参数为包含输入片段的总输出时长。例如，若 `duration=15` 而输入视频为 3 秒，则模型将生成 12 秒的新内容。
          minimum: 2
          maximum: 15
          default: 5
        prompt_extend:
          type: boolean
          description: 在生成前使用大语言模型对提示词进行扩写优化，适合简短或模糊的提示词，但会增加耗时。设置为 `false` 则按原始提示词生成。
          default: true
        watermark:
          type: boolean
          description: 在视频右下角添加 "AI 生成" 水印。
          default: false
        seed:
          type: integer
          description: 随机种子，用于生成可复现的结果。相同种子和参数会产生相似（但不完全相同）的输出。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应结果。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符，用于追踪和排查问题。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 用于轮询任务状态的任务 ID，配合 `GET /tasks/{task_id}` 使用。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务的初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    Wan27I2VTaskStatusResponse:
      type: object
      description: wan2.7 图像转视频任务的状态响应。
      properties:
        request_id:
          type: string
          description: 请求 ID，用于排查问题。联系支持时请提供此 ID。
          example: 2ca1c497-f9e0-449d-9a3f-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，提交后 24 小时内可查询。
              example: af6efbc0-4bef-4194-8246-xxxxxx
            task_status:
              type: string
              description: 任务生命周期：`PENDING` → `RUNNING` → `SUCCEEDED` 或 `FAILED`。主动停止时为 `CANCELED`，过期后为 `UNKNOWN`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`）。
              example: 2025-09-25 11:07:28.590
            scheduled_time:
              type: string
              description: 任务开始执行时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`）。
              example: 2025-09-25 11:07:35.349
            end_time:
              type: string
              description: 任务结束时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`），仅在 `SUCCEEDED` 或 `FAILED` 状态下出现。
              example: 2025-09-25 11:17:11.650
            orig_prompt:
              type: string
              description: 原始提示词文本，对应请求参数 `prompt`。
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL（MP4，H.264 编码），仅在 `task_status` 为 `SUCCEEDED` 时出现。**有效期 24 小时**，请及时下载。
              example: https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx
            code:
              type: string
              description: 错误码，仅在 `task_status` 为 `FAILED` 时出现。
            message:
              type: string
              description: 错误信息，仅在 `task_status` 为 `FAILED` 时出现。
        usage:
          type: object
          description: 资源消耗信息，仅在 `task_status` 为 `SUCCEEDED` 时出现。
          properties:
            duration:
              type: integer
              description: 计费视频时长（秒）。
            input_video_duration:
              type: integer
              description: 输入视频时长（秒），首帧任务时为 `0`。
            output_video_duration:
              type: integer
              description: 输出视频时长（秒）。
            video_count:
              type: integer
              description: 生成的视频数量，固定为 `1`。
            SR:
              type: integer
              description: 所用分辨率档位（例如，`720` 对应 720P，`1080` 对应 1080P）。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符，用于追踪和支持。
        code:
          type: string
          description: 机器可读的错误码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 人类可读的错误信息。
          example: Invalid model name
````
