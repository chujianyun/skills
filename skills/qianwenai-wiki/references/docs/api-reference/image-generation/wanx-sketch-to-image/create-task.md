> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 万相涂鸦作画 — 创建任务

> 提交涂鸦作画任务，获取任务 ID。

## OpenAPI

````yaml post /services/aigc/image2image/image-synthesis
openapi: 3.0.0
info:
  title: 万相-涂鸦作画
  description: 本文介绍万相-涂鸦作画模型的API输入输出参数。万相-涂鸦作画通过手绘图案和文字描述，生成精美的涂鸦绘画作品。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - ApiKeyAuth: []
paths:
  /services/aigc/image2image/image-synthesis:
    post:
      summary: 创建任务获取任务ID
      description: 发起创建任务请求，该请求会返回任务ID（task_id）。图像模型处理时间较长，HTTP调用仅支持异步获取模型结果。
      operationId: createSketchToImageTask
      requestBody:
        required: true
        description: 创建涂鸦作画任务的请求体
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateTaskRequest"
      responses:
        "200":
          description: 成功创建任务
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CreateTaskResponse"
              examples:
                success:
                  summary: 成功响应
                  value:
                    output:
                      task_status: PENDING
                      task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                    request_id: 4909100c-7b5a-9f92-bfe5-xxxxxx
                error:
                  summary: 异常响应
                  value:
                    code: InvalidApiKey
                    message: No API-key provided.
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
      x-codeSamples:
        - lang: cURL
          label: curl
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
                "model": "wanx-sketch-to-image-lite",
                "input": {
                    "sketch_image_url": "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6609471071/p743851.jpg",
                    "prompt": "一棵参天大树"
                },
                "parameters": {
                    "size": "768*768",
                    "n": 2,
                    "sketch_weight": 3,
                    "style": "<watercolor>"
                }
            }'
        - lang: Python
          label: Python SDK 同步调用
          source: |-
            from http import HTTPStatus
            from urllib.parse import urlparse, unquote
            from pathlib import PurePosixPath
            import requests
            from dashscope import ImageSynthesis
            import os

            prompt = "一棵参天大树"
            sketch_image_url = "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6609471071/p743851.jpg"
            model = "wanx-sketch-to-image-lite"
            task = "image2image"

            print('----sync call, please wait a moment----')
            rsp = ImageSynthesis.call(api_key=os.getenv("DASHSCOPE_API_KEY"),
                                      model=model,
                                      prompt=prompt,
                                      n=1,
                                      style='<watercolor>',
                                      size='768*768',
                                      sketch_image_url=sketch_image_url,
                                      task=task)
            print('response: %s' % rsp)
            if rsp.status_code == HTTPStatus.OK:
                print(rsp.output)
                for result in rsp.output.results:
                    file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
                    with open('./%s' % file_name, 'wb+') as f:
                        f.write(requests.get(result.url).content)
            else:
                print('sync_call Failed, status_code: %s, code: %s, message: %s' %
                      (rsp.status_code, rsp.code, rsp.message))
        - lang: Python
          label: Python SDK 异步调用
          source: |-
            from http import HTTPStatus
            from urllib.parse import urlparse, unquote
            from pathlib import PurePosixPath
            import requests
            from dashscope import ImageSynthesis
            import os

            prompt = "一棵参天大树"
            sketch_image_url = "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6609471071/p743851.jpg"
            model = "wanx-sketch-to-image-lite"
            task = "image2image"

            def async_call():
                print('----create task----')
                task_info = create_async_task()
                print('----wait task done then save image----')
                wait_async_task(task_info)

            def create_async_task():
                rsp = ImageSynthesis.async_call(api_key=os.getenv("DASHSCOPE_API_KEY"),
                                                model=model,
                                                prompt=prompt,
                                                n=1,
                                                style='<watercolor>',
                                                size='768*768',
                                                sketch_image_url=sketch_image_url,
                                                task=task)
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
        - lang: Java
          label: Java SDK 同步调用
          source: |-
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.JsonUtils;

            public class Main {
                public void syncCall() {
                    String prompt = "一棵参天大树";
                    String sketchImageUrl = "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6609471071/p743851.jpg";
                    String model = "wanx-sketch-to-image-lite";
                    ImageSynthesisParam param = ImageSynthesisParam.builder()
                            .model(model)
                            .prompt(prompt)
                            .n(1)
                            .size("768*768")
                            .sketchImageUrl(sketchImageUrl)
                            .style("<watercolor>")
                            .build();

                    String task = "image2image";
                    ImageSynthesis imageSynthesis = new ImageSynthesis(task);
                    ImageSynthesisResult result = null;
                    try {
                        System.out.println("---sync call, please wait a moment----");
                        result = imageSynthesis.call(param);
                    } catch (ApiException | NoApiKeyException e){
                        throw new RuntimeException(e.getMessage());
                    }
                    System.out.println(JsonUtils.toJson(result));
                }

                public static void main(String[] args){
                    Main text2Image = new Main();
                    text2Image.syncCall();
                }
            }
        - lang: Java
          label: Java SDK 异步调用
          source: |-
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
            import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.JsonUtils;

            public class Main {
                public void asyncCall() {
                    System.out.println("---create task----");
                    String taskId = this.createAsyncTask();
                    System.out.println("---wait task done then return image url----");
                    this.waitAsyncTask(taskId);
                }

                public String createAsyncTask() {
                    String prompt = "一棵参天大树";
                    String sketchImageUrl = "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/6609471071/p743851.jpg";
                    String model = "wanx-sketch-to-image-lite";
                    ImageSynthesisParam param = ImageSynthesisParam.builder()
                            .model(model)
                            .prompt(prompt)
                            .n(1)
                            .size("768*768")
                            .sketchImageUrl(sketchImageUrl)
                            .style("<watercolor>")
                            .build();

                    String task = "image2image";
                    ImageSynthesis imageSynthesis = new ImageSynthesis(task);
                    ImageSynthesisResult result = null;
                    try {
                        result = imageSynthesis.asyncCall(param);
                    } catch (Exception e){
                        throw new RuntimeException(e.getMessage());
                    }
                    String taskId = result.getOutput().getTaskId();
                    System.out.println("taskId=" + taskId);
                    return taskId;
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
  schemas:
    CreateTaskRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 调用模型，固定为 wanx-sketch-to-image-lite。
          example: wanx-sketch-to-image-lite
        input:
          $ref: "#/components/schemas/Input"
        parameters:
          $ref: "#/components/schemas/Parameters"
    Input:
      type: object
      required:
        - prompt
        - sketch_image_url
      description: 输入的基本信息，比如提示词、图像URL地址。
      properties:
        prompt:
          type: string
          description: 提示词，用来描述生成图像中期望包含的元素和视觉特点。支持中英文，长度不超过75个字符，超过部分会自动截断。
          example: 一棵参天大树
        sketch_image_url:
          type: string
          description: 输入草图的URL地址。输入草图需要与输出图像的分辨率比例保持一致，否则会导致图片拉伸变形，建议使用白色背景图。URL需为公网可访问的地址，并支持HTTP或HTTPS协议，URL地址中不能包含中文字符。图像格式支持JPG、JPEG、PNG、TIFF、WEBP。图像分辨率不小于256×256像素且不超过2048×2048像素。图像大小不超过10 MB。
    Parameters:
      type: object
      description: 图像处理参数。
      properties:
        style:
          type: string
          description: 输出图像的风格。
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
          x-enumDescriptions:
            <auto>: 默认值，由模型随机输出图像风格。
            <3d cartoon>: 3D卡通。
            <anime>: 二次元。
            <oil painting>: 油画。
            <watercolor>: 水彩。
            <sketch>: 素描。
            <chinese painting>: 中国画。
            <flat illustration>: 扁平插画。
        size:
          type: string
          description: 输出图像的分辨率。目前仅支持一种图像分辨率：768*768，且为默认值。
          default: 768*768
        n:
          type: integer
          description: 生成图片的数量。取值范围为1~4张，默认为4。
          default: 4
          minimum: 1
          maximum: 4
        sketch_weight:
          type: integer
          description: 输入草图对输出图像的约束程度。取值范围为0-10，取值间隔为1，默认值为10。取值越大表示输出图像跟输入草图越相似。
          default: 10
          minimum: 0
          maximum: 10
        sketch_extraction:
          type: boolean
          description: 如果上传图片是RGB图片，而非草图（sketch线稿），此参数可控制是否对输入图片进行sketch边缘提取。默认值为False，表示不进行提取。设置为True时，表示进行提取，此时sketch_color字段失效。
          default: false
        sketch_color:
          type: array
          description: 此字段在sketch_extraction=false时生效，所包含数值均被视为画笔色，其余数值均会视为背景色。模型会基于一种或多种画笔色描绘的区域生成新的画作。默认值为[]。当sketch_image_url线稿中的线条不是黑色，而是包含其他一种或多种颜色时，可以指定一个或多个RGB颜色数值作为画笔色。
          default: []
          items:
            type: array
            items:
              type: integer
            minItems: 3
            maxItems: 3
          example:
            - - 134
              - 134
              - 134
            - - 0
              - 0
              - 0
    CreateTaskResponse:
      type: object
      properties:
        output:
          $ref: "#/components/schemas/CreateTaskOutput"
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
    CreateTaskOutput:
      type: object
      description: 任务输出信息。
      properties:
        task_id:
          type: string
          description: 任务ID。查询有效期24小时。
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
          x-enumDescriptions:
            PENDING: 任务排队中
            RUNNING: 任务处理中
            SUCCEEDED: 任务执行成功
            FAILED: 任务执行失败
            CANCELED: 任务已取消
            UNKNOWN: 任务不存在或状态未知
    QueryTaskResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
        output:
          $ref: "#/components/schemas/QueryTaskOutput"
        usage:
          $ref: "#/components/schemas/Usage"
    QueryTaskOutput:
      type: object
      description: 任务输出信息。任务数据（如任务状态、图像URL等）仅保留24小时，超时后会被自动清除。请您务必及时保存生成的图像。
      properties:
        task_id:
          type: string
          description: 任务ID。查询有效期24小时。
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
          x-enumDescriptions:
            PENDING: 任务排队中
            RUNNING: 任务处理中
            SUCCEEDED: 任务执行成功
            FAILED: 任务执行失败
            CANCELED: 任务已取消
            UNKNOWN: 任务不存在或状态未知
        results:
          type: array
          description: 任务结果列表，包括图像URL、部分任务执行失败报错信息等。
          items:
            $ref: "#/components/schemas/ResultItem"
        task_metrics:
          $ref: "#/components/schemas/TaskMetrics"
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
    ResultItem:
      type: object
      description: 单个任务结果。
      properties:
        url:
          type: string
          description: 生成图像的URL地址。
        code:
          type: string
          description: 该任务结果失败的错误码。
        message:
          type: string
          description: 该任务结果失败的详细信息。
    TaskMetrics:
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
    Usage:
      type: object
      description: 输出信息统计。只对成功的结果计数。
      properties:
        image_count:
          type: integer
          description: 模型成功生成图片的数量。计费公式：费用 = 图片数量 × 单价。
  securitySchemes:
    ApiKeyAuth:
      type: http
      scheme: bearer
      bearerFormat: token
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````
