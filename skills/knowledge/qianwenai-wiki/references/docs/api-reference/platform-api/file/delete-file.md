> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 删除文件

## OpenAPI

````yaml delete /files/{file_id}
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
  /files/{file_id}:
    delete:
      operationId: deleteFile
      summary: 删除文件
      description: 通过文件 ID 删除指定文件。
      parameters:
        - name: file_id
          in: path
          required: true
          description: 待删除文件的 ID。
          schema:
            type: string
            example: file-batch-xxx
      responses:
        "200":
          description: 文件删除成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DeleteFileResponse"
              example:
                object: file
                deleted: true
                id: file-batch-xxx
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

            result = client.files.delete(
              "file-batch-xxx"
            )
            print(result.model_dump_json())
        - lang: javascript
          label: Node.js
          source: |-
            import OpenAI from "openai";

            const client = new OpenAI({
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
            });

            const result = await client.files.delete(
              "file-batch-xxx"
            );
            console.log(result);
        - lang: curl
          label: cURL
          source: |-
            curl -X DELETE "https://dashscope.aliyuncs.com/compatible-mode/v1/files/file-batch-xxx" \
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
