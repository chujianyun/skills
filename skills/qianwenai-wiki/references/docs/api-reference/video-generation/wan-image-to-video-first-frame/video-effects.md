> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 万相-视频特效列表

> 万相视频特效模板完整列表，包含首帧和首尾帧模型支持的所有特效模板参数值、支持模型及输入图像建议。

万相提供视频特效功能，**无需输入提示词，只需指定特效模板**，即可轻松生成预设的动态效果。

视频特效仅支持在[图生视频-基于首帧](/api-reference/video-generation/wan-image-to-video-first-frame/create-task)和[图生视频-基于首尾帧](/api-reference/video-generation/wan-image-to-video-first-last-frames/create-task)中使用。

## 使用方法

视频特效与图生视频的使用方式不同，请遵循以下规则：

- **仅需一张首帧图像**：无论选用的是"基于首帧"还是"基于首尾帧"的模型，**只需要提供一张首帧图像**。
- **无需任何提示词**：在特效模式下，模型会忽略 prompt 字段。建议不传入该参数，专注于选择视觉效果。
- **选择一个模板**：通过 `template` 参数从特效列表中选择一个动态效果。模型将根据模板生成指定的动态效果。

<Note>
  不同的模型支持的特效模板有所不同。请务必参考[特效列表-首帧生视频](#特效列表-首帧生视频)和[特效列表-首尾帧生视频](#特效列表-首尾帧生视频)，确保所使用的 template 值与模型匹配。
</Note>

### 示例代码

<Tabs>
  <Tab title="图生视频-基于首帧">
    **首帧特效**：对首帧图像生成特效视频。

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/video-generation/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wanx2.1-i2v-turbo",
      "input": {
        "img_url": "https://cdn.translate.alibaba.com/r/wanx-demo-1.png",
        "template": "flying"
      },
      "parameters": {
        "resolution": "720P"
      }
    }'
    ```

    完整代码请参见[图生视频-基于首帧](/api-reference/video-generation/wan-image-to-video-first-frame/create-task)。
  </Tab>

  <Tab title="图生视频-基于首尾帧">
    **首尾帧特效**：只需提供一张首帧图像，无需尾帧图像，即可生成视频特效。

    - 若同时提供 first\_frame\_url、last\_frame\_url、template，将忽略 last\_frame\_url。
    - 若仅提供 last\_frame\_url、template，请求将报错。

    ```bash
    curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2video/video-synthesis' \
      -H 'X-DashScope-Async: enable' \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H 'Content-Type: application/json' \
      -d '{
      "model": "wanx2.1-kf2v-plus",
      "input": {
        "first_frame_url": "https://ty-yuanfang.oss-cn-hangzhou.aliyuncs.com/lizhengjia.lzj/tmp/11.png",
        "template": "hanfu-1"
      },
      "parameters": {
        "resolution": "720P",
        "prompt_extend": true
      }
    }'
    ```

    完整代码请参见[图生视频-基于首尾帧](/api-reference/video-generation/wan-image-to-video-first-last-frames/create-task)。
  </Tab>
</Tabs>

## 特效列表-首帧生视频

视频效果取决于模板和输入图片。为获得最佳效果，请先预览模板示例，并参考其"输入图像建议"，再使用您自己的图片进行尝试。

### 通用特效

| 特效名称  | `template` 参数值 | 支持模型                                | 输入图像建议                       |
| :---: | :------------: | :---------------------------------: | :--------------------------- |
| 解压捏捏  | `squish`       | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持任意主体。建议使用主体突出，与背景有明显区分度的图片 |
| 转圈圈   | `rotation`     | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持任意主体。建议使用主体突出，与背景有明显区分度的图片 |
| 戳戳乐   | `poke`         | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持任意主体。建议使用主体突出，与背景有明显区分度的图片 |
| 气球膨胀  | `inflate`      | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持任意主体。建议使用主体突出，与背景有明显区分度的图片 |
| 分子扩散  | `dissolve`     | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持任意主体。建议使用主体突出，与背景有明显区分度的图片 |
| 热浪融化  | `melt`         | wanx2.1-i2v-plus                    | 支持任意主体。建议使用主体突出，与背景有明显区分度的图片 |
| 冰淇淋星球 | `icecream`     | wanx2.1-i2v-plus                    | 支持任意主体。建议使用主体突出，与背景有明显区分度的图片 |

### 单人特效

| 特效名称 | `template` 参数值 | 支持模型                                | 输入图像建议                |
| :--: | :------------: | :---------------------------------: | :-------------------- |
| 时光木马 | `carousel`     | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持单人照片。建议使用半身至全身的正面照片 |
| 爱你哟  | `singleheart`  | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持单人照片。建议使用半身至全身的正面照片 |
| 摇摆时刻 | `dance1`       | wanx2.1-i2v-plus                    | 支持单人照片。建议使用半身至全身的正面照片 |
| 头号甩舞 | `dance2`       | wanx2.1-i2v-plus                    | 支持单人照片。建议使用全身正面照片     |
| 星摇时刻 | `dance3`       | wanx2.1-i2v-plus                    | 支持单人照片。建议使用全身正面照片     |
| 指感节奏 | `dance4`       | wanx2.1-i2v-plus                    | 支持单人照片。建议使用半身至全身的正面照片 |
| 舞动开关 | `dance5`       | wanx2.1-i2v-plus                    | 支持单人照片。建议使用半身至全身的正面照片 |
| 人鱼觉醒 | `mermaid`      | wanx2.1-i2v-plus                    | 支持单人照片。建议使用半身的正面照片    |
| 学术加冕 | `graduation`   | wanx2.1-i2v-plus                    | 支持单人照片。建议使用半身至全身的正面照片 |
| 巨兽追袭 | `dragon`       | wanx2.1-i2v-plus                    | 支持单人照片。建议使用半身至全身的正面照片 |
| 财从天降 | `money`        | wanx2.1-i2v-plus                    | 支持单人照片。建议使用半身至全身的正面照片 |
| 水母之约 | `jellyfish`    | wanx2.1-i2v-plus                    | 支持单人照片。建议使用半身至全身的正面照片 |
| 瞳孔穿越 | `pupil`        | wanx2.1-i2v-plus                    | 支持单人照片。建议使用半身至全身的正面照片 |

### 单人或动物特效

| 特效名称 | `template` 参数值 | 支持模型                                | 输入图像建议                          |
| :--: | :------------: | :---------------------------------: | :------------------------------ |
| 魔法悬浮 | `flying`       | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持单人或动物照片。建议使用全身的正面照片           |
| 赠人玫瑰 | `rose`         | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持单人或动物照片。建议使用半身至全身的正面照片，避免露出手部 |
| 闪亮玫瑰 | `crystalrose`  | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持单人或动物照片。建议使用半身至全身的正面照片，避免露出手部 |

### 双人特效

| 特效名称 | `template` 参数值 | 支持模型                                | 输入图像建议                               |
| :--: | :------------: | :---------------------------------: | :----------------------------------- |
| 爱的抱抱 | `hug`          | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持双人照片。建议两人正面看向镜头或相对站立（面对面），可为半身或全身照 |
| 唇齿相依 | `frenchkiss`   | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持双人照片。建议两人正面看向镜头或相对站立（面对面），可为半身或全身照 |
| 双倍心动 | `coupleheart`  | wanx2.1-i2v-plus, wanx2.1-i2v-turbo | 支持双人照片。建议两人正面看向镜头或相对站立（面对面），可为半身或全身照 |

## 特效列表-首尾帧生视频

视频效果取决于模板和输入图片。为获得最佳效果，请先预览模板示例，并参考其"输入图像建议"，再使用您自己的图片进行尝试。

<Note>
  首尾帧生视频的特效是基于首尾帧模型训练，但实际使用时**仅需传入首帧图像**，无需提供尾帧，效果等同于首帧生成视频。具体请参见[使用方法](#使用方法)。
</Note>

### 单人特效

| 特效名称 | `template` 参数值 | 支持模型              | 输入图像建议                |
| :--: | :------------: | :---------------: | :-------------------- |
| 唐韵翩然 | `hanfu-1`      | wanx2.1-kf2v-plus | 支持单人照片。建议使用半身至全身的正面照片 |
| 机甲变身 | `solaron`      | wanx2.1-kf2v-plus | 支持单人照片。建议使用半身至全身的正面照片 |
| 闪耀封面 | `magazine`     | wanx2.1-kf2v-plus | 支持单人照片。建议使用半身至全身的正面照片 |
| 机械觉醒 | `mech1`        | wanx2.1-kf2v-plus | 支持单人照片。建议使用半身至全身的正面照片 |
| 赛博登场 | `mech2`        | wanx2.1-kf2v-plus | 支持单人照片。建议使用半身至全身的正面照片 |

## API 参考

- API 参数说明和完整代码示例，请参见[图生视频-基于首帧](/api-reference/video-generation/wan-image-to-video-first-frame/create-task)、[图生视频-基于首尾帧](/api-reference/video-generation/wan-image-to-video-first-last-frames/create-task)。
