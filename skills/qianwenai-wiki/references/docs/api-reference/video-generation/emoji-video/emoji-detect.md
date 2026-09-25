> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Emoji — 图像检测

> 检测图像中的人物形象是否满足表情包 Emoji 视频生成模型的要求

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

`emoji-detect-v1` 是一个图像合规性检测模型，用于判断输入图像中的人物形象是否满足表情包 Emoji 模型的要求。检测通过后，模型输出人脸区域及扩展后的动态表情区域坐标，供后续 Emoji 视频生成使用。

## 模型概览

| 模型名称            | 模型简介                                                                                           |
| --------------- | ---------------------------------------------------------------------------------------------- |
| emoji-detect-v1 | 检测输入的图像是否符合 Emoji 视频生成所需要的图像规范。检测通过后，输出人脸区域（bbox\_face）和扩展后的动态表情区域（ext\_bbox\_face）坐标，供视频生成使用。 |

## 输入图像要求

**合规图像（检测通过）需满足**：

- **单人正面肖像**
- **面部无遮挡**（如手、头发、饰品等）
- **表情自然**，无夸张表情
- **头部姿态端正**，无大幅度倾斜

**不合规图像示例（检测失败）**：

| 脸部区域附近露出手部 | 存在面部遮挡 | 存在夸张表情 | 头部倾斜角度过大 |
| ---------- | ------ | ------ | -------- |
| 手部遮挡       | 面部被遮挡  | 夸张表情   | 头部倾斜     |

## 计费与限流

- 模型免费额度和计费单价请参见[模型价格](/developer-guides/getting-started/pricing)。
- 模型限流请参见[限流](/developer-guides/administration/rate-limits)。

<Note>
  当图像因不合规而导致检测不通过时，本次 API 调用仍会正常计费，因为模型已经执行了完整的检测流程。
</Note>

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](/api-reference/preparation/error-messages)进行解决。

## OpenAPI

````yaml post /services/aigc/image2video/face-detect
openapi: 3.1.0
info:
  title: Emoji 图像检测 API
  description: 检测输入图像中的人物形象是否满足表情包 Emoji 模型的要求。检测通过后返回人脸区域及扩展后的动态表情区域坐标，供后续 Emoji 视频生成使用。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/image2video/face-detect:
    post:
      operationId: detectEmojiPortrait
      summary: Emoji 图像检测
      description: 检测输入图像中的人物形象是否满足表情包 Emoji 模型（emoji-detect-v1）的要求。检测通过后，返回人脸区域坐标（bbox_face）和扩展后的动态表情区域坐标（ext_bbox_face），可直接作为 Emoji 视频生成 API 的入参。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/EmojiDetectRequest"
      responses:
        "200":
          description: 请求成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/EmojiDetectResponse"
              examples:
                pass:
                  summary: 检测通过
                  value:
                    output:
                      bbox_face:
                        - 212
                        - 194
                        - 460
                        - 441
                      ext_bbox_face:
                        - 63
                        - 30
                        - 609
                        - 575
                    usage:
                      image_count: 1
                    request_id: 78becbc4-f7f7-41ea-9e38-xxxxxx
                fail_detection:
                  summary: 检测不通过
                  value:
                    output:
                      code: InvalidFile.FacePose
                      message: The pose of the detected face is invalid, please upload other image with the expected oriention.
                    usage:
                      image_count: 1
                    request_id: ed0d0d8f-e55a-4144-b855-xxxxxx
                fail_request:
                  summary: 请求失败
                  value:
                    request_id: 5e1fefbd-fa7a-4e59-82a0-xxxxxx
                    code: InvalidParameter
                    message: Required body invalid, please check the request body format.
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              examples:
                InvalidParameter:
                  summary: 参数缺失或无效
                  value:
                    code: InvalidParameter
                    message: Required body invalid, please check the request body format.
                    request_id: 5e1fefbd-fa7a-4e59-82a0-xxxxxx
        "401":
          description: 认证失败 — API Key 无效或缺失
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              examples:
                InvalidApiKey:
                  summary: API Key 无效
                  value:
                    code: InvalidApiKey
                    message: No API-key provided.
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
        "429":
          description: 超出速率限制
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
        "500":
          description: 服务端内部错误
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/face-detect' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "emoji-detect-v1",
              "input": {
                "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250912/uopnly/emoji-%E5%9B%BE%E5%83%8F%E6%A3%80%E6%B5%8B.png"
              },
              "parameters": {
                "ratio": "1:1"
              }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    EmojiDetectRequest:
      type: object
      required:
        - model
        - input
        - parameters
      properties:
        model:
          type: string
          description: 模型名称，固定为 `emoji-detect-v1`。
          enum:
            - emoji-detect-v1
          example: emoji-detect-v1
        input:
          type: object
          required:
            - image_url
          description: 输入的基本信息，如待检测图像。
          properties:
            image_url:
              type: string
              format: uri
              description: |-
                待检测图像的公网 URL。支持 HTTP 或 HTTPS 协议。

                **图像限制**：
                - **格式**：JPEG、JPG、PNG、BMP、WEBP
                - **分辨率**：宽度和高度均在 400 到 7000 像素之间
                - **文件大小**：不超过 10 MB

                本地文件可通过[上传文件获取临时 URL](/api-reference/platform-api/file/upload-file)。
              example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250912/uopnly/emoji-%E5%9B%BE%E5%83%8F%E6%A3%80%E6%B5%8B.png
        parameters:
          type: object
          required:
            - ratio
          description: 图像处理参数。
          properties:
            ratio:
              type: string
              description: 待检测区域的长宽比。对于 Emoji 视频生成，此值固定为 `1:1`。
              enum:
                - 1:1
              example: 1:1
    EmojiDetectResponse:
      type: object
      description: Emoji 图像检测响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识，可用于请求明细溯源和问题排查。
          example: 78becbc4-f7f7-41ea-9e38-xxxxxx
        output:
          type: object
          description: 任务输出信息。
          properties:
            bbox_face:
              type: array
              items:
                type: integer
              description: 检测到的人脸区域坐标，格式为 `[x1, y1, x2, y2]`，单位为像素，对应左上和右下两个点的坐标。仅在检测通过时返回。此值应作为 Emoji 视频生成接口 `input.face_bbox` 参数的值。
              example:
                - 212
                - 194
                - 460
                - 441
            ext_bbox_face:
              type: array
              items:
                type: integer
              description: 扩展后的动态表情区域坐标，格式为 `[x1, y1, x2, y2]`，单位为像素，对应左上和右下两个点的坐标。仅在检测通过时返回。此值应作为 Emoji 视频生成接口 `input.ext_bbox` 参数的值。
              example:
                - 63
                - 30
                - 609
                - 575
            code:
              type: string
              description: 错误码。仅在检测不通过时返回，详情请参见[错误信息](/api-reference/preparation/error-messages)。
            message:
              type: string
              description: 错误信息。仅在检测不通过时返回，详情请参见[错误信息](/api-reference/preparation/error-messages)。
        usage:
          type: object
          description: 输出信息统计。
          properties:
            image_count:
              type: integer
              description: 本次请求检测图像数量，固定为 1 张，用于计费。无论检测是否通过，只要请求成功就计费；请求失败不计费。
              example: 1
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
          example: 5e1fefbd-fa7a-4e59-82a0-xxxxxx
        code:
          type: string
          description: 错误码。
          example: InvalidParameter
        message:
          type: string
          description: 错误描述信息。
          example: Required body invalid, please check the request body format.
````
