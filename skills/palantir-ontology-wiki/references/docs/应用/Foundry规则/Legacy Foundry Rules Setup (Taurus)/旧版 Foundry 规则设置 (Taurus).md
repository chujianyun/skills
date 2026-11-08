:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# 旧版 Foundry 规则设置 (Taurus)

:::callout{theme="warning"}
在2022年7月之前，Foundry 规则（以前称为Taurus）需要额外的配置，并使用略有不同的概念。以下文档涵盖了此版本与新版Foundry规则之间的差异。
:::

## 变换管道

以前，用户需要创建和维护一个运行规则的[代码库](https://www.palantir.com/docs/foundry/code-repositories/overview/)，而不是由Foundry规则自动生成**变换管道**。

了解更多关于创建和[更新此代码库](%E9%85%8D%E7%BD%AE%E5%8F%98%E6%8D%A2%E7%AE%A1%E9%81%93.md)的信息。

## Workshop 应用程序

以前，[规则输入](../Core%20concepts/%E8%A7%84%E5%88%99%E9%80%BB%E8%BE%91.md#inputs)不是在[工作流配置编辑器](../Core%20concepts/Foundry%20Rules%20%E5%B7%A5%E4%BD%9C%E6%B5%81%E9%85%8D%E7%BD%AE.md)中配置的，而需要在Workshop应用程序和变换管道中配置。

此外，规则输出需要在三个位置配置：Workshop应用程序、变换管道和[Ontology 管理器](../../%E6%9C%AC%E4%BD%93%E7%AE%A1%E7%90%86%E5%99%A8/%E6%A6%82%E8%BF%B0.md)。在下面的[规则操作](#rule-actions)部分中了解更多关于旧版规则输出的信息。

了解更多关于在[Workshop应用程序](%E9%85%8D%E7%BD%AE%20Workshop%20%E5%BA%94%E7%94%A8%E7%A8%8B%E5%BA%8F.md)和[变换管道](%E9%85%8D%E7%BD%AE%E5%8F%98%E6%8D%A2%E7%AE%A1%E9%81%93.md)中添加和移除规则输入的信息。

## 规则操作

在[工作流输出](../Core%20concepts/Foundry%20Rules%20%E5%B7%A5%E4%BD%9C%E6%B5%81%E9%85%8D%E7%BD%AE.md#workflow-outputs)之前，输出模式的强制执行是通过Foundry操作实现的。操作的参数代表数据集列，必须映射到由逻辑输出的列或用户输入的静态值。在[变换内部](%E9%85%8D%E7%BD%AE%E5%8F%98%E6%8D%A2%E7%AE%A1%E9%81%93.md#rule-action-datasets)可以访问规则操作，以检索指定格式的所有匹配行。当检索指定规则操作的结果时，*产生的数据集将包含使用该操作的所有规则输出的行*。这样设计是为了更容易实现所有Foundry规则输出的一致性。作为Foundry操作，它们必须在Ontology管理器中配置。

了解更多关于[配置规则操作](%E9%85%8D%E7%BD%AE%E8%A7%84%E5%88%99%E6%93%8D%E4%BD%9C.md)的信息。

:::callout{theme="neutral"}
虽然规则操作是通过Foundry操作配置的，但操作并不直接在相关Object上执行。目前，唯一的效果是指定输出模式。
:::

:::callout{theme="neutral"}
一些在2021年1月之前部署的旧版Foundry规则（以前称为Taurus）需要升级才能使用规则操作。除非您被特别指示，否则您可能不需要这样做。

了解更多关于[升级以使用规则操作](%E5%8D%87%E7%BA%A7%E4%BB%A5%E4%BD%BF%E7%94%A8%E8%A7%84%E5%88%99%E6%93%8D%E4%BD%9C.md)的信息。
:::
