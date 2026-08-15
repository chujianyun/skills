> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像生成模型

> 选择适合文生图、图片编辑等场景的模型。

## 从闭源模型迁移到千问AI平台？

如果你正在使用 Nano Banana、GPT Image、Midjourney 或 Seedream，可参考下表选择对应的千问AI平台模型。

| 能力档位  | 闭源模型代表                                 | 千问AI平台推荐                                |
| ----- | -------------------------------------- | --------------------------------------- |
| 高质量   | Nano Banana Pro、GPT Image、Seedream 4.0 | `qwen-image-3.0-pro`、`wan2.7-image-pro` |
| 平衡    | Imagen 4 Ultra、Midjourney v7           | `qwen-image-3.0`、`wan2.7-image`         |
| 快速低成本 | FLUX.2                                 | `z-image-turbo`                         |

## 文生图

推荐从 `qwen-image-3.0-pro` 开始——擅长复杂版面生成（报纸、分镜、菜单、试卷等）、10 像素小字精准渲染、多语言字体和摄影级细节，支持负向提示词排除不想要的元素，单次调用最多输出 6 张变体图。最高支持 2048×2048。

追求速度和成本时改用 `qwen-image-3.0`，能力相同、生成更快。

### 何时改用 `wan2.7-image-pro`

- 需要超过 2K 的分辨率——最高支持 4096×4096
- 需要品牌色精确控制
- 需要顺序模式单次输出最多 12 张角色一致的图片

### 何时改用 `z-image-turbo`

- 只需生图，不需要编辑
- 追求速度或成本——速度快 10 倍，价格约 1/5
- 写实人像和产品图

### 不确定选哪个？

[在模型体验中试用](https://platform.qianwenai.com/home/try-ai)——同样的提示词，直接对比效果。风格偏好因人而异。

## 图片编辑

推荐从 `qwen-image-3.0-pro` 开始——支持负向提示词，单次最多输出 6 张，且生图和编辑使用同一模型 ID。支持一至三张输入图片，可做多图融合。

### 何时改用 `wan2.7-image-pro`

- 需要更多参考图——最多支持 9 张输入图片
- 需要边界框交互式编辑
- 需要角色一致性多图生成

## 推荐模型

| 模型                   | 适用场景                          | 文生图 | 编辑 | 最大输出数      | 最大分辨率                         |
| -------------------- | ----------------------------- | --- | -- | ---------- | ----------------------------- |
| `qwen-image-3.0-pro` | 复杂版面生成、小字渲染、多语言字体、摄影级细节、负向提示词 | ✓   | ✓  | 6          | 2048×2048                     |
| `qwen-image-3.0`     | qwen-image-3.0-pro 的快速版       | ✓   | ✓  | 6          | 2048×2048                     |
| `wan2.7-image-pro`   | 4K 输出、品牌色、多图一致性、多图编辑          | ✓   | ✓  | 4（顺序模式 12） | 4096×4096（文生图）/ 2048×2048（编辑） |
| `wan2.7-image`       | 同等能力，生成更快，最高 2K               | ✓   | ✓  | 4（顺序模式 12） | 2048×2048                     |
| `z-image-turbo`      | 快速生图、低成本、写实人像                 | ✓   |    | 1          | 2048×2048                     |

## 全部模型

<AccordionGroup>
  <Accordion title="Qwen Image">
| 模型 ID                           | 文生图 | 编辑 | 最大输出数 | 最大分辨率     |
| ------------------------------- | --- | -- | ----- | --------- |
| `qwen-image-3.0-pro`            | ✓   | ✓  | 6     | 2048×2048 |
| `qwen-image-3.0`                | ✓   | ✓  | 6     | 2048×2048 |
| `qwen-image-2.0-pro`            | ✓   | ✓  | 6     | 2048×2048 |
| `qwen-image-2.0-pro-2026-06-22` | ✓   | ✓  | 6     | 2048×2048 |
| `qwen-image-2.0-pro-2026-04-22` | ✓   | ✓  | 6     | 2048×2048 |
| `qwen-image-2.0-pro-2026-03-03` | ✓   | ✓  | 6     | 2048×2048 |
| `qwen-image-2.0`                | ✓   | ✓  | 6     | 2048×2048 |
| `qwen-image-2.0-2026-03-03`     | ✓   | ✓  | 6     | 2048×2048 |
  </Accordion>

  <Accordion title="Wan">
| 模型 ID              | 文生图 | 编辑 | 最大输出数      | 最大分辨率                         |
| ------------------ | --- | -- | ---------- | ----------------------------- |
| `wan2.7-image-pro` | ✓   | ✓  | 4（顺序模式 12） | 4096×4096（文生图）/ 2048×2048（编辑） |
| `wan2.7-image`     | ✓   | ✓  | 4（顺序模式 12） | 2048×2048                     |
  </Accordion>

  <Accordion title="Z-Image">
| 模型 ID           | 文生图 | 编辑 | 最大输出数 | 最大分辨率     |
| --------------- | --- | -- | ----- | --------- |
| `z-image-turbo` | ✓   |    | 1     | 2048×2048 |
  </Accordion>

  <Accordion title="Vidu（生数科技）">
| 模型 ID                              | 文生图 | 参考图生图 | 编辑 | 最大输出数 | 最大分辨率 |
| ---------------------------------- | --- | ----- | -- | ----- | ----- |
| `vidu/vidu-image_reference2image`  | ✓   | ✓     | ✓  | 1     | 4K    |
| `vidu/viduq3-fast_reference2image` | ✓   | ✓     | ✓  | 1     | 4K    |
| `vidu/viduq2-pro_reference2image`  | ✓   | ✓     | ✓  | 1     | 4K    |
| `vidu/viduq2-fast_reference2image` | ✓   | ✓     | ✓  | 1     | 1K    |
  </Accordion>

  <Accordion title="Legacy">
    上一代模型。新项目推荐使用 Qwen Image 3.0 或 Wan 2.7。

    ### Wan

| 模型 ID                | 文生图 | 编辑 | 最大输出数 | 最大分辨率       |
| -------------------- | --- | -- | ----- | ----------- |
| `wan2.6-t2i`         | ✓   |    | 4     | \~1440×1440 |
| `wan2.6-image`       | ✓\* | ✓  | 4     | \~1440×1440 |
| `wan2.5-t2i-preview` | ✓   |    | 4     | \~1440×1440 |
| `wan2.5-i2i-preview` |     | ✓  | 4     | 1280×1280   |
| `wan2.2-t2i-plus`    | ✓   |    | 4     | \~1440×1440 |
| `wan2.2-t2i-flash`   | ✓   |    | 4     | \~1440×1440 |
| `wan2.1-t2i-plus`    | ✓   |    | 4     | \~1440×1440 |
| `wan2.1-t2i-turbo`   | ✓   |    | 4     | \~1440×1440 |
| `wanx2.1-t2i-plus`   | ✓   |    | 4     | \~1440×1440 |
| `wanx2.1-t2i-turbo`  | ✓   |    | 4     | \~1440×1440 |
| `wanx2.0-t2i-turbo`  | ✓   |    | 4     | \~1440×1440 |
| `wanx2.1-imageedit`  |     | ✓  | 4     | \~1440×1440 |
| `wanx-v1`            | ✓   |    | 4     | \~1440×1440 |

    \* 需设置 `enable_interleave=true` 和 `stream=true`。详见[文生图指南](/developer-guides/image-generation/text-to-image)。

    ### Qwen Image

| 模型 ID                             | 文生图 | 编辑 | 最大输出数 | 最大分辨率     |
| --------------------------------- | --- | -- | ----- | --------- |
| `qwen-image-max`                  | ✓   |    | 1     | 1664×928  |
| `qwen-image-max-2025-12-30`       | ✓   |    | 1     | 1664×928  |
| `qwen-image-plus`                 | ✓   |    | 1     | 1664×928  |
| `qwen-image-plus-2026-01-09`      | ✓   |    | 1     | 1664×928  |
| `qwen-image`                      | ✓   |    | 1     | 1664×928  |
| `qwen-image-edit-max`             |     | ✓  | 6     | 2048×2048 |
| `qwen-image-edit-max-2026-01-16`  |     | ✓  | 6     | 2048×2048 |
| `qwen-image-edit-plus`            |     | ✓  | 6     | 2048×2048 |
| `qwen-image-edit-plus-2025-12-15` |     | ✓  | 6     | 2048×2048 |
| `qwen-image-edit-plus-2025-10-30` |     | ✓  | 6     | 2048×2048 |
| `qwen-image-edit`                 |     | ✓  | 1     | 1024×1024 |
  </Accordion>

  <Accordion title="图像处理工具">
    非生成型图像处理 API。

| 模型 ID                           | 功能                  |
| ------------------------------- | ------------------- |
| `qwen-mt-image`                 | 图像翻译（自动识别语言并翻译图中文字） |
| `wanx-background-generation-v2` | 商品图背景生成             |
| `wanx-sketch-to-image-lite`     | 涂鸦生成图片              |
| `wanx-style-repaint-v1`         | 人物风格重绘              |
| `wanx-x-painting`               | 图像局部重绘              |
| `image-out-painting`            | 画面扩展（外绘）            |
| `image-instance-segmentation`   | 人物实例分割              |
  </Accordion>
</AccordionGroup>

---

## 了解更多

<CardGroup cols={2}>
  <Card title="图片生成指南" icon="PhotoCodeOutlined" href="/developer-guides/image-generation/text-to-image">
    了解如何通过 API 生成图片。
  </Card>

  <Card title="免费试用" icon="RocketOutlined" href="https://platform.qianwenai.com/home/try-ai">
    在浏览器中试用模型，无需 API Key。
  </Card>
</CardGroup>
