> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 基于千问AI平台构建应用

> 千问AI平台提供文本、视觉、语音及图像视频生成的 AI 模型，兼容 OpenAI SDK，支持函数调用与结构化输出，快速构建智能体应用。

{/* 核心改动区域：外层增加卡片容器，并使用垂直居中对齐 */}

<div style={{ padding: "16px 0 48px 0" }}>
  <div style={{display: "flex", flexWrap: "wrap", gap: "2rem", alignItems: "center"}}>
    <div style={{flex: "1 1 280px"}}>
      <h2 style={{marginTop: 0, fontSize: "1.5rem", fontWeight: "600", borderBottom: "none", paddingBottom: 0}}>开发者快速入门</h2>

      <p style={{color: "#4B5563", lineHeight: "1.6", marginTop: "12px", marginBottom: "24px"}}>
        几分钟内完成首次 API 调用。可直接使用任意 OpenAI SDK 或客户端无缝接入。
      </p>

      [开始使用 →](/developer-guides/getting-started/first-api-call)
    </div>

    <div style={{flex: "2 1 420px"}}>
      ```python
      import os
      from openai import OpenAI

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
      )
      completion = client.chat.completions.create(
        model="qwen3.8-max",
        messages=[{"role": "user", "content": "Summarize the benefits of solar energy in three bullet points."}]
      )
      print(completion.choices[0].message.content)
      ```
    </div>
  </div>
</div>

{/* 卡片区域结束 */}

## 模型

推荐使用 **qwen3.7-plus** 兼顾质量与速度。选择旗舰模型 **qwen3.8-max** 应对最复杂的推理和编程任务，或使用 **qwen3.7-flash** 获得更高性价比。所有模型共用同一套 API，只需更改 `model` 参数即可切换。[查看全部模型 →](/developer-guides/getting-started/model-selection)

<CardGroup cols={3}>
  <Card title="qwen3.8-max" icon="Qwen" href="https://www.qianwenai.com/models/qwen3.8-max">
    复杂推理与编程
  </Card>

  <Card title="qwen3.7-plus" icon="Qwen" href="https://www.qianwenai.com/models/qwen3.7-plus">
    质量、速度与成本均衡
  </Card>

  <Card title="qwen3.7-flash" icon="Qwen" href="https://www.qianwenai.com/models/qwen3.7-flash">
    快速且高性价比
  </Card>
</CardGroup>

## 开始构建

<CardGroup cols={2}>
  <Card title="文本读取与生成" icon="TextResizeOutlined" href="/developer-guides/text-generation/quickstart">
    使用模型生成文本、摘要、翻译或编写代码
  </Card>

  <Card title="图像与视频理解" icon="ImageInPictureOutlined" href="/developer-guides/multimodal/vision">
    分析图像、从截图中提取文字，或根据设计稿还原页面
  </Card>

  <Card title="图像生成" icon="BrushOutlined" href="/developer-guides/image-generation/text-to-image">
    使用 Wan 和 Qwen 模型，通过文本提示词创建和编辑图像
  </Card>

  <Card title="视频生成" icon="VideoOutlined" href="/developer-guides/video-generation/text-to-video">
    将图像转化为视频片段，或根据文本描述生成视频
  </Card>

  <Card title="语音合成" icon="MicrophoneOutlined" href="/developer-guides/speech/tts-models">
    将文本转换为自然语音，支持内置音色、音色克隆和音色设计
  </Card>

  <Card title="构建智能体应用" icon="ToolOutlined" href="/developer-guides/tool-calling/function-calling">
    通过函数调用将模型连接到外部工具和 API
  </Card>

  <Card title="通过推理解决复杂问题" icon="BulbOutlined" href="/developer-guides/text-generation/thinking">
    使用推理模型解决多步数学、逻辑和编程问题
  </Card>

  <Card title="结构化数据输出" icon="CodeOutlined" href="/developer-guides/text-generation/structured-output">
    从模型响应中提取符合指定 Schema 的 JSON 数据
  </Card>
</CardGroup>

---

[定价](/developer-guides/getting-started/pricing) | [API 参考](/api-reference/preparation/api-key) | [免费额度](/resources/free-quota)
