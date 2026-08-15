> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 声音设计

> 通过文本描述创建自定义音色，无需音频样本，支持 Qwen-TTS、CosyVoice 和 Qwen-Audio-TTS 模型。

声音设计（Voice Design）无需音频样本，仅通过自然语言描述即可创建定制化音色。

## 概述

声音设计适用于快速原型验证、创意内容生产、游戏角色配音等场景。

千问AI平台平台提供以下模型系列的声音设计能力：

- **CosyVoice**：支持实时与非实时语音合成（v3.5 系列）。
- **Qwen-TTS**：支持实时与非实时语音合成，声音描述长度上限更高（2048 字符）。
- **Qwen-Audio-TTS**：支持实时与非实时语音合成（qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash）。

如果您已有音频样本，请参见[声音复刻](/developer-guides/speech/voice-cloning)。如需了解模型选型建议，请参见[语音合成](/developer-guides/speech/tts-models)。

<Warning>
  Voice design 中的 `target_model` 必须与合成时的 `model` 一致，否则会导致调用失败。
</Warning>

## 前提条件

- 已[配置 API Key](/api-reference/preparation/api-key) 并将其[设置到环境变量](/api-reference/preparation/export-api-key-env)。
- 如果通过 DashScope SDK 调用，需要[安装最新版 SDK](/api-reference/preparation/install-sdk)。

## 快速开始

声音设计的基本流程为：描述 -> 创建 -> 使用。

1. **编写声音描述**：用自然语言描述期望的声音特质。详细的编写指南请参见[编写声音描述](#编写声音描述)。
2. **创建音色**：调用声音设计接口，系统根据描述生成音色并返回预览音频。建议试听确认效果后再使用。
3. **使用音色合成语音**：调用语音合成接口，传入音色 ID 进行语音合成。

### Qwen-TTS 声音设计

以下示例演示如何创建音色并用于语音合成。

<Tip>
  建议先试听返回的预览音频，确认效果后再用于合成，以降低调用成本。
</Tip>

#### 创建音色

<Tabs>
  <Tab title="Python">
    ```python
    import os
    import requests
    import dashscope

    # ======= 常量配置 =======
    DEFAULT_TARGET_MODEL = "qwen3-tts-vd-2026-01-26"  # 声音设计、语音合成要使用相同的模型
    DEFAULT_PREFERRED_NAME = "custom_voice"

    # 声音描述：用自然语言描述期望的声音特质
    VOICE_PROMPT = "年轻活泼的女性声音，语速较快，带有明显的上扬语调，适合介绍时尚产品。"

    def create_voice_by_design(voice_prompt: str,
                               target_model: str = DEFAULT_TARGET_MODEL,
                               preferred_name: str = DEFAULT_PREFERRED_NAME) -> str:
      """
      通过声音描述创建音色，并返回 voice 参数
      """
      api_key = os.getenv("DASHSCOPE_API_KEY")

      url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"
      payload = {
        "model": "qwen-voice-enrollment",  # 不要修改该值
        "input": {
          "action": "create",
          "target_model": target_model,
          "preferred_name": preferred_name,
          "voice_prompt": voice_prompt
        }
      }
      headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
      }

      resp = requests.post(url, json=payload, headers=headers)
      if resp.status_code != 200:
        raise RuntimeError(f"创建 voice 失败: {resp.status_code}, {resp.text}")

      result = resp.json()
      # 返回预览音频（可选：先试听确认效果）
      preview_audio = result.get("output", {}).get("preview_audio")
      if preview_audio:
        print(f"预览音频URL: {preview_audio}")

      try:
        return result["output"]["voice"]
      except (KeyError, ValueError) as e:
        raise RuntimeError(f"解析 voice 响应失败: {e}")

    if __name__ == '__main__':
      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      voice_id = create_voice_by_design(VOICE_PROMPT)
      print(f"创建的音色ID: {voice_id}")

      text = "大家好，欢迎来到我们的直播间！今天给大家推荐的这款产品真的超级好用。"
      response = dashscope.MultiModalConversation.call(
        model=DEFAULT_TARGET_MODEL,
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        text=text,
        voice=voice_id,
        stream=False
      )
      print(response)
    ```
  </Tab>

  <Tab title="cURL">
    **步骤一：通过声音描述创建音色**

    ```bash
    curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "model": "qwen-voice-enrollment",
      "input": {
        "action": "create",
        "target_model": "qwen3-tts-vd-2026-01-26",
        "preferred_name": "custom_voice",
        "voice_prompt": "年轻活泼的女性声音，语速较快，带有明显的上扬语调，适合介绍时尚产品。"
      }
    }'
    ```

    **步骤二：使用设计音色合成语音**

    将上一步返回的 `voice` 值填入以下请求中。

    ```bash
    # 将 YOUR_VOICE_ID 替换为上一步返回的 voice 值

    curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H 'Content-Type: application/json' \
    -d '{
      "model": "qwen3-tts-vd-2026-01-26",
      "input": {
        "text": "大家好，欢迎来到我们的直播间！今天给大家推荐的这款产品真的超级好用。",
        "voice": "YOUR_VOICE_ID"
      }
    }'
    ```
  </Tab>
</Tabs>

### CosyVoice 声音设计

CosyVoice 同样支持通过文本描述创建音色，使用流程与 Qwen-TTS 类似。

<Note>
  CosyVoice 声音设计基于 FunAudioGen-VD 模型能力。相同描述文本（Prompt）设计的音色可能存在差异，建议多次生成后择优使用。
</Note>

#### 创建音色

调用声音复刻/设计 API，通过 `voice_prompt` 参数传入声音描述，`preview_text` 参数指定预览音频朗读的文本。

<Tabs>
  <Tab title="cURL">
    **步骤一：通过声音描述创建音色**

    ```bash
    curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "voice-enrollment",
      "input": {
        "action": "create_voice",
        "target_model": "cosyvoice-v3-plus",
        "voice_prompt": "沉稳的中年男性播音员，音色低沉浑厚，富有磁性，语速平稳，吐字清晰，适合用于新闻播报或纪录片解说。",
        "preview_text": "各位听众朋友，大家好，欢迎收听晚间新闻。",
        "prefix": "announcer",
        "language_hints": ["zh"]
      },
      "parameters": {
        "sample_rate": 24000,
        "response_format": "wav"
      }
    }'
    ```

    **步骤二：使用设计音色合成语音**

    将上一步返回的 `voice` 值填入以下请求中。

    ```bash
    # 将 YOUR_VOICE_ID 替换为上一步返回的 voice 值

    curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/SpeechSynthesizer \
    -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
    -H "Content-Type: application/json" \
    -d '{
      "model": "cosyvoice-v3-plus",
      "input": {
        "text": "各位听众朋友，大家好，欢迎收听晚间新闻。",
        "voice": "YOUR_VOICE_ID",
        "format": "wav",
        "sample_rate": 24000
      }
    }'
    ```
  </Tab>
</Tabs>

如需使用自定义音色进行实时流式合成，请参见[流式语音合成](/developer-guides/speech/realtime-streaming)。完整的 API 参数说明及更多操作（列出、查询、删除），请参见 [Voice design API 参考](/api-reference/speech-synthesis/voice-design/create-voice)。

## 配额与计费

### 音色配额与自动清理

- **音色总数限制**：每个千问AI平台账号下，CosyVoice 与 Qwen-TTS 分别最多可创建 1000 个自定义音色（两类配额独立计算）。
- **自动清理规则**：若单个音色在过去 1 年内未被用于任何语音合成请求，系统将自动删除该音色。

### 计费规则

<Note>
  以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
</Note>

- **CosyVoice**：创建音色免费。
- **Qwen-TTS**：按 0.2 元/个计费，创建失败不计费。

  **免费额度**：

  - 千问AI平台开通后 90 天内，可享 10 次免费音色创建机会。
  - 创建失败不占用免费次数。
  - 删除音色不会恢复免费次数。
  - 免费额度用完或超出 90 天有效期后，创建音色将按 0.2 元/个的价格计费。

## 适用范围

支持的模型：

- **CosyVoice**：cosyvoice-v3.5-plus、cosyvoice-v3.5-flash、cosyvoice-v3-plus、cosyvoice-v3-flash
- **Qwen-Audio-TTS**：qwen-audio-3.0-tts-plus、qwen-audio-3.0-tts-flash
- **Qwen-TTS**：
  - **Qwen3-TTS-VD-Realtime**：qwen3-tts-vd-realtime-2026-01-15（最新快照版）、qwen3-tts-vd-realtime-2025-12-16（快照版）
  - **Qwen3-TTS-VD**：qwen3-tts-vd-2026-01-26（最新快照版）

<Note>
  * CosyVoice 声音设计基于 FunAudioGen-VD 模型能力。
  * 相同描述文本（Prompt）设计的音色可能存在差异，建议多次生成后择优使用。
</Note>

## 编写声音描述

声音描述（`voice_prompt`）直接决定生成音色的效果。清晰、具体的描述能帮助模型更准确地生成目标音色。

### 要求与限制

- **长度限制**：`voice_prompt` 的最大长度因模型而异：CosyVoice 不超过 500 个字符，Qwen-TTS 不超过 2048 个字符。
- **支持语言**：描述文本仅支持中文和英文。

### 核心原则

1. **具体而非模糊**：使用描绘声音特质的词语，如"低沉""清脆""语速偏快"，避免"好听""普通"等主观或模糊的表述。
2. **多维而非单一**：好的描述通常涵盖多个维度（如性别、年龄、情感等）。仅写"女声"过于宽泛，难以生成有特色的音色。
3. **客观而非主观**：聚焦声音的物理和感知特征。例如，用"音调偏高，带有活力"代替"我最喜欢的声音"。
4. **原创而非模仿**：描述声音的特质，而非要求模仿特定人物（如名人、演员）。模型不支持模仿，且可能涉及版权风险。
5. **简洁而非冗余**：确保每个词都有明确作用，避免重复的同义词或无意义的修饰。

### 描述维度参考

建议组合以下维度来描述声音，维度越丰富，生成效果越精准。

| 维度 | 描述示例                                                       |
| -- | ---------------------------------------------------------- |
| 性别 | 男性、女性、中性                                                   |
| 年龄 | 儿童（5-12 岁）、青少年（13-18 岁）、青年（19-35 岁）、中年（36-55 岁）、老年（55 岁以上） |
| 音调 | 高音、中音、低音、偏高、偏低                                             |
| 语速 | 快速、中速、缓慢、偏快、偏慢                                             |
| 情感 | 开朗、沉稳、温柔、严肃、活泼、冷静、治愈                                       |
| 特点 | 有磁性、清脆、沙哑、圆润、甜美、浑厚、有力                                      |
| 用途 | 新闻播报、广告配音、有声书、动画角色、语音助手、纪录片解说                              |

### 示例

- 标准播音风格：吐字清晰精准，字正腔圆
- 年轻活泼的女性声音，语速较快，带有明显的上扬语调，适合介绍时尚产品
- 沉稳的中年男性，语速缓慢，音色低沉有磁性，适合朗读新闻或纪录片解说
- 温柔知性的女性，30 岁左右，语调平和，适合有声书朗读
- 可爱的儿童声音，大约 8 岁女孩，说话略带稚气，适合动画角色配音

## 管理自定义音色

声音设计和声音复刻创建的音色共用同一套管理接口。您可以查询音色列表、查看音色详情或删除不再需要的音色。

API 接口和参数详情请参见 [Voice design API 参考](/api-reference/speech-synthesis/voice-design/create-voice)。

## 常见问题

### Q：相同的声音描述每次生成的音色一样吗？

不一定。声音设计具有随机性，相同描述可能生成略有差异的音色。建议多次生成后试听，择优使用。

### Q：声音描述可以使用哪些语言？

目前声音描述（`voice_prompt`）仅支持中文和英文，但生成的音色可用于合成多种语言的语音。

### Q：声音设计和声音复刻有什么区别？

声音设计通过文本描述从零创建音色，无需音频样本，适合设计全新的声音形象。声音复刻基于真实音频样本复制音色，适合还原特定人物的声音。详情请参见[声音复刻](/developer-guides/speech/voice-cloning)。

## API 参考

- [Voice design API 参考](/api-reference/speech-synthesis/voice-design/create-voice) -- API 参数和响应格式
- [流式语音合成](/developer-guides/speech/realtime-streaming) -- 使用自定义音色进行实时合成
- [Qwen TTS](/api-reference/speech-synthesis/qwen-tts) -- 使用自定义音色进行非流式合成
- [获取 API Key](/api-reference/preparation/api-key) -- 设置身份认证
