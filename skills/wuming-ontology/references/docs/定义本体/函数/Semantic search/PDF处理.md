:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# PDF处理

本页面提供了一个基本指南，以使用[Pipeline Builder](https://www.palantir.com/docs/foundry/pipeline-builder/overview/)解析PDF以进行语义搜索，并推荐在[Workshop](https://www.palantir.com/docs/foundry/workshop/overview/)应用中展示信息的方法。

语义搜索是处理PDF的强大工具，特别是当内容被分解成更小的单独嵌入的“块”时，帮助用户和工作流找到可能难以访问的重要信息。这在考虑到PDF中大量未被注意的非结构化知识时尤其有用。

要使用此功能，只需将您的PDF上传到Foundry，提取文本，分块相同的文本，搜索这些块，并通过侧边呈现相应的PDF来为用户提供交叉验证的真实来源。

## 设置语义搜索以在PDF中进行搜索

按照以下步骤导入PDF并建立语义搜索，以从PDF中呈现内容：

1. [将PDF导入为媒体集](https://www.palantir.com/docs/foundry/data-integration/media-sets/#import-media)
2. [将媒体集添加到Pipeline Builder中](https://www.palantir.com/docs/foundry/pipeline-builder/datasets-add/#add-datasets-from-foundry-to-pipeline-builder)
3. 使用 **获取媒体引用** 面板。

![获取媒体引用面板](../../../../assets/foundry/functions/get-media-references.png)

4. 使用 **文本提取** 面板。

[官方图片已失效：文本提取面板](https://www.palantir.com/docs/resources/foundry/functions/text-extraction.png)

5. 遵循[分块](%E5%88%86%E5%9D%97.md)策略。
6. 创建具有[媒体引用](https://www.palantir.com/docs/foundry/data-integration/media-sets/#media-references)属性的块对象。
7. 在[语义搜索工作流](%E4%BD%BF%E7%94%A8Palantir%E6%8F%90%E4%BE%9B%E7%9A%84%E6%A8%A1%E5%9E%8B%E5%88%9B%E5%BB%BA%E8%AF%AD%E4%B9%89%E6%90%9C%E7%B4%A2%E5%B7%A5%E4%BD%9C%E6%B5%81.md)中搜索块。
8. 在Workshop中使用[PDF查看器微件](https://www.palantir.com/docs/foundry/workshop/widgets-pdf-viewer/)，注意配置选项。


> 配图缺失说明：本页有 1 个官方图片地址在抓取及重试时失效（返回 HTML 错误页）。下列地址保留用于溯源，未替换成其他版本的图片。

- 官方图片已失效：<https://www.palantir.com/docs/resources/foundry/functions/text-extraction.png>
