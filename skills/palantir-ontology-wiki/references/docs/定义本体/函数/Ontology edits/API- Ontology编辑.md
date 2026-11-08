:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# API: Ontology编辑

除了编写基于Ontology返回衍生值的函数外，您还可以编写函数以编辑Ontology中对象的属性和链接。本页面记录了可用于函数的对象编辑API。有关编辑函数如何工作的详细信息，请参阅[概述页面](%E6%A6%82%E8%BF%B0.md)。

为了在操作环境中实际使用，**Ontology编辑函数必须配置为操作**，称为[函数支持的操作](../../%E5%8A%A8%E4%BD%9C%E7%B1%BB%E5%9E%8B/Function-backed%20actions/%E6%A6%82%E8%BF%B0.md)。以这种方式配置操作可以让您提供额外的元数据、配置权限，并在各种操作界面中访问操作。如[文档](%E6%A6%82%E8%BF%B0.md#when-edits-are-applied)中所述，在操作之外运行编辑函数实际上不会修改任何对象数据。

:::callout{theme="warning" title="警告"}
在编辑对象后搜索它们可能会返回意外结果。详情请参阅[注意事项部分](%E6%A6%82%E8%BF%B0.md#caveat-edits-and-object-search)。
:::

## 声明编辑函数

编辑Ontology的函数必须：

* 使用从`@foundry/functions-api`导入的`@OntologyEditFunction()`装饰器进行装饰
* 使用从`@foundry/functions-api`导入的`@Edits([object type])`装饰器进行装饰，以指定将要编辑的对象类型
* 明确具有`void`返回类型

## 更新属性

您可以通过简单地重新指派对象的属性值来编辑属性值。例如：

```typescript
employee.lastName = newName; // 将员工的姓氏更新为新的名字
```

如果在同一函数执行过程中访问 `lastName` 属性值，将返回您刚刚设置的新值。

对象上的[数组属性](../Functions%20on%20objects/API-%20Object%E5%92%8C%E9%93%BE%E6%8E%A5.md#array-properties)是使用 `ReadOnlyArray` 类型生成的。要修改数组，请创建它的副本，修改该副本，然后更新属性：

```typescript
// 复制到一个新数组
let arrayCopy = [...myObject.myArrayProperty];
// 现在你可以修改复制的数组
arrayCopy.push(newItem);
// 然后覆盖属性值
myObject.myArrayProperty = arrayCopy;
```

请注意，您无法更新现有Object的主键属性值。

## 更新链接

`SingleLink`和`MultiLink`接口有多种方法可用于更新链接：

```typescript
// 设置员工的主管
employee.supervisor.set(newSupervisor);

// 清除员工的主管
employee.supervisor.clear();

// 为给定的员工添加新的报告
employee.reports.add(newReport);

// 删除与给定员工关联的旧报告
employee.reports.remove(oldReport);
```

正如更新属性一样，在更新后访问链接将反映出您所做的更新。

## 创建对象

您可以使用 `@foundry/ontology-api` 中提供的 `Objects.create()` 接口创建新对象。在创建新对象时，您必须为其主键指定一个值。

在此示例中，我们创建一个新的 Ticket 对象，指定其 ID，设置其 `dueDate` 属性，并通过修改 `assignedTickets` 链接指派给指定的 Employee。

```typescript
import { OntologyEditFunction, Edits } from "@foundry/functions-api";
import { Employee, Objects, Tickets } from "@foundry/ontology-api";

export class TicketActionFunctions {
    // 使用装饰器标注，该方法会编辑Employee和Tickets对象
    @Edits(Employee, Tickets)
    // 标记该方法为本体编辑函数
    @OntologyEditFunction()
    public createNewTicketAndAssignToEmployee(employee: Employee, ticketId: Integer): void {
        // 创建一个新的工单对象
        const newTicket = Objects.create().ticket(ticketId);

        // 设置工单的截止日期为当前日期加7天
        newTicket.dueDate = LocalDate.now().plusDays(7);

        // 将新工单添加到员工的已分配工单列表中
        employee.assignedTickets.add(newTicket);
    }
}
```

## 删除Objects

您可以通过调用`.delete()`方法删除一个Object。

在这个例子中，我们删除指派给指定员工的所有工单。

```typescript
const tickets = employee.tickets.all(); // 获取员工的所有工单
tickets.forEach(ticket => ticket.delete()); // 遍历每个工单并删除
```
