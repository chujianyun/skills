> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 录音文件转写

> 将音视频文件转为文字

千问AI平台提供多个模型系列用于录音文件转写：**Qwen-Audio-3.0-ASR-Flash** 支持热词、Prompt 上下文和说话人分离，**Fun-ASR** 支持高精度多语言转写与歌曲识别，**Qwen-ASR** 具备增强的语义理解能力，**Qwen-Omni** 支持基于提示词的上下文感知转写。

<Tip>
  有关模型可用性、支持语言和功能对比，请参见[语音识别模型](/developer-guides/speech/speech-to-text-models)。
</Tip>

## 快速开始

<Tabs>
  <Tab title="Qwen-Audio-3.0-ASR-Flash-Filetrans/Fun-ASR">
    **支持的模型**：

    - **Qwen-Audio-3.0-ASR-Flash-Filetrans**：qwen-audio-3.0-asr-flash-filetrans
    - **Qwen-Audio-3.0-ASR-Flash**：qwen-audio-3.0-asr-flash
    - **Fun-ASR**：fun-asr（稳定版，当前等同 fun-asr-2025-11-07）、fun-asr-2025-11-07（快照版）、fun-asr-2025-08-25（快照版）、fun-asr-mtl（稳定版，当前等同 fun-asr-mtl-2025-08-25）、fun-asr-mtl-2025-08-25（快照版）
    - **Fun-ASR-Flash**：fun-asr-flash-2026-06-15

    **支持语言**：

    - fun-asr 和 fun-asr-2025-11-07：普通话、粤语、吴语、闽南语、客家话、赣语、湘语、晋语、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语、斯洛伐克语。同时支持中原、西南、冀鲁、江淮、兰银、胶辽、东北、北京、港台等地区的普通话口音。
    - fun-asr-2025-08-25：普通话和英语。
    - fun-asr-mtl 和 fun-asr-mtl-2025-08-25：普通话、粤语、英语、日语、韩语、越南语、泰语、印尼语、马来语、菲律宾语、印地语、阿拉伯语、法语、德语、西班牙语、葡萄牙语、俄语、意大利语、荷兰语、瑞典语、丹麦语、芬兰语、挪威语、希腊语、波兰语、捷克语、匈牙利语、罗马尼亚语、保加利亚语、克罗地亚语和斯洛伐克语。
    - fun-asr-flash-2026-06-15：同 fun-asr-2025-11-07。

    **支持采样率**：任意

    **支持音频格式**：aac、amr、avi、flac、flv、m4a、mkv、mov、mp3、mp4、mpeg、ogg、opus、wav、webm、wma、wmv

    ### 发起首次调用

    [获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。

    由于音视频文件通常较大，文件传输和语音识别可能需要较长时间。录音文件识别 API 采用异步调用方式提交任务。识别完成后，需要通过查询接口获取识别结果。

    #### 异步提交并同步等待

    提交任务后阻塞等待，直到任务完成。

    <CodeGroup>
      ```python Python
      from http import HTTPStatus
      from dashscope.audio.asr import Transcription
      from urllib import request
      import dashscope
      import os
      import json

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      # 如果您没有配置环境变量，请用 API Key 替换下行代码：dashscope.api_key = "sk-xxx"
      dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

      task_response = Transcription.async_call(
        model='qwen-audio-3.0-asr-flash-filetrans',
        file_urls=['https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/bjgrbu/hello_world_female_en.wav',
            'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/rlrbee/hello_world_male_en.wav'],
        language_hints=['zh', 'en']  # language_hints 为可选参数，用于指定音频的语言代码。取值范围请参见 API 参考文档。
      )

      transcription_response = Transcription.wait(task=task_response.output.task_id)

      if transcription_response.status_code == HTTPStatus.OK:
        for transcription in transcription_response.output['results']:
          if transcription['subtask_status'] == 'SUCCEEDED':
            url = transcription['transcription_url']
            result = json.loads(request.urlopen(url).read().decode('utf8'))
            print(json.dumps(result, indent=4,
            ensure_ascii=False))
          else:
            print('转写失败！')
            print(transcription)
      else:
        print('错误：', transcription_response.output.message)
      ```

      ```java Java
      import com.alibaba.dashscope.audio.asr.transcription.*;
      import com.alibaba.dashscope.utils.Constants;
      import com.google.gson.*;

      import java.io.BufferedReader;
      import java.io.InputStreamReader;
      import java.net.HttpURLConnection;
      import java.net.URL;
      import java.util.Arrays;
      import java.util.List;

      public class Main {
        public static void main(String[] args) {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
          // 创建转写请求参数
          TranscriptionParam param =
              TranscriptionParam.builder()
                  // 如果您没有配置环境变量，请用 API Key 替换下行代码：.apiKey("sk-xxx")
                  .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                  .model("qwen-audio-3.0-asr-flash-filetrans")
                  // language_hints 为可选参数，用于指定音频的语言代码。取值范围请参见 API 参考文档。
                  .parameter("language_hints", new String[]{"zh", "en"})
                  .fileUrls(
                      Arrays.asList(
                      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/bjgrbu/hello_world_female_en.wav",
                      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/rlrbee/hello_world_male_en.wav"))
                  .build();
          try {
            Transcription transcription = new Transcription();
            // 提交转写请求
            TranscriptionResult result = transcription.asyncCall(param);
            System.out.println("RequestId: " + result.getRequestId());
            // 检查任务是否提交成功
            if (result.getTaskId() == null) {
              System.out.println("Error: " + result.getOutput());
              System.exit(1);
            }
            // 阻塞等待任务完成并获取结果
            result = transcription.wait(
                TranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
            // 获取转写结果
            List<TranscriptionTaskResult> taskResultList = result.getResults();
            if (taskResultList != null && taskResultList.size() > 0) {
              for (TranscriptionTaskResult taskResult : taskResultList) {
                String transcriptionUrl = taskResult.getTranscriptionUrl();
                HttpURLConnection connection =
                    (HttpURLConnection) new URL(transcriptionUrl).openConnection();
                connection.setRequestMethod("GET");
                connection.connect();
                BufferedReader reader =
                    new BufferedReader(new InputStreamReader(connection.getInputStream()));
                Gson gson = new GsonBuilder().setPrettyPrinting().create();
                JsonElement jsonResult = gson.fromJson(reader, JsonObject.class);
                System.out.println(gson.toJson(jsonResult));
              }
            }
          } catch (Exception e) {
            System.out.println("error: " + e);
          }
          System.exit(0);
        }
      }
      ```
    </CodeGroup>

    <Accordion title="完整的识别结果以 JSON 格式输出到控制台。结果包含转写文本以及文本在音视频文件中的起止时间（单位为毫秒）。">
      **第一条结果**

      ```json
      {
        "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/bjgrbu/hello_world_female_en.wav",
        "properties": {
          "audio_format": "pcm_s16le",
          "channels": [
            0
          ],
          "original_sampling_rate": 24000,
          "original_duration_in_milliseconds": 3280
        },
        "transcripts": [
          {
            "channel_id": 0,
            "content_duration_in_milliseconds": 3000,
            "text": "Hello world, this is Alibaba Speech Lab. ",
            "sentences": [
              {
                "begin_time": 240,
                "end_time": 3240,
                "text": "Hello world, this is Alibaba Speech Lab. ",
                "sentence_id": 1,
                "words": [
                  {
                    "begin_time": 240,
                    "end_time": 640,
                    "text": "Hello",
                    "punctuation": ""
                  },
                  {
                    "begin_time": 640,
                    "end_time": 960,
                    "text": " world",
                    "punctuation": ","
                  },
                  {
                    "begin_time": 1280,
                    "end_time": 1480,
                    "text": " this",
                    "punctuation": ""
                  },
                  {
                    "begin_time": 1480,
                    "end_time": 1840,
                    "text": " is",
                    "punctuation": ""
                  },
                  {
                    "begin_time": 1840,
                    "end_time": 2520,
                    "text": " Alibaba",
                    "punctuation": ""
                  },
                  {
                    "begin_time": 2520,
                    "end_time": 2920,
                    "text": " Speech",
                    "punctuation": ""
                  },
                  {
                    "begin_time": 2920,
                    "end_time": 3240,
                    "text": " Lab",
                    "punctuation": ". "
                  }
                ]
              }
            ]
          }
        ]
      }
      ```

      **第二条结果**

      ```json
      {
        "file_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/rlrbee/hello_world_male_en.wav",
        "properties": {
          "audio_format": "pcm_s16le",
          "channels": [
            0
          ],
          "original_sampling_rate": 24000,
          "original_duration_in_milliseconds": 4000
        },
        "transcripts": [
          {
            "channel_id": 0,
            "content_duration_in_milliseconds": 3160,
            "text": "Hello world, this is Alibaba Speech Lab. ",
            "sentences": [
              {
                "begin_time": 800,
                "end_time": 3960,
                "text": "Hello world, this is Alibaba Speech Lab. ",
                "sentence_id": 1,
                "words": [
                  {
                    "begin_time": 800,
                    "end_time": 1200,
                    "text": "Hello",
                    "punctuation": ""
                  },
                  {
                    "begin_time": 1200,
                    "end_time": 1640,
                    "text": " world",
                    "punctuation": ","
                  },
                  {
                    "begin_time": 1880,
                    "end_time": 2120,
                    "text": " this",
                    "punctuation": ""
                  },
                  {
                    "begin_time": 2120,
                    "end_time": 2560,
                    "text": " is",
                    "punctuation": ""
                  },
                  {
                    "begin_time": 2560,
                    "end_time": 3360,
                    "text": " Alibaba",
                    "punctuation": ""
                  },
                  {
                    "begin_time": 3360,
                    "end_time": 3720,
                    "text": " Speech",
                    "punctuation": ""
                  },
                  {
                    "begin_time": 3720,
                    "end_time": 3960,
                    "text": " Lab",
                    "punctuation": ". "
                  }
                ]
              }
            ]
          }
        ]
      }
      ```
    </Accordion>

    #### 异步提交并轮询查询

    提交任务后通过轮询获取结果，而非阻塞等待。

    <CodeGroup>
      ```python Python
      from http import HTTPStatus
      from dashscope.audio.asr import Transcription
      import dashscope
      import os
      import json

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      # 如果您没有配置环境变量，请用 API Key 替换下行代码：dashscope.api_key = "sk-xxx"
      dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

      transcribe_response = Transcription.async_call(
        model='qwen-audio-3.0-asr-flash-filetrans',
        file_urls=['https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/bjgrbu/hello_world_female_en.wav',
            'https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/rlrbee/hello_world_male_en.wav']
      )

      while True:
        if transcribe_response.output.task_status == 'SUCCEEDED' or transcribe_response.output.task_status == 'FAILED':
          break
        transcribe_response = Transcription.fetch(task=transcribe_response.output.task_id)

      if transcribe_response.status_code == HTTPStatus.OK:
        print(json.dumps(transcribe_response.output, indent=4, ensure_ascii=False))
        print('转写完成！')
      ```

      ```java Java
      import com.alibaba.dashscope.audio.asr.transcription.*;
      import com.alibaba.dashscope.common.TaskStatus;
      import com.alibaba.dashscope.utils.Constants;
      import com.google.gson.*;

      import java.util.Arrays;

      public class Main {
        public static void main(String[] args) {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
          // 创建转写请求参数
          TranscriptionParam param =
              TranscriptionParam.builder()
                  // 如果您没有配置环境变量，请用 API Key 替换下行代码：.apiKey("sk-xxx")
                  .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                  .model("qwen-audio-3.0-asr-flash-filetrans")
                  .fileUrls(
                      Arrays.asList(
                          "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/bjgrbu/hello_world_female_en.wav",
                          "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/rlrbee/hello_world_male_en.wav"))
                  .build();
          try {
            Transcription transcription = new Transcription();
            // 提交转写请求
            TranscriptionResult result = transcription.asyncCall(param);
            System.out.println("RequestId: " + result.getRequestId());
            // 检查任务是否提交成功
            if (result.getTaskId() == null) {
              System.out.println("Error: " + result.getOutput());
              System.exit(1);
            }
            // 轮询任务执行结果，直到任务完成
            while (true) {
              result = transcription.fetch(TranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
              if (result.getTaskStatus() == TaskStatus.SUCCEEDED || result.getTaskStatus() == TaskStatus.FAILED) {
                break;
              }
              Thread.sleep(1000);
            }
            // 打印结果
            System.out.println(new GsonBuilder().setPrettyPrinting().create().toJson(result.getOutput()));
          } catch (Exception e) {
            System.out.println("error: " + e);
          }
          System.exit(0);
        }
      }
      ```
    </CodeGroup>

    <Note>
      **生产环境建议**

      - **文件托管**：将音频文件上传至阿里云 OSS，通过 URL 方式调用，避免使用本地文件上传（本地文件调用上限 100 QPS，不支持扩容）。
      - **异步轮询**：长音频转写采用异步模式，建议设置合理的轮询间隔（如 2\~5 秒），避免频繁查询消耗配额。如需突破 20–100 QPS 查询上限，可改用事件回调通知（参见[接收异步任务通知](/developer-guides/receive-async-task-notifications)）。
      - **错误处理**：实现完善的重试机制；网络超时或服务端临时错误（5xx）按指数退避策略重试。
      - **降噪处理**：噪声较大的音频建议先用 FFmpeg 等工具预处理后再提交识别。
      - **模型选择**：根据音频时长选择合适的模型。5 分钟以内的短音频使用 Qwen3-ASR-Flash，超过 5 分钟的长音频使用 Qwen-Audio-3.0-ASR-Flash-Filetrans、Fun-ASR 或 Qwen3-ASR-Flash-Filetrans。
    </Note>

    #### RESTful API

    使用任意 HTTP 库提交任务并轮询获取结果。以下 Python 示例演示了完整流程：

    ```python
    import requests
    import json
    import os
    import time

    # 如果您没有配置环境变量，请用 API Key 替换下行代码：api_key = "sk-xxx"
    api_key = os.getenv("DASHSCOPE_API_KEY")
    file_urls = [
      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/bjgrbu/hello_world_female_en.wav",
      "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260401/rlrbee/hello_world_male_en.wav",
    ]

    region = "dashscope.aliyuncs.com"

    # 提交录音文件转写任务，包含待转写的文件 URL 列表
    def submit_task(apikey, file_urls) -> str:

      headers = {
        "Authorization": f"Bearer {apikey}",
        "Content-Type": "application/json",
        "X-DashScope-Async": "enable",
      }
      data = {
        "model": "qwen-audio-3.0-asr-flash-filetrans",
        "input": {"file_urls": file_urls},
        "parameters": {
          "channel_id": [0],
          # "vocabulary_id": "vocab-Xxxx", # 可选，热词 ID。
        },
      }
      # 录音文件转写服务的 URL
      service_url = (
        f"https://{region}/api/v1/services/audio/asr/transcription"
      )
      response = requests.post(
        service_url, headers=headers, data=json.dumps(data)
      )

      # 打印响应内容
      if response.status_code == 200:
        return response.json()["output"]["task_id"]
      else:
        print("任务提交失败！")
        print(response.json())
        return None

    # 循环查询任务状态，直到任务完成
    def wait_for_complete(task_id):
      headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
      }

      pending = True
      while pending:
        # 任务状态查询服务的 URL
        service_url = f"https://{region}/api/v1/tasks/{task_id}"
        response = requests.get(
          service_url, headers=headers
        )
        if response.status_code == 200:
          status = response.json()['output']['task_status']
          if status == 'SUCCEEDED':
            print("任务完成！")
            pending = False
            return response.json()['output']['results']
          elif status == 'RUNNING' or status == 'PENDING':
            pass
          else:
            print("任务失败！")
            pending = False
        else:
          print("查询失败！")
          pending = False
        print(response.json())
        time.sleep(0.1)

    task_id = submit_task(apikey=api_key, file_urls=file_urls)
    print("task_id: ", task_id)
    result = wait_for_complete(task_id)
    print("转写结果：", result)
    ```

    #### 同步调用（Qwen-Audio-3.0-ASR-Flash/Fun-ASR-Flash）

    Qwen-Audio-3.0-ASR-Flash/Fun-ASR-Flash 系列模型支持对最长 5 分钟的音频文件进行同步调用，结果可以以流式或非流式方式返回。

    ```bash
    curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header "Content-Type: application/json" \
      --header "X-DashScope-SSE: disable" \
      --data '{
      "model": "qwen-audio-3.0-asr-flash",
      "input": {
        "messages": [
          {
            "role": "user",
            "content": [
              {
                "type": "input_audio",
                "input_audio": {
                  "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/paraformer/hello_world_female2.wav"
                }
              }
            ]
          }
        ]
      },
      "parameters": {
        "format": "wav",
        "sample_rate": "16000"
      }
    }'
    ```

    <Note>
      Qwen-Audio-3.0-ASR-Flash/Fun-ASR-Flash 系列模型通过 DashScope 同步调用接口（multimodal-generation 端点）返回的响应结构与标准 DashScope 多模态接口格式不同，实际返回结构为：

      ```json
      {
        "output": {
          "output": {
            "sentence": {
              "text": "识别文本内容"
            }
          },
          "text": "Hello World，这里是阿里巴巴语音实验室。"
        },
        "request_id": "..."
      }
      ```

      其中 `output.output.sentence.text` 和顶层 `output.text` 为识别文本字段，无 `choices` 字段，请据此解析响应。
    </Note>
  </Tab>

  <Tab title="Qwen-ASR">
    开始之前，请先[获取 API Key](/api-reference/preparation/api-key)。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。

    <Tabs>
      <Tab title="DashScope">
        <Tabs>
          <Tab title="Qwen3-ASR-Flash-Filetrans">
            Qwen3-ASR-Flash-Filetrans 专为音频文件的异步转写设计，支持最长 12 小时的录音。该模型需要输入可公开访问的音频文件 URL，不支持直接上传本地文件。这是一个非流式 API，在任务完成后返回完整的识别结果。

            <Tabs>
              <Tab title="cURL">
                使用 cURL 进行语音识别时，需先提交任务获取 task\_id，然后使用该 ID 查询任务结果。

                #### 提交任务

                ```bash
                curl -X POST 'https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H "Content-Type: application/json" \
                -H "X-DashScope-Async: enable" \
                -d '{
                  "model": "qwen3-asr-flash-filetrans",
                  "input": {
                    "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                  },
                  "parameters": {
                    "channel_id":[
                      0
                    ],
                    "enable_itn": false,
                    "enable_words": true
                  }
                }'
                ```

                #### 获取任务结果

                此查询接口默认 20 QPS、最高可扩容到 100 QPS。如需更高频次或避免轮询限流，建议配置异步任务回调（参见[接收异步任务通知](/developer-guides/receive-async-task-notifications)）。

                ```bash
                curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H "Content-Type: application/json"
                ```

                #### 完整示例

                <CodeGroup>
                  ```java Java
                  import com.google.gson.Gson;
                  import com.google.gson.annotations.SerializedName;
                  import okhttp3.*;

                  import java.io.IOException;
                  import java.util.concurrent.TimeUnit;

                  public class Main {
                    private static final String API_URL_SUBMIT = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription";
                    private static final String API_URL_QUERY = "https://dashscope.aliyuncs.com/api/v1/tasks/";
                    private static final Gson gson = new Gson();

                    public static void main(String[] args) {
                      // 如果您没有配置环境变量，请用 API Key 替换下行代码：String apiKey = "sk-xxx"
                      String apiKey = System.getenv("DASHSCOPE_API_KEY");

                      OkHttpClient client = new OkHttpClient();

                      // 1. 提交任务
                      String payloadJson = """
                          {
                            "model": "qwen3-asr-flash-filetrans",
                            "input": {
                              "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                            },
                            "parameters": {
                              "channel_id": [0],
                              "enable_itn": false,
                              "enable_words": true
                            }
                          }
                          """;

                      RequestBody body = RequestBody.create(payloadJson, MediaType.get("application/json; charset=utf-8"));
                      Request submitRequest = new Request.Builder()
                          .url(API_URL_SUBMIT)
                          .addHeader("Authorization", "Bearer " + apiKey)
                          .addHeader("Content-Type", "application/json")
                          .addHeader("X-DashScope-Async", "enable")
                          .post(body)
                          .build();

                      String taskId = null;

                      try (Response response = client.newCall(submitRequest).execute()) {
                        if (response.isSuccessful() && response.body() != null) {
                          String respBody = response.body().string();
                          ApiResponse apiResp = gson.fromJson(respBody, ApiResponse.class);
                          if (apiResp.output != null) {
                            taskId = apiResp.output.taskId;
                            System.out.println("任务已提交。task_id: " + taskId);
                          } else {
                            System.out.println("提交响应内容：" + respBody);
                            return;
                          }
                        } else {
                          System.out.println("任务提交失败！HTTP 状态码：" + response.code());
                          if (response.body() != null) {
                            System.out.println(response.body().string());
                          }
                          return;
                        }
                      } catch (IOException e) {
                        e.printStackTrace();
                        return;
                      }

                      // 2. 轮询任务状态
                      boolean finished = false;
                      while (!finished) {
                        try {
                          TimeUnit.SECONDS.sleep(2);  // 等待 2 秒后再次查询
                        } catch (InterruptedException e) {
                          Thread.currentThread().interrupt();
                          return;
                        }

                        String queryUrl = API_URL_QUERY + taskId;
                        Request queryRequest = new Request.Builder()
                            .url(queryUrl)
                            .addHeader("Authorization", "Bearer " + apiKey)
                            .addHeader("Content-Type", "application/json")
                            .get()
                            .build();

                        try (Response response = client.newCall(queryRequest).execute()) {
                          if (response.body() != null) {
                            String queryResponse = response.body().string();
                            ApiResponse apiResp = gson.fromJson(queryResponse, ApiResponse.class);

                            if (apiResp.output != null && apiResp.output.taskStatus != null) {
                              String status = apiResp.output.taskStatus;
                              System.out.println("当前任务状态：" + status);
                              if ("SUCCEEDED".equalsIgnoreCase(status)
                                  || "FAILED".equalsIgnoreCase(status)
                                  || "UNKNOWN".equalsIgnoreCase(status)) {
                                finished = true;
                                System.out.println("任务完成。最终结果：");
                                System.out.println(queryResponse);
                              }
                            } else {
                              System.out.println("查询响应内容：" + queryResponse);
                            }
                          }
                        } catch (IOException e) {
                          e.printStackTrace();
                          return;
                        }
                      }
                    }

                    static class ApiResponse {
                      @SerializedName("request_id")
                      String requestId;
                      Output output;
                    }

                    static class Output {
                      @SerializedName("task_id")
                      String taskId;
                      @SerializedName("task_status")
                      String taskStatus;
                    }
                  }
                  ```

                  ```python Python
                  import os
                  import time
                  import requests
                  import json

                  API_URL_SUBMIT = "https://dashscope.aliyuncs.com/api/v1/services/audio/asr/transcription"
                  API_URL_QUERY_BASE = "https://dashscope.aliyuncs.com/api/v1/tasks/"

                  def main():
                    # 如果您没有配置环境变量，请用 API Key 替换下行代码：api_key = "sk-xxx"
                    api_key = os.getenv("DASHSCOPE_API_KEY")

                    headers = {
                      "Authorization": f"Bearer {api_key}",
                      "Content-Type": "application/json",
                      "X-DashScope-Async": "enable"
                    }

                    # 1. 提交任务
                    payload = {
                      "model": "qwen3-asr-flash-filetrans",
                      "input": {
                        "file_url": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                      },
                      "parameters": {
                        "channel_id": [0],
                        # "language": "zh",
                        "enable_itn": False,
                        "enable_words": True
                      }
                    }

                    print("正在提交 ASR 转写任务...")
                    try:
                      submit_resp = requests.post(API_URL_SUBMIT, headers=headers, data=json.dumps(payload))
                    except requests.RequestException as e:
                      print(f"任务提交请求失败：{e}")
                      return

                    if submit_resp.status_code != 200:
                      print(f"任务提交失败！HTTP 状态码：{submit_resp.status_code}")
                      print(submit_resp.text)
                      return

                    resp_data = submit_resp.json()
                    output = resp_data.get("output")
                    if not output or "task_id" not in output:
                      print("提交响应内容异常：", resp_data)
                      return

                    task_id = output["task_id"]
                    print(f"任务已提交。task_id: {task_id}")

                    # 2. 轮询任务状态
                    finished = False
                    while not finished:
                      time.sleep(2)  # 等待 2 秒后再次查询

                      query_url = API_URL_QUERY_BASE + task_id
                      try:
                        query_resp = requests.get(query_url, headers=headers)
                      except requests.RequestException as e:
                        print(f"任务查询失败：{e}")
                        return

                      if query_resp.status_code != 200:
                        print(f"任务查询失败！HTTP 状态码：{query_resp.status_code}")
                        print(query_resp.text)
                        return

                      query_data = query_resp.json()
                      output = query_data.get("output")
                      if output and "task_status" in output:
                        status = output["task_status"]
                        print(f"当前任务状态：{status}")

                        if status.upper() in ("SUCCEEDED", "FAILED", "UNKNOWN"):
                          finished = True
                          print("任务完成。最终结果：")
                          print(json.dumps(query_data, indent=2, ensure_ascii=False))
                      else:
                        print("查询响应内容：", query_data)

                  if __name__ == "__main__":
                    main()
                  ```
                </CodeGroup>
              </Tab>

              <Tab title="Java SDK">
                ```java
                import com.alibaba.dashscope.audio.qwen_asr.*;
                import com.alibaba.dashscope.utils.Constants;
                import com.google.gson.Gson;
                import com.google.gson.GsonBuilder;
                import com.google.gson.JsonObject;

                import java.io.BufferedReader;
                import java.io.InputStreamReader;
                import java.net.HttpURLConnection;
                import java.net.URL;
                import java.util.ArrayList;
                import java.util.HashMap;

                public class Main {
                  public static void main(String[] args) {
                    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                    QwenTranscriptionParam param =
                        QwenTranscriptionParam.builder()
                            // 如果您没有配置环境变量，请用 API Key 替换下行代码：.apiKey("sk-xxx")
                            .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                            .model("qwen3-asr-flash-filetrans")
                            .fileUrl("https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav")
                            //.parameter("language", "zh")
                            //.parameter("channel_id", new ArrayList<String>(){{add("0");add("1");}})
                            .parameter("enable_itn", false)
                            .parameter("enable_words", true)
                            .build();
                    try {
                      QwenTranscription transcription = new QwenTranscription();
                      // 提交任务
                      QwenTranscriptionResult result = transcription.asyncCall(param);
                      System.out.println("create task result: " + result);
                      // 查询任务状态
                      result = transcription.fetch(QwenTranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
                      System.out.println("task status: " + result);
                      // 等待任务完成
                      result =
                          transcription.wait(
                              QwenTranscriptionQueryParam.FromTranscriptionParam(param, result.getTaskId()));
                      System.out.println("task result: " + result);
                      // 获取语音识别结果
                      QwenTranscriptionTaskResult taskResult = result.getResult();
                      if (taskResult != null) {
                        // 获取识别结果的 URL
                        String transcriptionUrl = taskResult.getTranscriptionUrl();
                        // 从 URL 获取结果
                        HttpURLConnection connection =
                            (HttpURLConnection) new URL(transcriptionUrl).openConnection();
                        connection.setRequestMethod("GET");
                        connection.connect();
                        BufferedReader reader =
                            new BufferedReader(new InputStreamReader(connection.getInputStream()));
                        // 格式化输出 JSON 结果
                        Gson gson = new GsonBuilder().setPrettyPrinting().create();
                        System.out.println(gson.toJson(gson.fromJson(reader, JsonObject.class)));
                      }
                    } catch (Exception e) {
                      System.out.println("error: " + e);
                    }
                  }
                }
                ```
              </Tab>

              <Tab title="Python SDK">
                ```python
                import json
                import os
                import sys
                from http import HTTPStatus

                import dashscope
                from dashscope.audio.qwen_asr import QwenTranscription
                from dashscope.api_entities.dashscope_response import TranscriptionResponse

                # 运行转写脚本
                if __name__ == '__main__':
                  # 如果您没有配置环境变量，请用 API Key 替换下行代码：dashscope.api_key = "sk-xxx"
                  dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

                  dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
                  task_response = QwenTranscription.async_call(
                    model='qwen3-asr-flash-filetrans',
                    file_url='https://dashscope.oss-cn-beijing.aliyuncs.com/samples/audio/sensevoice/rich_text_example_1.wav',
                    #language="",
                    enable_itn=False,
                    enable_words=True
                  )
                  print(f'task_response: {task_response}')
                  print(task_response.output.task_id)
                  query_response = QwenTranscription.fetch(task=task_response.output.task_id)
                  print(f'query_response: {query_response}')
                  task_result = QwenTranscription.wait(task=task_response.output.task_id)
                  print(f'task_result: {task_result}')
                ```
              </Tab>
            </Tabs>
          </Tab>

          <Tab title="Qwen3-ASR-Flash">
            Qwen3-ASR-Flash 支持最长 5 分钟的录音。该模型接受可公开访问的音频文件 URL 或直接上传的本地文件作为输入，还支持以流式方式返回识别结果。

            #### 输入：音频文件 URL

            <CodeGroup>
              ```python Python SDK
              import os
              import dashscope

              dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

              messages = [
                {"role": "user", "content": [{"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"}]}
              ]

              response = dashscope.MultiModalConversation.call(
                # 如果您没有配置环境变量，请用 API Key 替换下行代码：api_key = "sk-xxx"
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                model="qwen3-asr-flash",
                messages=messages,
                result_format="message",
                asr_options={
                  #"language": "zh", # 可选。如果已知音频语言，可通过此参数指定以提高识别准确率。
                  "enable_itn":False
                }
              )
              print(response)
              ```

              ```java Java SDK
              import java.util.Arrays;
              import java.util.Collections;
              import java.util.HashMap;
              import java.util.Map;

              import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
              import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
              import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
              import com.alibaba.dashscope.common.MultiModalMessage;
              import com.alibaba.dashscope.common.Role;
              import com.alibaba.dashscope.exception.ApiException;
              import com.alibaba.dashscope.exception.NoApiKeyException;
              import com.alibaba.dashscope.exception.UploadFileException;
              import com.alibaba.dashscope.utils.Constants;
              import com.alibaba.dashscope.utils.JsonUtils;

              public class Main {
                public static void simpleMultiModalConversationCall()
                    throws ApiException, NoApiKeyException, UploadFileException {
                  MultiModalConversation conv = new MultiModalConversation();
                  MultiModalMessage userMessage = MultiModalMessage.builder()
                      .role(Role.USER.getValue())
                      .content(Arrays.asList(
                      Collections.singletonMap("audio", "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3")))
                      .build();

                  MultiModalMessage sysMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                      .build();

                  Map<String, Object> asrOptions = new HashMap<>();
                  asrOptions.put("enable_itn", false);
                  // asrOptions.put("language", "zh"); // 可选。如果已知音频语言，可通过此参数指定以提高识别准确率。
                  MultiModalConversationParam param = MultiModalConversationParam.builder()
                      // 如果您没有配置环境变量，请用 API Key 替换下行代码：.apiKey("sk-xxx")
                      .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                      .model("qwen3-asr-flash")
                      .message(sysMessage)
                      .message(userMessage)
                      .parameter("asr_options", asrOptions)
                      .build();
                  MultiModalConversationResult result = conv.call(param);
                  System.out.println(JsonUtils.toJson(result));
                }
                public static void main(String[] args) {
                  try {
                    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                    simpleMultiModalConversationCall();
                  } catch (ApiException | NoApiKeyException | UploadFileException e) {
                    System.out.println(e.getMessage());
                  }
                  System.exit(0);
                }
              }
              ```

              ```bash cURL
              curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H "Content-Type: application/json" \
              -d '{
                "model": "qwen3-asr-flash",
                "input": {
                  "messages": [
                    {
                      "content": [
                        {
                          "audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                        }
                      ],
                      "role": "user"
                    }
                  ]
                },
                "parameters": {
                  "asr_options": {
                    "enable_itn": false
                  }
                }
              }'
              ```
            </CodeGroup>

            #### 输入：Base64 编码的音频文件

            输入 Base64 编码的数据（[Data URL](https://www.rfc-editor.org/rfc/rfc2397)），格式为：`data:<mediatype>;base64,<data>`。

            - `<mediatype>`：MIME 类型

              因音频格式而异，例如：

              - WAV：`audio/wav`
              - MP3：`audio/mpeg`

            - `<data>`：音频的 Base64 编码字符串

              Base64 编码会增大文件体积。请确保原始文件足够小，以使编码后的数据不超过 10 MB 的输入限制。

            - 示例：`data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9`

            <Accordion title="查看示例代码">
              <CodeGroup>
                ```python Python
                import base64, pathlib

                # input.mp3 是本地音频文件。请替换为您自己的音频文件路径，并确保符合音频要求
                file_path = pathlib.Path("input.mp3")
                base64_str = base64.b64encode(file_path.read_bytes()).decode()
                data_uri = f"data:audio/mpeg;base64,{base64_str}"
                ```

                ```java Java
                import java.nio.file.*;
                import java.util.Base64;

                public class Main {
                  /**
                      * filePath 是本地音频文件。请替换为您自己的音频文件路径，并确保符合音频要求
                      */
                  public static String toDataUrl(String filePath) throws Exception {
                    byte[] bytes = Files.readAllBytes(Paths.get(filePath));
                    String encoded = Base64.getEncoder().encodeToString(bytes);
                    return "data:audio/mpeg;base64," + encoded;
                  }

                  // 使用示例
                  public static void main(String[] args) throws Exception {
                    System.out.println(toDataUrl("input.mp3"));
                  }
                }
                ```
              </CodeGroup>
            </Accordion>

            本示例使用的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260106/gpkfrr/welcome.mp3)。

            <CodeGroup>
              ```python Python SDK
              import base64
              import dashscope
              import os
              import pathlib

              dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

              # 请替换为您实际的音频文件路径
              file_path = "welcome.mp3"
              # 请替换为您实际的音频文件 MIME 类型
              audio_mime_type = "audio/mpeg"

              file_path_obj = pathlib.Path(file_path)
              if not file_path_obj.exists():
                raise FileNotFoundError(f"未找到音频文件：{file_path}")

              base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
              data_uri = f"data:{audio_mime_type};base64,{base64_str}"

              messages = [
                {"role": "user", "content": [{"audio": data_uri}]}
              ]
              response = dashscope.MultiModalConversation.call(
                # 如果您没有配置环境变量，请用 API Key 替换下行代码：api_key = "sk-xxx",
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                model="qwen3-asr-flash",
                messages=messages,
                result_format="message",
                asr_options={
                  # "language": "zh", # 可选。如果已知音频语言，可通过此参数指定以提高识别准确率。
                  "enable_itn":False
                }
              )
              print(response)
              ```

              ```java Java SDK
              import java.io.IOException;
              import java.nio.file.Files;
              import java.nio.file.Paths;
              import java.util.*;

              import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
              import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
              import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
              import com.alibaba.dashscope.common.MultiModalMessage;
              import com.alibaba.dashscope.common.Role;
              import com.alibaba.dashscope.exception.ApiException;
              import com.alibaba.dashscope.exception.NoApiKeyException;
              import com.alibaba.dashscope.exception.UploadFileException;
              import com.alibaba.dashscope.utils.Constants;
              import com.alibaba.dashscope.utils.JsonUtils;

              public class Main {
                // 请替换为您实际的音频文件路径
                private static final String AUDIO_FILE = "welcome.mp3";
                // 请替换为您实际的音频文件 MIME 类型
                private static final String AUDIO_MIME_TYPE = "audio/mpeg";

                public static void simpleMultiModalConversationCall()
                    throws ApiException, NoApiKeyException, UploadFileException, IOException {
                  MultiModalConversation conv = new MultiModalConversation();
                  MultiModalMessage userMessage = MultiModalMessage.builder()
                      .role(Role.USER.getValue())
                      .content(Arrays.asList(
                      Collections.singletonMap("audio", toDataUrl())))
                      .build();

                  MultiModalMessage sysMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                      .build();

                  Map<String, Object> asrOptions = new HashMap<>();
                  asrOptions.put("enable_itn", false);
                  // asrOptions.put("language", "zh"); // 可选。如果已知音频语言，可通过此参数指定以提高识别准确率。
                  MultiModalConversationParam param = MultiModalConversationParam.builder()
                      // 如果您没有配置环境变量，请用 API Key 替换下行代码：.apiKey("sk-xxx")
                      .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                      .model("qwen3-asr-flash")
                      .message(sysMessage)
                      .message(userMessage)
                      .parameter("asr_options", asrOptions)
                      .build();
                  MultiModalConversationResult result = conv.call(param);
                  System.out.println(JsonUtils.toJson(result));
                }

                public static void main(String[] args) {
                  try {
                    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                    simpleMultiModalConversationCall();
                  } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
                    System.out.println(e.getMessage());
                  }
                  System.exit(0);
                }

                // 生成 data URI
                public static String toDataUrl() throws IOException {
                  byte[] bytes = Files.readAllBytes(Paths.get(AUDIO_FILE));
                  String encoded = Base64.getEncoder().encodeToString(bytes);
                  return "data:" + AUDIO_MIME_TYPE + ";base64," + encoded;
                }
              }
              ```
            </CodeGroup>

            #### 输入：本地音频文件的绝对路径

            使用 DashScope SDK 处理本地文件时，需要提供文件路径。下表说明了不同操作系统和 SDK 下文件路径的构造方式。

| 系统            | SDK        | 输入文件路径             | 示例                             |
| ------------- | ---------- | ------------------ | ------------------------------ |
| Linux 或 macOS | Python SDK | `file://<绝对文件路径>`  | `file:///home/images/test.png` |
| Linux 或 macOS | Java SDK   | `file://<绝对文件路径>`  | `file:///home/images/test.png` |
| Windows       | Python SDK | `file://<绝对文件路径>`  | `file://D:/images/test.png`    |
| Windows       | Java SDK   | `file:///<绝对文件路径>` | `file:///D:/images/test.png`   |

            <Warning>
              使用本地文件时，API 调用限制为 100 QPS 且无法扩容。请勿在生产环境、高并发场景或压力测试中使用此方式。如需更高并发，请将文件上传至 OSS，然后通过音频文件 URL 调用 API。
            </Warning>

            本示例使用的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260106/gpkfrr/welcome.mp3)。

            <CodeGroup>
              ```python Python SDK
              import os
              import dashscope

              dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

              # 请将 ABSOLUTE_PATH/welcome.mp3 替换为本地音频文件的绝对路径
              audio_file_path = "file://ABSOLUTE_PATH/welcome.mp3"

              messages = [
                {"role": "user", "content": [{"audio": audio_file_path}]}
              ]
              response = dashscope.MultiModalConversation.call(
                # 如果您没有配置环境变量，请用 API Key 替换下行代码：api_key = "sk-xxx"
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                model="qwen3-asr-flash",
                messages=messages,
                result_format="message",
                asr_options={
                  # "language": "zh", # 可选。如果已知音频语言，可通过此参数指定以提高识别准确率。
                  "enable_itn":False
                }
              )
              print(response)
              ```

              ```java Java SDK
              import java.util.Arrays;
              import java.util.Collections;
              import java.util.HashMap;
              import java.util.Map;

              import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
              import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
              import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
              import com.alibaba.dashscope.common.MultiModalMessage;
              import com.alibaba.dashscope.common.Role;
              import com.alibaba.dashscope.exception.ApiException;
              import com.alibaba.dashscope.exception.NoApiKeyException;
              import com.alibaba.dashscope.exception.UploadFileException;
              import com.alibaba.dashscope.utils.Constants;
              import com.alibaba.dashscope.utils.JsonUtils;

              public class Main {
                public static void simpleMultiModalConversationCall()
                    throws ApiException, NoApiKeyException, UploadFileException {
                  // 请将 ABSOLUTE_PATH/welcome.mp3 替换为本地文件的绝对路径
                  String localFilePath = "file://ABSOLUTE_PATH/welcome.mp3";
                  MultiModalConversation conv = new MultiModalConversation();
                  MultiModalMessage userMessage = MultiModalMessage.builder()
                      .role(Role.USER.getValue())
                      .content(Arrays.asList(
                      Collections.singletonMap("audio", localFilePath)))
                      .build();

                  MultiModalMessage sysMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                      .build();

                  Map<String, Object> asrOptions = new HashMap<>();
                  asrOptions.put("enable_itn", false);
                  // asrOptions.put("language", "zh"); // 可选。如果已知音频语言，可通过此参数指定以提高识别准确率。
                  MultiModalConversationParam param = MultiModalConversationParam.builder()
                      // 如果您没有配置环境变量，请用 API Key 替换下行代码：.apiKey("sk-xxx")
                      .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                      .model("qwen3-asr-flash")
                      .message(sysMessage)
                      .message(userMessage)
                      .parameter("asr_options", asrOptions)
                      .build();
                  MultiModalConversationResult result = conv.call(param);
                  System.out.println(JsonUtils.toJson(result));
                }
                public static void main(String[] args) {
                  try {
                    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                    simpleMultiModalConversationCall();
                  } catch (ApiException | NoApiKeyException | UploadFileException e) {
                    System.out.println(e.getMessage());
                  }
                  System.exit(0);
                }
              }
              ```
            </CodeGroup>

            #### 流式输出

            模型逐步生成结果，而非一次性返回。非流式输出会等待模型生成完毕后返回完整结果；流式输出则实时返回中间结果，让您在生成过程中即可读取结果，减少等待时间。根据不同的调用方式，设置不同参数以启用流式输出：

            - DashScope Python SDK：将 `stream` 参数设置为 true。
            - DashScope Java SDK：使用 `streamCall` 接口。
            - DashScope HTTP：设置请求头 `X-DashScope-SSE` 为 `enable`。

            <Tabs>
              <Tab title="Python SDK">
                ```python
                import os
                import dashscope

                dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

                messages = [
                  {"role": "user", "content": [{"audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"}]}
                ]
                response = dashscope.MultiModalConversation.call(
                  # 如果您没有配置环境变量，请用 API Key 替换下行代码：api_key = "sk-xxx"
                  api_key=os.getenv("DASHSCOPE_API_KEY"),
                  model="qwen3-asr-flash",
                  messages=messages,
                  result_format="message",
                  asr_options={
                    # "language": "zh", # 可选。如果已知音频语言，可通过此参数指定以提高识别准确率。
                    "enable_itn":False
                  },
                  stream=True
                )

                for response in response:
                  try:
                    print(response["output"]["choices"][0]["message"].content[0]["text"])
                  except:
                    pass
                ```
              </Tab>

              <Tab title="Java SDK">
                ```java
                import java.util.Arrays;
                import java.util.Collections;
                import java.util.HashMap;
                import java.util.Map;

                import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
                import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
                import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
                import com.alibaba.dashscope.common.MultiModalMessage;
                import com.alibaba.dashscope.common.Role;
                import com.alibaba.dashscope.exception.ApiException;
                import com.alibaba.dashscope.exception.NoApiKeyException;
                import com.alibaba.dashscope.exception.UploadFileException;
                import com.alibaba.dashscope.utils.Constants;
                import io.reactivex.Flowable;

                public class Main {
                  public static void simpleMultiModalConversationCall()
                      throws ApiException, NoApiKeyException, UploadFileException {
                    MultiModalConversation conv = new MultiModalConversation();
                    MultiModalMessage userMessage = MultiModalMessage.builder()
                        .role(Role.USER.getValue())
                        .content(Arrays.asList(
                        Collections.singletonMap("audio", "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3")))
                        .build();

                    MultiModalMessage sysMessage = MultiModalMessage.builder().role(Role.SYSTEM.getValue())
                        .build();

                    Map<String, Object> asrOptions = new HashMap<>();
                    asrOptions.put("enable_itn", false);
                    // asrOptions.put("language", "zh"); // 可选。如果已知音频语言，可通过此参数指定以提高识别准确率。
                    MultiModalConversationParam param = MultiModalConversationParam.builder()
                        // 如果您没有配置环境变量，请用 API Key 替换下行代码：.apiKey("sk-xxx")
                        .apiKey(System.getenv("DASHSCOPE_API_KEY"))
                        .model("qwen3-asr-flash")
                        .message(sysMessage)
                        .message(userMessage)
                        .parameter("asr_options", asrOptions)
                        .build();
                    Flowable<MultiModalConversationResult> resultFlowable = conv.streamCall(param);
                    resultFlowable.blockingForEach(item -> {
                      try {
                        System.out.println(item.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("text"));
                      } catch (Exception e){
                        System.exit(0);
                      }
                    });
                  }

                  public static void main(String[] args) {
                    try {
                      Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                      simpleMultiModalConversationCall();
                    } catch (ApiException | NoApiKeyException | UploadFileException e) {
                      System.out.println(e.getMessage());
                    }
                    System.exit(0);
                  }
                }
                ```
              </Tab>

              <Tab title="cURL">
                ```bash
                curl -X POST "https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation" \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H "Content-Type: application/json" \
                -H "X-DashScope-SSE: enable" \
                -d '{
                  "model": "qwen3-asr-flash",
                  "input": {
                    "messages": [
                      {
                        "content": [
                          {
                            "text": ""
                          }
                        ],
                        "role": "system"
                      },
                      {
                        "content": [
                          {
                            "audio": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                          }
                        ],
                        "role": "user"
                      }
                    ]
                  },
                  "parameters": {
                    "incremental_output": true,
                    "asr_options": {
                      "enable_itn": false
                    }
                  }
                }'
                ```
              </Tab>
            </Tabs>
          </Tab>
        </Tabs>
      </Tab>

      <Tab title="OpenAI 兼容">
        仅 Qwen3-ASR-Flash 系列模型支持 OpenAI 兼容方式调用。OpenAI 兼容模式仅接受可公开访问的音频文件 URL，不支持本地文件路径。

        请使用 OpenAI Python SDK 1.52.0 或更高版本，Node.js SDK 4.68.0 或更高版本。

        `asr_options` 参数不属于 OpenAI 标准。使用 OpenAI SDK 时，需通过 `extra_body` 传递。

        #### 输入：音频文件 URL

        <Tabs>
          <Tab title="Python SDK">
            ```python
            from openai import OpenAI
            import os

            try:
              client = OpenAI(
                # 如果您没有配置环境变量，请用 API Key 替换下行代码：api_key = "sk-xxx",
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
              )

              stream_enabled = False  # 设置为 True 可启用流式输出
              completion = client.chat.completions.create(
                model="qwen3-asr-flash",
                messages=[
                  {
                    "content": [
                      {
                        "type": "input_audio",
                        "input_audio": {
                          "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                        }
                      }
                    ],
                    "role": "user"
                  }
                ],
                stream=stream_enabled,
                # stream 为 False 时不要设置 stream_options
                # stream_options={"include_usage": True},
                extra_body={
                  "asr_options": {
                    # "language": "zh",
                    "enable_itn": False
                  }
                }
              )
              if stream_enabled:
                full_content = ""
                print("流式输出：")
                for chunk in completion:
                  # 如果 stream_options.include_usage 为 True，最后一个 chunk 的 choices 字段为空列表，需跳过（可通过 chunk.usage 获取 token 用量）
                  print(chunk)
                  if chunk.choices and chunk.choices[0].delta.content:
                    full_content += chunk.choices[0].delta.content
                print(f"完整内容：{full_content}")
              else:
                print(f"非流式输出：{completion.choices[0].message.content}")
            except Exception as e:
              print(f"错误：{e}")
            ```
          </Tab>

          <Tab title="Node.js SDK">
            ```javascript
            // 运行前准备：
            // 适用于 Windows/Mac/Linux：
            // 1. 确保已安装 Node.js（建议 14 及以上版本）
            // 2. 运行以下命令安装依赖：npm install openai

            import OpenAI from "openai";

            const client = new OpenAI({
              // 如果您没有配置环境变量，请用 API Key 替换下行代码：apiKey: "sk-xxx",
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
            });

            async function main() {
              try {
                const streamEnabled = false; // 启用流式输出
                const completion = await client.chat.completions.create({
                  model: "qwen3-asr-flash",
                  messages: [
                    {
                      role: "user",
                      content: [
                        {
                          type: "input_audio",
                          input_audio: {
                            data: "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                          }
                        }
                      ]
                    }
                  ],
                  stream: streamEnabled,
                  // stream 为 false 时不要设置 stream_options
                  // stream_options: {
                  //   "include_usage": true
                  // },
                  asr_options: {
                    // language: "zh",
                    enable_itn: false
                  }
                });

                if (streamEnabled) {
                  let fullContent = "";
                  console.log("流式输出：");
                  for await (const chunk of completion) {
                    console.log(JSON.stringify(chunk));
                    if (chunk.choices && chunk.choices.length > 0) {
                      const delta = chunk.choices[0].delta;
                      if (delta && delta.content) {
                        fullContent += delta.content;
                      }
                    }
                  }
                  console.log(`完整内容：${fullContent}`);
                } else {
                  console.log(`非流式输出：${completion.choices[0].message.content}`);
                }
              } catch (err) {
                console.error(`错误：${err}`);
              }
            }

            main();
            ```
          </Tab>

          <Tab title="cURL">
            ```bash
            curl -X POST 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions' \
            -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
            -H "Content-Type: application/json" \
            -d '{
              "model": "qwen3-asr-flash",
              "messages": [
                {
                  "content": [
                    {
                      "type": "input_audio",
                      "input_audio": {
                        "data": "https://dashscope.oss-cn-beijing.aliyuncs.com/audios/welcome.mp3"
                      }
                    }
                  ],
                  "role": "user"
                }
              ],
              "stream":false,
              "asr_options": {
                "enable_itn": false
              }
            }'
            ```
          </Tab>
        </Tabs>

        #### 输入：Base64 编码的音频文件

        输入 Base64 编码的数据（[Data URL](https://www.rfc-editor.org/rfc/rfc2397)），格式为：`data:<mediatype>;base64,<data>`。

        - `<mediatype>`：MIME 类型

          因音频格式而异，例如：

          - WAV：`audio/wav`
          - MP3：`audio/mpeg`

        - `<data>`：音频的 Base64 编码字符串

          Base64 编码会增大文件体积。请确保原始文件足够小，以使编码后的数据不超过 10 MB 的输入限制。

        - 示例：`data:audio/wav;base64,SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//PAxABQ/BXRbMPe4IQAhl9`

        <Accordion title="查看示例代码">
          <CodeGroup>
            ```python Python
            import base64, pathlib

            # input.mp3 是本地音频文件。请替换为您自己的音频文件路径，并确保符合音频要求
            file_path = pathlib.Path("input.mp3")
            base64_str = base64.b64encode(file_path.read_bytes()).decode()
            data_uri = f"data:audio/mpeg;base64,{base64_str}"
            ```

            ```java Java
            import java.nio.file.*;
            import java.util.Base64;

            public class Main {
              /**
                  * filePath 是本地音频文件。请替换为您自己的音频文件路径，并确保符合音频要求
                  */
              public static String toDataUrl(String filePath) throws Exception {
                byte[] bytes = Files.readAllBytes(Paths.get(filePath));
                String encoded = Base64.getEncoder().encodeToString(bytes);
                return "data:audio/mpeg;base64," + encoded;
              }

              // 使用示例
              public static void main(String[] args) throws Exception {
                System.out.println(toDataUrl("input.mp3"));
              }
            }
            ```
          </CodeGroup>
        </Accordion>

        <Tabs>
          <Tab title="Python SDK">
            本示例使用的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260106/gpkfrr/welcome.mp3)。

            ```python
            import base64
            from openai import OpenAI
            import os
            import pathlib

            try:
              # 请替换为您实际的音频文件路径
              file_path = "welcome.mp3"
              # 请替换为您实际的音频文件 MIME 类型
              audio_mime_type = "audio/mpeg"

              file_path_obj = pathlib.Path(file_path)
              if not file_path_obj.exists():
                raise FileNotFoundError(f"未找到音频文件：{file_path}")

              base64_str = base64.b64encode(file_path_obj.read_bytes()).decode()
              data_uri = f"data:{audio_mime_type};base64,{base64_str}"

              client = OpenAI(
                # 如果您没有配置环境变量，请用 API Key 替换下行代码：api_key = "sk-xxx",
                api_key=os.getenv("DASHSCOPE_API_KEY"),
                base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
              )

              stream_enabled = False  # 设置为 True 可启用流式输出
              completion = client.chat.completions.create(
                model="qwen3-asr-flash",
                messages=[
                  {
                    "content": [
                      {
                        "type": "input_audio",
                        "input_audio": {
                          "data": data_uri
                        }
                      }
                    ],
                    "role": "user"
                  }
                ],
                stream=stream_enabled,
                # stream 为 False 时不要设置 stream_options
                # stream_options={"include_usage": True},
                extra_body={
                  "asr_options": {
                    # "language": "zh",
                    "enable_itn": False
                  }
                }
              )
              if stream_enabled:
                full_content = ""
                print("流式输出：")
                for chunk in completion:
                  # 如果 stream_options.include_usage 为 True，最后一个 chunk 的 choices 字段为空列表，需跳过（可通过 chunk.usage 获取 token 用量）
                  print(chunk)
                  if chunk.choices and chunk.choices[0].delta.content:
                    full_content += chunk.choices[0].delta.content
                print(f"完整内容：{full_content}")
              else:
                print(f"非流式输出：{completion.choices[0].message.content}")
            except Exception as e:
              print(f"错误：{e}")
            ```
          </Tab>

          <Tab title="Node.js SDK">
            本示例使用的音频文件为：[welcome.mp3](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/en-US/20260106/gpkfrr/welcome.mp3)。

            ```javascript
            // 运行前准备：
            // 适用于 Windows/Mac/Linux：
            // 1. 确保已安装 Node.js（建议 14 及以上版本）
            // 2. 运行以下命令安装依赖：npm install openai

            import OpenAI from "openai";
            import { readFileSync } from 'fs';

            const client = new OpenAI({
              // 如果您没有配置环境变量，请用 API Key 替换下行代码：apiKey: "sk-xxx",
              apiKey: process.env.DASHSCOPE_API_KEY,
              baseURL: "https://dashscope.aliyuncs.com/compatible-mode/v1",
            });

            const encodeAudioFile = (audioFilePath) => {
                const audioFile = readFileSync(audioFilePath);
                return audioFile.toString('base64');
            };

            // 请替换为您实际的音频文件路径
            const dataUri = `data:audio/mpeg;base64,${encodeAudioFile("welcome.mp3")}`;

            async function main() {
              try {
                const streamEnabled = false; // 启用流式输出
                const completion = await client.chat.completions.create({
                  model: "qwen3-asr-flash",
                  messages: [
                    {
                      role: "user",
                      content: [
                        {
                          type: "input_audio",
                          input_audio: {
                            data: dataUri
                          }
                        }
                      ]
                    }
                  ],
                  stream: streamEnabled,
                  // stream 为 false 时不要设置 stream_options
                  // stream_options: {
                  //   "include_usage": true
                  // },
                  asr_options: {
                    // language: "zh",
                    enable_itn: false
                  }
                });

                if (streamEnabled) {
                  let fullContent = "";
                  console.log("流式输出：");
                  for await (const chunk of completion) {
                    console.log(JSON.stringify(chunk));
                    if (chunk.choices && chunk.choices.length > 0) {
                      const delta = chunk.choices[0].delta;
                      if (delta && delta.content) {
                        fullContent += delta.content;
                      }
                    }
                  }
                  console.log(`完整内容：${fullContent}`);
                } else {
                  console.log(`非流式输出：${completion.choices[0].message.content}`);
                }
              } catch (err) {
                console.error(`错误：${err}`);
              }
            }

            main();
            ```
          </Tab>
        </Tabs>
      </Tab>
    </Tabs>
  </Tab>

  <Tab title="Qwen-Omni">
    使用 **Qwen-Omni**（`qwen3.5-omni-plus`、`qwen3.5-omni-flash`、`qwen3-omni-flash`）进行基于提示词上下文的录音转写。您可以在系统提示词中描述您的业务领域，以提高识别准确率。

    <Warning>
      Qwen-Omni 会解析所有音频内容，而非仅限语音。音乐、打字声或环境噪声可能导致模型输出描述性文字而非转写结果。对于混合音频，建议使用 VAD 预处理以提取语音片段，或在系统提示词中添加指令："仅转写人声语音，忽略非语音声音。"
    </Warning>

    [获取 API Key](/api-reference/preparation/api-key) 并[将其设置为环境变量](/api-reference/preparation/export-api-key-env)。[安装 SDK](/api-reference/preparation/install-sdk)。

    <CodeGroup>
      ```python Python
      import os
      from openai import OpenAI

      client = OpenAI(
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
      )

      completion = client.chat.completions.create(
        model="qwen3-omni-flash",
        messages=[
          {"role": "system", "content": "Transcribe the following audio exactly as spoken. Output only the transcription text. Ignore non-speech sounds."},
          {"role": "user", "content": [
            {"type": "input_audio", "input_audio": {"data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav"}},
            {"type": "text", "text": "Transcribe this audio."}
          ]}
        ],
        modalities=["text"],
        stream=True,
      )

      for chunk in completion:
        if chunk.choices and chunk.choices[0].delta.content:
          print(chunk.choices[0].delta.content, end="")
      ```

      ```bash cURL
      curl -X POST https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "qwen3-omni-flash",
        "messages": [
          {"role": "system", "content": "Transcribe the following audio exactly as spoken. Output only the transcription text. Ignore non-speech sounds."},
          {"role": "user", "content": [
            {"type": "input_audio", "input_audio": {"data": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250211/tixcef/cherry.wav"}},
            {"type": "text", "text": "Transcribe this audio."}
          ]}
        ],
        "modalities": ["text"],
        "stream": true
      }'
      ```
    </CodeGroup>

    <Tip>
      有关 Qwen-Omni 的完整多模态对话能力，请参见[音视频文件理解](/developer-guides/speech/multimodal-speech)。
    </Tip>
  </Tab>
</Tabs>

## 上下文增强

**适用模型：** 支持上下文增强功能，可将对话历史传入 ASR 模型，显著提升专有词汇的转写准确率。详细的使用方法和效果示例，请参见下方。

**使用场景：** 适用于将 ASR 与大语言模型结合的场景。将历史对话上下文（LLM 的回复和此前的识别结果）传入 ASR 模型，可显著提升对人名、地名、产品术语等专有名词的转写准确率——比传统热词更灵活。

**用法：** 通过 `input.messages` 传入对话历史。使用 `assistant` 角色表示 LLM 此前的回复，使用 `user` 角色配合 `input_text` 类型表示此前的识别结果。上下文需成对出现在当前音频消息之前。

**支持的文本类型**包括（但不限于）：

- 各种分隔符格式的热词列表（例如：热词 1、热词 2、热词 3、热词 4）
- 任意长度与格式的文本段落或篇章
- 混合内容：词表与段落的任意组合
- 无关或无意义文本（包括乱码）。模型对无关内容容忍度较高，识别质量很少因此下降。

**示例：**

某段音频的正确识别结果为："投行圈内部的那些黑话，你了解哪些？首先，外资九大投行，Bulge Bracket，BB ……"

| **不使用上下文增强**                                                                                                             | **使用上下文增强**                                                                           |
| ------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| 未使用上下文增强时，部分投行公司名称识别有误，例如 "Bird Rock" 正确应为 "Bulge Bracket"。<br /><br />识别结果："投行圈内部的那些黑话，你了解哪些？首先，外资九大投行，Bird Rock，BB ……" | 使用上下文增强，对投行公司名称识别正确。<br /><br />识别结果："投行圈内部的那些黑话，你了解哪些？首先，外资九大投行，Bulge Bracket，BB ……" |

实现上述效果，可在上下文中加入以下任一内容：

- 词表：
  - 词表 1：

```plaintext
Bulge Bracket、Boutique、Middle Market、国内券商
```

- 词表 2：

```plaintext
Bulge Bracket Boutique Middle Market 国内券商
```

- 词表 3：

```plaintext
['Bulge Bracket', 'Boutique', 'Middle Market', '国内券商']
```

- 自然语言：

```plaintext
投行分类大揭秘！
最近有不少澳洲的小伙伴问我，到底什么是投行？今天就来给大家科普一下，对于留学生来说，投行主要可以分为四大类：Bulge Bracket、Boutique、Middle Market 和国内券商。
Bulge Bracket 投行：这就是我们常说的九大投行，包括高盛、摩根士丹利等。这些大行在业务范围和规模上都相当庞大。
Boutique 投行：这些投行规模相对较小，但业务领域非常专注。比如 Lazard、Evercore 等，它们在特定领域有着深厚的专业知识和经验。
Middle Market 投行：这类投行主要服务于中型公司，提供并购、IPO 等业务。虽然规模不如大行，但在特定市场上有很高的影响力。
国内券商：随着中国市场的崛起，国内券商在国际市场上也扮演着越来越重要的角色。
此外，还有一些 Position 和 business 的划分，大家可以参考相关的图表。希望这些信息能帮助大家更好地了解投行，为未来的职业生涯做好准备！
```

- 有干扰的自然语言：部分文本与识别内容无关，例如下面示例里的人名。

```plaintext
投行分类大揭秘！
最近有不少澳洲的小伙伴问我，到底什么是投行？今天就来给大家科普一下，对于留学生来说，投行主要可以分为四大类：Bulge Bracket、Boutique、Middle Market 和国内券商。
Bulge Bracket 投行：这就是我们常说的九大投行，包括高盛、摩根士丹利等。这些大行在业务范围和规模上都相当庞大。
Boutique 投行：这些投行规模相对较小，但业务领域非常专注。比如 Lazard、Evercore 等，它们在特定领域有着深厚的专业知识和经验。
Middle Market 投行：这类投行主要服务于中型公司，提供并购、IPO 等业务。虽然规模不如大行，但在特定市场上有很高的影响力。
国内券商：随着中国市场的崛起，国内券商在国际市场上也扮演着越来越重要的角色。
此外，还有一些 Position 和 business 的划分，大家可以参考相关的图表。希望这些信息能帮助大家更好地了解投行，为未来的职业生涯做好准备！
王皓轩 李梓涵 张景行 刘欣怡 陈俊杰 杨思远 赵雨桐 黄志强 周子墨 吴雅静 徐若曦 孙浩然 胡瑾瑜 朱晨曦 郭文博 何静姝 高宇航 林逸飞
郑晓燕 梁博文 罗佳琪 宋明哲 谢婉婷 唐子骞 韩梦瑶 冯毅然 曹沁雪 邓子睿 萧望舒 许嘉树
程一诺 袁芷若 彭浩宇 董思淼 范景玉 苏子衿 吕文轩 蒋诗涵 丁沐宸
魏书瑶 任天佑 姜亦辰 华清羽 沈星河 傅瑾瑜 姚星辰 钟灵毓 阎立诚 金若水 陶然亭 戚少商 薛芷兰 邹云帆 熊子昂 柏文峰 易千帆
```

## API 参考

<Tabs>
  <Tab title="Qwen-Audio-3.0-ASR-Flash-Filetrans/Fun-ASR">
    - [RESTful API](/api-reference/speech-recognition/fun-asr-recording/restful-api)
    - [Python SDK](/api-reference/speech-recognition/fun-asr-recording/python-sdk)
    - [Java SDK](/api-reference/speech-recognition/fun-asr-recording/java-sdk)
  </Tab>

  <Tab title="Qwen-ASR">
    [录音文件识别 - Qwen API 参考](/api-reference/speech-recognition/qwen-asr/openai)
  </Tab>

  <Tab title="Qwen-Omni">
    - [音视频文件理解](/developer-guides/speech/multimodal-speech)
    - [语音到语音模型](/developer-guides/speech/s2s-models)
  </Tab>
</Tabs>

## 常见问题

<Tabs>
  <Tab title="Qwen-Audio-3.0-ASR-Flash-Filetrans/Fun-ASR">
    #### 如何提高识别准确率？

    您应综合考虑所有相关因素并采取相应措施。

    主要影响因素包括：

    1. 音质：录音设备质量、采样率和环境噪声会影响音频清晰度。高质量的音频是准确识别的基础。
    2. 说话人特征：音高、语速、口音和方言的差异会增加识别难度，尤其是罕见方言或浓重口音。
    3. 语言和词汇：中英混合、专业术语或俚语会增加识别难度。您可以配置热词来优化这些场景的识别效果。
    4. 上下文理解：缺乏上下文可能导致语义歧义，特别是在需要上下文才能正确识别的场景中。

    优化方法：

    1. 提升音频质量：使用高性能麦克风和支持推荐采样率的设备。减少环境噪声和回声。
    2. 适应说话人特征：对于涉及浓重口音或多方言的场景，选择支持相应方言的模型。
    3. 配置热词：为专业术语、专有名词等特定词汇设置热词。详情请参见[自定义热词](/developer-guides/speech/improve-recognition-accuracy)。
    4. 保留上下文：避免将音频切分为过短的片段。
  </Tab>

  <Tab title="Qwen-ASR">
    #### 问：如何为 API 提供可公开访问的音频 URL？

    建议使用对象存储服务（OSS），它提供高可用、高可靠的存储，并可方便地生成公开访问的 URL。

    **验证 URL 是否可公开访问**：在浏览器中打开该 URL，或使用 curl 确保音频文件能够成功下载或播放（HTTP 状态码 200）。

    #### 问：如何检查音频格式是否满足要求？

    使用开源工具 [ffprobe](https://ffmpeg.org/ffprobe.html) 快速获取音频详细信息：

    ```bash
    # 查看容器格式（format_name）、编解码器（codec_name）、采样率（sample_rate）和声道数（channels）
    ffprobe -v error -show_entries format=format_name -show_entries stream=codec_name,sample_rate,channels -of default=noprint_wrappers=1 your_audio_file.mp3
    ```

    <a id="q-how-do-i-process-audio-to-meet-model-requirements" />

    #### 问：如何处理音频以满足模型要求？

    使用开源工具 [FFmpeg](https://ffmpeg.en.lo4d.com/download) 进行音频裁剪或格式转换：

    - **音频裁剪：从长音频中截取片段**

    ```bash
    # -i：输入文件
    # -ss 00:01:30：起始时间（1 分 30 秒）
    # -t 00:02:00：截取时长（2 分钟）
    # -c copy：复制音频流，不重新编码（速度快）
    # output_clip.wav：输出文件
    ffmpeg -i long_audio.wav -ss 00:01:30 -t 00:02:00 -c copy output_clip.wav
    ```

    - **格式转换**

      例如，将任意音频转换为 16 kHz、16 位、单声道 WAV

    ```bash
    # -i：输入文件
    # -ac 1：设置为单声道
    # -ar 16000：设置采样率为 16000 Hz（16 kHz）
    # -sample_fmt s16：设置采样格式为 16 位有符号整数 PCM
    # output.wav：输出文件
    ffmpeg -i input.mp3 -ac 1 -ar 16000 -sample_fmt s16 output.wav
    ```
  </Tab>

  <Tab title="Qwen-Omni">
    <Warning>
      Qwen-Omni 会解析所有音频内容，而非仅限语音。音乐、打字声或环境噪声可能导致模型输出描述性文字而非转写结果。对于混合音频，建议使用 VAD 预处理以提取语音片段，或在系统提示词中添加指令："仅转写人声语音，忽略非语音声音。"
    </Warning>

    #### 问：什么情况下应该使用 Qwen-Omni 而非专用 ASR 模型？

    适合使用 Qwen-Omni 的场景：

    1. **领域专业术语**：需要转写包含专业词汇的音频。您可以在系统提示词中描述您的业务领域。
    2. **上下文感知转写**：希望提供对话上下文以提高准确率。
    3. **多模态理解**：需要同时处理音频与图像或视频。
    4. **OpenAI 兼容性**：偏好使用 OpenAI 兼容 API。

    适合使用专用 ASR 模型（Fun-ASR、Qwen-ASR）的场景：

    1. **低延迟**：专用 ASR 模型的单次请求延迟更低。
    2. **热词**：需要热词支持（仅 Fun-ASR 支持）。
    3. **说话人分离**：需要识别不同说话人（仅 Fun-ASR 支持）。
    4. **长音频文件**：Fun-ASR 支持最长 12 小时的音频。如果启用说话人分离功能，建议音频时长不超过 2 小时。

    #### 问：如何使用 Qwen-Omni 提高转写准确率？

    通过系统提示词提供上下文：

    ```python
    messages=[
      {"role": "system", "content": "You are transcribing a medical consultation. Key terms: diabetes, hypertension, metformin."},
      {"role": "user", "content": [{"type": "input_audio", "input_audio": {"data": "..."}}, {"type": "text", "text": "Transcribe this audio."}]}
    ]
    ```
  </Tab>
</Tabs>
