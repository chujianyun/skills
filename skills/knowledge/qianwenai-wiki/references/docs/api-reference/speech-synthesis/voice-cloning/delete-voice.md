> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 删除克隆音色

> 删除克隆音色并释放配额。

## OpenAPI

````yaml post /services/audio/tts/customization
openapi: 3.1.0
info:
  title: 千问AI平台声音克隆 API — 删除声音
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: DashScope API 服务器
security:
  - BearerAuth: []
paths:
  /services/audio/tts/customization:
    post:
      operationId: deleteClonedVoice
      summary: 删除克隆声音
      description: 删除指定的克隆声音并释放其占用的配额。每个账号最多可创建 1,000 个声音。超过一年未用于合成的声音将被自动删除。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DeleteClonedVoiceRequest"
      responses:
        "200":
          description: 声音删除成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DeleteClonedVoiceResponse"
        "400":
          description: 声音不存在
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/ErrorResponse"
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
                "action": "delete",
                "voice": "yourVoice"
              }
            }'
        - lang: python
          label: Python
          source: |-
            import os
            import requests

            api_key = os.getenv("DASHSCOPE_API_KEY")
            url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"

            voice_to_delete = "yourVoice"  # 要删除的声音名称（替换为实际值）

            payload = {
              "model": "qwen-voice-enrollment", # 请勿修改此值
              "input": {
                "action": "delete",
                "voice": voice_to_delete
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
              request_id = data["request_id"]

              print(f"删除成功")
              print(f"请求 ID：{request_id}")
            else:
              print("请求失败：", response.text)
        - lang: java
          label: Java
          source: |-
            import com.google.gson.Gson;
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
                String voiceToDelete = "yourVoice"; // 要删除的声音名称（替换为实际值）

                String jsonPayload =
                    "{"
                        + "\"model\": \"qwen-voice-enrollment\"," // 请勿修改此值
                        + "\"input\": {"
                        +     "\"action\": \"delete\","
                        +     "\"voice\": \"" + voiceToDelete + "\""
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
                  System.out.println("响应内容：" + response.toString());

                  if (status == 200) {
                    Gson gson = new Gson();
                    JsonObject jsonObj = gson.fromJson(response.toString(), JsonObject.class);
                    String requestId = jsonObj.get("request_id").getAsString();

                    System.out.println("删除成功");
                    System.out.println("请求 ID：" + requestId);
                  }

                } catch (Exception e) {
                  e.printStackTrace();
                }
              }
            }
components:
  schemas:
    DeleteClonedVoiceRequest:
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
            - voice
          properties:
            action:
              type: string
              description: 操作类型，固定为 `delete`。
              enum:
                - delete
              example: delete
            voice:
              type: string
              description: 要删除的声音名称。可通过[查询克隆声音列表](/api-reference/speech-synthesis/voice-cloning/list-voices)接口获取声音名称。
              example: qwen-tts-vc-guanyu-voice-20250812105009984-838b
    DeleteClonedVoiceResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            voice:
              type: string
              description: 已删除的声音名称。
              example: qwen-tts-vc-guanyu-voice-20250812105009984-838b
        usage:
          type: object
          properties:
            count:
              type: integer
              description: 始终为 `0`。删除声音不计费。
              example: 0
        request_id:
          type: string
          description: 请求 ID，用于问题排查。
          example: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
    ErrorResponse:
      type: object
      properties:
        request_id:
          type: string
          example: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        code:
          type: string
          description: 错误码。
          example: BadRequest.VoiceNotFound
        message:
          type: string
          description: 错误信息。
          example: "Voice not found: yourVoice"
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````
