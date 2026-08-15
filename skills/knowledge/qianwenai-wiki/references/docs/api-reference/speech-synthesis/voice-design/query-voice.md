> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 查询音色详情

> 查询指定音色的详细信息。

## OpenAPI

````yaml post /services/audio/tts/customization
openapi: 3.1.0
info:
  title: 千问AI平台 音色设计 API — 查询音色
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
security:
  - BearerAuth: []
paths:
  /services/audio/tts/customization:
    post:
      operationId: queryVoice
      summary: 查询音色
      description: 返回指定音色的详细信息。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/QueryVoiceRequest"
      responses:
        "200":
          description: 音色查询成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/QueryVoiceResponse"
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
                "action": "query",
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

            voice_to_query = "qwen-tts-vd-announcer-voice-20251210145409-a1b2"  # 替换为实际音色名称

            payload = {
              "model": "qwen-voice-design",  # 此值固定，请勿修改
              "input": {
                "action": "query",
                "voice": voice_to_query
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

              print("音色详情：")
              print(f"- 音色名称：{output['voice']}")
              print(f"- 绑定模型：{output['target_model']}")
              print(f"- 语言：{output['language']}")
              print(f"- 音色描述：{output['voice_prompt']}")
              print(f"- 创建时间：{output['gmt_create']}")
              print(f"- 最后修改时间：{output['gmt_modified']}")
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
                String voiceToQuery = "qwen-tts-vd-announcer-voice-20251210145409-a1b2"; // 替换为实际音色名称

                String jsonPayload =
                    "{"
                        + "\"model\": \"qwen-voice-design\"," // 此值固定，请勿修改
                        + "\"input\": {"
                        +     "\"action\": \"query\","
                        +     "\"voice\": \"" + voiceToQuery + "\""
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
                    JsonObject output = jsonObj.getAsJsonObject("output");

                    System.out.println("音色详情：");
                    System.out.println("- 音色名称：" + output.get("voice").getAsString());
                    System.out.println("- 绑定模型：" + output.get("target_model").getAsString());
                    System.out.println("- 语言：" + output.get("language").getAsString());
                    System.out.println("- 音色描述：" + output.get("voice_prompt").getAsString());
                    System.out.println("- 创建时间：" + output.get("gmt_create").getAsString());
                    System.out.println("- 最后修改时间：" + output.get("gmt_modified").getAsString());
                  }

                } catch (Exception e) {
                  e.printStackTrace();
                }
              }
            }
components:
  schemas:
    QueryVoiceRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 音色定制模型。固定为 `qwen-voice-design`。
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
              description: 操作类型。固定为 `query`。
              enum:
                - query
              example: query
            voice:
              type: string
              description: 待查询的音色名称。可从[查询音色列表](/api-reference/speech-synthesis/voice-design/list-voices)接口的返回结果中获取。
              example: qwen-tts-vd-announcer-voice-20251210145409-a1b2
    QueryVoiceResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            voice:
              type: string
              description: 音色名称。
              example: qwen-tts-vd-announcer-voice-20251210145409-a1b2
            target_model:
              type: string
              description: 与该音色绑定的语音合成模型。
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
              description: 预览文本。
              example: Dear listeners, hello everyone.
            gmt_create:
              type: string
              description: 创建时间。
              example: 2025-12-10 14:54:09
            gmt_modified:
              type: string
              description: 最后修改时间。
              example: 2025-12-10 17:47:48
        usage:
          type: object
          properties:
            count:
              type: integer
              description: 固定为 `0`，查询操作不计费。
              example: 0
        request_id:
          type: string
          description: 请求 ID，可用于问题排查。
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
