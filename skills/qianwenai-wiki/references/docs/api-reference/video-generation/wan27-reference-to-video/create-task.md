> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Wan 2.7 — 参考素材生成视频

> 提交 Wan 2.7 参考素材生成视频任务

基于多模态输入（文本、图片、视频），使用 Wan 2.7 模型（`wan2.7-r2v`）生成自然逼真的表演视频。

- **角色演绎**：从参考图片或视频中复刻角色外观。参考视频还可复刻音色。支持单人或多人表演，最多可提供 5 个参考素材。
- **媒体数组输入**：通过 `media` 数组提供参考图片、视频或首帧图像。在提示词中使用 `Video 1`/`Image 1` 按序引用对应角色，图片和视频分别计数。
- **多分镜叙事**：通过时间段描述多镜头叙事（如 `镜头 1 [0-3s]: ...`），提供关键镜头，模型自动识别分镜逻辑。
- **声音克隆**：通过 `reference_voice` 提供音频文件来设定音色。未指定时，默认使用参考视频中的音频。
- **分辨率与画面比例**：通过 `resolution` 设置输出质量（720P/1080P），通过 `ratio` 设置画面比例（16:9、9:16、1:1、4:3、3:4）。提供 `first_frame` 首帧图像时，`ratio` 自动根据图像推断。
- **提示词扩写**：启用 `prompt_extend` 后，LLM 会自动扩写提示词。较短的提示词效果提升明显，但会增加处理时间。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: Wan 2.7 参考内容生视频 API
  description: Wan 2.7 参考内容生视频 API。基于参考图片或视频生成表演视频，支持多模态输入（文本、图像、视频）。采用新协议，通过 media 数组传入参考内容，支持分辨率和比例参数配置，并提供增强版响应元数据。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createWan27RefToVideo
      summary: 创建 Wan 2.7 参考内容生视频任务
      description: 创建一个 Wan 2.7 参考内容生视频任务。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 必须设置为 `enable`，用于创建异步任务。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Wan27RefToVideoRequest"
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
          label: cURL - 多主体参考
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.7-r2v-2026-06-12",
              "input": {
                "prompt": "Video 2 holds Image 3 and plays a soothing American country ballad in a coffee shop, while Video 1 smiles, watches Video 2, and slowly walks towards him",
                "media": [
                  {"type": "reference_video", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/hfugmr/wan-r2v-role1.mp4"},
                  {"type": "reference_video", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4"},
                  {"type": "reference_image", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"}
                ]
              },
              "parameters": {
                "resolution": "720P",
                "duration": 10,
                "prompt_extend": false,
                "watermark": true
              }
            }'
        - lang: curl
          label: cURL - 单图参考
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
              -H 'X-DashScope-Async: enable' \
              -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
              -H 'Content-Type: application/json' \
              -d '{
              "model": "wan2.7-r2v-2026-06-12",
              "input": {
                "prompt": "Based on the reference image, in the style of a 3D cartoon adventure movie. The characters are in a cute Q-style but with detailed textures, smooth movements, and vibrant colors. Keep the characters and the forest scene consistent. Do not add text. Atmosphere: Adventurous, light-hearted, mysterious, whimsical. Characters: A young boy explorer with a round hat, backpack, and short cloak. His sidekick: a small flying robot with a round body and glowing blue eyes. Scene: A magical forest with giant tree roots, mushrooms, vines, a treasure cave entrance, and sunbeams. Storyboard: 1. Wide shot: Tall trees and intersecting sunbeams in the magical forest, creating a mysterious and bright environment. 2. Medium shot: The little boy pushes aside vines to explore forward. 3. Medium shot: The little robot flies beside him, scanning ahead with its blue light. 4. Close-up: An old treasure map unfolds in his hands. 5. Close-up: His face lights up with excitement. 6. Action shot: The two jump over tree roots and a small stream, venturing deeper into the forest. 7. Medium shot: A moss-covered treasure chest is revealed behind the vines. 8. Close-up: A golden glow emanates from the edge of the chest. 9. Final shot: The boy and the robot stand before the chest, looking at each other in surprise, filled with a sense of adventure.",
                "media": [
                  {"type": "reference_image", "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260403/wgjaxy/banana_storyboard_00000020.png"}
                ]
              },
              "parameters": {
                "resolution": "720P",
                "duration": 10,
                "prompt_extend": false,
                "watermark": true
              }
            }'
        - lang: python
          label: Python - 同步调用
          source: |-
            from http import HTTPStatus
            from dashscope import VideoSynthesis
            import dashscope
            import os
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            # 若没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
            api_key = os.getenv("DASHSCOPE_API_KEY")
            def sample_sync_call_r2v():
                # 同步调用，直接返回结果
                print('please wait...')
                rsp = VideoSynthesis.call(
                    api_key=api_key,
                    model='wan2.7-r2v-2026-06-12',
                    prompt='视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ',
                    media=[
                        {
                            "type": "reference_image",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg",
                            "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3"
                        },
                        {
                            "type": "reference_video",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4",
                            "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/isllrq/wan-r2v-boy-voice.mp3"
                        },
                        {
                            "type": "reference_image",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png"
                        },
                        {
                            "type": "reference_image",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
                        },
                        {
                            "type": "reference_image",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
                        }
                    ],
                    resolution='720P',
                    ratio='16:9',
                    duration=10,
                    prompt_extend=False,
                    watermark=True)
                print(rsp)
                if rsp.status_code == HTTPStatus.OK:
                    print(rsp.output.video_url)
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))
            if __name__ == '__main__':
                sample_sync_call_r2v()
        - lang: python
          label: Python - 异步调用
          source: |-
            import os
            from http import HTTPStatus
            from dashscope import VideoSynthesis
            import dashscope
            dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'
            # 若没有配置环境变量，请用API Key将下行替换为：api_key="sk-xxx"
            api_key = os.getenv("DASHSCOPE_API_KEY")
            def sample_async_call_r2v():
                # 异步调用，返回一个task_id
                rsp = VideoSynthesis.async_call(
                    api_key=api_key,
                    model='wan2.7-r2v-2026-06-12',
                    prompt='视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ',
                    media=[
                        {
                            "type": "reference_image",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg",
                            "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3"
                        },
                        {
                            "type": "reference_video",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4",
                            "reference_voice": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/isllrq/wan-r2v-boy-voice.mp3"
                        },
                        {
                            "type": "reference_image",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png"
                        },
                        {
                            "type": "reference_image",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png"
                        },
                        {
                            "type": "reference_image",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png"
                        }
                    ],
                    resolution='720P',
                    ratio='16:9',
                    duration=10,
                    prompt_extend=False,
                    watermark=True)
                print(rsp)
                if rsp.status_code == HTTPStatus.OK:
                    print("task_id: %s" % rsp.output.task_id)
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))
                # 获取异步任务信息
                status = VideoSynthesis.fetch(task=rsp, api_key=api_key)
                if status.status_code == HTTPStatus.OK:
                    print(status.output.task_status)
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (status.status_code, status.code, status.message))
                # 等待异步任务结束
                rsp = VideoSynthesis.wait(task=rsp, api_key=api_key)
                print(rsp)
                if rsp.status_code == HTTPStatus.OK:
                    print(rsp.output.video_url)
                else:
                    print('Failed, status_code: %s, code: %s, message: %s' %
                          (rsp.status_code, rsp.code, rsp.message))
            if __name__ == '__main__':
                sample_async_call_r2v()
        - lang: java
          label: Java - 同步调用
          source: |-
            // Copyright (c) Alibaba, Inc. and its affiliates.
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesis;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisParam;
            import com.alibaba.dashscope.aigc.videosynthesis.VideoSynthesisResult;
            import com.alibaba.dashscope.exception.ApiException;
            import com.alibaba.dashscope.exception.InputRequiredException;
            import com.alibaba.dashscope.exception.NoApiKeyException;
            import com.alibaba.dashscope.utils.JsonUtils;
            import com.alibaba.dashscope.utils.Constants;
            import java.util.ArrayList;
            import java.util.HashMap;
            import java.util.List;
            import java.util.Map;
            public class Ref2Video {
                static {
                            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                }
                // 若没有配置环境变量，请用API Key将下行替换为：apiKey="sk-xxx"
                    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");
                public static void ref2video() throws ApiException, NoApiKeyException, InputRequiredException {
                    VideoSynthesis vs = new VideoSynthesis();
                    List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg")
                                .type("reference_image")
                                .referenceVoice("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3")
                                .build());
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4")
                                .type("reference_video")
                                .referenceVoice("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/isllrq/wan-r2v-boy-voice.mp3")
                                .build());
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png")
                                .type("reference_image")
                                .build());
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png")
                                .type("reference_image")
                                .build());
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png")
                                .type("reference_image")
                                .build());
                    }};
                    Map<String, Object> parameters = new HashMap<>();
                    parameters.put("resolution", "720P");
                    parameters.put("ratio", "16:9");
                    parameters.put("prompt_extend", false);
                    parameters.put("watermark", true);
                    VideoSynthesisParam param =
                            VideoSynthesisParam.builder()
                                    .apiKey(apiKey)
                                    .model("wan2.7-r2v-2026-06-12")
                                    .prompt("视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ")
                                    .media(media)
                                    .duration(10)
                                    .parameters(parameters)
                                    .build();
                    System.out.println("please wait...");
                    VideoSynthesisResult result = vs.call(param);
                    System.out.println(JsonUtils.toJson(result));
                }
                public static void main(String[] args) {
                    try {
                        ref2video();
                    } catch (ApiException | NoApiKeyException | InputRequiredException e) {
                        System.out.println(e.getMessage());
                    }
                    System.exit(0);
                }
            }
        - lang: java
          label: Java - 异步调用
          source: |-
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
            import java.util.ArrayList;
            import java.util.HashMap;
            import java.util.List;
            import java.util.Map;
            public class Ref2VideoAsync {
                static {
                            Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
                }
                // 若没有配置环境变量，请用API Key将下行替换为：apiKey="sk-xxx"
                    public static String apiKey = System.getenv("DASHSCOPE_API_KEY");
                public static void asyncRef2video() throws ApiException, NoApiKeyException, InputRequiredException, InterruptedException {
                    VideoSynthesis vs = new VideoSynthesis();
                    List<VideoSynthesisParam.Media> media = new ArrayList<VideoSynthesisParam.Media>(){{
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg")
                                .type("reference_image")
                                .referenceVoice("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/gbqewz/wan-r2v-girl-voice.mp3")
                                .build());
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4")
                                .type("reference_video")
                                .referenceVoice("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/isllrq/wan-r2v-boy-voice.mp3")
                                .build());
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/rtjeqf/wan-r2v-object3.png")
                                .type("reference_image")
                                .build());
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qpzxps/wan-r2v-object4.png")
                                .type("reference_image")
                                .build());
                        add(VideoSynthesisParam.Media.builder()
                                .url("https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/wfjikw/wan-r2v-backgroud5.png")
                                .type("reference_image")
                                .build());
                    }};
                    Map<String, Object> parameters = new HashMap<>();
                    parameters.put("resolution", "720P");
                    parameters.put("ratio", "16:9");
                    parameters.put("prompt_extend", false);
                    parameters.put("watermark", true);
                    VideoSynthesisParam param =
                            VideoSynthesisParam.builder()
                                    .apiKey(apiKey)
                                    .model("wan2.7-r2v-2026-06-12")
                                    .prompt("视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：“今天的阳光真好。”图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：“真好听，能不能再唱一遍”。 ")
                                    .media(media)
                                    .duration(10)
                                    .parameters(parameters)
                                    .build();
                    // 提交异步任务
                    VideoSynthesisResult result = vs.asyncCall(param);
                    System.out.println("task_id: " + result.getOutput().getTaskId());
                    System.out.println(JsonUtils.toJson(result));
                    // 等待任务完成
                    result = vs.wait(result, null);
                    System.out.println(JsonUtils.toJson(result));
                }
                public static void main(String[] args) {
                    try {
                        asyncRef2video();
                    } catch (ApiException | NoApiKeyException | InputRequiredException | InterruptedException e) {
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
    Wan27RefToVideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型标识符。可选值：`wan2.7-r2v`（主线版本，持续更新）、`wan2.7-r2v-2026-06-12`（最新快照版本）。
          enum:
            - wan2.7-r2v
            - wan2.7-r2v-2026-06-12
          example: wan2.7-r2v
        input:
          $ref: "#/components/schemas/Wan27RefToVideoInput"
        parameters:
          $ref: "#/components/schemas/Wan27RefToVideoParameters"
    Wan27RefToVideoInput:
      type: object
      required:
        - prompt
        - media
      description: Wan 2.7 参考内容生视频的输入数据。
      properties:
        prompt:
          type: string
          maxLength: 5000
          description: |-
            描述期望视频内容的文本提示词。支持中文和英文，每个汉字、字母和标点符号均计为一个字符，超出限制的文本将自动截断。

            **引用标识符**：使用 `图片 1`、`图片 2`（英文：`Image 1`、`Image 2`）等标识符引用参考图片中的角色，使用 `视频 1`、`视频 2`（英文：`Video 1`、`Video 2`）等标识符引用参考视频中的角色。编号与 `media` 数组中的顺序对应，图片和视频分开计数——`图片 1` 与 `视频 1` 可以同时存在。若只有一张参考图片或一段参考视频，也可以直接用「参考图片」或「参考视频」来指代。

            **场景描述**：支持两种描述方式：（1）直接使用标识符："图片 1 正在图片 2 中玩耍"；（2）补充主体或场景背景："图片 1 中的猫正在图片 2 中的房间里玩耍"。

            **多镜头分镜**：使用时间段描述多镜头叙事（例如 `镜头 1 [0-3s]: ...`）。无需描述每个镜头，只需提供关键镜头，模型会自动识别分镜逻辑。
          example: Video 2 holds Image 3 and plays a soothing American country ballad in a coffee shop
        negative_prompt:
          type: string
          maxLength: 500
          description: 指定生成视频中需要排除的内容。支持中文和英文，最多 500 个字符，超出限制的文本将自动截断。示例值：`low resolution, error, worst quality, low quality, disfigured, extra fingers, bad proportions`。
        media:
          type: array
          description: |-
            参考媒体对象数组，每个对象包含 `type` 和 `url` 字段。支持图片和视频输入，用于视觉参考。图片支持多视角输入，常用于角色、道具和场景的参考。

            **排列顺序**：数组中第一个 `reference_video` 为视频 1，第二个为视频 2，以此类推；第一个 `reference_image` 为图片 1，第二个为图片 2。图片和视频分开计数。

            **数量限制**：至少需要 1 张参考图片或参考视频；图片与视频总数不得超过 5 个；`first_frame` 最多允许 1 个。每张参考图片或参考视频在用于主角刻画时，应只包含单个角色。
          items:
            $ref: "#/components/schemas/MediaItem"
          minItems: 1
          maxItems: 5
        reference_voice:
          type: string
          format: uri
          description: |-
            用于音色参考的音频文件 URL。配合 `reference_image` 或 `reference_video` 使用，为主角指定音色。该音频仅用于音色参考，与说话内容无关。

            支持格式：WAV、MP3。时长：1-10 秒。文件大小上限：15 MB。

            **默认行为**：若 `reference_video` 包含音频且未指定 `reference_voice`，则使用视频原音作为音色参考。

            **优先级**：若同时提供了 `reference_video` 音频和 `reference_voice`，则以 `reference_voice` 为准。

            为获得最佳效果，参考音频的语言应与提示词语言一致。
    MediaItem:
      type: object
      required:
        - type
        - url
      description: 参考媒体项（图片、视频或首帧图片）。
      properties:
        type:
          type: string
          description: |-
            参考媒体的类型。
            - `reference_image`：包含单个角色或物体的参考图片。支持格式：JPEG、JPG、PNG（不支持 alpha 通道）、BMP、WEBP。分辨率：每边 240-8000 px。宽高比：1:8 至 8:1。文件大小上限：20 MB。
            - `reference_video`：包含单个角色的参考视频。支持格式：MP4、MOV。时长：1-30 秒。分辨率：每边 240-4096 px。宽高比：1:8 至 8:1。文件大小上限：100 MB。
            - `first_frame`：生成视频的首帧图片，最多允许 1 张。支持格式和限制与 `reference_image` 相同。与主体参考配合使用时，分两种场景：（1）主体已在首帧中——通过主体参考增强角色一致性或参考音色；（2）主体不在首帧中——通过主体参考定义视频中途出现的新角色特征。
          enum:
            - reference_image
            - reference_video
            - first_frame
        url:
          type: string
          format: uri
          description: 参考媒体文件的 URL。
    Wan27RefToVideoParameters:
      type: object
      description: Wan 2.7 参考内容生视频的生成参数。
      properties:
        resolution:
          type: string
          description: |-
            视频清晰度档位，分辨率越高费用越高。

            实际输出尺寸取决于 `ratio` 参数：
            - **720P**：16:9=1280x720，9:16=720x1280，1:1=960x960，4:3=1104x832，3:4=832x1104
            - **1080P**：16:9=1920x1080，9:16=1080x1920，1:1=1440x1440，4:3=1648x1248，3:4=1248x1648
          enum:
            - 720P
            - 1080P
          default: 1080P
        ratio:
          type: string
          description: 输出视频的宽高比。若提供了 `first_frame` 首帧图片，则忽略此参数，视频将采用首帧图片的宽高比。
          enum:
            - 16:9
            - 9:16
            - 1:1
            - 4:3
            - 3:4
          default: 16:9
        duration:
          type: integer
          description: 视频时长（秒），时长越长费用越高，按秒计费。取值范围视参考素材而定：若参考素材包含视频，范围为 2-10 秒；若参考素材仅含图片，范围为 2-15 秒。
          minimum: 2
          maximum: 15
          default: 5
        prompt_extend:
          type: boolean
          description: 是否使用大语言模型对提示词进行扩写。对简短提示词有改善效果，但会增加处理时间。
          default: true
        seed:
          type: integer
          description: 用于可复现生成的随机种子。若不指定，则随机生成。固定种子有助于提高复现性，但由于模型生成具有随机性，相同种子并不保证输出完全一致。
          minimum: 0
          maximum: 2147483647
        watermark:
          type: boolean
          description: 是否在输出视频右下角添加「AI 生成」水印。
          default: false
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务创建成功后返回的响应。
      properties:
        request_id:
          type: string
          description: 唯一请求 ID。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。使用此 ID 调用 `GET /tasks/{task_id}` 轮询任务结果。
            task_status:
              type: string
              description: 任务初始状态，通常为 `PENDING`。
              enum:
                - PENDING
    TaskStatusResponse:
      type: object
      description: 包含 Wan 2.7 参考内容生视频任务当前状态和结果的响应。
      properties:
        request_id:
          type: string
          description: 唯一请求 ID。
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
            task_status:
              type: string
              description: 任务当前状态。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间，UTC+8 格式（例如：`2026-04-02 22:53:19.537`）。
            scheduled_time:
              type: string
              description: 任务调度时间，UTC+8 格式。
            end_time:
              type: string
              description: 任务完成时间，UTC+8 格式。
            orig_prompt:
              type: string
              description: 提示词扩写前的原始提示词内容。
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL（MP4 格式，H.264 编码）。仅在 `task_status` 为 `SUCCEEDED` 时存在，有效期 24 小时，请及时下载。
            code:
              type: string
              description: 错误码，仅在 `task_status` 为 `FAILED` 时存在。
            message:
              type: string
              description: 错误信息，仅在 `task_status` 为 `FAILED` 时存在。
        usage:
          type: object
          description: 用量统计（仅在任务成功时存在）。
          properties:
            duration:
              type: integer
              description: 总计费时长（秒），等于 `input_video_duration` 与 `output_video_duration` 之和。
            input_video_duration:
              type: integer
              description: 输入参考视频的时长（秒）。
            output_video_duration:
              type: integer
              description: 生成视频的时长（秒）。
            video_count:
              type: integer
              description: 生成视频数量（固定为 1）。
            SR:
              type: integer
              description: 生成视频的分辨率（如 720 或 1080）。
            ratio:
              type: string
              description: 生成视频的宽高比（如 `16:9`）。
    DashScopeErrorResponse:
      type: object
      description: DashScope API 错误响应。
      properties:
        request_id:
          type: string
          description: 唯一请求 ID。
        code:
          type: string
          description: 错误码（例如 `InvalidParameter`、`Throttling`、`Unauthorized`）。
          example: InvalidParameter
        message:
          type: string
          description: 可读的错误信息。
          example: "Invalid parameter: resolution"
````
