:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Object标识符

在Foundry中，Object的身份有几种不同的表示方式，理解这些不同的表示对于在函数中编写正确的代码非常重要。本节解释了对象标识的各种方式以及对代码的影响。

## 标识符类型

### Object RIDs

"RID"指的是[资源标识符 ↗](https://github.com/palantir/resource-identifier)，这是Palantir用于标识实体的开源规范。Ontology对象在创建时会被指派一个RID，创建方式可以是通过索引支持的数据集，或者作为操作的一部分。

在函数中，每个[Ontology对象](API-%20Object%E5%92%8C%E9%93%BE%E6%8E%A5.md)都有一个类型为`string | undefined`的`rid`字段。RID可能未定义的原因是可以使用[对象创建](../Ontology%20edits/API-%20Ontology%E7%BC%96%E8%BE%91.md#creating-objects)API在函数中创建新对象。新创建的对象总是具有`undefined`的`rid`值，而现有对象总是具有已定义的`rid`。

### 主键

Object还可以通过其对象类型和主键唯一标识。主键是唯一的`propertyId`和值对。例如，Employee对象类型可以通过一个名为`employeeId`的`字符串`属性唯一标识。

所有Ontology对象总是具有`typeId`和`primaryKey`字段，包括新创建的对象。这是因为在创建新对象时必须提供主键。

## 对代码的影响

### 检查相等性

在函数中，每个Ontology对象都使用[JavaScript对象 ↗](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Object)表示。一个Ontology对象可能会被表示为多个JavaScript对象。例如，如果您多次从[Object搜索](API%EF%BC%9A%E5%AF%B9%E8%B1%A1%E9%9B%86.md)加载Ontology对象，或者在对象搜索中加载对象以及将其作为参数传入，这种情况就可能发生：

```typescript
public myFunction(employee: Employee): void {
    // 使用搜索功能查找与传入的员工ID完全匹配的员工
    const employee2 = Objects.search().employee()
        .filter(e => e.id.exactMatch(employee.id))
        .all()[0];

    // 打印比较结果：使用 == 比较两个员工对象
    console.log(employee == employee2); // false

    // 打印比较结果：使用 === 比较两个员工对象
    console.log(employee === employee2); // false

    // 打印比较结果：比较两个员工对象的ID属性
    console.log(employee.id === employee2.id); // true
}
```

此代码片段用于比较员工对象。虽然 `employee` 和 `employee2` 是不同的对象实例（因此 `==` 和 `===` 比较都返回 `false`），但它们的 `id` 属性相同（因此 `employee.id === employee2.id` 返回 `true`）。
即使在上述示例中，`employee` 和 `employee2` 都指的是相同概念的Ontology对象，用 `==` 和 `===` 运算符比较它们会返回 `false`，因为变量指向两个不同的 JavaScript 对象。简单地比较 `rid` 字段可能会有问题，因为新创建的对象的 `rid` 为 `undefined`。

因此，比较两个Ontology对象是否相等的最佳方法是比较 `typeId` 和 `primaryKey`:

```typescript
function isEqual(o1: OntologyObject, o2: OntologyObject) {
    // 检查两个OntologyObject对象的typeId和primaryKey是否相等
    return o1.typeId === o2.typeId
        && JSON.stringify(o1.primaryKey) == JSON.stringify(o2.primaryKey);
}
```

### Object 映射

将 Object 映射到某个值通常是有用的。例如，您可能希望遍历一个对象数组并存储值以便更高效地查找。

由于上述相等性检查问题，您不能简单地使用 JavaScript Map 来为每个 Object 存储值。相反，您可以使用 [FunctionsMap](../TypeScript%20basics/%E8%BE%93%E5%85%A5%E5%92%8C%E8%BE%93%E5%87%BA%E7%B1%BB%E5%9E%8B.md#collections)，它专门设计用于支持 OntologyObjects 作为键。
