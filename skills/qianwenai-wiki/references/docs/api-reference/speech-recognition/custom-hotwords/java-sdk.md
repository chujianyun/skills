> ## Documentation Index
> Fetch the complete documentation index at: https://platform.qianwenai.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 定制热词 Java SDK

> 通过Java SDK管理定制热词列表，包括创建、查询、更新和删除热词列表。

通过Java SDK管理定制热词列表，包括VocabularyService类的方法说明与示例代码。

**用户指南：**[用户指南](/developer-guides/speech/improve-recognition-accuracy)。

## 服务端点

```
https://dashscope.aliyuncs.com/api/v1
```

## VocabularyService

**包路径**：`com.alibaba.dashscope.audio.asr.vocabulary.VocabularyService`

**功能**：管理热词列表的生命周期（创建、查询、更新、删除）

### 构造方法

```java
public VocabularyService(String apiKey)
```

**参数**：

| 参数     | 类型     | 说明                |
| ------ | ------ | ----------------- |
| apiKey | String | DashScope API Key |

### createVocabulary() - 创建热词列表

**方法签名**：

```java
public Vocabulary createVocabulary(String targetModel,String prefix,JsonArray vocabulary) throws NoApiKeyException, InputRequiredException
```

**参数**：

| 参数          | 类型        | 必填 | 说明                                                               |
| ----------- | --------- | -- | ---------------------------------------------------------------- |
| targetModel | String    | 是  | 使用热词列表的语音识别模型，必须与后续调用语音识别接口时使用的模型一致。                             |
| prefix      | String    | 是  | 热词列表自定义前缀，仅允许数字和小写字母，长度不超过10个字符。                                 |
| vocabulary  | JsonArray | 是  | 热词列表，每个JsonObject包含 text、weight、lang 等字段。详情请参见[热词对象结构](#热词对象结构)。 |

**返回值**：

| 类型         | 说明                          |
| ---------- | --------------------------- |
| Vocabulary | 热词列表对象，包含 vocabularyId 等信息。 |

**异常**：

| 异常类型                   | 说明          |
| ---------------------- | ----------- |
| NoApiKeyException      | API Key 为空。 |
| InputRequiredException | 必填参数为空。     |

### listVocabulary() - 批量查询热词列表

**方法签名**：

```java
public Vocabulary[] listVocabulary(String prefix) throws NoApiKeyException, InputRequiredException

public Vocabulary[] listVocabulary(String prefix, int pageIndex, int pageSize) throws NoApiKeyException, InputRequiredException
```

**参数**：

| 参数        | 类型     | 必填 | 说明                           |
| --------- | ------ | -- | ---------------------------- |
| prefix    | String | 否  | 热词列表自定义前缀，如果设定则只返回指定前缀的热词列表。 |
| pageIndex | int    | 否  | 页码索引，从0开始计数。默认值：0。           |
| pageSize  | int    | 否  | 每页包含数据条数。默认值：10。             |

**返回值**：

| 类型            | 说明        |
| ------------- | --------- |
| Vocabulary\[] | 热词列表对象数组。 |

**Vocabulary 对象字段（list返回）**：

| 字段           | 类型     | 说明                           |
| ------------ | ------ | ---------------------------- |
| vocabularyId | String | 热词列表ID。                      |
| gmtCreate    | String | 创建时间。                        |
| gmtModified  | String | 修改时间。                        |
| status       | String | 状态：OK（可调用）、UNDEPLOYED（不可调用）。 |

**异常**：

| 异常类型                   | 说明          |
| ---------------------- | ----------- |
| NoApiKeyException      | API Key 为空。 |
| InputRequiredException | 必填参数为空。     |

### queryVocabulary() - 查询热词列表

**方法签名**：

```java
public Vocabulary queryVocabulary(String vocabularyId) throws NoApiKeyException, InputRequiredException
```

**参数**：

| 参数           | 类型     | 必填 | 说明           |
| ------------ | ------ | -- | ------------ |
| vocabularyId | String | 是  | 需要查询的热词列表ID。 |

**返回值**：

| 类型         | 说明             |
| ---------- | -------------- |
| Vocabulary | 热词列表对象，包含详细信息。 |

**Vocabulary 对象字段（query返回）**：

| 字段          | 类型        | 说明                                   |
| ----------- | --------- | ------------------------------------ |
| vocabulary  | JsonArray | 热词列表内容                               |
| targetModel | String    | 使用热词列表的语音识别模型，必须与后续调用语音识别接口时使用的模型一致。 |
| gmtCreate   | String    | 创建时间。                                |
| gmtModified | String    | 修改时间。                                |
| status      | String    | 状态：OK（可调用）、UNDEPLOYED（不可调用）。         |

**异常**：

| 异常类型                   | 说明          |
| ---------------------- | ----------- |
| NoApiKeyException      | API Key 为空。 |
| InputRequiredException | 必填参数为空。     |

### updateVocabulary() - 更新热词列表

**方法签名**：

```java
public void updateVocabulary(String vocabularyId,JsonArray vocabulary) throws NoApiKeyException, InputRequiredException
```

**参数**：

| 参数           | 类型        | 必填 | 说明                |
| ------------ | --------- | -- | ----------------- |
| vocabularyId | String    | 是  | 需要更新的热词列表ID。      |
| vocabulary   | JsonArray | 是  | 新的热词列表，将完全替换原有内容。 |

**返回值**：无

**异常**：

| 异常类型                   | 说明          |
| ---------------------- | ----------- |
| NoApiKeyException      | API Key 为空。 |
| InputRequiredException | 必填参数为空。     |

### deleteVocabulary() - 删除热词列表

**方法签名**：

```java
public void deleteVocabulary(String vocabularyId) throws NoApiKeyException, InputRequiredException
```

**参数**：

| 参数           | 类型     | 必填 | 说明           |
| ------------ | ------ | -- | ------------ |
| vocabularyId | String | 是  | 需要删除的热词列表ID。 |

**返回值**：无

**异常**：

| 异常类型                   | 说明          |
| ---------------------- | ----------- |
| NoApiKeyException      | API Key 为空。 |
| InputRequiredException | 必填参数为空。     |

## Vocabulary 类

**包路径**：`com.alibaba.dashscope.audio.asr.vocabulary.Vocabulary`

**功能**：热词列表对象，封装热词列表的元数据和内容

### 主要方法

| 方法                | 返回类型       | 说明              |
| ----------------- | ---------- | --------------- |
| getVocabularyId() | String     | 获取热词列表ID。       |
| getTargetModel()  | String     | 获取目标模型。         |
| getVocabulary()   | JsonArray  | 获取热词列表内容。       |
| getStatus()       | String     | 获取状态。           |
| getGmtCreate()    | String     | 获取创建时间。         |
| getGmtModified()  | String     | 获取修改时间。         |
| getData()         | JsonObject | 获取完整数据（JSON格式）。 |

## 热词对象结构

**用于 `vocabulary` 参数的 JsonObject 定义**：

| 字段     | 类型     | 必填 | 说明                                                                                                                                                                            |
| ------ | ------ | -- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| text   | String | 是  | 热词文本。热词文本的语言必须在所选模型的支持范围内，不同模型支持的语言各不相同。热词用于提升识别的准确率，请使用实际词语而非任意字符组合。长度限制：含非 ASCII 字符时不超过 15 个字符；纯 ASCII 时空格分隔片段不超过 7 个。                                                      |
| weight | int    | 是  | 热词权重。常用值：4。取值范围：\[1, 5]。如果效果不明显，可以适当增加权重，但权重过大可能产生负面效果，导致其他词语识别不准确。                                                                                                           |
| lang   | String | 否  | 待识别音频的语言代码。设置后，系统将对指定语种进行热词识别增强。如果无法提前确定语种，可不设置，模型会自动识别语种。取值范围（因模型而异）：Paraformer 支持 zh（中文）、en（英文）、ja（日语）、yue（粤语）、ko（韩语）、de（德语）、fr（法语）、ru（俄语）；Fun-ASR 支持 zh（中文）、en（英文）、ja（日语）。 |

## 示例代码

### 创建热词列表

```java
import com.alibaba.dashscope.audio.asr.vocabulary.Vocabulary;
import com.alibaba.dashscope.audio.asr.vocabulary.VocabularyService;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.util.ArrayList;
import java.util.List;

public class Main {
  // 若没有配置环境变量，请将下行替换为：public static String apiKey = "sk-xxx"
  public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

  public static void main(String[] args) throws NoApiKeyException, InputRequiredException {
    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";
    String targetModel = "fun-asr";

    JsonArray vocabularyJson = new JsonArray();
    List<Hotword> wordList = new ArrayList<>();
    wordList.add(new Hotword("吴贻弓", 4));
    wordList.add(new Hotword("阙里人家", 4));

    for (Hotword word : wordList) {
      JsonObject jsonObject = new JsonObject();
      jsonObject.addProperty("text", word.text);
      jsonObject.addProperty("weight", word.weight);
      vocabularyJson.add(jsonObject);
    }

    VocabularyService service = new VocabularyService(apiKey);
    Vocabulary vocabulary = service.createVocabulary(targetModel, "testpfx", vocabularyJson);
    System.out.println("热词列表ID：" + vocabulary.getVocabularyId());
  }
}

class Hotword {
  String text;
  int weight;

  public Hotword(String text, int weight) {
    this.text = text;
    this.weight = weight;
  }
}
```

### 批量查询热词列表

```java
import com.alibaba.dashscope.audio.asr.vocabulary.Vocabulary;
import com.alibaba.dashscope.audio.asr.vocabulary.VocabularyService;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class Main {
  // 若没有配置环境变量，请将下行替换为：public static String apiKey = "sk-xxx"
  public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

  public static void main(String[] args) throws NoApiKeyException, InputRequiredException {
    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";

    VocabularyService service = new VocabularyService(apiKey);
    Vocabulary[] vocabularies = service.listVocabulary("testpfx");
    Gson gson = new GsonBuilder()
        .setPrettyPrinting()
        .create();
    System.out.println("热词列表：" + gson.toJson(vocabularies));
  }
}
```

### 查询热词列表

```java
import com.alibaba.dashscope.audio.asr.vocabulary.Vocabulary;
import com.alibaba.dashscope.audio.asr.vocabulary.VocabularyService;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class Main {
  // 若没有配置环境变量，请将下行替换为：public static String apiKey = "sk-xxx"
  public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

  public static void main(String[] args) throws NoApiKeyException, InputRequiredException {
    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";

    VocabularyService service = new VocabularyService(apiKey);
    // 查询时替换为实际的热词列表ID
    Vocabulary vocabulary = service.queryVocabulary("vocab-testpfx-xxxx");
    Gson gson = new GsonBuilder()
        .setPrettyPrinting()
        .create();
    System.out.println("热词列表：" + gson.toJson(vocabulary.getData()));
  }
}
```

### 更新热词列表

```java
import com.alibaba.dashscope.audio.asr.vocabulary.VocabularyService;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import java.util.ArrayList;
import java.util.List;

public class Main {
  // 若没有配置环境变量，请将下行替换为：public static String apiKey = "sk-xxx"
  public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

  public static void main(String[] args) throws NoApiKeyException, InputRequiredException {
    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";

    JsonArray vocabularyJson = new JsonArray();
    List<Hotword> wordList = new ArrayList<>();
    wordList.add(new Hotword("吴贻弓", 4, "zh"));
    wordList.add(new Hotword("阙里人家", 4, "zh"));

    for (Hotword word : wordList) {
      JsonObject jsonObject = new JsonObject();
      jsonObject.addProperty("text", word.text);
      jsonObject.addProperty("weight", word.weight);
      jsonObject.addProperty("lang", word.lang);
      vocabularyJson.add(jsonObject);
    }

    VocabularyService service = new VocabularyService(apiKey);
    // 替换为实际的热词列表ID
    service.updateVocabulary("vocab-testpfx-xxx", vocabularyJson);
  }
}

class Hotword {
  String text;
  int weight;
  String lang;

  public Hotword(String text, int weight, String lang) {
    this.text = text;
    this.weight = weight;
    this.lang = lang;
  }
}
```

### 删除热词列表

```java
import com.alibaba.dashscope.audio.asr.vocabulary.VocabularyService;
import com.alibaba.dashscope.exception.InputRequiredException;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.utils.Constants;

public class Main {
  // 若没有配置环境变量，请将下行替换为：public static String apiKey = "sk-xxx"
  public static String apiKey = System.getenv("DASHSCOPE_API_KEY");

  public static void main(String[] args) throws NoApiKeyException, InputRequiredException {
    Constants.baseHttpApiUrl = "https://dashscope.aliyuncs.com/api/v1";

    VocabularyService service = new VocabularyService(apiKey);
    // 删除时替换为实际的热词列表ID
    service.deleteVocabulary("vocab-testpfx-xxxx");
  }
}
```
