> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# LivePortrait 图像检测

> 检测人物肖像图片是否符合 LivePortrait 视频生成模型的输入规范

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

LivePortrait-detect 模型用于检测输入的图片是否满足 [LivePortrait 视频生成](/api-reference/video-generation/liveportrait-video/create-task)所需的人物肖像图片规范，通常在生成数字人播报视频前作为图像筛选步骤使用。

## 模型概览

| 模型名                 | 模型简介                                                |
| ------------------- | --------------------------------------------------- |
| liveportrait-detect | 特定的图像检测模型，用于检测输入的图片是否满足 LivePortrait 模型所需的人物肖像图片规范。 |

## 输入限制

- 图像格式：JPEG、JPG、PNG、BMP、WEBP
- 文件大小：小于 10 MB
- 宽高比：不超过 2
- 最大边长：不超过 4096 像素
- 仅支持 HTTP 或 HTTPS 公网链接，不支持本地路径

<Note>
  如需将本地图像上传获取临时公网 URL，请参考[上传文件获取临时 URL](/api-reference/platform-api/file/upload-file)。
</Note>

## 检测不通过原因

| output.message          | 原因说明                    |
| ----------------------- | ----------------------- |
| No human face detected. | 未检测到人脸（包括人脸过小、侧脸、遮挡等情况） |

## 状态码说明

通用错误码请参阅[错误信息](/api-reference/preparation/error-messages)。

## OpenAPI

````yaml post /services/aigc/image2video/face-detect
openapi: 3.1.0
info:
  title: LivePortrait 图像检测 API
  description: LivePortrait-detect 模型，用于确认输入的人物肖像图片是否符合 LivePortrait 模型的输入规范。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 中国内地（北京）
security:
  - BearerAuth: []
paths:
  /services/aigc/image2video/face-detect:
    post:
      operationId: detectLivePortraitImage
      summary: 检测人物肖像图像
      description: 检测输入的图片是否满足 LivePortrait 视频生成模型所需的人物肖像图片规范。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/LivePortraitDetectRequest"
      responses:
        "200":
          description: 检测成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/LivePortraitDetectResponse"
              examples:
                pass:
                  summary: 检测通过
                  value:
                    output:
                      pass: true
                      message: ""
                    usage:
                      image_count: 1
                    request_id: a92e2ffd-9263-44ba-92c5-xxxxxx
                fail:
                  summary: 检测不通过
                  value:
                    output:
                      pass: false
                      message: No human face detected.
                    usage:
                      image_count: 1
                    request_id: c56f62df-724e-9c19-96bd-xxxxxx
                error:
                  summary: 请求错误
                  value:
                    code: InvalidParameter.UnsupportedFileFormat
                    message: Input files format not supported.
                    request_id: 788b30fe-05f6-999f-a0b1-xxxxxx
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              examples:
                UnsupportedFileFormat:
                  summary: 文件格式不支持
                  value:
                    code: InvalidParameter.UnsupportedFileFormat
                    message: Input files format not supported.
                    request_id: 788b30fe-05f6-999f-a0b1-xxxxxx
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
                    message: Invalid API-key provided.
                    request_id: fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1
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
              "model": "liveportrait-detect",
              "input": {
                "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250911/ynhjrg/p874909.png"
              }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    LivePortraitDetectRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称，固定为 `liveportrait-detect`。
          enum:
            - liveportrait-detect
          example: liveportrait-detect
        input:
          type: object
          required:
            - image_url
          description: 输入图像参数。
          properties:
            image_url:
              type: string
              format: uri
              description: |-
                待检测图像的公网可访问 URL。

                **图像要求**：
                - **格式**：JPEG、JPG、PNG、BMP、WEBP
                - **文件大小**：小于 10 MB
                - **宽高比**：不超过 2
                - **最大边长**：不超过 4096 像素
                - **URL**：必须为 HTTP 或 HTTPS 协议的公网可访问地址，不支持本地路径
              example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250911/ynhjrg/p874909.png
    LivePortraitDetectResponse:
      type: object
      description: 人物肖像图像检测响应。
      properties:
        request_id:
          type: string
          description: 本次请求的系统唯一码，用于链路追踪和问题排查。
          example: a92e2ffd-9263-44ba-92c5-xxxxxx
        output:
          type: object
          description: 检测结果。
          properties:
            pass:
              type: boolean
              description: 图像是否通过检测。`true` 表示图像符合 LivePortrait 模型的人物肖像规范，`false` 表示不符合。
              example: true
            message:
              type: string
              description: 检测结果信息。检测通过时为空字符串；检测不通过时返回原因，例如 `No human face detected.`（未检测到人脸，包括人脸过小、侧脸、遮挡等情况）。
              example: ""
        usage:
          type: object
          description: 使用量统计。
          properties:
            image_count:
              type: integer
              description: 本次检测的图像数量，固定为 `1`。用于计费。
              example: 1
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
          example: 788b30fe-05f6-999f-a0b1-xxxxxx
        code:
          type: string
          description: 错误码。
          example: InvalidParameter.UnsupportedFileFormat
        message:
          type: string
          description: 错误描述信息。
          example: Input files format not supported.
````
