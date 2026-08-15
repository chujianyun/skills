> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 录音文件识别最佳实践

> 使用 ffmpeg 对视频文件进行预处理，提取音轨并压缩，从而加快 Paraformer 录音文件识别的吞吐效率。

虽然 Paraformer 语音识别 API 可以兼容视频文件，但由于视频文件尺寸通常较大、传输较为耗时，建议对其进行预处理，仅提取需要进行语音识别的音轨，并进行合理压缩，从而显著降低文件尺寸。这样做将大大加快视频文件转写的吞吐效率。以下展示了如何使用 ffmpeg 进行相关预处理。

## 前提条件

安装 ffmpeg：请前往 [ffmpeg 官方网站](https://ffmpeg.org/) 下载并安装。

## 预处理视频文件

使用 ffmpeg 提取视频文件中的第一条音轨、降采样到 16kHz、并压缩编码为 opus 文件。

```shell
ffmpeg -i input-video-file -ac 1 -ar 16000 -acodec libopus output-audio-file.opus
```

一般情况下，输出的音频文件将显著小于输入视频文件的尺寸。之后可向文件转写 API 提交该音频文件（以 URL 指定），获得语音识别结果。
