> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 删除音色

> 删除音色并释放配额。

## OpenAPI

````yaml post /services/audio/tts/customization
openapi: 3.1.0
info:
  title: 千问AI平台 语音设计 API — 删除音色
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - BearerAuth: []
paths:
  /services/audio/tts/customization:
    post:
      operationId: deleteVoice
      summary: 删除音色
      description: 删除指定音色并释放其配额。每个账号最多可创建 1,000 个音色。超过一年未用于合成的音色将被自动删除。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/DeleteVoiceRequest"
      responses:
        "200":
          description: 音色删除成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DeleteVoiceResponse"
        "400":
          description: 音色不存在
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
              "model": "qwen-voice-design",
              "input": {
                "action": "delete",
                "voice": "qwen-tts-vd-announcer-voice-20251210145409-a1b2"
              }
            }'
        - lang: python
          label: Python
          source: |-
            import os
            import requests

            api_key = os.getenv("DASHSCOPE_API_KEY")
            url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"

            voice_to_delete = "qwen-tts-vd-announcer-voice-20251210145409-a1b2"  # 替换为实际音色名称

            payload = {
              "model": "qwen-voice-design",  # 此值固定，请勿修改
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
              output = data["output"]
              print("已删除音色：", output["voice"])
            else:
              print("请求失败：", response.text)
        - lang: java
          label: Java
          source: |-
            import java.io.BufferedReader;
            import java.io.InputStreamReader;
            import java.io.OutputStream;
            import java.net.HttpURLConnection;
            import java.net.URL;

            public class Main {
              public static void main(String[] args) {
                String apiKey = System.getenv("DASHSCOPE_API_KEY");
                String apiUrl = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization";
                String voiceToDelete = "qwen-tts-vd-announcer-voice-20251210145409-a1b2"; // 替换为实际音色名称

                String jsonPayload =
                    "{"
                        + "\"model\": \"qwen-voice-design\"," // 此值固定，请勿修改
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
                } catch (Exception e) {
                  e.printStackTrace();
                }
              }
            }
components:
  schemas:
    DeleteVoiceRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 语音设计模型，固定值为 `qwen-voice-design`。
          enum:
            - qwen-voice-design
          example: qwen-voice-design
        input:
          type: object
          required:
            - action
            - voice
          properties:
            action:
              type: string
              description: 操作类型，固定值为 `delete`。
              enum:
                - delete
              example: delete
            voice:
              type: string
              description: 要删除的音色名称，可通过[获取音色列表](/api-reference/speech-synthesis/voice-design/list-voices)接口查询。
              example: qwen-tts-vd-announcer-voice-20251210145409-a1b2
    DeleteVoiceResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            voice:
              type: string
              description: 已删除的音色名称。
              example: qwen-tts-vd-announcer-voice-20251210145409-a1b2
        usage:
          type: object
          description: 用量信息（删除操作时为空）。
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
          example: VoiceNotFound
        message:
          type: string
          description: 错误信息。
          example: "Voice not found: qwen-tts-vd-announcer-voice-xxxx"
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````
