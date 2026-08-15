> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# wan3.0-video 视频生成

> wan3.0-video 全能参考视频生成模型。支持文生视频、首帧/首尾帧生视频、全能参考生视频、有声视频等能力。邀测中。

## OpenAPI

````yaml post /services/aigc/video-generation/video-synthesis
openapi: 3.1.0
info:
  title: 万相 3.0 视频生成 API
  description: 万相 3.0 是全能参考视频生成模型（All-in-One），统一支持文生视频、图生视频（首帧/首尾帧）、参考生视频和参考文件生视频等多种用法，最长可生成30秒视频。提交异步任务后，通过 `GET /tasks/{task_id}` 轮询获取结果。
  version: 1.0.0
servers:
  - url: https://dashscope.aliyuncs.com/api/v1
    description: 千问AI平台
security:
  - BearerAuth: []
paths:
  /services/aigc/video-generation/video-synthesis:
    post:
      operationId: createWan30VideoTask
      summary: 提交视频生成任务
      description: 提交视频生成任务，返回 `task_id` 用于轮询查询。支持文生视频、首帧/首尾帧生视频、全能参考生视频、参考文件生视频等用法。
      parameters:
        - name: X-DashScope-Async
          in: header
          required: true
          description: 必须设置为 `enable`，表示异步提交任务。缺少此请求头将报错："current user api does not support synchronous calls"。
          schema:
            type: string
            enum:
              - enable
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: "#/components/schemas/Wan30VideoRequest"
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
          label: 参考文件生视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "wan3.0-video",
                "input": {
                    "prompt": "一支高端智能眼镜产品广告，整体风格极简、未来感、时尚高级，光影克制，画面以黑色、银灰色、冰蓝色为主色调，局部点缀柔和白光与参数UI图形。开场在纯黑背景中，一副智能眼镜从黑暗中缓缓浮现，镜腿边缘掠过精致高光，镜框轮廓在冷冽边缘光下被勾勒出来，镜头超近距离掠过镜片、鼻托、转轴、镜腿与材质细节，展现金属与高性能复合材料的细腻质感，表面处理高级克制，线条轻薄流畅。随后产品在空中缓慢旋转，画面以极简动态图形同步展示核心参数信息。随后镜头快速收拢，所有零件精准回归组装成完整产品，切换到年轻模特佩戴展示，模特五官立体、气质自信，穿着简洁高级的都市时尚服装，在极简空间和城市光影环境中自然转头、抬手、行走、微笑，镜头从正面、侧面、斜后方展示眼镜佩戴状态，突出轻薄贴合、时尚轮廓与日常百搭属性。结尾在纯色背景中，产品悬浮定格，镜头缓慢推进到品牌logo和核心slogan，整体音乐极简电子氛围配合精准鼓点，节奏干净有力，画面质感高级、克制、纯粹，具有强烈品牌记忆点和国际化科技审美。",
                    "media": [
                        {
                            "type": "file",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260806/ebapmr/glass.pptx"
                        }
                    ]
                },
                "parameters": {
                    "resolution": "480P",
                    "ratio": "adaptive",
                    "duration": 10
                }
            }'
        - lang: curl
          label: 参考生视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "wan3.0-video",
                "input": {
                    "prompt": "视频1抱着图3，在图4的椅子上弹奏一支舒缓的乡村民谣，并说道：\"今天的阳光真好。\"图1手中拿着图2，路过视频1，把手中的图2放到视频1旁边的桌子上，并说道：\"真好听，能不能再唱一遍\"。",
                    "media": [
                        {
                            "type": "reference_image",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg"
                        },
                        {
                            "type": "reference_video",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260129/qigswt/wan-r2v-role2.mp4"
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
                    ]
                },
                "parameters": {
                    "resolution": "480P",
                    "ratio": "adaptive",
                    "duration": 5
                }
            }'
        - lang: curl
          label: 文生视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "wan3.0-video",
                "input": {
                    "prompt": "一只小猫在月光下的屋顶上奔跑，城市的霓虹灯在远处闪烁，电影级画质，流畅运镜。"
                },
                "parameters": {
                    "resolution": "480P",
                    "ratio": "adaptive",
                    "duration": 5
                }
            }'
        - lang: curl
          label: 首帧生视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "wan3.0-video",
                "input": {
                    "prompt": "一幅都市奇幻艺术的场景。一个充满动感的涂鸦艺术角色。一个由喷漆所画成的少年，正从一面混凝土墙上活过来。他一边用极快的语速演唱一首英文rap，一边摆着一个经典的、充满活力的说唱歌手姿势。场景设定在夜晚一个充满都市感的铁路桥下。灯光来自一盏孤零零的街灯，营造出电影般的氛围，充满高能量和惊人的细节。视频的音频部分完全由rap构成，没有其他对话或杂音。",
                    "media": [
                        {
                            "type": "first_frame",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
                        }
                    ]
                },
                "parameters": {
                    "resolution": "480P",
                    "ratio": "adaptive",
                    "duration": 5
                }
            }'
        - lang: curl
          label: 首尾帧生视频
          source: |-
            curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
                -H 'X-DashScope-Async: enable' \
                -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
                -H 'Content-Type: application/json' \
                -d '{
                "model": "wan3.0-video",
                "input": {
                    "prompt": "一个年轻女孩从微笑逐渐变为大笑，镜头缓缓推进，背景光线从冷色调渐变为暖色调。",
                    "media": [
                        {
                            "type": "first_frame",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250925/wpimhv/rap.png"
                        },
                        {
                            "type": "last_frame",
                            "url": "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260408/sjuytr/wan-r2v-object-girl.jpg"
                        }
                    ]
                },
                "parameters": {
                    "resolution": "480P",
                    "ratio": "adaptive",
                    "duration": 5
                }
            }'
components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      description: 千问AI平台 API Key。详见[获取 API Key](/api-reference/preparation/api-key)。
  schemas:
    Wan30VideoRequest:
      type: object
      required:
        - model
        - input
      properties:
        model:
          type: string
          description: 模型名称。固定值：`wan3.0-video`。
          enum:
            - wan3.0-video
          example: wan3.0-video
        input:
          type: object
          description: 输入的基本信息。`prompt` 和 `media` 必填其一。
          properties:
            prompt:
              type: string
              description: 文本提示词，用来描述期望生成的视频内容。和 `media` 必填其一。支持中英文，每个汉字/字母占一个字符，不超过 20000 个字符，超过部分会自动截断。在全能参考模式下，prompt 中可以用"图1""视频1"等指代 media 数组中对应顺序的媒体素材。
              maxLength: 20000
              example: 一只小猫在月光下的屋顶上奔跑，城市的霓虹灯在远处闪烁，电影级画质，流畅运镜。
            media:
              type: array
              description: 媒体素材数组，支持图像、视频、音频、文件和网页作为输入。和 `prompt` 必填其一。在参考生视频模式下，按照数组顺序定义 prompt 中素材引用的顺序（图和视频分别计数）。`reference_xx`/`file`/`link` 类型和 `first_frame`/`last_frame` 类型互斥，不能在同一请求中混用。
              items:
                $ref: "#/components/schemas/MediaItem"
        parameters:
          $ref: "#/components/schemas/Wan30VideoParameters"
    MediaItem:
      type: object
      required:
        - type
        - url
      properties:
        type:
          type: string
          description: 媒体素材类型。`reference_xx`/`file`/`link` 类型和 `first_frame`/`last_frame` 类型互斥。
          enum:
            - first_frame
            - last_frame
            - reference_image
            - reference_video
            - reference_audio
            - file
            - link
        url:
          type: string
          description: 媒体素材 URL 或 Base64 编码数据。支持公网 URL（HTTP/HTTPS）、OSS 临时 URL（`oss://dashscope-instant/...`）和 Base64 编码（`data:{MIME_type};base64,{data}`）。
    Wan30VideoParameters:
      type: object
      description: 视频处理参数。
      properties:
        resolution:
          type: string
          description: 生成视频的分辨率档位。
          enum:
            - 480P
            - 720P
            - 1080P
          default: 1080P
        ratio:
          type: string
          description: 生成视频的宽高比。`adaptive` 表示根据输入媒体比例和意图自动推荐合适的长宽比。
          enum:
            - adaptive
            - 16:9
            - 4:3
            - 1:1
            - 3:4
            - 9:16
          default: adaptive
        duration:
          type: integer
          description: 生成视频的时长，单位为秒。无视频输入时取值范围为 [2, 30] 的整数；有视频输入时输入视频总时长 + 输出视频时长不超过 30 秒。传 `-1` 时为智能时长模式，模型根据输入自动推荐合适时长。
          default: 5
        audio:
          type: boolean
          description: 输出视频是否包含音频。`true`（默认）：包含声音；`false`：不包含音轨。开关声音价格相同。
          default: true
        seed:
          type: integer
          description: 随机种子，用于复现生成结果。
          minimum: 0
          maximum: 2147483647
        watermark:
          type: boolean
          description: 是否添加水印标识。
          default: false
    AsyncTaskSubmitResponse:
      type: object
      description: 异步任务提交响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识，用于链路追踪和问题排查。
          example: 4909100c-7b5a-9f92-bfe5-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID，查询有效期 24 小时。配合 `GET /tasks/{task_id}` 使用。请勿重复创建任务，轮询获取即可。
              example: 0385dc79-5ff8-4d82-bcb6-xxxxxx
            task_status:
              type: string
              description: 初始任务状态，通常为 `PENDING`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
    Wan30VideoTaskStatusResponse:
      type: object
      description: 万相 3.0 视频生成任务状态响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识。可用于请求明细溯源和问题排查。
          example: 78c9b768-0285-996c-b682-xxxxxx
        output:
          type: object
          properties:
            task_id:
              type: string
              description: 任务 ID。
              example: 17ed7e50-00cf-4509-aea1-xxxxxx
            task_status:
              type: string
              description: 任务状态。流转：`PENDING`（排队中）-> `RUNNING`（处理中）-> `SUCCEEDED`（成功）/ `FAILED`（失败）。手动取消为 `CANCELED`，过期为 `UNKNOWN`。
              enum:
                - PENDING
                - RUNNING
                - SUCCEEDED
                - FAILED
                - CANCELED
                - UNKNOWN
            submit_time:
              type: string
              description: 任务提交时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-08-06 10:01:35.452
            scheduled_time:
              type: string
              description: 任务执行时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。
              example: 2026-08-06 10:01:35.507
            end_time:
              type: string
              description: 任务完成时间。格式为 YYYY-MM-DD HH:mm:ss.SSS。仅在 `SUCCEEDED` 或 `FAILED` 时返回。
              example: 2026-08-06 10:13:33.838
            orig_prompt:
              type: string
              description: 原始输入的提示词。
            video_url:
              type: string
              format: uri
              description: 生成视频的 URL 地址。仅在 `task_status` 为 `SUCCEEDED` 时返回。视频 URL 仅保留 24 小时，请及时保存。
              example: https://dashscope-result-bj.oss-cn-beijing.aliyuncs.com/xxx/video.mp4
            code:
              type: string
              description: 错误码。仅在 `task_status` 为 `FAILED` 时返回。
            message:
              type: string
              description: 错误信息。仅在 `task_status` 为 `FAILED` 时返回。
        usage:
          type: object
          description: 输出信息统计。只对成功的结果计数。
          properties:
            video_count:
              type: integer
              description: 生成视频的数量。固定为 1。
            duration:
              type: number
              description: 生成视频的时长，单位为秒。
            input_video_duration:
              type: number
              description: 输入视频的时长，单位为秒。无视频输入时为 0.0。
            output_video_duration:
              type: number
              description: 输出视频的时长，单位为秒。
            fps:
              type: integer
              description: 生成视频的帧率。
            SR:
              type: integer
              description: 生成视频的分辨率。示例值：720。
            ratio:
              type: string
              description: 生成视频的宽高比。示例值：16:9。
    DashScopeErrorResponse:
      type: object
      description: API 错误响应。
      properties:
        request_id:
          type: string
          description: 请求唯一标识，用于链路追踪和问题排查。
        code:
          type: string
          description: 错误码。
          example: InvalidApiKey
        message:
          type: string
          description: 错误描述信息。
          example: No API-key provided.
````
