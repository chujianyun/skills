> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan — 创建任务

> 提交文生视频任务（wan2.6 及更早版本）

Wan 文生视频模型支持文本、图片和音频输入，可生成最长 15 秒、最高 1080P 分辨率的视频。

- **核心能力**：支持整数时长（2–15 秒）、自定义分辨率（480P、720P、1080P）、提示词改写和水印。
- **音频能力**：支持自动配音或自定义音频文件，实现音视频同步。**（wan2.5 和 wan2.6 支持）**
- **多镜头叙事**：支持多镜头生成，转场时主体保持一致。**（仅 wan2.6 支持）**

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: Wan 文本生成视频 API
  description: Wan 文本生成视频 API。支持多模态输入（文字、图像、音频），可生成最长 15 秒、分辨率高达 1080P 的视频。采用异步任务模式——先提交任务，再轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createTextToVideo
      summary: 创建文本生成视频任务
      description: 创建文本生成视频任务。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 异步任务提交时必须设置为 `enable`。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/TextToVideoRequest"
      responses:
        "200":
          description: 任务提交成功
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/AsyncTaskSubmitResponse"
        "400":
          description: 请求参数无效
          content:
            application/json:
              schema:
                $ref: "#/components/schemas/DashScopeErrorResponse"
      x-codeSamples:
        - lang: python
          label: Python（同步调用）
          source: |-
            import os
            from http import HTTPStatus
            from dashscope import VideoSynthesis
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            api_key = os.getenv("DASHSCOPE_API_KEY", "YOUR_API_KEY")

            print('please wait...')
            rsp = VideoSynthesis.call(api_key=api_key,
                                      model='wan2.6-t2v',
                                      prompt='A thrilling detective chase story with cinematic storytelling. Shot 1 [0–3 s]: Wide shot of a rainy New York street at night, neon lights flickering, a detective in a black trench coat walking briskly. Shot 2 [3–6 s]: Medium shot of the detective entering an old building, rain soaking his coat, the door closing slowly behind him. Shot 3 [6–9 s]: Close-up of the detective\'s focused, determined eyes as distant sirens wail and he frowns slightly in thought. Shot 4 [9–12 s]: Medium shot of the detective moving carefully down a dim hallway, his flashlight illuminating the path ahead. Shot 5 [12–15 s]: Close-up of the detective discovering a key clue, his face lighting up with sudden realization.',
                                      size="1280*720",
                                      duration=15,
                                      shot_type="multi",
                                      prompt_extend=True,
                                      watermark=True)
            print(rsp)
            if rsp.status_code == HTTPStatus.OK:
              print("video_url:", rsp.output.video_url)
            else:
              print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))
        - lang: python
          label: Python（异步调用）
          source: |-
            import os
            from http import HTTPStatus
            from dashscope import VideoSynthesis
            import dashscope

            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

            api_key = os.getenv("DASHSCOPE_API_KEY")

            def sample_async_call_t2v():
              # 异步调用，返回 task_id
              rsp = VideoSynthesis.async_call(api_key=api_key,
                              model='wan2.6-t2v',
                              prompt='A vision of harmony between future technology and nature. Shot 1 [0–2 s]: Wide shot of an aerial garden in a futuristic city, floating plants swaying gently in the breeze. Shot 2 [2–4 s]: A robot gardener carefully trims plants with precise, graceful movements. Shot 3 [4–7 s]: Sunlight streams through a transparent dome, illuminating the entire garden and showcasing perfect fusion of technology and nature. Shot 4 [7–10 s]: The camera pulls back to reveal the grand scale of the entire futuristic city, with the aerial garden just one part of it.',
                              size='1280*720',
                              shot_type="multi",  # 多镜头
                              duration=10,
                              prompt_extend=True,
                              watermark=True,
                              negative_prompt="",
                              seed=12345)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print("task_id: %s" % rsp.output.task_id)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

              # 等待异步任务完成
              rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
              print(rsp)
              if rsp.status_code == HTTPStatus.OK:
                print(rsp.output.video_url)
              else:
                print('Failed, status_code: %s, code: %s, message: %s' % (rsp.status_code, rsp.code, rsp.message))

            if __name__ == '__main__':
              sample_async_call_t2v()
        - lang: java
          label: Java（同步调用）
          source: |-
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.JsonUtils;
            import com.alibaba.dashscope.utils.Constants;

            public class Text2Video {

              static {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              }

              static String apiKey = System.getenv("DASHSCOPE_API_KEY");

              public static void text2video() throws ApiException, NoApiKeyException, InputRequiredException {
                VideoSynthesis vs = new VideoSynthesis();
                VideoSynthesisParam param =
                    VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-t2v")
                        .prompt("A thrilling detective chase story with cinematic storytelling. Shot 1 [0–3 s]: Wide shot of a rainy New York street at night, neon lights flickering, a detective in a black trench coat walking briskly. Shot 2 [3–6 s]: Medium shot of the detective entering an old building, rain soaking his coat, the door closing slowly behind him. Shot 3 [6–9 s]: Close-up of the detective’s focused, determined eyes as distant sirens wail and he frowns slightly in thought. Shot 4 [9–12 s]: Medium shot of the detective moving carefully down a dim hallway, his flashlight illuminating the path ahead. Shot 5 [12–15 s]: Close-up of the detective discovering a key clue, his face lighting up with sudden realization.")
                        .duration(15)
                        .size("1280*720")
                        .shotType("multi")
                        .promptExtend(true)
                        .watermark(true)
                        .build();
                System.out.println("please wait...");
                VideoSynthesisResult result = vs.call(param);
                System.out.println(JsonUtils.toJson(result));
              }

              public static void main(String[] args) {
                try {
                  text2video();
                } catch (ApiException | NoApiKeyException | InputRequiredException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
        - lang: java
          label: Java（异步调用）
          source: |-
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.JsonUtils;
            import com.alibaba.dashscope.utils.Constants;

            public class Text2Video {
              static {
                Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
              }

              static String apiKey = System.getenv("DASHSCOPE_API_KEY");

              public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
                VideoSynthesis vs = new VideoSynthesis();
                VideoSynthesisParam param =
                    VideoSynthesisParam.builder()
                        .apiKey(apiKey)
                        .model("wan2.6-t2v")
                        .prompt("A vision of harmony between future technology and nature. Shot 1 [0–2 s]: Wide shot of an aerial garden in a futuristic city, floating plants swaying gently in the breeze. Shot 2 [2–4 s]: A robot gardener carefully trims plants with precise, graceful movements. Shot 3 [4–7 s]: Sunlight streams through a transparent dome, illuminating the entire garden and showcasing perfect fusion of technology and nature. Shot 4 [7–10 s]: The camera pulls back to reveal the grand scale of the entire futuristic city, with the aerial garden just one part of it.")
                        .negativePrompt("")
                        .size("1280*720")
                        .shotType("multi")
                        .duration(10)
                        .promptExtend(true)
                        .watermark(true)
                        .seed(12345)
                        .build();
                // 异步调用
                VideoSynthesisResult task = vs.asyncCall(param);
                System.out.println(JsonUtils.toJson(task));
                System.out.println("please wait...");

                // 获取结果
                VideoSynthesisResult result = vs.wait(task, apiKey);
                System.out.println(JsonUtils.toJson(result));
              }

              public static void main(String[] args) {
                try {
                  text2Video();
                } catch (ApiException | NoApiKeyException | InputRequiredException e) {
                  System.out.println(e.getMessage());
                }
                System.exit(0);
              }
            }
        - lang: curl
          label: cURL - 快速入门
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.6-t2v",
              "input": {
                "prompt": "A thrilling detective chase story with cinematic storytelling. Shot 1 [0–3 s]: Wide shot of a rainy New York street at night, neon lights flickering, a detective in a black trench coat walking briskly. Shot 2 [3–6 s]: Medium shot of the detective entering an old building, rain soaking his coat, the door closing slowly behind him. Shot 3 [6–9 s]: Close-up of the detective’s focused, determined eyes as distant sirens wail and he frowns slightly in thought. Shot 4 [9–12 s]: Medium shot of the detective moving carefully down a dim hallway, his flashlight illuminating the path ahead. Shot 5 [12–15 s]: Close-up of the detective discovering a key clue, his face lighting up with sudden realization."
              },
              "parameters": {
                "size": "1280*720",
                "prompt_extend": true,
                "watermark": true,
                "duration": 15,
                "shot_type": "multi"
              }
            }'
        - lang: curl
          label: cURL - 多镜头视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.6-t2v",
              "input": {
                "prompt": "A vision of harmony between future technology and nature. Shot 1 [0–2 s]: Wide shot of an aerial garden in a futuristic city, floating plants swaying gently in the breeze. Shot 2 [2–4 s]: A robot gardener carefully trims plants with precise, graceful movements. Shot 3 [4–7 s]: Sunlight streams through a transparent dome, illuminating the entire garden and showcasing perfect fusion of technology and nature. Shot 4 [7–10 s]: The camera pulls back to reveal the grand scale of the entire futuristic city, with the aerial garden just one part of it."
              },
              "parameters": {
                "size": "1280*720",
                "shot_type": "multi",
                "duration": 10,
                "prompt_extend": true,
                "watermark": true,
                "negative_prompt": "",
                "seed": 12345
              }
            }'
        - lang: curl
          label: cURL - 音频同步
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.6-t2v",
              "input": {
                "prompt": "Shot from a low angle, in a medium close-up, with warm tones. In a classic detective office, a fox wearing a dark brown trench coat sits in a leather chair, speaking in a smooth voice.",
                "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250929/stjqnq/%E7%8B%90%E7%8B%B8.mp3"
              },
              "parameters": {
                "size": "1280*720",
                "shot_type": "multi",
                "duration": 10,
                "prompt_extend": true,
                "watermark": true,
                "negative_prompt": "",
                "seed": 12345
              }
            }'
        - lang: curl
          label: cURL - 静音视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.2-t2v-plus",
              "input": {
                "prompt": "Low contrast. A street musician performs in a retro 1970s-style subway station, bathed in dim colors and rough textures."
              },
              "parameters": {
                "size": "832*480",
                "prompt_extend": true,
                "watermark": true,
                "seed": 12345
              }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    TextToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。支持的模型及其能力详见端点描述中的模型列表。
          enum:
            - wan2.6-t2v
            - wan2.5-t2v-preview
            - wan2.2-t2v-plus
            - wan2.1-t2v-turbo
            - wan2.1-t2v-plus
          example: wan2.6-t2v
        input:
          type: object
          required:
            - prompt
          description: 视频生成的输入数据。
          properties:
            prompt:
              type: string
              description: "描述目标视频内容的文字提示词。生成多镜头视频（wan2.6）时，请使用以下格式：`Shot 1 [0–3 s]: 内容描述。Shot 2 [3–6 s]: 内容描述。` 以此类推。"
              example: A thrilling detective chase story with cinematic storytelling.
            audio_url:
              type: string
              format: uri
              description: 用于音视频同步的音频文件 URL。模型会根据音频对齐口型动作。支持 HTTP/HTTPS URL。**仅 wan2.5 和 wan2.6 系列支持。** 若在 wan2.5/wan2.6 上省略此参数，模型将自动生成背景音频（自动配音）。
        parameters:
          $ref: "#/components/schemas/TextToVideoParameters"
    TextToVideoParameters:
      type: object
      description: 视频生成参数。
      properties:
        size:
          type: string
          description: |-
            输出视频分辨率，格式为 `宽*高`。可用尺寸因模型而异：
            - **wan2.6-t2v**：`1280*720`（720P）、`1920*1080`（1080P）
            - **wan2.5-t2v-preview**：`832*480`（480P）、`1280*720`（720P）、`1920*1080`（1080P）
            - **wan2.2-t2v-plus**：`832*480`（480P）、`1920*1080`（1080P）
            - **wan2.1-t2v-turbo**：`832*480`（480P）、`1280*720`（720P）
            - **wan2.1-t2v-plus**：`1280*720`（720P）
          example: 1280*720
        duration:
          type: integer
          description: |-
            视频时长（秒）。可用时长因模型而异：
            - **wan2.6-t2v**：2 至 15 的整数
            - **wan2.5-t2v-preview**：5 或 10
            - **wan2.2-t2v-plus、wan2.1 系列**：固定为 5
          example: 15
        shot_type:
          type: string
          description: 镜头构成模式。设置为 `"multi"` 可启用多镜头叙事，自动进行镜头切换。**仅 wan2.6 系列支持。**
          enum:
            - multi
        prompt_extend:
          type: boolean
          description: 启用提示词优化。`true`（默认）：模型对提示词进行优化以提升生成效果。`false`：直接使用原始提示词。生成多镜头视频时建议启用。
          default: true
        watermark:
          type: boolean
          description: 在生成的视频上添加水印。默认值：`true`。
          default: true
        negative_prompt:
          type: string
          description: 描述不希望出现在视频中的内容。
        seed:
          type: integer
          description: 随机数种子，用于结果复现。取值范围：[0, 2147483647]。在相同参数下使用相同种子可获得更一致（但不完全相同）的结果。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应结果。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符，用于追踪和排查问题。
          example: c1209113-8437-424f-a386-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 用于轮询任务状态的任务 ID。配合 `GET /tasks/{task_id}` 使用。
              example: 966cebcd-dedc-4962-af88-xxxxxx
            task_status:
              type: string
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    TaskStatusResponse:
      type: object
      description: 查询异步任务状态的响应结果。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符。
          example: c1209113-8437-424f-a386-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 966cebcd-dedc-4962-af88-xxxxxx
            task_status:
              type: string
              description: 当前任务状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL（MP4 格式）。仅在 `task_status` 为 `SUCCEEDED` 时返回。**有效期 24 小时**——请及时下载。
              example: https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx
            code:
              type: string
              description: 错误代码。仅在 `task_status` 为 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息。仅在 `task_status` 为 `FAILED` 时返回。
            task_metrics:
              type: object
              description: 任务结果统计。
              properties:
                TOTAL:
                  type: integer
                  description: 任务总数。
                SUCCEEDED:
                  type: integer
                  description: 成功任务数。
                FAILED:
                  type: integer
                  description: 失败任务数。
        usage:
          type: object
          description: 用量统计。仅在任务成功时返回。
          properties:
            video_count:
              type: integer
              description: 生成的视频数量。
            video_duration:
              type: integer
              description: 生成视频的总时长（秒）。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符。
        code:
          type: string
          description: 错误代码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 人类可读的错误信息。
          example: Invalid model name
````
