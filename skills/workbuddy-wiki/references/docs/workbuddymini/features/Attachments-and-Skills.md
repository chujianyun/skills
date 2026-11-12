# 添加附件与技能

## 概览

点击输入栏**左侧的 + 按钮**，展开工具面板：

![工具面板](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/attachments-1.DE74-ZoI.png)

| 入口 | 功能 | 适用场景 |
| --- | --- | --- |
| **摄像头** | 调用手机摄像头实时拍照 | 拍摄纸质文档、白板笔记、发票、名片等 |
| **照片 / 视频** | 从手机相册选择已有图片和视频 | 处理已保存的截图、照片和视频 |
| **手机文件** | 从本机文件管理选择文件 | 上传 Excel、Word、PDF、TXT 等文件 |
| **微信文件** | 从微信聊天记录选择文件 | 上传 Excel、Word、PDF、TXT 等文件 |
| **腾讯文档** | 从已连接的腾讯文档中选择文件 | 支持读取腾讯文档中的所有文件 |
| **添加技能（Skills）** | 为当前对话启用技能包 | 需要 PPT 制作、海报生成、xlsx 处理等特定能力 |
| **ima 知识库** | 访问已连接的 ima 知识库 | 搜索、选文件、一键派活、产出回传，全流程在手机上完成 |

## 摄像头

点击 **摄像头** 后，调用手机摄像头进行拍照。

- **每次拍摄 1 张照片** ，拍摄完成后自动返回对话界面
- 照片会显示在输入框上方，点击 × 可移除
- 如需拍摄多张，需再次点击 **+** → **摄像头** 重复操作

![摄像头拍照](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image23.BvFbeSyw.png)

> **Tip: **注意：****
>
> **使用摄像头或照片功能时，建议选择带「视觉」标签的模型（如 MiniMax-M2.7 或 Kimi-K2.5），否则 AI 无法理解图片内容。**

## 照片/视频

点击 **照片/视频** 后，进入手机相册选择界面。

- **支持一次选择多张图片（最多 5 张）**
- 选中的图片显示在输入框上方，可逐张预览和删除
- 支持常见图片格式：JPG、PNG 等

![选择照片](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image24.DLVo-FTV.png)

**摄像头 vs 照片**

|  | 摄像头 | 照片 |
| --- | --- | --- |
| **来源** | 实时拍摄 | 手机相册 |
| **数量** | 每次 1 张 | 支持多选（最多 5 张） |
| **适用场景** | 临时拍 1 张快速识别 | 已拍好多张，批量上传 |

> **Note: **推荐做法**：**
>
> 需要多张图片时，先用手机自带相机拍完，再通过「照片」一次性选择上传。

## 文件

WorkBuddy小程序 支持添加本地文件、微信聊天中的文件、腾讯文档和ima 知识库。

### 文档和知识库

打开WorkBuddy小程序自动连接相同账号的腾讯文档、IMA 知识库。未连接可通过以下流程连接：

1. 点击 **腾讯文档 / IMA 知识库** 前往小程序：

![腾讯文档小程序](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/attachments-2.RfvayaUA.png)

1. 勾选已阅读并同意协议后，点击 **同意** 授权完成连接：

![腾讯文档小程序](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/attachments-3.D3u8yZC7.png)

1. 选择 **腾讯文档 / IMA 知识库** 中的文件，点击 **添加** 在新建对话中引用目标文件：

![腾讯文档小程序](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/attachments-4.BVHFJ4qd.png)

**支持的文件类型：**

| 类型 | 格式 |
| --- | --- |
| **表格** | .xlsx、.xls、.csv |
| **文档** | .docx、.doc、.txt |
| **PDF** | .pdf |
| **图片** | .jpg、.png、.gif |
| **其他** | 根据连接 文档/知识库 支持情况而定 |

## 技能

技能是 WorkBuddy 的扩展能力包，用于执行特定类型的任务。选中的技能会在当前对话中生效。

点击 **添加技能** 后，打开技能选择面板。

![技能选择面板](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image26.D13aEEhR.png)

### 1）什么时候需要手动添加技能？

如果你希望明确指定使用某个技能，或者 AI 没有自动启用你需要的技能，可以通过此入口手动添加。

### 2）如何安装更多技能？

如果技能列表中没有你需要的技能，可以通过 **SkillHub** 获取更多：[SkillHub - 专为中国用户优化的 Skills 社区](https://skillhub.tencent.com/)，搜索所需 Skill 后复制其**安装指令**，将安装指令粘贴至 WorkBuddy 对话框中发送即可，安装成功后即可在技能列表中使用。

![安装技能](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/image27.FdJyBnD6.png)
