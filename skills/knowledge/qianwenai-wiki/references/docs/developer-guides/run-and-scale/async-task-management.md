> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 异步任务管理

> 千问AI平台的两种异步模式：Task API 用于媒体生成，Batch API 用于大规模文本处理

千问AI平台提供两种异步处理机制，根据场景选择：

|            | Task API                               | Batch API                                           |
| ---------- | -------------------------------------- | --------------------------------------------------- |
| **适用场景**   | 图像生成、视频生成、文件转写                         | 大规模文本生成、向量化                                         |
| **工作方式**   | 提交请求 → 获取 task ID → 轮询结果               | 上传 JSONL 请求文件 → 轮询完成状态 → 下载结果                       |
| **端点**     | `dashscope.aliyuncs.com/api/v1/tasks/` | `dashscope.aliyuncs.com/compatible-mode/v1/batches` |
| **费用**     | 标准价格                                   | **5 折优惠**                                           |
| **完成时间**   | 数秒到数分钟                                 | 最长 24 小时（可配置至 336 小时）                               |
| **结果保留时间** | 24 小时                                  | 30 天                                                |
| **单次请求上限** | 1 个任务（支持多输出，如 `n=4`）                   | 单文件最多 50,000 条请求，500 MB                             |

## Task API

图像生成、视频生成和文件转写使用 Task API：提交一个请求，获取 task ID，然后轮询结果。

### 工作流程

每个任务都遵循相同的两步模式：

1. **创建任务** — 发送 POST 请求，获取 `task_id`
2. **查询结果** — 轮询 `GET /api/v1/tasks/{task_id}`，直到任务进入终态

```
POST（创建）──→ task_id
                     │
       ┌─────────────┘
       ▼
  ┌─────────┐    ┌─────────┐    ┌───────────┐
  │ PENDING │───→│ RUNNING │───→│ SUCCEEDED │
  └─────────┘    └─────────┘    └───────────┘
       │              │
       ▼              ▼
  ┌──────────┐   ┌────────┐
  │ CANCELED │   │ FAILED │
  └──────────┘   └────────┘
```

#### 任务状态

| 状态          | 说明                        |
| ----------- | ------------------------- |
| `PENDING`   | 已排队，等待处理                  |
| `RUNNING`   | 正在处理                      |
| `SUCCEEDED` | 处理成功                      |
| `FAILED`    | 处理失败                      |
| `CANCELED`  | 已手动取消（仅可从 `PENDING` 状态取消） |
| `UNKNOWN`   | task ID 已过期或无法查询          |

### 创建任务

部分 API（如图像生成）同时支持同步和异步模式。添加 `X-DashScope-Async` 请求头可强制使用异步模式：

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-Async: enable" \
  -d '{
    "model": "wan2.6-t2i",
    "input": {
      "messages": [
        {
          "role": "user",
          "content": [
            {"text": "A cat sitting on a windowsill at sunset"}
          ]
        }
      ]
    }
  }'
```

响应中会返回 `task_id`：

```json
{
  "request_id": "e5d5af82-9a08-xxx",
  "output": {
    "task_id": "86ecf553-d340-xxx",
    "task_status": "PENDING"
  }
}
```

<Note>
  视频生成 API 始终以异步方式运行，无需添加 `X-DashScope-Async` 请求头。
</Note>

### 查询结果

使用返回的 `task_id` 轮询任务端点：

<Tabs>
  <Tab title="curl">
    ```bash
    curl -X GET "https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-xxx" \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>

  <Tab title="Python">
    ```python
    import requests
    import os

    task_id = "86ecf553-d340-xxx"
    url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
    headers = {"Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}"}

    response = requests.get(url, headers=headers)
    result = response.json()
    print(result["output"]["task_status"])
    ```
  </Tab>
</Tabs>

任务完成后，结果会包含在 `output` 字段中：

```json
{
  "request_id": "e5d5af82-9a08-xxx",
  "output": {
    "task_id": "86ecf553-d340-xxx",
    "task_status": "SUCCEEDED",
    "submit_time": "2025-01-15 10:30:00.000",
    "scheduled_time": "2025-01-15 10:30:01.000",
    "end_time": "2025-01-15 10:30:12.000",
    "finished": true,
    "choices": [
      {
        "finish_reason": "stop",
        "message": {
          "role": "assistant",
          "content": [
            {
              "image": "https://dashscope-result-xxx.oss-xxx.aliyuncs.com/...",
              "type": "image"
            }
          ]
        }
      }
    ]
  },
  "usage": {
    "image_count": 1,
    "input_tokens": 0,
    "output_tokens": 0
  }
}
```

<Note>
  旧版模型（Wan 2.5 及更早版本）返回的响应结构不同，使用 `results` 和 `task_metrics` 字段而非 `choices`。详见[文生图 API 参考](/api-reference/image-generation/wan-text-to-image-v2/query-result)。
</Note>

任务失败时，响应中会包含错误码和错误信息：

```json
{
  "output": {
    "task_id": "86ecf553-d340-xxx",
    "task_status": "FAILED",
    "code": "DataInspectionFailed",
    "message": "Input or output data may contain inappropriate content."
  }
}
```

### 轮询策略

固定间隔轮询会浪费 API 调用次数，还可能触发限流。建议使用指数退避策略。

从较短的轮询间隔开始，逐步增大。不同模态的典型完成时间不同：

| 模态        | 初始间隔 | 递增倍数  | 超时时间    |
| --------- | ---- | ----- | ------- |
| 图像生成      | 3 秒  | 1.5 倍 | 2 分钟    |
| 视频生成      | 15 秒 | 1.5 倍 | 5 分钟    |
| 文件转写（ASR） | 5 秒  | 1.5 倍 | 取决于音频时长 |

<Tabs>
  <Tab title="Python">
    ```python
    import time
    import requests
    import os

    def poll_task(task_id, initial_interval=3, max_interval=15, timeout=120):
      """使用指数退避策略轮询任务。"""
      url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
      headers = {"Authorization": f"Bearer {os.getenv('DASHSCOPE_API_KEY')}"}

      interval = initial_interval
      elapsed = 0

      while elapsed < timeout:
        response = requests.get(url, headers=headers)
        result = response.json()
        status = result["output"]["task_status"]

        if status == "SUCCEEDED":
          return result
        elif status == "FAILED":
          raise Exception(
            f"Task failed: {result['output'].get('code', 'Unknown')} - "
            f"{result['output'].get('message', '')}"
          )

        time.sleep(interval)
        elapsed += interval
        interval = min(interval * 1.5, max_interval)

      raise TimeoutError(f"Task {task_id} did not complete within {timeout}s")

    # 图像生成：初始间隔 3 秒，最大间隔 15 秒，超时 2 分钟
    result = poll_task("86ecf553-d340-xxx", initial_interval=3, max_interval=15, timeout=120)

    # 视频生成：初始间隔 15 秒，最大间隔 60 秒，超时 5 分钟
    result = poll_task("86ecf553-d340-xxx", initial_interval=15, max_interval=60, timeout=300)
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    async function pollTask(taskId, { initialInterval = 3000, maxInterval = 15000, timeout = 120000 } = {}) {
      const url = `https://dashscope.aliyuncs.com/api/v1/tasks/${taskId}`;
      const headers = { Authorization: `Bearer ${process.env.DASHSCOPE_API_KEY}` };

      let interval = initialInterval;
      const deadline = Date.now() + timeout;

      while (Date.now() < deadline) {
        const res = await fetch(url, { headers });
        const result = await res.json();
        const { task_status, code, message } = result.output;

        if (task_status === "SUCCEEDED") return result;
        if (task_status === "FAILED") throw new Error(`Task failed: ${code} - ${message}`);

        await new Promise(resolve => setTimeout(resolve, interval));
        interval = Math.min(interval * 1.5, maxInterval);
      }

      throw new Error(`Task ${taskId} did not complete within ${timeout}ms`);
    }
    ```
  </Tab>
</Tabs>

### SDK 封装

DashScope Python SDK 已封装轮询逻辑。使用 `call()` 可同步等待结果，使用 `async_call()` + `wait()` 可手动控制流程。

```python
import dashscope
from dashscope.aigc.image_generation import ImageGeneration

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

message = {"role": "user", "content": [{"text": "A cat sitting on a windowsill at sunset"}]}

# 方式一：同步调用 — SDK 内部自动轮询
result = ImageGeneration.call(
  model="wan2.7-image-pro",
  messages=[message],
  n=1
)
print(result.output.choices[0].message.content[0]["image"])

# 方式二：异步调用 — 手动控制等待时机
task = ImageGeneration.async_call(
  model="wan2.7-image-pro",
  messages=[message],
  n=1
)
# 在此处可执行其他操作...
result = ImageGeneration.wait(task)
print(result.output.choices[0].message.content[0]["image"])
```

其他模态的用法相同：

```python
from dashscope import VideoSynthesis

task = VideoSynthesis.async_call(model="wan2.6-t2v", prompt="...")
result = VideoSynthesis.wait(task)
```

### 批量管理任务

#### 查询任务列表

按时间范围、状态或模型筛选任务：

```bash
curl -X GET "https://dashscope.aliyuncs.com/api/v1/tasks/?start_time=20250115100000&end_time=20250115120000&status=FAILED&model_name=wan2.6-t2i&page_no=1&page_size=20" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

支持的筛选参数：

| 参数           | 说明                                                |
| ------------ | ------------------------------------------------- |
| `start_time` | 时间范围起点，格式：`YYYYMMDDhhmmss`                        |
| `end_time`   | 时间范围终点，格式：`YYYYMMDDhhmmss`                        |
| `status`     | 按任务状态筛选（`PENDING`、`RUNNING`、`SUCCEEDED`、`FAILED`） |
| `model_name` | 按模型名称筛选                                           |
| `page_no`    | 页码（从 1 开始）                                        |
| `page_size`  | 每页结果数                                             |

<Note>
  时间范围不能超过 24 小时。如果不指定 `start_time` 和 `end_time`，默认返回最近 24 小时内的任务。
</Note>

#### 取消任务

取消处于 `PENDING` 状态的任务：

```bash
curl -X POST "https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-xxx/cancel" \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<Warning>
  只能取消 `PENDING` 状态的任务。任务进入 `RUNNING` 状态后将继续执行直至完成。
</Warning>

#### 限流

任务管理端点（查询、列表、取消）共享 **20 QPS** 的账户级别限流。如果需要管理大量并发任务，建议批量检查状态，避免高频轮询每个任务。

### Task API 最佳实践

**及时下载结果** — 任务数据和结果 URL（图像、视频）仅保留 **24 小时**。过期后，任务元数据和生成的文件会被自动删除。任务完成后应立即将结果下载到持久化存储。

**处理多输出任务** — 请求多个输出（如 `n=4` 张图片）时，只要**至少有一个**输出成功生成，任务即标记为 `SUCCEEDED`。遍历 `choices` 数组并检查 `finish_reason` 以处理部分成功的情况：

```python
result = poll_task(task_id)
choices = result["output"]["choices"]
print(f"共生成 {len(choices)} 个输出")

for choice in choices:
  if choice["finish_reason"] == "stop":
    for item in choice["message"]["content"]:
      if "image" in item:
        download(item["image"])
  else:
    print(f"输出被跳过：{choice['finish_reason']}")
```

**避免重复提交任务** — 每次 POST 请求都会创建新任务，即使参数完全相同。如果应用需要重试失败的请求，请记录 task ID 以避免重复提交和不必要的费用。

## Batch API

Batch API 以**标准价格 5 折**处理大规模文本生成或向量化请求。上传 JSONL 格式的请求文件，等待处理完成后下载结果。

| 特性         | 详情                              |
| ---------- | ------------------------------- |
| **支持的模型**  | Qwen 文本生成模型、文本向量化模型             |
| **输入格式**   | JSONL 文件，最多 50,000 条请求 / 500 MB |
| **完成窗口**   | 24 小时（可配置至 336 小时）              |
| **结果保留时间** | 30 天                            |
| **取消**     | 任何阶段均可取消（进行中的请求会先完成）            |

Batch API 使用 OpenAI 兼容端点和 SDK。完整指南（含示例、输入格式、任务状态和管理操作）请参阅 [Batch API](/developer-guides/text-generation/batch)。

## 常见错误

以下错误同时适用于 Task API 和 Batch API：

| 错误                     | 原因           | 处理方式                                                           |
| ---------------------- | ------------ | -------------------------------------------------------------- |
| `DataInspectionFailed` | 输入或输出被内容审核拦截 | 修改 prompt 后重试。参阅[内容安全](/developer-guides/run-and-scale/safety) |
| `Throttling.RateQuota` | 超出限流         | 降低请求频率；增大轮询间隔                                                  |
| 任务/批处理卡住               | 处理时间超出预期     | Task API：继续轮询直到超时。Batch API：增大 `completion_window`             |

## 下一步

- [管理异步任务](/api-reference/more/manage-asynchronous-tasks) — Task API 参考（查询、列表、取消）
- [Batch API](/developer-guides/text-generation/batch) — Batch API 完整指南
- [文生图](/developer-guides/image-generation/text-to-image) — 含异步任务示例的图像生成指南
- [文生视频](/developer-guides/video-generation/text-to-video) — 含异步任务示例的视频生成指南
- [限流](/developer-guides/administration/rate-limits) — 账户级别限流详情
