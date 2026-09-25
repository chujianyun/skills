> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen — 异步图像生成（3.0系列）

> qwen-image-3.0 系列模型的异步图像生成接口

<Note>
  先[获取 API Key](/api-reference/preparation/api-key) 并[配置环境变量](/api-reference/preparation/export-api-key-env)。如果使用 SDK，还需[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

## 调用流程

1. **提交任务**：通过 `POST /services/aigc/image-generation/generation` 提交任务，请求头中需包含 `X-DashScope-Async: enable`。
2. **轮询结果**：通过 [`GET /tasks/{task_id}`](/api-reference/image-generation/qwen-text-to-image-task-query) 查询任务状态，直到 `task_status` 变为 `SUCCEEDED` 或 `FAILED`。建议每 10 秒轮询一次。

## OpenAPI

````yaml post /services/aigc/image-generation/generation
openapi: 3.1.0
info:
  title: Qwen-Image API
  description: Qwen-Image 文生图 API，支持所有模型的同步调用，以及旧版模型的异步调用。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope
security:
  - BearerAuth: []
paths:
  /services/aigc/image-generation/generation:
    post:
      operationId: createQwenImage30Async
      summary: 异步生成图像（3.0系列）
      description: "qwen-image-3.0 系列模型的异步调用接口。与同步接口共用相同的请求参数结构，仅需在请求头中增加 `X-DashScope-Async: enable`，服务受理后返回任务 ID（`task_id`），再通过任务 ID 轮询查询接口获取最终结果。"
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步处理配置参数。必须设置为 `enable`。缺少此请求头将报错："current user api does not support synchronous calls"。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/QwenImage30AsyncRequest"
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
          label: cURL（文生图 - 提交任务）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
            --header 'Content-Type: application/json' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'X-DashScope-Async: enable' \
            --data '{
              "model": "qwen-image-3.0-pro",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "text": "A healing-style hand-drawn poster featuring three puppies playing with a ball on lush green grass."
                      }
                    ]
                  }
                ]
              },
              "parameters": {
                "prompt_extend": true
              }
            }'
        - lang: curl
          label: cURL（查询结果）
          source: |-
            # 将 {task_id} 替换为第 1 步返回的实际任务 ID
            curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
              --header "Authorization: Bearer $DASHSCOPE_API_KEY"
        - lang: python
          label: Python (DashScope SDK)
          source: |-
            from http import HTTPStatus
            from urllib.parse import urlparse, unquote
            from pathlib import PurePosixPath
            import requests
            import os
            import dashscope
            from dashscope import MultiModalConversation

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            prompt = ("A healing-style hand-drawn poster featuring three puppies "
                      "playing with a ball on lush green grass.")

            api_key = os.getenv("DASHSCOPE_API_KEY")

            messages = [
              {
                "role": "user",
                "content": [{"text": prompt}]
              }
            ]

            print('----正在调用接口，请等待任务完成。----')
            response = MultiModalConversation.call(
              api_key=api_key,
              model="qwen-image-3.0-pro",
              messages=messages,
              result_format='message',
              stream=False,
              prompt_extend=True
            )

            if response.status_code == HTTPStatus.OK:
              content = response.output.choices[0].message.content
              for item in content:
                if 'image' in item:
                  image_url = item['image']
                  file_name = PurePosixPath(
                    unquote(urlparse(image_url).path)
                  ).parts[-1]
                  with open(f'./{file_name}', 'wb+') as f:
                    f.write(requests.get(image_url).content)
                  print(f"Image saved: {file_name}")
            else:
              print(f"Failed: {response.code}, {response.message}")
        - lang: java
          label: Java (DashScope SDK)
          source: |-
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.utils.Constants;
            import com.alibaba.dashscope.utils.JsonUtils;

            import java.util.*;

            public class QwenImage30Async {
              static {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              }

              static String apiKey = System.getenv("DASHSCOPE_API_KEY");

              public static void main(String[] args) throws Exception {
                String prompt = "A healing-style hand-drawn poster featuring three puppies "
                  + "playing with a ball on lush green grass.";

                MultiModalMessage userMessage = MultiModalMessage.builder()
                  .role(Role.USER.getValue())
                  .content(List.of(Map.of("text", prompt)))
                  .build();

                Map<String, Object> parameters = new HashMap<>();
                parameters.put("prompt_extend", true);

                MultiModalConversationParam param = MultiModalConversationParam.builder()
                  .apiKey(apiKey)
                  .model("qwen-image-3.0-pro")
                  .messages(List.of(userMessage))
                  .parameters(parameters)
                  .build();

                MultiModalConversation conversation = new MultiModalConversation();
                System.out.println("---正在调用接口，请等待任务完成。----");
                MultiModalConversationResult result = conversation.call(param);
                System.out.println(JsonUtils.toJson(result));
              }
            }
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    QwenImageSyncRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - qwen-image-3.0-pro
            - qwen-image-3.0
            - qwen-image-2.0-pro
            - qwen-image-2.0-pro-2026-06-22
            - qwen-image-2.0-pro-2026-04-22
            - qwen-image-2.0-pro-2026-03-03
            - qwen-image-2.0
            - qwen-image-2.0-2026-03-03
            - qwen-image-max
            - qwen-image-max-2025-12-30
            - qwen-image-plus
            - qwen-image
          example: qwen-image-3.0-pro
        input:
          type: object
          required:
            - messages
          description: 包含消息数组的输入数据。
          properties:
            messages:
              type: array
              description: 仅支持单轮对话。必须包含且只包含一条角色为 `user` 的消息。
              minItems: 1
              maxItems: 1
              items:
                $ref: "#/components/schemas/QwenImageMessage"
        parameters:
          $ref: "#/components/schemas/QwenImageSyncParameters"
    QwenImageMessage:
      type: object
      required:
        - role
        - content
      properties:
        role:
          type: string
          enum:
            - user
          description: 必须为 `user`。
        content:
          type: array
          description: 消息内容数组，必须且只包含一个文本对象。
          minItems: 1
          maxItems: 1
          items:
            $ref: "#/components/schemas/QwenImageContentPart"
    QwenImageContentPart:
      type: object
      required:
        - text
      properties:
        text:
          type: string
          description: 描述目标内容、风格和构图的正向提示词。支持中英文。qwen-image-3.0 系列推荐不超过 4500 Token；qwen-image-2.0 系列上限为 1300 Token；其他模型为 800 Token。超出部分将自动截断。
          example: 画面是一张竖幅户外人像摄影，左上方深蓝色招牌上以白色哥特体大字写着 Il Messaggero，招牌下方是报刊亭的玻璃展示窗，内部陈列着许多报纸与杂志封面。
    QwenImageSyncParameters:
      type: object
      description: 图像生成参数。
      properties:
        negative_prompt:
          type: string
          description: 描述不希望在图像中出现的内容。最多 500 个字符，超出部分自动截断。
          maxLength: 500
        size:
          type: string
          description: |-
            输出分辨率，格式为 `宽*高`。

            - **qwen-image-3.0 系列**：总像素在 512\*512 到 2048\*2048 之间，宽高比在 1:8 到 8:1 之间，不指定时由模型根据提示词自动推荐分辨率。
            - **qwen-image-2.0 系列**：总像素在 512\*512 到 2048\*2048 之间，默认 `2048*2048`。
            - **qwen-image-max**：支持自定义分辨率（总像素在 512\*512 到 2048\*2048 之间）和固定尺寸。
            - **qwen-image-plus/image**：仅支持固定尺寸。

            qwen-image-max/plus/image 的固定尺寸：`1664*928`（16:9，默认）、`1472*1104`（4:3）、`1328*1328`（1:1）、`1104*1472`（3:4）、`928*1664`（9:16）。
          default: 2048*2048
          example: 2048*2048
        n:
          type: integer
          description: |-
            生成图像数量。默认值：1。

            - **qwen-image-3.0 / qwen-image-2.0 系列**：1-6 张。
            - **qwen-image-max/plus 系列**：固定为 1 张。
          minimum: 1
          maximum: 6
          default: 1
        prompt_extend:
          type: boolean
          description: 启用提示词改写。`true`（默认）：模型先优化提示词再生成；qwen-image-3.0 系列按 `prompt_extend_mode` 指定的方式改写。`false`：直接使用原始提示词。
          default: true
        prompt_extend_mode:
          type: string
          description: |-
            提示词改写方式。仅 qwen-image-3.0 系列支持。

            - `direct`（默认）：直接提示词增强（DPE），适用于大多数场景。
            - `agent`：智能体提示词增强（APE），改写更精细，仅文生图支持。
          enum:
            - direct
            - agent
          default: direct
        watermark:
          type: boolean
          description: 在图像右下角添加 "Qwen-Image" 水印。默认值：`false`。
          default: false
        seed:
          type: integer
          description: 随机数种子。范围：[0, 2147483647]。相同种子可产生更一致（但不完全相同）的结果。若不指定，则使用随机种子。
          minimum: 0
          maximum: 2147483647
    QwenImageAsyncRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。异步调用仅支持 `qwen-image-plus` 和 `qwen-image`。
          enum:
            - qwen-image-plus
            - qwen-image
          example: qwen-image-plus
        input:
          type: object
          required:
            - prompt
          description: 输入数据。
          properties:
            prompt:
              type: string
              description: 描述目标内容、风格和构图的正向提示词。支持中英文。qwen-image-3.0 系列推荐不超过 4500 Token；qwen-image-2.0 系列上限为 1300 Token；其他模型为 800 Token。超出部分将自动截断。
              example: A cute orange cat sitting on a windowsill, realistic style
            negative_prompt:
              type: string
              description: 描述不希望在图像中出现的内容。最多 500 个字符。
              maxLength: 500
        parameters:
          $ref: "#/components/schemas/QwenImageAsyncParameters"
    QwenImageAsyncParameters:
      type: object
      description: Qwen-Image 异步调用的生成参数。
      properties:
        size:
          type: string
          description: 输出分辨率，格式为 `宽*高`。可选尺寸：`1664*928`（16:9，默认）、`1472*1104`（4:3）、`1328*1328`（1:1）、`1104*1472`（3:4）、`928*1664`（9:16）。
          default: 1664*928
          enum:
            - 1664*928
            - 1472*1104
            - 1328*1328
            - 1104*1472
            - 928*1664
          example: 1664*928
        n:
          type: integer
          description: 生成图像数量，固定为 1，填写其他值将报错。
          enum:
            - 1
          default: 1
        prompt_extend:
          type: boolean
          description: 启用智能提示词改写。`true`（默认）：模型优化提示词后再生成。`false`：直接使用原始提示词。
          default: true
        watermark:
          type: boolean
          description: 在图像右下角添加 "Qwen-Image" 水印。默认值：`false`。
          default: false
        seed:
          type: integer
          description: 随机数种子。范围：[0, 2147483647]。相同种子可产生更一致（但不完全相同）的结果。
          minimum: 0
          maximum: 2147483647
    QwenImage30AsyncRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - qwen-image-3.0-pro
            - qwen-image-3.0
          example: qwen-image-3.0-pro
        input:
          type: object
          required:
            - messages
          description: 包含消息数组的输入数据。
          properties:
            messages:
              type: array
              description: 请求内容数组。当前仅支持单轮对话，数组内有且只有一个对象。
              items:
                $ref: "#/components/schemas/QwenImageMessage"
        parameters:
          $ref: "#/components/schemas/QwenImageSyncParameters"
    QwenImageSyncResponse:
      type: object
      description: Qwen-Image 同步生成的响应结果。
      example:
        output:
          choices:
            - finish_reason: stop
              message:
                content:
                  - image: https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx
                role: assistant
        usage:
          output_height: 2048
          output_width: 2048
          input_image_count: 0
          input_image_type: qima_input_2k
          output_image_count: 1
          output_image_type: qima_output_2k
        request_id: d0250a3d-b07f-49e1-bdc8-6793f4929xxx
      properties:
        output:
          type: object
          properties:
            choices:
              type: array
              description: 生成结果列表，每张生成图像对应一个元素。
              items:
                $ref: "#/components/schemas/QwenImageChoice"
            task_metric:
              type: object
              description: 任务结果统计信息。qwen-image-2.0 和 qwen-image-3.0 系列不返回此字段。
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
            rewrite_status:
              type: string
              description: 提示词改写状态。具体取值由请求是否开启改写以及改写执行结果决定。
        usage:
          type: object
          description: 用量统计（仅统计成功结果）。字段随模型系列不同：qwen-image-3.0 系列返回 `output_*` / `input_*` 字段，其他系列返回 `image_count` / `width` / `height`。
          properties:
            output_width:
              type: integer
              description: 最终输出图片的宽度（像素）。仅 qwen-image-3.0 系列返回。
            output_height:
              type: integer
              description: 最终输出图片的高度（像素）。仅 qwen-image-3.0 系列返回。
            input_image_count:
              type: integer
              description: 请求中输入图片的数量。文生图为 0，图像编辑按实际输入图片数返回。仅 qwen-image-3.0 系列返回。
            input_image_type:
              type: string
              description: 输入图片计量档位，按输出分辨率像素面积判断：面积不大于 2,250,000 为 `qima_input_1k`，大于 2,250,000 为 `qima_input_2k`。仅 qwen-image-3.0 系列返回。
            output_image_count:
              type: integer
              description: 实际返回的输出图片数量。仅 qwen-image-3.0 系列返回。
            output_image_type:
              type: string
              description: 输出图片计量档位，按输出分辨率像素面积判断：面积不大于 2,250,000 为 `qima_output_1k`，大于 2,250,000 为 `qima_output_2k`。仅 qwen-image-3.0 系列返回。
            image_count:
              type: integer
              description: 已生成的图像数量。qwen-image-3.0 系列不返回此字段，改用 `output_image_count`。
            width:
              type: integer
              description: 生成图像的宽度（像素）。qwen-image-3.0 系列不返回此字段，改用 `output_width`。
            height:
              type: integer
              description: 生成图像的高度（像素）。qwen-image-3.0 系列不返回此字段，改用 `output_height`。
        request_id:
          type: string
          description: 唯一请求标识符，用于追踪和排查问题。
          example: abf1645b-b630-433a-92f6-xxxxxx
    QwenImageChoice:
      type: object
      properties:
        finish_reason:
          type: string
          description: "`stop` 表示正常结束。"
          example: stop
        message:
          type: object
          properties:
            role:
              type: string
              description: 始终为 `assistant`。
              enum:
                - assistant
            content:
              type: array
              description: 响应内容数组。
              items:
                $ref: "#/components/schemas/QwenImageResponseContentPart"
    QwenImageResponseContentPart:
      type: object
      properties:
        image:
          type: string
          description: 生成图像的 URL（PNG 格式）。**有效期 24 小时**，请及时下载。
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交后的响应结果。
      example:
        output:
          task_status: PENDING
          task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
        request_id: 4909100c-7b5a-9f92-bfe5-xxxxxx
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于轮询状态。配合 `GET /tasks/{task_id}` 使用。
            task_status:
              type: string
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    AsyncTaskStatusResponse:
      type: object
      description: 异步任务状态及结果。
      example:
        request_id: 7434edb2-3cba-44e6-a772-xxxxxx
        output:
          task_id: 878f591e-ebdf-4e45-97eb-xxxxxx
          task_status: SUCCEEDED
          submit_time: 2025-09-09 11:38:54.741
          scheduled_time: 2025-09-09 11:38:54.781
          end_time: 2025-09-09 11:39:19.484
          results:
            - orig_prompt: Healing-style hand-drawn poster...
              actual_prompt: Childhood-inspired hand-drawn poster design...
              url: https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/7d/xxx.png?Expires=xxxx
        usage:
          image_count: 1
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
            task_status:
              type: string
              description: 当前任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务调度执行时间。
            end_time:
              type: string
              description: 任务完成时间。
            code:
              type: string
              description: 错误码。仅当 `task_status` 为 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息。仅当 `task_status` 为 `FAILED` 时返回。
            results:
              type: array
              description: 生成的图像结果。仅当 `task_status` 为 `SUCCEEDED` 时返回。
              items:
                $ref: "#/components/schemas/AsyncTaskResult"
            task_metrics:
              $ref: "#/components/schemas/TaskMetrics"
        usage:
          type: object
          description: 用量统计。
          properties:
            image_count:
              type: integer
              description: 成功生成的图像数量。
    AsyncTaskResult:
      type: object
      description: 异步任务中的单条生成结果。
      properties:
        orig_prompt:
          type: string
          description: 用户提交的原始提示词。
        actual_prompt:
          type: string
          description: 实际用于生成的提示词（启用 `prompt_extend` 时可能与原始提示词不同）。
        url:
          type: string
          description: 生成图像的 URL。**有效期 24 小时。**
    TaskMetrics:
      type: object
      description: 任务完成度统计。
      properties:
        TOTAL:
          type: integer
          description: 请求生成的图像总数。
        SUCCEEDED:
          type: integer
          description: 成功生成的图像数量。
        FAILED:
          type: integer
          description: 生成失败的图像数量。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        code:
          type: string
          description: 错误码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 人类可读的错误信息。
          example: num_images_per_prompt must be 1
````
