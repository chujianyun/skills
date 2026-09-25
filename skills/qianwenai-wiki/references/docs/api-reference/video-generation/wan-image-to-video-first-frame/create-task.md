> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan — 创建任务

> 提交图生视频任务

根据首帧图片和文本提示词生成视频。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: Wan 图像转视频（首帧）API
  description: 使用 Wan 图像转视频模型，根据首帧图像和文字描述生成视频。支持音频同步、多镜头叙事以及多种分辨率规格。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createI2VFirstFrame
      summary: 创建图像转视频任务
      description: 使用首帧图像创建图像转视频任务。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 必须设置为 `enable`。HTTP 请求仅支持异步处理。若省略此请求头，将返回 "当前用户 API 不支持同步调用" 的错误。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/I2VFirstFrameRequest"
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
        - lang: python
          label: Python（同步调用）
          source: |-
            import base64
            import os
            from http import HTTPStatus
            from dashscope import VideoSynthesis
            import mimetypes
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            # 如果未配置环境变量，请将下一行替换为您的 API Key：api_key="sk-xxx"
            api_key = os.getenv("DASHSCOPE_API_KEY")

            # --- 辅助函数：用于 Base64 编码 ---
            # 格式：data:{MIME_type};base64,{base64_data}
            def encode_file(file_path):
              mime_type, _ = mimetypes.guess_type(file_path)
              if not mime_type or not mime_type.startswith("image/"):
                raise ValueError("Unsupported or unrecognized image format")
              with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
              return f"data:{mime_type};base64,{encoded_string}"

            """
            图片输入方式：
            从以下三种方式中选择一种，

            1. 使用公开 URL - 适用于可公开访问的图片
            2. 使用本地文件 - 适用于本地开发和测试
            3. 使用 Base64 编码 - 适用于私有图片或需要加密传输的场景
            """

            # [方式 1] 使用可公开访问的图片 URL
            # 示例：使用公开图片 URL
            img_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"

            # [方式 2] 使用本地文件（支持绝对路径和相对路径）
            # 格式要求：file:// + 文件路径
            # 示例（绝对路径）：
            # img_url = "file://" + "/path/to/your/img.png"    # Linux/macOS
            # img_url = "file://" + "/C:/path/to/your/img.png"  # Windows
            # 示例（相对路径）：
            # img_url = "file://" + "./img.png"                # 相对于当前可执行文件的路径

            # [方式 3] 使用 Base64 编码的图片
            # img_url = encode_file("./img.png")

            # 设置音频 URL
            audio_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"

            def sample_call_i2v():
              # 同步调用，直接返回结果
              print('请稍候...')
              rsp = VideoSynthesis.call(api_key=api_key,
                                          model='wan2.6-i2v-flash',
                                          prompt='A scene of urban fantasy art. A dynamic graffiti art character. A boy made of spray paint comes to life from a concrete wall. He raps an English song at high speed while striking a classic, energetic rapper pose. The scene is set under an urban railway bridge at night. The lighting comes from a single street lamp, creating a cinematic atmosphere full of high energy and amazing detail. The audio of the video consists entirely of his rap, with no other dialogue or noise.',
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
        - lang: python
          label: Python（异步调用）
          source: |-
            import os
            from http import HTTPStatus
            from dashscope import VideoSynthesis
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            # 如果未配置环境变量，请将下一行替换为您的 API Key：api_key="sk-xxx"
            api_key = os.getenv("DASHSCOPE_API_KEY")

            # 使用可公开访问的图片 URL
            img_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"

            # 设置音频 URL
            audio_url = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"

            def sample_async_call_i2v():
              # 异步调用，返回 task_id
              rsp = VideoSynthesis.async_call(api_key=api_key,
                              model='wan2.6-i2v-flash',
                              prompt='A scene of urban fantasy art. A dynamic graffiti art character. A boy made of spray paint comes to life from a concrete wall. He raps an English song at high speed while striking a classic, energetic rapper pose. The scene is set under an urban railway bridge at night. The lighting comes from a single street lamp, creating a cinematic atmosphere full of high energy and amazing detail. The audio of the video consists entirely of his rap, with no other dialogue or noise.',
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
                print("task_id: %s" % rsp.output.task_id)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))

              # 获取异步任务信息
              status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
              if status.status_code == HTTPStatus.OK:
                print(status.output.task_status)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                          (status.status_code, status.code, status.message))

              # 等待异步任务完成
              rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output.video_url)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))

            if __name__ == '__main__':
              sample_async_call_i2v()
        - lang: java
          label: Java（同步调用）
          source: |-
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

              // 如果未配置环境变量，请将下一行替换为您的 API Key：apiKey="sk-xxx"
              static String apiKey = System.getenv("DASHSCOPE_API_KEY");

              /**
                 * 图片输入方式：从以下三种方式中选择一种
                 *
                 * 1. 使用公开 URL - 适用于可公开访问的图片
                 * 2. 使用本地文件 - 适用于本地开发和测试
                 * 3. 使用 Base64 编码 - 适用于私有图片或需要加密传输的场景
                 */

              // [方式 1] 公开 URL
              static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";

              // [方式 2] 本地文件路径（file://+绝对路径）
              // static String imgUrl = "file://" + "/your/path/to/img.png";    // Linux/macOS
              // static String imgUrl = "file://" + "/C:/your/path/to/img.png";  // Windows

              // [方式 3] Base64 编码
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
                        .prompt("A scene of urban fantasy art. A dynamic graffiti art character. A boy made of spray paint comes to life from a concrete wall. He raps an English song at high speed while striking a classic, energetic rapper pose. The scene is set under an urban railway bridge at night. The lighting comes from a single street lamp, creating a cinematic atmosphere full of high energy and amazing detail. The audio of the video consists entirely of his rap, with no other dialogue or noise.")
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
                  throw new IllegalArgumentException("File does not exist: " + filePath);
                }
                // 检测 MIME 类型
                String mimeType = null;
                try {
                  mimeType = Files.probeContentType(path);
                } catch (IOException e) {
                  throw new IllegalArgumentException("Cannot detect file type: " + filePath);
                }
                if (mimeType == null || !mimeType.startsWith("image/")) {
                  throw new IllegalArgumentException("Unsupported or unrecognized image format");
                }
                // 读取文件内容并编码
                byte[] fileBytes = null;
                try{
                  fileBytes = Files.readAllBytes(path);
                } catch (IOException e) {
                  throw new IllegalArgumentException("Cannot read file content: " + filePath);
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
        - lang: java
          label: Java（异步调用）
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.

            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisListResult;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.task.AsyncTaskListParam;
            import com.alibaba.dashscope.utils.JsonUtils;
            import com.alibaba.dashscope.utils.Constants;

            import java.util.HashMap;
            import java.util.Map;

            public class Image2Video {

              static {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              }

              // 如果未配置环境变量，请将下一行替换为您的 API Key：api_key="sk-xxx"
              static String apiKey = System.getenv("DASHSCOPE_API_KEY");
              // 设置输入图片 URL
              static String imgUrl = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png";

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
                        .prompt("A scene of urban fantasy art. A dynamic graffiti art character. A boy made of spray paint comes to life from a concrete wall. He raps an English song at high speed while striking a classic, energetic rapper pose. The scene is set under an urban railway bridge at night. The lighting comes from a single street lamp, creating a cinematic atmosphere full of high energy and amazing detail. The audio of the video consists entirely of his rap, with no other dialogue or noise.")
                        .imgUrl(imgUrl)
                        .audioUrl(audioUrl)
                        .duration(10)
                        .parameters(parameters)
                        .resolution("720P")
                        .negativePrompt("")
                        .build();
                // 异步调用
                VideoSynthesisResult task = vs.asyncCall(param);
                System.out.println(JsonUtils.toJson(task));
                System.out.println("请稍候...");

                // 获取结果
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
                // 如果 DASHSCOPE_API_KEY 已设置为环境变量，apiKey 可以为 null
                VideoSynthesisResult result = is.fetch(taskId, apiKey);
                System.out.println(result.getOutput());
                System.out.println(result.getUsage());
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
        - lang: curl
          label: cURL - 多镜头叙事
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.6-i2v-flash",
              "input": {
                "prompt": "A scene of urban fantasy art. A dynamic graffiti art character. A boy made of spray paint comes to life from a concrete wall.",
                "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
                "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
              },
              "parameters": {
                "resolution": "720P",
                "prompt_extend": true,
                "duration": 10,
                "shot_type": "multi"
              }
            }'
        - lang: curl
          label: cURL - 自动配音
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.5-i2v-preview",
              "input": {
                "prompt": "A scene of urban fantasy art. A dynamic graffiti art character. A boy made of spray paint comes to life from a concrete wall. He raps an English song at high speed while striking a classic, energetic rapper pose. The scene is set under an urban railway bridge at night. The lighting comes from a single street lamp, creating a cinematic atmosphere full of high energy and amazing detail. The audio of the video consists entirely of his rap, with no other dialogue or noise.",
                "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
              },
              "parameters": {
                "resolution": "480P",
                "prompt_extend": true,
                "duration": 10
              }
            }'
        - lang: curl
          label: cURL - 提供音频文件
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.5-i2v-preview",
              "input": {
                "prompt": "A scene of urban fantasy art. A dynamic graffiti art character. A boy made of spray paint comes to life from a concrete wall. He raps an English song at high speed while striking a classic, energetic rapper pose. The scene is set under an urban railway bridge at night. The lighting comes from a single street lamp, creating a cinematic atmosphere full of high energy and amazing detail. The audio of the video consists entirely of his rap, with no other dialogue or noise.",
                "img_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png",
                "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3"
              },
              "parameters": {
                "resolution": "480P",
                "prompt_extend": true,
                "duration": 10
              }
            }'
        - lang: curl
          label: cURL - 无声视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.2-i2v-plus",
              "input": {
                "prompt": "A cat running on the grass",
                "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"
              },
              "parameters": {
                "resolution": "480P",
                "prompt_extend": true
              }
            }'
        - lang: curl
          label: cURL - 使用负向提示词
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.2-i2v-plus",
              "input": {
                "prompt": "A cat running on the grass",
                "negative_prompt": "flowers",
                "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png"
              },
              "parameters": {
                "resolution": "480P",
                "prompt_extend": true
              }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    I2VFirstFrameRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wan2.6-i2v-flash
            - wan2.6-i2v
            - wan2.5-i2v-preview
            - wan2.2-i2v-flash
            - wan2.2-i2v-plus
            - wan2.1-i2v-turbo
            - wan2.1-i2v-plus
          example: wan2.6-i2v-flash
        input:
          type: object
          required:
            - img_url
          description: 输入数据，包括首帧图像、提示词和可选音频。
          properties:
            prompt:
              type: string
              description: |-
                用于描述生成视频内容和视觉特征的文字提示词。支持中英文。不同模型的长度限制：
                - wan2.6 和 wan2.5 模型：最多 1,500 个字符。
                - wan2.2 和 wan2.1 模型：最多 800 个字符。

                超出限制的文本将自动截断。提示词撰写技巧请参见图生视频提示词指南。
              example: A cat running on the grass
            negative_prompt:
              type: string
              description: 负向提示词，描述不希望出现在视频中的内容。支持中英文，最多 500 个字符，超出部分自动截断。
              maxLength: 500
              example: low resolution, error, worst quality, low quality
            img_url:
              type: string
              description: |-
                首帧图像的 URL 或 Base64 字符串。

                **图像约束：**
                - 格式：JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP。
                - 分辨率：宽高均需在 360 至 2,000 像素之间。
                - 文件大小：不超过 10 MB。

                **支持的输入格式：**
                1. 公开 URL（支持 HTTP/HTTPS）。
                2. Base64 编码图像：`data:{MIME_type};base64,{base64_data}`。
              example: https://cdn.translate.alibaba.com/r/wanx-demo-1.png
            audio_url:
              type: string
              description: |-
                音频文件的 URL。模型在生成视频时将与该音频同步。仅 wan2.6 和 wan2.5 模型支持。

                **音频约束：**
                - 格式：wav、mp3。
                - 时长：3 至 30 秒。
                - 文件大小：不超过 15 MB。
                - 若音频时长超过视频 `duration`，将自动截断；若短于视频时长，剩余部分无声。
              example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/ozwpvi/rap.mp3
        parameters:
          $ref: "#/components/schemas/I2VFirstFrameParameters"
    I2VFirstFrameParameters:
      type: object
      description: 视频生成参数。
      properties:
        resolution:
          type: string
          description: |-
            生成视频的分辨率规格。模型会将输出缩放至相近的总像素数，宽高比与输入图像尽量保持一致。分辨率直接影响费用（1080P > 720P > 480P）。

            各模型默认值及可选项：
            - wan2.6-i2v-flash：720P、1080P（默认：1080P）
            - wan2.6-i2v：720P、1080P（默认：1080P）
            - wan2.5-i2v-preview：480P、720P、1080P（默认：1080P）
            - wan2.2-i2v-flash：480P、720P、1080P（默认：720P）
            - wan2.2-i2v-plus：480P、1080P（默认：1080P）
            - wan2.1-i2v-turbo：480P、720P（默认：720P）
            - wan2.1-i2v-plus：720P（固定）
          enum:
            - 480P
            - 720P
            - 1080P
          example: 720P
        duration:
          type: integer
          description: |-
            生成视频的时长（秒）。时长越长费用越高（按秒计费）。

            各模型有效值：
            - wan2.6-i2v-flash：2–15 的整数（默认：5）
            - wan2.6-i2v：2–15 的整数（默认：5）
            - wan2.5-i2v-preview：5、10（默认：5）
            - wan2.2-i2v-flash：固定为 5（不可配置）
            - wan2.2-i2v-plus：固定为 5（不可配置）
            - wan2.1-i2v-turbo：3、4、5（默认：5）
            - wan2.1-i2v-plus：固定为 5（不可配置）
          example: 5
        prompt_extend:
          type: boolean
          description: 是否启用提示词改写。启用后，LLM 将对输入提示词进行改写，可提升短提示词的生成质量，但会增加处理时间。
          default: true
          example: true
        shot_type:
          type: string
          description: 视频采用单一连续镜头还是多镜头切换。仅 wan2.6 模型支持，且仅在 `prompt_extend` 为 `true` 时生效。指定后将覆盖提示词中与镜头相关的描述。
          enum:
            - single
            - multi
          default: single
          example: single
        audio:
          type: boolean
          description: 是否生成有声视频。仅 wan2.6-i2v-flash 支持。优先级：`audio` > `audio_url`。若 `audio=false`，即使提供了 `audio_url`，输出视频也为无声。音频设置会影响定价。
          default: true
          example: true
        watermark:
          type: boolean
          description: 是否在视频右下角添加 "AI 生成" 水印。
          default: false
          example: false
        seed:
          type: integer
          description: 随机数种子，用于控制生成结果的可复现性。取值范围：[0, 2147483647]。若不设置，则随机使用种子。相同种子不保证生成完全相同的结果。
          minimum: 0
          maximum: 2147483647
          example: 12345
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应结果。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符，用于追踪和排查问题。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 用于轮询任务状态的任务 ID。配合 `GET /tasks/{task_id}` 使用，有效期 24 小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
              example: PENDING
    TaskStatusResponse:
      type: object
      description: 轮询任务状态的响应结果。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
          example: 2ca1c497-f9e0-449d-9a3f-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: af6efbc0-4bef-4194-8246-xxxxxx
            task_status:
              type: string
              description: 当前任务状态。状态流转：PENDING → RUNNING → SUCCEEDED 或 FAILED。UNKNOWN 表示任务不存在或已过期。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间。UTC+8 格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-09-25 11:07:28.590
            scheduled_time:
              type: string
              description: 任务开始运行的时间。UTC+8 格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-09-25 11:07:35.349
            end_time:
              type: string
              description: 任务完成时间。UTC+8 格式：YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-09-25 11:17:11.650
            video_url:
              type: string
              description: 生成视频的 URL。仅在 `task_status` 为 `SUCCEEDED` 时返回，有效期 24 小时，请及时下载。格式为 MP4（H.264 编码）。
              example: https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.mp4?Expires=xxx
            orig_prompt:
              type: string
              description: 原始输入提示词。
            actual_prompt:
              type: string
              description: 当 `prompt_extend=true` 时，返回实际用于生成的优化后提示词。`prompt_extend=false` 时不返回。wan2.6 模型不返回此字段。
            code:
              type: string
              description: 错误码。仅在任务失败时返回。
            message:
              type: string
              description: 详细错误信息。仅在任务失败时返回。
        usage:
          type: object
          description: 输出统计信息。仅在任务成功时返回，具体字段因模型版本而异。
          properties:
            duration:
              type: integer
              description: 用于计费的视频总时长。对于 wan2.6 模型：`input_video_duration + output_video_duration`。
            input_video_duration:
              type: integer
              description: 输入视频时长（秒）。图像转视频时固定为 0。由 wan2.6 模型返回。
            output_video_duration:
              type: integer
              description: 输出视频时长（秒）。由 wan2.6 模型返回。
            video_count:
              type: integer
              description: 生成视频数量。固定为 1。
              example: 1
            SR:
              type: integer
              description: 生成视频的分辨率规格（如 720）。由 wan2.6、wan2.5 和 wan2.2 模型返回。
              example: 720
            audio:
              type: boolean
              description: 输出视频是否有声。仅 wan2.6-i2v-flash 返回。
            video_duration:
              type: integer
              description: 生成视频的时长（秒）。仅 wan2.1 模型返回。
            video_ratio:
              type: string
              description: 生成视频的宽高比。固定为 `standard`。仅 wan2.1 模型返回。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        code:
          type: string
          description: 错误码（如 `InvalidApiKey`、`InvalidParameter`、`Throttling`）。
          example: InvalidApiKey
        message:
          type: string
          description: 可读的错误信息。
          example: No API-key provided.
````
