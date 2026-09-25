> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# AI试衣 — 创建任务

> 提交AI试衣任务

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## OpenAPI

````yaml post /services/aigc/image2image/image-synthesis
openapi: 3.1.0
info:
  title: AI试衣 API
  version: 1.0.0
  description: AI试衣模型支持使用服饰平拍图片以及人物正面全身照，生成逼真的试衣效果图。提供两个模型：aitryon（基础版，生成更快）和 aitryon-plus（Plus版，在图像清晰度、布料纹理和 Logo 还原方面表现更出色，但生成耗时更长）。两个模型的接口参数完全一致，仅 model 字段不同。
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
paths:
  /services/aigc/image2image/image-synthesis:
    post:
      operationId: createAiTryonTask
      summary: 创建试衣任务
      description: 发送 POST 请求创建AI虚拟试衣任务。因该模型调用耗时较长，故采用异步调用的方式创建任务。任务创建后，系统会立即返回一个 task_id，需使用此 task_id 在24小时内查询任务结果。
      security:
        - BearerAuth: []
      parameters:
        - name: Content-Type
          in: header
          required: true
          description: 请求类型，固定值为 application/json。
          schema:
            type: string
            default: application/json
        - name: Authorization
          in: header
          required: true
          description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
          schema:
            type: string
        - name: X-DashScope-Async
          in: header
          required: true
          description: 固定值为 enable，表示使用异步调用方式。
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
              $ref: "#/components/schemas/AiTryonRequest"
      responses:
        "200":
          description: 任务提交成功。
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
              examples:
                InvalidParameter:
                  summary: 参数缺失或格式错误
                  value:
                    code: InvalidParameter
                    message: The request is missing required parameters or in a wrong format, please check the parameters that you send.
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
                InvalidURL:
                  summary: 图片URL无效
                  value:
                    code: InvalidURL
                    message: "The request URL is invalid, please check the request URL is available and the request image format is one of the following types: JPEG, JPG, PNG, BMP, and WEBP."
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
                InvalidPerson:
                  summary: 模特图不合规
                  value:
                    code: InvalidPerson
                    message: The input image has no human body or multi human bodies. Please upload other image with single person.
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
                InvalidGarment:
                  summary: 缺少服饰图片
                  value:
                    code: InvalidGarment
                    message: Missing clothing image.Please input at least one top garment or bottom garment image.
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
                InvalidInputLength:
                  summary: 图片尺寸或文件大小不符合要求
                  value:
                    code: InvalidInputLength
                    message: The image resolution is invalid, please make sure that the largest length of image is smaller than 4096, and the smallest length of image is larger than 150. and the size of image ranges from 5KB to 5MB.
                    request_id: 7438d53d-6eb8-4596-8835-xxxxxx
        "401":
          description: 认证失败。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: InvalidApiKey
                message: No API-key provided.
                request_id: 7438d53d-6eb8-4596-8835-xxxxxx
        "429":
          description: 请求频率超过限制。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
              example:
                code: Throttling
                message: Requests throttling triggered.
                request_id: fb53c4ec-1c12-4fc4-a580-xxxxxxxxxxxx
      x-codeSamples:
        - lang: curl
          label: 试穿上装
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
                "model": "aitryon",
                "input": {
                    "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
                    "top_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/epousa/short_sleeve.jpeg"
                },
                "parameters": {
                    "resolution": -1,
                    "restore_face": true
                }
             }'
        - lang: curl
          label: 试穿上装（保留原下装）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
                "model": "aitryon",
                "input": {
                    "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
                    "top_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/epousa/short_sleeve.jpeg",
                    "bottom_garment_url": "图片分割API输出的图像URL"
                },
                "parameters": {
                    "resolution": -1,
                    "restore_face": true
                }
             }'
        - lang: curl
          label: 试穿下装
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
                "model": "aitryon",
                "input": {
                    "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
                    "bottom_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/rchumi/pants.jpeg"
                },
                "parameters": {
                    "resolution": -1,
                    "restore_face": true
                }
            }'
        - lang: curl
          label: 试穿下装（保留原上衣）
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
                "model": "aitryon",
                "input": {
                    "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
                    "top_garment_url": "图片分割API输出的图像URL",
                    "bottom_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/rchumi/pants.jpeg"
                },
                "parameters": {
                    "resolution": -1,
                    "restore_face": true
                }
             }'
        - lang: curl
          label: 试穿上下装
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
                "model": "aitryon",
                "input": {
                    "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
                    "top_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/epousa/short_sleeve.jpeg",
                    "bottom_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/rchumi/pants.jpeg"
                },
                "parameters": {
                    "resolution": -1,
                    "restore_face": true
                }
            }'
        - lang: curl
          label: 试穿连衣裙/连体服
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
                "model": "aitryon",
                "input": {
                    "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
                    "top_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/odngby/dress.jpg"
                },
                "parameters": {
                    "resolution": -1,
                    "restore_face": true
                }
            }'
        - lang: curl
          label: Plus版-试穿上装
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis/' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
                "model": "aitryon-plus",
                "input": {
                    "person_image_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/ubznva/model_person.png",
                    "top_garment_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250626/epousa/short_sleeve.jpeg"
                },
                "parameters": {
                    "resolution": -1,
                    "restore_face": true
                }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    AiTryonRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 指明需要调用的模型。`aitryon`（基础版）生成更快；`aitryon-plus`（Plus版）在清晰度和纹理还原方面更出色，但耗时更长。
          enum:
            - aitryon
            - aitryon-plus
          default: aitryon
        input:
          type: object
          required:
            - person_image_url
          description: 输入参数。
          properties:
            person_image_url:
              type: string
              format: uri
              description: 模特人物图片的公网URL。5KB≤图像文件≤5M，150≤图像边长≤4096，格式支持jpg/png/jpeg/bmp/heic。需保持图片中有且仅有一个完整的人。仅支持HTTP/HTTPS链接，不支持本地路径。
            top_garment_url:
              type: string
              format: uri
              description: 上装/连衣裙服饰图的公网URL。需上传服饰平拍图，保持服饰是单一主体且完整，背景干净，四周不宜留白过多。对于连衣裙/连体衣，请将图片URL填入此字段，并将 bottom_garment_url 留空。5KB≤图像文件≤5M，150≤图像边长≤4096，格式支持jpg/png/jpeg/bmp/heic。仅支持HTTP/HTTPS链接，不支持本地路径。
            bottom_garment_url:
              type: string
              format: uri
              description: 下装服饰图的公网URL。5KB≤图像文件≤5M，150≤图像边长≤4096，格式支持jpg/png/jpeg/bmp/heic。需上传服饰平拍图，保持服饰是单一主体且完整，背景干净，四周不宜留白过多。仅支持HTTP/HTTPS链接，不支持本地路径。
        parameters:
          type: object
          description: 可选参数。
          properties:
            resolution:
              type: integer
              description: 输出图片的分辨率。-1（默认值）：与原图尺寸保持一致；1024：表示 576x1024 分辨率；1280：表示 720x1280 分辨率。若后续还需调用AI试衣-图片精修API，此值必须设为 -1。
              enum:
                - -1
                - 1024
                - 1280
              default: -1
            restore_face:
              type: boolean
              description: 是否还原模特图中的人脸。true（默认值）：保留原图人脸；false：随机生成一张新的人脸。若后续还需调用AI试衣-图片精修API，此值必须设为 true。
              default: true
    AsyncTaskSubmitResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 异步任务的唯一ID。
            task_status:
              type: string
              description: 任务提交后的状态。
              enum:
                - PENDING
        request_id:
          type: string
          description: 本次请求的唯一ID。
    TaskStatusResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 查询的任务ID。
            task_status:
              type: string
              description: 任务状态。
              enum:
                - PENDING
                - PRE-PROCESSING
                - RUNNING
                - POST-PROCESSING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
                - CANCELED
            image_url:
              type: string
              format: uri
              description: 生成的试衣效果图地址。image_url有效期为24小时，请及时下载。
            submit_time:
              type: string
              description: 任务提交时间。
            scheduled_time:
              type: string
              description: 任务执行时间。
            end_time:
              type: string
              description: 任务完成时间。
            code:
              type: string
              description: 错误码。任务失败时返回此参数。
            message:
              type: string
              description: 错误详情。任务失败时返回此参数。
        usage:
          type: object
          properties:
            image_count:
              type: integer
              description: 本次请求生成的图片张数。
        request_id:
          type: string
          description: 本次请求的唯一ID。
    DashScopeErrorResponse:
      type: object
      properties:
        code:
          type: string
          description: 错误码。
        message:
          type: string
          description: 错误信息。
        request_id:
          type: string
          description: 请求ID。
````
