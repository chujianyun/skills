> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 管理异步任务

> 查询和管理异步任务

图像生成、视频生成等模型以异步方式运行：先创建任务并获取任务 ID，再通过该 ID 查询结果。您可以通过以下 API 查询任务结果、批量查看任务状态以及取消排队中的任务。

## 前提条件

通过 HTTP 调用以下 API。

[获取 API Key](/api-reference/preparation/api-key)，然后[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。

## 查询异步任务结果

**接口说明**：通过 `task_id` 查询任务的状态和结果。

**流控限制**：单千问AI平台账号 20 QPS。

<Warning>
  - 您可以查询该 API Key 所属千问AI平台账号下的所有任务，包括该账号下其他 API Key 创建的任务，但无法查询其他账号的任务。

  - 已完成的任务数据默认保留 24 小时（具体时长请参考对应 API 文档），到期后自动删除。
</Warning>

### 请求端点

```bash
GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}
```

### 请求参数

| 传参方式   | 字段            | 类型     | 必选 | 描述                            | 示例值                                  |
| ------ | ------------- | ------ | -- | ----------------------------- | ------------------------------------ |
| Header | Authorization | String | 是  | API Key，格式为 Bearer sk-ws-xxx。 | Bearer sk-ws-xxx                     |
| Path   | task\_id      | String | 是  | 要查询的任务 ID。                    | a8532587-xxxx-xxxx-xxxx-0c46b17950d1 |

### 返回参数

| 字段                     | 类型     | 描述                                                                   | 示例值                                           |
| ---------------------- | ------ | -------------------------------------------------------------------- | --------------------------------------------- |
| request\_id            | String | 本次请求的唯一标识。                                                           | 7574ee8f-xxxx-xxxx-xxxx-11c33ab46e51          |
| output                 | Object | 成功时包含任务结果，失败时包含错误码和错误信息。对于包含多个子任务的请求，可能同时包含结果和错误信息。                  | -                                             |
| output.task\_id        | String | 所查询的任务 ID。                                                           | a8532587-xxxx-xxxx-xxxx-0c46b17950d1          |
| output.task\_status    | String | 任务状态。包含多个子任务时，只要有一个子任务成功，整个任务即标记为 SUCCEEDED，失败的子任务会在 output 中显示错误信息。 | PENDING, RUNNING, SUCCEEDED, FAILED, UNKNOWN  |
| output.submit\_time    | String | 任务提交时间。                                                              | 2023-12-20 21:36:31.896                       |
| output.scheduled\_time | String | 任务开始执行时间。                                                            | 2023-12-20 21:36:39.009                       |
| output.end\_time       | String | 任务结束时间。                                                              | 2023-12-20 21:36:45.913                       |
| output.code            | String | 错误码，仅在失败时返回。                                                         | -                                             |
| output.message         | String | 错误信息，仅在失败时返回。                                                        | -                                             |
| output.task\_metrics   | Object | 子任务状态统计。                                                             | `{ "TOTAL": 4, "SUCCEEDED": 3, "FAILED": 1 }` |
| usage                  | Object | 本次请求的计费信息，因任务类型而异。                                                   | `"usage": {"image_count": 1}`                 |

### 请求示例

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/73205176-xxxx-xxxx-xxxx-16bd5d902219' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

<Note>
  如果您未将 API Key 设置为环境变量，请将 `$DASHSCOPE_API_KEY` 替换为实际的 API Key。示例：`--header "Authorization: Bearer sk-ws-xxx"`。
</Note>

### 返回示例

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
      {
        "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx1.png"
      },
      {
        "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx2.png"
      },
      {
        "url": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx3.png"
      },
      {
        "code": "DataInspectionFailed",
        "message": "Output data may contain inappropriate content."
      }
    ],
    "task_metrics": {
      "TOTAL": 4,
      "SUCCEEDED": 3,
      "FAILED": 1
    }
  },
  "usage": {
    "image_count": 3
  }
}
```

## 批量查询异步任务状态

**接口说明**：按时间范围、模型或状态批量查询多个任务的状态。

**流控限制**：单千问AI平台账号 20 QPS。

<Warning>
  - 您可以查询该 API Key 所属千问AI平台账号下的所有任务，包括该账号下其他 API Key 创建的任务，但无法查询其他账号的任务。

  - 已完成的任务数据默认保留 24 小时（具体时长请参考对应 API 文档），到期后自动删除。
</Warning>

### 请求端点

```bash
GET https://dashscope.aliyuncs.com/api/v1/tasks/
```

### 请求参数

| 传参方式   | 字段            | 类型      | 必选 | 描述                                                                                          | 示例值                                         |
| ------ | ------------- | ------- | -- | ------------------------------------------------------------------------------------------- | ------------------------------------------- |
| Header | Authorization | String  | 是  | API Key，格式为 Bearer sk-ws-xxx。                                                               | Bearer sk-ws-xxx                            |
| Params | task\_id      | String  | 否  | 指定任务 ID。设置后仅返回该任务，不设置则查询多个任务。                                                               | a8532587-xxxx-xxxx-xxxx-0c46b17950d1        |
| Params | start\_time   | String  | 否  | 起始时间（格式：YYYYMMDDhhmmss）。默认为 end\_time 前 24 小时；若 end\_time 也未指定，则默认为最近 24 小时。时间范围不能超过 24 小时。 | 20230420193058 表示 2023 年 4 月 20 日 19:30:58。 |
| Params | end\_time     | String  | 否  | 结束时间（格式：YYYYMMDDhhmmss）。默认为 start\_time 后 24 小时。时间范围不能超过 24 小时。                             | 20230420193058 表示 2023 年 4 月 20 日 19:30:58。 |
| Params | model\_name   | String  | 否  | 模型名称。                                                                                       | wan2.6-t2v                                  |
| Params | status        | String  | 否  | 任务状态：PENDING, RUNNING, SUCCEEDED, FAILED, CANCELED, UNKNOWN                                 |                                             |
| Params | page\_no      | Integer | 否  | 页码，默认值：1。                                                                                   | -                                           |
| Params | page\_size    | Integer | 否  | 每页条数，默认值：10。                                                                                | -                                           |

### 返回参数

| 字段                             | 类型      | 描述                                                          | 示例值                                                                  |
| ------------------------------ | ------- | ----------------------------------------------------------- | -------------------------------------------------------------------- |
| request\_id                    | String  | 本次请求的唯一标识。                                                  | 7574ee8f-xxxx-xxxx-xxxx-11c33ab46e51                                 |
| data                           | Array   | 查询结果列表。                                                     | 见下方示例                                                                |
| data\[].api\_key\_id           | String  | API Key ID。                                                 | 见下方示例                                                                |
| data\[].caller\_parent\_id     | String  | 千问AI平台账号 ID。                                                | 见下方示例                                                                |
| data\[].caller\_uid            | String  | 千问AI平台账号 UID。                                               | 见下方示例                                                                |
| data\[].gmt\_create            | Long    | 任务创建时间，毫秒级时间戳。                                              | 见下方示例                                                                |
| data\[].start\_time            | Long    | 任务开始时间，毫秒级时间戳。                                              | 见下方示例                                                                |
| data\[].end\_time              | Long    | 任务结束时间，毫秒级时间戳。                                              | 见下方示例                                                                |
| data\[].region                 | String  | 地域。                                                         | 见下方示例                                                                |
| data\[].request\_id            | String  | 任务提交时的请求 ID。                                                | 见下方示例                                                                |
| data\[].status                 | String  | 任务状态：PENDING, RUNNING, SUCCEEDED, FAILED, CANCELED, UNKNOWN | 见下方示例                                                                |
| data\[].task\_id               | String  | 任务 ID。                                                      | 见下方示例                                                                |
| data\[].user\_api\_unique\_key | String  | 根据任务提交时的模型 API 参数生成的唯一索引。                                   | 见下方示例                                                                |
| data\[].model\_name            | String  | 模型名称。                                                       | 见下方示例                                                                |
| page\_no                       | Integer | 当前页码。                                                       | `"page_no": 1`                                                       |
| page\_size                     | Integer | 每页条数。                                                       | `"page_size": 10`                                                    |
| total\_page                    | Integer | 总页数。                                                        | `"total_page": 4`                                                    |
| total                          | Integer | 总条数。                                                        | `"total": 39`                                                        |
| code                           | String  | 错误码，仅在失败时返回。                                                | `"code": "Throttling.RateQuota"`                                     |
| message                        | String  | 错误信息，仅在失败时返回。                                               | `"message": "Requests rate limit exceeded, please try again later."` |

### 请求示例

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/?start_time=xxx&end_time=xxx&status=xxx' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 返回示例

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

## 取消异步任务

**接口说明**：取消处于 `PENDING` 状态的任务。其他状态的任务无法取消。

**流控限制**：单千问AI平台账号 20 QPS。

<Warning>
  - 您可以取消该 API Key 所属千问AI平台账号下的所有任务，包括该账号下其他 API Key 创建的任务，但无法取消其他账号的任务。
</Warning>

### 请求端点

```bash
POST https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}/cancel
```

### 请求参数

| 传参方式   | 字段            | 类型     | 必选 | 描述                            | 示例值                                  |
| ------ | ------------- | ------ | -- | ----------------------------- | ------------------------------------ |
| Header | Authorization | String | 是  | API Key，格式为 Bearer sk-ws-xxx。 | Bearer sk-ws-xxx                     |
| Path   | task\_id      | String | 是  | 要取消的任务 ID。                    | a8532587-xxxx-xxxx-xxxx-0c46b17950d1 |

### 返回参数

| 字段          | 类型     | 描述            | 示例值                                                                  |
| ----------- | ------ | ------------- | -------------------------------------------------------------------- |
| request\_id | String | 本次请求的唯一标识。    | 7574ee8f-xxxx-xxxx-xxxx-11c33ab46e51                                 |
| code        | String | 错误码，仅在失败时返回。  | `"code": "Throttling.RateQuota"`                                     |
| message     | String | 错误信息，仅在失败时返回。 | `"message": "Requests rate limit exceeded, please try again later."` |

### 请求示例

```bash
curl -X POST 'https://dashscope.aliyuncs.com/api/v1/tasks/73205176-xxxx-xxxx-xxxx-16bd5d902219/cancel' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

### 返回示例

```json
{
  "request_id": "f1a2b3c4-xxxx-xxxx-xxxx-e03c35068d83"
}
```

## 错误码

| HTTP 状态码 | 错误码（code）            | 错误信息（message）                                                               | 说明                                                     |
| -------- | -------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------ |
| 400      | UnsupportedOperation | Failed to cancel the task, please confirm if the task is in PENDING status. | 取消任务失败，请确认任务状态为 PENDING。仅 PENDING 状态的任务可取消，其他状态任务无法取消。 |
