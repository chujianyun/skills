> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 视频生成模型

> 选择文生视频、图生视频、角色动画等场景的模型。

## 从闭源模型迁移到千问AI平台？

如果你正在使用 Sora、Veo、Kling 或 Runway，可参考下表选择对应的千问AI平台模型。

| 模型能力                | 闭源模型代表                    | 千问AI平台推荐                                                 |
| ------------------- | ------------------------- | -------------------------------------------------------- |
| 文生视频（t2v）、图生视频（i2v） | Sora 2、Veo 3.1、Kling 3.0  | `happyhorse-1.1-t2v`、`happyhorse-1.1-i2v`、`wan3.0-video` |
| 参考生视频（r2v）          | Seedance 2.0、Runway Gen-4 | `happyhorse-1.1-r2v`、`wan3.0-video`                      |

## 文生视频

通过文本提示词生成有声视频，推荐使用 `happyhorse-1.1-t2v`。支持 1080P 分辨率，单片段最长 15 秒。

Wan 系列推荐使用 `wan3.0-video`，支持更长视频（最长 30 秒）、自适应长宽比、智能时长、声音开关、参考音频等能力。支持 480P/720P/1080P 分辨率。

## 图生视频

将静态图片转化为动态视频。首帧生视频推荐使用 `happyhorse-1.1-i2v`，Wan 系列推荐使用 `wan3.0-video`，支持首帧和首尾帧生视频。

### 首尾帧生视频，构建长视频

使用首尾帧模型（推荐 `wan3.0-video`）可以串联多个片段：将上一片段的末帧作为下一片段的首帧，实现无缝过渡，适用于叙事、产品演示或教程等场景。

## 参考生视频

基于参考图片在不同场景中保持角色一致性，推荐使用 `happyhorse-1.1-r2v`。Wan 系列推荐使用 `wan3.0-video`，支持多参考图片、视频、音频的全能参考能力，还支持传入文件（docx、ppt、pdf 等）和网页链接作为参考。

## 视频编辑

通过文本指令对已有视频进行风格转换、元素替换等编辑操作，推荐使用 `happyhorse-1.0-video-edit`。如果需要进行特效复刻、运镜复刻，推荐使用 `wan2.7-videoedit`。

## 角色动画

将参考视频中的动作迁移到静态人物图片上 → `wan2.2-animate-move`。将视频中的人物替换为图片中的人物 → `wan2.2-animate-mix`。

## 推荐模型

| 模型                          | 适用场景                   | 最大分辨率             | 最大时长   |
| --------------------------- | ---------------------- | ----------------- | ------ |
| `wan3.0-video`              | 文生视频、首帧/首尾帧生视频、全能参考生视频 | 480P, 720P, 1080P | 2-30 秒 |
| `happyhorse-1.1-t2v`        | 文生视频                   | 480P, 720P, 1080P | 3-15 秒 |
| `happyhorse-1.1-i2v`        | 首帧生视频                  | 480P, 720P, 1080P | 3-15 秒 |
| `happyhorse-1.1-r2v`        | 参考图像生视频                | 480P, 720P, 1080P | 3-15 秒 |
| `happyhorse-1.0-video-edit` | 视频编辑                   | 720P, 1080P       | 3-15 秒 |
| `wan2.7-videoedit`          | 视频编辑、特效复刻、运镜复刻         | 720P, 1080P       | 2-10 秒 |
| `wan2.2-animate-move`       | 动作迁移到静态人物              | 720P              | 2-30 秒 |
| `wan2.2-animate-mix`        | 视频中替换人物                | 720P              | 2-30 秒 |

## 全部模型

<AccordionGroup>
  <Accordion title="HappyHorse">
| 模型                          | 能力     | 特性                               | 输出                     |
| --------------------------- | ------ | -------------------------------- | ---------------------- |
| `happyhorse-1.1-t2v`        | 文生视频   | 音频、画面比例控制（16:9/9:16/1:1/4:3/3:4） | 720P、1080P。3-15 秒。MP4  |
| `happyhorse-1.1-i2v`        | 图生视频   | 音频、首帧驱动                          | 720P、1080P。3-15 秒。MP4  |
| `happyhorse-1.1-r2v`        | 参考视频生成 | 音频、1-9 张参考图像、多角色融合               | 720P、1080P。3-15 秒。MP4  |
| `happyhorse-1.0-t2v`        | 文生视频   | 音频、画面比例控制（16:9/9:16/1:1/4:3/3:4） | 720P、1080P。3-15 秒。MP4  |
| `happyhorse-1.0-i2v`        | 图生视频   | 音频、首帧驱动                          | 720P、1080P。3-15 秒。MP4  |
| `happyhorse-1.0-r2v`        | 参考视频生成 | 音频、1-9 张参考图像、多角色融合               | 720P、1080P。3-15 秒。MP4  |
| `happyhorse-1.0-video-edit` | 视频编辑   | 风格变换、局部替换、音频（自动/保留原始）            | 720P、1080P。最长 15 秒。MP4 |
  </Accordion>

  <Accordion title="Wan 3.0（邀测中）">
| 模型             | 能力               | 特性                                     | 输出                                  |
| -------------- | ---------------- | -------------------------------------- | ----------------------------------- |
| `wan3.0-video` | 全能参考（All-in-One） | 文生视频、首帧/首尾帧、全能参考、有声视频、声音开关、智能时长、自适应长宽比 | 480P, 720P, 1080P。2-30 秒。30 fps，MP4 |
  </Accordion>

  <Accordion title="Wan 2.7">
| 模型                      | 能力         | 特性                        | 输出                            |
| ----------------------- | ---------- | ------------------------- | ----------------------------- |
| `wan2.7-t2v`            | 文生视频       | 音频同步、多镜头叙事、画面比例控制         | 720P、1080P。2-15 秒。30 fps，MP4  |
| `wan2.7-t2v-2026-06-12` | 文生视频（快照）   | 同 `wan2.7-t2v`            | 720P、1080P。2-15 秒。30 fps，MP4  |
| `wan2.7-t2v-2026-04-25` | 文生视频（快照）   | 同 `wan2.7-t2v`            | 720P、1080P。2-15 秒。30 fps，MP4  |
| `wan2.7-i2v`            | 图生视频       | 音频同步、首帧、首尾帧、视频续写          | 720P、1080P。2-15 秒。30 fps，MP4  |
| `wan2.7-i2v-2026-04-25` | 图生视频（快照）   | 同 `wan2.7-i2v`            | 720P、1080P。2-15 秒。30 fps，MP4  |
| `wan2.7-r2v`            | 参考视频生成     | 音频同步、多角色、语音克隆、首帧控制        | 720P、1080P。2-15 秒。30 fps，MP4  |
| `wan2.7-r2v-2026-06-12` | 参考视频生成（快照） | 同 `wan2.7-r2v`            | 720P、1080P。2-15 秒。30 fps，MP4  |
| `wan2.7-videoedit`      | 视频编辑       | 音频（自动生成/保留原始）、参考图片、画面比例控制 | 720P、1080P。最长 10 秒。30 fps，MP4 |
  </Accordion>

  <Accordion title="角色动画">
| 模型                             | 能力                  | 特性                       | 输出                        |
| ------------------------------ | ------------------- | ------------------------ | ------------------------- |
| `wan2.2-animate-move`          | 动作迁移                | `wan-std` / `wan-pro` 模式 | 720P。2-30 秒。15/25 fps。MP4 |
| `wan2.2-animate-mix`           | 视频换脸                | `wan-std` / `wan-pro` 模式 | 720P。2-30 秒。15/25 fps。MP4 |
| `animate-anyone-gen2`          | 动作迁移（AnimateAnyone） | 需先用预处理模型提取动作模板           | 720P。MP4                  |
| `animate-anyone-detect-gen2`   | 图片质量检测（预处理）         | —                        | —                         |
| `animate-anyone-template-gen2` | 动作模板提取（预处理）         | —                        | —                         |
| `wan2.2-s2v-detect`            | 数字人图像检测（预处理）        | 检查图像是否满足数字人生成要求          | —                         |
  </Accordion>

  <Accordion title="旧版模型">
    上一代模型。新项目建议使用 Wan 2.7。

    ### Wan 2.6

| 模型                 | 能力     | 特性          | 输出                           |
| ------------------ | ------ | ----------- | ---------------------------- |
| `wan2.6-t2v`       | 文生视频   | 音频同步、多镜头叙事  | 720P、1080P。2-15 秒。30 fps，MP4 |
| `wan2.6-i2v`       | 图生视频   | 音频同步、多镜头叙事  | 720P、1080P。2-15 秒。30 fps，MP4 |
| `wan2.6-i2v-flash` | 图生视频   | 音频、多镜头、快速生成 | 720P、1080P。2-15 秒。30 fps，MP4 |
| `wan2.6-r2v`       | 参考视频生成 | 音频同步、多角色、叙事 | 720P、1080P。2-10 秒。30 fps，MP4 |
| `wan2.6-r2v-flash` | 参考视频生成 | 多角色、快速生成    | 720P、1080P。2-10 秒。30 fps，MP4 |

    ### Wan 2.5

| 模型                   | 能力   | 特性   | 输出                                  |
| -------------------- | ---- | ---- | ----------------------------------- |
| `wan2.5-t2v-preview` | 文生视频 | 音频同步 | 480P、720P、1080P。5 秒、10 秒。30 fps，MP4 |
| `wan2.5-i2v-preview` | 图生视频 | 音频同步 | 480P、720P、1080P。5 秒、10 秒。30 fps，MP4 |

    ### Wan 2.2

| 模型                  | 能力    | 特性                | 输出                             |
| ------------------- | ----- | ----------------- | ------------------------------ |
| `wan2.2-t2v-plus`   | 文生视频  | 无音频               | 480P、1080P。5 秒。30 fps，MP4      |
| `wan2.2-i2v-plus`   | 图生视频  | 无音频               | 480P、1080P。5 秒。30 fps，MP4      |
| `wan2.2-i2v-flash`  | 图生视频  | 无音频，速度比 2.1 快 50% | 480P、720P、1080P。5 秒。30 fps，MP4 |
| `wan2.2-kf2v-flash` | 首尾帧生成 | 无音频               | 480P、720P、1080P。5 秒。30 fps，MP4 |

    ### Wan 2.1

| 模型                 | 能力    | 特性  | 输出                         |
| ------------------ | ----- | --- | -------------------------- |
| `wan2.1-t2v-plus`  | 文生视频  | 无音频 | 720P。5 秒。30 fps，MP4        |
| `wan2.1-t2v-turbo` | 文生视频  | 无音频 | 480P、720P。5 秒。30 fps，MP4   |
| `wan2.1-i2v-plus`  | 图生视频  | 无音频 | 720P。5 秒。30 fps，MP4        |
| `wan2.1-i2v-turbo` | 图生视频  | 无音频 | 480P、720P。3-5 秒。30 fps，MP4 |
| `wan2.1-kf2v-plus` | 首尾帧生成 | 无音频 | 720P。5 秒。30 fps，MP4        |
| `wan2.1-vace-plus` | 视频编辑  | 无音频 | 720P。最长 5 秒。30 fps，MP4     |

    ### Wan 2.1（wanx）

| 模型                  | 能力       | 特性  | 输出                     |
| ------------------- | -------- | --- | ---------------------- |
| `wanx2.1-t2v-plus`  | 文生视频     | 无音频 | 720P。5 秒。30 fps，MP4    |
| `wanx2.1-t2v-turbo` | 文生视频     | 无音频 | 720P。5 秒。30 fps，MP4    |
| `wanx2.1-i2v-plus`  | 图生视频（首帧） | 无音频 | 720P。5 秒。30 fps，MP4    |
| `wanx2.1-i2v-turbo` | 图生视频（首帧） | 无音频 | 720P。5 秒。30 fps，MP4    |
| `wanx2.1-kf2v-plus` | 首尾帧生成    | 无音频 | 720P。5 秒。30 fps，MP4    |
| `wanx2.1-vace-plus` | 视频编辑     | 无音频 | 720P。最长 5 秒。30 fps，MP4 |
  </Accordion>
</AccordionGroup>

<AccordionGroup>
  <Accordion title="第三方（PixVerse / 可灵 / Vidu）">
    通过同一 API 可用的第三方视频生成模型。

    ### PixVerse（爱诗科技）

| 模型                                | 能力        | 音频 | 最大分辨率   |
| --------------------------------- | --------- | -- | ------- |
| `pixverse/pixverse-c1-t2v`        | 文生视频      | 支持 | 360P    |
| `pixverse/pixverse-v6-t2v`        | 文生视频      | 支持 | 360P    |
| `pixverse/pixverse-v5.6-t2v`      | 文生视频      | 支持 | 360P    |
| `pixverse/pixverse-c1-it2v`       | 图生视频（首帧）  | 支持 | 360P    |
| `pixverse/pixverse-v6-it2v`       | 图生视频（首帧）  | 支持 | 360P    |
| `pixverse/pixverse-v5.6-it2v`     | 图生视频（首帧）  | 支持 | 360P    |
| `pixverse/pixverse-c1-kf2v`       | 图生视频（首尾帧） | 支持 | 360P    |
| `pixverse/pixverse-v6-kf2v`       | 图生视频（首尾帧） | 支持 | 360P    |
| `pixverse/pixverse-v5.6-kf2v`     | 图生视频（首尾帧） | 支持 | 360P    |
| `pixverse/pixverse-c1-r2v`        | 参考生视频     | 支持 | 360P    |
| `pixverse/pixverse-v5.6-r2v`      | 参考生视频     | 支持 | 360P    |
| `pixverse/pixverse-lipsync`       | 视频对口型     | —  | 与输入视频一致 |
| `pixverse/pixverse-motioncontrol` | 视频动作模仿    | —  | 720P    |
| `pixverse/pixverse-upscale`       | 视频超清      | —  | 4K      |

    ### 可灵（快手）

| 模型                                     | 能力                | 音频 | 最大分辨率 |
| -------------------------------------- | ----------------- | -- | ----- |
| `kling/kling-v3-omni-video-generation` | 文生/图生/首尾帧/参考/视频编辑 | —  | 720P  |
| `kling/kling-v3-video-generation`      | 文生/图生/首尾帧         | —  | 720P  |

    ### Vidu（生数科技）

| 模型                                  | 能力            | 音频   | 最大分辨率 |
| ----------------------------------- | ------------- | ---- | ----- |
| `vidu/viduq3-pro_text2video`        | 文生视频          | 支持   | 540P  |
| `vidu/viduq3-turbo_text2video`      | 文生视频（快速）      | 支持   | 540P  |
| `vidu/viduq2_text2video`            | 文生视频          | —    | 540P  |
| `vidu/viduq3-pro-fast_img2video`    | 图生视频（首帧，旗舰极速） | 支持   | 1080P |
| `vidu/viduq3-pro_img2video`         | 图生视频（首帧）      | 支持   | 540P  |
| `vidu/viduq3-turbo_img2video`       | 图生视频（首帧，快速）   | 支持   | 540P  |
| `vidu/viduq2-pro_img2video`         | 图生视频（首帧）      | —    | 540P  |
| `vidu/viduq2-turbo_img2video`       | 图生视频（首帧，快速）   | —    | 540P  |
| `vidu/viduq3-pro_start-end2video`   | 图生视频（首尾帧）     | 支持   | 540P  |
| `vidu/viduq3-turbo_start-end2video` | 图生视频（首尾帧，快速）  | 支持   | 540P  |
| `vidu/viduq2-pro_start-end2video`   | 图生视频（首尾帧）     | —    | 540P  |
| `vidu/viduq2-turbo_start-end2video` | 图生视频（首尾帧，快速）  | —    | 540P  |
| `vidu/viduq3-ad_reference2video`    | 参考生视频（广告）     | 支持   | 1080P |
| `vidu/viduq3-drama_reference2video` | 参考生视频（精品剧）    | 默认有声 | 1080P |
| `vidu/viduq2-pro_reference2video`   | 参考生视频         | —    | 540P  |
| `vidu/viduq2_reference2video`       | 参考生视频         | —    | 540P  |
  </Accordion>
</AccordionGroup>

---

## 了解更多

<CardGroup cols={2}>
  <Card title="文生视频" icon="MovieOutlined" href="/developer-guides/video-generation/text-to-video">
    通过文本提示词生成视频。
  </Card>

  <Card title="图生视频：首帧驱动" icon="PhotoVideoOutlined" href="/developer-guides/video-generation/image-to-video">
    从单张图片生成动态视频。
  </Card>

  <Card title="首尾帧生成" icon="PhotoVideoOutlined" href="/developer-guides/video-generation/image-to-video-first-last">
    在两帧之间生成过渡动画。
  </Card>

  <Card title="参考视频生成" icon="UserCodeOutlined" href="/developer-guides/video-generation/reference-video">
    生成角色一致的视频。
  </Card>

  <Card title="视频编辑" icon="VideoPlusOutlined" href="/developer-guides/video-generation/video-editing">
    编辑、续写和重绘视频。
  </Card>
</CardGroup>
