> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wanx — 创建任务

> 异步 wanx-x-painting 图像局部重绘

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

<Warning>
  wanx-x-painting 模型当前仅提供免费体验，免费额度用完后不可调用且不支持付费。免费额度详情请参见[免费额度](/resources/free-quota)。
</Warning>

通过指定掩码区域，使用文本提示词对图像进行局部重绘。支持多种风格，包括 3D 卡通、动画、油画、水彩、素描、中国画和扁平插画。

## OpenAPI

````yaml post /services/aigc/image2image/image-synthesis
openapi: 3.1.0
info:
  title: 万相-图像局部重绘 API
  description: 图像局部重绘 API。根据用户输入的原始图片、掩码图和 prompt 提示词，在涂抹区域生成与文字描述相对应的内容，而涂抹区域外的部分则基本保持不变。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API 端点
security:
  - BearerAuth: []
paths:
  /services/aigc/image2image/image-synthesis:
    post:
      operationId: createWanxXPaintingTask
      summary: 创建图像局部重绘任务
      description: 创建图像局部重绘任务，使用 wanx-x-painting 模型。根据输入的原始图片、掩码图和提示词，在掩码标记的区域内生成新的图像内容。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: |-
            异步处理配置参数。HTTP 请求只支持异步，必须设置为 `enable`。

            **重要：** 缺少此请求头将报错："current user api does not support synchronous calls"。
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
              $ref: "#/components/schemas/WanxXPaintingRequest"
      responses:
        "200":
          description: 任务提交成功。使用 `task_id` 轮询获取结果。
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
          description: 认证失败。API 密钥无效。
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
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
              --header 'X-DashScope-Async: enable' \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
              --header 'Content-Type: application/json' \
              --data '{
              "model": "wanx-x-painting",
              "input": {
                "prompt": "一只狗戴着红色眼镜",
                "base_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg",
                "mask_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png"
              },
              "parameters": {
                "size": "1024*1024",
                "n": 1
              }
            }'
        - lang: python
          label: Python SDK - 同步调用
          source: |-
            from http import HTTPStatus
            from urllib.parse import urlparse, unquote
            from pathlib import PurePosixPath
            import requests
            from dashscope import ImageSynthesis

            prompt = "一只狗戴着红色眼镜"
            model = "wanx-x-painting"
            task = "image2image"
            extra_input = {
              "base_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg",
              "mask_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png"
            }

            print('----sync call, please wait a moment----')
            rsp = ImageSynthesis.call(model=model,
                                      prompt=prompt,
                                      n=1,
                                      size='1024*1024',
                                      task=task,
                                      extra_input=extra_input)
            if rsp.status_code == HTTPStatus.OK:
              print(rsp)
              for result in rsp.output.results:
                file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                with open('./%s' % file_name, 'wb+') as f:
                  f.write(requests.get(result.url).content)
            else:
              print('sync_call Failed, status_code: %s, code: %s, message: %s' %
                    (rsp.status_code, rsp.code, rsp.message))
        - lang: python
          label: Python SDK - 异步调用
          source: |-
            from http import HTTPStatus
            from urllib.parse import urlparse, unquote
            from pathlib import PurePosixPath
            import requests
            from dashscope import ImageSynthesis

            prompt = "一只狗戴着红色眼镜"
            model = "wanx-x-painting"
            task = "image2image"
            extra_input = {
              "base_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg",
              "mask_image_url": "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png"
            }

            def async_call():
              print('----create task----')
              task_info = create_async_task()
              print('----wait task done then save image----')
              wait_async_task(task_info)

            def create_async_task():
              rsp = ImageSynthesis.async_call(model=model,
                                              prompt=prompt,
                                              n=1,
                                              size='1024*1024',
                                              task=task,
                                              extra_input=extra_input)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output)
              else:
                print('create_async_task Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))
              return rsp

            def wait_async_task(task):
              rsp = ImageSynthesis.wait(task)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output.task_status)
                for result in rsp.output.results:
                  file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                  with open('./%s' % file_name, 'wb+') as f:
                    f.write(requests.get(result.url).content)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' %
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
            import com.alibaba.dashscope.utils.JsonUtils;
            import java.util.HashMap;

            public class Main {
              public void syncCall() {
                String task = "image2image";
                ImageSynthesis imageSynthesis = new ImageSynthesis(task);
                ImageSynthesisParam param = genImageSynthesis();
                ImageSynthesisResult result = null;
                try {
                  System.out.println("---sync call, please wait a moment----");
                  result = imageSynthesis.call(param);
                } catch (ApiException | NoApiKeyException e){
                  throw new RuntimeException(e.getMessage());
                }
                System.out.println(JsonUtils.toJson(result));
              }

              private ImageSynthesisParam genImageSynthesis(){
                HashMap<String,Object> extraInputMap = new HashMap<>();
                extraInputMap.put("base_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg");
                extraInputMap.put("mask_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png");
                String prompt = "一只狗戴着红色眼镜";
                String model = "wanx-x-painting";
                return ImageSynthesisParam.builder()
                        .model(model)
                        .prompt(prompt)
                        .n(1)
                        .size("1024*1024")
                        .extraInputs(extraInputMap)
                        .build();
              }

              public static void main(String[] args){
                Main text2Image = new Main();
                text2Image.syncCall();
              }
            }
        - lang: java
          label: Java SDK - 异步调用
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.JsonUtils;
            import java.util.HashMap;

            public class Main {
              public void asyncCall() {
                System.out.println("---create task----");
                String taskId = this.createAsyncTask();
                System.out.println("---wait task done then return image url----");
                this.waitAsyncTask(taskId);
              }

              public String createAsyncTask() {
                String task = "image2image";
                ImageSynthesis imageSynthesis = new ImageSynthesis(task);
                ImageSynthesisParam param = genImageSynthesis();
                ImageSynthesisResult result = null;
                try {
                  result = imageSynthesis.asyncCall(param);
                } catch (ApiException | NoApiKeyException e){
                  throw new RuntimeException(e.getMessage());
                }
                String taskId = result.getOutput().getTaskId();
                System.out.println("taskId=" + taskId);
                return taskId;
              }

              private ImageSynthesisParam genImageSynthesis(){
                String prompt = "一只狗戴着红色眼镜";
                String model = "wanx-x-painting";
                HashMap<String,Object> extraInputMap = new HashMap<>();
                extraInputMap.put("base_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg");
                extraInputMap.put("mask_image_url", "http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png");
                return ImageSynthesisParam.builder()
                        .model(model)
                        .prompt(prompt)
                        .n(1)
                        .size("1024*1024")
                        .extraInputs(extraInputMap)
                        .build();
              }

              public void waitAsyncTask(String taskId) {
                ImageSynthesis imageSynthesis = new ImageSynthesis();
                ImageSynthesisResult result = null;
                try {
                  result = imageSynthesis.wait(taskId, null);
                } catch (ApiException | NoApiKeyException e){
                  throw new RuntimeException(e.getMessage());
                }
                System.out.println(JsonUtils.toJson(result.getOutput()));
                System.out.println(JsonUtils.toJson(result.getUsage()));
              }

              public static void main(String[] args){
                Main text2Image = new Main();
                text2Image.asyncCall();
              }
            }
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    WanxXPaintingRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。示例值：wanx-x-painting。
          enum:
            - wanx-x-painting
          example: wanx-x-painting
        input:
          $ref: "#/components/schemas/WanxXPaintingInput"
        parameters:
          $ref: "#/components/schemas/WanxXPaintingParameters"
    WanxXPaintingInput:
      type: object
      required:
        - prompt
        - base_image_url
        - mask_image_url
      description: 输入的基本信息，如提示词、图像 URL 等。
      properties:
        prompt:
          type: string
          description: |-
            正向提示词，用来描述生成图像中期望包含的元素和视觉特点。

            支持中英文，长度不超过 75 个字符，超过部分会自动截断。
          maxLength: 75
          example: 一只狗戴着红色眼镜
        base_image_url:
          type: string
          description: |-
            输入图像 URL 地址，不支持填写图像 Base64 数据。

            URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。

            **图像限制：**
            - 图像格式：JPG、JPEG、PNG、BMP。
            - 图像分辨率：大于 256×256 像素，小于 4096×4096 像素。
            - 图像大小：不超过 10 MB。
            - URL 地址中不能包含中文字符。
          example: http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/source3.jpg
        mask_image_url:
          type: string
          description: |-
            用户标记涂抹区域的图像 URL 地址，需要和 base_image_url 图像分辨率保持一致。不支持填写图像 Base64 数据。

            URL 需为公网可访问的地址，并支持 HTTP 或 HTTPS 协议。

            **图像限制：**
            - 图像格式：JPG、JPEG、PNG、BMP。
            - 图像分辨率：大于 256×256 像素，小于 4096×4096 像素。
            - 图像大小：不超过 10 MB。
            - URL 地址中不能包含中文字符。
          example: http://synthesis-source.oss-accelerate.aliyuncs.com/lingji/validation/mask2img/demo/glasses.png
    WanxXPaintingParameters:
      type: object
      description: 图像处理参数。
      properties:
        style:
          type: string
          description: |-
            输出图像的风格。目前支持以下风格取值：
            - `<auto>`：默认。
            - `<3d cartoon>`：3D 卡通。
            - `<anime>`：动画。
            - `<oil painting>`：油画。
            - `<watercolor>`：水彩。
            - `<sketch>`：素描。
            - `<chinese painting>`：中国画。
            - `<flat illustration>`：扁平插画。
          enum:
            - <auto>
            - <3d cartoon>
            - <anime>
            - <oil painting>
            - <watercolor>
            - <sketch>
            - <chinese painting>
            - <flat illustration>
          default: <auto>
          example: <auto>
        size:
          type: string
          description: |-
            输出图像的分辨率。目前支持 3 种图像分辨率：
            - `1024*1024`：默认值。
            - `720*1280`
            - `1280*720`
          enum:
            - 1024*1024
            - 720*1280
            - 1280*720
          default: 1024*1024
          example: 1024*1024
        n:
          type: integer
          description: 生成图片的数量。取值范围为 1~4 张，默认为 1。
          minimum: 1
          maximum: 4
          default: 1
          example: 1
        mask_color:
          type: array
          description: |-
            RGB 颜色数值列表，用于指定掩码图片中表示涂抹区域的颜色。默认值为 []。

            当该字段为空，默认对掩码图片进行二值化处理（处理后白色代表涂抹区域）。当该字段非空时，表示 RGB 颜色数值列表，代表一种或多种颜色。这些 RGB 颜色所描绘的区域即为涂抹区域，如 [0,0,0] 和 [134,134,134]，而未被指定的颜色则视为背景色。

            示例值：[[0, 0, 0], [134, 134, 134]]。
          items:
            type: array
            items:
              type: integer
              minimum: 0
              maximum: 255
            minItems: 3
            maxItems: 3
          example:
            - - 0
              - 0
              - 0
            - - 134
              - 134
              - 134
    AsyncTaskSubmitResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
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
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
    WanxXPaintingTaskStatusResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
            task_status:
              type: string
              description: |-
                任务状态。
                - PENDING：任务排队中
                - RUNNING：任务处理中
                - SUCCEEDED：任务执行成功
                - FAILED：任务执行失败
                - CANCELED：任务已取消
                - UNKNOWN：任务不存在或状态未知
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            results:
              type: array
              description: 任务结果列表，包括图像 URL、部分任务执行失败报错信息等。
              items:
                type: object
                properties:
                  url:
                    type: string
                    description: 生成的图像 URL。有效期 24 小时。
                  code:
                    type: string
                    description: 该条结果请求失败的错误码。请求成功时不会返回此参数。
                  message:
                    type: string
                    description: 该条结果请求失败的详细信息。请求成功时不会返回此参数。
            task_metrics:
              type: object
              description: 任务结果统计。
              properties:
                TOTAL:
                  type: integer
                  description: 总的任务数。
                SUCCEEDED:
                  type: integer
                  description: 任务状态为成功的任务数。
                FAILED:
                  type: integer
                  description: 任务状态为失败的任务数。
            code:
              type: string
              description: 请求失败的错误码。请求成功时不会返回此参数，详情请参见错误信息文档。
            message:
              type: string
              description: 请求失败的详细信息。请求成功时不会返回此参数，详情请参见错误信息文档。
        usage:
          type: object
          description: 输出信息统计。只对成功的结果计数。
          properties:
            image_count:
              type: integer
              description: 模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 标识错误类型的错误码。
        message:
          type: string
          description: 详细的错误信息。
        request_id:
          type: string
          description: 用于排查问题的请求唯一标识。
````
