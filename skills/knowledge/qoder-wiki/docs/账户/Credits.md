# Credits

用户无法无限制地使用高级大语言模型，因此我们采用基于 Credits 的配额机制。Credits 表示 AI 在执行任务时消耗的资源配额。

## 消耗 Credits 的功能

在 Qoder 中，以下用户请求会消耗 Credits：

- Inline Chat
- Ask 模式
- Agent 模式
- Quest Mode
- Repo Wiki

具体消耗的 Credits 数量会因任务复杂度和所使用的特定高级模型而有所不同。

## 如何扣减 Credits

不同时间获取的 Credits 到期时间各不相同。系统会优先使用最先到期的 Credits，帮助您最大化发挥 Credits 的价值。

即使用户已用尽高级模型的配额（即 Credits 已耗尽），我们仍会提供每日限量的基础模型调用额度。

## 错误

失败的 Qoder 模型请求不会扣减 Credits。只有在模型 API 调用成功时才会扣除 Credits。

## 任务与 Credits 消耗指南

|  | Median (50K context window) | Median (200K context window) |
| --- | --- | --- |
| Ask | ~ 3 Credits / User Request | ~ 4 Credits / User Request |
| Agent | ~ 7 Credits / User Request | ~ 12 Credits / User Request |
| Quest | / | ~ 100 Credits / Quest Task |
| Repo Wiki | / | ~ 50 Credits / Repository |

**注意：** 未来随着新功能推出，我们可能会依据其资源需求更新 Credits 消耗率。

## 查看 Credits 使用情况

登录 Qoder 官网。点击右上角头像，进入 Settings > Usage。

在这里，你可以查看当前 Plan，以及资源包中可用与已使用的 Credits 信息。

- **Credits 使用优先级**：优先消耗最先到期的 Credits
- **Credits 到期**：不同类型的 Credits 有各自的到期时间

通过你的 Plan 获得的 Credits 在当前订阅周期内有效。这些 Credits 会在订阅周期结束时自动归零。
