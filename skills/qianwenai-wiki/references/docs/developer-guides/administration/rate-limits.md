> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 限流

> 了解和管理 API 限流

## 速率限制的工作原理

速率限制控制您的账户每分钟可以对每个模型消耗的 API 请求数和 Token 数。限制分为两种：

- **RPM**（Requests Per Minute）：每分钟最大 API 调用次数。
- **TPM**（Tokens Per Minute）：每分钟最大处理 Token 数。

速率限制在**账户级别**生效，同一账户下的所有业务空间和 API Key 共享配额。

<Note>
  速率限制同时按秒生效：RPS = RPM / 60，TPS = TPM / 60。即使每分钟的总用量未超限，单秒内的突发请求也可能触发限流。
</Note>

## 查看速率限制

查看速率限制的入口因业务空间而异：

- **默认业务空间**：默认业务空间使用账户级别限制。前往[模型市场](https://www.qianwenai.com/models)，选择一个模型，在其详情页的**速率限制与上下文**区域查看该模型的 RPM 和 TPM 限制。
- **子业务空间**：前往**设置** > [业务空间](https://platform.qianwenai.com/home/settings/workspaces)，点击子业务空间的**编辑**，再点击**编辑模型**。每个模型会显示其**调用/分钟**（RPM）和 **Token/分钟**（TPM）值。

## 按业务空间设置速率限制

您可以在[业务空间](/developer-guides/administration/workspace)中为单个模型设置自定义的 RPM 和 TPM 限制。

<Steps>
  <Step title="进入业务空间页面">
    前往**设置** > [业务空间](https://platform.qianwenai.com/home/settings/workspaces)，点击子业务空间的**编辑**按钮。
  </Step>

  <Step title="添加模型并设置限制">
    在**模型权限**下，点击**编辑模型**添加模型。为每个模型设置**调用/分钟**（RPM）和 **Token/分钟**（TPM），然后点击**应用**。
  </Step>

  <Step title="提交">
    点击**提交**以应用新的速率限制。
  </Step>
</Steps>

为业务空间设置的 RPM 和 TPM 不能超过该模型的账户级别限制。默认业务空间使用账户级别限制，无法修改。

## 临时提升频率限制

如果某个模型需要更高的吞吐量，可以通过账户设置申请临时提升。

<Steps>
  <Step title="进入限流提额页面">
    前往[限流提额](https://platform.qianwenai.com/home/settings/rate-limit)页面。
  </Step>

  <Step title="申请提升">
    点击**临时提升频率限制**，选择模型，输入目标 **Token 频率上限**（**Token / 60 秒**）。对话框会显示**当前额度**和**上限**。
  </Step>

  <Step title="提交">
    点击**提交**以应用临时提升。
  </Step>
</Steps>

<Warning>
  请根据实际需求申请配额。长期未使用的配额可能会被缩减至默认限制。
</Warning>

### 支持限流提额的模型

以下模型支持通过控制台申请临时提升频率限制：

- qwen3.6-plus
- qwen3.6-flash
- qwen3.5-flash
- qwen3.5-plus
- qwen3-vl-flash
- qwen-plus
- qwen-plus-latest
- qwen3-max
- text-embedding-v4
- qwen3-vl-plus
- qwen-flash

<Tip>
  支持限流提额的模型可能会更新，具体以[控制台](https://platform.qianwenai.com/home/settings/rate-limit)展示为准。
</Tip>

**限流提额**页面的**申请记录**还展示所有临时提升申请的历史记录，包括每次申请的**提交时间**、**模型代码**和**账号 TPM 上限**。

## 速率限制错误

触发速率限制时，API 返回 HTTP 状态码 `429`，错误信息会指出触发了哪种限制：

| 错误信息                                                                       | 原因                           |
| -------------------------------------------------------------------------- | ---------------------------- |
| `Requests rate limit exceeded` 或 `You exceeded your current requests list` | 达到 RPM 限制                    |
| `Allocated quota exceeded` 或 `You exceeded your current quota`             | 达到 TPM 限制                    |
| `Request rate increased too quickly`                                       | 请求量突增触发了稳定性保护，即使 RPM/TPM 未超限 |

**限制在一分钟内重置。** 其他错误请参阅[错误信息](/api-reference/preparation/error-messages)。

## 最佳实践

### 平滑请求速率

将请求均匀分散在时间维度上，避免突发集中发送。使用恒定速率调度、指数退避或请求队列来避免触发每秒限制。

### 使用备用模型

请求被限流时，可回退到备用模型以保持服务可用性：

```python
import os
import asyncio
from openai import AsyncOpenAI, APIStatusError

API_KEY = os.getenv("DASHSCOPE_API_KEY")
MODEL = "qwen-plus-2025-07-28"
BACKUP_MODEL = "qwen-plus-2025-07-14"
QUESTION = "Who are you?"
NUM_REQUESTS = 10

client = AsyncOpenAI(
  api_key=API_KEY,
  base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

async def send_request(model):
  try:
    await client.chat.completions.create(
      model=model,
      messages=[{"role": "user", "content": QUESTION}]
    )
    return True
  except APIStatusError as e:
    if e.status_code == 429:
      print(f"[触发速率限制] 模型 {model}")
      return False
    raise
  except Exception as e:
    print(f"[请求失败] 模型 {model}，错误：{e}")
    return False

async def task(i):
  if await send_request(MODEL):
    return True
  return await send_request(BACKUP_MODEL)

async def main():
  results = await asyncio.gather(*(task(i) for i in range(NUM_REQUESTS)))
  print(f"成功：{sum(results)}，失败：{len(results) - sum(results)}")

if __name__ == "__main__":
  asyncio.run(main())
```

### 拆分大任务

长对话或大文档会快速消耗大量 Token。将大批量任务拆分为小批次，分时提交，以控制在 TPM 限制内。

### 选择高配额模型

稳定版或最新版模型通常比旧版快照有更高的速率限制。建议尽量使用模型的最新版本。

### 使用批量推理

如果不需要实时结果，可以使用 [Batch API](/developer-guides/text-generation/batch)。批量任务不受实时速率限制，但可能存在排队和处理延迟。
