> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 通用视频编辑

> 重绘、延展与编辑

**快捷链接**：API 参考：[wan2.7](/api-reference/video-generation/wan27-video-editing/create-task)、[wan2.1](/api-reference/video-generation/wan-general-video-editing/create-task)

## 可用模型

**支持的模型**：

| **模型**                | **功能**                         | **输入模态** | **输出视频规格**                                  |
| --------------------- | ------------------------------ | -------- | ------------------------------------------- |
| wan2.7-videoedit `推荐` | 音频（自动/保留原声）、风格迁移、物体替换、参考图编辑    | 文本、图片、视频 | 分辨率：720P、1080P。时长：最长 10 秒。30 fps，MP4（H.264） |
| wan2.1-vace-plus      | 视频无音频。多图参考、视频重绘、局部编辑、视频延展、画面扩展 | 文本、图片、视频 | 分辨率：720P。时长：最长 5 秒。30 fps，MP4（H.264 编码）     |

## Wan 2.7 视频编辑

通过文本提示词和可选的参考图，以最高 1080P 分辨率编辑视频——支持风格转换、物体替换，以及将参考图中的内容迁移到源视频中。使用统一模型，无需设置 `function` 参数。

### 参数说明（wan2.7）

| **参数**                     | **类型**  | **必选** | **说明**                                                 |
| -------------------------- | ------- | ------ | ------------------------------------------------------ |
| `model`                    | string  | 是      | `"wan2.7-videoedit"`                                   |
| `input.prompt`             | string  | 否      | 最多 5,000 字符。描述期望的编辑效果。                                 |
| `input.negative_prompt`    | string  | 否      | 最多 500 字符。需要排除的内容。                                     |
| `input.media`              | array   | 是      | 必须包含一个 `video` 项。可选包含最多 4 个 `reference_image` 项。       |
| `parameters.resolution`    | string  | 否      | `"720P"` 或 `"1080P"`（默认）。                              |
| `parameters.ratio`         | string  | 否      | `"16:9"`、`"9:16"`、`"1:1"`、`"4:3"`、`"3:4"`。默认与输入视频比例一致。 |
| `parameters.duration`      | integer | 否      | `0` = 保持输入视频完整时长（默认）。`2`-`10` = 截取输入视频指定时长。            |
| `parameters.audio_setting` | string  | 否      | `"auto"`（默认，模型自动决定）或 `"origin"`（保留原声）。                 |
| `parameters.prompt_extend` | boolean | 否      | 默认值：`true`。                                            |
| `parameters.watermark`     | boolean | 否      | 默认值：`false`。                                           |

### 示例：更改视频风格

<Tabs>
  <Tab title="curl">
    **第 1 步：创建任务**

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    --header 'X-DashScope-Async: enable' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
      "model": "wan2.7-videoedit",
      "input": {
        "prompt": "Convert the entire scene to a claymation style",
        "media": [
          {
            "type": "video",
            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4"
          }
        ]
      },
      "parameters": {
        "resolution": "720P",
        "prompt_extend": true,
        "watermark": true
      }
    }'
    ```

    **第 2 步：通过任务 ID 获取结果**

    将 `{task_id}` 替换为上一步 API 返回的 `task_id` 值。

    ```bash
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>

  <Tab title="Python">
    ```python
    import os
    import time
    import requests

    API_KEY = os.environ.get("DASHSCOPE_API_KEY")
    BASE_URL = "https://dashscope.aliyuncs.com/api/v1"

    # 第 1 步：提交任务
    response = requests.post(
      f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
      headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
      },
      json={
        "model": "wan2.7-videoedit",
        "input": {
          "prompt": "Convert the entire scene to a claymation style",
          "media": [
            {
              "type": "video",
              "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/ldnfdf/wan2.7-videoedit-style-change.mp4",
            }
          ],
        },
        "parameters": {
          "resolution": "720P",
          "prompt_extend": True,
          "watermark": True,
        },
      },
    )
    task_id = response.json()["output"]["task_id"]
    print(f"任务已提交: {task_id}")

    # 第 2 步：轮询获取结果
    while True:
      status_resp = requests.get(
        f"{BASE_URL}/tasks/{task_id}",
        headers={"Authorization": f"Bearer {API_KEY}"},
      )
      status = status_resp.json()["output"]["task_status"]
      if status == "SUCCEEDED":
        print(f"视频已生成: {status_resp.json()['output']['video_url']}")
        break
      elif status == "FAILED":
        print(f"任务失败: {status_resp.json()['output'].get('message')}")
        break
      print(f"状态: {status} -- 等待 10 秒...")
      time.sleep(10)
    ```
  </Tab>
</Tabs>

### 示例：使用参考图编辑

通过参考图替换视频中的物体：

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wan2.7-videoedit",
  "input": {
    "prompt": "Replace the girl'\''s clothes in the video with the clothes from the image",
    "media": [
      {
        "type": "video",
        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/nlspwm/T2VA_22.mp4"
      },
      {
        "type": "reference_image",
        "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260402/fwjpqf/wan2.7-videoedit-change-clothes.png"
      }
    ]
  },
  "parameters": {
    "resolution": "720P",
    "prompt_extend": true,
    "watermark": true
  }
}'
```

## Wan 2.1 视频编辑（VACE）

`wan2.1-vace-plus` 模型支持 5 种专业编辑功能，通过 `function` 参数选择。

### 核心功能

#### 多图参考

**功能说明**：支持最多 **3** 张参考图，涵盖主体和背景（人物、动物、服装、场景等）。模型将多张图片融合生成连贯的视频内容。

**参数设置**：

- `function`：必须设为 **`image_reference`**。
- `ref_images_url`：URL 数组，支持 1 到 3 张参考图。
- `obj_or_bg`：标识每张图是主体（obj）还是背景（bg）。该数组长度必须与 `ref_images_url` 数组长度一致。

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入提示词**</th>
    <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入参考图 1（主体参考）**</th>
    <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入参考图 2（背景参考）**</th>
    <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输出视频**</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      视频中，一位少女从古老而雾气弥漫的森林深处走出。她步伐轻盈，镜头捕捉着她每一个优雅的瞬间。当她停下脚步环顾四周郁郁葱葱的树木时，脸上绽放出惊喜与喜悦的微笑。这个光影交错的画面，记录了她与自然的美妙邂逅。
    </td>

    <td style={{verticalAlign: "top"}}>
      <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/1007461571/p955656.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      <img alt="image" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/1007461571/p955657.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      [输出视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250704/agazky/20250506150137950398164_52_29_29.mp4)
    </td>
  </tr>
</table>

调用 API 前，请先[获取 API Key](/api-reference/preparation/api-key)，然后[将 API Key 设置为环境变量](/api-reference/preparation/export-api-key-env)。

<Tabs>
  <Tab title="curl">
    **第 1 步：创建任务获取任务 ID**

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    --header 'X-DashScope-Async: enable' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
      "model": "wan2.1-vace-plus",
      "input": {
        "function": "image_reference",
        "prompt": "In the video, a girl gracefully walks out from a misty, ancient forest. Her steps are light, and the camera captures her every nimble moment. When she stops and looks around at the lush woods, a smile of surprise and joy blossoms on her face. This scene, frozen in a moment of interplay between light and shadow, records her wonderful encounter with nature.",
        "ref_images_url": [
          "http://wanx.alicdn.com/material/20250318/image_reference_2_5_16.png",
          "http://wanx.alicdn.com/material/20250318/image_reference_1_5_16.png"
        ]
      },
      "parameters": {
        "prompt_extend": true,
        "obj_or_bg": ["obj","bg"],
        "size": "1280*720"
      }
    }'
    ```

    **第 2 步：通过任务 ID 获取结果**

    将 `{task_id}` 替换为上一步 API 返回的 `task_id` 值。

    ```bash
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>

  <Tab title="Python">
    ```python
    import os
    import requests
    import time

    BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
    API_KEY = os.environ.get("DASHSCOPE_API_KEY")

    def create_task():
      """创建视频合成任务并返回 task_id"""
      try:
        resp = requests.post(
          f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
          headers={
            "X-DashScope-Async": "enable",
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
          },
          json={
            "model": "wan2.1-vace-plus",
            "input": {
              "function": "image_reference",
              "prompt": "In the video, a girl walks out from the depths of an ancient, misty forest. Her steps are light, and the camera captures her every graceful moment. When she stops and looks around at the lush trees, a smile of surprise and joy blossoms on her face. This scene, frozen in a moment of intertwined light and shadow, records her wonderful encounter with nature.",
              "ref_images_url": [
                "http://wanx.alicdn.com/material/20250318/image_reference_2_5_16.png",
                "http://wanx.alicdn.com/material/20250318/image_reference_1_5_16.png"
              ]
            },
            "parameters": {"prompt_extend": True, "obj_or_bg": ["obj", "bg"], "size": "1280*720"}
          },
          timeout=30
        )
        resp.raise_for_status()
        return resp.json()["output"]["task_id"]
      except requests.RequestException as e:
        raise RuntimeError(f"创建任务失败: {e}")

    def poll_result(task_id):
      while True:
        try:
          resp = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10
          )
          resp.raise_for_status()
          data = resp.json()["output"]
          status = data["task_status"]
          print(f"状态: {status}")

          if status == "SUCCEEDED":
            return data["video_url"]
          elif status in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"任务失败: {data.get('message', '未知错误')}")
          time.sleep(15)
        except requests.RequestException as e:
          print(f"轮询异常: {e}，15 秒后重试...")
          time.sleep(15)

    if __name__ == "__main__":
      task_id = create_task()
      print(f"任务 ID: {task_id}")
      video_url = poll_result(task_id)
      print(f"\n视频生成成功: {video_url}")
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import org.json.*;
    import java.io.*;
    import java.net.*;
    import java.util.HashMap;
    import java.util.Map;

    public class VideoSynthesis {
      static final String BASE_URL = "https://dashscope.aliyuncs.com/api/v1";
      static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
      private static final Map<String, String> COMMON_HEADERS = new HashMap<>();

      static {
        if (API_KEY == null || API_KEY.isEmpty()) {
          throw new IllegalStateException("DASHSCOPE_API_KEY 未设置");
        }
        COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
        // 启用 HTTP 长连接（JVM 默认启用，但显式设置更可靠）
        System.setProperty("http.keepAlive", "true");
        System.setProperty("http.maxConnections", "20");
      }

      public static boolean isValidUserUrl(String urlString) {
        try {
          URL url = new URL(urlString);
          // 检查协议是否安全
          String protocol = url.getProtocol();
          if (!"https".equalsIgnoreCase(protocol) && !"http".equalsIgnoreCase(protocol)) {
            return false;
          }

          return true;
        } catch (Exception e) {
          System.err.println("无效 URL: " + e.getMessage());
          return false;
        }
      }

      // 通用 HTTP POST 请求
      private static String httpPost(String path, JSONObject body) throws Exception {
        HttpURLConnection conn = createConnection(path, "POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        try (OutputStream os = conn.getOutputStream()) {
          os.write(body.toString().getBytes("UTF-8"));
        }
        return readResponse(conn);
      }

      // 通用 HTTP GET 请求
      private static String httpGet(String path) throws Exception {
        HttpURLConnection conn = createConnection(path, "GET");
        return readResponse(conn);
      }

      // 创建连接（复用连接参数）
      private static HttpURLConnection createConnection(String path, String method) throws Exception {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();

        // 配置连接属性
        conn.setRequestMethod(method);
        conn.setConnectTimeout(30000);  // 30 秒连接超时
        conn.setReadTimeout(60000);     // 60 秒读取超时
        conn.setInstanceFollowRedirects(true);  // 允许重定向

        // 设置公共请求头
        for (Map.Entry<String, String> entry : COMMON_HEADERS.entrySet()) {
          conn.setRequestProperty(entry.getKey(), entry.getValue());
        }

        // 异步任务请求头
        if (path.contains("video-synthesis")) {
          conn.setRequestProperty("X-DashScope-Async", "enable");
        }

        // 设置内容类型和接受类型
        conn.setRequestProperty("Accept", "application/json");

        return conn;
      }

      // 读取响应（自动处理错误流）
      private static String readResponse(HttpURLConnection conn) throws IOException {
        InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400)
            ? conn.getInputStream()
            : conn.getErrorStream();

        if (is == null) {
          throw new IOException("无法获取响应流，响应码: " + conn.getResponseCode());
        }

        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
          StringBuilder sb = new StringBuilder();
          String line;
          while ((line = br.readLine()) != null) {
            sb.append(line);
            sb.append("\n");  // 添加换行符以保持原始格式
          }
          return sb.toString();
        }
      }

      // 第 1 步：创建任务
      public static String createTask() throws Exception {
        JSONObject body = new JSONObject()
            .put("model", "wan2.1-vace-plus")
            .put("input", new JSONObject()
                .put("function", "image_reference")
                .put("prompt", "In the video, a girl walks out from the depths of an ancient, misty forest. Her steps are light, and the camera captures her every graceful moment. When she stops and looks around at the lush trees, a smile of surprise and joy blossoms on her face. This scene, frozen in a moment of intertwined light and shadow, records her wonderful encounter with nature.")
                .put("ref_images_url", new JSONArray()
                    .put("http://wanx.alicdn.com/material/20250318/image_reference_2_5_16.png")
                    .put("http://wanx.alicdn.com/material/20250318/image_reference_1_5_16.png")))
            .put("parameters", new JSONObject()
                .put("prompt_extend", true)
                .put("obj_or_bg", new JSONArray().put("obj").put("bg"))
                .put("size", "1280*720"));

        String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
        JSONObject jsonResponse = new JSONObject(resp);

        // 检查响应是否包含错误信息
        if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
          String errorMessage = jsonResponse.optString("message", "未知错误");
          throw new RuntimeException("创建任务失败: " + errorMessage + "，详情: " + resp);
        }
        JSONObject output = jsonResponse.getJSONObject("output");
        return output.getString("task_id");
      }

      // 第 2 步：轮询获取结果（15 秒间隔，无重试次数限制）
      public static String pollResult(String taskId) throws Exception {
        while (true) {
          String resp = httpGet("/tasks/" + taskId);
          JSONObject responseJson = new JSONObject(resp);

          // 验证响应结构
          if (!responseJson.has("output")) {
            throw new RuntimeException("API 响应缺少 'output' 字段: " + resp);
          }

          JSONObject output = responseJson.getJSONObject("output");
          String status = output.getString("task_status");
          System.out.println("状态: " + status);

          if ("SUCCEEDED".equals(status)) {
            return output.getString("video_url");
          } else if ("FAILED".equals(status) || "CANCELLED".equals(status)) {
            String message = output.optString("message", "未知错误");
            throw new RuntimeException("任务失败: " + message + "，任务 ID: " + taskId + "，详情: " + resp);
          }
          Thread.sleep(15000);
        }
      }

      public static void main(String[] args) {
        try {
          System.out.println("正在创建视频合成任务...");
          String taskId = createTask();
          System.out.println("任务创建成功，任务 ID: " + taskId);
          System.out.println("正在轮询任务结果...");
          String videoUrl = pollResult(taskId);
          System.out.println("视频 URL: " + videoUrl);
        } catch (Exception e) {
          System.err.println("发生错误: " + e.getMessage());
          e.printStackTrace(); // 打印完整堆栈信息用于调试
        }
      }

    }
    ```
  </Tab>
</Tabs>

#### 视频重绘

**功能说明**：从输入视频中提取主体的姿态和运动、构图和运动轮廓，或草图结构，然后结合文本提示词生成具有相同动态特征的新视频。也支持通过参考图替换主体。

**参数设置**：

- `function`：必须设为 **`video_repainting`**。
- `video_url`**：必选**。输入视频的 URL。必须为 MP4 格式，不超过 50 MB，时长不超过 5 秒。
- `control_condition`：可选。视频特征提取方式，决定保留原视频的哪些特征：
  - `posebodyface`：提取面部表情和肢体动作，保留面部表情细节。
  - `posebody`：仅提取肢体动作，不含面部。仅控制身体运动。
  - `depth`：提取构图和运动轮廓，保留场景结构。
  - `scribble`：提取草图结构，保留草图边缘细节。
- `strength`：可选。控制特征提取强度。范围：0.0--1.0。默认值：1.0。值越高，输出越接近原视频；值越低，创作自由度越大。
- `ref_images_url`：可选。参考图的 URL，用于替换输入视频中的主体。

| **输入提示词**                                                              | **输入视频**                                                                                                | **输出视频**                                                                                                       |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| 视频展示了一辆由绅士驾驶的黑色**蒸汽朋克风格汽车**，装饰着齿轮和铜管。背景是蒸汽动力糖果工厂，融合复古元素，营造出怀旧而趣味十足的场景。 | [输入视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250704/lblkoq/depth_2.mp4) | [输出视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250704/sesktr/depth_2_output.mp4) |

<Tabs>
  <Tab title="curl">
    **第 1 步：创建任务获取任务 ID**

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    --header 'X-DashScope-Async: enable' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
      "model": "wan2.1-vace-plus",
      "input": {
        "function": "video_repainting",
        "prompt": "The video shows a black steampunk-style car driven by a gentleman. The car is decorated with gears and copper pipes. The background features a steam-powered candy factory and retro elements, creating a vintage and playful scene.",
        "video_url": "http://wanx.alicdn.com/material/20250318/video_repainting_1.mp4"
      },
      "parameters": {
        "prompt_extend": false,
        "control_condition": "depth"
      }
    }'
    ```

    **第 2 步：通过任务 ID 获取结果**

    将 `{task_id}` 替换为上一步 API 返回的 `task_id` 值。

    ```bash
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>

  <Tab title="Python">
    ```python
    import os
    import requests
    import time

    BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
    API_KEY = os.environ.get("DASHSCOPE_API_KEY")

    def create_task():
      """创建视频重绘任务并返回 task_id"""
      try:
        resp = requests.post(
          f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
          headers={
            "X-DashScope-Async": "enable",
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
          },
          json={
            "model": "wan2.1-vace-plus",
            "input": {
              "function": "video_repainting",
              "prompt": "The video shows a black steampunk-style car driven by a gentleman, adorned with gears and copper pipes. The background is a steam-powered candy factory with retro elements, creating a vintage and playful scene.",
              "video_url": "http://wanx.alicdn.com/material/20250318/video_repainting_1.mp4"
            },
            "parameters": {
              "prompt_extend": False, # 视频重绘建议关闭提示词改写
              "control_condition": "depth" # 可选: posebodyface, posebody, depth, scribble
            }
          },
          timeout=30
        )
        resp.raise_for_status()
        return resp.json()["output"]["task_id"]
      except requests.RequestException as e:
        raise RuntimeError(f"创建任务失败: {e}")

    def poll_result(task_id):
      while True:
        try:
          resp = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10
          )
          resp.raise_for_status()
          data = resp.json()["output"]
          status = data["task_status"]
          print(f"状态: {status}")

          if status == "SUCCEEDED":
            return data["video_url"]
          elif status in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"任务失败: {data.get('message', '未知错误')}")
          time.sleep(15)
        except requests.RequestException as e:
          print(f"轮询异常: {e}，15 秒后重试...")
          time.sleep(15)

    if __name__ == "__main__":
      task_id = create_task()
      print(f"任务 ID: {task_id}")
      video_url = poll_result(task_id)
      print(f"\n视频生成成功: {video_url}")
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import org.json.*;
    import java.io.*;
    import java.net.*;
    import java.util.HashMap;
    import java.util.Map;

    public class VideoRepainting {
      static final String BASE_URL = "https://dashscope.aliyuncs.com/api/v1";
      static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
      private static final Map<String, String> COMMON_HEADERS = new HashMap<>();

      static {
        if (API_KEY == null || API_KEY.isEmpty()) {
          throw new IllegalStateException("DASHSCOPE_API_KEY 未设置");
        }
        COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
        System.setProperty("http.keepAlive", "true");
        System.setProperty("http.maxConnections", "20");
      }

      // 通用 HTTP POST 请求
      private static String httpPost(String path, JSONObject body) throws Exception {
        HttpURLConnection conn = createConnection(path, "POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        try (OutputStream os = conn.getOutputStream()) {
          os.write(body.toString().getBytes("UTF-8"));
        }
        return readResponse(conn);
      }

      // 通用 HTTP GET 请求
      private static String httpGet(String path) throws Exception {
        HttpURLConnection conn = createConnection(path, "GET");
        return readResponse(conn);
      }

      // 创建连接
      private static HttpURLConnection createConnection(String path, String method) throws Exception {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod(method);
        conn.setConnectTimeout(30000);
        conn.setReadTimeout(60000);
        conn.setInstanceFollowRedirects(true);
        for (Map.Entry<String, String> entry : COMMON_HEADERS.entrySet()) {
          conn.setRequestProperty(entry.getKey(), entry.getValue());
        }
        if (path.contains("video-synthesis")) {
          conn.setRequestProperty("X-DashScope-Async", "enable");
        }
        conn.setRequestProperty("Accept", "application/json");
        return conn;
      }

      // 读取响应
      private static String readResponse(HttpURLConnection conn) throws IOException {
        InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400)
            ? conn.getInputStream()
            : conn.getErrorStream();
        if (is == null) throw new IOException("无法获取响应流，响应码: " + conn.getResponseCode());
        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
          StringBuilder sb = new StringBuilder();
          String line;
          while ((line = br.readLine()) != null) {
            sb.append(line).append("\n");
          }
          return sb.toString();
        }
      }

      // 第 1 步：创建视频重绘任务
      public static String createTask() throws Exception {
        JSONObject body = new JSONObject()
            .put("model", "wan2.1-vace-plus")
            .put("input", new JSONObject()
                .put("function", "video_repainting")
                .put("prompt", "The video shows a black steampunk-style car driven by a gentleman, adorned with gears and copper pipes. The background is a steam-powered candy factory with retro elements, creating a vintage and playful scene.")
                .put("video_url", "http://wanx.alicdn.com/material/20250318/video_repainting_1.mp4"))
            .put("parameters", new JSONObject()
                .put("prompt_extend", false)
                .put("control_condition", "depth"));

        String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
        JSONObject jsonResponse = new JSONObject(resp);

        if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
          String errorMessage = jsonResponse.optString("message", "未知错误");
          throw new RuntimeException("创建任务失败: " + errorMessage);
        }
        return jsonResponse.getJSONObject("output").getString("task_id");
      }

      // 第 2 步：轮询获取结果
      public static String pollResult(String taskId) throws Exception {
        while (true) {
          String resp = httpGet("/tasks/" + taskId);
          JSONObject output = new JSONObject(resp).getJSONObject("output");
          String status = output.getString("task_status");
          System.out.println("状态: " + status);

          if ("SUCCEEDED".equals(status)) {
            return output.getString("video_url");
          } else if ("FAILED".equals(status) || "CANCELLED".equals(status)) {
            throw new RuntimeException("任务失败: " + output.optString("message", "未知错误"));
          }
          Thread.sleep(15000);
        }
      }

      public static void main(String[] args) {
        try {
          System.out.println("正在创建视频重绘任务...");
          String taskId = createTask();
          System.out.println("任务创建成功，任务 ID: " + taskId);
          System.out.println("正在轮询任务结果...");
          String videoUrl = pollResult(taskId);
          System.out.println("视频 URL: " + videoUrl);
        } catch (Exception e) {
          System.err.println("发生错误: " + e.getMessage());
          e.printStackTrace();
        }
      }
    }
    ```
  </Tab>
</Tabs>

#### 局部编辑

**功能说明**：对视频指定区域进行精细编辑，支持添加、删除和修改元素，或替换主体和背景。上传蒙版图指定编辑区域——模型会自动跟踪目标并融合生成内容。

**参数设置**：

- `function`：必须设为 **`video_edit`**。
- `video_url`**：必选**。原始输入视频的 URL。
- `mask_image_url`：可选。与 `mask_video_url` 二选一，推荐使用此参数。蒙版图的 URL。蒙版中白色区域为编辑区域，黑色区域保持不变。
- `mask_frame_id`：可选。与 `mask_image_url` 配合使用，指定蒙版对应视频的哪一帧。默认为第一帧。
- `mask_type`：可选。指定编辑区域的行为模式：
  - `tracking`（默认）：编辑区域自动跟随目标的运动轨迹。
  - `fixed`：编辑区域保持固定位置。
- `expand_ratio`：可选。仅在 `mask_type` 为 `tracking` 时生效。
  - 蒙版区域向外扩展的比例。范围：0.0--1.0。默认值：0.05。
  - 值越小越贴合目标，值越大扩展区域越广。
- `size`：可选。输出分辨率，格式为 `宽*高`（如 `1280*720`）。
- `ref_images_url`：可选。参考图的 URL。编辑区域的内容将替换为参考图中的内容。

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入提示词**</th>
    <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入视频**</th>
    <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输入蒙版图**</th>
    <th style={{textAlign: "left", width: "25%", paddingBottom: "8px"}}>**输出视频**</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      视频展示了一家巴黎风格的法式咖啡馆，一只<strong>穿西装的狮子</strong>正优雅地品尝咖啡。它一只手端着咖啡杯轻轻啜饮，表情悠然自得。咖啡馆装饰考究，柔和的色调和温暖的灯光照亮了狮子所在的区域。
    </td>

    <td style={{verticalAlign: "top"}}>
      [输入视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250703/cckalc/Inpainting_src_2_new.mp4)
    </td>

    <td style={{verticalAlign: "top"}}>
      <img alt="mask" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/3160651571/p955179.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} /> 白色区域为编辑区域。
    </td>

    <td style={{verticalAlign: "top"}}>
      [输出视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250703/egunuc/Inpainting_res_2_new.mp4)
    </td>
  </tr>
</table>

<Tabs>
  <Tab title="curl">
    **第 1 步：创建任务获取任务 ID**

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    --header 'X-DashScope-Async: enable' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
      "model": "wan2.1-vace-plus",
      "input": {
        "function": "video_edit",
        "prompt": "The video shows a Parisian-style French cafe where a lion in a suit is elegantly sipping coffee. It holds a coffee cup in one hand, taking a gentle sip with a relaxed expression. The cafe is tastefully decorated, with soft hues and warm lighting illuminating the area where the lion is.",
        "mask_image_url": "http://wanx.alicdn.com/material/20250318/video_edit_1_mask.png",
        "video_url": "http://wanx.alicdn.com/material/20250318/video_edit_2.mp4",
        "mask_frame_id": 1
      },
      "parameters": {
        "prompt_extend": false,
        "mask_type": "tracking",
        "expand_ratio": 0.05,
        "size": "1280*720"
      }
    }'
    ```

    **第 2 步：通过任务 ID 获取结果**

    将 `{task_id}` 替换为上一步 API 返回的 `task_id` 值。

    ```bash
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>

  <Tab title="Python">
    ```python
    import os
    import requests
    import time

    BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
    API_KEY = os.environ.get("DASHSCOPE_API_KEY")

    def create_task():
      """创建局部编辑任务并返回 task_id"""
      try:
        resp = requests.post(
          f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
          headers={
            "X-DashScope-Async": "enable",
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
          },
          json={
            "model": "wan2.1-vace-plus",
            "input": {
              "function": "video_edit",
              "prompt": "The video shows a Parisian-style French cafe where a lion in a suit is elegantly sipping coffee. It holds a coffee cup in one hand, taking a gentle sip with a relaxed expression. The cafe is tastefully decorated, with soft tones and warm lighting illuminating the area where the lion is.",
              "mask_image_url": "http://wanx.alicdn.com/material/20250318/video_edit_1_mask.png",
              "video_url": "http://wanx.alicdn.com/material/20250318/video_edit_2.mp4",
              "mask_frame_id": 1 # 蒙版对应的帧索引
            },
            "parameters": {
              "prompt_extend": False,
              "mask_type": "tracking", # 跟踪模式
              "expand_ratio": 0.05,
              "size": "1280*720"
            }
          },
          timeout=30
        )
        resp.raise_for_status()
        return resp.json()["output"]["task_id"]
      except requests.RequestException as e:
        raise RuntimeError(f"创建任务失败: {e}")

    def poll_result(task_id):
      while True:
        try:
          resp = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10
          )
          resp.raise_for_status()
          data = resp.json()["output"]
          status = data["task_status"]
          print(f"状态: {status}")

          if status == "SUCCEEDED":
            return data["video_url"]
          elif status in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"任务失败: {data.get('message', '未知错误')}")
          time.sleep(15)
        except requests.RequestException as e:
          print(f"轮询异常: {e}，15 秒后重试...")
          time.sleep(15)

    if __name__ == "__main__":
      task_id = create_task()
      print(f"任务 ID: {task_id}")
      video_url = poll_result(task_id)
      print(f"\n视频生成成功: {video_url}")
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import org.json.*;
    import java.io.*;
    import java.net.*;
    import java.util.HashMap;
    import java.util.Map;

    public class VideoRegionalEdit {
      static final String BASE_URL = "https://dashscope.aliyuncs.com/api/v1";
      static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
      private static final Map<String, String> COMMON_HEADERS = new HashMap<>();

      static {
        if (API_KEY == null || API_KEY.isEmpty()) {
          throw new IllegalStateException("DASHSCOPE_API_KEY 未设置");
        }
        COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
        System.setProperty("http.keepAlive", "true");
      }

      private static String httpPost(String path, JSONObject body) throws Exception {
        HttpURLConnection conn = createConnection(path, "POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        try (OutputStream os = conn.getOutputStream()) {
          os.write(body.toString().getBytes("UTF-8"));
        }
        return readResponse(conn);
      }

      private static String httpGet(String path) throws Exception {
        HttpURLConnection conn = createConnection(path, "GET");
        return readResponse(conn);
      }

      private static HttpURLConnection createConnection(String path, String method) throws Exception {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod(method);
        conn.setConnectTimeout(30000);
        conn.setReadTimeout(60000);
        for (Map.Entry<String, String> entry : COMMON_HEADERS.entrySet()) {
          conn.setRequestProperty(entry.getKey(), entry.getValue());
        }
        if (path.contains("video-synthesis")) {
          conn.setRequestProperty("X-DashScope-Async", "enable");
        }
        return conn;
      }

      private static String readResponse(HttpURLConnection conn) throws IOException {
        InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400) ? conn.getInputStream() : conn.getErrorStream();
        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
          StringBuilder sb = new StringBuilder();
          String line;
          while ((line = br.readLine()) != null) sb.append(line).append("\n");
          return sb.toString();
        }
      }

      // 第 1 步：创建局部编辑任务
      public static String createTask() throws Exception {
        JSONObject body = new JSONObject()
            .put("model", "wan2.1-vace-plus")
            .put("input", new JSONObject()
                .put("function", "video_edit")
                .put("prompt", "The video shows a Parisian-style French cafe where a lion in a suit is elegantly sipping coffee. It holds a coffee cup in one hand, taking a gentle sip with a relaxed expression. The cafe is tastefully decorated, with soft tones and warm lighting illuminating the area where the lion is.")
                .put("mask_image_url", "http://wanx.alicdn.com/material/20250318/video_edit_1_mask.png")
                .put("video_url", "http://wanx.alicdn.com/material/20250318/video_edit_2.mp4")
                .put("mask_frame_id", 1))
            .put("parameters", new JSONObject()
                .put("prompt_extend", false)
                .put("mask_type", "tracking")
                .put("expand_ratio", 0.05)
                .put("size", "1280*720"));

        String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
        JSONObject jsonResponse = new JSONObject(resp);

        if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
          String errorMessage = jsonResponse.optString("message", "未知错误");
          throw new RuntimeException("创建任务失败: " + errorMessage);
        }
        return jsonResponse.getJSONObject("output").getString("task_id");
      }

      // 第 2 步：轮询获取结果
      public static String pollResult(String taskId) throws Exception {
        while (true) {
          String resp = httpGet("/tasks/" + taskId);
          JSONObject output = new JSONObject(resp).getJSONObject("output");
          String status = output.getString("task_status");
          System.out.println("状态: " + status);

          if ("SUCCEEDED".equals(status)) return output.getString("video_url");
          else if ("FAILED".equals(status) || "CANCELLED".equals(status))
            throw new RuntimeException("任务失败: " + output.optString("message"));
          Thread.sleep(15000);
        }
      }

      public static void main(String[] args) {
        try {
          System.out.println("正在创建局部编辑任务...");
          String taskId = createTask();
          System.out.println("任务创建成功，任务 ID: " + taskId);
          String videoUrl = pollResult(taskId);
          System.out.println("视频 URL: " + videoUrl);
        } catch (Exception e) {
          e.printStackTrace();
        }
      }
    }
    ```
  </Tab>
</Tabs>

#### 视频延展

**功能说明**：基于输入的图片或视频片段，预测并生成连续内容。支持从首帧或首段片段向后延展，也支持从末帧或末段片段向前延展。生成的视频时长为 5 秒。

**参数设置**：

- `function`：必须设为 **`video_extension`**。
- `prompt`**：必选**。描述期望延展的内容。
- `first_clip_url`：可选。首段视频片段的 URL（不超过 3 秒）。模型基于此片段生成后续视频。
- `last_clip_url`：可选。末段视频片段的 URL（不超过 3 秒）。模型基于此片段生成前序内容。
- `first_frame_url`：可选。首帧图片的 URL。视频从该帧向后延展。
- `last_frame_url`：可选。末帧图片的 URL。视频从该帧向前生成。

<Note>
  `first_clip_url`、`last_clip_url`、`first_frame_url`、`last_frame_url` 至少指定其中一个。
</Note>

| **输入提示词**                  | **输入首段片段（1 秒）**                                                                                                   | **输出视频（延展后为 5 秒）**                                                                                                         |
| -------------------------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| 一只**戴墨镜的狗在街上玩滑板**，3D 卡通风格。 | [输入视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250619/guknnt/video_extension_1.mp4) | [输出视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250704/rzrbyy/cur_gallery_20250515140027.mp4) |

<Tabs>
  <Tab title="curl">
    **第 1 步：创建任务获取任务 ID**

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    --header 'X-DashScope-Async: enable' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
      "model": "wan2.1-vace-plus",
      "input": {
        "function": "video_extension",
        "prompt": "A dog wearing sunglasses is skateboarding on the street, 3D cartoon.",
        "first_clip_url": "http://wanx.alicdn.com/material/20250318/video_extension_1.mp4"
      },
      "parameters": {
        "prompt_extend": false
      }
    }'
    ```

    **第 2 步：通过任务 ID 获取结果**

    将 `{task_id}` 替换为上一步 API 返回的 `task_id` 值。

    ```bash
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>

  <Tab title="Python">
    ```python
    import os
    import requests
    import time

    BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
    API_KEY = os.environ.get("DASHSCOPE_API_KEY")

    def create_task():
      """创建视频延展任务并返回 task_id"""
      try:
        resp = requests.post(
          f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
          headers={
            "X-DashScope-Async": "enable",
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
          },
          json={
            "model": "wan2.1-vace-plus",
            "input": {
              "function": "video_extension",
              "prompt": "A dog wearing sunglasses is skateboarding on the street, 3D cartoon.",
              "first_clip_url": "http://wanx.alicdn.com/material/20250318/video_extension_1.mp4"
            },
            "parameters": {
              "prompt_extend": False
            }
          },
          timeout=30
        )
        resp.raise_for_status()
        return resp.json()["output"]["task_id"]
      except requests.RequestException as e:
        raise RuntimeError(f"创建任务失败: {e}")

    def poll_result(task_id):
      while True:
        try:
          resp = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10
          )
          resp.raise_for_status()
          data = resp.json()["output"]
          status = data["task_status"]
          print(f"状态: {status}")

          if status == "SUCCEEDED":
            return data["video_url"]
          elif status in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"任务失败: {data.get('message', '未知错误')}")
          time.sleep(15)
        except requests.RequestException as e:
          print(f"轮询异常: {e}，15 秒后重试...")
          time.sleep(15)

    if __name__ == "__main__":
      task_id = create_task()
      print(f"任务 ID: {task_id}")
      video_url = poll_result(task_id)
      print(f"\n视频生成成功: {video_url}")
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import org.json.*;
    import java.io.*;
    import java.net.*;
    import java.util.HashMap;
    import java.util.Map;

    public class VideoExtension {
      static final String BASE_URL = "https://dashscope.aliyuncs.com/api/v1";
      static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
      private static final Map<String, String> COMMON_HEADERS = new HashMap<>();

      static {
        if (API_KEY == null || API_KEY.isEmpty()) {
          throw new IllegalStateException("DASHSCOPE_API_KEY 未设置");
        }
        COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
        System.setProperty("http.keepAlive", "true");
      }

      private static String httpPost(String path, JSONObject body) throws Exception {
        HttpURLConnection conn = createConnection(path, "POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        try (OutputStream os = conn.getOutputStream()) {
          os.write(body.toString().getBytes("UTF-8"));
        }
        return readResponse(conn);
      }

      private static String httpGet(String path) throws Exception {
        HttpURLConnection conn = createConnection(path, "GET");
        return readResponse(conn);
      }

      private static HttpURLConnection createConnection(String path, String method) throws Exception {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod(method);
        conn.setConnectTimeout(30000);
        conn.setReadTimeout(60000);
        for (Map.Entry<String, String> entry : COMMON_HEADERS.entrySet()) {
          conn.setRequestProperty(entry.getKey(), entry.getValue());
        }
        if (path.contains("video-synthesis")) {
          conn.setRequestProperty("X-DashScope-Async", "enable");
        }
        return conn;
      }

      private static String readResponse(HttpURLConnection conn) throws IOException {
        InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400) ? conn.getInputStream() : conn.getErrorStream();
        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
          StringBuilder sb = new StringBuilder();
          String line;
          while ((line = br.readLine()) != null) sb.append(line).append("\n");
          return sb.toString();
        }
      }

      // 第 1 步：创建视频延展任务
      public static String createTask() throws Exception {
        JSONObject body = new JSONObject()
            .put("model", "wan2.1-vace-plus")
            .put("input", new JSONObject()
                .put("function", "video_extension")
                .put("prompt", "A dog wearing sunglasses is skateboarding on the street, 3D cartoon.")
                .put("first_clip_url", "http://wanx.alicdn.com/material/20250318/video_extension_1.mp4"))
            .put("parameters", new JSONObject()
                .put("prompt_extend", false));

        String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
        JSONObject jsonResponse = new JSONObject(resp);

        if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
          String errorMessage = jsonResponse.optString("message", "未知错误");
          throw new RuntimeException("创建任务失败: " + errorMessage);
        }
        return jsonResponse.getJSONObject("output").getString("task_id");
      }

      // 第 2 步：轮询获取结果
      public static String pollResult(String taskId) throws Exception {
        while (true) {
          String resp = httpGet("/tasks/" + taskId);
          JSONObject output = new JSONObject(resp).getJSONObject("output");
          String status = output.getString("task_status");
          System.out.println("状态: " + status);

          if ("SUCCEEDED".equals(status)) return output.getString("video_url");
          else if ("FAILED".equals(status) || "CANCELLED".equals(status))
            throw new RuntimeException("任务失败: " + output.optString("message"));
          Thread.sleep(15000);
        }
      }

      public static void main(String[] args) {
        try {
          System.out.println("正在创建视频延展任务...");
          String taskId = createTask();
          System.out.println("任务创建成功，任务 ID: " + taskId);
          String videoUrl = pollResult(taskId);
          System.out.println("视频 URL: " + videoUrl);
        } catch (Exception e) {
          e.printStackTrace();
        }
      }
    }
    ```
  </Tab>
</Tabs>

#### 画面扩展

**功能说明**：基于提示词，将视频画面内容向四周（上、下、左、右）按比例扩展。保持视频主体的连续性，并确保与背景自然融合。

**参数设置**：

- `function`：必须设为 **`video_outpainting`**。
- `video_url`**：必选**。原始输入视频的 URL。
- `top_scale`：可选。向上扩展比例。范围：1.0--2.0。默认值：1.0（不扩展）。
- `bottom_scale`：可选。向下扩展比例。范围：1.0--2.0。默认值：1.0。
- `left_scale`：可选。向左扩展比例。范围：1.0--2.0。默认值：1.0。
- `right_scale`：可选。向右扩展比例。范围：1.0--2.0。默认值：1.0。

<Tip>
  **示例**：将 `left_scale` 设为 1.5，表示画面左侧扩展为原始宽度的 1.5 倍。
</Tip>

| **输入提示词**                           | **输入视频**                                                                                                        | **输出视频**                                                                                                                             |
| ----------------------------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 一位优雅的女士正在热情地演奏小提琴，**身后是一支完整的交响乐团**。 | [输入视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250704/ewansh/cur_gallery_038.mp4) | [输出视频](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20250704/wabras/1d3e788a-1a5d-47d9-9c85-b33793f15cdc.mp4) |

<Tabs>
  <Tab title="curl">
    **第 1 步：创建任务获取任务 ID**

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
    --header 'X-DashScope-Async: enable' \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
    --header 'Content-Type: application/json' \
    --data '{
      "model": "wan2.1-vace-plus",
      "input": {
        "function": "video_outpainting",
        "prompt": "An elegant lady is passionately playing the violin, with a full symphony orchestra behind her.",
        "video_url": "http://wanx.alicdn.com/material/20250318/video_outpainting_1.mp4"
      },
      "parameters": {
        "prompt_extend": false,
        "top_scale": 1.5,
        "bottom_scale": 1.5,
        "left_scale": 1.5,
        "right_scale": 1.5
      }
    }'
    ```

    **第 2 步：通过任务 ID 获取结果**

    将 `{task_id}` 替换为上一步 API 返回的 `task_id` 值。

    ```bash
    curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
    --header "Authorization: Bearer $DASHSCOPE_API_KEY"
    ```
  </Tab>

  <Tab title="Python">
    ```python
    import os
    import requests
    import time

    BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
    API_KEY = os.environ.get("DASHSCOPE_API_KEY")

    def create_task():
      """创建画面扩展任务并返回 task_id"""
      try:
        resp = requests.post(
          f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
          headers={
            "X-DashScope-Async": "enable",
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
          },
          json={
            "model": "wan2.1-vace-plus",
            "input": {
              "function": "video_outpainting",
              "prompt": "An elegant lady is passionately playing the violin, with a full symphony orchestra behind her.",
              "video_url": "http://wanx.alicdn.com/material/20250318/video_outpainting_1.mp4"
            },
            "parameters": {
              "prompt_extend": False,
              "top_scale": 1.5,    # 向上扩展比例
              "bottom_scale": 1.5, # 向下扩展比例
              "left_scale": 1.5,   # 向左扩展比例
              "right_scale": 1.5   # 向右扩展比例
            }
          },
          timeout=30
        )
        resp.raise_for_status()
        return resp.json()["output"]["task_id"]
      except requests.RequestException as e:
        raise RuntimeError(f"创建任务失败: {e}")

    def poll_result(task_id):
      while True:
        try:
          resp = requests.get(
            f"{BASE_URL}/tasks/{task_id}",
            headers={"Authorization": f"Bearer {API_KEY}"},
            timeout=10
          )
          resp.raise_for_status()
          data = resp.json()["output"]
          status = data["task_status"]
          print(f"状态: {status}")

          if status == "SUCCEEDED":
            return data["video_url"]
          elif status in ("FAILED", "CANCELLED"):
            raise RuntimeError(f"任务失败: {data.get('message', '未知错误')}")
          time.sleep(15)
        except requests.RequestException as e:
          print(f"轮询异常: {e}，15 秒后重试...")
          time.sleep(15)

    if __name__ == "__main__":
      task_id = create_task()
      print(f"任务 ID: {task_id}")
      video_url = poll_result(task_id)
      print(f"\n视频生成成功: {video_url}")
    ```
  </Tab>

  <Tab title="Java">
    ```java
    import org.json.*;
    import java.io.*;
    import java.net.*;
    import java.util.HashMap;
    import java.util.Map;

    public class VideoOutpainting {
      static final String BASE_URL = "https://dashscope.aliyuncs.com/api/v1";
      static final String API_KEY = System.getenv("DASHSCOPE_API_KEY");
      private static final Map<String, String> COMMON_HEADERS = new HashMap<>();

      static {
        if (API_KEY == null || API_KEY.isEmpty()) {
          throw new IllegalStateException("DASHSCOPE_API_KEY 未设置");
        }
        COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
        System.setProperty("http.keepAlive", "true");
      }

      private static String httpPost(String path, JSONObject body) throws Exception {
        HttpURLConnection conn = createConnection(path, "POST");
        conn.setRequestProperty("Content-Type", "application/json");
        conn.setDoOutput(true);
        try (OutputStream os = conn.getOutputStream()) {
          os.write(body.toString().getBytes("UTF-8"));
        }
        return readResponse(conn);
      }

      private static String httpGet(String path) throws Exception {
        HttpURLConnection conn = createConnection(path, "GET");
        return readResponse(conn);
      }

      private static HttpURLConnection createConnection(String path, String method) throws Exception {
        URL url = new URL(BASE_URL + path);
        HttpURLConnection conn = (HttpURLConnection) url.openConnection();
        conn.setRequestMethod(method);
        conn.setConnectTimeout(30000);
        conn.setReadTimeout(60000);
        for (Map.Entry<String, String> entry : COMMON_HEADERS.entrySet()) {
          conn.setRequestProperty(entry.getKey(), entry.getValue());
        }
        if (path.contains("video-synthesis")) {
          conn.setRequestProperty("X-DashScope-Async", "enable");
        }
        return conn;
      }

      private static String readResponse(HttpURLConnection conn) throws IOException {
        InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400) ? conn.getInputStream() : conn.getErrorStream();
        try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
          StringBuilder sb = new StringBuilder();
          String line;
          while ((line = br.readLine()) != null) sb.append(line).append("\n");
          return sb.toString();
        }
      }

      // 第 1 步：创建画面扩展任务
      public static String createTask() throws Exception {
        JSONObject body = new JSONObject()
            .put("model", "wan2.1-vace-plus")
            .put("input", new JSONObject()
                .put("function", "video_outpainting")
                .put("prompt", "An elegant lady is passionately playing the violin, with a full symphony orchestra behind her.")
                .put("video_url", "http://wanx.alicdn.com/material/20250318/video_outpainting_1.mp4"))
            .put("parameters", new JSONObject()
                .put("prompt_extend", false)
                .put("top_scale", 1.5)
                .put("bottom_scale", 1.5)
                .put("left_scale", 1.5)
                .put("right_scale", 1.5));

        String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
        JSONObject jsonResponse = new JSONObject(resp);

        if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
          String errorMessage = jsonResponse.optString("message", "未知错误");
          throw new RuntimeException("创建任务失败: " + errorMessage);
        }
        return jsonResponse.getJSONObject("output").getString("task_id");
      }

      // 第 2 步：轮询获取结果
      public static String pollResult(String taskId) throws Exception {
        while (true) {
          String resp = httpGet("/tasks/" + taskId);
          JSONObject output = new JSONObject(resp).getJSONObject("output");
          String status = output.getString("task_status");
          System.out.println("状态: " + status);

          if ("SUCCEEDED".equals(status)) return output.getString("video_url");
          else if ("FAILED".equals(status) || "CANCELLED".equals(status))
            throw new RuntimeException("任务失败: " + output.optString("message"));
          Thread.sleep(15000);
        }
      }

      public static void main(String[] args) {
        try {
          System.out.println("正在创建画面扩展任务...");
          String taskId = createTask();
          System.out.println("任务创建成功，任务 ID: " + taskId);
          String videoUrl = pollResult(taskId);
          System.out.println("视频 URL: " + videoUrl);
        } catch (Exception e) {
          e.printStackTrace();
        }
      }
    }
    ```
  </Tab>
</Tabs>

## 输入图片和视频

### 输入图片

- **图片数量**：参见上方各功能所需的数量说明。
- **输入方式**：
  - **公开 URL**：支持 HTTP 和 HTTPS 协议。示例：`https://xxxx/xxx.png`。

### 输入视频

- **视频数量**：参见上方各功能所需的数量说明。
- **输入方式**：
  - **公开 URL**：支持 HTTP 和 HTTPS 协议。示例：`https://xxxx/xxx.mp4`。

## 输出视频

- **视频数量**：1 个。
- **格式**：MP4。分辨率和尺寸详见下方视频规格说明。
- **URL 有效期**：24 小时。
- **尺寸**：因所选功能而异。
  - **多图参考 / 局部编辑**：
    - 输出分辨率固定为 720P。
    - 具体宽高由 `size` 参数决定。
  - **视频重绘 / 视频延展 / 画面扩展**：
    - 输入视频分辨率为 720P 或更低时，输出分辨率与输入一致。
    - 输入视频分辨率高于 720P 时，输出等比缩放至 720P。

## 计费与限流

- 免费额度和定价详见[模型调用计费](/developer-guides/getting-started/pricing)。
- 限流规则详见[限流](/developer-guides/administration/rate-limits)。
- 计费说明：
  - 输入免费。输出按成功生成的**视频秒数**计费。
  - 模型调用失败或处理异常不收费，也不消耗[免费额度](/resources/free-quota)。

## API 参考

- [wan2.7 视频编辑 API 参考](/api-reference/video-generation/wan27-video-editing/create-task)
- [wan2.1 通用视频编辑 API 参考](/api-reference/video-generation/wan-general-video-editing/create-task)

## 常见问题

### 多图参考最多支持几张图片？

最多支持 3 张参考图。超过 3 张时只取前 3 张。为获得最佳效果，建议主体图使用纯色背景以突出主体，背景图不要包含主体对象。

### 视频重绘何时应关闭提示词改写？

如果文本描述与输入视频内容不一致，模型可能会误解您的意图。此时建议手动关闭提示词改写，即设置 `prompt_extend=false`，并在提示词中提供清晰、具体的场景描述，以提高一致性和准确性。

### 局部编辑中蒙版图和蒙版视频的区别

通过 `mask_image_url` 指定蒙版图，或通过 `mask_video_url` 指定蒙版视频，二者选其一。**推荐使用蒙版图**，因为您只需在单帧中指定编辑区域，系统会自动跟踪目标。
