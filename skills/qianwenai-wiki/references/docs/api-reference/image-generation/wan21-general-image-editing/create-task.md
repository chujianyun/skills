> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.1 — 创建任务

> 异步 Wan 2.1 通用图像编辑

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

支持 10 种图像编辑功能：

| 功能     | `function` 值                 | 说明         |
| ------ | ---------------------------- | ---------- |
| 整图风格化  | `stylization_all`            | 整体风格迁移     |
| 局部风格化  | `stylization_local`          | 局部风格迁移     |
| 指令编辑   | `description_edit`           | 根据文字描述编辑图像 |
| 蒙版编辑   | `description_edit_with_mask` | 结合蒙版的精准编辑  |
| 去水印    | `remove_watermark`           | 去除图片水印     |
| 扩图     | `expand`                     | 向四个方向扩展画布  |
| 超分辨率   | `super_resolution`           | 提高图像分辨率    |
| 上色     | `colorization`               | 为黑白图片上色    |
| 涂鸦成图   | `doodle`                     | 基于涂鸦生成图像   |
| 卡通特征控制 | `control_cartoon_feature`    | 保持人物特征的卡通化 |

## OpenAPI

````yaml post /services/aigc/image2image/image-synthesis
openapi: 3.1.0
info:
  title: Wan2.1 通用图像编辑 API
  description: Wan 2.1 通用图像编辑 API。支持 10 种编辑功能：整图风格化、局部风格化、指令编辑、蒙版编辑、去水印、扩图、超分辨率、上色、涂鸦成图、卡通特征控制。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /services/aigc/image2image/image-synthesis:
    post:
      operationId: createWan21ImageEdit
      summary: 创建图像编辑任务
      description: 使用 Wan 2.1 创建图像编辑任务。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 启用异步处理，必须设置为 `enable`。HTTP 请求仅支持异步调用，省略此 Header 会返回错误。
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
              $ref: "#/components/schemas/Wan21ImageEditRequest"
      responses:
        "200":
          description: 任务提交成功。使用 `task_id` 轮询结果。
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
          description: 认证失败，API Key 无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidApiKey
                message: Invalid API-key provided.
                request_id: 7438d53d-6eb8-4596-8835-xxxxxx
      x-codeSamples:
        - lang: curl
          label: 整图风格化 stylization_all
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wanx2.1-imageedit",
              "input": {
                "function": "stylization_all",
                "prompt": "转换成法国绘本风格",
                "base_image_url": "http://wanx.alicdn.com/material/20250318/stylization_all_1.jpeg"
              },
              "parameters": {
                "n": 1
              }
            }'
        - lang: curl
          label: Base64 编码输入
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wanx2.1-imageedit",
              "input": {
                "function": "stylization_all",
                "prompt": "转换成法国绘本风格",
                "base_image_url": "data:image/jpeg;base64,/9j/4AAQSkZJR......"
              },
              "parameters": {
                "n": 1
              }
            }'
        - lang: curl
          label: 局部风格化 stylization_local
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wanx2.1-imageedit",
              "input": {
                "function": "stylization_local",
                "prompt": "把房子变成木板风格。",
                "base_image_url": "http://wanx.alicdn.com/material/20250318/stylization_local_1.png"
              },
              "parameters": {
                "n": 1
              }
            }'
        - lang: curl
          label: 指令编辑 description_edit
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wanx2.1-imageedit",
              "input": {
                "function": "description_edit",
                "prompt": "把她的头发修改为红色。",
                "base_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_2.png"
              },
              "parameters": {
                "n": 1
              }
            }'
        - lang: curl
          label: 蒙版编辑 description_edit_with_mask
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wanx2.1-imageedit",
              "input": {
                "function": "description_edit_with_mask",
                "prompt": "陶瓷兔子拿着陶瓷小花。",
                "base_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg",
                "mask_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
              },
              "parameters": {
                "n": 1
              }
            }'
        - lang: curl
          label: 去水印 remove_watermark
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wanx2.1-imageedit",
              "input": {
                "function": "remove_watermark",
                "prompt": "去除图像中的文字",
                "base_image_url": "http://wanx.alicdn.com/material/20250318/remove_watermark_1.png"
              },
              "parameters": {
                "n": 1
              }
            }'
        - lang: curl
          label: 扩图 expand
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wanx2.1-imageedit",
              "input": {
                "function": "expand",
                "prompt": "一位绿色仙子",
                "base_image_url": "http://wanx.alicdn.com/material/20250318/expand_2.jpg"
              },
              "parameters": {
                "top_scale": 1.5,
                "bottom_scale": 1.5,
                "left_scale": 1.5,
                "right_scale": 1.5,
                "n": 1
              }
            }'
        - lang: curl
          label: 超分辨率 super_resolution
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wanx2.1-imageedit",
              "input": {
                "function": "super_resolution",
                "prompt": "图像超分。",
                "base_image_url": "http://wanx.alicdn.com/material/20250318/super_resolution_1.jpeg"
              },
              "parameters": {
                "upscale_factor": 2,
                "n": 1
              }
            }'
        - lang: curl
          label: 上色 colorization
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wanx2.1-imageedit",
              "input": {
                "function": "colorization",
                "prompt": "蓝色背景，黄色的叶子。",
                "base_image_url": "http://wanx.alicdn.com/material/20250318/colorization_1.jpeg"
              },
              "parameters": {
                "n": 1
              }
            }'
        - lang: curl
          label: 涂鸦成图 doodle
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wanx2.1-imageedit",
              "input": {
                "function": "doodle",
                "prompt": "北欧极简风格的客厅。",
                "base_image_url": "http://wanx.alicdn.com/material/20250318/doodle_1.png"
              },
              "parameters": {
                "n": 1
              }
            }'
        - lang: curl
          label: 卡通特征控制 control_cartoon_feature
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wanx2.1-imageedit",
              "input": {
                "function": "control_cartoon_feature",
                "prompt": "卡通形象小心翼翼地探出头，窥视着房间内一颗璀璨的蓝色宝石。",
                "base_image_url": "http://wanx.alicdn.com/material/20250318/control_cartoon_feature_1.png"
              },
              "parameters": {
                "n": 1
              }
            }'
        - lang: python
          label: Python SDK（同步）
          source: |-
            import base64
            import os
            from http import HTTPStatus
            from dashscope import ImageSynthesis
            import mimetypes

            api_key = os.getenv("DASHSCOPE_API_KEY")

            def encode_file(file_path):
              mime_type, _ = mimetypes.guess_type(file_path)
              if not mime_type or not mime_type.startswith("image/"):
                raise ValueError("不支持或无法识别的图像格式")
              with open(file_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
              return f"data:{mime_type};base64,{encoded_string}"

            # 【方式一】使用公网图片 URL
            mask_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
            base_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg"

            # 【方式二】使用本地文件
            # mask_image_url = "file://" + "/path/to/your/mask_image.png"
            # base_image_url = "file://" + "C:/path/to/your/base_image.jpeg"

            # 【方式三】使用Base64编码的图片
            # mask_image_url = encode_file("./mask_image.png")
            # base_image_url = encode_file("./base_image.jpeg")

            def sample_sync_call_imageedit():
              print('please wait...')
              rsp = ImageSynthesis.call(api_key=api_key,
                                        model="wanx2.1-imageedit",
                                        function="description_edit_with_mask",
                                        prompt="陶瓷兔子拿着陶瓷小花",
                                        mask_image_url=mask_image_url,
                                        base_image_url=base_image_url,
                                        n=1)
              assert rsp.status_code == HTTPStatus.OK
              print('response: %s' % rsp)
              if rsp.status_code == HTTPStatus.OK:
                for result in rsp.output.results:
                  print("---------------------------")
                  print(result.url)
              else:
                print('sync_call Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))

            if __name__ == '__main__':
              sample_sync_call_imageedit()
        - lang: python
          label: Python SDK（异步）
          source: |-
            import os
            from http import HTTPStatus
            from dashscope import ImageSynthesis

            api_key = os.getenv("DASHSCOPE_API_KEY")
            mask_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
            base_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg"

            def sample_async_call_imageedit():
              rsp = ImageSynthesis.async_call(api_key=api_key,
                                              model="wanx2.1-imageedit",
                                              function="description_edit_with_mask",
                                              prompt="陶瓷兔子拿着陶瓷小花",
                                              mask_image_url=mask_image_url,
                                              base_image_url=base_image_url,
                                              n=1)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print("task_id: %s" % rsp.output.task_id)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))
              status = ImageSynthesis.fetch(task=rsp, api_key=api_key)
              if status.status_code == HTTPStatus.OK:
                print(status.output.task_status)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (status.status_code, status.code, status.message))
              rsp = ImageSynthesis.wait(rsp)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output)
                for result in rsp.output.results:
                  print("---------------------------")
                  print(result.url)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))

            if __name__ == '__main__':
              sample_async_call_imageedit()
        - lang: java
          label: Java SDK（同步）
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.JsonUtils;
            import java.io.IOException;
            import java.nio.file.Files;
            import java.nio.file.Path;
            import java.nio.file.Paths;
            import java.util.Base64;
            import java.util.HashMap;
            import java.util.Map;

            public class ImageEditSync {
              static String apiKey = System.getenv("DASHSCOPE_API_KEY");
              static String maskImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png";
              static String baseImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg";

              public static void syncCall() {
                Map<String, Object> parameters = new HashMap<>();
                parameters.put("prompt_extend", true);
                ImageSynthesisParam param =
                    ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wanx2.1-imageedit")
                        .function(ImageSynthesis.ImageEditFunction.DESCRIPTION_EDIT_WITH_MASK)
                        .prompt("陶瓷兔子拿着陶瓷小花")
                        .maskImageUrl(maskImageUrl)
                        .baseImageUrl(baseImageUrl)
                        .n(1)
                        .size("1024*1024")
                        .parameters(parameters)
                        .build();
                ImageSynthesis imageSynthesis = new ImageSynthesis();
                ImageSynthesisResult result = null;
                try {
                  System.out.println("---sync call, please wait a moment----");
                  result = imageSynthesis.call(param);
                } catch (ApiException | NoApiKeyException e){
                  throw new RuntimeException(e.getMessage());
                }
                System.out.println(JsonUtils.toJson(result));
              }

              public static String encodeFile(String filePath) {
                Path path = Paths.get(filePath);
                if (!Files.exists(path)) { throw new IllegalArgumentException("文件不存在: " + filePath); }
                String mimeType = null;
                try { mimeType = Files.probeContentType(path); } catch (IOException e) { throw new IllegalArgumentException("无法检测文件类型: " + filePath); }
                if (mimeType == null || !mimeType.startsWith("image/")) { throw new IllegalArgumentException("不支持或无法识别的图像格式"); }
                byte[] fileBytes = null;
                try { fileBytes = Files.readAllBytes(path); } catch (IOException e) { throw new IllegalArgumentException("无法读取文件内容: " + filePath); }
                String encodedString = Base64.getEncoder().encodeToString(fileBytes);
                return "data:" + mimeType + ";base64," + encodedString;
              }

              public static void main(String[] args) { syncCall(); }
            }
        - lang: java
          label: Java SDK（异步）
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.task.AsyncTaskListParam;
            import com.alibaba.dashscope.utils.JsonUtils;
            import java.util.HashMap;
            import java.util.Map;

            public class ImageEditAsync {
              static String apiKey = System.getenv("DASHSCOPE_API_KEY");
              static String maskImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png";
              static String baseImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg";

              public static void asyncCall() {
                Map<String, Object> parameters = new HashMap<>();
                parameters.put("prompt_extend", true);
                ImageSynthesisParam param =
                    ImageSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wanx2.1-imageedit")
                        .function(ImageSynthesis.ImageEditFunction.DESCRIPTION_EDIT_WITH_MASK)
                        .prompt("陶瓷兔子拿着陶瓷小花")
                        .maskImageUrl(maskImageUrl)
                        .baseImageUrl(baseImageUrl)
                        .n(1)
                        .size("1024*1024")
                        .parameters(parameters)
                        .build();
                ImageSynthesis imageSynthesis = new ImageSynthesis();
                ImageSynthesisResult result = null;
                try {
                  System.out.println("---async call, please wait a moment----");
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

              public static void main(String[] args) { asyncCall(); }
            }
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan21ImageEditRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wanx2.1-imageedit
          example: wanx2.1-imageedit
        input:
          $ref: "#/components/schemas/Wan21ImageEditInput"
        parameters:
          $ref: "#/components/schemas/Wan21ImageEditParameters"
    Wan21ImageEditInput:
      type: object
      required:
        - function
        - prompt
        - base_image_url
      description: 图像编辑的输入数据。
      properties:
        function:
          type: string
          description: |-
            编辑功能类型。

            | 值 | 功能 |
            |---|---|
            | `stylization_all` | 整图风格化 |
            | `stylization_local` | 局部风格化 |
            | `description_edit` | 指令编辑 |
            | `description_edit_with_mask` | 蒙版编辑（需要 `mask_image_url`） |
            | `remove_watermark` | 去水印 |
            | `expand` | 扩图 |
            | `super_resolution` | 超分辨率 |
            | `colorization` | 上色 |
            | `doodle` | 涂鸦成图 |
            | `control_cartoon_feature` | 卡通特征控制 |
          enum:
            - stylization_all
            - stylization_local
            - description_edit
            - description_edit_with_mask
            - remove_watermark
            - expand
            - super_resolution
            - colorization
            - doodle
            - control_cartoon_feature
          example: description_edit_with_mask
        prompt:
          type: string
          description: 文本提示词，描述对图像的编辑要求。支持中英文。最大长度：800 字符，超出部分将被截断。
          maxLength: 800
          example: 陶瓷兔子拿着陶瓷小花。
        base_image_url:
          type: string
          description: |-
            待编辑的原始图像 URL 或 Base64 编码字符串。

            **图像要求：**
            - 支持格式：JPG、JPEG、PNG、BMP、TIFF、WEBP
            - 分辨率：宽高各需在 512~4096 像素之间
            - 最大文件大小：10 MB

            **支持的输入格式：**
            - **公网 URL**：支持 HTTP 和 HTTPS
            - **Base64 编码**：格式为 `data:{MIME_type};base64,{base64_data}`
          example: http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg
        mask_image_url:
          type: string
          description: 蒙版图像 URL 或 Base64 编码字符串。仅当 `function` 为 `description_edit_with_mask` 时需要。蒙版图像中白色区域为需要编辑的区域，黑色区域为保留区域。蒙版图像的尺寸应与原始图像一致。
          example: http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png
    Wan21ImageEditParameters:
      type: object
      description: 控制输出数量、随机种子、水印等处理选项。不同编辑功能支持不同的参数。
      properties:
        n:
          type: integer
          description: 生成图片的数量。取值范围：1~4，默认值：1。
          default: 1
          minimum: 1
          maximum: 4
          example: 1
        seed:
          type: integer
          description: 随机种子。取值范围：[0, 2147483647]。不设置时算法自动生成。固定种子可复现结果，但由于固有随机性，相同种子不保证完全一致的结果。
          minimum: 0
          maximum: 2147483647
        watermark:
          type: boolean
          description: 是否在图片右下角添加固定文字 "AI生成" 水印。默认值：false。
          default: false
          example: false
        strength:
          type: number
          description: 图像修改强度。仅适用于 `stylization_all` 和 `description_edit` 功能。取值范围：0.0~1.0，默认值：0.5。值越大，生成图像与原图差异越大。
          minimum: 0
          maximum: 1
          default: 0.5
          example: 0.5
        top_scale:
          type: number
          description: 向上扩展比例。仅适用于 `expand` 功能。取值范围：1.0~2.0，默认值：1.0。例如 1.5 表示向上扩展原图高度的 50%。
          minimum: 1
          maximum: 2
          default: 1
          example: 1.5
        bottom_scale:
          type: number
          description: 向下扩展比例。仅适用于 `expand` 功能。取值范围：1.0~2.0，默认值：1.0。
          minimum: 1
          maximum: 2
          default: 1
          example: 1.5
        left_scale:
          type: number
          description: 向左扩展比例。仅适用于 `expand` 功能。取值范围：1.0~2.0，默认值：1.0。
          minimum: 1
          maximum: 2
          default: 1
          example: 1.5
        right_scale:
          type: number
          description: 向右扩展比例。仅适用于 `expand` 功能。取值范围：1.0~2.0，默认值：1.0。
          minimum: 1
          maximum: 2
          default: 1
          example: 1.5
        upscale_factor:
          type: integer
          description: 超分辨率放大倍数。仅适用于 `super_resolution` 功能。取值范围：1~4，默认值：1。
          minimum: 1
          maximum: 4
          default: 1
          example: 2
        is_sketch:
          type: boolean
          description: 是否为线稿输入。仅适用于 `doodle` 功能。默认值：false。当为 false 时，模型会先从输入图像中提取线稿；当为 true 时，直接将输入图像作为线稿使用。
          default: false
          example: false
    AsyncTaskSubmitResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，可在 24 小时内用于查询任务状态。
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
          description: 请求的唯一标识符，用于问题排查。
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
              description: 任务 ID，可在 24 小时内用于查询任务状态。
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
              description: 任务提交时间。时区为 UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            scheduled_time:
              type: string
              description: 任务开始执行时间。时区为 UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            end_time:
              type: string
              description: 任务完成时间。时区为 UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`。
            results:
              type: array
              description: 生成结果数组。每个条目包含图片 URL，或失败时的错误详情。
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: 生成图像的 URL，有效期 24 小时。
                  code:
                    type: string
                    description: 单张图片生成失败的错误码。仅在部分失败时返回。
                  message:
                    type: string
                    description: 单张图片生成失败的错误信息。仅在部分失败时返回。
            task_metrics:
              type: object
              description: 任务结果统计。
              properties:
                TOTAL:
                  type: integer
                  description: 总任务数。
                SUCCEEDED:
                  type: integer
                  description: 成功数。
                FAILED:
                  type: integer
                  description: 失败数。
            code:
              type: string
              description: 错误码。仅在任务失败时返回。
            message:
              type: string
              description: 错误详情。仅在任务失败时返回。
        usage:
          type: object
          description: 用量统计。仅统计成功的结果。
          properties:
            image_count:
              type: integer
              description: 成功生成的图片数量。计费公式：费用 = 图片数量 x 单价。
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 错误码。
        message:
          type: string
          description: 错误详情。
        request_id:
          type: string
          description: 请求的唯一标识符，用于问题排查。
````
