> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像画面扩展

> 使用 image-out-painting 模型调整图片尺寸或拓宽画面视野，支持按宽高比、按比例、按方向添加像素以及旋转扩图等多种扩图方式。

当需调整图片尺寸以适配特定布局，或在不裁剪主体的前提下拓宽视野时，可使用图像画面扩展模型。该模型支持多种扩图方式：

- 指定宽高比扩图
- 指定横向或纵向扩展比例
- 自定义上下左右各方向扩展像素数
- 同时支持先旋转再扩图

## 模型与价格

<Note>
  以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
</Note>

| 模型名称               | 计费单价    | 任务下发接口QPS限制 | 同时处理中任务数量 | 免费额度[（查看）](/resources/free-quota) |
| :----------------: | :-----: | :---------: | :-------: | :-------------------------------: |
| image-out-painting | 0.18元/张 | 2           | 5         | 500张                              |

模型限流规则及常见问题，请参见[限流](/developer-guides/administration/rate-limits)。

## 模型效果

**原图**

<Frame>
  <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p826951.png" alt="原图" width="250" />
</Frame>

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", verticalAlign: "middle", width: "25%", paddingBottom: "8px"}}>旋转扩图（逆时针旋转90度）</th>
      <th style={{textAlign: "center", verticalAlign: "middle", width: "25%", paddingBottom: "8px"}}>等比例扩图（1.5:1.5）</th>
      <th style={{textAlign: "center", verticalAlign: "middle", width: "25%", paddingBottom: "8px"}}>指定方向添加像素扩图（上下左右添加像素）</th>
      <th style={{textAlign: "center", verticalAlign: "middle", width: "25%", paddingBottom: "8px"}}>指定宽高比扩图（4:3）</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849684.png" alt="旋转扩图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849665.png" alt="等比例扩图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p834106.jpg" alt="指定方向扩图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p851774.png" alt="指定宽高比扩图" style={{display: "block", width: "100%"}} />
      </td>
    </tr>
  </tbody>
</table>

其他效果示例请参考[更多扩图示例](#更多扩图示例)。

## 快速开始

### 前提条件

您需要已[获取 API Key](/api-reference/preparation/api-key)并[配置 API Key 到环境变量](/api-reference/preparation/export-api-key-env)。

<Tip>
  **扩图建议**：为了获得更自然的扩展效果，建议将最终输出图像的宽高比控制在接近 **1:1** 的范围内。例如，从 1000x1000 扩展到 1500x1500 的效果，通常优于扩展到 2000x1000。
</Tip>

### 示例代码

本模型**仅提供 HTTP API**，请参考以下示例代码。

<Tabs>
  <Tab title="curl">
    <Note>HTTP 调用新手指南请参见 [Postman](/developer-guides/clients-and-developer-tools/postman)。</Note>

    由于图像生成耗时较长，API 采用异步模式，调用流程分两步：

    <Steps>
      <Step title="步骤1：创建任务获取任务ID">
        接口返回任务ID，可根据任务ID查询图像生成的结果。

        **请求示例**

        <CodeGroup>
          ```bash 旋转扩图
          curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
          --header 'X-DashScope-Async: enable' \
          --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
          --header 'Content-Type: application/json' \
          --data '{
              "model": "image-out-painting",
              "input": {
                  "image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E5%9B%BE%E5%83%8F%E7%94%BB%E9%9D%A2%E6%89%A9%E5%B1%95.png"
              },
              "parameters": {
                  "angle": 90,
                  "x_scale": 1.5,
                  "y_scale": 1.5
              }
          }'
          ```

          ```bash 等比例扩图
          curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
          --header 'X-DashScope-Async: enable' \
          --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
          --header 'Content-Type: application/json' \
          --data '{
              "model": "image-out-painting",
              "input": {
                  "image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E5%9B%BE%E5%83%8F%E7%94%BB%E9%9D%A2%E6%89%A9%E5%B1%95.png"
              },
              "parameters": {
                  "x_scale": 1.5,
                  "y_scale": 1.5
              }
          }'
          ```

          ```bash 指定方向添加像素扩图
          curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
          --header 'X-DashScope-Async: enable' \
          --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
          --header 'Content-Type: application/json' \
          --data-raw '{
              "model": "image-out-painting",
              "input": {
                  "image_url": "https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p826951.png"
              },
              "parameters": {
                  "left_offset": 546,
                  "right_offset": 960,
                  "top_offset": 158,
                  "bottom_offset": 939
              }
          }'
          ```

          ```bash 指定宽高比扩图
          curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting' \
          --header 'X-DashScope-Async: enable' \
          --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
          --header 'Content-Type: application/json' \
          --data-raw '{
              "model": "image-out-painting",
              "input": {
                  "image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E5%9B%BE%E5%83%8F%E7%94%BB%E9%9D%A2%E6%89%A9%E5%B1%95.png"
              },
              "parameters":{
                  "angle":0,
                  "output_ratio":"4:3",
                  "best_quality":false,
                  "limit_image_size":true
              }
          }'
          ```
        </CodeGroup>

        **响应示例**

        请求成功后，API 会返回任务 ID。该 `task_id` 的查询有效期为 24 小时。

        ```json
        {
            "output": {
                "task_status": "PENDING",
                "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
            },
            "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
        }
        ```
      </Step>

      <Step title="步骤2：查询任务结果">
        使用步骤1中获取的 `task_id`，通过 GET 请求轮询任务查询接口，直到 `task_status` 变为 SUCCEEDED。任务成功后，响应中会包含生成的图像 URL。

        **请求示例**

        请将 `86ecf553-d340-4e21-xxxxxxxxx` 替换为真实的 task\_id。

        ```bash
        curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
        --header "Authorization: Bearer $DASHSCOPE_API_KEY"
        ```

        **响应示例**

        <Note>图像URL有效期为24小时，请及时下载图像。</Note>

        ```json
        {
            "request_id": "b67df059-ca6a-9d51-afcd-9b3c4456b1e2",
            "output": {
                "task_id": "d76ec1e8-ea27-4038-8913-235c88ef0f70",
                "task_status": "SUCCEEDED",
                "submit_time": "2024-05-16 13:50:01.247",
                "scheduled_time": "2024-05-16 13:50:01.354",
                "end_time": "2024-05-16 13:50:27.795",
                "output_image_url": "https://xxxx/xxxx"
            },
            "usage": {
                "image_count": 1
            }
        }
        ```
      </Step>
    </Steps>
  </Tab>

  <Tab title="Python">
    <Note>千问AI平台不提供官方的图像画面扩展 Python SDK。以下示例代码基于 `requests` 库实现 HTTP 调用，可供参考。</Note>

    **环境配置**

    - 推荐使用 Python 3.8 及以上版本。
    - 请安装必要的依赖包。

    ```bash
    pip install -U requests
    ```

    **请求示例**

    ```python
    import os
    import requests
    import time
    from http import HTTPStatus

    # 从环境变量获取千问AI平台API Key，或直接在代码中赋值
    api_key = os.getenv("DASHSCOPE_API_KEY")
    if not api_key:
      raise ValueError("请设置环境变量 DASHSCOPE_API_KEY")

    def submit_task():
      """提交一个扩图任务"""
      url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/out-painting"

      headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable"  # 异步调用
      }

      body = {
        "model": "image-out-painting",
        "input": {
          "image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E5%9B%BE%E5%83%8F%E7%94%BB%E9%9D%A2%E6%89%A9%E5%B1%95.png"
        },
        "parameters": {
          "angle": 90,
          "x_scale": 1.5,
          "y_scale": 1.5
        }
      }

      response = requests.post(url, headers=headers, json=body)

      if response.status_code == HTTPStatus.OK:
        task_id = response.json().get('output', {}).get('task_id')
        print(f"任务提交成功，任务ID为: {task_id}")
        return task_id
      else:
        print(f"任务提交失败，状态码: {response.status_code}, 响应: {response.text}")
        return None

    def query_task_result(task_id):
      """根据任务ID轮询查询结果"""
      if not task_id:
        return

      url = f"https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}"
      headers = {"Authorization": f"Bearer {api_key}"}

      print("开始查询任务状态...")
      while True:
        response = requests.get(url, headers=headers)
        if response.status_code != HTTPStatus.OK:
          print(f"查询失败，状态码: {response.status_code}, 响应: {response.text}")
          break

        response_data = response.json()
        task_status = response_data.get('output', {}).get('task_status')

        if task_status == 'SUCCEEDED':
          print("任务成功完成！")
          print(f"任务成功响应数据: {response_data}")
          url = response_data.get('output', {}).get('output_image_url', "")
          print(f"生成图片 URL: {url}")
          break
        elif task_status == 'FAILED':
          print(f"任务失败。错误信息: {response_data}")
          break
        else:
          print(f"任务正在处理中，当前状态: {task_status}...")
          # 这是一个简单轮询方式，建议在生产中采用更优雅的轮询机制
          time.sleep(5)  # 等待5秒后再次查询

    if __name__ == '__main__':
      task_id = submit_task()
      if task_id:
        query_task_result(task_id)
    ```

    **响应示例**

    ```plaintext
    任务提交成功，任务ID为: 34d63d84-04c7-452e-88a4-ee76444d05e6
    开始查询任务状态...
    任务正在处理中，当前状态: RUNNING...
    任务正在处理中，当前状态: RUNNING...
    任务成功完成！
    任务成功响应数据: {'request_id': 'ca5c1337-445e-9636-a46a-ba4b0cb39635', 'output': {'task_id': '34d63d84-04c7-452e-88a4-ee76444d05e6', 'task_status': 'SUCCEEDED', 'submit_time': '2025-09-02 16:51:12.386', 'scheduled_time': '2025-09-02 16:51:12.410', 'end_time': '2025-09-02 16:51:22.478', 'output_image_url': 'https://vigen-invi.oss-cn-shanghai.aliyuncs.com/xxx.jpg?xxxx'}, 'usage': {'image_count': 1}}
    生成图片 URL: https://vigen-invi.oss-cn-shanghai.aliyuncs.com/xxx.jpg?xxxx
    ```
  </Tab>
</Tabs>

## 更多扩图示例

### 按宽高比扩图

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", width: "35%", paddingBottom: "8px"}}>原图</th>
      <th style={{textAlign: "center", width: "35%", paddingBottom: "8px"}}>扩图后</th>
      <th style={{textAlign: "left", width: "30%", paddingBottom: "8px"}}>扩图参数</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p851787.png" alt="原图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p851788.png" alt="扩图后" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{verticalAlign: "middle"}}><code>output\_ratio: "1:1"</code></td>
    </tr>
  </tbody>
</table>

### 按比例扩图

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", width: "35%", paddingBottom: "8px"}}>原图</th>
      <th style={{textAlign: "center", width: "35%", paddingBottom: "8px"}}>扩图后</th>
      <th style={{textAlign: "left", width: "30%", paddingBottom: "8px"}}>扩图参数</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849744.png" alt="原图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849746.png" alt="扩图后" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{verticalAlign: "middle"}}><code>x\_scale: 2.46, y\_scale: 2.20</code></td>
    </tr>

    <tr>
      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849750.png" alt="原图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849751.png" alt="扩图后" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{verticalAlign: "middle"}}><code>x\_scale: 1.86, y\_scale: 1.72</code></td>
    </tr>

    <tr>
      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849758.png" alt="原图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849759.png" alt="扩图后" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{verticalAlign: "middle"}}><code>x\_scale: 2.39, y\_scale: 1.24</code></td>
    </tr>

    <tr>
      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849761.png" alt="原图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849762.png" alt="扩图后" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{verticalAlign: "middle"}}><code>x\_scale: 1.41, y\_scale: 1.24</code></td>
    </tr>
  </tbody>
</table>

### 按方向添加像素扩图

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", width: "35%", paddingBottom: "8px"}}>原图</th>
      <th style={{textAlign: "center", width: "35%", paddingBottom: "8px"}}>扩图后</th>
      <th style={{textAlign: "left", width: "30%", paddingBottom: "8px"}}>扩图参数</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849779.png" alt="原图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849782.png" alt="扩图后" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{verticalAlign: "middle"}}><code>left: 758, right: 968, top: 343, bottom: 539</code></td>
    </tr>

    <tr>
      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849794.png" alt="原图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849795.png" alt="扩图后" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{verticalAlign: "middle"}}><code>left: 394, right: 879, top: 914, bottom: 709</code></td>
    </tr>

    <tr>
      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849798.png" alt="原图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849800.png" alt="扩图后" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{verticalAlign: "middle"}}><code>left: 698, right: 420, top: 614, bottom: 643</code></td>
    </tr>
  </tbody>
</table>

### 旋转扩图

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", width: "35%", paddingBottom: "8px"}}>原图</th>
      <th style={{textAlign: "center", width: "35%", paddingBottom: "8px"}}>扩图后</th>
      <th style={{textAlign: "left", width: "30%", paddingBottom: "8px"}}>扩图参数</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849722.png" alt="原图" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{textAlign: "center", verticalAlign: "middle"}}>
        <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7181881571/p849713.png" alt="扩图后" style={{display: "block", width: "100%"}} />
      </td>

      <td style={{verticalAlign: "middle"}}><code>angle: 45, x\_scale: 1.2, y\_scale: 1.2</code></td>
    </tr>
  </tbody>
</table>

## API 参考

关于图像画面扩展模型的输入输出参数，请参见[图像画面扩展 API](/api-reference/image-generation/image-out-painting/create-task)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](/api-reference/preparation/error-messages)进行解决。

## 常见问题

**Q：调用 API 时返回错误，可能是什么原因？**

A：请检查以下几点：

- API Key 是否正确，并且已配置到环境变量或代码中。
- 检查免费额度是否已用尽。
- 请求参数是否正确，例如 `image_url` 是否可公网访问。本地文件请参见[上传文件获取临时URL](/api-reference/platform-api/file/upload-file)。

**Q：为什么我的任务长时间处于 `RUNNING` 状态？**

A：图像生成需要一定时间，通常在数十秒内完成。如果任务长时间未完成，可能是因为系统繁忙。如果超过数分钟仍未完成，请检查服务状态或联系技术支持。
