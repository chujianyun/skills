:::callout{theme="warning"}
注意：以下翻译的准确性尚未经过验证。这是使用 [AIP ↗](https://www.palantir.com/platforms/aip/) 从原始英文文本进行的机器翻译。
:::

# Ontology中的模型

组织正在寻求利用人工智能（AI）和机器学习（ML）来加速和改善决策。然而，将AI/ML投入运营的现实是复杂的，投资回报通常难以达到预期。

Foundry提供了弥合这一差距的关键能力：一个可靠的数据基础、用于评估和比较模型与组织目标的工具，以及将模型部署到面向用户的操作工作流程中的功能。此页面重点介绍最后一步：将评估后的模型部署到生产中。

## 端到端工作流程

从高层次上看，这些是在Foundry中实现AI/ML运营化所需的端到端步骤：

1. 创建一个[建模目标](https://www.palantir.com/docs/foundry/model-integration/objectives/)来描述ML项目的组织案例。
2. 模型被创建并提交到目标；模型可以是[在Foundry中开发](https://www.palantir.com/docs/foundry/integrate-models/integrate-overview/)的，也可以是[从外部来源集成](https://www.palantir.com/docs/foundry/integrate-models/external-model-connection/)的。
3. 模型被[评估](https://www.palantir.com/docs/foundry/evaluate-models/model-evaluation-automatic/)以满足定量和定性要求，然后被[部署](https://www.palantir.com/docs/foundry/manage-models/set-up-live/)，以便可以进行交互式查询。
4. 模型输入和输出通过简单的点击界面[映射到Ontology概念](https://www.palantir.com/docs/foundry/model-integration/objectives/)。
5. 完成Ontology映射后，模型无缝可用于[应用程序开发](https://www.palantir.com/docs/foundry/workshop/scenarios-overview/)，使模型结果可以直接呈现给最终用户。模型也可以在[系统级场景](%E5%BA%94%E7%94%A8/%E9%A1%B6%E7%82%B9/Scenarios/%E6%A6%82%E8%A7%88.md)中进行探索，使分析师能够模拟整个组织的更改。

## 优势

就像将数据集映射到Ontology概念为工作流程开发和决策提供了[优势](%E4%B8%BA%E4%BB%80%E4%B9%88%E5%88%9B%E5%BB%BAOntology%EF%BC%9F.md)一样，将模型映射到Ontology也提供了许多优势：

* **可解释性**。因为所有建模结果都用现实世界的概念（一个对象类型的属性）定义，最终用户无需理解机器学习即可使用建模结果。相反，用户只需与简单的概念如*预测*、*估计*或*分类*进行交互。
* **规模经济**。不再是每个建模项目都是为特定应用案例而创建的定制化努力，建模工作可以随着时间的推移相互借鉴。例如，为一个应用案例产生的预测可以立即用于后续的应用案例，从而减少重复工作并随着时间的推移更快地为最终用户提供价值。
* **大规模连接性**。通过整合ML模型，Ontology成为组织的单一真实来源，不仅在数据方面，而且在*逻辑*方面。模型编码了组织对未来变化的预期。通过这种方式，Ontology成为整个企业的"数字孪生"，解锁了以各种不同的建模努力无法实现的方式模拟整个组织更改的能力。
