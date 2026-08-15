> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 分析图像与视频

> 基于视觉输入生成内容

视觉模型能够理解图像和视频，回答问题、提取文本、求解问题并生成描述。这些多模态模型将视觉理解与语言能力相结合，可应用于从 OCR 到创意写作的各类任务。

## 视觉输入结构

视觉模型可同时接受图像、视频和文本提示词。每条消息可包含多种内容类型：

- **文本提示词**：关于视觉内容的问题或指令
- **图像 URL**：在线图像的直接链接
- **Base64 图像**：本地文件的编码图像数据
- **视频 URL**：视频内容的直接链接（特定模型支持）

## 发起第一个视觉调用

**前提条件**

- [获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/install-sdk)
- 如需使用 SDK，请安装对应版本（Python SDK 1.24.6+，Java SDK 2.21.10+）

**选择哪个 API？**

- **OpenAI 兼容**：适合新集成或从 OpenAI 迁移
- **DashScope**：如果偏好原生 SDK 或需要 DashScope 特有功能，请使用此选项

<Tabs>
  <Tab title="OpenAI 兼容">
    <CodeGroup>
      ```python Python
      from openai import OpenAI
      import os

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
      )

      completion = client.chat.completions.create(
        model="qwen3.7-plus",
        messages=[
          {
            "role": "user",
            "content": [
              {
                "type": "image_url",
                "image_url": {
                  "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                },
              },
              {"type": "text", "text": "描述你在这张图片中看到的内容"},
            ],
          },
        ],
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
        const response = await openai.chat.completions.create({
          model: "qwen3.7-plus",
          messages: [
            {
              role: "user",
              content: [{
                  type: "image_url",
                  image_url: {
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                  }
                },
                {
                  type: "text",
                  text: "描述你在这张图片中看到的内容"
                }
              ]
            }
          ]
        });
        console.log(response.choices[0].message.content);
      }
      main()
      ```

      ```bash curl
      curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'Content-Type: application/json' \
      --data '{
        "model": "qwen3.7-plus",
        "messages": [
          {"role": "user",
            "content": [
            {"type": "image_url", "image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}},
            {"type": "text", "text": "描述你在这张图片中看到的内容"}
          ]
        }]
      }'
      ```
    </CodeGroup>

    **响应**

    ```
    这是一张在海滩上拍摄的照片。照片中，一人一狗坐在沙滩上，背景是大海和天空。人与狗似乎在互动，狗的前爪搭在人的手上。阳光从画面右侧照入，为场景增添了温暖的氛围。
    ```

    <Accordion title="完整 JSON 响应" defaultOpen>
      ```json
      {
        "choices": [
          {
            "message": {
              "content": "This image depicts a heartwarming scene on a sandy beach...",
              "reasoning_content": "The user wants a description of the image.\n\n1. **Identify the main subjects:** A woman and a dog...",
              "role": "assistant"
            },
            "finish_reason": "stop",
            "index": 0,
            "logprobs": null
          }
        ],
        "object": "chat.completion",
        "usage": {
          "prompt_tokens": 2520,
          "completion_tokens": 777,
          "total_tokens": 3297,
          "completion_tokens_details": {
            "reasoning_tokens": 539,
            "text_tokens": 238
          },
          "prompt_tokens_details": {
            "image_tokens": 2503,
            "text_tokens": 17
          }
        },
        "created": 1774322504,
        "system_fingerprint": null,
        "model": "qwen3.7-plus",
        "id": "chatcmpl-be9bf2d1-2e70-91c4-b8bc-c7f5bbd30320"
      }
      ```
    </Accordion>
  </Tab>

  <Tab title="DashScope">
    <CodeGroup>
      ```python Python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      messages = [
      {
        "role": "user",
        "content": [
        {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
        {"text": "描述你在这张图片中看到的内容"}]
      }]

      response = dashscope.MultiModalConversation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3.7-plus',
        messages=messages
      )

      print(response.output.choices[0].message.content[0]["text"])
      ```

      ```java Java
      import java.util.Arrays;
      import java.util.Collections;

      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;

      public class Main {

        static {
          Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
        }

        public static void simpleMultiModalConversationCall()
            throws ApiException, NoApiKeyException, UploadFileException {
          MultiModalConversation conv = new MultiModalConversation();
          MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
              .content(Arrays.asList(
              Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"),
              Collections.singletonMap("text", "描述你在这张图片中看到的内容"))).build();
          MultiModalConversationParam param = MultiModalConversationParam.builder()
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen3.7-plus")
              .messages(Arrays.asList(userMessage))
              .build();
          MultiModalConversationResult result = conv.call(param);
          System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
        }
        public static void main(String[] args) {
          try {
            simpleMultiModalConversationCall();
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
          System.exit(0);
        }
      }
      ```

      ```bash curl
      curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
        "model": "qwen3.7-plus",
        "input":{
          "messages":[
            {
              "role": "user",
              "content": [
                {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                {"text": "描述你在这张图片中看到的内容"}
              ]
            }
          ]
        }
      }'
      ```
    </CodeGroup>

    **响应**

    ```
    这是一张在海滩上拍摄的照片。照片中有一名女性和一只狗。女性坐在沙滩上，微笑着与狗互动。狗戴着项圈，似乎在与女性握手。背景是大海和天空，阳光照射在她们身上，营造出温暖的氛围。
    ```

    <Accordion title="完整 JSON 响应" defaultOpen>
      ```json
      {
        "output": {
          "choices": [
            {
              "finish_reason": "stop",
              "message": {
                "role": "assistant",
                "content": [
                  {
                    "text": "这是一张在海滩上拍摄的照片。照片中有一名穿格子衬衫的人和一只戴项圈的狗。他们坐在沙滩上，背景是大海和天空。阳光从画面右侧射入，为场景增添了温暖的氛围。"
                  }
                ]
              }
            }
          ]
        },
        "usage": {
          "output_tokens": 55,
          "input_tokens": 1271,
          "image_tokens": 1247
        },
        "request_id": "ccf845a3-dc33-9cda-b581-20fe7dc23f70"
      }
      ```
    </Accordion>
  </Tab>
</Tabs>

## 对比模型性能

### 回答图像相关问题

描述图像内容，或对其进行分类和标注，例如识别人物、地点、动物和植物。

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingRight: "12px", paddingBottom: "8px"}}>输入</th>
    <th style={{textAlign: "left", paddingLeft: "12px", paddingBottom: "8px"}}>输出</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4450772671/p1025117.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      阳光刺眼时，图片中的哪件物品应该用上？
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>阳光刺眼时，应该使用图片中的粉色太阳镜。太阳镜能有效遮挡强光、减少紫外线对眼睛的伤害，在强烈阳光下帮助保护视力、提升视觉舒适度。</td>
  </tr>
</table>

### 基于图像生成创意内容

根据图像或视频内容生成生动的文字描述，适用于故事写作、文案创作、短视频脚本等创意场景。

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingRight: "12px", paddingBottom: "8px"}}>输入</th>
    <th style={{textAlign: "left", paddingLeft: "12px", paddingBottom: "8px"}}>输出</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <img src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      请根据图片内容，帮我写一篇有趣的社交媒体帖子。
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>来自我们小小冬日仙境的圣诞祝福！我们正在用暖意融融的灯光、松果和满满的乡村风情迎接节日的到来。愿你的这个季节同样充满这份温暖与喜悦！</td>
  </tr>
</table>

### 提取文字与信息

识别图像中的文字和公式，或从收据、证书、表格中提取信息，支持格式化文本输出。Qwen3-VL 模型已将语言支持扩展至 33 种语言，详细列表请参阅[视觉模型](/developer-guides/getting-started/vision-models)。

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingRight: "12px", paddingBottom: "8px"}}>输入</th>
    <th style={{textAlign: "left", paddingLeft: "12px", paddingBottom: "8px"}}>输出</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <img src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260325/orpfsp/invoice.jpg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      Extract the following from the image: \['Invoice Code', 'Invoice Number', 'Destination', 'Fuel Surcharge', 'Fare', 'Travel Date', 'Departure Time', 'Train Number', 'Seat Number']. Please output in JSON format.
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      <code>
        {`{"Invoice Code": "221021325353", "Invoice Number": "10283819", "Destination": "Development Zone", "Fuel Surcharge": "2.0", "Fare": "8.00<Full>", "Travel Date": "2013-06-29", "Departure Time": "Serial", "Train Number": "040", "Seat Number": "371"}`}
      </code>
    </td>
  </tr>
</table>

### 解决复杂视觉问题

解答图像中的题目，例如数学、物理、化学题目，适用于小学、中学、大学及成人教育场景。

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "68%", paddingRight: "12px", paddingBottom: "8px"}}>输入</th>
    <th style={{textAlign: "left", width: "32%", paddingLeft: "12px", paddingBottom: "8px"}}>输出</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4923073671/p1025120.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      请逐步解答图片中的数学题。
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4923073671/p1025121.webp" style={{display: "block", width: "100%", margin: "0"}} />
    </td>
  </tr>
</table>

### 根据视觉设计生成代码

从图像或视频生成代码，可用于根据设计稿、网站截图等生成 HTML、CSS 和 JS 代码。

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "44%", paddingRight: "12px", paddingBottom: "8px"}}>输入</th>
    <th style={{textAlign: "left", width: "56%", paddingLeft: "12px", paddingBottom: "8px"}}>输出</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4450772671/p1025123.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      请根据我的草图，以黑色为主色调，用 HTML 和 CSS 设计一个网页。
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      <img src="https://img.alicdn.com/imgextra/i1/O1CN01PfqKQ81MnQucdjy7D_!!6000000001479-2-tps-1440-736.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      <strong>网页预览</strong>
    </td>
  </tr>
</table>

### 定位图像中的物体

模型支持 2D 和 3D 定位，可判断物体方向、视角变化及遮挡关系。Qwen3-VL 新增了 3D 定位能力。

<Note>
  对于 Qwen2.5-VL，目标检测在 480x480 至 2560x2560 分辨率范围内表现良好。超出该范围时，精度可能下降，偶尔出现边界框偏移。如需在原始图像上绘制定位结果，请参阅 [FAQ](#常见问题)。
</Note>

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingRight: "12px", paddingBottom: "8px"}}>输入</th>
    <th style={{textAlign: "left", width: "50%", paddingLeft: "12px", paddingBottom: "8px"}}>输出</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <strong>2D 定位</strong>

      <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4450772671/p1025125.webp" style={{display: "block", width: "100%", margin: "8px 0"}} />

      - 返回 Box（边界框）坐标：检测图像中所有食物，以 JSON 格式输出其 bbox 坐标。
        <br />- 返回 Point（质心）坐标：以点的形式定位图像中所有食物，以 XML 格式输出其点坐标。
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      <strong>2D 定位结果可视化</strong>

      <img src="https://img.alicdn.com/imgextra/i2/O1CN01nH0jIE1kIKnVTJ3RB_!!6000000004660-2-tps-1024-683.png" style={{display: "block", width: "100%", marginTop: "8px"}} />
    </td>
  </tr>
</table>

<Accordion title="3D 定位" defaultOpen>
  <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4450772671/p1025127.webp" width="300" />

  检测图像中的汽车并预测其 3D 位置。输出 JSON 格式：`[{"bbox_3d": [x_center, y_center, z_center, x_size, y_size, z_size, roll, pitch, yaw], "label": "category"}]`。
</Accordion>

<Accordion title="3D 定位结果可视化" defaultOpen>
  <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4450772671/p1025128.webp" width="300" />
</Accordion>

### 解析文档与 PDF

将基于图像的文档（如扫描件或图像 PDF）解析为 QwenVL HTML 或 QwenVL Markdown 格式。该格式不仅能精准识别文本，还能获取图像、表格等元素的位置信息。Qwen3-VL 新增了将文档解析为 Markdown 格式的能力。

<Note>
  推荐使用以下提示词：`qwenvl html`（解析为 HTML 格式）或 `qwenvl markdown`（解析为 Markdown 格式）。
</Note>

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "48%", paddingRight: "12px", paddingBottom: "8px"}}>输入</th>
    <th style={{textAlign: "left", width: "52%", paddingLeft: "12px", paddingBottom: "8px"}}>输出</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <img src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260325/xkvcud/20260325134759.jpg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      qwenvl markdown.
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      <img src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260325/pvtibq/output_annotated.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      <strong>结果可视化</strong>
    </td>
  </tr>
</table>

### 分析视频内容

分析视频内容，例如定位特定事件并获取时间戳，或生成关键时段的摘要。

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "50%", paddingRight: "12px", paddingBottom: "8px"}}>输入</th>
    <th style={{textAlign: "left", paddingLeft: "12px", paddingBottom: "8px"}}>输出</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top", paddingRight: "12px"}}>
      <video src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250307/ozcoym/hailuo_1060827889_RF.hd.mp4" controls style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

      Please describe the series of actions of the person in the video. Output in JSON format with start\_time, end\_time, and event. Use HH:mm:ss for timestamps.
    </td>

    <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
      <code>
        {`{"events": [{"start_time": "00:00:00", "end_time": "00:00:05", "event": "The person walks towards the table holding a cardboard box and places it on the table."}, {"start_time": "00:00:05", "end_time": "00:00:15", "event": "The person picks up a scanner and scans the label on the cardboard box."}, {"start_time": "00:00:15", "end_time": "00:00:21", "event": "The person puts the scanner back in its place and then picks up a pen to write information in a notebook."}]}`}
      </code>
    </td>
  </tr>
</table>

## 处理视觉内容

### 思考模式

<Tip>
  关于启用/禁用、流式输出及 `thinking_budget` 的说明，请参阅[思考](/developer-guides/text-generation/thinking)。
</Tip>

视觉模型默认值：`qwen3-vl-plus` 和 `qwen3-vl-flash` 默认**关闭**思考，Qwen3.5 及以后系列默认**开启**思考。带有 `-thinking` 后缀的模型始终开启思考。`stepfun/step-3.7-flash` 默认**关闭**思考，通过 `enable_thinking` 开启。

### 使用多张图像

在单个请求中传入多张图像，适用于**产品对比、多页文档处理**等任务。在 `user message` 的 `content` 数组中包含多个图像对象即可。

<Warning>
  每次请求：通过**公共 URL** 或**本地文件路径**传入时，最多支持 **256** 张图像；通过 **Base64 编码**传入时，最多支持 **250** 张图像。此外，所有图像与文本的 Token 总数必须**低于**模型的最大输入上限（图像与文本合计的 Token 限制）。
</Warning>

<Tabs>
  <Tab title="OpenAI 兼容">
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
          model="qwen3.7-plus",
          messages=[
            {"role": "user","content": [
              {"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},},
              {"type": "image_url","image_url": {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},},
              {"type": "text", "text": "这两张图片描述的是什么？"},
              ],
            }
          ],
        )

        print(completion.choices[0].message.content)
        ```

        **响应**

        ```
        图片 1 展示了一名女性和一只拉布拉多猎犬在海滩上互动的场景。女性穿着格子衬衫坐在沙滩上，与狗握手。背景是海浪和天空，整张图片充满了温馨愉快的氛围。

        图片 2 展示了一只老虎在森林中行走的场景。老虎的毛色为橙色带黑色条纹，正在向前迈步。周围是茂密的树木和植被，地面覆盖着落叶，整张图片给人一种原野自然的感觉。
        ```
      </Tab>

      <Tab title="Node.js">
        ```javascript
        import OpenAI from "openai";

        const openai = new OpenAI(
          {
            apiKey: process.env.DASHSCOPE_API_KEY,
            baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
          }
        );

        async function main() {
          const response = await openai.chat.completions.create({
            model: "qwen3.7-plus",
            messages: [
                  {role: "user",content: [
              {type: "image_url",image_url: {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"}},
              {type: "image_url",image_url: {"url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"}},
              {type: "text", text: "这两张图片描述的是什么？" },
            ]}]
          });
          console.log(response.choices[0].message.content);
        }

        main()
        ```

        **响应**

        ```
        在第一张图片中，一个人和一只狗在海滩上互动。那个人穿着格子衬衫，狗戴着项圈，他们似乎在握手或击掌。

        在第二张图片中，一只老虎正在森林中行走。老虎的毛色为橙色带黑色条纹，背景是绿色的树木和植被。
        ```
      </Tab>

      <Tab title="curl">
        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H 'Content-Type: application/json' \
        -d '{
          "model": "qwen3.7-plus",
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "type": "image_url",
                  "image_url": {
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"
                  }
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"
                  }
                },
                {
                  "type": "text",
                  "text": "这两张图片描述的是什么？"
                }
              ]
            }
          ]
        }'
        ```

        **响应**

        ```
        图片 1 展示了一名女性和一只拉布拉多猎犬在海滩上互动的场景。女性穿着格子衬衫坐在沙滩上，与狗握手。背景是海景和夕阳，整张图片看起来非常温馨和谐。

        图片 2 展示了一只老虎在森林中行走的场景。老虎的毛色为橙色带黑色条纹，正在向前迈步。周围是茂密的树木和植被，地面覆盖着落叶，整张图片充满了自然的野性与活力。
        ```

        <Accordion title="完整 JSON 响应" defaultOpen>
          ```json
          {
            "choices": [
              {
                "message": {
                  "content": "图片 1 展示了一名女性和一只拉布拉多猎犬在海滩上互动的场景。女性穿着格子衬衫坐在沙滩上，与狗握手。背景是海景和夕阳，整张图片看起来非常温馨和谐。\n\n图片 2 展示了一只老虎在森林中行走的场景。老虎的毛色为橙色带黑色条纹，正在向前迈步。周围是茂密的树木和植被，地面覆盖着落叶，整张图片充满了自然的野性与活力。",
                  "role": "assistant"
                },
                "finish_reason": "stop",
                "index": 0,
                "logprobs": null
              }
            ],
            "object": "chat.completion",
            "usage": {
              "prompt_tokens": 2497,
              "completion_tokens": 109,
              "total_tokens": 2606
            },
            "created": 1725948561,
            "system_fingerprint": null,
            "model": "qwen3.7-plus",
            "id": "chatcmpl-0fd66f46-b09e-9164-a84f-3ebbbedbac15"
          }
          ```
        </Accordion>
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import dashscope

        dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

        messages = [
          {
            "role": "user",
            "content": [
              {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
              {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},
              {"text": "这两张图片描述的是什么？"}
            ]
          }
        ]

        response = dashscope.MultiModalConversation.call(
          api_key=os.getenv('DASHSCOPE_API_KEY'),
          model='qwen3.7-plus',
          messages=messages
        )

        print(response.output.choices[0].message.content[0]["text"])
        ```

        **响应**

        ```
        这些图片展示了一些动物和自然场景。在第一张图片中，一个人和一只狗在海滩上互动。第二张图片是一只老虎在森林中行走。
        ```
      </Tab>

      <Tab title="Java">
        ```java
        import java.util.Arrays;
        import java.util.Collections;
        import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
        import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
        import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
        import com.alibaba.dashscope.common.MultiModalMessage;
        import com.alibaba.dashscope.common.Role;
        import com.alibaba.dashscope.exception.ApiException;
        import com.alibaba.dashscope.exception.NoApiKeyException;
        import com.alibaba.dashscope.exception.UploadFileException;
        import com.alibaba.dashscope.utils.Constants;

        public class Main {
          static {
            Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
          }
          public static void simpleMultiModalConversationCall()
              throws ApiException, NoApiKeyException, UploadFileException {
            MultiModalConversation conv = new MultiModalConversation();
            MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"),
                Collections.singletonMap("image", "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"),
                Collections.singletonMap("text", "这两张图片描述的是什么？"))).build();
            MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.7-plus")
                .messages(Arrays.asList(userMessage))
                .build();
            MultiModalConversationResult result = conv.call(param);
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));    }
          public static void main(String[] args) {
            try {
              simpleMultiModalConversationCall();
            } catch (ApiException | NoApiKeyException | UploadFileException e) {
              System.out.println(e.getMessage());
            }
            System.exit(0);
          }
        }
        ```

        **响应**

        ```
        这些图片展示了一些动物和自然场景。

        1. 第一张图片：一名女性和一只狗在海滩上互动。女性穿着格子衬衫坐在沙滩上，狗戴着项圈，伸出爪子与女性握手。
        2. 第二张图片：一只老虎在森林中行走。老虎的毛色为橙色带黑色条纹，背景是树木和落叶。
        ```
      </Tab>

      <Tab title="curl">
        ```bash
        curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
        --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
        --header 'Content-Type: application/json' \
        --data '{
          "model": "qwen3.7-plus",
          "input":{
            "messages":[
              {
                "role": "user",
                "content": [
                  {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241022/emyrja/dog_and_girl.jpeg"},
                  {"image": "https://dashscope.oss-cn-beijing.aliyuncs.com/images/tiger.png"},
                  {"text": "这两张图片展示了什么？"}
                ]
              }
            ]
          }
        }'
        ```

        **响应**

        ```
        这些图片展示了一些动物和自然场景。在第一张图片中，一个人和一只狗在海滩上互动。第二张图片是一只老虎在森林中行走。
        ```

        <Accordion title="完整 JSON 响应" defaultOpen>
          ```json
          {
            "output": {
              "choices": [
                {
                  "finish_reason": "stop",
                  "message": {
                    "role": "assistant",
                    "content": [
                      {
                        "text": "这些图片展示了一些动物和自然场景。在第一张图片中，一个人和一只狗在海滩上互动。第二张图片是一只老虎在森林中行走。"
                      }
                    ]
                  }
                }
              ]
            },
            "usage": {
              "output_tokens": 81,
              "input_tokens": 1277,
              "image_tokens": 2497
            },
            "request_id": "ccf845a3-dc33-9cda-b581-20fe7dc23f70"
          }
          ```
        </Accordion>
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

### 分析视频内容

视觉理解模型支持理解视频内容。您可以以图像列表（视频帧）或视频文件的形式提供文件。以下是通过 URL 指定在线视频或图像列表进行理解的示例代码。有关视频限制或图像列表中可传入的图像数量，请参阅[视频限制](#输入文件限制)部分。

<Note>
  建议使用最新版本或近期快照版本的模型，以获得更好的视频文件理解性能。
</Note>

<Tabs>
  <Tab title="视频文件">
    视觉理解模型通过从视频中提取一系列帧来分析内容。您可以使用以下两个参数控制帧提取策略：

    - **fps**：控制提取频率，每隔 `1/fps` 秒提取一帧。取值范围为 \[0.1, 10]，默认值为 2.0。
      - 高速运动场景：设置较高的 fps 值以捕获更多细节。
      - 静态或长视频：设置较低的 fps 值以提高效率。
    - **max\_frames**： 提取帧数的上限。当基于 fps 计算的帧数超过 max\_frames 时，系统会自动均匀采样，使帧数保持在上限以内。**此参数仅对 DashScope SDK 生效。**

    <Tabs>
      <Tab title="OpenAI 兼容">
        <Note>
          使用 OpenAI SDK 或 HTTP 方式直接向视觉理解模型输入视频文件时，必须将用户消息中的 `"type"` 参数设置为 `"video_url"`。
        </Note>

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
              model="qwen3.7-plus",
              messages=[
                {
                  "role": "user",
                  "content": [
                    {
                      "type": "video_url",
                      "video_url": {
                        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                      },
                      "fps": 2
                    },
                    {
                      "type": "text",
                      "text": "总结这个视频中发生了什么"
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

            const openai = new OpenAI(
              {
                apiKey: process.env.DASHSCOPE_API_KEY,
                baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
              }
            );

            async function main() {
              const response = await openai.chat.completions.create({
                model: "qwen3.7-plus",
                messages: [
                  {
                    role: "user",
                    content: [
                      {
                        type: "video_url",
                        video_url: {
                          "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                        },
                        "fps": 2
                      },
                      {
                        type: "text",
                        text: "总结这个视频中发生了什么"
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

          <Tab title="curl">
            ```bash
            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
                "model": "qwen3.7-plus",
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "type": "video_url",
                        "video_url": {
                          "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4"
                        },
                        "fps":2
                      },
                      {
                        "type": "text",
                        "text": "总结这个视频中发生了什么"
                      }
                    ]
                  }
                ]
              }'
            ```
          </Tab>
        </Tabs>
      </Tab>

      <Tab title="DashScope">
        <Tabs>
          <Tab title="Python">
            ```python
            import dashscope
            import os

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            messages = [
              {"role": "user",
                "content": [
                  {"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4","fps":2},
                  {"text": "总结这个视频中发生了什么"}
                ]
              }
            ]

            response = dashscope.MultiModalConversation.call(
              api_key=os.getenv('DASHSCOPE_API_KEY'),
              model='qwen3.7-plus',
              messages=messages
            )

            print(response.output.choices[0].message.content[0]["text"])
            ```
          </Tab>

          <Tab title="Java">
            ```java
            import java.util.Arrays;
            import java.util.Collections;
            import java.util.HashMap;
            import java.util.Map;

            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.alibaba.dashscope.utils.Constants;

            public class Main {
              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }
              public static void simpleMultiModalConversationCall()
              throws ApiException, NoApiKeyException, UploadFileException {
                MultiModalConversation conv = new MultiModalConversation();
                Map<String, Object> params = new HashMap<>();
                params.put("video", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4");
                params.put("fps", 2);
                MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                params,
                Collections.singletonMap("text", "总结这个视频中发生了什么"))).build();
                MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.7-plus")
                .messages(Arrays.asList(userMessage))
                .build();
                MultiModalConversationResult result = conv.call(param);
                System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
              }
              public static void main(String[] args) {
                try {
                  simpleMultiModalConversationCall();
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
            ```
          </Tab>

          <Tab title="curl">
            ```bash
            curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H 'Content-Type: application/json' \
            -d '{
              "model": "qwen3.7-plus",
              "input":{
                "messages":[
                  {"role": "user","content": [{"video": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241115/cqqkru/1.mp4","fps":2},
                  {"text": "总结这个视频中发生了什么"}]}]}
            }'
            ```
          </Tab>
        </Tabs>
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="图像列表">
    当以图像列表形式（预提取的视频帧）传入视频时，可使用 `fps` 参数告知模型相邻帧之间的时间间隔，帮助模型更好地理解事件的顺序、持续时长和动态变化。该参数表示视频帧每隔 `1/fps` 秒从原始视频中提取一次，**Qwen3.5**、**Qwen3-VL 和 Qwen2.5-VL** 模型均支持此参数。

    <Tabs>
      <Tab title="OpenAI 兼容">
        <Note>
          使用 OpenAI SDK 或 HTTP 方式向视觉理解模型输入图像列表形式的视频时，必须将用户消息中的 `"type"` 参数设置为 `"video"`。
        </Note>

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
              model="qwen3.7-plus",
              messages=[{"role": "user","content": [
              {"type": "video","video": [
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
              "fps":2},
              {"type": "text","text": "描述这个视频的具体过程"},
              ]}]
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
                model: "qwen3.7-plus",
                messages: [{
                  role: "user",
                  content: [
                    {
                      type: "video",
                      video: [
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                        "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
                        "fps": 2
                    },
                    {
                      type: "text",
                      text: "描述这个视频的具体过程"
                    }
                  ]
                }]
              });
              console.log(response.choices[0].message.content);
            }

            main();
            ```
          </Tab>

          <Tab title="curl">
            ```bash
            curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H 'Content-Type: application/json' \
            -d '{
              "model": "qwen3.7-plus",
              "messages": [{"role": "user","content": [{"type": "video","video": [
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
              "fps":2},
              {"type": "text","text": "描述这个视频的具体过程"}]}]
            }'
            ```
          </Tab>
        </Tabs>
      </Tab>

      <Tab title="DashScope">
        <Tabs>
          <Tab title="Python">
            ```python
            import os
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            messages = [{"role": "user",
              "content": [
              {"video":["https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
              "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"],
              "fps":2},
              {"text": "描述这个视频的具体过程"}]}]
            response = dashscope.MultiModalConversation.call(
              api_key=os.getenv("DASHSCOPE_API_KEY"),
              model='qwen3.7-plus',
              messages=messages
            )
            print(response.output.choices[0].message.content[0]["text"])
            ```
          </Tab>

          <Tab title="Java">
            ```java
            // DashScope SDK 版本须为 2.21.10 或更高
            import java.util.Arrays;
            import java.util.Collections;
            import java.util.HashMap;
            import java.util.Map;

            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
            import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
            import com.alibaba.dashscope.common.MultiModalMessage;
            import com.alibaba.dashscope.common.Role;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.exception.UploadFileException;
            import com.alibaba.dashscope.utils.Constants;

            public class Main {
              static {
                Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
              }
              private static final String MODEL_NAME = "qwen3.7-plus";
              public static void videoImageListSample() throws ApiException, NoApiKeyException, UploadFileException {
                MultiModalConversation conv = new MultiModalConversation();
                Map<String, Object> params = new HashMap<>();
                params.put("video", Arrays.asList("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                    "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"));
                params.put("fps", 2);
                MultiModalMessage userMessage = MultiModalMessage.builder()
                    .role(Role.USER.getValue())
                    .content(Arrays.asList(
                    params,
                    Collections.singletonMap("text", "描述这个视频的具体过程")))
                    .build();
                MultiModalConversationParam param = MultiModalConversationParam.builder()
                    .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                    .model(MODEL_NAME)
                    .messages(Arrays.asList(userMessage)).build();
                MultiModalConversationResult result = conv.call(param);
                System.out.print(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
              }
              public static void main(String[] args) {
                try {
                  videoImageListSample();
                } catch (ApiException | NoApiKeyException | UploadFileException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
            ```
          </Tab>

          <Tab title="curl">
            ```bash
            curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H 'Content-Type: application/json' \
            -d '{
              "model": "qwen3.7-plus",
              "input": {
                "messages": [
                  {
                    "role": "user",
                    "content": [
                      {
                        "video": [
                          "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/xzsgiz/football1.jpg",
                          "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/tdescd/football2.jpg",
                          "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/zefdja/football3.jpg",
                          "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20241108/aedbqh/football4.jpg"
                        ],
                        "fps":2
                      },
                      {
                        "text": "描述这个视频的具体过程"
                      }
                    ]
                  }
                ]
              }
            }'
            ```
          </Tab>
        </Tabs>
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

### 使用本地文件

视觉理解模型提供两种上传本地文件的方式：Base64 编码和直接传入文件路径。请根据文件大小和使用的 SDK 选择合适的上传方式。具体建议请参阅[如何选择文件上传方式](#常见问题)。两种方式均须满足[图像限制](#输入文件限制)中描述的文件要求。

<Tabs>
  <Tab title="Base64 编码上传">
    将文件转换为 Base64 编码字符串后传入模型。OpenAI SDK、DashScope SDK 及 HTTP 请求均支持此方式。

    <Accordion title="通过 Base64 编码字符串传入文件的步骤（以图像为例）" defaultOpen>
      <Steps>
        <Step title="文件编码">
          将本地图像转换为 Base64 编码。

          <Accordion title="将图像转换为 Base64 编码的示例代码" defaultOpen>
            ```python
            #  编码函数：将本地文件转换为 Base64 编码字符串
            import base64
            def encode_image(image_path):
              with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode("utf-8")

            # 将 xxxx/eagle.png 替换为本地图像的绝对路径
            base64_image = encode_image("xxx/eagle.png")
            ```
          </Accordion>
        </Step>

        <Step title="构造 Data URL">
          格式如下：`data:[MIME_type];base64,<base64_image>`。

          1. 将 `MIME_type` 替换为实际媒体类型，确保与[支持的图像格式](#输入文件限制)表中的 `MIME type` 值匹配，例如 `image/jpeg` 或 `image/png`。
          2. `base64_image` 是上一步生成的 Base64 字符串。
        </Step>

        <Step title="调用模型">
          通过 `image` 或 `image_url` 参数传入 `Data URL` 并调用模型。
        </Step>
      </Steps>
    </Accordion>
  </Tab>

  <Tab title="文件路径上传">
    直接向模型传入本地文件路径。此方式仅支持 DashScope Python SDK 和 Java SDK，不支持 DashScope HTTP 或 OpenAI 兼容方式。

    请参考以下表格，根据编程语言和操作系统指定文件路径。

    <Accordion title="指定文件路径（以图像为例）" defaultOpen>
| **系统**        | **SDK**    | **输入文件路径**         | **示例**                         |
| ------------- | ---------- | ------------------ | ------------------------------ |
| Linux 或 macOS | Python SDK | `file://<文件绝对路径>`  | `file:///home/images/test.png` |
| Linux 或 macOS | Java SDK   | `file://<文件绝对路径>`  | `file:///home/images/test.png` |
| Windows       | Python SDK | `file://<文件绝对路径>`  | `file://D:/images/test.png`    |
| Windows       | Java SDK   | `file:///<文件绝对路径>` | `file:///D:/images/test.png`   |
    </Accordion>
  </Tab>
</Tabs>

下方代码示例展示了如何使用 Base64 编码和文件路径两种方式传入本地图像、视频和图像列表。示例数量较多，按文件类型分组整理。

<Accordion title="图像 - 通过文件路径传入（仅 DashScope）" defaultOpen>
  <Tabs>
    <Tab title="Python">
      ```python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      # 将 xxx/eagle.png 替换为本地图像的绝对路径
      local_path = "xxx/eagle.png"
      image_path = f"file://{local_path}"
      messages = [
        {'role':'user',
        'content': [{'image': image_path},
        {'text': '描述你在这张图片中看到的内容'}]}]
      response = dashscope.MultiModalConversation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3.7-plus',
        messages=messages)
      print(response.output.choices[0].message.content[0]["text"])
      ```
    </Tab>

    <Tab title="Java">
      ```java
      import java.util.Arrays;
      import java.util.Collections;
      import java.util.HashMap;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;

      public class Main {

        static {
          Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
        }

        public static void callWithLocalFile(String localPath)
            throws ApiException, NoApiKeyException, UploadFileException {
          String filePath = "file://"+localPath;
          MultiModalConversation conv = new MultiModalConversation();
          MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
              .content(Arrays.asList(new HashMap<String, Object>(){{put("image", filePath);}},
              new HashMap<String, Object>(){{put("text", "描述你在这张图片中看到的内容");}})).build();
          MultiModalConversationParam param = MultiModalConversationParam.builder()
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen3.7-plus")
              .messages(Arrays.asList(userMessage))
              .build();
          MultiModalConversationResult result = conv.call(param);
          System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));}

        public static void main(String[] args) {
          try {
            // Replace xxx/eagle.png with the absolute path of your local image
            callWithLocalFile("xxx/eagle.png");
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
          System.exit(0);
        }
      }
      ```
    </Tab>
  </Tabs>
</Accordion>

<Accordion title="图像 - 通过 Base64 编码传入" defaultOpen>
  <Tabs>
    <Tab title="OpenAI 兼容">
      <Tabs>
        <Tab title="Python">
          ```python
          from openai import OpenAI
          import os
          import base64

          def encode_image(image_path):
            with open(image_path, "rb") as image_file:
              return base64.b64encode(image_file.read()).decode("utf-8")

          base64_image = encode_image("xxx/eagle.png")
          client = OpenAI(
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
          )
          completion = client.chat.completions.create(
            model="qwen3.7-plus",
            messages=[
              {
                "role": "user",
                "content": [
                  {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{base64_image}"},
                  },
                  {"type": "text", "text": "描述你在这张图片中看到的内容"},
                ],
              }
            ],
          )
          print(completion.choices[0].message.content)
          ```
        </Tab>

        <Tab title="Node.js">
          ```javascript
          import OpenAI from "openai";
          import { readFileSync } from 'fs';

          const openai = new OpenAI(
              {
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
              }
          );

          const encodeImage = (imagePath) => {
              const imageFile = readFileSync(imagePath);
              return imageFile.toString('base64');
            };
          const base64Image = encodeImage("xxx/eagle.png")
          async function main() {
              const completion = await openai.chat.completions.create({
              model: "qwen3.7-plus",
              messages: [
              {"role": "user",
              "content": [{"type": "image_url",
              "image_url": {"url": `data:image/png;base64,${base64Image}`},},
              {"type": "text", "text": "描述你在这张图片中看到的内容"}]}]
              });
              console.log(completion.choices[0].message.content);
          }

          main();
          ```
        </Tab>

        <Tab title="curl">
          - 为便于展示，代码中的 Base64 编码字符串已截断，实际调用时必须传入完整的编码字符串。

          ```bash
          curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
          --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
          --header 'Content-Type: application/json' \
          --data '{
            "model": "qwen3.7-plus",
            "messages": [
            {
              "role": "user",
              "content": [
                {"type": "image_url", "image_url": {"url": "data:image/jpg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA"}},
                {"type": "text", "text": "描述你在这张图片中看到的内容"}
              ]
            }]
          }'
          ```
        </Tab>
      </Tabs>
    </Tab>

    <Tab title="DashScope">
      <Tabs>
        <Tab title="Python">
          ```python
          import base64
          import os
          import dashscope

          dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

          def encode_image(image_path):
            with open(image_path, "rb") as image_file:
              return base64.b64encode(image_file.read()).decode("utf-8")

          base64_image = encode_image("xxxx/eagle.png")

          messages = [
            {
              "role": "user",
              "content": [
                {"image": f"data:image/png;base64,{base64_image}"},
                {"text": "描述你在这张图片中看到的内容"},
              ],
            },
          ]

          response = dashscope.MultiModalConversation.call(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            model="qwen3.7-plus",
            messages=messages,
          )
          print(response.output.choices[0].message.content[0]["text"])
          ```
        </Tab>

        <Tab title="Java">
          ```java
          import java.io.IOException;
          import java.util.Arrays;
          import java.util.Collections;
          import java.util.HashMap;
          import java.util.Base64;
          import java.nio.file.Files;
          import java.nio.file.Path;
          import java.nio.file.Paths;

          import com.alibaba.dashscope.aigc.multimodalconversation.*;
          import com.alibaba.dashscope.common.MultiModalMessage;
          import com.alibaba.dashscope.common.Role;
          import com.alibaba.dashscope.exception.ApiException;
          import com.alibaba.dashscope.exception.NoApiKeyException;
          import com.alibaba.dashscope.exception.UploadFileException;
          import com.alibaba.dashscope.utils.Constants;

          public class Main {

            static {
              Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
            }

            private static String encodeImageToBase64(String imagePath) throws IOException {
              Path path = Paths.get(imagePath);
              byte[] imageBytes = Files.readAllBytes(path);
              return Base64.getEncoder().encodeToString(imageBytes);
            }

            public static void callWithLocalFile(String localPath) throws ApiException, NoApiKeyException, UploadFileException, IOException {

              String base64Image = encodeImageToBase64(localPath);

              MultiModalConversation conv = new MultiModalConversation();
              MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                  .content(Arrays.asList(
                  new HashMap<String, Object>() {{ put("image", "data:image/png;base64," + base64Image); }},
                  new HashMap<String, Object>() {{ put("text", "描述你在这张图片中看到的内容"); }}
                  )).build();

              MultiModalConversationParam param = MultiModalConversationParam.builder()
                  .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                  .model("qwen3.7-plus")
                  .messages(Arrays.asList(userMessage))
                  .build();

              MultiModalConversationResult result = conv.call(param);
              System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
            }

            public static void main(String[] args) {
              try {
                callWithLocalFile("xxx/eagle.png");
              } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
                System.out.println(e.getMessage());
              }
              System.exit(0);
            }
          }
          ```
        </Tab>

        <Tab title="curl">
          - 为便于展示，代码中的 Base64 编码字符串已截断，实际调用时必须传入完整的编码字符串。

          ```bash
          curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
          -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
          -H 'Content-Type: application/json' \
          -d '{
            "model": "qwen3.7-plus",
            "input":{
              "messages":[
                {
                  "role": "user",
                  "content": [
                  {"image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},
                  {"text": "描述你在这张图片中看到的内容"}
                  ]
                }
              ]
            }
          }'
          ```
        </Tab>
      </Tabs>
    </Tab>
  </Tabs>
</Accordion>

<Accordion title="视频文件 - 通过文件路径传入（仅 DashScope）" defaultOpen>
  本示例使用本地保存的 [test.mp4](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/nvwkcj/test.mp4) 文件。

  <Tabs>
    <Tab title="Python">
      ```python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      local_path = "xxx/test.mp4"
      video_path = f"file://{local_path}"
      messages = [
        {'role':'user',
        'content': [{'video': video_path,"fps":2},
        {'text': '这个视频描绘了什么场景？'}]}]
      response = dashscope.MultiModalConversation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3.7-plus',
        messages=messages)
      print(response.output.choices[0].message.content[0]["text"])
      ```
    </Tab>

    <Tab title="Java">
      ```java
      import java.util.Arrays;
      import java.util.Collections;
      import java.util.HashMap;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;

      public class Main {

        static {
          Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
        }

        public static void callWithLocalFile(String localPath)
            throws ApiException, NoApiKeyException, UploadFileException {
          String filePath = "file://"+localPath;
          MultiModalConversation conv = new MultiModalConversation();
          MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
              .content(Arrays.asList(new HashMap<String, Object>()
              {{
              put("video", filePath);
              put("fps", 2);
              }},
              new HashMap<String, Object>(){{put("text", "这个视频描绘了什么场景？");}})).build();
          MultiModalConversationParam param = MultiModalConversationParam.builder()
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model("qwen3.7-plus")
              .messages(Arrays.asList(userMessage))
              .build();
          MultiModalConversationResult result = conv.call(param);
          System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));}

        public static void main(String[] args) {
          try {
            callWithLocalFile("xxx/test.mp4");
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
          System.exit(0);
        }
      }
      ```
    </Tab>
  </Tabs>
</Accordion>

<Accordion title="视频文件 - 通过 Base64 编码传入" defaultOpen>
  <Tabs>
    <Tab title="OpenAI 兼容">
      <Tabs>
        <Tab title="Python">
          ```python
          from openai import OpenAI
          import os
          import base64

          def encode_video(video_path):
            with open(video_path, "rb") as video_file:
              return base64.b64encode(video_file.read()).decode("utf-8")

          base64_video = encode_video("xxx/test.mp4")
          client = OpenAI(
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
          )
          completion = client.chat.completions.create(
            model="qwen3.7-plus",
            messages=[
              {
                "role": "user",
                "content": [
                  {
                    "type": "video_url",
                    "video_url": {"url": f"data:video/mp4;base64,{base64_video}"},
                    "fps":2
                  },
                  {"type": "text", "text": "这个视频描绘了什么场景？"},
                ],
              }
            ],
          )
          print(completion.choices[0].message.content)
          ```
        </Tab>

        <Tab title="Node.js">
          ```javascript
          import OpenAI from "openai";
          import { readFileSync } from 'fs';

          const openai = new OpenAI(
              {
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
              }
          );

          const encodeVideo = (videoPath) => {
              const videoFile = readFileSync(videoPath);
              return videoFile.toString('base64');
            };
          const base64Video = encodeVideo("xxx/test.mp4")
          async function main() {
              const completion = await openai.chat.completions.create({
              model: "qwen3.7-plus",
              messages: [
              {"role": "user",
              "content": [{
              "type": "video_url",
              "video_url": {"url": `data:video/mp4;base64,${base64Video}`},
              "fps":2},
              {"type": "text", "text": "这个视频描绘了什么场景？"}]}]
              });
              console.log(completion.choices[0].message.content);
          }

          main();
          ```
        </Tab>

        <Tab title="curl">
          - 为便于展示，代码中的 Base64 编码字符串已截断，实际调用时必须传入完整的编码字符串。

          ```bash
          curl --location 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
          --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
          --header 'Content-Type: application/json' \
          --data '{
            "model": "qwen3.7-plus",
            "messages": [
            {
              "role": "user",
              "content": [
                {"type": "video_url", "video_url": {"url": "data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},"fps":2},
                {"type": "text", "text": "图像中描绘了什么场景？"}
              ]
            }]
          }'
          ```
        </Tab>
      </Tabs>
    </Tab>

    <Tab title="DashScope">
      <Tabs>
        <Tab title="Python">
          ```python
          import base64
          import os
          import dashscope

          dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

          def encode_video(video_path):
            with open(video_path, "rb") as video_file:
              return base64.b64encode(video_file.read()).decode("utf-8")

          base64_video = encode_video("xxxx/test.mp4")

          messages = [{'role':'user',
              'content': [{'video': f"data:video/mp4;base64,{base64_video}","fps":2},
              {'text': '这个视频描绘了什么场景？'}]}]
          response = dashscope.MultiModalConversation.call(
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            model='qwen3.7-plus',
            messages=messages)

          print(response.output.choices[0].message.content[0]["text"])
          ```
        </Tab>

        <Tab title="Java">
          ```java
          import java.io.IOException;
          import java.util.*;
          import java.nio.file.Files;
          import java.nio.file.Path;
          import java.nio.file.Paths;

          import com.alibaba.dashscope.aigc.multimodalconversation.*;
          import com.alibaba.dashscope.common.MultiModalMessage;
          import com.alibaba.dashscope.common.Role;
          import com.alibaba.dashscope.exception.ApiException;
          import com.alibaba.dashscope.exception.NoApiKeyException;
          import com.alibaba.dashscope.exception.UploadFileException;
          import com.alibaba.dashscope.utils.Constants;

          public class Main {

            static {
              Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
            }

            private static String encodeVideoToBase64(String videoPath) throws IOException {
              Path path = Paths.get(videoPath);
              byte[] videoBytes = Files.readAllBytes(path);
              return Base64.getEncoder().encodeToString(videoBytes);
            }

            public static void callWithLocalFile(String localPath)
                throws ApiException, NoApiKeyException, UploadFileException, IOException {

              String base64Video = encodeVideoToBase64(localPath);

              MultiModalConversation conv = new MultiModalConversation();
              MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                  .content(Arrays.asList(new HashMap<String, Object>()
                  {{
                  put("video", "data:video/mp4;base64," + base64Video);
                  put("fps", 2);
                  }},
                  new HashMap<String, Object>(){{put("text", "这个视频描绘了什么场景？");}})).build();

              MultiModalConversationParam param = MultiModalConversationParam.builder()
                  .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                  .model("qwen3.7-plus")
                  .messages(Arrays.asList(userMessage))
                  .build();

              MultiModalConversationResult result = conv.call(param);
              System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
            }

            public static void main(String[] args) {
              try {
                callWithLocalFile("xxx/test.mp4");
              } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
                System.out.println(e.getMessage());
              }
              System.exit(0);
            }
          }
          ```
        </Tab>

        <Tab title="curl">
          - 为便于展示，代码中的 Base64 编码字符串已截断，实际调用时必须传入完整的编码字符串。

          ```bash
          curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
          -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
          -H 'Content-Type: application/json' \
          -d '{
            "model": "qwen3.7-plus",
            "input":{
              "messages":[
                {
                  "role": "user",
                  "content": [
                  {"video": "data:video/mp4;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA..."},
                  {"text": "这个视频描绘了什么场景？"}
                  ]
                }
              ]
            }
          }'
          ```
        </Tab>
      </Tabs>
    </Tab>
  </Tabs>
</Accordion>

<Accordion title="图像列表 - 通过文件路径传入（仅 DashScope）" defaultOpen>
  本示例使用本地保存的文件：[football1.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/spqrrx/football1.jpg)、[football2.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/vtnhyr/football2.jpg)、[football3.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/ykaoih/football3.jpg) 和 [football4.jpg](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250415/vkuupi/football4.jpg)。

  <Tabs>
    <Tab title="Python">
      ```python
      import os
      import dashscope

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      local_path1 = "football1.jpg"
      local_path2 = "football2.jpg"
      local_path3 = "football3.jpg"
      local_path4 = "football4.jpg"

      image_path1 = f"file://{local_path1}"
      image_path2 = f"file://{local_path2}"
      image_path3 = f"file://{local_path3}"
      image_path4 = f"file://{local_path4}"

      messages = [{'role':'user',
        'content': [{'video': [image_path1,image_path2,image_path3,image_path4],"fps":2},
        {'text': '这个视频描绘了什么场景？'}]}]
      response = dashscope.MultiModalConversation.call(
        api_key=os.getenv('DASHSCOPE_API_KEY'),
        model='qwen3.7-plus',
        messages=messages)

      print(response.output.choices[0].message.content[0]["text"])
      ```
    </Tab>

    <Tab title="Java">
      ```java
      // DashScope SDK 版本须为 2.21.10 或更高
      import java.util.Arrays;
      import java.util.Map;
      import java.util.HashMap;
      import java.util.Collections;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;

      public class Main {

        static {
          Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
        }

        private static final String MODEL_NAME = "qwen3.7-plus";
        public static void videoImageListSample(String localPath1, String localPath2, String localPath3, String localPath4)
            throws ApiException, NoApiKeyException, UploadFileException {
          MultiModalConversation conv = new MultiModalConversation();
          String filePath1 = "file://" + localPath1;
          String filePath2 = "file://" + localPath2;
          String filePath3 = "file://" + localPath3;
          String filePath4 = "file://" + localPath4;
          Map<String, Object> params = new HashMap<>();
          params.put("video", Arrays.asList(filePath1,filePath2,filePath3,filePath4));
          params.put("fps", 2);
          MultiModalMessage userMessage = MultiModalMessage.builder()
              .role(Role.USER.getValue())
              .content(Arrays.asList(params,
                  Collections.singletonMap("text", "描述这个视频的具体过程")))
              .build();
          MultiModalConversationParam param = MultiModalConversationParam.builder()
              .apiKey(System.getenv("DASHSCOPE_API_KEY"))
              .model(MODEL_NAME)
              .messages(Arrays.asList(userMessage)).build();
          MultiModalConversationResult result = conv.call(param);
          System.out.print(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
        }
        public static void main(String[] args) {
          try {
            videoImageListSample(
                "xxx/football1.jpg",
                "xxx/football2.jpg",
                "xxx/football3.jpg",
                "xxx/football4.jpg");
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
          System.exit(0);
        }
      }
      ```
    </Tab>
  </Tabs>
</Accordion>

<Accordion title="图像列表 - 通过 Base64 编码传入" defaultOpen>
  <Tabs>
    <Tab title="OpenAI 兼容">
      <Tabs>
        <Tab title="Python">
          ```python
          import os
          from openai import OpenAI
          import base64

          def encode_image(image_path):
            with open(image_path, "rb") as image_file:
              return base64.b64encode(image_file.read()).decode("utf-8")

          base64_image1 = encode_image("football1.jpg")
          base64_image2 = encode_image("football2.jpg")
          base64_image3 = encode_image("football3.jpg")
          base64_image4 = encode_image("football4.jpg")
          client = OpenAI(
            api_key=os.getenv("DASHSCOPE_API_KEY"),
            base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
          )
          completion = client.chat.completions.create(
            model="qwen3.7-plus",
            messages=[
            {"role": "user","content": [
              {"type": "video","video": [
                f"data:image/jpeg;base64,{base64_image1}",
                f"data:image/jpeg;base64,{base64_image2}",
                f"data:image/jpeg;base64,{base64_image3}",
                f"data:image/jpeg;base64,{base64_image4}",]},
              {"type": "text","text": "描述这个视频的具体过程"},
            ]}]
          )
          print(completion.choices[0].message.content)
          ```
        </Tab>

        <Tab title="Node.js">
          ```javascript
          import OpenAI from "openai";
          import { readFileSync } from 'fs';

          const openai = new OpenAI(
              {
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
              }
          );

          const encodeImage = (imagePath) => {
              const imageFile = readFileSync(imagePath);
              return imageFile.toString('base64');
            };

          const base64Image1 = encodeImage("football1.jpg")
          const base64Image2 = encodeImage("football2.jpg")
          const base64Image3 = encodeImage("football3.jpg")
          const base64Image4 = encodeImage("football4.jpg")
          async function main() {
              const completion = await openai.chat.completions.create({
              model: "qwen3.7-plus",
              messages: [
              {"role": "user",
              "content": [{"type": "video",
              "video": [
              `data:image/jpeg;base64,${base64Image1}`,
              `data:image/jpeg;base64,${base64Image2}`,
              `data:image/jpeg;base64,${base64Image3}`,
              `data:image/jpeg;base64,${base64Image4}`]},
              {"type": "text", "text": "这个视频描绘了什么场景？"}]}]
              });
              console.log(completion.choices[0].message.content);
          }

          main();
          ```
        </Tab>

        <Tab title="curl">
          - 为便于展示，代码中的 Base64 编码字符串已截断，实际调用时必须传入完整的编码字符串。

          ```bash
          curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
          -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
          -H 'Content-Type: application/json' \
          -d '{
            "model": "qwen3.7-plus",
            "messages": [{"role": "user",
            "content": [{"type": "video",
            "video": [
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA...",
            "data:image/jpeg;base64,nEpp6jpnP57MoWSyOWwrkXMJhHRCWYeFYb...",
            "data:image/jpeg;base64,JHWQnJPc40GwQ7zERAtRMK6iIhnWw4080s...",
            "data:image/jpeg;base64,adB6QOU5HP7dAYBBOg/Fb7KIptlbyEOu58..."
            ]},
            {"type": "text",
            "text": "描述这个视频的具体过程"}]}]
          }'
          ```
        </Tab>
      </Tabs>
    </Tab>

    <Tab title="DashScope">
      <Tabs>
        <Tab title="Python">
          ```python
          import base64
          import os
          import dashscope

          dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

          def encode_image(image_path):
            with open(image_path, "rb") as image_file:
              return base64.b64encode(image_file.read()).decode("utf-8")

          base64_image1 = encode_image("football1.jpg")
          base64_image2 = encode_image("football2.jpg")
          base64_image3 = encode_image("football3.jpg")
          base64_image4 = encode_image("football4.jpg")

          messages = [{'role':'user',
                'content': [
                {'video':
                [f"data:image/jpeg;base64,{base64_image1}",
                f"data:image/jpeg;base64,{base64_image2}",
                f"data:image/jpeg;base64,{base64_image3}",
                f"data:image/jpeg;base64,{base64_image4}"],
                "fps":2},
                {'text': '描述这个视频的具体过程'}]}]

          response = dashscope.MultiModalConversation.call(
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            model='qwen3.7-plus',
            messages=messages)

          print(response.output.choices[0].message.content[0]["text"])
          ```
        </Tab>

        <Tab title="Java">
          ```java
          // DashScope SDK 版本须为 2.21.10 或更高
          import java.util.*;
          import java.io.IOException;
          import java.nio.file.Files;
          import java.nio.file.Path;
          import java.nio.file.Paths;

          import com.alibaba.dashscope.aigc.multimodalconversation.*;
          import com.alibaba.dashscope.common.MultiModalMessage;
          import com.alibaba.dashscope.common.Role;
          import com.alibaba.dashscope.exception.ApiException;
          import com.alibaba.dashscope.exception.NoApiKeyException;
          import com.alibaba.dashscope.exception.UploadFileException;
          import com.alibaba.dashscope.utils.Constants;

          public class Main {
            static {
              Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
            }

            private static String encodeImageToBase64(String imagePath) throws IOException {
              Path path = Paths.get(imagePath);
              byte[] imageBytes = Files.readAllBytes(path);
              return Base64.getEncoder().encodeToString(imageBytes);
            }

            public static void simpleMultiModalConversationCall()
                throws ApiException, NoApiKeyException, UploadFileException, IOException {
              String base64Image1 = encodeImageToBase64("football1.jpg");
              String base64Image2 = encodeImageToBase64("football2.jpg");
              String base64Image3 = encodeImageToBase64("football3.jpg");
              String base64Image4 = encodeImageToBase64("football4.jpg");

              MultiModalConversation conv = new MultiModalConversation();
              Map<String, Object> params = new HashMap<>();
              params.put("video", Arrays.asList(
                "data:image/jpeg;base64," + base64Image1,
                "data:image/jpeg;base64," + base64Image2,
                "data:image/jpeg;base64," + base64Image3,
                "data:image/jpeg;base64," + base64Image4));
              params.put("fps", 2);
              MultiModalMessage userMessage = MultiModalMessage.builder()
                  .role(Role.USER.getValue())
                  .content(Arrays.asList(params,
                  Collections.singletonMap("text", "描述这个视频的具体过程")))
                  .build();
              MultiModalConversationParam param = MultiModalConversationParam.builder()
                  .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                  .model("qwen3.7-plus")
                  .messages(Arrays.asList(userMessage)).build();
              MultiModalConversationResult result = conv.call(param);
              System.out.print(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
            }
            public static void main(String[] args) {
              try {
                simpleMultiModalConversationCall();
              } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
                System.out.println(e.getMessage());
              }
              System.exit(0);
            }
          }
          ```
        </Tab>

        <Tab title="curl">
          - 为便于展示，代码中的 Base64 编码字符串已截断，实际调用时必须传入完整的编码字符串。

          ```bash
          curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
          -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
          -H 'Content-Type: application/json' \
          -d '{
            "model": "qwen3.7-plus",
            "input":{
              "messages":[
                {
                  "role": "user",
                  "content": [
                  {"video": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAA...",
                  "data:image/jpeg;base64,nEpp6jpnP57MoWSyOWwrkXMJhHRCWYeFYb...",
                  "data:image/jpeg;base64,JHWQnJPc40GwQ7zERAtRMK6iIhnWw4080s...",
                  "data:image/jpeg;base64,adB6QOU5HP7dAYBBOg/Fb7KIptlbyEOu58..."],
                  "fps":2},
                  {"text": "这个视频描绘了什么场景？"}
                  ]
                }
              ]
            }
          }'
          ```
        </Tab>
      </Tabs>
    </Tab>
  </Tabs>
</Accordion>

### 处理高分辨率图像

视觉理解模型 API 对单张图像编码后的视觉 token 数有上限。默认配置下，高分辨率图像会被压缩，可能导致细节丢失，影响理解准确度。启用 `vl_high_resolution_images` 或调整 `max_pixels` 可以增加视觉 token 数，从而保留更多图像细节，提升理解效果。

<Accordion title="查看各模型的每视觉 token 像素数、token 上限及像素上限" defaultOpen>
  <Note>
    如果输入图像的像素数超过模型的像素上限，图像将被缩小至上限以内。
  </Note>

| **模型**                                                                                                                     | **每 token 像素数** | **vl\_high\_resolution\_images** | **max\_pixels**                      | **token 上限**                            | **像素上限**                    |
| -------------------------------------------------------------------------------------------------------------------------- | --------------- | -------------------------------- | ------------------------------------ | --------------------------------------- | --------------------------- |
| `Qwen3.5` 和 `Qwen3-VL` 系列模型                                                                                                | `32*32`         | `true`                           | `max_pixels` 无效                      | `16384 tokens`                          | `16777216`（即 `16384*32*32`） |
| `Qwen3.5` 和 `Qwen3-VL` 系列模型                                                                                                | `32*32`         | `false`（默认）                      | 可自定义，默认值为 `2621440`，最大值为 `16777216`。 | 由 `max_pixels` 决定，即 `max_pixels/32/32`。 | `max_pixels`                |
| `qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-2025-08-13`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-08-15` | `32*32`         | `true`                           | `max_pixels` 无效                      | `16384 tokens`                          | `16777216`（即 `16384*32*32`） |
| 上述相同的 Qwen2.5-VL 模型                                                                                                        | `32*32`         | `false`（默认）                      | 可自定义，默认值为 `2621440`，最大值为 `16777216`。 | 由 `max_pixels` 决定，即 `max_pixels/32/32`。 | `max_pixels`                |
| `QVQ` 及其他 `Qwen2.5-VL` 模型                                                                                                  | `28*28`         | 不支持                              | 可自定义，默认值为 `1003520`，最大值为 `12845056`。 | 由 `max_pixels` 决定，即 `max_pixels/28/28`。 | `max_pixels`                |
</Accordion>

<Tabs>
  <Tab title="OpenAI 兼容">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import time
        from openai import OpenAI

        client = OpenAI(
          api_key=os.getenv("DASHSCOPE_API_KEY"),
          base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        )

        completion = client.chat.completions.create(
          model="qwen3.7-plus",
          messages=[
            {"role": "user","content": [
              {"type": "image_url","image_url": {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"},
              # max_pixels 表示输入图像的最大像素阈值。当 vl_high_resolution_images=True 时该参数无效，为 False 时可自定义，最大值因模型而异。
              # "max_pixels": 16384 * 32 * 32
              },
              {"type": "text", "text": "这张图片展现了什么节日氛围？"},
              ],
            }
          ],
          extra_body={"vl_high_resolution_images":True}

        )
        print(f"模型输出：{completion.choices[0].message.content}")
        print(f"输入 token 总数：{completion.usage.prompt_tokens}")
        ```
      </Tab>

      <Tab title="Node.js">
        ```javascript
        import OpenAI from "openai";

        const openai = new OpenAI(
          {
            apiKey: process.env.DASHSCOPE_API_KEY,
            baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1"
          }
        );

        const response = await openai.chat.completions.create({
            model: "qwen3.7-plus",
            messages: [
            {role: "user",content: [
              {type: "image_url",
              image_url: {"url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"},
              // max_pixels 表示输入图像的最大像素阈值。当 vl_high_resolution_images=True 时该参数无效，为 False 时可自定义，最大值因模型而异。
              // "max_pixels": 2560 * 32 * 32
              },
              {type: "text", text: "这张图片展现了什么节日氛围？" },
            ]}],
            vl_high_resolution_images:true
          })

        console.log("模型输出：",response.choices[0].message.content);
        console.log("输入 token 总数",response.usage.prompt_tokens);
        ```
      </Tab>

      <Tab title="curl">
        ```bash
        curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H 'Content-Type: application/json' \
        -d '{
          "model": "qwen3.7-plus",
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "type": "image_url",
                  "image_url": {
                    "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"
                  }
                },
                {
                  "type": "text",
                  "text": "这张图片展现了什么节日氛围？"
                }
              ]
            }
          ],
          "vl_high_resolution_images":true
        }'
        ```
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="DashScope">
    <Tabs>
      <Tab title="Python">
        ```python
        import os
        import time

        import dashscope

        dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

        messages = [
          {
            "role": "user",
            "content": [
              {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg",
              # max_pixels 表示输入图像的最大像素阈值。当 vl_high_resolution_images=True 时该参数无效，为 False 时可自定义，最大值因模型而异。
              # "max_pixels": 16384 * 32 * 32
              },
              {"text": "这张图片展现了什么节日氛围？"}
            ]
          }
        ]

        response = dashscope.MultiModalConversation.call(
            api_key=os.getenv('DASHSCOPE_API_KEY'),
            model='qwen3.7-plus',
            messages=messages,
            vl_high_resolution_images=True
          )

        print("模型输出",response.output.choices[0].message.content[0]["text"])
        print("输入 token 总数：",response.usage.input_tokens)
        ```
      </Tab>

      <Tab title="Java">
        ```java
        import java.util.Arrays;
        import java.util.Collections;
        import java.util.Map;
        import java.util.HashMap;
        import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
        import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
        import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
        import com.alibaba.dashscope.common.MultiModalMessage;
        import com.alibaba.dashscope.common.Role;
        import com.alibaba.dashscope.exception.ApiException;
        import com.alibaba.dashscope.exception.NoApiKeyException;
        import com.alibaba.dashscope.exception.UploadFileException;
        import com.alibaba.dashscope.utils.Constants;

        public class Main {

          static {
            Constants.baseHttpApiUrl="https://dashscope.aliyuncs.com/api/v1";
          }

          public static void simpleMultiModalConversationCall()
              throws ApiException, NoApiKeyException, UploadFileException {
            MultiModalConversation conv = new MultiModalConversation();
            Map<String, Object> map = new HashMap<>();
            map.put("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg");
            // max_pixels 表示输入图像的最大像素阈值。当 vl_high_resolution_images=True 时该参数无效，为 False 时可自定义，最大值因模型而异。
            // map.put("max_pixels", 2621440);
            MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                map,
                Collections.singletonMap("text", "这张图片展现了什么节日氛围？"))).build();
            MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                .model("qwen3.7-plus")
                .message(userMessage)
                .vlHighResolutionImages(true)
                .build();
            MultiModalConversationResult result = conv.call(param);
            System.out.println(result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
            System.out.println(result.getUsage().getInputTokens());
          }

          public static void main(String[] args) {
            try {
              simpleMultiModalConversationCall();
            } catch (ApiException | NoApiKeyException | UploadFileException e) {
              System.out.println(e.getMessage());
            }
            System.exit(0);
          }
        }
        ```
      </Tab>

      <Tab title="curl">
        ```bash
        curl -X POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation \
        -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
        -H 'Content-Type: application/json' \
        -d '{
          "model": "qwen3.7-plus",
          "input":{
            "messages":[
              {
                "role": "user",
                "content": [
                {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250212/earbrt/vcg_VCG211286867973_RF.jpg"},
                {"text": "这张图片展现了什么节日氛围？"}
                ]
              }
            ]
          },
          "parameters": {
            "vl_high_resolution_images": true
          }
        }'
        ```
      </Tab>
    </Tabs>
  </Tab>
</Tabs>

### 高级功能

- [多轮对话](/developer-guides/run-and-scale/multi-turn)
- [流式输出](/developer-guides/run-and-scale/streaming)

## 限制

### 输入文件限制

<Tabs>
  <Tab title="图像限制">
    - **图像分辨率**：
      - 最小尺寸：图像的宽和高均须大于 `10` 像素。
      - 宽高比：图像长边与短边之比不得超过 `200:1`。
      - 像素上限：
        - 建议将图像分辨率控制在 `8K（7680x4320）` 以内。超出此分辨率的图像因文件较大、网络传输时间较长，可能导致 API 调用超时。
        - 自动缩放：模型可通过 `max_pixels` 和 `min_pixels` 调整图像尺寸。因此，超高分辨率图像不会提升识别准确度，反而会增加调用失败的风险。建议提前在客户端将图像缩放至合理尺寸。

    - **支持的图像格式**
      - 分辨率低于 `4K（3840x2160）` 时，支持以下图像格式：

| **图像格式** | **常见扩展名**         | **MIME 类型** |
| -------- | ----------------- | ----------- |
| BMP      | .bmp              | image/bmp   |
| JPEG     | .jpe, .jpeg, .jpg | image/jpeg  |
| PNG      | .png              | image/png   |
| TIFF     | .tif, .tiff       | image/tiff  |
| WEBP     | .webp             | image/webp  |
| HEIC     | .heic             | image/heic  |

      - 分辨率在 `4K（3840x2160）` 至 `8K（7680x4320）` 之间时，仅支持 JPEG、JPG 和 PNG 格式。

    - **图像大小：**
      - 以公网URL传入时：Qwen3.8系列、Qwen3.7系列、Qwen3.6系列、Qwen3.5系列、Qwen3-VL系列单个图像不超过 `20MB`，其他模型单个图像不超过`10MB`
      - 以本地路径传入时：单个图像不超过`10MB`
      - 以 Base64 编码传入时（OpenAI 兼容接口或DashScope）：Qwen3.8系列、Qwen3.7系列、Qwen3.6系列、Qwen3.5、Qwen3-VL系列编码前的原始图像文件不超过 `20MB`，其他模型不超过`10MB`；且编码后的 Data URI 字符串不超过 `20MB`。
      - 以 Base64 编码传入时（Anthropic 兼容接口）：受**请求体整体不超过** `6MB` 的限制，**多张图像**时需共享此额度。
      - 关于如何压缩文件大小，请参见[如何将图像或视频压缩至所需大小](#常见问题)。

    - **支持的图像数量**：
      - 以公网URL或本地路径传入时：
        - Qwen3.8-Max、Qwen3.7-Plus：最多 2048 张
        - Qwen3.7-Flash、Qwen3.6-Plus、Qwen3.6-Flash、Qwen3.5-Plus、Qwen3.5-Flash、Qwen3-VL、Qwen-VL、QVQ系列：最多 256 张
      - 以 Base64 编码传入时：最多 250 张
  </Tab>

  <Tab title="视频限制">
    - **以图像列表形式传入时，列表中图像数量限制如下**：
      - `qwen3.5` 系列：最少 4 张，最多 8,000 张。
      - `qwen3-vl-plus` 系列、`qwen3-vl-flash` 系列、`qwen3-vl-235b-a22b-thinking` 和 `qwen3-vl-235b-a22b-instruct`：最少 4 张，最多 2,000 张。
      - 其他 `Qwen3-VL` 开源版本、`Qwen2.5-VL`（含商业版和开源版）及 `QVQ` 系列模型：最少 4 张，最多 512 张。
      - 其他模型：最少 4 张，最多 80 张。
    - **以视频文件形式传入时**：
      - **视频大小**：

        - 通过公开 URL 传入时：
          - `qwen3.5` 系列、`Qwen3-VL` 系列和 `qwen-vl-max`（含 `qwen-vl-max-latest`、`qwen-vl-max-2025-04-08` 及所有后续版本）：不超过 2 GB。
          - `qwen-vl-plus` 系列、其他 `qwen-vl-max` 模型、`Qwen2.5-VL` 开源系列和 `QVQ` 系列模型：不超过 1 GB。
          - 其他模型：不超过 150 MB。
        - 通过 Base64 编码字符串传入时：编码字符串须小于 10 MB。
        - 通过本地文件路径传入时：视频文件不超过 100 MB。

        关于如何压缩文件大小，请参见[如何将图像或视频压缩至所需大小](#常见问题)。
      - **视频时长**：
        - `qwen3.5` 系列：2 秒至 2 小时。
        - `qwen3-vl-plus` 系列、`qwen3-vl-flash` 系列、`qwen3-vl-235b-a22b-thinking` 和 `qwen3-vl-235b-a22b-instruct`：2 秒至 1 小时。
        - 其他 `Qwen3-VL` 开源系列和 `qwen-vl-max`（含 `qwen-vl-max-latest`、`qwen-vl-max-2025-04-08` 及后续版本）：2 秒至 20 分钟。
        - `qwen-vl-plus` 系列、其他 `qwen-vl-max` 模型、`Qwen2.5-VL` 开源系列和 `QVQ` 系列模型：2 秒至 10 分钟。
        - 其他模型：2 秒至 40 秒。
      - **视频格式**： MP4、AVI、MKV、MOV、FLV、WMV 等。
      - **视频分辨率**： 无特定限制。模型可通过 `max_pixels` 和 `min_pixels` 自动调整视频分辨率，视频文件越大并不意味着理解效果越好。
      - **视频数量**： 无论使用**公开 URL**、**Base64 编码**字符串还是**本地文件路径**，每次请求最多传入 **64** 个视频。除数量上限外，**所有**视频和**所有**文本的 token 总数必须**小于**模型的最大输入长度。
      - **音频理解**： 模型不支持理解视频文件中的音频内容。
  </Tab>
</Tabs>

### 文件传入方式

- **公共 URL**：提供支持 HTTP 或 HTTPS 协议的可公开访问的文件地址。为获得最佳稳定性和性能，建议将文件上传至 OSS 并获取公共 URL。

<Warning>
  为确保模型能够成功下载文件，公共 URL 的请求头中**必须**包含 Content-Length（文件大小）和 Content-Type（媒体类型，例如 image/jpeg）。如果任一字段缺失或不正确，文件下载将失败。
</Warning>

- **以 Base64 编码字符串传入**： 将文件转换为 Base64 编码字符串后传入。
- **以本地文件路径传入（仅 DashScope SDK）**： 传入本地文件的路径。

<Note>
  关于文件传入方式的选择建议，请参见[如何选择文件上传方式？](#常见问题)
</Note>

## 投入生产

- **图像/视频预处理**： 视觉理解模型对输入文件的大小有限制。有关如何压缩文件的详细信息，请参见[图像或视频压缩方法](#常见问题)。
- **处理文本文件**： 视觉理解模型仅支持处理图像格式的文件，无法直接处理文本文件。请将文本文件转换为图像格式。建议使用图像处理库（例如 `Python` 的 `pdf2image`）将文件逐页转换为多张高质量图像，然后通过[多图像输入](#使用多张图像)方式传入模型。
- **容错与稳定性**
  - 超时处理：在非流式调用中，如果模型在 180 秒内未完成输出，通常会触发超时错误。为提升用户体验，超时后响应体会返回已生成的内容。如果响应头包含 `x-dashscope-partialresponse:true`，则表示该响应触发了超时。您可以使用[续写模式](/developer-guides/text-generation/partial-mode)功能（部分模型支持），将已生成的内容添加到 messages 数组后重新发送请求，让大模型继续生成。详情请参见[基于未完成输出继续生成](/developer-guides/text-generation/partial-mode)。
  - 重试机制：设计合理的 API 调用重试逻辑（例如指数退避），以应对网络抖动或服务临时不可用的情况。

## 计费规则

- **计费**： 总费用基于输入和输出的 token 总数。关于输入和输出价格，请参见[模型市场](https://www.qianwenai.com/models)。
  - **Token 构成**： 输入 token 由文本 token 和由图像或视频转换而来的 token 组成。输出 token 为模型生成的文本。在思考模式下，模型的思考过程也计入输出 token。如果思考过程不作为输出，则按非思考模式的价格计费。
  - **计算图像和视频的 token 数**： 使用以下代码估算图像或视频的 token 消耗量。该估算仅供参考，实际用量以 API 响应为准。

<Accordion title="计算图像和视频的 token 数" defaultOpen>
  <Tabs>
    <Tab title="图像">
      公式：`图像 Token 数 = h_bar * w_bar / token_pixels + 2`

      - `h_bar, w_bar`：缩放后图像的高度和宽度。在处理图像之前，模型会将其缩放至特定的像素上限。像素上限取决于 `max_pixels` 和 `vl_high_resolution_images` 参数的值。详情请参见[处理高分辨率图像](#处理高分辨率图像)。
      - `token_pixels`：每个视觉 `token` 对应的像素值。该值因模型而异：
        - `Qwen3.5`、`Qwen3-VL`、`qwen-vl-max`、`qwen-vl-max-latest`、`qwen-vl-max-2025-08-13`、`qwen-vl-plus`、`qwen-vl-plus-latest`、`qwen-vl-plus-2025-08-15`：每个 `token` 对应 `32x32` 像素。
        - `QVQ` 及其他 `Qwen2.5-VL` 模型：每个 token 对应 `28x28` 像素。

      以下代码展示了模型内部大致的图像缩放逻辑，可用于估算图像的 token 数。实际计费以 API 响应为准。

      ```python
      import math
      # 使用以下命令安装 Pillow 库：pip install Pillow
      from PIL import Image

      def token_calculate(image_path, max_pixels, vl_high_resolution_images):
        # 打开指定的图像文件。
        image = Image.open(image_path)

        # 获取图像的原始尺寸。
        height = image.height
        width = image.width

        # 将宽度和高度调整为 32 或 28 的倍数（取决于模型）。
        h_bar = round(height / 32) * 32
        w_bar = round(width / 32) * 32

        # 图像 token 数的下限：4 个 token。
        min_pixels = 4 * 32 * 32
        # 如果 vl_high_resolution_images 设为 True，输入图像 token 数的上限为 16,386，对应的最大像素值为 16384 * 32 * 32 或 16384 * 28 * 28；否则使用 max_pixels 设定的值。
        if vl_high_resolution_images:
          max_pixels = 16384 * 32 * 32
        else:
          max_pixels = max_pixels

        # 对图像进行缩放，使总像素数处于 [min_pixels, max_pixels] 范围内。
        if h_bar * w_bar > max_pixels:
          beta = math.sqrt((height * width) / max_pixels)
          h_bar = math.floor(height / beta / 32) * 32
          w_bar = math.floor(width / beta / 32) * 32
        elif h_bar * w_bar < min_pixels:
          beta = math.sqrt(min_pixels / (height * width))
          h_bar = math.ceil(height * beta / 32) * 32
          w_bar = math.ceil(width * beta / 32) * 32
        return h_bar, w_bar

      if __name__ == "__main__":
        # 将 xxx/test.jpg 替换为您本地图像的路径。
        h_bar, w_bar =  token_calculate("xxx/test.jpg", max_pixels=16384*32*32, vl_high_resolution_images=False)
        print(f"缩放后图像尺寸：高 {h_bar}，宽 {w_bar}")
        # 系统会自动添加 <vision_bos> 和 <vision_eos> 视觉标记（各 1 个 token）。
        token = int((h_bar * w_bar) / (32 * 32))+2
        print(f"图像的 token 数：{token}")
      ```
    </Tab>

    <Tab title="视频">
      - **视频文件**：

      当模型处理视频文件时，会先提取视频帧，再计算所有帧的 token 总数。您可以使用以下代码，通过提供视频路径来估算视频消耗的 token 总数：

      ```python
      # 使用前请安装：pip install opencv-python
      import math
      import os
      import logging
      import cv2

      logger = logging.getLogger(__name__)

      FRAME_FACTOR = 2
      IMAGE_FACTOR = 32
      MAX_RATIO = 200
      VIDEO_MIN_PIXELS = 4 * 32 * 32
      VIDEO_MAX_PIXELS = 640 * 32 * 32
      FPS = 2.0
      FPS_MIN_FRAMES = 4
      FPS_MAX_FRAMES = 2000
      VIDEO_TOTAL_PIXELS = int(float(os.environ.get('VIDEO_MAX_PIXELS', 131072 * 32 * 32)))

      def round_by_factor(number: int, factor: int) -> int:
        return round(number / factor) * factor

      def ceil_by_factor(number: int, factor: int) -> int:
        return math.ceil(number / factor) * factor

      def floor_by_factor(number: int, factor: int) -> int:
        return math.floor(number / factor) * factor

      def extract_vision_info(conversations):
        vision_infos = []
        if isinstance(conversations[0], dict):
          conversations = [conversations]
        for conversation in conversations:
          for message in conversation:
            if isinstance(message["content"], list):
              for ele in message["content"]:
                if (
                  "image" in ele
                  or "image_url" in ele
                  or "video" in ele
                  or ele.get("type","") in ("image", "image_url", "video")
                ):
                  vision_infos.append(ele)
        return vision_infos

      def smart_nframes(ele,total_frames,video_fps):
        assert not ("fps" in ele and "nframes" in ele), "Only accept either `fps` or `nframes`"
        fps = ele.get("fps", FPS)
        min_frames = ceil_by_factor(ele.get("min_frames", FPS_MIN_FRAMES), FRAME_FACTOR)
        max_frames = floor_by_factor(ele.get("max_frames", min(FPS_MAX_FRAMES, total_frames)), FRAME_FACTOR)
        duration = total_frames / video_fps if video_fps != 0 else 0
        if duration-int(duration)>(1/fps):
          total_frames = math.ceil(duration * video_fps)
        else:
          total_frames = math.ceil(int(duration)*video_fps)
        nframes = total_frames / video_fps * fps
        if nframes > total_frames:
          logger.warning(f"smart_nframes: nframes[{nframes}] > total_frames[{total_frames}]")
        nframes = int(min(min(max(nframes, min_frames), max_frames), total_frames))
        if not (FRAME_FACTOR <= nframes and nframes <= total_frames):
          raise ValueError(f"nframes should in interval [{FRAME_FACTOR}, {total_frames}], but got {nframes}.")
        return nframes

      def get_video(video_path):
        cap = cv2.VideoCapture(video_path)
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        return frame_height, frame_width, total_frames, video_fps

      def smart_resize(ele, path, factor=IMAGE_FACTOR):
        height, width, total_frames, video_fps = get_video(path)
        min_pixels = VIDEO_MIN_PIXELS
        total_pixels = VIDEO_TOTAL_PIXELS
        nframes = smart_nframes(ele, total_frames, video_fps)
        max_pixels = max(min(VIDEO_MAX_PIXELS, total_pixels / nframes * FRAME_FACTOR),int(min_pixels * 1.05))

        if max(height, width) / min(height, width) > MAX_RATIO:
          raise ValueError(
            f"absolute aspect ratio must be smaller than {MAX_RATIO}, got {max(height, width) / min(height, width)}"
          )

        h_bar = max(factor, round_by_factor(height, factor))
        w_bar = max(factor, round_by_factor(width, factor))
        if h_bar * w_bar > max_pixels:
          beta = math.sqrt((height * width) / max_pixels)
          h_bar = floor_by_factor(height / beta, factor)
          w_bar = floor_by_factor(width / beta, factor)
        elif h_bar * w_bar < min_pixels:
          beta = math.sqrt(min_pixels / (height * width))
          h_bar = ceil_by_factor(height * beta, factor)
          w_bar = ceil_by_factor(width * beta, factor)
        return h_bar, w_bar

      def token_calculate(video_path, fps):
        messages = [{"content": [{"video": video_path, "fps": fps}]}]
        vision_infos = extract_vision_info(messages)[0]
        resized_height, resized_width = smart_resize(vision_infos, video_path)
        height, width, total_frames, video_fps = get_video(video_path)
        num_frames = smart_nframes(vision_infos, total_frames, video_fps)
        print(f"原始视频尺寸：{height}*{width}，模型输入尺寸：{resized_height}*{resized_width}，视频总帧数：{total_frames}，fps 为 {fps} 时提取的总帧数：{num_frames}", end=", ")
        video_token = int(math.ceil(num_frames / 2) * resized_height / 32 * resized_width / 32)
        video_token += 2
        return video_token

      video_token = token_calculate("xxx/test.mp4", 1)
      print("视频 token 数：", video_token)
      ```

      - **图像列表**：

      如果您以图像列表的形式传入视频，请使用以下代码计算消耗的 token 数：

      ```python
      # 使用前请安装：pip install Pillow
      import math
      import os
      import logging
      from typing import Tuple
      from PIL import Image

      logger = logging.getLogger(__name__)

      FRAME_FACTOR = 2
      IMAGE_FACTOR = 32
      TOKEN_DIVISOR = 32
      VISION_SPECIAL_TOKENS = 2
      MAX_RATIO = 200
      VIDEO_MIN_PIXELS = 4 * 32 * 32
      VIDEO_MAX_PIXELS = 640 * 32 * 32
      VIDEO_TOTAL_PIXELS = int(float(os.environ.get('VIDEO_MAX_PIXELS', 131072 * 32 * 32)))

      def round_by_factor(number: int, factor: int) -> int:
        return round(number / factor) * factor

      def ceil_by_factor(number: int, factor: int) -> int:
        return math.ceil(number / factor) * factor

      def floor_by_factor(number: int, factor: int) -> int:
        return math.floor(number / factor) * factor

      def get_image_size(image_path: str) -> Tuple[int, int]:
        if not os.path.exists(image_path):
          raise FileNotFoundError(f"图像文件未找到：{image_path}")
        try:
          image = Image.open(image_path)
          height = image.height
          width = image.width
          image.close()
          return height, width
        except Exception as e:
          raise ValueError(f"无法读取图像文件 {image_path}：{str(e)}")

      def smart_resize(height: int, width: int, nframes: int, factor: int = IMAGE_FACTOR) -> Tuple[int, int]:
        min_pixels = VIDEO_MIN_PIXELS
        total_pixels = VIDEO_TOTAL_PIXELS
        max_pixels = max(min(VIDEO_MAX_PIXELS, total_pixels / nframes * FRAME_FACTOR), int(min_pixels * 1.05))

        aspect_ratio = max(height, width) / min(height, width)
        if aspect_ratio > MAX_RATIO:
          raise ValueError(
            f"图像的宽高比必须小于 {MAX_RATIO}:1。当前比例为 {aspect_ratio:.2f}:1。"
          )

        h_bar = max(factor, round_by_factor(height, factor))
        w_bar = max(factor, round_by_factor(width, factor))
        if h_bar * w_bar > max_pixels:
          beta = math.sqrt((height * width) / max_pixels)
          h_bar = floor_by_factor(height / beta, factor)
          w_bar = floor_by_factor(width / beta, factor)
        elif h_bar * w_bar < min_pixels:
          beta = math.sqrt(min_pixels / (height * width))
          h_bar = ceil_by_factor(height * beta, factor)
          w_bar = ceil_by_factor(width * beta, factor)
        return h_bar, w_bar

      def calculate_video_tokens(image_path: str, nframes: int = 1, factor: int = IMAGE_FACTOR, verbose: bool = True) -> int:
        height, width = get_image_size(image_path)
        resized_height, resized_width = smart_resize(height, width, nframes, factor)
        video_token = int(
          math.ceil(nframes / 2) *
          (resized_height / TOKEN_DIVISOR) *
          (resized_width / TOKEN_DIVISOR)
        )
        video_token += VISION_SPECIAL_TOKENS
        if verbose:
          print(f"原始视频帧尺寸：{height}x{width}，模型输入尺寸：{resized_height}x{resized_width}，", end="")
        return video_token

      if __name__ == "__main__":
        try:
          video_token = calculate_video_tokens("xxx/test.jpg", nframes=30)
          print(f"视频 token 数：{video_token}\n")
        except Exception as e:
          print(f"错误：{str(e)}\n")
      ```
    </Tab>
  </Tabs>
</Accordion>

- **查看账单**： 在[账单页面](https://platform.qianwenai.com/home/billing/overview)查看账单或充值。

## 参考

关于视觉理解模型的输入和输出参数，请参见 [Chat API](/api-reference/chat/openai-chat)。

## 常见问题

<Accordion title="如何选择文件上传方式？" defaultOpen>
  根据 SDK 类型、文件大小和网络稳定性选择最合适的上传方式。

| **类型** | **规格**             | **DashScope SDK（Python、Java）** | **OpenAI 兼容 / DashScope HTTP** |
| ------ | ------------------ | ------------------------------ | ------------------------------ |
| 图像     | 大于 7 MB 且小于 10 MB  | 传入本地路径                         | 仅支持公共 URL，建议使用对象存储服务。          |
| 图像     | 小于 7 MB            | 传入本地路径                         | Base64 编码                      |
| 视频     | 大于 100 MB          | 仅支持公共 URL，建议使用对象存储服务。          | 仅支持公共 URL，建议使用对象存储服务。          |
| 视频     | 大于 7 MB 且小于 100 MB | 传入本地路径                         | 仅支持公共 URL，建议使用对象存储服务。          |
| 视频     | 小于 7 MB            | 传入本地路径                         | Base64 编码                      |

  <Note>
    Base64 编码会增加数据大小，因此原始文件必须小于 7 MB。使用 Base64 或本地路径可避免服务端下载超时，提升稳定性。
  </Note>
</Accordion>

<Accordion title="如何将图像或视频压缩至所需大小？" defaultOpen>
  视觉理解模型对输入文件的大小有限制，请使用以下方法压缩文件。

  **图像压缩方法**

  - 在线工具：使用 [CompressJPEG](https://compressjpeg.com/) 或 [TinyPng](https://free.tinypng.site/) 等在线工具。
  - 本地软件：使用 Photoshop 等软件在导出时调整质量。
  - 代码实现：

  ```python
  # pip install pillow

  from PIL import Image
  def compress_image(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
      img.save(output_path, "JPEG", optimize=True, quality=quality)

  # 传入本地图像
  compress_image("/xxx/before-large.jpeg","/xxx/after-min.jpeg")
  ```

  **视频压缩方法**

  - 在线工具：使用 [FreeConvert](https://www.freeconvert.com) 等在线工具。
  - 本地软件：使用 [HandBrake](https://handbrake.fr/) 等软件。
  - 代码实现：使用 FFmpeg 工具。详情请参见 [FFmpeg 官网](https://ffmpeg.org/download.html)。

  ```bash
  # 基本转换命令
  # -i：输入文件路径
  # -vcodec：视频编码器（推荐 libx264）
  # -crf：控制视频质量，取值范围 [18-28]，值越小质量越高
  # --preset：控制编码速度与压缩率，常用值：slow、fast、faster
  # -y：覆盖已有文件

  ffmpeg -i input.mp4 -vcodec libx264 -crf 28 -preset slow output.mp4
  ```
</Accordion>

<Accordion title="模型输出目标定位结果后，如何在原图上绘制边界框？" defaultOpen>
  视觉理解模型输出目标定位结果后，使用以下代码在原图上绘制边界框及其标签。

  - Qwen2.5-VL：以像素绝对值返回坐标，坐标相对于缩放图像的左上角。绘制边界框的代码请参见 [qwen2\_5\_vl\_2d.py](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251103/bgyust/qwen2_5-vl-2d.py)。
  - Qwen3-VL：返回归一化到 `[0, 999]` 范围内的相对坐标。绘制边界框的代码请参见 [qwen3\_vl\_2d.py](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251103/wpucdo/qwen3-vl-2d.py)（2D 定位）或 [qwen3\_vl\_3d.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20251103/mjjrka/qwen3_vl_3d.zip)（3D 定位）。
</Accordion>

## 错误码

如果调用失败，请参见[错误信息](/api-reference/preparation/error-messages)。
