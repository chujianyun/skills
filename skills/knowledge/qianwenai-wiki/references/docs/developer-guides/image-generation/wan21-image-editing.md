> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 万相2.1 通用图像编辑

> 使用万相-通用图像编辑模型，通过文本指令实现扩图、去水印、风格迁移、指令编辑、局部重绘等多种图像编辑任务。

<Note>
  请先[获取 API Key](/api-reference/preparation/api-key) 并[设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。
</Note>

## 模型概览

万相-通用图像编辑模型（`wanx2.1-imageedit`）支持输入文本指令，实现扩图、去水印、风格迁移、指令编辑、局部重绘、图像修复等多种图像编辑任务。

免费额度与计费详情请参见[免费额度](/resources/free-quota)和[计费说明](/developer-guides/getting-started/pricing)，限流信息请在[控制台](https://platform.qianwenai.com/home/benefits)查看。

## 快速开始

本节演示如何调用通用图像编辑 API 完成一次"局部重绘"任务。

SDK 在底层封装了异步处理逻辑，上层接口表现为同步调用（即单次请求并等待最终结果返回）；而 curl 示例则对应两个独立的异步 API 接口：一个用于提交任务，另一个用于查询结果。

<CodeGroup>
  ```python Python
  import base64
  import os
  from http import HTTPStatus
  from dashscope import ImageSynthesis
  import mimetypes

  """
  环境要求：
      dashscope python SDK >= 1.23.8
  安装/升级SDK:
      pip install -U dashscope
  """

  # 若没有配置环境变量，请用千问AI平台API Key将下行替换为：api_key="sk-xxx"
  api_key = os.getenv("DASHSCOPE_API_KEY")

  # --- 辅助函数：用于 Base64 编码 ---
  # 格式为 data:{MIME_type};base64,{base64_data}
  def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type or not mime_type.startswith("image/"):
      raise ValueError("不支持或无法识别的图像格式")
    with open(file_path, "rb") as image_file:
      encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

  """
  图像输入方式说明：
  以下提供了三种图片输入方式，三选一即可

  1. 使用公网URL - 适合已有公开可访问的图片
  2. 使用本地文件 - 适合本地开发测试
  3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
  """

  # 【方式一】使用公网图片 URL
  mask_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
  base_image_url = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg"

  # 【方式二】使用本地文件（支持绝对路径和相对路径）
  # 格式要求：file:// + 文件路径
  # 示例（绝对路径）：
  # mask_image_url = "file://" + "/path/to/your/mask_image.png"     # Linux/macOS
  # base_image_url = "file://" + "C:/path/to/your/base_image.jpeg"  # Windows
  # 示例（相对路径）：
  # mask_image_url = "file://" + "./mask_image.png"                 # 以实际路径为准
  # base_image_url = "file://" + "./base_image.jpeg"                # 以实际路径为准

  # 【方式三】使用Base64编码的图片
  # mask_image_url = encode_file("./mask_image.png")               # 以实际路径为准
  # base_image_url = encode_file("./base_image.jpeg")              # 以实际路径为准

  def sample_sync_call_imageedit():
    print('please wait...')
    rsp = ImageSynthesis.call(api_key=api_key,
                              model="wanx2.1-imageedit",
                              function="description_edit_with_mask",
                              prompt="陶瓷兔子拿着陶瓷小花",
                              mask_image_url=mask_image_url,
                              base_image_url=base_image_url,
                              n=1)
    assert rsp.status_code == HTTPStatus.OK

    print('response: %s' % rsp)
    if rsp.status_code == HTTPStatus.OK:
      for result in rsp.output.results:
        print("---------------------------")
        print(result.url)
    else:
      print('sync_call Failed, status_code: %s, code: %s, message: %s' %
            (rsp.status_code, rsp.code, rsp.message))

  if __name__ == '__main__':
    sample_sync_call_imageedit()
  ```

  ```json Python 响应示例
  {
      "status_code": 200,
      "request_id": "dc41682c-4e4a-9010-bc6f-xxxxxx",
      "code": null,
      "message": "",
      "output": {
          "task_id": "6e319d88-a07a-420c-9493-xxxxxx",
          "task_status": "SUCCEEDED",
          "results": [
              {
                  "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/xxx.png?xxxxxx"
              }
          ],
          "submit_time": "2025-05-26 14:58:27.320",
          "scheduled_time": "2025-05-26 14:58:27.339",
          "end_time": "2025-05-26 14:58:39.170",
          "task_metrics": {
              "TOTAL": 1,
              "SUCCEEDED": 1,
              "FAILED": 0
          }
      },
      "usage": {
          "image_count": 1
      }
  }
  ```

  ```java Java
  // Copyright (c) Alibaba, Inc. and its affiliates.

  import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
  import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
  import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
  import com.alibaba.dashscope.exception.ApiException;
  import com.alibaba.dashscope.exception.NoApiKeyException;
  import com.alibaba.dashscope.utils.JsonUtils;

  import java.io.IOException;
  import java.nio.file.Files;
  import java.nio.file.Path;
  import java.nio.file.Paths;
  import java.util.Base64;
  import java.util.HashMap;
  import java.util.Map;

  /**
   * 环境要求
   *      dashscope java SDK >=2.20.9
   * 更新maven依赖:
   *      https://mvnrepository.com/artifact/com.alibaba/dashscope-sdk-java
   */

  public class ImageEditSync {

      // 若没有配置环境变量，请用千问AI平台API Key将下行替换为：apiKey="sk-xxx"
      static String apiKey = System.getenv("DASHSCOPE_API_KEY");

      /**
       * 图像输入方式说明：三选一即可
       *
       * 1. 使用公网URL - 适合已有公开可访问的图片
       * 2. 使用本地文件 - 适合本地开发测试
       * 3. 使用Base64编码 - 适合私有图片或需要加密传输的场景
       */

      //【方式一】公网URL
      static String maskImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png";
      static String baseImageUrl = "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg";

      //【方式二】本地文件路径（file://+绝对路径 or file:///+绝对路径）
      // static String maskImageUrl = "file://" + "/your/path/to/mask_image.png";    // Linux/macOS
      // static String baseImageUrl = "file:///" + "C:/your/path/to/base_image.png";  // Windows

      //【方式三】Base64编码
      // static String maskImageUrl = encodeFile("/your/path/to/mask_image.png");
      // static String baseImageUrl = encodeFile("/your/path/to/base_image.png");

      public static void syncCall() {
          // 设置parameters参数
          Map<String, Object> parameters = new HashMap<>();
          parameters.put("prompt_extend", true);

          ImageSynthesisParam param =
                  ImageSynthesisParam.builder()
                          .apiKey(apiKey)
                          .model("wanx2.1-imageedit")
                          .function(ImageSynthesis.ImageEditFunction.DESCRIPTION_EDIT_WITH_MASK)
                          .prompt("陶瓷兔子拿着陶瓷小花")
                          .maskImageUrl(maskImageUrl)
                          .baseImageUrl(baseImageUrl)
                          .n(1)
                          .size("1024*1024")
                          .parameters(parameters)
                          .build();

          ImageSynthesis imageSynthesis = new ImageSynthesis();
          ImageSynthesisResult result = null;
          try {
              System.out.println("---sync call, please wait a moment----");
              result = imageSynthesis.call(param);
          } catch (ApiException | NoApiKeyException e){
              throw new RuntimeException(e.getMessage());
          }
          System.out.println(JsonUtils.toJson(result));
      }

      /**
       * 将文件编码为Base64字符串
       * @param filePath 文件路径
       * @return Base64字符串，格式为 data:{MIME_type};base64,{base64_data}
       */
      public static String encodeFile(String filePath) {
          Path path = Paths.get(filePath);
          if (!Files.exists(path)) {
              throw new IllegalArgumentException("文件不存在: " + filePath);
          }
          // 检测MIME类型
          String mimeType = null;
          try {
              mimeType = Files.probeContentType(path);
          } catch (IOException e) {
              throw new IllegalArgumentException("无法检测文件类型: " + filePath);
          }
          if (mimeType == null || !mimeType.startsWith("image/")) {
              throw new IllegalArgumentException("不支持或无法识别的图像格式");
          }
          // 读取文件内容并编码
          byte[] fileBytes = null;
          try{
              fileBytes = Files.readAllBytes(path);
          } catch (IOException e) {
              throw new IllegalArgumentException("无法读取文件内容: " + filePath);
          }

          String encodedString = Base64.getEncoder().encodeToString(fileBytes);
          return "data:" + mimeType + ";base64," + encodedString;
      }

      public static void main(String[] args) {
          syncCall();
      }
  }
  ```

  ```json Java 响应示例
  {
      "request_id": "bf6c6361-f0fc-949c-9d60-xxxxxx",
      "output": {
          "task_id": "958db858-153b-4c81-b243-xxxxxx",
          "task_status": "SUCCEEDED",
          "results": [
              {
                  "url": "https://dashscope-result-wlcb-acdr-1.oss-cn-wulanchabu-acdr-1.aliyuncs.com/xxx.png?xxxxxx"
              }
          ],
          "task_metrics": {
              "TOTAL": 1,
              "SUCCEEDED": 1,
              "FAILED": 0
          }
      },
      "usage": {
          "image_count": 1
      }
  }
  ```
</CodeGroup>

**curl 示例（异步两步调用）**

<Note>
  异步调用必须设置 Header 参数 `X-DashScope-Async` 为 `enable`。异步任务的 `task_id` 查询有效期为 24 小时，过期后任务状态将变为 `UNKNOWN`。
</Note>

**步骤1：发起创建任务请求**

该请求会返回一个任务ID（`task_id`）。

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx2.1-imageedit",
  "input": {
    "function": "description_edit_with_mask",
    "prompt": "陶瓷兔子拿着陶瓷小花",
    "base_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg",
    "mask_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
  },
  "parameters": {
    "n": 1
  }
}'
```

响应示例：

```json
{
    "output": {
        "task_status": "PENDING",
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
    },
    "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
}
```

**步骤2：根据任务ID查询结果**

使用上一步获取的 `task_id`，通过接口轮询任务状态，直到 `task_status` 变为 SUCCEEDED 或 FAILED。请将 `0385dc79-5ff8-4d82-bcb6-xxxxxx` 替换为真实的 task\_id。

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/0385dc79-5ff8-4d82-bcb6-xxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

响应示例：

```json
{
    "request_id": "eeef0935-02e9-9742-bb55-xxxxxx",
    "output": {
        "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx",
        "task_status": "SUCCEEDED",
        "submit_time": "2025-02-21 17:56:31.786",
        "scheduled_time": "2025-02-21 17:56:31.821",
        "end_time": "2025-02-21 17:56:42.530",
        "results": [
            {
                "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/aaa.png"
            }
        ],
        "task_metrics": {
            "TOTAL": 1,
            "SUCCEEDED": 1,
            "FAILED": 0
        }
    },
    "usage": {
        "image_count": 1
    }
}
```

## 关键能力

通用图像编辑 API 通过 `function` 参数来指定不同的图像编辑功能。所有功能均遵循[快速开始](#快速开始)的调用方式。

下文以 curl 调用为例，仅列出各功能专属的 `input` 和 `parameters` JSON 片段，用于说明请求体中需配置的内容。完整请求结构（包含 model、input、parameters 等顶层字段）请参见 [API 参考](#api-参考)。

### 全局风格化

将整张图像迁移至指定的艺术风格。使用场景包括：绘本创作、社交媒体配图（生成符合特定视觉风格的背景或概念图）等。

- **如何使用**：将参数 `function` 设置为 `stylization_all`。
- **支持的风格**：法国绘本风格、金箔艺术风格。
- **搭配使用的参数**：`parameters.strength` (0.0-1.0, 默认 0.5) 控制修改幅度，值越小越接近原图。
- **提示词技巧**：使用"转换成xx风格"的句式，如"转换成法国绘本风格"。

<Accordion title="请求示例">
  ```json
  {
    "input": {
      "function": "stylization_all",
      "prompt": "转换成法国绘本风格",
      "base_image_url": "http://wanx.alicdn.com/material/20250318/stylization_all_3.png"
    },
    "parameters": {
      "strength": 0.5
    }
  }
  ```
</Accordion>

### 局部风格化

仅对图像中指定区域进行风格迁移，需配合 mask 使用。

- **如何使用**：将参数 `function` 设置为 `stylization_local`，并提供 `mask_image_url`。
- **提示词技巧**：描述希望应用的风格，如"把房子变成木板风格"。

<Accordion title="请求示例">
  ```json
  {
    "input": {
      "function": "stylization_local",
      "prompt": "把房子变成木板风格",
      "base_image_url": "http://wanx.alicdn.com/material/20250318/stylization_local_3.png",
      "mask_image_url": "http://wanx.alicdn.com/material/20250318/stylization_local_3_mask.png"
    },
    "parameters": {
      "strength": 0.5
    }
  }
  ```
</Accordion>

### 指令编辑

根据文字描述对整张图像进行编辑，无需提供 mask。

- **如何使用**：将参数 `function` 设置为 `description_edit`。
- **搭配使用的参数**：`parameters.strength` (0.0-1.0, 默认 0.5) 控制修改幅度，值越小越接近原图。
- **提示词技巧**：描述期望的修改结果，如"把她的头发修改为红色"。

<Accordion title="请求示例">
  ```json
  {
    "input": {
      "function": "description_edit",
      "prompt": "把她的头发修改为红色",
      "base_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_3.jpeg"
    },
    "parameters": {
      "strength": 0.5
    }
  }
  ```
</Accordion>

### 局部重绘

结合 mask 进行精准局部编辑，对指定区域进行重新绘制。

- **如何使用**：将参数 `function` 设置为 `description_edit_with_mask`，并提供 `mask_image_url`。
- **提示词技巧**：描述期望在 mask 区域内呈现的内容，如"陶瓷兔子拿着陶瓷小花"。

<Accordion title="请求示例">
  ```json
  {
    "input": {
      "function": "description_edit_with_mask",
      "prompt": "陶瓷兔子拿着陶瓷小花",
      "base_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3.jpeg",
      "mask_image_url": "http://wanx.alicdn.com/material/20250318/description_edit_with_mask_3_mask.png"
    }
  }
  ```
</Accordion>

### 去文字水印

去除图片中的文字水印。

- **如何使用**：将参数 `function` 设置为 `remove_watermark`。
- **提示词技巧**：使用"去除图像中的文字"等描述。

<Accordion title="请求示例">
  ```json
  {
    "input": {
      "function": "remove_watermark",
      "prompt": "去除图像中的文字",
      "base_image_url": "http://wanx.alicdn.com/material/20250318/remove_watermark_3.png"
    }
  }
  ```
</Accordion>

### 扩图

向四个方向扩展画布，生成原图之外的内容。

- **如何使用**：将参数 `function` 设置为 `expand`。
- **搭配使用的参数**：`top_scale`、`bottom_scale`、`left_scale`、`right_scale`（默认各 1.0），设置各方向的扩展比例，如 1.5 表示该方向扩展到原来的 1.5 倍。

<Accordion title="请求示例">
  ```json
  {
    "input": {
      "function": "expand",
      "base_image_url": "http://wanx.alicdn.com/material/20250318/expand_3.jpeg"
    },
    "parameters": {
      "top_scale": 1.5,
      "bottom_scale": 1.5,
      "left_scale": 1.5,
      "right_scale": 1.5
    }
  }
  ```
</Accordion>

### 图像超分

提高图像分辨率（超分辨率重建）。

- **如何使用**：将参数 `function` 设置为 `super_resolution`。
- **搭配使用的参数**：`parameters.upscale_factor`（默认 2），设置放大倍数。

<Accordion title="请求示例">
  ```json
  {
    "input": {
      "function": "super_resolution",
      "base_image_url": "http://wanx.alicdn.com/material/20250318/super_resolution_3.jpeg"
    },
    "parameters": {
      "upscale_factor": 2
    }
  }
  ```
</Accordion>

### 图像上色

为黑白图片自动上色。

- **如何使用**：将参数 `function` 设置为 `colorization`。
- **提示词技巧**：描述期望的颜色方案，如"蓝色背景，黄色的叶子"。

<Accordion title="请求示例">
  ```json
  {
    "input": {
      "function": "colorization",
      "prompt": "蓝色背景，黄色的叶子",
      "base_image_url": "http://wanx.alicdn.com/material/20250318/colorization_3.jpeg"
    }
  }
  ```
</Accordion>

### 线稿生图 / 涂鸦作画

基于线稿或涂鸦生成图像，通过 `is_sketch` 参数区分两种输入类型。

- **如何使用**：将参数 `function` 设置为 `doodle`。
- **搭配使用的参数**：
  - `is_sketch: false`（默认）：输入为线稿图，生成风格化图像。
  - `is_sketch: true`：输入为涂鸦，生成对应内容图像。
- **提示词技巧**：描述期望生成的图像内容及风格，如"北欧极简风格的客厅"。

<Accordion title="请求示例（线稿生图）">
  ```json
  {
    "input": {
      "function": "doodle",
      "prompt": "北欧极简风格的客厅",
      "base_image_url": "http://wanx.alicdn.com/material/20250318/doodle_3.png",
      "is_sketch": false
    }
  }
  ```
</Accordion>

<Accordion title="请求示例（涂鸦作画）">
  ```json
  {
    "input": {
      "function": "doodle",
      "prompt": "一颗树，二次元动漫风格",
      "base_image_url": "http://wanx.alicdn.com/material/20250318/doodle_sketch_3.png",
      "is_sketch": true
    }
  }
  ```
</Accordion>

### 参考卡通形象生图

<Warning>
  使用本功能处理受版权保护的卡通形象可能构成侵权行为。请确保您拥有所参考形象的合法使用权，或使用您原创的形象，并自行承担所有相关法律责任。
</Warning>

保持参考卡通形象特征，根据提示词生成新的场景图像。

- **如何使用**：将参数 `function` 设置为 `control_cartoon_feature`。
- **提示词技巧**：采用"卡通形象..."的句式，详细描述形象的动作和所处环境。

<Accordion title="请求示例">
  ```json
  {
    "input": {
      "function": "control_cartoon_feature",
      "prompt": "卡通形象小心翼翼地探出头，窥视着房间内一颗璀璨的蓝色宝石",
      "base_image_url": "http://wanx.alicdn.com/material/20250318/control_cartoon_feature_1.png"
    }
  }
  ```
</Accordion>

## 应用于生产环境

**最佳实践**

- **异步轮询**：轮询查询异步任务结果时，建议采用合理的轮询策略（如前30秒每3秒一次，之后拉长间隔），避免因过于频繁的请求而触发限流。
- **参数调优**：对于 `strength` 等影响效果的关键参数，建议在正式上线前进行小范围测试，找到最适合业务场景的数值。
- **图像存储**：API 返回的图像 URL 有效期24小时。请及时将生成的图像下载并转存到您自己的持久化对象存储服务中。

**风险防范**

- **错误处理**：对任务查询结果中的 `task_status` 进行判断。对于 `FAILED` 状态，应记录 `code` 和 `message` 以便排查。部分错误（如系统超时）可能是瞬时的，可设计重试逻辑。
- **内容安全**：API 会对输入和输出内容进行安全审核。若内容不合规，请求将会报错 `DataInspectionFailed` 错误。

## API 参考

关于万相-通用图像编辑模型的输入与输出参数，请参见 [Wan 2.1 — 编辑图像](/api-reference/image-generation/wan21-general-image-editing/create-task)。

## 计费与限流

- 模型免费额度和计费单价请参见[模型列表与价格](/developer-guides/getting-started/pricing)。
- 模型限流请参见[万相](/developer-guides/administration/rate-limits)。
- 计费说明：
  - 按成功生成的**图像张数**计费。仅当接口返回 `task_status` 为 `SUCCEEDED` 并成功生成图像后，才会计费。
  - 模型调用失败或处理错误不产生任何费用，也不消耗[新人免费额度](/resources/free-quota)。

## 错误码

如果模型调用失败并返回报错信息，请参见[错误信息](/api-reference/preparation/error-messages)进行解决。

## 常见问题

**Q: 为什么我的任务会失败（FAILED）？**

A: 任务失败的常见原因包括：

1. 内容审核不通过：输入或生成的图像内容触发了安全策略。
2. 参数错误：请求中的参数不合法，如 `function` 名称错误、URL 无法访问等。
3. 模型内部错误：模型在处理过程中遇到预期外的问题。请检查任务查询响应中的 `code` 和 `message` 字段，获取具体错误码和信息，以便定位问题。
