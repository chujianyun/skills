> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 机器翻译（Qwen-MT）

> 支持 92 种语言及术语干预

Qwen-MT 是基于 Qwen3 微调的机器翻译模型，支持 92 种语言。它提供术语干预、领域提示和翻译记忆功能，帮助提升翻译质量。

## 工作原理

1. **提供待翻译文本**：`messages` 数组中只能包含一条消息，`role` 设为 `user`，`content` 为待翻译的文本。

2. **设置语言**：在 `translation_options` 参数中设置源语言（`source_lang`）和目标语言（`target_lang`）。支持的语言列表见[支持的语言](#supported-languages)。如需自动检测源语言，将 `source_lang` 设为 `auto`。

<Tip>指定源语言可以提高翻译准确性。您也可以通过[自定义提示词](#custom-prompts)设置语言。</Tip>

<Tabs>
  <Tab title="OpenAI 兼容">
    ```python
    # 导入依赖并创建客户端...
    completion = client.chat.completions.create(
      model="qwen-mt-flash",    # 选择模型
      # messages 参数只能包含一条 role 为 user 的消息，content 为待翻译文本。
      messages=[{"role": "user", "content": "No me reí después de ver este video"}],
      # translation_options 不是标准 OpenAI 参数，需通过 extra_body 传递。
      extra_body={"translation_options": {"source_lang": "auto", "target_lang": "English"}},
    )
    ```
  </Tab>

  <Tab title="DashScope">
    ```python
    # 导入依赖...
    response = dashscope.Generation.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      model="qwen-mt-flash",  # 选择模型
      messages=[{"role": "user", "content": "No me reí después de ver este video"}],  # messages：role 为 user，content 为待翻译文本。
      translation_options={"source_lang": "auto", "target_lang": "English"},  # 配置翻译选项
      result_format="message"
    )
    ```
  </Tab>
</Tabs>

**使用限制**

- **仅支持单轮翻译**：该模型专为翻译任务设计，不支持多轮对话。
- **不支持系统消息**：不能通过 `system` 角色的消息设置全局行为，请在 `translation_options` 参数中定义翻译配置。

## 模型选择

- **通用场景**首选`qwen-mt-flash`，在翻译质量、速度和成本之间取得最佳平衡，支持增量流式输出。
- **最高翻译质量**（专业文献、正式文书）选`qwen-mt-plus`。
- **最低延迟**（实时聊天等简单场景）选`qwen-mt-lite`。

| 模型            | 适用场景                                   | 质量 | 速度 | 成本 | 支持语言数 | 支持增量流式输出 |
| ------------- | -------------------------------------- | -- | -- | -- | ----- | -------- |
| qwen-mt-plus  | 翻译质量要求高的场景，如专业领域、正式文档、学术论文、技术报告        | 最佳 | 标准 | 高  | 92    | 不支持      |
| qwen-mt-flash | **通用首选。** 适用于网站/应用内容、产品描述、日常沟通、博客文章等场景 | 良好 | 快  | 低  | 92    | 支持       |
| qwen-mt-turbo | 该模型将不再更新，请使用 flash 替代。                 | 一般 | 快  | 低  | 92    | 不支持      |
| qwen-mt-lite  | 简单、对延迟敏感的场景，如实时聊天、直播弹幕翻译               | 基础 | 最快 | 最低 | 31    | 支持       |

模型详情、定价和限流，请参见[模型市场](https://www.qianwenai.com/models)。

## 快速开始

[获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。

<Tabs>
  <Tab title="OpenAI 兼容">
    **请求示例**

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        # 若未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )
      messages = [
        {
          "role": "user",
          "content": "No me reí después de ver este video"
        }
      ]
      translation_options = {
        "source_lang": "auto",
        "target_lang": "English"
      }

      completion = client.chat.completions.create(
        model="qwen-mt-plus",
        messages=messages,
        extra_body={
          "translation_options": translation_options
        }
      )
      print(completion.choices[0].message.content)
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen-mt-flash",
        "messages": [{"role": "user", "content": "No me reí después de ver este video"}],
        "translation_options": {
            "source_lang": "auto",
            "target_lang": "English"
            }
      }'
      ```
    </CodeGroup>

    **响应示例**

    ```text
    I didn't laugh after watching this video.
    ```
  </Tab>

  <Tab title="DashScope">
    **请求示例**

    <Warning>DashScope Java SDK 版本需为 2.20.6 或更高。</Warning>

    <CodeGroup>
      ```python Python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
      messages = [
        {
          "role": "user",
          "content": "No me reí después de ver este video"
        }
      ]
      translation_options = {
        "source_lang": "auto",
        "target_lang": "English",
      }
      response = dashscope.Generation.call(
        # 若未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model="qwen-mt-turbo",  # 本示例使用 qwen-mt-turbo，您可根据需要替换为其他模型。
        messages=messages,
        result_format='message',
        translation_options=translation_options
      )
      print(response.output.choices[0].message.content)
      ```

      ```java Java
      // DashScope SDK 版本需为 2.20.6 或更高。
      import java.lang.System;
      import java.util.Collections;
      import com.alibaba.dashscope.aigc.generation.Generation;
      import com.alibaba.dashscope.aigc.generation.GenerationParam;
      import com.alibaba.dashscope.aigc.generation.GenerationResult;
      import com.alibaba.dashscope.aigc.generation.TranslationOptions;
      import com.alibaba.dashscope.common.Message;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.InputRequiredException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.protocol.Protocol;

      public class Main {
        public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
          Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");
          Message userMsg = Message.builder()
              .role(Role.USER.getValue())
              .content("No me reí después de ver este video")
              .build();
          TranslationOptions options = TranslationOptions.builder()
              .sourceLang("auto")
              .targetLang("English")
              .build();
          GenerationParam param = GenerationParam.builder()
              // 若未配置环境变量，请将下行替换为您的 API Key：.apiKey("sk-xxx")
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen-mt-plus")
              .messages(Collections.singletonList(userMsg))
              .resultFormat(GenerationParam.ResultFormat.MESSAGE)
              .translationOptions(options)
              .build();
          return gen.call(param);
        }
        public static void main(String[] args) {
          try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
          } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("Error message: "+e.getMessage());
            e.printStackTrace();
          } finally {
            System.exit(0);
          }
        }
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen-mt-turbo",
        "input": {
          "messages": [
            {
              "content": "No me reí después de ver este video",
              "role": "user"
            }
          ]
        },
        "parameters": {
          "translation_options": {
            "source_lang": "auto",
            "target_lang": "English"
          }
        }
      }'
      ```
    </CodeGroup>

    **响应示例**

    ```text
    I didn't laugh after watching this video.
    ```
  </Tab>
</Tabs>

## 流式输出

<Tip>
  流式输出的通用概念（SSE 协议、如何启用流式、计费和 Token 用量），请参见[流式输出](/developer-guides/run-and-scale/streaming)。本节仅介绍机器翻译特有的流式行为。
</Tip>

在翻译调用中添加 `stream: true` 即可启用流式输出。与[标准流式输出](/developer-guides/run-and-scale/streaming)的唯一区别是需要包含 `translation_options`：

```python
completion = client.chat.completions.create(
  model="qwen-mt-flash",
  messages=[{"role": "user", "content": "No me reí después de ver este video"}],
  stream=True,
  stream_options={"include_usage": True},
  extra_body={"translation_options": {"source_lang": "auto", "target_lang": "English"}},
)
for chunk in completion:
  if chunk.choices:
    print(chunk.choices[0].delta.content or "", end="", flush=True)
```

**模型差异**：

| 模型                          | 增量流式输出                       |
| --------------------------- | ---------------------------- |
| qwen-mt-flash, qwen-mt-lite | 支持 — 每个 chunk 仅包含新生成的内容      |
| qwen-mt-plus, qwen-mt-turbo | 不支持 — 每个 chunk 包含截至目前生成的全部内容 |

DashScope 接口中，在支持的模型上设置 `incremental_output=True` 可启用增量流式输出。

## 提升翻译质量

在专业翻译任务中，可能遇到以下问题：

- **术语不一致**：产品名称或行业术语翻译不正确。
- **风格不匹配**：译文风格不符合特定领域（如法律、营销）的要求。

您可以通过术语干预、翻译记忆和领域提示来解决这些问题。

### 术语干预

当文本包含品牌名称、产品名称或技术术语时，为确保翻译的准确性和一致性，您可以在 `terms` 字段中提供术语表，指定模型使用您定义的翻译。

按以下步骤定义和传递术语：

<Steps>
  <Step title="定义术语">
    创建一个 JSON 数组并赋值给 `terms` 字段。数组中每个对象表示一个术语，格式如下：

    ```json
    {
      "source": "原文术语",
      "target": "预设译文"
    }
    ```
  </Step>

  <Step title="传递术语">
    通过 `translation_options` 参数传递定义的 `terms` 数组。
  </Step>
</Steps>

<Tabs>
  <Tab title="OpenAI 兼容">
    **请求示例**

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        # 若未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )
      messages = [
        {
          "role": "user",
          "content": "Este conjunto de biosensores utiliza grafeno, un material novedoso. Su objetivo son los elementos químicos. Su agudo «sentido del olfato» le permite reflejar el estado de salud del cuerpo de forma más profunda y precisa."
        }
      ]

      # --- 第一次请求：不使用 terms 参数 ---
      print("--- [不使用术语干预的翻译结果] ---")
      translation_options_without_terms = {
        "source_lang": "auto",
        "target_lang": "English"
      }

      completion_without_terms = client.chat.completions.create(
        model="qwen-mt-turbo",
        messages=messages,
        extra_body={
          "translation_options": translation_options_without_terms
        }
      )
      print(completion_without_terms.choices[0].message.content)

      print("\n" + "="*50 + "\n") # 对比分隔线

      # --- 第二次请求：使用 terms 参数 ---
      print("--- [使用术语干预的翻译结果] ---")
      translation_options_with_terms = {
        "source_lang": "auto",
        "target_lang": "English",
        "terms": [
          {
            "source": "biosensor",
            "target": "biological sensor"
          },
          {
            "source": "estado de salud del cuerpo",
            "target": "health status of the body"
          }
        ]
      }

      completion_with_terms = client.chat.completions.create(
        model="qwen-mt-turbo",
        messages=messages,
        extra_body={
          "translation_options": translation_options_with_terms
        }
      )
      print(completion_with_terms.choices[0].message.content)
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen-mt-turbo",
        "messages": [
          {
            "role": "user",
            "content": "Este conjunto de biosensores utiliza grafeno, un material novedoso. Su objetivo son los elementos químicos. Su agudo «sentido del olfato» le permite reflejar el estado de salud del cuerpo de forma más profunda y precisa."
          }
        ],
        "translation_options": {
          "source_lang": "auto",
          "target_lang": "English",
          "terms": [
            {
              "source": "biosensor",
              "target": "biological sensor"
            },
            {
              "source": "estado de salud del cuerpo",
              "target": "health status of the body"
            }
          ]
        }
      }'
      ```
    </CodeGroup>

    **响应示例**

    添加术语后，翻译结果与您传入的术语一致："**biological sensor**" 和 "**health status of the body**"。

    ```text
    --- [不使用术语干预的翻译结果] ---
    This set of biosensors uses graphene, a new material, whose target substance is chemical elements. Its sensitive "sense of smell" allows it to more deeply and accurately reflect one's health condition.

    ==================================================
    --- [使用术语干预的翻译结果] ---
    This biological sensor uses a new material called graphene. Its target is chemical elements, and its sensitive "sense of smell" enables it to reflect the health status of the body more deeply and accurately.
    ```
  </Tab>

  <Tab title="DashScope">
    **请求示例**

    <CodeGroup>
      ```python Python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
      messages = [
        {
          "role": "user",
          "content": "Este conjunto de biosensores utiliza grafeno, un material novedoso. Su objetivo son los elementos químicos. Su agudo «sentido del olfato» le permite reflejar el estado de salud del cuerpo de forma más profunda y precisa."
        }
      ]
      translation_options = {
        "source_lang": "auto",
        "target_lang": "English",
        "terms": [
          {
            "source": "biosensor",
            "target": "biological sensor"
          },
          {
            "source": "estado de salud del cuerpo",
            "target": "health status of the body"
          }
        ]
      }
      response = dashscope.Generation.call(
        # 若未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model="qwen-mt-turbo",  # 本示例使用 qwen-mt-turbo，您可根据需要替换为其他模型。
        messages=messages,
        result_format='message',
        translation_options=translation_options
      )
      print(response.output.choices[0].message.content)
      ```

      ```java Java
      // DashScope SDK 版本需为 2.20.6 或更高。
      import java.lang.System;
      import java.util.Collections;
      import java.util.Arrays;
      import com.alibaba.dashscope.aigc.generation.Generation;
      import com.alibaba.dashscope.aigc.generation.GenerationParam;
      import com.alibaba.dashscope.aigc.generation.GenerationResult;
      import com.alibaba.dashscope.aigc.generation.TranslationOptions;
      import com.alibaba.dashscope.aigc.generation.TranslationOptions.Term;
      import com.alibaba.dashscope.common.Message;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.InputRequiredException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.protocol.Protocol;

      public class Main {
        public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
          Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");
          Message userMsg = Message.builder()
              .role(Role.USER.getValue())
              .content("Este conjunto de biosensores utiliza grafeno, un material novedoso. Su objetivo son los elementos químicos. Su agudo «sentido del olfato» le permite reflejar el estado de salud del cuerpo de forma más profunda y precisa.")
              .build();
          Term term1 = Term.builder()
              .source("biosensor")
              .target("biological sensor")
              .build();
          Term term2 = Term.builder()
              .source("estado de salud del cuerpo")
              .target("health status of the body")
              .build();
          TranslationOptions options = TranslationOptions.builder()
              .sourceLang("auto")
              .targetLang("English")
              .terms(Arrays.asList(term1, term2))
              .build();
          GenerationParam param = GenerationParam.builder()
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen-mt-plus")
              .messages(Collections.singletonList(userMsg))
              .resultFormat(GenerationParam.ResultFormat.MESSAGE)
              .translationOptions(options)
              .build();
          return gen.call(param);
        }
        public static void main(String[] args) {
          try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
          } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("Error message: "+e.getMessage());
          }
          System.exit(0);
        }
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "model": "qwen-mt-turbo",
        "input": {
          "messages": [
            {
              "content": "Este conjunto de biosensores utiliza grafeno, un material novedoso. Su objetivo son los elementos químicos. Su agudo «sentido del olfato» le permite reflejar el estado de salud del cuerpo de forma más profunda y precisa.",
              "role": "user"
            }
          ]
        },
        "parameters": {
          "translation_options": {
            "source_lang": "auto",
            "target_lang": "English",
            "terms": [
              {
                "source": "biosensor",
                "target": "biological sensor"
              },
              {
                "source": "estado de salud del cuerpo",
                "target": "health status of the body"
              }
            ]
          }
        }
      }'
      ```
    </CodeGroup>

    **响应示例**

    ```text
    This biological sensor uses graphene, a new material, and its target is chemical elements. Its sensitive "nose" can more deeply and accurately reflect the health status of the human body.
    ```
  </Tab>
</Tabs>

### 翻译记忆

如需指定模型使用特定的翻译风格或句式，您可以在 `tm_list` 字段中提供源语言-目标语言的句对作为示例。模型会模仿这些示例的风格来完成当前翻译任务。

<Steps>
  <Step title="定义翻译记忆">
    创建一个名为 `tm_list` 的 JSON 数组。数组中每个 JSON 对象包含一个源语言句子及其对应的译文，格式如下：

    ```json
    {
      "source": "源语言语句",
      "target": "对应译文"
    }
    ```
  </Step>

  <Step title="传递翻译记忆">
    通过 `translation_options` 参数传递翻译记忆数组。
  </Step>
</Steps>

<Tabs>
  <Tab title="OpenAI 兼容">
    **请求示例**

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        # 若未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )
      messages = [
        {
          "role": "user",
          "content": "El siguiente comando muestra la información de la versión de Thrift instalada."
        }
      ]
      translation_options = {
        "source_lang": "auto",
        "target_lang": "English",
        "tm_list": [
          {
            "source": "Puede utilizar uno de los siguientes métodos para consultar la versión del motor de un clúster:",
            "target": "You can use one of the following methods to query the engine version of a cluster:"
          },
          {
            "source": "La versión de Thrift utilizada por nuestro HBase en la nube es la 0.9.0. Por lo tanto, recomendamos que la versión del cliente también sea la 0.9.0. Puede descargar Thrift 0.9.0 desde aquí. El paquete de código fuente descargado se utilizará posteriormente. Primero debe instalar el entorno de compilación de Thrift. Para la instalación desde el código fuente, puede consultar el sitio web oficial de Thrift.",
            "target": "The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website."
          },
          {
            "source": "Puede instalar el SDK a través de PyPI. El comando de instalación es el siguiente:",
            "target": "You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:"
          }
        ]
      }

      completion = client.chat.completions.create(
        model="qwen-mt-plus",
        messages=messages,
        extra_body={
          "translation_options": translation_options
        }
      )
      print(completion.choices[0].message.content)
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen-mt-turbo",
        "messages": [
          {
            "role": "user",
            "content": "El siguiente comando muestra la información de la versión de Thrift instalada."
          }
        ],
        "translation_options": {
          "source_lang": "auto",
          "target_lang": "English",
          "tm_list":[
                {"source": "Puede utilizar uno de los siguientes métodos para consultar la versión del motor de un clúster:", "target": "You can use one of the following methods to query the engine version of a cluster:"},
                {"source": "La versión de Thrift utilizada por nuestro HBase en la nube es la 0.9.0. Por lo tanto, recomendamos que la versión del cliente también sea la 0.9.0. Puede descargar Thrift 0.9.0 desde aquí. El paquete de código fuente descargado se utilizará posteriormente. Primero debe instalar el entorno de compilación de Thrift. Para la instalación desde el código fuente, puede consultar el sitio web oficial de Thrift.", "target": "The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website."},
                {"source": "Puede instalar el SDK a través de PyPI. El comando de instalación es el siguiente:", "target": "You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:"}
          ]
        }
      }'
      ```
    </CodeGroup>

    **响应示例**

    ```text
    You can run the following command to view the version of Thrift that is installed:
    ```
  </Tab>

  <Tab title="DashScope">
    **请求示例**

    <CodeGroup>
      ```python Python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
      messages = [
        {
          "role": "user",
          "content": "El siguiente comando muestra la información de la versión de Thrift instalada."
        }
      ]
      translation_options = {
        "source_lang": "auto",
        "target_lang": "English",
        "tm_list": [
          {
            "source": "Puede utilizar uno de los siguientes métodos para consultar la versión del motor de un clúster:",
            "target": "You can use one of the following methods to query the engine version of a cluster:"
          },
          {
            "source": "La versión de Thrift utilizada por nuestro HBase en la nube es la 0.9.0. Por lo tanto, recomendamos que la versión del cliente también sea la 0.9.0. Puede descargar Thrift 0.9.0 desde aquí. El paquete de código fuente descargado se utilizará posteriormente. Primero debe instalar el entorno de compilación de Thrift. Para la instalación desde el código fuente, puede consultar el sitio web oficial de Thrift.",
            "target": "The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website."
          },
          {
            "source": "Puede instalar el SDK a través de PyPI. El comando de instalación es el siguiente:",
            "target": "You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:"
          }
        ]}
      response = dashscope.Generation.call(
        # 若未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model="qwen-mt-turbo",  # 本示例使用 qwen-mt-turbo，您可根据需要替换为其他模型。
        messages=messages,
        result_format='message',
        translation_options=translation_options
      )
      print(response.output.choices[0].message.content)
      ```

      ```java Java
      // DashScope SDK 版本需为 2.20.6 或更高。
      import java.lang.System;
      import java.util.Collections;
      import java.util.Arrays;
      import com.alibaba.dashscope.aigc.generation.Generation;
      import com.alibaba.dashscope.aigc.generation.GenerationParam;
      import com.alibaba.dashscope.aigc.generation.GenerationResult;
      import com.alibaba.dashscope.aigc.generation.TranslationOptions;
      import com.alibaba.dashscope.aigc.generation.TranslationOptions.Tm;
      import com.alibaba.dashscope.common.Message;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.InputRequiredException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.protocol.Protocol;

      public class Main {
        public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
          Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");
          Message userMsg = Message.builder()
              .role(Role.USER.getValue())
              .content("El siguiente comando muestra la información de la versión de Thrift instalada.")
              .build();
          Tm tm1 = Tm.builder()
              .source("Puede utilizar uno de los siguientes métodos para consultar la versión del motor de un clúster:")
              .target("You can use one of the following methods to query the engine version of a cluster:")
              .build();
          Tm tm2 = Tm.builder()
              .source("La versión de Thrift utilizada por nuestro HBase en la nube es la 0.9.0. Por lo tanto, recomendamos que la versión del cliente también sea la 0.9.0. Puede descargar Thrift 0.9.0 desde aquí. El paquete de código fuente descargado se utilizará posteriormente. Primero debe instalar el entorno de compilación de Thrift. Para la instalación desde el código fuente, puede consultar el sitio web oficial de Thrift.")
              .target("The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website.")
              .build();
          Tm tm3 = Tm.builder()
              .source("Puede instalar el SDK a través de PyPI. El comando de instalación es el siguiente:")
              .target("You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:")
              .build();
          TranslationOptions options = TranslationOptions.builder()
              .sourceLang("auto")
              .targetLang("English")
              .tmList(Arrays.asList(tm1, tm2, tm3))
              .build();
          GenerationParam param = GenerationParam.builder()
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen-mt-plus")
              .messages(Collections.singletonList(userMsg))
              .resultFormat(GenerationParam.ResultFormat.MESSAGE)
              .translationOptions(options)
              .build();
          return gen.call(param);
        }
        public static void main(String[] args) {
          try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
          } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("Error message: "+e.getMessage());
          }
          System.exit(0);
        }
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "model": "qwen-mt-turbo",
        "input": {
          "messages": [
            {
              "content": "El siguiente comando muestra la información de la versión de Thrift instalada.",
              "role": "user"
            }
          ]
        },
        "parameters": {
          "translation_options": {
            "source_lang": "auto",
            "target_lang": "English",
            "tm_list":[
                {"source": "Puede utilizar uno de los siguientes métodos para consultar la versión del motor de un clúster:", "target": "You can use one of the following methods to query the engine version of a cluster:"},
                {"source": "La versión de Thrift utilizada por nuestro HBase en la nube es la 0.9.0. Por lo tanto, recomendamos que la versión del cliente también sea la 0.9.0. Puede descargar Thrift 0.9.0 desde aquí. El paquete de código fuente descargado se utilizará posteriormente. Primero debe instalar el entorno de compilación de Thrift. Para la instalación desde el código fuente, puede consultar el sitio web oficial de Thrift.", "target": "The version of Thrift used by ApsaraDB for HBase is 0.9.0. Therefore, we recommend that you use Thrift 0.9.0 to create a client. Click here to download Thrift 0.9.0. The downloaded source code package will be used later. You must install the Thrift compiling environment first. For more information, see Thrift official website."},
                {"source": "Puede instalar el SDK a través de PyPI. El comando de instalación es el siguiente:", "target": "You can run the following command in Python Package Index (PyPI) to install Elastic Container Instance SDK for Python:"}
            ]
        }
      }'
      ```
    </CodeGroup>

    **响应示例**

    ```text
    You can use the following commands to check the version information of thrift installed;
    ```
  </Tab>
</Tabs>

### 领域提示

如需让翻译风格适应特定领域，您可以通过 `translation_options` 参数传递领域提示。例如，法律或政务领域的翻译应使用正式用语，而社交媒体的翻译应口语化。

<Warning>领域提示目前仅支持英文。</Warning>

<Tabs>
  <Tab title="OpenAI 兼容">
    **请求示例**

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        # 若未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )
      messages = [
        {
          "role": "user",
          "content": "La segunda instrucción SELECT devuelve un número que indica la cantidad de filas que habría devuelto la primera instrucción SELECT si no se hubiera utilizado la cláusula LIMIT."
        }
      ]

      # --- 第一次请求：不使用 domains 参数 ---
      print("--- [不使用领域提示的翻译结果] ---")
      translation_options_without_domains = {
        "source_lang": "auto",
        "target_lang": "English",
      }

      completion_without_domains = client.chat.completions.create(
        model="qwen-mt-plus",
        messages=messages,
        extra_body={
          "translation_options": translation_options_without_domains
        }
      )
      print(completion_without_domains.choices[0].message.content)

      print("\n" + "="*50 + "\n") # 对比分隔线

      # --- 第二次请求：使用 domains 参数 ---
      print("--- [使用领域提示的翻译结果] ---")
      translation_options_with_domains = {
        "source_lang": "auto",
        "target_lang": "English",
        "domains": "The sentence is from a cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style."
      }

      completion_with_domains = client.chat.completions.create(
        model="qwen-mt-plus",
        messages=messages,
        extra_body={
          "translation_options": translation_options_with_domains
        }
      )
      print(completion_with_domains.choices[0].message.content)
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen-mt-turbo",
        "messages": [
          {
            "role": "user",
            "content": "La segunda instrucción SELECT devuelve un número que indica la cantidad de filas que habría devuelto la primera instrucción SELECT si no se hubiera utilizado la cláusula LIMIT."
          }
        ],
        "translation_options": {
          "source_lang": "auto",
          "target_lang": "English",
          "domains": "The sentence is from a cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style."
        }
      }'
      ```
    </CodeGroup>

    **响应示例**

    ```text
    --- [不使用领域提示的翻译结果] ---
    The second SELECT statement returns a number indicating how many rows the first SELECT statement would return without the LIMIT clause.

    ==================================================

    --- [使用领域提示的翻译结果] ---
    The second SELECT statement returns a number that indicates how many rows the first SELECT statement would have returned if it had not included a LIMIT clause.
    ```
  </Tab>

  <Tab title="DashScope">
    **请求示例**

    <CodeGroup>
      ```python Python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
      messages = [
        {
          "role": "user",
          "content": "La segunda instrucción SELECT devuelve un número que indica la cantidad de filas que habría devuelto la primera instrucción SELECT si no se hubiera utilizado la cláusula LIMIT."
        }
      ]
      translation_options = {
        "source_lang": "auto",
        "target_lang": "English",
        "domains": "The sentence is from a cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style."
      }
      response = dashscope.Generation.call(
        # 若未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model="qwen-mt-turbo",
        messages=messages,
        result_format='message',
        translation_options=translation_options
      )
      print(response.output.choices[0].message.content)
      ```

      ```java Java
      // DashScope SDK 版本需为 2.20.6 或更高。
      import java.lang.System;
      import java.util.Collections;
      import com.alibaba.dashscope.aigc.generation.Generation;
      import com.alibaba.dashscope.aigc.generation.GenerationParam;
      import com.alibaba.dashscope.aigc.generation.GenerationResult;
      import com.alibaba.dashscope.aigc.generation.TranslationOptions;
      import com.alibaba.dashscope.common.Message;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.InputRequiredException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.protocol.Protocol;

      public class Main {
        public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
          Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");
          Message userMsg = Message.builder()
              .role(Role.USER.getValue())
              .content("La segunda instrucción SELECT devuelve un número que indica la cantidad de filas que habría devuelto la primera instrucción SELECT si no se hubiera utilizado la cláusula LIMIT.")
              .build();
          TranslationOptions options = TranslationOptions.builder()
              .sourceLang("auto")
              .targetLang("English")
              .domains("The sentence is from a cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style.")
              .build();
          GenerationParam param = GenerationParam.builder()
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              // 注意：qwen-mt-lite 不支持领域提示
              .model("qwen-mt-plus")
              .messages(Collections.singletonList(userMsg))
              .resultFormat(GenerationParam.ResultFormat.MESSAGE)
              .translationOptions(options)
              .build();
          return gen.call(param);
        }
        public static void main(String[] args) {
          try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
          } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("Error message: "+e.getMessage());
          }
          System.exit(0);
        }
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "model": "qwen-mt-turbo",
        "input": {
          "messages": [
            {
              "content": "La segunda instrucción SELECT devuelve un número que indica la cantidad de filas que habría devuelto la primera instrucción SELECT si no se hubiera utilizado la cláusula LIMIT.",
              "role": "user"
            }
          ]
        },
        "parameters": {
          "translation_options": {
            "source_lang": "auto",
            "target_lang": "English",
            "domains": "The sentence is from a cloud IT domain. It mainly involves computer-related software development and usage methods, including many terms related to computer software and hardware. Pay attention to professional troubleshooting terminologies and sentence patterns when translating. Translate into this IT domain style."}
        }
      }'
      ```
    </CodeGroup>

    **响应示例**

    ```text
    The second SELECT statement returns a number that indicates how many rows were returned by the first SELECT statement without a LIMIT clause.
    ```
  </Tab>
</Tabs>

<a id="custom-prompts" />

## 自定义提示词

您可以在 Qwen-MT 中使用自定义提示词来指定语言、风格等细节。此方式与 `translation_options` 参数互斥——如果同时使用，`translation_options` 可能不会生效。

<Tip>为获得最佳翻译效果，建议使用 `translation_options` 配置翻译设置。</Tip>

示例：将西班牙语翻译为英语（法律领域）：

<Tabs>
  <Tab title="OpenAI 兼容">
    **请求示例**

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        # 若未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )
      prompt_template = """
      # Role
      You are a professional legal translation expert, proficient in both Spanish and English, and you are especially skilled at handling commercial contracts and legal documents.

      # Task
      I need you to translate the following Spanish legal text into professional, accurate, and formal English.

      # Translation Requirements
      1.  **Fidelity to the Original**: Strictly translate according to the meaning and legal intent of the original text. Do not add or omit information.
      2.  **Precise Terminology**: Use standard legal terms common in the Common Law system. For example, "甲方" should be translated as "Party A", "乙方" as "Party B", and "不可抗力" as "Force Majeure".
      3.  **Formal Tone**: Maintain the rigorous, objective, and formal style inherent in legal documents.
      4.  **Clarity of Language**: The translation must be clear, unambiguous, and conform to the expressive conventions of English legal writing.
      5.  **Format Preservation**: Retain the paragraphs, numbering, and basic format of the original text.

      # Text to be Translated
      {text_to_translate}
      """

      # --- 2. 准备待翻译的法律文本 ---
      chinese_legal_text = "Este contrato entrará en vigor a partir de la fecha en que ambas partes lo firmen y sellen, y tendrá una vigencia de un año."
      final_prompt = prompt_template.format(text_to_translate=chinese_legal_text)

      # --- 3. 构建 messages ---
      messages = [{"role": "user", "content": final_prompt}]

      # --- 4. 发起 API 请求 ---
      completion = client.chat.completions.create(model="qwen-mt-plus", messages=messages)

      # --- 5. 打印翻译结果 ---
      translation_result = completion.choices[0].message.content
      print(translation_result)
      ```

      ```javascript Node.js
      import OpenAI from 'openai';

      const client = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
      });

      const promptTemplate = `
      # Role
      You are a professional legal translation expert, proficient in both Spanish and English, specializing in business contracts and legal documents.

      # Task
      I need you to translate the following Spanish legal text into professional, accurate, and formal English.

      # Translation Requirements
      1.  **Fidelity to the Original**: Translate strictly according to the meaning and legal intent of the original text. Do not add or omit information.
      2.  **Precise Terminology**: Use standard legal terms common in the Common Law system. For example, "甲方" should be translated as "Party A", "乙方" as "Party B", and "不可抗力" as "Force Majeure".
      3.  **Formal Tone**: Maintain the rigorous, objective, and formal tone inherent in legal documents.
      4.  **Clarity**: The translation must be clear, unambiguous, and conform to the expressive conventions of English legal writing.
      5.  **Format Preservation**: Retain the paragraphs, numbering, and basic format of the original text.

      # Text to Translate
      {text_to_translate}
      `;

      const spanishLegalText = "This Contract shall become effective from the date of signature and seal by both parties and shall be valid for a period of one year.";
      const finalPrompt = promptTemplate.replace('{text_to_translate}', spanishLegalText);

      const messages = [{"role": "user", "content": finalPrompt}];

      async function main() {
        const completion = await client.chat.completions.create({
          model: "qwen-mt-plus",
          messages: messages
        });

        const translationResult = completion.choices[0].message.content;
        console.log(translationResult);
      }

      main();
      ```
    </CodeGroup>

    **响应示例**

    ```text
    This Contract shall become effective from the date on which both parties sign and affix their seals, and its term of validity shall be one year.
    ```
  </Tab>

  <Tab title="DashScope">
    **请求示例**

    <CodeGroup>
      ```python Python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
      prompt_template = """
      # Role
      You are a professional legal translation expert, proficient in both Spanish and English, with special expertise in handling business contracts and legal documents.

      # Task
      I need you to translate the following Spanish legal text into professional, accurate, and formal English.

      # Translation Requirements
      1.  **Fidelity to the Original**: Strictly translate according to the meaning and legal intent of the original text. Do not add or omit any information.
      2.  **Precise Terminology**: Use standard legal terms common to the Common Law system. For example, "甲方" should be translated as "Party A", "乙方" as "Party B", and "不可抗力" as "Force Majeure".
      3.  **Formal Tone**: Maintain the rigorous, objective, and formal style inherent in legal documents.
      4.  **Clear Phrasing**: The translation must be clear, unambiguous, and conform to the conventions of English legal writing.
      5.  **Preserve Formatting**: Maintain the paragraphs, numbering, and basic format of the original text.

      # Text to be Translated
      {text_to_translate}
      """

      # --- 2. 准备待翻译的法律文本 ---
      chinese_legal_text = "This Contract shall become effective from the date of signature and seal by both parties and shall be valid for a period of one year."
      final_prompt = prompt_template.format(text_to_translate=chinese_legal_text)

      # --- 3. 构建 messages ---
      messages = [
        {
          "role": "user",
          "content": final_prompt
        }
      ]

      response = dashscope.Generation.call(
        # 若未配置环境变量，请将下行替换为您的 API Key：api_key="sk-xxx",
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model="qwen-mt-plus",
        messages=messages,
        result_format='message',
      )
      print(response.output.choices[0].message.content)
      ```

      ```java Java
      // DashScope SDK 版本需为 2.20.6 或更高。
      import java.lang.System;
      import java.util.Collections;
      import com.alibaba.dashscope.aigc.generation.Generation;
      import com.alibaba.dashscope.aigc.generation.GenerationParam;
      import com.alibaba.dashscope.aigc.generation.GenerationResult;
      import com.alibaba.dashscope.common.Message;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.InputRequiredException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.protocol.Protocol;

      public class Main {
        public static GenerationResult callWithMessage() throws ApiException, NoApiKeyException, InputRequiredException {
          Generation gen = new Generation(Protocol.HTTP.getValue(), "https://dashscope.aliyuncs.com/api/v1");
          String promptTemplate = "# Role\n" +
              "You are a professional legal translation expert, proficient in both Spanish and English, specializing in business contracts and legal documents.\n\n" +
              "# Task\n" +
              "I need you to translate the following Spanish legal text into professional, accurate, and formal English.\n\n" +
              "# Translation Requirements\n" +
              "1.  **Fidelity to the Original**: Translate strictly according to the meaning and legal intent of the original text. Do not add or omit any information.\n" +
              "2.  **Precise Terminology**: Use standard legal terms common to the Common Law system.\n" +
              "3.  **Formal Tone**: Maintain the rigorous, objective, and formal tone inherent in legal documents.\n" +
              "4.  **Clarity**: The translation must be clear, unambiguous, and conform to the conventions of English legal writing.\n" +
              "5.  **Format Preservation**: Retain the paragraphs, numbering, and basic format of the original text.\n\n" +
              "# Text to Translate\n%s";
          String spanishLegalText = "Este contrato entrará en vigor a partir de la fecha en que ambas partes lo firmen y sellen, y tendrá una vigencia de un año.";
          String finalPrompt = String.format(promptTemplate, spanishLegalText);
          Message userMsg = Message.builder()
              .role(Role.USER.getValue())
              .content(finalPrompt)
              .build();
          GenerationParam param = GenerationParam.builder()
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen-mt-plus")
              .messages(Collections.singletonList(userMsg))
              .resultFormat(GenerationParam.ResultFormat.MESSAGE)
              .build();
          return gen.call(param);
        }
        public static void main(String[] args) {
          try {
            GenerationResult result = callWithMessage();
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
          } catch (ApiException | NoApiKeyException | InputRequiredException e) {
            System.err.println("Error message: "+e.getMessage());
            e.printStackTrace();
          }
          }
      }
      ```
    </CodeGroup>

    **响应示例**

    ```text
    This Contract shall become effective from the date on which both parties sign and affix their seals, and its term of validity shall be one year.
    ```
  </Tab>
</Tabs>

## 生产建议

- **控制输入 Token 数量**

  Qwen-MT 模型的最大输入限制为 8,192 个 Token。对于长内容，可采用以下策略控制输入 Token 数：

  - **分段翻译**：翻译长文本时，按语义单元（如段落或完整句子）而非字符数分段处理，以保持上下文完整性，提高翻译质量。
  - **提供最相关的参考内容**：术语、翻译记忆和领域提示都会作为 Token 加入输入提示词。为优化 Token 用量，请只提供与当前任务最相关的参考内容，避免使用大而全的通用列表。

- **根据场景设置 `source_lang`**

  - 源语言不确定时（如社交聊天中包含多语言文本），将 `source_lang` 设为 `auto`，由模型自动识别源语言。
  - 语言固定且准确性要求高的场景（如技术文档、操作手册），始终明确指定 `source_lang`，可以提高翻译准确性。

<a id="supported-languages" />

## 支持的语言

发送请求时，请使用下表中的 **English name** 或 **Code**。

<Tip>如果不确定源语言，可以将 `source_lang` 参数设为 `auto` 进行自动检测。</Tip>

<Tabs>
  <Tab title="qwen-mt-plus/flash/turbo（92 种语言）">
| 语言         | English name           | Code   |
| ---------- | ---------------------- | ------ |
| 英语         | English                | en     |
| 简体中文       | Chinese                | zh     |
| 繁体中文       | Traditional Chinese    | zh\_tw |
| 俄语         | Russian                | ru     |
| 日语         | Japanese               | ja     |
| 韩语         | Korean                 | ko     |
| 西班牙语       | Spanish                | es     |
| 法语         | French                 | fr     |
| 葡萄牙语       | Portuguese             | pt     |
| 德语         | German                 | de     |
| 意大利语       | Italian                | it     |
| 泰语         | Thai                   | th     |
| 越南语        | Vietnamese             | vi     |
| 印度尼西亚语     | Indonesian             | id     |
| 马来语        | Malay                  | ms     |
| 阿拉伯语       | Arabic                 | ar     |
| 印地语        | Hindi                  | hi     |
| 希伯来语       | Hebrew                 | he     |
| 缅甸语        | Burmese                | my     |
| 泰米尔语       | Tamil                  | ta     |
| 乌尔都语       | Urdu                   | ur     |
| 孟加拉语       | Bengali                | bn     |
| 波兰语        | Polish                 | pl     |
| 荷兰语        | Dutch                  | nl     |
| 罗马尼亚语      | Romanian               | ro     |
| 土耳其语       | Turkish                | tr     |
| 高棉语        | Khmer                  | km     |
| 老挝语        | Lao                    | lo     |
| 粤语         | Cantonese              | yue    |
| 捷克语        | Czech                  | cs     |
| 希腊语        | Greek                  | el     |
| 瑞典语        | Swedish                | sv     |
| 匈牙利语       | Hungarian              | hu     |
| 丹麦语        | Danish                 | da     |
| 芬兰语        | Finnish                | fi     |
| 乌克兰语       | Ukrainian              | uk     |
| 保加利亚语      | Bulgarian              | bg     |
| 塞尔维亚语      | Serbian                | sr     |
| 泰卢固语       | Telugu                 | te     |
| 南非荷兰语      | Afrikaans              | af     |
| 亚美尼亚语      | Armenian               | hy     |
| 阿萨姆语       | Assamese               | as     |
| 阿斯图里亚斯语    | Asturian               | ast    |
| 巴斯克语       | Basque                 | eu     |
| 白俄罗斯语      | Belarusian             | be     |
| 波斯尼亚语      | Bosnian                | bs     |
| 加泰罗尼亚语     | Catalan                | ca     |
| 宿务语        | Cebuano                | ceb    |
| 克罗地亚语      | Croatian               | hr     |
| 埃及阿拉伯语     | Egyptian Arabic        | arz    |
| 爱沙尼亚语      | Estonian               | et     |
| 加利西亚语      | Galician               | gl     |
| 格鲁吉亚语      | Georgian               | ka     |
| 古吉拉特语      | Gujarati               | gu     |
| 冰岛语        | Icelandic              | is     |
| 爪哇语        | Javanese               | jv     |
| 卡纳达语       | Kannada                | kn     |
| 哈萨克语       | Kazakh                 | kk     |
| 拉脱维亚语      | Latvian                | lv     |
| 立陶宛语       | Lithuanian             | lt     |
| 卢森堡语       | Luxembourgish          | lb     |
| 马其顿语       | Macedonian             | mk     |
| 迈蒂利语       | Maithili               | mai    |
| 马耳他语       | Maltese                | mt     |
| 马拉地语       | Marathi                | mr     |
| 美索不达米亚阿拉伯语 | Mesopotamian Arabic    | acm    |
| 摩洛哥阿拉伯语    | Moroccan Arabic        | ary    |
| 内志阿拉伯语     | Najdi Arabic           | ars    |
| 尼泊尔语       | Nepali                 | ne     |
| 北阿塞拜疆语     | North Azerbaijani      | az     |
| 北黎凡特阿拉伯语   | North Levantine Arabic | apc    |
| 北乌兹别克语     | Northern Uzbek         | uz     |
| 书面挪威语      | Norwegian Bokmal       | nb     |
| 新挪威语       | Norwegian Nynorsk      | nn     |
| 奥克西坦语      | Occitan                | oc     |
| 奥里亚语       | Odia                   | or     |
| 邦阿西楠语      | Pangasinan             | pag    |
| 西西里语       | Sicilian               | scn    |
| 信德语        | Sindhi                 | sd     |
| 僧伽罗语       | Sinhala                | si     |
| 斯洛伐克语      | Slovak                 | sk     |
| 斯洛文尼亚语     | Slovenian              | sl     |
| 南黎凡特阿拉伯语   | South Levantine Arabic | ajp    |
| 斯瓦希里语      | Swahili                | sw     |
| 他加禄语       | Tagalog                | tl     |
| 塔伊兹-亚丁阿拉伯语 | Ta'izzi-Adeni Arabic   | acq    |
| 托斯克阿尔巴尼亚语  | Tosk Albanian          | sq     |
| 突尼斯阿拉伯语    | Tunisian Arabic        | aeb    |
| 威尼斯语       | Venetian               | vec    |
| 瓦瑞语        | Waray                  | war    |
| 威尔士语       | Welsh                  | cy     |
| 西波斯语       | Western Persian        | fa     |
  </Tab>

  <Tab title="qwen-mt-lite（31 种语言）">
| 语言     | English name        | Code   |
| ------ | ------------------- | ------ |
| 英语     | English             | en     |
| 简体中文   | Chinese             | zh     |
| 繁体中文   | Traditional Chinese | zh\_tw |
| 俄语     | Russian             | ru     |
| 日语     | Japanese            | ja     |
| 韩语     | Korean              | ko     |
| 西班牙语   | Spanish             | es     |
| 法语     | French              | fr     |
| 葡萄牙语   | Portuguese          | pt     |
| 德语     | German              | de     |
| 意大利语   | Italian             | it     |
| 泰语     | Thai                | th     |
| 越南语    | Vietnamese          | vi     |
| 印度尼西亚语 | Indonesian          | id     |
| 马来语    | Malay               | ms     |
| 阿拉伯语   | Arabic              | ar     |
| 印地语    | Hindi               | hi     |
| 希伯来语   | Hebrew              | he     |
| 乌尔都语   | Urdu                | ur     |
| 孟加拉语   | Bengali             | bn     |
| 波兰语    | Polish              | pl     |
| 荷兰语    | Dutch               | nl     |
| 土耳其语   | Turkish             | tr     |
| 高棉语    | Khmer               | km     |
| 捷克语    | Czech               | cs     |
| 瑞典语    | Swedish             | sv     |
| 匈牙利语   | Hungarian           | hu     |
| 丹麦语    | Danish              | da     |
| 芬兰语    | Finnish             | fi     |
| 他加禄语   | Tagalog             | tl     |
| 波斯语    | Persian             | fa     |
  </Tab>
</Tabs>

## API 参考

API 参数详情请参见：

- [OpenAI 兼容接口](/api-reference/chat/openai-chat)
- [DashScope 接口](/api-reference/chat/dashscope)
