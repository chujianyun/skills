> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan — 创建任务

> 提交视频编辑任务

该模型支持文本、图片和视频多模态输入，生成编辑后的视频。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: Wan 视频编辑 API
  description: Wan 统一视频编辑 API，支持多模态输入（文本、图像、视频），提供五大核心能力：多图参考、视频重绘、局部编辑、视频续写和画面扩展。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createVideoEditing
      summary: 创建视频编辑任务
      description: 创建视频编辑任务。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 必须设置为 `enable` 以创建异步任务。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/VideoEditingRequest"
      responses:
        "200":
          description: 任务创建成功。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求参数无效。
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: curl
          label: cURL - 多图参考
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "wanx2.1-vace-plus",
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
        - lang: python
          label: Python - 多图参考
          source: |-
            import os
            import requests
            import time

            BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
            API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")
            headers = {"X-DashScope-Async": "enable", "Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

            def create_task():
              """创建视频合成任务，返回 task_id"""
              try:
                resp = requests.post(
                  f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
                  headers={
                    "X-DashScope-Async": "enable",
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                  },
                  json={
                    "model": "wanx2.1-vace-plus",
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
                raise RuntimeError(f"Failed to create task: {e}")

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
                  print(f"Status: {status}")

                  if status == "SUCCEEDED":
                    return data["video_url"]
                  elif status in ("FAILED", "CANCELLED"):
                    raise RuntimeError(f"Task failed: {data.get('message', 'Unknown error')}")
                  time.sleep(15)
                except requests.RequestException as e:
                  print(f"Polling exception: {e}, retrying in 15 seconds...")
                  time.sleep(15)

            if __name__ == "__main__":
              task_id = create_task()
              print(f"Task ID: {task_id}")
              video_url = poll_result(task_id)
              print(f"\nVideo generated successfully: {video_url}")
        - lang: java
          label: Java - 多图参考
          source: |-
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
                  throw new IllegalStateException("DASHSCOPE_API_KEY is not set");
                }
                COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
                System.setProperty("http.keepAlive", "true");
                System.setProperty("http.maxConnections", "20");
              }

              public static boolean isValidUserUrl(String urlString) {
                try {
                  URL url = new URL(urlString);
                  String protocol = url.getProtocol();
                  if (!"https".equalsIgnoreCase(protocol) && !"http".equalsIgnoreCase(protocol)) {
                    return false;
                  }

                  return true;
                } catch (Exception e) {
                  System.err.println("Invalid URL: " + e.getMessage());
                  return false;
                }
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

              private static String readResponse(HttpURLConnection conn) throws IOException {
                InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400)
                    ? conn.getInputStream()
                    : conn.getErrorStream();

                if (is == null) {
                  throw new IOException("Cannot get response stream, response code: " + conn.getResponseCode());
                }

                try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
                  StringBuilder sb = new StringBuilder();
                  String line;
                  while ((line = br.readLine()) != null) {
                    sb.append(line);
                    sb.append("\n");
                  }
                  return sb.toString();
                }
              }

              public static String createTask() throws Exception {
                JSONObject body = new JSONObject()
                    .put("model", "wanx2.1-vace-plus")
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

                if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
                  String errorMessage = jsonResponse.optString("message", "Unknown error");
                  throw new RuntimeException("Failed to create task: " + errorMessage + ", details: " + resp);
                }
                JSONObject output = jsonResponse.getJSONObject("output");
                return output.getString("task_id");
              }

              public static String pollResult(String taskId) throws Exception {
                while (true) {
                  String resp = httpGet("/tasks/" + taskId);
                  JSONObject responseJson = new JSONObject(resp);

                  if (!responseJson.has("output")) {
                    throw new RuntimeException("API response is missing the 'output' field: " + resp);
                  }

                  JSONObject output = responseJson.getJSONObject("output");
                  String status = output.getString("task_status");
                  System.out.println("Status: " + status);

                  if ("SUCCEEDED".equals(status)) {
                    return output.getString("video_url");
                  } else if ("FAILED".equals(status) || "CANCELLED".equals(status)) {
                    String message = output.optString("message", "Unknown error");
                    throw new RuntimeException("Task failed: " + message + ", Task ID: " + taskId + ", details: " + resp);
                  }
                  Thread.sleep(15000);
                }
              }

              public static void main(String[] args) {
                try {
                  System.out.println("Creating video synthesis task...");
                  String taskId = createTask();
                  System.out.println("Task created successfully, Task ID: " + taskId);
                  System.out.println("Polling for task result...");
                  String videoUrl = pollResult(taskId);
                  System.out.println("Video URL: " + videoUrl);
                } catch (Exception e) {
                  System.err.println("An error occurred: " + e.getMessage());
                  e.printStackTrace();
                }
              }

            }
        - lang: curl
          label: cURL - 视频重绘
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "wanx2.1-vace-plus",
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
        - lang: python
          label: Python - 视频重绘
          source: |-
            import os
            import requests
            import time

            BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
            API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

            def create_task():
              """创建视频重绘任务，返回 task_id"""
              try:
                resp = requests.post(
                  f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
                  headers={
                    "X-DashScope-Async": "enable",
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                  },
                  json={
                    "model": "wanx2.1-vace-plus",
                    "input": {
                      "function": "video_repainting",
                      "prompt": "The video shows a black steampunk-style car driven by a gentleman, adorned with gears and copper pipes. The background is a steam-powered candy factory with retro elements, creating a vintage and playful scene.",
                      "video_url": "http://wanx.alicdn.com/material/20250318/video_repainting_1.mp4"
                    },
                    "parameters": {
                      "prompt_extend": False, # 建议视频重绘时关闭提示词改写。
                      "control_condition": "depth" # 可选：posebodyface、posebody、depth、scribble
                    }
                  },
                  timeout=30
                )
                resp.raise_for_status()
                return resp.json()["output"]["task_id"]
              except requests.RequestException as e:
                raise RuntimeError(f"Failed to create task: {e}")

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
                  print(f"Status: {status}")

                  if status == "SUCCEEDED":
                    return data["video_url"]
                  elif status in ("FAILED", "CANCELLED"):
                    raise RuntimeError(f"Task failed: {data.get('message', 'Unknown error')}")
                  time.sleep(15)
                except requests.RequestException as e:
                  print(f"Polling exception: {e}, retrying in 15 seconds...")
                  time.sleep(15)

            if __name__ == "__main__":
              task_id = create_task()
              print(f"Task ID: {task_id}")
              video_url = poll_result(task_id)
              print(f"\nVideo generated successfully: {video_url}")
        - lang: java
          label: Java - 视频重绘
          source: |-
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
                  throw new IllegalStateException("DASHSCOPE_API_KEY is not set");
                }
                COMMON_HEADERS.put("Authorization", "Bearer " + API_KEY);
                System.setProperty("http.keepAlive", "true");
                System.setProperty("http.maxConnections", "20");
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

              private static String readResponse(HttpURLConnection conn) throws IOException {
                InputStream is = (conn.getResponseCode() >= 200 && conn.getResponseCode() < 400)
                    ? conn.getInputStream()
                    : conn.getErrorStream();
                if (is == null) throw new IOException("Cannot get response stream, response code: " + conn.getResponseCode());
                try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
                  StringBuilder sb = new StringBuilder();
                  String line;
                  while ((line = br.readLine()) != null) {
                    sb.append(line).append("\n");
                  }
                  return sb.toString();
                }
              }

              public static String createTask() throws Exception {
                JSONObject body = new JSONObject()
                    .put("model", "wanx2.1-vace-plus")
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
                  String errorMessage = jsonResponse.optString("message", "Unknown error");
                  throw new RuntimeException("Failed to create task: " + errorMessage);
                }
                return jsonResponse.getJSONObject("output").getString("task_id");
              }

              public static String pollResult(String taskId) throws Exception {
                while (true) {
                  String resp = httpGet("/tasks/" + taskId);
                  JSONObject output = new JSONObject(resp).getJSONObject("output");
                  String status = output.getString("task_status");
                  System.out.println("Status: " + status);

                  if ("SUCCEEDED".equals(status)) {
                    return output.getString("video_url");
                  } else if ("FAILED".equals(status) || "CANCELLED".equals(status)) {
                    throw new RuntimeException("Task failed: " + output.optString("message", "Unknown error"));
                  }
                  Thread.sleep(15000);
                }
              }

              public static void main(String[] args) {
                try {
                  System.out.println("Creating video repainting task...");
                  String taskId = createTask();
                  System.out.println("Task created successfully, Task ID: " + taskId);
                  System.out.println("Polling for task result...");
                  String videoUrl = pollResult(taskId);
                  System.out.println("Video URL: " + videoUrl);
                } catch (Exception e) {
                  System.err.println("An error occurred: " + e.getMessage());
                  e.printStackTrace();
                }
              }
            }
        - lang: curl
          label: cURL - 局部编辑
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "wanx2.1-vace-plus",
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
                "expand_ratio": 0.05
              }
            }'
        - lang: python
          label: Python - 局部编辑
          source: |-
            import os
            import requests
            import time

            BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
            API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

            def create_task():
              """创建局部编辑任务，返回 task_id"""
              try:
                resp = requests.post(
                  f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
                  headers={
                    "X-DashScope-Async": "enable",
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                  },
                  json={
                    "model": "wanx2.1-vace-plus",
                    "input": {
                      "function": "video_edit",
                      "prompt": "The video shows a Parisian-style French cafe where a lion in a suit is elegantly sipping coffee. It holds a coffee cup in one hand, taking a gentle sip with a relaxed expression. The cafe is tastefully decorated, with soft tones and warm lighting illuminating the area where the lion is.",
                      "mask_image_url": "http://wanx.alicdn.com/material/20250318/video_edit_1_mask.png",
                      "video_url": "http://wanx.alicdn.com/material/20250318/video_edit_2.mp4",
                      "mask_frame_id": 1 # 蒙版对应的视频帧索引
                    },
                    "parameters": {
                      "prompt_extend": False,
                      "mask_type": "tracking", # 跟踪模式
                      "expand_ratio": 0.05
                    }
                  },
                  timeout=30
                )
                resp.raise_for_status()
                return resp.json()["output"]["task_id"]
              except requests.RequestException as e:
                raise RuntimeError(f"Failed to create task: {e}")

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
                  print(f"Status: {status}")

                  if status == "SUCCEEDED":
                    return data["video_url"]
                  elif status in ("FAILED", "CANCELLED"):
                    raise RuntimeError(f"Task failed: {data.get('message', 'Unknown error')}")
                  time.sleep(15)
                except requests.RequestException as e:
                  print(f"Polling exception: {e}, retrying in 15 seconds...")
                  time.sleep(15)

            if __name__ == "__main__":
              task_id = create_task()
              print(f"Task ID: {task_id}")
              video_url = poll_result(task_id)
              print(f"\nVideo generated successfully: {video_url}")
        - lang: java
          label: Java - 局部编辑
          source: |-
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
                  throw new IllegalStateException("DASHSCOPE_API_KEY is not set");
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

              public static String createTask() throws Exception {
                JSONObject body = new JSONObject()
                    .put("model", "wanx2.1-vace-plus")
                    .put("input", new JSONObject()
                        .put("function", "video_edit")
                        .put("prompt", "The video shows a Parisian-style French cafe where a lion in a suit is elegantly sipping coffee. It holds a coffee cup in one hand, taking a gentle sip with a relaxed expression. The cafe is tastefully decorated, with soft tones and warm lighting illuminating the area where the lion is.")
                        .put("mask_image_url", "http://wanx.alicdn.com/material/20250318/video_edit_1_mask.png")
                        .put("video_url", "http://wanx.alicdn.com/material/20250318/video_edit_2.mp4")
                        .put("mask_frame_id", 1))
                    .put("parameters", new JSONObject()
                        .put("prompt_extend", false)
                        .put("mask_type", "tracking")
                        .put("expand_ratio", 0.05));

                String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
                JSONObject jsonResponse = new JSONObject(resp);

                if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
                  String errorMessage = jsonResponse.optString("message", "Unknown error");
                  throw new RuntimeException("Failed to create task: " + errorMessage);
                }
                return jsonResponse.getJSONObject("output").getString("task_id");
              }

              public static String pollResult(String taskId) throws Exception {
                while (true) {
                  String resp = httpGet("/tasks/" + taskId);
                  JSONObject output = new JSONObject(resp).getJSONObject("output");
                  String status = output.getString("task_status");
                  System.out.println("Status: " + status);

                  if ("SUCCEEDED".equals(status)) return output.getString("video_url");
                  else if ("FAILED".equals(status) || "CANCELLED".equals(status))
                    throw new RuntimeException("Task failed: " + output.optString("message"));
                  Thread.sleep(15000);
                }
              }

              public static void main(String[] args) {
                try {
                  System.out.println("Creating local editing task...");
                  String taskId = createTask();
                  System.out.println("Task created successfully, Task ID: " + taskId);
                  String videoUrl = pollResult(taskId);
                  System.out.println("Video URL: " + videoUrl);
                } catch (Exception e) {
                  e.printStackTrace();
                }
              }
            }
        - lang: curl
          label: cURL - 视频续写
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "wanx2.1-vace-plus",
              "input": {
                "function": "video_extension",
                "prompt": "A dog wearing sunglasses is skateboarding on the street, 3D cartoon.",
                "first_clip_url": "http://wanx.alicdn.com/material/20250318/video_extension_1.mp4"
              },
              "parameters": {
                "prompt_extend": false
              }
            }'
        - lang: python
          label: Python - 视频续写
          source: |-
            import os
            import requests
            import time

            BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
            API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

            def create_task():
              """创建视频续写任务，返回 task_id"""
              try:
                resp = requests.post(
                  f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
                  headers={
                    "X-DashScope-Async": "enable",
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                  },
                  json={
                    "model": "wanx2.1-vace-plus",
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
                raise RuntimeError(f"Failed to create task: {e}")

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
                  print(f"Status: {status}")

                  if status == "SUCCEEDED":
                    return data["video_url"]
                  elif status in ("FAILED", "CANCELLED"):
                    raise RuntimeError(f"Task failed: {data.get('message', 'Unknown error')}")
                  time.sleep(15)
                except requests.RequestException as e:
                  print(f"Polling exception: {e}, retrying in 15 seconds...")
                  time.sleep(15)

            if __name__ == "__main__":
              task_id = create_task()
              print(f"Task ID: {task_id}")
              video_url = poll_result(task_id)
              print(f"\nVideo generated successfully: {video_url}")
        - lang: java
          label: Java - 视频续写
          source: |-
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
                  throw new IllegalStateException("DASHSCOPE_API_KEY is not set");
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

              public static String createTask() throws Exception {
                JSONObject body = new JSONObject()
                    .put("model", "wanx2.1-vace-plus")
                    .put("input", new JSONObject()
                        .put("function", "video_extension")
                        .put("prompt", "A dog wearing sunglasses is skateboarding on the street, 3D cartoon.")
                        .put("first_clip_url", "http://wanx.alicdn.com/material/20250318/video_extension_1.mp4"))
                    .put("parameters", new JSONObject()
                        .put("prompt_extend", false));

                String resp = httpPost("/services/aigc/video-generation/video-synthesis", body);
                JSONObject jsonResponse = new JSONObject(resp);

                if (jsonResponse.has("code") && jsonResponse.getInt("code") != 200) {
                  String errorMessage = jsonResponse.optString("message", "Unknown error");
                  throw new RuntimeException("Failed to create task: " + errorMessage);
                }
                return jsonResponse.getJSONObject("output").getString("task_id");
              }

              public static String pollResult(String taskId) throws Exception {
                while (true) {
                  String resp = httpGet("/tasks/" + taskId);
                  JSONObject output = new JSONObject(resp).getJSONObject("output");
                  String status = output.getString("task_status");
                  System.out.println("Status: " + status);

                  if ("SUCCEEDED".equals(status)) return output.getString("video_url");
                  else if ("FAILED".equals(status) || "CANCELLED".equals(status))
                    throw new RuntimeException("Task failed: " + output.optString("message"));
                  Thread.sleep(15000);
                }
              }

              public static void main(String[] args) {
                try {
                  System.out.println("Creating video extension task...");
                  String taskId = createTask();
                  System.out.println("Task created successfully, Task ID: " + taskId);
                  String videoUrl = pollResult(taskId);
                  System.out.println("Video URL: " + videoUrl);
                } catch (Exception e) {
                  e.printStackTrace();
                }
              }
            }
        - lang: curl
          label: cURL - 画面扩展
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
            --header 'X-DashScope-Async: enable' \
            --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
            --header 'Content-Type: application/json' \
            --data '{
              "model": "wanx2.1-vace-plus",
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
        - lang: python
          label: Python - 画面扩展
          source: |-
            import os
            import requests
            import time

            BASE_URL = "https://dashscope.aliyuncs.com/api/v1"
            API_KEY = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

            def create_task():
              """创建视频画面扩展任务，返回 task_id"""
              try:
                resp = requests.post(
                  f"{BASE_URL}/services/aigc/video-generation/video-synthesis",
                  headers={
                    "X-DashScope-Async": "enable",
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                  },
                  json={
                    "model": "wanx2.1-vace-plus",
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
                raise RuntimeError(f"Failed to create task: {e}")

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
                  print(f"Status: {status}")

                  if status == "SUCCEEDED":
                    return data["video_url"]
                  elif status in ("FAILED", "CANCELLED"):
                    raise RuntimeError(f"Task failed: {data.get('message', 'Unknown error')}")
                  time.sleep(15)
                except requests.RequestException as e:
                  print(f"Polling exception: {e}, retrying in 15 seconds...")
                  time.sleep(15)

            if __name__ == "__main__":
              task_id = create_task()
              print(f"Task ID: {task_id}")
              video_url = poll_result(task_id)
              print(f"\nVideo generated successfully: {video_url}")
        - lang: java
          label: Java - 画面扩展
          source: |-
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
                  throw new IllegalStateException("DASHSCOPE_API_KEY is not set");
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

              public static String createTask() throws Exception {
                JSONObject body = new JSONObject()
                    .put("model", "wanx2.1-vace-plus")
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
                  String errorMessage = jsonResponse.optString("message", "Unknown error");
                  throw new RuntimeException("Failed to create task: " + errorMessage);
                }
                return jsonResponse.getJSONObject("output").getString("task_id");
              }

              public static String pollResult(String taskId) throws Exception {
                while (true) {
                  String resp = httpGet("/tasks/" + taskId);
                  JSONObject output = new JSONObject(resp).getJSONObject("output");
                  String status = output.getString("task_status");
                  System.out.println("Status: " + status);

                  if ("SUCCEEDED".equals(status)) return output.getString("video_url");
                  else if ("FAILED".equals(status) || "CANCELLED".equals(status))
                    throw new RuntimeException("Task failed: " + output.optString("message"));
                  Thread.sleep(15000);
                }
              }

              public static void main(String[] args) {
                try {
                  System.out.println("Creating video frame expansion task...");
                  String taskId = createTask();
                  System.out.println("Task created successfully, Task ID: " + taskId);
                  String videoUrl = pollResult(taskId);
                  System.out.println("Video URL: " + videoUrl);
                } catch (Exception e) {
                  e.printStackTrace();
                }
              }
            }
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    VideoEditingRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。
          enum:
            - wanx2.1-vace-plus
          example: wanx2.1-vace-plus
        input:
          $ref: "#/components/schemas/VideoEditingInput"
        parameters:
          $ref: "#/components/schemas/VideoEditingParameters"
    VideoEditingInput:
      type: object
      required:
        - function
        - prompt
      description: 视频编辑的输入数据，各功能所需字段不同。
      properties:
        function:
          type: string
          description: 要使用的视频编辑能力。
          enum:
            - image_reference
            - video_repainting
            - video_edit
            - video_extension
            - video_outpainting
          example: image_reference
        prompt:
          type: string
          description: 对目标视频内容的文字描述。
          example: In the video, a girl walks out from the depths of an ancient, misty forest.
        ref_images_url:
          type: array
          description: 参考图像 URL 数组。`image_reference` 功能使用（1-3 张图像），`video_repainting` 和 `video_edit` 可选使用（1 张图像，用于替换主体）。
          items:
            type: string
            format: uri
          minItems: 1
          maxItems: 3
          example:
            - http://wanx.alicdn.com/material/20250318/image_reference_2_5_16.png
            - http://wanx.alicdn.com/material/20250318/image_reference_1_5_16.png
        video_url:
          type: string
          format: uri
          description: 输入视频的 URL。`video_repainting`、`video_edit` 和 `video_outpainting` 必填。格式须为 MP4，大小不超过 50 MB，时长不超过 5 秒。
          example: http://wanx.alicdn.com/material/20250318/video_repainting_1.mp4
        mask_image_url:
          type: string
          format: uri
          description: 用于 `video_edit` 的蒙版图像 URL。白色区域将被编辑，黑色区域保持不变。与 `mask_video_url` 二选一。
        mask_video_url:
          type: string
          format: uri
          description: 用于 `video_edit` 的蒙版视频 URL。与 `mask_image_url` 二选一，推荐使用 `mask_image_url`。
        mask_frame_id:
          type: integer
          description: 用于带 `mask_image_url` 的 `video_edit`：指定蒙版对应的视频帧索引。默认为第一帧（0）。
          default: 0
          example: 1
        first_clip_url:
          type: string
          format: uri
          description: 用于 `video_extension`：第一段视频片段的 URL（不超过 3 秒）。模型将基于此片段生成后续内容。
        last_clip_url:
          type: string
          format: uri
          description: 用于 `video_extension`：最后一段视频片段的 URL（不超过 3 秒）。模型将生成其前面的内容。
        first_frame_url:
          type: string
          format: uri
          description: 用于 `video_extension`：首帧图像的 URL，视频将从该帧向后延伸生成。
        last_frame_url:
          type: string
          format: uri
          description: 用于 `video_extension`：末帧图像的 URL，视频将从该帧向前追溯生成。
    VideoEditingParameters:
      type: object
      description: 视频编辑的生成参数，可用参数因功能而异。
      properties:
        prompt_extend:
          type: boolean
          description: 启用提示词改写。`true`（默认）：模型自动优化提示词；`false`：原样使用提示词。`video_repainting` 时建议关闭此项。
          default: true
        size:
          type: string
          description: 输出分辨率，格式为 `宽*高`。用于 `image_reference` 和 `video_edit`。
          example: 1280*720
        obj_or_bg:
          type: array
          description: 用于 `image_reference`：标识每张参考图像为主体（`obj`）或背景（`bg`）。数组长度须与 `ref_images_url` 一致。
          items:
            type: string
            enum:
              - obj
              - bg
          example:
            - obj
            - bg
        control_condition:
          type: string
          description: 用于 `video_repainting`：视频特征提取方式，决定保留原视频中的哪些特征。
          enum:
            - posebodyface
            - posebody
            - depth
            - scribble
          example: depth
        strength:
          type: number
          description: 用于 `video_repainting`：控制特征提取强度。值越高，输出越接近原视频；值越低，创意空间越大。
          minimum: 0
          maximum: 1
          default: 1
        mask_type:
          type: string
          description: 用于 `video_edit`：指定编辑区域的行为。`tracking`（默认）：编辑区域自动跟随目标运动；`fixed`：编辑区域固定不动。
          enum:
            - tracking
            - fixed
          default: tracking
        expand_ratio:
          type: number
          description: "用于带 `mask_type: tracking` 的 `video_edit`：蒙版区域向外扩展的比例。值越小越贴合目标，值越大扩展范围越广。"
          minimum: 0
          maximum: 1
          default: 0.05
        top_scale:
          type: number
          description: 用于 `video_outpainting`：向上扩展比例。设为 1.5 时，顶部扩展至原高度的 1.5 倍。
          minimum: 1
          maximum: 2
          default: 1
        bottom_scale:
          type: number
          description: 用于 `video_outpainting`：向下扩展比例。
          minimum: 1
          maximum: 2
          default: 1
        left_scale:
          type: number
          description: 用于 `video_outpainting`：向左扩展比例。
          minimum: 1
          maximum: 2
          default: 1
        right_scale:
          type: number
          description: 用于 `video_outpainting`：向右扩展比例。
          minimum: 1
          maximum: 2
          default: 1
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务创建成功后的响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符，可使用 `GET /tasks/{task_id}` 轮询任务结果。
            task_status:
              type: string
              description: 初始任务状态，通常为 `PENDING`。
              enum:
                - PENDING
    TaskStatusResponse:
      type: object
      description: 包含视频编辑任务当前状态与结果的响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务标识符。
            task_status:
              type: string
              description: 当前任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELLED
            video_url:
              type: string
              format: uri
              description: 生成的视频 URL，仅在 `task_status` 为 `SUCCEEDED` 时存在。有效期 24 小时，请及时下载。
            code:
              type: string
              description: 错误代码，仅在 `task_status` 为 `FAILED` 时存在。
            message:
              type: string
              description: 错误信息，仅在 `task_status` 为 `FAILED` 时存在。
        usage:
          type: object
          description: 用量统计（仅在任务成功时存在）。
          properties:
            video_count:
              type: integer
              description: 生成的视频数量。
            video_duration:
              type: integer
              description: 生成视频的时长（秒）。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 唯一请求标识符。
        code:
          type: string
          description: 错误代码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 可读的错误描述。
          example: "Invalid parameter: function"
````
