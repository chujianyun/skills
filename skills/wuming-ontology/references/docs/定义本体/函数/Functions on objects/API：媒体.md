:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# API：媒体

:::callout{theme="warning"}
函数在具有严格内存限制的环境中执行。当处理文件数据时，超出这些内存限制可能会很快发生；我们建议仅与小于20MB的媒体进行交互。
:::

如果一个对象有一个媒体引用属性，您可以使用函数与关联的*媒体项*交互。媒体项提供了许多方法，以便捷地与底层媒体进行交互。有许多内置操作允许您轻松地与不同类型的媒体进行交互，而无需外部库。以下文档解释了可用的功能以及如何使用它们。

如果您需要任何当前尚未提供的操作，您可能需要使用外部库或编写自己的自定义代码。[了解更多关于向函数库添加NPM依赖项的信息。](../TypeScript%20basics/%E6%B7%BB%E5%8A%A0%20npm%20%E4%BE%9D%E8%B5%96%E9%A1%B9.md)

## 通用操作

某些操作被所有媒体类型支持。

### 读取原始媒体数据

要从媒体项中读取原始数据，请在媒体项上使用`readAsync`方法。您可以通过选择对象上的媒体引用属性来访问媒体项。`readAsync`方法的签名如下：
`Blob` 是一种标准的[JavaScript 类型 ↗](https://developer.mozilla.org/en-US/docs/Web/API/Blob)，表示不可变的原始数据的类似文件的对象。如上所述，您可以将其与库一起使用，以超出默认功能的方式与媒体进行交互。

### 获取媒体元数据

要获取媒体项的元数据，请在媒体项上使用 `getMetadataAsync` 方法。`getMetadataAsync` 方法的签名如下：

```typescript
getMetadataAsync(): Promise<IMediaMetadata>;
// 获取媒体元数据的异步方法，返回一个Promise对象，解析后得到IMediaMetadata类型的数据
```

## 类型守卫

提供了几种类型守卫，这将允许您访问特定于某些媒体类型的功能。以下类型守卫可以用于媒体项元数据：

* `isAudioMetadata()`
* `isDicomMetadata()`
* `isDocumentMetadata()`
* `isImageryMetadata()`
* `isVideoMetadata()`

例如，您可以使用图像类型守卫提取图像特定的元数据字段：

```typescript
const metadata = await myObject.mediaReference?.getMetadataAsync();
// 获取媒体的元数据信息

if (isImageryMetadata(metadata)) {
    // 判断元数据是否为图像类型
    const imageWidth = metadata.dimensions?.width;
    // 获取图像的宽度
    ...
}
```

您还可以在媒体项命名空间上使用类型保护，这样可以让您访问更多类型特定媒体项的方法。这里可以使用的类型保护是：

* `MediaItem.isAudio()`
* `MediaItem.isDocument()`
* `MediaItem.isImagery()`

## 文档特定操作

### 文本提取

要从文档中提取文本，您可以在媒体项上使用 `ocrAsync` 或 `extractTextAsync` 方法。

对于机器生成的PDF，提取嵌入PDF中的数字文本可能比使用光学字符识别（OCR）更快和/或更准确。以下是文本提取用法的示例：

```typescript
// 该函数定义了一个异步函数 extractTextAsync，它接受一个参数 options，类型为 IDocumentExtractTextOptions。
// 该函数返回一个 Promise，其解析结果是一个字符串数组。
extractTextAsync(options: IDocumentExtractTextOptions): Promise<string[]>;
```

以下内容可以作为 TypeScript 对象非必填提供：

* `startPage`: 起始页（包含），从零开始编号。
* `endPage`: 结束页（不包含），从零开始编号。

对于非机器生成的 PDF，最好使用 OCR 方法来提取文本。

```typescript
ocrAsync(options: IDocumentOcrOptions): Promise<string[]>;

// 该函数是一个异步光学字符识别（OCR）函数
// 参数 options 是一个 IDocumentOcrOptions 类型的对象，包含 OCR 所需的配置选项
// 返回一个 Promise 对象，解析为一个字符串数组，每个字符串代表识别出的文本
```

以下内容可以选择性地作为 TypeScript 对象提供：

* `startPage`: 从零开始的起始页（包含）。
* `endPage`: 从零开始的结束页（不包含）。
* `languages`: 要识别的语言列表（可以为空）。
* `scripts`: 要识别的脚本列表（可以为空）。
* `outputType`: 指定输出类型为 `text` 或 `hocr`。

请记住，您需要使用类型保护以访问特定媒体类型的操作。以下是使用 `isDocument` 类型保护然后执行 OCR 文本提取的示例：

```typescript
import { MediaItem } from "@foundry/functions-api";
import { ArxivPaper } from "@foundry/ontology-api";

@Function()
public async firstPageText(paper: ArxivPaper): Promise<string | undefined> {
    // 检查 mediaReference 是否为文档类型
    if (MediaItem.isDocument(paper.mediaReference!)) {
        // 使用 OCR 技术提取文档第一页的文本
        const text = (await paper.mediaReference.ocrAsync({ endPage: 1, languages: [], scripts: [], outputType: 'text' }))[0];
        return text;
    }

    // 如果 mediaReference 不是文档类型，则返回 undefined
    return undefined;
}
```

## 音频特定操作

### 转录

音频媒体项支持使用 `transcribeAsync` 方法进行转录。其签名如下：

```typescript
transcribeAsync(options: IAudioTranscriptionOptions): Promise<string>;
// 该函数用于异步音频转录操作，接受一个 IAudioTranscriptionOptions 类型的选项参数，返回一个 Promise 对象，该对象解析为字符串形式的转录结果。
```

以下选项是非必填的，可以用来指定转录的运行方式。可用选项包括：

* `language`：要转录的语言，使用 `TranscriptionLanguage` 枚举传递。
* `performanceMode`：以 `More Economical` 或 `More Performant` 模式运行转录，使用 `TranscriptionPerformanceMode` 枚举传递。
* `outputFormat`：通过传递一个 `type` 为 `plainTextNoSegmentData`（纯文本）或 `pttml` 的对象来指定输出格式。如果类型是 `plainTextNoSegmentData`，`pttml` 是一种 [类似于 TTML 的格式 ↗](https://en.wikipedia.org/wiki/Timed_Text_Markup_Language)，该对象还可以接受一个布尔值 `addTimestamps` 参数。

以下是提供转录选项的示例：

```typescript
import { Function, MediaItem, TranscriptionLanguage, TranscriptionPerformanceMode } from "@foundry/functions-api";
import { AudioFile } from "@foundry/ontology-api";

@Function()
public async transcribeAudioFile(file: AudioFile): Promise<string|undefined> {
    // 检查文件是否为音频文件
    if (MediaItem.isAudio(file.mediaReference!)) {
        // 异步转录音频文件，指定语言为英语，性能模式为更经济，并且输出格式为纯文本（不包含分段数据），包含时间戳
        return await file.mediaReference.transcribeAsync({
            language: TranscriptionLanguage.ENGLISH,
            performanceMode: TranscriptionPerformanceMode.MORE_ECONOMICAL,
            outputFormat: {type: "plainTextNoSegmentData", addTimestamps: true}
        });
    }

    // 如果文件不是音频文件，返回 undefined
    return undefined;
}
```
