# 排障与反馈

资料核对：2026-09-16。先收集端、版本、空间与错误表现；避免从“功能不可见”直接推断产品故障。

## 最短排查路径

| 现象 | 先检查 | 官方来源 |
|---|---|---|
| 开了连接器却无工具 | 新建对话、配置完整性、网络与账号授权 | [连接器](https://qwenwork.cn/docs/features/connectors) |
| 桌面定时任务没跑 | 本地时区、唤醒状态、执行记录和数据源 | [桌面定时任务](https://qwenwork.cn/docs/desktop/scheduled-tasks) |
| 成员有账号却不能用积分 | 空间、有效订阅、坐席、上级与成员限额 | [成员管理](https://qwenwork.cn/docs/enterprise/members) |
| 换电脑看不到历史 | 桌面历史是本机记录，不能假设自动同步 | [桌面入门](https://qwenwork.cn/docs/getting-started/desktop-workflow) |
| 网页打不开 | 根据 Pages 状态及 403/429/503 区分原因 | [我的网页](https://qwenwork.cn/docs/web/pages) |
| 上传失败 | 剩余存储、空文件、重名、附件数量和当前上传状态 | [个人网盘](https://qwenwork.cn/docs/web/drive) |

## 需要官方协助时

准备现象、预期、发生时间、复现步骤，以及脱敏截图或录屏。向官方客服提交受影响会话的 User ID / Session ID，不能拿正常会话编号代替。找不到编号时先提供发生时间和会话截图。密码、验证码、访问令牌不要放入反馈或公开 Wiki。

来源：[提问指南](https://qwenwork.cn/docs/feedback/how-to-ask)。

## 数据范围与安全说明

官方隐私说明针对 Web 与钉钉内服务，涉及账号、任务、上传资料、使用与管理数据；不能把它直接解释为所有桌面组件、第三方连接器的统一承诺。涉及数据存储、隐私模式或跨境要求时核对当前协议、企业配置和服务提供方说明，不仅依赖本地摘要。

来源：[隐私与安全](https://qwenwork.cn/docs/getting-started/privacy-security)。
