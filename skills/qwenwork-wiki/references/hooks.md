# 企业 HTTP Hooks

资料核对：2026-09-16。以下仅为实现时易错点，完整字段与当前行为须读取官方专页。

## 事件与执行边界

企业后台按事件配置 HTTP Hook，由桌面客户端调用。事件包括 `SessionStart`、`UserPromptSubmit`、`PreToolUse`、`PostToolUse`、`Stop`、`Notification`。

要在操作发生前阻断用 PreToolUse；PostToolUse 已发生在工具执行之后，不能撤销副作用，也不能保证隐藏原输出。Stop 的 `decision: block` 要求继续工作，而 `continue: false` 表示停止；服务应根据 `stop_hook_active` 限制重复要求，防止循环。

## 配置与失败语义

Hook 类型为 `http`，以 POST 发送 JSON；同事件匹配项可并行执行且按 URL 去重，不能依赖数组顺序。`updatedInput` 是完整替换，不是局部合并。PreToolUse 权限决定聚合顺序为 deny、ask、allow。

不能把 HTTP 失败当作安全拒绝：非 2xx、连接失败或超时会记录错误后继续原流程，且不自动重试。PreToolUse 的 2xx 响应若 JSON 或字段非法则拒绝工具调用。需要严格阻断时，必须核对事件专用响应，不用超时模拟拒绝。

来源：[Hooks 官方说明](https://qwenwork.cn/docs/desktop/hooks)。
