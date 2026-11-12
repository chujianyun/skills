:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Ontology 更改

除了编写从 Ontology 读取数据的函数外，您还可以编写创建对象并编辑对象之间属性和链接的函数。 本页记录了函数中可用的对象编辑 API。 有关编辑函数如何工作的更多详细信息，请参阅[概述页面](../Ontology%20edits/%E6%A6%82%E8%BF%B0.md)。

为了使函数中创建的更改实际应用，Ontology 编辑函数*必须配置为[函数支持的操作](../../%E5%8A%A8%E4%BD%9C%E7%B1%BB%E5%9E%8B/Function-backed%20actions/%E6%A6%82%E8%BF%B0.md)*。 以这种方式配置操作可以让您提供附加元数据、配置权限，并在各种操作接口中访问操作。 正如[文档](../Ontology%20edits/%E6%A6%82%E8%BF%B0.md#when-edits-are-applied)中所指出的那样，在操作之外运行编辑函数实际上不会修改任何对象数据。

:::callout{theme="warning" title="警告"}
编辑后立即搜索对象可能会返回意外结果。 详情请参见[注意事项部分](../Ontology%20edits/%E6%A6%82%E8%BF%B0.md#caveat-edits-and-object-search)。
:::

## 定义编辑函数

编辑 Ontology 的函数必须：

* 使用从 `functions.api` 导入的 `@function(edits=[MyObjectType])` 装饰器来指定将要编辑的对象类型。
* 具有从 `functions.api` 导入的显式 `Array[OntologyEdit]` 返回类型提示。

## 构建 Ontology 编辑容器

要在 Python 函数中执行 Ontology 编辑，首先从 [OSDK 客户端](%E5%AF%B9%E8%B1%A1%E4%B8%8A%E7%9A%84%E5%87%BD%E6%95%B0.md)构建一个 Ontology 编辑容器。例如：

```python
ontology_edits = FoundryClient().ontology.edits()
# 创建一个FoundryClient实例，并通过它获取ontology的edits
# FoundryClient是一个用于连接Foundry平台的客户端库
# ontology是指本体，用于定义概念及其关系
# edits可能是指对本体的编辑或修改操作
```

这个容器用于跟踪在函数中所做的所有编辑。

## 更新属性

在Python函数中的Ontology对象默认是只读的。尝试修改其属性将引发异常。

为了编辑一个对象，首先需要使用Ontology编辑容器获取该对象的可编辑视图，可以从现有对象实例获取：

```python
# 调用 `MyObjectType` 类中的 `edit` 方法来编辑 `my_object` 对象
editable_object = edits.objects.MyObjectType.edit(my_object)
```

或给定一个Object主键：

```python
# 使用 MyObjectType 的 edit 方法编辑对象
editable_object = edits.objects.MyObjectType.edit(object_primary_key)
```

一旦您有一个可编辑的Object，您可以通过重新指派Object的属性值来编辑属性值。例如：

```python
# 将可编辑的员工对象的姓氏更新为新名称
editable_employee.last_name = new_name
```

在同一函数执行过程中，随后访问`editable_employee`的`last_name`属性值将返回刚刚设置的新值。然而，原始的不可编辑Object将不会反映这些更改。

可编辑Object上的[数组属性](../Functions%20on%20objects/API-%20Object%E5%92%8C%E9%93%BE%E6%8E%A5.md#array-properties)是只读的。要修改数组，请创建其副本，修改副本，然后更新属性：

```python
# 复制到一个新的数组
array_copy = list(editable_object.my_array_property)
# 现在你可以修改复制的数组
array_copy.append(new_item)
# 然后覆盖属性的值
editable_object.my_array_property = array_copy
```

请注意，现有Object的主键属性值无法更新。

## 更新链接

单链接和多链接属性有多种方法可以用于更新链接：

```python
# 设置员工的主管
editable_employee.supervisor.set(new_supervisor)

# 清除员工的主管
editable_employee.supervisor.clear()

# 给指定员工添加新的报告
editable_employee.reports.add(new_report)

# 删除与指定员工关联的旧报告
editable_employee.reports.remove(new_report)
```

与更新属性一样，在更新后访问 `editable_employee` 的链接将反映您所做的更新。

## 创建Objects

您可以使用Ontology编辑容器上的 `MyObjectType.create()` 方法创建新的Objects。创建新的Object时，必须为其主键指定一个值。

在此示例中，我们创建一个具有给定ID的新Ticket Object，设置其 `due_date` 属性，并通过修改 `assigned_tickets` 链接将其指派给给定的Employee。

```python
from datetime import datetime, timedelta

from functions.api import function, Integer, Array, OntologyEdit
from ontology_sdk import FoundryClient
from ontology_sdk.ontology.objects import Employee, Ticket

@function(edits=[Employee, Ticket])
def create_new_ticket_and_assign_to_employee(employee: Employee, ticket_id: Integer) -> list[OntologyEdit]:
    # 创建本体编辑客户端实例
    ontology_edits = FoundryClient().ontology.edits()

    # 创建新的工单对象，并设置其ID
    new_ticket = ontology_edits.objects.Ticket.create(ticket_id)
    # 设置工单的截止日期为当前日期加上7天
    new_ticket.due_date = datetime.now() + timedelta(days=7)

    # 获取可编辑的员工对象
    editable_employee = ontology_edits.objects.Employee.edit(employee)
    # 将新创建的工单添加到员工的已分配工单中
    editable_employee.assigned_tickets.add(new_ticket)

    # 返回所有的编辑操作
    return ontology_edits.get_edits()
```

此代码定义了一个函数 `create_new_ticket_and_assign_to_employee`，用于创建一个新的工单并将其分配给指定的员工。通过使用 `FoundryClient` 创建和编辑本体对象，函数将新工单添加到员工的已分配工单列表中，并返回所有的编辑操作。
属性值也可以直接传递给创建方法，除了主键。例如：

```python
new_due_date = datetime.now() + timedelta(days=7)
# 创建一个新的工单，并设置其到期日期为当前日期加7天
new_ticket = ontology_edits.objects.Ticket.create(ticket_id, due_date=new_due_date)
```

## 删除Objects

您可以通过在Ontology编辑容器上调用`MyObjectType.delete()`方法来删除一个Object。

在此示例中，我们删除指派给指定员工的所有票据：

```python
for ticket in employee.tickets:
    # 遍历员工的票据列表，并删除每个票据
    ontology_edits.objects.Ticket.delete(ticket)
```

可以使用主键而不是实例来删除Objects：

```python
# 删除指定 ID 的 Ticket 对象
ontology_edits.objects.Ticket.delete(ticket_id)
```
