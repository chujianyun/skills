> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 鞋靴模特

> 输入模特模板图和鞋靴多视角图片，AI自动完成鞋靴试穿重绘生成。

鞋靴模特生成支持输入多视角鞋靴系列图片，同时对输入模特模板图的鞋子区域进行鞋靴AI试穿，实现模特鞋靴布局重绘生成。最终生成图片效果布局自然、细节丰富、画面细腻、试穿结果逼真。可用于模特商品图设计、新鞋AI试穿、模特穿戴布局重绘等场景。

## 特色优势

- **效果业界领先**：鞋靴模特生成图像语义一致性更精准，AI局部创作布局自然、细节丰富、画面细腻、结果逼真，又保持视觉效果的和谐与专业性，无需担心人工合成的痕迹。
- **稳定、易用平台服务**：提供在高并发、大流量下的稳定鞋靴模特生成图片生成响应，可直接调用的简单推理API接口，服务简单易用，易被集成，兼容性强。

## 使用场景

- **鞋靴商品设计**：结合AI技术的优势，设计师们能够以前所未有的速度和精确度探索创新设计。设计师可以输入从复古皮革靴到未来感十足的运动鞋极速模特AI试穿，确保每一款新品都能商品图极速上架。
- **新鞋创意试穿**：顾客在选购鞋靴时，只需简单输入本人照片，就能"穿上"任何一款店铺新款鞋靴，直观感受外观搭配效果，大大提升了购物的便捷性和趣味性。
- **模特穿戴重绘**：模特试穿能轻松更换模特展示的鞋靴款式，与模特的服装、背景完美融合，创造出多样化的时尚造型。无需重新拍摄，既节省成本又提高了效率。

## 模型概览

<Note>
  shoemodel-v1 模型当前仅供免费体验，免费额度用完后不可调用，敬请关注后续动态。免费额度详情请参见[免费额度](/resources/free-quota)。
</Note>

## 快速开始

### 输入限制

**模特模板图**：

- 图片比例：图长边与短边的比例需在`[2:3, 3:2]`范围内，推荐比例为`4:3`。
- 图片格式：JPEG、PNG、JPG、BMP、WEBP、AVIF。
- 图片大小：建议不超过5M。

**鞋靴多视角图**：

- 图片比例：图长边与短边的比例需在`[2:3, 3:2]`范围内，推荐与模特模板图一样，比例为`4:3`。
- 图片格式：JPEG、PNG、JPG、BMP、WEBP、AVIF。
- 图片大小：建议不超过5M。
- 图片个数：多视角图片个数小于3。

**URL地址**：

- 不能包含中文字符。

### 效果展示

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", paddingBottom: "8px"}}>**模特模板图（template\_image\_url）**</th>
      <th style={{textAlign: "center", paddingBottom: "8px"}}>**鞋靴多视角图（shoe\_image\_url）**</th>
      <th style={{textAlign: "center", paddingBottom: "8px"}}>**输出结果**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="模特模板图" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809310.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="鞋靴多视角图" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809301.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="输出结果" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809309.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

### 调用示例

由于模型计算耗时较长，示例代码展示异步处理的调用方式，以避免请求超时。

您需要已[获取API Key](/api-reference/preparation/api-key)并[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)。

**1. 创建鞋靴布局重绘任务**

接口返回任务ID，可根据任务ID查询图像生成的结果。

```bash
curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/virtualmodel/generation' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data '{
  "model": "shoemodel-v1",
  "input": {
    "template_image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E9%9E%8B%E9%9D%B4%E5%9B%BE.webp",
    "shoe_image_url": ["https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E9%9E%8B%E9%9D%B4temp.webp"]
  },
  "parameters": {
    "n": 1
  }
}'
```

**2. 根据任务ID查询任务状态与结果**

```bash
curl -X GET \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
https://dashscope.aliyuncs.com/api/v1/tasks/13b1848b-5493-4c0e-8c44-xxxxxxxxxxxx
```

## 输入示例示范

### 正确输入示例

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", paddingBottom: "8px"}}>**模特模板图**</th>
      <th style={{textAlign: "center", paddingBottom: "8px"}}>**鞋靴图**</th>
      <th style={{textAlign: "center", paddingBottom: "8px"}}>**输出结果**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="正确示例-模特模板图1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809304.jpeg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="正确示例-鞋靴图1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809306.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="正确示例-输出结果1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809308.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="正确示例-模特模板图2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809297.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="正确示例-鞋靴图2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809300.jpeg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="正确示例-输出结果2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809311.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>

    <tr>
      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="正确示例-模特模板图3" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809298.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="正确示例-鞋靴图3a" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809299.jpeg" style={{width: "48%", margin: "0 0 8px 0", display: "inline-block"}} />

        <img alt="正确示例-鞋靴图3b" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809302.jpeg" style={{width: "48%", margin: "0 0 8px 0", display: "inline-block"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="正确示例-输出结果3" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809307.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

### 错误输入示例

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", paddingBottom: "8px"}}>**没有脚**</th>
      <th style={{textAlign: "center", paddingBottom: "8px"}}>**脚部缺失或姿态非正常站立**</th>
      <th style={{textAlign: "center", paddingBottom: "8px"}}>**膝盖缺失或鞋靴边界距离图片左右边界太近**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="错误示例-没有脚" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809303.jpeg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="错误示例-脚部缺失" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809312.jpeg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="错误示例-膝盖缺失" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/8268778171/p809305.jpeg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

## API参考

API的输入输出参数，请参见[鞋靴模特API参考](/api-reference/image-generation/shoe-model/create-task)。
