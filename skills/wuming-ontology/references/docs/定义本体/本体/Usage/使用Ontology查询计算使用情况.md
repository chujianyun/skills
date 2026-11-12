:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 使用Ontology查询计算使用情况

Foundry Ontology是一个数据后台，将基于文件的数据映射到以组织为中心的Object，并为数据探索、数据分析、操作数据编辑、场景分析等提供高速查询服务。Ontology将数据存储在多模态存储后端中，每个后端都有其自己的用途，并可以在单个请求中灵活查询。查询Foundry Ontology需要了解一些基础概念，下面将讨论这些概念。

:::callout{theme="neutral"}
如果您与Palantir签订了企业合同，请在进行计算使用量计算之前联系您的Palantir代表。
:::

## 核心概念：Object类型和对象集

第一个重要概念是**object类型**及其对应的**对象集**之间的区别。**object类型**是实体本身的语义表示（例如Object的名称和属性）。

一个object类型有一个对应的**对象集**，其中包含Objects本身。**对象集**的大小对应于传入数据集的行数以及Ontology操作创建和删除的Objects数量。

## 核心概念：查询类型

第二个重要概念是**查询类型**的概念，包括筛选、聚合、搜索范围和数据输出操作。每种查询类型都需要计算来执行。

* 筛选将考虑整个对象集，并应用筛选条件以生成更小的输出集。
* 聚合将获取输入对象集，并在集合中所有Objects的一个属性上运行聚合函数（如`sum`或`avg`）。
* 搜索范围将获取传入对象集，并根据传入集的某个属性在另一个对象集上运行二次筛选。
* 数据输出操作将替换指定对象集中的Object属性的值。

[查看API文档以了解有关查询类型的更多信息。](https://www.palantir.com/docs/foundry/api/ontology-resources/objects/aggregate)

在使用Foundry Ontology时，**查询类型**通过以下[Foundry应用程序](../../../%E5%9F%BA%E4%BA%8EOntology%E7%9A%84%E5%BA%94%E7%94%A8%E7%A8%8B%E5%BA%8F.md)对**对象集**执行：

* Object Explorer
* Workshop
* Quiver
* Slate
* Vertex
* Foundry Rules
* Foundry Machinery
* Object APIs (OPIs)

从这些来源中的任何一个查询Ontology将使用计算秒来运行查询，如下所示：

* 固定的、最低数量的查询开销计算秒。
* 额外的扩展数量的计算秒，这些计算秒通过用于服务查询的计算量来测量。

## 使用Ontology对象查询测量Foundry计算

### 使用Object Storage v1测量计算

Object Storage v1（Phonograph）在耐用的、水平可扩展的集群中存储在分布式索引集中。 在这些索引中，数据位于大型数据结构中，由Ontology查询引擎遍历。执行查询时，引擎可以通过遍历索引来避免在搜索过程中处理大量数据。此过程称为"剪枝"。

使用此引擎，您可以通过评估最多1000倍更少的记录来搜索数十亿条记录。每次对记录的物理评估称为"命中"。Object Storage v1旨在将每次查询中的命中次数降到最低。

### 使用Object Storage v2测量计算

Object Storage v2（OSv2）以Palantir优化的增强索引格式存储Objects，以实现高速索引、搜索范围和数据输出，以及顺利地与多个计算后端进行交接以完成复杂任务。这包括作为查询一部分的完全并行化Spark计算。

鉴于Object Storage v2也使用高效的索引结构，与Object Storage v1的**命中**原则相同适用于基本查询。然而，按需Spark容器也可用在查询过程中旋转。

对Object Storage v2后端中的Objects进行的查询按以下模式使用计算：

* 对于Object Storage v1后端中的Objects，每个查询有固定的`16`计算秒开销。
* 对于Object Storage v2后端中的Objects，每个查询有固定的`4`计算秒开销。Object Storage v2的优化结构需要的开销比Object Storage v1少，因此固定计算秒开销减少。
* 当通过查询的剪枝过程进行计算工作时，需要额外的计算秒。额外的计算秒随着索引中的Object数量以及查询类型而扩展。
* 在Object Storage v2（OSv2）中，索引剪枝同样需要额外的计算秒。然而，当在超过100,000个Objects上运行搜索范围，或在单个请求中对超过10,000个Objects进行数据输出操作时，OSv2还支持按需Spark集群搜索。这些Spark集群与平台上所有其他基于Spark的应用程序使用方式相同。请参阅[并行化计算文档](https://www.palantir.com/docs/foundry/resource-management/usage-types/)以获取描述。
* 写回Ontology的操作有最低开销。每个操作有`18`计算秒开销。操作也随着在写回请求中编辑的Objects数量进行扩展，每多编辑一个Object实例则额外增加`1`计算秒。
* 通过Functions运行的函数在Objects上有最低开销。具体来说，每个函数执行有固定的`4`计算秒开销。

**下表总结了每种查询类型的最低计算秒使用情况。**

| 查询类型          | 最低计算秒          |
|-----------------|----------------------|
| Ontology V1查询 | 16                   |
| Ontology V2查询 | 4                    |
| Objects上操作     | 18                   |
| Objects上函数     | 4                    |

## 理解Ontology查询的Foundry计算使用驱动因素

* 作为非常简单的规则，每个查询的固定计算使用量随查询数量线性增长。执行较少的查询将减少总计算使用量。
* 对对象集服务的更复杂查询（例如通用多对象搜索）将启动对每个object类型的多个子查询。将搜索限制为单个object类型以减少使用的查询数量。
* 对较小对象集的查询将使用较少的计算，因为查询中的**命中**次数与被查询的对象集的大小成正比。
* 在执行其他操作之前进行的前期筛选将利用高度索引的后台结构。这将减少查询中的**命中**次数，从而减少总体计算使用量。这在聚合和搜索范围中特别重要，因为筛选后的对象集比完整对象集需要更少的计算来处理。

## 调查Ontology查询的Foundry计算使用情况

在Foundry中，计算秒被归因于平台中的资源，而不是与这些资源交互的用户。

当涉及到Ontology查询时，有多种方式可以归因于计算。作为一般规则，计算附加到查询来源的资源。然而，当没有用于生成计算的已保存资源（例如通过API）时，计算将附加到被查询的object类型。如果在单个请求中查询多个Objects，则通过在Objects之间平均分配来归因于计算。

以下资源类型的Ontology查询计算归因于它们，而不是底层Objects：

* Workshop应用程序
* Carbon页面
* Quiver分析和仪表盘
* Vertex应用程序
* Slate应用程序
* Foundry Machinery应用程序
* Foundry Rules资源
* Foundry Automate
* AIP Logic

以下交互模式的Ontology查询计算直接附加到它们查询的object类型上，因为没有可以附加计算的固定资源。

* Object Explorer
* Object APIs（包括OSDK）
