> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创建部署

> 在千问AI平台上部署自定义模型，为生产工作负载创建专属推理服务。

千问AI平台部署为模型提供专属推理服务，支持部署官方模型和自定义模型。部署后通过独立端点调用，享有资源独占、性能可配置等能力。

## 前提条件

- 一个千问AI平台账号。请登录[控制台](https://platform.qianwenai.com)。
- 可部署的模型：官方模型（如 Qwen 系列、DeepSeek、GLM 等）或通过微调任务发布的[自定义模型](/developer-guides/custom-models/overview)。

## 创建部署

前往[部署页面](https://platform.qianwenai.com/home/model-production/deployments)，点击**创建部署**打开向导。

### 1. 基本信息

- **部署名称**：输入名称以标识此部署。
- **选择模型**：从下拉菜单中选择可部署的模型。
- **模型代码**：查看并可选自定义 API 调用时使用的模型代码后缀。

### 2. 配置

可用的计费方式取决于所选模型，具体请在[创建部署](https://platform.qianwenai.com/home/model-production/deployments/create)时查看。

| 计费方式           | 说明                              | 付费类型               | 计费公式                                           |
| -------------- | ------------------------------- | ------------------ | ---------------------------------------------- |
| **按 Token 计费** | 按实际消耗量计费，不使用不计费。仅支持部分 LoRA 微调模型 | 按量付费               | `输入 Token × 输入单价 + 输出 Token × 输出单价`            |
| **按模型单元（MU）**  | 资源独占，性能可配置。适合生产环境稳定算力需求         | 按量付费（按小时）/ 预付费（按月） | `模型单元数量 × 单价（元/小时）`                            |
| **按预置吞吐（PTU）** | 预留吞吐保障，额度内不限速。适合高并发低延迟场景        | 按量付费（按小时）/ 预付费（按天） | `输入 kTPM × 输入单价 + 输出 kTPM × 输出单价（元/(kTPM·小时)）` |

#### 按模型单元（MU）计费配置

选择 MU 计费后，需额外配置：

- **部署模板**：选择部署模板，不同模板对应不同的模型单元类型和资源配置。
- **部署副本数**：设置副本数量，总模型单元 = 单副本模型单元 × 副本数。

<Note>
  模型单元（MU）部署的配额需联系客服或商务申请后提供。若创建部署时提示配额不足，请联系客服或您的商务对接人开通相应配额。
</Note>

#### 按预置吞吐（PTU）计费配置

选择 PTU 计费后，需配置输入和输出吞吐额度（单位 kTPM）：

- 按量付费：按实际使用时长计费。
- 预付费：选择购买时长，可开启自动续费。

<Note>
  部署创建后计费方式不可更改。如需切换，请删除部署并重新创建。
</Note>

### 3. 费用估算

审核费用估算——计费方式、付费类型和预估价格——然后点击**创建部署**提交。

<Warning>
  部署一旦达到**运行中**状态即开始计费，即使尚未发送任何推理请求。
</Warning>

## 创建后

提交后，部署进入**部署中**状态。配置通常需要几分钟。当状态变为**运行中**时，部署即可接收推理请求。您可以在部署列表点击**试用**，直接在控制台发送测试请求验证效果，无需编写代码。

## 调用已部署的模型

将部署的**模型代码**作为 chat completions API 的 `model` 参数。在[部署页面](https://platform.qianwenai.com/home/model-production/deployments)的部署名称下方找到模型代码。

<Tabs>
  <Tab title="OpenAI-compatible (Python)">
    ```python
    import os
    from openai import OpenAI

    client = OpenAI(
      api_key=os.getenv("DASHSCOPE_API_KEY"),
      base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )

    completion = client.chat.completions.create(
      model="your-deployment-model-code",  # 替换为您的模型代码
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing in simple terms."},
      ],
    )
    print(completion.choices[0].message.content)
    ```
  </Tab>

  <Tab title="curl">
    ```bash
    curl "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" \
      -H "Authorization: Bearer $DASHSCOPE_API_KEY" \
      -H "Content-Type: application/json" \
      -d '{
        "model": "your-deployment-model-code",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Explain quantum computing in simple terms."}
        ]
      }'
    ```
  </Tab>
</Tabs>

## 下一步

- [管理部署](/developer-guides/deployment/manage-deployments) -- 监控、停止和删除您的部署。
