> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 查询克隆音色列表

> 分页查询当前账号下的克隆音色列表。

## OpenAPI

````yaml post /services/audio/tts/customization
openapi: 3.1.0
info:
  title: 千问AI平台声音克隆 API — 查询声音列表
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API
security:
  - BearerAuth: []
paths:
  /services/audio/tts/customization:
    post:
      operationId: listClonedVoices
      summary: 查询已克隆的音色列表
      description: 返回当前账号下已克隆音色的分页列表。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/ListClonedVoicesRequest"
      responses:
        "200":
          description: 声音列表获取成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ListClonedVoicesResponse"
      x-codeSamples:
        - lang: bash
          label: cURL
          source: |-
            curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen-voice-enrollment",
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
              "model": "qwen-voice-enrollment", # 此值固定，请勿修改
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

              print("已找到以下声音：")
              for item in voice_list:
                print(f"- 声音：{item['voice']}  创建时间：{item['gmt_create']}  模型：{item['target_model']}")
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
                        + "\"model\": \"qwen-voice-enrollment\"," // 此值固定，请勿修改
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

                    System.out.println("\n已找到以下声音：");
                    for (int i = 0; i < voiceList.size(); i++) {
                      JsonObject voiceItem = voiceList.get(i).getAsJsonObject();
                      String voice = voiceItem.get("voice").getAsString();
                      String gmtCreate = voiceItem.get("gmt_create").getAsString();
                      String targetModel = voiceItem.get("target_model").getAsString();

                      System.out.printf("- 声音：%s  创建时间：%s  模型：%s\n",
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
    ListClonedVoicesRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 声音克隆模型，固定为 `qwen-voice-enrollment`。
          enum:
            - qwen-voice-enrollment
          example: qwen-voice-enrollment
        input:
          type: object
          required:
            - action
          properties:
            action:
              type: string
              description: 操作类型，固定为 `list`。
              enum:
                - list
              example: list
            page_index:
              type: integer
              description: 页码（从 0 开始），范围：0 到 1000000。
              default: 0
              minimum: 0
              maximum: 1000000
              example: 0
            page_size:
              type: integer
              description: 每页返回条数，范围：1 到 1000000。
              default: 10
              minimum: 1
              maximum: 1000000
              example: 10
    ListClonedVoicesResponse:
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
              description: 每页条数。
              example: 10
            total_count:
              type: integer
              description: 声音总数。
              example: 2
            voice_list:
              type: array
              description: 声音对象数组。
              items:
                $ref: "#/components/schemas/VoiceItem"
        usage:
          type: object
          properties:
            count:
              type: integer
              description: 固定为 `0`，查询声音列表不计费。
              example: 0
        request_id:
          type: string
          description: 请求 ID，用于问题排查。
          example: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    VoiceItem:
      type: object
      properties:
        voice:
          type: string
          description: 声音名称，调用语音合成接口时作为 `voice` 参数传入。
          example: qwen-tts-vc-guanyu-voice-20250812105009984-838b
        gmt_create:
          type: string
          description: 声音创建时间。
          example: 2025-08-11 17:59:32
        gmt_modified:
          type: string
          description: 最后修改时间。
          example: 2025-08-11 17:59:32
        language:
          type: string
          description: 声音语言。
          example: zh
        target_model:
          type: string
          description: 与该声音绑定的语音合成模型。
          example: qwen3-tts-vc-realtime-2026-01-15
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````
