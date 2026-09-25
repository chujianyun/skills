> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 联网搜索

> 让模型响应基于实时网络数据——查询天气、股票价格、近期新闻等训练数据截止日期后的内容。

由于训练数据的时效性限制，大模型无法准确回答股票价格、明日天气等实时问题，启用联网搜索后，模型将基于实时检索数据回复。

<Note>
  调用 API 前，请先[获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。
</Note>

## 使用方式

联网搜索支持以下三种 API 调用方式，启用参数各有不同：

<Note>
  qwen3.7-max 等模型的联网搜索请使用[快速开始](#快速开始)中的 Responses API 或 DashScope API。
</Note>

## 快速开始

<Tabs>
  <Tab title="OpenAI 兼容 - Chat Completions">
    通过 `enable_search: true` 参数启用联网搜索。Python SDK 通过 `extra_body` 传入，Node.js SDK 作为顶层参数传入。

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )
      completion = client.chat.completions.create(
        model="qwen3-max",
        messages=[{"role": "user", "content": "杭州明天天气如何"}],
        extra_body={"enable_search": True}
      )
      print(completion.choices[0].message.content)
      ```

      ```javascript Node.js
      import OpenAI from "openai";

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      async function main() {
        const completion = await openai.chat.completions.create({
          model: "qwen3-max",
          messages: [{ role: "user", content: "杭州明天天气如何" }],
          enable_search: true
        });
        console.log(completion.choices[0].message.content);
      }
      main();
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3-max",
        "messages": [{"role": "user", "content": "杭州明天天气如何"}],
        "enable_search": true
      }'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="OpenAI 兼容 - Responses API">
    在 `tools` 数组中添加 `web_search`。建议同时开启 `web_extractor` 和 `code_interpreter` 以获取最佳效果。

    <Note>
      Responses API 支持 Qwen3.5 及之后的 Max、Plus、Flash 系列（含快照版本）、qwen3-max / qwen3-max-2026-01-23、deepseek-v4-pro-0813、deepseek-v4-flash、deepseek-v4-flash-0731。建议同时开启 `web_search`、`web_extractor` 和 `code_interpreter` 以获取最佳效果。
    </Note>

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
      )
      response = client.responses.create(
        model="qwen3-max-2026-01-23",
        input="杭州天气",
        tools=[
          {"type": "web_search"},
          {"type": "web_extractor"},
          {"type": "code_interpreter"}
        ],
        extra_body={"enable_thinking": True}
      )
      print(response.output_text)
      ```

      ```javascript Node.js
      import OpenAI from "openai";

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
      });

      async function main() {
        const response = await openai.responses.create({
          model: "qwen3-max-2026-01-23",
          input: "杭州天气",
          tools: [
            { type: "web_search" },
            { type: "web_extractor" },
            { type: "code_interpreter" }
          ],
          enable_thinking: true
        });
        console.log(response.output_text);
      }
      main();
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/responses \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3-max-2026-01-23",
        "input": "杭州天气",
        "tools": [{"type": "web_search"}, {"type": "web_extractor"}, {"type": "code_interpreter"}],
        "enable_thinking": true
      }'
      ```
    </CodeGroup>

    执行联网搜索后，搜索来源会在响应的 `output` 数组中 `type` 为 `web_search_call` 的元素内返回，其 `action.sources` 字段为搜索来源链接列表。可在上述示例的 `response` 基础上按如下方式提取：

    <Note>
      Responses API 暂不支持 `enable_source`、`enable_citation`、`citation_format` 参数，不会在回复内容中自动插入 `[1]` 角标。
    </Note>

    ```python Python
    # 在上述 response 的基础上提取搜索来源
    print("=" * 20 + "搜索来源" + "=" * 20)
    for item in response.output:
        if item.type == "web_search_call":
            for i, source in enumerate(item.action.sources, start=1):
                print(f"[{i}] {source.url}")
    ```
  </Tab>

  <Tab title="DashScope">
    通过 `enable_search=True` 参数启用联网搜索。

    <CodeGroup>
      ```python Python
      import os
      import dashscope
      dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

      response = dashscope.Generation.call(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        model="qwen3-max",
        messages=[{"role": "user", "content": "杭州明天天气如何"}],
        enable_search=True,
        result_format="message"
      )
      print(response.output.choices[0].message.content)
      ```

      ```java Java
      import java.util.Arrays;
      import com.alibaba.dashscope.aigc.generation.Generation;
      import com.alibaba.dashscope.aigc.generation.GenerationParam;
      import com.alibaba.dashscope.aigc.generation.GenerationResult;
      import com.alibaba.dashscope.common.Message;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.utils.Constants;

      public class Main {
        static { Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1"; }
        public static void main(String[] args) throws Exception {
          Generation gen = new Generation();
          Message userMsg = Message.builder()
            .role(Role.USER.getValue())
            .content("明天杭州什么天气？")
            .build();
          GenerationParam param = GenerationParam.builder()
            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
            .model("qwen3-max")
            .messages(Arrays.asList(userMsg))
            .resultFormat(GenerationParam.ResultFormat.MESSAGE)
            .enableSearch(true)
            .build();
          GenerationResult result = gen.call(param);
          System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent());
        }
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3-max",
        "input": {
          "messages": [{"role": "user", "content": "明天杭州天气如何？"}]
        },
        "parameters": {
          "enable_search": true,
          "result_format": "message"
        }
      }'
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## 多模态模型的联网搜索

qwen3.5-plus、qwen3.5-flash 以及 qwen3.5-omni 系列等模型支持图片、视频等多模态输入，属于多模态模型。这类模型需通过**多模态接口**（`multimodal-generation` 端点）调用：Python 与 Java 使用 `MultiModalConversation`，而不能使用面向纯文本模型的 `Generation`（`text-generation` 端点）。多模态模型的基础调用方式可参见[视觉推理](/developer-guides/multimodal/vision)、[图像与视频理解](/developer-guides/getting-started/vision-models)。

<Note>
  若使用 `Generation`（`text-generation` 端点）调用上述多模态模型，会返回 `400 url error, please check url`，请改用 `MultiModalConversation`（`multimodal-generation` 端点）。

  Java SDK 的 `MultiModalConversationParam` 提供 `enableSearch(true)` 用于开启联网搜索，但未提供 `searchOptions()` 方法，需通过通用参数 `parameter("search_options", ...)` 注入搜索策略等配置；Python 的 `MultiModalConversation.call` 可直接传入 `search_options`。

  多模态模型开启联网搜索时需使用**流式调用**（Java 使用 `streamCall`，Python 设置 `stream=True`），否则会返回 `Non-streaming mode does not support Web Search` 报错。
</Note>

<CodeGroup>
  ```python Python
  import os
  import dashscope
  from dashscope import MultiModalConversation

  responses = MultiModalConversation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3.5-plus",
    messages=[{"role": "user", "content": [{"text": "杭州今天天气如何"}]}],
    enable_search=True,
    search_options={
      "search_strategy": "agent",
      "enable_source": True,
    },
    stream=True,
    incremental_output=True,
  )
  for response in responses:
    print(response.output.choices[0].message.content)
  ```

  ```java Java
  // dashscope SDK >= 2.19.0
  import java.util.Arrays;
  import java.util.Collections;
  import io.reactivex.Flowable;
  import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
  import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
  import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
  import com.alibaba.dashscope.aigc.generation.SearchOptions;
  import com.alibaba.dashscope.common.MultiModalMessage;
  import com.alibaba.dashscope.common.Role;

  public class Main {
    public static void main(String[] args) throws Exception {
      MultiModalConversation conv = new MultiModalConversation();
      MultiModalMessage userMsg = MultiModalMessage.builder()
        .role(Role.USER.getValue())
        .content(Arrays.asList(Collections.singletonMap("text", "杭州今天天气如何")))
        .build();
      SearchOptions searchOptions = SearchOptions.builder()
        .searchStrategy("agent")
        .enableSource(true)
        .build();
      MultiModalConversationParam param = MultiModalConversationParam.builder()
        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
        .model("qwen3.5-plus")
        .messages(Arrays.asList(userMsg))
        .enableSearch(true)
        .parameter("search_options", searchOptions)
        .incrementalOutput(true)
        .build();
      Flowable<MultiModalConversationResult> result = conv.streamCall(param);
      result.blockingForEach(message ->
        System.out.print(message.getOutput().getChoices().get(0).getMessage().getContent()));
    }
  }
  ```
</CodeGroup>

## 支持的模型

**千问系列**

| 模型系列               | 可用模型                                                                                                                                |
| ------------------ | ----------------------------------------------------------------------------------------------------------------------------------- |
| Qwen3.8 Max        | qwen3.8-max                                                                                                                         |
| Qwen3.8 开源         | qwen3.8-2.4t-a95b                                                                                                                   |
| Qwen3.7 Max        | qwen3.7-max、qwen3.7-max-preview、qwen3.7-max-2026-05-17 及之后版本                                                                        |
| Qwen3.6 Max        | qwen3.6-max-preview                                                                                                                 |
| Qwen3 Max          | qwen3-max、qwen3-max-2025-09-23 及之后版本、qwen3-max-preview                                                                              |
| Qwen3.7 Plus       | qwen3.7-plus、qwen3.7-plus-2026-05-26 及之后版本                                                                                          |
| Qwen3.6 Plus       | qwen3.6-plus、qwen3.6-plus-2026-04-02 及之后版本                                                                                          |
| Qwen3.5 Plus       | qwen3.5-plus、qwen3.5-plus-2026-02-15 及之后版本                                                                                          |
| Qwen3.7 Flash      | qwen3.7-flash、qwen3.7-flash-2026-07-15 及之后版本                                                                                        |
| Qwen3.6 Flash      | qwen3.6-flash、qwen3.6-flash-2026-04-16 及之后版本                                                                                        |
| Qwen3.5 Flash      | qwen3.5-flash、qwen3.5-flash-2026-02-23 及之后版本                                                                                        |
| Qwen Max           | qwen-max 及之后的快照版本                                                                                                                   |
| Qwen Plus          | qwen-plus、qwen-plus-latest、qwen-plus-2025-07-14 及之后版本                                                                               |
| Qwen Flash         | qwen-flash、qwen-flash-2025-07-28 及之后版本                                                                                              |
| Qwen Turbo         | qwen-turbo                                                                                                                          |
| QwQ                | qwq-plus                                                                                                                            |
| Qwen Omni          | qwen3.5-omni-plus、qwen3.5-omni-plus-2026-03-15、qwen3.5-omni-flash、qwen3.5-omni-flash-2026-03-15                                     |
| Qwen Omni Realtime | qwen3.5-omni-plus-realtime、qwen3.5-omni-plus-realtime-2026-03-15、qwen3.5-omni-flash-realtime、qwen3.5-omni-flash-realtime-2026-03-15 |
| 角色扮演               | qwen-plus-character、qwen-flash-character、qwen-flash-character-2026-02-26                                                            |

2025 年 7 月后发布的 Qwen Max、Qwen Plus、Qwen Flash 模型自动支持联网搜索。

**第三方模型**

| 提供商      | 可用模型                                                                                                                                                                 |
| -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DeepSeek | deepseek-v4-pro-0813、deepseek-v4-pro、deepseek-v4-flash、deepseek-v4-flash-0731、deepseek-v3.2、deepseek-v3.2-exp、deepseek-v3.1、deepseek-r1-0528、deepseek-r1、deepseek-v3 |
| Kimi     | Moonshot-Kimi-K2-Instruct                                                                                                                                            |
| MiniMax  | MiniMax-M2.1                                                                                                                                                         |

## 核心能力

除基础搜索外，联网搜索还支持以下高级功能。DashScope 协议支持所有功能；OpenAI 兼容协议（Chat Completions）不支持返回搜索来源、角标标注等功能。

| 功能         | DashScope | OpenAI 兼容-Chat | OpenAI 兼容-Responses |
| ---------- | :-------: | :------------: | :-----------------: |
| 基础联网搜索     | 支持        | 支持             | 支持                  |
| 强制联网搜索     | 支持        | 支持             | 不支持                 |
| 设置搜索量级策略   | 支持        | 支持             | 不支持                 |
| 垂域搜索       | 支持        | 支持             | 不支持                 |
| 搜索时效性      | 支持        | 支持             | 不支持                 |
| 限定来源站点     | 支持        | 支持             | 不支持                 |
| 自然语言控制检索范围 | 支持        | 支持             | 不支持                 |
| 返回搜索来源     | 支持        | 不支持            | 不支持                 |
| 角标引用标注     | 支持        | 不支持            | 不支持                 |
| 提前返回搜索来源   | 支持        | 不支持            | 不支持                 |
| 图文混合输出     | 支持        | 支持             | 不支持                 |

## 搜索量级策略

通过 `search_options` 中的 `search_strategy` 字段控制搜索行为：

- **`turbo`**（默认）：兼顾响应速度与搜索效果，适用于大多数场景。
- **`max`**：调用多源搜索引擎，结果更详尽，响应时间更长。
- **`agent`**：多轮信息检索与整合，模型自主决定搜索时机和频次，适合复杂查询和英文场景。启用时仅支持 `enable_source`，其他联网搜索功能不可用，每次调用额外收费。
- **`agent_max`**：在 `agent` 基础上支持网页全文阅读。仅 qwen3-max、qwen3-max-2026-01-23 思考模式可用，每次调用额外收费。

<Tabs>
  <Tab title="OpenAI 兼容">
    ```python Python {5}
    extra_body={
      "enable_search": True,
      "search_options": {
        "search_strategy": "max"  # turbo（默认）/ max / agent / agent_max
      }
    }
    ```
  </Tab>

  <Tab title="DashScope">
    ```python Python {4-5}
    search_options={
      "search_strategy": "max",
      "enable_source": True
    }
    ```
  </Tab>
</Tabs>

## 强制联网搜索

默认情况下，模型会自行判断是否联网。设置 `forced_search: true` 可强制执行搜索，适用于强依赖实时信息的场景。

<Tabs>
  <Tab title="OpenAI 兼容">
    ```python Python {3}
    extra_body={
      "enable_search": True,
      "search_options": {"forced_search": True}
    }
    ```
  </Tab>

  <Tab title="DashScope">
    ```python Python {2}
    search_options={
      "forced_search": True
    }
    ```
  </Tab>
</Tabs>

## 获取搜索来源与引用标注

以上 `enable_source`、`enable_citation`、`citation_format` 参数仅支持 DashScope 调用方式。Responses API 暂不支持上述 `enable_citation` 角标标注（不会在回复内容中自动插入 `[1]` 角标），但搜索来源会在响应中自动返回。

1. **返回搜索来源**：设置 `enable_source: true`，响应的 `search_info.search_results` 包含来源列表，每项含 `index`、`title`、`url`。
2. **角标标注**：在 `enable_source: true` 的前提下，设置 `enable_citation: true`，回复正文中出现 `[1]` 等角标。
3. **角标样式**：通过 `citation_format` 设置，可选 `"[<number>]"`（默认）或 `"[ref_<number>]"`。

<CodeGroup>
  ```python Python
  import os
  import dashscope

  response = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=[{"role": "user", "content": "杭州明天天气是什么？"}],
    enable_search=True,
    search_options={
      "enable_source": True,
      "enable_citation": True,
      "citation_format": "[ref_<number>]"
    },
    result_format="message"
  )
  for web in response.output.search_info["search_results"]:
    print(f"[{web['index']}]: [{web['title']}]({web['url']})")
  print(response.output.choices[0].message.content)
  ```

  ```java Java
  SearchOptions searchOptions = SearchOptions.builder()
    .enableSource(true)
    .enableCitation(true)
    .citationFormat("[ref_<number>]")
    .build();
  ```

  ```bash curl
  curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen-plus",
    "input": {"messages": [{"role": "user", "content": "杭州明天天气是什么？"}]},
    "parameters": {
      "enable_search": true,
      "search_options": {
        "enable_source": true,
        "enable_citation": true,
        "citation_format": "[ref_<number>]"
      },
      "result_format": "message"
    }
  }'
  ```
</CodeGroup>

## 垂域搜索

设置 `enable_search_extension: true` 可为天气、股票等结构化查询检索垂直领域数据，比通用搜索结果更精准。DashScope Java SDK 不支持此参数。

| 领域       | 说明               | 示例                 |
| -------- | ---------------- | ------------------ |
| 天气       | 实时、未来及历史天气       | 杭州天气               |
| 股票       | A 股、港股、美股实时/历史行情 | 沪指昨天收盘点数           |
| 汇率       | 多币种最新汇率          | 人民币与美元的汇率          |
| 油价       | 全国各地最新汽柴油价格      | 杭州油价               |
| 万年历      | 农历、节气、吉凶宜忌       | 今天是农历几号            |
| 金价 / 银价  | 最新及历史行情          | 金价多少钱了             |
| 彩票       | 双色球、大乐透等开奖结果     | 最新一期双色球开奖结果        |
| 电视剧 / 电影 | 主流平台最新资讯         | 近期热播电视剧            |
| 车牌限行     | 根据车牌号查询当日限行      | 浙Axxxxxx，今天是否在杭州限行 |
| 足球赛事     | 英超、西甲等赛程与积分榜     | 英超现在哪支球队排名第一       |

<Tabs>
  <Tab title="OpenAI 兼容">
    ```python Python {3}
    extra_body={
      "enable_search": True,
      "search_options": {"enable_search_extension": True}
    }
    ```
  </Tab>

  <Tab title="DashScope">
    ```python Python {3-4}
    search_options={
      "enable_search_extension": True,
      "enable_source": True  # 垂域数据在 search_info["extra_tool_info"] 中返回
    }
    ```
  </Tab>
</Tabs>

## 搜索时效性

通过 `freshness` 参数限制搜索来源的时间范围，过滤超出范围的历史网页。仅对 `search_strategy: turbo` 生效。

**可选值**：`7`、`30`、`180`、`365`（天数）；不设置则不限制时间范围。

**支持的模型**：qwen3-max、qwen3-max-preview、qwen3-max-2025-09-23、qwen-plus、qwen-flash、qwen-plus-character、qwen-flash-character、qwen-flash-character-2026-02-26

<Tabs>
  <Tab title="OpenAI 兼容">
    ```python Python {4-5}
    extra_body={
      "enable_search": True,
      "search_options": {
        "search_strategy": "turbo",
        "freshness": 7  # 仅检索最近 7 天内的内容
      }
    }
    ```
  </Tab>

  <Tab title="DashScope">
    ```python Python {3-4}
    search_options={
      "search_strategy": "turbo",
      "freshness": 7,
      "enable_source": True
    }
    ```
  </Tab>
</Tabs>

## 限定来源站点

通过 `assigned_site_list` 将搜索限定在指定网站列表，最多配置 25 个站点。仅对 `search_strategy: turbo` 生效。当指定站点内无相关内容时，模型将使用自身知识回答。

<Note>
  DashScope Java SDK 不支持此参数。
</Note>

**支持的模型**：qwen3-max、qwen3-max-preview、qwen3-max-2025-09-23、qwen-plus、qwen-flash、qwen-plus-character、qwen-flash-character、qwen-flash-character-2026-02-26

<Tabs>
  <Tab title="OpenAI 兼容">
    ```python Python {4-5}
    extra_body={
      "enable_search": True,
      "search_options": {
        "search_strategy": "turbo",
        "assigned_site_list": ["baidu.com", "sina.cn"]
      }
    }
    ```
  </Tab>

  <Tab title="DashScope">
    ```python Python {3-5}
    search_options={
      "search_strategy": "turbo",
      "enable_source": True,
      "assigned_site_list": ["baidu.com", "sina.cn"]
    }
    ```
  </Tab>
</Tabs>

## 自然语言控制检索范围

通过 `prompt_intervene` 参数用自然语言引导搜索方向，适用于限定主题或地域的场景。

**支持的模型**：qwen3-max、qwen3-max-preview、qwen3-max-2025-09-23、qwen-plus、qwen-flash、qwen-plus-character、qwen-flash-character、qwen-flash-character-2026-02-26。DashScope Java SDK 不支持此参数。

<Tabs>
  <Tab title="OpenAI 兼容">
    ```python Python {4-7}
    extra_body={
      "enable_search": True,
      "search_options": {
        "search_strategy": "turbo",
        "intention_options": {
          "prompt_intervene": "仅检索AI技术相关内容"
        }
      }
    }
    ```
  </Tab>

  <Tab title="DashScope">
    ```python Python {3-7}
    search_options={
      "search_strategy": "turbo",
      "enable_source": True,
      "intention_options": {
        "prompt_intervene": "仅检索AI技术相关内容"
      }
    }
    ```
  </Tab>
</Tabs>

## 提前返回搜索来源

仅支持 DashScope 流式调用（不支持 OpenAI 兼容协议和 Java SDK）。在流式场景下，从获取搜索结果到生成首个 token 通常有 0.5 秒以上的延迟。设置 `prepend_search_result: true` 可在获取到搜索结果后立刻将其作为首个数据包返回，降低首包延时。

```python Python
import os
import dashscope

responses = dashscope.Generation.call(
  api_key=os.getenv("DASHSCOPE_API_KEY"),
  model="qwen-plus",
  messages=[{"role": "user", "content": "杭州明天天气是什么？"}],
  enable_search=True,
  search_options={
    "enable_source": True,
    "prepend_search_result": True  # 首包仅包含搜索来源
  },
  result_format="message",
  stream=True,
  incremental_output=True
)

first_chunk = True
for resp in responses:
  if first_chunk:
    search_info = resp.output.get("search_info", {})
    if search_info:
      print(f"已阅读 {len(search_info['search_results'])} 个页面")
      for web in search_info["search_results"]:
        print(f"[{web['index']}]: [{web['title']}]({web['url']})")
      first_chunk = False
  content = resp.output.choices[0].message.content
  print(content, end="")
```

## 图文混合输出

设置 `enable_text_image_mixed: true` 可让模型在回复中嵌入相关图片（以 HTML `<img>` 标签形式）。此参数与 `enable_search` 相互独立，无需同时启用。DashScope Java SDK 不支持此参数。

**支持的模型**：qwen-max、qwen-plus-latest、qwen-flash

<Tabs>
  <Tab title="OpenAI 兼容">
    ```python Python {4}
    completion = client.chat.completions.create(
      model="qwen-plus-latest",
      messages=[{"role": "user", "content": "介绍一下杭州西湖"}],
      extra_body={"enable_text_image_mixed": True}
    )
    ```
  </Tab>

  <Tab title="DashScope">
    ```python Python {5}
    response = dashscope.Generation.call(
      model="qwen-plus-latest",
      messages=[{"role": "user", "content": "介绍一下杭州西湖"}],
      enable_text_image_mixed=True,
      result_format="message"
    )
    ```
  </Tab>
</Tabs>

## 深度思考 + 联网搜索

联网搜索可与深度思考模式结合使用，适合行业趋势分析、多源信息整合等复杂任务。模型获取检索内容后先推理再生成回复，用户可观察推理路径。

**支持联网搜索的深度思考模型**

- **千问Max**：qwen3-max、qwen3-max-2026-01-23、qwen3-max-preview
- **千问开源**：qwen3.8-2.4t-a95b
- **千问Plus**：qwen-plus、qwen-plus-latest、qwen-plus-2025-07-14 及之后的快照版本
- **千问Flash**：qwen-flash、qwen-flash-2025-07-28 及之后的快照版本
- **千问Turbo**：qwen-turbo
- **QwQ**：qwq-plus
- **DeepSeek**：deepseek-v4-pro-0813、deepseek-v4-pro、deepseek-v4-flash、deepseek-v4-flash-0731、deepseek-v3.2、deepseek-v3.2-exp、deepseek-v3.1、deepseek-r1-0528、deepseek-r1（其中 deepseek-v4-pro-0813、deepseek-v4-flash、deepseek-v4-flash-0731 同时支持 Responses API）

<CodeGroup>
  ```python Python (OpenAI 兼容)
  import os
  from openai import OpenAI

  client = OpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
  )
  completion = client.chat.completions.create(
    model="qwen-plus",
    messages=[{"role": "user", "content": "结合近期AI热点新闻，预测AI的发展趋势"}],
    extra_body={
      "enable_thinking": True,
      "enable_search": True,
      "search_options": {
        "forced_search": True,
        "search_strategy": "max"
      }
    },
    stream=True,
    stream_options={"include_usage": True}
  )

  is_answering = False
  for chunk in completion:
    if not chunk.choices:
      print(chunk.usage)
      continue
    delta = chunk.choices[0].delta
    if hasattr(delta, "reasoning_content") and delta.reasoning_content:
      print(delta.reasoning_content, end="", flush=True)
    elif delta.content:
      if not is_answering:
        print("\n--- 回复 ---")
        is_answering = True
      print(delta.content, end="", flush=True)
  ```

  ```python Python (DashScope)
  import os
  import dashscope

  responses = dashscope.Generation.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen-plus",
    messages=[{"role": "user", "content": "结合近期AI热点新闻，预测AI的发展趋势"}],
    enable_thinking=True,
    enable_search=True,
    search_options={
      "forced_search": True,
      "enable_source": True,
      "enable_citation": True,
      "citation_format": "[ref_<number>]",
      "search_strategy": "max"
    },
    stream=True,
    incremental_output=True,
    result_format="message"
  )

  is_answering, is_first = False, True
  for chunk in responses:
    if is_first:
      for web in chunk.output.search_info["search_results"]:
        print(f"[{web['index']}]: [{web['title']}]({web['url']})")
      is_first = False
    rc = chunk.output.choices[0].message.reasoning_content
    content = chunk.output.choices[0].message.content
    if rc:
      print(rc, end="", flush=True)
    elif content:
      if not is_answering:
        print("\n--- 回复 ---")
        is_answering = True
      print(content, end="", flush=True)
  ```
</CodeGroup>

## 计费

计费涉及两个方面：

- **模型调用费用**：联网搜索获取的网页内容会追加到 prompt 中，增加输入 token 数量，按模型标准价格计费。详见[计费说明](/developer-guides/getting-started/pricing)。

- **搜索调用费用**（每 1,000 次）：

  <Note>
    使用 Responses API 方式时，联网搜索工具的计费与 `agent` 策略相同。
  </Note>

  <Note>
    以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
  </Note>

| 策略（`search_strategy`） | 功能             | 费用             |
| --------------------- | -------------- | -------------- |
| `turbo`（默认）           | 兼顾速度与效果        | 3元             |
| `max`                 | 多源搜索，结果更全面     | 4元             |
| `agent`               | 多轮检索与信息整合      | 4元             |
| `agent_max`           | 搜索 + 网页提取器阅读全文 | 搜索 4元；网页抓取限时免费 |

## 错误码

如果调用失败，请参阅[错误码](/api-reference/preparation/error-messages)。
