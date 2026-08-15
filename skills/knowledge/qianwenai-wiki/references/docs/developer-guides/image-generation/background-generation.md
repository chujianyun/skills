> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像背景生成 - Wan

> 使用万相图像背景生成模型为商品图像生成高质量背景，支持文本引导、图像引导以及边缘引导元素。

万相图像背景生成模型专为商品换背景而设计。您可以选择文本引导（通过输入中英文描述生成背景）、图像引导（使用现有图片作为背景参考），或同时结合这两种方式。此外，模型还支持使用边缘引导元素（即图像的增强边缘特征），可以指定前景和背景内容。借助边缘引导元素，前景和背景在生成时能更自然地与商品融合。该模型适合电商和海报场景，助您快速生成高质量的商品图像。

## 模型概览

**模型效果示意**

<Frame>
  <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5996781571/p904710.png" alt="图像背景生成效果示意" />
</Frame>

**模型说明**

<Note>
  以下价格为目录价。具体优惠活动及折扣价格请前往[模型市场](https://www.qianwenai.com/models)查看。
</Note>

| 模型名                           | 计费单价    | 任务下发接口QPS限制 | 同时处理中任务数量 | 免费额度[（查看）](/resources/free-quota) |
| :---------------------------: | :-----: | :---------: | :-------: | :-------------------------------: |
| wanx-background-generation-v2 | 0.08元/张 | 2           | 1         | 500张                              |

## 前期准备

本文的示例代码使用HTTP调用。在调用前，您需要[开通模型服务并获取API Key](/api-reference/preparation/api-key)，再[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)。

图像模型处理时间较长，为了避免请求超时，HTTP调用仅支持异步获取模型结果。您需要发起两个请求：

- **创建任务**：首先发送一个请求创建任务，该请求会返回任务ID。下文的示例代码已提供创建任务代码。
- **根据任务ID查询结果**：使用上一步获得的任务ID，查询模型生成的结果。查询接口如下所示，需要将`86ecf553-d340-4e21-xxxxxxxxx`替换为真实的任务ID。

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/86ecf553-d340-4e21-xxxxxxxxx \
--header "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 关键能力

万相图像背景生成模型提供多种背景生成方式。生成方式从简单到复杂依次排列如下：

- **文本引导**：最简单的生成方式，通过输入中英文描述即可生成背景。
- **图像引导**：基于引导图像生成相似背景。`noise_level`可用于调整生成背景与引导图像之间的相关性。
- **文本+图像引导**：当结合引导文本和引导图像时，可通过`ref_prompt_weight`设置引导文本的权重，调整引导文本和引导图像对生成背景的影响。
- **文本、图像以及引入边缘引导元素（前景/背景）**：适合复杂且需要细节的商品背景生成场景。比如，设置商品摆放的展台为前景，模型会将展台和主体商品自然地融合。这里的前景或背景需要使用边缘引导算法生成。文本、图像及边缘引导元素可以自由组合成多种生成方式。下文将以**文本+图像+边缘引导元素（前景/背景）** 为例，展示边缘引导元素对图像背景生成的影响。

<Tip>
  **使用建议**：优先体验文本引导或图像引导，再使用文本与图像结合的引导方式。若商品背景要求高且场景复杂，可以考虑选择包含边缘引导元素的生成方式。
</Tip>

### 文本引导

最简单的生成方式，推荐优先尝试。通过输入中英文描述，即可为主体图像生成背景。

字数限制：英文最多支持150个单词，中文大概是100到120个中文字符，超过部分会被自动忽略。

<Frame>
  <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5996781571/p904924.png" alt="文本引导效果示意" />
</Frame>

<Accordion title="示例代码">
  ```bash
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/' \
  --header 'X-DashScope-Async: enable' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wanx-background-generation-v2",
    "input": {
      "base_image_url": "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/main_images/new_main_img/a.png",
      "ref_prompt": "山脉和晚霞"
    },
    "parameters": {
      "model_version": "v3",
      "n": 1
    }
  }'
  ```
</Accordion>

### 图像引导

基于引导图像为主体商品生成相似背景。模型能够将主体图像自然地融合至基于引导图像生成的背景中。

<Frame>
  <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5996781571/p904932.png" alt="图像引导效果示意" />
</Frame>

<Accordion title="示例代码">
  ```bash
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/' \
  --header 'X-DashScope-Async: enable' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wanx-background-generation-v2",
    "input": {
      "base_image_url": "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/main_images/new_main_img/a.png",
      "ref_image_url": "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_images/c5e50d27be534709817b2ab080b0162f_0.jpg"
    },
    "parameters": {
      "model_version": "v3",
      "n": 1,
      "noise_level": 300
    }
  }'
  ```
</Accordion>

**设置noise\_level字段**

通过`noise_level`调整生成的背景与引导图像之间的相关性。noise\_level字段的取值范围为\[0,999]，默认值为300。

- **数值越小**：表示生成背景与引导图像的相关性越高。
- **数值越大**：表示生成背景与引导图像的相关性越低。

<Frame>
  <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5996781571/p905184.png" alt="noise_level对比效果" />
</Frame>

### 文本+图像引导

您还可以结合引导文本和引导图像生成主体商品的背景。

<Frame>
  <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5996781571/p905213.png" alt="文本+图像引导效果示意" />
</Frame>

<Accordion title="示例代码">
  ```bash
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/' \
  --header 'X-DashScope-Async: enable' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wanx-background-generation-v2",
    "input": {
      "base_image_url": "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/main_images/new_main_img/a.png",
      "ref_image_url": "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_images/c5e50d27be534709817b2ab080b0162f_0.jpg",
      "ref_prompt": "山脉和晚霞"
    },
    "parameters": {
      "model_version": "v3",
      "n": 1,
      "ref_prompt_weight": 0.5
    }
  }'
  ```
</Accordion>

**设置ref\_prompt\_weight字段**

当同时设置引导文本和引导图像时，可通过`ref_prompt_weight`设置引导文本的权重，调整引导文本和引导图像对生成背景的影响程度。ref\_prompt\_weight字段的取值范围为\[0,1]，默认值为0.5。

- **ref\_prompt\_weight \< 0.5**：表示引导图像对生成背景的影响更大。
- **ref\_prompt\_weight = 0.5**：表示引导文本和引导图像权重各为0.5，对于生成背景的影响程度一样。
- **ref\_prompt\_weight > 0.5**：表示引导文本对生成背景的影响更大。

<Frame>
  <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5996781571/p905869.png" alt="ref_prompt_weight对比效果" />
</Frame>

### 文本+图像+边缘引导元素（前景/背景）

结合引导文本、引导图像，以及边缘引导元素图像（前景或背景），适用于复杂且需要细节的商品背景生成场景。对于边缘引导元素图像，前景图像会对主体商品产生遮挡，而背景图像的图层则位于主体商品之后。需要注意的是，前景和背景图像需通过边缘引导算法生成。

**为什么前景和背景需要使用边缘引导算法生成？**

图像背景任务通常采用边缘引导算法，因其能够有效保留图像中的边缘和结构信息，同时增强细节表现，提高生成结果的自然性和真实感。

**怎么添加前景/背景元素？**

{/* 边缘引导元素生成方法的API参考页面尚未创建，待创建后更新链接 */}

- 使用边缘引导元素生成方法生成前景或背景元素图像。
- 可以设置每个前景或背景元素图像的prompt，也可以不设置，用空字符串占位。
- 前景和背景元素列表顺序对应生成背景的图层顺序均为从底至上。

下图中的"桃花"、"可爱小狗"为前景元素的prompt，"树叶"为背景元素的prompt。其中，前景元素列表顺序为桃花、可爱小狗，对应生成背景的图层顺序为：桃花图层位于主体商品之前，可爱小狗图层位于桃花图层之前。背景元素为树叶，对应生成背景的图层为：树叶图层位于主体商品之后。

<Frame>
  <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/5996781571/p904710.png" alt="边缘引导元素效果示意" />
</Frame>

<Accordion title="示例代码">
  ```bash
  curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/' \
  --header 'X-DashScope-Async: enable' \
  --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
  --header 'Content-Type: application/json' \
  --data '{
    "model": "wanx-background-generation-v2",
    "input": {
      "base_image_url": "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/main_images/new_main_img/a.png",
      "ref_image_url": "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_images/c5e50d27be534709817b2ab080b0162f_0.jpg",
      "ref_prompt": "山脉和晚霞",
      "reference_edge": {
        "foreground_edge": [
          "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/huaban_soft_edge/6cdd13941cef1b11d885aea1717b983ae566b8efc9094-vcsvxa_fw658webp.png",
          "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_edge/2c36cc4b7da027279e87311dac48fc2d5d784b1e72c0e-x4f1wC_fw658webp.png"
        ],
        "background_edge": [
          "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/ref_edge/0718a9741e07c52ca5506e75c4f2b99e22fff68a4c7d3-P9WGLr_fw658webp.png"
        ],
        "foreground_edge_prompt": [
          "粉色桃花",
          "可爱小狗"
        ],
        "background_edge_prompt": [
          "树叶"
        ]
      }
    },
    "parameters": {
      "model_version": "v3",
      "n": 1,
      "ref_prompt_weight": 0.5,
      "noise_level": 300
    }
  }'
  ```
</Accordion>

## 使用须知

### 输入图像限制

#### 主体图像限制

主体图像必须为带透明背景的RGBA四通道图像，即主体为彩色且背景为透明的图像。输出图像的分辨率与该图像保持一致。

- 主体图像请不要使用半透明图像，这可能导致模型混淆。
- 主体图像不要带有文字，如大段文字、表格文字、图片混合文字等。

| 正确示例（带透明背景RGBA图像）                                                                                                        | 错误示例：半透明图像                                                                                                                | 错误示例：主体图像有文字                                                                                                                |
| :----------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------------: |
| <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9461437371/p904092.png" alt="正确示例" width="200" /> | <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9461437371/p904091.png" alt="半透明图像" width="200" /> | <img src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/9461437371/p904125.jpg" alt="主体图像有文字" width="200" /> |

#### 引导图像限制

引导图像可以是RGB图像或带透明背景的RGBA图像。对于RGBA图像，Alpha通道值为0的区域不参与引导过程的生成。

#### 前景或背景元素图像限制

每个前景或背景图像必须为带透明背景的RGBA四通道图像，分辨率和主体图像相同，如果不同则会自动缩放到和主体图像相同的分辨率。

{/* 边缘引导元素生成方法的API参考页面尚未创建，待创建后更新链接 */}

### 如何查看并获取RGBA图像

1. 检查图片格式。常见的RGBA格式包括png、webp等，而jpg、jpeg格式不是RGBA图像格式。
2. 检查图片是否为RGBA图像。常用的方法有：
   1. 鼠标右键查看图像的文件属性，检查图像的通道信息。如果图像属性没有通道信息，使用图像编辑软件（如PS）进行查看。
   2. 使用Python脚本检查图片属性，代码见步骤3的`打印图像模式`。
3. 将RGB图像转化为RGBA图像。

```bash
pip install Pillow
```

```python
from PIL import Image
import os

# 获取当前文件所在目录路径
current_dir = os.path.dirname(os.path.abspath(__file__))
print(f"当前文件目录路径: {current_dir}")

# 打开图片
image_path = os.path.join(current_dir, 'image.jpg')
image = Image.open(image_path)

# 打印原始图像模式
print("原始图像模式:", image.mode)

# 转换为RGBA模式（确保有Alpha通道）
if image.mode != 'RGBA':
  image = image.convert('RGBA')
else:
  print("图像已为RGBA模式")

# --------------------- 新增背景透明化逻辑 ---------------------
# 设置需要转为透明的背景色（默认白色，可修改为其他颜色如 (0, 0, 0) 黑色）
background_color = (255, 255, 255)  # RGB白色
pixels = image.load()  # 加载像素数据

for y in range(image.height):
  for x in range(image.width):
    r, g, b, a = pixels[x, y]
    # 检查当前像素是否为目标背景色（RGB值完全匹配）
    if (r, g, b) == background_color:
      # 将背景色设为完全透明（Alpha=0）
      pixels[x, y] = (r, g, b, 0)
    else:
      # 保留非背景色像素（Alpha保持不变）
      pixels[x, y] = (r, g, b, a)

# --------------------- 保存与显示 ---------------------
output_path = os.path.join(current_dir, 'output_transparent.png')  # 保存到当前目录
image.save(output_path, 'PNG')
print(f"已保存透明背景图片至：{output_path}")

# 显示图片（可选）
image.show()
```

### 如何切换模型版本

图像背景生成模型为`wanx-background-generation-v2`，如果需要切换模型版本，请设置`parameters.model_version`参数。

- v2：旧版模型，速度快，默认值。
- v3：新版模型，效果更好但响应速度慢，推荐切换到最新版本v3。

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/background-generation/generation/' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "wanx-background-generation-v2",
  "input": {
    "base_image_url": "https://vision-poster.oss-cn-shanghai.aliyuncs.com/lllcho.lc/data/test_data/images/main_images/new_main_img/a.png",
    "ref_prompt": "山脉和晚霞"
  },
  "parameters": {
    "model_version": "v2",
    "n": 1
  }
}'
```

## 相关文档

- [图像背景生成API参考](/api-reference/image-generation/background-generation/create-task)：查看完整的请求参数和返回参数说明。
- [图像API文档常见问题](/resources/faq-images-videos)：图像模型通用问题汇总，包含模型计费与限流、接口高频报错等。
