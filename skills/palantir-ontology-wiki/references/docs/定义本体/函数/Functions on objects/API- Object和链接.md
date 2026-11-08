:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# API: Object和链接

导入到项目中的每个[Object类型](../../%E5%AF%B9%E8%B1%A1%E9%93%BE%E6%8E%A5%E7%B1%BB%E5%9E%8B/Object%20types/%E6%A6%82%E8%A7%88.md)都会转换为TypeScript API，以便您可以轻松访问和操作Foundry中可用的Object。

### 属性

每个Object类型的[属性](../../%E5%AF%B9%E8%B1%A1%E9%93%BE%E6%8E%A5%E7%B1%BB%E5%9E%8B/Properties/%E6%A6%82%E8%A7%88.md)都会转换为为每个Object类型生成的TypeScript接口上的字段。生成的字段名称使用Ontology中指定的API名称。

您可以通过简单的点符号访问每个属性的字段：

```typescript
const firstName = employee.firstName; // 获取员工的名字
```

请注意，由于属性可能没有设置具体值，因此访问属性值时返回的类型可能是`undefined`。TypeScript编译器会给出错误，除非您明确处理`undefined`情况。有关详细信息，请参阅[此指南](../TypeScript%20basics/%E5%A4%84%E7%90%86%E6%9C%AA%E5%AE%9A%E4%B9%89%E5%80%BC.md)。

#### 数组属性

对象类型上的数组属性会转换为`ReadOnlyArray`类型。这是为了使[编辑](../Ontology%20edits/API-%20Ontology%E7%BC%96%E8%BE%91.md)数组属性的语义清晰——修改数组属性值的唯一方法是用一个全新的数组值更新它。

如果您想操作数组属性的值，请制作它的副本：

```typescript
// 复制到一个新数组
let arrayCopy = [...myObject.myArrayProperty]; // 使用扩展运算符复制数组
// 现在可以修改复制的数组
arrayCopy.push(newItem); // 向复制的数组中添加新元素
```

### 链接类型

Object类型之间的[链接类型](../../%E5%AF%B9%E8%B1%A1%E9%93%BE%E6%8E%A5%E7%B1%BB%E5%9E%8B/Link%20types/%E6%A6%82%E8%BF%B0.md)也被转换为每个Object类型的TypeScript接口中的字段。要遍历链接，请访问该字段，然后调用用于加载Object的方法之一。链接类型字段名称是使用Ontology中指定的API名称生成的。

Foundry Ontology支持定义1对1、1对多和多对多的链接类型。当访问链接的`1`端时，生成的字段为`SingleLink`类型。您可以使用`get()`或`getAsync()`方法访问链接的Object：

```typescript
const manager = employee.manager.get(); // 获取员工的管理者对象
```

与属性一样，当您遍历一对一或多对一链接时，如果没有链接的Object，返回值可能是`undefined`。请遵循[指南](../TypeScript%20basics/%E5%A4%84%E7%90%86%E6%9C%AA%E5%AE%9A%E4%B9%89%E5%80%BC.md)以处理这些链接的`undefined`值。

当访问链接的`many`端时，生成的字段是`MultiLink`类型。您可以使用`all()`或`allAsync()`方法访问链接对象的数组。如果没有链接对象，这些方法将返回一个空数组。

```typescript
const employees = employee.reports.all(); // 获取所有员工的报告
```

遍历链接可能开销较大，因为这需要在后端加载哪些对象被链接。有关如何更高效地执行链接遍历的详细信息，请参见[此部分](../Performance%20and%20limits/%E4%BC%98%E5%8C%96%E6%80%A7%E8%83%BD.md#optimizing-link-traversals)。

从调用`.all()`或`.allAsync()`返回的链接对象数组是一个`ReadOnlyArray`。如果您想修改该数组，请先制作其副本：

```typescript
let copiedEmployees = [...employee.reports.all()];
// 复制 employee 对象中 reports 的所有记录到 copiedEmployees 数组中
```

您可以将链接作为`对象集`遍历，以避免在内存中加载链接的Object实例。当在Ontology中创建链接时，将在此类型的对象集上生成API，以“搜索周围”其他链接的对象集。

```typescript
import { ObjectSet, Employee } from "@foundry/ontology-api";

// 假设你有一个对象集可用：
// const employee_id = "123";
// const employeeObjectSet : ObjectSet<Employee> = Objects.search().employee().filter(exactMatch(employee_id));

// 从员工对象集查找与其他对象类型相关的对象集
const linkedObjs: ObjectSet<OtherObjectType> = employeeObjectSet.searchAroundToOtherObjectType();
```

以上代码片段展示了如何从员工对象集中查找与其他对象类型相关的对象集。`searchAroundToOtherObjectType` 方法可以用于检索这些关联对象。
如果您操作一个Object的单一实例并从那里进行搜索，您将得到一个`MultiLink<objectType>`。您不能将这个`MultiLink`转换为`对象集`；您必须将Object实例转换为对象集以便转向其他对象集。

```typescript
// 假设:
// const employee: Employee

// MultiLink可以加载到内存中以便进一步处理。

const linkedObjs: MultiLink<objectType> = employee.reports

// 将单个对象实例转换为对象集。此语句比`employee().filter()`语句耗时更长。
const employeeObjectSet : ObjectSet<Employee> = Objects.search().employee([employee])

// 从这里，你可以使用上面的"searchAroundToOtherObjectType"方法来处理仅对象集。
```

### Ontology 元数据

函数通过提供对象和属性列表来访问可用的Ontology。可以通过访问每个对象类型的常量类型来获取Ontology元数据信息。请参阅以下部分以获取更多详细信息。

#### Object 属性元数据

Object 属性也包括类型元数据，这提供了对每个属性类型的程序化访问。您可以使用此功能进行高级工作流，例如识别给定类型的所有属性或验证给定属性名称是否具有特定类型。

例如，对于包含员工对象**类型**的Ontology，您可以按如下方式访问该对象**类型**属性的类型信息：

```javascript
import { Employee } from "@foundry/ontology-api";
// 导入 Employee 类，来自 @foundry/ontology-api

...
const type = Employee.properties.firstName;
// 获取 Employee 类中属性的 firstName，用于访问员工的名字
```

在这种情况下，如果`firstName`是`Employee`对象类型上的一个字符串属性，那么其类型将是`StringPropertyBaseType`。

可用的属性类型如下：

* `BooleanPropertyBaseType`
* `BytePropertyBaseType`
* `DatePropertyBaseType`
* `FloatPropertyBaseType`
* `TimestampPropertyBaseType`
* `ShortPropertyBaseType`
* `GeohashPropertyBaseType`
* `DecimalPropertyBaseType`
* `StringPropertyBaseType`
* `LongPropertyBaseType`
* `IntegerPropertyBaseType`
* `DoublePropertyBaseType`
* `ArrayPropertyBaseType`
* `VectorPropertyBaseType`
