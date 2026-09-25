> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan — 创建任务

> 提交首尾帧图生视频任务

Wan kf2v 模型根据**首帧图片**、**尾帧图片**和**文本提示词**，生成平滑过渡的视频。

## OpenAPI

````yaml post /services/aigc/image2video/video-synthesis
openapi: 3.1.0
info:
  title: Wan 图生视频（首尾帧）API
  description: 使用 Wan kf2v 模型，基于首帧图像、尾帧图像和文本提示词，生成过渡自然流畅的视频。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/image2video/video-synthesis:
    post:
      operationId: createI2VFirstLast
      summary: 创建图生视频任务
      description: 基于首帧和尾帧图像创建图生视频任务。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步提交任务时必须设置为 `enable`，否则返回错误。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/I2VFirstLastRequest"
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
          label: cURL - 基础示例
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.2-kf2v-flash",
              "input": {
                "first_frame_url": "https://wanx.alicdn.com/material/20250318/first_frame.png",
                "last_frame_url": "https://wanx.alicdn.com/material/20250318/last_frame.png",
                "prompt": "Realistic style, a small black cat looks up at the sky curiously, the camera gradually rises from eye level, and finally captures its curious gaze from a top-down view."
              },
              "parameters": {
                "resolution": "480P",
                "prompt_extend": true
              }
            }'
        - lang: curl
          label: cURL - 含负向提示词
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.1-kf2v-plus",
              "input": {
                "first_frame_url": "https://wanx.alicdn.com/material/20250318/first_frame.png",
                "last_frame_url": "https://wanx.alicdn.com/material/20250318/last_frame.png",
                "prompt": "Realistic style, a small black cat looks up at the sky curiously, the camera gradually rises from eye level, and finally captures its curious gaze from a top-down view.",
                "negative_prompt": "people"
              },
              "parameters": {
                "resolution": "720P",
                "prompt_extend": true
              }
            }'
        - lang: python
          label: Python (Sync)
          source: |-
            import os
            from http import HTTPStatus
            # dashscope sdk >= 1.23.4
            from dashscope import VideoSynthesis
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            # 从环境变量获取 DashScope API Key
            api_key = os.getenv("DASHSCOPE_API_KEY")

            # ========== 图像输入方式（二选一）==========
            # [方式一] 使用公开图片 URL
            first_frame_url = "https://wanx.alicdn.com/material/20250318/first_frame.png"
            last_frame_url = "https://wanx.alicdn.com/material/20250318/last_frame.png"

            # [方式二] 使用本地文件路径（file:// + 文件路径）
            # 使用绝对路径
            # first_frame_url = "file://" + "/path/to/your/first_frame.png"  # Linux/macOS
            # last_frame_url = "file://" + "C:/path/to/your/last_frame.png"  # Windows
            # 或使用相对路径
            # first_frame_url = "file://" + "./first_frame.png"              # 替换为实际路径
            # last_frame_url = "file://" + "./last_frame.png"                # 替换为实际路径

            def sample_sync_call_kf2v():
              print('please wait...')
              rsp = VideoSynthesis.call(api_key=api_key,
                                          model="wan2.2-kf2v-flash",
                                          prompt="Realistic style, a small black cat looks up at the sky curiously, the camera gradually rises from eye level, and finally captures its curious gaze from a top-down view.",
                                          first_frame_url=first_frame_url,
                                          last_frame_url=last_frame_url,
                                          resolution="720P",
                                          prompt_extend=True)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output.video_url)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))

            if __name__ == '__main__':
              sample_sync_call_kf2v()
        - lang: python
          label: Python (Async)
          source: |-
            import os
            from http import HTTPStatus
            # dashscope sdk >= 1.23.4
            from dashscope import VideoSynthesis
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            # 从环境变量获取 DashScope API Key
            api_key = os.getenv("DASHSCOPE_API_KEY")

            # ========== 图像输入方式（二选一）==========
            # [方式一] 使用公开图片 URL
            first_frame_url = "https://wanx.alicdn.com/material/20250318/first_frame.png"
            last_frame_url = "https://wanx.alicdn.com/material/20250318/last_frame.png"

            # [方式二] 使用本地文件路径（file:// + 文件路径）
            # 使用绝对路径
            # first_frame_url = "file://" + "/path/to/your/first_frame.png"  # Linux/macOS
            # last_frame_url = "file://" + "C:/path/to/your/last_frame.png"  # Windows
            # 或使用相对路径
            # first_frame_url = "file://" + "./first_frame.png"              # 替换为实际路径
            # last_frame_url = "file://" + "./last_frame.png"                # 替换为实际路径

            def sample_async_call_kf2v():
              print('please wait...')
              rsp = VideoSynthesis.async_call(api_key=api_key,
                              model="wan2.2-kf2v-flash",
                              prompt="Realistic style, a small black cat looks up at the sky curiously, the camera gradually rises from eye level, and finally captures its curious gaze from a top-down view.",
                              first_frame_url=first_frame_url,
                              last_frame_url=last_frame_url,
                              resolution="720P",
                              prompt_extend=True)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print("task_id: %s" % rsp.output.task_id)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))

              # 获取任务信息，包含任务状态
              status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
              if status.status_code == HTTPStatus.OK:
                print(status.output.task_status)  # 查看任务状态
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                          (status.status_code, status.code, status.message))

              # 轮询等待任务完成
              rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output.video_url)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))

            if __name__ == '__main__':
              sample_async_call_kf2v()
        - lang: java
          label: Java (Sync)
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.

            // dashscope sdk >= 2.20.1
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;

            import java.util.HashMap;
            import java.util.Map;

            public class Kf2vSyncIntl {

              static {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              }

              // 从环境变量获取 DashScope API Key
              static String apiKey = System.getenv("DASHSCOPE_API_KEY");

              /**
                 * 图像输入方式（二选一）：
                 *
                 * [方式一] 公开 URL
                 */
              static String firstFrameUrl = "https://wanx.alicdn.com/material/20250318/first_frame.png";
              static String lastFrameUrl = "https://wanx.alicdn.com/material/20250318/last_frame.png";

                 /**
                 * [方式二] 本地文件路径（file:// + 绝对路径 或 file:/// + 绝对路径）
                 */
              // static String firstFrameUrl = "file://" + "/your/path/to/first_frame.png";  // Linux/macOS
              // static String lastFrameUrl = "file:///" + "C:/path/to/your/img.png";        // Windows

              public static void syncCall() {

                Map<String, Object> parameters = new HashMap<>();
                parameters.put("prompt_extend", true);
                parameters.put("resolution", "720P");

                VideoSynthesis videoSynthesis = new VideoSynthesis();
                VideoSynthesisParam param =
                    VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.2-kf2v-flash")
                        .prompt("Realistic style, a small black cat looks up at the sky curiously, the camera gradually rises from eye level, and finally captures its curious gaze from a top-down view.")
                        .firstFrameUrl(firstFrameUrl)
                        .lastFrameUrl(lastFrameUrl)
                        .parameters(parameters)
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
          label: Java (Async)
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.

            // dashscope sdk >= 2.20.1
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;
            import java.util.HashMap;
            import java.util.Map;

            public class Kf2vAsync {

              static {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              }

              // 从环境变量获取 DashScope API Key
              static String apiKey = System.getenv("DASHSCOPE_API_KEY");

              /**
                 * 图像输入方式（二选一）
                 *
                 * [方式一] 公开 URL
                 */
              static String firstFrameUrl = "https://wanx.alicdn.com/material/20250318/first_frame.png";
              static String lastFrameUrl = "https://wanx.alicdn.com/material/20250318/last_frame.png";

              /**
                 * [方式二] 本地文件路径（file:// + 绝对路径 或 file:/// + 绝对路径）
                 */
              // static String firstFrameUrl = "file://" + "/your/path/to/first_frame.png";   // Linux/macOS
              // static String lastFrameUrl = "file:///" + "C:/path/to/your/img.png";        // Windows

              public static void asyncCall(){

                // 设置参数
                Map<String, Object> parameters = new HashMap<>();
                parameters.put("prompt_extend", true);
                parameters.put("resolution", "720P");

                VideoSynthesis videoSynthesis = new VideoSynthesis();
                VideoSynthesisParam param =
                    VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.2-kf2v-flash")
                        .prompt("Realistic style, a small black cat looks up at the sky curiously, the camera gradually rises from eye level, and finally captures its curious gaze from a top-down view.")
                        .firstFrameUrl(firstFrameUrl)
                        .lastFrameUrl(lastFrameUrl)
                        .parameters(parameters)
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

              public static void main(String[] args){
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
    I2VFirstLastRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wan2.2-kf2v-flash
            - wan2.1-kf2v-plus
          example: wan2.2-kf2v-flash
        input:
          type: object
          required:
            - first_frame_url
            - last_frame_url
          description: 输入数据，包含首尾帧图像和可选提示词。
          properties:
            prompt:
              type: string
              description: 描述期望视频内容的文本提示词。支持中英文，最长 800 个字符，超出部分自动截断。若首尾帧的主体或场景发生变化，建议描述过渡方式（如镜头运动或主体动作）。
              maxLength: 800
              example: Realistic style, a small black cat looks up at the sky curiously, the camera gradually rises from eye level, and finally captures its curious gaze from a top-down view.
            negative_prompt:
              type: string
              description: 描述视频中不希望出现的内容。支持中英文，最长 500 个字符，超出部分自动截断。
              maxLength: 500
              example: low resolution, error, worst quality, low quality, deformed, extra fingers, bad proportions
            first_frame_url:
              type: string
              description: 首帧图像的 URL。输出视频的宽高比与该图像一致。必须可公开访问（HTTP 或 HTTPS）。**图像要求**：格式：JPEG、JPG、PNG（无 Alpha 通道）、BMP 或 WEBP；分辨率：每边 360–2000 像素；文件大小：不超过 10 MB。
              example: https://wanx.alicdn.com/material/20250318/first_frame.png
            last_frame_url:
              type: string
              description: 尾帧图像的 URL。必须可公开访问（HTTP 或 HTTPS）。分辨率可与首帧不同，无需对齐。**图像要求**：格式：JPEG、JPG、PNG（无 Alpha 通道）、BMP 或 WEBP；分辨率：每边 360–2000 像素；文件大小：不超过 10 MB。
              example: https://wanx.alicdn.com/material/20250318/last_frame.png
        parameters:
          $ref: "#/components/schemas/I2VFirstLastParameters"
    I2VFirstLastParameters:
      type: object
      description: 视频生成参数。
      properties:
        resolution:
          type: string
          description: 生成视频的分辨率档位。调整清晰度（总像素数）但不改变宽高比。视频宽高比与首帧图像一致。**分辨率影响计费**：1080P > 720P > 480P。可选值取决于模型：`wan2.2-kf2v-flash`：480P、720P、1080P（默认：720P）；`wan2.1-kf2v-plus`：480P、720P（默认：720P）。
          enum:
            - 480P
            - 720P
            - 1080P
          default: 720P
          example: 720P
        duration:
          type: integer
          description: 生成视频的时长（秒）。固定为 5 秒，不可修改。
          enum:
            - 5
          default: 5
        prompt_extend:
          type: boolean
          description: 是否启用提示词优化。启用后，大语言模型将对输入提示词进行改写，对短提示词效果更佳，但会增加处理时间。默认值：`true`。
          default: true
        watermark:
          type: boolean
          description: 在视频右下角添加「AI 生成」水印。默认值：`false`。
          default: false
        seed:
          type: integer
          description: 随机数种子，用于控制生成结果的可复现性。范围：[0, 2147483647]。不填则使用随机种子。即使设置种子，结果仍可能因模型随机性而有所不同。
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
              description: 用于轮询任务状态的任务 ID，配合 `GET /tasks/{task_id}` 使用。有效期 24 小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务的初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
    TaskStatusResponse:
      type: object
      description: 查询任务状态的响应结果。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符，用于追踪和排查问题。
          example: ec016349-6b14-9ad6-8009-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 3f21a745-9f4b-4588-b643-xxxxxx
            task_status:
              type: string
              description: 任务当前状态。状态流转：PENDING → RUNNING → SUCCEEDED 或 FAILED。UNKNOWN 表示任务不存在或已过期。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间（UTC+8）。格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-04-18 10:36:58.394
            scheduled_time:
              type: string
              description: 任务开始运行时间（UTC+8）。格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-04-18 10:37:13.802
            end_time:
              type: string
              description: 任务完成时间（UTC+8）。格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-04-18 10:45:23.004
            video_url:
              type: string
              description: 生成视频的 URL（MP4 格式，H.264 编码）。仅在 `task_status` 为 `SUCCEEDED` 时返回。有效期 24 小时。
              example: https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/xxx.mp4?xxxxx
            orig_prompt:
              type: string
              description: 原始输入提示词。
            actual_prompt:
              type: string
              description: 启用提示词优化后实际使用的改写提示词。未启用提示词优化时不返回此字段。
            code:
              type: string
              description: 错误码。仅在任务失败时返回。
            message:
              type: string
              description: 详细错误信息。仅在任务失败时返回。
        usage:
          type: object
          description: 用量统计。仅在任务成功时返回。
          properties:
            video_duration:
              type: integer
              description: 视频时长（秒）。固定值：5。计费公式：费用 = 视频时长（秒）× 单价。
              example: 5
            video_count:
              type: integer
              description: 生成的视频数量。固定为 1。
              example: 1
            video_ratio:
              type: string
              description: 视频宽高比。仅 wan2.1 模型返回。固定为 `standard`。
              example: standard
            SR:
              type: integer
              description: 视频分辨率档位。仅 wan2.2 模型返回。可选值：480、720 或 1080。
              enum:
                - 480
                - 720
                - 1080
              example: 480
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符。
        code:
          type: string
          description: 错误码（如 `InvalidParameter`、`InvalidApiKey`、`Throttling`）。
          example: InvalidApiKey
        message:
          type: string
          description: 人类可读的错误信息。
          example: No API-key provided.
````
