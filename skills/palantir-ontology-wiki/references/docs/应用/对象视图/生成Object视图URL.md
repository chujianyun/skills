:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 生成Object视图URL

在开发Object视图的过程中，您可能需要生成指向特定Object或搜索Object的URL。

如果您是在iframe中嵌入这些视图而不是将它们作为链接提供，请附加URL查询参数`embedded=true`，这将加载没有Workspace侧边栏的视图。

:::callout{theme="neutral"}
要了解如何创建指向搜索或Exploration的URL，请参阅[生成Object Explorer URL](../%E5%AF%B9%E8%B1%A1%E6%B5%8F%E8%A7%88%E5%99%A8/%E7%94%9F%E6%88%90%20Object%20Explorer%20%E9%93%BE%E6%8E%A5.md)。
:::

## 生成Object链接

有两种方法可以链接到URL。

**选项1**

`/workspace/hubble/external/object/v0/<object-type-id>?<primary-key-property-id>=<primary-key-property-value>`

例如：

`/workspace/hubble/external/object/v0/aircraft?aircraftId=1234`

**选项2**

`/workspace/hubble/external/search/v2/?objectId=<objectRid>`

当主键属性值可能包含特殊字符时，推荐使用这种方式。

此URL在Object Explorer的上下文中加载Object视图。要加载没有额外包装的Object视图（例如，用于iframe中），请创建类似`/workspace/hubble/objects/<objectRid>`的URL。
