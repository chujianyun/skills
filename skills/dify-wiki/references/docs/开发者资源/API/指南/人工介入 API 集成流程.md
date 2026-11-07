# 人工介入 API 集成流程

> 通过 API 处理暂停中的人工介入表单的端到端流程

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/api-reference/guides/human-input-flow.md)。

当工作流执行到 [人工介入](../../../%E4%BD%BF%E7%94%A8/%E7%BC%96%E6%8E%92/Workflow%20%E4%B8%8E%20Chatflow/%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5/%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5.md) 节点时会暂停，并在流式响应中发出 `human_input_required` 事件。该事件携带 `form_token`，集成方可凭其驱动整个表单生命周期，直到工作流恢复执行。

各接口的字段参考，详见 [人工介入 API](../%E5%BA%94%E7%94%A8%20API/%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5/%E8%8E%B7%E5%8F%96%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5%E8%A1%A8%E5%8D%95.md)。

## 流程

下方流程同时适用于 Workflow 和 Chatflow 应用。两者仅在第 1 步的入口接口上有所不同。

**1. 以流式返回方式启动应用**

1. Workflow 应用调用 [执行工作流](../%E5%BA%94%E7%94%A8%20API/%E5%B7%A5%E4%BD%9C%E6%B5%81%E8%BF%90%E8%A1%8C/%E6%89%A7%E8%A1%8C%E5%B7%A5%E4%BD%9C%E6%B5%81.md)，Chatflow 应用调用 [发送对话消息](../%E5%BA%94%E7%94%A8%20API/%E5%AF%B9%E8%AF%9D%E6%B6%88%E6%81%AF/%E5%8F%91%E9%80%81%E5%AF%B9%E8%AF%9D%E6%B6%88%E6%81%AF.md)，并传入终端用户的 `user` 标识。
2. 在 SSE 流中关注 `human_input_required` 事件，提取其中的 `form_token`。

   若 `form_token` 为 `null`，说明表单没有通过 Web 应用投递，而 API 只能处理这种投递方式。表单实际的投递方式列在 `approval_channels` 中。此时可以直接跳到第 5 步，等待接收者通过这些方式回复，或者 [停止这次运行](%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5%20API%20%E9%9B%86%E6%88%90%E6%B5%81%E7%A8%8B.md#停止已暂停的运行)。

   `human_input_required` 事件同时携带本次运行的 `workflow_run_id`；请保留它，以便在第 5 步需要时恢复监听。

**2. 获取表单定义**

使用 `form_token` 调用 [获取人工介入表单](../%E5%BA%94%E7%94%A8%20API/%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5/%E8%8E%B7%E5%8F%96%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5%E8%A1%A8%E5%8D%95.md) 接口。响应包含渲染后的 Markdown、输入字段定义、可用操作、已预填的默认值，以及一个 `expiration_time`，超过该时间后表单将无法再提交。将表单呈现给接收者。

若表单在提交前过期，暂停的运行会按节点配置的超时行为处理；恢复后的事件流中携带的是 `human_input_form_timeout`，而非 `human_input_form_filled`。

**3. （仅文件输入）上传本地文件**

若接收者为 `file` 或 `file-list` 输入附加了本地文件，请先通过 [上传文件](../%E5%BA%94%E7%94%A8%20API/%E6%96%87%E4%BB%B6%E6%93%8D%E4%BD%9C/%E4%B8%8A%E4%BC%A0%E6%96%87%E4%BB%B6.md) 上传。该接口返回一个 `id`，提交时作为 `upload_file_id` 引用。执行、上传和提交各次调用使用同一个 `user`（见 [终端用户身份](%E7%BB%88%E7%AB%AF%E7%94%A8%E6%88%B7%E8%BA%AB%E4%BB%BD.md)）。

远程文件无需上传：在提交时以 `{transfer_method: remote_url, url}` 映射内联附加即可。

**4. 提交响应**

调用 [提交人工介入表单](../%E5%BA%94%E7%94%A8%20API/%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5/%E6%8F%90%E4%BA%A4%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5%E8%A1%A8%E5%8D%95.md) 接口，附上接收者输入的值、所选的 `action` 以及你的 `user`。`action` 必须是第 2 步表单定义中的某个操作。

文件输入既可使用 `{transfer_method: local_file, upload_file_id}` 映射（来自第 3 步），也可在提交时直接使用 `{transfer_method: remote_url, url}` 映射。两种模式的权衡详见 [先上传 vs 直接提交远程 URL](%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5%20API%20%E9%9B%86%E6%88%90%E6%B5%81%E7%A8%8B.md#先上传-vs-直接提交远程-url)。

提交一旦成功即为最终结果：表单随之关闭，工作流沿匹配的操作分支恢复执行，同一个 `form_token` 无法再次提交。

若提交被拒绝（操作无效、缺少必填输入，或远程文件抓取失败），表单保持不变，修正输入后可用同一个 `form_token` 重新提交。

**5. 继续监听工作流**

若原 SSE 流已关闭，可调用 [流式获取工作流事件](../%E5%BA%94%E7%94%A8%20API/%E5%B7%A5%E4%BD%9C%E6%B5%81%E8%BF%90%E8%A1%8C/%E6%B5%81%E5%BC%8F%E8%8E%B7%E5%8F%96%E5%B7%A5%E4%BD%9C%E6%B5%81%E4%BA%8B%E4%BB%B6.md) 重新连接：使用第 1 步中的 `workflow_run_id`，并携带启动运行时的同一个 `user`（`user` 不一致会返回 404）。

恢复后的事件流会先携带确认提交的 `human_input_form_filled`（表单过期时则是 `human_input_form_timeout`），随后像从未暂停过一样，继续输出其余节点事件直至完成。

如需先重放已执行节点的状态，可附带 `include_state_snapshot=true`。若工作流串联了多个人工介入节点，流默认会在每次暂停时关闭；传入 `continue_on_pause=true` 可让同一条流跨越所有暂停保持连接。

## 停止已暂停的运行

如果不想回复表单，而是直接结束已暂停的运行，请用运行的 `task_id` 调用 [停止工作流任务](../%E5%BA%94%E7%94%A8%20API/%E5%B7%A5%E4%BD%9C%E6%B5%81%E8%BF%90%E8%A1%8C/%E5%81%9C%E6%AD%A2%E5%B7%A5%E4%BD%9C%E6%B5%81%E4%BB%BB%E5%8A%A1.md)（Workflow 应用）或 [停止响应](../%E5%BA%94%E7%94%A8%20API/%E5%AF%B9%E8%AF%9D%E6%B6%88%E6%81%AF/%E5%81%9C%E6%AD%A2%E5%93%8D%E5%BA%94.md)（Chatflow 应用）。`task_id` 可以从事件流的事件中获取。对于 Chatflow 应用，请传入发起这次运行的 `user`。传入其他 `user` 时，运行不会停止，但调用仍会返回成功。

运行会以 `stopped` 状态结束。表单随之过期，`form_token` 也就不再可用。正在监听 [流式获取工作流事件](../%E5%BA%94%E7%94%A8%20API/%E5%B7%A5%E4%BD%9C%E6%B5%81%E8%BF%90%E8%A1%8C/%E6%B5%81%E5%BC%8F%E8%8E%B7%E5%8F%96%E5%B7%A5%E4%BD%9C%E6%B5%81%E4%BA%8B%E4%BB%B6.md) 的客户端会收到状态为 `stopped` 的 `workflow_finished` 事件。

## 先上传 vs 直接提交远程 URL

文件输入支持两种提交模式：

* **先上传，再使用 `upload_file_id`**（推荐）

  [上传文件](../%E5%BA%94%E7%94%A8%20API/%E6%96%87%E4%BB%B6%E6%93%8D%E4%BD%9C/%E4%B8%8A%E4%BC%A0%E6%96%87%E4%BB%B6.md) 在上传阶段即校验文件大小限制，接收者可立即看到错误并在提交前重试。

* **使用 `transfer_method: remote_url` 直接提交**

  后端在提交阶段抓取文件。集成更快，但任何大小、类型或抓取失败都会拒绝整次提交，接收者可能需要重填其他字段。

> [!TIP]
>
> 对于需要接收者反馈的交互式表单，优先选择先上传模式。仅当流程完全程序化、无需任何人重新输入时，直接提交模式的代价才能被抵消。

## 提交方式要求

人工介入 API 仅支持通过人工介入节点的 Web 应用提交方式投递的表单。仅通过邮件投递的表单不会向 API 暴露 `form_token`。

## 示例：带文件的提交

本示例的表单包含一个 `feedback` 段落输入、一个 `attachments` 文件列表输入，以及 `approve` / `reject` 两个操作。

1. 调用 [获取人工介入表单](../%E5%BA%94%E7%94%A8%20API/%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5/%E8%8E%B7%E5%8F%96%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5%E8%A1%A8%E5%8D%95.md) 接口获取表单定义：

   ```http theme={null}
   GET /form/human_input/<form_token>
   Authorization: Bearer {api-key}
   ```

   返回表单定义：

   ```json theme={null}
   {
     "form_content": "请审阅草稿并确认或提出修改。",
     "inputs": [
       {
         "type": "paragraph",
         "output_variable_name": "feedback",
         "default": {
           "type": "constant",
           "selector": [],
           "value": ""
         }
       },
       {
         "type": "file-list",
         "output_variable_name": "attachments",
         "allowed_file_types": [
           "image",
           "document"
         ],
         "allowed_file_extensions": [],
         "allowed_file_upload_methods": [
           "local_file",
           "remote_url"
         ],
         "number_limits": 5
       }
     ],
     "resolved_default_values": {},
     "user_actions": [
       {
         "id": "approve",
         "title": "批准",
         "button_style": "primary"
       },
       {
         "id": "reject",
         "title": "请求修改",
         "button_style": "default"
       }
     ],
     "expiration_time": 1745510400
   }
   ```

2. 针对每个本地文件，调用 [上传文件](../%E5%BA%94%E7%94%A8%20API/%E6%96%87%E4%BB%B6%E6%93%8D%E4%BD%9C/%E4%B8%8A%E4%BC%A0%E6%96%87%E4%BB%B6.md) 接口：

   ```http theme={null}
   POST /files/upload
   Authorization: Bearer {api-key}
   Content-Type: multipart/form-data

   file=<binary>
   user=abc-123
   ```

   返回 `{"id": "1a77f0df-...", ...}`。

3. 调用 [提交人工介入表单](../%E5%BA%94%E7%94%A8%20API/%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5/%E6%8F%90%E4%BA%A4%E4%BA%BA%E5%B7%A5%E4%BB%8B%E5%85%A5%E8%A1%A8%E5%8D%95.md) 接口，附上接收者输入与所选操作：

   ```http theme={null}
   POST /form/human_input/<form_token>
   Authorization: Bearer {api-key}
   Content-Type: application/json

   {
     "inputs": {
       "feedback": "可以发布",
       "attachments": [
         {"transfer_method": "local_file", "upload_file_id": "1a77f0df-..."}
       ]
     },
     "action": "approve",
     "user": "abc-123"
   }
   ```

   返回 `{}`。工作流沿 `approve` 分支恢复执行。

4. 调用 [流式获取工作流事件](../%E5%BA%94%E7%94%A8%20API/%E5%B7%A5%E4%BD%9C%E6%B5%81%E8%BF%90%E8%A1%8C/%E6%B5%81%E5%BC%8F%E8%8E%B7%E5%8F%96%E5%B7%A5%E4%BD%9C%E6%B5%81%E4%BA%8B%E4%BB%B6.md) 重新连接运行的事件流，跟踪至运行完成，与上文流程的第 5 步相同。
