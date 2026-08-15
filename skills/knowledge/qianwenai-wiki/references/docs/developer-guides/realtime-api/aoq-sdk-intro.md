> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# SDK简介

> AOQ SDK 平台支持与架构概述

AOQ SDK 面向实时多模态场景，帮助开发者基于 Realtime API 快速搭建实时交互应用。

## API设计与回调机制

AOQ SDK 采用声明式 API 设计：您只需通过 API 设置期望的目标状态，SDK 会自动判断当前状态并在适当时机完成切换，同时通过回调实时反馈执行进度。无需关心具体的调用时机，也无需重复调用。

## 异常处理机制

AOQ SDK 在遇到异常时会自动尝试恢复，仅在无法自行恢复时才通过回调通知开发者介入处理。无法恢复的错误主要分为两类：物理限制（如网络中断、音视频设备故障、CPU 或内存不足）和外部因素（如 Token 无效）。

## 下载指南

AOQ SDK 为自研产品，请通过官网下载，详情请参见[SDK下载](/developer-guides/realtime-api/sdk-download)。
