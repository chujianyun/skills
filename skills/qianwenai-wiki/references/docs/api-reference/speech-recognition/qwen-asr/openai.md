> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 录音文件识别（Qwen-ASR）OpenAI 兼容

> 通过 Chat API 进行语音识别

## 接入方式

根据模型选择对应的接入方式。

| 模型                        | 接入方式                                                                                |
| ------------------------- | ----------------------------------------------------------------------------------- |
| Qwen3-ASR-Flash-Filetrans | 仅支持 [DashScope 异步调用](/api-reference/speech-recognition/qwen-asr/dashscope-async)    |
| Qwen3-ASR-Flash           | OpenAI 兼容接口和 [DashScope 同步调用](/api-reference/speech-recognition/qwen-asr/dashscope) |

## 支持的音频格式

Qwen3-ASR-Flash 支持 Base64 编码音频和可公开访问的 URL 作为输入。

## Base64 编码音频输入

使用 [Data URL](https://www.rfc-editor.org/rfc/rfc2397) 格式：`data:<mediatype>;base64,<data>`。

- `<mediatype>`：MIME 类型。例如 WAV：`audio/wav`，MP3：`audio/mpeg`。
- `<data>`：Base64 编码字符串。编码会增大文件体积，请确保编码后的音频不超过 10 MB。

示例：`data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9`

<Accordion title="Base64 编码示例">
  <Tabs>
    <Tab title="Python">
      ```python
      import base64, pathlib

      # 将 "input.mp3" 替换为您的音频文件路径
      file_path = pathlib.Path("input.mp3")
      base64_str = base64.b64encode(file_path.read_bytes()).decode()
      data_uri = f"data:audio/mpeg;base64,{base64_str}"
      ```
    </Tab>

    <Tab title="Java">
      ```java
      import java.nio.file.*;
      import java.util.Base64;

      public class Main {
        /**
         * 将 "filePath" 替换为您的音频文件路径。
         */
        public static String toDataUrl(String filePath) throws Exception {
          byte[] bytes = Files.readAllBytes(Paths.get(filePath));
          String encoded = Base64.getEncoder().encodeToString(bytes);
          return "data:audio/mpeg;base64," + encoded;
        }

        // 用法示例
        public static void main(String[] args) throws Exception {
          System.out.println(toDataUrl("input.mp3"));
        }
      }
      ```
    </Tab>
  </Tabs>
</Accordion>

<Note>
  `asr_options` 是非标准参数。使用 OpenAI SDK 时，需通过 `extra_body` 传入。
</Note>

## OpenAPI

````yaml post /compatible-mode/v1/chat/completions
openapi: 3.1.0
info:
  title: Qwen-ASR 音频文件识别 API
  description: Qwen-ASR 音频文件识别 API 参考文档，支持 OpenAI 兼容协议、DashScope 同步协议和 DashScope 异步协议。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com
    description: DashScope API 服务器
security:
  - bearer: []
paths:
  /compatible-mode/v1/chat/completions:
    post:
      operationId: asrOpenAICompatible
      summary: 识别音频（OpenAI 兼容）
      description: 通过 OpenAI 兼容的 Chat Completions API 识别音频文件，支持 Qwen3-ASR-Flash。接受 URL 或 Base64 编码数据格式的音频输入。
      security:
        - bearer: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/OpenAIASRRequest"
      responses:
        "200":
          description: 成功响应
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/OpenAIASRResponse"
      x-codeSamples:
        - lang: python
          label: Audio URL
          source: |-
            from openai import OpenAI
            import os

            try:
              client = OpenAI(
                # 如果您尚未配置环境变量，请将以下代码行替换为您的 API Key：api_key = "sk-xxx",
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
              )


              stream_enabled = False  # 是否启用流式输出
              completion = client.chat.completions.create(
                model="qwen3-asr-flash",
                messages=[
                  {
                    "content": [
                      {
                        "type": "input_audio",
                        "input_audio": {
                          "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                        }
                      }
                    ],
                    "role": "user"
                  }
                ],
                stream=stream_enabled,
                # 当 stream 设置为 False 时，不能设置 stream_options 参数
                # stream_options={"include_usage": True},
                extra_body={
                  "asr_options": {
                    # "language": "zh",
                    "enable_itn": False
                  }
                }
              )
              if stream_enabled:
                full_content = ""
                print("流式输出内容为：")
                for chunk in completion:
                  # 若 stream_options.include_usage 为 True，最后一个 chunk 的 choices 字段为空列表，应跳过（可通过 chunk.usage 获取 token 用量）
                  print(chunk)
                  if chunk.choices and chunk.choices[0].delta.content:
                    full_content += chunk.choices[0].delta.content
                print(f"完整内容为：{full_content}")
              else:
                print(f"非流式输出内容为：{completion.choices[0].message.content}")
            except Exception as e:
              print(f"错误信息：{e}")
        - lang: python
          label: Base64-encoded audio
          source: |-
            import base64
            from openai import OpenAI
            import os
            import pathlib

            try:
              # 替换为您的音频文件实际路径
              file_path = "welcome.mp3"
              # 替换为您的音频文件的实际 MIME 类型
              audio_mime_type = "audio/mpeg"

              file_path_obj = pathlib.Path(file_path)
              if not file_path_obj.exists():
                raise FileNotFoundError(f"未找到音频文件：{file_path}")

              base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
              data_uri = f"data:{audio_mime_type};base64,{base64_str}"

              client = OpenAI(
                # 如果您尚未配置环境变量，请将以下代码行替换为您的 API Key：api_key = "sk-xxx",
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
              )


              stream_enabled = False  # 是否启用流式输出
              completion = client.chat.completions.create(
                model="qwen3-asr-flash",
                messages=[
                  {
                    "content": [
                      {
                        "type": "input_audio",
                        "input_audio": {
                          "data": data_uri
                        }
                      }
                    ],
                    "role": "user"
                  }
                ],
                stream=stream_enabled,
                # 当 stream 设置为 False 时，不能设置 stream_options 参数
                # stream_options={"include_usage": True},
                extra_body={
                  "asr_options": {
                    # "language": "zh",
                    "enable_itn": False
                  }
                }
              )
              if stream_enabled:
                full_content = ""
                print("流式输出内容为：")
                for chunk in completion:
                  # 若 stream_options.include_usage 为 True，最后一个 chunk 的 choices 字段为空列表，应跳过（可通过 chunk.usage 获取 token 用量）
                  print(chunk)
                  if chunk.choices and chunk.choices[0].delta.content:
                    full_content += chunk.choices[0].delta.content
                print(f"完整内容为：{full_content}")
              else:
                print(f"非流式输出内容为：{completion.choices[0].message.content}")
            except Exception as e:
              print(f"错误信息：{e}")
        - lang: javascript
          label: Audio URL
          source: |-
            // 运行前准备：
            // 适用于 Windows/Mac/Linux：
            // 1. 确保已安装 Node.js（建议版本 >= 14）
            // 2. 运行以下命令安装必要的依赖项：npm install openai

            import OpenAI from "openai";

            const client = new OpenAI({
              // 如果您尚未配置环境变量，请将以下代码行替换为您的 API Key：apiKey: "sk-xxx",
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
            });

            async function main() {
              try {
                const streamEnabled = false; // 是否启用流式输出
                const completion = await client.chat.completions.create({
                  model: "qwen3-asr-flash",
                  messages: [
                    {
                      role: "user",
                      content: [
                        {
                          type: "input_audio",
                          input_audio: {
                            data: "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                          }
                        }
                      ]
                    }
                  ],
                  stream: streamEnabled,
                  // 当 stream 设置为 false 时，不能设置 stream_options 参数
                  // stream_options: {
                  //   "include_usage": true
                  // },
                  extra_body: {
                    asr_options: {
                      // language: "zh",
                      enable_itn: false
                    }
                  }
                });

                if (streamEnabled) {
                  let fullContent = "";
                  console.log("流式输出内容为：");
                  for await (const chunk of completion) {
                    console.log(JSON.stringify(chunk));
                    if (chunk.choices && chunk.choices.length > 0) {
                      const delta = chunk.choices[0].delta;
                      if (delta && delta.content) {
                        fullContent += delta.content;
                      }
                    }
                  }
                  console.log(`完整内容为：${fullContent}`);
                } else {
                  console.log(`非流式输出内容为：${completion.choices[0].message.content}`);
                }
              } catch (err) {
                console.error(`错误信息：${err}`);
              }
            }

            main();
        - lang: javascript
          label: Base64-encoded audio
          source: |-
            // 运行前准备：
            // 适用于 Windows/Mac/Linux：
            // 1. 确保已安装 Node.js（建议版本 >= 14）
            // 2. 运行以下命令安装必要的依赖项：npm install openai

            import OpenAI from "openai";
            import { readFileSync } from 'fs';

            const client = new OpenAI({
              // 如果您尚未配置环境变量，请将以下代码行替换为您的 API Key：apiKey: "sk-xxx",
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
            });

            const encodeAudioFile = (audioFilePath) => {
                const audioFile = readFileSync(audioFilePath);
                return audioFile.toString('base64');
            };

            // 替换为您的音频文件实际路径
            const dataUri = `data:audio/mpeg;base64,${encodeAudioFile("welcome.mp3")}`;

            async function main() {
              try {
                const streamEnabled = false; // 是否启用流式输出
                const completion = await client.chat.completions.create({
                  model: "qwen3-asr-flash",
                  messages: [
                    {
                      role: "user",
                      content: [
                        {
                          type: "input_audio",
                          input_audio: {
                            data: dataUri
                          }
                        }
                      ]
                    }
                  ],
                  stream: streamEnabled,
                  // 当 stream 设置为 false 时，不能设置 stream_options 参数
                  // stream_options: {
                  //   "include_usage": true
                  // },
                  extra_body: {
                    asr_options: {
                      // language: "zh",
                      enable_itn: false
                    }
                  }
                });

                if (streamEnabled) {
                  let fullContent = "";
                  console.log("流式输出内容为：");
                  for await (const chunk of completion) {
                    console.log(JSON.stringify(chunk));
                    if (chunk.choices && chunk.choices.length > 0) {
                      const delta = chunk.choices[0].delta;
                      if (delta && delta.content) {
                        fullContent += delta.content;
                      }
                    }
                  }
                  console.log(`完整内容为：${fullContent}`);
                } else {
                  console.log(`非流式输出内容为：${completion.choices[0].message.content}`);
                }
              } catch (err) {
                console.error(`错误信息：${err}`);
              }
            }

            main();
        - lang: bash
          label: Audio URL
          source: |-
            curl -X POST 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen3-asr-flash",
              "messages": [
                {
                  "content": [
                    {
                      "type": "input_audio",
                      "input_audio": {
                        "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                      }
                    }
                  ],
                  "role": "user"
                }
              ],
              "stream":false,
              "asr_options": {
                "enable_itn": false
              }
            }'
components:
  securitySchemes:
    bearer:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    OpenAIASRRequest:
      type: object
      required:
        - model
        - messages
      properties:
        model:
          type: string
          description: 模型名称。仅支持 Qwen3-ASR-Flash。
          examples:
            - qwen3-asr-flash
        messages:
          type: array
          description: 消息列表。
          items:
            type: object
            required:
              - role
              - content
            properties:
              role:
                type: string
                description: 消息发送者的角色。
                enum:
                  - system
                  - user
              content:
                type: array
                description: 消息内容。
                items:
                  type: object
                  properties:
                    type:
                      type: string
                      description: 音频输入时设置为 `input_audio`。
                      enum:
                        - input_audio
                    input_audio:
                      type: object
                      description: 音频输入对象。
                      properties:
                        data:
                          type: string
                          description: 待识别的音频。支持互联网可访问文件的 URL 和 Base64 编码数据（Data URL 格式：`data:<mediatype>;base64,<data>`）。
                    text:
                      type: string
                      description: 自定义识别的上下文（仅限系统消息）。提供背景文本、实体词汇表及其他参考信息。长度限制：10,000 个 token。
        asr_options:
          type: object
          description: 是否启用特定功能。非标准 OpenAI 参数——使用 OpenAI SDK 时请通过 `extra_body` 传递。
          properties:
            language:
              type: string
              description: 若已知音频语言，可指定该参数以提高识别准确率。只能指定一种语言。若音频包含多种语言，请勿设置此参数。
              enum:
                - zh
                - yue
                - en
                - ja
                - de
                - ko
                - ru
                - fr
                - pt
                - ar
                - it
                - es
                - hi
                - id
                - th
                - tr
                - uk
                - vi
                - cs
                - da
                - fil
                - fi
                - is
                - ms
                - no
                - pl
                - sv
            enable_itn:
              type: boolean
              description: 是否启用逆文本规范化（ITN）。仅适用于中文和英文音频。
              default: false
        stream:
          type: boolean
          description: 是否使用流式输出。建议设置为 `true` 以提高响应速度并降低超时风险。
          default: false
        stream_options:
          type: object
          description: 流式输出配置。仅在 `stream` 为 `true` 时生效。
          properties:
            include_usage:
              type: boolean
              description: 是否在响应的最后一个数据块中包含 token 消耗信息。
              default: false
    OpenAIASRResponse:
      type: object
      properties:
        id:
          type: string
          description: 本次调用的唯一标识符。
          example: chatcmpl-487abe5f-d4f2-9363-a877-xxxxxxx
        choices:
          type: array
          description: 模型的输出信息。
          items:
            type: object
            properties:
              finish_reason:
                type: string
                description: 生成中为 `null`，自然结束时为 `stop`，超出最大长度时为 `length`。
                enum:
                  - stop
                  - length
                  - null
                example: stop
              index:
                type: integer
                description: "`choices` 数组中当前对象的索引。"
                example: 0
              message:
                type: object
                description: 模型输出的消息对象。
                properties:
                  role:
                    type: string
                    description: 输出消息的角色，始终为 `assistant`。
                    example: assistant
                  content:
                    type: string
                    description: 语音识别结果文本。
                    example: 欢迎使用千问AI平台。
                  annotations:
                    type: array
                    description: 输出的注释信息，例如语言和情绪。
                    items:
                      type: object
                      properties:
                        type:
                          type: string
                          description: 固定为 `audio_info`。
                          example: audio_info
                        language:
                          type: string
                          description: 识别音频所用的语言。
                          enum:
                            - zh
                            - yue
                            - en
                            - ja
                            - de
                            - ko
                            - ru
                            - fr
                            - pt
                            - ar
                            - it
                            - es
                            - hi
                            - id
                            - th
                            - tr
                            - uk
                            - vi
                            - cs
                            - da
                            - fil
                            - fi
                            - is
                            - ms
                            - no
                            - pl
                            - sv
                          example: zh
                        emotion:
                          type: string
                          description: 识别音频中的情绪。
                          enum:
                            - surprised
                            - neutral
                            - happy
                            - sad
                            - disgusted
                            - angry
                            - fearful
                          example: neutral
                    example:
                      - emotion: neutral
                        language: zh
                        type: audio_info
          example:
            - finish_reason: stop
              index: 0
              message:
                annotations:
                  - emotion: neutral
                    language: zh
                    type: audio_info
                content: 欢迎使用千问AI平台。
                role: assistant
        created:
          type: integer
          description: 请求创建时的 UNIX 时间戳（秒）。
          example: 1767683986
        model:
          type: string
          description: 本次请求使用的模型。
          example: qwen3-asr-flash
        object:
          type: string
          description: 始终为 `chat.completion`。
          example: chat.completion
        usage:
          type: object
          description: Token 消耗信息。
          properties:
            completion_tokens:
              type: integer
              description: 模型输出的 token 数量。
              example: 12
            completion_tokens_details:
              type: object
              properties:
                text_tokens:
                  type: integer
                  description: 模型输出文本的 token 数量。
                  example: 12
            prompt_tokens:
              type: integer
              description: 输入的 token 数量。
              example: 42
            prompt_tokens_details:
              type: object
              properties:
                audio_tokens:
                  type: integer
                  description: 输入音频的 token 长度。每秒音频折算为 25 个 token，不足 1 秒按 1 秒计算。
                  example: 42
                text_tokens:
                  type: integer
                  description: 忽略此参数。
                  example: 0
            seconds:
              type: integer
              description: 音频时长（秒）。
              example: 1
            total_tokens:
              type: integer
              description: 输入和输出的 token 总量。
              example: 54
      examples:
        - summary: 非流式响应
          value:
            choices:
              - finish_reason: stop
                index: 0
                message:
                  annotations:
                    - emotion: neutral
                      language: zh
                      type: audio_info
                  content: 欢迎使用千问AI平台。
                  role: assistant
            created: 1767683986
            id: chatcmpl-487abe5f-d4f2-9363-a877-xxxxxxx
            model: qwen3-asr-flash
            object: chat.completion
            usage:
              completion_tokens: 12
              completion_tokens_details:
                text_tokens: 12
              prompt_tokens: 42
              prompt_tokens_details:
                audio_tokens: 42
                text_tokens: 0
              seconds: 1
              total_tokens: 54
    DashScopeASRRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。仅支持 Qwen3-ASR-Flash。
          examples:
            - qwen3-asr-flash
        input:
          type: object
          required:
            - messages
          description: 输入对象。
          properties:
            messages:
              type: array
              description: 消息列表。
              items:
                type: object
                required:
                  - role
                  - content
                properties:
                  role:
                    type: string
                    description: 消息发送者的角色。
                    enum:
                      - system
                      - user
                  content:
                    type: array
                    description: 消息内容。
                    items:
                      type: object
                      properties:
                        audio:
                          type: string
                          description: 待识别的音频（用户消息）。支持 URL、Base64 编码数据和本地文件路径（仅限 SDK）。
                        text:
                          type: string
                          description: 自定义识别的上下文（系统消息）。长度限制：10,000 个 token。
        parameters:
          type: object
          description: 附加参数。
          properties:
            asr_options:
              type: object
              description: 是否启用特定功能。仅 Qwen3-ASR-Flash 支持。
              properties:
                language:
                  type: string
                  description: 若已知音频语言，可指定该参数以提高识别准确率。只能指定一种语言。若音频包含多种语言，请勿设置此参数。
                  enum:
                    - zh
                    - yue
                    - en
                    - ja
                    - de
                    - ko
                    - ru
                    - fr
                    - pt
                    - ar
                    - it
                    - es
                    - hi
                    - id
                    - th
                    - tr
                    - uk
                    - vi
                    - cs
                    - da
                    - fil
                    - fi
                    - is
                    - ms
                    - no
                    - pl
                    - sv
                enable_itn:
                  type: boolean
                  description: 是否启用逆文本规范化（ITN）。仅适用于中文和英文音频。
                  default: false
    DashScopeASRResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 本次调用的唯一标识符。Java SDK 中返回为 `requestId`。
          example: 568e2bf0-d6f2-97f8-9f15-a57b11dc6977
        output:
          type: object
          description: 调用结果。
          properties:
            choices:
              type: array
              description: 模型输出，当 `result_format` 为 `message` 时返回。
              items:
                type: object
                properties:
                  finish_reason:
                    type: string
                    description: 生成中为 `null`，自然结束时为 `stop`，超出最大长度时为 `length`。
                    enum:
                      - stop
                      - length
                      - null
                    example: stop
                  message:
                    type: object
                    description: 模型输出的消息对象。
                    properties:
                      role:
                        type: string
                        description: 输出消息的角色，始终为 `assistant`。
                        example: assistant
                      content:
                        type: array
                        description: 输出消息内容。
                        items:
                          type: object
                          properties:
                            text:
                              type: string
                              description: 语音识别结果文本。
                              example: 欢迎使用千问AI平台。
                        example:
                          - text: 欢迎使用千问AI平台。
                      annotations:
                        type: array
                        description: 输出的注释信息。
                        items:
                          type: object
                          properties:
                            type:
                              type: string
                              description: 固定为 `audio_info`。
                              example: audio_info
                            language:
                              type: string
                              description: 识别音频所用的语言。
                              enum:
                                - zh
                                - yue
                                - en
                                - ja
                                - de
                                - ko
                                - ru
                                - fr
                                - pt
                                - ar
                                - it
                                - es
                                - hi
                                - id
                                - th
                                - tr
                                - uk
                                - vi
                                - cs
                                - da
                                - fil
                                - fi
                                - is
                                - ms
                                - no
                                - pl
                                - sv
                              example: zh
                            emotion:
                              type: string
                              description: 识别音频中的情绪。
                              enum:
                                - surprised
                                - neutral
                                - happy
                                - sad
                                - disgusted
                                - angry
                                - fearful
                              example: neutral
                        example:
                          - language: zh
                            type: audio_info
                            emotion: neutral
              example:
                - finish_reason: stop
                  message:
                    annotations:
                      - language: zh
                        type: audio_info
                        emotion: neutral
                    content:
                      - text: 欢迎使用千问AI平台。
                    role: assistant
        usage:
          type: object
          description: Token 消耗信息。
          properties:
            input_tokens_details:
              type: object
              properties:
                text_tokens:
                  type: integer
                  description: 忽略此参数。
                  example: 0
            output_tokens_details:
              type: object
              properties:
                text_tokens:
                  type: integer
                  description: 识别文本输出的 token 长度。
                  example: 6
            seconds:
              type: integer
              description: 音频时长（秒）。
              example: 1
      examples:
        - summary: DashScope 同步响应
          value:
            output:
              choices:
                - finish_reason: stop
                  message:
                    annotations:
                      - language: zh
                        type: audio_info
                        emotion: neutral
                    content:
                      - text: 欢迎使用千问AI平台。
                    role: assistant
            usage:
              input_tokens_details:
                text_tokens: 0
              output_tokens_details:
                text_tokens: 6
              seconds: 1
            request_id: 568e2bf0-d6f2-97f8-9f15-a57b11dc6977
    AsyncASRRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。仅支持 Qwen3-ASR-Flash-Filetrans。
          examples:
            - qwen3-asr-flash-filetrans
        input:
          type: object
          required:
            - file_url
          description: 输入对象。
          properties:
            file_url:
              type: string
              description: 待识别音频文件的 URL，必须可通过互联网访问。
        parameters:
          type: object
          description: 附加参数。
          properties:
            language:
              type: string
              description: 若已知音频语言，可指定该参数以提高识别准确率。
              enum:
                - zh
                - yue
                - en
                - ja
                - de
                - ko
                - ru
                - fr
                - pt
                - ar
                - it
                - es
                - hi
                - id
                - th
                - tr
                - uk
                - vi
                - cs
                - da
                - fil
                - fi
                - is
                - ms
                - no
                - pl
                - sv
            enable_itn:
              type: boolean
              description: 是否启用逆文本规范化（ITN）。仅适用于中文和英文音频。
              default: false
            enable_words:
              type: boolean
              description: 是否返回词级时间戳。设置为 `false` 时返回句级时间戳；设置为 `true` 时返回词级时间戳（支持中文、英文、日语、韩语、德语、法语、西班牙语、意大利语、葡萄牙语和俄语）。同时影响断句方式：`false` 基于 VAD 断句，`true` 基于 VAD 和标点符号断句。
              default: false
            text:
              type: string
              description: 自定义识别的上下文。提供背景文本、实体词汇表及其他参考信息。长度限制：10,000 个 token。
            channel_id:
              type: array
              items:
                type: integer
              description: 多轨音频文件中需要识别的音轨索引，从 0 开始。默认值：`[0]`。每个指定轨道单独计费。
              default:
                - 0
    AsyncASRSubmitResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 本次调用的唯一标识符。
          example: 92e3decd-0c69-47a8-xxxxxxxxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，用于查询任务结果。
              example: 8fab76d0-0eed-4d20-929f-xxxxxxxxxxxx
            task_status:
              type: string
              description: 任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
              example: PENDING
      examples:
        - summary: 任务已提交
          value:
            request_id: 92e3decd-0c69-47a8-xxxxxxxxxxxx
            output:
              task_id: 8fab76d0-0eed-4d20-929f-xxxxxxxxxxxx
              task_status: PENDING
    AsyncASRGetResponse:
      type: object
      properties:
        request_id:
          type: string
          description: 本次调用的唯一标识符。
          example: 1dca6c0a-0ed1-4662-aa39-xxxxxxxxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 8fab76d0-0eed-4d20-929f-xxxxxxxxxxxx
            task_status:
              type: string
              description: 任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - UNKNOWN
              example: SUCCEEDED
            result:
              type: object
              description: 识别结果（任务状态为 SUCCEEDED 时返回）。
              properties:
                transcription_url:
                  type: string
                  description: 识别结果 JSON 文件的下载链接，有效期 24 小时。
                  example: https://dashscope-result.oss-cn-beijing.aliyuncs.com/result.json?Expires=1761631066&OSSAccessKeyId=LTAIxxxx&Signature=xxxx
            submit_time:
              type: string
              description: 任务提交时间。
              example: 2025-10-27 13:57:45.948
            scheduled_time:
              type: string
              description: 任务调度时间（执行开始时间）。
              example: 2025-10-27 13:57:46.018
            end_time:
              type: string
              description: 任务结束时间。
              example: 2025-10-27 13:57:47.079
            task_metrics:
              type: object
              description: 任务指标，包含子任务状态统计。
              properties:
                TOTAL:
                  type: integer
                  description: 子任务总数。
                  example: 1
                SUCCEEDED:
                  type: integer
                  description: 成功的子任务数。
                  example: 0
                FAILED:
                  type: integer
                  description: 失败的子任务数。
                  example: 0
            code:
              type: string
              description: 错误码，仅在任务失败时返回。
              example: FILE_403_FORBIDDEN
            message:
              type: string
              description: 错误信息，仅在任务失败时返回。
              example: FILE_403_FORBIDDEN
        usage:
          type: object
          description: Token 消耗信息。
          properties:
            seconds:
              type: integer
              description: 音频时长（秒）。
              example: 3
      examples:
        - summary: SUCCEEDED
          value:
            request_id: 1dca6c0a-0ed1-4662-aa39-xxxxxxxxxxxx
            output:
              task_id: 8fab76d0-0eed-4d20-929f-xxxxxxxxxxxx
              task_status: SUCCEEDED
              submit_time: 2025-10-27 13:57:45.948
              scheduled_time: 2025-10-27 13:57:46.018
              end_time: 2025-10-27 13:57:47.079
              result:
                transcription_url: https://dashscope-result.oss-cn-beijing.aliyuncs.com/result.json?Expires=1761631066&OSSAccessKeyId=LTAIxxxx&Signature=xxxx
            usage:
              seconds: 3
        - summary: RUNNING
          value:
            request_id: 6769df07-2768-4fb0-ad59-xxxxxxxxxxxx
            output:
              task_id: 9be1700a-0f8e-4778-be74-xxxxxxxxxxxx
              task_status: RUNNING
              submit_time: 2025-10-27 14:19:31.150
              scheduled_time: 2025-10-27 14:19:31.233
              task_metrics:
                TOTAL: 1
                SUCCEEDED: 0
                FAILED: 0
        - summary: FAILED
          value:
            request_id: 3d141841-858a-466a-9ff9-xxxxxxxxxxxx
            output:
              task_id: c58c7951-7789-4557-9ea3-xxxxxxxxxxxx
              task_status: FAILED
              submit_time: 2025-10-27 15:06:06.915
              scheduled_time: 2025-10-27 15:06:06.967
              end_time: 2025-10-27 15:06:07.584
              code: FILE_403_FORBIDDEN
              message: FILE_403_FORBIDDEN
````
