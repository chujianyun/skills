> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# EMO — 图像检测

> 检测图像是否符合 EMO 视频生成模型的人物肖像图片规范

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[配置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

EMO 图像检测用于判断输入图像是否符合 EMO 视频生成模型的人物肖像图片规范，通常在生成唱演视频前作为图像筛选步骤使用。检测通过后会返回人脸区域坐标和动态区域坐标，可直接作为 EMO 视频生成 API 的入参。

## OpenAPI

````yaml post /services/aigc/image2video/face-detect
openapi: 3.1.0
info:
  title: EMO Portrait Image Detection API
  description: EMO 图像检测 API。检测输入图像是否符合 EMO 视频生成模型的人物肖像图片规范。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/image2video/face-detect:
    post:
      operationId: detectEmoPortrait
      summary: EMO 图像检测
      description: 检测输入图像是否符合 EMO 视频生成模型的人物肖像图片规范。返回图像是否通过检测、人脸区域坐标和动态区域坐标。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/EmoDetectRequest"
      responses:
        "200":
          description: 检测成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/EmoDetectResponse"
              examples:
                pass:
                  summary: 图像检测通过
                  value:
                    output:
                      check_pass: true
                      face_bbox:
                        - 302
                        - 286
                        - 610
                        - 593
                      ext_bbox:
                        - 71
                        - 9
                        - 840
                        - 778
                      humanoid: true
                    usage:
                      image_count: 1
                    request_id: c56f62df-724e-9c19-96bd-xxxxxx
                fail:
                  summary: 图像检测不通过
                  value:
                    output:
                      check_pass: false
                      humanoid: false
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
            curl 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/face-detect' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "emo-detect-v1",
              "input": {
                "image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251225/onmomb/emo.png"
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
    EmoDetectRequest:
      type: object
      required:
        - model
        - input
        - parameters
      properties:
        model:
          type: string
          description: 模型名称，固定为 `emo-detect-v1`。
          enum:
            - emo-detect-v1
          example: emo-detect-v1
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

                <Tip>如需将本地图像上传获取临时 URL，请参考[上传文件获取临时URL](/api-reference/platform-api/file/upload-file)。</Tip>
              example: https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251225/onmomb/emo.png
        parameters:
          type: object
          required:
            - ratio
          description: 检测参数。
          properties:
            ratio:
              type: string
              description: |-
                希望检测确认的画幅比例。

                - `1:1`：适用于头像图片（默认值）
                - `3:4`：适用于半身像图片
              enum:
                - 1:1
                - 3:4
              default: 1:1
              example: 1:1
    EmoDetectResponse:
      type: object
      description: EMO 图像检测响应。
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
              description: 图像是否通过检测。`true` 表示图像符合 EMO 视频生成模型的人物肖像图片规范，`false` 表示不符合。
              example: true
            face_bbox:
              type: array
              items:
                type: integer
              description: 算法检测到的人脸区域坐标 `[x1, y1, x2, y2]`，对应左上和右下两个点的坐标。可将该值作为 EMO 视频生成 API 的入参。检测通过时返回。
              example:
                - 302
                - 286
                - 610
                - 593
            ext_bbox:
              type: array
              items:
                type: integer
              description: 算法预测的动态区域坐标 `[x1, y1, x2, y2]`，对应左上和右下两个点的坐标。该区域的宽高比与入参画幅一致。可将该值作为 EMO 视频生成 API 的入参。检测通过时返回。
              example:
                - 71
                - 9
                - 840
                - 778
            humanoid:
              type: boolean
              description: 检测到的对象是否为人像。`true` 表示检测到人像，`false` 表示未检测到人像。
              example: true
            code:
              type: string
              description: 检测未通过或请求失败时的错误码。检测通过时不返回此字段。
            message:
              type: string
              description: 检测未通过或请求失败时的错误描述。检测通过时不返回此字段。
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
