> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 查询文件列表

## OpenAPI

````yaml get /files
openapi: 3.1.0
info:
  title: 千问AI平台 File API
  description: 上传并管理文件，用于文档解析或批量处理。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/compatible-mode/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /files:
    get:
      operationId: listFiles
      summary: 查询文件列表
      description: 列出账户下所有文件（包括已上传的文件和批量处理结果），支持按用途、创建时间筛选，并提供分页功能。
      parameters:
        - name: after
          in: query
          required: false
          description: 分页游标。设置为当前页最后一项的 `id`，即可获取下一页数据。
          schema:
            type: string
            example: file-batch-xxx
        - name: limit
          in: query
          required: false
          description: 每页返回的文件数量，范围 1-2,000，默认值为 2,000。
          schema:
            type: integer
            minimum: 1
            maximum: 2000
            default: 2000
        - name: purpose
          in: query
          required: false
          description: 按用途筛选文件，可选值：`file-extract`、`batch`。
          schema:
            type: string
            enum:
              - file-extract
              - batch
        - name: create_before
          in: query
          required: false
          description: 筛选在此时间之前创建的文件，支持格式：`yyyyMMddHHmmss`、`yyyy-MM-dd HH:mm:ss`、`yyyy-MM-dd`、`yyyyMMdd`。
          schema:
            type: string
            example: "20250306123000"
        - name: create_after
          in: query
          required: false
          description: 筛选在此时间之后创建的文件，支持格式：`yyyyMMddHHmmss`、`yyyy-MM-dd HH:mm:ss`、`yyyy-MM-dd`、`yyyyMMdd`。
          schema:
            type: string
            example: "20250306123000"
      responses:
        "200":
          description: 文件列表获取成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ListFilesResponse"
              example:
                data:
                  - id: file-batch-xxx
                    bytes: 27
                    created_at: 1722480543
                    filename: test.txt
                    object: file
                    purpose: batch
                    status: processed
                    status_details: null
                  - id: file-batch-yyy
                    bytes: 431986
                    created_at: 1718089390
                    filename: test.pdf
                    object: file
                    purpose: batch
                    status: processed
                    status_details: null
                object: list
                has_more: false
      x-codeSamples:
        - lang: python
          label: Python
          source: |-
            import os
            from openai import OpenAI

            client = OpenAI(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
            )

            file_list = client.files.list(
              after="file-batch-xxx",
              limit=20
            )
            print(file_list.model_dump_json())
        - lang: javascript
          label: Node.js
          source: |-
            import OpenAI from "openai";

            const client = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
            });

            const fileList = await client.files.list({
              after: "file-batch-xxx",
              limit: 20,
            });
            console.log(fileList);
        - lang: curl
          label: cURL
          source: |-
            curl "https://dashscope.aliyuncs.com/compatible-mode/v1/files" \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY"
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    UploadFileRequest:
      type: object
      required:
        - file
        - purpose
      properties:
        file:
          type: string
          format: binary
          description: 待上传的文件。
        purpose:
          type: string
          enum:
            - file-extract
            - batch
          description: |-
            文件用途。

            - `file-extract`：文档解析，最大 150 MB，支持格式：TXT、DOCX、PDF、XLSX、EPUB、MOBI、MD、CSV、JSON、BMP、PNG、JPG/JPEG、GIF、扫描版 PDF。
            - `batch`：批量处理，最大 500 MB，JSONL 格式（[批量文件要求](/developer-guides/text-generation/batch#input-file-format)）。
    FileObject:
      type: object
      properties:
        id:
          type: string
          description: 文件的唯一标识符。
          example: file-fe-xxx
        bytes:
          type: integer
          description: 文件大小，单位为字节。
          example: 2055
        created_at:
          type: integer
          description: 文件创建时间的 Unix 时间戳（秒）。
          example: 1729065448
        filename:
          type: string
          description: 上传时的文件名。
          example: test.txt
        object:
          type: string
          enum:
            - file
          description: 固定值 `file`。
        purpose:
          type: string
          description: 文件用途，可选值：`batch`、`file-extract`、`batch_output`。
          example: file-extract
        status:
          type: string
          description: 文件当前状态。
          example: processed
        status_details:
          type: string
          nullable: true
          description: 状态的补充说明，无详细信息时为 `null`。
    ListFilesResponse:
      type: object
      properties:
        object:
          type: string
          enum:
            - list
          description: 固定值 `list`。
        data:
          type: array
          description: 文件对象列表。
          items:
            $ref: "#/components/schemas/FileObject"
        has_more:
          type: boolean
          description: 是否存在下一页数据。
    DeleteFileResponse:
      type: object
      properties:
        object:
          type: string
          enum:
            - file
          description: 固定值 `file`。
        deleted:
          type: boolean
          description: 文件是否已成功删除。
        id:
          type: string
          description: 已删除文件的 ID。
          example: file-batch-xxx
````
