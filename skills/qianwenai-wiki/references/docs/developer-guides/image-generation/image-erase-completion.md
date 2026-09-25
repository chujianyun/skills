> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像擦除补全

> 输入原图、待擦除区域掩码图像以及保留区域掩码图像，可以在保留原图背景的同时擦除指定图像区域。

<Warning>
  image-erase-completion 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费，推荐参考[图像编辑（Qwen）](/developer-guides/image-generation/image-editing)或[图像编辑-Wan](/developer-guides/image-generation/wan-image-editing)获取替代方案。
</Warning>

## 基本介绍

图像擦除补全通过指定图像 mask 中要删除的人体、宠物、物品、文字、水印等图像区域，在保留背景的同时移除图像中的一个或多个人物、物体、文字等元素，此功能不支持通过输入 prompt 指定消除区域。擦除补全技术结合 AIGC inpainting 等先进技术，可以在多种场景下应用，从而满足用户对隐私保护、内容创作和图像编辑等方面需求。

推荐配合使用[人物实例分割](/developer-guides/image-generation/person-instance-segmentation)接口来进行人体消除，选择完整人体 mask 区域来消除一个或多个人物，能准确地画出每一个对象边界的像素级掩码（mask）。

### 使用场景

- **个人隐私保护**：在社交媒体平台上分享照片时，需要移除照片中的某些人物或敏感信息（如特定人物、地址、电话号码等）。擦除补全功能能够快速移除这些元素，避免个人信息泄露。
- **电商商品图制作**：在电商平台上展示产品时，需要去除产品图片上的水印、商标或其他不需要的元素。擦除补全能够识别并移除这些元素，使产品图片更加干净、专业，提升用户体验。
- **营销广告制作**：在广告制作中，需要将产品图片与特定场景或人物结合，但原始图片中可能包含不需要的元素。AI 消除功能能够轻松移除这些图像元素，增强海报或广告视觉创意效果。
- **社交媒体创作**：用户在社交媒体上分享照片时，可能希望移除照片中的路人、杂乱背景等。AI 擦除补全功能让用户能够轻松实现这一需求，提升照片的质量和美观度。

### 特色优势

- AI 擦除补全技术能够智能填补被移除元素留下的空白区域，使修复后的图像看起来自然无痕，又保持视觉效果的和谐与专业性，无需担心人工合成的痕迹。
- AI 擦除补全功能能够自动识别和移除图像中的多种图像格式和尺寸元素的对象，精确识别图像中的对象，确保擦除对象的准确性和补全对象的一致性与自然性。
- 企业级平台服务提供在高并发、大流量下的稳定图像处理响应和 99.9% 的可靠性保障，可直接调用的简单推理 API 接口，服务简单易用，易被集成，兼容性强。

### 模型概览

<table>
  <thead>
    <tr>
      <th>模型名</th>
      <th>免费额度[（查看）](/resources/free-quota)</th>
      <th>计费单价</th>
      <th>任务下发接口 QPS 限制</th>
      <th>同时处理中任务数量</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>image-erase-completion</td>
      <td style={{textAlign: "center"}}>500 张</td>
      <td>目前仅供免费体验。免费额度用完后不可调用，推荐参考[图像编辑（Qwen）](/developer-guides/image-generation/image-editing)或[图像编辑-Wan](/developer-guides/image-generation/wan-image-editing)获取替代方案。</td>
      <td style={{textAlign: "center"}}>2</td>
      <td style={{textAlign: "center"}}>1</td>
    </tr>
  </tbody>
</table>

## 快速开始

为获得更好的图像效果，保留区域图像掩码图应确保干净、不含任何待擦除对象。当通过人物实例分割获取掩码图像时，可设置 `parameters.dilate_flag=true` 对掩码区域做膨胀，规避涂抹区域边缘遗漏，得到清晰完整的掩码图。

- **待擦除区域（mask\_url）**：掩码图像应将待擦除区域像素值置为非零值（即非纯黑色），其他区域像素值置为零（纯黑色）。
- **保留区域（foreground\_url）**：掩码图像应将待保留区域像素值置为非零值（即非纯黑色），其他区域像素值置为零（纯黑色）。

图像输入限制：

- 图片分辨率：可支持输入分辨率范围：单边不小于 512 且不超过 4096。
- 图片格式：JPEG、PNG、JPG、BMP、WEBP。
- 图片大小：不超过 10M。
- URL 地址中不能包含中文字符。

<table style={{width: "100%", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", width: "20%"}}>**原图（image\_url）**</th>
      <th style={{textAlign: "center", width: "20%"}}>**人物实例分割掩码图像**</th>
      <th style={{textAlign: "center", width: "20%"}}>**待擦除区域（mask\_url）**</th>
      <th style={{textAlign: "center", width: "20%"}}>**保留区域（foreground\_url）**</th>
      <th style={{textAlign: "center", width: "20%"}}>**输出**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="原图" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p840837.png" style={{width: "100%"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="人物实例分割掩码" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850595.png" style={{width: "100%"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="待擦除区域掩码" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p840839.png" style={{width: "100%"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="保留区域掩码" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p840841.png" style={{width: "100%"}} />
      </td>

      <td style={{verticalAlign: "top", textAlign: "center"}}>
        <img alt="输出图像" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/0184161571/p840842.png" style={{width: "100%"}} />
      </td>
    </tr>
  </tbody>
</table>

由于模型计算耗时较长，示例代码展示异步处理的调用方式，以避免请求超时。

您需要已[获取 API Key](/api-reference/preparation/api-key)并[配置 API Key 到环境变量](/api-reference/preparation/export-api-key-env)。

**1、创建图像擦除补全任务**

接口返回任务 ID，可根据任务 ID 查询图像生成的结果。

```bash
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--header 'Content-Type: application/json' \
--header 'X-DashScope-DataInspection: enable' \
--data-raw '{
  "model": "image-erase-completion",
  "input": {
    "image_url": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com/your-image.png",
    "mask_url": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com/your-mask.png",
    "foreground_url": "https://your-bucket.oss-cn-hangzhou.aliyuncs.com/your-foreground.png"
  },
  "parameters": {
    "dilate_flag": true
  }
}'
```

**2、根据任务 ID 查询任务状态与结果**

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/13b1848b-5493-4c0e-8c44-xxxxxxxxxxxx \
     -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 效果示例

### 保持图像细节（默认，fast\_mode=false）

调用示例：

```json
{
  "model": "image-erase-completion",
  "input": {
    "image_url": "http://xxx/image.jpg",
    "mask_url": "http://xxx/mask.png",
    "foreground_url": "http://xxx/foreground.png"
  },
  "parameters": {
    "dilate_flag": true
  }
}
```

<table style={{width: "100%", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", width: "20%"}}>**原图（image\_url）**</th>
      <th style={{textAlign: "center", width: "20%"}}>**人物实例分割掩码图像**</th>
      <th style={{textAlign: "center", width: "20%"}}>**待擦除区域（mask\_url）**</th>
      <th style={{textAlign: "center", width: "20%"}}>**保留区域（foreground\_url）**</th>
      <th style={{textAlign: "center", width: "20%"}}>**输出图像**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        <img alt="原图1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850620.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="分割掩码1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850624.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="擦除区域1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850629.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="保留区域1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850631.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="输出图像1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850632.png" style={{width: "100%"}} />
      </td>
    </tr>

    <tr>
      <td>
        <img alt="原图2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850621.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="分割掩码2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850625.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="擦除区域2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850636.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="保留区域2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850635.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="输出图像2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850634.png" style={{width: "100%"}} />
      </td>
    </tr>

    <tr>
      <td>
        <img alt="原图3" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850622.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="分割掩码3" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850626.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="擦除区域3" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850640.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="保留区域3" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850639.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="输出图像3" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850638.png" style={{width: "100%"}} />
      </td>
    </tr>

    <tr>
      <td>
        <img alt="原图4" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850623.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="分割掩码4" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850627.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="擦除区域4" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850641.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="保留区域4" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850642.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="输出图像4" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850643.png" style={{width: "100%"}} />
      </td>
    </tr>
  </tbody>
</table>

### 忽略图像细节（fast\_mode=true）

`fast_mode` 模式适合不需要生成大量细节的场景。

调用示例：

```json
{
  "model": "image-erase-completion",
  "input": {
    "image_url": "http://xxx/image.jpg",
    "mask_url": "http://xxx/mask.png"
  },
  "parameters": {
    "fast_mode": true
  }
}
```

<table style={{width: "100%", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "center", width: "33%"}}>**原图（image\_url）**</th>
      <th style={{textAlign: "center", width: "33%"}}>**擦除区域掩码图像（mask\_url）**</th>
      <th style={{textAlign: "center", width: "34%"}}>**输出图像**</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        <img alt="原图1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850649.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="擦除区域掩码1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850652.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="输出图像1" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850653.png" style={{width: "100%"}} />
      </td>
    </tr>

    <tr>
      <td>
        <img alt="原图2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850657.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="擦除区域掩码2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850658.png" style={{width: "100%"}} />
      </td>

      <td>
        <img alt="输出图像2" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/zh-CN/2949386271/p850659.png" style={{width: "100%"}} />
      </td>
    </tr>
  </tbody>
</table>

## API 参考

API 的输入输出参数，请参见[图像擦除补全](/api-reference/image-generation/image-erase-completion/create-task)。
