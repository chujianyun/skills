> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 图像生成微调

> 提升 Wan 图像生成效果

通过编写高效的提示词，使用[文生图指南](/developer-guides/image-generation/text-to-image)生成高质量图像。本指南涵盖提示词结构、视觉词汇和实用示例，帮助您稳定获得理想的生成效果。

## 提示词结构

提示词越完整、越精确，生成图像的质量就越高。以下两种提示词公式适用于不同需求。

### 基础公式

**适用人群**：初次尝试 AI 创作的新用户，以及将 AI 作为灵感来源的用户。适合快速探索和创意实验。

**提示词 = 主体 + 场景 + 风格**

| 要素     | 控制内容                    | 示例                |
| ------ | ----------------------- | ----------------- |
| **主体** | 画面主体——人物、动物、植物、物体或虚构生物  | "一只金毛犬"、"一座中世纪城堡" |
| **场景** | 主体所在的环境——室内/室外、季节、天气、时间 | "在雪地森林中"、"海滩日落时分" |
| **风格** | 艺术风格——写实、抽象、绘画风格        | "水彩风格"、"电影摄影风格"   |

**示例**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingRight: "12px"}}>提示词</th>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingLeft: "12px"}}>效果</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top", paddingRight: "12px"}}>
        25岁中国女孩，圆脸，看向镜头，精致民族服饰，<strong>商业摄影</strong>，<strong>户外</strong>，<strong>电影灯光</strong>，<strong>半身特写</strong>，精致淡妆，锐利边缘。
      </td>

      <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
        <img alt="基础公式示例" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902465.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

### 进阶公式

**适用人群**：有一定 AI 图像生成经验的用户。当您需要精细控制镜头、氛围和细节时使用此公式。

**提示词 = 主体 + 场景 + 风格 + 镜头 + 氛围 + 细节修饰**

| 要素       | 控制内容           | 示例                     |
| -------- | -------------- | ---------------------- |
| **主体**   | 具有特定特征和动作的主要对象 | "一个穿红裙子的可爱10岁中国女孩"     |
| **场景**   | 详细的环境特征        | "被动物王国城市街道商店环绕"        |
| **风格**   | 具体的艺术风格或视觉技法   | "水彩风格"、"皮克斯风格"、"羊毛毡风格" |
| **镜头**   | 景别、角度、镜头类型和构图  | "特写"、"居中构图"、"摄影镜头"     |
| **氛围**   | 情绪和情感基调        | "梦幻"、"孤寂"、"壮丽"、"童趣"    |
| **细节修饰** | 质量和美学的精细调整     | "4K"、"高分辨率"、"逆光"、"自然"  |

**示例**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <thead>
    <tr>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingRight: "12px"}}>提示词</th>
      <th style={{textAlign: "left", width: "50%", paddingBottom: "8px", paddingLeft: "12px"}}>效果</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{verticalAlign: "top", paddingRight: "12px"}}>
        <strong>一只羊毛毡制成的熊猫</strong>，戴着宽边帽，穿着蓝色警察制服马甲，腰间系着皮带，携带警用装备，戴蓝色手套，穿皮鞋，奔跑姿态，毡制效果，<strong>被动物王国城市街道商店环绕</strong>，高级滤镜，路灯，动物王国，童趣，可爱外观，夜晚，明亮，自然，可爱，4K，毡制材质，<strong>摄影镜头</strong>，居中构图，<strong>羊毛毡风格</strong>，<strong>皮克斯风格</strong>，<strong>逆光</strong>。
      </td>

      <td style={{verticalAlign: "top", paddingLeft: "12px"}}>
        <img alt="进阶公式示例" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902591.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

### 结构化提示词模板

如需最大程度地控制生成效果，可将以下维度作为参照清单，选取与目标图像相关的维度组合使用。

| 维度        | 描述        | 示例值                |
| --------- | --------- | ------------------ |
| **主体**    | 画面的主要焦点   | "一只猎豹"、"一座古老的灯塔"   |
| **动作/姿态** | 主体正在做什么   | "奔跑中"、"看向镜头"       |
| **风格**    | 艺术手法      | "3D 卡通"、"水墨画"、"写实" |
| **场景**    | 背景环境      | "茂密森林"、"夜晚的城市街道"   |
| **光照**    | 光源和光线质感   | "电影灯光"、"逆光"、"霓虹灯"  |
| **氛围**    | 情绪或情感     | "宁静"、"戏剧性"、"奇幻"    |
| **镜头角度**  | 拍摄视角      | "平视"、"鸟瞰"、"仰视"     |
| **景别**    | 主体在画面中的比例 | "大特写"、"中景"、"远景"    |
| **镜头**    | 模拟的镜头类型   | "微距"、"长焦"、"鱼眼"     |

## 提示词参数

文生图 V2 的提示词相关参数：

| 参数                | 位置                                | 描述                                                  |
| ----------------- | --------------------------------- | --------------------------------------------------- |
| `text`            | `input.messages[].content[].text` | 正向提示词，描述要生成的图像内容。支持中文和英文。                           |
| `negative_prompt` | `parameters.negative_prompt`      | 反向提示词，指定需要从图像中排除的内容。                                |
| `prompt_extend`   | `parameters.prompt_extend`        | 是否启用智能提示词改写。默认为 `true`，由大语言模型进行智能改写。建议保持默认值以获得最佳效果。 |

**请求示例**

```json
{
  "model": "wan2.6-t2i",
  "input": {
    "messages": [
      {
        "role": "user",
        "content": [
          {
            "text": "一家鲜花店，精美的橱窗，漂亮的木门，门口摆放着鲜花"
          }
        ]
      }
    ]
  },
  "parameters": {
    "negative_prompt": "人物",
    "prompt_extend": true
  }
}
```

## 提示词词汇参考

以下内容提供五个视觉维度的常用关键词：景别、视角、镜头类型、风格和光照。您可以将任意关键词直接添加到提示词中。

### 景别

景别控制主体在画面中的占比，通常分为远景、全景、中景、近景和特写。

| 景别类型    | 适用场景          | 提示词关键词             |
| ------- | ------------- | ------------------ |
| **大特写** | 突出面部细节、纹理、表情  | `extreme close-up` |
| **近景**  | 聚焦单一主体，保留部分环境 | `close-up`         |
| **中景**  | 平衡主体与环境       | `medium shot`      |
| **远景**  | 强调环境，展现空间感    | `long shot`        |

**示例**

**大特写**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        高清相机，情感摄影，日落，大特写人像。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="大特写" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902496.jpeg" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**近景**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        18岁中国女孩，古装，圆脸，看向镜头，精致民族服饰，商业摄影，户外，电影灯光，半身近景，精致淡妆，锐利边缘。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="近景" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902497.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**中景**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        电影时尚人像摄影，亚洲年轻女性，中国苗族女孩，圆脸，看向镜头，优雅深色民族服饰，中广角镜头，晴天，理想化，高清相机拍摄。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="中景" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902498.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**远景**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        两个小人物站在远处的山顶上，背景是壮丽的雪山，背对镜头，静静欣赏日落。夕阳将雪山染成金色，与蔚蓝天空形成鲜明对比。两人仿佛沉醉于这壮观的自然景色中，整幅画面充满宁静与和谐。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="远景" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902495.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

### 视角

视角控制相机相对于主体的拍摄角度。

| 视角类型   | 适用场景          | 提示词关键词                   |
| ------ | ------------- | ------------------------ |
| **平视** | 自然、亲切的视角      | `eye level perspective`  |
| **鸟瞰** | 俯瞰全景、展现图案和规模  | `bird's eye perspective` |
| **仰视** | 戏剧性、雄伟、突出主体气势 | `low angle`              |
| **航拍** | 地形全景、地理环境概览   | `aerial perspective`     |

**示例**

**平视**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        平视视角下的草原场景，一群绵羊悠闲地在翠绿的草地上吃草，羊毛在清晨柔和的阳光下泛着温暖的金色光泽，形成优美的光影效果。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="平视" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902548.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**鸟瞰**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        从空中俯瞰冰湖，湖中心有一艘小船，周围是漩涡图案和鲜艳的蓝色海水。螺旋深渊，从上方俯视拍摄，展现水面涟漪和雪地下层的精细细节。凝望辽阔寒冷的广袤天地，营造令人敬畏的宁静感。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="鸟瞰" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902550.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**仰视**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        热带地区的壮观场景，高大的椰子树如巨人般矗立，茂密的枝叶直指蓝天。仰视镜头让观者仿佛站在树下，感受大自然的雄伟与生机。阳光透过叶缝洒下斑驳光影，增添几分神秘与浪漫。整幅画面充满热带气息，仿佛能闻到椰香、感受到拂面微风。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="仰视" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902549.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**航拍**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        大雪，村庄，道路，灯光，树木。航拍视角，写实效果。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="航拍" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902547.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

### 镜头类型

镜头类型模拟不同相机镜头及其光学特性。

| 镜头类型    | 适用场景         | 提示词关键词                  |
| ------- | ------------ | ----------------------- |
| **微距**  | 微小细节、纹理、小型物体 | `macro lens`            |
| **超广角** | 壮阔风景、建筑内景    | `ultra-wide angle lens` |
| **长焦**  | 突出主体，背景虚化    | `telephoto lens`        |
| **鱼眼**  | 夸张畸变、创意效果    | `fisheye lens`          |

**示例**

**微距**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        樱桃，碳酸水，微距，专业调色，干净锐利对焦，商业高品质，杂志获奖摄影，超写实，UHD，8K。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="微距" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902553.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**超广角**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        蓝天碧海中的小岛，阳光透过树叶洒下斑驳光影。超广角镜头。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="超广角" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902556.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**长焦**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        长焦镜头下，一只猎豹站在茂密的森林中，面朝镜头，背景巧妙虚化，使猎豹的面部成为画面的绝对焦点。阳光透过叶缝洒在猎豹身上，形成斑驳的光影效果，增强了视觉冲击力。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="长焦" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902555.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**鱼眼**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        鱼眼镜头的特殊视角下，一位女性站立并直视镜头。她的形象在画面中心被夸张放大，周围呈现强烈的畸变效果，营造出独特的视觉冲击。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="鱼眼" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902554.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

### 风格

风格定义图像的艺术外观和渲染技法。

| 风格        | 适用场景        | 提示词关键词                   |
| --------- | ----------- | ------------------------ |
| **3D 卡通** | 动画角色、趣味场景   | `3D cartoon style`       |
| **末日废土**  | 反乌托邦、废墟环境   | `post-apocalyptic style` |
| **点彩**    | 印象派点画、纹理感   | `pointillism`            |
| **超现实主义** | 梦幻、不可能的场景   | `surrealist style`       |
| **水彩**    | 柔和、绘画感、透明效果 | `watercolor`             |
| **黏土**    | 雕塑感、手工质感    | `clay style`             |
| **写实**    | 摄影级真实感、逼真细节 | `realistic`              |
| **陶瓷**    | 釉面、雕塑感、瓷器质感 | `ceramic`                |
| **3D**    | 三维渲染、CGI 质感 | `3D`、`C4D rendering`     |
| **水墨画**   | 东亚传统笔墨艺术    | `ink painting`           |
| **折纸**    | 纸折叠、几何感、极简  | `origami`                |
| **工笔画**   | 精细的中国传统绘画   | `Gongbi painting`        |
| **中国水墨**  | 水墨晕染与中式美学   | `Chinese ink style`      |

**示例**

**3D 卡通**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        女子网球运动员，短发，白色网球服，黑色短裤，侧身回球，3D 卡通风格。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="3D 卡通" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902559.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**末日废土**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        火星上的城市，末日废土风格。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="末日废土" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902561.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**点彩**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        一座可爱的白色小房子，茅草屋顶，覆雪的草原，大胆的点彩技法，莫奈风格，清晰笔触，模糊边缘，原始边缘纹理，低饱和度色调，低对比度，莫兰迪色系。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="点彩" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902564.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**超现实主义**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        深灰色大海中一条粉色发光的河流，极简、唯美的氛围，电影灯光，超现实主义风格。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="超现实主义" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902562.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**水彩**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        淡水彩，咖啡馆外，明亮白色背景，细节较少，梦幻感，吉卜力工作室风格。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="水彩" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902563.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**黏土**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        黏土风格，穿蓝色毛衣的小男孩，棕色卷发，深蓝色贝雷帽，画板，户外，海边，半身照。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="黏土" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902560.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**写实**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        篮子，葡萄，野餐布，超写实静物摄影，微距镜头，丁达尔效应。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="写实" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902570.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**陶瓷**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        一只精细的陶瓷小狗安静地卧在桌上，脖子上系着精致的铃铛。每一缕毛发都精心雕刻，眼睛、鼻子和嘴巴的细节栩栩如生。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="陶瓷" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902568.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**3D**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        中国龙，可爱的中国龙趴在白云上睡觉，迷人花园，晨雾中，特写，正面视角，3D，C4D 渲染，32K 超高清，中国朋克风，动物雕像，Octane 渲染，超高清。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="3D" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902567.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**水墨画**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        兰花，水墨画，留白，意境，吴冠中风格，细腻笔触，宣纸质感。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="水墨画" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902565.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**折纸**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        折纸杰作，牛皮纸熊猫，森林背景，中景，极简主义，逆光，最佳品质。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="折纸" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902566.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**工笔画**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        清晨，一枝梅花傲立雪中，花瓣如丝般精致，露珠轻挂其上，展现工笔画的精美之妙。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="工笔画" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902571.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**中国水墨**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        中国水墨风格，一位黑色长发男子，金色发簪，金色蝴蝶飞舞环绕，白色衣裳，高细节，高品质，深蓝色背景，背景隐约可见水墨竹林。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="中国水墨" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902569.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

### 光照

光照设定图像的情绪、氛围和视觉层次。

| 光照类型    | 适用场景          | 提示词关键词                             |
| ------- | ------------- | ---------------------------------- |
| **自然光** | 户外场景、真实温暖感    | `sunlight`、`moonlight`、`starlight` |
| **逆光**  | 剪影、光晕效果、戏剧性轮廓 | `backlight`                        |
| **霓虹灯** | 城市夜景、赛博朋克美学   | `neon light`                       |
| **环境光** | 柔和、弥漫、氛围感光照   | `ambient light`                    |

**示例**

**自然光**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        清晨的阳光洒在茂密森林的地面上，银白色光线穿透树冠，形成斑驳的光影，营造出写实而宁静的氛围。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="自然光" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902574.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**逆光**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        逆光环境下，模特的轮廓线更加分明，金色光线和丝绸环绕模特，营造梦幻般的光晕效果。整个场景充满艺术气息，展现高水准的摄影技巧与创意。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="逆光" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902575.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**霓虹灯**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        雨后的城市街景，霓虹灯在湿润的地面上映射出五彩光芒。行人撑伞匆匆而过，车辆缓缓驶过奇幻的街道，留下缤纷的光迹。整幅画面充满城市夜晚的神秘与浪漫，仿佛每颗雨滴都在诉说着城市的故事。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="霓虹灯" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902576.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>

**环境光**

<table style={{width: "100%", borderCollapse: "collapse", tableLayout: "fixed"}}>
  <tbody>
    <tr>
      <td style={{verticalAlign: "top", width: "55%", paddingRight: "12px"}}>
        夜晚河畔的浪漫艺术场景，环境光柔和地照亮水面，一组莲花灯缓缓漂向河心，灯光与波光粼粼的水面交相辉映，营造梦幻般的视觉效果。
      </td>

      <td style={{verticalAlign: "top", width: "45%", paddingLeft: "12px"}}>
        <img alt="环境光" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/2031097471/p902577.png" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
      </td>
    </tr>
  </tbody>
</table>
