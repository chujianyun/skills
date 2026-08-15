> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Dify

> 低代码 LLM 应用平台

Dify 是一个通过可视化工作流构建 LLM 应用的低代码平台。将其连接到千问AI平台的按量付费 API，即可创建由 Qwen 模型驱动的聊天助手、智能体和知识库。

## 快速开始

几分钟即可上手：

```text
# 1. 安装插件
进入 Dify 插件市场 → Models → 搜索 "TONGYI" → 安装

# 2. 配置（Settings → Model Providers → TONGYI → Settings）
API Key: sk-ws-xxx
Use international endpoint: No

# 3. 测试（创建空白应用 → 聊天助手）
选择模型：qwen3.5-plus
输入消息："写一个 Python hello world 程序"
```

预期结果：模型返回 Python 代码

## 配置

### 基本设置

配置 Dify 连接千问AI平台：

- 插件：TONGYI（从 Dify 插件市场安装）
- 使用国际端点：**No**
- 认证方式：需要 API Key
- 模型选择：从插件中选择可用模型

### 详细配置步骤

<Steps>
  <Step title="安装 TONGYI 插件">
    进入 [Dify 插件市场](https://cloud.dify.ai/plugins?category=discover) → **Models** → **TONGYI** → 安装
  </Step>

  <Step title="配置 API Key">
    点击头像 → **Settings** → **Model Providers** → **TONGYI** → **Settings**

    - API Key：您的 [API Key](https://platform.qianwenai.com/home/api-keys)
    - Use international endpoint：**No**
  </Step>

  <Step title="启用模型">
    点击 TONGYI 卡片上的模型列表 → 开启所需模型
  </Step>
</Steps>

<Tip>
  如果 TONGYI 插件中没有最新模型，可使用 **OpenAI-API-compatible** 插件，端点填写 `https://dashscope.aliyuncs.com/compatible-mode/v1`
</Tip>

<Note>
  使用千问AI平台提供的 DeepSeek 模型也请使用 TONGYI 插件。
</Note>

### 限制

- 插件维护：TONGYI 插件由 Dify 维护，而非由千问AI平台维护
- 模型可用性：部分最新模型可能需要通过 OpenAI-compatible 插件接入

## 使用示例

<Tabs>
  <Tab title="聊天助手">
    <Steps>
      <Step title="创建应用">
        工作区 → **Create blank app** → **Chat assistant**
      </Step>

      <Step title="配置模型">
        选择 **qwen3.5-plus** → 如可用，开启思考模式
      </Step>

      <Step title="测试对话">
        输入："解释神经网络的工作原理"
      </Step>
    </Steps>
  </Tab>

  <Tab title="包含 LLM 节点的工作流">
    <Steps>
      <Step title="创建工作流">
        工作区 → 创建 **Chatflow** 或 **Workflow**
      </Step>

      <Step title="添加 LLM 节点">
        将 LLM 节点拖到画布 → 选择 **qwen3.5-plus**
      </Step>

      <Step title="运行节点">
        添加用户消息 → 点击运行按钮
      </Step>
    </Steps>
  </Tab>

  <Tab title="知识库">
    <Steps>
      <Step title="创建知识库">
        进入[知识库](https://cloud.dify.ai/datasets) → 新建
      </Step>

      <Step title="上传文档">
        选择数据来源 → 上传文件
      </Step>

      <Step title="配置 Embedding">
        文本分段时选择 **text-embedding-v4**，Rerank 模型可选 **gte-rerank-v2**
      </Step>
    </Steps>
  </Tab>

  <Tab title="视觉模型">
    <Steps>
      <Step title="选择视觉模型">
        选择 **qwen3.5-plus** 或 **qwen3-vl-plus**
      </Step>

      <Step title="开启视觉功能">
        在聊天或 LLM 节点中开启 **Vision** 开关
      </Step>

      <Step title="上传图片">
        在对话中上传图片进行分析
      </Step>
    </Steps>
  </Tab>
</Tabs>

## 常见问题

**"Invalid API-key provided" 错误**

> 解决方法：
>
> - 尝试安装早期版本的 TONGYI 插件
> - 使用默认工作区（非子工作区）的 API Key。`0.0.41` 版本的千问插件会校验 `qwen-turbo` 模型调用权限，建议使用默认业务空间的 API Key。
> - 确认 "Use international endpoint" 已设为 No

**带 `-latest` 后缀的模型不可用**

> 解决方法：使用 OpenAI-API-compatible 插件，配置如下：
>
> - Endpoint：`https://dashscope.aliyuncs.com/compatible-mode/v1`
> - API key：您的千问AI平台 API Key
> - Model：手动输入模型 ID

**Token 消耗过高**

> 解决方法：
>
> - 根据任务选择合适的模型
> - 设置合理的上下文窗口大小
> - 定期清理对话历史

**Vision 开关未显示**

> 解决方法：确认已选择支持视觉的模型（`qwen3.5-plus` 或 `qwen3-vl-plus`）

**如何使用 Qwen-Omni / Qwen-Audio / Qwen-OCR 模型？**

> 以上模型均不支持直接在 Dify 上配置，您可通过 Chatflow 或工作流的 HTTP 节点接入，接入细节请参见文档中的 curl 命令。为了降低 HTTP 节点的超时风险，建议您通过流式输出方式调用。

**如何使用万相模型？**

> Dify 没有提供万相模型相关的插件，通过 Dify 的 Chatflow/工作流的 HTTP 节点可达到文生图/视频的功能。步骤：
>
> 1. 下载并导入工作流模板（万相-文生图Demo.yml 或 万相-文生视频Demo.yml），在[工作室](https://cloud.dify.ai/apps)点击**导入 DSL 文件**并选择模板。
> 2. 进入工作流界面，将 `DASHSCOPE_API_KEY` 的值修改为您的 API Key。
> 3. 点击**运行**按钮即可生成作品。视频生成时间一般在 5 分钟以上。
> 4. （可选）发布为工具，以便在其他大模型应用中使用。
>
> 模板默认使用 `wanx2.1-t2i-turbo`/`wan2.2-t2i-flash`（文生图）/ `wanx2.1-t2v-turbo`（文生视频）。您可以在 STEP1 节点修改模型。

## 进阶功能

### 思考模式

对于支持推理的模型：

1. 选择支持思考模式的模型
2. 开启思考模式开关
3. 设为 "True" 启用逐步推理

### 代码执行节点

从响应中提取推理过程：

- 在代码执行节点中使用正则表达式
- 将思考过程与最终答案分离
- 按需格式化输出

## 相关资源

- **模型列表**：[可用模型 →](/developer-guides/getting-started/text-generation-models)
- **视觉模型**：[图像理解指南 →](/developer-guides/multimodal/vision)
- **Embeddings**：[文本嵌入模型 →](/developer-guides/embeddings/embedding)
- **API 文档**：[OpenAI-compatible 参考 →](/api-reference/chat/openai-chat)
