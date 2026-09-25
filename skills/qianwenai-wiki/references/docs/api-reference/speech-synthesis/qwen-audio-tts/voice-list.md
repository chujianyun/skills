> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Qwen-Audio-TTS 音色列表

> qwen-audio-3.0-tts-plus 与 qwen-audio-3.0-tts-flash 支持的系统音色与基础音色列表

Qwen-Audio-TTS 支持的系统音色如下表所示。除系统音色外，还提供通过声音复刻预先生成的基础音色，详情请参见[基础音色列表](#base-voices)。若需要更加个性化的音色，也可通过声音复刻功能免费定制专属音色，详情请参见[使用复刻的音色进行语音合成](/api-reference/speech-synthesis/voice-cloning/overview)。

进行语音合成时：

- 每个模型（`model`）仅支持一组特定的音色（`voice`），不能将一个模型的音色与另一个模型混用。如果所填音色不在当前模型支持的音色列表中，服务将返回 `InvalidParameter` 错误（例如 `[cosyvoice:]Engine error [411]: TTS speak operation failed`）；此时请对照下方对应模型的音色列表，确认所填 voice 在当前 model 的支持范围内。
- 待合成文本（`text`）必须在所选音色支持的语言范围内，否则可能出现发音错误或语音不自然。

## qwen-audio-3.0-tts-plus 系统音色列表

| 场景         | 音色名称 | 音色参数            | 特质    | 年龄  | 性别 | 语言         | 试听                                                                                                                                |
| ---------- | ---- | --------------- | ----- | --- | -- | ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 社交陪伴（旗舰音色） | 龙安灵心 | `longanlingxin` | 知心温暖音 | 25岁 | 女  | 中文（普通话）、英文 | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/deqsie/01_longanlingxin.wav" controls /> |
| 社交陪伴（旗舰音色） | 龙安鲁风 | `longanlufeng`  | 明亮开朗音 | 25岁 | 男  | 中文（普通话）、英文 | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/tpgsdv/02_longanlufeng.wav" controls />  |

## qwen-audio-3.0-tts-flash 系统音色列表

| 场景              | 音色名称      | 音色参数                | 特质     | 年龄  | 性别 | 语言         | 试听                                                                                                                                |
| --------------- | --------- | ------------------- | ------ | --- | -- | ---------- | --------------------------------------------------------------------------------------------------------------------------------- |
| 社交陪伴（精品中文）      | 龙安风悦      | `longanfengyue`     | 自然亲切音  | 30岁 | 女  | 中文（普通话）、英文 | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/djxajf/03_longanfengyue.wav" controls /> |
| 社交陪伴（精品中文）      | 龙安元妃      | `longanyuanfei`     | 高傲妃子音  | 30岁 | 女  | 中文（普通话）、英文 | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/lnyaxv/04_longanyuanfei.wav" controls /> |
| 社交陪伴（精品中文）      | 龙安灵希      | `longanlingxi`      | 可爱甜美音  | 25岁 | 女  | 中文（普通话）、英文 | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/pfkypj/05_longanlingxi.wav" controls />  |
| 社交陪伴（精品中文）      | 龙安小昕      | `longanxiaoxin`     | 亲切活泼音  | 22岁 | 女  | 中文（普通话）、英文 | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/msjxqk/07_longanxiaoxin.wav" controls /> |
| 社交陪伴（精品中文）      | 龙安欢       | `longanhuan_v3.6`   | —      | 25岁 | 女  | 中文（普通话）、英文 | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/glwaer/09_longanhuan.wav" controls />    |
| 儿童陪伴/智能玩具（精品儿童） | 龙杰力豆      | `longjielidou_v3.6` | 天真男童   | 5岁  | 男  | 中文（普通话）、英文 | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/wirytn/08_longjielidou.wav" controls />  |
| 儿童陪伴/智能玩具（精品儿童） | 龙泡泡       | `longpaopao_v3.6`   | 软糯可爱音  | 5岁  | 女  | 中文（普通话）、英文 | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/nrgkjo/13_longpaopao.wav" controls />    |
| 角色音/游戏（精品中文）    | 龙火火       | `longhuohuo_v3.6`   | 顽皮少年音  | 8岁  | 男  | 中文（普通话）、英文 | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/efdgqh/11_longhuohuo.wav" controls />    |
| 角色音/游戏（精品中文）    | 龙川叔       | `longchuanshu_v3.6` | 川普大叔音  | 40岁 | 男  | 中文（普通话）、英文 | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/makxfd/12_longchuanshu.wav" controls />  |
| 社交陪伴/语音助手（精品英文） | loongmary | `loongmary`         | 温暖英音   | 20岁 | 女  | 英文         | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/wpitzn/01_loongmary.wav" controls />     |
| 社交陪伴/语音助手（精品英文） | loongeva  | `loongeva_v3.6`     | 高智美音   | 28岁 | 女  | 英文         | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/xajwqw/02_loongeva.wav" controls />      |
| 社交陪伴/语音助手（精品英文） | loongJohn | `loongjohn`         | 沉稳亲切美音 | 28岁 | 男  | 英文         | <audio src="https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260706/pwxpto/03_loongjohn_1.wav" controls />   |

<a id="base-voices" />

## 基础音色列表

除上述系统音色外，`qwen-audio-3.0-tts-plus` 和 `qwen-audio-3.0-tts-flash` 各自还提供 500 余个通过声音复刻生成的基础音色，调用方式与系统音色一致。基础音色命名格式为 `qwen-audio-3.0-tts-{plus|flash}-{音色后缀}`，两个模型同一后缀对应同一套试听音频。完整音色列表请下载下方 Excel 查看：

- `qwen-audio-3.0-tts-plus` 基础音色列表（Excel）：[qwen-audio-3.0-tts-plus基础音色.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260723/ydwqqz/qwen-audio-3.0-tts-plus%E5%9F%BA%E7%A1%80%E9%9F%B3%E8%89%B2.xlsx)
- `qwen-audio-3.0-tts-flash` 基础音色列表（Excel）：[qwen-audio-3.0-tts-flash基础音色.xlsx](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260723/thosjr/qwen-audio-3.0-tts-flash%E5%9F%BA%E7%A1%80%E9%9F%B3%E8%89%B2.xlsx)
- 基础音色试听音频包（plus 和 flash 共用）：[基础音色试听音频包.zip](https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20260720/tuuuqo/%E5%9F%BA%E7%A1%80%E9%9F%B3%E8%89%B2%E8%AF%95%E5%90%AC%E9%9F%B3%E9%A2%91%E5%8C%85.zip)

**试听步骤**：

1. 下载 Excel 和试听音频包，将音频包解压到本地。
2. 在 Excel 中找到"预览音频文件名"列，获取音频文件名。
3. 在解压目录中找到对应文件，使用播放器打开试听。
