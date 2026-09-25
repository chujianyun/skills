> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文本与多模态向量化

> 向量化模型可将文本、图像、视频等数据转换为数值向量，用于语义搜索、推荐、聚类、分类、异常检测等下游任务。

## 前提条件

[获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。

## 获取向量

### 文本向量化

调用 API 时，在请求中指定要向量化的文本和模型名称。

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      input_text = "The quality of the clothes is excellent"

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      completion = client.embeddings.create(
        model="qwen3.7-text-embedding",
        input=input_text
      )

      print(completion.model_dump_json())
      ```

      ```javascript Node.js
      const OpenAI = require("openai");

      const openai = new OpenAI({
        apiKey: process.env.DASHSCOPE_API_KEY,
        baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1'
      });

      async function getEmbedding() {
        try {
          const inputTexts = "The quality of the clothes is excellent";
          const completion = await openai.embeddings.create({
            model: "qwen3.7-text-embedding",
            input: inputTexts,
            dimensions: 1024
          });

          console.log(JSON.stringify(completion, null, 2));
        } catch (error) {
          console.error('Error:', error);
        }
      }

      getEmbedding();
      ```

      ```bash curl
      curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/embeddings' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json' \
      --data '{
        "model": "qwen3.7-text-embedding",
        "input": "The quality of the clothes is excellent"
      }'
      ```
    </CodeGroup>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python
      import dashscope
      from http import HTTPStatus

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      input_text = "The quality of the clothes is excellent"
      resp = dashscope.TextEmbedding.call(
        model="qwen3.7-text-embedding",
        input=input_text,
      )

      if resp.status_code == HTTPStatus.OK:
        print(resp)
      ```

      ```java Java
      import com.alibaba.dashscope.embeddings.TextEmbedding;
      import com.alibaba.dashscope.embeddings.TextEmbeddingParam;
      import com.alibaba.dashscope.embeddings.TextEmbeddingResult;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.utils.Constants;

      import java.util.Collections;

      public class Main {
        static {
          Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
        }
        public static void main(String[] args) {
          String inputTexts = "The quality of the clothes is excellent";
          try {
            TextEmbeddingParam param = TextEmbeddingParam
                .builder()
                .model("qwen3.7-text-embedding")
                .texts(Collections.singleton(inputTexts))
                .build();

            TextEmbedding textEmbedding = new TextEmbedding();
            TextEmbeddingResult result = textEmbedding.call(param);

            System.out.println(result);

          } catch (NoApiKeyException e) {
            System.err.println("调用 API 时发生异常: " + e.getMessage());
            System.err.println("请检查 API Key 是否已正确配置。");
            e.printStackTrace();
          }
        }
      }
      ```

      ```bash curl
      curl --location 'https://dashscope.aliyuncs.com/api/v1/services/embeddings/text-embedding/text-embedding' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json' \
      --data '{
        "model": "qwen3.7-text-embedding",
        "input": {
          "texts": [
          "The quality of the clothes is excellent"
          ]
        }
      }'
      ```
    </CodeGroup>
  </Tab>
</Tabs>

### 多模态独立向量

为每种输入（文本、图像或视频）分别生成独立向量。适合为图片和文字标题各自建立索引。

<Note>
  多模态 Embedding 需使用 DashScope SDK 或 HTTP API，不支持 OpenAI 兼容接口。
</Note>

<Tabs>
  <Tab title="Python">
    ```python
    import dashscope
    import json
    import os

    image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"

    resp = dashscope.MultiModalEmbedding.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      model="tongyi-embedding-vision-plus",
      input=[{"image": image}],
    )

    print(json.dumps(resp.output, indent=4))
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import com.alibaba.dashscope.embeddings.MultiModalEmbedding;
    import com.alibaba.dashscope.embeddings.MultiModalEmbeddingItemImage;
    import com.alibaba.dashscope.embeddings.MultiModalEmbeddingParam;
    import com.alibaba.dashscope.embeddings.MultiModalEmbeddingResult;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.alibaba.dashscope.exception.UploadFileException;

    import java.util.Collections;

    public class Main {
      public static void main(String[] args) {
        try {
          MultiModalEmbedding embedding = new MultiModalEmbedding();
          MultiModalEmbeddingItemImage image = new MultiModalEmbeddingItemImage(
            "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png");

          MultiModalEmbeddingParam param = MultiModalEmbeddingParam.builder()
            .model("tongyi-embedding-vision-plus")
            .contents(Collections.singletonList(image))
            .build();

          MultiModalEmbeddingResult result = embedding.call(param);
          System.out.println(result);

        } catch (ApiException | NoApiKeyException | UploadFileException e) {
          System.err.println(e.getMessage());
        }
      }
    }
    ```
  </Tab>
</Tabs>

视频输入：将 `{"image": image}` 替换为 `{"video": video_url}`。

### 多模态融合向量

将多模态输入（文本 + 图片 + 视频）编码为 **1 个向量**。适合图文混合检索——例如输入一张衬衫图片加上文本"找相似但更年轻的款式"，模型将图像和文本指令融合为一个向量。

<Tabs>
  <Tab title="Python">
    ```python
    import dashscope
    import json
    import os

    text = "白色运动鞋，轻量透气"
    image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"

    resp = dashscope.MultiModalEmbedding.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      model="qwen3-vl-embedding",
      input=[
        {"text": text},
        {"image": image},
      ],
      enable_fusion=True,
    )

    print(json.dumps(resp.output, indent=4))
    ```
  </Tab>

  <Tab title="Java (HTTP)">
    ```java
    import java.net.URI;
    import java.net.http.HttpClient;
    import java.net.http.HttpRequest;
    import java.net.http.HttpResponse;

    public class Main {
      public static void main(String[] args) throws Exception {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        String requestBody = "{"
            + "\"model\": \"qwen3-vl-embedding\","
            + "\"input\": {"
            + "  \"contents\": ["
            + "    {\"text\": \"这是一段测试文本，用于生成多模态融合向量\"},"
            + "    {\"image\": \"https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png\"},"
            + "    {\"video\": \"https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4\"}"
            + "  ]"
            + "},"
            + "\"parameters\": {"
            + "  \"enable_fusion\": true"
            + "}"
            + "}";
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding"))
            .header("Authorization", "Bearer " + apiKey)
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(requestBody))
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
      }
    }
    ```
  </Tab>
</Tabs>

#### 各模型的融合方式

| 模型                                         | 融合方式                                                           |
| ------------------------------------------ | -------------------------------------------------------------- |
| `qwen3-vl-embedding`                       | 添加 `enable_fusion=True` 参数                                     |
| `qwen2.5-vl-embedding`                     | 默认即为融合模式，无需额外参数                                                |
| `tongyi-embedding-vision-plus-2026-03-06`  | 将 text、image 放在同一个 content 对象中：`[{"text": ..., "image": ...}]` |
| `tongyi-embedding-vision-flash-2026-03-06` | 同上                                                             |

<Accordion title="tongyi-embedding-vision-plus-2026-03-06 融合示例">
  该模型通过将 text 和 image 放在**同一个 content 对象**中实现融合，无需 `enable_fusion` 参数。

  <CodeGroup>
    ```python Python
    import dashscope
    import json
    import os

    resp = dashscope.MultiModalEmbedding.call(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      model="tongyi-embedding-vision-plus-2026-03-06",
      input=[
        {"text": "白色运动鞋", "image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"}
      ],
      dimension=1152,
    )

    print(json.dumps(resp.output, indent=4))
    ```

    ```java Java（HTTP）
    import java.net.URI;
    import java.net.http.HttpClient;
    import java.net.http.HttpRequest;
    import java.net.http.HttpResponse;

    public class Main {
      public static void main(String[] args) throws Exception {
        String apiKey = System.getenv("DASHSCOPE_API_KEY");
        String requestBody = "{"
            + "\"model\": \"tongyi-embedding-vision-plus-2026-03-06\","
            + "\"input\": {"
            + "  \"contents\": ["
            + "    {"
            + "      \"text\": \"白色运动鞋，轻量透气，适合跑步和日常穿着\","
            + "      \"image\": \"https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png\""
            + "    }"
            + "  ]"
            + "},"
            + "\"parameters\": {"
            + "  \"dimension\": 1152"
            + "}"
            + "}";
        HttpClient client = HttpClient.newHttpClient();
        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create("https://dashscope.aliyuncs.com/api/v1/services/embeddings/multimodal-embedding/multimodal-embedding"))
            .header("Authorization", "Bearer " + apiKey)
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(requestBody))
            .build();
        HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
        System.out.println(response.body());
      }
    }
    ```
  </CodeGroup>
</Accordion>

## 模型选择

### 文本向量

| **模型**                                                                                     | **向量维度**                                 | **批次大小** | **每批最大 Token 数** | **支持的语言**                                        |
| ------------------------------------------------------------------------------------------ | ---------------------------------------- | -------- | ---------------- | ------------------------------------------------ |
| qwen3.7-text-embedding                                                                     | 2,560、2,048、1,536、1,024（默认）、768、512、256  | 20       | 128,000          | 中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄语等201种主流语种与方言   |
| text-embedding-v4（属于 [Qwen3-Embedding](https://qwenlm.github.io/blog/qwen3-embedding/) 系列） | 2,048、1,536、1,024（默认）、768、512、256、128、64 | 10       | 33,000           | 100+ 种主流语言，包括中文、英文、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄语等 |
| text-embedding-v3                                                                          | 1,024（默认）、768、512、256、128、64             | 10       | 8,192            | 50+ 种主流语言，包括中文、英文、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄语等  |
| text-embedding-v2                                                                          | 1,536                                    | 25       | 2,048            | 中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄语               |
| text-embedding-v1                                                                          | 1,536                                    | 25       | 2,048            | 中文、英语、西班牙语、法语、葡萄牙语、印尼语                           |
| text-embedding-async-v2                                                                    | 1,536                                    | 100,000  | 2,048            | 中文、英语、西班牙语、法语、葡萄牙语、印尼语、日语、韩语、德语、俄语               |
| text-embedding-async-v1                                                                    | 1,536                                    | 100,000  | 2,048            | 中文、英语、西班牙语、法语、葡萄牙语、印尼语                           |

<Note>
  批次大小是指单次 API 调用中可处理的最大文本数量。例如，text-embedding-v4 的批次大小为 10，即单次请求最多可传入 10 条文本进行向量化，每条文本不超过 33,000 个 Token。此限制适用于：

  - 字符串数组输入：数组最多包含 10 个元素。
  - 文件输入：文本文件最多包含 10 行文本。
</Note>

<Accordion title="qwen3.7-text-embedding 所有支持语言">
  - **汉藏语系**：中文（简体中文、繁体中文、粤语）、缅甸语、藏语、梅泰语
  - **印欧语系**：英语、法语、葡萄牙语、德语、罗马尼亚语、瑞典语、丹麦语、保加利亚语、俄语、捷克语、希腊语、乌克兰语、西班牙语、荷兰语、斯洛伐克语、克罗地亚语、波兰语、立陶宛语、挪威语（博克马尔语）、挪威尼诺斯克语、波斯语、斯洛文尼亚语、古吉拉特语、拉脱维亚语、意大利语、奥克语、尼泊尔语、马拉地语、白俄罗斯语、塞尔维亚语、卢森堡语、威尼斯语、阿萨姆语、威尔士语、西里西亚语、阿斯图里亚语、恰蒂斯加尔语、阿瓦德语、迈蒂利语、博杰普尔语、信德语、爱尔兰语、法罗语、印地语、旁遮普语、孟加拉语、奥里雅语、塔吉克语、东意第绪语、伦巴第语、利古里亚语、西西里语、弗留利语、撒丁岛语、加利西亚语、加泰罗尼亚语、冰岛语、托斯克语、阿尔巴尼亚语、林堡语、达里语、南非荷兰语、马其顿语、僧伽罗语、乌尔都语、马加希语、波斯尼亚语、亚美尼亚语、拉特加利亚语、苏格兰盖尔语、中库尔德语、北库尔德语、南普什图语、梵语、敦达里语、马尔瓦里语、阿希拉尼语、巴盖利语、巴格里语、本德利语、布拉吉语、库马翁语、克什米尔语
  - **亚非语系**：阿拉伯语（标准语、内志语、黎凡特语、埃及语、摩洛哥语、美索不达米亚语、塔伊兹-阿德尼语、突尼斯语、海湾语、阿尔及利亚语、苏丹语、利比亚语）、希伯来语、马耳他语、阿姆哈拉语、提格里尼亚语、卡比尔语、索马里语、西中奥罗莫语、豪萨语
  - **南岛语系**：印度尼西亚语、马来语、他加禄语、宿务语、爪哇语、巽他语、米南加保语、巴厘岛语、班加语、邦阿西楠语、伊洛科语、瓦雷语（菲律宾）、高原马达加斯加语、马达加斯加语、布吉语、毛利语、萨摩亚语、夏威夷语、斐济语
  - **德拉威语**：泰米尔语、泰卢固语、卡纳达语、马拉雅拉姆语
  - **突厥语系**：土耳其语、北阿塞拜疆语、北乌兹别克语、哈萨克语、巴什基尔语、鞑靼语、克里米亚鞑靼语、吉尔吉斯语、土库曼语、维吾尔语
  - **壮侗语系**：泰语、老挝语、掸语
  - **乌拉尔语系**：芬兰语、爱沙尼亚语、匈牙利语、草原马里语
  - **南亚语系**：越南语、高棉语
  - **尼日尔-刚果语系**：约鲁巴语、埃维语、卢旺达语、林加拉语、北索托语、尼扬贾语、绍纳语、南索托语、茨瓦纳语、科萨语、祖鲁语、卢干达语、斯瓦蒂语、聪加语、通布卡语、文达语、乔奎语、卢巴-卡赛语、隆迪语、姆本杜语、基库尤语、刚果语、尼日利亚富拉语、沃洛夫语、丰语、卡比耶语、莫西语、阿坎语、特维语、班巴拉语、伊博语
  - **其他**：日语、韩语、格鲁吉亚语、巴斯克语、海地语、帕皮阿门托语、卡布维尔迪亚努语、托克皮辛语、斯瓦希里语、中部艾马拉语、图卢语、那加语、尼日利亚皮钦语、毛里求斯克里奥尔语、桑戈语、阿亚库乔克丘亚语、喀尔喀蒙古语、西南丁卡语、努埃尔语、瓜拉尼语
</Accordion>

### 多模态向量

| **模型**                                   | **向量维度**                            | **文本长度限制**   | **图片大小限制**                      | **视频大小限制**                  |
| ---------------------------------------- | ----------------------------------- | ------------ | ------------------------------- | --------------------------- |
| qwen3-vl-embedding                       | 2560（默认）、2048、1536、1024、768、512、256 | 32,000 Token | 单张不超过 10 MB                     | 不超过 50 MB                   |
| qwen2.5-vl-embedding                     | 2048、1024（默认）、768、512               | 32,000 Token | 单张不超过 5 MB                      | 不超过 50 MB                   |
| tongyi-embedding-vision-plus-2026-03-06  | 1152（默认）、1024、512、256、128、64        | 1,024 Token  | 建议单张不超过 5 MB，最大 10 MB，支持最多 64 张 | 不超过 50 MB，编码类型为 H.264/H.265 |
| tongyi-embedding-vision-flash-2026-03-06 | 768（默认）、512、256、128、64              | 1,024 Token  | 建议单张不超过 5 MB，最大 10 MB，支持最多 64 张 | 不超过 50 MB，编码类型为 H.264/H.265 |
| tongyi-embedding-vision-plus             | 1152                                | 1,024 Token  | 单张不超过 3 MB，支持最多 8 张             | 不超过 10 MB                   |
| tongyi-embedding-vision-flash            | 768                                 | 1,024 Token  | 单张不超过 3 MB，支持最多 8 张             | 不超过 10 MB                   |
| multimodal-embedding-v1                  | 1,024                               | 512 Token    | 单张不超过 3 MB                      | 不超过 10 MB                   |

<Note>
  只有文本数据？使用 text-embedding-v4——更快、更便宜、维度选择更多。多模态 Embedding 专为跨模态检索设计（文本+图片、文本+视频）。
</Note>

#### 输入与语种限制

**融合向量模型**

| **模型**               | **文本**                                                                                                                                                               | **图片**                                                | **视频**             | **单次请求条数**                |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------ | ------------------------- |
| qwen3-vl-embedding   | 中、英、日、韩、法、德等 33 种语言（中文、日语、韩语、印尼语、越南语、泰语、英语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、瑞典语、丹麦语、捷克语、挪威语、荷兰语、芬兰语、土耳其语、波兰语、斯瓦希里语、罗马尼亚语、塞尔维亚语、希腊语、哈萨克语、乌兹别克语、宿务语、阿拉伯语、乌尔都语、波斯语、印地语/天城语、希伯来语） | JPEG、PNG、WEBP、BMP、TIFF、ICO、DIB、ICNS、SGI（URL 或 Base64） | MP4、AVI、MOV（仅 URL） | 总数不超过 20，图片不超过 10，视频不超过 1 |
| qwen2.5-vl-embedding | 中、英、日、韩、法、德等 11 种语言（中文、英语、日语、韩语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、印尼语）                                                                                                         | JPEG、PNG、WEBP、BMP、TIFF、ICO、DIB、ICNS、SGI（URL 或 Base64） | MP4、AVI、MOV（仅 URL） | 图片、文本、视频、融合对象每种类型最多 1 次   |

**独立向量模型**

| **模型**                                   | **文本**                                                                                                                                                            | **图片**                                                | **视频**                                   | **单次请求条数**                      |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- | ---------------------------------------- | ------------------------------- |
| tongyi-embedding-vision-plus-2026-03-06  | 中、英、日、韩等超 30 种语言（中文、日语、韩语、印尼语、越南语、泰语、英语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、瑞典语、丹麦语、捷克语、挪威语、荷兰语、芬兰语、土耳其语、波兰语、斯瓦希里语、罗马尼亚语、塞尔维亚语、希腊语、哈萨克语、乌兹别克语、宿务语、阿拉伯语、乌尔都语、波斯语、印地语/天城语、希伯来语） | JPEG、PNG、WEBP、BMP、TIFF、ICO、DIB、ICNS、SGI（URL 或 Base64） | MP4、MPEG、MOV、MPG、WEBM、AVI、FLV、MKV（仅 URL） | 总数不超过 20，图片不超过 64，视频不超过 8       |
| tongyi-embedding-vision-flash-2026-03-06 | 中、英、日、韩等超 30 种语言（中文、日语、韩语、印尼语、越南语、泰语、英语、法语、德语、俄语、葡萄牙语、西班牙语、意大利语、瑞典语、丹麦语、捷克语、挪威语、荷兰语、芬兰语、土耳其语、波兰语、斯瓦希里语、罗马尼亚语、塞尔维亚语、希腊语、哈萨克语、乌兹别克语、宿务语、阿拉伯语、乌尔都语、波斯语、印地语/天城语、希伯来语） | JPEG、PNG、WEBP、BMP、TIFF、ICO、DIB、ICNS、SGI（URL 或 Base64） | MP4、MPEG、MOV、MPG、WEBM、AVI、FLV、MKV（仅 URL） | 总数不超过 20，图片不超过 64，视频不超过 8       |
| tongyi-embedding-vision-plus             | 中文与英文                                                                                                                                                             | JPG、PNG、BMP（URL 或 Base64）                             | MP4、MPEG、MOV、MPG、WEBM、AVI、FLV、MKV（仅 URL） | 无数量限制，Token 数不超过单批次上限           |
| tongyi-embedding-vision-flash            | 中文与英文                                                                                                                                                             | JPG、PNG、BMP（URL 或 Base64）                             | MP4、MPEG、MOV、MPG、WEBM、AVI、FLV、MKV（仅 URL） | 无数量限制，Token 数不超过单批次上限           |
| multimodal-embedding-v1                  | 中文与英文                                                                                                                                                             | JPG、PNG、BMP（URL 或 Base64）                             | MP4、MPEG、MOV、MPG、WEBM、AVI、FLV、MKV（仅 URL） | 总数不超过 20；图片、视频各最多 1 条，文本最多 20 条 |

## 核心功能

### 切换向量维度

`qwen3.7-text-embedding`、`text-embedding-v4`、`text-embedding-v3`、`tongyi-embedding-vision-plus-2026-03-06`、`tongyi-embedding-vision-flash-2026-03-06`、`qwen3-vl-embedding` 和 `qwen2.5-vl-embedding` 支持自定义向量维度。维度越高，保留的语义信息越丰富，但存储和计算开销也更大。

- **通用场景（推荐）**：1024 维在性能与成本之间取得了最佳平衡，适合大多数语义检索任务。
- **高精度场景**：对精度要求较高的领域，可选择 1536 或 2048 维。精度有一定提升，但存储和计算开销显著增加。
- **资源受限场景**：对成本敏感的场景，可选择 768 维或更低。资源消耗显著降低，但语义信息会有一定损失。

<Tabs>
  <Tab title="OpenAI 兼容">
    ```python
    import os
    from openai import OpenAI

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    resp = client.embeddings.create(
      model="qwen3.7-text-embedding",
      input=["I like it and will buy from here again"],
      # 设置向量维度为 256
      dimensions=256
    )
    print(f"Embedding dimensions: {len(resp.data[0].embedding)}")
    ```
  </Tab>

  <Tab title="DashScope">
    ```python
    import dashscope

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    resp = dashscope.TextEmbedding.call(
      model="qwen3.7-text-embedding",
      input=["I like it and will buy from here again"],
      # 设置向量维度为 256
      dimension=256
    )

    print(f"Embedding dimensions: {len(resp.output['embeddings'][0]['embedding'])}")
    ```
  </Tab>
</Tabs>

### 区分查询文本与文档文本（text\_type）

<Note>
  该参数目前仅支持通过 DashScope SDK 和 API 启用。
</Note>

在搜索类任务中，对不同类型的内容进行针对性的向量化处理，可以充分发挥各自的作用，从而获得最佳检索效果。`text_type` 参数就是为此设计的：

- `text_type: 'query'`：用于用户输入的**查询文本**。模型生成的向量更具方向性，类似"标题"向量，专为"提问"和"检索"优化。
- `text_type: 'document'`（默认）：用于存储在数据库中的**文档文本**。模型生成的向量包含更全面的信息，类似"正文"向量，专为被检索优化。

使用短文本匹配长文本时，应区分 `query` 和 `document`。对于所有文本角色相同的任务（如聚类或分类），无需设置此参数。

### 使用指令提升效果（instruct）

<Note>
  该参数目前仅支持通过 DashScope SDK 和 API 启用。
</Note>

提供清晰的英文指令，可引导 `qwen3.7-text-embedding` 和 `text-embedding-v4` 针对特定检索场景优化向量质量，有效提升精度。`qwen3.7-text-embedding` 的指令遵循能力较 text-embedding-v4 提升 **16.4%**，建议优先使用。使用此功能时，需将 `text_type` 参数设置为 `query`。

```python
import dashscope

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

# 场景：为搜索引擎构建文档向量时，可添加指令来优化检索的向量质量。
resp = dashscope.TextEmbedding.call(
  model="qwen3.7-text-embedding",
  input="Research papers on machine learning",
  text_type="query",
  instruct="Given a research paper query, retrieve relevant research paper"
)
```

### 稠密向量与稀疏向量

<Note>
  该参数目前仅支持通过 DashScope SDK 和 API 启用。
</Note>

`qwen3.7-text-embedding`、`text-embedding-v4` 和 `text-embedding-v3` 支持三种向量输出类型，满足不同检索策略的需求。其中 `qwen3.7-text-embedding` 的 Sparse Embedding 采用全新类 SPLADE 训练策略，效果提升 **8.4%**，并新增支持跨语言检索。

| **向量类型（`output_type`）** | **核心优势**                                       | **主要不足**                    | **典型应用场景**             |
| ----------------------- | ---------------------------------------------- | --------------------------- | ---------------------- |
| dense                   | **深度语义理解**。能识别同义词和上下文，检索结果更相关。                 | **计算和存储成本更高**。无法保证精确的关键词匹配。 | 语义搜索、AI 对话、内容推荐。       |
| sparse                  | **计算效率高**。专注于**精确关键词匹配**和快速过滤。                 | **牺牲语义理解**。无法处理同义词或上下文。     | 日志检索、商品 SKU 搜索、精确信息过滤。 |
| dense\&sparse           | 结合语义和关键词，获得最佳搜索效果。**生成成本相同**，API 调用开销与单向量模式一致。 | **存储需求大**。系统架构和检索逻辑更复杂。     | 高质量生产级混合搜索引擎。          |

## 使用示例

<Note>
  以下代码仅供演示。在生产环境中，应预先计算向量并存储到向量数据库中。检索时只需计算查询向量。
</Note>

### 语义搜索

通过计算查询与文档之间的向量相似度，实现精准的语义匹配。

```python
import dashscope
import numpy as np
from dashscope import TextEmbedding

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def cosine_similarity(a, b):
  """计算余弦相似度"""
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def semantic_search(query, documents, top_k=5):
  """执行语义搜索"""
  # 生成查询向量
  query_resp = TextEmbedding.call(
  model="qwen3.7-text-embedding",
  input=query,
  dimension=1024
  )
  query_embedding = query_resp.output['embeddings'][0]['embedding']

  # 生成文档向量
  doc_resp = TextEmbedding.call(
  model="qwen3.7-text-embedding",
  input=documents,
  dimension=1024
  )

  # 计算相似度
  similarities = []
  for i, doc_emb in enumerate(doc_resp.output['embeddings']):
    similarity = cosine_similarity(query_embedding, doc_emb['embedding'])
    similarities.append((i, similarity))

  # 排序并返回 top_k 结果
  similarities.sort(key=lambda x: x[1], reverse=True)
  return [(documents[i], sim) for i, sim in similarities[:top_k]]

# 使用示例
documents = [
  "Artificial intelligence is a branch of computer science",
  "Machine learning is an important method for achieving artificial intelligence",
  "Deep learning is a subfield of machine learning"
]
query = "What is AI?"
results = semantic_search(query, documents, top_k=2)
for doc, sim in results:
  print(f"Similarity: {sim:.3f}, Document: {doc}")
```

### 推荐系统

通过分析用户历史行为的向量，发现用户兴趣偏好并推荐相似内容。

```python
import dashscope
import numpy as np
from dashscope import TextEmbedding

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def cosine_similarity(a, b):
  """计算余弦相似度"""
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
def build_recommendation_system(user_history, all_items, top_k=10):
  """构建推荐系统"""
  # 生成用户历史向量
  history_resp = TextEmbedding.call(
  model="qwen3.7-text-embedding",
  input=user_history,
  dimension=1024
  )

  # 计算用户偏好向量（取均值）
  user_embedding = np.mean([
  emb['embedding'] for emb in history_resp.output['embeddings']
  ], axis=0)

  # 生成所有物品的向量
  items_resp = TextEmbedding.call(
  model="qwen3.7-text-embedding",
  input=all_items,
  dimension=1024
  )

  # 计算推荐得分
  recommendations = []
  for i, item_emb in enumerate(items_resp.output['embeddings']):
    score = cosine_similarity(user_embedding, item_emb['embedding'])
    recommendations.append((all_items[i], score))

  # 排序并返回推荐结果
  recommendations.sort(key=lambda x: x[1], reverse=True)
  return recommendations[:top_k]

# 使用示例
user_history = ["Science Fiction", "Action", "Suspense"]
all_movies = ["Future World", "Space Adventure", "Ancient War", "Romantic Journey", "Superhero"]
recommendations = build_recommendation_system(user_history, all_movies)
for movie, score in recommendations:
  print(f"Recommendation Score: {score:.3f}, Movie: {movie}")
```

### 文本聚类

通过分析文本向量之间的距离，自动将相似文本归为一组。

```python
# 需要安装 scikit-learn：pip install scikit-learn
import dashscope
import numpy as np
from sklearn.cluster import KMeans

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def cluster_texts(texts, n_clusters=2):
  """对一组文本进行聚类"""
  # 1. 获取所有文本的向量
  resp = dashscope.TextEmbedding.call(
  model="qwen3.7-text-embedding",
  input=texts,
  dimension=1024
  )
  embeddings = np.array([item['embedding'] for item in resp.output['embeddings']])

  # 2. 使用 KMeans 算法进行聚类
  kmeans = KMeans(n_clusters=n_clusters, random_state=0, n_init='auto').fit(embeddings)

  # 3. 整理并返回结果
  clusters = {i: [] for i in range(n_clusters)}
  for i, label in enumerate(kmeans.labels_):
    clusters[label].append(texts[i])
  return clusters

# 使用示例
documents_to_cluster = [
  "Mobile phone company A releases a new phone",
  "Search engine company B launches a new system",
  "World Cup final: Argentina vs. France",
  "China wins another gold medal at the Olympics",
  "A company releases its latest AI chip",
  "European Cup match report"
]
clusters = cluster_texts(documents_to_cluster, n_clusters=2)
for cluster_id, docs in clusters.items():
  print(f"--- Cluster {cluster_id} ---")
  for doc in docs:
    print(f"- {doc}")
```

### 文本分类

通过计算输入文本与预定义标签之间的向量相似度，无需预先标注样本即可识别和分类新类别。

```python
import dashscope
import numpy as np

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def cosine_similarity(a, b):
  """计算余弦相似度"""
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def classify_text_zero_shot(text, labels):
  """零样本文本分类"""
  # 1. 获取输入文本和所有标签的向量
  resp = dashscope.TextEmbedding.call(
  model="qwen3.7-text-embedding",
  input=[text] + labels,
  dimension=1024
  )
  embeddings = resp.output['embeddings']
  text_embedding = embeddings[0]['embedding']
  label_embeddings = [emb['embedding'] for emb in embeddings[1:]]

  # 2. 计算与每个标签的相似度
  scores = [cosine_similarity(text_embedding, label_emb) for label_emb in label_embeddings]

  # 3. 返回相似度最高的标签
  best_match_index = np.argmax(scores)
  return labels[best_match_index], scores[best_match_index]

# 使用示例
text_to_classify = "The fabric of this dress is comfortable and the style is nice"
possible_labels = ["Digital Products", "Apparel & Accessories", "Food & Beverage", "Home & Living"]

label, score = classify_text_zero_shot(text_to_classify, possible_labels)
print(f"Input text: '{text_to_classify}'")
print(f"Best matching category: '{label}' (Similarity: {score:.3f})")
```

### 异常检测

通过计算文本向量与正常样本向量中心之间的相似度，识别与正常模式显著不同的异常数据。

<Note>
  示例代码中的阈值仅用于演示。实际业务场景中，相似度的具体数值取决于数据内容和分布，没有固定阈值。请根据自己的数据集校准该值。
</Note>

```python
import dashscope
import numpy as np

dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

def cosine_similarity(a, b):
  """计算余弦相似度"""
  return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def detect_anomaly(new_comment, normal_comments, threshold=0.6):
  # 1. 将所有正常评论和新评论向量化
  all_texts = normal_comments + [new_comment]
  resp = dashscope.TextEmbedding.call(
  model="qwen3.7-text-embedding",
  input=all_texts,
  dimension=1024
  )
  embeddings = [item['embedding'] for item in resp.output['embeddings']]

  # 2. 计算正常评论的中心向量（均值）
  normal_embeddings = np.array(embeddings[:-1])
  normal_center_vector = np.mean(normal_embeddings, axis=0)

  # 3. 计算新评论与中心向量的相似度
  new_comment_embedding = np.array(embeddings[-1])
  similarity = cosine_similarity(new_comment_embedding, normal_center_vector)

  # 4. 判断是否为异常
  is_anomaly = similarity < threshold
  return is_anomaly, similarity

# 使用示例
normal_user_comments = [
  "Today's meeting was productive",
  "The project is progressing smoothly",
  "The new version will be released next week",
  "User feedback is positive"
]

test_comments = {
  "Normal comment": "The feature works as expected",
  "Anomaly - meaningless garbled text": "asdfghjkl zxcvbnm"
}

print("--- Anomaly Detection Example ---")
for desc, comment in test_comments.items():
  is_anomaly, score = detect_anomaly(comment, normal_user_comments)
  result = "Yes" if is_anomaly else "No"
  print(f"Comment: '{comment}'")
  print(f"Is anomaly: {result} (Similarity to normal samples: {score:.3f})\n")
```

## API 参考

- [OpenAI 兼容 Embedding API 详情](/api-reference/text-embedding/openai-embedding)
- [DashScope Embedding API 详情](/api-reference/text-embedding/dashscope-embedding)
- [多模态 Embedding API 详情](/api-reference/multimodal-embedding/dashscope-multimodal-embedding)

## 错误码

如果调用失败，请参阅[错误信息](/api-reference/preparation/error-messages)。

## 模型性能（MTEB/CMTEB）

- **MTEB**：Massive Text Embedding Benchmark，针对分类、聚类、检索等任务的通用能力综合评测。
- **CMTEB**：Chinese Massive Text Embedding Benchmark，专门针对中文文本的评测。
- 分数范围为 0 到 100，数值越高表示性能越好。

| **模型**                    | **MTEB** | **MTEB（检索任务）** | **CMTEB** | **CMTEB（检索任务）** |
| ------------------------- | -------- | -------------- | --------- | --------------- |
| text-embedding-v3（512 维）  | 62.11    | 54.30          | 66.81     | 71.88           |
| text-embedding-v3（768 维）  | 62.43    | 54.74          | 67.90     | 72.29           |
| text-embedding-v3（1024 维） | 63.39    | 55.41          | 68.92     | 73.23           |
| text-embedding-v4（512 维）  | 64.73    | 56.34          | 68.79     | 73.33           |
| text-embedding-v4（1024 维） | 68.36    | 59.30          | 70.14     | 73.98           |
| text-embedding-v4（2048 维） | 71.58    | 61.97          | 71.99     | 75.01           |
