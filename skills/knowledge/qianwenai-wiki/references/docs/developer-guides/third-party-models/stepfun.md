> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Stepfun-阶跃星辰

> 本文档介绍如何在千问AI平台调用阶跃星辰（Stepfun）直供的 Step 系列模型推理服务。

## 快速开始

stepfun/step-3.7-flash 是阶跃星辰直供的多模态推理模型，**默认关闭思考模式**，您可以通过设置`enable_thinking`为`true`开启思考模式。开启后，模型的推理过程通过`reasoning_content`字段返回，您可以通过`reasoning_effort`参数（可选值：`low`、`medium`、`high`）控制推理深度。运行以下代码快速调用 stepfun/step-3.7-flash 模型。

需要已获取 API Key 并完成配置 API Key 到环境变量。如果通过 SDK 调用，需要安装 SDK。

<Tabs>
  <Tab title="Python">
    ```python
    from openai import OpenAI
    import os
    # 初始化OpenAI客户端
    client = OpenAI(
      # 如果没有配置环境变量，请用千问AI平台API Key替换：api_key="sk-xxx"
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    messages = [{"role": "user", "content": "9.9和9.11哪个大？"}]
    completion = client.chat.completions.create(
      model="stepfun/step-3.7-flash",
      messages=messages,
      stream=True,
      stream_options={
        "include_usage": True
      },
      extra_body={
        "enable_thinking": True
      }
    )
    reasoning_content = ""  # 完整思考过程
    answer_content = ""  # 完整回复
    is_answering = False  # 是否进入回复阶段
    print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
    for chunk in completion:
      if not chunk.choices:
        print("\n" + "=" * 20 + "Token 消耗" + "=" * 20 + "\n")
        print(chunk.usage)
        continue
      delta = chunk.choices[0].delta
      # 只收集思考内容
      if hasattr(delta, "reasoning_content") and delta.reasoning_content is not None:
        if not is_answering:
          print(delta.reasoning_content, end="", flush=True)
        reasoning_content += delta.reasoning_content
      # 收到content，开始进行回复
      if hasattr(delta, "content") and delta.content:
        if not is_answering:
          print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
          is_answering = True
        print(delta.content, end="", flush=True)
        answer_content += delta.content
    ```

    **返回结果**

    ```text
    ====================思考过程====================
    好的，用户问的是9.9和9.11哪个大。首先我需要比较这两个小数。
    9.9可以写成9.90，而9.11就是9.11。
    比较小数部分：90 > 11，所以9.9 > 9.11。
    ====================完整回复====================
    9.9 更大。
    将两个数对齐小数位：9.9 = 9.90，而 9.11 = 9.11。比较小数部分，0.90 > 0.11，因此 **9.9 > 9.11**。
    ====================Token 消耗====================
    CompletionUsage(completion_tokens=85, prompt_tokens=10, total_tokens=95, prompt_tokens_details={'cached_tokens': 0})
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";
    import process from 'process';
    // 初始化OpenAI客户端
    const openai = new OpenAI({
      // 如果没有配置环境变量，请用千问AI平台API Key替换：apiKey: "sk-xxx"
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    });
    let reasoningContent = ''; // 完整思考过程
    let answerContent = ''; // 完整回复
    let isAnswering = false; // 是否进入回复阶段
    async function main() {
      try {
        const messages = [{ role: 'user', content: '9.9和9.11哪个大？' }];
        const stream = await openai.chat.completions.create({
          model: 'stepfun/step-3.7-flash',
          messages,
          stream: true,
          stream_options: {
            include_usage: true
          },
          enable_thinking: true
        });
        console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');
        for await (const chunk of stream) {
          if (!chunk.choices?.length) {
            console.log('\n' + '='.repeat(20) + 'Token 消耗' + '='.repeat(20) + '\n');
            console.log(chunk.usage);
            continue;
          }
          const delta = chunk.choices[0].delta;
          // 只收集思考内容
          if (delta.reasoning_content !== undefined && delta.reasoning_content !== null) {
            if (!isAnswering) {
              process.stdout.write(delta.reasoning_content);
            }
            reasoningContent += delta.reasoning_content;
          }
          // 收到content，开始进行回复
          if (delta.content !== undefined && delta.content) {
            if (!isAnswering) {
              console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
              isAnswering = true;
            }
            process.stdout.write(delta.content);
            answerContent += delta.content;
          }
        }
      } catch (error) {
        console.error('Error:', error);
      }
    }
    main();
    ```

    **返回结果**

    ```text
    ====================思考过程====================
    好的，用户问的是9.9和9.11哪个大。首先我需要比较这两个小数。
    9.9可以写成9.90，而9.11就是9.11。
    比较小数部分：90 > 11，所以9.9 > 9.11。
    ====================完整回复====================
    9.9 更大。
    将两个数对齐小数位：9.9 = 9.90，而 9.11 = 9.11。比较小数部分，0.90 > 0.11，因此 **9.9 > 9.11**。
    ====================Token 消耗====================
    { prompt_tokens: 10, completion_tokens: 85, total_tokens: 95, prompt_tokens_details: { cached_tokens: 0 } }
    ```
  </Tab>

  <Tab title="HTTP">
    ```bash
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "stepfun/step-3.7-flash",
        "messages": [
            {
                "role": "user",
                "content": "9.9和9.11哪个大？"
            }
        ],
        "stream": true,
        "stream_options": {
            "include_usage": true
        },
        "enable_thinking": true
    }'
    ```
  </Tab>
</Tabs>

## 多模态调用示例

stepfun/step-3.7-flash 不仅支持纯文本对话，还具备多模态理解能力，支持图像和视频输入。

### 图像理解

图像理解功能让模型能够识别和分析图像内容。支持通过公网 URL 或 Base64 编码传入图像。图像文件的限制请参见[文件限制](#文件限制)。

<Tabs>
  <Tab title="Python">
    ```python
    import os
    from openai import OpenAI
    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
      model="stepfun/step-3.7-flash",
      messages=[
        {
          "role": "user",
          "content": [
            {"type": "text", "text": "图中描绘的是什么景象?"},
            {
              "type": "image_url",
              "image_url": {
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg",
                "detail": "high"
              }
            }
          ]
        }
      ]
    )
    # 输出思考过程
    if hasattr(completion.choices[0].message, 'reasoning_content') and completion.choices[0].message.reasoning_content:
      print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
      print(completion.choices[0].message.reasoning_content)
    # 输出回复内容
    print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
    print(completion.choices[0].message.content)
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";
    import process from 'process';
    const openai = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
    });
    const completion = await openai.chat.completions.create({
      model: 'stepfun/step-3.7-flash',
      messages: [
        {
          role: 'user',
          content: [
            { type: 'text', text: '图中描绘的是什么景象?' },
            {
              type: 'image_url',
              image_url: {
                url: 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg',
                detail: 'high'
              }
            }
          ]
        }
      ]
    });
    // 输出思考过程
    if (completion.choices[0].message.reasoning_content) {
      console.log('\n' + '='.repeat(20) + '思考过程' + '='.repeat(20) + '\n');
      console.log(completion.choices[0].message.reasoning_content);
    }
    // 输出回复内容
    console.log('\n' + '='.repeat(20) + '完整回复' + '='.repeat(20) + '\n');
    console.log(completion.choices[0].message.content);
    ```
  </Tab>

  <Tab title="HTTP">
    ```bash
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
        "model": "stepfun/step-3.7-flash",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "图中描绘的是什么景象?"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg",
                            "detail": "high"
                        }
                    }
                ]
            }
        ]
    }'
    ```
  </Tab>
</Tabs>

### 视频理解

视频理解功能让模型能够识别和分析视频内容。支持通过公网 URL 传入视频。视频文件的限制请参见[文件限制](#文件限制)。

<Tabs>
  <Tab title="Python">
    ```python
    import os
    from openai import OpenAI
    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    completion = client.chat.completions.create(
      model="stepfun/step-3.7-flash",
      messages=[
        {
          "role": "user",
          "content": [
            {
              "type": "video_url",
              "video_url": {
                "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
              }
            },
            {
              "type": "text",
              "text": "这段视频的内容是什么?"
            }
          ]
        }
      ]
    )
    print(completion.choices[0].message.content)
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";
    const openai = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    });
    async function main() {
      const response = await openai.chat.completions.create({
        model: "stepfun/step-3.7-flash",
        messages: [
          {
            role: "user",
            content: [
              {
                type: "video_url",
                video_url: {
                  url: "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                }
              },
              {
                type: "text",
                text: "这段视频的内容是什么?"
              }
            ]
          }
        ]
      });
      console.log(response.choices[0].message.content);
    }
    main();
    ```
  </Tab>

  <Tab title="HTTP">
    ```bash
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
        "model": "stepfun/step-3.7-flash",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "video_url",
                        "video_url": {
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                        }
                    },
                    {
                        "type": "text",
                        "text": "这段视频的内容是什么?"
                    }
                ]
            }
        ]
    }'
    ```
  </Tab>
</Tabs>

### 文件限制

<Tabs>
  <Tab title="图像文件">
    - \*\*支持的图像格式：\*\*JPG/JPEG、PNG、WEBP、静态 GIF
    - \*\*单张图像大小：\*\*不超过 10M
    - \*\*多图输入限制：\*\*单次请求最多 50 张图像，多张图片总大小不超过 20M
    - \*\*图像分辨率：\*\*建议长或宽不超过 4096 像素。分辨率越高，模型推理成本越高（网络传输时间、首字延迟和费用消耗相应增加）
    - \*\*图像传入方式：\*\*支持通过 HTTP/HTTPS 公网 URL 或 Base64 编码传入
  </Tab>

  <Tab title="视频文件">
    - \*\*视频大小：\*\*最大 128M
    - \*\*视频时长：\*\*无时长限制，推荐 5 分钟以内
    - \*\*音频理解：\*\*不支持对视频文件的音频进行理解
  </Tab>
</Tabs>

## 其它功能

| 功能               | 支持情况 | 备注                                                   |
| ---------------- | ---- | ---------------------------------------------------- |
| 多轮对话             | 支持   | 思考模式下需在每轮 assistant 消息中保留`reasoning_content`字段，否则会报错 |
| Function Calling | 支持   | 不支持`tool_choice`参数                                   |
| 上下文缓存            | 支持   | 支持隐式缓存，自动开启                                          |
| 结构化输出            | 支持   | `response_format`不支持 json\_schema                    |
| 联网搜索             | 不支持  | —                                                    |
| 前缀续写             | 不支持  | —                                                    |
| 多模态输入            | 支持   | 支持图像（URL/Base64）和视频（URL）输入                           |

stepfun/step-3.7-flash 不支持以下参数：`tool_choice`、`thinking_budget`、`top_k`、`modalities`、`repetition_penalty`、`vl_high_resolution_images`、`preserve_thinking`、`enable_search`、`search_options`、`seed`、`logprobs`、`top_logprobs`、`n`。

支持的参数中，部分参数取值范围与功能与千问AI平台不一致：

| 参数                  | 千问AI平台                                   | Step                                          |
| ------------------- | ---------------------------------------- | --------------------------------------------- |
| `temperature`       | 取值范围 \[0, 2)                             | 取值范围 \[0, 2)，默认 1.0                           |
| `top_p`             | 取值范围 (0, 1.0]                            | 取值范围 (0, 1.0]，默认 0.95                         |
| `max_tokens`        | 不限制思考模型思维链长度，仅限制输出长度                     | 限制思考过程和最终回答的总体输出长度                            |
| `reasoning_effort`  | 控制 DeepSeek-V4 系列模型的推理力度，可选值`high`/`max` | 可选值为`low`、`medium`、`high`，用于控制推理深度，需开启思考模式后生效 |
| `stream_options`    | 其属性`include_usage`默认为`false`，可设为`true`   | 其属性`include_usage`强制为`true`，无法关闭              |
| `detail`            | 不支持                                      | 可选`low`/`high`，默认`low`                        |
| `frequency_penalty` | 不支持                                      | 范围 0.0\~1.0，默认 0                              |

## 模型列表与计费

Step 系列模型是阶跃星辰直供的多模态推理模型，支持文本、图像和视频输入，支持通过`enable_thinking`开启思考模式。

模型上下文长度与价格信息请参见[千问AI平台控制台](https://www.qianwenai.com/models)。

按照模型的输入与输出 Token 计费。

> 思考模式下，思维链按照输出 Token 计费。

## 错误码

Step 系列模型由阶跃星辰直供，其错误码与千问AI平台标准错误码存在差异。调用 Step 模型时，请以下表为准。

| 错误码         | 错误原因                                          | 解决方法                  |
| ----------- | --------------------------------------------- | --------------------- |
| 400 - 格式错误  | 请求参数格式不正确，可能包括图片无法下载、图片数量超限、模型不支持的输入类型、参数值不合法 | 检查请求体、模型能力和参数范围       |
| 401 - 认证失败  | 缺少或无效的 API Key                                | 检查 API Key 及请求头格式是否正确 |
| 402 - 余额不足  | 账户余额不足                                        | 检查账户余额，及时进行充值         |
| 429 - 请求超限  | 请求过于频繁，超出速率限制                                 | 实现指数退避和重试逻辑，或降低请求频率   |
| 451 - 内容拦截  | 请求内容或响应内容未通过审核                                | 修改请求内容，避免输入不安全或敏感内容   |
| 500 - 服务器失败 | 服务器内部故障                                       | 请稍后重试，持续出现时联系我们解决     |
| 503 - 服务器故障 | 服务器负载过高                                       | 请稍后重试                 |
