> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Postman

> API 测试工具

Postman 是一款图形化 HTTP 测试工具，方便测试千问AI平台 API。你可以用它验证 API 端点、测试图片/视频生成等异步操作，以及在编写代码之前快速验证集成方案。

## 快速开始

几分钟即可上手：

```text
# 1. 安装
从 postman.com/downloads 下载 Postman

# 2. 创建请求（New → HTTP Request）
Method: POST
URL: https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation

# 3. 配置（Headers 选项卡）
Authorization: Bearer $DASHSCOPE_API_KEY
Content-Type: application/json

# 4. 测试（Body 选项卡 → raw → JSON）
{
  "model": "qwen-plus",
  "input": {
    "messages": [{"role": "user", "content": "Hello, who are you?"}]
  }
}
```

预期结果：返回包含模型回复的 JSON 响应

## 配置

### 基本设置

为千问AI平台 API 配置 Postman：

- API 端点：`https://dashscope.aliyuncs.com`
- 认证方式：Bearer Token（使用 API Key）
- Content-Type：`application/json`

### API 类型

千问AI平台提供两种 API 模式：

| 类型     | 适用场景            | 响应方式                |
| ------ | --------------- | ------------------- |
| **同步** | 文本生成、Embeddings | 即时返回结果              |
| **异步** | 图片/视频生成         | 返回 Task ID → 轮询获取结果 |

## 同步 API

### 文本生成示例

<Steps>
  <Step title="创建请求">
    New → HTTP Request → POST
  </Step>

  <Step title="设置 URL">
    ```
    https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
    ```
  </Step>

  <Step title="添加请求头">
| Key           | Value                        |
| ------------- | ---------------------------- |
| Authorization | Bearer \$DASHSCOPE\_API\_KEY |
| Content-Type  | application/json             |
  </Step>

  <Step title="添加请求体">
    ```json
    {
      "model": "qwen-plus",
      "input": {
        "messages": [
          {"role": "user", "content": "Write a haiku about coding"}
        ]
      },
      "parameters": {
        "temperature": 0.7
      }
    }
    ```
  </Step>

  <Step title="发送请求">
    点击 **Send** → 查看响应
  </Step>
</Steps>

## 异步 API

对于耗时较长的任务（图片、视频生成），使用异步模式：

### 第 1 步：创建任务

<Steps>
  <Step title="配置请求">
    Method：**POST**
    URL：`https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis`
  </Step>

  <Step title="添加请求头">
| Key               | Value                        |
| ----------------- | ---------------------------- |
| X-DashScope-Async | enable                       |
| Authorization     | Bearer \$DASHSCOPE\_API\_KEY |
| Content-Type      | application/json             |
  </Step>

  <Step title="添加请求体">
    ```json
    {
      "model": "wan2.6-t2i",
      "input": {
        "prompt": "A serene mountain landscape at sunset"
      },
      "parameters": {
        "size": "1024*1024",
        "n": 1
      }
    }
    ```
  </Step>

  <Step title="发送并保存 task_id">
    点击 **Send** 发送请求，获取 `task_id`。有效期 24 小时，过期后无法查询，请及时获取结果。

    ```json
    {
      "request_id": "896b2ccd-a0cd-40a8-a557-bb73cee5cf95",
      "output": {
        "task_id": "42442de9-917d-4c41-80a7-37fb7ad25ed2",
        "task_status": "PENDING"
      }
    }
    ```
  </Step>
</Steps>

### 第 2 步：查询结果

<Steps>
  <Step title="配置查询请求">
    Method：**GET**
    URL：`https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}`
    将 `{task_id}` 替换为实际的任务 ID
  </Step>

  <Step title="添加请求头">
| Key           | Value                        |
| ------------- | ---------------------------- |
| Authorization | Bearer \$DASHSCOPE\_API\_KEY |
  </Step>

  <Step title="轮询直至完成">
    重复发送请求（建议每 3-5 秒一次），直到 `task_status` 变为 `SUCCEEDED`，获取图像 URL。图像 URL 有效期为 **24 小时**，请及时下载。

    ```json
    {
      "output": {
        "task_id": "42442de9-917d-4c41-80a7-37fb7ad25ed2",
        "task_status": "SUCCEEDED",
        "results": [
          {
            "orig_prompt": "A serene mountain landscape at sunset",
            "url": "https://dashscope-result-wlcb.oss-cn-wulanchabu.aliyuncs.com/..."
          }
        ]
      }
    }
    ```
  </Step>
</Steps>

## cURL 到 Postman 的映射

将 cURL 示例转换为 Postman 请求：

| cURL              | Postman        | 位置                 |
| ----------------- | -------------- | ------------------ |
| `curl -X POST`    | POST           | Method 下拉菜单        |
| URL               | URL            | URL 输入框            |
| `-H 'Key: Value'` | Headers        | Headers 选项卡        |
| `-d '{...}'`      | Body           | Body 选项卡（raw JSON） |
| `$VARIABLE`       | `{{variable}}` | 环境变量               |

## 环境变量

设置可复用的变量：

<Steps>
  <Step title="创建环境">
    Environments → Create New → 命名为 "千问AI平台"
  </Step>

  <Step title="添加变量">
| Variable  | Value                                                            |
| --------- | ---------------------------------------------------------------- |
| api\_key  | \$DASHSCOPE\_API\_KEY                                            |
| base\_url | [https://dashscope.aliyuncs.com](https://dashscope.aliyuncs.com) |
| model     | qwen-plus                                                        |
  </Step>

  <Step title="在请求中使用">
    - Headers：`Bearer {{api_key}}`
    - URL：`{{base_url}}/api/v1/...`
    - Body：`"model": "{{model}}"`
  </Step>
</Steps>

## 集合

将相关请求组织在一起：

1. **创建集合**：Collections → New Collection
2. **添加请求**：将请求拖入集合
3. **分享**：导出为 JSON 或分享链接
4. **批量运行**：Runner → 选择集合 → Run

## 测试技巧

### 响应验证

在 **Tests** 选项卡中添加测试脚本：

```javascript
pm.test("Status is 200", () => {
  pm.response.to.have.status(200);
});

pm.test("Has output", () => {
  const json = pm.response.json();
  pm.expect(json).to.have.property("output");
});
```

### 异步轮询自动化

通过脚本自动化任务轮询：

```javascript
// 在创建任务请求的 Tests 选项卡中
const taskId = pm.response.json().output.task_id;
pm.environment.set("task_id", taskId);

// 设置下一个请求为查询任务状态
postman.setNextRequest("Query Task Status");
```

## 常见问题排查

**401 Unauthorized**

> 解决方法：
>
> - 检查 API Key 是否正确
> - 确认 Authorization 请求头包含 "Bearer " 前缀
> - 确认 API Key 仍有可用额度

**400 Bad Request**

> 解决方法：
>
> - 检查请求体的 JSON 语法
> - 确认必填字段完整
> - 确认模型名称正确

**任务一直处于 PENDING 状态**

> 解决方法：
>
> - 图片/视频生成可能需要几分钟
> - 每 5-10 秒轮询一次
> - 查看 task\_metrics 了解进度

**连接超时**

> 解决方法：
>
> - 在 Settings → General 中增大超时时间
> - 检查网络连接
> - 先尝试发送更简单的请求

## 生产环境注意事项

<Warning>
  Postman 仅用于测试。在生产环境中：

  - 使用对应编程语言的官方 SDK
  - 实现完善的错误处理
  - 为异步任务添加重试逻辑
  - 安全存储 API Key
</Warning>

## 相关资源

- **API 参考**：[完整 API 文档 →](/api-reference/chat/dashscope)
- **模型**：[可用模型 →](/developer-guides/getting-started/text-generation-models) | [定价 →](/developer-guides/getting-started/pricing)
- **SDK**：[官方客户端库 →](/api-reference/preparation/install-sdk)
- **Postman 文档**：[Postman 官方指南 →](https://learning.postman.com/docs)
