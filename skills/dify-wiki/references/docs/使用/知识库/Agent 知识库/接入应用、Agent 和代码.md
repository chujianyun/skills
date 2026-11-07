# 接入应用、Agent 和代码

> Agent 知识库可在哪些地方使用，以及如何分别关闭各类访问

> 本文档由 AI 自动翻译。如有任何不准确之处，请参考 [英文原版](https://docs.dify.ai/en/cloud/use-dify/knowledge-base/use-knowledge-in-apps.md)。

一个 [Agent 知识库](Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93.md) 可同时供多个应用使用。需要基于它作答的工作流、Agent 或程序都可以接入；你本机上的编码 Agent 也能通过 Dify CLI 读取其中的文档。

> [!NOTE]
>
> 聊天助手、旧版 Agent 和文本生成应用无法检索 Agent 知识库。如需让应用基于 Agent 知识库作答，可改用 Chatflow 应用或 Agent 重新搭建。

## 在 Workflow 和 Chatflow 应用中使用

添加一个 [Agent 知识检索](../../%E7%BC%96%E6%8E%92/Workflow%20%E4%B8%8E%20Chatflow/%E8%8A%82%E7%82%B9/Agent%20%E7%9F%A5%E8%AF%86%E6%A3%80%E7%B4%A2.md) 节点，再选择它要检索的知识库。你没有查看权限的知识库不会出现在选择列表中。

如需只检索部分文档，可在节点中 [按元数据过滤](../../%E7%BC%96%E6%8E%92/Workflow%20%E4%B8%8E%20Chatflow/%E8%8A%82%E7%82%B9/Agent%20%E7%9F%A5%E8%AF%86%E6%A3%80%E7%B4%A2.md#filter-by-metadata)。

如需禁止所有工作流检索该知识库（包括测试运行），在知识库的 **设置** 中关闭 **工作流访问**。已在使用它的工作流会在该节点处运行失败，直到你重新开启。

## 在新 Agent 中使用

在 [Agent](../../%E7%BC%96%E6%8E%92/Agent/Agent.md) 的 **配置** 编辑器中，把知识库添加到 **[Agent 知识库](../../%E7%BC%96%E6%8E%92/Agent/%E6%9E%84%E5%BB%BA%20Agent.md#agent-knowledge-base)** 下。

Agent 会根据知识库的名称和描述，自行判断何时检索，并且始终使用「快速」检索深度。

如需禁止已发布的 Agent 检索该知识库，在知识库的 **设置** 中关闭 **API 访问**。使用它的 Agent 仍会照常运行，只是无法再检索它。这个开关同时控制服务 API，关闭后服务 API 也无法访问。

## 在自己的代码中调用

通过 [服务 API](../../../%E5%BC%80%E5%8F%91%E8%80%85%E8%B5%84%E6%BA%90/API/%E6%8C%87%E5%8D%97/API%20%E6%A6%82%E8%A7%88/%E7%9F%A5%E8%AF%86%E5%BA%93/Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93%20API.md)，你的代码可向知识库提问，在后台运行耗时更长的「研究」检索，还能维护其中的文档。

如需阻止 API 调用方访问，在知识库的 **设置** 中关闭 **API 访问**。[Agent](../../%E7%BC%96%E6%8E%92/Agent/Agent.md) 也会随之失去访问权限。

## 供编码 Agent 读取

你本机上的编码 Agent（例如 Claude Code 或 Codex）可在工作时把知识库当作参考资料。借助 Dify CLI，它能像翻看文件夹里的文件一样浏览文档、阅读内容，并按原词精确搜索。

它无法修改知识库中的任何内容。如需像应用那样按语义检索，可使用 [服务 API](%E6%8E%A5%E5%85%A5%E5%BA%94%E7%94%A8%E3%80%81Agent%20%E5%92%8C%E4%BB%A3%E7%A0%81.md#在自己的代码中调用)。

按 CLI 文档中的 [快速开始](../../../%E5%BC%80%E5%8F%91%E8%80%85%E8%B5%84%E6%BA%90/CLI/%E5%BF%AB%E9%80%9F%E5%BC%80%E5%A7%8B.md) 完成配置：安装 `difyctl`，用你的 Dify 账号登录，再用 `difyctl` Skill 配置你的编码 Agent。

之后直接告诉编码 Agent 你要做什么，并附上两项信息：

* `difyctl knowledge_fs`，即要使用的命令。`difyctl` Skill 并未涵盖这组命令。
* 知识库的 ID。在 Dify 中打开该知识库，从浏览器地址栏复制：它是 `/datasets/new/` 与其后第一个 `/` 之间的那一段。

例如：

```text wrap theme={null}
用 difyctl knowledge_fs 读取 Dify 知识库 5b9e2c71-0d4a-4f3e-9a6b-2c8d1e7f4a30 中的 API 设计规范，再对照这些规范检查我对接口的改动。
```

只要你在 Dify 中能查看某个 Agent 知识库，编码 Agent 就能打开它。

编码 Agent 只会在你登录时 Dify 中打开的那个工作空间里查找。如果知识库在其他工作空间，先 [将 `difyctl` 切换到该工作空间](https://docs.dify.ai/zh/cli/manage-sign-in#switch-your-workspace)。

## 应用上线之后

同步或重新上传文档后，新版本一完成索引，你的应用、Agent、API 调用方和外部编码 Agent 就会读到它。

在 **概览** 页面留意已停止同步的数据源，以及没有检索到任何内容的问题。各自的处理方法详见 [维护 Agent 知识库](%E7%BB%B4%E6%8A%A4%20Agent%20%E7%9F%A5%E8%AF%86%E5%BA%93.md)。
