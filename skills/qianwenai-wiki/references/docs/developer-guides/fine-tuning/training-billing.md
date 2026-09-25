> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 微调训练计费

> 千问AI平台模型微调的训练计费规则、公式与各模型训练单价。

微调训练按训练消耗的 Token 数计费。不同模型类型的计费公式和单价不同：文本生成与视觉理解模型按训练数据 Token 计费；图像与视频生成模型按训练步数或视频时长折算的 Token 计费。

创建微调任务时，控制台底部显示预估训练费用，点击**计算详情**可查看训练 Token 总数、循环次数和训练单价明细。

## 文本生成模型

按训练 Token 计费：

```
训练费用 = 训练数据 Token 总数 × 循环次数 × 训练单价（最小计费单位：1 Token）
```

| 模型服务                         | 模型代码                           | 训练单价              |
| ---------------------------- | ------------------------------ | ----------------- |
| Qwen3.6-Flash-2026-04-16     | qwen3.6-flash-2026-04-16       | ¥0.05 / 千 Token   |
| Qwen3.5-27B                  | qwen3.5-27b                    | ¥0.05 / 千 Token   |
| Qwen3.5-9B                   | qwen3.5-9b                     | ¥0.02 / 千 Token   |
| Qwen3.5-Flash-2026-02-23     | qwen3.5-flash-2026-02-23       | ¥0.05 / 千 Token   |
| Qwen3-32B                    | qwen3-32b                      | ¥0.04 / 千 Token   |
| Qwen3-30B-A3B-Instruct-2507  | qwen3-30b-a3b-instruct-2507    | ¥0.03 / 千 Token   |
| Qwen3-14B                    | qwen3-14b                      | ¥0.03 / 千 Token   |
| Qwen3-8B                     | qwen3-8b                       | ¥0.006 / 千 Token  |
| Qwen3-4B-Instruct-2507       | qwen3-4b-instruct-2507         | ¥0.006 / 千 Token  |
| Qwen3-1.7B                   | qwen3-1.7b                     | ¥0.0045 / 千 Token |
| Qwen3-0.6B                   | qwen3-0.6b                     | ¥0.003 / 千 Token  |
| Qwen2.5-72B-Instruct         | qwen2.5-72b-instruct           | ¥0.15 / 千 Token   |
| Qwen2.5-32B-Instruct         | qwen2.5-32b-instruct           | ¥0.03 / 千 Token   |
| Qwen2.5-14B-Instruct         | qwen2.5-14b-instruct           | ¥0.03 / 千 Token   |
| Qwen2.5-7B-Instruct          | qwen2.5-7b-instruct            | ¥0.006 / 千 Token  |
| 千问-Plus-Character-2025-11-06 | qwen-plus-character-2025-11-06 | ¥0.15 / 千 Token   |

## 视觉理解模型

视觉理解（VL）模型与文本生成模型共用同一计费公式：

```
训练费用 = 训练数据 Token 总数 × 循环次数 × 训练单价（最小计费单位：1 Token）
```

| 模型服务                    | 模型代码                    | 训练单价             |
| ----------------------- | ----------------------- | ---------------- |
| Qwen3-VL-8B-Instruct    | qwen3-vl-8b-instruct    | ¥0.012 / 千 Token |
| Qwen3-VL-8B-Thinking    | qwen3-vl-8b-thinking    | ¥0.012 / 千 Token |
| Qwen3-VL-4B-Instruct    | qwen3-vl-4b-instruct    | ¥0.006 / 千 Token |
| Qwen2.5-VL-72B-Instruct | qwen2.5-vl-72b-instruct | ¥0.05 / 千 Token  |
| Qwen2.5-VL-32B-Instruct | qwen2.5-vl-32b-instruct | ¥0.02 / 千 Token  |
| Qwen2.5-VL-7B-Instruct  | qwen2.5-vl-7b-instruct  | ¥0.01 / 千 Token  |

<Note>
  VL 模型的图像/视频 Token 按以下公式估算，用于估算训练数据 Token 数：

  ```
  图像 Token = h_bar × w_bar / token_pixels + 2
  ```

  - `h_bar`、`w_bar`：缩放后的图像长宽（模型预处理将图像缩至特定像素上限内，上限与 `max_pixels` 和 `vl_high_resolution_images` 参数有关）
  - `token_pixels`（每个视觉 Token 对应的像素值）：
    - Qwen3-VL 系列：每个 Token 对应 32×32 像素
    - Qwen2.5-VL 系列：每个 Token 对应 28×28 像素
  - 视频文件先抽帧，再计算所有视频帧的总 Token 数
</Note>

## 图像生成模型

Wan 系列图像生成模型按训练 Token 计费：

```
训练费用 = 训练 Token 总量 × 训练单价（计费单位：每千 Token）
训练 Token 总量 ≈ max_steps × Lstep
```

- `max_steps`：最大训练步数（创建微调任务时配置的超参数）
- `Lstep`：每步的 Token 消耗量，近似等于 `Lmax`，由 `max_token_length` 和 `generation_type` 共同决定。

| generation\_type | max\_token\_length | Lmax    |
| ---------------- | ------------------ | ------- |
| t2i（文生图）         | 1k                 | 128,000 |
| t2i（文生图）         | 2k                 | 232,200 |
| i2i（图生图）         | 1k                 | 232,200 |
| i2i（图生图）         | 2k                 | 320,000 |

| 模型名称             | 训练单价            |
| ---------------- | --------------- |
| wan2.7-image-pro | ¥0.08 / 千 Token |
| wan2.7-image     | ¥0.08 / 千 Token |

计费示例：使用 wan2.7-image-pro 进行 t2i 微调，`max_steps = 200`，`max_token_length = "1k"`，训练单价 ¥0.08 / 千 Token：

- 查表得 `Lmax = 128,000`（t2i，1k），`Lstep ≈ Lmax = 128,000`
- 训练 Token 总量 ≈ 200 × 128,000 = 25,600,000 = 25,600 千 Token
- 训练费用 ≈ 25,600 × 0.08 = ¥2,048

## 视频生成模型

Wan 系列视频生成模型按训练 Token 计费：

```
训练费用 = 训练 Token 总量 × 训练单价（计费单位：每千 Token）
训练 Token 总量 = ( Σ 视频计费时长 ) × ( max_pixels / 1024 ) × n_epochs
```

- `Σ 视频计费时长`：训练集中所有视频的计费时长之和（秒）
- `max_pixels`：视频最大像素数（创建微调任务时配置的超参数）
- `n_epochs`：循环次数（创建微调任务时配置的超参数）
- 单个视频计费时长：先将原始时长（秒）四舍五入取整，再按模型上限取值。
  - wan2.5 模型：计费时长 = min(10, 四舍五入后时长)，单条最多按 10 秒。
  - wan2.2 模型：计费时长 = min(5, 四舍五入后时长)，单条最多按 5 秒。

| 模型名称                     | 训练单价            |
| ------------------------ | --------------- |
| wan2.2-i2v-flash（基于首帧）   | ¥0.06 / 千 Token |
| wan2.5-i2v-preview（基于首帧） | ¥0.32 / 千 Token |
| wan2.2-kf2v-flash（基于首尾帧） | ¥0.06 / 千 Token |

计费示例：训练集含 2 条视频，时长 3.4 秒和 6.5 秒，`max_pixels = 262144`，`n_epochs = 400`，训练单价 ¥0.06 / 千 Token（wan2.2）：

- 视频 1：3.4 → 四舍五入 3 秒 → min(5, 3) = 3 秒
- 视频 2：6.5 → 四舍五入 7 秒 → min(5, 7) = 5 秒
- 总计费时长 = 3 + 5 = 8 秒
- 训练 Token 总量 = 8 × (262144 / 1024) × 400 = 819,200 = 819.2 千 Token
- 训练费用 = 819.2 × 0.06 = ¥49.15

## 下一步

- [微调概览](/developer-guides/fine-tuning/overview) -- 训练方式、训练模式与支持模型总览
- [创建微调任务](/developer-guides/fine-tuning/create-fine-tuning-job) -- 在控制台创建训练任务
- [超参数参考](/developer-guides/fine-tuning/hyperparameters) -- `max_steps`、`n_epochs`、`max_pixels` 等参数说明
