> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 错误信息

> API 错误码参考

本文介绍使用千问AI平台服务可能出现的错误信息及解决方案。

## 400-InvalidParameter

### parameter.enable\_thinking must be set to false for non-streaming calls/parameter.enable\_thinking only support stream call

**原因**： 使用非流式输出方式调用了思考模式模型。

**解决方案**：请将`enable_thinking`参数设置为`false`，或者改用[流式输出](/developer-guides/run-and-scale/streaming)方式调用思考模式模型。

### The thinking\_budget parameter must be a positive integer and not greater than xxx

**原因**： `thinking_budget` 参数不在可选值范围内。

**解决方案**： 请参见模型列表中模型的最大思维链长度，指定为大于0且不超过该长度的值。

### This model only support stream mode, please enable the stream parameter to access the model.

**原因**： 模型仅支持[流式输出](/developer-guides/run-and-scale/streaming)，但调用时未启用流式输出。

**解决方案**： 请使用[流式输出](/developer-guides/run-and-scale/streaming)方式调用模型。

### This model does not support enable\_search.

**原因**： 当前模型不支持[联网搜索](/developer-guides/tool-calling/web-search)能力，但指定了`enable_search`参数为`true`。

**解决方案**： 请调用支持联网搜索能力的模型。

### 暂时不支持当前设置的语种！

**原因**： 使用 Qwen-MT 模型时，传入的 `source_lang` 或 `target_lang` 格式错误，或不在[支持的语言](/developer-guides/text-generation/qwen-mt)里。

**解决方案**： 请传入正确格式的英文名或语种编码。

### The incremental\_output parameter must be "true" when enable\_thinking is true

**原因**： 模型开启思考模式时仅支持增量流式输出，未将`incremental_output`参数设置为`true`。

**解决方案**： 请将`incremental_output`参数设置为`true`再调用，API将返回增量内容。

### The incremental\_output parameter of this model cannot be set to False.

**原因**： 模型仅支持增量流式输出，未将`incremental_output`参数设置为`true`。

**解决方案**： 请将`incremental_output`参数设置为`true`再调用，API将返回增量内容。

### Range of input length should be \[1, xxx]

**原因**： 调用模型时输入内容长度超过模型上限。

**解决方案**：

- 若通过代码调用，请控制 messages 数组中的 Token 数在模型最大输入Token范围内；
- 使用对话客户端（如Chatbox）或千问AI平台控制台进行连续对话时，每次请求都会附带历史记录，容易超出模型限制。超出限制后，请开启新对话。

### Range of max\_tokens should be \[1, xxx]

**原因**： `max_tokens` 参数设置未在 \[1, 模型最大输出 Token 数]的范围内。

**解决方案**： `max_tokens`上限请参考模型列表文档中的"最大输出 Token 数"。

### Temperature should be in \[0.0, 2.0)/'temperature' must be Float

**原因**： temperature参数设置不在\[0.0, 2.0)范围。

**解决方案**： 将temperature参数设置为大于等于0，小于2的数字。

### Range of top\_p should be (0.0, 1.0]/'top\_p' must be Float

**原因**： top\_p参数设置不在`(0.0, 1.0]`范围。

**解决方案**： 将`top_p`参数设置为大于0，小于等于1的数字。

### Parameter top\_k be greater than or equal to 0

**原因**： `top_k`参数设置为小于0的数字。

**解决方案**： 将`top_k`参数设置为大于等于0的数字。

### Repetition\_penalty should be greater than 0.0

**原因**： `repetition_penalty`参数设置为小于等于0的数字。

**解决方案**： 将`repetition_penalty`参数设置为大于0的数字。

### Presence\_penalty should be in \[-2.0, 2.0]

**原因**： `presence_penalty`参数不在`[-2.0,2.0]`区间。

**解决方案**： 将`presence_penalty`参数设置在`[-2.0,2.0]`区间。

### Range of n should be \[1, 4]

**原因**： n 参数设置未在 \[1, 4]的范围内。

**解决方案**： 将 n 参数设置在\[1, 4]范围内。

### Range of seed should be \[0, 9223372036854775807]

**原因**： 使用DashScope协议时，`seed` 参数设置未在 \[0, 9223372036854775807]的范围内。

**解决方案**： 将`seed`参数设置在 \[0, 9223372036854775807]的范围内。

### Request method 'GET' is not supported.

**原因**： 当前接口不支持 `GET` 请求方法。

**解决方案**： 请查阅接口文档，使用该接口支持的请求方法（如 `POST` 等）重新发起请求。

### messages with role "tool" must be a response to a preceding message with "tool\_calls"

**原因**： 在工具调用时没有向 messages 数组添加 Assistant Message。

**解决方案**： 请将模型第一轮响应的 Assistant Message 添加到 messages 数组后再添加 Tool Message。

### An assistant message with "tool\_calls" must be followed by tool messages responding to each "tool\_call\_id"

**原因**： assistant 消息包含 tool\_calls 时，后续必须跟随 tool 角色消息来响应每个 tool\_call\_id。常见于使用工具调用时消息序列格式不正确，例如在带 tool\_calls 的 assistant 消息之后直接追加 user 消息。

**解决方案**： 在带 tool\_calls 的 assistant 消息之后、发送下一个 user 消息之前，插入对应的 tool 角色消息（每条包含匹配的 tool\_call\_id 和该工具的执行结果）。assistant 消息中的每个 tool\_call\_id 都必须有且仅有一条 tool 消息与之对应。

### Required body invalid, please check the request body format.

**原因**： 请求体（body）格式不符合接口要求。

**解决方案**： 请检查请求体，确保为标准的JSON字符串。常见问题有：多了`,`、括号未闭合、引号未闭合等。

错误示例（`text`字段缺少闭合引号，导致请求体不是合法 JSON）：

```json
{"model":"qwen-image-edit","input":{"messages":[{"role":"user","content":[{"image":"https://example.com/img.png"},{"text":"请将图片背景改为蓝色}]}]}}
```

正确示例：

```json
{"model":"qwen-image-edit","input":{"messages":[{"role":"user","content":[{"image":"https://example.com/img.png"},{"text":"请将图片背景改为蓝色"}]}]}}
```

提交请求前可使用 jsonlint.com 等 JSON 校验工具检查请求体语法，也可借助大模型帮助修复请求体格式。

### input content must be a string.

**原因**： 纯文本模型不支持将 messages 中的 content 设置为非字符串类型。

**解决方案**： 请勿将content设置为如`[{"type": "text","text": "你是谁？"}]`的数组类型。

### The content field is a required field.

**原因**： 发起请求时，未指定`content`参数，如`{"role": "user"}`。

**解决方案**： 请指定`content`参数。如`{"role": "user","content": "你是谁"}`。

### current user api does not support http call.

**原因**：当前模型不支持非流式输出。

**解决方案**：请使用[流式输出](/developer-guides/run-and-scale/streaming)。

### Either "prompt" or "messages" must exist and cannot both be none

**原因**： 调用大模型时，既未指定`messages`参数，也未指定`prompt`参数（即将废弃）。如果指定了`messages`参数后报错，可能是因为格式错误，例如通过DashScope-HTTP时，`messages`需放入`input`对象中，而不是与`model`参数并列。

**解决方案**： 请指定`messages`参数。如果已指定但仍报错，请参见[千问](/developer-guides/getting-started/text-generation-models)API文档，检查其位置是否正确。

### 'messages' must contain the word 'json' in some form, to use 'response\_format' of type 'json\_object'.

**原因**： 使用[结构化输出](/developer-guides/text-generation/structured-output)时，提示词中不包含 `json` 关键词。

**解决方案**： 在提示词中加入`json`（不区分大小写），如：“请以json格式输出”。

### Json mode response is not supported when enable\_thinking is true

**原因**： 使用[结构化输出](/developer-guides/text-generation/structured-output)时开启了模型的思考模式。

**解决方案**： 请在使用结构化输出时，将`enable_thinking`设为`false`关闭思考模式。也可参见常见问题[思考模式模型如何结构化输出？](/resources/faq-text-generation)

### Tool names are not allowed to be \[search]

**原因**： 工具名称无法设置为`search`。

**解决方案**： 工具名称请设置为`search`之外的值。

### Unknown format of response\_format, response\_format should be a dict, includes 'type' and an optional key 'json\_schema'. The response\_format type from user is xxx.

**原因**： 指定的`response_format`参数不符合规定。

**解决方案**： 如需使用[结构化输出](/developer-guides/text-generation/structured-output)功能，请将`response_format`参数设置为`{"type": "json_object"}`。

### The value of the enable\_thinking parameter is restricted to True.

**原因**： 部分模型（如`qwen3-235b-a22b-thinking-2507`）不可将`enable_thinking`参数设为 `false`。

**解决方案**：

- 若通过第三方工具调用（如 Cherry Studio），请打开输入框的思考开关。
- 若通过代码调用，请将`enable_thinking`设为`true`。

### 'audio' output only support with stream=true

**原因**： 在使用Qwen-Omni模型时，未使用流式输出方式，而模型仅支持流式输出方式。

**解决方案**： 设置`stream`参数为`true`以启用流式输出。

### tool\_choice is one of the strings that should be \["none", "auto"]

**原因**： 发起 Function Calling 时指定的 `tool_choice` 参数有误。

**解决方案**： 请指定为 "auto"（由大模型自主选择工具）或 "none"（强制不使用工具）。

### Model not exist.

**原因**： 设置的`model`参数不存在或格式不正确。

**解决方案**：

- **检查模型名称格式**：确认`model`参数大小写是否正确，是否存在多余的空格。
- **使用正确的模型名称**：请对照模型列表中的模型名称，检查输入的`model`是否正确。请勿混用开源社区的模型名与千问AI平台模型ID，如应该使用`qwen3-235b-a22b-instruct-2507`，而非`Qwen/Qwen3-235B-A22B-Instruct-2507`。

### The product is not activated, please confirm that you have activated products and try again after activation.

**原因**： 所调用的模型服务未开通（未激活）。通过 OpenAI 兼容接口调用时，若目标模型未在模型市场开通，网关会返回该错误，错误码为`invalid_parameter_error`。

**解决方案**：

- **开通模型服务**：请前往[模型市场](https://www.qianwenai.com/models)，确认所调用的模型（如`kimi-k3`）处于已开通状态后再行调用。
- **开通千问AI平台服务**：若尚未开通千问AI平台服务，请先开通后再调用。

### The result\_format parameter must be "message" when enable\_thinking is true

**原因**： 调用思考模式模型，`result_format`参数未设置为`"message"`。

**解决方案**： 将`result_format`参数设置为`"message"`。

### The audio is empty

**原因**： 输入音频时间过短，导致采样点不足。

**解决方案**： 请增加音频的时间。

### File parsing in progress, please try again later.

**原因**：使用 Qwen-Long 模型时，文件未完成解析。

**解决方案**：请等待文件解析完成后再重试。

### The "stop" parameter must be of type "str", "list\[str]", "list\[int]", or "list\[list\[int]]", and all elements within the list must be of the same type.

**原因**： `stop` 参数不符合`str`, `list[str]`, `list[int],` 或`list[list[int]]`格式。

**解决方案**： 参见[千问](/developer-guides/getting-started/text-generation-models)API 文档，设置正确格式的`stop` 参数。

### Value error, batch size is invalid, it should not be larger than xxx.

**原因**： 调用 Embedding 模型时，文本数量超过模型上限。

**解决方案**： 参考[Embedding](/developer-guides/embeddings/embedding)文档中模型的**批次大小**信息，控制传入文本的数量。

### Invalid file \[id:file-fe-].

**原因**：提供的 file-id 无效。例如输入错误、使用了不属于当前千问AI平台账号的 file-id。

**解决方案**：通过[OpenAI兼容-File](/api-reference/platform-api/file)确认file-id是否有效，或重新上传[OpenAI兼容-File](/api-reference/platform-api/file)来获取新的file\_id后进行调用。

### \[] is too short

**原因**： 输入的messages为空数组。

**解决方案**： 请添加 message 后再发起请求。

### The tool call is not supported.

**原因**： 使用的模型不支持传入tools参数。

**解决方案**： 请更换为支持Function Calling的Qwen或DeepSeek模型。

### Repetitive tool calls detected in the conversation history. The same tool call with identical name and arguments has been repeated across multiple consecutive rounds. Please modify your request or adjust the tool call arguments to avoid infinite loops.

**原因**： 在对话历史中检测到重复的工具调用：名称和参数完全相同的工具调用在多个连续轮次中重复出现，模型可能已陷入循环。该错误对应的 HTTP 状态码为 400，错误码为`InternalError.Algo.InvalidParameter`。

**解决方案**：

- 在每轮工具调用后，将工具的执行结果以 Tool Message 形式追加到`messages`数组中，再发起下一轮请求，便于模型据此推进而非重复发起相同调用。
- 检查工具是否正常返回结果；若工具持续返回相同或无效结果，建议在应用侧增加工具调用次数上限或终止逻辑，避免无限循环。
- 必要时优化提示词，明确任务完成的条件，避免模型反复发起同一工具调用。

### The provided messages input is invalid. The error info is \[Unexpected item type in content] / Input should be a valid string / Input should be a valid dictionary or instance of ... (input.messages.x.content...)

**原因**：`messages` 数组中某条消息的 `content` 字段包含了不受支持的元素类型。当 `content` 为数组时，其中每个元素必须是字符串，或符合规范的对象（如 `{"type": "text", "text": "..."}`、`{"type": "image_url", ...}` 等）；若数组中混入了数字、布尔值、嵌套数组，或 `type` 取值不受支持的对象，则会触发该错误。该错误对应的 HTTP 状态码为 400，错误码为 `InternalError.Algo.InvalidParameter`。

**常见场景**：使用纯文本模型（如 Qwen-Max 文本系列，包括 `qwen3-max`）时，若 `messages`（尤其是多轮对话历史）中包含图片（`image_url`）等多模态 `content` 元素时，由于纯文本模型不支持图片等模态输入，同样会触发该错误（在部分接入工具/智能体中，该报错可能被转述为"模型服务商返回空内容"等提示）。

**解决方案**：

- **纯文本模型**：请将 `content` 设置为字符串，不要传入数组或其他类型。若业务需要图片等多模态输入，请改用多模态模型（如 Qwen-VL、Qwen3-VL 系列）；若需继续使用纯文本模型，请在调用前从 `messages` 及对话历史中移除图片（`image_url`）等多模态元素。
- **多模态模型**：`content` 数组中的每个元素都需为合法对象，`type` 仅支持 `text`、`image_url`、`video_url`、`video` 等模型支持的模态类型，请勿混入数字、布尔值、嵌套数组，或缺少 `type`、`type` 取值非法的元素。

### Required parameter(xxx) missing or invalid, please check the request parameters.

**原因**： 接口调用参数不合法。

**解决方案**： 请检查请求参数，确保所有必需参数都已提供且格式正确。

### input must contain file\_urls

**原因**： 使用语音识别（Paraformer）的录音文件识别时，未对请求参数`file_urls`赋值。

**解决方案**： 请在请求中包含`file_urls`参数并为其赋值。

### The provided URL does not appear to be valid. Ensure it is correctly formatted.

**原因**： 当使用视觉理解、全模态或音频理解模型时，传入数据的 URL 或本地路径无效或不符合要求。

**解决方案**：

- **传入 URL** ：需要以 `http://`、 `https://`、`data:`开头。若以`data:`开头, 在 Base64 编码数据前需要包含`"base64"`。
- **传入本地路径**：需要以`file://`开头。
- **传入临时URL**：通过 HTTP 调用，需确保请求的 Header 中添加了参数 `X-DashScope-OssResourceResolve: enable`。
- 通过 SDK 调用：仅支持 DashScope SDK调用，请勿使用 OpenAI SDK。

### Input should be a valid dictionary or instance of GPT3Message

**原因**： messages 字段的构造格式不符合要求，例如括号数量不匹配、缺少必要的键值对等。

**解决方案**： 请检查`messages`字段的JSON结构是否正确。

### Value error, contents is neither str nor list of str.: input.contents

**原因**： 使用 Embedding 模型时，输入不是字符串也不是字符串数组。

**解决方案**： 请修改输入格式为字符串或字符串列表。

### File \[id:file-fe-xxx] format is not supported.

**原因**： Qwen-Long模型仅限于处理纯文本格式文件（TXT、DOCX、PDF、EPUB、MOBI、MD），不支持图片或扫描文档。

**解决方案**： 如需对图片内容进行文本提取、分析和总结，可使用千问VL模型。

### File \[id:file-fe-] cannot be found.

**原因**： 仅在Qwen-Long模型的对话场景中，在发起对话请求后的极短时间内调用OpenAI文件兼容接口删除相关文件时才会出现。

**解决方案**： 请等待模型完成对话后再删除相关文件。

### Too many files provided.

**原因**： 提供的file-id数量超限。

**解决方案**： 请确保file-id数量小于100。

### File \[id:file-fe-] exceeds size limit.

**原因**：文件大小超出限制。

**解决方案**： 确保文件小于150 MB。

### File \[id:file-fe-] exceeds page limits (15000 pages).

**原因**： 文件页数超出限制。

**解决方案**： 确保文件页数少于15000页。

### File \[id:file-fe-] content blank.

**原因**： 文件内容为空。

**解决方案**： 确保文件内容不为空。

### Total message token length exceed model limit (10000000 tokens).

**原因**： 输入总长度超过了10,000,000 Token。

**解决方案**： 请确保message长度符合要求。

### The video modality input does not meet the requirements because: the range of sequence images should be (4, 512)./(4,80).

**原因**： 使用千问 VL 模型以图像列表方式输入视频时，图像数量不符合要求。

**解决方案**： Qwen3-VL与Qwen2.5-VL系列模型需传入4-512张图片；其他模型需传入4-80张图片。详情可参见[图像与视频理解](/developer-guides/multimodal/vision)。

### Exceeded limit on max bytes per data-uri item : 10485760'. / Multimodal file size is too large

**原因**： 向多模态模型（Qwen-VL、QVQ、Qwen-Omni）传入的本地图像或视频超出大小限制。

**解决方案**：

- **本地文件**：Base64 编码后单个文件不得超过 10 MB。
- **文件 URL**：图像文件不得超过 10 MB；对于视频文件，Qwen3-VL、qwen-vl-max：不超过 2GB；
- qwen-vl-plus系列：不超过 1GB；
- 其他模型不超过 150MB。

压缩文件体积请参见[如何将图像或视频压缩到满足要求的大小？](/resources/faq-images-videos)

### Input should be 'Cherry', 'Serena', 'Ethan' or 'Chelsie': parameters.audio.voice

**原因**： 使用Qwen-Omni或Qwen-TTS 时`voice`参数指定错误。

**解决方案**： 请指定为'Cherry', 'Serena', 'Ethan' 或 'Chelsie'中的一个。

### The image length and width do not meet the model restrictions.

**原因**： 传入千问VL模型的图像尺寸（长度和宽度）不符合模型的要求。

**解决方案**： 图像尺寸需满足以下要求：宽度和高度均不小于10像素，且宽高比不应超过200:1或1:200。

### Failed to decode the image during the data inspection.

**原因**： 图像解码失败。

**解决方案**： 请确认图像是否有损坏，以及图像格式是否符合要求。

### The file format is illegal and cannot be opened. / The audio format is illegal and cannot be opened. / The media format is not supported or incorrect for the data inspection.

**原因**： 无法支持的文件格式或文件无法打开。

**解决方案**： 请确认文件是否损坏、文件扩展名和实际格式是否匹配、文件格式是否支持。

### The input messages do not contain elements with the role of user.

**原因**：

- 调用模型时，未向模型传入 User Message；
- 或API调用千问AI平台工作流应用时，在开始节点中传入的参数，需通过`biz_params`参数传递（而非`user_prompt_params`）。

**解决方案**： 请确保向模型传入User Message，或正确传递自定义参数。

### Failed to download multimodal content. / Download the media resource timed out during the data inspection process. / Unable to download the media resource during the data inspection process.

**原因**：服务端无法下载公网 URL 指向的媒体文件，可能由以下原因导致。

- **连通性问题**： 使用了[阿里云对象存储服务](https://www.aliyun.com/product/oss)内网地址。
- **网络延迟**： 远距离访问引发超时。
- **服务不稳定**： 源存储服务响应慢或不可达。
- **安全策略拦截**： 服务端下载公网 URL 时携带的 User-Agent 包含`DashScopeUserBot`标识，第三方服务器的安全策略可能拦截该标识导致下载失败。

**解决方案**：

- **更换存储服务**建议使用低延迟的存储服务。推荐使用[阿里云对象存储服务](https://www.aliyun.com/product/oss)生成公网链接（请勿使用内网地址）。
- **调整传输方式**若传入公网 URL 方式失败，可参考[传入本地文件（Base64 编码或文件路径）](/resources/faq-images-videos)切换为推荐的传入方式：

| **文件类型** | **文件规格**         | **DashScope SDK（Python、Java）**                                | **OpenAI 兼容 / DashScope HTTP**                                |
| -------- | ---------------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| 图像       | 大于 7MB 小于 10MB   | 传入本地路径                                                        | 仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss) |
| 图像       | 小于 7MB           | 传入本地路径                                                        | Base64 编码                                                     |
| 视频       | 大于 100 MB        | 仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss) | 仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss) |
| 视频       | 大于 7MB 小于 100 MB | 传入本地路径                                                        | 仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss) |
| 视频       | 小于 7MB           | 传入本地路径                                                        | Base64 编码                                                     |
| 音频       | 大于 10 MB         | 仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss) | 仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss) |
| 音频       | 大于 7MB 小于 10 MB  | 传入本地路径                                                        | 仅支持公网 URL，建议使用[阿里云对象存储服务](https://www.aliyun.com/product/oss) |
| 音频       | 小于 7MB           | 传入本地路径                                                        | Base64 编码                                                     |

Base64 编码会增大数据体积，原始文件大小应小于 7 MB。
使用 Base64 或本地路径可避免服务端下载超时，提升稳定性。

- \*\*放行`DashScopeUserBot`\*\*若图片托管在您控制的服务器上，请在安全策略中放行 User-Agent 包含`DashScopeUserBot`的请求。也可改用[传入本地文件（Base64 编码或文件路径）](/resources/faq-images-videos)的方式，避免服务端下载公网 URL。

### Failed to find the requested media resource during the data inspection process.

**原因**：传入的资源URL无效或无法访问。

**解决方案**：

- 确认URL格式正确且可访问
- 确认资源文件未被删除或移动
- 确认URL未过期（如使用OSS签名URL，需检查有效期）

### url error, please check url！

- **原因一： 模型名称与API 端点不匹配**：例如调用纯文本模型时使用了多模态接口，或者调用多模态模型时使用了纯文本接口。**解决方案**：通过DashScope使用qwen3.7-plus、qwen3-vl-plus等**多模态模型**时：需使用MultiModalConversation.call() 或multimodal-generation端点，具体参考[图像与视频理解](/developer-guides/multimodal/vision)。
  若使用 spring-ai-alibaba 框架，请确认是否设置多模态参数[withMultiModel](https://github.com/spring-ai-alibaba/examples/blob/c66ffdec789defe4adf86b34bac0084df3b71e92/spring-ai-alibaba-multi-model-example/dashscope-multi-model/src/main/java/com/alibaba/cloud/ai/example/multi/controller/MultiModelController.java#L82)。
- 通过DashScope使用qwen3-max、qwen-plus、deepseek-v3.2等**纯文本模型**时，需使用Generation.call() 或 text-generation 端点，具体参考[文本生成模型概述](/developer-guides/getting-started/text-generation-models)。
- 通过DashScope使用CosyVoice**声音复刻**接口时：该接口包含 `model` 与 `target_model` 参数：需将 `model` 设置为 `voice-enrollment`， `target_model` 设置为具体的 CosyVoice 模型，具体参考[CosyVoice声音复刻/设计API](/api-reference/speech-synthesis/voice-cloning/overview)。
- **原因二：DashScope SDK 版本过低**：调用图像/视频生成模型时，旧版SDK无法识别正确的服务端地址；**解决方案**：[升级 SDK 版本](/api-reference/preparation/install-sdk)

### Don't have authorization to access the media resource during the data inspection process.

**原因**： 调用模型时，传入的OSS中带签名的文件URL已经过期。

**解决方案**： 请确保在文件URL的有效期内访问该文件。

### The item of content should be a message of a certain modal.

**原因**： 使用DashScope SDK调用多模态模型时，`content` 数组中每个元素的键必须为以下值之一：`image`、`video`、`audio` 或 `text`。

**解决方案**： 请使用正确的`content`参数。

### Invalid video file.

**原因**： 传入的视频文件无效。

**解决方案**： 请检查视频文件是否损坏或格式是否正确。

### The video modality input does not meet the requirements because: The video file is too long.

**原因**： 传入千问VL模型或者Qwen-Omni 模型的视频时长超过限制。

**解决方案**：

- Qwen2.5-VL模型支持的视频时长应在2秒至10分钟之间。
- 其他千问VL或Qwen-Omni 模型支持的视频时长应在2秒至40秒之间。

### Field required: xxx

**原因**： 缺少入参。

**解决方案**： 请根据错误提示`xxx`补充对应的参数。

### The request is missing required parameters or in a wrong format, please check the parameters that you send.

**原因**： 缺少入参，或入参格式错误。

**解决方案**： 请检查请求参数是否完整且格式正确。

### Invalid ext\_bbox.

**原因**： 输入的ext\_bbox无效。

**解决方案**： 详情参见[Emoji 视频生成](/api-reference/video-generation/emoji-video/create-task)。

### Driven not exist: driven\_id.

**原因**： 输入的driven\_id不存在。

**解决方案**： 详情参见[Emoji 视频生成](/api-reference/video-generation/emoji-video/create-task)。

### Missing training files.

**原因**： 参数错误，缺少参数或者参数格式问题等。

### The style is invalid.

**原因**： style不在枚举范围内。

**解决方案**： 请检查`style`参数的取值是否正确。

### The style\_level is invalid.

**原因**： style\_level不在枚举范围内。

**解决方案**： 详情参见[EMO 视频生成](/api-reference/video-generation/emo-video/create-task)。

### parameters.video\_ratio must be 9:16 or 3:4.

**原因**： video\_ratio 入参只能为 9:16 或 3:4。

**解决方案**： 请修改`video_ratio`参数为 "9:16" 或 "3:4"。

### the xxx parm is invalid!

**原因**： 输入参数超出范围。

**解决方案**： 详情参见[视频风格重绘](/developer-guides/video-generation/video-editing)。

### input json error.

**原因**： 输入JSON错误。

**解决方案**： 请检查请求的JSON格式是否正确。

### read image error.

**原因**： 读取图像失败。

**解决方案**： 请检查图像文件是否损坏或格式是否正确。

### the parameters must conform to the specification: xxx.

**原因**： 输入参数值超出范围。

**解决方案**： 请根据错误提示`xxx`检查并修正参数值。

### The size of person image and coarse\_image are not the same.

**原因**： coarse\_image分辨率和person\_image不一致。

**解决方案**： 请确保`coarse_image`和`person_image`的分辨率一致。

### The request is missing required parameters or the parameters are out of the specified range, please check the parameters that you send.

**原因**： 缺少必要的接口调用参数或参数越界。

**解决方案**： 请检查并修正请求参数。

### image format error

**原因**： 图片格式错误。

**解决方案**： 需要是图片url或者Base64字符串。

### No messages found in input

**原因**： 请求参数中需要有messages字段。

**解决方案**： 详情参见[千问-图像编辑](/api-reference/image-generation/qwen-image-editing)。

### Invalid image format or corrupted file

**原因**： 输入图片格式错误或文件损坏。

**解决方案**： 请检查文件是否可正常打开和下载，确保文件完整且格式符合要求。

### download image failed

**原因**： 图片不能下载。

**解决方案**： 请检查文件是否可正常下载。

### messages length only support 1

**原因**： messages数组长度仅支持 1。

**解决方案**： 即只能传入一条对话消息。详情参见[千问-图像编辑](/api-reference/image-generation/qwen-image-editing)。

### content length only support 2

**原因**： content数组长度仅支持为2。

**解决方案**： 即只能传入一组text和image。详情参见[千问-图像编辑](/api-reference/image-generation/qwen-image-editing)。

### lack of image or text

**原因**： 请求参数缺少image或text字段。

**解决方案**： 详情参见[千问-图像编辑](/api-reference/image-generation/qwen-image-editing)。

### num\_images\_per\_prompt must be 1.

**原因**： 请求参数不合法，参数`n`（生成图片数量）只能设置为1。

**解决方案**： 请将参数`n`的值设置为1。

### Input files format not supported.

**原因**： 音频、图片格式不符合要求。

**解决方案**： 音频支持格式mp3, wav, aac，图片支持格式jpg, jpeg, png, bmp, webp。详情参见[LivePortrait 视频生成](/api-reference/video-generation/liveportrait-video/create-task)。

### Failed to download input files.

**原因**： 输入文件下载失败。

**解决方案**： 请检查文件URL是否可访问，网络是否通畅。

### oss download error.

**原因**： 输入图像下载失败。

**解决方案**： 请检查图像的OSS链接是否正确且可访问。

### The image content does not comply with green network verification.

**原因**： 图像内容不合规。

**解决方案**： 请更换符合内容安全规范的图像。

### read video error.

**原因**： 读取视频失败。

**解决方案**： 请检查视频文件是否损坏或格式不受支持。

### the size of input image is too small or too large.

**原因**： 输入图像的尺寸过小或者过大。

**解决方案**： 请调整图像尺寸以符合API要求。

### The request parameter is invalid, please check the request parameter.

**原因**： `clothes_type`入参不合规。

**解决方案**： 详情参见[AI试衣-图片分割](/api-reference/image-generation/aitryon-parsing)。

### The type or value of {parameter} is out of definition.

**原因**： 参数类型或值不符合要求。

**解决方案**： 详情参见[LivePortrait 视频生成](/api-reference/video-generation/liveportrait-video/create-task)。

### The request parameter is invalid, please check the request parameter.

**原因**： 画幅入参不合规。

**解决方案**： 可选"1:1"或"3:4"。

### request timeout after 23 seconds.

**原因**： 超过23秒未向服务发送数据。该报错信息在使用[实时语音合成（Sambert）](/api-reference/speech-synthesis/sambert/websocket)、[实时语音识别/翻译（Gummy）](/developer-guides/speech/realtime-multimodal-speech)、[语音识别（Paraformer）](/api-reference/speech-recognition/paraformer-realtime/websocket-api)和[实时语音合成（Qwen-Audio-TTS/CosyVoice）](/api-reference/speech-synthesis/cosyvoice/python-sdk)时产生。

**解决方案**： 请检查为什么长时间未向服务器发送数据。如果长时间（超过23秒）不向服务端发送消息，请及时结束任务。

### Please ensure input text is valid.

**原因**： 若您使用[实时语音合成（Qwen-Audio-TTS/CosyVoice）](/api-reference/speech-synthesis/cosyvoice/python-sdk)，此错误通常是由于未发送待合成文本引起的。可能原因包括：参数遗漏（未为 `text` 参数赋值）或代码异常（导致对 `text` 参数的赋值失败）。

**解决方案**： 请排查代码，确保 `text` 参数被正确赋值并发送。

### Missing required parameter 'payload.model'! Please follow the protocol!

**原因**： 若您使用[实时语音合成（Qwen-Audio-TTS/CosyVoice）](/api-reference/speech-synthesis/cosyvoice/python-sdk)，此错误通常是由于发送[run-task指令](/api-reference/speech-synthesis/cosyvoice/websocket-api)未指定`model`参数。

**解决方案**： 请指定 `model` 参数。

### \[tts:]Engine return error code: 418

**原因**： 使用[实时语音合成（Qwen-Audio-TTS/CosyVoice）](/api-reference/speech-synthesis/cosyvoice/python-sdk)，请求参数 `voice`（音色）不正确，或 `model`（模型）与 `voice`（音色）版本不匹配。

**解决方案**：

1. **检查** `voice` **参数赋值**：

- 如果使用的是默认音色，请对照[Python SDK](/api-reference/speech-synthesis/cosyvoice/python-sdk)中的“voice参数”进行确认。
- 如果使用的是声音复刻音色，请通过[CosyVoice声音复刻/设计API](/developer-guides/speech/voice-design)接口确认音色状态为“OK”，并确保音色归属账号与调用账号一致。

2. **检查版本匹配**：v2模型只能使用v2的音色，v1模型只能使用v1的音色，两者不可混用。

### Request voice is invalid!

**原因**： 若您使用[实时语音合成（Qwen-Audio-TTS/CosyVoice）](/api-reference/speech-synthesis/cosyvoice/python-sdk)，此错误通常是因为未设置音色。

**解决方案**： 请检查是否对`voice`参数赋值。若您使用[WebSocket API](/api-reference/speech-synthesis/cosyvoice/websocket-api)，请参照API文档按照正确JSON格式配置参数。

### ref\_images\_url and obj\_or\_bg must be the same length.

**原因**： 使用[万相-视频编辑2.1](/developer-guides/video-generation/video-editing)的多图参考功能时，`ref_images_url`和`obj_or_bg`的数组长度不一致。

**解决方案**： 请确保`ref_images_url`和`obj_or_bg`的数组长度一致。

### check input data style.

**原因**： 输入参数不满足入参要求。

**解决方案**： 请检查并修正输入参数。

### An error during model pre-process.

**原因**： 传入了错误格式的 content 字段。

**解决方案**：

- 若通过代码调用，请勿将content设置为如`[{"type": "text", "text": "你是谁？"}]`的array类型。
- 若使用 [Cline](/developer-guides/clients-and-developer-tools/cline) ，请在设置界面单击`MODEL CONFIGURATION`，并勾选 **Enable R1 messages format**。

### The image size is not supported for the data inspection.

**原因**：

- 传入千问VL模型的图像尺寸（长度和宽度）不符合模型的要求。
- 输出图像大小超出限制（10MB）。

**解决方案**：

- 图像尺寸需满足以下要求：图像的宽度和高度均不小于10像素。
- 宽高比不应超过200:1或1:200

调整生成图像的参数。

### Required parameter(data\_sources) missing or invalid, please check the request parameters.

**原因**： 调用 SubmitIndexJob 接口时返回此错误，原因是调用 CreateIndex 接口时未指定必传参数`SourceType`。

**解决方案**： 基于给定文档创建知识库时，此参数需传入`DATA_CENTER_FILE`；基于给定类目创建知识库时，此参数需传入`DATA_CENTER_CATEGORY`。详见 CreateIndex 文档。

### Wrong Content-Type of multimodal url

**原因**：URL请求的响应头信息`Content-Type`字段不正确。

千问VL模型支持的Content Type为：image/bmp、image/bmp、image/icns、image/x-icon、image/jpeg、image/jp2、image/png、image/sgi、image/tiff、image/webp。详情可参见[千问VL模型支持的图像](/resources/faq-images-videos)。

**解决方案**：

查看`Content-Type`字段

1. 打开浏览器（如Chrome或Firefox）。
2. 打开开发者工具（通常按F12或右键选择“检查”）。
3. 切换到Network标签。
4. 将图片的URL输入到地址栏并访问。
5. 找到对应的请求，查看Headers部分，在“响应头”（Response Headers）部分中查找Content-Type字段。

### Field required: image\_url

**原因**： 缺少入参`image_url`。

**解决方案**： 请参考[Emoji 视频生成](/api-reference/video-generation/emoji-video/create-task)，传入`image_url`参数。

### Field required: driven\_id

**原因**： 缺少入参`driven_id`。

**解决方案**： 请参考[Emoji 视频生成](/api-reference/video-generation/emoji-video/create-task)，传入`driven_id`参数。

### Invalid ext\_bbox

**原因**： 输入`ext_bbox`参数无效。

**解决方案**： 请参考[Emoji 视频生成](/api-reference/video-generation/emoji-video/create-task)，传入正确的`ext_bbox`。

### Driven not exist: driven\_id

**原因**：输入`driven_id`不存在。

**解决方案**： 请参考[Emoji 视频生成](/api-reference/video-generation/emoji-video/create-task)，传入正确的`driven_id`。

### Text request limit violated, expected 1.

**原因**：在调用CosyVoice语音合成的[WebSocket API](/api-reference/speech-synthesis/cosyvoice/websocket-api)时，将`enable_ssml`设为`true`后多次发送continue-task指令。

**解决方案**： `enable_ssml`设为`true`后，只允许发送一次continue-task指令。

### SSML text is not supported at the moment!

**原因**：使用CosyVoice语音合成功能时，当前模型或音色不支持 SSML，或未正确启用 SSML 功能。

**解决方案**：请根据[限制与约束](/developer-guides/speech/realtime-streaming)进行排查

### At least one of 'lyrics' or 'prompt' must be provided.

**原因**： 使用Fun-Music模型时，请求中未提供`lyrics`或`prompt`参数。

**解决方案**： 请在请求中至少提供`lyrics`或`prompt`参数之一。

### Lyrics content is illegal and cannot be used for music generation.

**原因**： 使用Fun-Music模型时，歌词内容检测未通过，可能包含侵权内容。

**解决方案**： 请修改歌词内容，确保不包含侵权或违规内容后重试。

## 400-invalid\_request\_error-invalid\_value

### -1 is lesser than the minimum of 0 - 'seed'/'seed' must be Integer

**原因**： 使用OpenAI兼容协议时，`seed` 参数设置未在 \[0, 2^31-1]的范围内。

**解决方案**： 将`seed`参数设置在 \[0, 2^31-1]的范围内。

## 400-invalid\_request\_error

### you must provide a model parameter.

**原因**： 请求时没有提供 `model` 参数。

**解决方案**： 请在请求中添加`model`参数。

## 400-InvalidParameter.NotSupportEnableThinking

### The model xxx does not support enable\_thinking.

**原因**： 当前使用的模型不支持设定参数 `enable_thinking`。

**解决方案**： 请求时去掉`enable_thinking`参数，或使用支持思考模式的模型。

## 400-invalid\_value

### The requested voice 'xxx' is not supported.

**原因**： 在进行Qwen-TTS实时语音合成时，选用的音色是通过Qwen-TTS声音复刻功能生成的，但二者使用的模型不同。

**解决方案**： 请检查声音复刻时的请求参数`target_model`和语音合成时的请求参数`model`是否一致。

## 400-Arrearage

### Access denied, please make sure your account is in good standing.

**原因**： API Key 所属的千问AI平台账号存在欠费，导致访问被拒绝。

**解决方案**：前往[账单概览](https://platform.qianwenai.com/home/billing/overview)查看是否欠费：

- 未欠费：请确认该 API Key 是否属于当前账号。如果账号不存在欠费的情况，可能账户出现异常，详情请联系客服进一步排查。
- 欠费：请及时充值。充值后，系统余额可能存在延迟，请稍等后重试。

### API provider returned a billing error — your API key has run out of credits or has an insufficient balance. Check your provider's billing dashboard and top up or switch to a different API key.

**原因**：通过 OpenClaw 等第三方客户端调用千问AI平台时，若底层账号欠费或余额不足，客户端会将服务端返回的计费类错误聚合为此英文提示。其底层对应的千问AI平台服务端错误码为 Arrearage（即上文 **Access denied, please make sure your account is in good standing.** ），并非客户端本身的计费问题。

**解决方案**：前往[费用与成本](https://platform.qianwenai.com/home/billing/overview)查看账号是否欠费：欠费请及时充值（充值后系统余额可能存在延迟，请稍候后重试）；未欠费请确认调用所用的 API Key 是否属于当前账号。

### isv.OUT\_OF\_SERVICE

**原因**： 千问AI平台账号余额不足，导致服务被暂停。其底层原因与本节的 Arrearage（`Access denied, please make sure your account is in good standing.`）一致，均为账户欠费。

**解决方案**：前往[费用与成本](https://platform.qianwenai.com/home/billing/overview)为千问AI平台账号充值，余额充足后服务自动恢复。

## 400-DataInspectionFailed/data\_inspection\_failed

### Input or output data may contain inappropriate content. / Input data may contain inappropriate content. / Output data may contain inappropriate content.

**原因**： 输入或者输出包含疑似敏感内容被绿网拦截。

**解决方案**： 请修改输入内容后重试。

### Input xxx data may contain inappropriate content.

**原因**： 输入数据（如提示词或图像）可能包含敏感内容。 **解决方案**： 内容合规检查，请修改输入后重试。

### Qwen rejected the input image before model inference; no actual ad/porn/OCR result was produced.

**原因**：输入图片在进入模型推理前，被内容安全前置检测（绿网）判定为疑似包含敏感或违规内容而拦截。模型未对该图片进行推理，因此不会返回任何识别、OCR 或分析结果。此为对多模态输入图片的安全合规前置校验，与上文输入内容被绿网拦截属同一内容安全机制。

**解决方案**：请更换或修改输入图片后重试；若确认图片内容合规仍被持续拦截，可提交工单进一步核实。

## 400-APIConnectionError

### Connection error.

**原因**： 本地网络问题，通常是因为开启了代理。

**解决方案**： 请关闭或者重启代理。

### The operation was canceled. / Connection reset

**原因**： 客户端设置的超时时间过短或网络波动，可能导致请求被取消（如`The operation was canceled`）或连接重置（如`Connection reset`）。

**解决方案**：

- 适当放宽客户端超时配置（如调整至 50 秒以上）。
- 使用`curl`命令测试网络连通性，以排除本地网络问题。

## 400-InvalidFile.DownloadFailed

### The audio file cannot be downloaded.

**原因**： 使用[语音识别（Paraformer）](/api-reference/speech-recognition/paraformer-realtime/websocket-api)录音文件识别，待识别文件下载失败。

**解决方案**： 请检查待识别音频文件URL是否可通过公网访问。

## 400-InvalidFile.AudioLengthError

### Audio length must be between 1s and 300s.

**原因**： 音频长度不符合要求。

**解决方案**： 请确保音频时长在\[1, 300]秒范围内

### Audio length must be between 1s and 180s.

**原因**： 音频长度不符合要求。

**解决方案**： 请确保音频时长在\[1, 180]秒范围内。

## 400-InvalidFile.NoHuman

### The input image has no human body. Please upload other image with single person.

**原因**： 输入图片中没有人或未检测到人脸。

**解决方案**： 请上传单人照。

## 400-InvalidFile.BodyProportion

### The proportion of the detected person in the picture is too large or too small, please upload other image.

**原因**： 上传图片中人物占比不符合要求。

**解决方案**： 请上传符合人物占比要求的图片。

## 400-InvalidFile.FacePose

### The pose of the detected face is invalid, please upload other image with whole face and expected orientation.

**原因**： 上传图片中人物面部姿态不符合要求（要求面部可见，头部朝向无严重偏移）。

**解决方案**： 请上传符合要求的图片。

### The pose of the detected face is invalid, please upload other image with the expected oriention.

**原因**： 上传图片中人物面部姿态不符合要求（要求面部朝向无严重偏移）。

**解决方案**： 请确保图片中人脸朝向无偏斜。

### The pose of the detected face is invalid, please upload other image with the expected orientation.

**原因**： 上传图片中人物面部姿态不符合要求（要求面部朝向无严重偏移）。

**解决方案**： 请确保图片中人脸朝向无偏斜。

## 400-InvalidFile.Resolution

### The image resolution is invalid, please make sure that the largest length of image is smaller than 7000, and the smallest length of image is larger than 400.

**原因**： 上传图像大小不符合要求。

**解决方案**： 上传图片的分辨率不得高于7000*7000，且不得低于400*400。

### The image resolution is invalid, please make sure that the largest length of image is smaller than 4096, and the smallest length of image is larger than 224.

**原因**： 上传图像大小不符合要求。

**解决方案**： 上传图片的分辨率最长边小于 4096 像素，且最短边大于 224 像素。

### The image resolution is invalid, please make sure that the largest length of image is smaller than xxx, and the smallest length of image is larger than yyy.

**原因**： 上传图像大小不符合要求。

**解决方案**： 上传图片的分辨率不得高于xxx*xxx，且不得低于yyy*yyy。

### The image resolution is invalid, please make sure that the aspect ratio is smaller than xxx, and largest length of image is smaller than yyy.

**原因**： 上传图像大小不符合要求。

**解决方案**： 上传图片的长宽比必须小于xxx，且分辨率不得高于yyy\*yyy。

### Invalid video resolution. The height or width of video must be xxx \~ yyy.

**原因**： 视频分辨率不符合要求。

**解决方案**： 视频边长需介于xxx-yyy之间。

## 400-InvalidFile.FPS

### Invalid video FPS. The video FPS must be 15 \~ 60.

**原因**： 视频帧率不符合要求。

**解决方案**： 视频帧率需介于15-60fps之间。

## 400-InvalidFile.Value

### The value of the image is invalid, please upload other clearer image.

**原因**： 上传图片过暗不符合要求。

**解决方案**： 请确保图片中人脸清晰。

## 400-InvalidFile.FrontBody

### The pose of the detected person is invalid, please upload other image with the front view.

**原因**： 上传图片中人物背身不符合要求。

**解决方案**： 请确保图片中人物正面朝向镜头。

## 400-InvalidFile.FullFace

### The pose of the detected face is invalid, please upload other image with whole face.

**原因**： 上传图片中人物面部姿态不符合要求（要求面部可见）。

**解决方案**： 请确保图片中人脸完整无遮挡。

## 400-InvalidFile.FaceNotMatch

### There are no matched face in the video with the provided reference image.

**原因**： 参考图与视频人脸匹配失败。

**解决方案**： 详情参见[VideoRetalk视频生成](/api-reference/video-generation/video-retalk/create-task)。

## 400-InvalidFile.Content

### The first frame of input video has no human body. Please choose another clip.

**原因**： 视频首帧需要有人。

**解决方案**： 请选择包含人体的视频片段。

### The human is too small in the first frame of input video. Please choose another clip.

**原因**： 视频首帧人物过小。

**解决方案**： 请选择首帧人物占比较大的视频。

### The human is not clear in the first frame of input video. Please choose another clip.

**原因**： 视频首帧人物不清晰。

**解决方案**： 请选择首帧人物清晰的视频。

### The input image has no human body or multi human bodies. Please upload other image with single person.

**原因**： 输入图片中没有人或有多人。

**解决方案**： 请上传单人照。

### The input image has no human body or has unclear human body. Please upload other image.

**原因**： 输入图片中人体不完整或者没有人体。

**解决方案**： 请上传包含完整清晰人体的图片。

### The input image has multi human bodies. Please upload other image with single person.

**原因**： 输入图片中有多人。

**解决方案**： 请上传单人照。

## 400-InvalidFile.FullBody

### The human is not fullbody in the first frame of input video. Please choose another clip.

**原因**： 视频首帧人物不完整。

**解决方案**： 需露出人物全身。

### The pose of the detected person is invalid, please upload other image with whole body, or change the ratio parameter to 1:1。

**原因**： 上传图片中人物姿态不符合要求。

**解决方案**： 请上传符合要求的图片，头像照要求头部完整可见，半身照要求髋部以上完整可见，或者调整图像宽高比为1:1。

## 400-InvalidFile.BodyPose

### The pose of the detected person is invalid, please upload other image with whole body and expected orientation.

**原因**： 单人的动作不符合要求。

**解决方案**： 请上传符合要求的图片，要求肩膀及踝部可见，非背身，非坐姿，人物朝向无严重偏移。

## 400-InvalidFile.Size

### Invalid file size. The video file size must be less than 200MB, and the audio file size must be less than 15MB.

**原因**： 文件大小不符合要求。

**解决方案**： 视频文件必须小于200MB，音频文件必须小于15MB。

### Invalid file size, The image file size must be smaller than 5MB.

**原因**： 文件大小不符合要求。

**解决方案**： 图片文件必须小于5MB。

### Invalid file size. The video/audio/image file size must be less than xxxMB.

**原因**： 文件大小不符合要求。

**解决方案**： 视频/音频/图像文件必须小于指定的MB数。

## 400-InvalidFile.Duration

### Invalid file duration. The file duration must be xxx s \~ yyy s.

**原因**： 文件时长不符合要求。

**解决方案**： 视频/音频文件时长需要介于xxx-yyy s之间。

## 400-InvalidFile.ImageSize

### The size of image is beyond limit.

**原因**： 图片大小超出限制。

**解决方案**： 要求图片长宽比例不大于2，且最长边不大于4096。

## 400-InvalidFile.AspectRatio

### Invalid file ratio. The file aspect ratio (height/width) must be between 3:1 and 1:3.

**原因**： 文件长宽比不符合要求。

**解决方案**： 视频文件长宽比需要介于3:1到1:3之间。

### Invalid file ratio. The file aspect ratio (height/width) must be between 2.0 and 0.5.

**原因**： 文件长宽比不符合要求。

**解决方案**： 图片文件宽高比必须在2.0到0.5之间。

## 400-InvalidFile.Openerror

### Invalid file, cannot open file as video/audio/image.

**原因**： 文件无法打开。

**解决方案**： 请检查文件是否损坏或格式是否正确。

## 400-InvalidFile.Template.Content

### Invalid template content.

**原因**： 动作模板无权限，或模板内容不符合要求。

**解决方案**： 请检查模板权限和内容。

## 400-InvalidFile.Format

### Invalid file format，the request file format is one of the following types: MP4, AVI, MOV, MP3, WAV, AAC, JPEG, JPG, PNG, BMP, and WEBP.

**原因**： 文件格式不符合要求。

**解决方案**： 使用符合要求的文件：视频支持mp4、avi、mov；音频支持mp3, wav, aac；图片支持jpg, jpeg, png, bmp, webp。

## 400-InvalidFile.MultiHuman

### The input image has multi human bodies. Please upload other image with single person.

**原因**： 输入图片中有多人。

**解决方案**： 请上传单人照。

## 400-InvalidPerson

### The input image has no human body or multi human bodies. Please upload other image with single person.

**原因**： 输入图片中没有人或有多人。

**解决方案**： 请上传单人照。

## 400-InvalidParameter.DataInspection

### Unable to download the media resource during the data inspection process.

**原因**： 下载图片或音频文件超时。

**解决方案**： 如果从海外发起调用，由于跨境网络不稳定，可能会导致下载资源超时。请将文件存储到国内的 [OSS](https://help.aliyun.com/product/31815.html) 中，再发起模型调用。也可以使用[临时存储空间](/api-reference/platform-api/file/upload-file)上传文件。

## 400-FlowNotPublished

### Flow has not published yet, please publish flow and try again.

**原因**： 流程未发布。

**解决方案**： 请发布流程后再重试。

## 400-InvalidImage.ImageSize

### The size of image is beyond limit.

**原因**： 图片大小超出限制。

**解决方案**： 要求图片长宽比例不大于2，且最长边不大于4096。

## 400-InvalidImage.NoHumanFace

### No human face detected.

**原因**： 未检测到人脸（仅生成任务异步查询接口）。

**解决方案**： 请上传包含清晰人脸的图片。

## 400-InvalidImageResolution

### The input image resolution is too large or small.

**原因**： 输入图像分辨率过大或过小。

**解决方案**： 图像分辨率不低于256×256像素，不超过5760×3240像素。

## 400-InvalidImageFormat

### The input image is in invalid format.

**原因**： 图片格式不符合要求。

**解决方案**： 使用JPEG、PNG、JPG、BMP、WEBP格式的图片。

## 400-InvalidURL

### Invalid URL provided in your request.

**原因**： URL 无效。

**解决方案**： 使用有效的 URL。

### Required URL is missing or invalid, please check the request URL.

**原因**： 输入的URL无效或缺失。

**解决方案**： 请提供正确的URL。

### The request URL is invalid, make sure the url is correct and is an image.

**原因**： 输入的URL无效。

**解决方案**： 请确保URL正确且指向一个图像文件。

### The input audio is longer than xxs.

**原因**： 输入的音频文件超过最大时长xx秒。

**解决方案**： 请将音频文件裁剪至xx秒以内。

### File size is larger than 15MB.

**原因**： 输入的音频文件超过最大限制15MB。

**解决方案**： 请将音频文件压缩至15MB以内。

### File type is not supported. Allowed types are: .wav, .mp3.

**原因**： 输入的音频格式不合规。

**解决方案**： 当前仅支持wav、mp3格式。

### The request URL is invalid, please check the request URL is available and the request image format is one of the following types: JPEG, JPG, PNG, BMP, and WEBP.

**原因**： 图片不可访问或下载的文件格式不支持。

**解决方案**： 请确保URL可访问，且图片格式为JPEG, JPG, PNG, BMP或WEBP。

## 400-InvalidImage.FileFormat

### Invalid image type. Please ensure the uploaded file is a valid image.

**原因**：图片文件格式不支持。

**解决方案**：使用JPG、JPEG、PNG、BMP、WEBP格式的图片。

## 400-InvalidURL.ConnectionRefused

### Connection to xxx refused, please provide available URL.

**原因**： 下载被拒绝。

**解决方案**： 请提供可用的URL。

## 400-InvalidURL.Timeout

### Download xxx timeout, please check network connection.

**原因**： 下载超时。

**解决方案**： 请检查网络连接。

## 400-BadRequestException

### Invalid part type.

**原因**： 仅在Qwen-Long模型的对话场景中，用户上传了Qwen-Long模型暂不支持的文件类型。

**解决方案**： 请上传Qwen-Long支持的文件类型。

## 400-BadRequest.EmptyInput

### Required input parameter missing from request.

**原因**： 请求时未添加`input`参数。

**解决方案**： 请在请求中添加`input`参数。

## 400-BadRequest.EmptyParameters

### Required parameter "parameters" missing from request.

**原因**：请求时未添加 `parameters`参数。

**解决方案**： 请在请求中添加`parameters`参数。

## 400-BadRequest.EmptyModel

### Required parameter "model" missing from request.

**原因**： 请求时未提供 `model`参数。

**解决方案**： 请在请求中添加`model`参数。

## 400-BadRequest.IllegalInput

### The input parameter requires json format.

**原因**： 入参格式不符合API要求的JSON格式。

**解决方案**： 请检查入参格式，确保为标准的JSON。

## 400-BadRequest.InputDownloadFailed

### Failed to download the input file: xxx.

**原因**： 下载输入文件失败，可能是由于下载超时、下载失败或者文件超过限额大小。

**解决方案**： 请根据详细错误信息`xxx`排查。

### Failed to download the input file.

**原因**： 使用Qwen-TTS声音复刻时，服务器下载待复刻音频失败。

**解决方案**： 请检查音频文件是否可以正常下载，若能下载，请检查音频文件大小是否超出限制（超过10MB）。

## 400-BadRequest.UnsupportedFileFormat

### File format unsupported.

**原因**：[CosyVoice声音复刻](/api-reference/speech-synthesis/voice-cloning/overview)时，上传的音频格式不符合模型要求。

**解决方案**： 音频格式需为 WAV（16bit）、MP3 或 M4A。需要注意的是，不能仅凭文件后缀名判断格式，例如，后缀名为 `.mp3` 的文件可能是其他格式（如 Opus）。建议通过工具（如ffprobe、mediainfo）或命令（如Linux/macOS的file命令）确认音频文件的实际编码格式，以确保符合要求。

### Input file format is not supported.

**原因**： 输入文件的格式不受支持。

**解决方案**： 请使用支持的文件格式。

## 400-BadRequest.TooLarge

### Payload Too Large.

**原因**： 文件大小超出限制。

**解决方案**：

- “purpose”参数为“file-extract”时文档不能超150MB、图片不能超20MB。
- “purpose”参数为“batch”时，文件不能超500MB。 请拆分并分批[上传文件](/api-reference/platform-api/file/upload-file)。

## 400-BadRequest.ResourceNotExist

### The Required resource not exist.

**原因**：

- [CosyVoice声音复刻](/api-reference/speech-synthesis/voice-cloning/overview)更新、查询或删除接口调用时，对应音色不存在。
- 使用[定制热词（Paraformer）](/api-reference/speech-recognition/paraformer-realtime/websocket-api)或[定制热词（Gummy）](/developer-guides/speech/realtime-multimodal-speech)时，更新、查询或删除接口调用的热词资源不存在。

## 400-Throttling.AllocationQuota

### 您当前的配额为xxx

**原因**： [CosyVoice声音复刻](/api-reference/speech-synthesis/voice-cloning/overview)音色数量已达限额。

**解决方案**： [删除](/api-reference/speech-synthesis/voice-cloning/delete-voice)部分音色。

### Free allocated quota exceeded.

**原因**： 使用定制热词（Paraformer）或定制热词（Gummy）时，热词数目已超过上限（每个账号默认10个，Paraformer和Gummy共用）。

**解决方案**： 删除部分热词。

### Maximum voice storage limit exceeded, please delete existing voices.

**原因**： 使用Qwen-TTS声音复刻时，超过主账号可用的音色数目上限。

**解决方案**： 请[删除](/api-reference/speech-synthesis/voice-design/delete-voice)一部分音色。

## 400-InvalidGarment

### Missing clothing image.Please input at least one top garment or bottom garment image.

**原因**： 缺少服饰图片。

**解决方案**： 请至少提供一张上装 (top\_garment\_url) 或下装 (bottom\_garment\_url) 的图片。

## 400-InvalidSchema

### Database schema is invalid for text2sql.

**原因**： 未输入数据库Schema信息。

**解决方案**： 请输入数据库Schema信息。

## 400-InvalidSchemaFormat

### Database schema format is invalid for text2sql.

**原因**： 输入数据表信息格式异常。

**解决方案**： 请检查并修正数据表信息的格式。

## 400-Audio.AudioShortError

### valid audio too short!

**原因**： 用于[CosyVoice声音复刻](/api-reference/speech-synthesis/voice-cloning/overview)的音频有效时长过短。

**解决方案**：音频时长应尽量控制在 10\~15 秒之间。录音时请确保朗读连贯，并包含至少一段超过 5 秒的连续语音。

## 400-Audio.AudioSilentError

### silent audio error.

**原因**： [CosyVoice声音复刻](/api-reference/speech-synthesis/voice-cloning/overview)音频文件为静音或非静音长度过短。

**解决方案**： 用于声音复刻的音频时长应尽量控制在 10\~15 秒之间，并包含至少一段超过 5 秒的连续语音。

## 400-InvalidInputLength

### The image resolution is invalid, please make sure that the largest length of image is smaller than 4096, and the smallest length of image is larger than 150. and the size of image ranges from 5KB to 5MB.

**原因**： 图片尺寸或文件大小不符合要求。

**解决方案**： 请参见[输入图片要求](/resources/faq-images-videos)。

## 400-FaqRuleBlocked

### Input or output data is blocked by faq rule.

**原因**： 命中FAQ规则干预模块。

## 400-ClientDisconnect

### Client disconnected before task finished!

**原因**： 任务结束前，客户端主动断开了连接。该报错信息在使用语音合成或识别相关服务时产生。

**解决方案**： 请检查代码，不要在任务结束前断开和服务端的连接。

## 400-ServiceUnavailableError

### Role must be user or assistant and Content length must be greater than 0.

**原因**： 输入内容长度为0或`role`不正确。

**解决方案**： 请检查输入内容长度大于0，并确保参数格式（如`role`）符合API文档的要求。

## 400-IPInfringementSuspect

### Input data is suspected of being involved in IP infringement.

**原因**： 输入数据（如提示词或图像）涉嫌知识产权侵权。

**解决方案**： 内容合规检查，请检查输入，确保不包含引发侵权风险的内容。

## 400-UnsupportedOperation

### The operation is unsupported on the referee object.

**原因**： 关联的对象不支持该操作。

**解决方案**： 请检查操作对象和操作类型是否匹配。

### The fine-tune job can not be deleted because it is succeeded,failed or canceled.

**原因**： 无法删除该微调任务，因为其状态已是“成功”、“失败”或“已取消”。

**解决方案**： 只有处于特定状态的任务才能被删除，请勿删除已终结状态的任务。

## 400-CustomRoleBlocked

### Input or output data may contain inappropriate content with custom rule.

**原因**： 请求或响应内容没有通过自定义策略。

**解决方案**： 请检查内容或调整自定义策略。

## 400-Audio.PreprocessError

### Audio preprocess error.

**原因**： 使用Qwen-TTS声音复刻时，待复刻音频预处理异常，可能的原因为：`text`参数内容与音频文本差别过大、有效人声过短、无声音等。

**解决方案**： 请调整`text`参数的内容，若调整后无效，请参照录音操作指南重新录制音频。

### No segments meet minimum duration requirement

**原因**： 使用Qwen-TTS声音复刻时，待复刻音频有效人声过短。

**解决方案**： 请参照录音操作指南重新录制音频。

## 400-BadRequest.VoiceNotFound

### Voice '%s' not found.

**原因**： 使用Qwen-TTS声音复刻时，调用删除音色接口时，音色已删除或音色不存在。

**解决方案**： 请检查传入的`voice`参数是否正确。

## 400-Audio.DecoderError

### Decoder audio file failed.

**原因**： 使用Qwen-TTS声音复刻时，待复刻音频解码失败。/ CosyVoice声音复刻音频文件解码失败。

**解决方案**： 请检查音频文件是否损坏，并确保音频满足音频文件格式要求（如Qwen-TTS）或为 WAV（16bit）、MP3 或 M4A（如CosyVoice）。

## 400-Audio.AudioRateError

### File sample rate unsupported.

**原因**： 使用Qwen-TTS声音复刻或CosyVoice声音复刻时，待复刻音频采样率不符合要求。

**解决方案**： 采样率需大于等于24000 Hz。

## 400-Audio.DurationLimitError

### Audio duration exceeds maximum allowed limit.

**原因**： 使用Qwen-TTS声音复刻时，待复刻音频过长。

**解决方案**： 音频不得超过60秒。

## 401-InvalidApiKey/invalid\_api\_key

### Invalid API-key provided. / Incorrect API key provided.

**原因**： API Key 填写错误。

**解决方案**： 常见错误原因及修正方式如下：

- **读取错误的环境变量**，**错误写法**：`api_key=os.getenv("sk-xxx") `，系统将尝试读取名为 `sk-xxx` 的环境变量，而非将 `sk-xxx` 当作密钥。
- **正确写法**：**若已配置环境变量**：请写为`api_key=os.getenv("DASHSCOPE_API_KEY")`；
  确保运行前已设置`DASHSCOPE_API_KEY`环境变量。
- **若未配置环境变量**：请写为`api_key = "sk-xxx"`。
  此方式便于调试，请勿用于生产环境。

**填写错误**：千问AI平台的 API Key 以 `sk-ws-` 开头（早期创建的 Key 以 `sk-` 开头），请确认未误填其他模型提供商的密钥，且复制时未包含多余空格或换行符。

**工具适配问题**：第三方工具未正确适配（如[Dify](/developer-guides/clients-and-developer-tools/dify)最新版本插件不稳定导致报错，可尝试安装旧版本千问插件；旧版本[Cline](/developer-guides/clients-and-developer-tools/cline)调用模型时API Provider选择了Alibaba Qwen，应选择OpenAI兼容）。

若以上均不符合，可能是 API Key 被删除，请重新获取并发起调用。

## 401-NOT AUTHORIZED

### Access denied: Either you are not authorized to access this workspace, or the workspace does not exist. Please:\nVerify the workspace configuration.\nCheck your API endpoint settings. Ensure you are targeting the correct environment.

**原因**：

- WorkspaceId值无效，或当前账号不是该业务空间的成员。
- 或者请求的接入地址（服务接入点）有误。

**解决方案**：

- 请确认WorkspaceId值无误且账号已是该业务空间的成员后，再调用接口。
- 请确认接入地址正确。

## 401-invalid access token or token expired

### invalid access token or token expired.

**可能原因**：Token Plan 使用了错误的 Base URL（如按量计费或其他套餐的接入地址）。

**解决方案**：请使用 Token Plan 专属的 Base URL：

- Anthropic 兼容端点：`https://token-plan.cn-beijing.maas.aliyuncs.com/apps/anthropic`
- OpenAI 兼容端点：`https://token-plan.cn-beijing.maas.aliyuncs.com/compatible-mode/v1`

## 403-AccessDenied/access\_denied

### Current user api does not support asynchronous calls.

**原因**： 接口不支持异步调用。

**解决方案**： 请移除请求头中的 `X-DashScope-Async`，或将其值设为 `disable`。

### current user api does not support synchronous calls.

**原因**： 接口不支持同步调用。

**解决方案**： 请在请求头中设置 `X-DashScope-Async: enable`。

### Invalid according to Policy: Policy expired.

**原因**： 在获取临时公网URL时，文件上传凭证已经过期。

**解决方案**： 请重新调用文件上传凭证接口生成新凭证。

### Access denied.

**原因**： 无权访问此模型。可能因该模型需申请权限，或模型免费额度已耗尽且不支持付费使用（如 `deepseek-r1-distill-llama-70b`）。

**使用通用 API Key 调用 Token Plan 专属模型**

**原因**： Token Plan 专属模型（如 `qwen3.8-max-preview`）仅限 Token Plan 订阅用户使用专属 API Key（以 `sk-sp-` 开头）配合 Token Plan 专属 Base URL 调用。使用通用 API Key（以 `sk-` 开头）调用这些模型会返回 403 `access_denied` 错误。

**解决方案**： 请前往千问AI平台控制台，在**我的订阅**的 API Key 区域获取 Token Plan 专属 API Key 与专属 Base URL，并确认同时更新了两者，具体配置方法请参见[快速开始](/token-plan/quickstart)。若 API Key 与 Base URL 不匹配（例如专属 API Key 搭配通用 Base URL），将返回 401 鉴权错误，请参见本文档 **401-InvalidApiKey/invalid\_api\_key**。

**解决方案**： 请前往[模型市场](https://www.qianwenai.com/models)，在对应模型卡片下方单击**立即申请**发起测试申请。或改用其他模型，例如千问或万相的文生图模型替代 Flux。

## 403-AccessDenied.Unpurchased

### Access to model denied. Please make sure you are eligible for using the model.

**原因**： 未开通千问AI平台服务。

**解决方案**： 请参照以下流程注册并开通千问AI平台服务。

1. **注册账号**：千问AI平台账号即阿里云账号。如果没有阿里云账号，请访问[千问AI平台](https://platform.qianwenai.com/)注册。详见[账号与访问](/resources/faq-account)。
2. **开通服务**：首次登录千问AI平台时，阅读并同意《千问AI平台服务协议》和《隐私政策》后，即自动开通服务。如果未弹出服务协议，则表示您已开通。

如果控制台提示需要认证，请点击提示条完成认证。

## 403-Model.AccessDenied

### Model access denied.

**原因**： 无权限调用对应的标准模型或自定义模型。

**解决方案**：

- **调用标准模型**：使用子业务空间的API-KEY调用标准模型（例如`qwen-plus`）时，子业务空间需具备该模型的调用权限。详见[模型调用授权](/developer-guides/administration/workspace)。
- **调用自定义模型**：自定义模型部署成功后，仅能用其所在业务空间的API-KEY调用，且无需模型调用授权。

## 403-App.AccessDenied

### App access denied.

**原因**： 无权限访问应用或者模型。

**解决方案**：

- 仔细确认对访问的业务空间和子账号做了访问授权。
- 仔细检查应用是否发布。
- 仔细核实传入的APP ID、API KEY是否正确。
- 如果是Claude Code报错，请使用默认业务空间的API Key。
- 若上述建议都正确，建议刷新数据重新发布再调用，或尝试重新创建智能体。

## 403-Workspace.AccessDenied

### Workspace access denied.

**原因**： 无权限访问业务空间的应用或者模型。

**解决方案**：

- 如果调用子业务空间的应用，请参考[业务空间](/developer-guides/administration/workspace)。
- 如果调用子业务空间的模型，请参考[子业务空间的模型调用](/developer-guides/administration/workspace)。
- 也可改为使用主账号的API KEY，主账号具有所有业务空间的权限。

## 403-Endpoint.AccessDenied

### Workspace endpoint access denied.

**原因**：可能调用了已下线的模型（例如 `qwen-max-2025-01-25` 等历史快照版本）。模型下线后，对应的调用端点不再提供服务，会返回该报错。

**解决方案**：

- 确认所调用的模型是否已下线。
- 若模型已下线，请改用其推荐的替代模型重新调用。

## 403-AllocationQuota.FreeTierOnly

### The free tier of the model has been exhausted. If you wish to continue access the model on a paid basis, please disable the "use free tier only" mode in the management console.

**原因一**：全新未认证用户免费额度用尽后发起请求。

**解决方案**：完成认证并充值后再进行调用。

**原因二**：用户开启了[免费额度用完即停](/resources/free-quota)，且免费额度耗尽后发起请求。

控制台显示的免费额度为分钟级更新（需手动刷新页面）。

**解决方案**：

- 如需继续以付费方式调用，可随时关闭[免费额度用完即停](/resources/free-quota)开关，无需等到免费额度用完；关闭后即可按量付费继续调用。

## 404-ModelNotFound/model\_not\_found

### The provided model xxx is not supported by the Batch API.

**原因**： 当前模型暂不支持 Batch 调用，或者可能存在模型名称拼写错误。

**解决方案**： 请参考[OpenAI兼容-Batch（文件输入）](/developer-guides/text-generation/batch)，确认支持 Batch调用的模型及其正确名称。

### Model can not be found. / The model xxx does not exist. / The model xxx does not exist or you do not have access to it.

**原因**： 当前访问的模型不存在，或您还未开通千问AI平台服务。

**解决方案**：

- 请对照模型列表中的模型名称，检查您输入的模型名称（参数`model`的取值）是否正确。
- 请前往模型市场开通模型服务。
- 如果您使用**专属部署端点**调用模型，出现 ModelNotFound 时还需检查以下两点：
  1. **确认使用部署名称**：专属部署端点的`model`参数应填写部署名称（model code），而非模型名称。部署名称可在千问AI平台控制台的**模型部署**页面查看，格式类似`qwen3.5-flash-2026-02-23-9439a8e1eafa`。使用模型名称调用专属部署端点，或在标准 API 端点上使用部署名称，均会返回`model_not_found`。
  2. **区分调用方式**：通用调用使用标准 API 端点和模型名称，专属部署调用使用专属部署端点 URL 和部署名称，两者不可混用。通用调用与专属部署调用的 API-KEY 也可能不同，混用会导致`invalid_api_key`认证错误。

## 404-model\_not\_supported

### Unsupported model xxx for OpenAI compatibility mode.

**原因**： 当前模型不支持以 OpenAI 兼容方式接入。

**解决方案**： 请您使用DashScope原生方式调用。

## 404-WorkSpaceNotFound

### WorkSpace can not be found.

**原因**： 业务空间不存在。

## 404-NotFound

### Not found!

**原因**：

- 要查询/操作的资源不存在。
- 使用定制热词时，传入的热词ID无效或对应热词不存在。

**解决方案**：

- 请检查要查询/操作的资源ID是否错误。
- 检查热词ID是否正确并参照API文档按照正确的方式进行调用。

### Request path not found.

**原因**： 使用Fun-Music模型时，访问的服务地址不存在。

**解决方案**： 请检查接口路径是否正确及是否存在异常字符。

## 409-Conflict

### Model instance xxx already exists, please specify a suffix.

**原因**： 已存在重名的部署实例。

**解决方案**：为部署的模型指定不同的后缀名。

## 429-Throttling

### Requests throttling triggered.

**原因**： 接口调用触发限流。

**解决方案**： 请降低调用频率或稍后重试。

### Too many fine-tune job in running, please retry later. / Only 20 fine-tune job in running or succeeded allowed per user.

**原因**： 资源的创建触发平台限制。

**解决方案**： 可以删除不再使用的模型。如需提高并发量或保留更多模型，请联系商务经理进行申请提额。

### Too many requests in route. Please try again later.

**原因**：请求过多触发限流。

**解决方案**：请稍后重试。

### All models are temporarily rate-limited. Please try again in a few minutes.

**原因**：当通过客户端（如 Claude Code）调用多个模型时，若所有可用模型均触发 429 限流，客户端会聚合返回此提示。底层对应的千问AI平台服务端错误码为 Throttling.RateQuota 或 Throttling.AllocationQuota。

**解决方案**：

- 等待数分钟后重试，限流会自动解除。
- 降低请求并发数，避免短时间内发送过多请求。
- 如需更高调用频率，可参考[限流](/developer-guides/administration/rate-limits)申请提额。

## 429-Throttling.RateQuota/LimitRequests/limit\_requests/ResourceExhausted/Too many requests

### You have exceeded your request limit./Requests rate limit exceeded, please try again later. /You exceeded your current requests list.

**原因**： 调用频率（RPS/RPM）触发限流。

**解决方案**： 请参考[限流](/developer-guides/administration/rate-limits)，控制调用频率。

<Note>
  若单次调用即返回 429，请检查请求头是否设置了 `X-DashScope-Async: enable`。部分模型不支持异步调用，设置该请求头时即使单次请求也会返回 429。请移除 `X-DashScope-Async` 请求头，或将其值设为 `disable`，然后使用同步调用重试。详情请参见本文档中「**403-AccessDenied/access\_denied**」下「**Current user api does not support asynchronous calls.**」条目。
</Note>

## 429-Throttling.BurstRate/limit\_burst\_rate

### Request rate increased too quickly. To ensure system stability, please adjust your client logic to scale requests more smoothly over time.

**原因**：在未达到限流条件时，调用频率骤增，触发系统稳定性保护机制。

**解决方案**：建议优化客户端调用逻辑，采用平滑请求策略（如匀速调度、指数退避或请求队列缓冲），将请求均匀分散在时间窗口内，避免瞬时高峰。

## 429-Throttling.AllocationQuota/insufficient\_quota

### Allocated quota exceeded, please increase your quota limit./ You exceeded your current quota, please check your plan and billing details.

**原因**： 每秒钟或每分钟消耗Token数（TPS/TPM）触发限流。

**解决方案**： 前往[限流](/developer-guides/administration/rate-limits)文档查看模型限流条件并调整调用策略。

可参考[限流FAQ](/developer-guides/administration/rate-limits)避免触发限流。

### Too many requests. Batch requests are being throttled due to system capacity limits. Please try again later.

**原因**： Batch请求过多触发限流。

**解决方案**： 暂时无法处理您的请求，请稍后再进行重试。

### Free allocated quota exceeded.

**原因**： 免费额度已到期或耗尽，且该模型暂不支持按量计费。

**解决方案**： 使用其它模型替换，例如：千问Audio模型额度耗尽，可使用[非实时（Qwen-Omni）](/api-reference/real-time-multimodal/realtime-python-sdk)模型。

### Maximum voice-clone voice limit exceeded.

**原因**： 使用Qwen-TTS声音复刻时，超过主账号可用的音色数目上限。

**解决方案**： 请[删除](/api-reference/speech-synthesis/voice-design/delete-voice)一部分音色。

## 429-Throttling.Concurrency

### Too many concurrent requests.

**原因**： 当前并发请求数超出平台动态分配的上限。

**解决方案**： 等待片刻后重试即可。平台会根据整体资源负载动态调整并发上限，高峰时段可能触发此限制。如需提升 TPM 额度，可参考[限流](/developer-guides/administration/rate-limits)申请临时限流额度提升。

## 429-CommodityNotPurchased

### Commodity has not purchased yet.

**原因**： 业务空间未订购。

**解决方案**： 请先订购业务空间服务。

## 429-PrepaidBillOverdue

### The prepaid bill is overdue.

**原因**： 业务空间预付费账单到期。

## 429-PostpaidBillOverdue

### The postpaid bill is overdue.

**原因**： 模型推理商品已失效。

## 430-Audio.DecoderError

### Decoder audio file failed.

**原因**：[CosyVoice声音复刻](/api-reference/speech-synthesis/voice-cloning/overview)音频文件解码失败。

**解决方案**：建议通过工具（如ffprobe、mediainfo）或命令（如Linux/macOS的file命令）确认音频文件的实际编码格式，以确保符合要求。

## 430-Audio.FileSizeExceed

### File too large

**原因**： [CosyVoice声音复刻](/api-reference/speech-synthesis/voice-cloning/overview)音频文件大小超限。

**解决方案**： 用于声音复刻的音频文件需10M以内。

## 430-Audio.AudioRateError

### File sample rate unsupported

**原因**： [CosyVoice声音复刻](/api-reference/speech-synthesis/voice-cloning/overview)音频文件采样率不支持。

**解决方案**： 采样率设置为16KHz及以上。

## 430-Audio.AudioSilentError

### Silent file unsupported.

**原因**：[CosyVoice声音复刻](/api-reference/speech-synthesis/voice-cloning/overview)音频文件为静音或非静音长度过短。

**解决方案**： 音频时长应尽量控制在 10\~15 秒之间，并包含至少一段超过 5 秒的连续语音。

## 500-InternalError/internal\_error

### An internal error has occurred, please try again later or contact service support.

**原因**： 内部错误。

**解决方案**：

- 如果您使用[（Qwen-Omni）模型](/api-reference/real-time-multimodal/realtime-python-sdk)，需要使用流式输出方式。
- 如果您使用[CosyVoice声音复刻](/api-reference/speech-synthesis/voice-cloning/overview)，则可能的原因是：音频文件不规范，比如声音本身有问题，有杂音或者声音忽高忽低。请参见[录音操作指南](/api-reference/speech-synthesis/voice-cloning/overview)录音后重试。
- 录音文件URL无法访问，请按照[CosyVoice声音复刻/设计API](/developer-guides/speech/voice-design)中的说明操作后重试。
- 录音文件时长过长。尽量选择10\~15秒的录音。录音时请确保朗读连贯，并包含至少一段超过 5 秒的连续语音。

### Internal server error!

**原因**： 内部算法错误。

**解决方案**： 请稍后重试。

### audio preprocess server error

使用[CosyVoice声音复刻](/api-reference/speech-synthesis/voice-cloning/overview)：

- **原因**：音频文件不规范，比如声音本身有问题，有杂音或者声音忽高忽低。**解决方案**：请参见[录音操作指南](/api-reference/speech-synthesis/voice-cloning/overview)录音后重试。
- **原因**：录音文件URL无法访问，**解决方案**：请按照[CosyVoice声音复刻/设计API](/developer-guides/speech/voice-design)中的说明操作后重试。
- **原因**：录音文件时长过长。**解决方案**：尽量选择10\~15秒的录音。录音时请确保朗读连贯，并包含至少一段超过 5 秒的连续语音。

## 500-InternalError.FileUpload

### oss upload error.

**原因**： 文件上传失败。

**解决方案**： 请检查OSS配置和网络。

## 500-InternalError.Upload

### Failed to upload result.

**原因**： 生成结果上传失败。

**解决方案**： 请检查存储配置或稍后重试。

## 500-InternalError.Algo

### inference internal error.

**原因**： 服务异常。

**解决方案**： 请先尝试重试，排除偶发情况。

### Expecting ',' delimiter: line x column xxx (char xxx)

**原因**： 模型生成的JSON数据不合法，无法正常发起工具调用。

**解决方案**： 建议更换最新的模型或优化提示词后重试。

### Missing Content-Length of multimodal url.

**原因**： URL请求的响应头信息缺失`Content-Length`字段。

**解决方案**： 如果问题无法解决，请尝试使用其他图片链接。

查看`Content-Length`字段

1. 打开浏览器（如Chrome或Firefox）。
2. 打开开发者工具（通常按F12或右键选择“检查”）。
3. 切换到Network标签。
4. 将图片的URL输入到地址栏并访问。
5. 找到对应的请求，查看Headers部分，在“响应头”（Response Headers）部分中查找Content-Length字段

### An error occurred in model serving, error message is: \[Request rejected by inference engine!]

**原因**： 模型服务底层服务器出现错误。

**解决方案**： 请稍后重试。

### An internal error has occurred during algorithm execution.

**原因**： 算法运行时发生错误。

**解决方案**： 请稍后重试。

### Inference error: Inference error.

**原因**： 推理发生错误。

**解决方案**： 请检查输入的图片文件是否有损坏或检查人物图片的质量（需包含完整清晰的人脸）。

### Role must be in \[user, assistant]

**原因**： 在使用Qwen-MT模型时，messages数组中包含了非 `user`角色的消息。

**解决方案**： 请确保messages数组中仅包含一个元素，且该元素必须是用户消息（User Message）。

### Embedding\_pipeline\_Error: xxx

**原因**： 图像或视频预处理出错。

**解决方案**： 请确认上传的图片或视频及请求代码符合要求后重试。

### Receive batching backend response failed!

**原因**： 服务内部错误。

**解决方案**： 请稍后重试。

### \[music]Receive batching backend response failed!

**原因**： 使用Fun-Music模型时，服务超出并发限制。

**解决方案**： 请降低并发请求数量后重试。

### Other kinds of server error.

**原因**： 使用Fun-Music模型时，系统内部未知异常。

**解决方案**： 建议提供请求ID给技术人员排查。

### An internal error has occurred during execution, please try again later or contact service support. / algorithm process error. / inference error. / An internal error occurs during computation, please try this model later.

**原因**： 内部算法错误。

**解决方案**： 请稍后重试。

### list index out of range

**原因**： messages 数组最后一位需为 User Message。

**解决方案**： 请调整`messages`数组的顺序，确保最后一个元素是 `{"role": "user", ...}`。

## 500-InternalError.Timeout

### An internal timeout error has occurred during execution, please try again later or contact service support.

**原因**： 异步任务提交后，在3小时内未返回结果，导致超时。

**解决方案**： 请检查任务执行情况，或联系技术支持。

## 500-SystemError

### A system error has occurred, please try again later.

**原因**： 系统错误。

**解决方案**： 请稍后重试。若您使用千问AI平台应用，请参照示例代码或说明文档，查看是否代码编写有误，若依然无法确定问题，加入[Spring AI Alibaba官网](https://java2ai.com/?spm=4347728f.638c0b20.0.0.23f87982NTcSMy)最下方提供的DING群，联系开发人员进行定位。

## 500-ModelServiceFailed

### Failed to request model service.

**原因**： 模型服务调用失败。

**解决方案**： 请稍后重试。

## 500-RequestTimeOut

### Request timed out, please try again later. / Response timeout! / I/O error on POST request for "[https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions](https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions)": timeout

**原因**：

- 调用大模型时请求超时，超时报错时间为300秒。
- 使用语音识别（Paraformer）时，长时间未向服务器发送音频或者长时间发送静音音频。
- 调用图像生成或编辑模型时，因图片尺寸较大或处理复杂度较高，处理时间超出限制。

**解决方案**：

- 通过流式输出方式发起请求，具体操作请参见[流式输出](/developer-guides/run-and-scale/streaming)。
- 将请求参数`heartbeat`设为`true`或及时结束识别任务。
- 调用图像模型时，可尝试降低图片分辨率、简化编辑需求，或稍后重试。

调用千问模型时，响应体中会将已生成的内容返回，不再报超时错误。详情请参见[文本生成](/developer-guides/getting-started/text-generation-models)。

## 500-ResponseTimeout

### Response stream timeout

**原因**： 使用Fun-Music模型时，内部执行超时。

**解决方案**： 建议进行重试调用。

## 500-InvokePluginFailed

### Failed to invoke plugin.

**原因**： 插件调用失败。

**解决方案**： 请检查插件配置和可用性。

## 500-AppProcessFailed

### Failed to proceed application request.

**原因**： 应用流程处理失败。

**解决方案**： 请检查应用配置和流程节点。

## 500-RewriteFailed

### Failed to rewrite content for prompt.

**原因**： 调用改写prompt的大模型失败。

**解决方案**： 请稍后重试。

## 500-RetrivalFailed

### Failed to retrieve data from documents.

**原因**： 文档检索失败。

**解决方案**： 请检查文档索引和检索配置。

## 500/503-ModelServingError

### Too many requests. Your requests are being throttled due to system capacity limits. Please try again later.

**原因**： 网络资源目前处于饱和状态，暂时无法处理您的请求。

**解决方案**： 请稍后再进行尝试。

## 503-ModelUnavailable

### Model is unavailable, please try again later.

**原因**： 模型暂时无法提供服务。

**解决方案**： 请稍后重试。

## SDK 报错

### error.AuthenticationError: No api key provided. You can set by dashscope.api\_key = your\_api\_key in code, or you can set it via environment variable DASHSCOPE\_API\_KEY= your\_api\_key.

**原因**： 使用DashScope SDK 时未提供API Key。

**解决方案**： 具体配置API Key的方法，请参见[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)。

### openai.OpenAIError: The api\_key client option must be set either by passing api\_key to the client or by setting the OPENAI\_API\_KEY environment variable

**原因**： 使用 OpenAI SDK 时未传入 API Key。

**解决方案**：

- **通过环境变量传入 API Key 来源（推荐）** 将`DASHSCOPE_API_KEY`设为环境变量（参见[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)），初始化`client`时，通过`os.getenv`读取：`client = OpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),...)`
- **明文传入 API Key（仅限测试）** 直接将 API Key 传入`api_key`参数：`client = OpenAI(api_key="sk-...", ...)`**注意**：此方法存在安全风险，请勿用于生产环境。

### Bad Request for url: xxx

**原因**： 使用 Python requests 库时，添加 `response.raise_for_status()`语句导致报错时不返回服务端的具体错误内容。

**解决方案**： 请用 `print(response.json())` 查看服务端返回信息。

### Cannot resolve symbol 'ttsv2'

**原因**： 若您使用[实时语音合成（Qwen-Audio-TTS/CosyVoice）](/api-reference/speech-synthesis/cosyvoice/python-sdk)，出现该问题的原因是DashScope SDK版本过低。

**解决方案**： 请[安装最新版 DashScope SDK](/api-reference/preparation/install-sdk)。

## NetworkError

### NoApiKeyException: Can not find api-key.

**原因**： 环境变量配置没有生效。

**解决方案**： 您可以重启客户端或IDE后重试。更多情况请参考[常见问题](/api-reference/preparation/export-api-key-env)。

### ConnectException: Failed to connect to dashscope.aliyuncs.com

**原因**： 本地网络环境存在异常。

**解决方案**： 请检查本地网络，例如因证书问题导致无法访问 HTTPS，防火墙设置有误等情况。建议您更换网络环境或服务器进行测试。

### InputRequiredException: Parameter invalid: text is null

**原因**：使用[实时语音合成（Qwen-Audio-TTS/CosyVoice）](/api-reference/speech-synthesis/cosyvoice/python-sdk)时未发送待合成文本。

**解决方案**：调用语音合成接口时为 `text` 参数赋值。

### MultiModalConversation.call() missing 1 required positional argument: 'messages'

**原因**：当前使用的DashScope SDK版本过低。

**解决方案**：请[安装最新版 DashScope SDK](/api-reference/preparation/install-sdk)。

## mismatched\_model

### The model 'xxx' for this request does not match the rest of the batch. Each batch must contain requests for a single model.

**原因**： 在单个 Batch 任务中，所有请求都必须选用同一个模型。

**解决方案**： 请根据[OpenAI兼容-Batch（文件输入）](/developer-guides/text-generation/batch)检查您的输入文件。

## duplicate\_custom\_id

### The custom\_id 'xxx' for this request is a duplicate of another request. The custom\_id parameter must be unique for each request in a batch.

**原因**： 在单个 Batch 任务中，每条请求的 ID 必须唯一。

**解决方案**： 请根据[OpenAI兼容-Batch（文件输入）](/developer-guides/text-generation/batch)检查您的输入文件，确保所有请求 ID 不重复。

### Upload file capacity exceed limit. / Upload file number exceed limit.

**原因**： 上传文件失败，当前千问AI平台账号下的存储空间已满或接近满额。

**解决方案**： 可以通过[OpenAI兼容-File](/api-reference/platform-api/file)接口删除不需要的文件以释放空间。当前存储空间支持最大文件数为10000个，总量不超过100 GB。

## WebSocket 报错

### Invalid payload data

**原因**： 使用语音识别/翻译（Gummy）的WebSocket API，发送给服务端的JSON格式有误。

**解决方案**：

1. 检查发送`run-task`指令时，`payload`中是否有“`"input": {}`”，若无，请添加。
2. 确认在最终是否发送了完整的`finish-task`指令，且遵循其格式说明。请勿发送自创内容（如`{ "input": { "end_of_stream": true } }`）。

### The decoded text message was too big for the output buffer and the endpoint does not support partial messages

**原因**： 使用语音识别（Paraformer）或语音识别/翻译（Gummy）的流式语音识别时，服务返回的识别结果数据量过大。

**解决方案**： 请分段发送待识别音频，建议每次发送的音频时长约为100毫秒，数据大小保持在1KB至16KB之间。

### TimeoutError: websocket connection could not established within 5s. Please check your network connection, firewall settings, or server status.

**原因**： 若您使用语音合成（CosyVoice），无法在5秒内建立websocket连接。

**解决方案**： 请检查本地网络、防火墙设置，或更换网络环境或服务器进行测试。

### unsupported audio format:xxx

**原因**： CosyVoice声音复刻时，上传的音频格式不符合模型要求。

**解决方案**： 音频格式需为 WAV（16bit）、MP3 或 M4A。请注意，不能仅凭文件后缀名判断格式，建议通过工具（如ffprobe、mediainfo）或命令（如Linux/macOS的file命令）确认音频文件的实际编码格式。

### internal unknown error

**原因**： CosyVoice声音复刻音频文件格式可能不符合要求。

**解决方案**： 音频格式需为 WAV（16bit）、MP3 或 M4A。建议通过工具（如ffprobe、mediainfo）或命令确认音频文件的实际编码格式。

### Invalid backend response received (missing status name)

**原因**： 使用语音识别（Paraformer）的录音文件识别的RESTful API时，请求参数拼写有误。

**解决方案**： 请参照API文档检查代码。

### NO\_INPUT\_AUDIO\_ERROR

**原因**： 未检测到有效语音。

**解决方案**： 若您使用语音识别（Paraformer）实时语音识别，请通过如下方式排查：

1. 检查是否有音频输入。
2. 检查音频格式是否正确（支持pcm、wav、mp3、opus、speex、aac、amr等）。

### SUCCESS\_WITH\_NO\_VALID\_FRAGMENT

**原因**： 若您使用语音识别（Paraformer）录音文件识别，识别结果查询接口调用成功，但是VAD模块未检测到有效语音。

**解决方案**： 请排查录音文件是否包含有效语音，如果都是无效语音（例如纯静音），则没有识别结果是正常现象。

### ASR\_RESPONSE\_HAVE\_NO\_WORDS

**原因**： 若您使用语音识别（Paraformer）录音文件识别，识别结果查询接口调用成功，但是最终识别结果为空。

**解决方案**： 请排查录音文件是否包含有效语音，或有效语音是否都是语气词且开启了顺滑参数`disfluency_removal_enabled`，导致语气词被过滤。

### FILE\_DOWNLOAD\_FAILED

**原因**： 若您使用语音识别（Paraformer）录音文件识别，待识别文件下载失败。

**解决方案**： 请检查录音文件路径是否正确，以及是否可以通过外网访问和下载。

### FILE\_CHECK\_FAILED

**原因**： 若您使用语音识别（Paraformer）录音文件识别，文件格式错误。

**解决方案**： 请检查录音文件是否是单轨/双轨的WAV格式或MP3格式。

### FILE\_TOO\_LARGE

**原因**： 若您使用语音识别（Paraformer）录音文件识别，待识别文件过大。

**解决方案**： 请检查录音文件大小是否超过2GB，超过则需您对录音文件分段。

### FILE\_NORMALIZE\_FAILED

**原因**： 若您使用语音识别（Paraformer）录音文件识别，待识别文件归一化失败。

**解决方案**： 请检查录音文件是否有损坏，是否可以正常播放。

### FILE\_PARSE\_FAILED

**原因**： 若您使用语音识别（Paraformer）录音文件识别，文件解析失败。

**解决方案**： 请检查录音文件是否有损坏，是否可以正常播放。

### MKV\_PARSE\_FAILED

**原因**： 若您使用语音识别（Paraformer）录音文件识别，MKV解析失败。

**解决方案**： 请检查录音文件是否损坏，是否可以正常播放。

### FILE\_TRANS\_TASK\_EXPIRED

**原因**： 若您使用语音识别（Paraformer）录音文件识别，录音文件识别任务过期。

**解决方案**： TaskId不存在，或者已过期。请重新提交任务。

### REQUEST\_INVALID\_FILE\_URL\_VALUE

**原因**： 若您使用语音识别（Paraformer）录音文件识别，请求file\_link参数非法。

**解决方案**： 请确认`file_url`参数格式是否正确。

### CONTENT\_LENGTH\_CHECK\_FAILED

**原因**： 若您使用语音识别（Paraformer）录音文件识别，`content-length`检查失败。

**解决方案**： 请检查下载待识别录音文件时，HTTP response中的`content-length`与文件实际大小是否一致。

### FILE\_404\_NOT\_FOUND

**原因**： 若您使用语音识别（Paraformer）录音文件识别，需要下载的文件不存在。

**解决方案**： 请检查文件URL是否正确。

### FILE\_403\_FORBIDDEN

**原因**： 若您使用语音识别（Paraformer）录音文件识别，没有权限下载待识别录音。

**解决方案**： 请检查文件访问权限。

### FILE\_SERVER\_ERROR

**原因**： 若您使用语音识别（Paraformer）录音文件识别，请求的文件所在的服务不可用。

**解决方案**： 请稍后重试或检查文件服务器状态。

### AUDIO\_DURATION\_TOO\_LONG

**原因**： 若您使用语音识别（Paraformer）录音文件识别，请求的文件时长超过12小时。

**解决方案**： 建议将音频进行切分，分多次提交识别任务。可使用FFmpeg等工具切分。

### DECODE\_ERROR

**原因**： 若您使用语音识别（Paraformer）录音文件识别，检测音频文件信息失败。

**解决方案**： 请确认文件下载链接中文件为支持的音频格式。

### CLIENT\_ERROR-\[qwen-tts:]Engine return error code: 411

**原因**： 在进行Qwen-TTS实时语音合成时，选用的模型是`qwen-tts-vc-realtime-2025-08-20`，但音色是默认音色。该模型仅支持复刻音色。

**解决方案**： 请使用通过声音复刻生成的音色，而非默认音色。

### NO\_VALID\_AUDIO\_ERROR

**原因**： 使用语音识别（Paraformer）或语音识别/翻译（Gummy）时，待识别音频无效。

**解决方案**： 请检查音频格式、采样率等是否满足要求。

### InvalidParameter: task can not be null

**原因**：使用CosyVoice语音合成WebSocket API时，run-task 指令或 finish-task 指令的 payload 中缺少 input 字段，或 continue-task 指令中缺少 input.text 字段。

**解决方案**：

1. 检查 run-task 指令：确保 payload 中包含 `"input": {}`（空对象），不可省略 input 字段。
2. 检查 continue-task 指令：确保 payload.input 中包含 text 字段，且 text 不为空字符串。
3. 检查 finish-task 指令：确保 payload 中包含 `"input": {}`。

## 200-BailianGateway.Workspace.NotAuthorised

**控制台出现错误信息"部分功能使用受限"。**

**原因**：

1. 访问 URL 中包含了特殊字符或非标准格式，导致业务空间授权验证失败。
2. RAM 子账号操作没有权限的业务空间。

**解决方案**：

1. 请重新访问千问AI平台控制台首页，再导航到目标页面。
2. 需要千问AI平台账号或具有管理员权限的 RAM 账号为该子账号开通对应业务空间的权限。
