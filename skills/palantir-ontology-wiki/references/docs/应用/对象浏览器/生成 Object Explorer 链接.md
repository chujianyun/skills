:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 生成 Object Explorer 链接

在开发 Object 视图的过程中，或将 Object 视图集成到 Slate 应用程序或外部系统时，您可能需要生成链接到特定 Object 或搜索 Objects 的链接。

要了解如何创建链接到特定 Object View 的URL，请参阅 Object Views 文档中的[生成 Object Views URLs](../%E5%AF%B9%E8%B1%A1%E8%A7%86%E5%9B%BE/%E7%94%9F%E6%88%90Object%E8%A7%86%E5%9B%BEURL.md)。

## 生成仅关键字搜索

如果您的文本包含特殊字符或空格，您需要对其进行编码：

`encodeURIComponent("hello world");`

创建一个 URL:

`<BASEURL>/hubble/external/keyword/v0/<MY_ENCODED_TEXT>`

## 链接到探索

Object Explorer 可以打开链接到特定对象类型、已保存的探索或在URL中描述的筛选的新搜索。每种类型的链接都可以在默认的探索视图中打开，显示聚合结果的图表，或者通过在链接 URL 的末尾添加参数`perspectiveId=results`在表格结果视图中打开。

**打开特定对象类型的探索**

可以使用 `objectTypeId` URL 参数打开特定对象类型的探索。例如：

`/workspace/hubble/exploration?objectTypeId=aircraft`。

要在结果视图中打开，请添加`perspectiveId=results`参数：

`/workspace/hubble/exploration?objectTypeId=aircraft&perspectiveId=results`

**加载已保存的探索或对象集**

使用`saved`路径打开已保存的探索或对象集。

`/workspace/hubble/exploration/saved/ri.object-set.main.versioned-object-set.4b117663-06d7-4bd1-a2be-8e1ba20998cb`

要加载由另一个 Foundry 应用程序创建的对象集，请使用`external/objectSet`路径。

`/workspace/hubble/external/objectSet/v0/ri.object-set.main.object-set.f6916120-5b52-4312-8be4-9f5764983907`

## \[高级] 生成复杂搜索

生成您的筛选集，使其看起来像：

```json
{
  "keyword": "",
  "objectTypes": [
    "google-reviews"
  ],
  "filters": [
    {
      "type": "propertyFilter",
      "objectType": "google-reviews",
      "propertyType": "Description",
      "value": {
          "type": "textFilter",
          "text": "hello"
      }
      // 筛选描述中包含“hello”的Google评论
    },
    {
      "type": "propertyFilter",
      "objectType": "google-reviews",
      "propertyType": "rating",
      "value": {
          "type": "valuesFilter",
          "values": ["3", "4"]
      }
      // 筛选评分为3或4的Google评论
    },
    {
      "type": "propertyFilter",
      "objectType": "google-reviews",
      "propertyType": "creation-date",
      "value": {
          "type": "dateRangeFilter",
          "dateRangeFilter": {
              "start": "2000-01-10",
              "end": "2000-01-11"
          }
      }
      // 筛选创建日期在2000-01-10到2000-01-11之间的Google评论
    },
    {
      "type": "linkFilter",
      "objectType": "google-reviews",
      "linkType": "restaurant-to-review",
      "value": {
          "type": "presenceFilter",
          "matchType": "MUST_HAVE"
      }
      // 筛选与餐厅有链接关系的Google评论
    }
  ]
}
```

有多种类型的筛选可用，包括：

* **numberRangeFilter:** `min` (非必填数字), `max` (非必填数字)
* **relativeDateFilter:** `sinceDaysAgo` (非必填数字), `untilDaysAgo` (非必填数字)
* **timestampRangeFilter:** `startMillis` (非必填数字), `endMillis` (非必填数字)
* **relativeTimestampFilter:** `sinceMillisAgo` (非必填数字), `untilMillisAgo` (非必填数字)

:::callout{theme="neutral"}
此示例可能已过时 – 请使用以下说明查找最新格式。
:::

值的类型必须与在 Object Explorer 中默认显示该属性的微件的类型匹配。例如：直方图微件使用 `valuesFilter`; 文本框使用 `textFilter`。

生成这些筛选的推荐方法是：

1. 打开 Object Explorer 并搭建一个示例搜索，选择所有要生成的筛选的示例值

2. 打开 Chrome 控制台 (*右键单击* -> *检查元素*)。确保检查 Object Explorer 提供的元素，例如结果计数，而不仅仅是打开 Chrome 控制台。

3. 在控制台中运行 `await hubble_get_current_search()`。

这将返回当前筛选集的 JSON 格式，您可以用它来确定正确的格式，并为值添加替换。

:::callout{theme="neutral"}
您可以有多个 *PROPERTY* 筛选，但只能有一个 *LINK* 筛选。
:::

4. 对其进行 URL 编码：

`encodeURIComponent(<MY_FILTERS>);`

5. 创建一个 URL：

`<BASEURL>/hubble/external/search/v2/{<ENCODED-URL-FROM-ABOVE>}`
