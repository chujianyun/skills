> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像背景生成 — 创建任务

> 提交图像背景生成异步任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 模型概览

**模型简介**

| 模型名                           | 模型简介                                                                                   |
| ----------------------------- | -------------------------------------------------------------------------------------- |
| wanx-background-generation-v2 | Wan-图像背景生成模型，为主体商品生成背景图，适用于电商和海报场景。支持多种背景生成方法：文本引导、图像引导、文本与图像结合引导，以及文本、图像与边缘引导元素的综合应用。 |

## 边缘引导元素生成方法

边缘引导元素生成方法因其能够有效保留图像中的边缘和结构信息，在图像背景生成任务中常用于生成前景或背景元素图像。

**步骤1**：PS 抠图，导出带透明背景的 4 通道格式图像。

**步骤2**：生成边缘引导元素图像。

针对步骤2，提供两种方案，任选一种即可。

**方案一：ModelScope 在线生成**

访问 ModelScope [背景图 edge 元素生成](https://modelscope.cn/studios/lllcho/bg_edge_elements)，直接上传第一步抠图后的图像点击运行即可获得符合要求的元素图像。

**方案二：使用代码本地生成**

安装依赖包：

```bash
pip install controlnet-aux==0.0.7
```

运行以下 Python 脚本生成边缘引导元素：

```python
import numpy as np
from PIL import Image
from controlnet_aux.processor import Processor

hed_processor = Processor('softedge_hed')

def make_elements(name):
  img=Image.open(name)
  img=np.array(img)
  img[:,:,:-1]=img[:,:,:-1]*(img[:,:,-1:]>127)
  img=Image.fromarray(img,mode='RGBA')
  r,g,b,a=img.split()
  img=Image.merge(mode='RGB',bands=[r,g,b])
  edge = hed_processor(img, to_pil=True).resize(img.size).convert('RGB')
  edge.putalpha(a)
  edge=np.array(edge)
  edge[:,:,:-1]=edge[:,:,:-1]*(edge[:,:,-1:]>50)
  edge=Image.fromarray(edge,mode='RGBA')
  edge.save('result.png')

# 使用方法：将步骤1导出的前景图路径传入
make_elements('foreground.png')
```

## 错误码

大模型服务通用状态码请查阅[错误信息](/api-reference/preparation/error-messages)。

## 常见问题

### wanx-background-generation-v3 模型不存在

**报错场景**：如果将 `model` 参数设置为 `wanx-background-generation-v3`，发送请求后报错显示模型不存在。

```json
{
    "code": "InvalidParameter",
    "message": "Model not exist.",
    "request_id": "539f3cf9-9b9c-9a0f-988f-1829c7eb502f"
}
```

**原因及解决方案**：目前图像背景生成只有 `wanx-background-generation-v2` 这一个模型。如果需要切换 V3 模型，请设置 `parameters.model_version` 为 `v3`，才能成功调用 v3 模型。

### 使用示例图片报错提示需要提供 RGBA 模式的图片

**报错场景**：将文档的示例图片下载到本地后重新上传，使用新链接请求时报错图像格式是 RGB 而非 RGBA。

```json
{
    "request_id": "8f7d6829-281a-9270-944b-xxxxxx",
    "output": {
        "task_id": "72a2d266-6822-4165-a6e4-xxxxxx",
        "task_status": "FAILED",
        "submit_time": "2024-11-07 09:51:19.xxx",
        "scheduled_time": "2024-11-07 09:51:19.xxx",
        "end_time": "2024-11-07 09:51:20.xxx",
        "code": "BadRequest.UnsupportedFileFormat",
        "message": "Base image require RGBA format, but is RGB, modes concept see https://pillow.readthedocs.io/en/stable/handbook/concepts.html#concept-modes"
    },
    "usage": {
        "image_count": 0
    }
}
```

**主要原因**：主体图像、前景元素图像或背景元素图像不是 RGBA 图像。图片从示例链接下载后再上传的过程中可能改变原始格式，例如：下载时使用不支持透明度的格式（如 .jpg、.jpeg）、上传至存储服务器时不支持 RGBA 格式，或图像编辑工具未保留透明度。

**解决方案**：确保图像保存为支持 RGBA 透明通道的格式（如 .png），并在整个上传流程中保留透明度信息。

## OpenAPI

````yaml post /services/aigc/background-generation/generation/
openapi: 3.1.0
info:
  title: 图像背景生成 API
  description: 本文介绍Wan-背景生成模型的输入输出参数。Wan-图像背景生成模型为主体商品生成背景图，适用于电商和海报场景。支持多种背景生成方法：文本引导、图像引导、文本与图像结合引导，以及文本、图像与边缘引导元素的综合应用。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 中国内地（北京）
security:
  - BearerAuth: []
paths:
  /services/aigc/background-generation/generation/:
    post:
      operationId: createBackgroundGenerationTask
      summary: 创建任务获取任务ID
      description: 提交异步背景生成任务。API 会立即返回 task_id，需轮询 GET /tasks/{task_id} 获取结果。图像模型处理时间较长，HTTP 调用仅支持异步获取模型结果。
      parameters:
        - name: Content-Type
          in: header
          required: true
          description: 请求内容类型，必须设置为 application/json。
          schema:
            type: string
            enum:
              - application/json
        - name: Authorization
          in: header
          required: true
          description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
          schema:
            type: string
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步处理配置参数。HTTP 请求只支持异步，必须设置为 enable。缺少此请求头将报错："current user api does not support synchronous calls"。
          schema:
            type: string
            enum:
              - enable
        - name: X-DashScope-WorkSpace
          in: header
          required: false
          description: 千问AI平台业务空间 ID。示例值：llm-xxxx。主账号 API-Key 可不填；RAM 子账号 API-Key 必填。
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/BackgroundGenerationRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
              examples:
                success:
                  summary: 任务已接受
                  value:
                    output:
                      task_status: PENDING
                      task_id: 0385dc79-5ff8-4d82-bcb6-xxxxxx
                    request_id: 4909100c-7b5a-9f92-bfe5-xxxxxx
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              examples:
                InvalidApiKey:
                  summary: 无效的 API Key
                  value:
                    code: InvalidApiKey
                    message: Invalid API-key provided.
                    request_id: fb53c4ec-1c12-4fc4-a580-xxxxxx
                DataInspection:
                  summary: 数据审核超时
                  value:
                    code: InvalidParameter.DataInspection
                    message: Download the media resource timed out during the data inspection process.
                    request_id: a4d78a5f-655f-9639-8437-xxxxxx
        "401":
          description: 认证失败 — API Key 无效或缺失
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
        "429":
          description: 请求频率超出限制
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "wanx-background-generation-v2",
              "input": {
                "base_image_url": "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/main_images/new_main_img/a.png",
                "ref_image_url": "http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_images/c5e50d27be534709817b2ab080b0162f_0.jpg",
                "ref_prompt": "山脉和晚霞",
                "reference_edge": {
                  "foreground_edge": [
                    "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/huaban_soft_edge/6cdd13941cef1b11d885aea1717b983ae566b8efc9094-vcsvxa_fw658webp.png",
                    "http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_edge/2c36cc4b7da027279e87311dac48fc2d5d784b1e72c0e-x4f1wC_fw658webp.png"
                  ],
                  "background_edge": [
                    "http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_edge/0718a9741e07c52ca5506e75c4f2b99e22fff68a4c7d3-P9WGLr_fw658webp.png"
                  ],
                  "foreground_edge_prompt": [
                    "粉色桃花",
                    "可爱小狗"
                  ],
                  "background_edge_prompt": [
                    "树叶"
                  ]
                }
              },
              "parameters": {
                "n": 4,
                "ref_prompt_weight": 0.5,
                "model_version": "v3"
              }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    BackgroundGenerationRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。当前仅支持填写 wanx-background-generation-v2。通过 parameters.model_version 参数切换 v2/v3 版本，请勿将 model 设置为 wanx-background-generation-v3。
          enum:
            - wanx-background-generation-v2
          example: wanx-background-generation-v2
        input:
          type: object
          required:
            - base_image_url
          description: 输入图像的基本信息。ref_image_url 和 ref_prompt 至少需要填写一个。
          properties:
            base_image_url:
              type: string
              format: uri
              description: 主体图像 URL。主体图像必须为带透明背景的 RGBA 四通道 PNG 图像，输出图像的分辨率与该图像保持一致。图像长边不超过 2048 像素。
              example: https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/main_images/new_main_img/a.png
            ref_image_url:
              type: string
              format: uri
              description: 引导图像 URL。用于引导背景风格。与 ref_prompt 至少需要填写一个。支持 jpg、png、webp 等常见格式。引导图像可以是 RGB 图像或带透明背景的 RGBA 图像。
              example: http://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_images/c5e50d27be534709817b2ab080b0162f_0.jpg
            ref_prompt:
              type: string
              description: 引导文本提示词，支持中英双语。与 ref_image_url 至少需要填写一个。英文最多支持 150 个单词，中文约 100-120 个中文字符，超过部分会被自动忽略。示例：山脉和晚霞。
              example: 山脉和晚霞
            neg_ref_prompt:
              type: string
              description: 负向提示词，描述画面不希望出现的内容。一般不填，使用模型内置的默认值。英文最多支持 150 个单词，中文约 100-120 个中文字字符。示例：低质量的，模糊的，错误的。
            reference_edge:
              type: object
              description: 边缘引导元素图像，包括前景元素图像列表和背景元素图像列表。
              properties:
                foreground_edge:
                  type: array
                  items:
                    type: string
                    format: uri
                  description: 前景元素图像 URL 列表。每个图像必须为带透明背景的 RGBA 四通道图像，分辨率和主体图像相同。所有前景元素生成的图层在主体前面，可以对主体形成遮挡。foreground_edge 和 background_edge 图像列表之和不得超过 10。
                foreground_edge_prompt:
                  type: array
                  items:
                    type: string
                  description: 前景元素列表对应的 prompt 列表。如果输入该参数，长度必须和 foreground_edge 列表相等，且顺序一一对应。无需填写某个元素的 prompt 时，可用空字符串占位。
                background_edge:
                  type: array
                  items:
                    type: string
                    format: uri
                  description: 背景元素图像 URL 列表。每个图像必须为带透明背景的 RGBA 四通道图像。生成图层在主体的后面，如果重叠会被主体遮挡。foreground_edge 和 background_edge 图像列表之和不得超过 10。
                background_edge_prompt:
                  type: array
                  items:
                    type: string
                  description: 背景元素列表对应的 prompt 列表。如果输入该参数，长度必须和 background_edge 列表相等，且顺序一一对应。无需填写某个元素的 prompt 时，可用空字符串占位。
            title:
              type: string
              deprecated: true
              description: 已废弃，建议使用图配文。图像上添加文字主标题，算法自动确定文字的大小和位置，限制 1-8 个字符。
              minLength: 1
              maxLength: 8
            sub_title:
              type: string
              deprecated: true
              description: 已废弃，建议使用图配文。图像上添加文字副标题，算法自动确定文字的大小和位置，限制 1-10 个字符。仅当 title 不为空时生效。
              minLength: 1
              maxLength: 10
        parameters:
          type: object
          description: 图像处理参数。
          properties:
            n:
              type: integer
              description: 图片生成的数量，支持 1-4 张，默认值 1。
              minimum: 1
              maximum: 4
              default: 1
              example: 4
            model_version:
              type: string
              description: 模型版本。v2：旧版模型，速度快（默认值）。v3：新版模型，速度稍慢但效果更好，推荐切换到 v3。
              enum:
                - v2
                - v3
              default: v2
              example: v3
            noise_level:
              type: integer
              description: 当 ref_image_url 不为空时生效。该参数在图像引导的过程中添加随机变化，数值越大生成背景与引导图像的相关性越低。默认值 300，取值范围 [0, 999]。
              minimum: 0
              maximum: 999
              default: 300
            ref_prompt_weight:
              type: number
              description: 仅当 ref_image_url 和 ref_prompt 同时输入时生效，表示引导文本 prompt 的权重。取值范围 [0, 1]，默认值 0.5。数值越大表示引导文本对生成背景的影响程度越大。
              minimum: 0
              maximum: 1
              default: 0.5
              example: 0.5
            scene_type:
              type: string
              deprecated: true
              description: 已废弃，不建议使用。使用场景：GENERAL（通用场景，默认值）、ROOM（室内家居场景）、COSMETIC（美妆场景，也适用于大部分小商品摆放场景）。
              enum:
                - GENERAL
                - ROOM
                - COSMETIC
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。
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
              description: 任务 ID。用于查询任务状态及结果，查询有效期 24 小时。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
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
    TaskStatusResponse:
      type: object
      description: 任务状态轮询响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: ded2407a-ec61-4a7d-adc0-xxxxxxxxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            task_id:
              type: string
              description: 任务 ID。查询有效期 24 小时。
              example: 86ecf553-d340-4e21-xxxxxxxxx
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
              description: 任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-12-23 10:25:26.436
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-12-23 10:25:26.471
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2025-12-23 10:26:06.390
            results:
              type: array
              description: 返回结果图像。仅在 task_status 为 SUCCEEDED 时返回。图像分辨率与输入图像（base_image_url）保持一致。
              items:
                type: object
                properties:
                  url:
                    type: string
                    format: uri
                    description: 生成图像的 URL。有效期 24 小时，请及时下载保存。
                    example: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx.png?Expires=xxx
            code:
              type: string
              description: 错误码。仅在 task_status 为 FAILED 时返回。
              example: InvalidParameter.FileDownload
            message:
              type: string
              description: 错误详情。仅在 task_status 为 FAILED 时返回。
              example: download for input_image error
            task_metrics:
              type: object
              description: 任务结果统计。
              properties:
                TOTAL:
                  type: integer
                  description: 总的任务数。
                  example: 4
                SUCCEEDED:
                  type: integer
                  description: 任务状态为成功的任务数。
                  example: 4
                FAILED:
                  type: integer
                  description: 任务状态为失败的任务数。
                  example: 0
        usage:
          type: object
          description: 输出信息统计。计费公式：费用 = 图片数量 × 单价。
          properties:
            image_count:
              type: integer
              description: 模型成功生成图片的数量。
              example: 4
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。
          example: fb53c4ec-1c12-4fc4-a580-xxxxxx
        code:
          type: string
          description: 请求失败的错误码。请求成功时不会返回此参数。
          example: InvalidApiKey
        message:
          type: string
          description: 请求失败的详细信息。请求成功时不会返回此参数。
          example: Invalid API-key provided.
````
