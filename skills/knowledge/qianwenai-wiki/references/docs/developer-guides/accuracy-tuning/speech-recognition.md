> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 语音识别最佳实践

> 通过音频质量优化、词汇定制和后处理纠错，提升语音识别准确率。

语音识别的准确率取决于三个因素：音频质量、词汇定制和后处理。音频质量差是最常见的错误原因，词汇定制解决领域专用术语的识别问题，后处理负责修正前两者遗漏的错误。

本指南涵盖以上三个方面。

## 音频质量

再强大的 ASR 模型也无法准确转录听不清的音频。音频质量是影响识别准确率最大的因素，也是改善成本最低的。

### 录音环境

| 因素        | 建议                                                |
| --------- | ------------------------------------------------- |
| **背景噪音**  | 在安静的房间录音，避免空调嗡嗡声、键盘敲击声和旁边的交谈声。如果无法避免噪音，使用指向性麦克风。  |
| **回声与混响** | 硬质墙壁、玻璃和空旷的大房间会产生回声。添加软质家具、使用较小的房间，或使用近讲麦克风。      |
| **说话距离**  | 与麦克风保持 10-30 厘米距离。太近会导致爆破音失真（"p"和"b"音），太远会录入环境噪音。 |
| **说话方式**  | 以自然语速说话。避免含糊不清、语尾拖长或多人同时说话。多人场景下，说话者之间留出明显停顿。     |

### 麦克风选择

不同场景需要不同类型的麦克风，选对麦克风可以从源头消除噪音。

| 场景            | 推荐麦克风                                    | 原因                                     |
| ------------- | ---------------------------------------- | -------------------------------------- |
| **呼叫中心 / 听写** | 带话杆的头戴式麦克风（如 Jabra Evolve2、Plantronics）  | 近讲设计可有效抑制背景噪音，嘴到麦克风的距离保持一致。单人场景下准确率最高。 |
| **采访 / 演示**   | 领夹式麦克风（如 Rode Wireless GO、DJI Mic）       | 夹在衣服上，解放双手。适合需要走动的单人场景。                |
| **会议室**       | 会议阵列麦克风（如 Jabra Speak、Poly Sync、XMOS 阵列） | 多个麦克风配合波束成形技术，能从各个方向收录说话者的声音，同时减少回声。   |
| **移动应用**      | 设备内置麦克风                                  | 日常使用尚可。对准确率要求高的移动应用，建议引导用户使用带内置麦克风的耳机。 |
| **电话（8kHz）**  | 不适用（运营商音频）                               | 使用 8kHz 模型。音频质量由电话网络决定。                |

<Tip>
  如果你能控制录音硬件，建议购买一款带降噪功能的 USB 耳麦。一副 50 美元的耳麦带来的准确率提升，超过任何软件优化手段。
</Tip>

### 音频格式

| 参数      | 建议                                                                         |
| ------- | -------------------------------------------------------------------------- |
| **采样率** | 16 kHz 或更高。仅对电话录音使用 8 kHz。更高的采样率（44.1 kHz、48 kHz）会被自动降采样——可以正常使用，但会占用更多带宽。 |
| **声道**  | 单声道。双声道可接受，但第二声道会被忽略。                                                      |
| **格式**  | PCM 或 WAV（无损格式），可完整保留信号。                                                   |
| **压缩**  | 对准确率要求高的场景，避免使用有损编码（MP3、AAC、OGG）。如果必须压缩，使用 OPUS 编码，码率不低于 32 kbps。          |
| **位深**  | 16 位。                                                                      |

<Warning>
  不要在发送音频到 ASR 前施加降噪、AGC（自动增益控制）或其他音频增强处理。这些滤波器可能在去除噪音的同时也去除了语音信号，反而降低准确率。请发送原始音频，让 ASR 模型自行处理噪音。
</Warning>

## 词汇定制

当 ASR 输出持续误识别特定术语（品牌名、产品名、专业术语、人名等）时，可以通过词汇定制来修正。具体方法取决于使用的模型。

| 方法             | 适用模型      | 工作原理                                                               |
| -------------- | --------- | ------------------------------------------------------------------ |
| **Prompt 上下文** | Qwen-Omni | 在系统提示词中描述你的领域。该模型本质是一个能理解音频的大语言模型，每次请求都会自适应。灵活性最高，但单次请求延迟高于专用 ASR。 |
| **上下文增强**      | Qwen3-ASR | 在 system 消息中传入领域上下文，模型动态适配。                                        |
| **热词**         | Fun-ASR   | 创建带权重的词汇列表，在 ASR 调用时传入列表 ID。                                       |

### Prompt 上下文（Qwen-Omni）

Qwen-Omni 不是传统的 ASR，而是一个能理解音频的大语言模型。在系统提示词中描述你的领域，模型即可自适应，无需预配置。这是最灵活的方法，但单次请求延迟高于专用 ASR 模型。

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
      model="qwen3-omni-flash",
      messages=[
        {
          "role": "system",
          "content": "You are transcribing investment banking discussions. "
               "Key terms: Bulge Bracket, Boutique, Middle Market, LBO, DCF."
        },
        {
          "role": "user",
          "content": [
            {
              "type": "input_audio",
              "input_audio": {
                "data": "https://example.com/meeting.mp3",
                "format": "mp3"
              }
            },
            {"type": "text", "text": "Transcribe this audio."}
          ]
        }
      ],
      stream=True,
      modalities=["text"],
    )

    for chunk in completion:
      if chunk.choices and chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
    ```
  </Tab>

  <Tab title="Node.js">
    ```javascript
    import OpenAI from "openai";

    const openai = new OpenAI({
      apiKey: process.env.DASHSCOPE_API_KEY,
      baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
    });

    const completion = await openai.chat.completions.create({
      model: "qwen3-omni-flash",
      messages: [
        {
          role: "system",
          content: "You are transcribing investment banking discussions. "
                 + "Key terms: Bulge Bracket, Boutique, Middle Market, LBO, DCF."
        },
        {
          role: "user",
          content: [
            {
              type: "input_audio",
              input_audio: {
                data: "https://example.com/meeting.mp3",
                format: "mp3"
              }
            },
            { type: "text", text: "Transcribe this audio." }
          ]
        }
      ],
      stream: true,
      modalities: ["text"],
    });

    for await (const chunk of completion) {
      if (chunk.choices?.[0]?.delta?.content) {
        process.stdout.write(chunk.choices[0].delta.content);
      }
    }
    ```
  </Tab>

  <Tab title="curl">
    ```bash
    curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "qwen3-omni-flash",
      "messages": [
        {
          "role": "system",
          "content": "You are transcribing investment banking discussions. Key terms: Bulge Bracket, Boutique, Middle Market, LBO, DCF."
        },
        {
          "role": "user",
          "content": [
            {
              "type": "input_audio",
              "input_audio": {
                "data": "https://example.com/meeting.mp3",
                "format": "mp3"
              }
            },
            {
              "type": "text",
              "text": "Transcribe this audio."
            }
          ]
        }
      ],
      "stream": true,
      "modalities": ["text"]
    }'
    ```
  </Tab>
</Tabs>

<Tip>
  当领域术语频繁变化，或者需要模型理解语义（而非仅做转录）时，使用 Prompt 上下文。如果术语列表稳定且音频可预测，热词或上下文增强的延迟更低。
</Tip>

### 上下文增强（Qwen3-ASR）

在 `system` 消息中传入领域相关的上下文。模型利用上下文提升专业术语的识别准确率——无需词汇列表，无需权重调整。支持词汇列表、段落描述或混合形式。

**前后对比**：

| 音频内容   | 无上下文                                     | 有上下文                                         |
| ------ | ---------------------------------------- | -------------------------------------------- |
| 投资银行术语 | "...the top banks, **Bird Rock**, BB..." | "...the top banks, **Bulge Bracket**, BB..." |

使用的上下文：`"Bulge Bracket, Boutique, Middle Market"`

**支持的上下文格式**——效果相同：

- **词汇列表**：`"Bulge Bracket, Boutique, Middle Market"`（逗号、空格或 JSON 数组分隔）
- **段落描述**：用自然语言描述领域（例如一段关于投资银行术语的描述）
- **混合形式**：在同一上下文中混合使用词汇列表和段落描述

<Tabs>
  <Tab title="Python">
    ```python
    import os
    import dashscope

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    messages = [
      {
        "role": "system",
        "content": [{"text": "Bulge Bracket, Boutique, Middle Market"}]
      },
      {
        "role": "user",
        "content": [{"audio": "https://example.com/investment-banking-audio.mp3"}]
      }
    ]

    response = dashscope.MultiModalConversation.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      model="qwen3-asr-flash",
      messages=messages,
      result_format="message"
    )
    print(response.output.choices[0].message.content[0]["text"])
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
    import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
    import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
    import com.alibaba.dashscope.common.MultiModalMessage;
    import com.alibaba.dashscope.common.Role;
    import java.util.*;

    public class ContextEnhancementExample {
      public static void main(String[] args) {
        MultiModalConversation conv = new MultiModalConversation();

        // 系统消息：传入领域上下文
        MultiModalMessage sysMessage = MultiModalMessage.builder()
            .role(Role.SYSTEM.getValue())
            .content(Arrays.asList(
              Collections.singletonMap("text", "Bulge Bracket, Boutique, Middle Market")
            ))
            .build();

        // 用户消息：传入音频
        MultiModalMessage userMessage = MultiModalMessage.builder()
            .role(Role.USER.getValue())
            .content(Arrays.asList(
              Collections.singletonMap("audio",
                "https://example.com/investment-banking-audio.mp3")
            ))
            .build();

        MultiModalConversationParam param = MultiModalConversationParam.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .model("qwen3-asr-flash")
            .message(sysMessage)
            .message(userMessage)
            .build();

        MultiModalConversationResult result = conv.call(param);
        System.out.println(result.getOutput().getChoices().get(0)
            .getMessage().getContent().get(0).get("text"));
      }
    }
    ```
  </Tab>
</Tabs>

<Note>
  上下文长度上限为 **10,000 tokens**。模型对上下文中的无关文本有较强的鲁棒性——即使包含无关的名称或描述，对准确率几乎没有负面影响。
</Note>

### 热词（Fun-ASR）

创建需要模型优先识别的词汇列表，然后在 ASR 调用时传入列表 ID。分为两步：

1. **创建热词列表**：通过[热词 API](/developer-guides/speech/improve-recognition-accuracy) 创建。指定 `target_model` 声明哪个 ASR 模型将使用该列表。
2. **传入列表 ID**：在 ASR 调用时传入。调用的模型必须与第 1 步中的 `target_model` 一致。

<Tabs>
  <Tab title="Python">
    ```python
    import dashscope
    from dashscope.audio.asr import *
    import os

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
    dashscope.base_websocket_api_url = 'wss://dashscope.aliyuncs.com/api-ws/v1/inference'
    dashscope.api_key = os.environ.get('DASHSCOPE_API_KEY')

    target_model = "fun-asr-realtime"

    # 第 1 步：创建热词列表
    service = VocabularyService()
    vocabulary_id = service.create_vocabulary(
      prefix='my-app',
      target_model=target_model,
      vocabulary=[
        {"text": "Bulge Bracket", "weight": 4},
        {"text": "Middle Market", "weight": 4}
      ]
    )

    # 第 2 步：使用热词列表进行识别
    if service.query_vocabulary(vocabulary_id)['status'] == 'OK':
      recognition = Recognition(
        model=target_model,
        format='wav',
        sample_rate=16000,
        callback=None,
        vocabulary_id=vocabulary_id
      )
      result = recognition.call('audio.wav')
      print(result.output)

    # 不再需要时清理热词列表
    service.delete_vocabulary(vocabulary_id)
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import com.alibaba.dashscope.audio.asr.recognition.*;
    import com.alibaba.dashscope.audio.asr.vocabulary.*;
    import com.alibaba.dashscope.utils.Constants;
    import com.google.gson.*;
    import java.io.File;

    public class HotwordExample {
      public static void main(String[] args) throws Exception {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        Constants.baseWebsocketApiUrl = "wss://dashscope.aliyuncs.com/api-ws/v1/inference";

        String targetModel = "fun-asr-realtime";

        // 第 1 步：创建热词列表
        JsonArray vocab = new JsonArray();
        JsonObject word1 = new JsonObject();
        word1.addProperty("text", "Bulge Bracket");
        word1.addProperty("weight", 4);
        vocab.add(word1);

        VocabularyService service = new VocabularyService(apiKey);
        Vocabulary vocabulary = service.createVocabulary(targetModel, "my-app", vocab);

        // 第 2 步：使用热词列表进行识别
        if ("OK".equals(service.queryVocabulary(vocabulary.getVocabularyId()).getStatus())) {
          Recognition recognizer = new Recognition();
          RecognitionParam param = RecognitionParam.builder()
              .model(targetModel)
              .apiKey(apiKey)
              .format("wav")
              .sampleRate(16000)
              .build();
          try {
            System.out.println(recognizer.call(param, new File("audio.wav")));
          } finally {
            recognizer.getDuplexApi().close(1000, "bye");
          }
        }

        service.deleteVocabulary(vocabulary.getVocabularyId());
        System.exit(0);
      }
    }
    ```
  </Tab>
</Tabs>

#### 热词格式

| 字段       | 类型     | 必填 | 说明                         |
| -------- | ------ | -- | -------------------------- |
| `text`   | string | 是  | 热词内容。必须是真实的词汇或短语。长度限制见下文。  |
| `weight` | int    | 是  | 优先级权重。范围：1-5，默认值：4。        |
| `lang`   | string | 否  | 语言代码（如 `en`、`zh`）。省略则自动检测。 |

**文本长度限制**：

- **包含非 ASCII 字符**：总字符数不超过 15。
- **纯 ASCII**：以空格分隔的单词数不超过 7。

#### 权重调优

- **从权重 4 开始。** 大多数术语用 4 即可。
- **仅在测试后发现某术语仍被漏识别时才提高到 5。** 过高的权重可能导致模型在不存在该词的地方产生幻觉。
- **不要把所有热词都设为 5。** 当所有词都是高优先级时，等于没有优先级。根据实际重要性区分权重。

<Warning>
  创建热词列表时指定的 `target_model` **必须与** ASR 调用中使用的模型一致。不匹配会导致热词不生效。
</Warning>

热词列表的创建、查询、更新和删除的完整 API 说明，参见[热词 API 参考](/developer-guides/speech/improve-recognition-accuracy)。

## 后处理纠错

词汇定制解决已知术语的问题，后处理负责修正其余错误——语法错误、上下文相关词汇和同音歧义。

### 双轨模式

对准确率要求极高的应用（医疗转录、法律记录、财务报告），建议将实时 ASR 与 LLM 后处理纠错结合使用：

```
音频流
    |
    v
+-------------------+     +-------------------+
| 实时 ASR | --> | LLM 后处理纠错 |
| （低延迟）  |     | （高准确率）    |
+-------------------+     +-------------------+
|   |
    v                           v
立即显示                    替换为纠错后的文本
（草稿转录）                （最终转录）
```

1. **快速通道**：将音频流发送到实时 ASR 端点（`qwen3-asr-flash-realtime` 或 `fun-asr-realtime`），立即显示中间结果。
2. **纠错通道**：收集句子级别的 ASR 输出，发送给 LLM（如 `qwen-plus`），附带领域感知的纠错提示词：

```
Fix any speech recognition errors in the following transcript.
Preserve the original meaning. Domain: [medical/legal/financial].
Transcript: "{asr_output}"
```

3. LLM 响应后（通常 1-2 秒），用纠错后的文本替换已显示的内容。

该模式特别适用于以下场景：

- 即使使用了词汇定制，领域术语仍经常被误识别。
- 准确率要求超过 98%。
- 用户体验上可以接受 1-2 秒的纠错延迟。

### 准确率评估

- **WER（词错误率）**：在每次优化前后进行测量。使用一组有代表性的音频样本，与人工校验的转录文本进行对比。
- **A/B 测试**：对比仅使用词汇定制 vs. 词汇定制 + 双轨纠错的效果。
- **逐词跟踪**：监控热词列表或上下文中每个术语的准确率。部分术语可能需要调整权重或补充上下文。

## 高并发 ASR

大规模运行 ASR 时，使用对象池管理 `Recognition` 实例，避免每次请求都创建新的 WebSocket 连接。

### Java：Recognition 对象池

使用 Apache Commons Pool2 对象池管理 `Recognition` 实例。要求 Java SDK >= 2.16.9。

**环境变量**：

| 变量                                          | 默认值 | 建议             |
| ------------------------------------------- | --- | -------------- |
| `DASHSCOPE_CONNECTION_POOL_SIZE`            | 32  | 峰值并发数的 2 倍     |
| `DASHSCOPE_MAXIMUM_ASYNC_REQUESTS`          | 32  | 与连接池大小一致       |
| `DASHSCOPE_MAXIMUM_ASYNC_REQUESTS_PER_HOST` | 32  | 与连接池大小一致       |
| `RECOGNITION_OBJECTPOOL_SIZE`               | 500 | 峰值并发数的 1.5-2 倍 |

```java
import com.alibaba.dashscope.audio.asr.recognition.Recognition;
import org.apache.commons.pool2.BasePooledObjectFactory;
import org.apache.commons.pool2.PooledObject;
import org.apache.commons.pool2.impl.DefaultPooledObject;
import org.apache.commons.pool2.impl.GenericObjectPool;
import org.apache.commons.pool2.impl.GenericObjectPoolConfig;

class RecognitionFactory extends BasePooledObjectFactory<Recognition> {
  public Recognition create() { return new Recognition(); }
  public PooledObject<Recognition> wrap(Recognition obj) {
    return new DefaultPooledObject<>(obj);
  }
}

// 创建全局单例池
GenericObjectPoolConfig<Recognition> config = new GenericObjectPoolConfig<>();
int poolSize = 500; // 或从 RECOGNITION_OBJECTPOOL_SIZE 读取
config.setMaxTotal(poolSize);
config.setMaxIdle(poolSize);
config.setMinIdle(poolSize);
GenericObjectPool<Recognition> recognitionPool =
  new GenericObjectPool<>(new RecognitionFactory(), config);

// 在每个任务线程中：
Recognition recognizer = recognitionPool.borrowObject();
try {
  // ... 执行识别任务
  recognitionPool.returnObject(recognizer);
} catch (Exception e) {
  // 失败的对象不要归还到池中
}
```

<Note>
  对象池大小必须小于或等于连接池大小，否则线程会在等待可用连接时阻塞。
</Note>

## 生产环境检查清单

- [ ] 根据场景选择了合适的麦克风
- [ ] 音频格式为无损（PCM/WAV），单声道，16 kHz 以上
- [ ] 未对音频施加预处理滤波器（降噪、AGC）
- [ ] 已配置词汇定制（上下文增强或热词，与所用模型匹配）
- [ ] 热词：`target_model` 与实际使用的 ASR 模型一致
- [ ] 热词：权重逐步调优，未全部设为最大值
- [ ] 已在有代表性的音频样本上测量 WER
- [ ] 已评估双轨模式是否适用于高准确率场景
- [ ] 已根据预期峰值负载配置连接池和对象池大小
- [ ] 错误处理将失败的对象丢弃，而非归还到池中
- [ ] 已设置 ASR 服务不可用时的降级处理
- [ ] 监控系统持续跟踪识别准确率

## 支持的模型

| 方法             | 支持的模型                                                                                                                                                   |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Prompt 上下文** | `qwen3.5-omni-plus`, `qwen3.5-omni-flash`, `qwen3.5-omni-plus-realtime`, `qwen3.5-omni-flash-realtime`, `qwen3-omni-flash`, `qwen3-omni-flash-realtime` |
| **上下文增强**      | `qwen3-asr-flash`, `qwen3-asr-flash-realtime`, `qwen3-asr-plus`, `qwen3-asr-plus-realtime`                                                              |
| **热词**         | `fun-asr-realtime`, `fun-asr`（及带日期的变体）                                                                                                                  |

完整模型列表参见[语音转文字模型](/developer-guides/speech/speech-to-text-models)。

## 计费

- **上下文增强**：无额外费用，按 Qwen3-ASR 标准 Token 计费。
- **热词**：免费，创建和使用热词列表不收费。

## 限制

- **上下文增强**：每条 system 消息最多 10,000 tokens。
- **热词**：每个账号最多 10 个热词列表（所有模型共享），每个列表最多 500 个热词。如需更多配额，请申请增加。
