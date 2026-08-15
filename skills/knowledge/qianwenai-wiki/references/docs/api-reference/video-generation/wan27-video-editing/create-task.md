> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.7 — 视频编辑

> 提交视频编辑任务（wan2.7）

使用文本提示和可选的参考图片编辑最高 1080P 的视频——支持更改风格、替换对象，或将参考图片中的内容融入源视频。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: Wan 2.7 视频编辑 API
  description: 基于 Wan 2.7 模型，通过多模态输入（文本、图片、视频）对视频进行编辑。提交异步任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createWan27VideoEditing
      summary: 创建视频编辑任务
      description: 提交视频编辑任务，返回用于轮询的 `task_id`。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步任务提交时必须设置为 `enable`。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Wan27VideoEditingRequest"
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
          label: cURL - 视频风格转换
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.7-videoedit",
              "input": {
                "prompt": "Convert the entire scene to a claymation style",
                "media": [
                  {
                    "type": "video",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4"
                  }
                ]
              },
              "parameters": {
                "resolution": "720P",
                "prompt_extend": true,
                "watermark": true
              }
            }'
        - lang: curl
          label: cURL - 参考图视频编辑
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.7-videoedit",
              "input": {
                "prompt": "Replace the girl's clothes in the video with the clothes from the image",
                "media": [
                  {
                    "type": "video",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4"
                  },
                  {
                    "type": "reference_image",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png"
                  }
                ]
              },
              "parameters": {
                "resolution": "720P",
                "prompt_extend": true,
                "watermark": true
              }
            }'
        - lang: python
          label: Python - 同步调用
          source: |-
            import os
            import base64
            import mimetypes
            from http import HTTPStatus
            # dashscope sdk >= 1.25.16
            from dashscope import VideoSynthesis
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            # 从环境变量获取 DashScope API Key
            api_key = os.getenv("DASHSCOPE_API_KEY")

            # ========== 参考图像输入方式（三选一）==========
            # [方式一] 使用公网图片 URL
            reference_image_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png"

            # [方式二] 使用本地文件路径（file:// + 文件路径）
            # reference_image_url = "file://" + "/path/to/image.png"      # Linux/macOS
            # reference_image_url = "file://" + "C:/path/to/image.png"    # Windows

            # [方式三] 使用 Base64 编码
            # def encode_file(file_path):
            #     mime_type, _ = mimetypes.guess_type(file_path)
            #     with open(file_path, "rb") as f:
            #         encoded = base64.b64encode(f.read()).decode('utf-8')
            #     return f"data:{mime_type};base64,{encoded}"
            # reference_image_url = encode_file("/path/to/image.png")

            def sync_call():
              print('please wait...')
              rsp = VideoSynthesis.call(
                api_key=api_key,
                model='wan2.7-videoedit',
                prompt='将视频中女孩的衣服替换为图片中的衣服',
                media=[
                  {
                    "type": "video",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4"
                  },
                  {
                    "type": "reference_image",
                    "url": reference_image_url
                  }
                ],
                resolution='720P',
                prompt_extend=True,
                watermark=True)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output.video_url)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))

            if __name__ == '__main__':
              sync_call()
        - lang: java
          label: Java - 同步调用
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.

            // dashscope sdk >= 2.22.14
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;

            import java.util.ArrayList;
            import java.util.HashMap;
            import java.util.List;
            import java.util.Map;

            public class VideoEdit {

              static {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              }

              // 从环境变量获取 DashScope API Key
              static String apiKey = System.getenv("DASHSCOPE_API_KEY");

              /**
               * 参考图像输入方式（三选一）：
               *
               * [方式一] 公开 URL
               */
              static String referenceImageUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png";

              /**
               * [方式二] 本地文件路径（file:// + 绝对路径）
               */
              // static String referenceImageUrl = "file://" + "/path/to/image.png";     // Linux/macOS
              // static String referenceImageUrl = "file://" + "C:/path/to/image.png";   // Windows

              public static void syncCall() {
                VideoSynthesis vs = new VideoSynthesis();
                List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>() {{
                  add(VideoSynthesisParam.Media.builder()
                          .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4")
                          .type("video")
                          .build());
                  add(VideoSynthesisParam.Media.builder()
                          .url(referenceImageUrl)
                          .type("reference_image")
                          .build());
                }};
                Map<String, Object> parameters = new HashMap<>();
                parameters.put("resolution", "720P");
                parameters.put("prompt_extend", true);
                parameters.put("watermark", true);
                VideoSynthesisParam param =
                    VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.7-videoedit")
                        .prompt("将视频中女孩的衣服替换为图片中的衣服")
                        .media(media)
                        .parameters(parameters)
                        .build();
                VideoSynthesisResult result = null;
                try {
                  System.out.println("---sync call, please wait---");
                  result = vs.call(param);
                } catch (ApiException | NoApiKeyException e) {
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
        - lang: python
          label: Python - 异步调用
          source: |-
            import os
            import base64
            import mimetypes
            from http import HTTPStatus
            # dashscope sdk >= 1.25.16
            from dashscope import VideoSynthesis
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            # 从环境变量获取 DashScope API Key
            api_key = os.getenv("DASHSCOPE_API_KEY")

            # ========== 参考图像输入方式（三选一）==========
            # [方式一] 使用公网图片 URL
            reference_image_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png"

            # [方式二] 使用本地文件路径（file:// + 文件路径）
            # reference_image_url = "file://" + "/path/to/image.png"      # Linux/macOS
            # reference_image_url = "file://" + "C:/path/to/image.png"    # Windows

            # [方式三] 使用 Base64 编码
            # def encode_file(file_path):
            #     mime_type, _ = mimetypes.guess_type(file_path)
            #     with open(file_path, "rb") as f:
            #         encoded = base64.b64encode(f.read()).decode('utf-8')
            #     return f"data:{mime_type};base64,{encoded}"
            # reference_image_url = encode_file("/path/to/image.png")

            def async_call():
              rsp = VideoSynthesis.async_call(
                api_key=api_key,
                model='wan2.7-videoedit',
                prompt='将视频中女孩的衣服替换为图片中的衣服',
                media=[
                  {
                    "type": "video",
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4"
                  },
                  {
                    "type": "reference_image",
                    "url": reference_image_url
                  }
                ],
                resolution='720P',
                prompt_extend=True,
                watermark=True)
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
              async_call()
        - lang: java
          label: Java - 异步调用
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.

            // dashscope sdk >= 2.22.14
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisListResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.task.AsyncTaskListParam;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;

            import java.util.ArrayList;
            import java.util.HashMap;
            import java.util.List;
            import java.util.Map;

            public class VideoEdit {

              static {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              }

              // 从环境变量获取 DashScope API Key
              static String apiKey = System.getenv("DASHSCOPE_API_KEY");

              /**
               * 参考图像输入方式（三选一）：
               *
               * [方式一] 公开 URL
               */
              static String referenceImageUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png";

              /**
               * [方式二] 本地文件路径（file:// + 绝对路径）
               */
              // static String referenceImageUrl = "file://" + "/path/to/image.png";     // Linux/macOS
              // static String referenceImageUrl = "file://" + "C:/path/to/image.png";   // Windows

              public static void asyncCall() {
                VideoSynthesis vs = new VideoSynthesis();
                List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>() {{
                  add(VideoSynthesisParam.Media.builder()
                          .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4")
                          .type("video")
                          .build());
                  add(VideoSynthesisParam.Media.builder()
                          .url(referenceImageUrl)
                          .type("reference_image")
                          .build());
                }};
                Map<String, Object> parameters = new HashMap<>();
                parameters.put("resolution", "720P");
                parameters.put("prompt_extend", true);
                parameters.put("watermark", true);
                VideoSynthesisParam param =
                    VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.7-videoedit")
                        .prompt("将视频中女孩的衣服替换为图片中的衣服")
                        .media(media)
                        .parameters(parameters)
                        .build();
                // 异步提交任务
                VideoSynthesisResult task = vs.asyncCall(param);
                System.out.println(JsonUtils.toJson(task));
                System.out.println("please wait...");
                // 等待任务完成并获取结果
                VideoSynthesisResult result = vs.wait(task, apiKey);
                System.out.println(JsonUtils.toJson(result));
              }

              // 获取任务列表
              public static void listTask() throws ApiException, NoApiKeyException {
                VideoSynthesis is = new VideoSynthesis();
                AsyncTaskListParam param = AsyncTaskListParam.builder().build();
                param.setApiKey(apiKey);
                VideoSynthesisListResult result = is.list(param);
                System.out.println(result);
              }

              // 获取单个任务结果
              public static void fetchTask(String taskId) throws ApiException, NoApiKeyException {
                VideoSynthesis is = new VideoSynthesis();
                VideoSynthesisResult result = is.fetch(taskId, apiKey);
                System.out.println(result.getOutput());
                System.out.println(result.getUsage());
              }

              public static void main(String[] args) {
                try {
                  asyncCall();
                } catch (ApiException | NoApiKeyException | InputRequiredException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan27VideoEditingRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型标识符，固定值为 `wan2.7-videoedit`。
          enum:
            - wan2.7-videoedit
          example: wan2.7-videoedit
        input:
          type: object
          required:
            - media
          description: 视频编辑的输入内容。
          properties:
            prompt:
              type: string
              description: 描述您希望进行的编辑操作，支持中英文，最多 5,000 个字符（超出自动截断）。
              example: Convert the entire scene to a claymation style
            negative_prompt:
              type: string
              description: 描述不希望出现在视频中的内容（如 `低质量、模糊、多余手指`），支持中英文，最多 500 个字符（超出自动截断）。
              example: low resolution, error, worst quality, low quality, incomplete, extra fingers, poor proportions
            media:
              type: array
              description: |-
                编辑所需的媒体素材，每个元素包含 `type` 和 `url` 字段。

                - **video**（必填，最多 1 个）：待编辑的视频。格式：MP4、MOV。时长：2-10 秒。分辨率：宽高均在 [240, 4096] 像素范围内。宽高比：1:8 至 8:1。文件大小：最大 100 MB。仅支持 HTTP/HTTPS URL。
                - **reference_image**（可选，最多 4 个）：用于风格或内容迁移的参考图片。格式：JPEG、JPG、PNG（不含 Alpha 通道）、BMP、WEBP。分辨率：宽高均在 [240, 8000] 像素范围内。宽高比：1:8 至 8:1。文件大小：最大 20 MB。支持 HTTP/HTTPS URL 和 Base64 编码数据（`data:{MIME_type};base64,{base64_data}`）。
              items:
                type: object
                required:
                  - type
                  - url
                properties:
                  type:
                    type: string
                    description: |-
                      媒体类型。

                      - `video`：待编辑的视频（必填，最多 1 个）。
                      - `reference_image`：参考图片（可选，最多 4 个）。
                    enum:
                      - video
                      - reference_image
                  url:
                    type: string
                    description: |-
                      URL 或 Base64 编码数据。

                      **视频**（`type=video`）：仅支持公开 URL（HTTP/HTTPS）。

                      **图片**（`type=reference_image`）：支持公开 URL（HTTP/HTTPS）或 Base64 字符串，格式为 `data:{MIME_type};base64,{base64_data}`。支持的 MIME 类型：`image/jpeg`、`image/png`、`image/bmp`、`image/webp`。
        parameters:
          $ref: "#/components/schemas/Wan27VideoEditingParameters"
    Wan27VideoEditingParameters:
      type: object
      description: 视频编辑参数。
      properties:
        resolution:
          type: string
          description: |-
            视频清晰度档位，分辨率越高费用越高。

            实际输出尺寸取决于 `ratio` 参数：
            - **720P**：16:9=1280x720，9:16=720x1280，1:1=960x960，4:3=1104x832，3:4=832x1104
            - **1080P**：16:9=1920x1080，9:16=1080x1920，1:1=1440x1440，4:3=1648x1248，3:4=1248x1648
          enum:
            - 720P
            - 1080P
          default: 1080P
        ratio:
          type: string
          description: 输出视频的宽高比。如不填写，将沿用输入视频的宽高比。
          enum:
            - 16:9
            - 9:16
            - 1:1
            - 4:3
            - 3:4
        duration:
          type: integer
          description: 输出视频时长（秒）。`0`（默认）：使用输入视频的完整时长，不截断。`2`-`10`：将输入视频截断至指定时长。
          maximum: 10
          minimum: 0
          default: 0
        audio_setting:
          type: string
          description: |-
            输出视频的音频处理方式。

            - `auto`（默认）：由模型根据 `prompt` 决定。若提示词描述了声音，则可能重新生成音频；否则保留原始音频。
            - `origin`：始终保留原始音频，不进行重新生成。
          enum:
            - auto
            - origin
          default: auto
        prompt_extend:
          type: boolean
          description: 在生成前使用大语言模型对提示词进行改写扩展，可改善简短或模糊提示词的生成效果，但会增加延迟。设为 `false` 则直接使用原始提示词。
          default: true
        watermark:
          type: boolean
          description: 在视频右下角添加「AI 生成」水印。
          default: false
        seed:
          type: integer
          description: 用于复现结果的随机种子。相同的种子与参数可生成相似（非完全相同）的输出。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应结果。
      properties:
        request_id:
          type: string
          description: 用于追踪和排查问题的唯一请求标识符。
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
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    Wan27VideoEditingTaskStatusResponse:
      type: object
      description: 查询 Wan 2.7 视频编辑任务状态的响应结果。
      properties:
        request_id:
          type: string
          description: 用于追踪和排查问题的唯一请求标识符。
          example: f16ae7e9-d518-92f8-a02c-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，提交后 24 小时内可查询。
              example: 05e68c7e-850c-49e4-b866-xxxxxx
            task_status:
              type: string
              description: 任务生命周期：`PENDING` -> `RUNNING` -> `SUCCEEDED` 或 `FAILED`。手动停止时为 `CANCELED`，过期后为 `UNKNOWN`。
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
              example: 2026-04-03 00:08:03.576
            scheduled_time:
              type: string
              description: 任务开始运行的时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`）。
              example: 2026-04-03 00:08:13.408
            end_time:
              type: string
              description: 任务完成时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`），仅在任务状态为 `SUCCEEDED` 或 `FAILED` 时返回。
              example: 2026-04-03 00:11:57.286
            orig_prompt:
              type: string
              description: 经 `prompt_extend` 改写前的原始提示词文本。
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL（MP4 格式，H.264 编码），仅在 `task_status` 为 `SUCCEEDED` 时返回。**有效期 24 小时**，请及时下载。
              example: https://dashscope-a717.oss-accelerate.aliyuncs.com/xxx.mp4?xxxx
            code:
              type: string
              description: 错误码，仅在 `task_status` 为 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息，仅在 `task_status` 为 `FAILED` 时返回。
        usage:
          type: object
          description: 资源消耗情况，仅在 `task_status` 为 `SUCCEEDED` 时返回。
          properties:
            input_video_duration:
              type: number
              description: 输入视频时长（秒）。
            output_video_duration:
              type: number
              description: 输出视频时长（秒）。
            duration:
              type: number
              description: 计费视频时长（秒），计算公式：`input_video_duration + output_video_duration`。
            SR:
              type: integer
              description: 输出视频的分辨率档位（如 `720`）。
            video_count:
              type: integer
              description: 生成的视频数量，固定值为 `1`。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 用于追踪和排查问题的唯一请求标识符。
        code:
          type: string
          description: 错误码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 人类可读的错误信息。
          example: Invalid model name
````
