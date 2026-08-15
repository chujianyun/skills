> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.7 — 创建任务

> Wan 2.7 异步图像生成与编辑

<Note>
  [获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

图像生成任务通常需要 1 到 2 分钟。为避免请求超时，可使用异步 API 将流程拆分为两步：

1. **创建任务**（本接口），获取 `task_id`。
2. **[查询结果](/api-reference/image-generation/wan27-image-gen-edit/query-result)**，使用 `task_id` 轮询任务状态。

请求体与[同步接口](/api-reference/image-generation/wan27-image-gen-edit/synchronous)使用相同的 `messages` 格式和参数，但需要添加 `X-DashScope-Async: enable` 请求头。

## OpenAPI

````yaml post /services/aigc/image-generation/generation
openapi: 3.1.0
info:
  title: Wan2.7 图像生成与编辑 API
  description: Wan2.7 图像生成与编辑 API，支持文生图、多图编辑、边界框交互式编辑以及图像集生成。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 北京
security:
  - BearerAuth: []
paths:
  /services/aigc/image-generation/generation:
    post:
      operationId: createWan27ImageTask
      summary: 创建图像生成任务
      description: |-
        创建异步图像生成或编辑任务。请求体格式与同步接口相同，但需要在请求头中添加 `X-DashScope-Async: enable`。

        图像生成任务通常需要 1 到 2 分钟。建议使用异步 API 以避免请求超时。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步处理配置。**必须设置为 `enable`**。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Wan27ImageRequest"
      responses:
        "200":
          description: 任务创建成功。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求参数无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL (text-to-image, async)
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
            --header 'Content-Type: application/json' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'X-DashScope-Async: enable' \
            --data '{
              "model": "wan2.7-image-pro",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "text": "A flower shop with exquisite windows, a beautiful wooden door, and flowers on display"
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "n": 1,
                "size": "2K",
                "watermark": false,
                "thinking_mode": true
              }
            }'
        - lang: curl
          label: cURL (image editing, async)
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
            --header 'Content-Type: application/json' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'X-DashScope-Async: enable' \
            --data '{
              "model": "wan2.7-image-pro",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"
                      },
                      {
                        "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"
                      },
                      {
                        "text": "Spray the graffiti from image 2 onto the car in image 1"
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "n": 1,
                "size": "2K",
                "watermark": false
              }
            }'
        - lang: curl
          label: cURL (interactive editing, async)
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
            --header 'Content-Type: application/json' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'X-DashScope-Async: enable' \
            --data '{
              "model": "wan2.7-image-pro",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "image": "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"
                      },
                      {
                        "image": "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"
                      },
                      {
                        "text": "Place the alarm clock from image 1 in the selected area of image 2, ensuring the scene and lighting blend naturally"
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "n": 1,
                "size": "2K",
                "watermark": false,
                "bbox_list": [[], [[989, 515, 1138, 681]]]
              }
            }'
        - lang: curl
          label: cURL (image set generation, async)
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
            --header 'Content-Type: application/json' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'X-DashScope-Async: enable' \
            --data '{
              "model": "wan2.7-image-pro",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "text": "Cinematic image group, documenting the same stray orange cat, features must be consistent throughout. First image: Spring, an orange cat walks under blooming cherry trees; Second image: Summer, an orange cat rests in the shade of an old street to escape the heat; Third image: Autumn, an orange cat walks on golden fallen leaves; Fourth image: Winter, an orange cat walks on snow, leaving paw prints."
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "enable_sequential": true,
                "n": 4,
                "size": "2K"
              }
            }'
        - lang: python
          label: Python - image editing (async)
          source: |-
            import os
            import base64
            import mimetypes
            import dashscope
            from dashscope.aigc.image_generation import ImageGeneration
            from dashscope.api_entities.dashscope_response import Message

            # 需要 SDK 版本 >= 1.25.15
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            api_key = os.getenv("DASHSCOPE_API_KEY")

            def encode_file(file_path):
              mime_type, _ = mimetypes.guess_type(file_path)
              if not mime_type or not mime_type.startswith("image/"):
                raise ValueError("Unsupported or unrecognized image format")
              with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
              return f"data:{mime_type};base64,{encoded_string}"

            # 图片输入支持三种方式：公开 URL、本地文件路径、Base64 编码
            image_1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"
            image_2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"
            # image_1 = "file:///path/to/your/car.png"
            # image_1 = encode_file("/path/to/your/car.png")

            message = Message(
              role="user",
              content=[
                {"text": "Spray the graffiti from image 2 onto the car in image 1"},
                {"image": image_1},
                {"image": image_2}
              ]
            )

            print("---async call for image editing, creating task----")
            response = ImageGeneration.async_call(
              model='wan2.7-image-pro',
              api_key=api_key,
              messages=[message],
              n=1,
              # wan2.7-image-pro 文生图支持 1K、2K 或 4K；
              # 图像编辑和图像集生成最高支持 2K
              size="2K",
              watermark=False
            )

            print("Task created:", response)

            # 等待任务完成
            result = ImageGeneration.wait(task=response, api_key=api_key)
            print(result)
        - lang: python
          label: Python - image set generation (async)
          source: |-
            import os
            import base64
            import mimetypes
            import dashscope
            from dashscope.aigc.image_generation import ImageGeneration
            from dashscope.api_entities.dashscope_response import Message

            # 需要 SDK 版本 >= 1.25.15
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            api_key = os.getenv("DASHSCOPE_API_KEY")

            def encode_file(file_path):
              mime_type, _ = mimetypes.guess_type(file_path)
              if not mime_type or not mime_type.startswith("image/"):
                raise ValueError("Unsupported or unrecognized image format")
              with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
              return f"data:{mime_type};base64,{encoded_string}"

            # 文生图像集（默认）
            message = Message(
              role="user",
              content=[
                {"text": "Cinematic image group, documenting the same stray orange cat, features must be consistent throughout. First image: Spring, an orange cat walks under blooming cherry trees; Second image: Summer, an orange cat rests in the shade of an old street to escape the heat; Third image: Autumn, an orange cat walks on golden fallen leaves; Fourth image: Winter, an orange cat walks on snow, leaving paw prints."}
              ]
            )

            # 图生图像集（取消注释后使用）
            # 图片输入支持三种方式：公开 URL、本地文件路径、Base64 编码
            # image_1 = "https://example.com/your-image.png"
            # image_1 = "file:///path/to/your/image.png"
            # image_1 = encode_file("/path/to/your/image.png")
            # message = Message(
            #   role="user",
            #   content=[
            #     {"text": "Generate a sequential image set based on the input image"},
            #     {"image": image_1}
            #   ]
            # )

            print("---async call for image set generation, creating task----")
            response = ImageGeneration.async_call(
              model='wan2.7-image-pro',
              api_key=api_key,
              messages=[message],
              enable_sequential=True,
              n=4,
              # wan2.7-image-pro 文生图支持 1K、2K 或 4K；
              # 图像编辑和图像集生成最高支持 2K
              size="2K"
            )

            print("Task created:", response)

            # 等待任务完成
            result = ImageGeneration.wait(task=response, api_key=api_key)
            print(result)
        - lang: java
          label: Java - image editing (async)
          source: |-
            import com.alibaba.dashscope.aigc.imagegeneration.*;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;

            import java.io.IOException;
            import java.nio.file.Files;
            import java.nio.file.Paths;
            import java.util.Arrays;
            import java.util.Base64;
            import java.util.Collections;

            /**
             * wan2.7-image-pro 图像编辑 - 异步调用示例
             * 需要 SDK 版本 >= 2.22.13
             */
            public class Main {

                static {
                    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                }

                static String apiKey = System.getenv("DASHSCOPE_API_KEY");

                public static String encodeFile(String filePath) throws IOException {
                    byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
                    String base64String = Base64.getEncoder().encodeToString(fileContent);
                    String mimeType = Files.probeContentType(Paths.get(filePath));
                    return "data:" + mimeType + ";base64," + base64String;
                }

                public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException {
                    // 图片输入支持三种方式：公开 URL、本地文件路径、Base64 编码
                    String image1 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp";
                    String image2 = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp";
                    // String image1 = "file:///path/to/your/car.png";
                    // String image1 = encodeFile("/path/to/your/car.png");

                    ImageGenerationMessage message = ImageGenerationMessage.builder()
                            .role("user")
                            .content(Arrays.asList(
                                    Collections.singletonMap("text", "Spray the graffiti from image 2 onto the car in image 1"),
                                    Collections.singletonMap("image", image1),
                                    Collections.singletonMap("image", image2)
                            )).build();

                    ImageGenerationParam param = ImageGenerationParam.builder()
                            .apiKey(apiKey)
                            .model("wan2.7-image-pro")
                            .n(1)
                            // wan2.7-image-pro 文生图支持 1K、2K 或 4K；
                            // 图像编辑和图像集生成最高支持 2K
                            .size("2K")
                            .messages(Arrays.asList(message))
                            .build();

                    ImageGeneration imageGeneration = new ImageGeneration();
                    ImageGenerationResult result = null;
                    try {
                        System.out.println("---asynchronous call for image editing, creating task----");
                        result = imageGeneration.asyncCall(param);
                    } catch (ApiException | NoApiKeyException | UploadFileException e) {
                        throw new RuntimeException(e.getMessage());
                    }
                    System.out.println("Task creation result:");
                    System.out.println(JsonUtils.toJson(result));

                    String taskId = result.getOutput().getTaskId();
                    waitTask(taskId);
                }

                public static void waitTask(String taskId) throws ApiException, NoApiKeyException {
                    ImageGeneration imageGeneration = new ImageGeneration();
                    System.out.println("\n---waiting for task completion----");
                    ImageGenerationResult result = imageGeneration.wait(taskId, apiKey);
                    System.out.println("Task completion result:");
                    System.out.println(JsonUtils.toJson(result));
                }

                public static void main(String[] args) {
                    try {
                        asyncCall();
                    } catch (ApiException | NoApiKeyException | UploadFileException e) {
                        System.out.println(e.getMessage());
                    }
                }
            }
        - lang: java
          label: Java - image set generation (async)
          source: |-
            import com.alibaba.dashscope.aigc.imagegeneration.*;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;

            import java.io.IOException;
            import java.nio.file.Files;
            import java.nio.file.Paths;
            import java.util.Arrays;
            import java.util.Base64;
            import java.util.Collections;

            /**
             * wan2.7-image-pro 图像集生成 - 异步调用示例
             * 需要 SDK 版本 >= 2.22.13
             */
            public class Main {

                static {
                    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                }

                static String apiKey = System.getenv("DASHSCOPE_API_KEY");

                public static String encodeFile(String filePath) throws IOException {
                    byte[] fileContent = Files.readAllBytes(Paths.get(filePath));
                    String base64String = Base64.getEncoder().encodeToString(fileContent);
                    String mimeType = Files.probeContentType(Paths.get(filePath));
                    return "data:" + mimeType + ";base64," + base64String;
                }

                public static ImageGenerationResult waitTask(String taskId)
                        throws ApiException, NoApiKeyException {
                    ImageGeneration imageGeneration = new ImageGeneration();
                    return imageGeneration.wait(taskId, apiKey);
                }

                public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException {
                    // 文生图像集（默认）
                    ImageGenerationMessage message = ImageGenerationMessage.builder()
                            .role("user")
                            .content(Collections.singletonList(
                                    Collections.singletonMap("text", "Cinematic image group, documenting the same stray orange cat, features must be consistent throughout. First image: Spring, an orange cat walks under blooming cherry trees; Second image: Summer, an orange cat rests in the shade of an old street to escape the heat; Third image: Autumn, an orange cat walks on golden fallen leaves; Fourth image: Winter, an orange cat walks on snow, leaving paw prints.")
                            )).build();

                    // 图生图像集（取消注释后使用）
                    // 图片输入支持三种方式：公开 URL、本地文件路径、Base64 编码
                    // String image1 = "https://example.com/your-image.png";
                    // String image1 = "file:///path/to/your/image.png";
                    // String image1 = encodeFile("/path/to/your/image.png");
                    // ImageGenerationMessage message = ImageGenerationMessage.builder()
                    //         .role("user")
                    //         .content(Arrays.asList(
                    //                 Collections.singletonMap("text", "Generate a sequential image set based on the input image"),
                    //                 Collections.singletonMap("image", image1)
                    //         )).build();

                    ImageGenerationParam param = ImageGenerationParam.builder()
                            .apiKey(apiKey)
                            .model("wan2.7-image-pro")
                            .messages(Collections.singletonList(message))
                            .enableSequential(true)
                            .n(4)
                            // wan2.7-image-pro 文生图支持 1K、2K 或 4K；
                            // 图像编辑和图像集生成最高支持 2K
                            .size("2K")
                            .build();

                    ImageGeneration imageGeneration = new ImageGeneration();
                    ImageGenerationResult taskResult = null;
                    try {
                        System.out.println("----async call, creating task----");
                        taskResult = imageGeneration.asyncCall(param);
                    } catch (ApiException | NoApiKeyException | UploadFileException e) {
                        throw new RuntimeException(e.getMessage());
                    }
                    System.out.println("Task created: " + JsonUtils.toJson(taskResult));

                    String taskId = taskResult.getOutput().getTaskId();
                    ImageGenerationResult result = waitTask(taskId);
                    System.out.println(JsonUtils.toJson(result));
                }

                public static void main(String[] args) {
                    try {
                        asyncCall();
                    } catch (ApiException | NoApiKeyException | UploadFileException e) {
                        System.out.println(e.getMessage());
                    }
                }
            }
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan27ImageRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。可选值：wan2.7-image-pro、wan2.7-image。
          enum:
            - wan2.7-image-pro
            - wan2.7-image
          example: wan2.7-image-pro
        input:
          type: object
          required:
            - messages
          description: 包含消息数组的输入数据。
          properties:
            messages:
              type: array
              description: 请求内容数组。目前仅支持单轮对话，即只能传入一组 role 和 content 参数，不支持多轮对话。
              minItems: 1
              maxItems: 1
              items:
                $ref: "#/components/schemas/Wan27ImageMessage"
        parameters:
          $ref: "#/components/schemas/Wan27ImageParameters"
    Wan27ImageMessage:
      type: object
      required:
        - role
        - content
      properties:
        role:
          type: string
          enum:
            - user
          description: 消息角色。必须为 `user`。
        content:
          type: array
          description: |-
            消息内容数组。必须包含一个 `text` 对象和 0 到 9 个 `image` 对象。

            使用多张图片时，在数组中放入多个 `image` 对象。图片顺序由数组位置决定。
          items:
            $ref: "#/components/schemas/Wan27ImageContentPart"
    Wan27ImageContentPart:
      type: object
      description: 图片或文本内容部分。
      properties:
        text:
          type: string
          description: 用户输入的提示词。支持中英文。长度不超过 5000 个字符（每个中文字符、字母、数字或符号均计为一个字符，超出部分自动截断）。`content` 数组中必须包含且仅包含一个 `text` 对象。
          maxLength: 5000
          example: Spray the graffiti from image 2 onto the car in image 1
        image:
          type: string
          description: |-
            输入图片，支持公开 URL（HTTP/HTTPS）或 Base64 编码字符串（`data:{mime_type};base64,{data}`）。

            **图片约束：**
            - 格式：JPEG、JPG、PNG（不支持 Alpha 通道）、BMP、WEBP。
            - 分辨率：宽和高各自在 240 到 8000 像素之间，宽高比在 [1:8, 8:1] 范围内。
            - 文件大小：最大 20 MB。
            - 数量：每次请求最多 9 张图片。
          example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp
    Wan27ImageParameters:
      type: object
      description: 图像处理参数。
      properties:
        size:
          type: string
          description: |-
            输出图像分辨率。支持两种指定方式，不可同时使用。

            **wan2.7-image-pro：**
            - 方式一（推荐）：`1K`、`2K`（默认）或 `4K`。
              - 适用范围：文生图（无图片输入，且非图像集生成模式）支持 1K、2K 和 4K；其他场景仅支持 1K 和 2K。
              - 总像素数：1K = 1024×1024，2K = 2048×2048，4K = 4096×4096。
              - 宽高比：有图片输入时，输出图像按最后一张输入图片的宽高比缩放到对应分辨率；无图片输入时，输出为正方形。
            - 方式二：以 `width*height` 形式指定像素数，宽高比在 [1:8, 8:1] 范围内。
              - 文生图：总像素数在 [768×768, 4096×4096] 范围内。
              - 其他场景：总像素数在 [768×768, 2048×2048] 范围内。

            **wan2.7-image：**
            - 方式一（推荐）：`1K` 或 `2K`（默认），不支持 4K。
            - 方式二：以 `width*height` 形式指定像素数。所有场景总像素数在 [768×768, 2048×2048] 范围内，宽高比在 [1:8, 8:1] 范围内。

            输出图像的实际像素值可能与指定值略有差异。
          example: 2K
        n:
          type: integer
          description: |-
            生成图像的数量。

            **注意：** `n` 的值直接影响费用。费用 = 单价 × 成功生成的图像数量。

            - 未启用图像集模式（`enable_sequential=false`）：表示生成图像的数量，范围 1–4，默认为 4。
            - 启用图像集模式（`enable_sequential=true`）：表示最多生成的图像数量，范围 1–12，默认为 12。实际数量由模型决定，不超过 `n`。
          minimum: 1
          maximum: 12
          default: 4
        enable_sequential:
          type: boolean
          description: |-
            控制图像生成模式。
            - `false`：默认值。
            - `true`：启用图像集输出模式。
          default: false
        thinking_mode:
          type: boolean
          description: 是否启用思考模式。默认为 `true`（启用）。仅在未启用图像集模式且无图片输入时生效。启用后，模型将增强推理能力以提升图像质量，但会增加生成时间。
          default: true
        bbox_list:
          type: array
          description: |-
            交互式编辑的选区。

            - 对应关系：列表长度必须与输入图片数量一致。若某张图片无需编辑，对应位置传入空列表 `[]`。
            - 坐标格式：`[x1, y1, x2, y2]`（左上角 x、左上角 y、右下角 x、右下角 y），使用原始图片的绝对像素坐标，左上角为 (0, 0)。
            - 限制：单张图片最多支持 2 个边界框。
          items:
            type: array
            description: 单张输入图片的边界框列表。空数组表示无边界框。
            items:
              type: array
              description: 单个边界框 [x1, y1, x2, y2]。
              items:
                type: integer
              minItems: 4
              maxItems: 4
            maxItems: 2
        color_palette:
          type: array
          description: 自定义色彩主题。由颜色（`hex`）和比例（`ratio`）对象组成的数组，须包含 3 到 10 种颜色（推荐设置为 8 种）。仅在未启用图像集模式（`enable_sequential=false`）时可用。
          minItems: 3
          maxItems: 10
          items:
            type: object
            required:
              - hex
              - ratio
            properties:
              hex:
                type: string
                description: 十六进制（HEX）格式的颜色值。示例：`#C2D1E6`。
              ratio:
                type: string
                description: 该颜色的占比，精确到小数点后两位（例如 `"25.00%"`）。所有 `ratio` 值之和必须为 100.00%。
          example:
            - hex: "#C2D1E6"
              ratio: 60.00%
            - hex: "#636574"
              ratio: 25.00%
            - hex: "#CBD4E4"
              ratio: 15.00%
        watermark:
          type: boolean
          description: 在图像右下角添加固定文字水印"AI Generated"。
          default: false
        seed:
          type: integer
          description: 随机数种子。有效范围：[0, 2147483647]。使用相同种子可生成相似结果。若不指定，算法将使用随机种子。注意：图像生成具有概率性，即使使用相同种子，结果也可能存在差异。
          minimum: 0
          maximum: 2147483647
    Wan27ImageResponse:
      type: object
      description: Wan2.7 图像生成响应。
      example:
        output:
          choices:
            - finish_reason: stop
              message:
                content:
                  - image: https://dashscope-result.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx
                    type: image
                role: assistant
          finished: true
        usage:
          image_count: 1
          input_tokens: 18790
          output_tokens: 2
          size: 2985*1405
          total_tokens: 18792
        request_id: a3f4befe-cacd-49c9-8298-xxxxxx
      properties:
        output:
          type: object
          properties:
            choices:
              type: array
              description: 生成结果列表。
              items:
                $ref: "#/components/schemas/Wan27ImageChoice"
            finished:
              type: boolean
              description: 生成是否已完成。
        usage:
          type: object
          description: 用量统计。
          properties:
            image_count:
              type: integer
              description: 已生成的图像数量。
            input_tokens:
              type: integer
              description: 消耗的输入 token 数量。
            output_tokens:
              type: integer
              description: 消耗的输出 token 数量。
            total_tokens:
              type: integer
              description: 消耗的总 token 数量。
            size:
              type: string
              description: 实际输出图像尺寸（宽×高）。
              example: 2985*1405
        request_id:
          type: string
          description: 唯一请求标识符。
          example: a3f4befe-cacd-49c9-8298-xxxxxx
    Wan27ImageChoice:
      type: object
      properties:
        finish_reason:
          type: string
          description: 生成完成的原因。
          example: stop
        message:
          type: object
          properties:
            role:
              type: string
              example: assistant
            content:
              type: array
              items:
                type: object
                properties:
                  image:
                    type: string
                    description: 生成图像的 URL。**URL 在 24 小时后失效，请及时下载保存。**
                    example: https://dashscope-result.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx
                  type:
                    type: string
                    example: image
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交成功后返回的响应。
      example:
        request_id: ccf4b2f4-bf30-9e13-9461-3a28c6a7bxxx
        output:
          task_id: 8811b4a4-00ac-4aa2-a2fd-017d3b90cxxx
          task_status: PENDING
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
          example: ccf4b2f4-bf30-9e13-9461-3a28c6a7bxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符。用于轮询结果接口，24 小时内有效。
              example: 8811b4a4-00ac-4aa2-a2fd-017d3b90cxxx
            task_status:
              type: string
              description: 初始任务状态。创建完成后始终为 `PENDING`。
              example: PENDING
    Wan27TaskStatusResponse:
      type: object
      description: 任务状态查询接口的响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
          example: 43d9e959-25bc-4dc7-9888-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符。
              example: 858cad55-4bdc-4ba3-ae6c-xxxxxx
            task_status:
              type: string
              description: 当前任务状态：`PENDING`（排队中）、`RUNNING`（处理中）、`SUCCEEDED`（已完成）、`FAILED`（失败）、`CANCELED`（已取消）、`UNKNOWN`（任务 ID 无效或已过期）。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
              example: SUCCEEDED
            submit_time:
              type: string
              description: 任务提交时间。
              example: 2026-03-31 19:57:58.840
            scheduled_time:
              type: string
              description: 任务调度时间。
              example: 2026-03-31 19:57:58.877
            end_time:
              type: string
              description: 任务完成时间。
              example: 2026-03-31 19:58:11.563
            finished:
              type: boolean
              description: 任务是否已结束。
              example: true
            choices:
              type: array
              description: 已生成的图像。仅在 `task_status` 为 `SUCCEEDED` 时存在。
              items:
                $ref: "#/components/schemas/Wan27ImageChoice"
            code:
              type: string
              description: 错误码。仅在 `task_status` 为 `FAILED` 时存在。
            message:
              type: string
              description: 错误信息。仅在 `task_status` 为 `FAILED` 时存在。
        usage:
          type: object
          description: 用量统计。仅在 `task_status` 为 `SUCCEEDED` 时存在。
          properties:
            image_count:
              type: integer
              description: 已生成的图像数量。
            input_tokens:
              type: integer
              description: 消耗的输入 token 数量。
            output_tokens:
              type: integer
              description: 消耗的输出 token 数量。
            total_tokens:
              type: integer
              description: 消耗的总 token 数量。
            size:
              type: string
              description: 实际输出图像尺寸。
              example: 2985*1405
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 错误码。
          example: InvalidParameter
        message:
          type: string
          description: 错误信息。
          example: Invalid parameter value
        request_id:
          type: string
          description: 唯一请求标识符。
          example: a3f4befe-cacd-49c9-8298-xxxxxx
````
