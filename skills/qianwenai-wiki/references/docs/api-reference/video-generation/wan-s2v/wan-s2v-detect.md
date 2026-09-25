> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 数字人图像检测

> 检测图像是否符合 wan2.2-s2v 视频生成模型的人物图像规格要求

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

万相数字人图像检测用于判断输入图像是否符合 wan2.2-s2v 视频生成模型的人物图像规格要求，通常在数字人视频生成前作为图像筛选步骤使用。

## OpenAPI

````yaml post /services/aigc/image2video/face-detect
openapi: 3.1.0
info:
  title: Wan Portrait Image Detection API
  description: 万相数字人图像检测 API。检测输入图像是否符合 wan2.2-s2v 视频生成模型的人物图像规格要求。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/image2video/face-detect:
    post:
      operationId: detectWanPortrait
      summary: 检测人物图像
      description: 检测输入图像是否符合 wan2.2-s2v 视频生成模型的人物图像规格要求。返回图像是否通过检测以及是否检测到人像。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/WanDetectRequest"
      responses:
        "200":
          description: 检测成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/WanDetectResponse"
              examples:
                pass:
                  summary: 检测通过
                  value:
                    output:
                      check_pass: true
                      humanoid: true
                    usage:
                      image_count: 1
                    request_id: c56f62df-724e-9c19-96bd-xxxxxx
                fail:
                  summary: 检测未通过
                  value:
                    output:
                      check_pass: false
                      code: ""
                      message: ""
                    usage:
                      image_count: 1
                    request_id: c56f62df-724e-9c19-96bd-xxxxxx
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
          description: 超出速率限制（RPS 上限为 5）
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
            curl 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/face-detect' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "wan2.2-s2v-detect",
              "input": {
                "image_url": "https://img.alicdn.com/imgextra/i3/O1CN011FObkp1T7Ttowoq4F_!!6000000002335-0-tps-1440-1797.jpg"
              }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    WanDetectRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称，固定为 `wan2.2-s2v-detect`。
          enum:
            - wan2.2-s2v-detect
          example: wan2.2-s2v-detect
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
                - **格式**：JPG、JPEG、PNG、BMP、WEBP
                - **分辨率**：宽和高必须在 400 到 7000 像素之间
                - **URL**：必须为 HTTP 或 HTTPS 协议的公网可访问地址

                <Tip>如需将本地图像上传获取临时 URL，请参考[上传文件获取临时 URL](/api-reference/platform-api/file/upload-file)。</Tip>
              example: https://img.alicdn.com/imgextra/i3/O1CN011FObkp1T7Ttowoq4F_!!6000000002335-0-tps-1440-1797.jpg
    WanDetectResponse:
      type: object
      description: 人物图像检测响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识符，用于链路追踪和问题排查。
          example: c56f62df-724e-9c19-96bd-xxxxxx
        output:
          type: object
          description: 检测结果。
          properties:
            check_pass:
              type: boolean
              description: 图像是否通过检测。`true` 表示图像符合 wan2.2-s2v 模型的人物图像规格要求，`false` 表示不符合。
              example: true
            humanoid:
              type: boolean
              description: 图像中是否检测到人像。`true` 表示检测到人像，`false` 表示未检测到。
              example: true
            code:
              type: string
              description: 检测未通过时的错误码。检测通过时不返回此字段。
            message:
              type: string
              description: 检测未通过时的错误描述。检测通过时不返回此字段。
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
