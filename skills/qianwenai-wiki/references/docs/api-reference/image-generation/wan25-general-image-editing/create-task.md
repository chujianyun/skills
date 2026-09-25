> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.5 — 创建任务

> 异步 Wan 2.5 图像编辑

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

通过文本提示词编辑图像，同时保持主体一致性。支持多图融合，最多可使用三张参考图像。

## OpenAPI

````yaml post /services/aigc/image2image/image-synthesis
openapi: 3.1.0
info:
  title: Wan2.5 通用图像编辑 API
  description: Wan2.5 通用图像编辑 API。通过文本提示词对图像进行编辑，保持主体一致性。支持单图编辑和多图融合，最多支持三张参考图。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /services/aigc/image2image/image-synthesis:
    post:
      operationId: createWan25ImageEdit
      summary: 创建图像编辑任务
      description: 使用 Wan2.5 创建图像编辑任务。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 开启异步处理模式，必须设置为 `enable`。HTTP 请求仅支持异步处理。省略此请求头将返回 "current user api does not support synchronous calls" 错误。
          schema:
            type: string
            enum:
              - enable
            default: enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Wan25ImageEditRequest"
      responses:
        "200":
          description: 任务提交成功。使用 `task_id` 轮询任务结果。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
              example:
                output:
                  task_status: PENDING
                  task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                request_id: 4909100c-7b5a-9f92-bfe5-xxxxxx
        "400":
          description: 请求参数无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidParameter
                message: Invalid request parameters.
                request_id: 7438d53d-6eb8-4596-8835-xxxxxx
        "401":
          description: 鉴权失败，API Key 无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidApiKey
                message: No API-key provided.
                request_id: 7438d53d-6eb8-4596-8835-xxxxxx
      x-codeSamples:
        - lang: curl
          label: 单图编辑
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.5-i2i-preview",
              "input": {
                "prompt": "Change the floral dress to a vintage-style lace long dress with exquisite embroidery details on the collar and cuffs.",
                "images": [
                  "https://img.alicdn.com/imgextra/i2/O1CN01vHOj4h28jOxUJPwY8_!!6000000007968-49-tps-1344-896.webp"
                ]
              },
              "parameters": {
                "prompt_extend": true,
                "n": 1
              }
            }'
        - lang: curl
          label: 多图融合
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.5-i2i-preview",
              "input": {
                "prompt": "Place the alarm clock from Image 1 next to the vase on the dining table in Image 2.",
                "images": [
                  "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp",
                  "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"
                ]
              },
              "parameters": {
                "n": 1
              }
            }'
        - lang: python
          label: Python SDK - 同步调用
          source: |-
            import base64
            import mimetypes
            from http import HTTPStatus
            from urllib.parse import urlparse, unquote
            from pathlib import PurePosixPath

            import dashscope
            import requests
            from dashscope import ImageSynthesis
            import os

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            api_key = os.getenv("DASHSCOPE_API_KEY")

            # --- 图像输入：使用 Base64 编码 ---
            def encode_file(file_path):
              mime_type, _ = mimetypes.guess_type(file_path)
              if not mime_type or not mime_type.startswith("image/"):
                raise ValueError("Unsupported or unrecognized image format")
              with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
              return f"data:{mime_type};base64,{encoded_string}"

            """
            图像输入方式：
            1. 使用公开 URL - 适合可公开访问的图像。
            2. 使用本地文件 - 适合本地开发和测试。
            3. 使用 Base64 编码 - 适合私有图像或需要加密传输的场景。
            """

            # [方式一] 使用公开图像 URL
            image_url_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"
            image_url_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"

            # [方式二] 使用本地文件（支持绝对路径和相对路径）
            # image_url_1 = "file://" + "/path/to/your/image_1.png"     # Linux/macOS
            # image_url_2 = "file://" + "C:/path/to/your/image_2.png"  # Windows

            # [方式三] 使用 Base64 编码图像
            # image_url_1 = encode_file("./image_1.png")
            # image_url_2 = encode_file("./image_2.png")

            print('----同步调用，请稍候----')
            rsp = ImageSynthesis.call(api_key=api_key,
                                      model="wan2.5-i2i-preview",
                                      prompt="Place the alarm clock from Image 1 next to the vase on the dining table in Image 2.",
                                      images=[image_url_1, image_url_2],
                                      negative_prompt="",
                                      n=1,
                                      # size="1280*1280",
                                      prompt_extend=True,
                                      watermark=False,
                                      seed=12345)
            print('response: %s' % rsp)
            if rsp.status_code == HTTPStatus.OK:
              for result in rsp.output.results:
                file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                with open('./%s' % file_name, 'wb+') as f:
                  f.write(requests.get(result.url).content)
            else:
              print('同步调用失败，status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))
        - lang: python
          label: Python SDK - 异步调用
          source: |-
            import os
            from http import HTTPStatus
            from urllib.parse import urlparse, unquote
            from pathlib import PurePosixPath
            import dashscope
            import requests
            from dashscope import ImageSynthesis

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            api_key = os.getenv("DASHSCOPE_API_KEY")

            image_url_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"
            image_url_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"

            def async_call():
              print('----创建任务----')
              task_info = create_async_task()
              print('----等待任务----')
              wait_async_task(task_info)

            def create_async_task():
              rsp = ImageSynthesis.async_call(api_key=api_key,
                              model="wan2.5-i2i-preview",
                              prompt="Place the alarm clock from Image 1 next to the vase on the dining table in Image 2.",
                              images=[image_url_1, image_url_2],
                              negative_prompt="",
                              n=1,
                              # size="1280*1280",
                              prompt_extend=True,
                              watermark=False,
                              seed=12345)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output)
              else:
                print('调用失败，status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))
              return rsp

            def wait_async_task(task):
              rsp = ImageSynthesis.wait(task=task, api_key=api_key)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output)
                for result in rsp.output.results:
                  file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                  with open('./%s' % file_name, 'wb+') as f:
                    f.write(requests.get(result.url).content)
              else:
                print('调用失败，status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))

            def fetch_task_status(task):
              status = ImageSynthesis.fetch(task=task, api_key=api_key)
              print(status)
              if status.status_code == HTTPStatus.OK:
                print(status.output.task_status)
              else:
                print('调用失败，status_code: %s, code: %s, message: %s' %
                          (status.status_code, status.code, status.message))

            def cancel_task(task):
              rsp = ImageSynthesis.cancel(task=task, api_key=api_key)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output.task_status)
              else:
                print('调用失败，status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))

            if __name__ == '__main__':
              async_call()
        - lang: java
          label: Java SDK - 同步调用
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.

            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;

            import java.io.IOException;
            import java.nio.file.Files;
            import java.nio.file.Path;
            import java.nio.file.Paths;
            import java.util.*;

            // 需要 SDK 版本 >= 2.22.2
            public class Image2Image {

              static {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              }

              static String apiKey = System.getenv("DASHSCOPE_API_KEY");

              /**
                 * 图像输入方式：
                 * 1. 使用公开 URL - 适合可公开访问的图像。
                 * 2. 使用本地文件 - 适合本地开发和测试。
                 * 3. 使用 Base64 编码 - 适合私有图像或需要加密传输的场景。
                 */

              //[方式一] 公开 URL
              static String imageUrl_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp";
              static String imageUrl_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp";

              //[方式二] 本地文件路径（file://+绝对路径 或 file:///+绝对路径）
              // static String imageUrl_1 = "file://" + "/your/path/to/image_1.png";
              // static String imageUrl_2 = "file:///" + "C:/your/path/to/image_2.png";

              //[方式三] Base64 编码
              // static String imageUrl_1 = encodeFile("/your/path/to/image_1.png");
              // static String imageUrl_2 = encodeFile("/your/path/to/image_2.png");

              static List<String> imageUrls = new ArrayList<>();
              static {
                imageUrls.add(imageUrl_1);
                imageUrls.add(imageUrl_2);
              }

              public static void syncCall() {
                Map<String, Object> parameters = new HashMap<>();
                parameters.put("prompt_extend", true);
                parameters.put("watermark", false);
                parameters.put("seed", 12345);

                ImageSynthesisParam param =
                    ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.5-i2i-preview")
                        .prompt("Place the alarm clock from Image 1 next to the vase on the dining table in Image 2.")
                        .images(imageUrls)
                        .n(1)
                        //.size("1280*1280")
                        .negativePrompt("")
                        .parameters(parameters)
                        .build();

                ImageSynthesis imageSynthesis = new ImageSynthesis();
                ImageSynthesisResult result = null;
                try {
                  System.out.println("---同步调用，请稍候----");
                  result = imageSynthesis.call(param);
                } catch (ApiException | NoApiKeyException e){
                  throw new RuntimeException(e.getMessage());
                }
                System.out.println(JsonUtils.toJson(result));
              }

              /**
                 * 将文件编码为 Base64 字符串。
                 * @param filePath 文件路径。
                 * @return 格式为 data:{MIME_type};base64,{base64_data} 的 Base64 字符串。
                 */
              public static String encodeFile(String filePath) {
                Path path = Paths.get(filePath);
                if (!Files.exists(path)) {
                  throw new IllegalArgumentException("File does not exist: " + filePath);
                }
                String mimeType = null;
                try {
                  mimeType = Files.probeContentType(path);
                } catch (IOException e) {
                  throw new IllegalArgumentException("Cannot detect file type: " + filePath);
                }
                if (mimeType == null || !mimeType.startsWith("image/")) {
                  throw new IllegalArgumentException("Unsupported or unrecognized image format");
                }
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
                syncCall();
              }
            }
        - lang: java
          label: Java SDK - 异步调用
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.

            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.task.AsyncTaskListParam;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;

            import java.util.ArrayList;
            import java.util.HashMap;
            import java.util.List;
            import java.util.Map;

            // 需要 SDK 版本 >= 2.22.2
            public class Image2Image {

              static {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              }

              static String apiKey = System.getenv("DASHSCOPE_API_KEY");

              static String imageUrl_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp";
              static String imageUrl_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp";

              static List<String> imageUrls = new ArrayList<>();
              static {
                imageUrls.add(imageUrl_1);
                imageUrls.add(imageUrl_2);
              }

              public static void asyncCall() {
                Map<String, Object> parameters = new HashMap<>();
                parameters.put("prompt_extend", true);
                parameters.put("watermark", false);
                parameters.put("seed", 12345);

                ImageSynthesisParam param =
                    ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.5-i2i-preview")
                        .prompt("Place the alarm clock from Image 1 next to the vase on the dining table in Image 2.")
                        .images(imageUrls)
                        .n(1)
                        //.size("1280*1280")
                        .negativePrompt("")
                        .parameters(parameters)
                        .build();
                ImageSynthesis imageSynthesis = new ImageSynthesis();
                ImageSynthesisResult result = null;
                try {
                  System.out.println("---异步调用，请稍候----");
                  result = imageSynthesis.asyncCall(param);
                } catch (ApiException | NoApiKeyException e){
                  throw new RuntimeException(e.getMessage());
                }

                System.out.println(JsonUtils.toJson(result));

                String taskId = result.getOutput().getTaskId();
                System.out.println("taskId=" + taskId);

                try {
                  result = imageSynthesis.wait(taskId, apiKey);
                } catch (ApiException | NoApiKeyException e){
                  throw new RuntimeException(e.getMessage());
                }
                System.out.println(JsonUtils.toJson(result));
                System.out.println(JsonUtils.toJson(result.getOutput()));
              }

              public static void listTask() throws ApiException, NoApiKeyException {
                ImageSynthesis is = new ImageSynthesis();
                AsyncTaskListParam param = AsyncTaskListParam.builder().build();
                param.setApiKey(apiKey);
                ImageSynthesisListResult result = is.list(param);
                System.out.println(result);
              }

              public void fetchTask(String taskId) throws ApiException, NoApiKeyException {
                ImageSynthesis is = new ImageSynthesis();
                ImageSynthesisResult result = is.fetch(taskId, apiKey);
                System.out.println(result.getOutput());
                System.out.println(result.getUsage());
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
    Wan25ImageEditRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wan2.5-i2i-preview
          example: wan2.5-i2i-preview
        input:
          $ref: "#/components/schemas/Wan25ImageEditInput"
        parameters:
          $ref: "#/components/schemas/Wan25ImageEditParameters"
    Wan25ImageEditInput:
      type: object
      required:
        - prompt
        - images
      description: 图像编辑的输入数据。
      properties:
        prompt:
          type: string
          description: 正向提示词，描述生成图像中需要包含的元素和视觉特征。支持中英文。最多 2,000 个字符，超出部分将被截断。
          example: Change the floral dress to a vintage-style lace long dress with exquisite embroidery details on the collar and cuffs.
        images:
          type: array
          description: |-
            输入图像 URL 数组。每次请求最多支持 3 张图像。多张图像时，数组顺序定义图像序号（图像 1、图像 2 等）。

            **图像限制：**
            - 支持格式：JPEG、JPG、PNG、BMP 和 WEBP。PNG alpha 通道将被忽略。
            - 分辨率：宽和高均须在 384 到 5,000 像素之间。
            - 最大文件大小：10 MB。

            **支持的输入格式：**
            - **公开 URL**：支持 HTTP 和 HTTPS。
            - **Base64 编码字符串**：格式：`data:{MIME_type};base64,{base64_data}`。
            - **本地文件路径**：格式：`file://{绝对路径}`（仅适用于 SDK 调用）。
          items:
            type: string
          minItems: 1
          maxItems: 3
          example:
            - https://img.alicdn.com/imgextra/i2/O1CN01vHOj4h28jOxUJPwY8_!!6000000007968-49-tps-1344-896.webp
        negative_prompt:
          type: string
          description: 反向提示词，描述生成图像中需要排除的元素。支持中英文。最多 500 个字符，超出部分将被截断。
          example: low resolution, error, worst quality, low quality, disfigured, extra fingers, bad proportions
    Wan25ImageEditParameters:
      type: object
      description: 控制输出分辨率、提示词改写、水印及其他处理选项。
      properties:
        size:
          type: string
          description: |-
            输出分辨率，格式为 `{宽度}*{高度}`。默认值：`1280*1280`。总像素数须在 589,824（768*768）到 1,638,400（1280*1280）之间，宽高比须在 1:4 到 4:1 之间。

            推荐分辨率：
            - 1280*1280 (1:1)
            - 1024*1024 (1:1)
            - 800*1200 (2:3)
            - 1200*800 (3:2)
            - 960*1280 (3:4)
            - 1280*960 (4:3)
            - 720*1280 (9:16)
            - 1280*720 (16:9)
            - 1344*576 (21:9)

            未指定时，系统默认输出 1280*1280 总像素数的图像，并保留与输入图像相近的宽高比：
            - 单图输入：宽高比与输入图像保持一致。
            - 多图输入：宽高比与最后一张输入图像保持一致。
          default: 1280*1280
          example: 1280*1280
        n:
          type: integer
          description: 生成图像的数量。有效范围：1 到 4。默认值：4。`n` 参数直接影响计费，值越大费用越高。建议测试时明确设置为 1 以控制成本。
          default: 4
          minimum: 1
          maximum: 4
          example: 1
        watermark:
          type: boolean
          description: 是否在图像右下角添加固定文字 "AI-generated" 水印。
          default: false
          example: false
        prompt_extend:
          type: boolean
          description: 开启智能提示词改写。启用后，大语言模型将优化您的提示词以获得更好的效果，但会增加处理时间。默认值：true。
          default: true
          example: true
        seed:
          type: integer
          description: 随机数种子。取值范围：[0, 2147483647]。未指定时，算法自动生成随机数作为种子。指定后，算法为每张图像（共 `n` 张）分别生成一个种子值（seed、seed+1、seed+2……）。若需复现特定结果，请使用固定种子值。注意：由于固有随机性，相同种子不一定能生成完全相同的结果。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。可在 24 小时内用于查询任务状态。
            task_status:
              type: string
              description: 任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
        request_id:
          type: string
          description: 请求的唯一标识符，可用于问题追踪与排查。
    ImageEditTaskStatusResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。可在 24 小时内用于查询任务状态。
            task_status:
              type: string
              description: 任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间，北京时间（UTC+8）。格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            scheduled_time:
              type: string
              description: 任务开始执行时间，北京时间（UTC+8）。格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            end_time:
              type: string
              description: 任务完成时间，北京时间（UTC+8）。格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            results:
              type: array
              description: 生成结果数组。每个条目包含图像 URL、提示词，或生成失败时的错误信息。
              items:
                type: object
                properties:
                  orig_prompt:
                    type: string
                    description: 原始输入提示词。
                  actual_prompt:
                    type: string
                    description: 启用提示词改写时实际使用的优化后提示词。未启用该功能时不返回。
                  url:
                    type: string
                    description: 生成图像的 URL。有效期 24 小时。
                  code:
                    type: string
                    description: 图像生成失败时的错误码。仅在部分失败时返回。
                  message:
                    type: string
                    description: 图像生成失败时的错误信息。仅在部分失败时返回。
            task_metrics:
              type: object
              description: 任务结果统计信息。
              properties:
                TOTAL:
                  type: integer
                  description: 任务总数。
                SUCCEEDED:
                  type: integer
                  description: 成功任务数。
                FAILED:
                  type: integer
                  description: 失败任务数。
            code:
              type: string
              description: 错误码。仅在任务失败时返回。
            message:
              type: string
              description: 详细错误信息。仅在任务失败时返回。
        usage:
          type: object
          description: 输出统计信息。仅统计成功生成的结果。
          properties:
            image_count:
              type: integer
              description: 成功生成的图像数量。计费公式：费用 = 图像数量 × 单价。
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 标识错误类型的错误码。
        message:
          type: string
          description: 详细错误信息。
        request_id:
          type: string
          description: 用于问题排查的唯一请求标识符。
````
