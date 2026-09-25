> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 提升识别准确率

> 通过预编译热词、即时热词和上下文增强提升语音识别准确率。

部分业务词汇（如产品名、专有名词、行业术语）不在模型通用词表中，识别准确率较低。千问AI平台语音识别提供预编译热词、即时热词和上下文增强三种方式，提升这类词汇的识别效果。

### 预编译热词、即时热词与上下文增强的区别

自定义热词分为预编译热词和即时热词两种。下表对比三种方式的差异，适用模型和接口不同：

| 维度   | 预编译热词                            | 即时热词                                | 上下文增强                                                        |
| ---- | -------------------------------- | ----------------------------------- | ------------------------------------------------------------ |
| 原理   | 预先创建带权重的词汇表，模型在解码时提升匹配概率         | 请求中直接携带带权重的热词，模型在解码时提升匹配概率          | 传入对话历史或领域语料，模型利用上下文修正识别结果                                    |
| 适用模型 | 参见[预编译热词](#预编译热词)                | 参见[即时热词](#即时热词)                     | 参见[上下文增强](#上下文增强)                                            |
| 适用场景 | 词汇已知且相对稳定，需要跨请求复用同一词表（如产品名、医学术语） | 临时性、会话级别的热词，无需跨请求复用（如单次会话中的人名、临时术语） | 词汇随对话动态变化，或需要通过上下文帮助模型理解专有名词（如会议纪要中的参会人、客服对话中的业务术语）          |
| 配置方式 | 预先创建热词列表，调用时传入列表 ID              | 请求中直接传入 `vocabulary` 键值对，无需创建列表     | 每次请求时传入对话历史或领域文本。非实时通过 `input.messages`，实时通过 `input.context` |

## 前提条件

1. 已[获取 API Key](/api-reference/preparation/api-key) 并将其配置到环境变量。
2. 如果通过 SDK 调用，需[安装 DashScope SDK](/api-reference/preparation/install-sdk)。

## 预编译热词

预先创建热词列表并获得列表 ID，识别时传入该 ID。适用于词汇已知且相对稳定、需要跨请求复用同一词表的场景（如产品名、医学术语）。

<Warning>
  即时热词仅支持 Qwen-Audio-3.0-ASR-Flash-Streaming、Qwen-Audio-3.0-ASR-Flash-Filetrans 和 Qwen-Audio-3.0-ASR-Flash 系列模型。对于这些模型，同时配置预编译热词和即时热词时，系统会合并两类热词；合并后超过 2,000 个时，随机选择 2,000 个使用。
</Warning>

### 支持的模型与地域

- **实时语音识别**：
  - **Qwen-Audio-3.0-ASR-Flash-Streaming**：`qwen-audio-3.0-asr-flash-streaming`
  - **Fun-ASR-Realtime**：`fun-asr-realtime`、`fun-asr-realtime-2026-02-28`、`fun-asr-realtime-2025-11-07`、`fun-asr-realtime-2025-09-15`、`fun-asr-flash-8k-realtime`、`fun-asr-flash-8k-realtime-2026-01-28`
  - **Paraformer**：`paraformer-realtime-v2`、`paraformer-realtime-8k-v2`
- **非实时语音识别**：
  - **Qwen-Audio-3.0-ASR-Flash-Filetrans**：`qwen-audio-3.0-asr-flash-filetrans`
  - **Qwen-Audio-3.0-ASR-Flash**：`qwen-audio-3.0-asr-flash`
  - **Fun-ASR-Flash**：`fun-asr-flash-2026-06-15`
  - **Fun-ASR**：`fun-asr`、`fun-asr-2025-11-07`、`fun-asr-2025-08-25`、`fun-asr-mtl`、`fun-asr-mtl-2025-08-25`
  - **Paraformer**：`paraformer-v2`、`paraformer-8k-v2`

完整模型列表请参见[语音识别模型](/developer-guides/speech/speech-to-text-models)。

### 快速开始

**工作流程：**

1. **创建热词列表**：调用[创建 API](/api-reference/speech-recognition/custom-hotwords/http-api) 定义热词列表，并将 `target_model` 设置为您计划使用的语音识别模型。
2. **使用热词列表**：在语音识别请求参数中传入热词列表 ID（`vocabulary_id`）。确保 `target_model` 与调用的模型一致。

完整流程示例：创建热词列表 → 调用语音识别 → 删除列表。示例音频：[asr\_example.wav](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250210/elouas/asr_example.wav)。

<Note>
  热词管理 API 与语音识别 API 必须使用同一账号，否则识别接口无法访问对应的热词列表。
</Note>

<Tabs>
  <Tab title="Python">
    ```python
    import dashscope
    from dashscope.audio.asr import *
    import os

    # 如果未配置环境变量，请将下一行替换为：dashscope.api_key = "sk-xxx"
    dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
    dashscope.base_websocket_api_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'
    prefix = 'testpfx'
    target_model = "qwen-audio-3.0-asr-flash-streaming"

    my_vocabulary = [
      {"text": "语音实验室", "weight": 4}
    ]

    service = VocabularyService()
    vocabulary_id = service.create_vocabulary(
      prefix=prefix,
      target_model=target_model,
      vocabulary=my_vocabulary)

    try:
      if service.query_vocabulary(vocabulary_id)['status'] == 'OK':
        recognition = Recognition(model=target_model,
                                format='wav',
                                sample_rate=16000,
                                callback=None,
                                vocabulary_id=vocabulary_id)
        result = recognition.call('asr_example.wav')
        print(result.output)
    finally:
      # 无论识别成功与否都删除热词列表，避免占用配额
      service.delete_vocabulary(vocabulary_id)
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import com.alibaba.dashscope.audio.asr.recognition.Recognition;
    import com.alibaba.dashscope.audio.asr.recognition.RecognitionParam;
    import com.alibaba.dashscope.audio.asr.vocabulary.Vocabulary;
    import com.alibaba.dashscope.audio.asr.vocabulary.VocabularyService;
    import com.alibaba.dashscope.exception.InputRequiredException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.alibaba.dashscope.utils.Constants;
    import com.google.gson.JsonArray;
    import com.google.gson.JsonObject;

    import java.io.File;
    import java.util.ArrayList;
    import java.util.List;

    public class Main {
      // 如果未配置环境变量，请将下一行替换为：public static String apiKey = "sk-xxx"
      public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

      public static void main(String[] args) throws NoApiKeyException, InputRequiredException {
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";

        String targetModel = "qwen-audio-3.0-asr-flash-streaming";

        JsonArray vocabularyJson = new JsonArray();
        List<Hotword> wordList = new ArrayList<>();
        wordList.add(new Hotword("语音实验室", 4));

        for (Hotword word : wordList) {
          JsonObject jsonObject = new JsonObject();
          jsonObject.addProperty("text", word.text);
          jsonObject.addProperty("weight", word.weight);
          vocabularyJson.add(jsonObject);
        }

        VocabularyService service = new VocabularyService(apiKey);
        Vocabulary vocabulary = service.createVocabulary(targetModel, "testpfx", vocabularyJson);

        try {
          if ("OK".equals(service.queryVocabulary(vocabulary.getVocabularyId()).getStatus())) {
            Recognition recognizer = new Recognition();
            RecognitionParam param =
                RecognitionParam.builder()
                    .model(targetModel)
                    .apiKey(apiKey)
                    .format("wav")
                    .sampleRate(16000)
                    .vocabularyId(vocabulary.getVocabularyId())
                    .build();

            try {
              System.out.println("识别结果：" + recognizer.call(param, new File("asr_example.wav")));
            } catch (Exception e) {
              e.printStackTrace();
            } finally {
              // 关闭 WebSocket 连接
              recognizer.getDuplexApi().close(1000, "bye");
            }
          }
        } finally {
          // 无论识别成功与否都删除热词列表，避免占用配额
          service.deleteVocabulary(vocabulary.getVocabularyId());
        }
        System.exit(0);
      }
    }

    class Hotword {
      String text;
      int weight;

      public Hotword(String text, int weight) {
        this.text = text;
        this.weight = weight;
      }
    }
    ```
  </Tab>
</Tabs>

### 热词格式

热词以 JSON 数组提交，数组元素定义单个热词及其属性。

**示例**：提升电影名称的识别率（Fun-ASR 及 Paraformer 系列模型）

```json
[
  {"text": "赛德克巴莱", "weight": 4, "lang": "zh"},
  {"text": "Seediq Bale", "weight": 4, "lang": "en"},
  {"text": "夏洛特烦恼", "weight": 4, "lang": "zh"},
  {"text": "Goodbye Mr. Loser", "weight": 4, "lang": "en"},
  {"text": "阙里人家", "weight": 4, "lang": "zh"},
  {"text": "Confucius' Family", "weight": 4, "lang": "en"}
]
```

**字段说明**：

| 字段     | 类型     | 是否必填 | 说明                                                                                                                                                                                                              |
| ------ | ------ | ---- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| text   | string | 是    | 热词文本，需为实际词语而非任意字符组合，且语言必须在所选模型的支持范围内。长度限制参见下文。                                                                                                                                                                  |
| weight | int    | 是    | 热词权重，取值范围 \[1, 5]，推荐 4。权重越高，模型越倾向于输出该词。使用 Qwen-Audio-3.0-ASR-Flash-Streaming、Qwen-Audio-3.0-ASR-Flash-Filetrans、Qwen-Audio-3.0-ASR-Flash 系列模型时，还支持 `weight=50`（超级热词），召回率大幅提升，但超级热词数量最多不超过 50 个。过高的权重可能影响其他词的识别。 |
| lang   | string | 否    | 语言代码，限定该热词作用的语种。语种未知时可省略。注意：`language_hints` 是语音识别接口的参数（非热词接口），用于声明音频语种。一旦设置，仅匹配 `language_hints` 所指定语种的热词生效，其他语种的热词将被忽略。                                                                                       |

## 即时热词

即时热词在识别请求中直接传入 `vocabulary` 键值对，本质上也是一组带权重的热词（与预编译热词的词表内容对应），区别仅在于随请求内联传入、无需预先创建热词列表。适用于临时性、会话级别的热词优化。

<Warning>
  即时热词仅支持 Qwen-Audio-3.0-ASR-Flash-Streaming、Qwen-Audio-3.0-ASR-Flash-Filetrans 和 Qwen-Audio-3.0-ASR-Flash 系列模型。对于这些模型，同时配置预编译热词和即时热词时，系统会合并两类热词；合并后超过 2,000 个时，随机选择 2,000 个使用。
</Warning>

### 支持的模型与地域

- **实时语音识别**：
  - **Qwen-Audio-3.0-ASR-Flash-Streaming**：`qwen-audio-3.0-asr-flash-streaming`
- **非实时语音识别**：
  - **Qwen-Audio-3.0-ASR-Flash-Filetrans**：`qwen-audio-3.0-asr-flash-filetrans`
  - **Qwen-Audio-3.0-ASR-Flash**：`qwen-audio-3.0-asr-flash`

### 快速开始

在语音识别请求的 `parameters` 中传入 `vocabulary`，无需创建热词列表。各接口的详细用法参见[语音识别](/developer-guides/speech/speech-to-text-models)下的 API 参考。

**示例**（非实时语音识别）：

```bash
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
     --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
     --header "Content-Type: application/json" \
     --header "X-DashScope-SSE: disable" \
     --data '{
    "model": "qwen-audio-3.0-asr-flash",
    "input": {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
                        }
                    }
                ]
            }
        ]
    },
    "parameters": {
        "format": "wav",
        "sample_rate": "16000",
        "vocabulary": {"张三": 5, "李四": 5}
    }
}'
```

### 热词格式

即时热词以 JSON 对象（键值对）传入：键为热词文本（`string`），值为热词权重（`integer`）。热词文本规范参见[热词文本规范](#热词文本规范)。

**示例**：

```json
{"张三": 5, "李四": 5, "语音实验室": 50}
```

权重取值范围为 **\[1, 5] 或 50**：取 \[1, 5] 为普通热词，值越大偏好越强；取 50 为超级热词，召回率大幅提升，但超级热词数量最多不超过 50 个。权重调优参见[调整热词权重](#调整热词权重)。

## 热词调优与规范

以下热词文本规范与调优建议对预编译热词和即时热词均适用。

### 热词文本规范

热词文本必须为实际词语，长度限制如下：

- **含非 ASCII 字符时**：总字符数（汉字、日文假名、韩文谚文、西里尔字母等非 ASCII 字符与 ASCII 字符合计）不超过 15 个。

  示例：

  - `"厄洛替尼盐酸盐"`（7 个字符）
  - `"EGFR抑制剂"`（7 个字符，其中 EGFR 占 4 个 ASCII 字符）
  - `"こんにちは"`（5 个字符）
  - `"Фенибут Белфарм"`（15 个字符，含空格）
  - `"Клофелин Белмедпрепараты"`（24 个字符）—— 超出限制

- **纯 ASCII 字符时**：按空格切分后的片段数不超过 7 个。

  示例：

  - `"Exothermic reaction"` —— 2 个片段
  - `"Human immunodeficiency virus type 1"` —— 5 个片段
  - `"The effect of temperature variations on enzyme activity in biochemical reactions"` —— 11 个片段，超出限制

### 调整热词权重

权重控制模型对热词的偏好程度，合理设置可在提升目标词识别率的同时避免误识别。

| 权重  | 效果       | 适用场景                                           |
| --- | -------- | ---------------------------------------------- |
| 1-2 | 轻微偏好     | 热词与常用词发音相似，需避免过度纠偏                             |
| 3-4 | 明显偏好（推荐） | 大多数场景的最佳起始值                                    |
| 5   | 强制偏好     | 该词在音频中频繁出现且几乎不会与其他词混淆。权重过高可能导致发音相近的其他词被误识别为热词。 |

建议从 `weight=4` 起测，根据识别效果逐步调整。

**超级热词（`weight=50`）**：预编译热词和即时热词均支持超级热词，但仅 Qwen-Audio-3.0-ASR-Flash-Streaming、Qwen-Audio-3.0-ASR-Flash-Filetrans、Qwen-Audio-3.0-ASR-Flash 系列模型支持。设为 50 时召回率大幅提升，但超级热词数量最多不超过 50 个。

### 设计建议

- **按场景分组**：为不同业务场景分别组织热词（如医疗术语、产品名称各成一组），便于维护与复用。预编译热词可为每个场景建立独立的热词列表。
- **多语种混合（预编译热词）**：同一热词列表可混入不同语种的热词，通过 `lang` 字段区分。语音识别时指定 `language_hints` 后，仅匹配该语种的热词生效。
- **定期清理（预编译热词）**：删除不再使用的热词列表以释放额度（每账号上限 10 个）。

## 热词限制与计费

| 限制项                  | 说明                                                                                                                                                                                                                                                                                                                              |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 热词列表数量（预编译热词）        | 热词列表是预编译热词预先创建的持久化词表（对应一个 `vocabulary_id`）。每账号最多 10 个，所有模型共享。                                                                                                                                                                                                                                                                   |
| 热词数量上限（预编译热词 / 即时热词） | 热词数量上限取决于语音识别所用的模型：<br />- Qwen-Audio-3.0-ASR-Flash-Streaming、Qwen-Audio-3.0-ASR-Flash-Filetrans、Qwen-Audio-3.0-ASR-Flash 系列：最多 2000 个。<br />- Fun-ASR-Realtime、Fun-ASR-Flash、Fun-ASR 系列主版本模型：最多 2000 个。<br />- Fun-ASR-Realtime、Fun-ASR-Flash、Fun-ASR 系列其他模型、Paraformer 系列：最多 500 个。<br />其中，预编译热词按单个热词列表计数；即时热词按单次请求传入的热词数计数。 |
| 超级热词数量（预编译热词 / 即时热词） | 权重为 50 的超级热词最多 50 个。                                                                                                                                                                                                                                                                                                            |
| 计费                   | 预编译热词与即时热词均免费。                                                                                                                                                                                                                                                                                                                  |

**API 参考：**[预编译热词 API 参考](/api-reference/speech-recognition/custom-hotwords/http-api)

## 上下文增强

### 支持的模型与地域

- **实时语音识别**：
  - **Qwen-Audio-3.0-ASR-Flash-Streaming**：`qwen-audio-3.0-asr-flash-streaming`
  - **Fun-ASR-Realtime**：`fun-asr-realtime`、`fun-asr-realtime-2025-11-07`
- **非实时语音识别**：
  - **Qwen-Audio-3.0-ASR-Flash-Filetrans**：`qwen-audio-3.0-asr-flash-filetrans`
  - **Qwen-Audio-3.0-ASR-Flash**：`qwen-audio-3.0-asr-flash`
  - **Fun-ASR-Flash**：`fun-asr-flash-2026-06-15`

### 快速开始

\*\*使用场景：\*\*通过传入对话历史或领域术语作为上下文，可显著提升专有词汇（人名、地名、产品术语等）的转写准确率。上下文既可以是多轮对话历史（前几轮的识别结果与大模型回复），也可以只是一组领域术语或词表。

**用法：**

- **非实时语音识别**：在 HTTP 请求的 `input.messages` 中传入上下文消息，置于音频消息之前。
- **实时语音识别**：在 WebSocket `run-task` 事件的 `input.context` 中传入上下文消息；任务执行中如需更新，发送 `continue-task` 事件。DashScope SDK 已封装该协议，通过参数直接传入即可。

传入前几轮的识别结果（`user`/`input_text`）和大模型回复（`assistant`/`text`）。若只需传入领域术语或词表，省略其中的对话历史（`assistant` 消息）即可。

<Note>
  使用上下文增强时需注意以下限制：

  - \*\*消息条数限制：\*\*引擎最多保留最近 5 轮的上下文内容。仅传入领域术语或词表时通常只需 1 条消息，不受此限制影响。超出时，早期消息会被自动忽略，不会报错。
  - \*\*文本长度限制：\*\*每轮上下文的文本总长度（同一轮中所有 `user` 和 `assistant` 消息的 `text` 字段长度之和）不超过 400 个字符（按字符数计算，每个字符计为 1，包括字母、汉字、数字、空格和标点等）。超出部分会从末尾截断，不会返回错误。多轮上下文中，每轮独立计算，互不影响。
  - \*\*上下文机制：\*\*上下文主要通过词表匹配方式生效，`text` 字段中需包含音频里待识别的原词（如"Kubernetes"、"Bulge Bracket"）。仅传入语义相关但不包含原词的描述，纠正效果有限。
</Note>

**请求体结构示例：**

```json
{
  "model": "qwen-audio-3.0-asr-flash",
  "input": {
    "messages": [
      {
        "role": "assistant",
        "content": [
          {
            "type": "text",
            "text": "前轮大模型的回复内容"
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "input_text",
            "text": "前轮用户语音的识别结果"
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "input_audio",
            "input_audio": {
              "data": "当前待识别的音频URL或Base64"
            }
          }
        ]
      }
    ]
  },
  "parameters": {}
}
```

### 效果示例

上下文的 `text` 字段内容格式灵活，可以是词表、自然语言段落或两者的混合，对无关文本的容错性极高。

某段音频正确识别结果应该为："投行圈内部的那些黑话，你了解哪些？首先，外资九大投行，Bulge Bracket，BB ..."

| 不使用上下文增强                                                                                  | 使用上下文增强                                                  |
| ----------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| 未使用上下文增强时，部分投行公司名称识别有误。例如"Bird Rock"正确应为"Bulge Bracket"。识别结果："...外资九大投行，Bird Rock，BB ..." | 使用上下文增强，投行公司名称识别正确。识别结果："...外资九大投行，Bulge Bracket，BB ..." |

上述示例中，在上下文的 `text` 字段中加入包含"Bulge Bracket"等专业术语的词表或自然语言段落即可实现增强效果。

## 常见问题

### 设置热词后识别效果没有改善？

依次排查：

1. **模型是否匹配（预编译热词）**：创建热词列表时指定的 `target_model` 必须与语音识别接口使用的模型一致。两者不一致时接口不会报错，识别仍能返回结果，但热词不生效。识别结果未命中预期热词时应优先排查此项。
2. **模型是否支持**：确认所用模型在上方支持列表中。
3. **权重是否合适**：将权重从 4 提到 5 观察效果。如果出现发音相近的其他词被误识别为热词，回调到 4。
4. **热词列表状态（预编译热词）**：通过查询接口确认 `status` 为 `OK`。

### 预编译热词在实时和非实时语音识别中的使用方式是否相同？

创建方式相同，调用时存在差异：

- **实时语音识别**：在 Recognition 或 WebSocket 连接参数中传入 `vocabulary_id`。
- **录音文件识别**：在 Transcription 请求参数中传入 `vocabulary_id`。

两种场景的 `target_model` 都必须与实际调用的语音识别模型一致。即时热词无需创建列表和指定 `target_model`，直接在请求参数中传入 `vocabulary` 键值对即可。对于支持即时热词的 Qwen-Audio-3.0-ASR-Flash-Streaming、Qwen-Audio-3.0-ASR-Flash-Filetrans 和 Qwen-Audio-3.0-ASR-Flash 系列模型，同时配置预编译热词和即时热词时，系统会合并两类热词；合并后超过 2,000 个时，随机选择 2,000 个使用。

### 除了热词和上下文增强，还有哪些方式可以提升识别准确率？

还可从以下方向优化：

- **音频质量**：采样率匹配模型要求（16 kHz 或 8 kHz），降低背景噪声。
- **选择合适的模型**：不同场景适用模型不同，详见[语音识别模型](/developer-guides/speech/speech-to-text-models)选型指南。
- **指定语种**：通过 `language_hints` 声明音频语种，可提升单语种场景的准确率。
