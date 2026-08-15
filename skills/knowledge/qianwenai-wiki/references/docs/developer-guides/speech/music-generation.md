> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 音乐生成

> Fun-Music 支持通过提示词描述音乐风格和场景，或提供自定义歌词，生成带有男声或女声的中文/英文完整歌曲，也支持生成纯音乐。

## 概述

Fun-Music 是端到端音乐生成模型，输入自然语言描述或自定义歌词即可生成完整歌曲或纯音乐：

- 通过提示词（`prompt`）描述音乐风格、场景、情绪和乐器偏好，模型自动创作歌词并生成歌曲
- 通过歌词（`lyrics`）提供自定义歌词内容，模型据此谱曲并演唱
- 通过声音性别（`gender`）选择男声或女声（仅 `fun-music-v1` 模型）
- 通过纯音乐模式（`is_instrumental`=true）生成无人声的纯音乐
- 支持流式和非流式两种输出模式
- 支持 MP3 和 WAV 两种音频格式输出

### 两个模型的区别

Fun-Music 提供两个模型，主要区别如下：

| 特性     | fun-music-v1                       | fun-music-preview             |
| ------ | ---------------------------------- | ----------------------------- |
| prompt | 与 lyrics 至少传入其中之一                  | 必选                            |
| lyrics | 与 prompt 至少传入其中之一；同时传入时仅 lyrics 生效 | 可选；传入后优先作为歌词内容（此时 prompt 不生效） |
| 纯音乐    | 支持（is\_instrumental=true）          | 支持（is\_instrumental=true）     |
| gender | 支持                                 | 不支持                           |

### 音频输出格式

通过 `format` 参数指定输出格式：

| 格式    | 特点          | 适用场景         |
| ----- | ----------- | ------------ |
| `mp3` | 有损压缩，文件体积小  | 网络传输、在线播放、存储 |
| `wav` | 无损格式，文件体积较大 | 后期处理、高质量播放   |

## 前提条件

- 已获取 API Key。获取方式请参见[获取 API Key](/api-reference/preparation/api-key)。
- 已将 API Key 配置到环境变量（推荐）：

```shell
export DASHSCOPE_API_KEY="sk-xxx"
```

## 快速开始

以下示例展示三种典型用法。

<Note>
  以下示例代码中的模型服务端点为 `dashscope.aliyuncs.com`。
</Note>

<Tabs>
  <Tab title="通过提示词生成歌曲">
    传入 `prompt` 参数描述音乐风格和场景，模型将自动创作歌词并生成歌曲。

    <CodeGroup>
      ```curl curl
      curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
          "model": "fun-music-v1",
          "input": {
              "prompt": "夏日清新民谣，木吉他与口琴伴奏，轻快节奏，适合旅行Vlog背景音乐",
              "gender": "female"
          }
      }'
      ```

      ```python Python
      import requests
      import os

      api_key = os.getenv("DASHSCOPE_API_KEY")
      url = "https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation"

      response = requests.post(url,
        headers={
          "Authorization": f"Bearer {api_key}",
          "Content-Type": "application/json"
        },
        json={
          "model": "fun-music-v1",
          "input": {
            "prompt": "夏日清新民谣，木吉他与口琴伴奏，轻快节奏，适合旅行Vlog背景音乐",
            "gender": "female"
          }
        }
      )

      result = response.json()
      audio_url = result["output"]["audio"]["url"]
      print(f"音乐生成成功！下载地址：{audio_url}")
      ```

      ```java Java
      import java.io.*;
      import java.net.HttpURLConnection;
      import java.net.URL;

      public class FunMusicDemo {
        public static void main(String[] args) throws Exception {
          String apiKey = System.getenv("DASHSCOPE_API_KEY");
          String endpoint = "https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation";

          HttpURLConnection conn = (HttpURLConnection) new URL(endpoint).openConnection();
          conn.setRequestMethod("POST");
          conn.setRequestProperty("Authorization", "Bearer " + apiKey);
          conn.setRequestProperty("Content-Type", "application/json");
          conn.setDoOutput(true);

          String jsonBody = "{\"model\":\"fun-music-v1\","
            + "\"input\":{\"prompt\":\"夏日清新民谣，木吉他与口琴伴奏，轻快节奏，适合旅行Vlog背景音乐\","
            + "\"gender\":\"female\"}}";

          try (OutputStream os = conn.getOutputStream()) {
            os.write(jsonBody.getBytes("UTF-8"));
          }

          try (BufferedReader reader = new BufferedReader(
              new InputStreamReader(conn.getInputStream(), "UTF-8"))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
              sb.append(line);
            }
            System.out.println(sb.toString());
          }
        }
      }
      ```
    </CodeGroup>
  </Tab>

  <Tab title="通过歌词生成歌曲">
    传入 `lyrics` 参数提供自定义歌词，模型将根据歌词谱曲并生成歌曲。

    <CodeGroup>
      ```curl curl
      curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
          "model": "fun-music-v1",
          "input": {
              "lyrics": "[verse]\n清晨的阳光穿过窗帘,\n咖啡的香气弥漫房间.\n翻开昨天未读完的书,\n时光就这样悄悄流转.\n\n[chorus]\n慢慢来不着急,\n生活本该如此惬意.\n把烦恼都丢进风里,\n拥抱每一个晴天雨季.",
              "gender": "female"
          }
      }'
      ```

      ```python Python
      import requests
      import os

      api_key = os.getenv("DASHSCOPE_API_KEY")
      url = "https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation"

      lyrics = """[verse]
      清晨的阳光穿过窗帘,
      咖啡的香气弥漫房间.
      翻开昨天未读完的书,
      时光就这样悄悄流转.

      [chorus]
      慢慢来不着急,
      生活本该如此惬意.
      把烦恼都丢进风里,
      拥抱每一个晴天雨季."""

      response = requests.post(url,
        headers={
          "Authorization": f"Bearer {api_key}",
          "Content-Type": "application/json"
        },
        json={
          "model": "fun-music-v1",
          "input": {
            "lyrics": lyrics,
            "gender": "female"
          }
        }
      )

      result = response.json()
      audio_url = result["output"]["audio"]["url"]
      print(f"音乐生成成功！下载地址：{audio_url}")
      ```

      ```java Java
      import java.io.*;
      import java.net.HttpURLConnection;
      import java.net.URL;

      public class FunMusicLyricsDemo {
        public static void main(String[] args) throws Exception {
          String apiKey = System.getenv("DASHSCOPE_API_KEY");
          String endpoint = "https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation";

          HttpURLConnection conn = (HttpURLConnection) new URL(endpoint).openConnection();
          conn.setRequestMethod("POST");
          conn.setRequestProperty("Authorization", "Bearer " + apiKey);
          conn.setRequestProperty("Content-Type", "application/json");
          conn.setDoOutput(true);

          String lyrics = "[verse]\\n清晨的阳光穿过窗帘,\\n"
            + "咖啡的香气弥漫房间.\\n"
            + "翻开昨天未读完的书,\\n"
            + "时光就这样悄悄流转.\\n\\n"
            + "[chorus]\\n慢慢来不着急,\\n"
            + "生活本该如此惬意.\\n"
            + "把烦恼都丢进风里,\\n"
            + "拥抱每一个晴天雨季.";

          String jsonBody = "{\"model\":\"fun-music-v1\","
            + "\"input\":{\"lyrics\":\"" + lyrics + "\","
            + "\"gender\":\"female\"}}";

          try (OutputStream os = conn.getOutputStream()) {
            os.write(jsonBody.getBytes("UTF-8"));
          }

          try (BufferedReader reader = new BufferedReader(
              new InputStreamReader(conn.getInputStream(), "UTF-8"))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
              sb.append(line);
            }
            System.out.println(sb.toString());
          }
        }
      }
      ```
    </CodeGroup>
  </Tab>

  <Tab title="生成纯音乐">
    将 `is_instrumental` 设为 `true`，可生成无人声的纯音乐。此时 `lyrics` 和 `gender` 参数将被忽略。

    <CodeGroup>
      ```curl curl
      curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
          "model": "fun-music-preview",
          "input": {
              "prompt": "宁静的钢琴曲，适合深夜阅读的背景音乐，舒缓优美",
              "is_instrumental": true
          }
      }'
      ```

      ```python Python
      import requests
      import os

      api_key = os.getenv("DASHSCOPE_API_KEY")
      url = "https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation"

      response = requests.post(url,
        headers={
          "Authorization": f"Bearer {api_key}",
          "Content-Type": "application/json"
        },
        json={
          "model": "fun-music-preview",
          "input": {
            "prompt": "宁静的钢琴曲，适合深夜阅读的背景音乐，舒缓优美",
            "is_instrumental": True
          }
        }
      )

      result = response.json()
      audio_url = result["output"]["audio"]["url"]
      print(f"纯音乐生成成功！下载地址：{audio_url}")
      ```

      ```java Java
      import java.io.*;
      import java.net.HttpURLConnection;
      import java.net.URL;

      public class FunMusicInstrumentalDemo {
        public static void main(String[] args) throws Exception {
          String apiKey = System.getenv("DASHSCOPE_API_KEY");
          String endpoint = "https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation";

          HttpURLConnection conn = (HttpURLConnection) new URL(endpoint).openConnection();
          conn.setRequestMethod("POST");
          conn.setRequestProperty("Authorization", "Bearer " + apiKey);
          conn.setRequestProperty("Content-Type", "application/json");
          conn.setDoOutput(true);

          String jsonBody = "{\"model\":\"fun-music-preview\","
            + "\"input\":{\"prompt\":\"宁静的钢琴曲，适合深夜阅读的背景音乐，舒缓优美\","
            + "\"is_instrumental\":true}}";

          try (OutputStream os = conn.getOutputStream()) {
            os.write(jsonBody.getBytes("UTF-8"));
          }

          try (BufferedReader reader = new BufferedReader(
              new InputStreamReader(conn.getInputStream(), "UTF-8"))) {
            StringBuilder sb = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
              sb.append(line);
            }
            System.out.println(sb.toString());
          }
        }
      }
      ```
    </CodeGroup>
  </Tab>
</Tabs>

## 创作指南

### 提示词（prompt）

`prompt` 是描述音乐创作意图的核心参数。模型会根据您的描述自动创作歌词、编曲并生成歌曲。

**撰写建议**：具体描述情绪、场景、乐器偏好，能生成更贴合需求的音乐。

- 推荐：`悲伤钢琴曲，雨夜思念`
- 不推荐：`悲伤音乐`（过于笼统）

<Note>
  您可以在提示词中直接指定乐器（如"钢琴伴奏""萨克斯独奏""古筝与竹笛"）、节奏（如"轻快节奏""慢节拍""密集鼓点"）和情感基调（如"温暖""伤感""热血""慵懒"），模型会尽可能遵循这些描述进行创作。描述越具体，生成效果越贴合预期。
</Note>

**不同风格的提示词示例**

| 风格 | 提示词示例                              |
| -- | ---------------------------------- |
| 民谣 | 温暖治愈的民谣歌曲，木吉他伴奏，讲述午后咖啡馆里的慵懒时光      |
| 古风 | 古风歌曲，古筝与竹笛伴奏，水墨山水般的悠远意境，诉说江湖离别     |
| 摇滚 | 热血摇滚，电吉他失真音墙，密集鼓点，唱出青春的叛逆与自由       |
| 抒情 | 抒情慢歌，钢琴伴奏，安静深沉，带有淡淡忧伤，适合表达思念与回忆    |
| 说唱 | 节拍鲜明的嘻哈说唱，808低音鼓，充满街头活力，讲述城市生活故事   |
| 儿歌 | 欢快可爱的儿童歌曲，木琴与手鼓伴奏，节奏简单明快，教小朋友认识大自然 |

### 歌词（lyrics）

`lyrics` 参数用于传入您自己编写的歌词，模型将严格根据歌词内容谱曲并生成歌曲。在歌词中使用结构标签可以控制歌曲的段落编排。

**结构标签**

| 标签         | 说明      |
| ---------- | ------- |
| `[intro]`  | 前奏，引入氛围 |
| `[verse]`  | 主歌，叙述故事 |
| `[chorus]` | 副歌，情感高潮 |
| `[bridge]` | 桥段，视角转换 |
| `[outro]`  | 尾奏，渐弱收尾 |

**歌词示例**

```plaintext
[intro]
琴键轻落，晚风微凉.
那年夏天，心跳悄悄发烫.

[verse]
教室窗边，阳光斜照你侧脸.
借半块橡皮，指尖碰出电流线.
放学路上，单车铃声追云烟.
你说未来很远，我却想走到终点.

[chorus]
青春是未拆的信笺，写满勇敢的誓言.
哪怕世界忽明又忽暗，有你就看见光点.
恋爱像初夏的雨甜，淋湿梦也不怕远.
我们笑着奔向明天，手牵手不回头望.

[bridge]
后来风雨打散纸伞，沉默代替了答案.
可心底那首歌未完，还等一句"别走散".

[chorus]
青春是未拆的信笺，写满勇敢的誓言.
哪怕世界忽明又忽暗，有你就看见光点.
恋爱像初夏的雨甜，淋湿梦也不怕远.
我们笑着奔向明天，手牵手不回头望.

[outro]
琴声渐远，星光铺满长街.
故事未完，下一页仍热烈.
```

**创作要求**

- **原创性原则**：严禁抄袭已发表歌曲的歌词，不得模仿知名歌曲的押韵模式或标志性句式。
- **内容安全**：禁止涉及政治、暴力、色情、低俗、恐怖、毒品等违法内容，保持内容健康、情感真挚。
- **语言要求**：仅支持中文或英文，不支持日文、韩文等其他语言。

### 声音性别（gender）

通过 `gender` 参数选择演唱声音的性别，默认为女声。仅 `fun-music-v1` 模型支持该参数。

- `female`：女声（默认）
- `male`：男声

### 纯音乐模式（is\_instrumental）

将 `is_instrumental` 参数设为 `true` 可生成无人声的纯音乐。此时 `lyrics` 和 `gender` 参数将被忽略。默认值为 `false`（生成歌曲）。

## 进阶功能

### 流式输出

流式模式支持边生成边返回音频数据，适用于实时播放等场景，`fun-music-v1` 和 `fun-music-preview` 均支持该模式。启用流式输出需要在请求头中添加 `X-DashScope-SSE: enable`。

<Note>
  流式模式与非流式模式的输入参数字符数限制不同，请注意区分：

  - 非流式模式：`lyrics` 支持中文 5~~350 字符、英文 5~~2000 字符，`prompt` 支持 1\~2000 字符。
  - 流式模式：`lyrics` 支持中文 300~~350 字、英文 200~~250 词，`prompt` 支持 5\~1000 个中文汉字或英文单词。
</Note>

<CodeGroup>
  ```curl curl
  curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation' \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-DashScope-SSE: enable" \
  -d '{
      "model": "fun-music-v1",
      "input": {
          "prompt": "节奏感强的电子舞曲，合成器音效，充满能量，适合健身运动场景",
          "gender": "male"
      }
  }'
  ```

  ```python Python
  import requests
  import os
  import json
  import base64

  api_key = os.getenv("DASHSCOPE_API_KEY")
  url = "https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation"

  response = requests.post(url,
    headers={
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json",
      "X-DashScope-SSE": "enable"
    },
    json={
      "model": "fun-music-v1",
      "input": {
        "prompt": "节奏感强的电子舞曲，合成器音效，充满能量，适合健身运动场景",
        "gender": "male"
      }
    },
    stream=True
  )

  output_file = "output.mp3"
  with open(output_file, "wb") as f:
    for line in response.iter_lines():
      if not line:
        continue
      decoded = line.decode("utf-8")
      if decoded.startswith("data:"):
        data = json.loads(decoded[5:])
        finish_reason = data.get("output", {}).get("finish_reason")
        if finish_reason == "null":
          audio_data = data["output"]["audio"].get("data", "")
          if audio_data:
            f.write(base64.b64decode(audio_data))
        elif finish_reason == "stop":
          print(f"音乐生成完成！已保存到 {output_file}")
  ```

  ```java Java
  import java.io.*;
  import java.net.HttpURLConnection;
  import java.net.URL;
  import java.util.Base64;

  public class FunMusicStreamDemo {
    public static void main(String[] args) throws Exception {
      String apiKey = System.getenv("DASHSCOPE_API_KEY");
      String endpoint = "https://dashscope.aliyuncs.com/api/v1/services/audio/music/generation";

      HttpURLConnection conn = (HttpURLConnection) new URL(endpoint).openConnection();
      conn.setRequestMethod("POST");
      conn.setRequestProperty("Authorization", "Bearer " + apiKey);
      conn.setRequestProperty("Content-Type", "application/json");
      conn.setRequestProperty("X-DashScope-SSE", "enable");
      conn.setDoOutput(true);

      String jsonBody = "{\"model\":\"fun-music-v1\","
        + "\"input\":{\"prompt\":\"节奏感强的电子舞曲，合成器音效，充满能量，适合健身运动场景\","
        + "\"gender\":\"male\"}}";

      try (OutputStream os = conn.getOutputStream()) {
        os.write(jsonBody.getBytes("UTF-8"));
      }

      String outputFile = "output.mp3";
      try (BufferedReader reader = new BufferedReader(
          new InputStreamReader(conn.getInputStream(), "UTF-8"));
         FileOutputStream fos = new FileOutputStream(outputFile)) {
        String line;
        while ((line = reader.readLine()) != null) {
          if (line.startsWith("data:")) {
            String data = line.substring(5);
            if (data.contains("\"finish_reason\":\"null\"")) {
              int start = data.indexOf("\"data\":\"") + 8;
              int end = data.indexOf("\"", start);
              if (start > 8 && end > start) {
                byte[] chunk = Base64.getDecoder().decode(
                  data.substring(start, end));
                fos.write(chunk);
              }
            } else if (data.contains("\"finish_reason\":\"stop\"")) {
              System.out.println("音乐生成完成！已保存到 " + outputFile);
            }
          }
        }
      }
    }
  }
  ```
</CodeGroup>

## API 参考

[音乐生成 API 参考](/api-reference/music-generation/fun-music)

## 常见问题

<AccordionGroup>
  <Accordion title="能否指定乐器、节奏或情感？">
    可以。在 `prompt` 中直接描述即可，例如"钢琴伴奏，慢节拍，伤感"。模型会尽可能遵循这些描述进行创作。描述越具体，生成效果越贴合预期。详细的提示词撰写建议请参见[提示词（prompt）](#提示词-prompt)。
  </Accordion>

  <Accordion title="两个模型怎么选？">
    `fun-music-v1` 支持通过 `gender` 参数选择男声或女声，且支持 `prompt` 和 `lyrics` 二选一。`fun-music-preview` 必须传入 `prompt`，不支持 `gender` 参数。两个模型的详细差异请参见[两个模型的区别](#两个模型的区别)。
  </Accordion>

  <Accordion title="生成的音频 URL 有效期是多久？">
    音频文件下载 URL 的有效期为 24 小时，请在此时间内完成下载。超过有效期后 URL 将失效，需要重新调用接口生成。
  </Accordion>

  <Accordion title="lyrics 和 prompt 有什么区别？">
    `lyrics` 参数用于传入您自己编写的歌词，模型将严格根据歌词内容谱曲并生成歌曲。`prompt` 参数用于传入对音乐风格、场景的自然语言描述，模型将自动创作并生成音乐。两个参数的必选性因模型而异：`fun-music-v1` 至少传入其中之一，若同时传入仅 `lyrics` 生效；`fun-music-preview` 必须传入 `prompt`，`lyrics` 为可选参数，传入后将优先作为歌词内容。
  </Accordion>

  <Accordion title="流式和非流式模式如何选择？">
    如果只需获取最终的完整音频文件，推荐使用非流式模式，接口调用更简单。如果需要在音乐生成过程中逐步获取音频数据（如边生成边播放），建议使用流式模式。
  </Accordion>
</AccordionGroup>
