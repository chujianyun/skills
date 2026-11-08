:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# API：对象集

**对象集**表示单一类型对象的无序集合。您可以使用函数API来筛选对象集，执行基于已定义链接类型的其他对象类型的周边搜索，并计算聚合值或检索具体对象。除了将单个对象作为输入传递给函数之外，您还可以随时使用对象搜索API搜索对象集。

:::callout{theme="neutral"}
筛选、排序和聚合仅适用于在Ontology应用中启用了`Searchable`渲染提示的属性。这些属性已被索引以便搜索。[了解如何启用`Searchable`渲染提示。](../../%E5%AF%B9%E8%B1%A1%E9%93%BE%E6%8E%A5%E7%B1%BB%E5%9E%8B/Metadata/%E6%B8%B2%E6%9F%93%E6%8F%90%E7%A4%BA.md)
:::

## 对象搜索

`Objects.search()`接口允许您启动对导入项目的任何对象类型的搜索。在此示例中，函数使用给定的`airportCode`查找从该机场出发的所有航班。然后，它找出这些航班的所有不同目的地并返回它们。

```typescript
import { Function } from "@foundry/functions-api";
import { Objects } from "@foundry/ontology-api";

export class FlightFunctions {
    @Function()
    public currentFlightDestinations(airportCode: string): Set<string> {
        // 搜索从给定机场代码出发的所有航班
        const flightsFromAirport = Objects.search()
            .flights()
            .filter(flight => flight.departureAirportCode.exactMatch(airportCode))
            .all();

        // 获取这些航班的目的地机场代码
        const destinations = flightsFromAirport.map(flight => flight.arrivalAirportCode!);

        // 使用Set去重并返回所有目的地机场代码
        return new Set(destinations);
    }
}
```

对象集也可以通过传递对象列表、对象资源标识符列表或对象集资源标识符作为搜索对象类型的参数来创建。例如：`Objects.search().flights([flight])`。

一旦有了给定类型的对象集，你可以对该集合执行各种操作，如下文所述。

## 筛选

对象集上的`.filter()`方法允许你基于对象的[可搜索](API%EF%BC%9A%E5%AF%B9%E8%B1%A1%E9%9B%86.md#searchable_note)属性来筛选对象集。筛选方法需要一个筛选定义，该定义基于你所筛选的属性类型。

* 所有属性类型都支持`.exactMatch()`筛选，筛选出在该属性值上完全匹配的对象。这对于筛选字符串的完全匹配（如上例），或筛选对象的主键非常有用（例如，`.filter(object => object.primaryKey.exactMatch(PrimaryKey))`）。
  * 要检查属性是否为`null`或`undefined`，请使用`hasProperty()`方法。
  * 要传递多个值，请使用扩展操作符`.exactMatch(...listVariable)`。如果传入空数组，筛选将被忽略。
* 字符串属性支持多种关键词筛选。查看Code Assist中每个方法的文档以获取详细信息。
  * `.phrase()`根据值是否包含给定短语来筛选。注意，字符串值中由连字符、下划线或句号分隔的连接词将被视为一个短语。例如，当搜索"banana"时，属性值为"banana\_pudding"的对象将不会被返回。
  * `.phrasePrefix()`根据值是否以给定短语和前缀开头来筛选。例如，`.phrasePrefix()`搜索`banana`将返回属性值为`banana_pudding`的对象；`.phrasePrefix()`搜索`pudding`将不匹配属性值`banana_pudding`。
  * `.prefixOnLastToken()`根据值是否包含给定短语（最后一个词元作为前缀处理）来筛选。
  * `.matchAnyToken()`，`.fuzzyMatchAnyToken()`将搜索查询拆分为词元（通常是单个词），然后根据值是否包含任何给定的词元进行筛选。`fuzzy`版本允许近似值匹配。注意，如果搜索查询或属性值包含连字符、下划线或句号，即使是连接词，也将被视为一个词元或短语。
  * `.matchAllTokens()`，`.fuzzyMatchAllTokens()`将搜索查询拆分为词元（通常是单个词），然后根据值是否包含所有给定的词元进行筛选。`fuzzy`版本允许近似值匹配。
    * 模糊筛选可以接受从`@foundry/functions-api`导入的非必填`Fuzziness`参数。
    * 可用`Fuzziness`选项的解释可以在[ElasticSearch文档↗](https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#fuzziness)中找到。更多信息也可以在下文中找到。
* 数字、日期和时间戳属性支持`.range()`筛选。
  * 范围筛选有一组`.lt()`，`.lte()`，`.gt()`和`gte()`方法，用于执行小于/小于或等于/大于/大于或等于（分别）比较。
* 布尔属性支持`.isTrue()`和`.isFalse()`筛选。
* Geohash属性支持`.withinDistanceOf()`，`.withinPolygon()`和`.withinBoundingBox()`筛选。
* GeoShape属性支持`.withinBoundingBox()`，`.intersectsBoundingBox()`，`.doesNotIntersectBoundingBox()`，`.withinPolygon()`，`.intersectsPolygon()`和`doesNotIntersectPolygon()`筛选。
* 链接筛选可用于筛选有或没有特定类型链接对象的对象，使用`.isPresent()`方法。
* 数组属性支持`.contains()`筛选，筛选出其数组属性值包含\_任何\_给定值的对象。

### 组合筛选

你可以使用从`@foundry/functions-api`导出的`Filters` API组合筛选。可用的方法有：

* `and()`筛选对象集以通过所有给定筛选的对象
* `or()`筛选对象集以通过任何给定筛选的对象
* `not()`否定给定筛选

在下面的例子中，我们可以使用`and()`来筛选航班目的地的对象集：

```typescript
import { Filters } from "@foundry/functions-api";

// 使用Objects.search()开始一个搜索操作
Objects.search()
    .flights() // 搜索航班对象
    .filter(flight => Filters.or( // 使用逻辑“或”来过滤航班
        Filters.and(flight.destination.exactMatch("SFO"), flight.passengerCount.gt(100)), // 目的地是SFO且乘客人数大于100
        Filters.and(flight.destination.exactMatch("LAX"), flight.passengerCount.gt(300)), // 目的地是LAX且乘客人数大于300
    ))
```

以上代码使用`@foundry/functions-api`库进行航班搜索，并过滤出符合以下条件的航班：目的地是旧金山国际机场（SFO）且乘客数大于100，或者目的地是洛杉矶国际机场（LAX）且乘客数大于300。
上述代码将筛选出到达SFO且乘客超过100人的航班，或到达LAX且乘客超过300人的航班。

:::callout{theme="warning" title="警告"}
对象集上的`.filter()`方法不使用操作符`&&`或`||`。要应用多个筛选，必须使用上面列出的`筛选`方法之一（或者多次调用`.filter()`以实现`and`条件）。
:::

### 以模糊搜索筛选字符串属性

指定非必填参数`fuzziness`可以提供对模糊匹配行为的更精细控制。如果不指定fuzziness，则根据您要搜索的词元的长度允许自动编辑距离。您需要从`@foundry/functions-api`导入`Fuzziness`以指定编辑距离。

#### 模糊匹配任意词元

```javascript
Objects.search()
  .employee()
  .filter(employee =>
    // 使用模糊匹配过滤员工，匹配度为LEVENSHSTEIN_TWO，允许两个字符的编辑距离
    employee.firstName.fuzzyMatchAnyToken("Michael", { fuzziness: Fuzziness.LEVENSHTEIN_TWO })
  )
  .all(); // 返回所有符合条件的员工对象
```

上面的代码返回的是与提供的搜索词在两次编辑内的任何员工名字（Levenshtein距离为二）。在这个例子中，包括`Michael`、`Micheal`、`Mikhael`、`Michel`、`Mikhail`、`Mihail`（但不包括例如`Miguel`）。如果您对搜索词的准确性有更高的确定性，可以使用较小的编辑距离进行搜索（使用不同的Levenshtein距离），以更加精确地筛选搜索结果。

#### 模糊匹配所有词元

```javascript
Objects.search()
    .employee()
    .filter(employee =>
        // 使用模糊匹配函数fuzzyMatchAllTokens来匹配员工的全名
        // "Michael Smith"是目标字符串
        // { fuzziness: Fuzziness.LEVENSHTEIN_ONE }指定了模糊程度为Levenshtein距离为1
        employee.fullName.fuzzyMatchAllTokens("Michael Smith", { fuzziness: Fuzziness.LEVENSHTEIN_ONE })
    )
    .all();
```

您还可以对多个词元短语使用模糊筛选。上面的代码将匹配全名包含**Michael**和**Smith**的员工，每个词元最多允许一个编辑——例如，`Mikhael Smitt`（即每个词元的Levenshtein距离为1）。使用`fuzzyMatchAllTokens`或`fuzzyMatchesAllTokens`筛选时，不考虑词元的顺序。

#### 字符串数组属性上的模糊匹配

所有基于数组的属性筛选都可以使用其基础类型可用的方法。例如，字符串数组属性可以基于任何可用于字符串属性的方法进行筛选，尽管方法的命名可能略有不同。对数组属性进行筛选时，只需数组元素中的单个匹配项即可返回该对象。

## 周边搜索

:::callout{title="周边搜索限制"}
加载到内存中的对象集 `.all()` 或 `.allAsync()` 允许有**最多3个周边搜索**。如果使用超过3个周边搜索，将会抛出错误。在对象存储V2中，从对象集A到对象集B执行周边搜索时，结果对象集B不能超过1000万个对象实例，否则将抛出错误。对于对象存储V1，限制为100,000个对象实例。
:::

基于对象集的对象类型，\_周边搜索\_方法生成以启用基于对象集的对象类型遍历[链接](../../%E5%AF%B9%E8%B1%A1%E9%93%BE%E6%8E%A5%E7%B1%BB%E5%9E%8B/Link%20types/%E6%A6%82%E8%BF%B0.md)。在下面的示例中，我们根据出发代码筛选航班对象集，然后进行周边搜索找到这些航班上的乘客。这将产生一个乘客对象集，可以进一步筛选或进行周边搜索。

```typescript
const passengersDepartingFromAirport = Objects.search()
    .flights()
    .filter(flight => flight.departureAirportCode.exactMatch(airportCode)) // 过滤出出发机场代码与指定代码完全匹配的航班
    .searchAroundPassengers(); // 查找与这些航班相关的乘客
```

导入到您的项目中的链接类型将仅生成Search Around方法。有关如何导入链接类型的详细信息，请参阅[教程](%E6%A6%82%E8%BF%B0.md#import-ontology-types)。

请注意，出于性能原因，您在单次搜索中可以进行的Search Around操作数量目前限制为3个。如果您尝试运行深度超过三层的Search Around搜索，搜索将在运行时出错。

## K近邻（KNN）

:::callout{title="KNN 限制"}
KNN仅支持索引到[OSv2](../../../%E6%9C%AC%E4%BD%93%E6%9E%B6%E6%9E%84/%E5%AF%B9%E8%B1%A1%E5%90%8E%E7%AB%AF/%E6%A6%82%E8%BF%B0.md)中的对象类型。k值限制在0 < K <= 100范围内。此外，搜索向量必须与用于索引的向量大小相同，并且有2048维的限制。如果超出这些限制，将抛出出错。
:::

具有嵌入属性的对象类型将可用于KNN搜索。这些搜索将返回具有嵌入属性最接近提供的嵌入参数的k值对象。以下示例返回与提供的电影剧本最相似的电影。在查询时生成嵌入将需要设置[模型实时部署](../%E6%A8%A1%E5%9E%8B%E4%B8%8A%E7%9A%84%E5%87%BD%E6%95%B0.md)。

确保`functions.json`中的`enableVectorProperties`设置为`true`。

```typescript
import { Objects } from "@foundry/ontology-api";

const kValue: number = 2;
// 向量可以从 FML Live 生成或来自现有对象
const vector: Double[] = [0.7, 0.1, 0.3];
const movies: Movies[] = Objects.search()
        .movies()
        // 使用最近邻算法查找与给定向量最接近的电影对象
        .nearestNeighbors(obj => obj.vectorProperty.near(vector, { kValue }))
        // 按相关性排序结果
        .orderByRelevance()
        // 获取前 k 个最相关的结果
        .take(kValue);
```

要查看完整的语义搜索工作流示例，请查阅[语义搜索工作流指南](../Semantic%20search/%E4%BD%BF%E7%94%A8Palantir%E6%8F%90%E4%BE%9B%E7%9A%84%E6%A8%A1%E5%9E%8B%E5%88%9B%E5%BB%BA%E8%AF%AD%E4%B9%89%E6%90%9C%E7%B4%A2%E5%B7%A5%E4%BD%9C%E6%B5%81.md)。

## 集合操作

相同Object类型的对象集可以通过集合操作以各种方式进行合并：

* `.union()` 创建一个新对象集，其中包含在任一给定对象集中的对象。
* `.intersect()` 创建一个新对象集，其中包含在所有给定对象集中的对象。
* `.subtract()` 移除给定对象集中存在的任何对象。

## 检索所有对象

`.all()` 和 `.allAsync()` 方法检索对象集中的所有对象。请注意，如果您尝试一次加载过多对象，您的函数将无法执行。目前，您可以加载的对象最大数量为100,000。然而，加载超过10,000个对象也可能导致函数执行超时。[了解更多关于函数中的时间和空间限制。](../Performance%20and%20limits/%E5%BC%BA%E5%88%B6%E9%99%90%E5%88%B6.md)

您可以使用 `.allAsync()` 方法来检索一个 Promise，该 Promise 解析为对象集中的所有对象。这对于并行从多个对象集中加载数据非常有用。

## 排序和限制

您可以通过对对象集应用排序子句，然后指定要加载的特定对象数量，以限制加载的对象数量，而不是检索所有对象。为此，您可以使用以下方法：

* `.orderBy()` 指定一个[可搜索的](API%EF%BC%9A%E5%AF%B9%E8%B1%A1%E9%9B%86.md#searchable_note)属性进行排序，并允许您指定排序方向。只有类型可以排序（数字、日期和字符串）的属性可用于此方法中选择。您可以多次调用 `.orderBy()` 以按多个属性排序。
* `.orderByRelevance()` 指定对象应按与提供的筛选的匹配程度排序，最相关的列在最前面。针对给定Object上的属性值的查询词的相关性是一个复杂的判断，考虑了词在属性值中出现的频率、词在所有对象中出现的频率等。仅执行 `.exactMatch()` 筛选或筛选非字符串属性时，相关性不太适用。请注意，在单次搜索中只能使用 `.orderBy()` 和 `.orderByRelevance()` 之一。
* `.take()` 和 `.takeAsync()` 使您能够从集合中检索指定数量的对象。这些方法仅在您指定排序后可用。

例如，以下代码将检索起始日期最早的十名员工：

```typescript
Objects.search()
    .employees() // 搜索员工对象
    .orderBy(e => e.startDate.asc()) // 按员工的开始日期升序排序
    .take(10) // 取前10个结果
```

举个例子，想象一个对象类型`claims`，其中包含某保险公司的事故索赔文本。我们希望找到一个涉及红色汽车和鹿的特定索赔。没有`.orderByRelevance()`这一行时，任何包含`red`、`car`、`collision`、`with`或`deer`中的任何一个词的结果可能会出现在前10个结果中。使用`.orderByRelevance()`这一行时，前10个结果将是包含最多搜索词的索赔，以便最相关的索赔最先出现。

```javascript
const results = Objects.search()
    .claims()
    .filter(doc => doc.text.matchAnyToken("red car collision with deer")) // 过滤文本中包含“red car collision with deer”任何一个词的文档
    .orderByRelevance() // 根据相关性排序
    .take(10) // 取前10个结果
```

## 计算聚合

:::callout{title="聚合限制"}
从 Objects API 返回的聚合限制为**总共10,000个桶**。如果超过此限制，将抛出出错。

当使用 `.topValues()` 进行分桶时，如果数据有超过 1,000 个不同的值，结果将是近似的。在这种情况下，前几个值的列表可能不准确。
:::

### 通过属性对 Objects 进行分组

在很多情况下，没有必要加载对象集中的所有 Objects。相反，您可以简单地加载一个分桶的值聚合来进行进一步分析。

要开始计算聚合，请在对象集上调用 `.groupBy()` 方法。这允许您在对象集中的对象类型的一个[可搜索](API%EF%BC%9A%E5%AF%B9%E8%B1%A1%E9%9B%86.md#searchable_note)属性上指定分桶。例如，以下代码按员工的起始日期对员工进行分组：

```typescript
Objects.search()
    .employees()
    // 按员工入职日期分组，单位为天
    .groupBy(e => e.startDate.byDays())
```

在指定按哪个属性进行分组时，您需要根据属性类型提供有关如何进行分组的附加信息：

* 对于 `boolean` 属性，唯一的选项是 `.topValues()`。这将返回两个桶，一个用于 `true` 和一个用于 `false`。
* 对于字符串属性，有两个选项：
  * `.topValues()`：用于快速响应时间和属性具有较小基数的情况。这将按字符串属性的前 1,000 个值进行分组。此限制是为了确保返回的聚合不会过大。
  * `.exactValues()`：用于更精确的聚合，并有可能考虑最多 10,000 个桶以用于高基数属性。可通过 `.exactValues({"maxBuckets": numBuckets})` 指定考虑的桶的数量，其中 `numBuckets` 必须是 0 到 10,000 之间的整数值。由于需要考虑更多结果，因此此方法的响应时间可能较长。
* 对于数值属性（例如 `Integer`、`Long`、`Float`、`Double`），有两个分组选项：
  * `.byRanges()` 允许您指定应使用的确切范围。例如，您可以使用 `.byRanges({ min: 0, max: 50 }, { min: 50, max: 100 })` 将对象分组到您在此处指定的 \[0, 50] 和 \[50, 100] 两个范围中。范围的 `min` 是包含的，`max` 是排除的。您可以省略 `min` 或 `max` 来表示包含从 -∞ 到 `max` 或从 `min` 到 ∞ 的值的桶。
  * `.byFixedWidth()` 指定每个桶的宽度。例如，您可以使用 `.byFixedWidth(50)` 将对象分组到每个宽度为 50 的范围中。
* 对于 `LocalDate` 属性，提供了各种方便的方法以便于分组：
  * `.byYear()`
  * `.byQuarter()`
  * `.byMonth()`
  * `.byWeek()`
  * `.byDays()` 将值分组到天。您可以传入用于桶宽度的天数。
* 对于 `Timestamp` 属性，适用与 `LocalDate` 相同的分组选项，并增加以下选项：
  * `.byHours()` 按小时分组值。您可以传入用于桶宽度的小时数。
  * `.byMinutes()` 按分钟分组值。您可以传入用于桶宽度的分钟数。
  * `.bySeconds()` 按秒分组值。您可以传入用于桶宽度的秒数。
* 对于 `Array` 属性，分组选项由数组中元素的类型决定。特别是，对于 `Array<PropertyType>`，您可以获得与 `PropertyType` 相同的分组方法（例如，`Array<boolean>` 获得与 `boolean` 相同的分组方法）。
  * 例如，如果您有一个名为 `employeeSet` 的 `Array<string>`，由 Alice 和 Bob 组成，他们分别在 `["US", "UK"]` 和 `["US"]` 工作过。那么 `employeeSet.groupBy(e => e.pastCountries.exactValue()).count()` 将返回 `{ "US": 2, "UK": 1 }`。

在按一个属性分组后，您可以选择调用 `.segmentBy()` 方法进行进一步分组。这允许您计算由两个[可搜索](API%EF%BC%9A%E5%AF%B9%E8%B1%A1%E9%9B%86.md#searchable_note)属性分组的三维聚合。例如，您可以按员工的起始日期以及他们的角色进行分组，如下所示：

```typescript
Objects.search()
    .employees()
    // 按员工的入职日期进行分组，精确到天
    .groupBy(e => e.startDate.byDays())
    // 按员工角色的最高值进行分段
    .segmentBy(e => e.role.topValues())
```

### 选择聚合指标

在对对象集进行分组后，可以调用各种聚合方法来计算每个桶上的聚合指标。需要属性的方法仅接受标记为[可搜索](API%EF%BC%9A%E5%AF%B9%E8%B1%A1%E9%9B%86.md#searchable_note)的属性。可能的聚合方法有：

* `.count()` 仅返回每个桶中的对象数量
* `.average()` 返回给定数值、时间戳、日期属性的平均值
* `.max()` 返回给定数值、时间戳、日期属性的最大值
* `.min()` 返回给定数值、时间戳、日期属性的最小值
* `.sum()` 返回给定数值属性的值之和
* `.cardinality()` 返回给定属性的不同值的近似数量

调用这些方法之一将返回`TwoDimensionalAggregation`或`ThreeDimensionalAggregation`。如果在调用最终聚合方法之前调用了`.segmentBy()`，则返回`ThreeDimensionalAggregation`。

[了解更多关于这些聚合类型的结构，包括**有效的分桶类型**。](../TypeScript%20basics/%E8%BE%93%E5%85%A5%E5%92%8C%E8%BE%93%E5%87%BA%E7%B1%BB%E5%9E%8B.md#aggregations)

请注意，结果聚合被包装在一个`Promise`中，因为计算聚合需要从远程服务加载数据。你可以使用[async/await ↗](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/async_function)语法来解包`Promise`结果。

下面是加载聚合并将其作为结果返回的完整示例。

```typescript
import { Function, ThreeDimensionalAggregation } from "@foundry/functions-api";
import { Objects } from "@foundry/ontology-api";

export class AggregationFunctions {
    @Function()
    public async employeesByRoleAndOffice(): Promise<ThreeDimensionalAggregation<string, string>> {
        return Objects.search()
            .employee() // 搜索员工对象
            .groupBy(e => e.title.topValues()) // 按员工职位分组
            .segmentBy(e => e.office.topValues()) // 按办公室位置细分
            .count(); // 统计每个组的员工数量
    }
}
```

以下是一个不使用groupBy语句进行聚合的完整示例：

```typescript
import { Function } from "@foundry/functions-api";
import { Objects } from "@foundry/ontology-api";

export class AggregationFunctions {
    @Function()
    public async employeesStats(): Promise<Double> {
        // 计算所有员工的数量，如果 count() 返回 undefined，则默认为零
        return Objects.search().employee().count() ?? 0;
    }
}
```

您还可以通过替换上面代码示例中的相应行来执行其他聚合操作，而无需groupBy，例如：

* 所有员工的数量: `Objects.search().employee().count();` （如上例所示）
* 员工的平均任期: `Objects.search().employee().average(e => e.tenure);`
* 员工的最大任期: `Objects.search().employee().max(e => e.tenure);`
* 员工的最小任期: `Objects.search().employee().min(e => e.tenure);`
* 所有员工薪资的总和: `Objects.search().employee().sum(e => e.salary);`
* 办公室的数量: `Objects.search().employee().cardinality(e => e.office);`

有关在内存中操作聚合结果的示例，请参阅[创建自定义聚合](%E5%88%9B%E5%BB%BA%E8%87%AA%E5%AE%9A%E4%B9%89%E8%81%9A%E5%90%88.md)指南。
