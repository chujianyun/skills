> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像编辑 - 万相2.7/2.6/2.5

> 万相图像编辑模型系列支持多图输入与多图输出，通过文本指令实现图像编辑、多图融合、主体特征保持、目标检测与分割等能力。

## 快速开始

本示例将演示如何使用`wan2.7-image-pro`模型，基于2张输入图片和提示词生成编辑后的图像。

提示词：把图2的涂鸦喷绘在图1的汽车上

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "19%", paddingBottom: "8px"}}>**输入图像1**</th>
      <th style={{textAlign: "left", width: "41%", paddingBottom: "8px"}}>**输入图像2**</th>
      <th style={{textAlign: "left", width: "40%", paddingBottom: "8px"}}>**输出图像（wan2.7-image-pro）**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="car" src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="paint" src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="output" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1063463.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

<Tabs>
  <Tab title="同步调用">
    <Note>请确保 DashScope Python SDK 版本不低于 `1.25.15`，DashScope Java SDK 版本不低于 `2.22.13`。</Note>

    <CodeGroup>
      ```python
      import os
      import dashscope
      from dashscope.aigc.image_generation import ImageGeneration
      from dashscope.api_entities.dashscope_response import Message

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      # 如果未设置环境变量，请将下行替换为：api_key="sk-xxx"
      api_key = os.getenv("DASHSCOPE_API_KEY")

      message = Message(
        role="user",
        # 支持本地文件，如 "image": "file://car.png"
        content=[
          {
            "text": "把图2的涂鸦喷绘在图1的汽车上"
          },
          {
            "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"
          },
          {
            "image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"
          }
        ]
      )
      print("----同步调用，请稍候----")
      rsp = ImageGeneration.call(
          model='wan2.7-image-pro',
          api_key=api_key,
          messages=[message],
          watermark=False,
          n=1,
          size="2K"
        )

      print(rsp)
      ```

      ```json
      {
          "status_code": 200,
          "request_id": "81d868c6-6ce1-92d8-a90d-d2ee71xxxxxx",
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
                                  "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                                  "type": "image"
                              }
                          ]
                      }
                  }
              ],
              "audio": null,
              "finished": true
          },
          "usage": {
              "input_tokens": 18790,
              "output_tokens": 2,
              "characters": 0,
              "image_count": 1,
              "size": "2985*1405",
              "total_tokens": 18792
          }
      }
      ```

      ```java
      import com.alibaba.dashscope.aigc.imagegeneration.*;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;
      import com.alibaba.dashscope.utils.JsonUtils;

      import java.util.Arrays;
      import java.util.Collections;

      /**
       * wan2.7-image-pro 图像编辑 - 同步调用示例
       */
      public class Main {

        static {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        }

        // 如果未配置环境变量，请将下行替换为：apiKey="sk-xxx"
        static String apiKey = System.getenv("DASHSCOPE_API_KEY");

        public static void basicCall() throws ApiException, NoApiKeyException, UploadFileException {
          // 构建多图输入消息
          ImageGenerationMessage message = ImageGenerationMessage.builder()
            .role("user")
            .content(Arrays.asList(
              // 支持多图输入，提供多张参考图
              Collections.singletonMap("text", "把图2的涂鸦喷绘在图1的汽车上"),
              Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"),
              Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp")
            )).build();

          // 图像编辑使用普通同步调用，无需设置 stream 和 enable_interleave
          ImageGenerationParam param = ImageGenerationParam.builder()
            .apiKey(apiKey)
            .model("wan2.7-image-pro")
            .messages(Collections.singletonList(message))
            .n(1)
            .size("2K")
            .build();

          ImageGeneration imageGeneration = new ImageGeneration();
          ImageGenerationResult result = null;
          try {
            System.out.println("---同步调用图像编辑，请稍候----");
            result = imageGeneration.call(param);
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
          }
          System.out.println(JsonUtils.toJson(result));
        }

        public static void main(String[] args) {
          try {
            basicCall();
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
        }
      }
      ```

      ```json
      {
          "requestId": "1bf6173a-e8de-9f75-94d3-5e618f875xxx",
          "usage": {
              "input_tokens": 18790,
              "output_tokens": 2,
              "total_tokens": 18792,
              "image_count": 1,
              "size": "2985*1405"
          },
          "output": {
              "choices": [
                  {
                      "finish_reason": "stop",
                      "message": {
                          "role": "assistant",
                          "content": [
                              {
                                  "image": "https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                                  "type": "image"
                              }
                          ]
                      }
                  }
              ],
              "finished": true
          },
          "status_code": 200,
          "code": "",
          "message": ""
      }
      ```

      ```bash
      curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header 'Content-Type: application/json' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --data '{
          "model": "wan2.7-image-pro",
          "input": {
              "messages": [
                  {
                      "role": "user",
                      "content": [
                          {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"},
                          {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"},
                          {"text": "把图2的涂鸦喷绘在图1的汽车上"}
                      ]
                  }
              ]
          },
          "parameters": {
              "size": "2K",
              "n": 1,
              "watermark": false
          }
      }'
      ```

      ```json
      {
          "output": {
              "choices": [
                  {
                      "finish_reason": "stop",
                      "message": {
                          "content": [
                              {
                                  "image": "https://dashscope-xxx.oss-xxx.aliyuncs.com/xxx.png?Expires=xxx",
                                  "type": "image"
                              }
                          ],
                          "role": "assistant"
                      }
                  }
              ],
              "finished": true
          },
          "usage": {
              "image_count": 1,
              "input_tokens": 10867,
              "output_tokens": 2,
              "size": "1488*704",
              "total_tokens": 10869
          },
          "request_id": "71dfc3c6-f796-9972-97e4-bc4efc4faxxx"
      }
      ```
    </CodeGroup>
  </Tab>

  <Tab title="异步调用">
    <Note>请确保 DashScope Python SDK 版本不低于 `1.25.15`，DashScope Java SDK 版本不低于 `2.22.13`。</Note>

    <CodeGroup>
      ```python
      import os
      import dashscope
      from dashscope.aigc.image_generation import ImageGeneration
      from dashscope.api_entities.dashscope_response import Message
      from http import HTTPStatus

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      # 如果未设置环境变量，请将下行替换为：api_key="sk-xxx"
      api_key = os.getenv("DASHSCOPE_API_KEY")

      # 创建异步任务
      def create_async_task():
        print("正在创建异步任务...")
        message = Message(
          role="user",
          content=[
            {'text': '把图2的涂鸦喷绘在图1的汽车上'},
            {'image': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp'},
            {'image': 'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp'}
          ]
        )
        response = ImageGeneration.async_call(
          model="wan2.7-image-pro",
          api_key=api_key,
          messages=[message],
          watermark=False,
          n=1,
          size="2K"
        )

        if response.status_code == 200:
          print("任务创建成功:", response)
          return response
        else:
          raise Exception(f"任务创建失败: {response.code} - {response.message}")

      # 等待任务完成
      def wait_for_completion(task_response):
        print("等待任务完成...")
        status = ImageGeneration.wait(task=task_response, api_key=api_key)

        if status.output.task_status == "SUCCEEDED":
          print("任务成功!")
          print("响应:", status)
        else:
          raise Exception(f"任务失败，状态: {status.output.task_status}")

      # 查询异步任务状态
      def fetch_task_status(task):
        print("查询任务状态...")
        status = ImageGeneration.fetch(task=task, api_key=api_key)

        if status.status_code == HTTPStatus.OK:
          print("任务状态:", status.output.task_status)
          print("响应详情:", status)
        else:
          print(f"查询失败: {status.code} - {status.message}")

      # 取消异步任务
      def cancel_task(task):
        print("取消任务...")
        response = ImageGeneration.cancel(task=task, api_key=api_key)

        if response.status_code == HTTPStatus.OK:
          print("任务已取消:", response.output.task_status)
        else:
          print(f"取消失败: {response.code} - {response.message}")

      # 主流程
      if __name__ == "__main__":
        task = create_async_task()
        wait_for_completion(task)
      ```

      ```json
      {
        "status_code": 200,
        "request_id": "4fb3050f-de57-4a24-84ff-e37ee5xxxxxx",
        "code": "",
        "message": "",
        "output": {
          "text": null,
          "finish_reason": null,
          "choices": null,
          "audio": null,
          "task_id": "127ec645-118f-4884-955d-0eba8dxxxxxx",
          "task_status": "PENDING"
        },
        "usage": {
          "input_tokens": 0,
          "output_tokens": 0,
          "characters": 0
        }
      }
      ```

      ```java
      import com.alibaba.dashscope.aigc.imagegeneration.*;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;
      import com.alibaba.dashscope.utils.JsonUtils;

      import java.util.Arrays;
      import java.util.Collections;

      /**
       * wan2.7-image-pro 图像编辑 - 异步调用示例
       */
      public class Main {

        static {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        }

        // 如果未配置环境变量，请将下行替换为：apiKey="sk-xxx"
        static String apiKey = System.getenv("DASHSCOPE_API_KEY");

        public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException {
          // 构建多图输入消息
          ImageGenerationMessage message = ImageGenerationMessage.builder()
            .role("user")
            .content(Arrays.asList(
              // 支持多图输入，提供多张参考图
              Collections.singletonMap("text", "把图2的涂鸦喷绘在图1的汽车上"),
              Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"),
              Collections.singletonMap("image", "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp")
            )).build();

          ImageGenerationParam param = ImageGenerationParam.builder()
            .apiKey(apiKey)
            .model("wan2.7-image-pro")
            .n(1)
            .size("2K")
            .messages(Arrays.asList(message))
            .build();

          ImageGeneration imageGeneration = new ImageGeneration();
          ImageGenerationResult result = null;
          try {
            System.out.println("---异步调用图像编辑，正在创建任务----");
            result = imageGeneration.asyncCall(param);
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
          }
          System.out.println("任务创建结果:");
          System.out.println(JsonUtils.toJson(result));

          String taskId = result.getOutput().getTaskId();
          // 等待任务完成
          waitTask(taskId);
        }

        public static void waitTask(String taskId) throws ApiException, NoApiKeyException {
          ImageGeneration imageGeneration = new ImageGeneration();
          System.out.println("\n---等待任务完成----");
          ImageGenerationResult result = imageGeneration.wait(taskId, apiKey);
          System.out.println("任务完成结果:");
          System.out.println(JsonUtils.toJson(result));
        }

        public static void main(String[] args) {
          try {
            asyncCall();
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
        }
      }
      ```

      ```json
      {
        "request_id": "4fb3050f-de57-4a24-84ff-e37ee5xxxxxx",
        "output": {
          "task_id": "127ec645-118f-4884-955d-0eba8dxxxxxx",
          "task_status": "PENDING"
        }
      }
      ```

      ```bash
      curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
      --header 'Content-Type: application/json' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'X-DashScope-Async: enable' \
      --data '{
        "model": "wan2.7-image-pro",
        "input": {
          "messages": [
            {
              "role": "user",
              "content": [
                {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/pjeqdf/car.webp"},
                {"image": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20251229/xsunlm/paint.webp"},
                {"text": "把图2的涂鸦喷绘在图1的汽车上"}
              ]
            }
          ]
        },
        "parameters": {
          "size": "2K",
          "n": 1,
          "watermark": false
        }
      }'
      ```

      ```json
      {
        "output": {
          "task_id": "127ec645-118f-4884-955d-0eba8dxxxxxx",
          "task_status": "PENDING"
        },
        "request_id": "4fb3050f-de57-4a24-84ff-e37ee5xxxxxx"
      }
      ```
    </CodeGroup>
  </Tab>
</Tabs>

<Accordion title="点击查看wan2.5-i2i-preview调用示例">
  wan2.5-i2i-preview使用不同的API端点和参数传入方式，其调用示例如下：

  ### 同步调用（wan2.5）

  <Note>请确保 DashScope Python SDK 版本不低于 `1.25.2`，DashScope Java SDK 版本不低于 `2.22.2`。</Note>

  <CodeGroup>
    ```python
    import base64
    import mimetypes
    from http import HTTPStatus
    from urllib.parse import urlparse, unquote
    from pathlib import PurePosixPath

    import dashscope
    import requests
    from dashscope import ImageSynthesis
    import os

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    # 如果未设置环境变量，请将下行替换为：api_key="sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")

    # --- 输入图片：Base64编码 ---
    # Base64格式：data:{MIME_type};base64,{base64_data}
    def encode_file(file_path):
      mime_type, _ = mimetypes.guess_type(file_path)
      if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("不支持或无法识别的图片格式")
      with open(file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
      return f"data:{mime_type};base64,{encoded_string}"

    """
    图像输入方式：
    选择以下其中一种：

    1. 公网URL — 适用于公开可访问的图片
    2. 本地文件 — 适用于本地开发和测试
    3. Base64编码 — 适用于私有图片或需要加密传输的场景
    """

    # [方式一] 公网图片URL
    image_url_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"
    image_url_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"

    # [方式二] 本地文件（支持绝对路径和相对路径）
    # 格式：file:// + 文件路径
    # 示例（绝对路径）：
    # image_url_1 = "file://" + "/path/to/your/image_1.png"     # Linux/macOS
    # image_url_2 = "file://" + "C:/path/to/your/image_2.png"  # Windows
    # 示例（相对路径）：
    # image_url_1 = "file://" + "./image_1.png"
    # image_url_2 = "file://" + "./image_2.png"

    # [方式三] Base64编码图片
    # image_url_1 = encode_file("./image_1.png")
    # image_url_2 = encode_file("./image_2.png")

    print('----同步调用，请稍候----')
    rsp = ImageSynthesis.call(api_key=api_key,
                              model="wan2.5-i2i-preview",
                              prompt="将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                              images=[image_url_1, image_url_2],
                              negative_prompt="",
                              n=1,
                              # size="1280*1280",
                              prompt_extend=True,
                              watermark=False,
                              seed=12345)
    print('response: %s' % rsp)
    if rsp.status_code == HTTPStatus.OK:
      # 保存图片到当前目录
      for result in rsp.output.results:
        file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
        with open('./%s' % file_name, 'wb+') as f:
          f.write(requests.get(result.url).content)
    else:
      print('同步调用失败, status_code: %s, code: %s, message: %s' %
            (rsp.status_code, rsp.code, rsp.message))
    ```

    ```json
    {
        "status_code": 200,
        "request_id": "8ad45834-4321-44ed-adf5-xxxxxx",
        "code": null,
        "message": "",
        "output": {
            "task_id": "3aff9ebd-35fc-4339-98a3-xxxxxx",
            "task_status": "SUCCEEDED",
            "results": [
                {
                    "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                    "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                    "actual_prompt": "将蓝色闹钟从图1放到图2餐桌花瓶右侧，靠近桌布边缘。保持闹钟面向镜头，平行于桌面，带自然投影。"
                }
            ],
            "submit_time": "2025-10-23 16:18:16.009",
            "scheduled_time": "2025-10-23 16:18:16.040",
            "end_time": "2025-10-23 16:19:09.591",
            "task_metrics": {
                "TOTAL": 1,
                "FAILED": 0,
                "SUCCEEDED": 1
            }
        },
        "usage": {
            "image_count": 1
        }
    }
    ```

    ```java
    // Copyright (c) Alibaba, Inc. and its affiliates.

    import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
    import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
    import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.alibaba.dashscope.utils.Constants;
    import com.alibaba.dashscope.utils.JsonUtils;

    import java.io.IOException;
    import java.nio.file.Files;
    import java.nio.file.Path;
    import java.nio.file.Paths;
    import java.util.*;

    public class Image2Image {

      static {
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
      }

      // 如果未配置环境变量，请将下行替换为：apiKey="sk-xxx"
      static String apiKey = System.getenv("DASHSCOPE_API_KEY");

      /**
       * 图像输入方式：选择以下其中一种
       *
       * 1. 公网URL — 适用于公开可访问的图片
       * 2. 本地文件 — 适用于本地开发和测试
       * 3. Base64编码 — 适用于私有图片或需要加密传输的场景
       */

      // [方式一] 公网URL
      static String imageUrl_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp";
      static String imageUrl_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp";

      // [方式二] 本地文件路径（file://+绝对路径 或 file:///+绝对路径）
      // static String imageUrl_1 = "file://" + "/your/path/to/image_1.png";    // Linux/macOS
      // static String imageUrl_2 = "file:///" + "C:/your/path/to/image_2.png";  // Windows

      // [方式三] Base64编码
      // static String imageUrl_1 = encodeFile("/your/path/to/image_1.png");
      // static String imageUrl_2 = encodeFile("/your/path/to/image_2.png");

      // 待编辑的图片列表
      static List<String> imageUrls = new ArrayList<>();
      static {
        imageUrls.add(imageUrl_1);
        imageUrls.add(imageUrl_2);
      }

      public static void syncCall() {
        // 设置参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        ImageSynthesisParam param =
          ImageSynthesisParam.builder()
            .apiKey(apiKey)
            .model("wan2.5-i2i-preview")
            .prompt("将图1中的闹钟放置到图2的餐桌的花瓶旁边位置")
            .images(imageUrls)
            .n(1)
             //.size("1280*1280")
            .negativePrompt("")
            .parameters(parameters)
            .build();

        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
          System.out.println("---同步调用，请稍候----");
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
          throw new IllegalArgumentException("不支持或无法识别的图片格式");
        }
        // 读取文件并编码
        byte[] fileBytes = null;
        try{
          fileBytes = Files.readAllBytes(path);
        } catch (IOException e) {
          throw new IllegalArgumentException("无法读取文件: " + filePath);
        }

        String encodedString = Base64.getEncoder().encodeToString(fileBytes);
        return "data:" + mimeType + ";base64," + encodedString;
      }

      public static void main(String[] args) {
        syncCall();
      }
    }
    ```

    ```json
    {
        "request_id": "d362685b-757f-4eac-bab5-xxxxxx",
        "output": {
            "task_id": "bfa7fc39-3d87-4fa7-b1e6-xxxxxx",
            "task_status": "SUCCEEDED",
            "results": [
                {
                    "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                    "actual_prompt": "将蓝色闹钟从图1放到图2餐桌花瓶右侧，靠近桌布边缘。保持闹钟面向镜头，平行于花瓶。",
                    "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"
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

  ### 异步调用（wan2.5）

  <Note>请确保 DashScope Python SDK 版本不低于 `1.25.2`，DashScope Java SDK 版本不低于 `2.22.2`。</Note>

  <CodeGroup>
    ```python
    import os
    from http import HTTPStatus
    from urllib.parse import urlparse, unquote
    from pathlib import PurePosixPath
    import dashscope
    import requests
    from dashscope import ImageSynthesis

    dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

    # 如果未设置环境变量，请将下行替换为：api_key="sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")

    # 公网图片URL
    image_url_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp"
    image_url_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"

    def async_call():
      print('----创建任务----')
      task_info = create_async_task()
      print('----等待任务----')
      wait_async_task(task_info)

    # 创建异步任务
    def create_async_task():
      rsp = ImageSynthesis.async_call(api_key=api_key,
                                      model="wan2.5-i2i-preview",
                                      prompt="将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                                      images=[image_url_1, image_url_2],
                                      negative_prompt="",
                                      n=1,
                                      # size="1280*1280",
                                      prompt_extend=True,
                                      watermark=False,
                                      seed=12345)
      print(rsp)
      if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
      else:
        print('失败, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))
      return rsp

    # 等待异步任务完成
    def wait_async_task(task):
      rsp = ImageSynthesis.wait(task=task, api_key=api_key)
      print(rsp)
      if rsp.status_code == HTTPStatus.OK:
        print(rsp.output)
        # 保存文件到当前目录
        for result in rsp.output.results:
          file_name = PurePosixPath(unquote(urlparse(result.url).path)).parts[-1]
          with open('./%s' % file_name, 'wb+') as f:
            f.write(requests.get(result.url).content)
      else:
        print('失败, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

    # 查询异步任务状态
    def fetch_task_status(task):
      status = ImageSynthesis.fetch(task=task, api_key=api_key)
      print(status)
      if status.status_code == HTTPStatus.OK:
        print(status.output.task_status)
      else:
        print('失败, status_code: %s, code: %s, message: %s' %
              (status.status_code, status.code, status.message))

    # 取消异步任务，仅PENDING状态的任务可以取消
    def cancel_task(task):
      rsp = ImageSynthesis.cancel(task=task, api_key=api_key)
      print(rsp)
      if rsp.status_code == HTTPStatus.OK:
        print(rsp.output.task_status)
      else:
        print('失败, status_code: %s, code: %s, message: %s' %
              (rsp.status_code, rsp.code, rsp.message))

    if __name__ == '__main__':
      async_call()
    ```

    ```json
    {
        "status_code": 200,
        "request_id": "31b04171-011c-96bd-ac00-f0383b669cc7",
        "code": "",
        "message": "",
        "output": {
            "task_id": "4f90cf14-a34e-4eae-xxxxxxxx",
            "task_status": "PENDING",
            "results": []
        },
        "usage": null
    }
    ```

    ```json
    {
        "status_code": 200,
        "request_id": "8ad45834-4321-44ed-adf5-xxxxxx",
        "code": null,
        "message": "",
        "output": {
            "task_id": "3aff9ebd-35fc-4339-98a3-xxxxxx",
            "task_status": "SUCCEEDED",
            "results": [
                {
                    "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx",
                    "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                    "actual_prompt": "将蓝色闹钟从图1放到图2餐桌花瓶右侧，靠近桌布边缘。保持闹钟面向镜头，平行于桌面，带自然投影。"
                }
            ],
            "submit_time": "2025-10-23 16:18:16.009",
            "scheduled_time": "2025-10-23 16:18:16.040",
            "end_time": "2025-10-23 16:19:09.591",
            "task_metrics": {
                "TOTAL": 1,
                "FAILED": 0,
                "SUCCEEDED": 1
            }
        },
        "usage": {
            "image_count": 1
        }
    }
    ```

    ```java
    // Copyright (c) Alibaba, Inc. and its affiliates.

    import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesis;
    import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisListResult;
    import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisParam;
    import com.alibaba.dashscope.aigc.imagesynthesis.ImageSynthesisResult;
    import com.alibaba.dashscope.exception.ApiException;
    import com.alibaba.dashscope.exception.NoApiKeyException;
    import com.alibaba.dashscope.task.AsyncTaskListParam;
    import com.alibaba.dashscope.utils.Constants;
    import com.alibaba.dashscope.utils.JsonUtils;

    import java.util.ArrayList;
    import java.util.HashMap;
    import java.util.List;
    import java.util.Map;

    public class Image2Image {

      static {
        Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
      }

      // 如果未配置环境变量，请将下行替换为：apiKey="sk-xxx"
      static String apiKey = System.getenv("DASHSCOPE_API_KEY");

      // 公网URL
      static String imageUrl_1 = "https://img.alicdn.com/imgextra/i3/O1CN0157XGE51l6iL9441yX_!!6000000004770-49-tps-1104-1472.webp";
      static String imageUrl_2 = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp";

      // 待编辑的图片列表
      static List<String> imageUrls = new ArrayList<>();
      static {
        imageUrls.add(imageUrl_1);
        imageUrls.add(imageUrl_2);
      }

      public static void asyncCall() {
        // 设置参数
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("prompt_extend", true);
        parameters.put("watermark", false);
        parameters.put("seed", 12345);

        ImageSynthesisParam param =
          ImageSynthesisParam.builder()
            .apiKey(apiKey)
            .model("wan2.5-i2i-preview")
            .prompt("将图1中的闹钟放置到图2的餐桌的花瓶旁边位置")
            .images(imageUrls)
            .n(1)
            //.size("1280*1280")
            .negativePrompt("")
            .parameters(parameters)
            .build();
        ImageSynthesis imageSynthesis = new ImageSynthesis();
        ImageSynthesisResult result = null;
        try {
          System.out.println("---异步调用，请稍候----");
          result = imageSynthesis.asyncCall(param);
        } catch (ApiException | NoApiKeyException e){
          throw new RuntimeException(e.getMessage());
        }

        System.out.println(JsonUtils.toJson(result));

        String taskId = result.getOutput().getTaskId();

        System.out.println("taskId=" + taskId);

        try {
          result = imageSynthesis.wait(taskId, apiKey);
        } catch (ApiException | NoApiKeyException e){
          throw new RuntimeException(e.getMessage());
        }
        System.out.println(JsonUtils.toJson(result));
        System.out.println(JsonUtils.toJson(result.getOutput()));
      }

      public static void listTask() throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        AsyncTaskListParam param = AsyncTaskListParam.builder().build();
        param.setApiKey(apiKey);
        ImageSynthesisListResult result = is.list(param);
        System.out.println(result);
      }

      public void fetchTask(String taskId) throws ApiException, NoApiKeyException {
        ImageSynthesis is = new ImageSynthesis();
        // 如果已设置 DASHSCOPE_API_KEY 环境变量，apiKey 可以为空
        ImageSynthesisResult result = is.fetch(taskId, apiKey);
        System.out.println(result.getOutput());
        System.out.println(result.getUsage());
      }

      public static void main(String[] args) {
        asyncCall();
      }
    }
    ```

    ```json
    {
        "request_id": "5dbf9dc5-4f4c-9605-85ea-542f97709ba8",
        "output": {
            "task_id": "7277e20e-aa01-4709-xxxxxxxx",
            "task_status": "PENDING"
        }
    }
    ```

    ```json
    {
        "request_id": "d362685b-757f-4eac-bab5-xxxxxx",
        "output": {
            "task_id": "bfa7fc39-3d87-4fa7-b1e6-xxxxxx",
            "task_status": "SUCCEEDED",
            "results": [
                {
                    "orig_prompt": "将图1中的闹钟放置到图2的餐桌的花瓶旁边位置",
                    "actual_prompt": "将蓝色闹钟从图1放到图2餐桌花瓶右侧，靠近桌布边缘。保持闹钟面向镜头，平行于花瓶。",
                    "url": "https://dashscope-result-sh.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"
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
</Accordion>

## 模型选型

- **wan2.7-image-pro、wan2.7-image**（推荐）：适合对编辑精度要求高、或需要生成多张内容连贯图像的场景。

  - [精准局部编辑](#4-交互式精准编辑)：框选图中指定区域，对该区域的对象进行移动、替换或添加新元素，适用于电商修图、设计稿调整。

  - 多格连续图生成：一次输出多张风格统一的图像，适用于漫画分镜、产品系列图、故事连环图。

- **wan2.6-image**：适合图文混排或带多张参考图的风格化编辑场景，支持在生成图像时生成对应文字内容，最多支持 4 张参考图输入。

- **wan2.5-i2i-preview**：适合简单的图像编辑和多图融合。

各模型的输入和输出规格见[输入图像规格](#输入图像规格)和[设置输出图像分辨率](#3-设置输出图像分辨率)。

## 效果展示

### 图生组图

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "40%", paddingBottom: "8px"}}>输入图像</th>
      <th style={{textAlign: "left", width: "60%", paddingBottom: "8px"}}>输出图像</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="输入人像" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1064359.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="output" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1064360.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "33%"}}>
        <img alt="输入人像2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1064362.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", width: "67%"}}>
        <img alt="output" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1064361.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

### 交互式编辑

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "70%", paddingBottom: "8px"}}>输入图像</th>
      <th style={{textAlign: "left", width: "30%", paddingBottom: "8px"}}>输出图像</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="交互式编辑输入2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/8163205771/p1064355.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="交互式编辑输出2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1064356.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        将图1中框选的图案放置到图二中框选处
      </td>
    </tr>
  </tbody>
</table>

### 多图融合

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "69%", paddingBottom: "8px"}}>输入图像</th>
      <th style={{textAlign: "left", width: "31%", paddingBottom: "8px"}}>输出图像</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="多图融合输入1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039962.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="多图融合输出1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039963.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        给图1的男生和图2的狗拍一张写真，男生搂着这只狗，人和狗都很开心，摄影棚柔和灯光，蓝色纹理背景
      </td>
    </tr>
  </tbody>
</table>

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "75%"}}>
        <img alt="多图融合输入2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039968.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", width: "25%"}}>
        <img alt="多图融合输出2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039971.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        给图1的裙子按照图2鸟的颜色进行配色，充满艺术感，衣服款式不变，模特不变
      </td>
    </tr>
  </tbody>
</table>

### 主体特征保持

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px"}}>输入图像</th>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px"}}>输出图像</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="主体特征保持输入2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/8163205771/p1040012.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="主体特征保持输出2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1040013.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

### 检测和分割

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px"}}>输入图像</th>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px"}}>输出图像</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="检测分割输入1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1040006.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="检测分割输出1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1040007.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        检测图片中的笔记本电脑和闹钟，画框并标注"laptop"和"clock"
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="检测分割输入2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1040008.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="检测分割输出2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1040009.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        分割图片中的玻璃杯
      </td>
    </tr>
  </tbody>
</table>

### 提取元素

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>输入图像</th>
      <th style={{textAlign: "left", width: "67%", paddingBottom: "8px"}}>输出图像</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="提取元素输入" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1040000.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="提取元素输出" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1040001.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        从上传照片中提取穿搭单品，将它们以平铺展示的方式排列在纯白背景上，保持真实细节与材质质感，时尚电商风格，适合服装展示。
      </td>
    </tr>
  </tbody>
</table>

### 文本编辑

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px"}}>输入图像</th>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px"}}>输出图像</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="文本编辑输入1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/8163205771/p1039976.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="文本编辑输出1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039977.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        去除全图水印
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="文本编辑输入2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039978.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="文本编辑输出2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039979.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        用手在沙滩上随意的写上"Time for Holiday?"
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="文本编辑输入3" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039980.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="文本编辑输出3" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039981.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        把18改成29，把JUNE改成SEPTEMBER
      </td>
    </tr>
  </tbody>
</table>

### 镜头与视角编辑

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px"}}>输入图像</th>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px"}}>输出图像</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="镜头编辑输入1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039991.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="镜头编辑输出1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039992.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        保持人物的特征不变，生成正视图、侧视图和背视图
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="镜头编辑输入2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/9163205771/p1039995.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="镜头编辑输出2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/8163205771/p1039996.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        用鱼眼镜头重新拍摄这张照片
      </td>
    </tr>
  </tbody>
</table>

## 输入说明

### 输入图像规格

| **规格** | **wan2.7-image-pro、wan2.7-image** | **wan2.6-image**               | **wan2.5-i2i-preview**         |
| ------ | --------------------------------- | ------------------------------ | ------------------------------ |
| 输入图像数量 | 0～9 张（0张对应文生图模式）                  | 图像编辑 1～4 张 / 图文混排 0～1 张        | 1～3 张                          |
| 图片格式   | JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP    | JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP | JPEG、JPG、PNG（不支持透明通道）、BMP、WEBP |
| 图片宽高范围 | \[240, 8000] 像素                   | \[240, 8000] 像素                | \[384, 5000] 像素                |
| 文件大小   | ≤ 20MB                            | ≤ 10MB                         | ≤ 10MB                         |
| 宽高比    | \[1:8, 8:1]                       | 不限                             | \[1:4, 4:1]                    |

### 图像输入顺序

多图输入时，按照数组中的顺序定义图像顺序。因此，提示词引用的图像编号需要**与图像数组中的顺序一一对应**，例如：数组中的第一张图片为"图1"，第二张为"图2"，或者使用标记形式如"\[图1]"、"\[图2]"。

```json
{
    "content": [
        {"text": "编辑指令，如：将图1中的闹钟放置到图2的餐桌的花瓶旁边位置"},
        {"image": "https://example.com/image1.png"},
        {"image": "https://example.com/image2.png"}
    ]
}
```

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "27%", paddingBottom: "8px"}}>**输入图像1**</th>
      <th style={{textAlign: "left", width: "20%", paddingBottom: "8px"}}>**输入图像2**</th>
      <th style={{textAlign: "left", width: "27%", paddingBottom: "8px"}}>**输出图像**</th>

      <th style={{textAlign: "left", width: "27%", paddingBottom: "8px"}} />
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top"}}>
        <img alt="image (19)-转换自-png" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3509593671/p1025838.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        图1
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="image (20)-转换自-png" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3509593671/p1025839.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        图2
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="04e0fc39-7ad6-41e0-9df9-1f69ac3ce825-转换自-png" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3509593671/p1021092.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        提示词：把图1移动到图2上
      </td>

      <td style={{verticalAlign: "top"}}>
        <img alt="36ed450d-bd54-4169-b13f-3d0f26d9d360-转换自-png" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3509593671/p1021093.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />

        提示词：把图2移动到图1上
      </td>
    </tr>
  </tbody>
</table>

### 图像传入方式

支持通过以下方式传入图像：

<Accordion title="方式一：公网URL">
  ```python
  # 使用公网可访问的图片URL
  image_url = "https://example.com/your-image.png"
  ```

  ```bash
  # 在curl中，直接在JSON body中传入URL
  "image": "https://example.com/your-image.png"
  ```
</Accordion>

<Accordion title="方式二：Base64编码">
  ```python
  import os
  import base64
  import mimetypes

  # 格式为 data:{mime_type};base64,{base64_data}
  def encode_file(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    with open(file_path, "rb") as image_file:
      encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return f"data:{mime_type};base64,{encoded_string}"

  # 调用编码函数，请将 "/path/to/your/image.png" 替换为您的本地图片文件路径，否则无法运行
  image = encode_file("/path/to/your/image.png")
  ```
</Accordion>

<Accordion title="方式三：本地文件路径（仅限SDK）">
  ```python
  # 本地文件路径格式：file:// + 绝对路径
  # Linux/macOS 示例：
  image_url = "file://" + "/path/to/your/image.png"
  # Windows 示例：
  image_url = "file:///" + "C:/path/to/your/image.png"

  # 相对路径示例：
  image_url = "file://" + "./your-image.png"
  ```

  此方式仅支持 SDK 调用。curl 请求需使用公网URL或Base64编码。
</Accordion>

## 关键能力

### 1. 指令遵循（提示词）

参数：`messages.content.text`或`input.prompt`（必选）、`negative_prompt`（可选）。

| **参数**           | **wan2.7-image-pro、wan2.7-image** | **wan2.6-image** | **wan2.5-i2i-preview** |
| ---------------- | --------------------------------- | ---------------- | ---------------------- |
| text             | 必选，最多5000字符                       | 必选，最多2000字符      | 不支持                    |
| prompt           | 不支持                               | 不支持              | 必选，最多2000字符            |
| negative\_prompt | 不支持                               | 支持，最多500字符       | 支持，最多500字符             |

### 2. 开启prompt智能改写

参数：`parameters.prompt_extend`（bool，**默认为 true**）。

此功能可自动扩展和优化较短的Prompt，提升输出图像效果。开启此功能会增加额外耗时。

| **参数**         | **wan2.7-image-pro、wan2.7-image** | **wan2.6-image** | **wan2.5-i2i-preview** |
| -------------- | --------------------------------- | ---------------- | ---------------------- |
| prompt\_extend | 不支持                               | 支持（仅图像编辑模式）      | 支持                     |

### 3. 设置输出图像分辨率

参数：`parameters.size`（string），格式为`"宽*高"`。

| **参数** | **wan2.7-image-pro、wan2.7-image**                                                                                                                                                                                                                        | **wan2.6-image**                                                                                                                                                                                                                                           | **wan2.5-i2i-preview**                                                                                                        |
| ------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| size   | **方式一：指定输出图片的分辨率（推荐）** 编辑模式（传入至少一张图片），可选的输出分辨率档位：`1K`、`2K`（默认）。`1K`：输出总像素接近 1024\*1024，宽高比与最后一张输入图像一致。`2K`：输出总像素接近 2048\*2048，宽高比与最后一张输入图像一致。**方式二：指定生成图像的宽高像素值** 总像素在 \[768\*768, 2048\*2048] 之间，宽高比范围为 \[1:8, 8:1]。仅文生图场景的 wan2.7-image-pro 支持 4K 分辨率。 | **方式一：参考输入图比例（推荐）** 编辑模式（`enable_interleave=false`），可选的输出分辨率档位：`1K`（默认）、`2K`。`1K`：输出总像素接近 1280\*1280，宽高比与最后一张输入图像一致。`2K`：输出总像素接近 2048\*2048，宽高比与最后一张输入图像一致。**方式二：指定生成图像的宽高像素值** 总像素在 \[768\*768, 2048\*2048] 之间，宽高比范围为 \[1:4, 4:1]。实际输出图像的像素值为接近指定值的16的倍数。 | **仅支持指定生成图像的宽高像素值** 总像素在 \[768\*768, 1280\*1280] 之间，宽高比范围为 \[1:4, 4:1]。若未指定`size`，系统将默认生成总像素为 `1280*1280` 的图像，宽高比与最后一张输入图像一致。 |

### 4. 交互式精准编辑

通过 `parameters.bbox_list` 参数框选图中需要编辑的物品或位置，实现更准确的编辑效果。**仅 wan2.7-image-pro、wan2.7-image 支持此功能。**

- 对应关系：列表长度必须与输入图片数量一致。若某张图片无需编辑，需要在对应位置传入空列表 `[]`。
- 坐标格式：`[x1, y1, x2, y2]`（左上角 x, 左上角 y, 右下角 x, 右下角 y），使用原图绝对像素坐标，左上角对应（0，0），x 轴向右，y 轴向下。
- 数量限制：单张图片最多支持 2 个边界框。

示例：输入 3 张图片，其中第 2 张无框选，第 1 张有两个框选：

```json
[
  [[0, 0, 12, 12], [25, 25, 100, 100]],
  [],
  [[10, 10, 50, 50]]
]
```

<Accordion title="如何确定编辑区域坐标">
  **方法一：OpenCV 画框**

  在图片上拖拽鼠标画框，精准直观：

  ```python
  # 安装依赖：pip install opencv-python
  import cv2
  import urllib.request

  # 下载示例图片（替换为您自己的图片 URL 或本地路径）
  image_url = "https://img.alicdn.com/imgextra/i3/O1CN01SfG4J41UYn9WNt4X1_!!6000000002530-49-tps-1696-960.webp"
  urllib.request.urlretrieve(image_url, "example.webp")

  # 读取图片并弹出交互窗口
  img = cv2.imread("example.webp")
  # 在弹出的窗口中用鼠标拖拽画框，按 Enter 确认选区，按 Esc 取消
  x, y, w, h = cv2.selectROI("Draw bounding box (Enter=confirm, Esc=cancel)", img)
  cv2.destroyAllWindows()

  # 将 OpenCV 返回的 (x, y, w, h) 转换为 bbox_list 所需的 [x1, y1, x2, y2] 格式
  bbox = [x, y, x + w, y + h]
  print(f"框选坐标: {bbox}")
  ```

  **方法二：视觉理解模型**

  通过 qwen3.7-plus 自动识别目标区域坐标，用自然语言描述目标即可获取坐标：

  ````python
  # 安装依赖：pip install dashscope pillow
  import os
  import json
  from dashscope import MultiModalConversation
  import dashscope
  from PIL import Image
  import urllib.request

  dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"

  def get_bbox_list(image, prompt):
    """
    通过 qwen3.7-plus 识别图片中的目标区域，返回绝对像素坐标列表。
    """
    full_prompt = (
      prompt + "\n"
      "请根据以上描述，返回对应区域的坐标。\n"
      "最多返回2个区域，优先返回最匹配的目标。\n"
      "严格按照JSON二维列表格式返回：[[x1, y1, x2, y2], ...]\n"
      "每组坐标：[左上角x, 左上角y, 右下角x, 右下角y]\n"
      "使用原图绝对像素坐标，左上角为(0,0)，x轴向右，y轴向下。\n"
      "如果只有一个区域，也必须使用二维列表：[[x1, y1, x2, y2]]\n"
      "只返回JSON列表，不要返回其他任何内容。"
    )

    messages = [
      {'role': 'user',
       'content': [
         {'image': image},
         {'text': full_prompt}
       ]}
    ]

    response = MultiModalConversation.call(
      api_key=os.getenv('DASHSCOPE_API_KEY'),
      model='qwen3.7-plus',
      messages=messages,
    )

    text = response.output.choices[0].message.content[0]["text"]
    text = text.replace("```json", "").replace("```", "").strip()
    coords = json.loads(text)

    if coords and not isinstance(coords[0], list):
      coords = [coords]

    # 获取图片尺寸，用于坐标转换
    if image.startswith("file://"):
      local_path = image[len("file://"):]
      img = Image.open(local_path)
    else:
      tmp_path = "temp_bbox_image"
      urllib.request.urlretrieve(image, tmp_path)
      img = Image.open(tmp_path)
    width, height = img.size

    # 模型返回归一化坐标 [0, 999]，转换为绝对像素坐标
    bbox_list = []
    for box in coords:
      bbox_list.append([
        int(box[0] / 1000 * width),
        int(box[1] / 1000 * height),
        int(box[2] / 1000 * width),
        int(box[3] / 1000 * height)
      ])

    return bbox_list

  # === 使用示例 ===
  image_url = "https://img.alicdn.com/imgextra/i3/O1CN01ewUWhg1eS3VqJ3wap_!!6000000003869-49-tps-2048-2048.webp"

  # 按名称选取目标
  bbox = get_bbox_list(image_url, "咖啡杯")

  # 按位置描述选取目标
  bbox = get_bbox_list(image_url, "盘子正中间的水果")
  ````
</Accordion>

## 计费与限流

- 模型免费额度和计费单价请参见[模型列表与价格](/developer-guides/getting-started/pricing)。

- 模型限流请参见[限流](/developer-guides/administration/rate-limits)。

- 计费说明：
  - 按成功生成的**图像张数**计费。仅当接口返回`task_status`为`SUCCEEDED`并成功生成图像后，才会计费。
  - 模型调用失败或处理错误不产生任何费用，也不消耗[免费额度](/resources/free-quota)。

## API参考

各模型使用不同的端点和请求结构：

| **模型**                                           | **端点**                                                                                                                                                                                            |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `wan2.7-image`、`wan2.7-image-pro`、`wan2.6-image` | 同步接口：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation`<br />异步接口：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation` |
| `wan2.5-i2i-preview`                             | 异步接口：`POST https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis`                                                                                                       |

- `wan2.7` / `wan2.6`：`messages` 格式，在 `messages[].content` 数组中，通过 `image` 传入图像，通过 `text` 传入提示词。
- `wan2.5`：通过 `input.images` 数组传入图像，通过 `input.prompt` 传入提示词。

输入和输出参数请参见 [Wan 2.7 API参考](/api-reference/image-generation/wan27-image-gen-edit/create-task)、[Wan 2.6 API参考](/api-reference/image-generation/wan26-image-gen-edit/create-task) 和 [Wan 2.5 API参考](/api-reference/image-generation/wan25-general-image-editing/create-task)。
