:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 管理Object类型和Object实例安全性

\*\*Ontology数据（Object类型）\*\*的访问控制和权限管理主要有两种形式：[Object输入数据源](#object-input-datasources)和[细粒度访问控制](#granular-access-controls-in-the-foundry-ontology)。

:::callout{theme="neutral"}
侧边栏中的**检查访问**面板可用于检查某人对Workshop或Slate应用的访问权限，包括对相关Object类型、其数据源和细粒度访问控制的访问。更多信息，请参见[检查访问面板文档](https://www.palantir.com/docs/foundry/security/checking-permissions/)。
:::

## Object输入数据源

Foundry Ontology中[Object实例](../../%E5%AE%9A%E4%B9%89%E6%9C%AC%E4%BD%93/%E5%AF%B9%E8%B1%A1%E9%93%BE%E6%8E%A5%E7%B1%BB%E5%9E%8B/Object%20types/%E6%A6%82%E8%A7%88.md)的数据权限由应用于输入数据源的权限控制。Foundry Ontology中的Object类型可以将三种类型的资源作为其输入数据源：Foundry数据集、Foundry受限视图和Foundry流。正在开发以支持Ontology中的其他数据源类型。

* **[Foundry数据集](https://www.palantir.com/docs/foundry/data-integration/datasets/)：** Foundry数据集是用于在Foundry Ontology中创建Object实例的最常见输入数据源。数据集中的每一行对应于Foundry Ontology中的一个完整Object实例，任何对数据集拥有至少`Viewer`权限的用户都可以访问从该数据集创建的所有Object实例。
* **[Foundry受限视图（RVs）](https://www.palantir.com/docs/foundry/security/restricted-views/)：** Foundry受限视图是用于在Foundry中授予行级权限的资源。受限视图也用于在Foundry Ontology中授予Object实例级别的访问控制。通过满足策略限制来访问受限视图中某特定行的用户，也可以访问从该行创建的Object实例。
* **[Foundry流](https://www.palantir.com/docs/foundry/data-integration/streams/)：** Foundry流是用于Foundry Ontology中低延迟流数据的输入数据源。通过偏离用于非流Foundry数据集的批处理基础设施，流能够在秒或分钟级别将数据索引到Foundry Ontology。任何对流数据源拥有至少`Viewer`权限的用户都可以访问从该流数据源创建的所有Object实例。

## Foundry Ontology中的细粒度访问控制

最常见的Ontology输入数据源是Foundry数据集；对于这些数据集，用户可以访问数据集的所有或无行和列，类似地，也可以访问所有或无对应的Object实例及其属性。然而，一些应用案例和工作流程可能需要比全有或全无数据源或其对应Object更细粒度的Object实例访问控制。

为此，[Foundry受限视图（RVs）](#foundry-restricted-views-rvs)提供行级访问控制，[多数据源Object类型（MDOs）](#multi-datasource-object-types-mdos)则为列或属性级别访问控制提供了解决方案。

### Foundry受限视图（RVs）

Foundry受限视图（RVs）启用对Foundry数据集或Foundry流\[Beta]中某些行的*行级访问控制*，以及从这些行创建的对应Object实例。对具有特定主键的Object实例的访问由能够访问输入受限视图数据源中特定行的人决定。

例如，某个医疗员工可能被允许查看包含其护理中心患者PHI的数据集行和Object实例，但被限制查看仅访问其他护理中心的患者数据，即使这两种类型的数据都存在于同一个数据集和Object类型中。

使用Ontology管理器，可以选择受限视图作为Object类型的输入数据源，与选择Foundry数据集的方式相同。

:::callout{theme="neutral"}
Foundry受限视图（RVs）对Foundry流的支持目前处于测试阶段，可能在您的Foundry注册中不可用。请联系Palantir支持了解更多信息。
:::

[了解更多关于设置RVs和管理Object实例行级权限的信息。](%E9%85%8D%E7%BD%AE%E5%8F%97%E9%99%90%E8%A7%86%E5%9B%BE%E6%94%AF%E6%8C%81%E7%9A%84%E5%AF%B9%E8%B1%A1%E7%B1%BB%E5%9E%8B.md)

### 多数据源Object类型（MDOs）

:::callout{theme="neutral"}
多数据源Object类型（MDOs）仅在Object Storage v2中可用。
:::

Foundry Ontology支持将多个输入数据源映射到单个Object类型。这样的Object类型被称为多数据源Object类型（MDOs）。

MDOs使您可以将来自不同数据源的列映射到Object类型的各种属性上。这反过来又使您可以对单个Object类型应用多个访问控制（对应于单独的输入数据源）。这些输入数据源可以是Foundry数据集或Foundry受限视图的任意组合。

例如，对于一个给定的护理事件Object类型，某些医疗员工可能需要访问包含个人健康信息（PHI）的Object属性，而其他员工不应拥有此访问权限。可以通过用两个独立的输入数据源支持`Care Event` Object类型并在每个输入数据源上应用不同的访问控制和权限来实现这种访问控制。不同的权限将被尊重并应用于Object实例，以便如果用户没有访问输入数据源的权限，则该用户将无法访问从输入数据源映射的属性。

[了解更多关于设置MDOs和管理Object实例列级权限的信息。](%E5%A4%9A%E6%95%B0%E6%8D%AE%E6%BA%90Object%E7%B1%BB%E5%9E%8B%EF%BC%88MDOs%EF%BC%89.md)
