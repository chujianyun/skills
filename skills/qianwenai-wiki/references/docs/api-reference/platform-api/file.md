> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文件管理

> 文件管理 API

通过 OpenAI 兼容的 Files API，上传文件用于文档解析或批量处理。

## 使用方式

通过 OpenAI SDK（Python/Node.js）或 HTTP 接口，上传、查询、列举和删除文件。

**前提条件**：

- API Key：[创建 API Key](/api-reference/preparation/api-key) 并[将 API Key 导出为环境变量](/api-reference/preparation/export-api-key-env)。

- 如需使用 OpenAI SDK，请安装 [OpenAI SDK](/api-reference/preparation/install-sdk)。

## 适用范围

File ID 可用于：

- [批量处理](/developer-guides/text-generation/batch)：批量文件上传。

## 接口列表

| 接口                                                     | 说明              |
| ------------------------------------------------------ | --------------- |
| [上传文件](/api-reference/platform-api/file/upload-file)   | 上传文件用于文档解析或批量处理 |
| [查询文件](/api-reference/platform-api/file/retrieve-file) | 通过 ID 查询文件详情    |
| [列举文件](/api-reference/platform-api/file/list-files)    | 列举账号下的所有文件      |
| [删除文件](/api-reference/platform-api/file/delete-file)   | 通过 ID 删除文件      |

## 快速开始

### 上传文件

最多可存储 10,000 个文件，总容量 100 GB，文件永久保存，不会过期。

### 用于文档解析

将 `purpose` 设为 `file-extract`。支持的格式：文本文件（TXT、DOCX、PDF、XLSX、EPUB、MOBI、MD、CSV、JSON）和图片（BMP、PNG、JPG/JPEG、GIF、扫描版 PDF）。**最大文件大小：150 MB**。

#### 请求示例

<Tabs>
  <Tab title="Python">
    ```python
    import os
    from pathlib import Path
    from openai import OpenAI

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # test.txt 是本地示例文件。
    file_object = client.files.create(file=Path("test.txt"), purpose="file-extract")

    print(file_object.model_dump_json())
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";
    import fs from "fs";

    const client = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    });

    const fileObject = await client.files.create({
      file: fs.createReadStream("test.txt"),
      purpose: "file-extract",
    });
    console.log(fileObject);
    ```
  </Tab>

  <Tab title="cURL">
    ```bash
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/files \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -F 'file=@"test.txt"' \
      -F 'purpose="file-extract"'
    ```
  </Tab>
</Tabs>

#### 响应示例

```json
{
  "id": "file-fe-xxx",
  "bytes": 2055,
  "created_at": 1729065448,
  "filename": "test.txt",
  "object": "file",
  "purpose": "file-extract",
  "status": "processed",
  "status_details": null
}
```

### 用于批量处理

将 `purpose` 设为 `batch`。上传符合[批量文件要求](/developer-guides/text-generation/batch#输入文件格式)的 JSONL 文件。**最大文件大小：500 MB**。

<Tip>
  批量调用请参考 [Batch API](/developer-guides/text-generation/batch)。
</Tip>

#### 请求示例

<Tabs>
  <Tab title="Python">
    ```python
    import os
    from pathlib import Path
    from openai import OpenAI

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    # test.jsonl 是本地示例文件。
    file_object = client.files.create(file=Path("test.jsonl"), purpose="batch")

    print(file_object.model_dump_json())
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";
    import fs from "fs";

    const client = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
    });

    const fileObject = await client.files.create({
      file: fs.createReadStream("test.jsonl"),
      purpose: "batch",
    });
    console.log(fileObject);
    ```
  </Tab>

  <Tab title="cURL">
    ```bash
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/files \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -F 'file=@"test.jsonl"' \
      -F 'purpose="batch"'
    ```
  </Tab>
</Tabs>

#### 响应示例

```json
{
  "id": "file-batch-xxx",
  "bytes": 231,
  "created_at": 1729065815,
  "filename": "test.jsonl",
  "object": "file",
  "purpose": "batch",
  "status": "processed",
  "status_details": null
}
```

## 计费说明

文件操作（上传、存储、查询、删除）免费。仅对模型推理的 Token 数（输入 + 输出）计费。

## 限流

限流标准：上传（3 QPS），查询/列举/删除（合计 10 QPS）。

## 上线建议

- **定期清理**：删除不再使用的文件，保持文件数量在 10,000 个限制以内。

- **状态验证**：使用上传的文件前，请确认 `status="processed"`。

- **限流处理**：上传（3 QPS），查询/列举/删除（合计 10 QPS）。建议实现指数退避重试机制。

- **错误处理**：处理网络超时、API 错误（格式无效、超出大小限制）以及文件数量限制错误。参考[错误码](/api-reference/preparation/error-messages)。

## 常见问题

### 1. 上传后文件状态一直停留在"processing"怎么办？

处理通常在数秒内完成。如果状态迟迟未变为 `processed`：

- 检查文件格式是否受支持。
- 检查文件大小是否在限制范围内（file-extract：150 MB，batch：500 MB）。
- 使用 `retrieve` API 轮询状态。

### 2. File ID 能跨账号共用吗？

不能。File ID 仅限于创建它的千问AI平台账号使用。

### 3. 上传的文件会永久保存吗？

是的，文件会一直保存，直到您主动删除。

### 4. 文件上传失败的原因有哪些？

- API Key 无效或未设置（`$DASHSCOPE_API_KEY` 未配置）。
- 文件格式不受支持。
- 文件大小超出限制（file-extract：150 MB，batch：500 MB）。
- 存储空间已满（10,000 个文件或 100 GB 总容量）。
- 超出限流（上传 3 QPS）。

### 5. `file-extract` 和 `batch` 分别适用于什么场景？

- `file-extract`：文档解析与数据提取。
- `batch`：批量推理任务（需要 JSONL 格式）。
