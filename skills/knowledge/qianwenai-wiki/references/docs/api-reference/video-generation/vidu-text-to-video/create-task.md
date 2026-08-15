> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Vidu — 创建任务

> 使用 Vidu 模型提交文生视频任务，异步生成视频。

提交文生视频任务后，服务将异步生成视频。提交任务后，使用 [查询视频结果](/api-reference/video-generation/vidu-text-to-video/query-result) 接口轮询任务状态，直到 `task_status` 为 `SUCCEEDED` 或 `FAILED`。

## 模型列表

| 模型                             | 最高分辨率 | 最长时长 |
| ------------------------------ | ----- | ---- |
| `vidu/viduq3-turbo_text2video` | 1080P | 16 秒 |
| `vidu/viduq3-pro_text2video`   | 1080P | 16 秒 |
| `vidu/viduq2_text2video`       | 1080P | 10 秒 |

## HTTP 调用

文生视频接口仅支持异步调用，请求时必须携带请求头 `X-DashScope-Async: enable`。

任务提交成功后返回 `task_id`，使用 [查询视频结果](/api-reference/video-generation/vidu-text-to-video/query-result) 接口获取生成结果。

### size 参数取值对照表

`size` 参数与 `resolution` 参数共同控制输出视频的尺寸。两者均传入时以 `size` 为准。

| 分辨率档位 | 宽高比  | size 取值（宽\*高） |
| ----- | ---- | ------------- |
| 540P  | 16:9 | 960\*528      |
| 540P  | 9:16 | 528\*960      |
| 540P  | 1:1  | 720\*720      |
| 540P  | 4:3  | 816\*608      |
| 540P  | 3:4  | 608\*816      |
| 720P  | 16:9 | 1280\*720     |
| 720P  | 9:16 | 720\*1280     |
| 720P  | 1:1  | 960\*960      |
| 720P  | 4:3  | 1104\*816     |
| 720P  | 3:4  | 816\*1104     |
| 1080P | 16:9 | 1920\*1080    |
| 1080P | 9:16 | 1080\*1920    |
| 1080P | 1:1  | 1440\*1440    |
| 1080P | 4:3  | 1674\*1238    |
| 1080P | 3:4  | 1238\*1674    |

<Note>
  `size` 与 `resolution` 均不传时，默认输出 720P 16:9（1280\*720）。
</Note>

## DashScope SDK 调用

<Note>
  使用 SDK 调用时，需安装对应版本的 DashScope SDK：

  - Python SDK：版本 >= 1.25.8
  - Java SDK：版本 >= 2.22.6

  安装方法参见[安装 DashScope SDK](/api-reference/preparation/install-sdk)。
</Note>

### Python SDK

<CodeGroup>
  ```python 同步调用
  from http import HTTPStatus
  from dashscope import VideoSynthesis
  import dashscope
  import os

  dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

  # 若没有配置环境变量，请用 API Key 将下行替换为：api_key="sk-xxx"
  api_key = os.getenv("DASHSCOPE_API_KEY")

  def sample_sync_call_t2v():
    print('please wait...')
    rsp = VideoSynthesis.call(api_key=api_key,
                              model='vidu/viduq3-turbo_text2video',
                              prompt='一只小猫在月光下奔跑',
                              size='960*528',
                              duration=5,
                              resolution='540P',
                              watermark=True)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
      print(rsp.output.video_url)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' %
            (rsp.status_code, rsp.code, rsp.message))

  if __name__ == '__main__':
    sample_sync_call_t2v()
  ```

  ```python 异步调用
  from http import HTTPStatus
  from dashscope import VideoSynthesis
  import dashscope
  import os

  dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

  # 若没有配置环境变量，请用 API Key 将下行替换为：api_key="sk-xxx"
  api_key = os.getenv("DASHSCOPE_API_KEY")

  def sample_async_call_t2v():
    rsp = VideoSynthesis.async_call(api_key=api_key,
                                    model='vidu/viduq3-turbo_text2video',
                                    prompt='一只小猫在月光下奔跑',
                                    size='960*528',
                                    duration=5,
                                    resolution='540P')
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
      print("task_id: %s" % rsp.output.task_id)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' %
            (rsp.status_code, rsp.code, rsp.message))

    status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
    if status.status_code == HTTPStatus.OK:
      print(status.output.task_status)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' %
            (status.status_code, status.code, status.message))

    rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
    print(rsp)
    if rsp.status_code == HTTPStatus.OK:
      print(rsp.output.video_url)
    else:
      print('Failed, status_code: %s, code: %s, message: %s' %
            (rsp.status_code, rsp.code, rsp.message))

  if __name__ == '__main__':
    sample_async_call_t2v()
  ```
</CodeGroup>

### Java SDK

<CodeGroup>
  ```java 同步调用
  // Copyright (c) Alibaba, Inc. and its affiliates.
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
      public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

      public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
          VideoSynthesis vs = new VideoSynthesis();
          VideoSynthesisParam param =
                  VideoSynthesisParam.builder()
                          .apiKey(apiKey)
                          .model("vidu/viduq3-turbo_text2video")
                          .prompt("一只小猫在月光下奔跑")
                          .size("960*528")
                          .resolution("540P")
                          .duration(5)
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

  ```java 异步调用
  // Copyright (c) Alibaba, Inc. and its affiliates.
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
      public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

      public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
          VideoSynthesis vs = new VideoSynthesis();
          VideoSynthesisParam param =
                  VideoSynthesisParam.builder()
                          .apiKey(apiKey)
                          .model("vidu/viduq3-turbo_text2video")
                          .prompt("一只小猫在月光下奔跑")
                          .size("960*528")
                          .resolution("540P")
                          .duration(5)
                          .watermark(true)
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
</CodeGroup>

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.0.0
info:
  title: Vidu 文生视频 API
  description: Vidu 文生视频模型基于文本提示词，生成一段流畅的视频。API 采用异步调用模式，包含"创建任务"和"查询结果"两个步骤。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createViduTextToVideoTask
      summary: 创建文生视频任务
      description: 提交文生视频任务，返回 task_id 用于后续轮询查询。
      parameters:
        - name: Content-Type
          in: header
          required: true
          description: 请求内容类型，必须设置为 application/json。
          schema:
            type: string
            enum:
              - application/json
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步处理配置参数。HTTP 请求只支持异步，必须设置为 enable。缺少此请求头将报错："current user api does not support synchronous calls"。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ViduTextToVideoRequest"
      responses:
        "200":
          description: 任务创建成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求失败
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "vidu/viduq3-turbo_text2video",
              "input": {
                "prompt": "一只小猫在月光下奔跑"
              },
              "parameters": {
                "size": "960*528",
                "resolution": "540P",
                "duration": 5,
                "watermark": true
              }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    ViduTextToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - vidu/viduq3-turbo_text2video
            - vidu/viduq3-pro_text2video
            - vidu/viduq2_text2video
          example: vidu/viduq3-turbo_text2video
        input:
          type: object
          required:
            - prompt
          description: 输入的基本信息，如提示词等。
          properties:
            prompt:
              type: string
              description: |-
                文本提示词。用来描述生成视频中期望包含的元素和视觉特点。支持中英文，每个汉字/字母占一个字符，不能超过 5000 个字符，超过部分会自动截断。示例值：一只小猫在月光下奔跑。

                提示词编写请参见Vidu视频生成Prompt指南。
              example: 一只小猫在月光下奔跑
        parameters:
          $ref: "#/components/schemas/ViduTextToVideoParameters"
    ViduTextToVideoParameters:
      type: object
      description: 视频生成参数，如设置视频分辨率、时长等。
      properties:
        resolution:
          type: string
          description: 分辨率档位。resolution 直接影响费用，请在调用前确认模型价格。
          enum:
            - 540P
            - 720P
            - 1080P
          default: 720P
          example: 720P
        size:
          type: string
          description: 生成视频的分辨率，格式为宽*高的像素值。默认值根据 resolution 而定：resolution=540P 时默认为 960*528，resolution=720P 时默认为 1280*720，resolution=1080P 时默认为 1920*1080。
        duration:
          type: integer
          description: 生成视频的时长，单位为秒。duration 直接影响费用，按秒计费，时间越长费用越高。vidu/viduq3-pro_text2video 和 vidu/viduq3-turbo_text2video：取值为 [1, 16] 之间的整数，默认值为 5。vidu/viduq2_text2video：取值为 [1, 10] 之间的整数，默认值为 5。
          default: 5
          example: 5
        audio:
          type: boolean
          description: 是否生成有声视频。开启后模型将根据视频内容自动生成匹配的背景音乐或音效。支持模型：vidu/viduq3-pro_text2video、vidu/viduq3-turbo_text2video。
          default: false
          example: false
        watermark:
          type: boolean
          description: 是否添加水印标识，水印位于视频右下角，文案固定为"内容由 AI 生成"。
          default: false
          example: false
        seed:
          type: integer
          description: 随机数种子，取值范围为 [0, 2147483647]。未指定时系统自动生成随机种子。若需提升生成结果的可复现性，建议固定 seed 值。由于模型生成具有概率性，即使使用相同 seed，也不能保证每次生成结果完全一致。示例值：12345。
          minimum: 0
          maximum: 2147483647
          example: 12345
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务创建成功响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。用于查询任务状态与结果，有效期 24 小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务状态。初始状态通常为 PENDING。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
              example: PENDING
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
    TaskStatusResponse:
      type: object
      description: 任务查询响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: eda50dad-a6d3-4e62-a70b-26bbb797ae81
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
              example: d9254244-1f9b-4b4c-be82-d9560ba25708
            task_status:
              type: string
              description: 任务状态。状态流转：PENDING（排队中）→ RUNNING（处理中）→ SUCCEEDED（成功）/ FAILED（失败）。初次查询状态通常为 PENDING 或 RUNNING。当状态变为 SUCCEEDED 时，响应中将包含生成的视频 URL。若状态为 FAILED，请检查错误信息并重试。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-03-27 13:32:13.962
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-03-27 13:32:14.008
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-03-27 13:32:43.375
            orig_prompt:
              type: string
              description: 原始输入的 prompt，对应请求参数 prompt。
              example: 一只小猫在月光下奔跑
            video_url:
              type: string
              description: 视频 URL。仅在 task_status 为 SUCCEEDED 时返回。视频格式为 MP4（H.264 编码），链接有效期 24 小时，请及时下载。
              example: https://prod-ss-vidu.s3.cn-northwest-1.amazonaws.com.cn/xxx.mp4?xxx
            code:
              type: string
              description: 请求失败的错误码。请求成功时不会返回此参数。
            message:
              type: string
              description: 请求失败的详细信息。请求成功时不会返回此参数。
        usage:
          type: object
          description: 输出信息统计，只对成功的结果计数。
          properties:
            duration:
              type: integer
              description: 总的视频计费时长（秒）。示例值：5。
              example: 5
            size:
              type: string
              description: 生成视频的分辨率。示例值：960*528。
              example: 960*528
            output_video_duration:
              type: integer
              description: 输出视频的时长（秒）。示例值：5。
              example: 5
            fps:
              type: integer
              description: 生成视频的帧率。示例值：24。
              example: 24
            audio:
              type: boolean
              description: 生成视频是否为有声视频。示例值：false。
              example: false
            SR:
              type: string
              description: 生成视频的分辨率档位。示例值：540。
              example: "540"
            video_count:
              type: integer
              description: 生成视频的数量。固定为 1。
              example: 1
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
          example: 7438d53d-6eb8-4596-8835-xxxxxx
        code:
          type: string
          description: 错误码。
          example: InvalidApiKey
        message:
          type: string
          description: 错误详细信息。
          example: No API-key provided.
````
