# Dify 插件

> 模块化组件，通过外部服务、自定义逻辑和专业工具扩展 Dify AI 应用

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/develop-plugin/getting-started/getting-started-dify-plugin.md)。

Dify 插件是模块化组件，通过外部服务、自定义功能和专业工具扩展你用 Dify 构建的 AI 应用。

![Marketplace](../../../../assets/images/cc5413742bbc28b91c14c2d2.png)

Marketplace

通过插件，你的 AI 应用可以：

* 连接外部 API
* 处理不同类型的数据
* 执行专业计算
* 执行现实世界的操作

## 从这里开始

> [card] [选择插件类型](%E9%80%89%E6%8B%A9%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B.md)
>
> 一份简短的决策指南，帮你在工具、模型、Agent 策略、扩展、数据源和触发器插件之间做出选择。

> [card] [安装 CLI](Dify%20%E6%8F%92%E4%BB%B6%20CLI.md)
>
> 在本机上配置 `dify`，几分钟内即可搭建一个新的插件项目。

## 插件类型

> [accordion] 模型
>
> 将 AI 模型打包并作为插件进行管理
>
> [了解更多](../%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%E4%B8%8E%E7%A4%BA%E4%BE%8B/%E6%8C%89%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E6%A8%A1%E5%9E%8B%E4%BE%9B%E5%BA%94%E5%95%86%E6%8F%92%E4%BB%B6.md)

> [accordion] 工具
>
> 为 Agent 和工作流构建专业功能
>
> [了解更多](../%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%E4%B8%8E%E7%A4%BA%E4%BE%8B/%E6%8C%89%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E5%B7%A5%E5%85%B7%E6%8F%92%E4%BB%B6.md)

> [accordion] Agent 策略
>
> 为自主 Agent 创建自定义推理策略
>
> [了解更多](../%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%E4%B8%8E%E7%A4%BA%E4%BE%8B/%E6%8C%89%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/Agent%20%E7%AD%96%E7%95%A5%E6%8F%92%E4%BB%B6.md)

> [accordion] 扩展
>
> 通过 HTTP Webhook 实现与外部服务的集成
>
> [了解更多](../%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%E4%B8%8E%E7%A4%BA%E4%BE%8B/%E6%8C%89%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/Endpoint%20%E6%8F%92%E4%BB%B6.md)

> [accordion] 数据源
>
> 将外部内容导入 Dify 的知识流水线
>
> [了解更多](../%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%E4%B8%8E%E7%A4%BA%E4%BE%8B/%E6%8C%89%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E6%95%B0%E6%8D%AE%E6%BA%90%E6%8F%92%E4%BB%B6.md)

> [accordion] 触发器
>
> 通过 Webhook 接收第三方平台事件，以此启动工作流
>
> [了解更多](../%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97%E4%B8%8E%E7%A4%BA%E4%BE%8B/%E6%8C%89%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E8%A7%A6%E5%8F%91%E5%99%A8%E6%8F%92%E4%BB%B6.md)

## 其他资源

> [card] [开发与调试](../%E7%89%B9%E6%80%A7%E4%B8%8E%E8%A7%84%E8%8C%83/%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E6%8F%92%E4%BB%B6%E8%B0%83%E8%AF%95.md)
>
> 高效插件开发的工具和技术

> [card] [发布与 Marketplace](../%E5%8F%91%E5%B8%83/%E5%8F%91%E5%B8%83%E6%8F%92%E4%BB%B6.md)
>
> 打包并与 Dify 社区分享你的插件

> [card] [API 与 SDK 参考](../%E7%89%B9%E6%80%A7%E4%B8%8E%E8%A7%84%E8%8C%83/%E6%8F%92%E4%BB%B6%E7%B1%BB%E5%9E%8B/%E9%80%9A%E7%94%A8%E8%A7%84%E8%8C%83.md)
>
> 技术规范和文档

> [card] [社区与贡献](../%E5%8F%91%E5%B8%83/%E6%A0%87%E5%87%86/%E6%8F%92%E4%BB%B6%E5%BC%80%E5%8F%91%E6%8C%87%E5%8D%97.md)
>
> 与其他开发者交流并为生态系统做出贡献
