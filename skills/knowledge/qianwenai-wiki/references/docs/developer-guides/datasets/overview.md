> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 数据集概览

> 在千问AI平台上管理用于模型微调和模型评测的数据集。

数据集是用于在千问AI平台上微调和评测模型的结构化数据文件。您可以在[数据集](https://platform.qianwenai.com/home/model-production/datasets)控制台页面创建、上传和管理数据集。

## 数据集类型

| 种类      | 用途     | 说明                                          |
| ------- | ------ | ------------------------------------------- |
| **训练集** | 用于模型微调 | 支持 SFT / DPO / CPT 算法，涵盖文本生成、视觉理解、图生视频等任务类型 |
| **评测集** | 用于模型评测 | 包含问题和参考答案，用于评估模型输出质量                        |

## 训练集数据格式

训练集的文件格式根据任务类型不同：

不同任务类型的文件格式、大小和数量限制不同：

| 训练任务类型    | 支持的算法           | 文件格式     | 大小与数量限制                | zip 内结构 / 字段                                                               |
| --------- | --------------- | -------- | ---------------------- | -------------------------------------------------------------------------- |
| 文本生成      | SFT / DPO / CPT | `.jsonl` | 最多 10 个文件，单文件最大 200 MB | 每行一个 JSON，SFT/DPO 为 `messages` 对话格式，CPT 为 `text` 纯文本                       |
| 视觉理解      | SFT             | `.zip`   | 1 个压缩包，最大 2 GB         | `data.jsonl`（最大 20 MB）+ 图片（单张最大 10 MB，支持 BMP/JPEG/PNG/WEBP）                |
| 图生视频（首帧）  | SFT             | `.zip`   | 1 个压缩包，最大 4 GB         | `data.jsonl`（20 MB）+ 图片（4096×4096/10 MB）+ 视频（4096×4096/30 MB/20 s，MP4/MOV） |
| 图生视频（首尾帧） | SFT             | `.zip`   | 1 个压缩包，最大 4 GB         | `data.jsonl` + `image/` 子目录（首尾帧图片）+ `video/` 子目录（视频），限制同首帧                 |

<Note>
  视觉理解与图生视频的 `.zip` 包内文件名仅支持英文字符，`data.jsonl` 必须固定命名。
</Note>

<Tabs>
  <Tab title="SFT">
    JSONL 每行包含 `messages` 数组：

    ```json
    {
      "messages": [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "谁在文艺复兴时期描绘了人体？"},
        {"role": "assistant", "content": "<think>思维链推理</think>文艺复兴时期许多艺术家描绘了人体形态。"}
      ]
    }
    ```

    <Tip>
      `<think>` 标签可选。包含此标签可让微调后的模型在回答前输出思维链推理过程。
    </Tip>
  </Tab>

  <Tab title="DPO">
    JSONL 每行包含 `messages`（上下文）、`chosen`（期望回答）和 `rejected`（不期望回答）：

    ```json
    {
      "messages": [
        {"role": "user", "content": "解释量子计算。"}
      ],
      "chosen": {"role": "assistant", "content": "量子计算利用量子比特..."},
      "rejected": {"role": "assistant", "content": "我不了解这方面。"}
    }
    ```
  </Tab>

  <Tab title="CPT">
    JSONL 每行包含一个 `text` 字段：

    ```json
    {"text": "您的领域语料文本内容。CPT 不使用指令-响应格式，直接使用原始文本。"}
    ```

    <Note>
      CPT 需要至少一千万 Token 的优质预训练数据。
    </Note>
  </Tab>

  <Tab title="视觉理解">
    导入文件为 `.zip` 格式，最大 2 GB，zip 包内文件名仅支持英文字符：

    ```
    Trainingdata_vl.zip
    ├── data.jsonl        # 必须固定命名为 data.jsonl，最大支持 20 MB
    ├── image_1.jpeg      # 图像最大分辨率 1024×1024，单张不超过 10 MB，支持 BMP/JPEG/PNG/WEBP
    └── image_2.jpg
    ```

    `data.jsonl` 每行使用多模态 messages 格式，`content` 字段为数组。如需传入 `system` 消息，其 `content` 必须使用数组格式 `[{"text": "..."}]`，不能用字符串：

    ```json
    {
      "messages": [
        {"role": "system", "content": [{"text": "你是一个视觉助手"}]},
        {"role": "user", "content": [
          {"text": "描述这张图片"},
          {"image": "image_1.jpeg"}
        ]},
        {"role": "assistant", "content": [{"text": "这张图片展示了..."}]}
      ]
    }
    ```

    图片通过 `{"image": "文件名"}` 引用。

    字段说明：

| 引用类型 | 字段                                 | 类型  | 必填 | 说明          |
| ---- | ---------------------------------- | --- | -- | ----------- |
| 图片   | `image`                            | str | 是  | 图片文件名       |
| 图片   | `resized_width` / `resized_height` | int | 否  | 目标缩放宽/高（像素） |
  </Tab>

  <Tab title="图生视频">
    使用 `.zip` 格式。首帧和首尾帧的目录结构不同。

    **首帧**：

    ```
    wan-i2v-training-dataset.zip
    ├── data.jsonl          # 最大 20 MB
    ├── image_1.jpeg        # 图片最大 4096×4096，单张 ≤ 10 MB（BMP/JPEG/PNG/WEBP）
    ├── video_1.mp4         # 视频最大 4096×4096，单个 ≤ 30 MB，时长 ≤ 20 s（MP4/MOV）
    ├── image_2.jpeg
    └── video_2.mp4
    ```

    ```json
    {"prompt": "航拍视角：清晨云海中的梯田被金色阳光点亮，镜头缓缓向前推进并俯冲", "first_frame_path": "image_1.png", "video_path": "video_1.mp4"}
    ```

    **首尾帧**：

    ```
    wan-kf2v-training-dataset.zip
    ├── data.jsonl                  # 最大 20 MB
    ├── image/                      # 存放首帧和尾帧图像
    │   ├── image_1_first.jpg       # 图片最大 4096×4096，单张 ≤ 10 MB（BMP/JPEG/PNG/WEBP）
    │   └── image_1_last.png
    └── video/                      # 存放训练目标视频
        ├── video_1.mp4             # 视频最大 4096×4096，单个 ≤ 30 MB，时长 ≤ 20 s（MP4/MOV）
        └── video_2.mov
    ```

    ```json
    {"video_path": "video/video_1.mp4", "first_frame_path": "image/image_1_first.jpg", "last_frame_path": "image/image_1_last.jpg", "prompt": "航拍视角：清晨云海中的梯田被金色阳光点亮，镜头缓缓向前推进并俯冲"}
    ```

    字段说明：

| 字段                 | 类型  | 必填    | 说明                     |
| ------------------ | --- | ----- | ---------------------- |
| `prompt`           | str | 是     | 视频画面内容描述，质量直接决定模型学到的效果 |
| `first_frame_path` | str | 是     | 首帧图像路径（相对 zip 根目录）     |
| `last_frame_path`  | str | 首尾帧必填 | 尾帧图像路径（仅首尾帧数据集需要）      |
| `video_path`       | str | 训练集必填 | 训练目标视频路径；验证集无需此字段      |

    <Note>
      - 数据量：建议至少 10 条，推荐 20-100 条以获得稳定效果。
      - 视频时长：wan2.2 模型建议 2-5 秒，wan2.5 模型建议 2-10 秒。
      - 支持微调的模型：图生视频（首帧）支持 `wan2.5-i2v-preview`、`wan2.2-i2v-flash`；图生视频（首尾帧）支持 `wan2.2-kf2v-flash`。
    </Note>

    **数据清洗建议**：

| 维度  | 正面要求                                  | 负面案例                      |
| --- | ------------------------------------- | ------------------------- |
| 一致性 | 核心特征高度统一（如训练"360度旋转"，所有视频须同为顺时针、速度接近） | 方向混杂，顺时针与逆时针并存，模型无法确定学习方向 |
| 多样性 | 主体与场景丰富，覆盖不同主体、构图、分辨率与长宽比             | 场景单一，模型误将无关元素当作特效一部分      |
| 均衡性 | 各类型数据比例均衡                             | 比例失调，少数类型生成效果差            |
| 纯净度 | 画面干净，使用无干扰原始素材                        | 带字幕、水印、黑边或噪点，模型可能把水印当特效学入 |
| 时长  | 素材时长 ≤ 目标时长（如期望生成 5 秒视频，素材裁剪为 4-5 秒）  | 素材过长导致动作学习不完整、产生截断感       |

    **Prompt 编写公式**：Prompt = \[主体描述] + \[背景描述] + \[触发词] + \[运动描述]

| 组成   | 说明                              | 是否必填 |
| ---- | ------------------------------- | ---- |
| 主体描述 | 画面中原本存在的人或物                     | 是    |
| 背景描述 | 主体所处的环境                         | 是    |
| 触发词  | 一个无实际意义的稀有词汇（如 `s86b5p`），用于触发特效 | 推荐   |
| 运动描述 | 特效发生的运动变化                       | 推荐   |
  </Tab>
</Tabs>

## 评测集数据格式

评测集目前仅支持**文本生成**任务类型，使用 JSONL 格式（`.jsonl`）。

根据评测任务的数据来源，评测集分为两种类型：

- **评测数据集**：仅包含输入和参考答案。评测时模型基于 `prompt` 进行在线推理，系统将推理结果与 `completion` 对比评分。
- **推理结果集**：包含模型已生成的输出（`output`），`completion` 为可选字段。评测时跳过在线推理，直接对已有输出评分，可显著降低推理成本。

| 数据来源类型 | 必需字段                  | 说明                                      |
| ------ | --------------------- | --------------------------------------- |
| 评测数据集  | `prompt`、`completion` | `prompt` 为用户问题，`completion` 为参考答案       |
| 推理结果集  | `prompt`、`output`     | `output` 为模型已生成的输出；`completion`（参考答案）可选 |

<Tabs>
  <Tab title="评测数据集">
    ```json
    {"prompt": "什么是机器学习？", "completion": "机器学习是人工智能的一个分支，通过算法让计算机从数据中学习模式和规律。"}
    {"prompt": "解释深度学习与传统机器学习的区别", "completion": "深度学习是机器学习的子集，使用多层神经网络自动提取特征..."}
    ```
  </Tab>

  <Tab title="推理结果集">
    ```json
    {"prompt": "什么是机器学习？", "completion": "机器学习是人工智能的一个分支...", "output": "机器学习是一种AI技术，让系统从数据中自动学习和改进。"}
    ```
  </Tab>
</Tabs>

<Tip>
  建议至少准备 50 条评测数据。200 条以上可获得统计显著性更高的评测结果。首次使用建议先用 10\~20 条样本验证评测配置的正确性。
</Tip>

## 下一步

- [创建数据集](/developer-guides/datasets/create-dataset) -- 上传数据并创建新数据集。
- [管理数据集](/developer-guides/datasets/manage-datasets) -- 发布、编辑或删除数据集。
- [创建微调任务](/developer-guides/fine-tuning/create-fine-tuning-job) -- 使用已发布的训练集训练自定义模型。
- [评测任务](/developer-guides/evaluation/evaluation-tasks) -- 使用已发布的评测集评测模型表现。
