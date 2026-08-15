> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 首次调用千问API

> 本文引导您完成千问模型的首次API调用

<Tip>千问AI平台提供新人免费额度。详见[免费额度](/resources/free-quota)。</Tip>

完成本指南后，您将能用Python、Node.js或其他语言发起真实请求。如果您已在使用OpenAI SDK，无需重新学习——只需将 `base_url` 指向千问AI平台、替换API Key，即可复用现有代码。

<Note>
  - 若您熟悉大模型调用，可直接查看[API参考文档](/api-reference/chat/openai-chat)。
  - 若您不熟悉编程，可参考[模型体验](https://platform.qianwenai.com/home/try-ai)，通过图形化界面与千问模型对话。
  - API调用与操作系统版本无关，只要网络能连通即可正常使用。
</Note>

本文以千问为例，引导您完成大模型API调用。按照以下步骤操作：

- 步骤一：创建账号并获取API Key
- 步骤二：配置API Key到环境变量
- 步骤三：调用千问API

## 步骤一：创建账号并获取API Key

<Steps>
  <Step title="登录千问AI平台">
    访问 [千问AI平台](https://platform.qianwenai.com/)，使用手机号、账号密码或支付宝扫码登录。
  </Step>

  <Step title="获取 API Key">
    进入 [**API Key**](https://platform.qianwenai.com/home/api-keys) 页面，点击**创建 API Key**，复制生成的 Key（以 `sk-ws-` 开头）。[详细说明 →](/api-reference/preparation/api-key)

    <Warning>
      请妥善保管 API Key，不要提交到代码仓库或公开分享。
    </Warning>
  </Step>
</Steps>

## 步骤二：配置API Key到环境变量

建议将API Key配置到环境变量，而不是直接写在代码里，以降低泄露风险。

<CodeGroup>
  ```bash macOS/Linux
  export DASHSCOPE_API_KEY="REDACTED"
  ```

  ```powershell Windows PowerShell
  $env:DASHSCOPE_API_KEY = "REDACTED"
  ```
</CodeGroup>

如需跨会话持久化配置，参见 [配置 API Key →](/api-reference/preparation/export-api-key-env)。

## 步骤三：调用千问API

选择您熟悉的语言或工具。千问AI平台兼容OpenAI SDK——如果您已安装，只需更新 `base_url` 和API Key即可直接使用。

<Tabs>
  <Tab title="Python">
    安装 OpenAI SDK：

    ```bash
    pip install openai
    ```

    创建文件 `hello_qwen.py`：

    ```python
    import os
    from openai import OpenAI

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
      model="qwen3.8-max",
      messages=[
        {"role": "user", "content": "Hello! Tell me a fun fact about AI."}
      ]
    )

    print(completion.choices[0].message.content)
    ```

    运行：

    ```bash
    python hello_qwen.py
    ```
  </Tab>

  <Tab title="Node.js">
    安装 OpenAI SDK：

    ```bash
    npm install openai
    ```

    创建文件 `hello_qwen.mjs`：

    ```javascript
    import OpenAI from "openai";

    const openai = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    });

    const completion = await openai.chat.completions.create({
      model: "qwen3.8-max",
      messages: [
        { role: "user", content: "Hello! Tell me a fun fact about AI." }
      ]
    });

    console.log(completion.choices[0].message.content);
    ```

    运行：

    ```bash
    node hello_qwen.mjs
    ```
  </Tab>

  <Tab title="curl">
    <CodeGroup>
      ```bash macOS/Linux
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "qwen3.8-max",
          "messages": [
            {
              "role": "user",
              "content": "Hello! Tell me a fun fact about AI."
            }
          ]
        }'
      ```

      ```powershell Windows PowerShell
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions `
        -H "Authorization: Bearer $env:DASHSCOPE_API_KEY" `
        -H "Content-Type: application/json" `
        -d '{
          \"model\": \"qwen3.8-max\",
          \"messages\": [
            {
              \"role\": \"user\",
              \"content\": \"Hello! Tell me a fun fact about AI.\"
            }
          ]
        }'
      ```
    </CodeGroup>
  </Tab>
</Tabs>

<Tip>
  Java、Go、PHP、C# 等语言可直接使用 curl 标签页中的 OpenAI 兼容端点，配合各语言的 HTTP 客户端调用。Java 也可使用 [DashScope Java SDK](/api-reference/preparation/install-sdk)。
</Tip>

<Note>
  在[模型市场](https://www.qianwenai.com/models)中，推理服务商为千问AI平台的模型无需手动开通，获取 API Key 后即可直接调用（部分邀测模型除外）。其他推理服务商（如硅基流动）的直供模型，需要先在模型市场开通后才能调用。
</Note>

## 下一步

- [文本生成指南](/developer-guides/text-generation/quickstart) — 流式输出、函数调用等进阶用法
- [视觉模型](/developer-guides/multimodal/vision) — 图片和视频分析
- [模型选择](/developer-guides/getting-started/model-selection) — 选择适合场景的模型
- [模型体验](https://platform.qianwenai.com/home/try-ai) — 在线试用模型
