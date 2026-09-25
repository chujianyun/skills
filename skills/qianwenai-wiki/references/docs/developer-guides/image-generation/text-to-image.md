> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 文生图

> 根据文本提示词生成图像。

根据文本描述生成图像。如需对比各模型并选择合适的方案，请参见[图像模型](/developer-guides/getting-started/image-models)。**模型体验**：[千问AI平台](https://platform.qianwenai.com/home/try-ai)。

## 模型效果展示

### Qwen-Image

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>复杂布局</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>长段落</th>
    <th style={{textAlign: "left", width: "34%", paddingBottom: "8px"}}>写实人像</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      <img alt="复杂布局" src="https://g-adoc.alcasset.com/media/maas_docs/maas-cn/common/images/6a4b3c2d1e0f9ea7.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      <img alt="长段落" src="https://g-adoc.alcasset.com/media/maas_docs/maas-cn/common/images/6a4b3c2d1e0f9ea6.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      <img alt="写实人像" src="https://g-adoc.alcasset.com/media/maas_docs/maas-cn/common/images/6a4b3c2d1e0f9ea5.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      UI设计
    </td>

    <td style={{verticalAlign: "top"}}>
      PPT
    </td>

    <td style={{verticalAlign: "top"}}>
      插画设计
    </td>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      <img alt="UI设计" src="https://g-adoc.alcasset.com/media/maas_docs/maas-cn/common/images/6a4b3c2d1e0f9ea4.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      <img alt="PPT" src="https://g-adoc.alcasset.com/media/maas_docs/maas-cn/common/images/6a4b3c2d1e0f9ebb.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      <img alt="插画设计" src="https://g-adoc.alcasset.com/media/maas_docs/maas-cn/common/images/6a4b3c2d1e0f9eba.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>
  </tr>
</table>

<Accordion title="点击查看提示词" defaultOpen>
  **复杂布局**:

  ```
  这是一张横向展开的电商店铺招牌信息图，整体采用 16:9 的宽屏比例，完美适配电脑端与平板端的店铺首页顶部展示。画面整体背景采用高饱和度的墨西哥传统色彩体系，以明黄、赤红、孔雀蓝、翠绿为主色调，色彩之间通过柔和的水彩晕染效果自然过渡，背景纸张带有轻微的手绘水彩纹理与细腻的颗粒质感，营造出一种温暖、热情且充满异域风情的视觉氛围。画面最顶部和最底部边缘，装饰着传统的墨西哥剪纸（Papel Picado）镂空图案，这些剪纸图案由连续的菱形、三角形与波浪形组合而成，以明黄、赤红、翠绿、紫色交替排列，呈现出随风飘动的轻盈姿态，镂空部分透出背景的深邃星空蓝，增加了画面的层次感与呼吸感。顶部剪纸下方与底部剪纸上方，各有一条连续的阿兹特克几何图腾边框，由连续的阶梯状折线与菱形图案组成，采用纯白色与暗金色线条勾勒，为整个店招奠定了浓厚的墨西哥文化底蕴与复古手工艺基调。画面四角点缀着立体的彩色陶罐与微型仙人掌盆栽，陶罐表面绘制着经典的蓝白相间塔拉韦拉（Talavera）花纹，釉面带有高光反射，仙人掌则呈现出饱满的翠绿色，带有细微的刺状纹理，这些角落元素起到了平衡画面重心、丰富视觉细节的作用。

  画面左侧三分之一区域为品牌主视觉与核心标识区，视觉中心是一个巨大的立体字“TodoTi”。字体设计巧妙融入了墨西哥自然元素，字母“T”的顶部延伸出两片翠绿的仙人掌叶片，叶片表面带有清晰的脉络纹理；字母“o”内部填充着赤红与明黄相间的太阳放射状光芒，光芒由十六条等距的直线构成；字母“d”的圆弧部分带有塔拉韦拉陶瓷的蓝白花纹，绘制着三朵牡丹与缠绕的藤蔓；字母“i”的点被替换为一颗立体的红色小番茄，表面带有白色的高光点。整个“TodoTi”字体采用粗犷的黑色描边，内部填充高饱和度的渐变色，并带有轻微的立体投影效果，使其在背景中跃然而出。在店名正下方，是一行醒目的品牌Slogan，文字内容为“TodoTi
  你的色彩生活馆”，字体采用圆润可爱的无衬线粗体，颜色为纯白色，带有轻微的红色外发光效果，文字排版居中对齐，字间距适中，确保在远距离观看时依然清晰易读。Slogan下方是一行较小的副标题，文字内容为“源自墨西哥的热情
  点亮每一个日常”，字体采用优雅的手写体风格，颜色为明黄色，排版同样居中，行距紧凑，与上方的Slogan形成良好的视觉层级。在文字后方的背景中，隐约浮现出一幅巨大的墨西哥太阳历（阿兹特克日历）半圆形浮雕，浮雕采用暗金色与古铜色渐变，表面刻有精细的几何纹路与人面图腾，人面图腾的眼睛呈菱形，嘴巴呈矩形，散发着柔和的金色光芒，为品牌标识提供了深厚的文化背景与视觉支撑。左侧边缘还垂直排列着三个小型的圆形徽章，分别写着“精选
  好物”、“源头
  直采”、“用心
  服务”，徽章底色为孔雀蓝，文字为白色，边缘带有白色的虚线缝线效果，增强了手工质感。

  画面中左部是核心插画与商品展示区，占据画面约四分之一的宽度。这里绘制了一幅充满墨西哥风情的生活场景插画。画面中心是一个戴着宽边草帽（Sombrero）、穿着彩色刺绣披风（Poncho）的卡通骷髅女孩（Catrina）。她的面部妆容精致，眼窝处画着黑色的心形图案，边缘带有白色的虚线装饰，脸颊点缀着红色的玫瑰花纹，花瓣层层叠叠，嘴角带着温暖甜美的微笑。她头上戴着巨大的明黄色宽边草帽，草帽边缘装饰着红绿相间的编织流苏，流苏长度约为五厘米；身上披着赤红与孔雀蓝交织的披风，披风上绣着繁复的阿兹特克几何图腾与盛开的万寿菊图案，万寿菊的花瓣呈放射状排列。她正微笑着推着一辆复古的木制手推车，手推车的轮子由彩色的马赛克瓷砖拼贴而成，瓷砖颜色包括蓝、白、黄、绿，充满艺术气息。手推车里装满了丰富且具体的日常用品，每一件商品都清晰可见并配有详细的标签。最前方是一个彩色的塔拉韦拉陶瓷马克杯，杯身绘制着蓝白相间的牡丹与藤蔓花纹，牡丹花瓣共有十二层，旁边漂浮着标签，文字为“塔拉韦拉陶瓷杯
  耐高温 釉下彩
  容量 350ml”。杯子后方是一个手工编织的收纳筐，筐体由天然剑麻编织而成，纹理呈人字形走向，带有两个皮革提手，标签文字为“手工编织收纳筐
  天然剑麻 结实耐用
  尺寸 30x20x15cm”。收纳筐上方放置着一个仙人掌形状的香薰蜡烛，蜡烛主体为翠绿色，表面带有细微的凸起纹理，顶部有一簇白色的火苗，火苗边缘带有淡黄色光晕，标签文字为“仙人掌香薰蜡烛
  植物精油 助眠安神
  燃烧时间 约40小时”。手推车的最里层堆放着几个色彩斑斓的抱枕，抱枕套采用棉麻材质，印着太阳神图腾与彩色条纹，四角带有长度约三厘米的流苏，标签文字为“墨西哥风情抱枕
  棉麻材质 可拆洗
  尺寸 45x45cm”。插画背景是一片阳光明媚的沙漠绿洲，远处有几棵高低错落的真实仙人掌，天空中飘浮着几朵洁白的云彩，整体光影采用温暖的侧逆光，为插画中的每一个元素镀上了一层宽度约两毫米的金色轮廓光，使画面充满生机与活力。

  画面中右部是商品分类导航区，采用四个色彩鲜艳的圆角矩形卡片，呈 2x2 网格排列，每个卡片代表一个日常用品分类，卡片之间保持着均匀且明确的间距，确保信息布局充实有序。左上角的卡片底色为赤红色，表面带有轻微的纸张纹理，圆角半径为十五像素，顶部标题为“家居布艺”，字体为白色粗体，下方配有一个彩色编织挂毯的扁平化图标，挂毯底部带有长度约两厘米的流苏。卡片正文分为两行，文字内容为“地毯 抱枕 桌布 窗帘
  采用优质棉麻，色彩鲜艳，
  为家增添墨西哥热情。”，文字颜色为纯白色，排版左对齐，行距设定为 1.5 倍。右上角的卡片底色为孔雀蓝，顶部标题为“餐厨用具”，字体为白色粗体，下方配有一个塔拉韦拉陶瓷盘的图标，盘子边缘绘制着连续的波浪纹。正文文字为“碗碟 杯具 餐具 收纳
  手工陶瓷质感，让每一餐
  都充满异域风情。”，文字颜色为明黄色，形成鲜明的色彩对比。左下角的卡片底色为明黄色，顶部标题为“卫浴洗护”，字体为深棕色粗体，下方配有一个仙人掌形状的肥皂盒图标，肥皂盒表面带有三根短刺。正文文字为“浴巾 皂盒 牙刷杯 置物架
  防水防潮材质，打造清爽
  舒适的洗浴空间。”，文字颜色为深棕色，确保在亮色背景上的高可读性。右下角的卡片底色为翠绿色，顶部标题为“生活杂货”，字体为白色粗体，下方配有一个彩色风车图标，风车四个叶片分别为红、黄、蓝、绿四色。正文文字为“衣架 挂钩 纸巾盒 垃圾桶
  实用与美观并存，细节之处
  彰显生活品味。”，文字颜色为纯白色。这四个分类卡片提供了清晰的商品导航，其本身的设计也高度契合墨西哥色彩美学，图标与文字的搭配直观且富有吸引力。

  画面右侧是促销与活动信息区，视觉主体是一个巨大的墨西哥吉他（Mariachi）形状的边框。吉他琴身采用温暖的原木色，表面绘制着精致的红色与金色雕花，雕花图案为缠绕的藤蔓与盛开的玫瑰，琴颈向上延伸，琴弦采用银白色线条绘制，闪烁着金属光泽。吉他琴身内部是核心的促销信息区域。顶部有一条横跨琴身的红色丝带横幅，上面写着“TodoTi
  新店开业
  狂欢季”，文字为白色粗体，带有轻微的立体阴影。横幅下方是巨大的促销数字，文字内容为“全场满 199
  减 50”，数字“199”和“50”采用明黄色与赤红色交替的超大号立体字，极具视觉冲击力，文字“全场满”和“减”采用白色中号字体，排版紧凑且对齐。数字下方是一行较小的优惠说明，文字为“新人首单立减 20 元
  包邮到家”，字体为白色手写体，显得亲切自然。吉他琴身底部排列着三个圆形的小徽章，分别写着“7天
  随心
  退换”、“极速
  发货”、“正品
  保障”，徽章底色为深蓝色，文字为白色，边缘带有宽度为一像素的金色细线描边。吉他琴颈部分延伸出几条彩色的丝带，丝带呈波浪状飘动，上面写着“活动时间
  即日起至
  本月底”，文字为深棕色，排版顺着丝带的弧度微微倾斜，增加了画面的动感与趣味性。

  画面底部是一条横向的品牌故事与文化区，占据画面下方约四分之一的空间。背景是深蓝色的夜空，点缀着大小不一的白色星星，星星呈五角星形状，边缘带有微弱的发光效果，天空中还分布着黑色的仙人掌剪影，剪影轮廓清晰，营造出一种静谧而深邃的氛围，与上方鲜艳热烈的色彩形成完美的视觉平衡。左侧是一个醒目的标题块，文字为“关于
  TodoTi”，字体为白色粗体，带有明黄色的外发光效果，排版垂直居中。标题右侧的内容分为三个等宽的列，每列都有独立的小标题和正文。第一列小标题为“设计理念”，字体为明黄色粗体，底部带有一条长度约五厘米的白色下划线，正文文字为“TodoTi 汲取墨西哥传统手工艺的色彩与灵感，
  将阿兹特克图腾、塔拉韦拉陶瓷纹理与现代家居
  实用主义完美结合，让日常用品成为家中的艺术品。”，文字为浅灰白色，排版左对齐，行距设定为 1.5 倍，确保长段落的阅读体验。第二列小标题为“品质承诺”，字体为明黄色粗体，底部同样带有白色下划线，正文文字为“我们严选全球优质供应商，每一件商品都经过
  严格的质量检测。从材质挑选到工艺打磨，
  只为给您提供安全、耐用、环保的生活好物。”，文字同样为浅灰白色，排版与第一列保持一致。第三列小标题为“生活哲学”，字体为明黄色粗体，底部带有白色下划线，正文文字为“生活需要丰富的色彩，TodoTi 倡导用色彩点亮日常。
  像墨西哥人一样热爱生活、享受当下，让每一次
  触摸、使用，都能感受到阳光般的温暖与热情。”，文字为浅灰白色。这三列文字内容详实，从设计、品质到理念，全方位展示了店铺的品牌内涵，配合底部的星空背景，整个店招兼具商业促销功能与品牌文化传播的深度。

  在最底部的边缘，紧贴着阿兹特克几何图腾边框的上方，是一条细长的互动与引导区。背景为半透明的纯白色，带有轻微的毛玻璃模糊效果，使其与上方的深蓝色夜空背景自然融合。
  获取更多家居灵感
  官方认证 TodoTiOfficial，文字为深棕色，排版紧凑，图标与文字对齐，清晰明了。中间是一个模拟搜索框的设计，框体为白色圆角矩形，带有浅灰色的内阴影，内部左侧有一个放大镜图标，放大镜镜片为圆形，手柄向右下方倾斜四十五度，右侧写着“搜索
  日常好物
  开启色彩生活”，文字为赤红色，模拟用户输入的状态，引导顾客进行商品搜索。右侧是客服联系引导，配有一个耳麦形状的图标，耳麦线条圆润，文字为“有任何问题
  随时联系我们
  客服热线 400-888-TODO
  在线时间 9:00-22:00”，文字为深棕色，排版与左侧对称。整个底部引导区信息明确，功能性强，为顾客提供了便捷的互动入口。
  ```

  **长段落**:

  ```
  中国古典水墨长卷风格，竖幅构图，画面自上而下、自右向左以行书题写柳永《雨霖铃·寒蝉凄切》全文（共12行，含标点与换行）：“寒蝉凄切，对长亭晚，骤雨初歇。都门帐饮无绪，留恋处、兰舟催发。执手相看泪眼，竟无语凝噎。念去去，千里烟波，暮霭沉沉楚天阔。多情自古伤离别，更那堪、冷落清秋节！今宵酒醒何处？杨柳岸，晓风残月。此去经年，应是良辰好景虚设。便纵有千种风情，更与何人说？”书法墨色浓淡相宜，飞白自然，笔锋遒劲中见婉转，行气连贯如流水；字迹略带微洇，仿宣纸渗透效果。背景为极简留白水墨意境：右下角绘一叶孤舟泊于浅滩，舟头微翘，缆绳轻系枯柳；左侧远景以淡墨晕染出层叠低垂的暮霭与空阔楚天，天际线处一抹青灰远山若隐若现；近景岸边斜出三两枝细柳，枝条纤柔，叶已疏落，承袭清秋萧瑟之气；柳梢悬一弯将隐未隐的残月，清冷微光映照薄雾中拂面的晓风痕迹（以几缕轻扬的柳丝与水纹示意）。整幅画气息沉郁隽永，哀而不伤，严格遵循宋词意境与传统文人画**“诗书画一体”**范式，无印章、无题跋、无现代元素。
  ```

  **写实人像**:

  ```
  帮我生成一张生活化美食男生人像写真，呈现实拍电影质感。画面主体是一位24岁左右的年轻男生，五官清爽干净，眉眼温和，皮肤自然清透，保留真实的肤质细节。他穿着质地柔软的米白色粗棒针织毛衣，内搭纯白T恤微微露出领口，展现出温暖、精致且松弛的生活气息。人物坐在温馨的西餐厅餐桌前，身体微微前倾，右手握着银质刀叉正在轻轻切开盘中的惠灵顿牛排，左手自然轻扶着桌面边缘。他微微侧头看向镜头，嘴角带着若有似无的松弛浅笑，眼神温柔且带有生活感。木质桌面上摆满了精致的西餐餐食，旁边有装着琥珀色饮品的复古高脚杯和一小瓶淡雅的复古插花。人物身后是通透的玻璃墙面，上面印有浅金色的法文手写体菜单“Menu du Jour”，文字以丝印工艺自然贴合在玻璃表面，并带有轻微的环境反光。环境采用暖黄色室内顶光，光线柔和地洒在人物面部和桌面食物上，食物表面泛着诱人的高光，背景玻璃透出室外微弱的冷色环境光，形成电影感十足的冷暖光影对比。采用近距离平视取景，机位略带侧前方的呼吸感，避免死板居中，小景深让背景的玻璃墙面和餐厅环境轻微虚化，形成温暖的散景光斑，前景的插花和饮品边缘也带有自然的虚化过渡，整体色调温暖治愈，充满浓郁的生活氛围与美食诱惑。
  ```

  **UI设计**:

  ```
  这张图片是一款沉浸式亚洲雨林声音探索体验网站的宽屏电脑端界面设计，整体氛围暗沉静谧，设计灵感源自老式野外录音设备与模拟科学仪器。整体配色以深邃祖母绿、浓郁黑曜石黑与柔和大地棕为主，营造出安宁沉静的氛围。界面搭载细微水汽与薄雾特效，柔和斑驳的光影折射效果模拟阳光穿透茂密树冠的景象，背景融入纸张细纹、叶脉等自然肌理。整体画面写实度极高，风格对标英国广播公司高端自然纪实纪录片，构图富有电影质感，渲染细节极致精细。
  页面最顶端横贯一整条极简半透明导航栏。最左侧为品牌标识，由精致线条绘制的老式模拟麦克风与龟背竹叶交织而成，搭配柔和米奶油色优雅衬线字体文字“RAINFOREST ARCHIVE”。导航栏右侧是导航菜单，包含四个极简文字链接，字体与颜色和品牌名保持一致：“Expeditions”、“Species”、“Field Notes”、“About”。
  页面上三分之二区域为主视觉横幅板块。背景是一张画质超清、氛围感浓郁的古老亚洲龙脑香科雨林实景图，林间萦绕着轻柔绵延的薄雾；前景虚化的深绿色蕨类枝叶形成自然暗角。横幅板块左侧叠加主标题，采用大号高对比度精致衬线字体，文字为“Voices of the
  Canopy”。标题正下方是字号更小、质感雅致的副标题，浅米奶油色，内容为“An auditory journey through the ancient
  dipterocarp forests of Southeast Asia.”。文字带有轻微打字机质感，字符排布存在细微自然错落，强化复古模拟设备的复古氛围。
  横幅板块中下位置是核心音频交互组件：一台复刻老式野外模拟录音机的精密播放器，原型为经典纳格拉或马兰茨磁带机。播放器机身采用拉丝深枪灰色金属材质，带有细微自然划痕与使用磨损痕迹；配有两个大型滚花金属旋钮，旋钮上印有小巧清晰的无衬线刻印文字“GAIN”与“MONITOR”。设备中央是经典音量表，内置温润柔和的琥珀色背光，表内指针轻靠零刻度位置。音量表右侧设有重型实体拨动开关，拨至上方代表“PLAY”播放状态。音频播放时，音量表向外缓缓扩散出同心波纹特效，形似轻柔水纹或细微声波，采用半透明雾绿色调，与薄雾背景自然融合。
  横幅板块下方，页面布局切换为简约纪实风网格，用作声音素材库区域。板块顶部配有精致小型标题，全大写字母加宽字距排版，文字为“CURRENT EXPEDITIONS”。标题下方采用规整双栏网格，陈列四张风格各异的声景卡片。
  左上第一张卡片：背景是氛围感暗沉的薄雾河岸缩略图，标题文字“Dawn Chorus in Danum Valley”，下方标注信息“Location: Sabah, Borneo”、“Duration: 42:15”，卡片右侧配有一枚小巧琥珀色标识，标注“Currently Playing”。
  右上第二张卡片：画面为湿润宽大绿叶特写，标题文字“Monsoon Rain on Broadleaves”，标注信息“Location: Khao Yai, Thailand”、“Duration: 1:15:30”，附带细线条边框按钮，文字“Listen”。
  左下第三张卡片：画面是黄昏时分森林树冠朦胧剪影，标题文字“Nocturnal Gibbon Calls”，标注信息“Location: Khao Sok, Thailand”、“Duration: 58:02”，附带细线条边框按钮，文字“Listen”。
  右下第四张卡片：画面为树皮纹理微距特写，标题文字“Hornbill Wingbeats”，标注信息“Location: Taman Negara, Malaysia”、“Duration: 24:40”，附带细线条边框按钮，文字“Listen”。
  声景网格最右侧，纵向贯穿该下半区域的竖版面板，设计复刻老式野外科学记录本内页。纸张带有柔和复古米黄肌理，页面右下角留有淡咖啡渍痕迹。面板标题采用打字机等宽字体，文字“FIELD NOTES”；正文墨水色调雅致、微微褪色，内容为：
  “Recorded using
  parabolic microphones
  and Nagra IV-S
  tape recorders.
  Humidity: 94%
  Temp: 24°C”
  文字旁配有深棕乌墨手绘精致猪笼草植物速写。
  页面最底端是极简页脚，整页宽度贯通，上方设有一条细深绿色分隔线。页脚左侧文字“Copyright 2024 Rainforest Archive”，右侧文字“Funded by the Wildlife Conservation Society”，两处文字均采用柔和低调的精致小号衬线字体。
  ```

  **PPT**:

  ```
  这是一张宽高比为 16:9 的专业教育类 PPT 幻灯片，整体背景采用极淡的蓝灰色柔和渐变，叠加有极低透明度的正弦波暗纹与微弱的网格点阵纹理，营造出严谨的物理学术氛围与科技感。画面顶部居中位置是主标题区域，文字为巨大的深藏青色无衬线粗体“AC Circuit Anaysis: Resistor with Sinusoidal Voltage”，标题下方紧贴一条明亮的橙色细横线作为视觉分割，横线两端带有微小的圆形端点装饰，增强版式的仪式感。画面主体分为左右两列，采用严谨的栅格对齐系统，左右两列宽度比例约为 1:1.2，确保右侧复杂的公式计算拥有充足的展示空间。左侧列顶部是一个圆角矩形橙色标题栏，内部居中显示白色加粗文字“PROBLEM DATA & WAVEFORM”，标题栏底部带有轻微的投影，使其具有浮起的立体质感。橙色标题栏下方是一个浅灰白色的圆角数据卡片，卡片边缘有极细的浅蓝色边框，内部垂直排列四个数据要点，每个要点左侧配有纯灰色的极简线性图标，依次为电阻符号、波浪线、电压箭头和时钟符号。四个要点的文字采用深灰色清晰字体，依次为“Resistor (R) = 10 Ω”、“Waveform = Sinusoidal”、“Peak Voltage (V subscript p) = 311 V”、“Period (T) = 0.02 s”，文字排版整齐，行距舒适，关键数字使用稍深的颜色进行视觉强调。数据卡片下方是图表区域，顶部居中显示深灰色图表标题“Voltage vs. Time”。图表主体是一个带有浅灰色网格线的二维坐标系，垂直 Y 轴左侧标有深灰色文字“Voltage (V)”，刻度线旁分别标有白色背景框包裹的深蓝色文字“+311”、“0”和“-311”。水平 X 轴下方标有深灰色文字“Time (s)”，刻度线旁标有“0.01”和“0.02”。坐标系中央绘制了一条平滑、饱满且带有轻微发光效果的鲜红色正弦波曲线，曲线线条粗细适中，展现出完美的周期性。在正弦波的波峰处，有一条深蓝色的垂直双向箭头指示振幅，箭头旁标有深蓝色文字“V subscript p = 311 V”。在 X 轴的一个完整周期上方，有一条深蓝色的水平尺寸标注线，两端带有垂直引出线，中间标有深蓝色文字“T = 0.02 s”。图表区域整体留白充足，视觉焦点集中在红色波形上。右侧列顶部同样是一个圆角矩形橙色标题栏，与左侧标题栏高度对齐，内部居中显示白色加粗文字“SOLUTION STEPS & CALCULATIONS”。橙色标题栏下方垂直排列四个浅蓝色渐变的圆角卡片，卡片之间保持均匀的垂直间距，内部留有充足的呼吸空间。第一个卡片左上角有一个深蓝色的圆形编号徽章，内部显示白色数字“1”。卡片标题为深蓝色加粗文字“1. Maximum Current (I subscript p)”。下方正文分为三行，采用标准数学公式的视觉样式排版，呈现为分数线、上下标和根号的优雅形态，文字内容为深灰色“Formula: Ohm’s Law, I subscript p = V subscript p over R”，接着是计算过程“I subscript p = 311 V over 10 Ω = 31.1 A”。卡片右下角有一个亮黄色底色的圆角高亮框，内部显示加粗的深蓝色文字“I subscript p = 31.1 A”。第二个卡片左上角编号徽章显示“2”，标题为“2. AC Voltmeter Reading (V subscript rms)”。正文包含说明“Voltmeters read RMS value.”，公式“V subscript rms = V subscript p over square root of 2”，以及计算“V subscript rms = 311 V over 1.414 ≈ 220 V”，右下角高亮框显示“V subscript rms ≈ 220 V”。第三个卡片编号徽章显示“3”，标题为“3. Actual Power Dissipated (P subscript avg)”。正文包含“Using RMS values.”，公式“P subscript avg = (V subscript rms) squared over R”，计算过程“P subscript avg = (220 V) squared over 10 Ω = 48400 over 10 W = 4840 W”，右下角高亮框显示“P subscript avg = 4.84 kW”。第四个卡片编号徽章显示“4”，标题为“4. Joule Heat in Half Cycle (Q subscript half)”。正文包含“Energy = Power × Time”，时间计算“Time = T over 2 = 0.01 s”，主计算“Q subscript half = P subscript avg × (0.01 s) = 4840 W × 0.01 s = 48.4 J”，右下角高亮框显示“Q subscript half = 48.4 J”。四个卡片的高亮框统一位于右下角，形成整齐的视觉对齐与阅读动线。画面最底部是一条极细的浅灰色横向分隔线，分隔线下方居中显示浅灰色小号无衬线字体“Experimental Physics - AC Circuits Analysis Module”。页脚区域保持极简，其余背景保持纯图形与留白。整张幻灯片色彩系统以深藏青、亮橙色、浅蓝灰和纯白为主，红色波形与黄色高亮框作为视觉点缀，打破了单调，提升了画面的活力与专业度。所有文字边缘锐利，对比度极高，确保在投影或屏幕上清晰可读。光影处理克制，仅通过卡片底部的微弱投影和标题栏的轻微高光来增强层次感，整体呈现出高度成熟、结构清晰、信息饱满的专业物理教学课件质感。
  ```

  **插画设计:**

  ```
  这幅画作以柔和的米白色水彩纸为底，呈现一幅手绘水彩插图。纸张表面展现出传统植物艺术的特征，包括清晰可见的颜料颗粒和湿画法带来的柔和色彩晕染。画面上方中央区域绘有一簇簇紫罗兰和三色堇。花瓣由淡紫色、深紫色和淡紫色渐变交织而成，花心呈金黄色。花朵旁点缀着一片翠绿色的小叶，以半透明的水彩晕染和精细的叶脉刻画而成。柔和的定向光线照亮画面，突显了水彩纸的质感和颜料的微妙变化。在花卉图案正下方，纸张下半部分水平居中的位置，是“Виолета”字样。该字样以弧形书法体书写，并使用了金属金色墨水。字母造型采用流畅、连续的笔画，并略带浮雕立体感，在光线照射下呈现出柔和的金属光泽。
  ```
</Accordion>

### Wan 系列

<table style={{width: "100%", borderCollapse: "separate", borderSpacing: "8px 0", tableLayout: "fixed"}}>
  <tr>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>人像摄影</th>
    <th style={{textAlign: "left", width: "33%", paddingBottom: "8px"}}>写实摄影</th>
    <th style={{textAlign: "left", width: "34%", paddingBottom: "8px"}}>绘画风格</th>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      <img alt="人像摄影" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/7661432671/p1023583.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      <img alt="写实摄影" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/7661432671/p1023584.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      <img alt="绘画风格" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/7661432671/p1023585.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      文字生成
    </td>

    <td style={{verticalAlign: "top"}}>
      海报设计
    </td>

    <td style={{verticalAlign: "top"}}>
      图集生成
    </td>
  </tr>

  <tr>
    <td style={{verticalAlign: "top"}}>
      <img alt="文字生成" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/7661432671/p1023588.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      <img alt="海报设计" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/7661432671/p1023589.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>

    <td style={{verticalAlign: "top"}}>
      <img alt="图集生成" src="https://help-static-aliyun-doc.aliyuncs.com/assets/img/en-US/7661432671/p1023591.webp" style={{display: "block", width: "100%", margin: "0 0 8px 0"}} />
    </td>
  </tr>
</table>

<Accordion title="点击查看提示词">
  **人像摄影**: hyper-realistic Scandinavian woman portrait, flowing platinum blonde hair and piercing blue eyes with prominent freckles, sharp intellectual gaze, Nordic cold-toned directional lighting creating icy atmosphere, minimalist modern styling with clean lines, shallow depth-of-field with a blurred, cold-gradient background, authentic Nordic facial features and porcelain skin texture.

  **写实摄影**: a fish-eye perspective forest scene with dramatic perspective distortion, ultra-detailed red fox staring into lens with piercing amber eyes, hyper-realistic fur texture showing individual guard hairs and undercoat layers, radially warped trees forming circular background patterns, watercolor painting style with translucent washes and organic pigment bleeding, soft pastel palette of moss green and earth ochre tones, painterly lighting with atmospheric glow through canopy gaps

  **绘画风格**: Vintage oil painting style pastoral scene, a farmer herding sheep across a meadow full of wildflowers, a windmill in the distance turning under blue sky and white clouds, smoke curling from the chimney of a wooden house, bright and soft colors, full of tranquility and comfort.

  **文字生成**: A page from a botanical illustration book, hand-drawn watercolor style, depicting a "dandelion" and labeling its various parts.

  **海报设计**: Cinematic poster scene: Extreme macro close-up of eye in wooden crack. Minimalist monochrome, watercolor-CGI fusion, low saturation. Slow push-in with tremor for surreal intensity. Vast negative space, hidden title. Optimized for immersive video generation.

  **图集生成**: Memories of an old man's life, four portraits in different frames, depicting his childhood (black and white photo), youth (military uniform photo), middle age (business suit work photo), and old age (photo with his wife).
</Accordion>

## 模型可用性

模型详情和定价请参见[图像模型](/developer-guides/getting-started/image-models)。

## 快速开始

### 前提条件

[获取 API Key](/api-reference/preparation/api-key) 并将其设置为环境变量。如需使用 SDK，请先[安装 SDK](/api-reference/preparation/install-sdk)。

<Note>
  Python SDK 需要 **1.25.15+** 版本，Java SDK 需要 **2.22.13+** 版本。
</Note>

### 示例代码

所有 Qwen-Image 模型都支持同步调用，其中 qwen-image-3.0 系列、`qwen-image-plus` 和 `qwen-image` 还支持异步调用，详见 [Qwen 3.0 异步调用](/api-reference/image-generation/qwen-text-to-image-30-async)和 [Qwen 异步调用](/api-reference/image-generation/qwen-text-to-image-async)。所有 Wan 文生图模型都支持异步调用，其中 `wan2.7-image-pro`、`wan2.7-image`、`wan2.6-image` 和 `wan2.6-t2i` 还支持同步调用。

<Tabs>
  <Tab title="同步调用（Qwen-Image）">
    **请求示例**

    <CodeGroup>
      ```python Python
      import json
      import os
      import dashscope
      from dashscope import MultiModalConversation

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      messages = [
        {
          "role": "user",
          "content": [
            {"text": "画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着 Il Messaggero，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。"}
          ]
        }
      ]

      # 如果未设置环境变量，请将下面一行替换为：api_key="sk-xxx"
      api_key = os.getenv("DASHSCOPE_API_KEY")

      response = MultiModalConversation.call(
        api_key=api_key,
        model="qwen-image-3.0-pro",
        messages=messages,
        result_format='message',
        stream=False,
        watermark=False,
        prompt_extend=True,
        negative_prompt="Low resolution, low quality, distorted limbs, malformed fingers, oversaturated colors, wax-figure appearance, lack of facial detail, excessive smoothness, AI-looking artifacts, chaotic composition, blurry or warped text.",
        size='2048*2048'
      )

      if response.status_code == 200:
        print(json.dumps(response, ensure_ascii=False))
      else:
        print(f"HTTP 状态码: {response.status_code}")
        print(f"错误码: {response.code}")
        print(f"错误信息: {response.message}")
      ```

      ```java Java
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
      import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
      import com.alibaba.dashscope.common.MultiModalMessage;
      import com.alibaba.dashscope.common.Role;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.JsonUtils;
      import com.alibaba.dashscope.utils.Constants;

      import java.io.IOException;
      import java.util.Arrays;
      import java.util.Collections;
      import java.util.HashMap;
      import java.util.Map;

      public class QwenImage {

        static {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        }

        // 如果未设置环境变量，请将下面一行替换为：static String apiKey="sk-xxx"
        static String apiKey = System.getenv("DASHSCOPE_API_KEY");

        public static void call() throws ApiException, NoApiKeyException, UploadFileException, IOException {

          MultiModalConversation conv = new MultiModalConversation();

          MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
              .content(Arrays.asList(
                  Collections.singletonMap("text", "画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着 Il Messaggero，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。")
              )).build();

          Map<String, Object> parameters = new HashMap<>();
          parameters.put("watermark", false);
          parameters.put("prompt_extend", true);
          parameters.put("negative_prompt", "Low resolution, low quality, distorted limbs, malformed fingers, oversaturated colors, wax-figure appearance, lack of facial detail, excessive smoothness, AI-looking artifacts, chaotic composition, blurry or warped text.");
          parameters.put("size", "2048*2048");

          MultiModalConversationParam param = MultiModalConversationParam.builder()
              .apiKey(apiKey)
              .model("qwen-image-3.0-pro")
              .messages(Collections.singletonList(userMessage))
              .parameters(parameters)
              .build();

          MultiModalConversationResult result = conv.call(param);
          System.out.println(JsonUtils.toJson(result));
        }

        public static void main(String[] args) {
          try {
            call();
          } catch (ApiException | NoApiKeyException | UploadFileException | IOException e) {
            System.out.println(e.getMessage());
          }
          System.exit(0);
        }
      }
      ```

      ```bash curl
      curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/multimodal-generation/generation' \
      --header 'Content-Type: application/json' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --data '{
        "model": "qwen-image-3.0-pro",
        "input": {
              "messages": [
          {
                  "role": "user",
                  "content": [
            {
                      "text": "画面是一张竖幅户外人像摄影，整体从上到下呈现温暖的午后街景氛围。顶部左侧到上方大面积被深绿色藤蔓和橙色小花覆盖，花叶从建筑檐口自然垂落，受阳光照射的叶片呈黄绿色高光，阴影处则偏深绿，形成浓密而柔和的背景层次。左上至中上区域是一块深蓝色横向招牌，招牌表面较暗、略带磨砂质感，上面以白色哥特体大字写着 Il Messaggero，文字位于画面左侧偏上，部分被前景花叶轻微遮挡，字体高对比、带装饰性尖角和粗细变化。招牌下方是报刊亭或书报摊的玻璃展示窗，黑色金属框架将橱窗分隔成多个矩形区域，内部陈列着许多报纸、杂志和书刊封面，但大多因景深虚化和光线反射而难以辨读，形成浅色纸张与深色边框交错的背景纹理。画面右上方是强烈的逆光区域，阳光从街道尽头照入，背景建筑被虚化成米灰色块面，边缘柔和，呈现明显的浅景深效果。画面中部偏右是一名年轻成年女性的半身至膝上人像，她回头面向镜头微笑，身体略向右转，肩背朝向观者，姿态自然放松。她有长而浓密的黑色波浪卷发，发丝被逆光勾勒出金色轮廓光，发梢在右侧向外散开，显得轻盈蓬松。她肤色白皙，脸型柔和偏鹅蛋形，眉形细致，眼睛明亮，眼妆清透，睫毛明显，面部带有自然高光，唇部为柔和珊瑚红色，笑容露齿，表情亲切明朗。她佩戴小巧耳饰，身穿黑色细肩带露背连衣裙，面料颜色深黑、轮廓简洁，细肩带从肩部向背部延伸，背部线条清晰。画面下部偏左到中部，她双手抱着一束玫瑰花，花束体积较大，主要由橙色、杏色、粉色和浅桃色玫瑰组成，花瓣层层卷曲，边缘被阳光照亮，绿色叶片和长花茎从花束下方垂出，花束与黑色裙装形成鲜明色彩对比。右侧背景是一条被阳光照亮的城市街道，地面呈暖灰与金黄色调，远处建筑、街边设施和一个模糊的红色圆形交通标志位于右下远景，均因焦外虚化而只保留色块和轮廓。整张照片采用暖色胶片感处理，带有细腻颗粒、柔和对比和明显逆光边缘光，人物位于视觉焦点，背景报刊亭、花藤、街道和阳光共同营造出浪漫、明亮、都市漫步式的氛围。"
            }
                  ]
          }
              ]
        },
        "parameters": {
              "negative_prompt": "Low resolution, low quality, distorted limbs, malformed fingers, oversaturated colors, wax-figure appearance, lack of facial detail, excessive smoothness, AI-looking artifacts, chaotic composition, blurry or warped text.",
              "prompt_extend": true,
              "watermark": false,
              "size": "2048*2048"
        }
      }'
      ```
    </CodeGroup>

    **响应示例**

    <Accordion title="完整 JSON 响应">
      ```json
      {
        "status_code": 200,
        "request_id": "d2d1a8c0-325f-9b9d-8b90-xxxxxx",
        "code": "",
        "message": "",
        "output": {
          "text": null,
          "finish_reason": null,
          "choices": [
            {
              "finish_reason": "stop",
              "message": {
                "role": "assistant",
                "content": [
                  {
                    "image": "https://dashscope-result.oss-cn-shanghai.aliyuncs.com/xxx.png?Expires=xxx"
                  }
                ]
              }
            }
          ]
        },
        "usage": {
          "output_height": 2048,
          "output_width": 2048,
          "input_image_count": 0,
          "input_image_type": "qima_input_2k",
          "output_image_count": 1,
          "output_image_type": "qima_output_2k"
        }
      }
      ```
    </Accordion>
  </Tab>

  <Tab title="异步调用（Wan）">
    **请求示例**

    <Note>
      使用 curl 时，先提交任务（POST），然后使用返回的 `task_id` 查询结果（GET）。`task_id` 的有效期为 24 小时。
    </Note>

    <CodeGroup>
      ```python Python
      import os
      import dashscope
      from dashscope.aigc.image_generation import ImageGeneration
      from dashscope.api_entities.dashscope_response import Message

      dashscope.base_http_api_url = 'https://dashscope.aliyuncs.com/api/v1'

      # 如果未设置环境变量，请将下面一行替换为：api_key="sk-xxx"
      api_key = os.getenv("DASHSCOPE_API_KEY")

      def main():
        message = Message(
          role="user",
          content=[
            {
              "text": "A young woman taking a casual selfie outdoors, natural lighting, warm tones, soft bokeh background with greenery"
            }
          ]
        )

        # 提交异步任务
        print("正在提交异步任务...")
        response = ImageGeneration.async_call(
          model="wan2.7-image-pro",
          api_key=api_key,
          messages=[message],
          enable_sequential=False,
          n=1,
          size="2K"
        )

        if response.status_code == 200:
          print(f"任务已提交，任务 ID: {response.output.task_id}")

          # 等待任务完成
          status = ImageGeneration.wait(task=response, api_key=api_key)

          if status.output.task_status == "SUCCEEDED":
            print("任务完成！")
            print(status)
          else:
            print(f"任务失败，状态: {status.output.task_status}")
        else:
          print(f"任务创建失败: {response.code} - {response.message}")

      if __name__ == "__main__":
        try:
          main()
        except Exception as e:
          print(f"错误: {e}")
      ```

      ```java Java
      import com.alibaba.dashscope.aigc.imagegeneration.*;
      import com.alibaba.dashscope.exception.ApiException;
      import com.alibaba.dashscope.exception.NoApiKeyException;
      import com.alibaba.dashscope.exception.UploadFileException;
      import com.alibaba.dashscope.utils.Constants;
      import com.alibaba.dashscope.utils.JsonUtils;

      import java.util.Collections;

      public class Main {

        static {
          Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
        }

        // 如果未设置环境变量，请将下面一行替换为：apiKey="sk-xxx"
        static String apiKey = System.getenv("DASHSCOPE_API_KEY");

        public static ImageGenerationResult waitTask(String taskId)
            throws ApiException, NoApiKeyException {
          ImageGeneration imageGeneration = new ImageGeneration();
          return imageGeneration.wait(taskId, apiKey);
        }

        public static void asyncCall() throws ApiException, NoApiKeyException, UploadFileException {
          ImageGenerationMessage message = ImageGenerationMessage.builder()
              .role("user")
              .content(Collections.singletonList(
                  Collections.singletonMap("text", "A young woman taking a casual selfie outdoors, natural lighting, warm tones, soft bokeh background with greenery")
              )).build();

          ImageGenerationParam param = ImageGenerationParam.builder()
              .apiKey(apiKey)
              .model("wan2.7-image-pro")
              .messages(Collections.singletonList(message))
              .enableSequential(false)
              .n(1)
              .size("2K")
              .build();

          ImageGeneration imageGeneration = new ImageGeneration();
          ImageGenerationResult taskResult = null;
          try {
            System.out.println("---- 正在提交异步任务 ----");
            taskResult = imageGeneration.asyncCall(param);
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            throw new RuntimeException(e.getMessage());
          }
          System.out.println("任务已创建: " + JsonUtils.toJson(taskResult));

          // 等待任务完成
          String taskId = taskResult.getOutput().getTaskId();
          ImageGenerationResult result = waitTask(taskId);
          System.out.println(JsonUtils.toJson(result));
        }

        public static void main(String[] args) {
          try {
            asyncCall();
          } catch (ApiException | NoApiKeyException | UploadFileException e) {
            System.out.println(e.getMessage());
          }
        }
      }
      ```

      ```bash curl（步骤一：提交任务）
      curl --location 'https://dashscope.aliyuncs.com/api/v1/services/aigc/image-generation/generation' \
      --header 'Content-Type: application/json' \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY" \
      --header 'X-DashScope-Async: enable' \
      --data '{
        "model": "wan2.7-image-pro",
        "input": {
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "text": "A young woman taking a casual selfie outdoors, natural lighting, warm tones, soft bokeh background with greenery"
                }
              ]
            }
          ]
        },
        "parameters": {
          "size": "2K",
          "n": 1,
          "watermark": false,
          "thinking_mode": true
        }
      }'
      ```

      ```bash curl（步骤二：查询结果）
      curl -X GET https://dashscope.aliyuncs.com/api/v1/tasks/{task_id} \
      --header "Authorization: Bearer $DASHSCOPE_API_KEY"
      ```
    </CodeGroup>

    **创建任务响应**

    <Accordion title="完整 JSON 响应">
      ```json
      {
        "output": {
          "task_status": "PENDING",
          "task_id": "0385dc79-5ff8-4d82-bcb6-xxxxxx"
        },
        "request_id": "4909100c-7b5a-9f92-bfe5-xxxxxx"
      }
      ```
    </Accordion>

    **查询结果响应**

    <Accordion title="完整 JSON 响应">
      ```json
      {
        "status_code": 200,
        "request_id": "56e318fd-ed60-99e8-8ca1-cdef25ca4xxx",
        "code": "",
        "message": "",
        "output": {
          "text": null,
          "finish_reason": null,
          "choices": [
            {
              "finish_reason": "stop",
              "message": {
                "role": "assistant",
                "content": [
                  {
                    "image": "https://dashscope-result.oss-cn-shanghai.aliyuncs.com/xxxxxx.png?Expires=xxxxxx",
                    "type": "image"
                  }
                ]
              }
            }
          ],
          "audio": null,
          "task_id": "77093787-a217-4c29-9cd4-ca7b5ac86xxx",
          "task_status": "SUCCEEDED",
          "submit_time": "2026-03-31 23:04:46.166",
          "scheduled_time": "2026-03-31 23:04:46.208",
          "end_time": "2026-03-31 23:05:11.664",
          "finished": true
        },
        "usage": {
          "input_tokens": 720,
          "output_tokens": 11,
          "characters": 0,
          "size": "2048*2048",
          "total_tokens": 731,
          "image_count": 1
        }
      }
      ```
    </Accordion>
  </Tab>
</Tabs>

## 核心能力

### 指令遵循

**参数说明**：

- **Prompt**（必选）：描述期望的内容、风格和构图。传入格式如下：
  - **Qwen-Image、Wan 2.7 和 `wan2.6-t2i`**：通过 `input.messages[].content[].text` 传入。参见[示例代码](#示例代码)中对应标签页的代码。
  - **Wan 2.5 及更早版本**：通过 `input.prompt` 传入。
- **negative\_prompt**（可选）：描述需要从图像中排除的元素，如"模糊"或"多余的手指"。通过 `parameters.negative_prompt` 设置。除 `wan2.7-image-pro` 和 `wan2.7-image` 外，所有模型均支持。
- **文本渲染（画面中的文字）**：模型可在画面中生成中英文文字，但对长文本（如完整古诗、长段落或多行文字）难以逐字精准还原，易出现错字、漏字或形近字替代。如对画面内文字的准确性有要求，建议尽量缩短画面内文字、仅保留关键标题或短语，或对成图中的关键文字进行后期编辑。

<Note>
  `wan2.7-image-pro` 和 `wan2.7-image` **不**支持 `negative_prompt`，请使用正向提示词来引导生成效果。
</Note>

**提示词编写建议**：结构化的提示词通常能产生更好的效果。详见[文生图提示词指南](/developer-guides/accuracy-tuning/image-generation)。

### 启用提示词改写

**参数**：`parameters.prompt_extend`（布尔值，默认：`true`）。

自动扩展简短的提示词以提升图像质量，会增加约 3-4 秒的延迟。

<Note>
  `wan2.7-image-pro` 和 `wan2.7-image` **不**支持 `prompt_extend`，请改用 `thinking_mode`——详见 [Wan 2.7 参数](#wan-2-7-参数)。
</Note>

**使用建议**：

- **启用**：当提示词比较简单或宽泛时，可显著提升生成质量。
- **禁用**（设为 `false`）：当需要精细控制、已编写详细提示词、或对延迟敏感时。

### 选择提示词改写方式

**参数**：`parameters.prompt_extend_mode`（字符串，默认：`direct`）。仅 qwen-image-3.0 系列支持，在 `prompt_extend` 为 `true` 时生效。

| 取值       | 说明                  | 适用场景               |
| -------- | ------------------- | ------------------ |
| `direct` | 直接提示词增强（DPE），默认值    | 大多数场景              |
| `agent`  | 智能体提示词增强（APE），改写更精细 | 提示词很简短、需要模型补充大量细节时 |

<Note>
  `agent` 仅文生图支持，图像编辑场景传入将返回 400 错误。
</Note>

### 设置输出图像分辨率

**参数**：`parameters.size`（字符串），格式为 `"宽*高"`。

| 模型                                | 尺寸格式        | 支持范围                        | 默认值                 | 宽高比       |
| --------------------------------- | ----------- | --------------------------- | ------------------- | --------- |
| qwen-image-3.0 系列                 | 自定义 `"宽*高"` | 512\*512 – 2048\*2048       | 由模型根据提示词自动推荐        | 1:8 – 8:1 |
| qwen-image-2.0 系列                 | 自定义 `"宽*高"` | 512\*512 – 2048\*2048       | 2048\*2048 (1:1)    | —         |
| qwen-image-max / qwen-image-plus  | 仅支持固定预设     | 见下方预设值                      | 1664\*928 (16:9)    | —         |
| `wan2.7-image-pro`                | 简写或 `"宽*高"` | 768\*768 – 4096\*4096       | `"2K"` (2048\*2048) | 1:8 – 8:1 |
| `wan2.7-image`                    | 简写或 `"宽*高"` | 768\*768 – 2048\*2048       | `"2K"` (2048\*2048) | 1:8 – 8:1 |
| `wan2.6-image`                    | 自定义 `"宽*高"` | 768\*768 – 1280\*1280       | 与输入一致（≤1280\*1280）  | 1:4 – 4:1 |
| `wan2.6-t2i`、`wan2.5-t2i-preview` | 自定义 `"宽*高"` | 1280\*1280 – 1440\*1440     | 1280\*1280          | 1:4 – 4:1 |
| wan2.2 及更早的文生图模型                  | 自定义 `"宽*高"` | 单边 \[512, 1440]，≤1440\*1440 | 1024\*1024 (1:1)    | —         |

<Note>
  此处列出的 `wan2.6-image` 仅针对其图文交错生成模式。如需图像编辑功能，请参见[图像编辑](/developer-guides/image-generation/image-editing)。
</Note>

**简写尺寸**（仅限 wan2.7，不可与像素值混用）：

| 简写     | 分辨率        | wan2.7-image-pro | wan2.7-image |
| ------ | ---------- | ---------------- | ------------ |
| `"1K"` | 1024\*1024 | 支持               | 支持           |
| `"2K"` | 2048\*2048 | 支持（默认）           | 支持（默认）       |
| `"4K"` | 4096\*4096 | 支持               | 不支持          |

**各像素范围下的推荐分辨率**：

| 宽高比  | 4K         | 2K         | 1K         |
| ---- | ---------- | ---------- | ---------- |
| 1:1  | 4096\*4096 | 2048\*2048 | 1280\*1280 |
| 16:9 | 4096\*2304 | 2688\*1536 | 1696\*960  |
| 9:16 | 2304\*4096 | 1536\*2688 | 960\*1696  |
| 4:3  | 4096\*3072 | 2368\*1728 | 1472\*1104 |
| 3:4  | 3072\*4096 | 1728\*2368 | 1104\*1472 |

- **4K**：仅 wan2.7-image-pro 支持。
- **2K**：wan2.7-image-pro、wan2.7-image、qwen-image-2.0/3.0 系列。
- **1K**：Wan 文生图模型。

**qwen-image-max / qwen-image-plus 固定分辨率**：1664\*928（16:9，默认）、1472\*1104（4:3）、1328\*1328（1:1）、1104\*1472（3:4）、928\*1664（9:16）。

### 设置生成图片数量

**参数**：`parameters.n`（整数）。

| 模型                                      | 范围    | 默认值 |
| --------------------------------------- | ----- | --- |
| wan2.7（`enable_sequential=false`）       | 1–4   | 4   |
| wan2.7（`enable_sequential=true`）        | 1–12  | 12  |
| qwen-image-2.0/3.0 系列                   | 1–6   | 1   |
| qwen-image-max / qwen-image-plus        | 仅支持 1 | 1   |
| wan2.6-image（`enable_interleave=false`） | 1–4   | 4   |
| wan2.6-image（`enable_interleave=true`）  | 仅支持 1 | 1   |
| wan2.6-t2i / wan2.5 及更早版本               | 1–4   | 4   |

<Note>
  费用 = 单价 x 成功生成的图片数。测试阶段建议将 `n` 设为 1。
</Note>

使用 `wan2.6-image` 的图文交错模式（`enable_interleave=true`）时，`n` 必须为 1。如需控制最大生成图片数，请使用 `parameters.max_images`（范围：1–5，默认：5）。实际生成数量由模型决定，可能少于指定的最大值。

### Wan 2.7 参数

以下参数仅适用于 `wan2.7-image-pro` 和 `wan2.7-image`。

- **`enable_sequential`**（布尔值，默认：`false`）：启用图集生成。设为 `true` 时，可将 `n` 设为 1-12，单次请求生成多张风格一致的图片。

  <Warning>
    `enable_sequential` 设为 `true` 时，`thinking_mode` 和 `color_palette` 不可用。
  </Warning>

- **`thinking_mode`**（布尔值，默认：`true`）：启用增强推理，提升提示词理解能力和图像质量。仅在 `enable_sequential` 为 `false` 时可用。

- **`color_palette`**（数组）：自定义配色方案。指定 3-10 种颜色（推荐 8 种），每种颜色包含十六进制色值和占比（百分比字符串），所有占比之和必须为 100%。仅在 `enable_sequential` 为 `false` 时可用。

<Accordion title="配色方案示例">
  ```json
  "color_palette": [
    {"hex": "#C2D1E6", "ratio": "23.51%"},
    {"hex": "#CDD8E9", "ratio": "20.13%"},
    {"hex": "#B5C8DB", "ratio": "15.88%"},
    {"hex": "#C0B5B4", "ratio": "13.27%"},
    {"hex": "#DAE0EC", "ratio": "10.11%"},
    {"hex": "#636574", "ratio": "8.93%"},
    {"hex": "#CACAD2", "ratio": "5.55%"},
    {"hex": "#CBD4E4", "ratio": "2.62%"}
  ]
  ```
</Accordion>

## 结合 OpenAI Agents SDK 使用

千问-文生图（Qwen-Image）等图像生成模型通过 DashScope 原生接口调用，不支持 OpenAI 兼容（compatible-mode）模式，因此无法直接作为 OpenAI Agents SDK 中 Agent 的推理模型。

在 OpenAI Agents SDK 等智能体框架中，可将图像生成能力封装为工具（function tool），由支持 OpenAI 兼容模式的文本对话模型（如 qwen-plus）作为 Agent 的推理核心进行调度。示例如下：

运行前请先安装依赖：`pip install openai-agents dashscope`。

```python
import os
import asyncio
import dashscope
from openai import AsyncOpenAI
from dashscope import MultiModalConversation
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel

# 从环境变量读取千问AI平台 API Key（若未配置，可直接替换为 api_key="sk-xxx"）
API_KEY = os.getenv("DASHSCOPE_API_KEY")
# 图像生成模型通过 DashScope 原生接口调用
dashscope.base_http_api_url = "https://dashscope.aliyuncs.com/api/v1"
# 文本对话模型（Agent 推理核心）通过 OpenAI 兼容模式接入
client = AsyncOpenAI(api_key=API_KEY, base_url="https://dashscope.aliyuncs.com/compatible-mode/v1")

# 将图像生成封装为工具（function tool），供 Agent 调用
@function_tool
def generate_image(prompt: str) -> str:
  """根据文本描述生成一张图片并返回图片 URL。prompt：图片内容的文字描述。"""
  rsp = MultiModalConversation.call(
    api_key=API_KEY,
    model="qwen-image",
    messages=[{"role": "user", "content": [{"text": prompt}]}],
    result_format="message",
  )
  if rsp.status_code != 200:
    return f"生成失败：{rsp.code} {rsp.message}"
  return rsp.output.choices[0].message.content[0]["image"]

agent = Agent(
  name="图像生成助手",
  instructions="你是图像生成助手。当用户想要图片时，调用 generate_image 工具，并把返回的图片 URL 告诉用户。",
  model=OpenAIChatCompletionsModel(model="qwen-plus", openai_client=client),
  tools=[generate_image],
)

async def main():
  result = await Runner.run(agent, "帮我画一只在草地上奔跑的柯基犬")
  print(result.final_output)

if __name__ == "__main__":
  asyncio.run(main())
```

## 上线注意事项

### 容错处理

- **限流**：`Throttling` 错误码或 HTTP 429 表示触发了限流。详见[限流](/developer-guides/administration/rate-limits)。
- **异步任务轮询**：前 30 秒每 3 秒轮询一次，之后逐步延长间隔。设置最终超时时间（如 2 分钟），超时后将任务视为失败。

### 风险防范

- **结果持久化**：图片 URL 在 24 小时后过期。获取结果后应立即下载并存储到自有存储服务（如 OSS）。
- **内容审核**：所有 `prompt` 和 `negative_prompt` 输入都会经过内容审核。不合规的输入会被拦截，返回 `DataInspectionFailed` 错误。
- **版权与合规**：提示词中引用品牌商标、名人肖像或受版权保护的 IP 可能存在侵权风险，由此产生的法律责任由用户自行承担。

## API 参考

- [Qwen - 同步调用](/api-reference/image-generation/qwen-text-to-image)
- [Z-Image](/api-reference/image-generation/z-image)
- [Wan 2.7 - 图像生成与编辑](/api-reference/image-generation/wan27-image-gen-edit/create-task)
- [Wan 2.6 - 图像生成与编辑](/api-reference/image-generation/wan26-image-gen-edit/create-task)
- [Wan - 文生图 V2](/api-reference/image-generation/wan-text-to-image-v2/create-task)

## 错误码

调用失败时，请参见[错误信息](/api-reference/preparation/error-messages)。
