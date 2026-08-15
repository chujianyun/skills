> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 异步任务管理 API 参考

> 通过 HTTP API 查询单个异步任务结果、批量查询异步任务状态、以及取消异步任务的完整参考文档。

本文档介绍异步任务管理 HTTP API 的完整参数与使用方法。在使用前，请确保已[获取 API Key](/api-reference/preparation/api-key)。所有接口的基础路径为：

```
https://dashscope.aliyuncs.com/api/v1/tasks
```

<Note>
  Windows CMD 请将 `$DASHSCOPE_API_KEY` 替换为 `%DASHSCOPE_API_KEY%`，PowerShell 请替换为 `$env:DASHSCOPE_API_KEY`。
</Note>

## 查询异步任务结果

查询指定异步任务的执行结果。接口 QPS 限制为 20 次/账号，任务完成后结果保留 24 小时。

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 输入参数

| 字段            | 类型     | 传参方式     | 必选 | 描述                              |
| ------------- | ------ | -------- | -- | ------------------------------- |
| Authorization | String | Header   | 是  | API Key，格式为 `Bearer sk-ws-xxx`。 |
| task\_id      | String | Url Path | 是  | 要查询的异步任务 ID。                    |

### 返回样例

```json
{
  "request_id": "45ac7f13-xxxx-xxxx-xxxx-e03c35068d83",
  "output": {
    "task_id": "73205176-xxxx-xxxx-xxxx-16bd5d902219",
    "task_status": "SUCCEEDED",
    "submit_time": "2023-12-20 21:36:31.896",
    "scheduled_time": "2023-12-20 21:36:39.009",
    "end_time": "2023-12-20 21:36:45.913",
    "results": [
      {"url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx1.png"},
      {"url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx2.png"},
      {"url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx3.png"},
      {"code": "DataInspectionFailed", "message": "Output data may contain inappropriate content."}
    ],
    "task_metrics": {"TOTAL": 4, "SUCCEEDED": 3, "FAILED": 1}
  },
  "usage": {"image_count": 3}
}
```

### 返回参数

| 参数名称                   | 类型     | 参数说明                                                     |
| ---------------------- | ------ | -------------------------------------------------------- |
| request\_id            | String | 本次请求的 ID。                                                |
| output                 | Object | 任务详情。                                                    |
| output.task\_id        | String | 异步任务 ID。                                                 |
| output.task\_status    | String | 任务状态，详见[任务状态](#任务状态)。                                    |
| output.submit\_time    | String | 任务提交时间。                                                  |
| output.scheduled\_time | String | 任务开始调度时间。                                                |
| output.end\_time       | String | 任务结束时间。                                                  |
| output.code            | String | 任务失败时的错误码。                                               |
| output.message         | String | 任务失败时的错误信息。                                              |
| output.task\_metrics   | Object | 子任务统计信息，格式为 `{"TOTAL": N, "SUCCEEDED": N, "FAILED": N}`。 |
| usage                  | Object | 资源用量，具体字段因任务类型不同而有所差异。                                   |

<Note>
  对于包含多个子任务的批量任务，只要有一个子任务成功，整体任务状态即为 SUCCEEDED。请通过 `output.task_metrics` 中的 `FAILED` 字段确认是否存在失败的子任务。
</Note>

---

## 批量查询异步任务状态

查询当前账号下的异步任务列表及其状态。接口 QPS 限制为 20 次/账号，仅可查询本账号下的任务。

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/?start_time=xxx&end_time=xxx&status=xxx' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 输入参数

| 字段            | 类型      | 传参方式   | 必选 | 描述                                                                                                                      |
| ------------- | ------- | ------ | -- | ----------------------------------------------------------------------------------------------------------------------- |
| Authorization | String  | Header | 是  | API Key，格式为 `Bearer sk-ws-xxx`。                                                                                         |
| start\_time   | String  | Query  | 否  | 查询起始时间，格式为 `YYYYMMDDhhmmss`。若不填，默认为 `end_time` 前 24 小时；若两者均不填，默认查询最近 24 小时的任务。`start_time` 与 `end_time` 的时间差不能超过 24 小时。 |
| end\_time     | String  | Query  | 否  | 查询截止时间，格式为 `YYYYMMDDhhmmss`。                                                                                            |
| model\_name   | String  | Query  | 否  | 按模型名称过滤。                                                                                                                |
| status        | String  | Query  | 否  | 按任务状态过滤，详见[任务状态](#任务状态)。                                                                                                |
| page\_no      | Integer | Query  | 否  | 页码，默认值为 1。                                                                                                              |
| page\_size    | Integer | Query  | 否  | 每页数据量，默认值为 10。                                                                                                          |

### 返回样例

```json
{
  "total": 2,
  "data": [
    {
      "api_key_id": "15xxxx",
      "caller_parent_id": "xxxxxxxxx",
      "caller_uid": "xxxxxxxxx",
      "gmt_create": 1745568428109,
      "model_name": "wanx2.1-kf2v-plus",
      "region": "cn-beijing",
      "request_id": "1abfc3c8-dd25-98da-ad0b-xxxxxx",
      "start_time": 1745568428138,
      "status": "RUNNING",
      "task_id": "50e2ccea-abc4-43d7-a0dc-xxxxxx",
      "user_api_unique_key": "apikey:v1:aigc:image2video:video-synthesis:wanx2.1-kf2v-plus"
    },
    {
      "api_key_id": "15xxxx",
      "caller_parent_id": "xxxxxxxxx",
      "caller_uid": "xxxxxxxxx",
      "end_time": 1745568302481,
      "gmt_create": 1745568293253,
      "model_name": "wanx2.1-t2i-turbo",
      "region": "cn-beijing",
      "request_id": "f6bf34d9-bf87-9e8b-9ed4-xxxxxx",
      "start_time": 1745568293273,
      "status": "SUCCEEDED",
      "task_id": "3c777dbc-8cc6-4d80-aa90-xxxxxx",
      "user_api_unique_key": "apikey:v1:aigc:text2image:image-synthesis:wanx2.1-t2i-turbo"
    }
  ],
  "total_page": 1,
  "page_no": 1,
  "request_id": "f6756b7e-d0bb-9b74-813a-xxxxxx",
  "page_size": 10
}
```

### 返回参数

| 参数名称                           | 类型      | 参数说明                     |
| ------------------------------ | ------- | ------------------------ |
| request\_id                    | String  | 本次请求的 ID。                |
| total                          | Integer | 满足条件的任务总数量。              |
| total\_page                    | Integer | 总页数。                     |
| page\_no                       | Integer | 当前页码。                    |
| page\_size                     | Integer | 每页数据量。                   |
| data                           | Array   | 任务列表。                    |
| data\[].task\_id               | String  | 异步任务 ID。                 |
| data\[].status                 | String  | 任务状态，详见[任务状态](#任务状态)。    |
| data\[].model\_name            | String  | 任务使用的模型名称。               |
| data\[].gmt\_create            | Long    | 任务创建时间（毫秒时间戳）。           |
| data\[].start\_time            | Long    | 任务开始时间（毫秒时间戳）。           |
| data\[].end\_time              | Long    | 任务结束时间（毫秒时间戳）。           |
| data\[].request\_id            | String  | 提交任务时的请求 ID。             |
| data\[].region                 | String  | 任务所在地域，例如 `cn-hangzhou`。 |
| data\[].api\_key\_id           | String  | 提交任务使用的 API Key ID。      |
| data\[].caller\_parent\_id     | String  | 千问AI平台账号 ID。             |
| data\[].caller\_uid            | String  | 千问AI平台账号 ID。             |
| data\[].user\_api\_unique\_key | String  | 提交任务的 API 唯一标识。          |
| code                           | String  | 请求失败时的错误码。               |
| message                        | String  | 请求失败时的错误信息。              |

---

## 取消异步任务

取消指定的异步任务。接口 QPS 限制为 20 次/账号。

<Note>
  只有处于 PENDING（排队等待）状态的任务可以被取消，已开始执行的任务无法取消。同一主账号下，任意 API Key 提交的任务均可取消。
</Note>

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}/cancel' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 输入参数

| 字段            | 类型     | 传参方式     | 必选 | 描述                              |
| ------------- | ------ | -------- | -- | ------------------------------- |
| Authorization | String | Header   | 是  | API Key，格式为 `Bearer sk-ws-xxx`。 |
| task\_id      | String | Url Path | 是  | 要取消的异步任务 ID。                    |

### 返回样例

```json
{
  "request_id": "45ac7f13-xxxx-xxxx-xxxx-e03c35068d83"
}
```

### 返回参数

| 参数名称        | 类型     | 参数说明        |
| ----------- | ------ | ----------- |
| request\_id | String | 本次请求的 ID。   |
| code        | String | 取消失败时的错误码。  |
| message     | String | 取消失败时的错误信息。 |

---

## 任务状态

| 任务状态      | 含义              |
| --------- | --------------- |
| PENDING   | 任务排队等待中，尚未开始执行。 |
| RUNNING   | 任务正在执行中。        |
| SUCCEEDED | 任务执行成功。         |
| FAILED    | 任务执行失败。         |
| CANCELED  | 任务已取消。          |
| UNKNOWN   | 任务状态未知。         |

---

## 错误码

| HTTP 状态码 | 错误码                  | 错误信息举例                                                                      | 含义             | 处理方式                     |
| -------- | -------------------- | --------------------------------------------------------------------------- | -------------- | ------------------------ |
| 400      | UnsupportedOperation | Failed to cancel the task, please confirm if the task is in PENDING status. | 任务当前状态不支持取消操作。 | 确认任务处于 PENDING 状态后再进行取消。 |
