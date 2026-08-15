> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 人物实例分割

> 识别图像中的不同人物对象，并画出每个对象边界的像素级掩码。

人物实例分割运用检测和分割技术，可以识别出图像中的每个人物对象，并为其生成精确的像素级掩码（mask）。

## 基本介绍

人物实例分割运用了检测和分割技术，不仅能够在图像中识别出不同的对象，而且还能准确地画出每一个对象边界的像素级掩码（mask）。

推荐配合使用[图像擦除补全](/developer-guides/image-generation/image-inpainting)接口来进行AI人体消除，选择完整人体mask区域来消除一个或多个人物。

### 使用场景

- **人像主体抠图**：人体分割通过将摄影主体人物从背景中分割出来，将背景虚化，以达到大光圈浅景深效果，突出人物主体。
- **证件照制作**：上传或拍摄一张多人生活照，可将人物精细地分割出来，再搭配擦除补全处理能力，最终制作出单人证件照。
- **营销广告制作**：在广告制作中，需要将产品图片与特定场景或人物分割，分离原始图片中可能包含不需要的前景或背景元素。

### 特色优势

- **适应复杂背景**：即使人物处于复杂背景环境，依然可以将人体准确地从背景中分割出来。
- **企业级平台服务**：提供在高并发、大流量下的稳定写真图片生成响应，可直接调用的简单推理API接口。

<Note>
  image-instance-segmentation 模型当前仅供免费体验，免费额度用完后不可调用，敬请关注后续动态。免费额度详情请参见[免费额度](/resources/free-quota)。
</Note>

## 快速开始

### 图像输入限制

- 图片分辨率：可支持输入分辨率范围：单边不小于512且不超过4096。
- 图片格式：JPEG、PNG、JPG、BMP、WEBP。
- 图片大小：不超过10M。
- URL地址中不能包含中文字符。

### 效果示例

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", width: "33%", paddingBottom: "8px"}}>**输入图像**</th>
      <th style={{textAlign: "center", width: "33%", paddingBottom: "8px"}}>**输出结果1：像素级掩码图像**</th>
      <th style={{textAlign: "center", width: "34%", paddingBottom: "8px"}}>**输出结果2：可视化图像**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="输入图像" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p841095.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="像素级掩码图像" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p841096.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="可视化图像" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/7854345271/p844284.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

### 调用示例

由于模型计算耗时较长，示例代码展示异步处理的调用方式，以避免请求超时。

您需要已[获取API Key](/api-reference/preparation/api-key)并[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)。

**1. 创建人物实例分割任务**

接口返回任务ID，可根据任务ID查询图像生成的结果。

```bash
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--data-raw '{
  "model": "image-instance-segmentation",
  "input": {
    "image_url": "https://huarong123.oss-cn-hangzhou.aliyuncs.com/image/%E4%BA%BA%E5%83%8F%E5%88%86%E5%89%B2.png"
  },
  "parameters": {}
}'
```

**2. 根据任务ID查询结果**

```bash
curl -X GET 'https://dashscope.aliyuncs.com/api/v1/tasks/{task_id}' \
-H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 计费说明

- 按**成功生成的图片数量**计费。模型调用失败或处理出错不会产生费用。
- 免费额度与计费详情请参见[免费额度](/resources/free-quota)和[计费说明](/developer-guides/getting-started/pricing)。
- 限流信息请在[控制台](https://platform.qianwenai.com/home/benefits)查看。

## API参考

API的输入输出参数，请参见[人物实例分割](/api-reference/image-generation/person-instance-segmentation/create-task)。

## 错误码

如果调用失败，请参见[错误信息](/api-reference/preparation/error-messages)。
