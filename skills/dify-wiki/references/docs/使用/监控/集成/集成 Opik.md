# 集成 Opik

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/cloud/use-dify/monitor/integrations/integrate-opik.md)。

## Opik 简介

Opik 是一个开源的 LLM 评估平台，用于评估、测试和监控大型语言模型（LLM）应用。它由 Comet 开发，旨在促进对基于 LLM 的应用进行更直观的协作、测试和监控。

> [!NOTE]
>
> 如需了解更多详情，请参考 [Opik](https://www.comet.com/site/products/opik/)。

***

## 开始配置 Opik

### 1. 注册/登录 [Opik](https://www.comet.com/signup?from=llm)

### 2. 获取 Opik API 密钥

从右上角的用户菜单中获取 Opik API 密钥。点击 **API Key**，然后点击 API Key 进行复制：

![](../../../../assets/images/6f8e514e92c5f58ce901743c.png)

### 3. 集成 Opik 与 Dify

在 Dify 应用中配置 Opik。打开需要监控的应用，在侧边菜单中打开 **监控**，并在页面上选择 **追踪应用性能**。

![](../../../../assets/images/c491684541adf4812c8fa596.png)

点击配置后，将在 Opik 中创建的 **API Key** 和 **项目名称**粘贴到配置中并保存。

![](../../../../assets/images/4a9592b7b250799495c018bf.png)

成功保存后，你可以在当前页面查看监控状态。

## 查看监控数据

配置完成后，你可以照常调试或使用 Dify 应用。所有使用历史都可以在 Opik 中监控。

![](../../../../assets/images/ff0e8ad0febff6d8dd0fad8d.png)

当你切换到 Opik 时，可以在仪表板中查看 Dify 应用的详细操作日志。

![](../../../../assets/images/1a5990a6ea5dcff7893138bc.png)

通过 Opik 的详细 LLM 操作日志将帮助你优化 Dify 应用的性能。

![](../../../../assets/images/b22de67cb637c8830be6053a.png)

## 监控数据列表

### **Workflow/Chatflow 追踪信息**

**用于追踪 Workflow 和 Chatflow**

| 工作流 | Opik 追踪 |
| - | - |
| workflow\_app\_log\_id/workflow\_run\_id | id |
| user\_session\_id | - 放置在元数据中 |
| `workflow_{id}` | name |
| start\_time | start\_time |
| end\_time | end\_time |
| inputs | inputs |
| outputs | outputs |
| Model token consumption | usage\_metadata |
| metadata | metadata |
| error | error |
| \[workflow] | tags |
| conversation\_id/none for workflow | conversation\_id in metadata |

**工作流追踪信息**

* workflow\_id - 工作流唯一标识符
* conversation\_id - 对话 ID
* workflow\_run\_id - 当前运行的 ID
* tenant\_id - 租户 ID
* elapsed\_time - 当前运行所用时间
* status - 运行状态
* version - 工作流版本
* total\_tokens - 当前运行使用的总令牌数
* file\_list - 处理的文件列表
* triggered\_from - 触发当前运行的来源
* workflow\_run\_inputs - 当前运行的输入数据
* workflow\_run\_outputs - 当前运行的输出数据
* error - 当前运行期间遇到的错误
* query - 运行期间使用的查询
* workflow\_app\_log\_id - Workflow 应用日志 ID
* message\_id - 关联的消息 ID
* start\_time - 运行开始时间
* end\_time - 运行结束时间
* workflow node executions - 工作流节点执行信息
* 元数据
  * workflow\_id - 工作流唯一标识符
  * conversation\_id - 对话 ID
  * workflow\_run\_id - 当前运行的 ID
  * tenant\_id - 租户 ID
  * elapsed\_time - 当前运行所用时间
  * status - 运行状态
  * version - 工作流版本
  * total\_tokens - 当前运行使用的总令牌数
  * file\_list - 处理的文件列表
  * triggered\_from - 触发当前运行的来源

#### **消息追踪信息**

**用于追踪 LLM 相关对话**

| 聊天 | Opik LLM |
| - | - |
| message\_id | id |
| user\_session\_id | - 放置在元数据中 |
| "llm" | name |
| start\_time | start\_time |
| end\_time | end\_time |
| inputs | inputs |
| outputs | outputs |
| Model token consumption | usage\_metadata |
| metadata | metadata |
| \["message", conversation\_mode] | tags |
| conversation\_id | conversation\_id in metadata |

**消息追踪信息**

* message\_id - 消息 ID
* message\_data - 消息数据
* user\_session\_id - 用户会话 ID
* conversation\_model - 对话模式
* message\_tokens - 消息中的令牌数
* answer\_tokens - 答案中的令牌数
* total\_tokens - 消息和答案中的总令牌数
* error - 错误信息
* inputs - 输入数据
* outputs - 输出数据
* file\_list - 处理的文件列表
* start\_time - 开始时间
* end\_time - 结束时间
* message\_file\_data - 与消息关联的文件数据
* conversation\_mode - 对话模式
* 元数据
  * conversation\_id - 对话 ID
  * ls\_provider - 模型供应商
  * ls\_model\_name - 模型 ID
  * status - 消息状态
  * from\_end\_user\_id - 发送用户的 ID
  * from\_account\_id - 发送账户的 ID
  * agent\_based - 消息是否基于代理
  * workflow\_run\_id - 工作流运行 ID
  * from\_source - 消息来源

#### **审核追踪信息**

**用于追踪对话审核**

| 审核 | Opik Tool |
| - | - |
| user\_id | - 放置在元数据中 |
| "moderation" | name |
| start\_time | start\_time |
| end\_time | end\_time |
| inputs | inputs |
| outputs | outputs |
| metadata | metadata |
| \["moderation"] | tags |

**审核追踪信息**

* message\_id - 消息 ID
* user\_id - 用户 ID
* workflow\_app\_log\_id - Workflow 应用日志 ID
* inputs - 审核输入数据
* message\_data - 消息数据
* flagged - 内容是否被标记需要注意
* action - 采取的具体行动
* preset\_response - 预设响应
* start\_time - 审核开始时间
* end\_time - 审核结束时间
* 元数据
  * message\_id - 消息 ID
  * action - 采取的具体行动
  * preset\_response - 预设响应

#### **建议问题追踪信息**

**用于追踪建议问题**

| 建议问题 | Opik LLM |
| - | - |
| user\_id | - 放置在元数据中 |
| "suggested\_question" | name |
| start\_time | start\_time |
| end\_time | end\_time |
| inputs | inputs |
| outputs | outputs |
| metadata | metadata |
| \["suggested\_question"] | tags |

**消息追踪信息**

* message\_id - 消息 ID
* message\_data - 消息数据
* inputs - 输入内容
* outputs - 输出内容
* start\_time - 开始时间
* end\_time - 结束时间
* total\_tokens - 令牌数量
* status - 消息状态
* error - 错误信息
* from\_account\_id - 发送账户的 ID
* agent\_based - 是否基于代理
* from\_source - 消息来源
* model\_provider - 模型供应商
* model\_id - 模型 ID
* suggested\_question - 建议问题
* level - 状态级别
* status\_message - 状态消息
* 元数据
  * message\_id - 消息 ID
  * ls\_provider - 模型供应商
  * ls\_model\_name - 模型 ID
  * status - 消息状态
  * from\_end\_user\_id - 发送用户的 ID
  * from\_account\_id - 发送账户的 ID
  * workflow\_run\_id - 工作流运行 ID
  * from\_source - 消息来源

#### **数据集检索追踪信息**

**用于追踪知识库检索**

| 数据集检索 | Opik Retriever |
| - | - |
| user\_id | - 放置在元数据中 |
| "dataset\_retrieval" | name |
| start\_time | start\_time |
| end\_time | end\_time |
| inputs | inputs |
| outputs | outputs |
| metadata | metadata |
| \["dataset\_retrieval"] | tags |
| message\_id | parent\_run\_id |

**数据集检索追踪信息**

* message\_id - 消息 ID
* inputs - 输入内容
* documents - 文档数据
* start\_time - 开始时间
* end\_time - 结束时间
* message\_data - 消息数据
* 元数据
  * message\_id - 消息 ID
  * ls\_provider - 模型供应商
  * ls\_model\_name - 模型 ID
  * status - 消息状态
  * from\_end\_user\_id - 发送用户的 ID
  * from\_account\_id - 发送账户的 ID
  * agent\_based - 是否基于代理
  * workflow\_run\_id - 工作流运行 ID
  * from\_source - 消息来源

#### **工具追踪信息**

**用于追踪工具调用**

| 工具 | Opik Tool |
| - | - |
| user\_id | - 放置在元数据中 |
| tool\_name | name |
| start\_time | start\_time |
| end\_time | end\_time |
| inputs | inputs |
| outputs | outputs |
| metadata | metadata |
| \["tool", tool\_name] | tags |

#### **工具追踪信息**

* message\_id - 消息 ID
* tool\_name - 工具名称
* start\_time - 开始时间
* end\_time - 结束时间
* tool\_inputs - 工具输入
* tool\_outputs - 工具输出
* message\_data - 消息数据
* error - 错误信息（如果有）
* inputs - 消息的输入
* outputs - 消息的输出
* tool\_config - 工具配置
* time\_cost - 时间消耗
* tool\_parameters - 工具参数
* file\_url - 关联文件的 URL
* 元数据
  * message\_id - 消息 ID
  * tool\_name - 工具名称
  * tool\_inputs - 工具输入
  * tool\_outputs - 工具输出
  * tool\_config - 工具配置
  * time\_cost - 时间消耗
  * error - 错误信息（如果有）
  * tool\_parameters - 工具参数
  * message\_file\_id - 消息文件 ID
  * created\_by\_role - 创建者角色
  * created\_user\_id - 创建者用户 ID

#### **生成名称追踪信息**

**用于追踪对话标题生成**

| 生成名称 | Opik Tool |
| - | - |
| user\_id | - 放置在元数据中 |
| "generate\_conversation\_name" | name |
| start\_time | start\_time |
| end\_time | end\_time |
| inputs | inputs |
| outputs | outputs |
| metadata | metadata |
| \["generate\_name"] | tags |

**生成名称追踪信息**

* conversation\_id - 对话 ID
* inputs - 输入数据
* outputs - 生成的对话名称
* start\_time - 开始时间
* end\_time - 结束时间
* tenant\_id - 租户 ID
* 元数据
  * conversation\_id - 对话 ID
  * tenant\_id - 租户 ID
