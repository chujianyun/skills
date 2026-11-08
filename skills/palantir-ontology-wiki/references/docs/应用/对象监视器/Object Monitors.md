:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Object Monitors

:::callout{theme="warning"}
Object Monitors 已被 [Automate](https://www.palantir.com/docs/foundry/automate/overview/) 取代。Automate 是一个完全向后兼容的产品，为平台中的所有业务自动化提供了单一入口。
:::

**Object Monitors** 应用程序允许终端用户和应用构建者查看 Foundry Ontology 中的数据何时发生更改。当发生更改时，object monitors 可以在满足指定条件时自动发送通知或提交操作。object monitors 在您的数据之上运行，旨在帮助用户跟踪单个搜索和 objects。object monitors 还可作为应用构建者的一种工具，将监控和警报功能纳入 Foundry 中构建的应用程序中。

Object 监测是 Foundry 中 objects 层的一项功能，可以被用于在各种工作流中，包括：

* **监测搜索：** 用户可以配置 object monitors，在保存的 object 探索有新结果时或当搜索的所有结果满足汇总标准时进行通知。
* **自动化通知：** 工作流构建者和自助式数据消费者可以配置 object monitors 以响应数据更改发送通知。通知可以通过以下方式发送：
  * 在 Foundry 通知中心内的弹出窗口
  * 电子邮件
  * 短信（使用 [webhooks](https://www.palantir.com/docs/foundry/data-connection/webhooks-overview/) 连接到第三方服务，如 [Twilio ↗](https://www.twilio.com/)）
  * 即时消息（使用 webhooks 连接到第三方服务，如 [Slack ↗](https://slack.com/) 或 [Microsoft Teams ↗](https://www.microsoft.com/microsoft-teams/group-chat-software)）
  * 定制或专有的消息系统
* **工作流自动化：** object monitors 可被用于在符合特定标准的 object 数据上自动执行操作。可以通过 object monitors 自动化的一些任务包括：
  * 检查数据异常并自动将这些 objects 传递到具有逻辑的操作中以解决问题。
  * 监测建议或潜在的操作，并在预配置的事件和时间条件满足时自动应用它们。这些操作可能包括通过 webhooks 向外部系统发出 API 调用，以直接在外部系统中应用更改。

## 访问 Object Monitors

要访问 Object Monitors 应用程序，请单击浏览器左侧的 Foundry 导航侧边栏中的名称或图标。**概览** 页面将显示您最近的监控活动列表，以及总监控数、已订阅或已静音的监控数，以及出现错误或即将过期的监控数。

**监控** 页面显示了可供您使用的监控的完整列表。按活动状态、通知和操作设置、创建者、过期日期、监控类型或条件状态筛选此列表。点击监控以打开监控概览面板，并查看历史活动、订阅者和其他详细信息。

通过[创建一个新的 object monitor](%E5%88%9B%E5%BB%BA%E4%B8%80%E4%B8%AA%E6%96%B0Object%E7%9B%91%E8%A7%86%E5%99%A8.md)来了解更多关于 object 监测的信息。

:::callout{theme="neutral"}
Object 监测旨在监控您数据的内容。如果您正在寻找数据连接和管道构建的健康监测，请查看 [数据健康](https://www.palantir.com/docs/foundry/data-health/overview/) 文档。
:::
