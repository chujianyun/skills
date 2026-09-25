> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 查询音色列表

> 分页查询账号下的声音列表。

## OpenAPI

````yaml post /services/audio/tts/customization
openapi: 3.1.0
info:
  title: 千问AI平台音色设计 API — 查询音色列表
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - BearerAuth: []
paths:
  /services/audio/tts/customization:
    post:
      operationId: listVoices
      summary: 查询音色列表
      description: 返回账号下的音色列表，支持分页查询。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ListVoicesRequest"
      responses:
        "200":
          description: 查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ListVoicesResponse"
      x-codeSamples:
        - lang: bash
          label: cURL
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen-voice-design",
              "input": {
                "action": "list",
                "page_size": 10,
                "page_index": 0
              }
            }'
        - lang: python
          label: Python
          source: |-
            import os
            import requests

            api_key = os.getenv("DASHSCOPE_API_KEY")
            url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"

            payload = {
              "model": "qwen-voice-design",  # 此值固定，请勿修改
              "input": {
                "action": "list",
                "page_size": 10,
                "page_index": 0
              }
            }

            headers = {
              "Authorization": f"Bearer {api_key}",
              "Content-Type": "application/json"
            }

            response = requests.post(url, json=payload, headers=headers)

            print("HTTP 状态码：", response.status_code)

            if response.status_code == 200:
              data = response.json()
              voice_list = data["output"]["voice_list"]

              print("已找到以下音色：")
              for item in voice_list:
                print(f"- 音色：{item['voice']}  创建时间：{item['gmt_create']}  模型：{item['target_model']}")
            else:
              print("请求失败：", response.text)
        - lang: java
          label: Java
          source: |-
            import com.google.gson.Gson;
            import com.google.gson.JsonArray;
            import com.google.gson.JsonObject;

            import java.io.BufferedReader;
            import java.io.InputStreamReader;
            import java.io.OutputStream;
            import java.net.HttpURLConnection;
            import java.net.URL;

            public class Main {
              public static void main(String[] args) {
                String apiKey = System.getenv("DASHSCOPE_API_KEY");
                String apiUrl = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization";

                String jsonPayload =
                    "{"
                        + "\"model\": \"qwen-voice-design\"," // 此值固定，请勿修改
                        + "\"input\": {"
                        +     "\"action\": \"list\","
                        +     "\"page_size\": 10,"
                        +     "\"page_index\": 0"
                        + "}"
                        + "}";

                try {
                  HttpURLConnection con = (HttpURLConnection) new URL(apiUrl).openConnection();
                  con.setRequestMethod("POST");
                  con.setRequestProperty("Authorization", "Bearer " + apiKey);
                  con.setRequestProperty("Content-Type", "application/json");
                  con.setDoOutput(true);

                  try (OutputStream os = con.getOutputStream()) {
                    os.write(jsonPayload.getBytes("UTF-8"));
                  }

                  int status = con.getResponseCode();
                  BufferedReader br = new BufferedReader(new InputStreamReader(
                      status >= 200 && status < 300 ? con.getInputStream() : con.getErrorStream(), "UTF-8"));

                  StringBuilder response = new StringBuilder();
                  String line;
                  while ((line = br.readLine()) != null) {
                    response.append(line);
                  }
                  br.close();

                  System.out.println("HTTP 状态码：" + status);
                  System.out.println("响应 JSON：" + response.toString());

                  if (status == 200) {
                    Gson gson = new Gson();
                    JsonObject jsonObj = gson.fromJson(response.toString(), JsonObject.class);
                    JsonArray voiceList = jsonObj.getAsJsonObject("output").getAsJsonArray("voice_list");

                    System.out.println("\n已找到以下音色：");
                    for (int i = 0; i < voiceList.size(); i++) {
                      JsonObject voiceItem = voiceList.get(i).getAsJsonObject();
                      String voice = voiceItem.get("voice").getAsString();
                      String gmtCreate = voiceItem.get("gmt_create").getAsString();
                      String targetModel = voiceItem.get("target_model").getAsString();

                      System.out.printf("- 音色：%s  创建时间：%s  模型：%s\n",
                          voice, gmtCreate, targetModel);
                    }
                  }

                } catch (Exception e) {
                  e.printStackTrace();
                }
              }
            }
components:
  schemas:
    ListVoicesRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 音色设计模型，固定值为 `qwen-voice-design`。
          enum:
            - qwen-voice-design
          example: qwen-voice-design
        input:
          type: object
          required:
            - action
          properties:
            action:
              type: string
              description: 操作类型，固定值为 `list`。
              enum:
                - list
              example: list
            page_index:
              type: integer
              description: 页码，从 0 开始计数，取值范围：0–200。
              default: 0
              minimum: 0
              maximum: 200
              example: 0
            page_size:
              type: integer
              description: 每页返回的结果数量，必须大于 0。
              default: 10
              minimum: 1
              example: 10
    ListVoicesResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            page_index:
              type: integer
              description: 当前页码。
              example: 0
            page_size:
              type: integer
              description: 每页条目数。
              example: 10
            total_count:
              type: integer
              description: 账号下的音色总数。
              example: 26
            voice_list:
              type: array
              description: 音色对象数组。
              items:
                $ref: "#/components/schemas/VoiceItem"
        usage:
          type: object
          description: 用量信息（查询操作时为空）。
        request_id:
          type: string
          description: 请求 ID，可用于问题排查。
          example: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    VoiceItem:
      type: object
      properties:
        voice:
          type: string
          description: 音色名称。
          example: qwen-tts-vd-announcer-voice-20251210170454-a1b2
        target_model:
          type: string
          description: 与该音色绑定的合成模型。
          example: qwen3-tts-vd-realtime-2026-01-15
        language:
          type: string
          description: 语言代码。
          example: en
        voice_prompt:
          type: string
          description: 音色描述。
          example: A composed middle-aged male announcer with a deep, rich and magnetic voice.
        preview_text:
          type: string
          description: 创建音色时使用的试听文本。
          example: Dear listeners, hello everyone. Welcome to the evening news.
        gmt_create:
          type: string
          description: 创建时间。
          example: 2025-12-10 17:04:54
        gmt_modified:
          type: string
          description: 最后修改时间。
          example: 2025-12-10 17:04:54
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````
