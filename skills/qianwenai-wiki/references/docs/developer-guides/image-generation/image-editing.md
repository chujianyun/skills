> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像编辑

> 通过文本指令修改图片

## 快速开始

以下示例展示如何使用 `qwen-image-3.0-pro`，根据三张输入图片和一段提示词生成两张编辑后的图片。

<Note>
  输入提示词：图 1 中的女孩穿上图 2 中的黑色连衣裙，摆出图 3 中的坐姿。
</Note>

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "20%", paddingBottom: "8px"}}>**输入图片 1**</th>
      <th style={{textAlign: "left", width: "22%", paddingBottom: "8px"}}>**输入图片 2**</th>
      <th style={{textAlign: "left", width: "20%", paddingBottom: "8px"}}>**输入图片 3**</th>
      <th style={{textAlign: "left", width: "20%", paddingBottom: "8px"}}>**输出图片（多张）**</th>

      <th style={{textAlign: "left", width: "18%", paddingBottom: "8px"}} />
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image99" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011682.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image98" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011684.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image89" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011683.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image100" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011681.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="imageout2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6903291671/p1022524.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

调用前，请先[获取 API Key](/api-reference/preparation/api-key) 并将其配置为环境变量。

如需通过 SDK 调用，请先[安装 DashScope SDK](/api-reference/preparation/install-sdk)。SDK 支持 Python 和 Java。

Qwen 图片编辑模型支持一至三张输入图片。`qwen-image-2.0`/`qwen-image-3.0`、`qwen-image-edit-max` 和 `qwen-image-edit-plus` 系列可生成一至六张图片，`qwen-image-edit` 仅可生成一张图片。生成图片的 URL **有效期为 24 小时**，请及时下载至本地。

<Tabs>
  <Tab title="Python">
    ```python
    import json
    import os
    import dashscope
    from dashscope import MultiModalConversation

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    # 模型支持一至三张输入图片
    messages = [
      {
        "role": "user",
        "content": [
          {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/thtclx/input1.png"},
          {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/iclsnx/input2.png"},
          {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/gborgw/input3.png"},
          {"text": "Make the girl from Image 1 wear the black dress from Image 2 and sit in the pose from Image 3."}
        ]
      }
    ]

    # 如未配置环境变量，请替换为您的 API Key：api_key="sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")

    # qwen-image-2.0/3.0、qwen-image-edit-max 和 qwen-image-edit-plus 系列支持输出 1 至 6 张图片。本示例输出 2 张。
    response = MultiModalConversation.call(
      api_key=api_key,
      model="qwen-image-3.0-pro",
      messages=messages,
      stream=False,
      n=2,
      watermark=False,
      negative_prompt=" ",
      prompt_extend=True,
      size="1024*1536",
    )

    if response.status_code == 200:
      # 如需查看完整响应，请取消注释以下行
      # print(json.dumps(response, ensure_ascii=False))
      for i, content in enumerate(response.output.choices[0].message.content):
        print(f"输出图片 {i+1} 的 URL：{content['image']}")
    else:
      print(f"HTTP 状态码：{response.status_code}")
      print(f"错误码：{response.code}")
      print(f"错误信息：{response.message}")
    ```

    <Accordion title="响应示例">
      ```json
      {
        "status_code": 200,
        "request_id": "fa41f9f9-3cb6-434d-a95d-4ae6b9xxxxxx",
        "code": "",
        "message": "",
        "output": {
          "text": null,
          "finish_reason": null,
          "choices": [
            {
              "finish_reason": "stop",
              "message": {
                "role": "assistant",
                "content": [
                  {
                    "image": "https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/xxx.png?Expires=xxx"
                  },
                  {
                    "image": "https://dashscope-result-hz.oss-cn-hangzhou.aliyuncs.com/xxx.png?Expires=xxx"
                  }
                ]
              }
            }
          ],
          "audio": null
        },
        "usage": {
          "output_height": 1536,
          "output_width": 1024,
          "input_image_count": 3,
          "input_image_type": "qima_input_1k",
          "output_image_count": 2,
          "output_image_type": "qima_output_1k"
        }
      }
      ```
    </Accordion>
  </Tab>

  <Tab title="Java">
    ```java
    import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
    import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
    import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
    import com.alibaba.dashscope.common.MultiModalMessage;
    import com.alibaba.dashscope.common.Role;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.alibaba.dashscope.exception.UploadFileException;
    import com.alibaba.dashscope.utils.JsonUtils;
    import com.alibaba.dashscope.utils.Constants;

    import java.io.IOException;
    import java.util.Arrays;
    import java.util.Collections;
    import java.util.HashMap;
    import java.util.Map;
    import java.util.List;

    public class QwenImageEdit {

      static {
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
      }

      // 如未配置环境变量，请替换为您的 API Key：apiKey="sk-xxx"
      static String apiKey = System.getenv("DASHSCOPE_API_KEY");

      public static void call() throws ApiException, NoApiKeyException, UploadFileException, IOException {

        MultiModalConversation conv = new MultiModalConversation();

        // 模型支持一至三张输入图片
        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
            .content(Arrays.asList(
                Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/thtclx/input1.png"),
                Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/iclsnx/input2.png"),
                Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/gborgw/input3.png"),
                Collections.singletonMap("text", "Make the girl from Image 1 wear the black dress from Image 2 and sit in the pose from Image 3.")
            )).build();
        // qwen-image-2.0/3.0、qwen-image-edit-max 和 qwen-image-edit-plus 系列支持输出 1 至 6 张图片。本示例输出 2 张。
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("watermark", false);
        parameters.put("negative_prompt", " ");
        parameters.put("n", 2);
        parameters.put("prompt_extend", true);
        parameters.put("size", "1024*1536");

        MultiModalConversationParam param = MultiModalConversationParam.builder()
            .apiKey(apiKey)
            .model("qwen-image-3.0-pro")
            .messages(Collections.singletonList(userMessage))
            .parameters(parameters)
            .build();

        MultiModalConversationResult result = conv.call(param);
        // 如需查看完整响应，请取消注释以下行
        // System.out.println(JsonUtils.toJson(result));
        List<Map<String, Object>> contentList = result.getOutput().getChoices().get(0).getMessage().getContent();
        int imageIndex = 1;
        for (Map<String, Object> content : contentList) {
          if (content.containsKey("image")) {
            System.out.println("输出图片 " + imageIndex + " 的 URL：" + content.get("image"));
            imageIndex++;
          }
        }
      }

      public static void main(String[] args) {
        try {
          call();
        } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
          System.out.println(e.getMessage());
        }
      }
    }
    ```

    <Accordion title="响应示例">
      ```json
      {
        "requestId": "46281da9-9e02-941c-ac78-be88b8xxxxxx",
        "usage": {
          "output_height": 1536,
          "output_width": 1024,
          "input_image_count": 3,
          "input_image_type": "qima_input_1k",
          "output_image_count": 2,
          "output_image_type": "qima_output_1k"
        },
        "output": {
          "choices": [
            {
              "finish_reason": "stop",
              "message": {
                "role": "assistant",
                "content": [
                  {
                    "image": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx"
                  },
                  {
                    "image": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx"
                  }
                ]
              }
            }
          ]
        }
      }
      ```
    </Accordion>
  </Tab>

  <Tab title="curl">
    ```curl
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
    --header 'Content-Type: application/json' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --data '{
      "model": "qwen-image-3.0-pro",
      "input": {
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/thtclx/input1.png"
              },
              {
                "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/iclsnx/input2.png"
              },
              {
                "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/gborgw/input3.png"
              },
              {
                "text": "Make the girl from Image 1 wear the black dress from Image 2 and sit in the pose from Image 3."
              }
            ]
          }
        ]
      },
      "parameters": {
        "n": 2,
        "negative_prompt": " ",
        "prompt_extend": true,
        "watermark": false,
        "size": "1024*1536"
      }
    }'
    ```

    <Accordion title="响应示例">
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
                    "image": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx"
                  },
                  {
                    "image": "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx"
                  }
                ]
              }
            }
          ]
        },
        "usage": {
          "output_height": 1536,
          "output_width": 1024,
          "input_image_count": 3,
          "input_image_type": "qima_input_1k",
          "output_image_count": 2,
          "output_image_type": "qima_output_1k"
        },
        "request_id": "bf37ca26-0abe-98e4-8065-xxxxxx"
      }
      ```
    </Accordion>
  </Tab>
</Tabs>

<Accordion title="将图片下载到本地">
  <Tabs>
    <Tab title="Python">
      ```python
      import requests

      def download_image(image_url, save_path='output.png'):
        try:
          response = requests.get(image_url, stream=True, timeout=300)  # 设置超时时间
          response.raise_for_status()  # 如果 HTTP 状态码不是 200，则抛出异常
          with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
              f.write(chunk)
          print(f"图片已成功下载至：{save_path}")

        except requests.exceptions.RequestException as e:
          print(f"图片下载失败：{e}")

      image_url = "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx"
      download_image(image_url, save_path='output.png')
      ```
    </Tab>

    <Tab title="Java">
      ```java
      import java.io.FileOutputStream;
      import java.io.InputStream;
      import java.net.HttpURLConnection;
      import java.net.URL;

      public class ImageDownloader {
        public static void downloadImage(String imageUrl, String savePath) {
          try {
            URL url = new URL(imageUrl);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setConnectTimeout(5000);
            connection.setReadTimeout(300000);
            connection.setRequestMethod("GET");
            InputStream inputStream = connection.getInputStream();
            FileOutputStream outputStream = new FileOutputStream(savePath);
            byte[] buffer = new byte[8192];
            int bytesRead;
            while ((bytesRead = inputStream.read(buffer)) != -1) {
              outputStream.write(buffer, 0, bytesRead);
            }
            inputStream.close();
            outputStream.close();

            System.out.println("图片已成功下载至：" + savePath);
          } catch (Exception e) {
            System.err.println("图片下载失败：" + e.getMessage());
          }
        }

        public static void main(String[] args) {
          String imageUrl = "https://dashscope-result-sz.oss-cn-shenzhen.aliyuncs.com/xxx.png?Expires=xxx";
          String savePath = "output.png";
          downloadImage(imageUrl, savePath);
        }
      }
      ```
    </Tab>
  </Tabs>
</Accordion>

## 输入说明

### 输入图片（messages）

`messages` 参数为数组，必须包含一个对象。该对象须包含 `role` 和 `content` 属性。`role` 属性必须设为 `user`。`content` 属性须同时包含 `image`（一至三张图片）和 `text`（一条编辑指令）。

输入图片须满足以下要求：

- 支持的图片格式为 JPG、JPEG、PNG、BMP、TIFF、WEBP 和 GIF。

  <Note>
    输出图片为 PNG 格式。动态 GIF 仅处理第一帧。
  </Note>

- 为获得最佳效果，图片分辨率的宽度和高度应在 384 至 3072 像素之间。分辨率过低可能导致输出模糊，过高则会增加处理时间。

- 单张图片文件大小不超过 10 MB。

```json
"messages": [
  {
    "role": "user",
    "content": [
      { "image": "图片 1 的公开 URL 或 Base64 数据" },
      { "image": "图片 2 的公开 URL 或 Base64 数据" },
      { "image": "图片 3 的公开 URL 或 Base64 数据" },
      { "text": "编辑指令，例如：'图 1 中的女孩穿上图 2 中的黑色连衣裙，摆出图 3 中的坐姿'" }
    ]
  }
]
```

### 图片输入顺序

当您提供多张输入图片时，图片的顺序由其在数组中的位置决定。因此，提示词引用的图片编号需要**与图片数组中的顺序一一对应**，例如：数组中的第一张图片为"图 1"，第二张为"图 2"，或者使用标记形式如"\[图 1]"、"\[图 2]"。

```json
{
  "content": [
    {"text": "编辑指令，如：将图 1 中的闹钟放置到图 2 的餐桌的花瓶旁边位置"},
    {"image": "https://example.com/image1.png"},
    {"image": "https://example.com/image2.png"}
  ]
}
```

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "27%", paddingBottom: "8px"}}>**输入图片 1**</th>
      <th style={{textAlign: "left", width: "20%", paddingBottom: "8px"}}>**输入图片 2**</th>
      <th style={{textAlign: "left", width: "27%", paddingBottom: "8px"}}>**输出图片**</th>

      <th style={{textAlign: "left", width: "27%", paddingBottom: "8px"}} />
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image (19)-转换自-png" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3509593671/p1025838.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        图 1
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image (20)-转换自-png" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3509593671/p1025839.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        图 2
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="04e0fc39-转换自-png" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3509593671/p1021092.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        提示词：把图 1 移动到图 2 上
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="36ed450d-转换自-png" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3509593671/p1021093.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        提示词：把图 2 移动到图 1 上
      </td>
    </tr>
  </tbody>
</table>

### 图片输入方式

**公开 URL**

- 您可以提供支持 HTTP 或 HTTPS 协议的公开图片 URL。
- 示例值：`https://xxxx/img.png`。

**Base64 编码**

将图片文件转换为 Base64 编码字符串，并按以下格式拼接：`data:<mime_type>;base64,<base64_data>`。

- `<mime_type>`：图片的媒体类型，须与文件格式对应。
- `<base64_data>`：文件的 Base64 编码字符串。
- 示例值：`data:image/jpeg;base64,GDU7MtCZz...`（示例已截断）

### 更多参数

通过以下**可选**参数调整生成效果：

- **n**：生成图片数量，默认值为 1。qwen-image-2.0/3.0、qwen-image-edit-max 和 qwen-image-edit-plus 系列模型支持生成一至六张图片，`qwen-image-edit` 模型仅支持生成一张图片。

- **negative\_prompt**：描述需要排除的内容，例如"模糊"或"多余的手指"。该参数有助于优化生成图片的质量。

- **watermark**：是否在图片右下角添加"Qwen-Image"水印。默认值为 `false`。

- **seed**：随机数种子，取值范围为 `[0, 2147483647]` 的整数。未指定时，算法将随机生成种子值。使用相同的种子值有助于保持生成结果的一致性。

以下**可选**参数仅适用于 qwen-image-2.0/3.0、qwen-image-edit-max 和 qwen-image-edit-plus 系列模型：

- **size**：输出图片的分辨率，格式为 `宽*高`，例如 `"1024*2048"`。对于 qwen-image-2.0/3.0 系列模型，可以自由设置宽度和高度，输出图片的总像素须在 512 x 512 至 2048 x 2048 之间。qwen-image-2.0 系列默认分辨率与输入图片相同（多张图片时取最后一张）；qwen-image-3.0 系列不指定时由模型根据提示词自动推荐分辨率。对于 qwen-image-edit-max 和 qwen-image-edit-plus 系列模型，宽度和高度的取值范围为 512 至 2048 像素。默认输出分辨率接近 `1024*1024`，且宽高比与原图相近。
- **prompt\_extend**：是否启用提示词改写功能。默认值为 `true`。启用后，模型会对提示词进行优化。该功能对简短或描述不够详细的提示词效果尤为显著。
- **prompt\_extend\_mode**：提示词改写方式，仅 qwen-image-3.0 系列支持。图像编辑仅支持默认值 `direct`（直接提示词增强，DPE）；传入 `agent` 将返回 400 错误。

完整参数列表请参见 [Qwen-Image-Edit API 参考](/api-reference/image-generation/qwen-image-editing)。

## 功能概览

### 多图融合

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入图片 1**</th>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入图片 2**</th>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入图片 3**</th>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输出图片**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image83" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011712.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image103" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011753.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4405461671/p1012002.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/4405461671/p1012004.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 图 1 中的女孩佩戴图 2 中的项链，左肩背着图 3 中的包。
      </td>
    </tr>
  </tbody>
</table>

### 主体一致性

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输出图片 1**</th>
      <th style={{textAlign: "left", width: "34%", paddingBottom: "8px"}}>**输出图片 2**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image5" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011789.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image4" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011790.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将图片改为蓝底证件照。人物穿白衬衫、黑西装，系条纹领带。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image6" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011791.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 人物穿白衬衫、灰西装，系条纹领带。一只手放在领带上，背景为浅色。
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image12" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1012037.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image13" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1012038.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将空调放置在客厅中，旁边有一张沙发。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image14" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1012039.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 从空调出风口添加雾气，雾气延伸到沙发上方。同时添加绿色叶片。
      </td>
    </tr>
  </tbody>
</table>

### 线稿生图

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输出图片**</th>

      <th style={{textAlign: "left", width: "34%", paddingBottom: "8px"}} />
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image42" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011821.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image43" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011822.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 生成一张与图 1 中详细轮廓匹配的图片，描述如下：一位年轻女性在阳光明媚的日子里微笑。她戴着豹纹框的圆形棕色太阳镜，头发整齐地扎起，佩戴珍珠耳环，围着带紫色星形图案的深蓝色围巾，穿着黑色皮夹克。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image44" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011824.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 生成一张与图 1 中详细轮廓匹配的图片，描述如下：一位老人对着镜头微笑，脸上布满皱纹，头发在风中凌乱，戴着金框老花镜，脖子上围着带星形图案的旧红色围巾，穿着棉袄。
      </td>
    </tr>
  </tbody>
</table>

### 创意商品生成

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输出图片**</th>

      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}} />

      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}} />
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="bear" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p999719.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image23" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011685.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 让这只熊坐在月亮下（白色背景上用浅灰色新月轮廓表示），抱着吉他，周围漂浮着小星星和写有"Be Kind"等短语的气泡。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image22" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011686.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将此图案印在 T 恤和纸质手提袋上。一位女模特正在展示这些物品。她还戴着一顶写有"Be kind"的棒球帽。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image21" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011687.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 一个超写实的 1/7 比例角色模型，设计为商业成品，放置在带有白色键盘的 iMac 旁的桌面上。模型站在一个干净的圆形透明亚克力底座上，底座无标签或文字。专业摄影棚灯光凸显雕刻细节。背景中 iMac 屏幕上显示同一模型的 ZBrush 建模过程。模型旁边放置一个正面带透明窗口的包装盒，窗口内仅展示透明塑料壳。包装盒略高于模型，尺寸合理。
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top"}} />

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p999632.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 这只熊穿着宇航服，手指向远方。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p999633.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 这只熊穿着华丽的礼服裙，双臂展开，呈优雅的舞蹈姿势。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p999630.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 这只熊穿着运动装，手持篮球，一条腿弯曲。
      </td>
    </tr>
  </tbody>
</table>

### 深度图生图

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输出图片**</th>

      <th style={{textAlign: "left", width: "34%", paddingBottom: "8px"}} />
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image36" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011810.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image37" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011811.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 生成一张与图 1 中深度图匹配的图片，描述如下：一辆蓝色自行车停在小巷旁，背景中石头缝隙里长着几株杂草。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image38" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011812.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 生成一张与图 1 中深度图匹配的图片，描述如下：一辆破旧的红色自行车停在泥泞的小路上，背景是茂密的原始森林。
      </td>
    </tr>
  </tbody>
</table>

### 关键点生图

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>**输出图片**</th>

      <th style={{textAlign: "left", width: "34%", paddingBottom: "8px"}} />
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image40" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011817.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image41" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011818.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 生成一张与图 1 中人体姿态匹配的图片，描述如下：一位穿着汉服的中国女性在雨中撑着油纸伞，背景是苏州园林。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image39" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011819.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 生成一张与图 1 中人体姿态匹配的图片，描述如下：一个年轻男子站在地铁站台上，戴着棒球帽，穿着 T 恤和牛仔裤，身后有一列列车正在飞驰。
      </td>
    </tr>
  </tbody>
</table>

### 文字编辑

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "35%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "35%", paddingBottom: "8px"}}>**输出图片**</th>
      <th style={{textAlign: "left", width: "15%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "15%", paddingBottom: "8px"}}>**输出图片**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p999641.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://img.alicdn.com/imgextra/i4/O1CN01tVRmgU1KTA9Kvy6vN_!!6000000001164-49-tps-1248-832.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将拼字游戏牌上的"HEALTH INSURANCE"替换为"<strong>Tomorrow will be better</strong>"。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1000039.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1000062.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将便签上的"Take a Breather"改为"<strong>Relax and Recharge</strong>"。
      </td>
    </tr>
  </tbody>
</table>

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输出图片**</th>

      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}} />

      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}} />
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image53" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011772.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image45" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011774.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将"Qwen-Image"改为黑色墨滴字体。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image46" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011775.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将"Qwen-Image"改为黑色手写字体。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image49" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011776.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将"Qwen-Image"改为黑色像素字体。
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top"}} />

      <td style={{verticalAlign: "top"}}>
        <img alt="image54" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011777.jpeg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将"Qwen-Image"改为红色。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image57" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011779.jpeg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将"Qwen-Image"改为蓝紫渐变色。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image59" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011780.jpeg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将"Qwen-Image"改为糖果色。
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top"}} />

      <td style={{verticalAlign: "top"}}>
        <img alt="image63" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011783.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将"Qwen-Image"的材质改为金属。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image64" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011784.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将"Qwen-Image"的材质改为云朵。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image67" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011786.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 将"Qwen-Image"的材质改为玻璃。
      </td>
    </tr>
  </tbody>
</table>

### 增删改

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输出图片**</th>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输出图片**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p999647.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p999648.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 在企鹅前面添加一块小木牌，上面写着"Welcome to Penguin Beach"。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p999649.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p999650.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 去掉盘子上的头发。
      </td>
    </tr>
  </tbody>
</table>

### 视角变换

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输出图片**</th>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输出图片**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p999964.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p999968.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 获取正面视图。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p999969.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p999970.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 朝向左边。
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p999974.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p999975.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 获取背面视图。
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p999971.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p999972.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 朝向右边。
      </td>
    </tr>
  </tbody>
</table>

### 旧照处理

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px"}}>**输入图片**</th>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px"}}>**输出图片**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p999552.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p999554.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 修复旧照片，去除划痕，降低噪点，增强细节，高分辨率，真实图像，自然肤色，清晰的面部特征，无失真。
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image31" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/5844029571/p1011757.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image32" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/6844029571/p1011759.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 根据图片内容智能上色，使画面更加生动。
      </td>
    </tr>
  </tbody>
</table>

## 计费与限流

免费额度和计费标准请参见[计费说明](/developer-guides/getting-started/pricing)。

限流策略请参见[限流](/developer-guides/administration/rate-limits)。

**计费详情**：

- 按**成功生成的图片数量**计费。模型调用失败或处理错误不产生费用，也不消耗免费额度。
- 您可以开启"仅免费额度"功能，避免免费额度用完后产生额外费用。详情请参见[新用户免费额度](/resources/free-quota)。

## API 参考

API 的输入输出参数请参见 [Qwen - image editing](/api-reference/image-generation/qwen-image-editing)。

## 错误码

调用失败时，请参见[错误信息](/api-reference/preparation/error-messages)。

## 常见问题

**Q：Qwen 图片编辑模型支持哪些语言？**

官方支持简体中文和**英文**。其他语言可能可用，但效果不保证。

**Q：如何查看模型调用量？**

模型调用完成一小时后，您可以前往[**用量分析**](https://platform.qianwenai.com/home/analytics)页面查看调用次数、成功率等指标。详情请参见[账单查询与费用管理](/resources/bill-query)。

**Q：如何获取图片存储域名白名单？**

模型生成的图片存储在 OSS 中，API 返回的是临时公开 URL。**如需为该下载 URL 配置防火墙白名单**，请注意：底层存储可能动态变化。本文不提供固定的 OSS 域名白名单，以免信息过时导致访问异常。如有安全管控需求，请联系您的客户经理获取最新的 OSS 域名列表。

更多问题请参见[图片与视频 FAQ](/resources/faq-images-videos)。
