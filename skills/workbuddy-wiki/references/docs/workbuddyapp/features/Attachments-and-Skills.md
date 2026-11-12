# 添加附件与更多功能

## 概览

点击输入栏**左侧的 + 按钮**，展开工具面板：

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-1.B-7QC7Qo.png)

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-2.B0ByURll.png)

**工具面板功能一览：**

| 入口 | 功能 | 适用场景 |
| --- | --- | --- |
| **拍照** | 调用手机摄像头实时拍照 | 拍摄纸质文档、白板笔记、发票、名片等 |
| **照片/视频** | 从手机相册选择已有图片和视频 | 处理已保存的截图、照片和视频 |
| **手机文件** | 从本机文件管理选择文件 | 上传 Excel、Word、PDF、TXT 等文件 |
| **腾讯文档** | 从已连接的腾讯文档中选择文件 | 支持读取腾讯文档中的所有文件 |
| **定时任务** | 设置定时或周期性自动任务 | 每日资讯推送、定期报告生成等 |
| **专家中心** | 浏览和发起专家对话 | 专业领域任务的精细化处理 |

## 拍照

点击 **拍照** 后，会请求相机权限（首次使用时），授权后进入拍照界面。

- **每次拍摄 1 张照片** ，拍摄完成后自动返回对话界面
- 照片会显示在输入框上方，点击 × 可移除
- 如需拍摄多张，需再次点击 **+** → **拍照** 重复操作

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-3.B8FBT8hd.png)

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-4.BmGAMlUA.png)

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-5.ZYnfZiDe.png)

>
> **⚠️ 注意**：使用拍照或照片功能时，建议选择带「视觉」标签的模型（如 DeepSeek-V4-Flash、Kimi-K2.5 等），否则 AI 无法理解图片内容。

## 照片/视频

点击 **照片/视频** 后，会请求相册访问权限（首次使用时），授权后进入相册选择界面。

- **支持一次选择多张图片（最多 5 张）**
- 选中的图片显示在输入框上方，可逐张预览和删除
- 支持常见图片格式：JPG、PNG 等

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-6.Bgcs97AT.png)

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-7.DKmWlq_U.png)

![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-8.EviPAcd1.png)

**拍照 vs 照片 对比：**

| 对比维度 | 拍照 | 照片 |
| --- | --- | --- |
| **来源** | 实时拍摄 | 手机相册 |
| **数量** | 每次 1 张 | 支持多选（最多 5 张） |
| **适用场景** | 临时拍 1 张快速识别 | 已拍好多张，批量上传 |

>
> **推荐做法**：需要多张图片时，先用手机自带相机拍完，再通过「照片」一次性选择上传。

## 手机文件

点击 **手机文件** 后，会调用系统文件选择器：

1. 浏览手机上的文件夹和文件
2. 选择目标文件，点击确认
3. 文件将添加到输入框上方，点击发送即可

**支持的文件类型：**

| 类型 | 格式 |
| --- | --- |
| **表格** | .xlsx、.xls、.csv |
| **文档** | .docx、.doc、.txt |
| **PDF** | .pdf |
| **图片** | .jpg、.png、.gif |

## 腾讯文档

App 登录后自动连接相同账号的腾讯文档。未连接时，按以下流程操作：

1. 点击 **腾讯文档** ![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-9.BWs78Yfd.png)
2. 勾选同意协议后，点击**同意**授权完成连接 ![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-10.Bq3UdXb5.png)
3. 选择目标文件，点击**添加**引用到当前对话 ![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-11.U6ag5wh9.png) ![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-12.D6nMGsNO.png)

## 定时任务

通过工具面板可快速设置定时或周期性自动任务：

1. 点击 **定时任务**，进入定时任务设置页面
2. 描述需要自动执行的任务内容
3. 设置执行频率（每天、每周、每月等）和执行时间
4. 保存后，WorkBuddy 将在设定时间自动执行 例如："每天早上 9 点推送昨日 AI 行业新闻摘要"、"每周五下午 5 点生成本周工作总结" ![](https://download.codebuddy.cn/web/docs/729f1aaad145b1c8092712d0da1c125fe9ebc748/docs/static/skill-13.DaNSxZFO.png)

## 专家

点击 **专家** 可浏览不同专业领域的专家，发起针对性对话：

- 按行业分类浏览专家
- 查看专家擅长领域和介绍
- 一键发起专家对话

>
> 详见 [侧边栏 - 专家](./Expert#专家)
