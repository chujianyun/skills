# MCP

> **Note: 简介**
>
> MCP（Model Context Protocol，模型上下文协议）用于将外部工具和服务接入 WorkBuddy，让 AI 获得发送通知、连接业务系统、访问数据源等扩展能力。

## 一、什么是 MCP

MCP 可以理解为 AI 的"USB 接口"——就像电脑通过 USB 连接外设一样，MCP 让 AI 连接各种外部工具和数据源。

WorkBuddy 已将 MCP 配置集成到界面中，**无需编码、无需手动改配置文件，可视化操作即可完成接入。**

### 核心价值

| 能力 | 说明 |
| --- | --- |
| **上下文共享** | 向模型提供文件内容、数据库记录、业务信息等上下文 |
| **工具调用** | 将文件读写、接口调用、消息发送等能力暴露给模型 |
| **可组合工作流** | 多个工具和服务通过 MCP 串联，组成自动化流程 |
| **数据控制** | 支持本地或受控方式运行，兼顾灵活性与安全性 |

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image-23.C1CuxqTr.png)

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image-24.CRT6MAV3.png)

## 二、MCP 市场

WorkBuddy 提供现成的 MCP 资源入口，可访问 [腾讯云 MCP 市场](https://cloud.tencent.com/developer/mcp) 获取更多开放生态能力。

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image-25.BYKwTF69.png)

## 三、配置方式

WorkBuddy 支持两种配置级别：

| 级别 | 适用场景 | 配置文件路径 |
| --- | --- | --- |
| **用户级** | 配置一次，所有项目复用 | `~/.workbuddy/mcp.json` |
| **项目级** | 仅当前项目生效，互不影响 | `<项目目录>/.workbuddy/mcp.json` |

> **Note: 如何选择？**
>
> 频繁跨项目使用的能力（如企微机器人通知）→ **用户级**；
>
>
> 仅特定项目需要的专属服务 → **项目级**。

## 四、快速上手：接入企微机器人

以企业微信机器人（WeCom Bot）为例，演示完整接入流程。

### 1）获取 WebHook URL

在企业微信群中：**添加群机器人** → 获取 WebHook URL。

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image-26.DmbHXPBZ.png)

### 2）打开 MCP 配置入口

进入侧边栏 **插件** → 点击右上角 **MCP 服务器** → **配置 MCP**。

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image-27.xMc_K6u2.png)

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image-28.Bh--Bb68.png)

### 3）填写 mcp.json

将以下配置粘贴到编辑器中，替换 `your-webhook-url` 为实际地址后保存：

json

```
{
  "mcpServers": {
    "wecom": {
      "command": "uvx",
      "args": ["wecom-bot-mcp-server"],
      "env": {
        "WECOM_WEBHOOK_URL": "your-webhook-url"
      }
    }
  }
}
```

>
> 示例地址：`https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx`

### 4）确认配置状态

保存后在界面中查看 MCP Server 状态：

| 状态 | 含义 |
| --- | --- |
| 🟢 绿色 | 连接成功，可正常使用 |
| 🔴 红色 | 配置异常，需检查配置内容、命令环境或地址 |

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image-29.Cvi-1ZCn.png)

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image-30.DZX5g0qP.png)

## 五、使用方式

配置完成后，用自然语言描述需求即可，WorkBuddy 会自动调用对应的 MCP Server。

**示例指令：**

>
> 请通过企业微信机器人通知：正式产品已发布，请 @xxxx 进行验收。

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image-31.C4zMTSsc.png)

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image-32.BR5VYjZa.png)

## 六、适用场景

| 场景 | 说明 |
| --- | --- |
| **发布通知** | 版本上线后自动通知项目群相关人员 |
| **任务提醒** | 将待办、验收、协作事项同步到企微群 |
| **流程打通** | 连接 WorkBuddy 任务处理与外部平台 |
| **能力扩展** | 通过更多 MCP Server 调用丰富的外部服务 |

## 七、最佳实践

> **Tip: 配置建议**
>
> - **公共能力配用户级** ：通知类能力配置一次，多项目复用
> - **专属接入配项目级** ：独立配置，避免互相影响
> - **从成熟示例起步** ：先接入 WeCom Bot 等路径清晰的 MCP Server
> - **描述尽量明确** ：说清通知对象、内容、是否需要 @，调用效果更稳定

> **Warning: 安全提示**
>
> - **妥善保管 WebHook URL** ——它是机器人调用凭证，切勿泄露
> - **检查 JSON 格式** ——配置失败时优先确认括号、引号是否完整
> - **关注状态指示灯** ——绿色可用，红色需排查
