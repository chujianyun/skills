> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创建克隆音色

> 上传音频创建克隆音色。无需训练，即时返回音色名称。

<Warning>
  `model` 是克隆模型（固定为 `qwen-voice-enrollment`）。`target_model` 是用于合成克隆音色的语音合成模型。后续合成调用中的 `model` 必须与此处的 `target_model` 一致，否则会导致调用失败。
</Warning>

<Expandable title="Base64 编码示例">
  Python：

  ```python
  import base64, pathlib

  # 将 input.mp3 替换为您的音频文件路径
  file_path = pathlib.Path("input.mp3")
  base64_str = base64.b64encode(file_path.read_bytes()).decode()
  data_uri = f"data:audio/mpeg;base64,{base64_str}"
  ```

  Java：

  ```java
  import java.nio.file.*;
  import java.util.Base64;

  public class Main {
    public static String toDataUrl(String filePath) throws Exception {
      byte[] bytes = Files.readAllBytes(Paths.get(filePath));
      String encoded = Base64.getEncoder().encodeToString(bytes);
      return "data:audio/mpeg;base64," + encoded;
    }

    public static void main(String[] args) throws Exception {
      System.out.println(toDataUrl("input.mp3"));
    }
  }
  ```
</Expandable>

<Warning>
  您须确保对提供的音频拥有合法所有权和使用权。使用本 API 前，请阅读[服务条款](https://terms.alicdn.com/legal-agreement/terms/b_platform_service_agreement/20240229113512917/20240229113512917.html)。
</Warning>

## OpenAPI

````yaml post /services/audio/tts/customization
openapi: 3.1.0
info:
  title: 千问AI平台 声音克隆 API
  description: 从音频克隆声音，用于 Qwen TTS 模型的语音合成。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 中国大陆
security:
  - BearerAuth: []
paths:
  /services/audio/tts/customization:
    post:
      operationId: createClonedVoice
      summary: 创建克隆声音
      description: 上传音频以创建克隆声音。立即返回声音名称，无需训练。将声音名称用于 [Qwen TTS](/api-reference/speech-synthesis/qwen-tts) 或[实时流式 TTS](/developer-guides/speech/realtime-streaming)。
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/CreateClonedVoiceRequest"
      responses:
        "200":
          description: 声音克隆成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/CreateClonedVoiceResponse"
        "400":
          description: 无效请求
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
                "action": "create",
                "target_model": "qwen3-tts-vc-realtime-2026-01-15",
                "preferred_name": "guanyu",
                "audio": {
                  "data": "https://xxx.wav"
                }
              }
            }'
        - lang: python
          label: Python
          source: |-
            import os
            import requests
            import base64, pathlib

            target_model = "qwen3-tts-vc-realtime-2026-01-15"
            preferred_name = "guanyu"
            audio_mime_type = "audio/mpeg"

            file_path = pathlib.Path("input.mp3")
            base64_str = base64.b64encode(file_path.read_bytes()).decode()
            data_uri = f"data:{audio_mime_type};base64,{base64_str}"

            api_key = os.getenv("DASHSCOPE_API_KEY")
            url = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization"

            payload = {
              "model": "qwen-voice-enrollment", # 请勿修改此值
              "input": {
                "action": "create",
                "target_model": target_model,
                "preferred_name": preferred_name,
                "audio": {
                  "data": data_uri
                }
              }
            }

            headers = {
              "Authorization": f"Bearer {api_key}",
              "Content-Type": "application/json"
            }

            # 发送 POST 请求
            resp = requests.post(url, json=payload, headers=headers)

            if resp.status_code == 200:
              data = resp.json()
              voice = data["output"]["voice"]
              print(f"Generated voice parameter: {voice}")
            else:
              print("Request failed:", resp.status_code, resp.text)
        - lang: java
          label: Java
          source: |-
            import com.google.gson.Gson;
            import com.google.gson.JsonObject;

            import java.io.*;
            import java.net.HttpURLConnection;
            import java.net.URL;
            import java.nio.file.*;
            import java.util.Base64;

            public class Main {
              private static final String TARGET_MODEL = "qwen3-tts-vc-realtime-2026-01-15";
              private static final String PREFERRED_NAME = "guanyu";
              private static final String AUDIO_FILE = "input.mp3";
              private static final String AUDIO_MIME_TYPE = "audio/mpeg";

              public static String toDataUrl(String filePath) throws Exception {
                byte[] bytes = Files.readAllBytes(Paths.get(filePath));
                String encoded = Base64.getEncoder().encodeToString(bytes);
                return "data:" + AUDIO_MIME_TYPE + ";base64," + encoded;
              }

              public static void main(String[] args) {
                String apiKey = System.getenv("DASHSCOPE_API_KEY");
                String apiUrl = "https://dashscope.aliyuncs.com/api/v1/services/audio/tts/customization";

                try {
                  String jsonPayload =
                      "{"
                          + "\"model\": \"qwen-voice-enrollment\"," // 请勿修改此值
                          + "\"input\": {"
                          +     "\"action\": \"create\","
                          +     "\"target_model\": \"" + TARGET_MODEL + "\","
                          +     "\"preferred_name\": \"" + PREFERRED_NAME + "\","
                          +     "\"audio\": {"
                          +         "\"data\": \"" + toDataUrl(AUDIO_FILE) + "\""
                          +     "}"
                          + "}"
                          + "}";

                  HttpURLConnection con = (HttpURLConnection) new URL(apiUrl).openConnection();
                  con.setRequestMethod("POST");
                  con.setRequestProperty("Authorization", "Bearer " + apiKey);
                  con.setRequestProperty("Content-Type", "application/json");
                  con.setDoOutput(true);

                  try (OutputStream os = con.getOutputStream()) {
                    os.write(jsonPayload.getBytes("UTF-8"));
                  }

                  int status = con.getResponseCode();
                  InputStream is = (status >= 200 && status < 300)
                      ? con.getInputStream()
                      : con.getErrorStream();

                  StringBuilder response = new StringBuilder();
                  try (BufferedReader br = new BufferedReader(new InputStreamReader(is, "UTF-8"))) {
                    String line;
                    while ((line = br.readLine()) != null) {
                      response.append(line);
                    }
                  }

                  System.out.println("HTTP status code: " + status);
                  System.out.println("Response content: " + response.toString());

                  if (status == 200) {
                    Gson gson = new Gson();
                    JsonObject jsonObj = gson.fromJson(response.toString(), JsonObject.class);
                    String voice = jsonObj.getAsJsonObject("output").get("voice").getAsString();
                    System.out.println("Generated voice parameter: " + voice);
                  }

                } catch (Exception e) {
                  e.printStackTrace();
                }
              }
            }
components:
  schemas:
    CreateClonedVoiceRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 声音克隆模型。固定为 `qwen-voice-enrollment`。
          enum:
            - qwen-voice-enrollment
          example: qwen-voice-enrollment
        input:
          type: object
          required:
            - action
            - target_model
            - preferred_name
            - audio
          properties:
            action:
              type: string
              description: 操作类型。固定为 `create`。
              enum:
                - create
              example: create
            target_model:
              type: string
              description: 克隆声音对应的语音合成模型。必须与后续合成调用中使用的模型一致。可选值：`qwen3-tts-vc-realtime-2026-01-15`、`qwen3-tts-vc-realtime-2025-11-27`（实时）、`qwen3-tts-vc-2026-01-22`（非实时）。
              enum:
                - qwen3-tts-vc-realtime-2026-01-15
                - qwen3-tts-vc-realtime-2025-11-27
                - qwen3-tts-vc-2026-01-22
              example: qwen3-tts-vc-realtime-2026-01-15
            preferred_name:
              type: string
              description: 声音名称中的关键词（支持数字、字母、下划线，最多 16 个字符）。会出现在生成的声音名称中。示例：`guanyu` 对应生成 `qwen-tts-vc-guanyu-voice-20250812105009984-838b`。
              maxLength: 16
              pattern: ^[a-zA-Z0-9_]+$
              example: guanyu
            audio:
              type: object
              required:
                - data
              properties:
                data:
                  type: string
                  description: 用于克隆的音频。支持两种格式：**Data URL** -- `data:<mediatype>;base64,<data>`（`<mediatype>` 为 `audio/wav`、`audio/mpeg` 或 `audio/mp4`；Base64 编码后的数据需小于 10 MB）。**音频 URL** -- 可公开访问的 URL（无需鉴权）。
                  example: https://xxx.wav
            text:
              type: string
              description: 与音频内容对应的文本。服务器会验证匹配程度，若差异过大则返回 `Audio.PreprocessError`。
              example: 可选。与音频内容对应的文本。
            language:
              type: string
              description: 音频语言。指定后必须与音频实际语言一致。
              enum:
                - zh
                - en
                - de
                - it
                - pt
                - es
                - ja
                - ko
                - fr
                - ru
              example: zh
    CreateClonedVoiceResponse:
      type: object
      properties:
        output:
          type: object
          properties:
            voice:
              type: string
              description: 生成的声音名称。在合成调用中将此值作为 `voice` 参数传入。
              example: qwen-tts-vc-guanyu-voice-20250812105009984-838b
            target_model:
              type: string
              description: 绑定到此声音的语音合成模型。
              example: qwen3-tts-vc-realtime-2026-01-15
            fallback_mode:
              type: boolean
              description: 当音频与模型不完全匹配时为 `true`，表示复刻效果可能不理想。
              example: false
            fallback_reason:
              type: string
              description: 降级原因。可能的值：`no_merged_segments`（无法合并音频段）、`no_valid_asr_segments`（无有效语音识别段）。仅在 `fallback_mode` 为 `true` 时返回。
              example: ""
        usage:
          type: object
          properties:
            count:
              type: integer
              description: 计费的声音创建次数。成功创建时固定为 `1`（每次计费 $0.01）。
              example: 1
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
          example: Audio.PreprocessError
        message:
          type: string
          description: 错误信息。
          example: Audio preprocessing failed.
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
````
