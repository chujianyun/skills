# Agent API

> 面向 Agent 应用的 API，涵盖流式对话消息、会话管理、文件上传及应用配置

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/api-reference/guides/agent.md)。

> [!NOTE]
>
> 这里的 Agent 指新的 Agent 应用类型（`agent` 模式）；旧版 Agent 应用（`agent-chat`）参见 [Chatbot 和旧版 Agent](%E5%AF%B9%E8%AF%9D%E5%9E%8B%E5%BA%94%E7%94%A8%20API.md)。

[Agent 应用](https://docs.dify.ai/zh/self-host/use-dify/build/new-agent/overview.md) 运行在 `agent` 模式下：发送消息、流式接收生成中的回复，并通过会话保留多轮上下文。

模型会自主推理并调用工具，这些过程也会出现在事件流中：回复文本以 `agent_message` 事件增量流式返回，每个推理步骤和工具调用则以 `agent_thought` 事件同步返回。

每轮回复结束时，会先收到一个携带完整回答的 `message` 事件，然后是 `message_end`。实时渲染按 `agent_message` 增量拼接即可；收尾的 `message` 就是最终回答，不要再追加拼接。

每个 `agent_thought` 事件都包含该步骤的 `thought`、所调用的 `tool` 及其 `tool_input`，以及工具返回的 `observation`。完整的流式事件结构，详见 [发送对话消息](../../%E5%BA%94%E7%94%A8%20API/%E5%AF%B9%E8%AF%9D%E6%B6%88%E6%81%AF/%E5%8F%91%E9%80%81%E5%AF%B9%E8%AF%9D%E6%B6%88%E6%81%AF.md)。

> [!NOTE]
>
> 认证方式、基础 URL，以及按终端用户区分数据的 `user` 字段，详见 [快速开始](../Dify%20API%20%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md) 和 [终端用户身份](../%E7%BB%88%E7%AB%AF%E7%94%A8%E6%88%B7%E8%BA%AB%E4%BB%BD.md)。

## 发送消息并接收流式回复

* **[发送对话消息](../../%E5%BA%94%E7%94%A8%20API/%E5%AF%B9%E8%AF%9D%E6%B6%88%E6%81%AF/%E5%8F%91%E9%80%81%E5%AF%B9%E8%AF%9D%E6%B6%88%E6%81%AF.md)**：向 Agent 应用发送用户提问。仅支持流式返回，使用阻塞式返回会收到 400 `bad_request` 错误。

  回复文本以 `agent_message` 增量事件流式返回，约每 0.5 秒合并发送一批，而非逐 token 推送。

  收尾的 `message_end` 事件会报告 token 用量，但不会包含知识检索引用（`retriever_resources`）。

  单次运行有两类上限，触及任一上限时，流式响应都会以 `agent_run_limit_exceeded` 错误码结束：

  * **时长**：单次运行默认在 1 小时后被终止。自部署环境要运行更长时间，可将 `APP_MAX_EXECUTION_TIME`、`WORKFLOW_MAX_EXECUTION_TIME` 和 `DIFY_AGENT_RUN_TIMEOUT_SECONDS` 都调高到目标时长以上。这些变量的说明详见 [环境变量](https://docs.dify.ai/zh/self-host/deploy/configuration/environments.md)。
  * **模型请求次数**：最多 500 次。

* **[停止响应](../../%E5%BA%94%E7%94%A8%20API/%E5%AF%B9%E8%AF%9D%E6%B6%88%E6%81%AF/%E5%81%9C%E6%AD%A2%E5%93%8D%E5%BA%94.md)**：在回复完成前中断流式输出。

* **[获取下一轮建议问题列表](../../%E5%BA%94%E7%94%A8%20API/%E5%AF%B9%E8%AF%9D%E6%B6%88%E6%81%AF/%E8%8E%B7%E5%8F%96%E4%B8%8B%E4%B8%80%E8%BD%AE%E5%BB%BA%E8%AE%AE%E9%97%AE%E9%A2%98%E5%88%97%E8%A1%A8.md)**：回复完成后，基于当前对话内容推荐后续问题。

## 管理会话

* **[获取会话列表](../../%E5%BA%94%E7%94%A8%20API/%E4%BC%9A%E8%AF%9D%E7%AE%A1%E7%90%86/%E8%8E%B7%E5%8F%96%E4%BC%9A%E8%AF%9D%E5%88%97%E8%A1%A8.md)**：按最近活跃时间排序，返回当前用户的会话。
* **[获取会话历史消息](../../%E5%BA%94%E7%94%A8%20API/%E4%BC%9A%E8%AF%9D%E7%AE%A1%E7%90%86/%E8%8E%B7%E5%8F%96%E4%BC%9A%E8%AF%9D%E5%8E%86%E5%8F%B2%E6%B6%88%E6%81%AF.md)**：返回某个会话的历史消息，适合滚动加载的聊天界面。每条消息的 `agent_thoughts` 数组会包含该轮的推理步骤。
* **[重命名会话](../../%E5%BA%94%E7%94%A8%20API/%E4%BC%9A%E8%AF%9D%E7%AE%A1%E7%90%86/%E9%87%8D%E5%91%BD%E5%90%8D%E4%BC%9A%E8%AF%9D.md)**：为会话设置名称，或根据会话内容自动生成名称。
* **[删除会话](../../%E5%BA%94%E7%94%A8%20API/%E4%BC%9A%E8%AF%9D%E7%AE%A1%E7%90%86/%E5%88%A0%E9%99%A4%E4%BC%9A%E8%AF%9D.md)**：删除会话及其消息。

## 上传文件

* **[上传文件](../../%E5%BA%94%E7%94%A8%20API/%E6%96%87%E4%BB%B6%E6%93%8D%E4%BD%9C/%E4%B8%8A%E4%BC%A0%E6%96%87%E4%BB%B6.md)**：上传图片、文档、音频或视频文件，仅限上传的终端用户使用。

  传给 [发送对话消息](../../%E5%BA%94%E7%94%A8%20API/%E5%AF%B9%E8%AF%9D%E6%B6%88%E6%81%AF/%E5%8F%91%E9%80%81%E5%AF%B9%E8%AF%9D%E6%B6%88%E6%81%AF.md) 的文件，会作为可下载的引用提供给 Agent，Agent 可在其沙箱中获取并查看。

* **[获取终端用户信息](../../%E5%BA%94%E7%94%A8%20API/%E7%BB%88%E7%AB%AF%E7%94%A8%E6%88%B7/%E8%8E%B7%E5%8F%96%E7%BB%88%E7%AB%AF%E7%94%A8%E6%88%B7%E4%BF%A1%E6%81%AF.md)**：根据终端用户 ID（例如上传文件响应中的 `created_by`）查询该用户的详细信息。

## 语音转写与合成

* **[语音转文字](../../%E5%BA%94%E7%94%A8%20API/%E8%AF%AD%E9%9F%B3%E4%B8%8E%E6%96%87%E5%AD%97%E8%BD%AC%E6%8D%A2/%E8%AF%AD%E9%9F%B3%E8%BD%AC%E6%96%87%E5%AD%97.md)**：将上传的音频文件（MP3、M4A、WAV、AMR 或 MPGA，最大 30 MB）转写为文字，让终端用户用语音代替打字输入。
* **[文字转语音](../../%E5%BA%94%E7%94%A8%20API/%E8%AF%AD%E9%9F%B3%E4%B8%8E%E6%96%87%E5%AD%97%E8%BD%AC%E6%8D%A2/%E6%96%87%E5%AD%97%E8%BD%AC%E8%AF%AD%E9%9F%B3.md)**：将回复合成为语音。

## 获取应用信息与配置

* **[获取应用基本信息](../../%E5%BA%94%E7%94%A8%20API/%E5%BA%94%E7%94%A8%E9%85%8D%E7%BD%AE/%E8%8E%B7%E5%8F%96%E5%BA%94%E7%94%A8%E5%9F%BA%E6%9C%AC%E4%BF%A1%E6%81%AF.md)**：返回应用的名称、描述、标签和模式。
* **[获取应用参数](../../%E5%BA%94%E7%94%A8%20API/%E5%BA%94%E7%94%A8%E9%85%8D%E7%BD%AE/%E8%8E%B7%E5%8F%96%E5%BA%94%E7%94%A8%E5%8F%82%E6%95%B0.md)**：返回调用需在 `inputs` 中传入的字段（名称、类型、默认值），以及应用的功能开关，可据此构建请求或客户端界面。
* **[获取应用元数据](../../%E5%BA%94%E7%94%A8%20API/%E5%BA%94%E7%94%A8%E9%85%8D%E7%BD%AE/%E8%8E%B7%E5%8F%96%E5%BA%94%E7%94%A8%E5%85%83%E6%95%B0%E6%8D%AE.md)**：返回应用的配置元数据；对 Agent 应用，`tool_icons` 为空。
* **[获取应用 Web 应用设置](../../%E5%BA%94%E7%94%A8%20API/%E5%BA%94%E7%94%A8%E9%85%8D%E7%BD%AE/%E8%8E%B7%E5%8F%96%E5%BA%94%E7%94%A8%20WebApp%20%E8%AE%BE%E7%BD%AE.md)**：返回 Web 应用的站点配置、主题和自定义选项。
