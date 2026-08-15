> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 批量调用

> 异步批量处理请求，费用低至实时调用的 50%

批量异步处理请求，费用仅为**实时调用价格的 50%**，结果在 24 小时内返回。

## 工作原理

1. **提交任务**：上传包含多个请求的 JSONL 文件，创建批量推理任务。
2. **异步处理**：系统在后台队列中处理任务。可通过控制台或API查询任务进度和状态。
3. **下载结果**：任务完成后，系统生成结果文件（记录成功响应）和错误文件（记录失败详情，如有）。

## 支持的模型

**文本生成模型**

- 千问 Max：`qwen3.8-max`、`qwen3.7-max`、`qwen3-max`
- 千问 Plus：`qwen3.7-plus`、`qwen3.6-plus`、`qwen3.5-plus`、`qwen-plus`、`qwen-plus-latest`
- 千问 Flash：`qwen3.7-flash`、`qwen3.6-flash`、`qwen3.5-flash`、`qwen-flash`
- 千问 Long：`qwen-long`、`qwen-long-latest`
- 第三方模型：`deepseek-r1`、`deepseek-v3.2`、`deepseek-v3`

**多模态模型**

- [图像与视频理解](/developer-guides/multimodal/vision)：`qwen3.8-max`、`qwen3.7-plus`、`qwen3.7-flash`、`qwen3.6-plus`、`qwen3.6-flash`、`qwen3.5-plus`、`qwen3.5-flash`、`qwen3-vl-plus`、`qwen3-vl-flash`
- 文字提取：`qwen-vl-ocr`、`qwen-vl-ocr-latest`
- 全模态：`qwen3.5-omni-plus`

**文本向量模型**

`text-embedding-v1`、`text-embedding-v2`、`text-embedding-v3`、`text-embedding-v4`

## 输入文件格式

输入文件为 JSONL 格式，每行一个请求：

```jsonl
{"custom_id":"req-1","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-plus","messages":[{"role":"user","content":"用两句话概括量子计算。"}]}}
{"custom_id":"req-2","method":"POST","url":"/v1/chat/completions","body":{"model":"qwen-plus","messages":[{"role":"user","content":"2+2 等于几？"}]}}
```

所有请求的 `url` 必须设为 `/v1/chat/completions`。每个文件最多 **50,000** 条请求，总大小不超过 **500 MB**，单行不超过 **1 MB**。所有请求必须使用同一个模型，每个 `custom_id` 必须唯一且不超过 256 个字符。

## 使用千问AI平台控制台

打开千问AI平台控制台的[批量 API](https://platform.qianwenai.com/home/model-production/batch-api) 页面。

### 创建批量推理任务

1. 点击**创建批量推理任务**。
2. 填写**任务名称**和**描述**，设置**最大等待时间**（1-14 天），上传 JSONL 输入文件。
3. 点击**创建批量推理任务**提交。

<Tip>
  点击右侧的**示例文件**可下载模板 JSONL 文件。
</Tip>

### 监控和管理任务

在任务列表中，查看每个任务的**进度**（已处理/总请求数）和**状态**。通过状态筛选定位任务。

点击**取消**可停止处于校验中或执行中状态的任务。点击**详情**查看任务配置、统计数据和文件。

### 下载结果

任务状态变为 `completed` 后，打开任务详情页面，在**输入输出文件**部分下载：

- **输出文件**：成功请求及其响应。
- **错误文件**（如有）：失败请求及错误详情。

两个文件都包含 `custom_id`，可与原始输入进行匹配。

### 查看用量

在[按量付费](https://platform.qianwenai.com/home/billing/pay-as-you-go)页面，按模型查看花费。批量调用的用量会以明细形式显示在**费用趋势**表格中。数据可能有 1-2 小时的延迟。

## 执行批量任务

### 上传文件

<CodeGroup>
  ```python Python
  import os
  from pathlib import Path
  from openai import OpenAI
  client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"), base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

  file_object = client.files.create(
    file=Path("input.jsonl"),
    purpose="batch"
  )
  print(file_object.id)  # <-- 在下一步中使用此 ID
  ```

  ```javascript Node.js
  import OpenAI from "openai";
  import fs from "fs";
  const client = new OpenAI({ apiKey: process.env.DASHSCOPE_API_KEY, baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1" });

  const fileObject = await client.files.create({
    file: fs.createReadStream("input.jsonl"),
    purpose: "batch"
  });
  console.log(fileObject.id);  // <-- 在下一步中使用此 ID
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/files \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --form 'file=@"input.jsonl"' \
    --form 'purpose="batch"'
  ```
</CodeGroup>

响应示例（关键字段）：

```json
{"id": "file-batch-xxx", "status": "uploaded", "purpose": "batch"}
```

<Tip>
  **复用已有文件 ID：** 上传文件后返回的 ID（如 `file-batch-xxx`）可以复用。如果输入内容不变，无需重新上传，直接使用已有 ID 创建任务：

  ```python
  batch = client.batches.create(
    input_file_id="file-batch-xxx",  # 直接使用已有文件 ID，无需重新上传
    endpoint="/v1/chat/completions",
    completion_window="24h"
  )
  ```

  可通过 `client.files.list(purpose="batch")` 接口查询已上传的 Batch 文件 ID。
</Tip>

### 创建批量任务

<CodeGroup>
  ```python Python {2,3}
  batch = client.batches.create(
    input_file_id="file-batch-xxx",       # <-- 上一步获取的文件 ID
    endpoint="/v1/chat/completions",       # <-- 必须与输入文件中的 url 一致
    completion_window="24h",               # <-- 24h 到 336h（14 天）
    metadata={
      "ds_name": "My batch job",         # <-- 可选：任务名称（最多 100 字符）
      "ds_description": "Weekly report", # <-- 可选：任务描述（最多 200 字符）
    }
  )
  print(batch.id)
  ```

  ```javascript Node.js {2,3}
  const batch = await client.batches.create({
    input_file_id: "file-batch-xxx",       // <-- 上一步获取的文件 ID
    endpoint: "/v1/chat/completions",      // <-- 必须与输入文件中的 url 一致
    completion_window: "24h",
    metadata: {
      ds_name: "My batch job",
      ds_description: "Weekly report",
    }
  });
  console.log(batch.id);
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/batches \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "input_file_id": "file-batch-xxx",
      "endpoint": "/v1/chat/completions",
      "completion_window": "24h",
      "metadata": {"ds_name": "My batch job"}
    }'
  ```
</CodeGroup>

<Tip>
  **使用测试模型试运行**：将 model 设为 `batch-test-model`，endpoint 设为 `/v1/chat/ds-test`，即可在不产生推理费用的情况下验证文件格式。限制：文件不超过 1 MB、不超过 100 行、最多 2 个并发任务。
</Tip>

### 查询状态

<CodeGroup>
  ```python Python
  batch = client.batches.retrieve("batch_xxx")
  print(batch.status)  # <-- 参见下方状态流转说明
  ```

  ```javascript Node.js
  const batch = await client.batches.retrieve("batch_xxx");
  console.log(batch.status);
  ```

  ```bash curl
  curl https://dashscope.aliyuncs.com/compatible-mode/v1/batches/batch_xxx \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
  ```
</CodeGroup>

状态流转：`validating` → `in_progress` → `finalizing` → `completed`。终态包括：`completed`、`failed`、`expired`、`cancelled`。建议每 1-2 分钟轮询一次。

响应示例（关键字段）：

```json
{
  "id": "batch_xxx",
  "status": "completed",
  "output_file_id": "file-batch_output-xxx",  // <-- 下载此文件获取结果
  "error_file_id": "file-batch_error-xxx",     // <-- 失败的请求（如有）
  "request_counts": {"total": 100, "completed": 98, "failed": 2}
}
```

### 下载结果

<CodeGroup>
  ```python Python
  content = client.files.content("file-batch_output-xxx")  # <-- 上一步的 output_file_id
  content.write_to_file("result.jsonl")
  ```

  ```javascript Node.js
  const content = await client.files.content("file-batch_output-xxx");
  const text = await content.text();
  fs.writeFileSync("result.jsonl", text);
  ```

  ```bash curl
  curl https://dashscope.aliyuncs.com/compatible-mode/v1/files/file-batch_output-xxx/content \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" > result.jsonl
  ```
</CodeGroup>

输出 JSONL 文件中的每行通过 `custom_id` 与请求对应：

```json
{"id": "batch_req_xxx", "custom_id": "req-1", "response": {"status_code": 200, "body": {"choices": [{"message": {"content": "..."}}], "usage": {...}}}}
```

用同样的方式下载错误文件（`error_file_id`）查看失败请求的详情。错误码说明参见[错误码](/api-reference/preparation/error-messages)。

## 管理批量任务

### 列出批量任务

<CodeGroup>
  ```python Python
  batches = client.batches.list(limit=10)
  ```

  ```bash curl
  curl 'https://dashscope.aliyuncs.com/compatible-mode/v1/batches?limit=10&status=completed,failed' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
  ```
</CodeGroup>

查询参数（query string）：`ds_name`（模糊匹配）、`input_file_ids`（逗号分隔，最多 20 个）、`status`（逗号分隔）、`create_after` / `create_before`（格式：`yyyyMMddHHmmss`）、`after`（游标）、`limit`（每页条数）。

### 取消批量任务

<CodeGroup>
  ```python Python
  client.batches.cancel("batch_xxx")
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/batches/batch_xxx/cancel \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY"
  ```
</CodeGroup>

取消后状态变为 `cancelling`，待进行中的请求完成后变为 `cancelled`。取消前已完成的请求仍会计费。

## 工具脚本

<Accordion title="CSV 转 JSONL">
  ```python
  import csv, json

  def build_messages(content):
    return [{"role": "user", "content": content}]

  with open("input.csv") as fin, open("input.jsonl", "w") as fout:
    for row in csv.reader(fin):
      request = {
        "custom_id": row[0],
        "method": "POST",
        "url": "/v1/chat/completions",
        "body": {"model": "qwen-plus", "messages": build_messages(row[1])}
      }
      fout.write(json.dumps(request, ensure_ascii=False) + "\n")
  ```
</Accordion>

<Accordion title="JSONL 结果转 CSV">
  ```python
  import json, csv

  columns = ["custom_id", "status_code", "content", "usage"]

  def get(obj, path):
    for key in path:
      obj = obj[key] if obj and key in obj else None
    return obj

  with open("result.jsonl") as fin, open("result.csv", "w") as fout:
    writer = csv.writer(fout)
    writer.writerow(columns)
    for line in fin:
      r = json.loads(line)
      writer.writerow([
        r.get("custom_id"),
        get(r, ["response", "status_code"]),
        get(r, ["response", "body", "choices", 0, "message", "content"]),
        get(r, ["response", "body", "usage"]),
      ])
  ```
</Accordion>

## 注意事项

- **5 折优惠**：输入和输出 token 按实时价格的 50% 计费，仅对成功请求收费。详见[计费说明](/developer-guides/getting-started/pricing)。
- **上下文限制**：在 Batch 场景下，`qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus`、`qwen3.7-flash`、`qwen3.6-plus`、`qwen3.6-flash`、`qwen3.5-plus`、`qwen3.5-flash` 和 `qwen3.5-omni-plus` 单次请求的上下文 Token 数最大支持 256K。`qwen3.5-omni-plus` 不支持语音输出。
- **思考 token**：`qwen3.8-max`、`qwen3.7-max`、`qwen3.7-plus` 及 `qwen3.6`、`qwen3.5` 系列模型默认开启思考功能，会产生额外 token 并按输出价格计费。建议使用混合思考模型时，显式设置 `enable_thinking` 参数（`true` 开启 / `false` 关闭）。在 JSONL 请求体中，`enable_thinking` 为 `body` 的顶层参数，须与 `model` 同级传入，不能放在 `extra_body` 中。详见[思考](/developer-guides/text-generation/thinking)。
- **不可叠加**：批量折扣不与上下文缓存或其他折扣叠加。
- **文件存储**：每个账号最多 10,000 个文件 / 100 GB。请及时删除旧文件释放空间。
- **频率限制**：创建 1,000 次/分钟（最多 1,000 个并发），查询 1,000 次/分钟，列表 100 次/分钟，取消 1,000 次/分钟。
- **任务保留期**：仅最近 30 天的任务可通过列表接口查询。

## API 参考

- [创建批量任务](/api-reference/platform-api/batch/create-batch)
- [查询批量任务](/api-reference/platform-api/batch/retrieve-batch)
- [列出批量任务](/api-reference/platform-api/batch/list-batches)
- [取消批量任务](/api-reference/platform-api/batch/cancel-batch)
