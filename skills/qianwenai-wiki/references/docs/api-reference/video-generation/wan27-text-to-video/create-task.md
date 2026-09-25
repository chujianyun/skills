> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.7 — 创建任务

> 提交文本生成视频任务（wan2.7）

通过文本提示生成最长 15 秒的 1080P 视频，支持音频同步和多镜头叙事。

## 与 wan2.6 的区别

- **分辨率控制**：使用 `resolution`（720P/1080P）+ `ratio`（16:9、9:16 等）替代精确像素 `size`。
- **更长提示词**：最多支持 5,000 字符（原为 1,500）。
- **负向提示词位置变更**：移至 `input.negative_prompt`，不再使用 `parameters.negative_prompt`。
- **移除 `shot_type` 参数**：直接在提示词中描述镜头。
- **水印默认关闭**：`watermark` 默认值改为 `false`（原为 `true`）。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: Wan 2.7 文字生成视频 API
  description: 使用 Wan 2.7 模型从文本生成视频。提交异步任务后，通过轮询 `GET /tasks/{task_id}` 获取生成结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createWan27TextToVideo
      summary: 创建文字生成视频任务
      description: 提交文字生成视频任务，返回用于轮询的 `task_id`。
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
              $ref: "#/components/schemas/Wan27TextToVideoRequest"
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
        - lang: curl
          label: cURL - 多镜头叙事
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.7-t2v-2026-06-12",
              "input": {
                "prompt": "A tense detective story with cinematic storytelling. Shot 1 [0\u20133 seconds] wide shot: Rainy New York street at night, neon lights flicker, a detective in a black trench coat walks briskly. Shot 2 [3\u20136 seconds] medium shot: The detective enters an old building, rain wets his coat, the door closes slowly behind him. Shot 3 [6\u20139 seconds] close-up: The detective\u2019s focused eyes, distant sirens sound, he frowns slightly. Shot 4 [9\u201312 seconds] medium shot: The detective moves carefully down a dim hallway, his flashlight illuminating the way. Shot 5 [12\u201315 seconds] close-up: The detective discovers a key clue, his face shows sudden realization."
              },
              "parameters": {
                "resolution": "720P",
                "ratio": "16:9",
                "prompt_extend": true,
                "watermark": true,
                "duration": 15
              }
            }'
        - lang: curl
          label: cURL - 提供音频文件
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.7-t2v-2026-06-12",
              "input": {
                "prompt": "An epic and cute scene. A small, adorable cartoon kitten general, wearing exquisitely detailed golden armor and a slightly oversized helmet, stands bravely on a cliff. He rides a small but heroic warhorse and says: \u2018The long clouds of Qinghai darken the snowy mountains, a lone city gazes at Yumen Pass from afar. Through a hundred battles in the yellow sand, the golden armor is worn, but we will not return until we have broken Loulan\u2019. Below the cliff, a vast and endless army of mice with makeshift weapons is charging forward. This is a dramatic, large-scale battle scene inspired by ancient Chinese war epics. In the distance, dark clouds gather in the sky over the snowy mountains. The overall atmosphere is a comical and epic fusion of \u2018cute\u2019 and \u2018domineering\u2019.",
                "audio_url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3"
              },
              "parameters": {
                "resolution": "1080P",
                "ratio": "16:9",
                "prompt_extend": true,
                "duration": 10
              }
            }'
        - lang: curl
          label: cURL - 自动配音
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.7-t2v-2026-06-12",
              "input": {
                "prompt": "An epic and cute scene. A small, adorable cartoon kitten general, wearing exquisitely detailed golden armor and a slightly oversized helmet, stands bravely on a cliff. He rides a small but heroic warhorse and says: \u2018The long clouds of Qinghai darken the snowy mountains, a lone city gazes at Yumen Pass from afar. Through a hundred battles in the yellow sand, the golden armor is worn, but we will not return until we have broken Loulan\u2019. Below the cliff, a vast and endless army of mice with makeshift weapons is charging forward. This is a dramatic, large-scale battle scene inspired by ancient Chinese war epics. In the distance, dark clouds gather in the sky over the snowy mountains. The overall atmosphere is a comical and epic fusion of \u2018cute\u2019 and \u2018domineering\u2019."
              },
              "parameters": {
                "resolution": "720P",
                "ratio": "16:9",
                "prompt_extend": true,
                "duration": 10
              }
            }'
        - lang: curl
          label: cURL - 使用负向提示词
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.7-t2v-2026-06-12",
              "input": {
                "prompt": "A kitten running in the moonlight",
                "negative_prompt": "flower"
              },
              "parameters": {
                "resolution": "720P",
                "ratio": "16:9"
              }
            }'
        - lang: python
          label: Python - 同步调用
          source: |
            from http import HTTPStatus
            from dashscope import VideoSynthesis
            import dashscope
            import os
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            # 若没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
            api_key = os.getenv("DASHSCOPE_API_KEY")
            def sample_sync_call_t2v():
                # call sync api, will return the result
                print('please wait...')
                rsp = VideoSynthesis.call(api_key=api_key,
                                          model='wan2.7-t2v-2026-06-12',
                                          prompt='一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说："青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。"。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是"可爱"与"霸气"的搞笑和史诗般的融合。',
                                          audio_url='https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3',
                                          resolution='720P',
                                          ratio='16:9',
                                          duration=10,
                                          negative_prompt="",
                                          prompt_extend=True,
                                          watermark=False,
                                          seed=12345)
                print(rsp)
                if rsp.status_code == HTTPStatus.OK:
                    print(rsp.output.video_url)
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))
            if __name__ == '__main__':
                sample_sync_call_t2v()
        - lang: python
          label: Python - 异步调用
          source: |-
            from http import HTTPStatus
            from dashscope import VideoSynthesis
            import dashscope
            import os
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            # 若没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
            api_key = os.getenv("DASHSCOPE_API_KEY")
            def sample_async_call_t2v():
                # call async api, will return the task information
                # you can get task status with the returned task id.
                rsp = VideoSynthesis.async_call(api_key=api_key,
                                                model='wan2.7-t2v-2026-06-12',
                                                prompt='一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说："青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。"。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是"可爱"与"霸气"的搞笑和史诗般的融合。',
                                                audio_url='https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3',
                                                resolution='720P',
                                                ratio='16:9',
                                                duration=10,
                                                negative_prompt="",
                                                prompt_extend=True,
                                                watermark=False,
                                                seed=12345)
                print(rsp)
                if rsp.status_code == HTTPStatus.OK:
                    print("task_id: %s" % rsp.output.task_id)
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))
                # get the task information include the task status.
                status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
                if status.status_code == HTTPStatus.OK:
                    print(status.output.task_status)  # check the task status
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (status.status_code, status.code, status.message))
                # wait the task complete, will call fetch interval, and check it's in finished status.
                rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
                print(rsp)
                if rsp.status_code == HTTPStatus.OK:
                    print(rsp.output.video_url)
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))
            if __name__ == '__main__':
                sample_async_call_t2v()
        - lang: java
          label: Java - 同步调用
          source: |
            // Copyright (c) Alibaba, Inc. and its affiliates.
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.JsonUtils;
            import com.alibaba.dashscope.utils.Constants;
            import java.util.HashMap;
            import java.util.Map;
            public class Text2Video {
                static {
                            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                }
                // 若没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
                    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");
                /**
                 * Create a video compositing task and wait for the task to complete.
                 */
                public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
                    VideoSynthesis vs = new VideoSynthesis();
                    VideoSynthesisParam param =
                            VideoSynthesisParam.builder()
                                    .apiKey(apiKey)
                                    .model("wan2.7-t2v-2026-06-12")
                                    .prompt("一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是可爱与霸气的搞笑和史诗般的融合。")
                                    .audioUrl("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3")
                                    .negativePrompt("")
                                    .resolution("720P")
                                    .ratio("16:9")
                                    .duration(10)
                                    .promptExtend(true)
                                    .watermark(false)
                                    .build();
                    System.out.println("please wait...");
                    VideoSynthesisResult result = vs.call(param);
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
        - lang: java
          label: Java - 异步调用
          source: |
            // Copyright (c) Alibaba, Inc. and its affiliates.
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisListResult;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.task.AsyncTaskListParam;
            import com.alibaba.dashscope.utils.JsonUtils;
            import com.alibaba.dashscope.utils.Constants;
            import java.util.HashMap;
            import java.util.Map;
            public class Text2Video {
                static {
                            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                }
                // 若没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
                    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");
                /**
                 * Create a video compositing task and wait for the task to complete.
                 */
                public static void text2Video() throws ApiException, NoApiKeyException, InputRequiredException {
                    VideoSynthesis vs = new VideoSynthesis();
                    VideoSynthesisParam param =
                            VideoSynthesisParam.builder()
                                    .apiKey(apiKey)
                                    .model("wan2.7-t2v-2026-06-12")
                                    .prompt("一幅史诗级可爱的场景。一只小巧可爱的卡通小猫将军，身穿细节精致的金色盔甲，头戴一个稍大的头盔，勇敢地站在悬崖上。他骑着一匹虽小但英勇的战马，说：”青海长云暗雪山，孤城遥望玉门关。黄沙百战穿金甲，不破楼兰终不还。“。悬崖下方，一支由老鼠组成的、数量庞大、无穷无尽的军队正带着临时制作的武器向前冲锋。这是一个戏剧性的、大规模的战斗场景，灵感来自中国古代的战争史诗。远处的雪山上空，天空乌云密布。整体氛围是可爱与霸气的搞笑和史诗般的融合。")
                                    .audioUrl("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250923/hbiayh/%E4%BB%8E%E5%86%9B%E8%A1%8C.mp3")
                                    .negativePrompt("")
                                    .resolution("720P")
                                    .ratio("16:9")
                                    .duration(10)
                                    .promptExtend(true)
                                    .watermark(false)
                                    .build();
                    // 异步调用
                    VideoSynthesisResult task = vs.asyncCall(param);
                    System.out.println(JsonUtils.toJson(task));
                    System.out.println("please wait...");
                    //获取结果
                    VideoSynthesisResult result = vs.wait(task, apiKey);
                    System.out.println(JsonUtils.toJson(result));
                }
                // 获取任务列表
                public static void listTask() throws ApiException, NoApiKeyException {
                    VideoSynthesis is = new VideoSynthesis();
                    AsyncTaskListParam param = AsyncTaskListParam.builder().build();
                    param.setApiKey(apiKey);
                    VideoSynthesisListResult result = is.list(param);
                    System.out.println(result);
                }
                // 获取单个任务结果
                public static void fetchTask(String taskId) throws ApiException, NoApiKeyException {
                    VideoSynthesis is = new VideoSynthesis();
                    // 如果已设置 DASHSCOPE_API_KEY 为环境变量，apiKey 可为空
                    VideoSynthesisResult result = is.fetch(taskId, apiKey);
                    System.out.println(result.getOutput());
                    System.out.println(result.getUsage());
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
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan27TextToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型标识符。可选值：`wan2.7-t2v`（主线版本，持续更新）、`wan2.7-t2v-2026-06-12`（最新快照版本）、`wan2.7-t2v-2026-04-25`（旧快照版本）。
          enum:
            - wan2.7-t2v
            - wan2.7-t2v-2026-06-12
            - wan2.7-t2v-2026-04-25
          example: wan2.7-t2v
        input:
          type: object
          required:
            - prompt
          description: 视频生成的输入内容。
          properties:
            prompt:
              type: string
              description: "描述您想要生成的视频内容，支持中英文，最多 5,000 个字符（超出自动截断）。多镜头视频可按时间戳描述每个镜头，例如：`Shot 1 [0-3 seconds] wide shot: ...`。"
              example: A kitten running in the moonlight.
            negative_prompt:
              type: string
              description: 描述视频中不想出现的内容（如 `low quality, blurry, extra fingers`），支持中英文，最多 500 个字符（超出自动截断）。
              example: low resolution, error, worst quality, low quality, deformed, extra fingers, bad proportions
            audio_url:
              type: string
              format: uri
              description: 用于口型同步和动作对齐的音频文件 URL。模型会将人物的口型动作与音频轨道匹配。支持通过 HTTP/HTTPS 访问的 WAV 和 MP3 格式，时长 2-30 秒，大小不超过 15 MB。音频长于视频时将被截断；短于视频时，剩余部分保持静音。若不填写，模型将自动生成匹配的背景音乐或音效。
        parameters:
          $ref: "#/components/schemas/Wan27TextToVideoParameters"
    Wan27TextToVideoParameters:
      type: object
      description: 视频生成参数。
      properties:
        resolution:
          type: string
          description: |-
            视频清晰度等级，分辨率越高费用越高。

            实际输出尺寸取决于 `ratio`：
            - **720P**：16:9=1280x720，9:16=720x1280，1:1=960x960，4:3=1104x832，3:4=832x1104
            - **1080P**：16:9=1920x1080，9:16=1080x1920，1:1=1440x1440，4:3=1648x1248，3:4=1248x1648
          enum:
            - 720P
            - 1080P
          default: 1080P
        ratio:
          type: string
          description: 生成视频的宽高比，默认值：`16:9`。
          enum:
            - 16:9
            - 9:16
            - 1:1
            - 4:3
            - 3:4
          default: 16:9
        duration:
          type: integer
          description: 视频时长（秒），取整数，范围 2-15。时长越长费用越高，按秒计费。
          minimum: 2
          maximum: 15
          default: 5
        prompt_extend:
          type: boolean
          description: 在生成前使用大语言模型对提示词进行改写扩展。对简短或模糊的提示词效果提升明显，但会增加响应时延。设为 `false` 可直接使用原始提示词。
          default: true
        watermark:
          type: boolean
          description: 在视频右下角添加「AI 生成」水印。
          default: false
        seed:
          type: integer
          description: 用于生成可复现结果的随机种子。相同种子和参数产生相近（而非完全相同）的输出。
          minimum: 0
          maximum: 2147483647
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交的响应。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符，用于追踪和排查问题。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 用于轮询任务状态的任务 ID，配合 `GET /tasks/{task_id}` 使用。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
    Wan27TaskStatusResponse:
      type: object
      description: Wan 2.7 文字生成视频的任务状态响应。
      properties:
        request_id:
          type: string
          description: 请求 ID，用于排查问题。联系技术支持时请提供此 ID。
          example: caa62a12-8841-41a6-8af2-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，提交后 24 小时内可查询。
              example: eff1443c-ccab-4676-aad3-xxxxxx
            task_status:
              type: string
              description: 任务生命周期：`PENDING` -> `RUNNING` -> `SUCCEEDED` 或 `FAILED`。手动停止时为 `CANCELED`，超期后为 `UNKNOWN`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`）。
              example: 2025-09-29 14:18:52.331
            scheduled_time:
              type: string
              description: 任务开始执行的时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`）。
              example: 2025-09-29 14:18:59.290
            end_time:
              type: string
              description: 任务结束时间（UTC+8，格式：`YYYY-MM-DD HH:mm:ss.SSS`）。仅在任务状态为 `SUCCEEDED` 或 `FAILED` 时返回。
              example: 2025-09-29 14:23:39.407
            orig_prompt:
              type: string
              description: 经 `prompt_extend` 改写前的原始提示词。
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL（MP4 格式，H.264 编码）。仅在 `task_status` 为 `SUCCEEDED` 时返回。**链接 24 小时内有效**，请及时下载。
              example: https://dashscope-result-sh.oss-accelerate.aliyuncs.com/xxx.mp4?Expires=xxx
            code:
              type: string
              description: 错误码，仅在 `task_status` 为 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息，仅在 `task_status` 为 `FAILED` 时返回。
        usage:
          type: object
          description: 资源用量，仅在 `task_status` 为 `SUCCEEDED` 时返回。
          properties:
            duration:
              type: number
              description: 计费视频时长（秒），等于 `output_video_duration`。
            input_video_duration:
              type: integer
              description: 文字生成视频时始终为 `0`（无输入视频）。
            output_video_duration:
              type: integer
              description: 输出视频时长（秒），与请求的 `duration` 一致。
            video_count:
              type: integer
              description: 生成的视频数量，始终为 `1`。
            ratio:
              type: string
              description: 实际使用的宽高比（如 `16:9`），与请求的 `ratio` 一致。
            SR:
              type: integer
              description: 实际使用的分辨率等级（如 `720` 对应 720P，`1080` 对应 1080P），与请求的 `resolution` 一致。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求的唯一标识符，用于追踪和技术支持。
        code:
          type: string
          description: 机器可读的错误码（如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 人类可读的错误信息。
          example: Invalid model name
````
