> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 定制热词 HTTP API

> 通过HTTP API管理定制热词列表，包括创建、查询、更新和删除热词列表。

**用户指南：**[定制热词](/developer-guides/speech/improve-recognition-accuracy)。

## 服务端点

```
POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization
```

## 请求头

| 参数            | 类型     | 是否必选 | 说明                                   |
| ------------- | ------ | ---- | ------------------------------------ |
| Authorization | string | 是    | 鉴权令牌，格式为`Bearer $DASHSCOPE_API_KEY`。 |
| Content-Type  | string | 是    | 请求体的媒体类型，固定为`application/json`。      |

## 创建热词列表

### 请求体

**model** *string* **（必选）**

定制热词模型，固定为`speech-biasing`。

**input** *object* **（必选）**

输入参数对象。

<Expandable title="属性">
  **action** *string* **（必选）**

  操作类型，固定为`create_vocabulary`。

  **target\_model** *string* **（必选）**

  使用热词列表的语音识别模型，必须与后续调用语音识别接口时使用的模型一致。

  **prefix** *string* **（必选）**

  热词列表自定义前缀，仅允许数字和小写字母，长度不超过10个字符。

  **vocabulary** *array\[object]* **（必选）**

  热词列表数组。

  <Expandable title="属性">
    **text** *string* **（必选）**

    热词文本。

    热词文本的语言必须在所选模型的支持范围内，不同模型支持的语言各不相同。

    热词用于提升识别的准确率，请使用实际词语而非任意字符组合。

    长度限制：含非 ASCII 字符时不超过 15 个字符；纯 ASCII 时空格分隔片段不超过 7 个。

    **weight** *integer* **（必选）**

    热词权重。常用值：4。

    取值范围：\[1, 5]。

    如果效果不明显，可以适当增加权重，但权重过大可能产生负面效果，导致其他词语识别不准确。

    **lang** *string* （可选）

    待识别音频的语言代码。设置后，系统将对指定语种进行热词识别增强。如果无法提前确定语种，可不设置，模型会自动识别语种。

    取值范围（因模型而异）：

    - Paraformer：zh（中文）、en（英文）、ja（日语）、yue（粤语）、ko（韩语）、de（德语）、fr（法语）、ru（俄语）
    - Fun-ASR：zh（中文）、en（英文）、ja（日语）
  </Expandable>
</Expandable>

### 请求示例

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "speech-biasing",
    "input": {
        "action": "create_vocabulary",
        "target_model": "fun-asr",
        "prefix": "testpfx",
        "vocabulary": [
          {"text": "赛德克巴莱", "weight": 4}
        ]
    }
}'
```

### 返回体

**request\_id** *string*

本次调用的唯一标识符。

**output** *object*

模型返回的数据。

<Expandable title="属性">
  **vocabulary\_id** *string*

  创建的热词列表ID。
</Expandable>

**usage** *object*

本次请求用量信息。

<Expandable title="属性">
  **count** *integer*

  创建的热词列表数量，固定为1。
</Expandable>

### 返回示例

```json
{
  "output": {
    "vocabulary_id": "vocab-testpfx-5112c3de3705486baxxxxxxx"
  },
  "usage": {
    "count": 1
  },
  "request_id": "aee47022-2352-40fe-acfa-xxxx"
}
```

## 批量查询热词列表

### 请求体

**model** *string* **（必选）**

定制热词模型，固定为`speech-biasing`。

**input** *object* **（必选）**

输入参数对象。

<Expandable title="属性">
  **action** *string* **（必选）**

  操作类型，固定为`list_vocabulary`。

  **prefix** *string* （可选）

  热词列表自定义前缀，如果设定则只返回指定前缀的热词列表。

  **page\_index** *integer*

  页码索引，从0开始计数。

  默认值：0。

  **page\_size** *integer*

  每页包含数据条数。

  默认值：10。
</Expandable>

### 请求示例

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "speech-biasing",
    "input": {
        "action": "list_vocabulary",
        "prefix": "testpfx",
        "page_index": 0,
        "page_size": 10
    }
}'
```

### 返回体

**request\_id** *string*

本次调用的唯一标识符。

**output** *object*

模型返回的数据。

<Expandable title="属性">
  **vocabulary\_list** *array\[object]*

  查询到的热词列表。

  <Expandable title="属性">
    **vocabulary\_id** *string*

    热词列表ID。

    **gmt\_create** *string*

    创建时间。

    **gmt\_modified** *string*

    修改时间。

    **status** *string*

    状态：

    - OK：可调用
    - UNDEPLOYED：不可调用
  </Expandable>
</Expandable>

**usage** *object*

本次请求用量信息。

<Expandable title="属性">
  **count** *integer*

  固定为1。
</Expandable>

### 返回示例

```json
{
  "output": {
    "vocabulary_list": [
      {
        "gmt_create": "2026-03-02 18:07:38",
        "gmt_modified": "2026-03-02 18:07:38",
        "status": "OK",
        "vocabulary_id": "vocab-ciotest-8e74bef2accf4xxxxxxxx"
      },
      {
        "gmt_create": "2026-02-27 19:04:48",
        "gmt_modified": "2026-02-28 13:40:40",
        "status": "OK",
        "vocabulary_id": "vocab-sifasr-f483ad46e1844fxxxxxxxx"
      }
    ]
  },
  "usage": {
    "count": 1
  },
  "request_id": "81d51a05-8cdd-45c0-973f-xxxxxxxx"
}
```

## 查询热词列表

### 请求体

**model** *string* **（必选）**

定制热词模型，固定为`speech-biasing`。

**input** *object* **（必选）**

输入参数对象。

<Expandable title="属性">
  **action** *string* **（必选）**

  操作类型，固定为`query_vocabulary`。

  **vocabulary\_id** *string* **（必选）**

  需要查询的热词列表ID。
</Expandable>

### 请求示例

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "speech-biasing",
    "input": {
        "action": "query_vocabulary",
        "vocabulary_id": "vocab-testpfx-xxxx"
    }
}'
```

### 返回体

**request\_id** *string*

本次调用的唯一标识符。

**output** *object*

模型返回的数据。

<Expandable title="属性">
  **gmt\_create** *string*

  创建时间。

  **gmt\_modified** *string*

  修改时间。

  **status** *string*

  状态：

  - OK：可调用
  - UNDEPLOYED：不可调用

  **target\_model** *string*

  使用热词列表的语音识别模型，必须与后续调用语音识别接口时使用的模型一致。

  **vocabulary** *array\[object]*

  查询到的热词列表。

  <Expandable title="属性">
    **text** *string*

    热词文本。

    **weight** *integer*

    热词权重。

    **lang** *string*

    待识别音频语种。
  </Expandable>
</Expandable>

**usage** *object*

本次请求用量信息。

<Expandable title="属性">
  **count** *integer*

  固定为1。
</Expandable>

### 返回示例

```json
{
  "output": {
    "gmt_create": "2025-12-19 11:47:11",
    "gmt_modified": "2025-12-19 11:47:11",
    "status": "OK",
    "target_model": "fun-asr",
    "vocabulary": [
      {
        "lang": "zh",
        "text": "赛德克巴莱",
        "weight": 4
      }
    ]
  },
  "usage": {
    "count": 1
  },
  "request_id": "3d461d3f-b2c4-4de5-xxxx"
}
```

## 更新热词列表

### 请求体

**model** *string* **（必选）**

定制热词模型，固定为`speech-biasing`。

**input** *object* **（必选）**

输入参数对象。

<Expandable title="属性">
  **action** *string* **（必选）**

  操作类型，固定为`update_vocabulary`。

  **vocabulary\_id** *string* **（必选）**

  需要更新的热词列表ID。

  **vocabulary** *array\[object]* **（必选）**

  新的热词列表，将完全替换原有内容。

  <Expandable title="属性">
    **text** *string* **（必选）**

    热词文本。

    热词文本的语言必须在所选模型的支持范围内，不同模型支持的语言各不相同。

    热词用于提升识别的准确率，请使用实际词语而非任意字符组合。

    长度限制：含非 ASCII 字符时不超过 15 个字符；纯 ASCII 时空格分隔片段不超过 7 个。

    **weight** *integer* **（必选）**

    热词权重。常用值：4。

    取值范围：\[1, 5]。

    如果效果不明显，可以适当增加权重，但权重过大可能产生负面效果，导致其他词语识别不准确。

    **lang** *string* （可选）

    待识别音频的语言代码。设置后，系统将对指定语种进行热词识别增强。如果无法提前确定语种，可不设置，模型会自动识别语种。

    取值范围（因模型而异）：

    - Paraformer：zh（中文）、en（英文）、ja（日语）、yue（粤语）、ko（韩语）、de（德语）、fr（法语）、ru（俄语）
    - Fun-ASR：zh（中文）、en（英文）、ja（日语）
  </Expandable>
</Expandable>

### 请求示例

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "speech-biasing",
    "input": {
        "action": "update_vocabulary",
        "vocabulary_id": "vocab-testpfx-xxx",
        "vocabulary": [
          {"text": "赛德克巴莱", "weight": 4, "lang": "zh"}
        ]
    }
}'
```

### 返回体

**request\_id** *string*

本次调用的唯一标识符。

**output** *object*

模型返回的数据，固定为空。

**usage** *object*

本次请求用量信息。

<Expandable title="属性">
  **count** *integer*

  更新的热词列表数量，固定为1。
</Expandable>

### 返回示例

```json
{
  "output": {},
  "usage": {
    "count": 1
  },
  "request_id": "aee47022-2352-40fe-acfa-xxxx"
}
```

## 删除热词列表

### 请求体

**model** *string* **（必选）**

定制热词模型，固定为`speech-biasing`。

**input** *object* **（必选）**

输入参数对象。

<Expandable title="属性">
  **action** *string* **（必选）**

  操作类型，固定为`delete_vocabulary`。

  **vocabulary\_id** *string* **（必选）**

  需要删除的热词列表ID。
</Expandable>

### 请求示例

```bash
curl -X POST https://dashscope.aliyuncs.com/api/v1/services/audio/asr/customization \
-H "Authorization: Bearer $DASHSCOPE_API_KEY" \
-H "Content-Type: application/json" \
-d '{
    "model": "speech-biasing",
    "input": {
        "action": "delete_vocabulary",
        "vocabulary_id": "vocab-testpfx-xxx"
    }
}'
```

### 返回体

**request\_id** *string*

本次调用的唯一标识符。

**output** *object*

模型返回的数据，固定为空。

**usage** *object*

本次请求用量信息。

<Expandable title="属性">
  **count** *integer*

  删除的热词列表数量，固定为1。
</Expandable>

### 返回示例

```json
{
  "output": {},
  "usage": {
    "count": 1
  },
  "request_id": "aee47022-2352-40fe-acfa-xxxx"
}
```
