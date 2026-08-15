> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创意海报生成

> 根据文字描述自动生成海报背景和文字排版，支持多种海报风格。

创意海报生成能够根据您的要求自动生成海报的背景和文字排版，支持多种海报风格。从宣传到祝福，让每一张海报都成为您的个性宣言。无需设计基础，帮助您轻松制作出彩作品，让创意触手可及。

<Warning>
  wanx-poster-generation-v1 模型当前仅提供**免费体验**，免费额度用完后不可调用且不支持付费，推荐参考[文本生成图像](/developer-guides/image-generation/text-to-image)获取替代方案。
</Warning>

## 基本介绍

### 使用场景

- **社交媒体与个人创作**：社交媒体用户和内容创作者可以根据自己的使用场景，生成相册或者视频的封面，或者是制作祝福卡片等。借助AI的创造力，帮助提升个人IP品牌形象，快速掌握流量密码。
- **新品发布会预热宣传**：通过输入产品特点和目标受众的偏好，包含产品的亮点、上市日期以及引人入胜的口号，用于社交媒体、电子邮件营销和线下广告，有效吸引潜在顾客的注意力，激发他们对新产品的兴趣。
- **节日促销活动推广**：商家可以利用AI创意海报生成工具快速设计出吸引眼球的产品宣传海报，只需输入"圣诞节"、"春节"等关键词，AI就能结合节日元素和品牌风格，创作出充满节日气氛的视觉作品。
- **艺术文化活动宣传**：只需提供音乐会或艺术展览活动名称、时间、地点和主题色彩等信息，AI就能生成多款风格各异的海报设计供选择，通过独特的视觉效果激发观众的兴趣，增加活动的曝光度和参与度。

### 特色优势

- **百变创意风格**：一键生成海报，创意无限，涵盖"剪纸工艺"、"折纸工艺"、"中国水墨"、"中国刺绣"、"真实场景"、"2D卡通"、"儿童水彩"、"赛博背景"等各类场景和风格。
- **多样化版式生成**：支持自动生成海报的背景和文字智能排版，支持横版和竖版海报，支持超高分辨率提升和高清二次精致修复模式，可极速制作多样化出彩海报作品。
- **效果业界领先**：创意海报生成图像语义一致性更精准，AI局部创作布局自然、细节丰富、画面细腻、结果逼真，又保持视觉效果的和谐与专业性，无需担心人工合成的痕迹。
- **稳定、易用平台服务**：提供在高并发、大流量下的稳定创意海报生成响应，可直接调用的简单推理API接口，服务简单易用，易被集成，兼容性强。

### 模型概览

<Note>
  wanx-poster-generation-v1 模型当前仅供免费体验，免费额度用完后不可调用且不支持付费，推荐参考[文本生成图像](/developer-guides/image-generation/text-to-image)获取替代方案。免费额度详情请参见[免费额度](/resources/free-quota)。
</Note>

## 快速开始

**输入限制**：

- 提示词输入限制：中文和英文提示词二者至少选其一，也可以都选。两者加起来最多50个字/单词。
- 主标题字符限制：最多30个字符。
- 副标题字符限制：最多30个字符。
- 正文字符限制：最多50个字符。

**请求参数示例**：

```json
{
  "model": "wanx-poster-generation-v1",
  "input": {
    "title": "春节快乐",
    "sub_title": "家庭团聚，共享天伦之乐",
    "body_text": "春节是中国最重要的传统节日之一，它象征着新的开始和希望",
    "prompt_text_zh": "灯笼，小猫，梅花",
    "wh_ratios": "竖版",
    "lora_name": "童话油画",
    "lora_weight": 0.8,
    "ctrl_ratio": 0.7,
    "ctrl_step": 0.7,
    "generate_mode": "generate",
    "generate_num": 1
  },
  "parameters": {}
}
```

由于模型计算耗时较长，示例代码展示异步处理的调用方式，以避免请求超时。

您需要已[获取API Key](/api-reference/preparation/api-key)并[配置API Key到环境变量](/api-reference/preparation/export-api-key-env)。

### 1. 创建创意海报生成任务

接口返回任务ID，可根据任务ID查询图像生成的结果。

```bash
curl --location --request POST 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text2image/image-synthesis' \
--header 'X-DashScope-Async: enable' \
--header 'Content-Type: application/json' \
--header "Authorization: Bearer $DASHSCOPE_API_KEY" \
--data '{
  "model": "wanx-poster-generation-v1",
  "input": {
    "title": "春节快乐",
    "sub_title": "家庭团聚，共享天伦之乐",
    "body_text": "春节是中国最重要的传统节日之一，它象征着新的开始和希望",
    "prompt_text_zh": "灯笼，小猫，梅花",
    "wh_ratios": "竖版",
    "lora_name": "童话油画",
    "lora_weight": 0.8,
    "ctrl_ratio": 0.7,
    "ctrl_step": 0.7,
    "generate_mode": "generate",
    "generate_num": 1
  },
  "parameters": {}
}'
```

### 2. 根据任务ID查询结果

```bash
curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
  -H "Authorization: Bearer $DASHSCOPE_API_KEY"
```

## 创意海报风格示例

<Accordion title="中国刺绣">
  ```json
  {
    "model": "wanx-poster-generation-v1",
    "input": {
      "title": "谷雨",
      "sub_title": "24 SOLAR TERMS",
      "body_text": "遥看春雨润百谷\n听闻万象正生长",
      "prompt_text_zh": "中国龙，梅花，云朵",
      "wh_ratios": "竖版",
      "lora_name": "中国刺绣",
      "lora_weight": 0.5,
      "ctrl_ratio": 0.7,
      "ctrl_step": 0.7,
      "generate_mode": "generate",
      "generate_num": 1
    },
    "parameters": {}
  }
  ```
</Accordion>

<Accordion title="2D插画1">
  ```json
  {
    "model": "wanx-poster-generation-v1",
    "input": {
      "title": "抽象艺术家",
      "sub_title": "有趣的灵魂终要相遇",
      "body_text": "创意海报生成，自由设计，瞬间点亮创意生活",
      "prompt_text_zh": "抽象艺术，几何形状，流动线条，极简主义，明亮色彩",
      "wh_ratios": "竖版",
      "lora_name": "2D插画1",
      "lora_weight": 0.8,
      "ctrl_ratio": 0.6,
      "ctrl_step": 0.6,
      "generate_mode": "generate",
      "generate_num": 1
    },
    "parameters": {}
  }
  ```
</Accordion>

<Accordion title="通过prompt指定风格（不设置lora_name）">
  ```json
  {
    "model": "wanx-poster-generation-v1",
    "input": {
      "title": "清明",
      "sub_title": "袅绕青烟\n穿越天上人间",
      "body_text": "人间四月芳菲始\n春归清明雨时节",
      "prompt_text_zh": "朦胧远山，柳树，雨水，2D插画",
      "wh_ratios": "竖版",
      "ctrl_ratio": 0.7,
      "ctrl_step": 0.7,
      "generate_mode": "generate",
      "generate_num": 1
    },
    "parameters": {}
  }
  ```
</Accordion>

<Accordion title="浅蓝抽象">
  ```json
  {
    "model": "wanx-poster-generation-v1",
    "input": {
      "title": "抽象艺术家",
      "sub_title": "有趣的灵魂终要相遇",
      "body_text": "创意海报生成，自由设计，瞬间点亮创意生活",
      "prompt_text_en": "master piece, high quality, futuristic city, streamlined, neon, light blue and light purple, glass texture",
      "wh_ratios": "竖版",
      "lora_name": "浅蓝抽象",
      "lora_weight": 0.8,
      "ctrl_ratio": 0.6,
      "ctrl_step": 0.6,
      "generate_mode": "generate",
      "generate_num": 1
    },
    "parameters": {}
  }
  ```
</Accordion>

<Accordion title="深蓝抽象">
  ```json
  {
    "model": "wanx-poster-generation-v1",
    "input": {
      "title": "抽象艺术家",
      "sub_title": "有趣的灵魂终要相遇",
      "body_text": "创意海报生成，自由设计，瞬间点亮创意生活",
      "prompt_text_en": "uminous Particles, Streamlined, holography, Particles, Abstract, Blue and Purple, Tech Style",
      "wh_ratios": "竖版",
      "lora_name": "深蓝抽象",
      "lora_weight": 0.8,
      "ctrl_ratio": 0.6,
      "ctrl_step": 0.6,
      "generate_mode": "generate",
      "generate_num": 1
    },
    "parameters": {}
  }
  ```
</Accordion>

<Accordion title="童话油画（竖版）">
  ```json
  {
    "model": "wanx-poster-generation-v1",
    "input": {
      "title": "元宵节",
      "sub_title": "正月十五",
      "body_text": "团圆时节，汤圆香甜，祝你幸福美满！",
      "prompt_text_zh": "灯笼，小猫，梅花",
      "wh_ratios": "竖版",
      "lora_name": "童话油画",
      "lora_weight": 0.8,
      "ctrl_ratio": 0.7,
      "ctrl_step": 0.7,
      "generate_mode": "generate",
      "generate_num": 1
    },
    "parameters": {}
  }
  ```
</Accordion>

<Accordion title="童话油画（横版）">
  ```json
  {
    "model": "wanx-poster-generation-v1",
    "input": {
      "title": "元宵节",
      "sub_title": "正月十五",
      "body_text": "团圆时节，汤圆香甜，祝你幸福美满！",
      "prompt_text_zh": "灯笼，小猫，梅花",
      "wh_ratios": "横版",
      "lora_name": "童话油画",
      "lora_weight": 0.8,
      "ctrl_ratio": 0.7,
      "ctrl_step": 0.7,
      "generate_mode": "generate",
      "generate_num": 1
    },
    "parameters": {}
  }
  ```
</Accordion>

<Accordion title="剪纸工艺">
  ```json
  {
    "model": "wanx-poster-generation-v1",
    "input": {
      "title": "星河浩瀚",
      "sub_title": "一闪一闪亮晶晶",
      "body_text": "创意海报生成，自由设计，瞬间点亮创意生活",
      "prompt_text_zh": "闪亮的星星，月亮，银河，卫星",
      "wh_ratios": "横版",
      "lora_name": "剪纸工艺",
      "lora_weight": 0.8,
      "ctrl_ratio": 0.6,
      "ctrl_step": 0.6,
      "generate_mode": "generate",
      "generate_num": 1
    },
    "parameters": {}
  }
  ```
</Accordion>

<Accordion title="浓郁色彩">
  ```json
  {
    "model": "wanx-poster-generation-v1",
    "input": {
      "title": "科技改变生活",
      "sub_title": "有趣的灵魂终要相遇",
      "body_text": "创意海报生成，自由设计，瞬间点亮创意生活",
      "prompt_text_zh": "黑色背景上的色彩爆炸，精细渲染的纹理，简单曲线，创新的页面设计，高速胶片，流线型的形式",
      "wh_ratios": "横版",
      "lora_name": "浓郁色彩",
      "lora_weight": 0.8,
      "ctrl_ratio": 0.8,
      "ctrl_step": 0.7,
      "generate_mode": "generate",
      "generate_num": 1
    },
    "parameters": {}
  }
  ```
</Accordion>

## API参考

API的输入输出参数，请参见[创意海报生成API参考](/api-reference/image-generation/creative-poster/create-task)。
