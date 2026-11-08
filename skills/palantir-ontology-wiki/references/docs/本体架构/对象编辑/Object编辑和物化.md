:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Object编辑和物化

Foundry Ontology通过结合来自各种数据源的数据和用户驱动的Object编辑，支持操作流程，帮助生成洞察，并维护对您重要事物的最新表示。在Foundry Ontology中，用户可以通过应用[操作](../../%E5%AE%9A%E4%B9%89%E6%9C%AC%E4%BD%93/%E5%8A%A8%E4%BD%9C%E7%B1%BB%E5%9E%8B/%E6%A6%82%E8%BF%B0.md)编辑属性值、添加和删除链接以及创建和删除Object。

Foundry中的操作是一个单一事务，根据用户定义的逻辑更改一个或多个Object的属性。操作使您能够在思考整体目标的同时使用和管理数据，而不是追逐特定的属性编辑。操作可以从Foundry应用程序（如[Workshop](https://www.palantir.com/docs/foundry/workshop/actions-use/)和[Object视图](../../%E5%BA%94%E7%94%A8/%E5%AF%B9%E8%B1%A1%E8%A7%86%E5%9B%BE/%E6%A6%82%E8%A7%88.md)）或通过[Foundry APIs](../../%E5%AE%9A%E4%B9%89%E6%9C%AC%E4%BD%93/%E5%8A%A8%E4%BD%9C%E7%B1%BB%E5%9E%8B/%E5%9C%A8%E5%B9%B3%E5%8F%B0%E4%B8%AD%E4%BD%BF%E7%94%A8%E6%93%8D%E4%BD%9C.md)从外部应用程序触发。有关如何配置和应用操作的更多信息，请参见[操作文档](../../%E5%AE%9A%E4%B9%89%E6%9C%AC%E4%BD%93/%E5%8A%A8%E4%BD%9C%E7%B1%BB%E5%9E%8B/%E6%A6%82%E8%BF%B0.md)。

本节的其他页面讨论了启用操作所需的Object类型和链接类型配置，以及Ontology中支持用户驱动编辑的基础机制。

:::callout{theme="warning"}
[具有Foundry流数据源的Object类型](../%E5%AF%B9%E8%B1%A1%E6%9D%83%E9%99%90%E7%AE%A1%E7%90%86/%E7%AE%A1%E7%90%86Object%E7%B1%BB%E5%9E%8B%E5%92%8CObject%E5%AE%9E%E4%BE%8B%E5%AE%89%E5%85%A8%E6%80%A7.md#object-input-datasources)尚不支持操作
:::
