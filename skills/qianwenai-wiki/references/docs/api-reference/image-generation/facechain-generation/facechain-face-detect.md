> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# FaceChain — 图像检测

> 检测图像中是否包含符合要求的人脸

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

FaceChain 人物图像检测用于判断输入图像是否包含符合要求的人脸，通常在人物写真生成前作为图像筛选步骤使用。

**限制**：每个账号 QPS 上限为 5。

## OpenAPI

````yaml post /services/vision/facedetection/detect
openapi: 3.1.0
info:
  title: FaceChain Face Detection API
  description: 人物图像检测 API。检测输入图像中是否包含人脸，用于人物写真生成前的图像筛选。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: Beijing
security:
  - BearerAuth: []
paths:
  /services/vision/facedetection/detect:
    post:
      operationId: detectFace
      summary: 检测人脸
      description: 检测输入图像中是否包含符合要求的人脸。支持批量输入多张图像，返回每张图像的检测结果。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/FaceDetectionRequest"
      responses:
        "200":
          description: 检测成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/FaceDetectionResponse"
              examples:
                success:
                  summary: 检测成功
                  value:
                    output:
                      is_face:
                        - true
                        - false
                        - true
                      failed_reason:
                        - ""
                        - no face detected
                        - ""
                    usage: {}
                    request_id: 549e0573-f630-9c17-8df2-08f605b4a646
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
                    message: Required parameter(s) missing or invalid, please check the request parameters.
                    request_id: fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1
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
        "429":
          description: 超出速率限制（QPS 上限为 5）
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
              examples:
                InternalErrorAlgo:
                  summary: 算法执行异常
                  value:
                    code: InternalError.Algo
                    message: 服务内部算法执行异常。常见原因为输入的图片 URL 包含非 ASCII 字符（如中文），请对 URL 进行编码处理后重试。
                    request_id: fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1
      x-codeSamples:
        - lang: curl
          label: cURL
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/vision/facedetection/detect' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "facechain-facedetect",
              "input": {
                "images": [
                  "https://example.com/image1.png",
                  "https://example.com/image2.jpg",
                  "https://example.com/image3.png"
                ]
              },
              "parameters": {}
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    FaceDetectionRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称，固定为 `facechain-facedetect`。
          enum:
            - facechain-facedetect
          example: facechain-facedetect
        input:
          type: object
          required:
            - images
          description: 输入图像参数。
          properties:
            images:
              type: array
              items:
                type: string
                format: uri
              description: |-
                待检测图像的公网可访问 URL 列表。

                **图像要求**：
                - **格式**：JPEG、PNG、JPG、WEBP
                - **分辨率**：宽和高必须在 256 到 4096 像素之间
                - **文件大小**：不超过 5 MB

                > **重要**
                >
                > 图片 URL 中如果包含非 ASCII 字符（如中文文件名），需要先进行 URL 编码（percent-encoding），否则可能导致 `InternalError.Algo` 错误。例如，在 Python 中使用 `urllib.parse.quote()`，在 JavaScript 中使用 `encodeURI()` 对 URL 进行编码。

                **选图建议**（用于人物写真生成）：
                - 每张图像仅包含 1 张人脸
                - 五官清晰可见、正面照
                - 人脸区域大于 128x128 像素
                - 避免佩戴墨镜或面部遮挡
                - 避免浓妆
              example:
                - https://example.com/image1.png
                - https://example.com/image2.jpg
        parameters:
          type: object
          description: 生成参数。当前无可用参数，传空对象 `{}` 即可。
          properties: {}
    FaceDetectionResponse:
      type: object
      description: 人脸检测响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符，用于链路追踪和问题排查。
          example: 549e0573-f630-9c17-8df2-08f605b4a646
        output:
          type: object
          description: 检测结果。
          properties:
            is_face:
              type: array
              items:
                type: boolean
              description: 每张输入图像的人脸检测结果。`true` 表示检测到符合要求的人脸，`false` 表示未检测到。数组顺序与输入图像顺序一致。
              example:
                - true
                - false
                - true
            failed_reason:
              type: array
              items:
                type: string
              description: 每张输入图像的检测失败原因。检测通过时为空字符串 `""`，未通过时返回具体原因（如 `"no face detected"`）。数组顺序与输入图像顺序一致。
              example:
                - ""
                - no face detected
                - ""
        usage:
          type: object
          description: 使用量统计。当前为空对象。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符。
          example: fb53c4ec-1c12-4fc4-a580-cdb7c3261fc1
        code:
          type: string
          description: 错误码。
          example: InvalidParameter
        message:
          type: string
          description: 错误描述信息。
          example: Required parameter(s) missing or invalid, please check the request parameters.
````
